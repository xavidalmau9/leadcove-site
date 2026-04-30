#!/usr/bin/env python3
"""
Brand kit PNG renderer.

Reads every SVG in svg/ and emits PNGs into png/ at standard sizes
suitable for favicons, social profile pictures, slide decks, email
signatures, app icons, and print.

Run with the venv:
  /tmp/lc-svg-env/bin/python3 render-png.py

Requires Fraunces font to be installed system-wide for the wordmark
and combined-logo SVGs to render with the correct typeface. Cairo
falls back to Times/Georgia otherwise — the marks-only files render
correctly regardless.
"""
import cairosvg
import os
import sys

HERE     = os.path.dirname(os.path.abspath(__file__))
SVG_DIR  = os.path.join(HERE, 'svg')
PNG_DIR  = os.path.join(HERE, 'png')

# (svg_filename, [(suffix, output_width, output_height_or_None), ...])
JOBS = [
    # ── Square marks — favicons, app icons, social avatars ────────────
    ('mark.svg', [
        ('16',   16,   16),
        ('32',   32,   32),
        ('64',   64,   64),
        ('128', 128,  128),
        ('256', 256,  256),
        ('512', 512,  512),
        ('1024', 1024, 1024),
    ]),
    ('mark-light.svg', [
        ('256', 256, 256),
        ('512', 512, 512),
        ('1024', 1024, 1024),
    ]),
    ('mark-mono-navy.svg', [
        ('256', 256, 256),
        ('512', 512, 512),
        ('1024', 1024, 1024),
    ]),
    ('mark-mono-white.svg', [
        ('256', 256, 256),
        ('512', 512, 512),
        ('1024', 1024, 1024),
    ]),

    # ── Wordmark only — for places where the mark is already adjacent
    # ── or context makes it redundant.
    ('wordmark.svg', [
        ('480',  480,  None),
        ('960',  960,  None),
        ('1920', 1920, None),
    ]),
    ('wordmark-light.svg', [
        ('480',  480,  None),
        ('960',  960,  None),
        ('1920', 1920, None),
    ]),

    # ── Horizontal lockup — site headers, email signatures, decks
    ('logo-horizontal.svg', [
        ('600',  600,  None),
        ('1200', 1200, None),
        ('2400', 2400, None),
    ]),
    ('logo-horizontal-light.svg', [
        ('600',  600,  None),
        ('1200', 1200, None),
        ('2400', 2400, None),
    ]),

    # ── Stacked lockup — square avatars, app splash, business cards
    ('logo-stacked.svg', [
        ('480',  480,  480),
        ('960',  960,  960),
        ('1920', 1920, 1920),
    ]),
    ('logo-stacked-light.svg', [
        ('480',  480,  480),
        ('960',  960,  960),
        ('1920', 1920, 1920),
    ]),
]

def main():
    os.makedirs(PNG_DIR, exist_ok=True)
    rendered = 0
    skipped  = 0
    for svg_name, outputs in JOBS:
        src = os.path.join(SVG_DIR, svg_name)
        if not os.path.isfile(src):
            print(f'  ⚠  missing: {svg_name}', file=sys.stderr)
            skipped += len(outputs)
            continue
        base = os.path.splitext(svg_name)[0]
        for suffix, w, h in outputs:
            out = os.path.join(PNG_DIR, f'{base}_{suffix}.png')
            try:
                cairosvg.svg2png(
                    url=src,
                    write_to=out,
                    output_width=w,
                    output_height=h,
                )
                size = os.path.getsize(out)
                print(f'  ✓ {base}_{suffix}.png  ({size//1024} KB)')
                rendered += 1
            except Exception as e:
                print(f'  ✗ {base}_{suffix}.png  → {e}', file=sys.stderr)
                skipped += 1

    print()
    print(f'Done: {rendered} rendered, {skipped} skipped.')

if __name__ == '__main__':
    main()
