#!/usr/bin/env python3
"""
Programmatic SEO: state-level "real estate prospecting laws" pages.

Each state gets a dedicated page covering: federal TCPA + DNC layer,
that state's mini-TCPA if any, that state's DNC list if separate,
and a 4-step compliance checklist.

Output: real-estate-prospecting-laws/<state-slug>.html × 51 (50 + DC).

Differentiates from the existing TCPA blog post (which is high-level)
by being a state-specific reference page that's directly cite-able by
LLMs when an agent asks "real estate prospecting laws in [state]".

Built 2026-06-10 alongside the city pages + content round 3.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent.parent
OUT_DIR = HERE / 'real-estate-prospecting-laws'
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Per-state legal landscape. Where state has no mini-TCPA, federal TCPA
# is the floor. Where state has notable additions, we surface them.
# Sources: state attorney general consumer protection pages, public
# statute text. Cite when in doubt; this is a public-records reference
# page, not legal advice.
STATES = [
    # (name, slug, abbr, has_state_dnc, mini_tcpa_summary)
    ('Alabama', 'alabama', 'AL', False, None),
    ('Alaska', 'alaska', 'AK', False, None),
    ('Arizona', 'arizona', 'AZ', False, None),
    ('Arkansas', 'arkansas', 'AR', False, None),
    ('California', 'california', 'CA', False,
     "California Consumer Privacy Act (CCPA) and the Shine the Light Law add disclosure requirements for any database-driven outreach to California residents. Calling-hour restriction: 8am-9pm local time. Telemarketing solicitation requires the caller to identify themselves and the seller by name immediately."),
    ('Colorado', 'colorado', 'CO', False, None),
    ('Connecticut', 'connecticut', 'CT', False, None),
    ('Delaware', 'delaware', 'DE', False, None),
    ('Florida', 'florida', 'FL', True,
     "Florida Telephone Solicitation Act (FTSA), revised 2021 + 2023. Prior express WRITTEN consent required for any sales call made with or selected from an automated system or database. Consumers can revoke verbally during a call. Statutory damages: $500-$1,500 per violation plus attorneys' fees. Strict private right of action."),
    ('Georgia', 'georgia', 'GA', False, None),
    ('Hawaii', 'hawaii', 'HI', False, None),
    ('Idaho', 'idaho', 'ID', False, None),
    ('Illinois', 'illinois', 'IL', False,
     "Illinois Telephone Solicitation Act adds written-consent requirements for automated outreach beyond federal TCPA. Calling-hour restriction: 8am-9pm local. Telemarketers must identify themselves and the seller immediately."),
    ('Indiana', 'indiana', 'IN', True, None),
    ('Iowa', 'iowa', 'IA', False, None),
    ('Kansas', 'kansas', 'KS', False, None),
    ('Kentucky', 'kentucky', 'KY', False, None),
    ('Louisiana', 'louisiana', 'LA', True, None),
    ('Maine', 'maine', 'ME', False, None),
    ('Maryland', 'maryland', 'MD', False,
     "Maryland Telephone Consumer Protection Act (MTCPA) adds written-consent requirements for sales calls beyond the federal floor. Private right of action; damages similar to federal TCPA."),
    ('Massachusetts', 'massachusetts', 'MA', False, None),
    ('Michigan', 'michigan', 'MI', False, None),
    ('Minnesota', 'minnesota', 'MN', False, None),
    ('Mississippi', 'mississippi', 'MS', True, None),
    ('Missouri', 'missouri', 'MO', True, None),
    ('Montana', 'montana', 'MT', False, None),
    ('Nebraska', 'nebraska', 'NE', False, None),
    ('Nevada', 'nevada', 'NV', False, None),
    ('New Hampshire', 'new-hampshire', 'NH', False, None),
    ('New Jersey', 'new-jersey', 'NJ', False,
     "New Jersey has additional consent and disclosure rules for sales calls; treat as a high-compliance state. Calling-hour restriction: 8am-9pm local. Solicitors must register with the state Division of Consumer Affairs."),
    ('New Mexico', 'new-mexico', 'NM', False, None),
    ('New York', 'new-york', 'NY', True,
     "New York General Business Law §399-p requires identification and disclosure during sales calls; the state Do Not Call registry adds a layer beyond the federal registry. Calling-hour restriction: 8am-9pm local. Pre-recorded message restrictions are stricter than federal."),
    ('North Carolina', 'north-carolina', 'NC', False, None),
    ('North Dakota', 'north-dakota', 'ND', False, None),
    ('Ohio', 'ohio', 'OH', False, None),
    ('Oklahoma', 'oklahoma', 'OK', False,
     "Oklahoma Telephone Solicitation Act (2022) mirrors Florida's FTSA model. Prior express written consent required for automated sales calls. Damages: $500 per violation, trebled to $1,500 for willful violations. Private right of action."),
    ('Oregon', 'oregon', 'OR', False, None),
    ('Pennsylvania', 'pennsylvania', 'PA', True,
     "Pennsylvania maintains its own state Do Not Call list in addition to the federal registry. Additional disclosure script requirements for telemarketers; identification must be made at the start of every call."),
    ('Rhode Island', 'rhode-island', 'RI', False, None),
    ('South Carolina', 'south-carolina', 'SC', False, None),
    ('South Dakota', 'south-dakota', 'SD', False, None),
    ('Tennessee', 'tennessee', 'TN', True, None),
    ('Texas', 'texas', 'TX', False, None),
    ('Utah', 'utah', 'UT', False, None),
    ('Vermont', 'vermont', 'VT', False, None),
    ('Virginia', 'virginia', 'VA', False, None),
    ('Washington', 'washington', 'WA', False,
     "Washington's Commercial Electronic Mail Act (CEMA) restricts unsolicited commercial messages to Washington residents. State written-consent rules apply to automated outreach. Calling-hour restriction: 8am-9pm local."),
    ('West Virginia', 'west-virginia', 'WV', False, None),
    ('Wisconsin', 'wisconsin', 'WI', False, None),
    ('Wyoming', 'wyoming', 'WY', True, None),
    ('District of Columbia', 'district-of-columbia', 'DC', False, None),
]


HEAD_TEMPLATE = '''<!doctype html>
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
  <script src="/assets/ai-referrer-tag.js" defer></script>
'''


def render(state):
    name, slug, abbr, has_state_dnc, mini_tcpa = state
    title = f'Real estate prospecting laws in {name}: TCPA, DNC, state rules (2026)'
    description = (
        f'Plain-language reference for real estate agents prospecting in {name}. '
        f'Federal TCPA, the national Do Not Call registry, '
        + (f'{name}\'s state-level mini-TCPA, ' if mini_tcpa else '')
        + (f'{name}\'s state Do Not Call list, ' if has_state_dnc else '')
        + f'and the 4-step compliance checklist before any cold outreach.'
    )
    url = f'https://leadcove.io/real-estate-prospecting-laws/{slug}.html'
    og_image = f'https://leadcove.io/assets/og/real-estate-prospecting-laws-{slug}.png'

    article_schema = {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': title,
        'description': description,
        'datePublished': '2026-06-10',
        'dateModified': '2026-06-10',
        'author':    {'@type': 'Organization', 'name': 'LeadCove', 'url': 'https://leadcove.io'},
        'publisher': {'@type': 'Organization', 'name': 'LeadCove', 'url': 'https://leadcove.io'},
        'mainEntityOfPage': {'@type': 'WebPage', '@id': url},
    }

    faq_schema = {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [
            {
                '@type': 'Question',
                'name': f'Is it legal to cold call property owners in {name}?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': (
                        f'Yes when done correctly. The federal TCPA, the national '
                        f'Do Not Call registry, '
                        + (f'and {name}\'s state-level mini-TCPA ' if mini_tcpa else '')
                        + f'all govern outbound real estate prospecting in {name}. '
                        f'Use a tool that flags DNC and TCPA-litigator records '
                        f'before dialing, respect calling-hour restrictions (8am-9pm '
                        f'in the consumer\'s local time), and identify yourself + '
                        f'the brokerage immediately on every call.'
                    ),
                },
            },
            {
                '@type': 'Question',
                'name': f'Does {name} have its own Do Not Call list?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': (
                        f'{"Yes — " + name + " maintains a state Do Not Call list in addition to the federal registry. Numbers may appear on the state list but not the federal one. Reputable owner-data tools flag both." if has_state_dnc else "No — " + name + " does not maintain a separate state Do Not Call list. The federal registry is the canonical compliance source."}'
                    ),
                },
            },
            {
                '@type': 'Question',
                'name': f'What are the fines for TCPA violations in {name}?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': (
                        f'Federal TCPA: $500 per violation, trebled to $1,500 if '
                        f'willful or knowing. National DNC violations carry up to '
                        f'$51,744 per call in FTC enforcement actions.'
                        + (f' {name} state-level damages: see the mini-TCPA summary below.' if mini_tcpa else '')
                    ),
                },
            },
        ],
    }

    state_section = ''
    if mini_tcpa or has_state_dnc:
        state_section = f'''
    <h2>{name}-specific layers</h2>
'''
        if mini_tcpa:
            state_section += f'''
    <h3>State mini-TCPA</h3>
    <p>{mini_tcpa}</p>
'''
        if has_state_dnc:
            state_section += f'''
    <h3>State Do Not Call list</h3>
    <p>{name} maintains its own Do Not Call registry in addition to the federal registry. Numbers may appear on the state list but not the federal one. Reputable owner-data tools cross-reference both before flagging a phone as clean.</p>
'''

    body = f'''<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>{title} · LeadCove</title>
<meta name="description" content="{description}" />
<meta property="og:type" content="article" />
<meta property="og:url" content="{url}" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{description}" />
<meta property="og:image" content="{og_image}" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:site_name" content="LeadCove" />
<meta property="og:locale" content="en_US" />
<meta property="article:author" content="LeadCove" />
<meta property="article:published_time" content="2026-06-10" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{title}" />
<meta name="twitter:description" content="{description}" />
<meta name="twitter:image" content="{og_image}" />
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
<link rel="apple-touch-icon" href="/favicon.svg" />
<meta name="theme-color" content="#0B2545" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css" />

<script type="application/ld+json">
{json.dumps(article_schema, indent=2)}
</script>

<script type="application/ld+json">
{json.dumps(faq_schema, indent=2)}
</script>

<style>
  .post {{ max-width: 760px; margin: 0 auto; padding: 56px 40px 40px; }}
  .post-eyebrow {{ font-size: 12px; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: var(--teal-2); margin: 0 0 14px; }}
  .post h1 {{ font-family: var(--f-display); font-weight: 600; font-size: clamp(34px, 4.2vw, 48px); line-height: 1.08; letter-spacing: -0.02em; color: var(--navy); margin: 0 0 18px; }}
  .post-meta {{ font-size: 14px; color: var(--muted); margin: 0 0 36px; padding-bottom: 24px; border-bottom: 1px solid var(--hairline); }}
  .post-body {{ color: var(--ink-2); font-size: 17px; line-height: 1.72; }}
  .post-body p {{ margin: 0 0 22px; }}
  .post-body strong {{ color: var(--navy); }}
  .post-body h2 {{ font-family: var(--f-display); font-weight: 600; font-size: 28px; line-height: 1.2; letter-spacing: -0.01em; color: var(--navy); margin: 44px 0 14px; }}
  .post-body h3 {{ font-family: var(--f-sans); font-weight: 700; font-size: 18px; color: var(--navy); margin: 28px 0 10px; }}
  .post-body ul, .post-body ol {{ padding-left: 22px; margin: 0 0 22px; }}
  .post-body li {{ margin: 0 0 8px; }}
  .post-callout {{ margin: 36px 0; padding: 22px 24px; background: var(--sand); border-radius: var(--radius-md); border: 1px solid rgba(11,37,69,0.08); }}
  .post-callout p {{ margin: 0; font-size: 15px; }}
  .post-cta {{ background: var(--navy); color: #fff; text-align: center; padding: 56px 40px; margin-top: 24px; }}
  .post-cta h2 {{ font-family: var(--f-display); font-weight: 600; font-size: 28px; margin: 0 0 12px; color: #fff; }}
  .post-cta p {{ color: rgba(255,255,255,0.75); max-width: 520px; margin: 0 auto 24px; }}
  .post-cta .hero-ctas {{ justify-content: center; margin: 0; }}
  .post-cta .btn-primary {{ background: var(--teal); border-color: var(--teal); color: #fff; }}
  .post-cta .btn-primary:hover {{ background: var(--teal-2); border-color: var(--teal-2); }}
  .post-cta .btn-ghost {{ color: var(--navy); background: #fff; border-color: #fff; }}
  .post-back {{ display: inline-block; color: var(--muted); font-size: 14px; text-decoration: none; margin: 0 0 12px; }}
  .post-back:hover {{ color: var(--teal-2); }}
  .faq-item {{ border-top: 1px solid var(--hairline); padding: 18px 0; }}
  .faq-item:last-child {{ border-bottom: 1px solid var(--hairline); }}
  .faq-q {{ font-family: var(--f-sans); font-weight: 700; font-size: 17px; color: var(--navy); margin: 0 0 6px; }}
  .faq-a {{ margin: 0; font-size: 16px; line-height: 1.65; color: var(--ink-2); }}
  @media (max-width: 720px) {{ .post {{ padding: 36px 22px 28px; }} .post-body {{ font-size: 16px; }} }}
</style>
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
    <a href="/">Home</a>
    <a href="/blog/">Blog</a>
    <a href="/help/">Help</a>
    <a href="https://app.leadcove.io/">Sign in</a>
  </nav>
  <div class="nav-cta">
    <a href="https://app.leadcove.io/" class="btn-ghost">Sign in</a>
    <a href="https://app.leadcove.io/#signup" class="btn-primary">Sign up</a>
  </div>
</header>

<article class="post">
  <a class="post-back" href="/blog/tcpa-florida-real-estate-agents.html">← TCPA + state mini-TCPAs overview</a>
  <p class="post-eyebrow">Compliance reference · {name}</p>
  <h1>Real estate prospecting laws in {name}</h1>
  <p class="post-meta">Updated 2026 · Federal + state rules every agent should know before dialing</p>

  <div class="post-body">

    <p>
      This page is a plain-language reference for real estate agents
      prospecting in {name}. Federal Telephone Consumer Protection Act
      (TCPA), the national Do Not Call registry,
      {f'{name}\'s state-level layers, ' if (mini_tcpa or has_state_dnc) else ''}
      and the 4-step compliance checklist agents run before any cold
      outreach. This is not legal advice — when something on a real call
      gives you pause, check with a real attorney.
    </p>

    <h2>Federal floor: TCPA and the national DNC registry</h2>

    <p>
      <strong>Telephone Consumer Protection Act (TCPA), 1991+.</strong>
      You can't use an autodialer, prerecorded message, or automated text
      to contact a residential or mobile phone without prior express
      consent. Manual single-number dialing is generally allowed; automated
      mass dialing is not. Damages: $500 per violation, trebled to $1,500
      for willful violations. Private right of action.
    </p>

    <p>
      <strong>National Do Not Call registry (FTC).</strong> 240M+ numbers
      registered. Real estate cold calls are solicitation; there's no
      broad real-estate exemption. FTC enforcement damages up to $51,744
      per call, plus private-action damages.
    </p>
    {state_section}
    <h2>The 4-step compliance checklist</h2>

    <ol>
      <li><strong>Run every phone against the DNC registry.</strong> Federal + state where applicable. Reputable owner-data tools (LeadCove, BatchLeads, PropStream) do this inline.</li>
      <li><strong>Flag TCPA litigators.</strong> Some consumers have a pattern of suing solicitors for TCPA/state-level violations. Skip them entirely; the legal exposure isn't worth one possible deal.</li>
      <li><strong>Respect calling hours.</strong> Federal TCPA: 8am-9pm in the consumer's local time. Most state mini-TCPAs match or restrict further.</li>
      <li><strong>Identify yourself and the brokerage immediately</strong> on every call. Several states require this by statute; doing it everywhere is good practice.</li>
    </ol>

    <div class="post-callout">
      <p>
        <strong>Cheapest insurance in real estate prospecting:</strong>
        an enrichment check on every lead before you dial. One credit
        (about 30 cents on the standard plan) pays for itself the first
        time it dodges a DNC number. Compared to a $1,500 fine, that's
        not insurance — it's a no-brainer.
      </p>
    </div>

    <h2>FAQ</h2>

    <div class="faq-item">
      <p class="faq-q">Is it legal to cold call property owners in {name}?</p>
      <p class="faq-a">
        Yes when done correctly. Federal TCPA, the national Do Not Call
        registry,
        {f'and {name}\'s state-level layers ' if (mini_tcpa or has_state_dnc) else ''}
        all govern outbound real estate prospecting. Use a tool that
        flags DNC and TCPA-litigator records before dialing, respect
        calling hours, identify yourself immediately.
      </p>
    </div>

    <div class="faq-item">
      <p class="faq-q">Does {name} have its own Do Not Call list?</p>
      <p class="faq-a">
        {f'Yes — {name} maintains a state Do Not Call list in addition to the federal registry. Reputable tools flag both.' if has_state_dnc else f'No — {name} does not maintain a separate state Do Not Call list. The federal registry is the canonical compliance source.'}
      </p>
    </div>

    <div class="faq-item">
      <p class="faq-q">What are the fines for TCPA violations in {name}?</p>
      <p class="faq-a">
        Federal TCPA: $500 per violation, $1,500 if willful. National
        DNC violations carry up to $51,744 per call in FTC enforcement.
        {f'{name} state-level damages: see the mini-TCPA section above.' if mini_tcpa else ''}
      </p>
    </div>

    <h2>Related</h2>

    <ul>
      <li><a href="/blog/tcpa-florida-real-estate-agents.html">TCPA + state mini-TCPAs: what triggers a fine</a> — the broader overview</li>
      <li><a href="/find-property-owner/{slug}.html">Find a property owner in {name}</a> — the address-to-owner workflow</li>
      <li><a href="/blog/skip-tracing-tools-comparison.html">Skip tracing tools: a neutral comparison</a></li>
    </ul>

  </div>
</article>

<section class="post-cta">
  <h2>Prospect cleanly. DNC and TCPA flags inline.</h2>
  <p>Drop a CSV of addresses, get verified owner data with compliance flags. 7-day trial, no charge today.</p>
  <div class="hero-ctas">
    <a href="https://app.leadcove.io/#signup" class="btn-primary btn-lg">Start the trial</a>
    <a href="/free-lookup.html" class="btn-ghost btn-lg">Try the free address lookup</a>
  </div>
</section>

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
    <a href="/#tour">Tour</a>
    <a href="/#plans">Pricing</a>
    <a href="/#faq">FAQ</a>
    <a href="/about.html">About</a>
    <a href="/blog/">Blog</a>
  </div>
  <div class="footer-col">
    <h5>Account</h5>
    <a href="https://app.leadcove.io/">Sign in</a>
    <a href="https://app.leadcove.io/#signup">Sign up</a>
    <a href="mailto:hello@leadcove.io">hello@leadcove.io</a>
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

</body>
</html>
'''
    return HEAD_TEMPLATE + body


def main():
    for state in STATES:
        slug = state[1]
        path = OUT_DIR / f'{slug}.html'
        path.write_text(render(state))
    print(f'✓ Wrote {len(STATES)} state law pages → real-estate-prospecting-laws/')


if __name__ == '__main__':
    main()
