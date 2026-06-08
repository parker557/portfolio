const jsonHeaders = {
  "Content-Type": "application/json; charset=utf-8",
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type"
};

const prompts = {
  property: {
    system:
      "You are helping with a portfolio demo for a property-management software project. Write concise, operational output for staff. Do not claim that a real ticket was created or that a vendor has been dispatched. Phrase actions as suggested next steps. Keep it concrete and easy to review.",
    user:
      "Return a short property-management triage draft with these labels: Summary, Priority, Staff Reply, Next Actions, Review Note."
  },
  finance: {
    system:
      "You are helping with a portfolio demo for an AI report-writing workflow. This is not financial advice. Do not recommend investments or make claims about guaranteed outcomes. Do not invent current prices, rent averages, tax rules, or dollar amounts unless the user provides them. Use placeholders or questions to verify when data is missing. Keep it cautious and review-first.",
    user:
      "Return a short financial planning draft with these labels: Scope, Checklist, Risk Notes, Questions To Verify, Review Note."
  }
};

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: jsonHeaders });
}

export async function onRequestPost({ request, env }) {
  if (!env.DEEPSEEK_API_KEY) {
    return json(
      {
        status: "deepseek endpoint not configured",
        message: "Set DEEPSEEK_API_KEY as a Cloudflare Pages secret, then redeploy."
      },
      503
    );
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return json({ status: "invalid request", message: "Expected JSON body." }, 400);
  }

  const mode = String(body.mode || "").toLowerCase();
  const prompt = prompts[mode];
  if (!prompt) {
    return json({ status: "invalid mode", message: "Use property or finance." }, 400);
  }

  const input = String(body.input || "").trim().slice(0, 1800);
  if (!input) {
    return json({ status: "missing input", message: "Add a short prompt or scenario." }, 400);
  }

  const model = env.DEEPSEEK_MODEL || "deepseek-chat";
  const baseUrl = (env.DEEPSEEK_BASE_URL || "https://api.deepseek.com").replace(/\/$/, "");

  try {
    const response = await fetch(`${baseUrl}/chat/completions`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${env.DEEPSEEK_API_KEY}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model,
        temperature: 0.25,
        max_tokens: 520,
        messages: [
          { role: "system", content: prompt.system },
          { role: "user", content: `${prompt.user}\n\nScenario:\n${input}` }
        ]
      })
    });

    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      return json(
        {
          status: "deepseek request failed",
          provider: "DeepSeek",
          model,
          statusCode: response.status,
          message: data.error?.message || "DeepSeek returned an error."
        },
        502
      );
    }

    const content = data.choices?.[0]?.message?.content?.trim() || "";
    return json({
      status: "deepseek draft complete",
      provider: "DeepSeek",
      model,
      mode,
      content,
      usage: data.usage || null
    });
  } catch (error) {
    return json(
      {
        status: "deepseek request failed",
        provider: "DeepSeek",
        model,
        message: error.message
      },
      502
    );
  }
}

function json(payload, status = 200) {
  return new Response(JSON.stringify(payload), {
    status,
    headers: jsonHeaders
  });
}
