#!/usr/bin/env node
/**
 * Programmatic SEO generator for leadcove.io
 *
 * Reads scripts/cities.json and writes 2 pages per city:
 *
 *   /skip-tracing/{slug}.html       → "Skip tracing for real estate agents in {City}, {ST}"
 *   /llc-owner-lookup/{slug}.html   → "LLC owner lookup in {City}, {ST}"
 *
 * Each page is unique enough to avoid doorway-content penalties:
 *   - Personalized intro paragraph by city traits (luxury / FL / metro)
 *   - Real local stats (median home price + agent count from cities.json)
 *   - Internal links to canonical SEO content (blog/, compare/)
 *   - Distinct H1, title, meta description, JSON-LD per page
 *   - Author-style content blocks tailored to the niche
 *
 * Also rewrites /sitemap.xml — generated city pages are inserted between
 * a pair of marker comments. Existing entries outside the markers are
 * preserved verbatim so manual blog/help/etc URLs aren't disturbed.
 *
 * Usage:
 *   node scripts/build-city-pages.js
 *
 * Idempotent — running twice produces the same output. Safe to re-run
 * after editing cities.json or the templates below.
 *
 * Xavi 2026-05-22 — automated acquisition Phase 2.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

const cities = JSON.parse(fs.readFileSync(path.join(__dirname, 'cities.json'), 'utf8'));
const today  = new Date().toISOString().slice(0, 10);

// ─── Template helpers ─────────────────────────────────────────────────

function fmt$(n) {
  return '$' + Math.round(n).toLocaleString();
}
function fmtN(n) {
  return Number(n).toLocaleString();
}

function shellHead(meta) {
  return `<!doctype html>
<html lang="en">
<head>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-Q17T70D5R4"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-Q17T70D5R4');
    gtag('config', 'AW-18148856780');
  </script>
  <script type="text/javascript">
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", "wq57o9awo1");
  </script>

<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>${escapeHtml(meta.title)}</title>
<meta name="description" content="${escapeHtml(meta.description)}" />
<meta name="keywords" content="${escapeHtml(meta.keywords)}" />
<link rel="canonical" href="${escapeHtml(meta.canonical)}" />
<meta property="og:type" content="article" />
<meta property="og:url" content="${escapeHtml(meta.canonical)}" />
<meta property="og:title" content="${escapeHtml(meta.title)}" />
<meta property="og:description" content="${escapeHtml(meta.description)}" />
<meta property="og:image" content="https://leadcove.io/assets/og.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:site_name" content="LeadCove" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="${escapeHtml(meta.title)}" />
<meta name="twitter:description" content="${escapeHtml(meta.description)}" />
<meta name="twitter:image" content="https://leadcove.io/assets/og.png" />
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
<link rel="apple-touch-icon" href="/favicon.svg" />
<meta name="theme-color" content="#0B2545" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css" />
<style>
  .local-hero { max-width: 880px; margin: 0 auto; padding: 64px 32px 24px; text-align: center; }
  .local-eyebrow { font-size: 12px; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: var(--teal-2); margin: 0 0 14px; }
  .local-h1 { font-family: var(--f-display); font-weight: 600; font-size: clamp(34px, 4.4vw, 52px); line-height: 1.05; letter-spacing: -0.02em; color: var(--navy); margin: 0 0 18px; }
  .local-lede { font-size: 18px; line-height: 1.55; color: var(--ink-2); max-width: 620px; margin: 0 auto 8px; }
  .local-body { max-width: 720px; margin: 0 auto; padding: 12px 32px 32px; color: var(--ink-2); font-size: 17px; line-height: 1.72; }
  .local-body h2 { font-family: var(--f-display); font-weight: 600; font-size: 28px; line-height: 1.2; color: var(--navy); margin: 36px 0 12px; letter-spacing: -0.01em; }
  .local-body h3 { font-weight: 700; font-size: 18px; color: var(--navy); margin: 22px 0 8px; }
  .local-body p { margin: 0 0 18px; }
  .local-body ul { padding-left: 22px; margin: 0 0 22px; }
  .local-body li { margin: 0 0 8px; }
  .local-body strong { color: var(--navy); }
  .local-stats { display: grid; grid-template-columns: repeat(3,1fr); gap: 14px; margin: 24px 0; }
  .local-stat { background: #fff; border: 1px solid var(--hairline); border-radius: 12px; padding: 18px; text-align: center; }
  .local-stat .num { font-size: 26px; font-weight: 800; color: var(--teal-2); letter-spacing: -0.02em; }
  .local-stat .lab { font-size: 12px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.06em; margin-top: 4px; font-weight: 600; }
  .local-cta { max-width: 720px; margin: 32px auto; padding: 36px 32px; background: var(--navy); color: #fff; border-radius: 16px; text-align: center; }
  .local-cta h2 { font-family: var(--f-display); font-weight: 600; font-size: 26px; color: #fff; margin: 0 0 12px; letter-spacing: -0.01em; }
  .local-cta p { color: rgba(255,255,255,0.75); margin: 0 0 18px; font-size: 15px; }
  .local-cta .btn-primary { background: var(--teal); display: inline-block; padding: 14px 28px; color: #fff; border-radius: 10px; text-decoration: none; font-weight: 700; }
  .local-related { max-width: 720px; margin: 32px auto; padding: 24px 32px; border-top: 1px solid var(--hairline); font-size: 14px; color: var(--muted); }
  .local-related a { color: var(--navy); font-weight: 500; display: inline-block; margin: 0 8px 6px 0; text-decoration: none; }
  .local-related a:hover { color: var(--teal-2); }
  @media (max-width: 640px) {
    .local-hero { padding: 48px 24px 16px; }
    .local-body { padding: 12px 24px 24px; font-size: 16px; }
    .local-stats { grid-template-columns: 1fr; }
  }
</style>
${meta.jsonld}
<script type="text/javascript">window.$crisp=[];window.CRISP_WEBSITE_ID="42ed026c-1c3c-432e-a4c8-fced861a42b2";(function(){d=document;s=d.createElement("script");s.src="https://client.crisp.chat/l.js";s.async=1;d.getElementsByTagName("head")[0].appendChild(s);})();</script>
</head>
<body>

<header class="nav">
  <a class="brand" href="/">
    <svg class="brand-mark" viewBox="0 0 40 40" aria-hidden="true">
      <path d="M3 26 C 8 22, 14 22, 20 26 C 26 30, 32 30, 37 26" stroke="currentColor" stroke-width="2.4" fill="none" stroke-linecap="round"/>
      <path d="M3 32 C 8 28, 14 28, 20 32 C 26 36, 32 36, 37 32" stroke="currentColor" stroke-width="2.4" fill="none" stroke-linecap="round" opacity="0.5"/>
      <circle cx="30" cy="14" r="3" fill="currentColor"/>
    </svg>
    <span class="brand-wordmark">LeadCove</span>
  </a>
  <nav class="nav-links">
    <a href="/free-lookup.html">Free lookup</a>
    <a href="/blog/">Blog</a>
    <a href="/help/">Help</a>
    <a href="https://app.leadcove.io/">Sign in</a>
  </nav>
  <div class="nav-cta">
    <a href="https://app.leadcove.io/" class="btn-ghost">Sign in</a>
    <a href="https://app.leadcove.io/?trial=1#signup" class="btn-primary">Start trial</a>
  </div>
</header>
`;
}

function shellFoot() {
  return `
<div class="footer-wrap">
<footer class="footer">
  <div class="footer-col">
    <div class="brand">
      <svg class="brand-mark" viewBox="0 0 40 40" aria-hidden="true">
        <path d="M3 26 C 8 22, 14 22, 20 26 C 26 30, 32 30, 37 26" stroke="currentColor" stroke-width="2.4" fill="none" stroke-linecap="round"/>
        <path d="M3 32 C 8 28, 14 28, 20 32 C 26 36, 32 36, 37 32" stroke="currentColor" stroke-width="2.4" fill="none" stroke-linecap="round" opacity="0.5"/>
        <circle cx="30" cy="14" r="3" fill="currentColor"/>
      </svg>
      <span class="brand-wordmark">LeadCove</span>
    </div>
    <p class="footer-tag">More dials. Less prep.</p>
  </div>
  <div class="footer-col">
    <h5>Product</h5>
    <a href="/#how">How it works</a>
    <a href="/#features">Features</a>
    <a href="/#plans">Pricing</a>
    <a href="/#faq">FAQ</a>
    <a href="/about.html">About</a>
    <a href="/blog/">Blog</a>
    <a href="/free-lookup.html">Free lookup</a>
  </div>
  <div class="footer-col">
    <h5>Account</h5>
    <a href="https://app.leadcove.io/">Sign in</a>
    <a href="https://app.leadcove.io/#signup">Sign up</a>
    <a href="mailto:hello@leadcove.io">hello@leadcove.io</a>
    <a href="https://www.instagram.com/leadcove.io" target="_blank" rel="noopener" aria-label="LeadCove on Instagram">Instagram</a>
    <a href="https://www.facebook.com/leadcove" target="_blank" rel="noopener" aria-label="LeadCove on Facebook">Facebook</a>
    <a href="https://www.linkedin.com/company/leadcove" target="_blank" rel="noopener" aria-label="LeadCove on LinkedIn">LinkedIn</a>
  </div>
  <div class="footer-col">
    <h5>Legal</h5>
    <a href="/terms.html">Terms of Service</a>
    <a href="/privacy.html">Privacy Policy</a>
    <a href="/tcpa.html">TCPA &amp; DNC</a>
  </div>
  <div class="footer-bar">
    © 2026 LeadCove · a brand owned by Miami Metro LLC · <a href="mailto:hello@leadcove.io" style="color:inherit;text-decoration:underline">hello@leadcove.io</a>
  </div>
</footer>
</div>

</body></html>`;
}

function jsonldArticle({ title, description, url, datePublished }) {
  return `<script type="application/ld+json">
${JSON.stringify({
  '@context': 'https://schema.org',
  '@type': 'Article',
  headline: title,
  description,
  datePublished,
  dateModified: datePublished,
  author: { '@type': 'Organization', name: 'LeadCove' },
  publisher: { '@type': 'Organization', name: 'LeadCove', url: 'https://leadcove.io/' },
  image: 'https://leadcove.io/assets/og.png',
  mainEntityOfPage: { '@type': 'WebPage', '@id': url },
}, null, 2)}
</script>`;
}

function escapeHtml(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

// ─── City-specific intro paragraph ────────────────────────────────────

function cityIntroForSkipTrace(c) {
  if (c.luxury && c.fl) {
    return `${c.city}, ${c.state} is a luxury market where 40-60% of properties are owned through LLCs, family trusts, or holding companies. The standard "look up the owner on the tax roll" workflow misses the actual human on most of those records — you get an entity name, not a callable contact. That's where LeadCove's automated LLC unmask makes a measurable difference for ${c.city} agents.`;
  }
  if (c.luxury) {
    return `${c.city}, ${c.state} agents working luxury or absentee-owner segments deal with one specific data problem: the property's deed shows an entity (LLC, Trust, Holdings Corp), and the chain to find the real owner is multiple manual lookups. LeadCove automates that chain — owner address-in, real-human contact-out.`;
  }
  if (c.fl) {
    return `${c.city}, ${c.state} agents have a built-in advantage: Florida is one of the strongest skip-tracing data states in the country (parcel data is public, statewide entity registry searchable). The bottleneck isn't data availability — it's stitching it together fast enough to actually call through the list before someone else does.`;
  }
  return `${c.city}, ${c.state} agents prospecting expireds, FSBOs, or absentee owners need one thing: a phone number that actually rings, attached to the real owner. Public records get you halfway. The other half — verified mobile, DNC status, LLC unmask — is what we automate.`;
}

function cityIntroForLLC(c) {
  if (c.luxury && c.fl) {
    return `In ${c.city}, ${c.state}, LLC ownership is the norm in luxury condos, oceanfront single-family, and absentee investor portfolios. Sunbiz (Florida's state corporate registry) gives you the registered agent name; LeadCove gives you the actual managing member's mobile and email — without the manual cross-reference.`;
  }
  if (c.fl) {
    return `${c.city}, ${c.state} sits in one of the friendliest U.S. states for LLC owner lookup — Florida's Sunbiz is fully searchable, and parcel records identify entity owners cleanly. The remaining gap is contact: who runs the LLC, and what's their phone? That's what LeadCove fills.`;
  }
  return `LLC-owned property is roughly 20-35% of the residential market nationally and 40-60% in luxury and absentee-heavy areas. ${c.city}, ${c.state} agents who don't have a workflow for unmasking entity owners are leaving a substantial slice of their farm unworked.`;
}

// ─── Page templates ───────────────────────────────────────────────────

function renderSkipTracePage(c) {
  const title = `Skip tracing for real estate agents in ${c.city}, ${c.state} | LeadCove`;
  const description = `Skip tracing built for ${c.city}, ${c.state} agents. Upload MLS expireds, FSBOs, or building canvasses — get back verified owner phones, emails, and LLC unmask. DNC + TCPA flags included.`;
  const url = `https://leadcove.io/skip-tracing/${c.slug}.html`;
  const keywords = `skip tracing ${c.city}, ${c.city} real estate skip tracing, ${c.city} ${c.state} skip trace, find property owner ${c.city}, ${c.city} expired listings`;

  const head = shellHead({
    title, description, keywords, canonical: url,
    jsonld: jsonldArticle({ title, description, url, datePublished: today }),
  });

  const body = `
<section class="local-hero">
  <p class="local-eyebrow">${escapeHtml(c.metro)} · Skip tracing</p>
  <h1 class="local-h1">Skip tracing for real estate agents in ${escapeHtml(c.city)}, ${escapeHtml(c.state)}.</h1>
  <p class="local-lede">Upload any address list — MLS expireds, FSBOs, building canvasses, your own CSV — and get back the real owner's mobile phone, email, mailing address, and (for entity-owned property) the human behind the LLC. ${c.fl ? 'Florida coverage from day one.' : 'Nationwide. No state-by-state setup.'}</p>
</section>

<section class="local-body">
  <div class="local-stats">
    <div class="local-stat"><div class="num">${fmt$(c.median_home)}</div><div class="lab">${escapeHtml(c.city)} median home</div></div>
    <div class="local-stat"><div class="num">${fmtN(c.agents_est)}</div><div class="lab">Active agents (est.)</div></div>
    <div class="local-stat"><div class="num">${c.luxury ? '40-60%' : '20-35%'}</div><div class="lab">LLC-owned property</div></div>
  </div>

  <p>${cityIntroForSkipTrace(c)}</p>

  <h2>How LeadCove skip tracing works for ${escapeHtml(c.city)} agents</h2>
  <p>You bring a list. We return owner data. That's the whole product. No state-by-state vendor switching, no manual Sunbiz / Secretary of State lookups for entity owners, no separate DNC scrub step.</p>
  <ul>
    <li><strong>Mobile + email</strong> — every record, ranked by recency. Not the listing agent's number. Not the tax-roll number from a 2014 refi.</li>
    <li><strong>LLC, Trust, Corp unmask</strong> — automated. The actual managing member's contact info appears next to the entity name on ~70-85% of records.</li>
    <li><strong>DNC + TCPA-litigator flags</strong> — per phone, per lookup. The compliance step happens before you ever dial.</li>
    <li><strong>Same-owner dedup</strong> — one credit per owner, even if they hold 8 properties in ${escapeHtml(c.city)}. ${c.luxury ? 'Crucial in luxury markets where the same family LLC shows up across multiple properties.' : 'Saves the duplicate-charge cost that legacy tools quietly bill.'}</li>
    <li><strong>No data, no charge</strong> — a missed lookup costs you zero credits.</li>
  </ul>

  <h2>Common ${escapeHtml(c.city)} use cases</h2>
  <h3>Working expireds</h3>
  <p>Pull the daily expired list from your MLS, strip the listing-agent contact columns, drop the file into LeadCove. Within a few minutes you have a callable list — owner name, mobile, email, DNC status, LLC unmask — ranked by whatever your priority columns are.</p>
  <h3>Building canvasses</h3>
  <p>${c.luxury ? `${c.city}'s mid- and high-rise residential is full of LLC- and Trust-owned units. A clean canvass starts with one address per unit and ends with a callable contact for the actual human owner — not the entity name.` : `Pick a target building or block. Pull every parcel address. LeadCove returns the owner record on each, with same-owner dedup so a multi-property owner only costs you one credit.`}</p>
  <h3>FSBO outreach</h3>
  <p>FSBO addresses often have wrong phone numbers attached on Zillow / FSBO.com — owners scrub them once they decide to sell. A fresh skip trace gets you the current mobile.</p>

  <h2>Pricing for ${escapeHtml(c.city)} agents</h2>
  <p>Three monthly plans, all carrying the full platform — Mission Control CRM, LLC unmask, DNC + TCPA flags, FUB sync on the higher tiers. The entry tier starts at the lowest price point and ships with a 7-day trial for $0 today. <a href="/#plans">See full pricing →</a></p>

  <h2>Try it on a ${escapeHtml(c.city)} address right now</h2>
  <p><a href="/free-lookup.html"><strong>Free lookup tool →</strong></a> Enter any ${escapeHtml(c.city)} property address and see the real owner data we surface. No signup. 3 free lookups per day. Email-gated reveal for the full record.</p>
</section>

<section class="local-cta">
  <h2>Run LeadCove on your next ${escapeHtml(c.city)} list.</h2>
  <p>7-day trial. $0 today. 10 credits to test on real ${escapeHtml(c.city)} rows.</p>
  <a class="btn-primary" href="https://app.leadcove.io/?utm_source=local&utm_medium=organic&utm_campaign=${encodeURIComponent(c.slug)}-skip-trace&trial=1#signup">Start your 7-day trial →</a>
</section>

<section class="local-related">
  <strong style="color:#0B2545">Related:</strong>
  <a href="/blog/skip-tracing-real-estate-agents.html">Skip tracing guide</a> ·
  <a href="/blog/llc-owner-lookup-unmask.html">LLC owner lookup</a> ·
  <a href="/blog/expired-listings-skip-tracing.html">Expired listings playbook</a> ·
  <a href="/llc-owner-lookup/${c.slug}.html">LLC owner lookup in ${escapeHtml(c.city)}</a> ·
  <a href="/compare/leadcove-vs-batchleads.html">vs BatchLeads</a> ·
  <a href="/compare/leadcove-vs-propstream.html">vs PropStream</a>
</section>
`;

  return head + body + shellFoot();
}

function renderLLCPage(c) {
  const title = `LLC owner lookup in ${c.city}, ${c.state} — find the human behind any LLC | LeadCove`;
  const description = `LLC-owned property in ${c.city}, ${c.state}? Unmask the actual managing member with phone, email, and mailing address — automated. No manual ${c.fl ? 'Sunbiz' : 'state-registry'} chasing.`;
  const url = `https://leadcove.io/llc-owner-lookup/${c.slug}.html`;
  const keywords = `LLC owner lookup ${c.city}, ${c.city} LLC unmask, find LLC owner ${c.city}, ${c.city} ${c.state} trust owner, ${c.city} entity owner search`;

  const head = shellHead({
    title, description, keywords, canonical: url,
    jsonld: jsonldArticle({ title, description, url, datePublished: today }),
  });

  const body = `
<section class="local-hero">
  <p class="local-eyebrow">${escapeHtml(c.metro)} · LLC owner lookup</p>
  <h1 class="local-h1">LLC owner lookup in ${escapeHtml(c.city)}, ${escapeHtml(c.state)}.</h1>
  <p class="local-lede">Find the actual human behind any LLC, Trust, or Corporation that owns property in ${escapeHtml(c.city)}. Automated. ${c.luxury ? '70-85% unmask yield on entity-owned records.' : 'No manual state-registry chasing.'}</p>
</section>

<section class="local-body">
  <div class="local-stats">
    <div class="local-stat"><div class="num">${c.luxury ? '40-60%' : '20-35%'}</div><div class="lab">${escapeHtml(c.city)} entity-owned</div></div>
    <div class="local-stat"><div class="num">70-85%</div><div class="lab">Unmask yield</div></div>
    <div class="local-stat"><div class="num">1</div><div class="lab">Credit per owner</div></div>
  </div>

  <p>${cityIntroForLLC(c)}</p>

  <h2>The manual ${escapeHtml(c.city)} LLC unmask workflow (what we automate)</h2>
  <ol>
    <li>Pull the property record from ${escapeHtml(c.state)} county clerk — get the LLC name.</li>
    <li>Search ${c.fl ? 'Florida Sunbiz' : `${c.state} Secretary of State`} for that entity — get the registered agent + managing member names.</li>
    <li>Skip trace the managing member's name — get phone + email.</li>
    <li>Verify DNC + TCPA status on the phone before dialing.</li>
    <li>Repeat for every entity-owned property on your list.</li>
  </ol>
  <p>For a 200-row list with 35% LLC ownership, that's 70 properties × 4 manual steps = 280 lookups before you make a single call. LeadCove collapses all of it into one upload.</p>

  <h2>What you get back per LLC-owned property in ${escapeHtml(c.city)}</h2>
  <ul>
    <li><strong>The actual human's name</strong> — managing member or trustee.</li>
    <li><strong>Mobile phone</strong> + landline if available, ranked by recency.</li>
    <li><strong>Personal email</strong> — typically a Gmail / Yahoo / personal Outlook, not the LLC's business email.</li>
    <li><strong>Mailing address</strong> — usually different from the property address (entity owners are typically absentee).</li>
    <li><strong>DNC + TCPA litigator flags</strong> — per phone.</li>
    <li><strong>Joint owners</strong> — when the LLC has multiple managing members, all surface in the same lookup.</li>
  </ul>

  <h2>Coverage and accuracy</h2>
  <p>Across our ${escapeHtml(c.state)} customer base, the LLC unmask hit rate runs 70-85% on residential entity-owned property. ${c.fl ? `Florida's Sunbiz is one of the most accessible state registries in the country, which keeps yields on the upper end of that range for ${escapeHtml(c.city)}.` : 'Yields vary by state-registry data freshness; LeadCove queries multiple sources and stitches the result before billing.'} Misses cost zero credits — we only charge on usable hits.</p>

  <h2>Try it free on one ${escapeHtml(c.city)} address</h2>
  <p><a href="/free-lookup.html"><strong>Free lookup tool →</strong></a> Enter any ${escapeHtml(c.city)} LLC-owned property address and we'll return the unmasked owner data — no signup, no card.</p>
</section>

<section class="local-cta">
  <h2>Stop guessing at LLC owners in ${escapeHtml(c.city)}.</h2>
  <p>7-day trial. $0 today. Run LeadCove on a list of ${escapeHtml(c.city)} entity-owned property and see the unmask yield yourself.</p>
  <a class="btn-primary" href="https://app.leadcove.io/?utm_source=local&utm_medium=organic&utm_campaign=${encodeURIComponent(c.slug)}-llc&trial=1#signup">Start your 7-day trial →</a>
</section>

<section class="local-related">
  <strong style="color:#0B2545">Related:</strong>
  <a href="/blog/llc-owner-lookup-unmask.html">Full LLC unmask guide</a> ·
  <a href="/blog/skip-tracing-real-estate-agents.html">Skip tracing primer</a> ·
  <a href="/skip-tracing/${c.slug}.html">Skip tracing in ${escapeHtml(c.city)}</a> ·
  <a href="/compare/leadcove-vs-batchleads.html">vs BatchLeads</a> ·
  <a href="/compare/leadcove-vs-propstream.html">vs PropStream</a> ·
  <a href="/compare/leadcove-vs-reiskip.html">vs REIskip</a>
</section>
`;

  return head + body + shellFoot();
}

// ─── Driver ───────────────────────────────────────────────────────────

const outSkip = path.join(ROOT, 'skip-tracing');
const outLLC  = path.join(ROOT, 'llc-owner-lookup');
fs.mkdirSync(outSkip, { recursive: true });
fs.mkdirSync(outLLC,  { recursive: true });

const sitemapUrls = [];

for (const c of cities) {
  const skipHtml = renderSkipTracePage(c);
  const llcHtml  = renderLLCPage(c);
  const skipPath = path.join(outSkip, `${c.slug}.html`);
  const llcPath  = path.join(outLLC,  `${c.slug}.html`);
  fs.writeFileSync(skipPath, skipHtml);
  fs.writeFileSync(llcPath,  llcHtml);
  sitemapUrls.push(`https://leadcove.io/skip-tracing/${c.slug}.html`);
  sitemapUrls.push(`https://leadcove.io/llc-owner-lookup/${c.slug}.html`);
}

console.log(`✅ Wrote ${cities.length} cities × 2 templates = ${cities.length * 2} pages`);

// Update sitemap.xml — insert between markers
const sitemapPath = path.join(ROOT, 'sitemap.xml');
let sitemap = fs.readFileSync(sitemapPath, 'utf8');

const startMarker = '<!-- PROGRAMMATIC_CITY_PAGES_START -->';
const endMarker   = '<!-- PROGRAMMATIC_CITY_PAGES_END -->';

const generatedBlock = `${startMarker}\n` +
  sitemapUrls.map(u => `  <url>\n    <loc>${u}</loc>\n    <lastmod>${today}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>`).join('\n') +
  `\n  ${endMarker}`;

if (sitemap.includes(startMarker) && sitemap.includes(endMarker)) {
  sitemap = sitemap.replace(
    new RegExp(`${startMarker}[\\s\\S]*?${endMarker}`),
    generatedBlock
  );
} else {
  // First run — insert before </urlset>
  sitemap = sitemap.replace('</urlset>', `  ${generatedBlock}\n</urlset>`);
}

fs.writeFileSync(sitemapPath, sitemap);
console.log(`✅ Updated sitemap.xml with ${sitemapUrls.length} URLs`);
