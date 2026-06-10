#!/usr/bin/env python3
"""
IndexNow submission — push every URL in our sitemap to Bing (which
powers ChatGPT search + Copilot), Yandex, Naver, and Seznam in one
shot. No dashboard login required; the verification file at
/{KEY}.txt proves we own the domain.

How IndexNow works:
  1. We host a verification file at https://leadcove.io/{KEY}.txt
     containing the key as its only content.
  2. We POST { host, key, keyLocation, urlList } to api.indexnow.org.
  3. Participating search engines re-fetch every URL within minutes.

Run this:
  - After deploying new blog posts (so Bing crawls them within minutes
    instead of weeks)
  - After any pricing or product change that affects an indexed page
  - As a one-shot baseline submission (this PR is the baseline)

Usage:
    python3 scripts/submit_indexnow.py             # submit every URL in sitemap.xml
    python3 scripts/submit_indexnow.py URL1 URL2…  # submit specific URLs

Built 2026-06-08 alongside the LLM/AI traffic playbook.
"""
import json
import pathlib
import re
import sys
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent.parent
SITEMAP = HERE / 'sitemap.xml'
KEY = '06a50c497f15c9a612cfe102a2d33ede'
HOST = 'leadcove.io'
KEY_LOCATION = f'https://{HOST}/{KEY}.txt'
ENDPOINT = 'https://api.indexnow.org/IndexNow'

# Max 10,000 URLs per request per the spec; we batch defensively.
BATCH_SIZE = 1000


def urls_from_sitemap():
    body = SITEMAP.read_text()
    return re.findall(r'<loc>([^<]+)</loc>', body)


def submit(urls):
    if not urls:
        print('No URLs to submit.')
        return
    print(f'Submitting {len(urls)} URL(s) to IndexNow…')
    for i in range(0, len(urls), BATCH_SIZE):
        chunk = urls[i:i + BATCH_SIZE]
        payload = {
            'host':        HOST,
            'key':         KEY,
            'keyLocation': KEY_LOCATION,
            'urlList':     chunk,
        }
        req = urllib.request.Request(
            ENDPOINT,
            data=json.dumps(payload).encode('utf-8'),
            method='POST',
            headers={
                'Content-Type': 'application/json; charset=utf-8',
                'User-Agent':   'LeadCove-IndexNow/1.0',
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                status = r.status
                body = r.read().decode('utf-8', errors='replace')
            print(f'  Batch {i // BATCH_SIZE + 1}: HTTP {status} ({len(chunk)} URLs)')
            if body.strip():
                print(f'    Response: {body.strip()[:200]}')
        except urllib.error.HTTPError as e:
            # 200/202 are success. 422 = some URLs invalid (we'll still
            # have processed the valid ones). Anything else is a real
            # failure worth surfacing.
            body = e.read().decode('utf-8', errors='replace') if e.fp else ''
            print(f'  Batch {i // BATCH_SIZE + 1}: HTTP {e.code} ({len(chunk)} URLs)')
            if body: print(f'    Response: {body.strip()[:200]}')
        except Exception as e:
            print(f'  Batch {i // BATCH_SIZE + 1}: ERROR — {e}')


def main():
    if len(sys.argv) > 1:
        urls = sys.argv[1:]
    else:
        urls = urls_from_sitemap()
    submit(urls)
    print('Done. Bing typically crawls within minutes; Yandex/Naver/Seznam')
    print('on their own schedule. No dashboard refresh needed.')


if __name__ == '__main__':
    main()
