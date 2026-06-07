const demos = {
  qwen: {
    title: "Qwen3-VL reference-guided detection",
    body: `
      <div class="demo-layout">
        <div class="demo-images">
          <figure><img src="./assets/qwen-ref.jpg" alt="Reference object"><figcaption>Reference object</figcaption></figure>
          <figure><img src="./assets/qwen-test.jpg" alt="Search image"><figcaption>Search image</figcaption></figure>
          <figure><img src="./assets/qwen-result.jpg" alt="Detection result"><figcaption>Rendered result</figcaption></figure>
        </div>
        <pre class="demo-log"><code>{
  "task": "find objects matching the reference image",
  "model": "Qwen3-VL-8B-Instruct",
  "steps": [
    "auto-pair testN with testN_ref",
    "construct VLM prompt",
    "parse JSON output",
    "convert normalized coordinates to pixels",
    "save rendered image, JSON, CSV/XLSX"
  ]
}</code></pre>
      </div>
    `
  },
  property: {
    title: "Property management agent workflow",
    body: `
      <div class="demo-layout">
        <ol class="step-list">
          <li><strong>Owner report</strong><br>Tenant reports a leaking pipe with priority and unit details.</li>
          <li><strong>Server route</strong><br>Express stores the issue and opens a Socket.IO update path.</li>
          <li><strong>AI draft</strong><br>OpenAI-compatible request drafts a staff-facing response.</li>
          <li><strong>Staff action</strong><br>Staff dashboard receives the issue, chat thread, and suggested next step.</li>
        </ol>
        <div>
          <h3>What this shows</h3>
          <p>Full-stack flow, session login, dashboards, chat, and an AI-assist path that can be inspected rather than treated as a black box.</p>
          <div class="metrics">
            <div><strong>2</strong><span>dashboards</span></div>
            <div><strong>3</strong><span>user roles tested</span></div>
            <div><strong>API</strong><span>AI draft path</span></div>
          </div>
        </div>
      </div>
    `
  },
  tracking: {
    title: "RealSense + SAM 3 tracking workflow",
    body: `
      <div class="demo-layout">
        <canvas class="tracking-canvas" id="demoTrackingCanvas" width="720" height="360" aria-label="Tracking simulation canvas"></canvas>
        <div>
          <h3>Structured perception output</h3>
          <p>The prototype combines color/depth input with mask tracking, then exports bbox, 2D/3D anchor points, pose cues, and object-state fields for robotics demos.</p>
          <pre class="demo-log"><code>{
  "bbox": [244, 96, 418, 231],
  "anchor_2d": [331, 166],
  "depth_m": 1.42,
  "state": "tracked",
  "pose_hint": "front-left reachable"
}</code></pre>
        </div>
      </div>
    `
  },
  chat: {
    title: "Secure chat design",
    body: `
      <div class="demo-layout">
        <ol class="step-list">
          <li><strong>Login</strong><br>Flask route validates user credentials and session state.</li>
          <li><strong>MFA</strong><br>OTP flow adds a second check before sensitive chat access.</li>
          <li><strong>TLS</strong><br>Nginx and certificates protect the deployed transport layer.</li>
          <li><strong>E2EE design</strong><br>Messages follow an encryption-first design with database-backed delivery.</li>
        </ol>
        <pre class="demo-log"><code>client -> TLS -> Flask app -> MySQL
OTP verified: true
message status: encrypted payload queued
docker-compose services: webapp, db, nginx</code></pre>
      </div>
    `
  },
  rentconnect: {
    title: "RentConnect secure SaaS flow",
    body: `
      <div class="demo-layout">
        <figure class="demo-images">
          <img src="./assets/rentconnect-showcase.png" alt="RentConnect showcase screen">
        </figure>
        <div>
          <h3>React and Firebase app structure</h3>
          <p>The project combines authentication, Firestore-backed data, Material UI components, Redux state, and payment integration wiring for a real-estate workflow.</p>
          <div class="metrics">
            <div><strong>React</strong><span>frontend</span></div>
            <div><strong>Firebase</strong><span>auth/data</span></div>
            <div><strong>AES</strong><span>security concept</span></div>
          </div>
        </div>
      </div>
    `
  },
  finance: {
    title: "AI report workflow",
    body: `
      <div class="demo-layout">
        <ol class="step-list">
          <li><strong>Local input</strong><br>Read configuration, history, and user-provided financial context.</li>
          <li><strong>LLM call</strong><br>Call a model API to generate a structured Markdown report.</li>
          <li><strong>Review step</strong><br>Keep the workflow local and treat output as a draft, not financial advice.</li>
        </ol>
        <pre class="demo-log"><code># Report skeleton
- context summary
- risk notes
- action checklist
- daily/monthly Markdown output
- manual review before use</code></pre>
      </div>
    `
  }
};

const demoOutput = document.getElementById("demoOutput");
const demoButtons = document.querySelectorAll("[data-demo]");

function setDemo(name, shouldScroll = true) {
  const demo = demos[name] || demos.qwen;
  demoOutput.innerHTML = `<h3>${demo.title}</h3>${demo.body}`;
  demoButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.demo === name && button.closest(".demo-tabs"));
  });
  if (name === "tracking") {
    const canvas = document.getElementById("demoTrackingCanvas");
    if (canvas) drawTracking(canvas, performance.now() / 1000);
  }
  if (shouldScroll) {
    document.getElementById("demos").scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

demoButtons.forEach((button) => {
  button.addEventListener("click", () => setDemo(button.dataset.demo));
});

let trackingOn = false;
let rafId = null;

function drawTracking(canvas, t = 0) {
  const ctx = canvas.getContext("2d");
  const w = canvas.width;
  const h = canvas.height;
  ctx.clearRect(0, 0, w, h);
  ctx.fillStyle = "#eef3f8";
  ctx.fillRect(0, 0, w, h);

  ctx.strokeStyle = "#d5dde8";
  ctx.lineWidth = 1;
  for (let x = 40; x < w; x += 52) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, h);
    ctx.stroke();
  }
  for (let y = 38; y < h; y += 42) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(w, y);
    ctx.stroke();
  }

  const cx = w * 0.5 + Math.sin(t * 1.4) * 96;
  const cy = h * 0.5 + Math.cos(t * 1.1) * 38;
  const bw = 180;
  const bh = 96;

  ctx.fillStyle = "rgba(19, 124, 120, 0.18)";
  ctx.strokeStyle = "#137c78";
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.ellipse(cx, cy, bw / 2, bh / 2, Math.sin(t) * 0.08, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  ctx.strokeStyle = "#315d9f";
  ctx.lineWidth = 3;
  ctx.strokeRect(cx - bw / 2, cy - bh / 2, bw, bh);

  ctx.fillStyle = "#b67318";
  ctx.beginPath();
  ctx.arc(cx, cy, 6, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = "#172033";
  ctx.font = "16px system-ui, sans-serif";
  ctx.fillText("mask + bbox + 2D/3D anchor", 24, 32);
  ctx.fillStyle = "#5c687a";
  ctx.fillText(`anchor: [${Math.round(cx)}, ${Math.round(cy)}]  depth: ${(1.2 + Math.sin(t) * 0.2).toFixed(2)}m`, 24, h - 24);
}

function animateTracking() {
  const canvases = [
    document.getElementById("trackingCanvas"),
    document.getElementById("demoTrackingCanvas")
  ].filter(Boolean);
  const t = performance.now() / 1000;
  canvases.forEach((canvas) => drawTracking(canvas, t));
  if (trackingOn) rafId = requestAnimationFrame(animateTracking);
}

document.getElementById("toggleTracking")?.addEventListener("click", () => {
  trackingOn = !trackingOn;
  if (trackingOn) {
    animateTracking();
  } else if (rafId) {
    cancelAnimationFrame(rafId);
  }
});

drawTracking(document.getElementById("trackingCanvas"), 0.4);
setDemo("qwen", false);
