const MAX_PARTICLES = 4000;
const AREA_PER_PARTICLE = 600;
const TRAIL_SAMPLES = 16;
const TRAIL_SECONDS = 1.1;
const LIFETIME_SECONDS = 7;
const MAX_STEP_SECONDS = 0.05;
const POINTER_POOL = 4;
const POINTER_SEED_RADIUS = 60;
const PARKED = -1e5;

const COMMON = /* wgsl */ `
struct Uniforms {
  size: vec2f,
  pointer: vec2f,
  time: f32,
  dt: f32,
  activity: f32,
  count: f32,
  line_width: f32,
  alpha: f32,
  column: f32,
  slow: vec3f,
  fast: vec3f,
}
@group(0) @binding(0) var<uniform> u: Uniforms;

const S = ${TRAIL_SAMPLES}u;
const QUANTUM: f32 = ${TRAIL_SECONDS / (TRAIL_SAMPLES - 1)};
const LIFETIME: f32 = ${LIFETIME_SECONDS};

fn pcg3d(seed: vec3u) -> vec3u {
  var v = seed * 1664525u + 1013904223u;
  v.x += v.y * v.z; v.y += v.z * v.x; v.z += v.x * v.y;
  v ^= v >> vec3u(16u);
  v.x += v.y * v.z; v.y += v.z * v.x; v.z += v.x * v.y;
  return v;
}

fn rand3(id: u32, generation: u32, salt: u32) -> vec3f {
  return vec3f(pcg3d(vec3u(id, generation, salt))) / 4294967295.0;
}

// Pool particles seed around the pointer while it moves and wait off screen otherwise.
fn pooled(id: u32) -> bool {
  return id % ${POINTER_POOL}u == 0u;
}

fn lifetime(id: u32) -> f32 {
  return LIFETIME * (0.6 + 0.8 * rand3(id, 0u, 91u).x) * select(1.0, 0.5, pooled(id));
}
`;

const STEP = /* wgsl */ `
${COMMON}
@group(0) @binding(1) var<storage, read_write> trail: array<vec2f>;
@group(0) @binding(2) var<storage, read_write> state: array<vec4f>;

const STALL_SPEED = 1.5;
const MARGIN = 40.0;
const SEED_RADIUS: f32 = ${POINTER_SEED_RADIUS};
const TAU = 6.2832;

// Stream function: its curl is the velocity, so the field is divergence free.
fn psi(p: vec2f) -> f32 {
  let q = p / 420.0;
  return 12600.0 * (
    sin(q.x + 0.21 * u.time) * cos(1.3 * q.y - 0.17 * u.time)
    + 0.5 * sin(2.1 * q.x - 1.7 * q.y + 0.23 * u.time)
    + 0.25 * cos(3.7 * q.x + 2.9 * q.y - 0.31 * u.time)
  );
}

fn velocity(p: vec2f) -> vec2f {
  let dx = psi(p + vec2f(1.0, 0.0)) - psi(p - vec2f(1.0, 0.0));
  let dy = psi(p + vec2f(0.0, 1.0)) - psi(p - vec2f(0.0, 1.0));
  return vec2f(dy, -dx) * 0.5;
}

fn rk4(p: vec2f, h: f32) -> vec2f {
  let k1 = velocity(p);
  let k2 = velocity(p + 0.5 * h * k1);
  let k3 = velocity(p + 0.5 * h * k2);
  let k4 = velocity(p + h * k3);
  return p + h * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0;
}

@compute @workgroup_size(64)
fn main(@builtin(global_invocation_id) gid: vec3u) {
  let id = gid.x;
  if (id >= u32(u.count)) { return; }
  let base = id * S;
  var st = state[id];  // age, time since last trail boundary, generation, speed
  var head = trail[base];

  var remaining = u.dt;
  for (var n = 0; n < 8 && remaining > 0.0; n++) {
    let h = min(remaining, QUANTUM - st.y);
    head = rk4(head, h);
    st.y += h;
    remaining -= h;
    if (st.y >= QUANTUM - 1e-6) {
      for (var j = S - 1u; j >= 2u; j--) { trail[base + j] = trail[base + j - 1u]; }
      trail[base + 1u] = head;
      st.y = 0.0;
    }
  }
  st.x += u.dt;
  st.w = length(velocity(head));

  let outside = any(head < vec2f(-MARGIN)) || any(head > u.size + vec2f(MARGIN));
  if (outside || st.w < STALL_SPEED || st.x > lifetime(id)) {
    st.z += 1.0;
    let generation = u32(st.z);
    if (pooled(id)) {
      let r = rand3(id, generation, 13u);
      let radius = SEED_RADIUS * sqrt(-2.0 * log(max(r.x, 1e-6)));
      let seed = u.pointer + radius * vec2f(cos(TAU * r.y), sin(TAU * r.y));
      head = select(vec2f(${PARKED}), seed, r.z < 6.0 * u.activity * u.dt);
    } else {
      for (var draw = 0u; draw < 4u; draw++) {
        head = rand3(id, generation, 7u ^ draw).xy * (u.size + vec2f(2.0 * MARGIN)) - vec2f(MARGIN);
        st.w = length(velocity(head));
        if (st.w >= STALL_SPEED) { break; }
      }
    }
    for (var j = 1u; j < S; j++) { trail[base + j] = head; }
    st.x = 0.0;
    st.y = 0.0;
  }
  trail[base] = head;
  state[id] = st;
}
`;

const DRAW = /* wgsl */ `
${COMMON}
@group(0) @binding(1) var<storage, read> trail: array<vec2f>;
@group(0) @binding(2) var<storage, read> state: array<vec4f>;

struct VOut {
  @builtin(position) position: vec4f,
  @location(0) across: f32,
  @location(1) alpha: f32,
  @location(2) color: vec3f,
}

@vertex
fn vs(@builtin(vertex_index) vi: u32, @builtin(instance_index) ii: u32) -> VOut {
  var corners = array<vec2f, 6>(
    vec2f(0.0, -1.0), vec2f(1.0, -1.0), vec2f(0.0, 1.0),
    vec2f(0.0, 1.0), vec2f(1.0, -1.0), vec2f(1.0, 1.0),
  );
  let corner = corners[vi];
  let id = ii / (S - 1u);
  let segment = ii % (S - 1u);
  let a = trail[id * S + segment];
  let b = trail[id * S + segment + 1u];
  let d = b - a;
  let dir = d / max(length(d), 1e-4);
  let half_width = 0.5 * u.line_width + 1.0;
  let p = mix(a, b, corner.x) + vec2f(-dir.y, dir.x) * corner.y * half_width;

  let st = state[id];
  let slot = f32(segment) + corner.x;
  let age = select(st.y + (slot - 1.0) * QUANTUM, 0.0, slot < 0.5);
  let tail = clamp(1.0 - age / (QUANTUM * f32(S - 1u)), 0.0, 1.0);
  let life = lifetime(id);
  let life_fade = smoothstep(0.0, life / 20.0, st.x) * (1.0 - smoothstep(0.8 * life, life, st.x));
  let column_fade = mix(0.3, 1.0, smoothstep(0.0, 140.0, abs(p.x - 0.5 * u.size.x) - u.column));
  let boost = select(1.0, 1.5, pooled(id));

  var out: VOut;
  out.position = vec4f(p / u.size * vec2f(2.0, -2.0) + vec2f(-1.0, 1.0), 0.0, 1.0);
  out.across = corner.y * half_width;
  out.alpha = tail * tail * life_fade * column_fade * boost * u.alpha;
  out.color = mix(u.slow, u.fast, clamp(st.w / 90.0, 0.0, 1.0));
  return out;
}

@fragment
fn fs(in: VOut) -> @location(0) vec4f {
  let half_width = 0.5 * u.line_width;
  let alpha = in.alpha * (1.0 - smoothstep(half_width - 0.5, half_width + 0.5, abs(in.across)));
  return vec4f(in.color * alpha, alpha);
}
`;

function hexToRgb(hex) {
  const n = parseInt(hex.trim().slice(1), 16);
  return [(n >> 16) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255];
}

async function start(canvas) {
  const adapter = await navigator.gpu?.requestAdapter({ powerPreference: 'low-power' });
  if (!adapter) return;
  const device = await adapter.requestDevice();
  const context = canvas.getContext('webgpu');
  const format = navigator.gpu.getPreferredCanvasFormat();
  context.configure({ device, format, alphaMode: 'premultiplied' });

  let width, height, count;
  const resize = () => {
    const dpr = Math.min(window.devicePixelRatio, 2);
    width = Math.max(canvas.clientWidth, 1);
    height = Math.max(canvas.clientHeight, 1);
    canvas.width = Math.round(width * dpr);
    canvas.height = Math.round(height * dpr);
    count = Math.min(MAX_PARTICLES, Math.max(300, Math.round((width * height) / AREA_PER_PARTICLE)));
  };
  resize();

  const trailData = new Float32Array(MAX_PARTICLES * TRAIL_SAMPLES * 2);
  const stateData = new Float32Array(MAX_PARTICLES * 4);
  for (let i = 0; i < MAX_PARTICLES; i++) {
    const pooled = i % POINTER_POOL === 0;
    const x = pooled ? PARKED : Math.random() * width;
    const y = pooled ? PARKED : Math.random() * height;
    for (let j = 0; j < TRAIL_SAMPLES; j++) trailData.set([x, y], (i * TRAIL_SAMPLES + j) * 2);
    stateData[i * 4] = Math.random() * LIFETIME_SECONDS * 0.6;
  }
  const storage = (data) => {
    const buffer = device.createBuffer({
      size: data.byteLength,
      usage: GPUBufferUsage.STORAGE,
      mappedAtCreation: true,
    });
    new Float32Array(buffer.getMappedRange()).set(data);
    buffer.unmap();
    return buffer;
  };
  const trailBuffer = storage(trailData);
  const stateBuffer = storage(stateData);

  const uniforms = new Float32Array(20);
  const uniformBuffer = device.createBuffer({
    size: uniforms.byteLength,
    usage: GPUBufferUsage.UNIFORM | GPUBufferUsage.COPY_DST,
  });

  const stepPipeline = device.createComputePipeline({
    layout: 'auto',
    compute: { module: device.createShaderModule({ code: STEP }) },
  });
  const drawModule = device.createShaderModule({ code: DRAW });
  const blend = { srcFactor: 'one', dstFactor: 'one-minus-src-alpha' };
  const drawPipeline = device.createRenderPipeline({
    layout: 'auto',
    vertex: { module: drawModule },
    fragment: { module: drawModule, targets: [{ format, blend: { color: blend, alpha: blend } }] },
  });
  const bind = (pipeline) =>
    device.createBindGroup({
      layout: pipeline.getBindGroupLayout(0),
      entries: [uniformBuffer, trailBuffer, stateBuffer].map((buffer, binding) => ({
        binding,
        resource: { buffer },
      })),
    });
  const stepBind = bind(stepPipeline);
  const drawBind = bind(drawPipeline);

  const readTheme = () => {
    const style = getComputedStyle(document.documentElement);
    const number = (name) => parseFloat(style.getPropertyValue(name));
    uniforms.set([number('--flow-width'), number('--flow-alpha'), number('--max-width') / 2 + 24], 8);
    uniforms.set(hexToRgb(style.getPropertyValue('--flow-slow')), 12);
    uniforms.set(hexToRgb(style.getPropertyValue('--flow-fast')), 16);
  };
  readTheme();

  const pointer = { x: PARKED, y: PARKED, activity: 0, stamp: 0 };
  let time = Math.random() * 100;

  const frame = (dt, draw = true) => {
    time += dt;
    uniforms.set([width, height, pointer.x, pointer.y, time, dt, pointer.activity, count]);
    device.queue.writeBuffer(uniformBuffer, 0, uniforms);

    const encoder = device.createCommandEncoder();
    if (dt > 0) {
      const pass = encoder.beginComputePass();
      pass.setPipeline(stepPipeline);
      pass.setBindGroup(0, stepBind);
      pass.dispatchWorkgroups(Math.ceil(count / 64));
      pass.end();
    }
    if (draw) {
      const pass = encoder.beginRenderPass({
        colorAttachments: [
          { view: context.getCurrentTexture().createView(), loadOp: 'clear', storeOp: 'store' },
        ],
      });
      pass.setPipeline(drawPipeline);
      pass.setBindGroup(0, drawBind);
      pass.draw(6, count * (TRAIL_SAMPLES - 1));
      pass.end();
    }
    device.queue.submit([encoder.finish()]);
  };

  const still = window.matchMedia('(prefers-reduced-motion: reduce)');
  let raf = 0;
  let last = 0;

  const tick = (now) => {
    const dt = Math.min(Math.max(now - last, 0) / 1000, MAX_STEP_SECONDS);
    last = now;
    pointer.activity *= Math.exp(-dt / 2);
    frame(dt);
    raf = requestAnimationFrame(tick);
  };

  // Reduced motion gets one still frame of a flow that has already developed.
  const run = () => {
    cancelAnimationFrame(raf);
    if (still.matches) {
      for (let i = 0; i < 120; i++) frame(1 / 30, false);
      frame(0);
    } else {
      last = performance.now();
      raf = requestAnimationFrame(tick);
    }
  };

  still.addEventListener('change', run);
  window.addEventListener('resize', () => {
    resize();
    frame(0);
  });
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    readTheme();
    frame(0);
  });
  window.addEventListener(
    'pointermove',
    (event) => {
      if (event.timeStamp - pointer.stamp < 250) {
        const moved = Math.hypot(event.clientX - pointer.x, event.clientY - pointer.y);
        pointer.activity = Math.min(1, pointer.activity + moved / 120);
      }
      pointer.x = event.clientX;
      pointer.y = event.clientY;
      pointer.stamp = event.timeStamp;
    },
    { passive: true },
  );
  device.lost.then(() => {
    cancelAnimationFrame(raf);
    canvas.remove();
  });

  run();
  canvas.dataset.ready = '';
}

const canvas = document.getElementById('flow');
start(canvas).catch(() => canvas.remove());
