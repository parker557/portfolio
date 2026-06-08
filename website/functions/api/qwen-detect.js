export async function onRequestPost(context) {
  const form = await context.request.formData();
  const prompt = String(form.get("prompt") || "");
  const sample = String(form.get("sample") || "test1");
  const hasReference = form.has("reference");
  const hasSearch = form.has("search");

  const hasDashScopeKey = Boolean(context.env.DASHSCOPE_API_KEY);
  const hasVllmEndpoint = Boolean(context.env.VLLM_BASE_URL);

  if (!hasDashScopeKey && !hasVllmEndpoint) {
    return Response.json(
      {
        status: "live inference not configured",
        sample,
        received: {
          prompt_chars: prompt.length,
          reference_uploaded: hasReference,
          search_uploaded: hasSearch
        },
        needs_one_of: [
          "DASHSCOPE_API_KEY for Alibaba Cloud Qwen vision models",
          "VLLM_BASE_URL and optional VLLM_API_KEY for your own OpenAI-compatible Qwen/VLM endpoint"
        ],
        next_step:
          "Add Cloudflare Pages secrets, then implement the provider-specific fetch call in functions/api/qwen-detect.js."
      },
      { status: 501 }
    );
  }

  return Response.json(
    {
      status: "provider credentials detected, provider call not implemented yet",
      sample,
      next_step:
        "Choose the target provider payload format: DashScope Qwen-VL or OpenAI-compatible vLLM."
    },
    { status: 501 }
  );
}
