# Zheng (John) Jiang Portfolio Website

Static personal website for Cloudflare Pages.

## Design Notes

- Keep the site project-first: screenshots, source links, demo previews, and handoff notes come before broad claims.
- Avoid generic AI-style copy: use concrete project context, short sentences, and honest "next improvement" notes.
- Keep it static and deployable on Cloudflare Pages. No API keys, no live model calls, and no backend dependency.
- Demo buttons are client-side previews only. They are meant to show workflow shape, not production inference.
- The Demo Lab includes recorded Qwen3-VL runs and a `/api/qwen-detect` Function stub for future live inference.
- True upload-and-infer needs a provider key or a deployed OpenAI-compatible VLM endpoint configured as Cloudflare Pages secrets.

## Local Preview

From this folder:

```powershell
python -m http.server 8788
```

Open:

```text
http://localhost:8788
```

## Cloudflare Pages - Direct Upload

Build command: none

Build output directory:

```text
.
```

Wrangler command:

```powershell
npx wrangler pages deploy . --project-name zheng-john-jiang-portfolio
```

## Cloudflare Pages - GitHub Connected Deploy

Repository:

```text
parker557/portfolio
```

Project root:

```text
website
```

Build command:

```text
None
```

Build output directory:

```text
website
```

## Notes

- This is a static showcase site. The demos are interactive previews, not live model inference.
- No API keys are embedded.
- Resume PDF is stored in `assets/Zheng_Jiang_Resume.pdf`.
