# LeadCove Brand Kit

Last updated 2026-04-30. Owned by **Miami Metro LLC** (Florida).

The brand identity is **coastal-tech**: a wave + sun glyph in teal on navy, the Fraunces serif for display, Inter for everything else, warm cream backgrounds in supporting roles. Two-color core palette, no decorative accents, lots of white space.

---

## 1. Logo files

All assets live in `/assets/brand/`. Vector-first — use SVGs anywhere they'll render. PNGs are pre-rendered for places that need raster.

```
svg/                    ← edit / scale to anything
  mark.svg                  (256×256, navy box, teal mark — primary mark)
  mark-light.svg            (256×256, transparent bg, teal mark)
  mark-mono-navy.svg        (256×256, single-color navy)
  mark-mono-white.svg       (256×256, single-color white — for dark bg)
  wordmark.svg              ("LeadCove" only, navy)
  wordmark-light.svg        ("LeadCove" only, white)
  logo-horizontal.svg       (mark + wordmark side-by-side — primary lockup)
  logo-horizontal-light.svg (same, white wordmark for dark bg)
  logo-stacked.svg          (mark on top, wordmark below)
  logo-stacked-light.svg    (same, white wordmark)

png/                    ← drop-in raster
  mark_16/32/64/128/256/512/1024.png
  mark-light_256/512/1024.png
  mark-mono-navy_256/512/1024.png
  mark-mono-white_256/512/1024.png
  wordmark_480/960/1920.png
  wordmark-light_480/960/1920.png
  logo-horizontal_600/1200/2400.png
  logo-horizontal-light_600/1200/2400.png
  logo-stacked_480/960/1920.png
  logo-stacked-light_480/960/1920.png

render-png.py           ← regenerate all PNGs from SVGs (cairosvg)
index.html              ← preview every variant in a browser
```

### Picking the right file

| Scenario | Use |
|---|---|
| Browser favicon | `mark_32.png` or `mark.svg` |
| App icon (iOS / Android) | `mark_512.png` / `mark_1024.png` |
| Twitter / LinkedIn / Facebook profile pic | `mark_512.png` |
| Social share image (Open Graph) | Build a 1200×630 with `logo-horizontal_1200.png` left-aligned + tagline (TODO: separate OG template) |
| Site header / nav | `logo-horizontal.svg` |
| Dark hero / press release banner | `logo-horizontal-light.svg` |
| Email signature | `logo-horizontal_600.png` |
| Slide deck title | `logo-horizontal_1200.png` or `logo-stacked_960.png` |
| Business card | `logo-stacked.svg` |
| Single-color print / embossing | `mark-mono-navy.svg` |
| Sponsor row / partner deck (where everyone is monochrome) | `mark-mono-navy.svg` |

---

## 2. Color palette

The two core brand colors:

| Token | Hex | Usage |
|---|---|---|
| **Navy** | `#0B2545` | Primary brand color. Backgrounds, body text on light, mark container, headlines. |
| **Teal** | `#0E9F95` | Accent / action color. Mark elements (waves + sun), buttons, links, success states. |

Supporting palette (keep cool palette honest, add warmth where helpful):

| Token | Hex | Usage |
|---|---|---|
| Navy-2 | `#13335F` | Lighter navy for gradients, hover states on dark surfaces |
| Teal-2 | `#0B807A` | Darker teal for hovers + secondary teal accents |
| Cream | `#FBF8F3` | Warm secondary background — sidebar panels, modals, quiet sections |
| Sand | `#F5EDE1` | Slightly warmer cream — banners, callouts |
| Ink | `#0F172A` | Body text on light backgrounds |
| Muted | `#64748B` | Secondary text, captions, metadata |

**Don't use** any other colors as brand expression. If we ever need a third accent (e.g. for a campaign), bring it in as a one-off and fold it back to navy/teal afterward.

---

## 3. Typography

Two type families, freely available via Google Fonts:

| Family | Weight | Use |
|---|---|---|
| **Fraunces** | 600 (semi-bold) | Display: section titles, plan names, page H1s, pull quotes. Has personality without shouting. |
| **Inter** | 400 / 500 / 600 / 700 | Everything else: body, UI labels, buttons, metadata. |

System fallback chain:
```
font-family: 'Fraunces', 'Times New Roman', Georgia, serif;
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
```

Letter-spacing on display: `-0.02em` for tight, modern feel. Body stays at default tracking.

---

## 4. Logo usage rules

### Clear space

Always reserve a margin around the logo equal to the height of the wave glyph (~20% of the mark's total height). No element — text, photo, badge — encroaches inside that margin.

### Minimum size

| Mark only | 16px wide (favicon) — anything smaller becomes a single dot |
| Horizontal lockup | 120px wide (~1 inch print) |
| Stacked lockup | 80px square |

Below these the wordmark stops being readable.

### Don'ts

- **Don't** stretch / squish the logo. Always uniform scaling.
- **Don't** rotate or skew.
- **Don't** swap the colors (no navy waves on teal box, etc).
- **Don't** put the full-color mark on a high-contrast colored background — use the mono variant if the bg is neither white, cream, nor navy.
- **Don't** use the wordmark in a different typeface ever. Always Fraunces 600.
- **Don't** apply effects (drop shadows, gradients, glows) outside what's in the SVG file. The favicon's drop-shadow when used inside the dashboard sidebar is the one exception.

---

## 5. Voice & messaging guidelines

This is where the brand kit and the engineering memory rules merge. Iron rules from the operating handbook:

| Rule | Source |
|---|---|
| Say **"owner data — name, phone, and/or email"** — never "phone + email" | `feedback_owner_data_not_phone_email.md` |
| Never use the word **"free"** in user-visible strings | `feedback_no_free_in_user_strings.md` |
| Never use **"tenant"** in user-visible strings — say "user" or "account" | `feedback_no_tenant_in_user_strings.md` |
| Geo qualifier is **"Florida"**, never "Miami" | `feedback_no_miami_in_marketing.md` |
| The verb is **"Enrich"**, not "Resolve" | `project_dashboard_ux_polish.md` |
| Job-to-be-done: *"You can't contact a prospect without their name, phone, and/or email. LeadCove solves this — quickly and simply."* | `feedback_owner_data_not_phone_email.md` |
| **"No data, no charge"** — billing rule + marketing promise in lockstep | `feedback_no_data_no_charge_iron_rule.md` |
| Same product on every plan — only included monthly credits change | `project_one_product_tiered_only_by_credits.md` |
| Customers bring their own list — we don't source data | `feedback_only_offer_what_we_can_source.md` (SUPERSEDED — current rule is don't offer sourcing at all) |

When adding marketing copy or UI strings, audit against these. Vocabulary discipline > clever framing.

---

## 6. Domain + entity

| Asset | Detail |
|---|---|
| Primary domain | **leadcove.io** |
| Customer dashboard | **app.leadcove.io** |
| Operator dashboard | **admin.leadcove.io** |
| Email | `hello@leadcove.io` (operations) · `hello@miamimetro.us` (legal/billing) |
| Legal owner | **Miami Metro LLC** (Florida) |
| Footer disclosure | `© 2026 LeadCove · a brand owned by Miami Metro LLC, Florida` |

LLC ownership disclosure is required on every legal page (terms, privacy, TCPA notice) per `feedback_no_miami_in_marketing.md` — the only place "Miami" appears on the public surface is in the legal entity name "Miami Metro LLC".

---

## 7. Regenerating the PNG set

If you ever change an SVG or add a new variant:

```bash
# One-time setup (already done if you ran this before):
python3 -m venv /tmp/lc-svg-env
/tmp/lc-svg-env/bin/pip install cairosvg

# Make sure Fraunces is installed system-wide for accurate wordmark
# rendering — otherwise the text falls back to Times Roman.

cd assets/brand
/tmp/lc-svg-env/bin/python3 render-png.py
```

Or open `index.html` in a browser to visually inspect every variant
without rendering.
