#!/usr/bin/env python3
"""
LeadCove · Instagram launch graphic #01 (before/after).

Renders two outputs:
  - ig-launch-01-square.png   (1080x1080) — feed post
  - ig-launch-01-story.png    (1080x1920) — Story / Reel cover

Concept (Xavi 2026-06-05): replace the "7 tabs to find one owner" tax
with one screen + 8 seconds. Visually contrast the two halves of the
workflow on brand-teal background, white logo, terse copy.

Run with the system python3:
    python3 render-ig-launch-01.py

Drops PNGs alongside this script. Idempotent — overwrites cleanly.
"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND_PNG = os.path.normpath(os.path.join(HERE, '..', 'brand', 'png'))

# ── Brand palette ──────────────────────────────────────────────────────
TEAL       = (14, 159, 149)         # --accent
TEAL_DARK  = (8, 95, 89)            # darker for gradient
NAVY       = (11, 37, 69)           # secondary
WHITE      = (255, 255, 255)
SAND       = (245, 240, 232)        # warm off-white for chip backgrounds
MUTED_DARK = (130, 160, 158)        # dim text on teal

# Font candidates (macOS). Fall back gracefully.
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


def gradient_bg(size, top, bottom):
    """Vertical 2-stop gradient."""
    w, h = size
    img = Image.new('RGB', size, top)
    px = img.load()
    for y in range(h):
        t = y / max(1, h - 1)
        px[0, y] = (
            int(top[0] + (bottom[0] - top[0]) * t),
            int(top[1] + (bottom[1] - top[1]) * t),
            int(top[2] + (bottom[2] - top[2]) * t),
        )
        for x in range(1, w):
            px[x, y] = px[0, y]
    return img


def rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    """Filled rounded rectangle (Pillow ≥9.2 has the helper, this is a
    safe wrapper that works on older builds too)."""
    try:
        draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)
    except AttributeError:
        # Fallback: rectangle + four corner ellipses
        x0, y0, x1, y1 = xy
        draw.rectangle((x0 + radius, y0, x1 - radius, y1), fill=fill)
        draw.rectangle((x0, y0 + radius, x1, y1 - radius), fill=fill)
        for cx, cy in [(x0, y0), (x1 - 2 * radius, y0),
                       (x0, y1 - 2 * radius), (x1 - 2 * radius, y1 - 2 * radius)]:
            draw.pieslice((cx, cy, cx + 2 * radius, cy + 2 * radius), 0, 360, fill=fill)


def text_w(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def draw_tab_chip(draw, x, y, w, h, label, font, label_color=NAVY):
    """A faded browser-tab pill labeled with a competitor name."""
    rounded_rect(draw, (x, y, x + w, y + h), radius=h // 2, fill=SAND)
    tw = text_w(draw, label, font)
    draw.text((x + (w - tw) // 2, y + (h - font.size) // 2 - 2),
              label, fill=label_color, font=font)


def render_square():
    W, H = 1080, 1080
    bg = gradient_bg((W, H), TEAL, TEAL_DARK)
    draw = ImageDraw.Draw(bg)

    # Top eyebrow — sits below 96-wide stacked logo (logo top y=28,
    # logo bottom ~188 after 0.6 aspect ratio scaling).
    f_eye = load_font(26, 'bold')
    eyebrow = 'FOR WORKING REAL ESTATE AGENTS'
    ew = text_w(draw, eyebrow, f_eye)
    draw.text(((W - ew) // 2, 205), eyebrow, fill=(180, 230, 224), font=f_eye)

    # Hero headline (two lines). Sized so the second line bottoms out
    # before the BEFORE/AFTER cards start (y=420).
    f_h1 = load_font(72, 'heavy')
    line1 = '7 lookup sites.'
    line2 = 'Or one screen.'
    w1 = text_w(draw, line1, f_h1)
    w2 = text_w(draw, line2, f_h1)
    draw.text(((W - w1) // 2, 250), line1, fill=WHITE, font=f_h1)
    draw.text(((W - w2) // 2, 330), line2, fill=WHITE, font=f_h1)

    # ── BEFORE card (left, faded chips of competitor names) ──────────
    f_chip = load_font(22, 'bold')
    f_label = load_font(26, 'bold')

    card_w = 460
    card_h = 460
    card_pad = 36

    # Left card (legacy). y=420 pushes the cards below the headline
    # baseline so "screen." descenders don't collide with the card top.
    lx, ly = 60, 420
    rounded_rect(draw, (lx, ly, lx + card_w, ly + card_h), radius=28, fill=(255, 255, 255, 255))
    # Header chip "BEFORE"
    rounded_rect(draw, (lx + card_pad, ly + card_pad, lx + card_pad + 130, ly + card_pad + 36),
                 radius=18, fill=(238, 232, 220))
    draw.text((lx + card_pad + 22, ly + card_pad + 7), 'BEFORE', fill=(120, 100, 70), font=f_chip)
    # Subhead
    f_sub = load_font(28, 'bold')
    draw.text((lx + card_pad, ly + card_pad + 56),
              '7 tabs.', fill=NAVY, font=f_sub)
    draw.text((lx + card_pad, ly + card_pad + 92),
              '2.5 hours.', fill=NAVY, font=f_sub)
    draw.text((lx + card_pad, ly + card_pad + 128),
              '~$62 in fees.', fill=NAVY, font=f_sub)

    # Stacked generic-tab chips. Named competitors INTENTIONALLY avoided
    # (iron rule feedback_no_third_party_brand_names_without_permission.md
    # — stylized text counts). The visual message is "many tabs", the
    # brand names weren't carrying the meaning.
    placeholders = ['site-one.com', 'site-two.com', 'site-three.com',
                    'site-four.com', 'site-five.com', 'site-six.com',
                    'site-seven.com']
    chip_y = ly + card_pad + 188
    for c in placeholders:
        chip_w = text_w(draw, c, f_chip) + 26
        draw_tab_chip(draw, lx + card_pad, chip_y, chip_w, 32, c, f_chip,
                      label_color=(100, 110, 120))
        chip_y += 38

    # ── AFTER card (right, the LeadCove modal) ───────────────────────
    rx, ry = W - 60 - card_w, 420
    rounded_rect(draw, (rx, ry, rx + card_w, ry + card_h), radius=28, fill=WHITE)
    # "AFTER" pill in teal
    rounded_rect(draw, (rx + card_pad, ry + card_pad, rx + card_pad + 110, ry + card_pad + 36),
                 radius=18, fill=(220, 245, 240))
    draw.text((rx + card_pad + 22, ry + card_pad + 7), 'AFTER', fill=(20, 110, 102), font=f_chip)
    # Subhead
    draw.text((rx + card_pad, ry + card_pad + 56),
              '1 screen.', fill=NAVY, font=f_sub)
    draw.text((rx + card_pad, ry + card_pad + 92),
              '8 seconds.', fill=NAVY, font=f_sub)
    draw.text((rx + card_pad, ry + card_pad + 128),
              '$0 today.', fill=NAVY, font=f_sub)

    # Owner-modal mock (the value prop visualized)
    panel_x = rx + card_pad
    panel_y = ry + card_pad + 188
    panel_w = card_w - 2 * card_pad
    panel_h = 232
    rounded_rect(draw, (panel_x, panel_y, panel_x + panel_w, panel_y + panel_h),
                 radius=16, fill=(247, 250, 250), outline=(220, 230, 230), width=1)
    # Owner name
    f_owner = load_font(26, 'bold')
    draw.text((panel_x + 18, panel_y + 16), 'Maria Espinoza', fill=NAVY, font=f_owner)
    # Three contact rows
    f_row = load_font(20, 'bold')
    f_tag = load_font(16, 'bold')
    rows = [
        ('305 ••• 4821',  'MOBILE',  TEAL),
        ('305 ••• 6109',  'LANDLINE',(120, 130, 140)),
        ('m••••@email.com', 'EMAIL', (90, 130, 200)),
    ]
    rh = 38
    rx2 = panel_x + 18
    ry2 = panel_y + 60
    for label, tag, color in rows:
        draw.text((rx2, ry2), label, fill=NAVY, font=f_row)
        tag_w = text_w(draw, tag, f_tag) + 16
        rounded_rect(draw, (panel_x + panel_w - 18 - tag_w, ry2 + 2,
                            panel_x + panel_w - 18, ry2 + 26),
                     radius=12, fill=color)
        draw.text((panel_x + panel_w - 18 - tag_w + 8, ry2 + 5), tag, fill=WHITE, font=f_tag)
        ry2 += rh

    # DNC verified strip
    verified_y = panel_y + panel_h - 32
    rounded_rect(draw, (panel_x + 18, verified_y, panel_x + panel_w - 18, verified_y + 24),
                 radius=12, fill=(220, 245, 240))
    f_verified = load_font(14, 'bold')
    draw.text((panel_x + 26, verified_y + 3), '✓ DNC-checked · TCPA-clean',
              fill=(20, 110, 102), font=f_verified)

    # ── Bottom CTA bar (white) ───────────────────────────────────────
    cta_h = 92
    cta_y = H - cta_h - 36
    rounded_rect(draw, (60, cta_y, W - 60, cta_y + cta_h), radius=cta_h // 2, fill=WHITE)
    f_cta = load_font(34, 'bold')
    cta = 'leadcove.io  ·  Free trial · $0 today'
    cw = text_w(draw, cta, f_cta)
    draw.text(((W - cw) // 2, cta_y + (cta_h - 34) // 2 - 6),
              cta, fill=NAVY, font=f_cta)

    # ── LeadCove logo (top-center, white-on-teal) ───────────────────
    # v1 used horizontal-light PNG which truncated to "LeadCov" — the
    # source PNG itself appears to have the wordmark cropped at the right
    # edge in both 600/1200/2400 variants. Switching to the STACKED
    # variant which is square (mark over wordmark) and renders cleanly.
    logo_path = os.path.join(BRAND_PNG, 'logo-stacked-light_480.png')
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert('RGBA')
        target_w = 96
        ratio = target_w / logo.width
        logo = logo.resize((target_w, int(logo.height * ratio)), Image.LANCZOS)
        bg.paste(logo, ((W - target_w) // 2, 28), logo)

    out_path = os.path.join(HERE, 'ig-launch-01-square.png')
    bg.save(out_path, 'PNG', optimize=True)
    print(f'✓ wrote {out_path}')
    return out_path


def render_story():
    """1080x1920 vertical variant — repurposes the square layout
    elements in a taller composition with breathing room top + bottom."""
    W, H = 1080, 1920
    bg = gradient_bg((W, H), TEAL, TEAL_DARK)
    draw = ImageDraw.Draw(bg)

    # Eyebrow sits BELOW the stacked logo (which is ~330px tall after
    # scaling). Pushed to y=430 to clear it cleanly.
    f_eye = load_font(30, 'bold')
    eyebrow = 'FOR WORKING REAL ESTATE AGENTS'
    ew = text_w(draw, eyebrow, f_eye)
    draw.text(((W - ew) // 2, 430), eyebrow, fill=(180, 230, 224), font=f_eye)

    f_h1 = load_font(96, 'heavy')
    line1 = '7 lookup sites.'
    line2 = 'Or one screen.'
    w1 = text_w(draw, line1, f_h1)
    w2 = text_w(draw, line2, f_h1)
    draw.text(((W - w1) // 2, 490), line1, fill=WHITE, font=f_h1)
    draw.text(((W - w2) // 2, 600), line2, fill=WHITE, font=f_h1)

    # Cards stacked vertically
    card_w = 880
    card_h = 380
    card_pad = 42

    # BEFORE card — pushed down to clear the bigger headline block above.
    lx = (W - card_w) // 2
    ly = 780
    rounded_rect(draw, (lx, ly, lx + card_w, ly + card_h), radius=32, fill=WHITE)
    f_chip = load_font(24, 'bold')
    f_sub  = load_font(34, 'bold')
    rounded_rect(draw, (lx + card_pad, ly + card_pad, lx + card_pad + 150, ly + card_pad + 40),
                 radius=20, fill=(238, 232, 220))
    draw.text((lx + card_pad + 24, ly + card_pad + 8), 'BEFORE',
              fill=(120, 100, 70), font=f_chip)
    draw.text((lx + card_pad, ly + card_pad + 64),
              '7 tabs · 2.5 hours · ~$62 in fees', fill=NAVY, font=f_sub)
    # Generic chips — see note in render_square() about avoiding
    # named third-party brands.
    placeholders = ['site-one.com', 'site-two.com', 'site-three.com',
                    'site-four.com', 'site-five.com', 'site-six.com']
    cx = lx + card_pad
    cy = ly + card_pad + 130
    for c in placeholders:
        chip_w = text_w(draw, c, f_chip) + 30
        if cx + chip_w > lx + card_w - card_pad:
            cx = lx + card_pad
            cy += 50
        draw_tab_chip(draw, cx, cy, chip_w, 38, c, f_chip,
                      label_color=(100, 110, 120))
        cx += chip_w + 12

    # AFTER card
    rx = lx
    ry = ly + card_h + 36
    rounded_rect(draw, (rx, ry, rx + card_w, ry + card_h), radius=32, fill=WHITE)
    rounded_rect(draw, (rx + card_pad, ry + card_pad, rx + card_pad + 130, ry + card_pad + 40),
                 radius=20, fill=(220, 245, 240))
    draw.text((rx + card_pad + 24, ry + card_pad + 8), 'AFTER',
              fill=(20, 110, 102), font=f_chip)
    draw.text((rx + card_pad, ry + card_pad + 64),
              '1 screen · 8 seconds · $0 today', fill=NAVY, font=f_sub)
    # Owner modal mock
    panel_x = rx + card_pad
    panel_y = ry + card_pad + 130
    panel_w = card_w - 2 * card_pad
    panel_h = 200
    rounded_rect(draw, (panel_x, panel_y, panel_x + panel_w, panel_y + panel_h),
                 radius=20, fill=(247, 250, 250), outline=(220, 230, 230), width=1)
    f_owner = load_font(30, 'bold')
    draw.text((panel_x + 22, panel_y + 18), 'Maria Espinoza',
              fill=NAVY, font=f_owner)
    f_row = load_font(24, 'bold')
    f_tag = load_font(18, 'bold')
    rows = [
        ('305 ••• 4821',  'MOBILE',   TEAL),
        ('305 ••• 6109',  'LANDLINE', (120, 130, 140)),
        ('m••••@email.com', 'EMAIL',  (90, 130, 200)),
    ]
    rh = 40
    rx2 = panel_x + 22
    ry2 = panel_y + 64
    for label, tag, color in rows:
        draw.text((rx2, ry2), label, fill=NAVY, font=f_row)
        tag_w = text_w(draw, tag, f_tag) + 18
        rounded_rect(draw, (panel_x + panel_w - 22 - tag_w, ry2 + 2,
                            panel_x + panel_w - 22, ry2 + 30),
                     radius=14, fill=color)
        draw.text((panel_x + panel_w - 22 - tag_w + 9, ry2 + 6),
                  tag, fill=WHITE, font=f_tag)
        ry2 += rh

    # CTA bar
    cta_h = 110
    cta_y = H - cta_h - 200
    rounded_rect(draw, (80, cta_y, W - 80, cta_y + cta_h), radius=cta_h // 2, fill=WHITE)
    f_cta = load_font(40, 'bold')
    cta = 'leadcove.io  ·  Free trial · $0 today'
    cw = text_w(draw, cta, f_cta)
    draw.text(((W - cw) // 2, cta_y + (cta_h - 40) // 2 - 8),
              cta, fill=NAVY, font=f_cta)

    # Logo — stacked variant (the horizontal PNG clips to "LeadCov")
    logo_path = os.path.join(BRAND_PNG, 'logo-stacked-light_960.png')
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert('RGBA')
        target_w = 200
        ratio = target_w / logo.width
        logo = logo.resize((target_w, int(logo.height * ratio)), Image.LANCZOS)
        bg.paste(logo, ((W - target_w) // 2, 90), logo)

    out_path = os.path.join(HERE, 'ig-launch-01-story.png')
    bg.save(out_path, 'PNG', optimize=True)
    print(f'✓ wrote {out_path}')
    return out_path


if __name__ == '__main__':
    render_square()
    render_story()
