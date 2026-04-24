# LeadCove — Marketing site

Landing page for **leadcove.io** — real estate lead enrichment SaaS.
Launching Miami May 2026, invite only.

## Structure

```
index.html         # single-page marketing site
styles.css         # all styles
favicon.svg        # mark
screenshots/       # product screenshots (drop PNGs here)
```

## Local preview

Open `index.html` in your browser. No build step.

## Product screenshots

The Product Tour section auto-fills from these files. If a file is missing,
a stylized placeholder renders in its slot.

| Path | What to capture |
|---|---|
| `screenshots/mission-control.png` | Today / Mission Control tab — priority calls + metrics |
| `screenshots/lead-modal.png` | Open lead modal — Call / SMS / FUB / log-outcome buttons |
| `screenshots/pipeline.png` | Pipeline kanban + analytics view |

Recommended size: **1600×1000** (16:10) for the main, **1200×800** for the
side two. PNG with transparent or dark navy background looks best.

## Deploy

This repo is wired for GitHub Pages — push to `main` and Pages serves it at
`leadcove.io` once DNS points here. Alternatively drop the folder on Vercel
/ Netlify / Cloudflare Pages — all work with zero config.
