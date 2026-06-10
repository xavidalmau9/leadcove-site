#!/usr/bin/env python3
"""
Auto-regenerate sitemap.xml from disk.

Walks the marketing site, gathers every HTML page that should be
indexed, and writes a fresh sitemap.xml with last-modified dates from
git history (or file mtime as fallback). Idempotent — safe to run in
CI on every push.

What gets included:
  - Top-level marketing pages (index, about, free-lookup, etc.)
  - blog/*.html (excluding blog/index.html which appears as blog/)
  - integrations/*.html
  - find-property-owner/*.html
  - llc-owner-lookup/*.html
  - help/*.html

What gets excluded:
  - Brand-asset directories
  - Screenshots
  - Internal mockup-render scratch
  - The IndexNow verification file

Run:
    python3 scripts/regenerate_sitemap.py

Outputs:
    sitemap.xml (overwritten)
"""
import datetime
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent.parent

BASE = 'https://leadcove.io'
SITEMAP = HERE / 'sitemap.xml'

# Top-level pages and their priority/changefreq overrides.
TOP_LEVEL = [
    ('/',                       'weekly',  1.0),
    ('/free-lookup.html',       'weekly',  0.95),
    ('/about.html',             'monthly', 0.7),
    ('/help/',                  'monthly', 0.6),
    ('/blog/',                  'weekly',  0.8),
    ('/press.html',             'monthly', 0.7),
    ('/terms.html',             'yearly',  0.3),
    ('/privacy.html',           'yearly',  0.3),
    ('/tcpa.html',              'yearly',  0.3),
]

# Directories to scan, with default priority + changefreq.
DIRS = [
    ('blog',                {'changefreq': 'monthly', 'priority': 0.8}),
    ('integrations',        {'changefreq': 'monthly', 'priority': 0.8}),
    ('find-property-owner',           {'changefreq': 'monthly', 'priority': 0.7}),
    ('llc-owner-lookup',              {'changefreq': 'monthly', 'priority': 0.7}),
    ('real-estate-prospecting-laws',  {'changefreq': 'monthly', 'priority': 0.7}),
    ('help',                {'changefreq': 'monthly', 'priority': 0.6}),
]

# Highlighted slugs that should be promoted to higher priority.
PROMOTED = {
    'skip-tracing-tools-comparison.html': 0.9,
    'crm-for-real-estate-agents-comparison.html': 0.9,
    'find-owner-mls-blank-privacy.html': 0.9,
    'find-property-owner-listing-address.html': 0.85,
}


def last_modified(path):
    """Get last-commit date for path via git; fall back to mtime."""
    try:
        rel = path.relative_to(HERE)
        out = subprocess.run(
            ['git', '-C', str(HERE), 'log', '-1', '--format=%cs', '--', str(rel)],
            check=True, capture_output=True, text=True, timeout=10,
        )
        date = out.stdout.strip()
        if date:
            return date
    except Exception:
        pass
    ts = datetime.datetime.fromtimestamp(path.stat().st_mtime)
    return ts.strftime('%Y-%m-%d')


def url_entry(loc, lastmod, changefreq, priority):
    return (
        '  <url>\n'
        f'    <loc>{loc}</loc>\n'
        + (f'    <lastmod>{lastmod}</lastmod>\n' if lastmod else '')
        + f'    <changefreq>{changefreq}</changefreq>\n'
        f'    <priority>{priority}</priority>\n'
        '  </url>\n'
    )


def main():
    today = datetime.date.today().strftime('%Y-%m-%d')
    parts = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
             '']

    # Top-level pages
    parts.append('  <!-- Top-level marketing pages -->')
    for path, freq, prio in TOP_LEVEL:
        # Try to use the canonical page on disk for mtime
        candidates = [
            HERE / path.lstrip('/').rstrip('/') / 'index.html',
            HERE / path.lstrip('/'),
        ]
        lastmod = today
        for c in candidates:
            if c.exists() and c.is_file():
                lastmod = last_modified(c)
                break
        parts.append(url_entry(f'{BASE}{path}', lastmod, freq, prio))

    # Directory-driven pages. Use rglob so we pick up nested folders
    # like help/<slug>/index.html — those serve at /help/<slug>/.
    for dirname, defaults in DIRS:
        d = HERE / dirname
        if not d.exists():
            continue
        parts.append(f'  <!-- {dirname}/ -->')
        for html in sorted(d.rglob('*.html')):
            rel = html.relative_to(d)
            if html.name == 'index.html' and rel == pathlib.Path('index.html'):
                continue  # blog/, help/ already covered in TOP_LEVEL
            lastmod = last_modified(html)
            # Build URL: foo.html → /dir/foo.html; sub/index.html → /dir/sub/
            if html.name == 'index.html':
                url_path = f'/{dirname}/{rel.parent.as_posix()}/'
            else:
                url_path = f'/{dirname}/{rel.as_posix()}'
            priority = PROMOTED.get(html.name, defaults['priority'])
            parts.append(url_entry(f'{BASE}{url_path}', lastmod, defaults['changefreq'], priority))

    parts.append('</urlset>')
    SITEMAP.write_text('\n'.join(parts))

    # Count for the operator
    count = SITEMAP.read_text().count('<loc>')
    print(f'✓ Sitemap regenerated: {count} URLs → {SITEMAP.name}')


if __name__ == '__main__':
    main()
