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
        <figure class="demo-capture">
          <img src="./assets/project-captures/property-staff-dashboard.png" alt="Property Management System staff dashboard screenshot">
          <figcaption>Staff dashboard after local login test</figcaption>
        </figure>
        <div>
          <h3>What this shows</h3>
          <p>Full-stack flow, session login, owner/staff dashboards, chat, and an AI-assist route that can be inspected instead of treated as a black box.</p>
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
        <figure class="demo-capture">
          <img src="./assets/project-captures/rentconnect-home.png" alt="RentConnect running React homepage">
          <figcaption>React app running locally on port 3001</figcaption>
        </figure>
        <div>
          <h3>React and Firebase app structure</h3>
          <p>The project combines authentication, Firestore-backed data, Material UI components, Redux state, and payment integration wiring for a real-estate SaaS workflow.</p>
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
        <figure class="demo-capture">
          <img src="./assets/project-captures/finance-terminal.png" alt="AI Finance Advisor terminal workflow screenshot">
          <figcaption>Terminal-style evidence for local report workflow</figcaption>
        </figure>
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
        <li>I started the Express server locally and tested owner/staff login paths before adding screenshots to this site.</li>
        <li>The project has session-backed dashboards, repair requests, notices, Socket.IO chat, and an OpenAI-compatible AI response route.</li>
        <li>Next improvement: replace mock data with a small database and add audit logs around issue changes.</li>
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
        <li>The project uses Docker Compose with Nginx, Flask, MySQL, TLS certificate files, init SQL, and OTP setup assets.</li>
        <li>I kept the video demo on the site because this project depends on local certificate/host setup and is not a simple static preview.</li>
        <li>Next improvement: add a clean threat-model note and a one-command health check for the service stack.</li>
      </ul>
    `
  },
  rentconnect: {
    title: "RentConnect Secure SaaS Platform",
    body: `
      <ul>
        <li>I installed the React dependencies with legacy peer handling and restored a missing image asset so the app could compile for screenshots.</li>
        <li>The useful part is the web app structure: React routes, Firebase config, Material UI, listing/search UI, and payment wiring.</li>
        <li>Next improvement: modernize old CRA dependencies and clean up ESLint warnings before treating it as production-ready.</li>
      </ul>
    `
  },
  finance: {
    title: "AI Finance Advisor",
    body: `
      <ul>
        <li>This is a local AI workflow experiment, not a product and not financial advice.</li>
        <li>The project stores configuration and history locally, calls an LLM when an API key is configured, and writes Markdown reports.</li>
        <li>Next improvement: separate data loading, model call, and report rendering into testable modules with safer sample data.</li>
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

const labModes = {
  qwen: {
    type: "qwen",
    intro: "Reference-guided detection with recorded samples and an optional live Qwen3-VL call.",
    sampleLabel: "Recorded sample",
    promptLabel: "Prompt",
    primaryText: "Run recorded replay",
    secondaryText: "Try live endpoint",
    help: "Click Try live endpoint to call the server-side Qwen/VLM function.",
    options: [
      { value: "test1", label: "Mouse objects, 3 detections" },
      { value: "test2", label: "Standee objects, 4 detections" }
    ]
  },
  property: {
    type: "deepseek",
    endpointMode: "property",
    linkedDemo: "property",
    intro: "Triage a property-management request and produce a short staff-facing draft.",
    sampleLabel: "Workflow sample",
    promptLabel: "Tenant / staff context",
    primaryText: "Run workflow replay",
    secondaryText: "Try DeepSeek endpoint",
    help: "DeepSeek can draft the triage note through a server-side Pages Function.",
    options: [
      {
        value: "leak_triage",
        label: "Leak request triage",
        prompt:
          "Tenant says water is leaking from the bathroom ceiling after 10pm. The owner dashboard needs a short priority note, a staff reply, and next actions. Keep it concise and operational.",
        images: {
          ref: "./assets/project-captures/property-login.png",
          search: "./assets/project-captures/property-staff-dashboard.png",
          result: "./assets/project-captures/property-owner-dashboard.png"
        },
        captions: ["Login/session flow", "Staff dashboard", "Owner dashboard"],
        metrics: ["3", "roles touched", "AI", "triage draft", "JSON", "handoff note"],
        replay: {
          priority: "urgent",
          issue_type: "water leak",
          staff_reply:
            "I logged this as urgent because there may be active water damage. Please share a photo and confirm whether the leak is still running.",
          next_actions: ["open repair request", "notify owner", "assign maintenance", "track follow-up"]
        }
      },
      {
        value: "notice_summary",
        label: "Resident notice summary",
        prompt:
          "Summarize a property notice for residents: elevator maintenance on Friday 9am-1pm, service team on site, access to floors may be delayed. Keep it clear and polite.",
        images: {
          ref: "./assets/project-captures/property-owner-dashboard.png",
          search: "./assets/project-captures/property-staff-dashboard.png",
          result: "./assets/project-captures/property-terminal.png"
        },
        captions: ["Owner view", "Staff view", "Server output"],
        metrics: ["2", "dashboards", "Notice", "summary", "Review", "before sending"],
        replay: {
          notice:
            "Elevator maintenance is scheduled for Friday from 9:00am to 1:00pm. A service team will be on site, and access between floors may be delayed during that window.",
          tone: "clear, polite, operational",
          review_required: true
        }
      }
    ]
  },
  finance: {
    type: "deepseek",
    endpointMode: "finance",
    linkedDemo: "finance",
    intro: "Generate a review-first financial report draft from a small sample profile.",
    sampleLabel: "Report sample",
    promptLabel: "Profile / report request",
    primaryText: "Run report replay",
    secondaryText: "Try DeepSeek endpoint",
    help: "This is a draft-writing demo only, not financial advice.",
    options: [
      {
        value: "cashflow_review",
        label: "Cashflow review draft",
        prompt:
          "Create a cautious financial report draft for a new graduate tracking rent, phone bill, food, transit, and emergency savings. Do not give investment advice. Do not invent prices or dollar amounts; use placeholders and questions to verify.",
        images: {
          ref: "./assets/project-captures/finance-terminal.png",
          search: "./assets/project-captures/finance-terminal.png",
          result: "./assets/project-captures/finance-terminal.png"
        },
        captions: ["Local workflow", "Report script", "Terminal evidence"],
        metrics: ["Draft", "review first", "0", "advice claims", "MD", "report output"],
        replay: {
          scope: "budget and cashflow draft",
          not_financial_advice: true,
          sections: ["context summary", "monthly cost checklist", "risk notes", "questions to verify"],
          next_step: "review numbers manually before using the report"
        }
      },
      {
        value: "job_budget",
        label: "Relocation budget draft",
        prompt:
          "Draft a relocation budget checklist for moving to Toronto for a first software role. Include rent deposit, phone, transport, food, laptop/cloud costs, and emergency buffer. No investment advice and no invented dollar amounts.",
        images: {
          ref: "./assets/project-captures/finance-terminal.png",
          search: "./assets/project-captures/property-owner-dashboard.png",
          result: "./assets/project-captures/rentconnect-home.png"
        },
        captions: ["Finance workflow", "Housing context", "Rental UI context"],
        metrics: ["Budget", "checklist", "Toronto", "relocation", "Manual", "review"],
        replay: {
          checklist: ["first month rent", "deposit", "phone plan", "transit", "food", "cloud/tool costs"],
          buffer_note: "keep a separate emergency buffer before taking on new recurring costs",
          review_required: true
        }
      }
    ]
  },
  tracking: {
    type: "static",
    linkedDemo: "tracking",
    intro: "Replay a structured perception state instead of only showing a mask on screen.",
    sampleLabel: "Tracking sample",
    promptLabel: "Object-state request",
    primaryText: "Run state replay",
    secondaryText: "Open preview panel",
    help: "This is a local replay of the tracking state shape; no camera is connected on the static site.",
    options: [
      {
        value: "mask_state",
        label: "Mask + bbox + anchor state",
        prompt:
          "Given color/depth input and a SAM mask, output bbox, 2D anchor, depth estimate, state, and a simple pose hint for a robotics demo.",
        images: {
          ref: () => makeTrackingFrame(0.2),
          search: () => makeTrackingFrame(1.4),
          result: () => makeTrackingFrame(2.6)
        },
        captions: ["Frame t0", "Frame t1", "Tracked state"],
        metrics: ["1", "tracked object", "1.42m", "depth cue", "JSON", "state"],
        replay: {
          bbox: [244, 96, 418, 231],
          anchor_2d: [331, 166],
          depth_m: 1.42,
          state: "tracked",
          pose_hint: "front-left reachable"
        }
      }
    ]
  },
  chat: {
    type: "static",
    linkedDemo: "chat",
    intro: "Show the secure-chat service shape: TLS, Flask, MySQL, OTP, and encrypted payload handling.",
    sampleLabel: "Security sample",
    promptLabel: "Flow to inspect",
    primaryText: "Run flow replay",
    secondaryText: "Open preview panel",
    help: "The full project depends on local certificates and Docker Compose, so this site shows the inspected flow.",
    options: [
      {
        value: "message_flow",
        label: "Encrypted message flow",
        prompt:
          "Trace a secure message from client login through OTP verification, TLS/Nginx, Flask, MySQL, and encrypted payload handling.",
        images: {
          ref: "./assets/project-captures/e2ee-terminal.png",
          search: "./assets/project-captures/e2ee-terminal.png",
          result: "./assets/project-captures/e2ee-terminal.png"
        },
        captions: ["Docker stack", "TLS/Nginx path", "Service evidence"],
        metrics: ["4", "services", "OTP", "login check", "TLS", "transport"],
        replay: {
          services: ["nginx", "flask webapp", "mysql", "otp setup"],
          message_status: "encrypted payload queued",
          deployment_note: "requires local hosts/certificate setup before running cleanly"
        }
      }
    ]
  },
  rentconnect: {
    type: "static",
    linkedDemo: "rentconnect",
    intro: "Replay the web-app structure behind the rental SaaS prototype.",
    sampleLabel: "SaaS sample",
    promptLabel: "Feature path",
    primaryText: "Run UI replay",
    secondaryText: "Open preview panel",
    help: "This is a static replay of the React/Firebase app structure and local screenshots.",
    options: [
      {
        value: "listing_flow",
        label: "Listing and account flow",
        prompt:
          "Show how the RentConnect prototype connects React routes, Firebase Auth, Firestore-backed data, listing search, Material UI, and payment wiring.",
        images: {
          ref: "./assets/project-captures/rentconnect-home.png",
          search: "./assets/project-captures/rentconnect-features.png",
          result: "./assets/project-captures/rentconnect-terminal.png"
        },
        captions: ["Home page", "Feature section", "Local terminal"],
        metrics: ["React", "frontend", "Firebase", "auth/data", "Adyen", "wiring"],
        replay: {
          frontend: "React + Material UI",
          data: "Firebase Auth / Firestore config shape",
          payment: "Adyen client-key wiring only; real payments need backend session flow",
          next_step: "modernize dependencies and tighten Firebase security rules"
        }
      }
    ]
  }
};

const demoOutput = document.getElementById("demoOutput");
const demoButtons = document.querySelectorAll("[data-demo]");
const labModeButtons = document.querySelectorAll("[data-lab-mode]");
const filterButtons = document.querySelectorAll("[data-filter]");
const projectCards = document.querySelectorAll(".project-card");
const projectDetailTitle = document.getElementById("projectDetailTitle");
const projectDetailBody = document.getElementById("projectDetailBody");
const sampleSelect = document.getElementById("sampleSelect");
const labSampleLabel = document.getElementById("labSampleLabel");
const labModeIntro = document.getElementById("labModeIntro");
const labPromptLabel = document.getElementById("labPromptLabel");
const labQwenControls = document.querySelectorAll(".lab-qwen-control");
const refUpload = document.getElementById("refUpload");
const searchUpload = document.getElementById("searchUpload");
const labPrompt = document.getElementById("labPrompt");
const labRefImage = document.getElementById("labRefImage");
const labSearchImage = document.getElementById("labSearchImage");
const labResultImage = document.getElementById("labResultImage");
const labRefCaption = document.getElementById("labRefCaption");
const labSearchCaption = document.getElementById("labSearchCaption");
const labResultCaption = document.getElementById("labResultCaption");
const labJsonOutput = document.getElementById("labJsonOutput");
const labDetectionCount = document.getElementById("labDetectionCount");
const labAvgTime = document.getElementById("labAvgTime");
const labOutputKind = document.getElementById("labOutputKind");
const labMetricOneLabel = document.getElementById("labMetricOneLabel");
const labMetricTwoLabel = document.getElementById("labMetricTwoLabel");
const labMetricThreeLabel = document.getElementById("labMetricThreeLabel");
const liveStatus = document.getElementById("liveStatus");
const liveHelpText = document.getElementById("liveHelpText");
const runRecordedButton = document.getElementById("runRecordedDemo");
const tryLiveButton = document.getElementById("tryLiveInference");

let currentLabMode = "qwen";

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

function populateLabOptions(mode) {
  if (!sampleSelect) return;
  sampleSelect.innerHTML = "";
  mode.options.forEach((option) => {
    const element = document.createElement("option");
    element.value = option.value;
    element.textContent = option.label;
    sampleSelect.appendChild(element);
  });
}

function setLabMode(name) {
  const mode = labModes[name] || labModes.qwen;
  currentLabMode = labModes[name] ? name : "qwen";

  labModeButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.labMode === currentLabMode);
  });

  if (labModeIntro) labModeIntro.textContent = mode.intro;
  if (labSampleLabel) labSampleLabel.textContent = mode.sampleLabel;
  if (labPromptLabel) labPromptLabel.textContent = mode.promptLabel;
  if (runRecordedButton) runRecordedButton.textContent = mode.primaryText;
  if (tryLiveButton) tryLiveButton.textContent = mode.secondaryText;

  labQwenControls.forEach((element) => {
    element.classList.toggle("lab-field-hidden", mode.type !== "qwen");
  });

  populateLabOptions(mode);

  if (mode.type === "qwen") {
    setLabSample(sampleSelect?.value || "test1");
  } else {
    setProjectLabSample(sampleSelect?.value || mode.options[0].value);
  }
}

function setLabSample(name) {
  const sample = qwenLabSamples[name] || qwenLabSamples.test1;
  labRefImage.src = sample.ref;
  labSearchImage.src = sample.search;
  labResultImage.src = sample.result;
  if (labRefCaption) labRefCaption.textContent = "Reference";
  if (labSearchCaption) labSearchCaption.textContent = "Search image";
  if (labResultCaption) labResultCaption.textContent = "Recorded result";
  labDetectionCount.textContent = sample.count;
  labAvgTime.textContent = sample.avgTime;
  if (labOutputKind) labOutputKind.textContent = "JSON";
  if (labMetricOneLabel) labMetricOneLabel.textContent = "detections";
  if (labMetricTwoLabel) labMetricTwoLabel.textContent = "recorded run time";
  if (labMetricThreeLabel) labMetricThreeLabel.textContent = "bbox output";
  if (labPrompt) {
    labPrompt.value =
      "Based on the two images above. The first image shows a target object. The second image contains multiple target objects. Find all objects of the same type in the second image and return JSON bounding boxes only.";
  }
  labJsonOutput.textContent = JSON.stringify(sample.json, null, 2);
  liveStatus.textContent = "recorded replay loaded";
  setLiveHelp("Recorded sample loaded. Click Try live endpoint to call the server-side DashScope function.");
}

function setProjectLabSample(value) {
  const mode = labModes[currentLabMode] || labModes.property;
  const sample = mode.options.find((item) => item.value === value) || mode.options[0];

  if (labPrompt) labPrompt.value = sample.prompt;
  setLabImages(sample.images, sample.captions);
  setLabMetrics(sample.metrics);
  labJsonOutput.textContent =
    typeof sample.replay === "string" ? sample.replay : JSON.stringify(sample.replay, null, 2);
  liveStatus.textContent = mode.type === "deepseek" ? "recorded replay ready" : "static replay ready";
  setLiveHelp(mode.help);
}

function setLabImages(images, captions = []) {
  const ref = resolveLabImage(images.ref);
  const search = resolveLabImage(images.search);
  const result = resolveLabImage(images.result);
  if (labRefImage) labRefImage.src = ref;
  if (labSearchImage) labSearchImage.src = search;
  if (labResultImage) labResultImage.src = result;
  if (labRefCaption) labRefCaption.textContent = captions[0] || "Input";
  if (labSearchCaption) labSearchCaption.textContent = captions[1] || "Process";
  if (labResultCaption) labResultCaption.textContent = captions[2] || "Output";
}

function resolveLabImage(value) {
  return typeof value === "function" ? value() : value;
}

function setLabMetrics(metrics) {
  const [one, oneLabel, two, twoLabel, three, threeLabel] = metrics;
  labDetectionCount.textContent = one;
  labAvgTime.textContent = two;
  if (labOutputKind) labOutputKind.textContent = three;
  if (labMetricOneLabel) labMetricOneLabel.textContent = oneLabel;
  if (labMetricTwoLabel) labMetricTwoLabel.textContent = twoLabel;
  if (labMetricThreeLabel) labMetricThreeLabel.textContent = threeLabel;
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
  setLiveHelp("Custom images are previewed locally. Click Try live endpoint to send them to the server-side function.");
}

labModeButtons.forEach((button) => {
  button.addEventListener("click", () => setLabMode(button.dataset.labMode));
});

sampleSelect?.addEventListener("change", () => {
  if (currentLabMode === "qwen") {
    setLabSample(sampleSelect.value);
  } else {
    setProjectLabSample(sampleSelect.value);
  }
});

runRecordedButton?.addEventListener("click", () => {
  if (currentLabMode === "qwen") {
    setLabSample(sampleSelect?.value || "test1");
    return;
  }

  setProjectLabSample(sampleSelect?.value || labModes[currentLabMode].options[0].value);
});

refUpload?.addEventListener("change", () => previewUpload(refUpload, labRefImage));
searchUpload?.addEventListener("change", () => previewUpload(searchUpload, labSearchImage, true));

tryLiveButton?.addEventListener("click", async () => {
  const mode = labModes[currentLabMode] || labModes.qwen;
  if (mode.type === "deepseek") {
    await runDeepSeekLiveDemo(mode);
    return;
  }

  if (mode.type === "static") {
    setDemo(mode.linkedDemo || currentLabMode);
    liveStatus.textContent = "opened preview panel";
    setLiveHelp("This project is shown as a static replay because the full service depends on local setup.");
    return;
  }

  await runQwenLiveInference();
});

async function runQwenLiveInference() {
  liveStatus.textContent = "checking endpoint...";
  setLiveHelp("Calling the Cloudflare Pages Function. The API key stays on the server side.");
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
    updateLiveHelp(payload, response.ok);
  } catch (error) {
    liveStatus.textContent = "endpoint not available on local static preview";
    setLiveHelp("The static local preview cannot reach the Pages Function. Test this on the deployed Cloudflare Pages site.");
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
}

async function runDeepSeekLiveDemo(mode) {
  liveStatus.textContent = "calling DeepSeek endpoint...";
  setLiveHelp("Calling the Cloudflare Pages Function. The DeepSeek key stays on the server side.");

  try {
    const response = await fetch("/api/deepseek-demo", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        mode: mode.endpointMode,
        input: labPrompt?.value || "",
        sample: sampleSelect?.value || ""
      })
    });
    const raw = await response.text();
    let payload;
    try {
      payload = JSON.parse(raw);
    } catch {
      payload = { status: "unexpected response", content: raw };
    }

    liveStatus.textContent = payload.status || "endpoint returned a response";
    renderDeepSeekPayload(payload, response.ok);
    updateDeepSeekHelp(payload, response.ok);
  } catch (error) {
    liveStatus.textContent = "endpoint not available on local static preview";
    setLiveHelp("The static local preview cannot reach the Pages Function. Test this on the deployed Cloudflare Pages site.");
    labJsonOutput.textContent = JSON.stringify(
      {
        status: "deepseek endpoint unavailable",
        message: "Deploy the Cloudflare Pages Function and add DEEPSEEK_API_KEY as a Pages secret.",
        error: error.message
      },
      null,
      2
    );
  }
}

function renderLivePayload(payload, isOk) {
  const results = payload?.parsed?.results || [];

  if (isOk && Array.isArray(results)) {
    labDetectionCount.textContent = String(results.length);
    labAvgTime.textContent = "live";
    drawLiveDetections(results);
  }

  labJsonOutput.textContent = JSON.stringify(payload.parsed || payload, null, 2);
}

function renderDeepSeekPayload(payload, isOk) {
  if (isOk && payload?.content) {
    labDetectionCount.textContent = "live";
    labAvgTime.textContent = payload.model || "DeepSeek";
    if (labOutputKind) labOutputKind.textContent = "Text";
    if (labMetricOneLabel) labMetricOneLabel.textContent = "draft mode";
    if (labMetricTwoLabel) labMetricTwoLabel.textContent = "model";
    if (labMetricThreeLabel) labMetricThreeLabel.textContent = "server response";
    labJsonOutput.textContent = payload.content;
    return;
  }

  labJsonOutput.textContent = JSON.stringify(payload, null, 2);
}

function updateLiveHelp(payload, isOk) {
  if (isOk && payload?.status === "live inference complete") {
    const count = payload?.parsed?.results?.length;
    setLiveHelp(
      count
        ? `DashScope returned ${count} detection result${count === 1 ? "" : "s"}; boxes were drawn on the result image.`
        : "DashScope returned a response. Review the JSON output if no boxes were drawn."
    );
    return;
  }

  if (payload?.status === "live inference not configured") {
    setLiveHelp("Add DASHSCOPE_API_KEY as a Cloudflare Pages secret, then redeploy the site.");
    return;
  }

  if (payload?.status === "dashscope request failed") {
    setLiveHelp("Check the DashScope key, model name, base URL region, account quota, and model permissions.");
    return;
  }

  setLiveHelp("Review the JSON output for provider details and next steps.");
}

function updateDeepSeekHelp(payload, isOk) {
  if (isOk && payload?.status === "deepseek draft complete") {
    setLiveHelp("DeepSeek returned a draft. Treat it as review-first output, not a final decision.");
    return;
  }

  if (payload?.status === "deepseek endpoint not configured") {
    setLiveHelp("Add DEEPSEEK_API_KEY as a Cloudflare Pages secret, then redeploy the site.");
    return;
  }

  if (payload?.status === "deepseek request failed") {
    setLiveHelp("Check the DeepSeek key, model name, base URL, quota, and account permissions.");
    return;
  }

  setLiveHelp("Review the response details and endpoint status.");
}

function setLiveHelp(message) {
  if (liveHelpText) liveHelpText.textContent = message;
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

function makeTrackingFrame(t) {
  const canvas = document.createElement("canvas");
  canvas.width = 720;
  canvas.height = 360;
  drawTracking(canvas, t);
  return canvas.toDataURL("image/png");
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
  setLabMode("qwen");

  if (noteMatch && projectDetails[noteMatch[1]]) {
    openProjectNote(noteMatch[1], false);
  } else {
    openProjectNote("qwen", false);
  }
}

drawTracking(document.getElementById("trackingCanvas"), 0.4);
initFromHash();
