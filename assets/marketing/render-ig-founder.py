#!/usr/bin/env python3
"""
LeadCove · Founder quote IG card.

Xavi 2026-06-08: "we need to try something new." Previous variants all
showed the product modal. This pivots to a human voice — Jules,
founder, working Miami agent — speaking directly. No dashboard, no
panels, no metric pills.

Portrait is a placeholder circular avatar with initials (JC) until
Jules sends a real headshot. Once received, swap PORTRAIT_PATH below.

1080×1080 square.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND_PNG = os.path.normpath(os.path.join(HERE, '..', 'brand', 'png'))

# Brand palette
TEAL       = (14, 159, 149)
TEAL_DARK  = (8, 95, 89)
NAVY       = (11, 22, 41)
WHITE      = (255, 255, 255)
ACCENT_HI  = (180, 230, 224)
SAND       = (245, 240, 232)

PORTRAIT_PATH = os.path.join(HERE, 'jules-portrait.png')   # swap when ready
PORTRAIT_INITIALS = 'JC'


def load_font(size, weight='regular'):
    candidates = {
        'bold':    ['/System/Library/Fonts/Supplemental/Arial Bold.ttf',
                    '/System/Library/Fonts/HelveticaNeue.ttc'],
        'regular': ['/System/Library/Fonts/Supplemental/Arial.ttf',
                    '/System/Library/Fonts/HelveticaNeue.ttc'],
        'italic':  ['/System/Library/Fonts/Supplemental/Arial Italic.ttf',
                    '/System/Library/Fonts/Supplemental/Arial.ttf'],
        'bolditalic': ['/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf',
                       '/System/Library/Fonts/Supplemental/Arial Bold.ttf'],
        'heavy':   ['/System/Library/Fonts/Supplemental/Arial Black.ttf'],
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


def wrap_lines(text, max_width, draw, font):
    """Word-wrap a long quote to fit max_width pixels."""
    words = text.split()
    lines, cur = [], ''
    for w in words:
        trial = (cur + ' ' + w).strip()
        if text_w(draw, trial, font) <= max_width:
            cur = trial
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines


def circle_portrait(size, initials):
    """Generate a placeholder circular portrait with initials."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Circular sand-tone disc with subtle inner ring
    d.ellipse((0, 0, size, size), fill=SAND, outline=WHITE, width=4)
    f_init = load_font(int(size * 0.42), 'heavy')
    iw = text_w(d, initials, f_init)
    d.text(((size - iw) // 2, int(size * 0.22)),
           initials, fill=NAVY, font=f_init)
    return img


def circle_crop(im, size):
    """Crop a square photo into a circle of `size` px."""
    im = im.convert('RGBA').resize((size, size), Image.LANCZOS)
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
    out = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    out.paste(im, (0, 0), mask)
    return out


def render():
    W, H = 1080, 1080
    bg = gradient_bg((W, H), TEAL, TEAL_DARK)
    draw = ImageDraw.Draw(bg)

    # LeadCove logo top-center (smaller, less prominent — the human voice
    # is the hero on this one)
    logo_path = os.path.join(BRAND_PNG, 'logo-stacked-light_480.png')
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert('RGBA')
        tw = 80
        ratio = tw / logo.width
        logo = logo.resize((tw, int(logo.height * ratio)), Image.LANCZOS)
        bg.paste(logo, ((W - tw) // 2, 34), logo)

    # Big opening quotation mark — sets the "this is a quote" tone
    f_quote_mark = load_font(220, 'heavy')
    draw.text((80, 180), '“', fill=ACCENT_HI, font=f_quote_mark)

    # The quote itself, wrapped over 4-5 lines.
    quote = (
        'I'  # smart apostrophe rendered below
        ' was spending two hours every Tuesday morning hunting down '
        'owner phones across seven lookup sites. I built LeadCove so I '
        'never have to do that again.'
    )
    # Use a real italic font, with curly quotes for newsprint feel
    f_quote = load_font(40, 'bolditalic')
    quote_text = (
        '’m a working Miami agent. I was spending two hours every '
        'Tuesday morning hunting owner phones across seven lookup sites. '
        'I built LeadCove so I never have to do that again.'
    )
    # Note: opens with apostrophe -> "I'm" reads cleanly. Prefix with "I"
    quote_text = 'I' + quote_text
    max_w = W - 160
    lines = wrap_lines(quote_text, max_w, draw, f_quote)
    y = 330
    line_h = 56
    for line in lines:
        draw.text((80, y), line, fill=WHITE, font=f_quote)
        y += line_h

    # Closing quotation mark, mirrored
    f_close = load_font(220, 'heavy')
    close_w = text_w(draw, '”', f_close)
    draw.text((W - 80 - close_w, y - 60),
              '”', fill=ACCENT_HI, font=f_close)

    # Attribution block (left-aligned) — portrait + name + title
    attr_y = y + 80
    if os.path.exists(PORTRAIT_PATH):
        portrait = circle_crop(Image.open(PORTRAIT_PATH), 130)
    else:
        portrait = circle_portrait(130, PORTRAIT_INITIALS)
    bg.paste(portrait, (80, attr_y), portrait)

    f_name = load_font(32, 'bold')
    f_title = load_font(20, 'regular')
    draw.text((240, attr_y + 30), 'Jules Cordero', fill=WHITE, font=f_name)
    draw.text((240, attr_y + 70),
              'Founder, LeadCove · Miami real estate agent',
              fill=ACCENT_HI, font=f_title)

    # Bottom CTA strip
    cta_h = 72
    cta_y = H - cta_h - 40
    rounded_rect(draw, (60, cta_y, W - 60, cta_y + cta_h),
                 radius=cta_h // 2, fill=WHITE)
    f_cta = load_font(28, 'bold')
    cta = 'leadcove.io  ·  7-day trial · $0 today'
    cw = text_w(draw, cta, f_cta)
    draw.text(((W - cw) // 2, cta_y + (cta_h - 28) // 2 - 4),
              cta, fill=NAVY, font=f_cta)

    out = os.path.join(HERE, 'ig-founder-quote.png')
    bg.save(out, 'PNG', optimize=True)
    print(f'✓ {out}')


if __name__ == '__main__':
    render()
