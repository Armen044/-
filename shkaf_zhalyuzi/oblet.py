#!/usr/bin/env python3
"""Облёт шкафа с жалюзийными фасадами (прихожая): сцена Blender, анимация дверей и ящиков, рендер Cycles.

python3 oblet.py [samples] [кадры: all | 1,60,120 | test]  -> frames/####.png
Размеры оценены по фото (заказчик их не указывал): шкаф 1500 × 600 × 2350 мм.
"""
import math
import os
import sys

import bpy
import bmesh
from mathutils import Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLES = int(sys.argv[1]) if len(sys.argv) > 1 else 24
FRAMES = sys.argv[2] if len(sys.argv) > 2 else "all"
MM = 0.001
FPS, END = 24, 264                       # 11 секунд
W, D, H, PL = 1500, 600, 2350, 100       # ширина, глубина с фасадом, высота, цоколь
CD = D - 20                              # корпус


def lin(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple((v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4) for v in c) + (1.0,)


bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = SAMPLES
sc.cycles.use_adaptive_sampling = True
sc.cycles.adaptive_threshold = 0.03
sc.cycles.use_denoising = True
sc.cycles.max_bounces = 6
sc.cycles.diffuse_bounces = 3
sc.cycles.glossy_bounces = 2
sc.cycles.caustics_reflective = sc.cycles.caustics_refractive = False
sc.render.use_persistent_data = True
sc.render.resolution_x, sc.render.resolution_y = 720, 1280
sc.render.fps = FPS
sc.frame_start, sc.frame_end = 1, END
sc.render.image_settings.file_format = "PNG"
sc.view_settings.view_transform = "AgX"
sc.view_settings.look = "AgX - Medium High Contrast"
sc.view_settings.exposure = -0.6
world = bpy.data.worlds.new("w")
sc.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.8, 0.8, 0.82, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.05
coll = sc.collection


# ---------------------------------------------------------------- материалы
def mat(name, color, rough=0.5, metal=0.0, spec=0.5):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = lin(color)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Specular IOR Level"].default_value = spec
    return m


def stone(name, base, vein, rough, tiles=False):
    """Мрамор/керамогранит: тёмная основа, тонкие прожилки, при tiles — швы плитки 600×1200."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = rough
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 1.6
    nz.inputs["Detail"].default_value = 12
    nz.inputs["Distortion"].default_value = 3.5
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    rp = nt.nodes.new("ShaderNodeValToRGB")          # узкая полоса -> прожилка
    el = rp.color_ramp.elements
    el[0].position, el[0].color = 0.485, (0, 0, 0, 1)
    el[1].position, el[1].color = 0.5, (1, 1, 1, 1)
    e2 = el.new(0.515)
    e2.color = (0, 0, 0, 1)
    nt.links.new(nz.outputs["Fac"], rp.inputs["Fac"])
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.inputs[6].default_value = lin(base)
    mix.inputs[7].default_value = lin(vein)
    nt.links.new(rp.outputs["Color"], mix.inputs[0])
    col = mix.outputs[2]
    if tiles:
        br = nt.nodes.new("ShaderNodeTexBrick")
        br.inputs["Scale"].default_value = 1.0
        br.inputs["Mortar Size"].default_value = 0.0025
        br.inputs["Brick Width"].default_value = 1.2
        br.inputs["Row Height"].default_value = 0.6
        br.offset = 0.0
        br.inputs["Color1"].default_value = br.inputs["Color2"].default_value = (1, 1, 1, 1)
        br.inputs["Mortar"].default_value = (0.35, 0.35, 0.35, 1)
        nt.links.new(tc.outputs["Object"], br.inputs["Vector"])
        mul = nt.nodes.new("ShaderNodeMix")
        mul.data_type = "RGBA"
        mul.blend_type = "MULTIPLY"
        mul.inputs[0].default_value = 1
        nt.links.new(col, mul.inputs[6])
        nt.links.new(br.outputs["Color"], mul.inputs[7])
        col = mul.outputs[2]
    nt.links.new(col, b.inputs["Base Color"])
    return m


def emission(name, color, strength):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Color"].default_value = color
    e.inputs["Strength"].default_value = strength
    o = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(e.outputs[0], o.inputs[0])
    return m


M = {
    "front": mat("front", "#F2F2F0", 0.42),
    "carcass": mat("carcass", "#F4F4F2", 0.55),
    "wall": mat("wall", "#ECECEA", 0.85, spec=0.3),
    "ceiling": mat("ceiling", "#1C1D1F", 0.7),
    "black": mat("black", "#141414", 0.32, metal=0.6),
    "base": mat("base", "#2E3033", 0.5),
    "floor": stone("floor", "#3B3E41", "#5E6164", 0.22, tiles=True),
    "marble": stone("marble", "#0B0B0C", "#9A9A9A", 0.06),
    "led": emission("led", (1.0, 0.93, 0.82, 1), 30),
}


# ---------------------------------------------------------------- геометрия
def box(name, x0, x1, y0, y1, z0, z1, m, bevel=1.2, parent=None):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=((x1 - x0) * MM, (y1 - y0) * MM, (z1 - z0) * MM), verts=bm.verts)
    bmesh.ops.translate(bm, vec=((x0 + x1) / 2 * MM, (y0 + y1) / 2 * MM, (z0 + z1) / 2 * MM), verts=bm.verts)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    if bevel:
        md = ob.modifiers.new("b", "BEVEL")
        md.width = bevel * MM
        md.segments = 2
        md.limit_method = "ANGLE"
    for p in me.polygons:
        p.use_smooth = True
    me.materials.append(M[m])
    if parent:                                      # геометрия задана в мировых координатах
        ob.parent = parent
        ob.matrix_parent_inverse = Matrix.Translation(-parent.location)
    return ob


def empty(name, x=0, y=0, z=0):
    e = bpy.data.objects.new(name, None)
    e.location = (x * MM, y * MM, z * MM)
    coll.objects.link(e)
    return e


def slats(name, x0, x1, z0, z1, parent):
    """Ряд наклонных ламелей жалюзи: одна ламель + модификатор «Массив»."""
    step, hh, tt = 26, 30, 8
    n = int((z1 - z0) / step)
    ob = box(name, x0, x1, -tt / 2, tt / 2, -hh / 2, hh / 2, "front", bevel=1.5)
    for v in ob.data.vertices:                      # ламель стоит в начале ряда, повёрнута на 30°
        y, z = v.co.y, v.co.z
        a = math.radians(30)
        v.co.y, v.co.z = y * math.cos(a) - z * math.sin(a) - 0.590, y * math.sin(a) + z * math.cos(a) + (z0 + step / 2) * MM
    arr = ob.modifiers.new("arr", "ARRAY")
    arr.count = n
    arr.use_relative_offset = False
    arr.use_constant_offset = True
    arr.constant_offset_displace = (0, 0, step * MM)
    ob.modifiers.move(ob.modifiers.find("arr"), 0)
    ob.parent = parent
    ob.matrix_parent_inverse = Matrix.Translation(-parent.location)


def handle(x, zc, parent, L=480):
    z0, z1 = zc - L / 2, zc + L / 2
    box("h_bar", x - 6, x + 6, -D - 34, -D - 22, z0, z1, "black", 2, parent)
    for z in (z0 + 25, z1 - 25):
        box("h_leg", x - 5, x + 5, -D - 22, -D, z - 5, z + 5, "black", 1, parent)


def door(i, x0, x1, hinge_x, angle):
    piv = empty(f"door{i}", hinge_x, -CD, 0)
    zb, zt = PL + 3, H - 3
    y0, y1 = -D, -CD
    mid = zb + 0.36 * (zt - zb)
    box("st", x0, x0 + 70, y0, y1, zb, zt, "front", 1.5, piv)
    box("st", x1 - 70, x1, y0, y1, zb, zt, "front", 1.5, piv)
    box("rl", x0 + 70, x1 - 70, y0, y1, zt - 70, zt, "front", 1.5, piv)
    box("rl", x0 + 70, x1 - 70, y0, y1, zb, zb + 70, "front", 1.5, piv)
    box("rl", x0 + 70, x1 - 70, y0, y1, mid - 45, mid + 45, "front", 1.5, piv)
    box("back", x0 + 70, x1 - 70, y1 - 5, y1, zb + 70, zt - 70, "front", 0, piv)
    slats("sl", x0 + 70, x1 - 70, zb + 70, mid - 45, piv)
    slats("sl", x0 + 70, x1 - 70, mid + 45, zt - 70, piv)
    hx = x1 - 45 if angle < 0 else x0 + 45
    handle(hx, 1080, piv)
    piv["open"] = angle
    return piv


# корпус
for x in (0, 492, 1484):
    box("side", x, x + 16, -CD, 0, PL, H, "carcass")
for z in (PL, H - 16):
    box("tb", 0, W, -CD, 0, z, z + 16, "carcass")
box("back", 0, W, -4, 0, PL, H, "carcass", 0)
box("plinth", 10, W - 10, -CD + 60, -CD + 76, 0, PL, "base", 1)
# левый отсек (за дверью электрощит — дверь не открываем): полки
for z in (330, 560, 780):
    box("sh", 16, 492, -CD + 2, -4, z, z + 16, "carcass")
# двустворчатый отсек: вертикальная стойка посередине
box("mid", 992, 1008, -CD + 2, -4, PL + 16, H - 16, "carcass")
for z in (1830, 430):                                  # левая половина: полка сверху, полка снизу
    box("sh", 508, 992, -CD + 2, -4, z, z + 16, "carcass")
for k in range(7):                                     # крючки под полкой
    x = 540 + k * 66
    box("hook", x - 5, x + 5, -30, -4, 1745, 1800, "black", 1)
    box("hook", x - 5, x + 5, -48, -30, 1745, 1757, "black", 1)
for z in (1830, 1500, 1220, 600, 400):                 # правая половина: полки
    box("sh", 1008, 1484, -CD + 2, -4, z, z + 16, "carcass")
drawers = []
for k, z in enumerate((1120, 950, 780)):               # 3 ящика сверху вниз
    e = empty(f"drawer{k}")
    box("df", 1012, 1480, -CD + 2, -CD + 20, z - 162, z - 4, "carcass", 1.5, e)
    box("ds", 1030, 1462, -CD + 20, -40, z - 150, z - 140, "carcass", 1, e)
    box("ds", 1030, 1042, -CD + 20, -40, z - 150, z - 40, "carcass", 1, e)
    box("ds", 1450, 1462, -CD + 20, -40, z - 150, z - 40, "carcass", 1, e)
    box("ds", 1030, 1462, -52, -40, z - 150, z - 40, "carcass", 1, e)
    drawers.append(e)
doors = [door(0, 2, 498, 0, -100), door(1, 502, 998, 500, -100), door(2, 1002, 1498, 1500, 100)]

# панель с крючками справа
box("panel", 1520, 1960, -18, 0, 120, H, "front", 1.5)
for row, z, n in ((0, 1700, 4), (1, 1120, 3)):
    for k in range(n):
        x = 1600 + k * (280 / (n - 1))
        box("hook", x - 6, x + 6, -40, -18, z, z + 45, "black", 1)
        box("hook", x - 6, x + 6, -58, -40, z, z + 12, "black", 1)

# помещение
box("floor", -2500, 4500, -6000, 200, -20, 0, "floor", 0)
box("wall_back", -2500, 4500, 0, 100, 0, 2800, "wall", 0)
box("wall_left", -1000, -900, -6000, 0, 0, 2800, "wall", 0)
box("column", 1980, 2580, -700, 0, 0, 2800, "marble", 2)
box("plinth_wall", -900, 0, -12, 0, 0, 70, "base", 0)
box("plinth_wall", 1960, 1980, -12, 0, 0, 70, "base", 0)
box("ceiling", -2500, 4500, -6000, -260, 2650, 2700, "ceiling", 0)
box("ceil_up", -2500, 4500, -260, 0, 2800, 2850, "wall", 0)
box("led", -900, 1980, -262, -252, 2640, 2652, "led", 0)

# свет: подсветка карниза, общий мягкий свет, точечный светильник
bpy.ops.object.light_add(type="AREA", location=(0.55, -0.20, 2.72))
cove = bpy.context.active_object
cove.data.shape = "RECTANGLE"
cove.data.size, cove.data.size_y = 3.0, 0.08
cove.data.energy = 380
cove.data.color = (1.0, 0.92, 0.8)
cove.rotation_euler = (math.radians(-35), 0, 0)
bpy.ops.object.light_add(type="AREA", location=(0.8, -3.4, 2.4))
fill = bpy.context.active_object
fill.data.size = 3.0
fill.data.energy = 260
fill.data.color = (1.0, 0.97, 0.93)
fill.rotation_euler = (math.radians(70), 0, 0)
bpy.ops.object.light_add(type="SPOT", location=(0.75, -1.1, 2.64))
spot = bpy.context.active_object
spot.data.energy = 140
spot.data.spot_size = math.radians(70)
spot.data.spot_blend = 0.8
spot.data.shadow_soft_size = 0.05

# ---------------------------------------------------------------- анимация
cam_data = bpy.data.cameras.new("cam")
cam_data.lens = 24
cam_data.sensor_width = 36
cam = bpy.data.objects.new("cam", cam_data)
coll.objects.link(cam)
sc.camera = cam
tgt = empty("target")
con = cam.constraints.new("TRACK_TO")
con.target = tgt
con.track_axis = "TRACK_NEGATIVE_Z"
con.up_axis = "UP_Y"


def key(ob, path, frame, value):
    setattr(ob, path, value)
    ob.keyframe_insert(data_path=path, frame=frame)


# камера: (кадр, позиция мм, цель мм)
CAM = [(1, (-650, -2900, 1500), (700, -300, 1300)),
       (72, (650, -3000, 1450), (750, -300, 1250)),
       (130, (850, -2550, 1400), (980, -300, 1200)),
       (200, (1100, -2250, 1350), (1000, -250, 1150)),
       (264, (300, -2750, 1450), (850, -300, 1250))]
for f, p, t in CAM:
    key(cam, "location", f, tuple(v * MM for v in p))
    key(tgt, "location", f, tuple(v * MM for v in t))
for d in doors[1:]:                                   # открываются двери двустворчатого отсека
    key(d, "rotation_euler", 1, (0, 0, 0))
    key(d, "rotation_euler", 76, (0, 0, 0))
    key(d, "rotation_euler", 124, (0, 0, math.radians(d["open"])))
for k, e in enumerate(drawers):                       # ящики выезжают по очереди и остаются открытыми
    s = 136 + k * 12
    key(e, "location", 1, (0, 0, 0))
    key(e, "location", s, (0, 0, 0))
    key(e, "location", s + 26, (0, -0.33, 0))
for ob in bpy.data.objects:                           # плавные ускорения/замедления
    if ob.animation_data and ob.animation_data.action:
        try:
            for fc in ob.animation_data.action.fcurves:
                for kp in fc.keyframe_points:
                    kp.interpolation = "BEZIER"
                    kp.easing = "EASE_IN_OUT"
        except AttributeError:
            pass

out = os.path.join(HERE, "frames")
os.makedirs(out, exist_ok=True)
if FRAMES == "all":
    sc.render.filepath = os.path.join(out, "")
    bpy.ops.render.render(animation=True)
else:
    for f in [int(x) for x in FRAMES.split(",")]:
        sc.frame_set(f)
        sc.render.filepath = os.path.join(out, f"test_{f:04d}.png")
        bpy.ops.render.render(write_still=True)
        print("done", f, flush=True)
