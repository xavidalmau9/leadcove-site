#!/usr/bin/env python3
"""
Wire the AI-referrer detection script into every HTML page that doesn't
already have it. Currently only the homepage and free-lookup carry it;
this script adds the include to every blog post + integration page so
visitors landing anywhere on the site get tagged with their AI source.

Insertion point: after the Microsoft Clarity script block (consistent
anchor across pages). Idempotent — skips pages that already include
the script.

Usage:
    python3 scripts/add_ai_referrer_to_all_pages.py
"""
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent.parent

TAG = (
    '\n  <!-- AI-referrer tagging — detects ChatGPT/Claude/Perplexity/Gemini'
    '\n       visitors and tags signup links with utm_source. See'
    '\n       /assets/ai-referrer-tag.js. -->'
    '\n  <script src="/assets/ai-referrer-tag.js" defer></script>'
)

# Anchor: end of the Clarity script block (a closing </script> right after
# the clarity tag call). Match the specific tag id so we don't double-paste
# into pages with multiple scripts.
ANCHOR_RE = re.compile(
    r'(\}\)\(window, document, "clarity", "script", "wq57o9awo1"\);\s*</script>)',
    re.M,
)


def files_to_patch():
    paths = []
    paths.extend((HERE / 'blog').glob('*.html'))
    paths.extend((HERE / 'integrations').glob('*.html'))
    paths.extend((HERE / 'help').glob('*.html'))
    paths.extend((HERE / 'llc-owner-lookup').glob('*.html'))
    # Top-level pages that have analytics but might miss the AI tag
    for name in ['about.html', 'tcpa.html', 'privacy.html', 'terms.html']:
        p = HERE / name
        if p.exists(): paths.append(p)
    return sorted(set(paths))


def patch(path):
    src = path.read_text()
    if '/assets/ai-referrer-tag.js' in src:
        return 'already-has'
    if not ANCHOR_RE.search(src):
        return 'no-clarity-anchor'
    new = ANCHOR_RE.sub(r'\1' + TAG, src, count=1)
    path.write_text(new)
    return 'patched'


def main():
    patched, skipped = [], []
    for p in files_to_patch():
        result = patch(p)
        rel = p.relative_to(HERE)
        if result == 'patched':
            patched.append(str(rel))
        else:
            skipped.append((str(rel), result))
    print(f'✓ Patched {len(patched)} file(s):')
    for n in patched: print(f'    {n}')
    if skipped:
        print(f'⋯ Skipped {len(skipped)}:')
        for n, why in skipped: print(f'    {n}  ({why})')


if __name__ == '__main__':
    main()
