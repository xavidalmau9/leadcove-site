#!/usr/bin/env python3
"""
LeadCove · Instagram graphic v2 — single product-screenshot hero.

After v1 user feedback (Xavi 2026-06-05): "square graphic has overlay
problems that is horrific". Issues:
  - Two competing cards (BEFORE chip stack vs AFTER mock) were dense
  - The mock owner card with "•••" masked phones looked fake
  - The DNC-checked footer had a missing-glyph "□" fallback
  - Three different pill colors in the AFTER card felt noisy

v2 approach: ONE composition. A high-fidelity render of the dashboard
owner-modal panel — same dark navy as the real dashboard, realistic
spacing, real status pills — using clear synthetic data per iron rule
(Jane Smith / 555-prefix / example.com / 1234 Example St).

Renders two outputs:
  ig-square-v2.png  (1080x1080) — feed post
  ig-story-v2.png   (1080x1920) — story / reel cover

Both reachable via `python3 render-ig-v2.py`. Idempotent.
"""
from PIL import Image, ImageDraw, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND_PNG = os.path.normpath(os.path.join(HERE, '..', 'brand', 'png'))

# Brand palette — pulled from the real dashboard CSS variables.
TEAL       = (14, 159, 149)
TEAL_DIM   = (10, 130, 122)
NAVY_BG    = (11, 22, 41)          # dashboard --bg
NAVY_PANEL = (17, 35, 57)          # dashboard panel
HAIRLINE   = (38, 55, 78)
INK        = (218, 230, 240)
INK_DIM    = (148, 168, 185)
WHITE      = (255, 255, 255)
GREEN_PILL = (28, 128, 92)
GREEN_TEXT = (180, 240, 210)
AMBER_PILL = (138, 80, 30)
AMBER_TEXT = (250, 200, 130)
GRAY_PILL  = (60, 78, 96)
GRAY_TEXT  = (200, 215, 230)

# ── Font loader ────────────────────────────────────────────────────────
def load_font(size, weight='regular'):
    candidates = {
        'bold':    ['/System/Library/Fonts/Supplemental/Arial Bold.ttf',
                    '/System/Library/Fonts/HelveticaNeue.ttc'],
        'regular': ['/System/Library/Fonts/Supplemental/Arial.ttf',
                    '/System/Library/Fonts/HelveticaNeue.ttc'],
        'heavy':   ['/System/Library/Fonts/Supplemental/Arial Black.ttf',
                    '/System/Library/Fonts/Supplemental/Arial Bold.ttf'],
    }
    for p in candidates.get(weight, candidates['regular']):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def text_w(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    try:
        draw.rounded_rectangle(xy, radius=radius, fill=fill,
                               outline=outline, width=width)
    except AttributeError:
        x0, y0, x1, y1 = xy
        draw.rectangle((x0 + radius, y0, x1 - radius, y1), fill=fill)
        draw.rectangle((x0, y0 + radius, x1, y1 - radius), fill=fill)
        for cx, cy in [(x0, y0), (x1 - 2 * radius, y0),
                       (x0, y1 - 2 * radius), (x1 - 2 * radius, y1 - 2 * radius)]:
            draw.pieslice((cx, cy, cx + 2 * radius, cy + 2 * radius),
                          0, 360, fill=fill)


def gradient_bg(size, top, bottom):
    w, h = size
    img = Image.new('RGB', size, top)
    px = img.load()
    for y in range(h):
        t = y / max(1, h - 1)
        c = (int(top[0] + (bottom[0] - top[0]) * t),
             int(top[1] + (bottom[1] - top[1]) * t),
             int(top[2] + (bottom[2] - top[2]) * t))
        for x in range(w):
            px[x, y] = c
    return img


def draw_status_pill(draw, x, y, label, fill, text_color, font):
    pw = text_w(draw, label, font) + 24
    ph = 28
    rounded_rect(draw, (x, y, x + pw, y + ph), radius=14, fill=fill)
    draw.text((x + 12, y + (ph - font.size) // 2 - 2), label,
              fill=text_color, font=font)
    return pw


# ── The dashboard panel (the centerpiece) ──────────────────────────────
def draw_owner_panel(target, top_left, width):
    """Render a high-fidelity owner panel onto `target` image at
    top_left=(x, y), spanning `width` px wide. Returns the panel height
    so the caller can place CTAs underneath. Uses clear synthetic data
    per iron rule (Jane Smith / 555 / example.com / 1234 Example St)."""
    draw = ImageDraw.Draw(target)
    x, y = top_left
    pad = 32

    # Compute height after we know how many rows we draw
    f_addr  = load_font(22, 'bold')
    f_owner = load_font(34, 'bold')
    f_label = load_font(14, 'bold')
    f_phone = load_font(24, 'bold')
    f_pill  = load_font(14, 'bold')
    f_meta  = load_font(16, 'regular')

    # Phones — 4 rows. 555 area code (universally fictional).
    phones = [
        ('(555) 010-4821',  'CLEAN',  GREEN_PILL, GREEN_TEXT, 'Worked',     GREEN_PILL, GREEN_TEXT),
        ('(555) 010-6109',  'CLEAN',  GREEN_PILL, GREEN_TEXT, 'Not tried',  GRAY_PILL,  GRAY_TEXT),
        ('(555) 010-7733',  'DNC',    AMBER_PILL, AMBER_TEXT, 'Not tried',  GRAY_PILL,  GRAY_TEXT),
    ]
    emails = [
        ('jsmith@example.com',     'Worked'),
        ('jane.s@example.com',     'Not tried'),
    ]

    # ── Layout math ──
    header_h     = 56              # property address bar
    owner_h      = 52              # owner name
    section_h    = 26              # "PHONES" / "EMAILS" label
    row_h        = 50
    phones_h     = section_h + len(phones) * row_h + 8
    emails_h     = section_h + len(emails) * row_h + 8
    footer_h     = 48
    panel_h = header_h + owner_h + phones_h + emails_h + footer_h + pad * 2

    # Panel background (dark navy with subtle inner border)
    rounded_rect(draw, (x, y, x + width, y + panel_h),
                 radius=22, fill=NAVY_PANEL,
                 outline=HAIRLINE, width=1)

    cy = y + pad

    # 1. Property address bar (sticky-like)
    draw.text((x + pad, cy + 6), '1234 EXAMPLE ST, UNIT 1509',
              fill=INK, font=f_addr)
    # close icon (×) to the right
    f_close = load_font(28, 'regular')
    draw.text((x + width - pad - 18, cy), '×',
              fill=INK_DIM, font=f_close)
    cy += header_h
    # divider
    draw.line((x + pad, cy - 12, x + width - pad, cy - 12),
              fill=HAIRLINE, width=1)

    # 2. Owner name
    draw.text((x + pad, cy), 'Jane Smith', fill=WHITE, font=f_owner)
    cy += owner_h

    # 3. PHONES section
    draw.text((x + pad, cy), 'PHONES', fill=INK_DIM, font=f_label)
    cy += section_h

    # Column heads
    f_col = load_font(13, 'bold')
    draw.text((x + pad, cy), 'NUMBER', fill=INK_DIM, font=f_col)
    draw.text((x + pad + 280, cy), 'STATUS', fill=INK_DIM, font=f_col)
    draw.text((x + pad + 420, cy), 'OUTCOME', fill=INK_DIM, font=f_col)
    cy += 18
    # subtle separator under heads
    draw.line((x + pad, cy, x + width - pad, cy), fill=HAIRLINE, width=1)
    cy += 4

    # NOTE: no ✓ / ⚠ prefixes — Arial fallback shows them as missing-glyph
    # boxes (□). The pill color carries the meaning: green=clean/worked,
    # amber=DNC, gray=not yet attempted.
    for num, status_label, status_fill, status_text, outcome_label, outcome_fill, outcome_text in phones:
        draw.text((x + pad, cy + 10), num, fill=WHITE, font=f_phone)
        draw_status_pill(draw, x + pad + 280, cy + 14,
                         status_label,
                         status_fill, status_text, f_pill)
        draw_status_pill(draw, x + pad + 420, cy + 14,
                         outcome_label,
                         outcome_fill, outcome_text, f_pill)
        cy += row_h

    cy += 8
    draw.line((x + pad, cy, x + width - pad, cy), fill=HAIRLINE, width=1)
    cy += 16

    # 4. EMAILS section
    draw.text((x + pad, cy), 'EMAILS', fill=INK_DIM, font=f_label)
    cy += section_h
    draw.text((x + pad, cy), 'ADDRESS', fill=INK_DIM, font=f_col)
    draw.text((x + pad + 420, cy), 'OUTCOME', fill=INK_DIM, font=f_col)
    cy += 18
    draw.line((x + pad, cy, x + width - pad, cy), fill=HAIRLINE, width=1)
    cy += 4

    for em, outcome in emails:
        draw.text((x + pad, cy + 10), em, fill=WHITE, font=f_phone)
        out_fill = GREEN_PILL if outcome == 'Worked' else GRAY_PILL
        out_text = GREEN_TEXT if outcome == 'Worked' else GRAY_TEXT
        draw_status_pill(draw, x + pad + 420, cy + 14,
                         outcome,
                         out_fill, out_text, f_pill)
        cy += row_h

    cy += 16

    # 5. Footer strip — the "every contact, every owner" callout
    strip_y = cy
    strip_h = footer_h - 12
    rounded_rect(draw, (x + pad, strip_y, x + width - pad, strip_y + strip_h),
                 radius=10, fill=(20, 60, 70))
    f_strip = load_font(15, 'bold')
    msg = 'Outcomes sync to this owner\'s 3 other properties — automatically.'
    msg_w = text_w(draw, msg, f_strip)
    draw.text((x + pad + ((width - 2 * pad - msg_w) // 2),
               strip_y + (strip_h - f_strip.size) // 2 - 2),
              msg, fill=(190, 240, 220), font=f_strip)

    return panel_h


# ── Square renderer ──────────────────────────────────────────────────
def render_square():
    W, H = 1080, 1080
    bg = gradient_bg((W, H), TEAL, TEAL_DIM)
    draw = ImageDraw.Draw(bg)

    # Top: logo (small, top-center)
    logo_path = os.path.join(BRAND_PNG, 'logo-stacked-light_480.png')
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert('RGBA')
        target_w = 88
        ratio = target_w / logo.width
        logo = logo.resize((target_w, int(logo.height * ratio)), Image.LANCZOS)
        bg.paste(logo, ((W - target_w) // 2, 28), logo)

    # Eyebrow + headline (terse, ONE line)
    f_eye = load_font(24, 'bold')
    eyebrow = 'EVERY OWNER · EVERY PHONE · EVERY EMAIL'
    ew = text_w(draw, eyebrow, f_eye)
    draw.text(((W - ew) // 2, 190), eyebrow, fill=(180, 230, 224), font=f_eye)

    f_h1 = load_font(64, 'heavy')
    headline = 'One screen. Verified.'
    hw = text_w(draw, headline, f_h1)
    draw.text(((W - hw) // 2, 226), headline, fill=WHITE, font=f_h1)

    # Center: the panel
    panel_w = W - 120
    panel_h = draw_owner_panel(bg, (60, 320), panel_w)

    # Bottom CTA bar
    cta_h = 80
    cta_y = H - cta_h - 36
    rounded_rect(draw, (60, cta_y, W - 60, cta_y + cta_h),
                 radius=cta_h // 2, fill=WHITE)
    f_cta = load_font(30, 'bold')
    cta = 'leadcove.io  ·  start free trial'
    cw = text_w(draw, cta, f_cta)
    draw.text(((W - cw) // 2, cta_y + (cta_h - 30) // 2 - 4),
              cta, fill=(11, 37, 69), font=f_cta)

    out = os.path.join(HERE, 'ig-square-v2.png')
    bg.save(out, 'PNG', optimize=True)
    print(f'✓ wrote {out}')


# ── Story renderer ─────────────────────────────────────────────────
def render_story():
    W, H = 1080, 1920
    bg = gradient_bg((W, H), TEAL, TEAL_DIM)
    draw = ImageDraw.Draw(bg)

    logo_path = os.path.join(BRAND_PNG, 'logo-stacked-light_960.png')
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert('RGBA')
        target_w = 160
        ratio = target_w / logo.width
        logo = logo.resize((target_w, int(logo.height * ratio)), Image.LANCZOS)
        bg.paste(logo, ((W - target_w) // 2, 100), logo)

    f_eye = load_font(28, 'bold')
    eyebrow = 'EVERY OWNER · EVERY PHONE · EVERY EMAIL'
    ew = text_w(draw, eyebrow, f_eye)
    draw.text(((W - ew) // 2, 420), eyebrow,
              fill=(180, 230, 224), font=f_eye)

    f_h1 = load_font(88, 'heavy')
    headline = 'One screen.'
    hw = text_w(draw, headline, f_h1)
    draw.text(((W - hw) // 2, 480), headline, fill=WHITE, font=f_h1)
    f_h2 = load_font(72, 'heavy')
    sub = 'Verified.'
    sw = text_w(draw, sub, f_h2)
    draw.text(((W - sw) // 2, 590), sub, fill=WHITE, font=f_h2)

    # Centered panel
    panel_w = W - 120
    draw_owner_panel(bg, (60, 740), panel_w)

    # CTA
    cta_h = 100
    cta_y = H - cta_h - 200
    rounded_rect(draw, (80, cta_y, W - 80, cta_y + cta_h),
                 radius=cta_h // 2, fill=WHITE)
    f_cta = load_font(38, 'bold')
    cta = 'leadcove.io  ·  start free trial'
    cw = text_w(draw, cta, f_cta)
    draw.text(((W - cw) // 2, cta_y + (cta_h - 38) // 2 - 6),
              cta, fill=(11, 37, 69), font=f_cta)

    out = os.path.join(HERE, 'ig-story-v2.png')
    bg.save(out, 'PNG', optimize=True)
    print(f'✓ wrote {out}')


if __name__ == '__main__':
    render_square()
    render_story()
