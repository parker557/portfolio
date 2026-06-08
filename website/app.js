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
  "checks": [
    "auto-pair testN with testN_ref",
    "parse JSON output",
    "convert normalized coordinates to pixels",
    "write JSON, CSV/XLSX, and rendered image"
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
        <div>
          <video class="demo-video" src="./assets/e2ee-chat-demo.mp4" controls playsinline preload="metadata"></video>
          <p class="video-caption">Compressed project clip from the E2EE Chat Network Application demo.</p>
        </div>
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

const projectDetails = {
  qwen: {
    title: "Qwen3-VL DuoImage Detector",
    body: `
      <ul>
        <li>I wanted the output to be checkable, so the script writes both machine-readable files and a rendered image.</li>
        <li>The useful engineering work is around the model call: pairing images, normalizing prompts, parsing JSON, and converting coordinates.</li>
        <li>Next improvement: add a small evaluation folder with expected boxes and failure examples.</li>
      </ul>
    `
  },
  property: {
    title: "Property Management System",
    body: `
      <ul>
        <li>This project is a practical full-stack workflow: report, store, notify, draft, respond.</li>
        <li>The AI path is intentionally visible rather than hidden behind a magic button, which makes debugging easier.</li>
        <li>Next improvement: add better audit logs and role-based permissions around issue changes.</li>
      </ul>
    `
  },
  tracking: {
    title: "RealSense + SAM 3 Tracking Prototype",
    body: `
      <ul>
        <li>The goal is not just segmentation, but structured state that another robotics component can consume.</li>
        <li>I worked around camera input, mask output, 2D/3D anchors, bounding boxes, and pose hints.</li>
        <li>Next improvement: store short clips and compare tracking stability across lighting and distance changes.</li>
      </ul>
    `
  },
  chat: {
    title: "E2EE Chat Network Application",
    body: `
      <ul>
        <li>The project helped me practice deployment-level thinking: TLS, Docker Compose, database setup, and authentication flow.</li>
        <li>I treated the security pieces as parts of a system instead of isolated checkboxes.</li>
        <li>Next improvement: add clearer threat-model notes and automated setup checks.</li>
      </ul>
    `
  },
  rentconnect: {
    title: "RentConnect Secure SaaS Platform",
    body: `
      <ul>
        <li>This is the frontend-heavy project I use to show React, Firebase, app structure, state, and UI workflows.</li>
        <li>The interesting part is connecting authentication, Firestore data, listing UI, and payment-provider wiring.</li>
        <li>Next improvement: tighten the README with screenshots for each role and setup path.</li>
      </ul>
    `
  },
  finance: {
    title: "AI Finance Advisor",
    body: `
      <ul>
        <li>This is a local AI workflow experiment, not a product and not financial advice.</li>
        <li>I used it to practice structured prompts, local files, repeatable Markdown output, and review-first AI writing.</li>
        <li>Next improvement: separate data loading, model call, and report rendering into testable modules.</li>
      </ul>
    `
  }
};

const qwenLabSamples = {
  test1: {
    ref: "./assets/qwen-test1-ref.jpg",
    search: "./assets/qwen-test1-search.jpg",
    result: "./assets/qwen-test1-result.jpg",
    count: 3,
    avgTime: "7-8s",
    json: {
      results: [
        {
          label: "target_object",
          bbox_qwen1000: [148.0, 110.0, 510.0, 420.0],
          bbox_2d: [166, 99, 573, 379]
        },
        {
          label: "target_object",
          bbox_qwen1000: [185.0, 470.0, 500.0, 830.0],
          bbox_2d: [208, 424, 562, 749]
        },
        {
          label: "target_object",
          bbox_qwen1000: [510.0, 360.0, 900.0, 650.0],
          bbox_2d: [573, 325, 1011, 587]
        }
      ]
    }
  },
  test2: {
    ref: "./assets/qwen-test2-ref.png",
    search: "./assets/qwen-test2-search.jpg",
    result: "./assets/qwen-test2-result.jpg",
    count: 4,
    avgTime: "9.5s",
    json: {
      results: [
        {
          label: "target_object",
          bbox_qwen1000: [30.0, 250.0, 350.0, 880.0],
          bbox_2d: [35, 184, 406, 649]
        },
        {
          label: "target_object",
          bbox_qwen1000: [280.0, 250.0, 500.0, 880.0],
          bbox_2d: [325, 184, 580, 649]
        },
        {
          label: "target_object",
          bbox_qwen1000: [480.0, 250.0, 780.0, 880.0],
          bbox_2d: [556, 184, 904, 649]
        },
        {
          label: "target_object",
          bbox_qwen1000: [780.0, 250.0, 990.0, 880.0],
          bbox_2d: [904, 184, 1147, 649]
        }
      ]
    }
  }
};

const demoOutput = document.getElementById("demoOutput");
const demoButtons = document.querySelectorAll("[data-demo]");
const filterButtons = document.querySelectorAll("[data-filter]");
const projectCards = document.querySelectorAll(".project-card");
const projectDetailTitle = document.getElementById("projectDetailTitle");
const projectDetailBody = document.getElementById("projectDetailBody");
const sampleSelect = document.getElementById("sampleSelect");
const refUpload = document.getElementById("refUpload");
const searchUpload = document.getElementById("searchUpload");
const labPrompt = document.getElementById("labPrompt");
const labRefImage = document.getElementById("labRefImage");
const labSearchImage = document.getElementById("labSearchImage");
const labResultImage = document.getElementById("labResultImage");
const labJsonOutput = document.getElementById("labJsonOutput");
const labDetectionCount = document.getElementById("labDetectionCount");
const labAvgTime = document.getElementById("labAvgTime");
const liveStatus = document.getElementById("liveStatus");

function setDemo(name, shouldScroll = true, shouldUpdateHash = true) {
  const demo = demos[name] || demos.qwen;
  demoOutput.innerHTML = `<h3>${demo.title}</h3>${demo.body}`;
  demoButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.demo === name && button.closest(".demo-tabs"));
  });

  if (name === "tracking") {
    const canvas = document.getElementById("demoTrackingCanvas");
    if (canvas) drawTracking(canvas, performance.now() / 1000);
  }

  if (shouldUpdateHash) {
    history.replaceState(null, "", `#demo-${name}`);
  }

  if (shouldScroll) {
    document.getElementById("demos").scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

function openProjectNote(name, shouldScroll = true) {
  const detail = projectDetails[name] || projectDetails.qwen;
  projectDetailTitle.textContent = detail.title;
  projectDetailBody.innerHTML = detail.body;
  history.replaceState(null, "", `#note-${name}`);

  if (shouldScroll) {
    document.getElementById("projectDetail").scrollIntoView({ behavior: "smooth", block: "center" });
  }
}

demoButtons.forEach((button) => {
  button.addEventListener("click", () => setDemo(button.dataset.demo));
});

document.querySelectorAll("[data-project-open]").forEach((button) => {
  button.addEventListener("click", () => openProjectNote(button.dataset.projectOpen));
});

function setProjectFilter(filterName) {
  filterButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.filter === filterName);
  });

  projectCards.forEach((card) => {
    const categories = (card.dataset.category || "").split(/\s+/);
    const shouldShow = filterName === "all" || categories.includes(filterName);
    card.classList.toggle("is-hidden", !shouldShow);
  });
}

filterButtons.forEach((button) => {
  button.addEventListener("click", () => setProjectFilter(button.dataset.filter));
});

function setLabSample(name) {
  const sample = qwenLabSamples[name] || qwenLabSamples.test1;
  labRefImage.src = sample.ref;
  labSearchImage.src = sample.search;
  labResultImage.src = sample.result;
  labDetectionCount.textContent = sample.count;
  labAvgTime.textContent = sample.avgTime;
  labJsonOutput.textContent = JSON.stringify(sample.json, null, 2);
  liveStatus.textContent = "recorded replay loaded";
}

function previewUpload(input, targetImage, fallbackResult = false) {
  const file = input.files?.[0];
  if (!file) return;
  const url = URL.createObjectURL(file);
  targetImage.src = url;
  if (fallbackResult) labResultImage.src = url;
  labDetectionCount.textContent = "preview";
  labAvgTime.textContent = "not run";
  labJsonOutput.textContent = JSON.stringify(
    {
      status: "custom image preview only",
      next_step: "connect a live VLM endpoint to run inference on uploaded images"
    },
    null,
    2
  );
  liveStatus.textContent = "custom images loaded; inference not run";
}

sampleSelect?.addEventListener("change", () => setLabSample(sampleSelect.value));

document.getElementById("runRecordedDemo")?.addEventListener("click", () => {
  setLabSample(sampleSelect?.value || "test1");
});

refUpload?.addEventListener("change", () => previewUpload(refUpload, labRefImage));
searchUpload?.addEventListener("change", () => previewUpload(searchUpload, labSearchImage, true));

document.getElementById("tryLiveInference")?.addEventListener("click", async () => {
  liveStatus.textContent = "checking endpoint...";
  const formData = new FormData();
  formData.append("sample", sampleSelect?.value || "test1");
  formData.append("prompt", labPrompt?.value || "");
  if (refUpload?.files?.[0]) formData.append("reference", refUpload.files[0]);
  if (searchUpload?.files?.[0]) formData.append("search", searchUpload.files[0]);

  try {
    const response = await fetch("/api/qwen-detect", {
      method: "POST",
      body: formData
    });
    const payload = await response.json();
    liveStatus.textContent = payload.status || "endpoint returned a response";
    renderLivePayload(payload, response.ok);
  } catch (error) {
    liveStatus.textContent = "endpoint not available on local static preview";
    labJsonOutput.textContent = JSON.stringify(
      {
        status: "live endpoint unavailable",
        message: "Deploy the Cloudflare Pages Function and add a model API key or vLLM endpoint.",
        error: error.message
      },
      null,
      2
    );
  }
});

function renderLivePayload(payload, isOk) {
  const results = payload?.parsed?.results || [];

  if (isOk && Array.isArray(results)) {
    labDetectionCount.textContent = String(results.length);
    labAvgTime.textContent = "live";
    drawLiveDetections(results);
  }

  labJsonOutput.textContent = JSON.stringify(payload.parsed || payload, null, 2);
}

function drawLiveDetections(results) {
  if (!labSearchImage || !labResultImage || !Array.isArray(results) || results.length === 0) return;

  const width = labSearchImage.naturalWidth || labSearchImage.width;
  const height = labSearchImage.naturalHeight || labSearchImage.height;
  if (!width || !height) return;

  const canvas = document.createElement("canvas");
  canvas.width = width;
  canvas.height = height;
  const ctx = canvas.getContext("2d");
  ctx.drawImage(labSearchImage, 0, 0, width, height);

  ctx.lineWidth = Math.max(3, Math.round(width / 320));
  ctx.font = `${Math.max(16, Math.round(width / 48))}px Arial, sans-serif`;

  results.forEach((result, index) => {
    const bbox = result.bbox_2d || result.bbox || result.box;
    if (!Array.isArray(bbox) || bbox.length < 4) return;

    const [x1, y1, x2, y2] = normalizeBbox(bbox, width, height);
    const label = result.label || `match ${index + 1}`;

    ctx.strokeStyle = "#2f5f98";
    ctx.fillStyle = "rgba(47, 95, 152, 0.16)";
    ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);
    ctx.fillRect(x1, y1, x2 - x1, y2 - y1);

    const text = `${index + 1}. ${label}`;
    const textWidth = ctx.measureText(text).width + 12;
    const labelY = Math.max(0, y1 - 28);
    ctx.fillStyle = "#172033";
    ctx.fillRect(x1, labelY, textWidth, 24);
    ctx.fillStyle = "#ffffff";
    ctx.fillText(text, x1 + 6, labelY + 18);
  });

  labResultImage.src = canvas.toDataURL("image/jpeg", 0.9);
}

function normalizeBbox(bbox, width, height) {
  const numbers = bbox.slice(0, 4).map(Number);
  const max = Math.max(...numbers);

  if (max <= 1) {
    return [
      numbers[0] * width,
      numbers[1] * height,
      numbers[2] * width,
      numbers[3] * height
    ];
  }

  return numbers;
}

let trackingOn = false;
let rafId = null;

function drawTracking(canvas, t = 0) {
  const ctx = canvas.getContext("2d");
  const w = canvas.width;
  const h = canvas.height;
  ctx.clearRect(0, 0, w, h);
  ctx.fillStyle = "#eef3e9";
  ctx.fillRect(0, 0, w, h);

  ctx.strokeStyle = "#d5dccd";
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

  ctx.fillStyle = "rgba(22, 111, 106, 0.18)";
  ctx.strokeStyle = "#166f6a";
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.ellipse(cx, cy, bw / 2, bh / 2, Math.sin(t) * 0.08, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  ctx.strokeStyle = "#2f5f98";
  ctx.lineWidth = 3;
  ctx.strokeRect(cx - bw / 2, cy - bh / 2, bw, bh);

  ctx.fillStyle = "#a86620";
  ctx.beginPath();
  ctx.arc(cx, cy, 6, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = "#172033";
  ctx.font = "16px Arial, sans-serif";
  ctx.fillText("mask + bbox + 2D/3D anchor", 24, 32);
  ctx.fillStyle = "#5d6676";
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

function initFromHash() {
  const hash = window.location.hash.replace("#", "");
  const demoMatch = hash.match(/^demo-(.+)$/);
  const noteMatch = hash.match(/^note-(.+)$/);

  if (demoMatch && demos[demoMatch[1]]) {
    setDemo(demoMatch[1], false, false);
    return;
  }

  setDemo("qwen", false, false);
  setProjectFilter("all");
  setLabSample("test1");

  if (noteMatch && projectDetails[noteMatch[1]]) {
    openProjectNote(noteMatch[1], false);
  } else {
    openProjectNote("qwen", false);
  }
}

drawTracking(document.getElementById("trackingCanvas"), 0.4);
initFromHash();
