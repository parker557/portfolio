const SAMPLE_ASSETS = {
  test1: {
    reference: "/assets/qwen-test1-ref.jpg",
    search: "/assets/qwen-test1-search.jpg"
  },
  test2: {
    reference: "/assets/qwen-test2-ref.png",
    search: "/assets/qwen-test2-search.jpg"
  }
};

const MAX_IMAGE_BYTES = 7 * 1024 * 1024;

export async function onRequestPost(context) {
  try {
    const form = await context.request.formData();
    const prompt = String(form.get("prompt") || "").trim();
    const sample = String(form.get("sample") || "test1");
    const referenceFile = getUploadedFile(form, "reference");
    const searchFile = getUploadedFile(form, "search");

    if (!context.env.DASHSCOPE_API_KEY) {
      return Response.json(
        {
          status: "live inference not configured",
          sample,
          received: {
            prompt_chars: prompt.length,
            reference_uploaded: Boolean(referenceFile),
            search_uploaded: Boolean(searchFile)
          },
          next_step:
            "Add DASHSCOPE_API_KEY as a Cloudflare Pages secret, then redeploy the Pages project."
        },
        { status: 501 }
      );
    }

    const referenceImage = referenceFile
      ? await fileToDataUrl(referenceFile)
      : await sampleAssetToDataUrl(context.request.url, sample, "reference");
    const searchImage = searchFile
      ? await fileToDataUrl(searchFile)
      : await sampleAssetToDataUrl(context.request.url, sample, "search");

    const model = context.env.DASHSCOPE_MODEL || "qwen3-vl-plus";
    const payload = buildDashScopePayload({
      model,
      prompt,
      referenceImage,
      searchImage
    });

    const result = await callDashScope(context.env.DASHSCOPE_API_KEY, payload, context.env);

    if (!result.ok) {
      return Response.json(
        {
          status: "dashscope request failed",
          sample,
          model,
          error: result.error
        },
        { status: 502 }
      );
    }

    const content = result.data?.choices?.[0]?.message?.content || "";
    const parsed = extractJson(content);

    return Response.json({
      status: "live inference complete",
      provider: "DashScope",
      endpoint: result.endpoint,
      model,
      sample,
      content,
      parsed,
      usage: result.data?.usage || null
    });
  } catch (error) {
    return Response.json(
      {
        status: "live inference error",
        message: error.message
      },
      { status: 500 }
    );
  }
}

function getUploadedFile(form, name) {
  const value = form.get(name);
  if (!value || typeof value === "string" || value.size === 0) return null;
  return value;
}

async function sampleAssetToDataUrl(requestUrl, sample, kind) {
  const asset = SAMPLE_ASSETS[sample]?.[kind] || SAMPLE_ASSETS.test1[kind];
  const url = new URL(asset, requestUrl);
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Could not load sample ${kind} image: ${response.status}`);
  }

  const contentType = response.headers.get("content-type") || "image/jpeg";
  const arrayBuffer = await response.arrayBuffer();
  return arrayBufferToDataUrl(arrayBuffer, contentType);
}

async function fileToDataUrl(file) {
  if (file.size > MAX_IMAGE_BYTES) {
    throw new Error("Image is too large. Please upload an image under 7 MB.");
  }

  const contentType = file.type || "image/jpeg";
  const arrayBuffer = await file.arrayBuffer();
  return arrayBufferToDataUrl(arrayBuffer, contentType);
}

function arrayBufferToDataUrl(arrayBuffer, contentType) {
  if (arrayBuffer.byteLength > MAX_IMAGE_BYTES) {
    throw new Error("Image is too large after loading. Please use a smaller image.");
  }

  const bytes = new Uint8Array(arrayBuffer);
  let binary = "";
  const chunkSize = 0x8000;

  for (let i = 0; i < bytes.length; i += chunkSize) {
    binary += String.fromCharCode(...bytes.subarray(i, i + chunkSize));
  }

  return `data:${contentType};base64,${btoa(binary)}`;
}

function buildDashScopePayload({ model, prompt, referenceImage, searchImage }) {
  const userPrompt =
    prompt ||
    "Find all objects in the search image that match the reference image. Return JSON only.";

  return {
    model,
    messages: [
      {
        role: "system",
        content:
          "You are a vision-language object detection assistant. Return compact JSON only, with no Markdown fences. The top-level object must have a results array. Each result must include label, confidence if available, and bbox_2d as a JSON array [x1, y1, x2, y2] in pixel coordinates."
      },
      {
        role: "user",
        content: [
          { type: "text", text: "Reference image:" },
          { type: "image_url", image_url: { url: referenceImage } },
          { type: "text", text: "Search image:" },
          { type: "image_url", image_url: { url: searchImage } },
          {
            type: "text",
            text: `${userPrompt}\n\nReturn valid JSON only. Do not use Markdown. Do not omit square brackets around bbox_2d. Example: {"results":[{"label":"target_object","confidence":0.82,"bbox_2d":[10,20,100,180]}]}`
          }
        ]
      }
    ],
    temperature: 0.1,
    max_tokens: 1200
  };
}

async function callDashScope(apiKey, payload, env) {
  const endpoints = buildEndpointCandidates(env);
  let lastError = null;

  for (const endpoint of endpoints) {
    const response = await fetch(`${endpoint}/chat/completions`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    const text = await response.text();
    const data = safeJsonParse(text);

    if (response.ok) {
      return { ok: true, endpoint, data };
    }

    lastError = {
      endpoint,
      status_code: response.status,
      response: data || text.slice(0, 1200)
    };
  }

  return { ok: false, error: lastError };
}

function buildEndpointCandidates(env) {
  if (env.DASHSCOPE_BASE_URL) return [normalizeEndpoint(env.DASHSCOPE_BASE_URL)];

  return [
    "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
  ];
}

function normalizeEndpoint(endpoint) {
  return endpoint.replace(/\/+$/, "").replace(/\/chat\/completions$/, "");
}

function safeJsonParse(text) {
  try {
    return JSON.parse(text);
  } catch {
    return null;
  }
}

function extractJson(content) {
  const text = Array.isArray(content)
    ? content.map((part) => part.text || "").join("\n")
    : String(content || "");

  const cleaned = text.replace(/```json|```/gi, "").trim();
  const first = cleaned.indexOf("{");
  const last = cleaned.lastIndexOf("}");

  if (first === -1 || last === -1 || last <= first) return null;
  const parsed = safeJsonParse(cleaned.slice(first, last + 1));
  if (parsed) return parsed;

  return extractLooseDetections(cleaned);
}

function extractLooseDetections(text) {
  const results = [];
  const pattern =
    /"label"\s*:\s*"([^"]+)"[\s\S]*?"confidence"\s*:\s*([0-9.]+)[\s\S]*?"bbox_2d"\s*:\s*\[?\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)/g;
  let match;

  while ((match = pattern.exec(text))) {
    results.push({
      label: match[1],
      confidence: Number(match[2]),
      bbox_2d: match.slice(3, 7).map(Number)
    });
  }

  if (results.length > 0) return { results };
  return null;
}
