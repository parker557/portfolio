# Zheng (John) Jiang Portfolio Website

Static personal website for Cloudflare Pages.

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
