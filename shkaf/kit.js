// Набор для «красивой» отрисовки моделей мебели на three.js (r160, UMD):
// процедурные текстуры, мягкий свет с отражениями, формы одежды/обуви/штанг.
const KIT = (() => {
  const rnd = (seed => () => ((seed = (seed * 16807) % 2147483647) - 1) / 2147483646)(12345);

  function canvasTex(size, draw, srgb = true) {
    const c = document.createElement('canvas');
    c.width = c.height = size;
    draw(c.getContext('2d'), size);
    const t = new THREE.CanvasTexture(c);
    t.wrapS = t.wrapT = THREE.RepeatWrapping;
    t.anisotropy = 8;
    if (srgb) t.colorSpace = THREE.SRGBColorSpace;
    return t;
  }

  // камень/терраццо – светлый фон с серыми вкраплениями и тонкими штрихами
  const stone = canvasTex(1024, (g, s) => {
    g.fillStyle = '#efedea'; g.fillRect(0, 0, s, s);
    for (let i = 0; i < 2600; i++) {
      const v = 120 + rnd() * 90 | 0;
      g.fillStyle = `rgba(${v},${v - 4},${v - 8},${0.25 + rnd() * 0.5})`;
      g.beginPath(); g.arc(rnd() * s, rnd() * s, 0.6 + rnd() * 1.8, 0, 7); g.fill();
    }
    g.lineCap = 'round';
    for (let i = 0; i < 260; i++) {
      const x = rnd() * s, y = rnd() * s, a = rnd() * 7, l = 6 + rnd() * 22;
      const v = 90 + rnd() * 80 | 0;
      g.strokeStyle = `rgba(${v},${v - 3},${v - 6},${0.35 + rnd() * 0.4})`;
      g.lineWidth = 0.8 + rnd() * 1.6;
      g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.cos(a) * l, y + Math.sin(a) * l); g.stroke();
    }
  });

  // паркет «ёлочка» (французская) – тёплый дуб
  const parquet = canvasTex(1024, (g, s) => {
    const cw = 512, ph = 128;
    g.fillStyle = '#7a5a3e'; g.fillRect(0, 0, s, s);
    for (let col = 0; col < s / cw; col++) {
      const x0 = col * cw, sl = col % 2 ? cw : -cw;
      for (let y = -2 * cw; y < s + 2 * cw; y += ph) {
        const k = rnd() * 22 - 11;
        g.fillStyle = `rgb(${172 + k | 0},${132 + k * 0.8 | 0},${94 + k * 0.6 | 0})`;
        g.beginPath();
        g.moveTo(x0, y); g.lineTo(x0 + cw, y + sl); g.lineTo(x0 + cw, y + sl + ph - 3); g.lineTo(x0, y + ph - 3);
        g.closePath(); g.fill();
        for (let f = 0; f < 10; f++) {                      // волокна дерева
          const t = rnd() * (ph - 8) + 3;
          g.strokeStyle = `rgba(95,62,35,${0.05 + rnd() * 0.08})`;
          g.lineWidth = 1 + rnd() * 2;
          g.beginPath(); g.moveTo(x0, y + t); g.lineTo(x0 + cw, y + sl + t); g.stroke();
        }
      }
    }
  });

  // штукатурка / окрашенная стена – едва заметный шум
  const plaster = canvasTex(512, (g, s) => {
    g.fillStyle = '#f1eeea'; g.fillRect(0, 0, s, s);
    for (let i = 0; i < 9000; i++) {
      const v = 225 + rnd() * 25 | 0;
      g.fillStyle = `rgba(${v},${v - 3},${v - 6},0.35)`;
      g.fillRect(rnd() * s, rnd() * s, 2, 2);
    }
  });

  // ЛДСП – мелкая текстура «текстиль/лён»
  const board = canvasTex(512, (g, s) => {
    g.fillStyle = '#ffffff'; g.fillRect(0, 0, s, s);
    for (let i = 0; i < s; i += 2) {
      g.fillStyle = `rgba(0,0,0,${0.015 + rnd() * 0.03})`; g.fillRect(0, i, s, 1);
      g.fillStyle = `rgba(0,0,0,${0.01 + rnd() * 0.02})`; g.fillRect(i, 0, 1, s);
    }
  });

  // ткань коробок
  const fabric = canvasTex(256, (g, s) => {
    g.fillStyle = '#ffffff'; g.fillRect(0, 0, s, s);
    for (let i = 0; i < s; i += 3) {
      g.fillStyle = 'rgba(0,0,0,0.06)'; g.fillRect(0, i, s, 1); g.fillRect(i, 0, 1, s);
    }
  });

  const MAPS = { stone, parquet, plaster, board, fabric };

  // UV в миллиметрах: текстура повторяется с шагом tile, а не растягивается по детали
  function boxUV(geo, sx, sy, sz, tile) {
    const uv = geo.attributes.uv;
    const dims = [[sz, sy], [sz, sy], [sx, sz], [sx, sz], [sx, sy], [sx, sy]];
    for (let f = 0; f < 6; f++)
      for (let k = 0; k < 4; k++) {
        const i = f * 4 + k;
        uv.setXY(i, uv.getX(i) * dims[f][0] / tile, uv.getY(i) * dims[f][1] / tile);
      }
  }

  const matCache = {};
  function material(key, spec) {
    if (matCache[key]) return matCache[key];
    let m;
    if (spec.basic) m = new THREE.MeshBasicMaterial({ color: spec.color });
    else {
      m = new THREE.MeshStandardMaterial({
        color: spec.color, roughness: spec.rough ?? 0.8, metalness: spec.metal ?? 0,
        envMapIntensity: spec.env ?? 1,
      });
      if (spec.map) m.map = MAPS[spec.map];
      if (spec.emissive) { m.emissive = new THREE.Color(spec.emissive); m.emissiveIntensity = spec.emissiveIntensity ?? 1; }
    }
    return (matCache[key] = m);
  }

  // силуэт вещи на плечиках: плечи, рукава-«крылья», чуть расширенный низ
  function garment(width, height, thick) {
    const w = width / 2, h = height;
    const sh = new THREE.Shape();
    sh.moveTo(-0.16 * w, 0);
    sh.quadraticCurveTo(0, -0.05 * w, 0.16 * w, 0);
    sh.lineTo(0.92 * w, -0.08 * w);
    sh.quadraticCurveTo(w, -0.12 * w, 0.96 * w, -0.2 * w);
    sh.lineTo(0.86 * w, -h + 0.05 * w);
    sh.quadraticCurveTo(0.86 * w, -h, 0.8 * w, -h);
    sh.lineTo(-0.8 * w, -h);
    sh.quadraticCurveTo(-0.86 * w, -h, -0.86 * w, -h + 0.05 * w);
    sh.lineTo(-0.96 * w, -0.2 * w);
    sh.quadraticCurveTo(-w, -0.12 * w, -0.92 * w, -0.08 * w);
    sh.closePath();
    const bev = Math.min(8, thick / 3);
    const geo = new THREE.ExtrudeGeometry(sh, { depth: Math.max(2, thick - 2 * bev), bevelEnabled: true,
      bevelThickness: bev, bevelSize: bev, bevelSegments: 2, curveSegments: 6 });
    geo.translate(0, h / 2, -(thick - 2 * bev) / 2);
    return geo;
  }

  // плечики: крючок + перекладина
  function hanger(width) {
    const g = new THREE.Group();
    const m = material('hanger', { color: 0x2b2826, rough: 0.4, metal: 0.3 });
    const bar = new THREE.Mesh(new THREE.CylinderGeometry(5, 5, width * 0.95, 8), m);
    bar.rotation.x = Math.PI / 2;
    const hook = new THREE.Mesh(new THREE.TorusGeometry(22, 3, 6, 12, Math.PI * 1.3), m);
    hook.position.y = 40;
    hook.rotation.y = Math.PI / 2;
    g.add(bar, hook);
    return g;
  }

  // главная функция: деталь [x0,x1,y0,y1,z0,z1] -> объект сцены
  function build(b, spec, key) {
    const [x0, x1, y0, y1, z0, z1] = b;
    const sx = x1 - x0, sy = z1 - z0, sz = y1 - y0;          // размеры в осях three (X, Y, Z)
    const pos = new THREE.Vector3((x0 + x1) / 2, (z0 + z1) / 2, (y0 + y1) / 2);
    const mat = material(key, spec);
    let obj;
    if (spec.shape === 'cloth') {
      const alongX = sx < sz;                                // толщина вещи вдоль X → штанга вдоль X
      const geo = garment(alongX ? sz : sx, sy, alongX ? sx : sz);
      if (alongX) geo.rotateY(Math.PI / 2);
      obj = new THREE.Group();
      const mesh = new THREE.Mesh(geo, mat);
      mesh.castShadow = mesh.receiveShadow = true;
      const hg = hanger(alongX ? sz : sx);
      hg.position.y = sy / 2 + 6;
      if (!alongX) hg.rotation.y = Math.PI / 2;
      obj.add(mesh, hg);
      obj.userData.mesh = mesh;
    } else if (spec.shape === 'shoe') {
      const geo = new THREE.CapsuleGeometry(0.5, 1, 4, 12);
      geo.rotateX(Math.PI / 2);
      geo.scale(sx, sy * 1.1, sz / 2);
      obj = new THREE.Mesh(geo, mat);
      pos.y -= sy * 0.05;
    } else if (spec.shape === 'rod') {
      const len = Math.max(sx, sz), r = Math.min(sx, sz, sy) / 2 + 2;
      const geo = new THREE.CylinderGeometry(r, r, len, 20);
      if (sx >= sz) geo.rotateZ(Math.PI / 2); else geo.rotateX(Math.PI / 2);
      obj = new THREE.Mesh(geo, mat);
    } else if (spec.shape === 'bar') {                        // ручка-рейлинг на двух опорах
      obj = new THREE.Group();
      const dims = [sx, sy, sz], long = dims.indexOf(Math.max(...dims));
      const rest = [0, 1, 2].filter(i => i !== long);
      const out = dims[rest[0]] >= dims[rest[1]] ? rest[0] : rest[1];     // ось «от фасада»
      const r = Math.min(dims[rest[0]], dims[rest[1]]) / 2;
      const axisRot = i => (i === 0 ? ['z', Math.PI / 2] : i === 2 ? ['x', Math.PI / 2] : null);
      const rod = new THREE.Mesh(new THREE.CylinderGeometry(r * 0.8, r * 0.8, dims[long], 16), mat);
      const ar = axisRot(long); if (ar) rod.rotation[ar[0]] = ar[1];
      rod.position.setComponent(out, dims[out] / 2 - r);
      obj.add(rod);
      for (const sgn of [-1, 1]) {
        const leg = new THREE.Mesh(new THREE.CylinderGeometry(r * 0.45, r * 0.45, dims[out], 10), mat);
        const lr = axisRot(out); if (lr) leg.rotation[lr[0]] = lr[1];
        leg.position.setComponent(long, sgn * (dims[long] / 2 - Math.min(40, dims[long] * 0.15)));
        obj.add(leg);
      }
      obj.children.forEach(c => { c.castShadow = true; });
    } else {
      const geo = new THREE.BoxGeometry(sx, sy, sz);
      if (spec.map) boxUV(geo, sx, sy, sz, spec.tile ?? 600);
      obj = new THREE.Mesh(geo, mat);
    }
    obj.position.copy(pos);
    if (obj.isMesh) { obj.castShadow = spec.shadow !== false; obj.receiveShadow = true; }
    return obj;
  }

  // свет: мягкое окружение (отражения) + основной источник с тенями
  function setup(renderer, scene) {
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.05;
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    // окружение – светлая «студия» с несколькими софтбоксами
    const env = new THREE.Scene();
    const room = new THREE.Mesh(new THREE.BoxGeometry(20, 12, 20),
      new THREE.MeshBasicMaterial({ color: 0x8f8a84, side: THREE.BackSide }));
    env.add(room);
    const panel = (w, h, x, y, z, ry, c) => {
      const p = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color: c, side: THREE.DoubleSide }));
      p.position.set(x, y, z); p.rotation.y = ry; p.lookAt(0, 0, 0);
      env.add(p);
    };
    panel(8, 4, 0, 5.5, 0, 0, 0xffffff);
    panel(6, 6, 9, 2, 3, 0, 0xfff3e2);
    panel(6, 6, -9, 2, -4, 0, 0xe8eeff);
    panel(10, 5, 0, 2, 9.5, 0, 0xffffff);
    const pm = new THREE.PMREMGenerator(renderer);
    scene.environment = pm.fromScene(env, 0.04).texture;
    pm.dispose();
    scene.add(new THREE.HemisphereLight(0xffffff, 0xb59a80, 0.35));
  }

  function sun(scene, pos, target, size) {
    const s = new THREE.DirectionalLight(0xfff6ea, 1.6);
    s.position.copy(pos);
    s.target.position.copy(target);
    s.castShadow = true;
    s.shadow.mapSize.set(2048, 2048);
    Object.assign(s.shadow.camera, { left: -size, right: size, top: size, bottom: -size, near: 100, far: 15000 });
    s.shadow.bias = -0.0004;
    s.shadow.normalBias = 2;
    s.shadow.radius = 4;
    scene.add(s, s.target);
    return s;
  }

  return { build, setup, sun, material, MAPS };
})();
