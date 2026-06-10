#!/usr/bin/env python3
"""
LeadCove · Instagram graphics — simplicity theme, 3 variants.

Xavi 2026-06-06: "give me 3 variations of something new to get someone
to try our platform... maybe try using skip tracing simplicity?"

Iron-rule notes:
  - feedback_no_skip_trace_in_user_strings.md — concept retained, word
    not used. We say "owner data" / "find the owner".
  - feedback_no_free_in_user_strings.md — substitutes are "$0 today"
    and "7-day trial".

Renders three 1080×1080 squares:
  ig-simplicity-A-timer.png       The 8-second stopwatch hero.
  ig-simplicity-B-paste.png       Paste address → get owner. One action.
  ig-simplicity-C-skip.png        "Skip the tabs. Find the owner."

All three use the same brand palette + logo placement so they read as
a campaign series.
"""
import os
import math
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND_PNG = os.path.normpath(os.path.join(HERE, '..', 'brand', 'png'))

# Brand palette
TEAL       = (14, 159, 149)
TEAL_DARK  = (8, 95, 89)
NAVY       = (11, 22, 41)
NAVY_PANEL = (17, 35, 57)
NAVY_DEEP  = (8, 18, 34)
HAIRLINE   = (38, 55, 78)
WHITE      = (255, 255, 255)
SAND       = (245, 240, 232)
INK_DIM    = (148, 168, 185)
ACCENT_HI  = (180, 230, 224)
GREEN_PILL = (28, 128, 92)
GREEN_TEXT = (180, 240, 210)


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
        draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)
    except AttributeError:
        x0, y0, x1, y1 = xy
        draw.rectangle((x0 + radius, y0, x1 - radius, y1), fill=fill)
        draw.rectangle((x0, y0 + radius, x1, y1 - radius), fill=fill)
        for cx, cy in [(x0, y0), (x1 - 2 * radius, y0),
                       (x0, y1 - 2 * radius), (x1 - 2 * radius, y1 - 2 * radius)]:
            draw.pieslice((cx, cy, cx + 2 * radius, cy + 2 * radius), 0, 360, fill=fill)


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


def paste_logo(bg, target_w, top_y):
    """Centered stacked-logo at the top of the canvas."""
    W, _ = bg.size
    logo_path = os.path.join(BRAND_PNG, 'logo-stacked-light_480.png')
    if not os.path.exists(logo_path): return
    logo = Image.open(logo_path).convert('RGBA')
    ratio = target_w / logo.width
    logo = logo.resize((target_w, int(logo.height * ratio)), Image.LANCZOS)
    bg.paste(logo, ((W - target_w) // 2, top_y), logo)


def draw_cta(bg, draw, cta_text, cta_h=72):
    W, H = bg.size
    cta_y = H - cta_h - 40
    rounded_rect(draw, (60, cta_y, W - 60, cta_y + cta_h),
                 radius=cta_h // 2, fill=WHITE)
    f_cta = load_font(28, 'bold')
    cw = text_w(draw, cta_text, f_cta)
    draw.text(((W - cw) // 2, cta_y + (cta_h - 28) // 2 - 4),
              cta_text, fill=NAVY, font=f_cta)


# ── Variant A — The 8-second timer ─────────────────────────────────────
# Concept: a single huge ring with "00:08" inside, on teal gradient.
# Reads as "this is how long owner lookup takes." Minimal copy.
def render_A():
    W, H = 1080, 1080
    bg = gradient_bg((W, H), TEAL, TEAL_DARK)
    draw = ImageDraw.Draw(bg)

    paste_logo(bg, 88, 36)

    f_eye = load_font(24, 'bold')
    eye = 'OWNER LOOKUP — ENTIRE WORKFLOW'
    draw.text(((W - text_w(draw, eye, f_eye)) // 2, 200),
              eye, fill=ACCENT_HI, font=f_eye)

    # Big timer ring
    cx, cy = W // 2, 560
    r_outer = 240
    r_inner = 200
    # Outer ring (teal-light)
    draw.ellipse((cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer),
                 fill=(40, 175, 165))
    # Inner disc (deep navy)
    draw.ellipse((cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner),
                 fill=NAVY)
    # Filled arc to imply progress (3/4 full → 6 seconds elapsed)
    # Drawn as a pieslice on top of the outer ring so the unfilled
    # quarter shows the teal-light hue.
    draw.pieslice((cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer),
                  -90, -90 + 270, fill=WHITE)
    # Re-draw inner disc so the pie shows only as the ring annulus
    draw.ellipse((cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner),
                 fill=NAVY)
    # Tick marks around the inner edge
    for i in range(12):
        ang = math.radians(i * 30 - 90)
        x1 = cx + (r_inner - 8)  * math.cos(ang)
        y1 = cy + (r_inner - 8)  * math.sin(ang)
        x2 = cx + (r_inner - 22) * math.cos(ang)
        y2 = cy + (r_inner - 22) * math.sin(ang)
        draw.line((x1, y1, x2, y2), fill=INK_DIM, width=2)

    # The number itself
    f_num = load_font(150, 'heavy')
    num = '8s'
    nw = text_w(draw, num, f_num)
    draw.text((cx - nw // 2, cy - 95), num, fill=WHITE, font=f_num)

    # Subhead under the ring
    f_sub = load_font(32, 'bold')
    sub = 'address → owner + every phone + email'
    sw = text_w(draw, sub, f_sub)
    draw.text(((W - sw) // 2, 830), sub, fill=WHITE, font=f_sub)

    draw_cta(bg, draw, 'leadcove.io  ·  7-day trial · $0 today')

    out = os.path.join(HERE, 'ig-simplicity-A-timer.png')
    bg.save(out, 'PNG', optimize=True)
    print(f'✓ {out}')


# ── Variant B — Paste address → owner ──────────────────────────────────
# Concept: a literal copy/paste flow. Address chip on left, arrow, owner
# card on right showing the FULL contact stack — 4 phones + 2 emails
# with mixed CLEAN/DNC + Mobile/Landline status pills. The asymmetry
# between the small address input and the big rich-result card visually
# communicates "tiny input → complete answer."
def render_B():
    W, H = 1080, 1080
    bg = gradient_bg((W, H), TEAL, TEAL_DARK)
    draw = ImageDraw.Draw(bg)

    paste_logo(bg, 88, 36)

    f_eye = load_font(24, 'bold')
    eye = 'ONE PASTE. EVERY OWNER.'
    draw.text(((W - text_w(draw, eye, f_eye)) // 2, 200),
              eye, fill=ACCENT_HI, font=f_eye)

    f_h1 = load_font(64, 'heavy')
    head1 = 'Drop the address.'
    head2 = 'Get every contact.'
    draw.text(((W - text_w(draw, head1, f_h1)) // 2, 245),
              head1, fill=WHITE, font=f_h1)
    draw.text(((W - text_w(draw, head2, f_h1)) // 2, 320),
              head2, fill=WHITE, font=f_h1)

    # Left card — the address as if pasted from clipboard.
    # Stays small (single input). y aligned with the TOP of the right
    # card so the arrow points level into the rich result panel.
    addr_w = 320
    addr_h = 200
    lx = 60
    ly = 430
    rounded_rect(draw, (lx, ly, lx + addr_w, ly + addr_h),
                 radius=22, fill=WHITE)
    f_label = load_font(14, 'bold')
    draw.text((lx + 22, ly + 22), 'PASTED ADDRESS', fill=(120, 140, 158), font=f_label)
    f_addr = load_font(24, 'bold')
    draw.text((lx + 22, ly + 56), '1234 EXAMPLE ST', fill=NAVY, font=f_addr)
    draw.text((lx + 22, ly + 88), 'UNIT 1509', fill=NAVY, font=f_addr)
    f_city = load_font(18, 'regular')
    draw.text((lx + 22, ly + 134), 'MIAMI, FL 33132', fill=(95, 115, 132), font=f_city)

    # Arrow points from the right edge of address card into the
    # right-card's top section (aligned with the owner name).
    ax = lx + addr_w + 12
    arrow_y = ly + 90
    draw.line((ax, arrow_y, ax + 56, arrow_y), fill=WHITE, width=5)
    draw.polygon([(ax + 56, arrow_y - 14),
                  (ax + 84, arrow_y),
                  (ax + 56, arrow_y + 14)], fill=WHITE)

    # Right card — the rich result. Grows tall and wide to fit the
    # full contact stack so the operator value lands at a glance.
    result_w = 560
    result_h = 470
    rx = W - 60 - result_w
    rounded_rect(draw, (rx, ly, rx + result_w, ly + result_h),
                 radius=22, fill=NAVY_PANEL, outline=HAIRLINE, width=1)
    # Header strip
    draw.text((rx + 24, ly + 20), 'OWNER FOUND', fill=ACCENT_HI, font=f_label)
    f_owner_name = load_font(30, 'bold')
    draw.text((rx + 24, ly + 44), 'Jane Smith', fill=WHITE, font=f_owner_name)
    # Subtle hairline under name
    draw.line((rx + 24, ly + 88, rx + result_w - 24, ly + 88),
              fill=HAIRLINE, width=1)

    # Phones section
    f_section = load_font(12, 'bold')
    draw.text((rx + 24, ly + 100), 'PHONES', fill=INK_DIM, font=f_section)

    # 4 rows: number  +  tag (Mobile/Landline)  +  status pill (CLEAN/DNC)
    phones = [
        ('(555) 010-4821',  'Mobile',   'CLEAN'),
        ('(555) 010-6109',  'Mobile',   'CLEAN'),
        ('(555) 010-7733',  'Landline', 'CLEAN'),
        ('(555) 010-2241',  'Mobile',   'DNC'),
    ]
    f_phone = load_font(20, 'bold')
    f_tag   = load_font(13, 'regular')
    f_pill  = load_font(12, 'bold')
    py = ly + 126
    AMBER_PILL = (138, 80, 30)
    AMBER_TEXT = (250, 200, 130)
    for num, tag, status in phones:
        draw.text((rx + 24, py), num, fill=WHITE, font=f_phone)
        draw.text((rx + 24 + text_w(draw, num, f_phone) + 12, py + 6),
                  '· ' + tag, fill=INK_DIM, font=f_tag)
        # Status pill at right edge
        fill = GREEN_PILL if status == 'CLEAN' else AMBER_PILL
        textc = GREEN_TEXT if status == 'CLEAN' else AMBER_TEXT
        pw = text_w(draw, status, f_pill) + 20
        rounded_rect(draw, (rx + result_w - 24 - pw, py + 1,
                            rx + result_w - 24, py + 25),
                     radius=12, fill=fill)
        draw.text((rx + result_w - 24 - pw + 10, py + 4),
                  status, fill=textc, font=f_pill)
        py += 34

    # Divider before emails
    py += 6
    draw.line((rx + 24, py, rx + result_w - 24, py),
              fill=HAIRLINE, width=1)
    py += 14

    # Emails section
    draw.text((rx + 24, py), 'EMAILS', fill=INK_DIM, font=f_section)
    py += 26

    emails = [
        ('jsmith@example.com', 'VERIFIED'),
        ('jane.s@example.com', 'VERIFIED'),
    ]
    for em, status in emails:
        draw.text((rx + 24, py), em, fill=WHITE, font=f_phone)
        pw = text_w(draw, status, f_pill) + 20
        rounded_rect(draw, (rx + result_w - 24 - pw, py + 1,
                            rx + result_w - 24, py + 25),
                     radius=12, fill=GREEN_PILL)
        draw.text((rx + result_w - 24 - pw + 10, py + 4),
                  status, fill=GREEN_TEXT, font=f_pill)
        py += 32

    draw_cta(bg, draw, 'leadcove.io  ·  7-day trial · $0 today')

    out = os.path.join(HERE, 'ig-simplicity-B-paste.png')
    bg.save(out, 'PNG', optimize=True)
    print(f'✓ {out}')


# ── Variant C — Skip the tabs ──────────────────────────────────────────
# Concept: the realtor's old workflow was 7 tabs; the new one is 1 window.
# Pun on "skip" (the verb) without using the regulated "skip-trace" term.
def render_C():
    W, H = 1080, 1080
    bg = gradient_bg((W, H), TEAL, TEAL_DARK)
    draw = ImageDraw.Draw(bg)

    paste_logo(bg, 88, 36)

    f_eye = load_font(24, 'bold')
    eye = 'OWNER LOOKUP, MINUS THE FRICTION'
    draw.text(((W - text_w(draw, eye, f_eye)) // 2, 200),
              eye, fill=ACCENT_HI, font=f_eye)

    f_h1 = load_font(82, 'heavy')
    line1 = 'Skip the tabs.'
    line2 = 'Find the owner.'
    draw.text(((W - text_w(draw, line1, f_h1)) // 2, 250),
              line1, fill=WHITE, font=f_h1)
    draw.text(((W - text_w(draw, line2, f_h1)) // 2, 350),
              line2, fill=WHITE, font=f_h1)

    # Left mini panel — stacked browser tabs with a giant X overlay
    panel_w = 420
    panel_h = 380
    lx = 70
    ly = 510
    rounded_rect(draw, (lx, ly, lx + panel_w, ly + panel_h),
                 radius=24, fill=SAND)
    # Title strip
    f_chip = load_font(14, 'bold')
    draw.text((lx + 30, ly + 26), 'OLD WAY', fill=(120, 100, 70), font=f_chip)
    # 7 stacked tab chips
    chip_y = ly + 60
    for i in range(7):
        rounded_rect(draw,
                     (lx + 30, chip_y, lx + panel_w - 30, chip_y + 32),
                     radius=8, fill=WHITE)
        f_tab = load_font(15, 'regular')
        draw.text((lx + 46, chip_y + 8),
                  f'lookup-site-{i+1}.com', fill=(130, 140, 152), font=f_tab)
        chip_y += 40
    # Giant red X across the tabs
    x_color = (200, 70, 70)
    draw.line((lx + 30, ly + 60, lx + panel_w - 30, ly + panel_h - 40),
              fill=x_color, width=8)
    draw.line((lx + panel_w - 30, ly + 60, lx + 30, ly + panel_h - 40),
              fill=x_color, width=8)

    # Right panel — the LeadCove single window
    rx = W - 70 - panel_w
    rounded_rect(draw, (rx, ly, rx + panel_w, ly + panel_h),
                 radius=24, fill=NAVY_PANEL, outline=HAIRLINE, width=1)
    draw.text((rx + 30, ly + 26), 'LEADCOVE', fill=ACCENT_HI, font=f_chip)
    # Owner name
    f_owner = load_font(28, 'bold')
    draw.text((rx + 30, ly + 60), 'Jane Smith', fill=WHITE, font=f_owner)
    f_addr2 = load_font(14, 'regular')
    draw.text((rx + 30, ly + 100), '1234 EXAMPLE ST · MIAMI, FL', fill=INK_DIM, font=f_addr2)

    # 3 stacked detail rows
    row_y = ly + 145
    rows = [
        ('(555) 010-4821', 'Mobile · clean'),
        ('(555) 010-6109', 'Landline · clean'),
        ('jsmith@example.com', 'Email · verified'),
    ]
    for label, sub in rows:
        f_row = load_font(20, 'bold')
        draw.text((rx + 30, row_y), label, fill=WHITE, font=f_row)
        f_sub = load_font(13, 'regular')
        draw.text((rx + 30, row_y + 26), sub, fill=INK_DIM, font=f_sub)
        row_y += 56

    # Result strip at bottom
    strip_y = ly + panel_h - 50
    rounded_rect(draw, (rx + 24, strip_y, rx + panel_w - 24, strip_y + 32),
                 radius=10, fill=(20, 60, 70))
    f_strip = load_font(13, 'bold')
    msg = 'resolved in 8 seconds'
    sw = text_w(draw, msg, f_strip)
    draw.text((rx + 24 + ((panel_w - 48) - sw) // 2, strip_y + 8),
              msg, fill=(190, 240, 220), font=f_strip)

    draw_cta(bg, draw, 'leadcove.io  ·  7-day trial · $0 today')

    out = os.path.join(HERE, 'ig-simplicity-C-skip.png')
    bg.save(out, 'PNG', optimize=True)
    print(f'✓ {out}')


if __name__ == '__main__':
    render_A()
    render_B()
    render_C()
