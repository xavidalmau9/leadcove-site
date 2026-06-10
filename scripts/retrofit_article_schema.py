#!/usr/bin/env python3
"""
One-shot retrofit: add JSON-LD Article schema to blog posts that don't
have it. LLMs use schema as a trust signal — pages with structured
metadata get cited more reliably.

Reads each <meta> tag in the existing post, builds the Article schema
from title, description, og:url, and the article:published_time (or
falls back to today's date if missing). Skips files that already have
an Article schema block. Idempotent.

Built 2026-06-08 as part of the LLM/AI traffic playbook.

Usage:
    python3 scripts/retrofit_article_schema.py
"""
import re
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent.parent
BLOG = HERE / 'blog'
DEFAULT_DATE = '2026-06-08'

# Posts to skip — they already have Article schema OR are the index.
SKIP = {
    'index.html',
    'expired-listings-skip-tracing.html',
    'free-property-owner-lookup.html',
    'llc-owner-lookup-unmask.html',
    'skip-tracing-real-estate-agents.html',
    'skip-tracing-tools-comparison.html',
}


def extract_meta(html, name=None, prop=None):
    """Pull the content attribute from a <meta name=...> or <meta property=...> tag."""
    if name:
        pat = re.compile(
            rf'<meta\s+name="{re.escape(name)}"\s+content="([^"]+)"', re.I)
    else:
        pat = re.compile(
            rf'<meta\s+property="{re.escape(prop)}"\s+content="([^"]+)"', re.I)
    m = pat.search(html)
    return m.group(1) if m else None


def extract_title(html):
    m = re.search(r'<title>([^<]+)</title>', html, re.I)
    if not m:
        return None
    # Strip trailing "· LeadCove"
    t = m.group(1).strip()
    t = re.sub(r'\s*·\s*LeadCove\s*$', '', t)
    return t


def build_article_schema(title, description, url, published, modified):
    return {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': title,
        'description': description,
        'datePublished': published,
        'dateModified': modified or published,
        'author': {
            '@type': 'Organization',
            'name': 'LeadCove',
            'url': 'https://leadcove.io',
        },
        'publisher': {
            '@type': 'Organization',
            'name': 'LeadCove',
            'url': 'https://leadcove.io',
        },
        'mainEntityOfPage': {
            '@type': 'WebPage',
            '@id': url,
        },
    }


def inject_schema(html, schema):
    """Insert the JSON-LD script tag just before </head>."""
    block = (
        '\n<!-- Article schema — added 2026-06-08 by retrofit script. -->\n'
        '<script type="application/ld+json">\n'
        + json.dumps(schema, indent=2)
        + '\n</script>\n'
    )
    if '</head>' not in html:
        return None
    return html.replace('</head>', block + '</head>', 1)


def main():
    updated = []
    skipped = []
    for path in sorted(BLOG.glob('*.html')):
        name = path.name
        if name in SKIP:
            skipped.append((name, 'already-has-schema-or-index'))
            continue

        html = path.read_text()
        if '"@type": "Article"' in html:
            skipped.append((name, 'already-has-article'))
            continue

        title = extract_title(html)
        description = (extract_meta(html, name='description')
                       or extract_meta(html, prop='og:description'))
        url = extract_meta(html, prop='og:url') or f'https://leadcove.io/blog/{name}'
        published = extract_meta(html, prop='article:published_time') or DEFAULT_DATE
        modified = extract_meta(html, prop='article:modified_time')

        if not title or not description:
            skipped.append((name, 'missing-title-or-description'))
            continue

        schema = build_article_schema(title, description, url, published, modified)
        new_html = inject_schema(html, schema)
        if new_html is None:
            skipped.append((name, 'no-head-tag-found'))
            continue
        path.write_text(new_html)
        updated.append(name)

    print(f'✓ Retrofitted Article schema on {len(updated)} post(s):')
    for n in updated:
        print(f'    {n}')
    print(f'⋯ Skipped {len(skipped)}:')
    for n, why in skipped:
        print(f'    {n}  ({why})')


if __name__ == '__main__':
    main()
