#!/usr/bin/env python3
"""
Programmatic SEO: top US county landing pages.

Real estate prospecting often happens at the county level — every
county runs its own property appraiser / assessor portal, deeds are
recorded at the county clerk, and "[county] property records" is a
high-volume search query.

Output: find-property-owner/county-<county-slug>-<state-abbr>.html
Slug prefix "county-" disambiguates from city slugs (e.g.,
"county-los-angeles-ca" vs "los-angeles-ca").

Built 2026-06-10 as round 5 of the LLM/AI traffic playbook.
"""
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent.parent
OUT_DIR = HERE / 'find-property-owner'
OUT_DIR.mkdir(parents=True, exist_ok=True)


def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", '', s)
    s = re.sub(r'[\s_-]+', '-', s)
    return s.strip('-')


# Top US counties by population. (county_name, state_abbr, principal_city).
# Approximate ranking by 2020 census + recent estimates.
COUNTIES = [
    ('Los Angeles', 'CA', 'Los Angeles'),
    ('Cook', 'IL', 'Chicago'),
    ('Harris', 'TX', 'Houston'),
    ('Maricopa', 'AZ', 'Phoenix'),
    ('San Diego', 'CA', 'San Diego'),
    ('Orange', 'CA', 'Santa Ana'),
    ('Miami-Dade', 'FL', 'Miami'),
    ('Kings', 'NY', 'Brooklyn'),
    ('Dallas', 'TX', 'Dallas'),
    ('Queens', 'NY', 'Queens'),
    ('Riverside', 'CA', 'Riverside'),
    ('Clark', 'NV', 'Las Vegas'),
    ('King', 'WA', 'Seattle'),
    ('San Bernardino', 'CA', 'San Bernardino'),
    ('Tarrant', 'TX', 'Fort Worth'),
    ('Bexar', 'TX', 'San Antonio'),
    ('Broward', 'FL', 'Fort Lauderdale'),
    ('Santa Clara', 'CA', 'San Jose'),
    ('New York', 'NY', 'Manhattan'),
    ('Wayne', 'MI', 'Detroit'),
    ('Alameda', 'CA', 'Oakland'),
    ('Middlesex', 'MA', 'Cambridge'),
    ('Suffolk', 'NY', 'Long Island'),
    ('Sacramento', 'CA', 'Sacramento'),
    ('Bronx', 'NY', 'The Bronx'),
    ('Nassau', 'NY', 'Mineola'),
    ('Hillsborough', 'FL', 'Tampa'),
    ('Palm Beach', 'FL', 'West Palm Beach'),
    ('Orange', 'FL', 'Orlando'),
    ('Cuyahoga', 'OH', 'Cleveland'),
    ('Travis', 'TX', 'Austin'),
    ('Mecklenburg', 'NC', 'Charlotte'),
    ('Franklin', 'OH', 'Columbus'),
    ('Fairfax', 'VA', 'Fairfax'),
    ('Hennepin', 'MN', 'Minneapolis'),
    ('Wake', 'NC', 'Raleigh'),
    ('Marion', 'IN', 'Indianapolis'),
    ('Salt Lake', 'UT', 'Salt Lake City'),
    ('Pima', 'AZ', 'Tucson'),
    ('Honolulu', 'HI', 'Honolulu'),
    ('Westchester', 'NY', 'White Plains'),
    ('Pinellas', 'FL', 'St. Petersburg'),
    ('Multnomah', 'OR', 'Portland'),
    ('Fulton', 'GA', 'Atlanta'),
    ('Duval', 'FL', 'Jacksonville'),
    ('Montgomery', 'MD', 'Rockville'),
    ('Snohomish', 'WA', 'Everett'),
    ('DuPage', 'IL', 'Wheaton'),
    ('Contra Costa', 'CA', 'Martinez'),
    ('Bergen', 'NJ', 'Hackensack'),
    ('Oakland', 'MI', 'Pontiac'),
    ('Worcester', 'MA', 'Worcester'),
    ('Hartford', 'CT', 'Hartford'),
    ('Erie', 'NY', 'Buffalo'),
    ('Macomb', 'MI', 'Mount Clemens'),
    ('Pierce', 'WA', 'Tacoma'),
    ('Essex', 'NJ', 'Newark'),
    ('Monroe', 'NY', 'Rochester'),
    ('Hamilton', 'OH', 'Cincinnati'),
    ('Baltimore', 'MD', 'Towson'),
    ('Jefferson', 'KY', 'Louisville'),
    ('Lee', 'FL', 'Fort Myers'),
    ('Anne Arundel', 'MD', 'Annapolis'),
    ('Polk', 'FL', 'Lakeland'),
    ('Davidson', 'TN', 'Nashville'),
    ('Shelby', 'TN', 'Memphis'),
    ('El Paso', 'TX', 'El Paso'),
    ('Collin', 'TX', 'Plano'),
    ('Denton', 'TX', 'Denton'),
    ('Fort Bend', 'TX', 'Sugar Land'),
    ('Hidalgo', 'TX', 'McAllen'),
    ('Williamson', 'TX', 'Georgetown'),
    ('Montgomery', 'TX', 'Conroe'),
    ('Brevard', 'FL', 'Cocoa'),
    ('Volusia', 'FL', 'Daytona Beach'),
    ('Seminole', 'FL', 'Sanford'),
    ('Pasco', 'FL', 'New Port Richey'),
    ('Manatee', 'FL', 'Bradenton'),
    ('Sarasota', 'FL', 'Sarasota'),
    ('Collier', 'FL', 'Naples'),
    ('St. Lucie', 'FL', 'Port St. Lucie'),
    ('DeKalb', 'GA', 'Decatur'),
    ('Gwinnett', 'GA', 'Lawrenceville'),
    ('Cobb', 'GA', 'Marietta'),
    ('Forsyth', 'GA', 'Cumming'),
    ('Hamilton', 'IN', 'Noblesville'),
    ('Lake', 'IL', 'Waukegan'),
    ('Will', 'IL', 'Joliet'),
    ('Lake', 'IN', 'Crown Point'),
    ('Kent', 'MI', 'Grand Rapids'),
    ('Washtenaw', 'MI', 'Ann Arbor'),
    ('Dakota', 'MN', 'Hastings'),
    ('Ramsey', 'MN', 'St. Paul'),
    ('Anoka', 'MN', 'Anoka'),
    ('St. Louis', 'MO', 'Clayton'),
    ('Jackson', 'MO', 'Kansas City'),
    ('Bernalillo', 'NM', 'Albuquerque'),
    ('Douglas', 'NE', 'Omaha'),
    ('Mercer', 'NJ', 'Trenton'),
    ('Hudson', 'NJ', 'Jersey City'),
    ('Union', 'NJ', 'Elizabeth'),
    ('Onondaga', 'NY', 'Syracuse'),
    ('Albany', 'NY', 'Albany'),
    ('Buncombe', 'NC', 'Asheville'),
    ('Guilford', 'NC', 'Greensboro'),
    ('Durham', 'NC', 'Durham'),
    ('Summit', 'OH', 'Akron'),
    ('Montgomery', 'OH', 'Dayton'),
    ('Oklahoma', 'OK', 'Oklahoma City'),
    ('Tulsa', 'OK', 'Tulsa'),
    ('Washington', 'OR', 'Hillsboro'),
    ('Allegheny', 'PA', 'Pittsburgh'),
    ('Montgomery', 'PA', 'Norristown'),
    ('Bucks', 'PA', 'Doylestown'),
    ('Lancaster', 'PA', 'Lancaster'),
    ('Providence', 'RI', 'Providence'),
    ('Charleston', 'SC', 'Charleston'),
    ('Greenville', 'SC', 'Greenville'),
    ('Knox', 'TN', 'Knoxville'),
    ('Hamilton', 'TN', 'Chattanooga'),
    ('Utah', 'UT', 'Provo'),
    ('Davis', 'UT', 'Farmington'),
    ('Chesterfield', 'VA', 'Chesterfield'),
    ('Loudoun', 'VA', 'Leesburg'),
    ('Prince William', 'VA', 'Manassas'),
    ('Virginia Beach', 'VA', 'Virginia Beach'),
    ('Spokane', 'WA', 'Spokane'),
    ('Milwaukee', 'WI', 'Milwaukee'),
    ('Dane', 'WI', 'Madison'),
    ('Waukesha', 'WI', 'Waukesha'),
    ('Larimer', 'CO', 'Fort Collins'),
    ('Boulder', 'CO', 'Boulder'),
    ('Adams', 'CO', 'Brighton'),
    ('Arapahoe', 'CO', 'Littleton'),
    ('Jefferson', 'CO', 'Golden'),
    ('Denver', 'CO', 'Denver'),
    ('El Paso', 'CO', 'Colorado Springs'),
    ('Pulaski', 'AR', 'Little Rock'),
    ('Davidson', 'NC', 'Lexington'),
    ('Cumberland', 'NC', 'Fayetteville'),
    ('Fairfield', 'CT', 'Bridgeport'),
    ('New Haven', 'CT', 'New Haven'),
    ('Plymouth', 'MA', 'Brockton'),
    ('Norfolk', 'MA', 'Dedham'),
    ('Bristol', 'MA', 'Taunton'),
    ('Essex', 'MA', 'Salem'),
    ('Hillsborough', 'NH', 'Manchester'),
    ('Rockingham', 'NH', 'Brentwood'),
]


STATE_SLUGS = {
    'AL': 'alabama', 'AK': 'alaska', 'AZ': 'arizona', 'AR': 'arkansas',
    'CA': 'california', 'CO': 'colorado', 'CT': 'connecticut',
    'DE': 'delaware', 'FL': 'florida', 'GA': 'georgia', 'HI': 'hawaii',
    'ID': 'idaho', 'IL': 'illinois', 'IN': 'indiana', 'IA': 'iowa',
    'KS': 'kansas', 'KY': 'kentucky', 'LA': 'louisiana', 'ME': 'maine',
    'MD': 'maryland', 'MA': 'massachusetts', 'MI': 'michigan',
    'MN': 'minnesota', 'MS': 'mississippi', 'MO': 'missouri',
    'MT': 'montana', 'NE': 'nebraska', 'NV': 'nevada',
    'NH': 'new-hampshire', 'NJ': 'new-jersey', 'NM': 'new-mexico',
    'NY': 'new-york', 'NC': 'north-carolina', 'ND': 'north-dakota',
    'OH': 'ohio', 'OK': 'oklahoma', 'OR': 'oregon',
    'PA': 'pennsylvania', 'RI': 'rhode-island', 'SC': 'south-carolina',
    'SD': 'south-dakota', 'TN': 'tennessee', 'TX': 'texas',
    'UT': 'utah', 'VT': 'vermont', 'VA': 'virginia',
    'WA': 'washington', 'WV': 'west-virginia', 'WI': 'wisconsin',
    'WY': 'wyoming', 'DC': 'district-of-columbia',
}

STATE_NAMES = {
    'AL':'Alabama','AK':'Alaska','AZ':'Arizona','AR':'Arkansas',
    'CA':'California','CO':'Colorado','CT':'Connecticut',
    'DE':'Delaware','FL':'Florida','GA':'Georgia','HI':'Hawaii',
    'ID':'Idaho','IL':'Illinois','IN':'Indiana','IA':'Iowa',
    'KS':'Kansas','KY':'Kentucky','LA':'Louisiana','ME':'Maine',
    'MD':'Maryland','MA':'Massachusetts','MI':'Michigan',
    'MN':'Minnesota','MS':'Mississippi','MO':'Missouri',
    'MT':'Montana','NE':'Nebraska','NV':'Nevada',
    'NH':'New Hampshire','NJ':'New Jersey','NM':'New Mexico',
    'NY':'New York','NC':'North Carolina','ND':'North Dakota',
    'OH':'Ohio','OK':'Oklahoma','OR':'Oregon',
    'PA':'Pennsylvania','RI':'Rhode Island','SC':'South Carolina',
    'SD':'South Dakota','TN':'Tennessee','TX':'Texas',
    'UT':'Utah','VT':'Vermont','VA':'Virginia',
    'WA':'Washington','WV':'West Virginia','WI':'Wisconsin',
    'WY':'Wyoming','DC':'District of Columbia',
}


HEAD = '''<!doctype html>
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


def render(county, abbr, principal_city):
    state_name = STATE_NAMES[abbr]
    state_slug = STATE_SLUGS[abbr]
    slug = f'county-{slugify(county)}-{abbr.lower()}'
    title = f'Find a property owner in {county} County, {state_name} (free address lookup, 2026)'
    description = (
        f'Look up the verified owner of any {county} County property by '
        f'address — including the registered LLC officer when the deed is '
        f'held by an entity. Pulls from {county} County records + licensed '
        f'B2B data, with DNC and TCPA-litigator flags applied before any outreach.'
    )
    url = f'https://leadcove.io/find-property-owner/{slug}.html'
    og_image = f'https://leadcove.io/assets/og/find-property-owner-{slug}.png'

    article_schema = {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': f'Find a property owner in {county} County, {state_name}',
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
                'name': f'How do I find the owner of a property in {county} County, {state_name}?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': (
                        f'Two starting points work in {county} County. The county '
                        f'property appraiser or assessor website publishes the '
                        f'recorded owner name and mailing address for every property '
                        f'in the county at no charge. For a list of {county} County '
                        f'addresses, a single-screen owner-data tool resolves each '
                        f'address directly to the verified owner with phones (DNC '
                        f'flagged), emails, and the registered LLC officer when '
                        f'entity-owned. The tool route is faster for multi-address '
                        f'workflows; the county portal is fine for single one-offs.'
                    ),
                },
            },
            {
                '@type': 'Question',
                'name': f'Where do I find {county} County property records?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': (
                        f'{county} County publishes property records through its '
                        f'official tax assessor or property appraiser website. Records '
                        f'include the recorded owner, mailing address, assessed value, '
                        f'tax history, and (in most counties) a link to the recorded '
                        f'deed. Search the county name + "property records" or "tax '
                        f'assessor" to find the official portal.'
                    ),
                },
            },
            {
                '@type': 'Question',
                'name': f'Is it legal to look up property owners in {county} County?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': (
                        f'Yes — property ownership records are public information in '
                        f'every {state_name} county. Contacting the owner is governed '
                        f'by the federal TCPA, the national Do Not Call registry, and '
                        f'any {state_name}-specific layers. Use a tool that flags DNC '
                        f'and TCPA-litigator records before outbound contact.'
                    ),
                },
            },
        ],
    }

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
  .post {{ max-width: 720px; margin: 0 auto; padding: 56px 40px 40px; }}
  .post-eyebrow {{ font-size: 12px; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: var(--teal-2); margin: 0 0 14px; }}
  .post h1 {{ font-family: var(--f-display); font-weight: 600; font-size: clamp(34px, 4.2vw, 48px); line-height: 1.08; letter-spacing: -0.02em; color: var(--navy); margin: 0 0 18px; }}
  .post-meta {{ font-size: 14px; color: var(--muted); margin: 0 0 36px; padding-bottom: 24px; border-bottom: 1px solid var(--hairline); }}
  .post-body {{ color: var(--ink-2); font-size: 17px; line-height: 1.72; }}
  .post-body p {{ margin: 0 0 22px; }}
  .post-body strong {{ color: var(--navy); }}
  .post-body h2 {{ font-family: var(--f-display); font-weight: 600; font-size: 28px; line-height: 1.2; letter-spacing: -0.01em; color: var(--navy); margin: 44px 0 14px; }}
  .post-body ul {{ padding-left: 22px; margin: 0 0 22px; }}
  .post-body li {{ margin: 0 0 8px; }}
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
  <a class="post-back" href="/find-property-owner/{state_slug}.html">← {state_name}</a>
  <p class="post-eyebrow">Location guide · {county} County, {abbr}</p>
  <h1>Find a property owner in {county} County, {state_name}</h1>
  <p class="post-meta">Updated 2026 · {county} County records + the workflow that scales beyond one address</p>

  <div class="post-body">

    <p>
      Looking up who owns a {county} County property — the county
      seat is {principal_city} — takes one of two starting points: the
      official county property appraiser or assessor website, or a
      single-screen owner-data tool that resolves the address directly
      to the verified owner with phones (DNC flagged) and emails.
      For a single one-off lookup, the county records site is the
      no-charge path. For a list of {county} County addresses, a
      tool that handles every address in one pass is materially
      faster.
    </p>

    <h2>Try the free address lookup on any {county} County property</h2>

    <p>
      Paste any address in {county} County into our
      <a href="/free-lookup.html">free address lookup tool</a> and see
      the verified owner name plus phones and emails returned in
      seconds. No account, no card.
    </p>

    <p style="text-align:center; margin: 36px 0;">
      <a href="/free-lookup.html" class="btn-primary btn-lg">Look up any {county} County address</a>
    </p>

    <h2>What's on a {county} County property record</h2>

    <ul>
      <li>The recorded owner name (person or LLC)</li>
      <li>The mailing address (often different from the property location for absentee owners)</li>
      <li>Assessed value and tax history</li>
      <li>Property characteristics (lot size, year built where applicable, square footage)</li>
      <li>A link to the recorded deed in most counties</li>
    </ul>

    <p>
      The county portal does not include the owner's phone number or
      email. To actually reach them, run the owner name + mailing
      address through an owner-data tool, or check consumer-records
      sites manually for one-offs.
    </p>

    <h2>Common questions</h2>

    <div class="faq-item">
      <p class="faq-q">How do I find the owner of a property in {county} County?</p>
      <p class="faq-a">
        The {county} County property appraiser or assessor website
        publishes the recorded owner name and mailing address for
        every property in the county at no charge. For a list of
        addresses, an owner-data tool resolves each one directly to
        the verified owner with phones (DNC flagged) and emails.
      </p>
    </div>

    <div class="faq-item">
      <p class="faq-q">Where do I find {county} County property records?</p>
      <p class="faq-a">
        Through the official {county} County tax assessor or property
        appraiser website. Search the county name + "property records"
        or "tax assessor" to find the official portal. Records include
        the recorded owner, mailing address, assessed value, tax
        history, and a link to the recorded deed in most counties.
      </p>
    </div>

    <div class="faq-item">
      <p class="faq-q">Is it legal to look up property owners in {county} County?</p>
      <p class="faq-a">
        Yes — property ownership records are public information in
        every {state_name} county. Contacting the owner is governed by
        the federal TCPA, the national Do Not Call registry, and any
        {state_name}-specific layers. Use a tool that flags DNC and
        TCPA-litigator records before outbound contact.
      </p>
    </div>

    <h2>Related</h2>

    <ul>
      <li><a href="/find-property-owner/{state_slug}.html">Find a property owner in {state_name}</a> — the state-level guide</li>
      <li><a href="/real-estate-prospecting-laws/{state_slug}.html">{state_name} prospecting laws: TCPA, DNC, and state rules</a></li>
      <li><a href="/blog/skip-tracing-tools-comparison.html">Skip tracing tools comparison</a></li>
      <li><a href="/blog/find-owner-mls-blank-privacy.html">When the MLS shows blank or "PRIVACY"</a></li>
    </ul>

  </div>
</article>

<section class="post-cta">
  <h2>One screen. Every {county} County owner. Every phone (DNC flagged).</h2>
  <p>Drop a CSV of addresses, get verified contact data in seconds. 7-day trial, no charge today.</p>
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
    <a href="/#plans">Pricing</a>
    <a href="/#faq">FAQ</a>
    <a href="/about.html">About</a>
    <a href="/blog/">Blog</a>
    <a href="/press.html">Press kit</a>
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
    return HEAD + body, slug


def main():
    written = 0
    seen = set()
    for county, abbr, principal in COUNTIES:
        html, slug = render(county, abbr, principal)
        if slug in seen:
            continue
        seen.add(slug)
        (OUT_DIR / f'{slug}.html').write_text(html)
        written += 1
    print(f'✓ Wrote {written} county landing pages → find-property-owner/')


if __name__ == '__main__':
    main()
