#!/usr/bin/env python3
"""
Per-page Open Graph image generator.

Reads every HTML file in blog/, extracts the title from the <title> tag,
and renders a custom 1200×630 OG image with the title in large type on
the LeadCove brand background. Saves each image to assets/og/<slug>.png.

Then walks each post and rewrites its <meta property="og:image"> +
<meta name="twitter:image"> to point at the per-page image.

Built 2026-06-08 after Xavi noted LinkedIn shared a generic preview
because every post used the same /assets/og.png.

Idempotent. Safe to re-run.

Usage:
    python3 scripts/generate_og_images.py
"""
import os
import re
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent.parent
BLOG = HERE / 'blog'
OG_DIR = HERE / 'assets' / 'og'
BRAND_PNG = HERE / 'assets' / 'brand' / 'png'

OG_DIR.mkdir(parents=True, exist_ok=True)

# Brand palette
TEAL      = (14, 159, 149)
TEAL_DARK = (8, 95, 89)
NAVY      = (11, 22, 41)
WHITE     = (255, 255, 255)
ACCENT_HI = (180, 230, 224)


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


def wrap_text(text, max_width, draw, font):
    """Word-wrap to fit max_width pixels."""
    words = text.split()
    lines, cur = [], ''
    for w in words:
        trial = (cur + ' ' + w).strip()
        if text_w(draw, trial, font) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


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


def extract_title(html):
    m = re.search(r'<title>([^<]+)</title>', html, re.I)
    if not m:
        return None
    t = m.group(1).strip()
    t = re.sub(r'\s*·\s*LeadCove\s*$', '', t)
    return t


def extract_eyebrow(html):
    """Pick up the post-eyebrow tag if present (e.g. 'Workflow', 'Comparison')."""
    m = re.search(r'<p class="post-eyebrow">([^<]+)</p>', html, re.I)
    if not m:
        return None
    return m.group(1).strip().upper()


def render_og(title, eyebrow, out_path):
    W, H = 1200, 630
    bg = gradient_bg((W, H), TEAL, TEAL_DARK)
    draw = ImageDraw.Draw(bg)

    # Logo top-left — stacked variant. The horizontal-light PNG has the
    # wordmark cropped at the right edge in every size variant; the
    # stacked variant is whole. Same issue surfaced when building the
    # IG launch graphics. Stacked is ~0.6 aspect so 100w × 167h fits
    # cleanly above the title without crowding.
    logo_path = BRAND_PNG / 'logo-stacked-light_480.png'
    if logo_path.exists():
        logo = Image.open(logo_path).convert('RGBA')
        target_w = 100
        ratio = target_w / logo.width
        logo = logo.resize((target_w, int(logo.height * ratio)), Image.LANCZOS)
        bg.paste(logo, (60, 50), logo)

    # Eyebrow (top-right, small caps)
    if eyebrow:
        f_eye = load_font(22, 'bold')
        ew = text_w(draw, eyebrow, f_eye)
        draw.text((W - 60 - ew, 60), eyebrow, fill=ACCENT_HI, font=f_eye)

    # Title — large, wrapped to ~3 lines max. Pick font size by length.
    title_len = len(title)
    if   title_len <= 50:  fsize = 62
    elif title_len <= 80:  fsize = 54
    elif title_len <= 110: fsize = 46
    else:                  fsize = 40

    f_title = load_font(fsize, 'heavy')
    max_w = W - 120
    lines = wrap_text(title, max_w, draw, f_title)

    # If 4+ lines, drop font size again
    if len(lines) > 4:
        f_title = load_font(int(fsize * 0.85), 'heavy')
        lines = wrap_text(title, max_w, draw, f_title)

    # Vertical-center the title block
    line_h = int(fsize * 1.15)
    total_h = line_h * len(lines)
    start_y = (H - total_h) // 2 + 20  # tiny offset down to balance against logo
    for i, line in enumerate(lines):
        draw.text((60, start_y + i * line_h), line, fill=WHITE, font=f_title)

    # CTA strip bottom
    f_cta = load_font(24, 'bold')
    cta = 'leadcove.io  ·  property-owner data for working agents'
    cw = text_w(draw, cta, f_cta)
    draw.text(((W - cw) // 2, H - 60), cta, fill=ACCENT_HI, font=f_cta)

    bg.save(out_path, 'PNG', optimize=True)


def slug_for(html_path):
    """blog/foo.html → 'foo'"""
    return html_path.stem


def update_og_meta(html_path, image_url):
    """Rewrite og:image + twitter:image meta tags in place."""
    html = html_path.read_text()
    new = re.sub(
        r'<meta property="og:image"\s+content="[^"]+"\s*/?>',
        f'<meta property="og:image" content="{image_url}" />',
        html,
        flags=re.I,
    )
    new = re.sub(
        r'<meta name="twitter:image"\s+content="[^"]+"\s*/?>',
        f'<meta name="twitter:image" content="{image_url}" />',
        new,
        flags=re.I,
    )
    if new != html:
        html_path.write_text(new)
        return True
    return False


def main():
    posts = sorted(p for p in BLOG.glob('*.html') if p.name != 'index.html')
    rendered = []
    updated_meta = []
    skipped = []

    for p in posts:
        html = p.read_text()
        title = extract_title(html)
        if not title:
            skipped.append((p.name, 'no-title'))
            continue
        eyebrow = extract_eyebrow(html)
        slug = slug_for(p)
        out = OG_DIR / f'{slug}.png'
        render_og(title, eyebrow, out)
        rendered.append(p.name)
        if update_og_meta(p, f'https://leadcove.io/assets/og/{slug}.png'):
            updated_meta.append(p.name)

    print(f'✓ Rendered {len(rendered)} OG image(s)')
    for n in rendered:
        print(f'    {n}')
    print(f'✓ Updated OG meta on {len(updated_meta)} post(s)')
    if skipped:
        print(f'⋯ Skipped {len(skipped)}:')
        for n, why in skipped:
            print(f'    {n}  ({why})')


if __name__ == '__main__':
    main()
