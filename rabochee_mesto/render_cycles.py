#!/usr/bin/env python3
"""Реалистичные виды рабочего места: сцена Blender (bpy) из model.py, рендер Cycles.

python3 render_cycles.py [samples] [виды через запятую]   ->  render/vid_*.jpg
"""
import math
import os
import random
import sys

import bpy
import bmesh
import numpy as np

import model
from sheet import W, CEIL, ZN0, UD, GAP, HR

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "render")
SAMPLES = int(sys.argv[1]) if len(sys.argv) > 1 else 128
ONLY = sys.argv[2].split(",") if len(sys.argv) > 2 else None
MM = 0.001


def lin(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple((v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4) for v in c) + (1.0,)


# ---------------------------------------------------------------- сцена
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = SAMPLES
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.02
scene.cycles.use_denoising = True
scene.cycles.max_bounces = 8
scene.cycles.diffuse_bounces = 4
scene.cycles.glossy_bounces = 3
scene.cycles.caustics_reflective = False
scene.cycles.caustics_refractive = False
scene.cycles.blur_glossy = 1.0
scene.render.image_settings.file_format = "JPEG"
scene.render.image_settings.quality = 92
scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Punchy"
scene.view_settings.exposure = -0.55

world = bpy.data.worlds.new("w")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.75, 0.82, 0.95, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.15


# ---------------------------------------------------------------- материалы
def principled(name, color, rough=0.6, sheen=0.0, spec=0.5, coat=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = lin(color) if isinstance(color, str) else color
    b.inputs["Roughness"].default_value = rough
    b.inputs["Specular IOR Level"].default_value = spec
    if sheen:
        b.inputs["Sheen Weight"].default_value = sheen
        b.inputs["Sheen Roughness"].default_value = 0.4
    if coat:
        b.inputs["Coat Weight"].default_value = coat
        b.inputs["Coat Roughness"].default_value = 0.25
    return m


def add_bump(m, scale, strength, kind="noise"):
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    if kind == "noise":
        tx = nt.nodes.new("ShaderNodeTexNoise")
        tx.inputs["Scale"].default_value = scale
        tx.inputs["Detail"].default_value = 8
    else:                                                       # ворс / букле
        tx = nt.nodes.new("ShaderNodeTexVoronoi")
        tx.inputs["Scale"].default_value = scale
    nt.links.new(tc.outputs["Object"], tx.inputs["Vector"])
    bp = nt.nodes.new("ShaderNodeBump")
    bp.inputs["Strength"].default_value = strength
    nt.links.new(tx.outputs[0] if kind == "noise" else tx.outputs["Distance"], bp.inputs["Height"])
    nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
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


def parquet_image(size=2048):
    """Паркет «французская ёлочка» с волокнами, как в визуализации."""
    rnd = np.random.default_rng(7)
    y, x = np.mgrid[0:size, 0:size].astype(np.float32)
    cw, ph = size / 4, size / 16                          # ширина колонны, ширина планки
    col = np.floor(x / cw)
    xl = x - col * cw
    sgn = np.where(col % 2 == 0, 1.0, -1.0)
    v = y + sgn * xl
    row = np.floor(v / ph)
    key = (col * 1000 + row).astype(np.int64)
    tone = (np.sin(key * 12.9898) * 43758.5453) % 1.0
    base = np.stack([0.60 + 0.09 * tone, 0.48 + 0.07 * tone, 0.36 + 0.05 * tone], -1)
    along = (xl + v * 0.0) / cw
    grain = np.sin((v - row * ph) * 0.9 + np.sin(along * 7 + tone * 30) * 2.5 + tone * 50)
    grain2 = rnd.normal(0, 1, (size, size)).astype(np.float32)
    shade = 1 + 0.05 * grain + 0.02 * grain2
    seam = ((v - row * ph) < 2.5) | (xl < 2.5)
    shade = np.where(seam, 0.55, shade)
    img = np.clip(base * shade[..., None], 0, 1)
    im = bpy.data.images.new("parquet", size, size)
    rgba = np.concatenate([img, np.ones((size, size, 1), np.float32)], -1)[::-1]
    im.pixels.foreach_set(rgba.astype(np.float32).ravel())
    im.pack()
    return im


def parquet_mat():
    m = principled("parquet", (1, 1, 1, 1), rough=0.38, coat=0.2)
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = parquet_image()
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (0.65, 0.65, 1)     # планка ≈ 95 × 600 мм
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nt.links.new(mp.outputs[0], tex.inputs["Vector"])
    nt.links.new(tex.outputs["Color"], b.inputs["Base Color"])
    bw = nt.nodes.new("ShaderNodeRGBToBW")
    bp = nt.nodes.new("ShaderNodeBump")
    bp.inputs["Strength"].default_value = 0.15
    nt.links.new(tex.outputs["Color"], bw.inputs[0])
    nt.links.new(bw.outputs[0], bp.inputs["Height"])
    nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m


MAT = {
    "facade": add_bump(principled("facade", "#8E8882", rough=0.55, spec=0.45), 900, 0.02),
    "top": add_bump(principled("top", "#8E8882", rough=0.5, spec=0.45), 900, 0.02),
    "carcass": principled("carcass", "#9A948E", rough=0.7),
    "back": principled("back", "#8E8882", rough=0.8),
    "plinth": principled("plinth", "#6E6863", rough=0.8),
    "rose": add_bump(principled("rose", "#C4908C", rough=0.55), 900, 0.02),
    "rose_back": principled("rose_back", "#B5827E", rough=0.7),
    "drawer_box": principled("drawer_box", "#D8D2CB", rough=0.7),
    "box": add_bump(principled("box", "#CDC3B6", rough=0.9, sheen=0.3), 300, 0.08),
    "box2": add_bump(principled("box2", "#8A7F74", rough=0.9, sheen=0.3), 300, 0.08),
    "socket": principled("socket", "#F2F0EC", rough=0.3),
    "bed": add_bump(principled("velvet", "#C98E88", rough=0.75, sheen=1.0), 600, 0.15),
    "linen": add_bump(principled("linen", "#DCD8D3", rough=0.95, sheen=0.5), 250, 0.25),
    "pillow": add_bump(principled("pillow", "#B3ADA7", rough=0.95, sheen=0.5), 250, 0.25),
    "pillow2": add_bump(principled("pillow2", "#E6E1DB", rough=0.95, sheen=0.5), 250, 0.25),
    "handle": principled("handle", "#E2AFA6", rough=0.42),
    "wall": add_bump(principled("wall", "#958F89", rough=0.92, spec=0.3), 150, 0.03),
    "wall_light": principled("wall_light", "#E9E6E2", rough=0.9),
    "ceiling": principled("ceiling", "#F2F0ED", rough=0.95),
    "boucle": add_bump(principled("boucle", "#EEEAE3", rough=1.0, sheen=1.0), 1800, 0.6, kind="voronoi"),
    "cream": principled("cream", "#E6DCC8", rough=0.3, coat=0.4),
    "caster": principled("caster", "#2A2826", rough=0.4),
    "frame": principled("frame", "#2B2B2B", rough=0.4),
    "led": emission("led", (1.0, 0.78, 0.5, 1), 25),
    "lamp": emission("lamp", (1.0, 0.85, 0.65, 1), 3),
    "parquet": parquet_mat(),
}
for i, c in enumerate(model.BOOKS):
    MAT["book%d" % i] = principled("book%d" % i, c, rough=0.65)


# ---------------------------------------------------------------- геометрия
coll = scene.collection


def cube(name, x0, x1, y0, y1, z0, z1, mat, bevel=1.5, seg=2, parent=None):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.scale = ((x1 - x0) * MM, (y1 - y0) * MM, (z1 - z0) * MM)
    ob.location = ((x0 + x1) / 2 * MM, -(y0 + y1) / 2 * MM, (z0 + z1) / 2 * MM)   # комната в сторону −y
    coll.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    ob.select_set(False)
    if bevel:
        md = ob.modifiers.new("b", "BEVEL")
        md.width = bevel * MM
        md.segments = seg
        md.limit_method = "ANGLE"
    me.materials.append(MAT[mat])
    for p in me.polygons:
        p.use_smooth = True
    if parent:
        mw = ob.matrix_world.copy()
        ob.parent = parent
        ob.matrix_world = mw
    return ob


model.build()
pivots = {}
for gid, meta in model.groups.items():
    e = bpy.data.objects.new(gid, None)
    coll.objects.link(e)
    if meta["type"] == "hinge":
        e.location = (meta["pivot"][0] * MM, -meta["pivot"][1] * MM, 0)
    pivots[gid] = e

SOFT = {"bed": (18, 4), "linen": (35, 5), "pillow": (60, 6), "pillow2": (60, 6), "box": (6, 2), "box2": (6, 2)}
for n, b in enumerate(model.boxes):
    x0, x1, y0, y1, z0, z1, kind = b[:7]
    gid = b[7] if len(b) > 7 else None
    if kind in ("wall_back", "floor"):
        continue
    bev, seg = SOFT.get(kind, (1.5, 2))
    if kind.startswith("book"):
        bev, seg = 1, 1
    bev = min(bev, (x1 - x0) / 2.2, (y1 - y0) / 2.2, (z1 - z0) / 2.2)
    cube("%s_%d" % (kind, n), x0, x1, y0, y1, z0, z1, kind, bevel=bev, seg=seg,
         parent=pivots.get(gid))

# ручки-полукруги
for gid, x, y, z in model.handles:
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=HR * MM, depth=10 * MM)
    ob = bpy.context.active_object
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, 0, 0),
                           plane_no=(0, 1, 0), clear_outer=True)
    bmesh.ops.holes_fill(bm, edges=bm.edges[:])
    bm.to_mesh(ob.data)
    bm.free()
    ob.rotation_euler = (math.pi / 2, 0, 0)
    ob.location = (x * MM, -(y + 5) * MM, z * MM)
    md = ob.modifiers.new("b", "BEVEL")
    md.width = 1.5 * MM
    md.segments = 2
    ob.data.materials.append(MAT["handle"])
    bpy.context.view_layer.update()
    mw = ob.matrix_world.copy()
    ob.parent = pivots[gid]
    ob.matrix_world = mw

# помещение: пол, стены, потолок, окно
cube("floor", -900, 4200, -50, 4200, -30, 0, "parquet", bevel=0)
cube("wall_back", -900, 4200, -100, 0, 0, CEIL, "wall", bevel=0)
cube("wall_left", -1000, -900, 0, 4200, 0, CEIL, "wall", bevel=0)
cube("wall_right", 4200, 4300, 0, 4200, 0, CEIL, "wall", bevel=0)
cube("ceiling", -900, 4200, 0, 4200, CEIL, CEIL + 50, "ceiling", bevel=0)
cube("wall_front", -900, 4200, 4200, 4300, 0, CEIL, "wall_light", bevel=0)
# окно на правой стене: тёмная рама и дневной свет
cube("win_frame", 4180, 4200, 900, 2300, 900, 2500, "frame", bevel=0)
bpy.ops.object.light_add(type="AREA", location=(4150 * MM, -1600 * MM, 1700 * MM))
win = bpy.context.active_object
win.data.shape = "RECTANGLE"
win.data.size, win.data.size_y = 1.4, 1.6
win.data.energy = 420
win.data.color = (0.92, 0.96, 1.0)
win.rotation_euler = (0, math.pi / 2, 0)
# мягкий заполняющий свет от «комнаты» за камерой
bpy.ops.object.light_add(type="AREA", location=(1500 * MM, -3900 * MM, 2400 * MM))
fill = bpy.context.active_object
fill.data.size = 3.0
fill.data.energy = 140
fill.data.color = (1.0, 0.96, 0.9)
fill.rotation_euler = (math.radians(60), 0, 0)

# LED под нишей: светящаяся полоса + узкий площадной источник вниз
cube("led_strip", 35, W - 35, UD - 40, UD - 26, ZN0 - 6, ZN0, "led", bevel=0)
bpy.ops.object.light_add(type="AREA", location=(W / 2 * MM, -(UD - 60) * MM, (ZN0 - 8) * MM))
led = bpy.context.active_object
led.data.shape = "RECTANGLE"
led.data.size, led.data.size_y = (W - 80) * MM, 0.03
led.data.energy = 55
led.data.color = (1.0, 0.72, 0.42)

# бра у кровати
for z in (1350, 1200):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.06, depth=0.05,
                                        location=((W + 280) * MM, -0.03, z * MM), rotation=(math.pi / 2, 0, 0))
    o = bpy.context.active_object
    o.data.materials.append(MAT["lamp"])
    bpy.ops.object.light_add(type="POINT", location=((W + 280) * MM, -0.09, z * MM))
    p = bpy.context.active_object
    p.data.energy = 1.5
    p.data.color = (1, 0.8, 0.55)
    p.data.shadow_soft_size = 0.05


# кресло «букле»
def arc_ring(r, tube, z, a0, a1, cx, cy):
    cu = bpy.data.curves.new("ring", "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = tube
    cu.bevel_resolution = 6
    cu.use_fill_caps = True
    sp = cu.splines.new("NURBS")
    n = 24
    sp.points.add(n - 1)
    for i in range(n):
        a = a0 + (a1 - a0) * i / (n - 1)
        sp.points[i].co = (cx + r * math.cos(a), cy + r * math.sin(a), z, 1)
    sp.use_endpoint_u = True
    sp.order_u = 4
    ob = bpy.data.objects.new("ring", cu)
    coll.objects.link(ob)
    cu.materials.append(MAT["boucle"])
    return ob


CX, CY = 0.86, -0.64
gap = math.radians(130)                       # разрыв колец смотрит на стол (+y, к стене)
for i, z in enumerate((0.575, 0.655, 0.735)):
    arc_ring(0.205 - i * 0.004, 0.046, z, math.pi / 2 + gap / 2, math.pi / 2 + 2 * math.pi - gap / 2, CX, CY)
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.215, depth=0.075, location=(CX, CY, 0.5))
seat = bpy.context.active_object
seat.data.materials.append(MAT["boucle"])
md = seat.modifiers.new("b", "BEVEL"); md.width = 0.03; md.segments = 5
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.22, depth=0.022, location=(CX, CY, 0.452))
bpy.context.active_object.data.materials.append(MAT["cream"])
bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.022, depth=0.33, location=(CX, CY, 0.28))
bpy.context.active_object.data.materials.append(MAT["cream"])
for l in range(5):
    a = l * 2 * math.pi / 5 + 0.3
    bpy.ops.mesh.primitive_cube_add(size=1, location=(CX + math.cos(a) * 0.15, CY + math.sin(a) * 0.15, 0.09),
                                    rotation=(0, 0, a))
    leg = bpy.context.active_object
    leg.scale = (0.3, 0.04, 0.025)
    leg.data.materials.append(MAT["cream"])
    md = leg.modifiers.new("b", "BEVEL"); md.width = 0.006; md.segments = 3
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.028, location=(CX + math.cos(a) * 0.29, CY + math.sin(a) * 0.29, 0.03))
    bpy.context.active_object.data.materials.append(MAT["caster"])

# мелочи на столе: открытая книга, тетради
cube("book_open_l", 40, 230, 160, 420, 750, 758, "pillow2", bevel=2)
cube("book_open_r", 232, 420, 160, 420, 750, 758, "pillow2", bevel=2)
cube("notebook", 600, 820, 220, 380, 750, 755, "book4", bevel=1)
cube("notebook2", 640, 840, 240, 400, 755, 760, "box", bevel=1)


# ---------------------------------------------------------------- камеры и состояния
def look(cam, frm, to):
    from mathutils import Vector
    frm, to = Vector((frm[0], -frm[1], frm[2])), Vector((to[0], -to[1], to[2]))
    cam.location = frm * MM
    d = to - frm
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


cam_data = bpy.data.cameras.new("cam")
cam = bpy.data.objects.new("cam", cam_data)
coll.objects.link(cam)
scene.camera = cam


def state(doors, drawers):
    for gid, meta in model.groups.items():
        e = pivots[gid]
        if meta["type"] == "hinge":
            e.rotation_euler = (0, 0, math.radians(meta["angle"]) * doors)
        else:
            e.location = (0, -300 * MM * drawers, 0)


VIEWS = {
    "obshchiy": dict(frm=(2050, 2650, 1400), to=(560, 0, 1300), lens=22, res=(1280, 1600), st=(0, 0)),
    "speredi":  dict(frm=(685, 3700, 1380), to=(685, 0, 1330), lens=26, res=(1600, 1200), st=(0, 0)),
    "nisha":    dict(frm=(1150, 1350, 1150), to=(560, 150, 1420), lens=30, res=(1600, 1100), st=(0, 0)),
    "otkryto":  dict(frm=(1950, 2700, 1400), to=(600, 200, 1350), lens=22, res=(1280, 1600), st=(0.85, 1)),
}
os.makedirs(OUT, exist_ok=True)
for name, v in VIEWS.items():
    if ONLY and name not in ONLY:
        continue
    state(*v["st"])
    look(cam, v["frm"], v["to"])
    cam_data.lens = v["lens"]
    cam_data.sensor_width = 36
    scene.render.resolution_x, scene.render.resolution_y = v["res"]
    scene.render.filepath = os.path.join(OUT, "vid_%s.jpg" % name)
    bpy.ops.render.render(write_still=True)
    print("done", name, flush=True)
