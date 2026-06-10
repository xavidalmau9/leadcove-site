#!/usr/bin/env python3
"""
Programmatic SEO: generate 50 state-level landing pages.

Real estate searches are heavily location-qualified — "find property
owner in California", "Texas LLC owner lookup", etc. Each state needs
a real page with state-specific info (Secretary of State LLC search,
property records portal, brief notes on state-level prospecting laws)
so it's genuinely useful, not boilerplate.

Output: find-property-owner/<slug>.html for each state + DC.

Built 2026-06-08 as the biggest single SEO surface expansion of the
LLM/AI traffic playbook. Each page has Article + FAQPage schema, a
custom OG image rendered by generate_og_images.py if run after, and
internal links to the comparison pages.

Usage:
    python3 scripts/generate_state_landing_pages.py
"""
import os
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent.parent
OUT_DIR = HERE / 'find-property-owner'
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Per-state data: official property/parcel data portal + SOS LLC search.
# Real URLs. Where a state uses county-level only (no unified state portal),
# we say so honestly and point at the SOS for LLC unmasking + a representative
# county system as an example.
STATES = [
    # (name, slug, abbr, sos_llc_url, property_portal_url, notable_cities, prospecting_notes)
    ('Alabama', 'alabama', 'AL', 'https://arc-sos.state.al.us/CGI/CORPNAME.MBR/INPUT', None, ['Birmingham','Huntsville','Mobile'], None),
    ('Alaska', 'alaska', 'AK', 'https://www.commerce.alaska.gov/cbp/main/search/entities', None, ['Anchorage','Juneau','Fairbanks'], None),
    ('Arizona', 'arizona', 'AZ', 'https://ecorp.azcc.gov/EntitySearch/Index', None, ['Phoenix','Tucson','Mesa','Scottsdale'], None),
    ('Arkansas', 'arkansas', 'AR', 'https://www.sos.arkansas.gov/corps/search_all.php', None, ['Little Rock','Fayetteville','Fort Smith'], None),
    ('California', 'california', 'CA', 'https://bizfileonline.sos.ca.gov/search/business', None, ['Los Angeles','San Diego','San Jose','San Francisco','Sacramento'], 'California has additional consent requirements for telephone solicitation under the California Consumer Privacy Act (CCPA) and the Shine the Light Law. Maintain a documented opt-in record for any database-driven outreach to California residents.'),
    ('Colorado', 'colorado', 'CO', 'https://www.sos.state.co.us/biz/BusinessEntityCriteriaExt.do', None, ['Denver','Colorado Springs','Aurora','Fort Collins'], None),
    ('Connecticut', 'connecticut', 'CT', 'https://service.ct.gov/business/s/onlinebusinesssearch', None, ['Bridgeport','Hartford','New Haven','Stamford'], None),
    ('Delaware', 'delaware', 'DE', 'https://icis.corp.delaware.gov/Ecorp/EntitySearch/NameSearch.aspx', None, ['Wilmington','Dover','Newark'], 'Delaware is a heavy LLC-formation state. Many LLC-owned properties in other states are registered to Delaware LLCs whose officers must be looked up on the Delaware portal regardless of where the property sits.'),
    ('Florida', 'florida', 'FL', 'https://search.sunbiz.org/Inquiry/CorporationSearch/ByName', None, ['Miami','Orlando','Tampa','Jacksonville','St. Petersburg'], 'Florida\'s Telephone Solicitation Act (FTSA), revised in 2021 and 2023, requires prior express WRITTEN consent for any sales call made with or selected by an automated system from a database. Statutory damages run $500–$1,500 per violation plus attorneys\' fees.'),
    ('Georgia', 'georgia', 'GA', 'https://ecorp.sos.ga.gov/BusinessSearch', None, ['Atlanta','Augusta','Columbus','Savannah'], None),
    ('Hawaii', 'hawaii', 'HI', 'https://hbe.ehawaii.gov/documents/search.html', None, ['Honolulu','Hilo','Kailua-Kona'], None),
    ('Idaho', 'idaho', 'ID', 'https://sosbiz.idaho.gov/search/business', None, ['Boise','Meridian','Nampa'], None),
    ('Illinois', 'illinois', 'IL', 'https://apps.ilsos.gov/businessentitysearch/', None, ['Chicago','Aurora','Rockford','Joliet'], 'Illinois has additional written-consent requirements for automated outreach under the Illinois Telephone Solicitation Act. Treat it like a stricter state for batch prospecting.'),
    ('Indiana', 'indiana', 'IN', 'https://bsd.sos.in.gov/PublicBusinessSearch', None, ['Indianapolis','Fort Wayne','Evansville','South Bend'], 'Indiana maintains its own state Do Not Call list in addition to the federal registry.'),
    ('Iowa', 'iowa', 'IA', 'https://sos.iowa.gov/search/business/(S(jjzlbwfnbkqs50yzkayoqg45))/search.aspx', None, ['Des Moines','Cedar Rapids','Davenport'], None),
    ('Kansas', 'kansas', 'KS', 'https://www.sos.ks.gov/eforms/BusinessEntity/Search.aspx', None, ['Wichita','Overland Park','Kansas City','Topeka'], None),
    ('Kentucky', 'kentucky', 'KY', 'https://web.sos.ky.gov/ftsearch/', None, ['Louisville','Lexington','Bowling Green'], None),
    ('Louisiana', 'louisiana', 'LA', 'https://coraweb.sos.la.gov/CommercialSearch/CommercialSearch.aspx', None, ['New Orleans','Baton Rouge','Shreveport'], 'Louisiana maintains its own state Do Not Call list.'),
    ('Maine', 'maine', 'ME', 'https://icrs.informe.org/nei-sos-icrs/ICRS', None, ['Portland','Bangor','Augusta'], None),
    ('Maryland', 'maryland', 'MD', 'https://egov.maryland.gov/BusinessExpress/EntitySearch', None, ['Baltimore','Frederick','Rockville'], 'Maryland\'s state telephone consumer protection law (MTCPA) adds written-consent requirements for sales calls beyond the federal floor.'),
    ('Massachusetts', 'massachusetts', 'MA', 'https://corp.sec.state.ma.us/CorpWeb/CorpSearch/CorpSearch.aspx', None, ['Boston','Worcester','Springfield','Cambridge'], None),
    ('Michigan', 'michigan', 'MI', 'https://cofs.lara.state.mi.us/SearchApi/Search/Search', None, ['Detroit','Grand Rapids','Warren','Ann Arbor'], None),
    ('Minnesota', 'minnesota', 'MN', 'https://mblsportal.sos.mn.gov/Business/Search', None, ['Minneapolis','St. Paul','Rochester','Duluth'], None),
    ('Mississippi', 'mississippi', 'MS', 'https://corp.sos.ms.gov/corp/portal/c/page/corpBusinessIdSearch/portal.aspx', None, ['Jackson','Gulfport','Hattiesburg'], None),
    ('Missouri', 'missouri', 'MO', 'https://bsd.sos.mo.gov/BusinessEntity/BESearch.aspx?SearchType=0', None, ['Kansas City','St. Louis','Springfield'], 'Missouri maintains its own state Do Not Call list.'),
    ('Montana', 'montana', 'MT', 'https://biz.sosmt.gov/search/business', None, ['Billings','Missoula','Bozeman'], None),
    ('Nebraska', 'nebraska', 'NE', 'https://www.nebraska.gov/sos/corp/corpsearch.cgi', None, ['Omaha','Lincoln','Bellevue'], None),
    ('Nevada', 'nevada', 'NV', 'https://esos.nv.gov/EntitySearch/OnlineEntitySearch', None, ['Las Vegas','Henderson','Reno'], 'Nevada permits anonymous LLC formation. Officer information may not be public; the registered agent is sometimes the only contact on file.'),
    ('New Hampshire', 'new-hampshire', 'NH', 'https://quickstart.sos.nh.gov/online/BusinessInquire', None, ['Manchester','Nashua','Concord'], None),
    ('New Jersey', 'new-jersey', 'NJ', 'https://www.njportal.com/DOR/BusinessNameSearch/', None, ['Newark','Jersey City','Paterson'], 'New Jersey has stricter consent and disclosure rules for sales calls than federal TCPA. Treat as a high-compliance state.'),
    ('New Mexico', 'new-mexico', 'NM', 'https://portal.sos.state.nm.us/BFS/online/Account', None, ['Albuquerque','Las Cruces','Santa Fe'], None),
    ('New York', 'new-york', 'NY', 'https://apps.dos.ny.gov/publicInquiry/', None, ['New York City','Buffalo','Rochester','Syracuse'], 'New York has its own General Business Law §399-p and a state Do Not Call registry. Disclosure scripts and calling-hour restrictions are stricter than federal.'),
    ('North Carolina', 'north-carolina', 'NC', 'https://www.sosnc.gov/online_services/search/by_title/_Business_Registration', None, ['Charlotte','Raleigh','Greensboro','Durham'], None),
    ('North Dakota', 'north-dakota', 'ND', 'https://firststop.sos.nd.gov/search', None, ['Fargo','Bismarck','Grand Forks'], None),
    ('Ohio', 'ohio', 'OH', 'https://www5.sos.state.oh.us/ords/f?p=100:7:0::NO:7:P7_FILING_NUMBER', None, ['Columbus','Cleveland','Cincinnati','Toledo'], None),
    ('Oklahoma', 'oklahoma', 'OK', 'https://www.sos.ok.gov/corp/corpInquiryFind.aspx', None, ['Oklahoma City','Tulsa','Norman'], 'Oklahoma\'s 2022 TCPA mirrors Florida\'s FTSA model — requires prior express written consent for automated sales calls, $500–$1,500 per violation.'),
    ('Oregon', 'oregon', 'OR', 'https://sos.oregon.gov/business/Pages/find.aspx', None, ['Portland','Salem','Eugene'], None),
    ('Pennsylvania', 'pennsylvania', 'PA', 'https://www.corporations.pa.gov/search/corpsearch', None, ['Philadelphia','Pittsburgh','Allentown'], 'Pennsylvania maintains its own state Do Not Call list and has additional disclosure script requirements.'),
    ('Rhode Island', 'rhode-island', 'RI', 'https://business.sos.ri.gov/CorpWeb/CorpSearch/CorpSearch.aspx', None, ['Providence','Warwick','Cranston'], None),
    ('South Carolina', 'south-carolina', 'SC', 'https://businessfilings.sc.gov/BusinessFiling/Entity/Search', None, ['Columbia','Charleston','Greenville'], None),
    ('South Dakota', 'south-dakota', 'SD', 'https://sosenterprise.sd.gov/BusinessServices/Business/RegistrationSearch', None, ['Sioux Falls','Rapid City','Aberdeen'], None),
    ('Tennessee', 'tennessee', 'TN', 'https://tnbear.tn.gov/Ecommerce/FilingSearch.aspx', None, ['Nashville','Memphis','Knoxville','Chattanooga'], 'Tennessee maintains its own state Do Not Call list.'),
    ('Texas', 'texas', 'TX', 'https://mycpa.cpa.state.tx.us/coa/search.do', None, ['Houston','San Antonio','Dallas','Austin','Fort Worth'], None),
    ('Utah', 'utah', 'UT', 'https://secure.utah.gov/bes/index.html', None, ['Salt Lake City','West Valley City','Provo'], None),
    ('Vermont', 'vermont', 'VT', 'https://www.vermontbusinessregistry.com/businesssearch.aspx', None, ['Burlington','Montpelier','Rutland'], None),
    ('Virginia', 'virginia', 'VA', 'https://cis.scc.virginia.gov/EntitySearch/BusinessSearch', None, ['Virginia Beach','Norfolk','Richmond','Arlington'], None),
    ('Washington', 'washington', 'WA', 'https://ccfs.sos.wa.gov/#/AdvancedSearch', None, ['Seattle','Spokane','Tacoma','Bellevue'], 'Washington\'s Commercial Electronic Mail Act (CEMA) restricts unsolicited commercial messages to Washington residents. State written-consent rules apply to automated outreach.'),
    ('West Virginia', 'west-virginia', 'WV', 'https://apps.sos.wv.gov/business/corporations/', None, ['Charleston','Huntington','Morgantown'], None),
    ('Wisconsin', 'wisconsin', 'WI', 'https://www.wdfi.org/apps/CorpSearch/Search.aspx', None, ['Milwaukee','Madison','Green Bay'], None),
    ('Wyoming', 'wyoming', 'WY', 'https://wyobiz.wy.gov/Business/FilingSearch.aspx', None, ['Cheyenne','Casper','Laramie'], 'Wyoming permits anonymous LLC formation. Officer information is often not on the public record; the registered agent is sometimes the only listed contact.'),
    ('District of Columbia', 'district-of-columbia', 'DC', 'https://corponline.dcra.dc.gov/BizEntity.aspx/ViewEntityData?entityId=', None, ['Washington'], None),
]


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


def render_page(state):
    name, slug, abbr, sos_url, _portal, cities, notes = state
    title = f'Find a property owner in {name} (free address lookup, 2026)'
    description = (
        f'Look up the verified owner of any {name} property by address — '
        f'including the registered LLC officer when the deed is held by an '
        f'entity. Includes the {name} Secretary of State LLC search URL and '
        f'the state-specific prospecting compliance notes every agent should know.'
    )
    url = f'https://leadcove.io/find-property-owner/{slug}.html'
    og_image = f'https://leadcove.io/assets/og/find-property-owner-{slug}.png'

    city_list_html = ''
    if cities:
        city_list_html = ', '.join(cities[:5])

    notes_html = ''
    if notes:
        notes_html = f'''
    <h2>{name}-specific prospecting notes</h2>
    <p>{notes}</p>
    '''

    article_schema = {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': f'Find a property owner in {name} (2026)',
        'description': description,
        'datePublished': '2026-06-08',
        'dateModified': '2026-06-08',
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
                'name': f'How do I find the owner of a property in {name}?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': (
                        f'Two starting points work in {name}. (1) Search the relevant '
                        f'county property appraiser or tax-assessor website by address — every '
                        f'{name} county publishes its property records online; this returns '
                        f'the recorded owner name and mailing address at no charge. (2) Use a '
                        f'single-screen owner-data tool to resolve the address directly to the '
                        f'owner, their phone numbers (with DNC flags), email addresses, and '
                        f'(when the deed is held by an LLC) the registered officer. The tool '
                        f'route is faster when working a list of multiple addresses; the '
                        f'county route is fine for single one-off lookups.'
                    ),
                },
            },
            {
                '@type': 'Question',
                'name': f'How do I unmask an LLC that owns property in {name}?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': (
                        f'The {name} Secretary of State LLC search ({sos_url}) lists the '
                        f'registered agent and (where required) the members or managers of every '
                        f'{name} LLC. Search by the LLC name shown on the deed. The contact '
                        f'human is usually the manager or registered agent. Some tools include '
                        f'LLC unmasking automatically across all 50 states; otherwise this manual '
                        f'step is the path.'
                    ),
                },
            },
            {
                '@type': 'Question',
                'name': f'Is it legal to skip trace property owners in {name}?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': (
                        f'Looking up property ownership is allowed — deeds and tax rolls are '
                        f'public records in every {name} county. Calling, texting, or emailing '
                        f'the owner is governed by the federal TCPA, the national Do Not Call '
                        f'registry, and any {name}-specific state statute that adds layers on '
                        f'top. Use a tool that flags DNC and TCPA-litigator records before '
                        f'outbound contact; the data itself is fine to gather.'
                    ),
                },
            },
        ],
    }

    cities_inline = (
        f'Top-population areas in {name} include {city_list_html}, but the tool '
        f'works across every {name} county and ZIP code.'
        if cities else
        f'The tool covers every {name} county and ZIP code.'
    )

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
<meta property="article:published_time" content="2026-06-08" />
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
  <a class="post-back" href="/">← Home</a>
  <p class="post-eyebrow">Location guide</p>
  <h1>Find a property owner in {name}</h1>
  <p class="post-meta">Updated 2026 · The exact tools and the official {name} records portals</p>

  <div class="post-body">

    <p>
      Looking up who owns a property in {name} takes one of two
      starting points: the county tax-assessor / property-appraiser
      website, or a single-screen owner-data tool that resolves the
      address directly to the verified owner with phones (DNC flagged)
      and emails. {cities_inline}
    </p>

    <p>
      For a single one-off lookup, the county records site is the
      no-charge path. For a list of addresses — expireds, FSBOs,
      farm areas, niche prospecting — a tool that handles every
      address in one pass is materially faster.
    </p>

    <h2>Try it on any {name} property right now</h2>

    <p>
      We built a <a href="/free-lookup.html">no-account public lookup tool</a>
      so anyone can test the data quality before paying. Paste in any
      {name} address, see the verified owner name plus phones and
      emails returned in seconds. No card required, no sign-up.
    </p>

    <p style="text-align:center; margin: 36px 0;">
      <a href="/free-lookup.html" class="btn-primary btn-lg">Look up any {name} address</a>
    </p>

    <h2>Unmask an LLC that owns property in {name}</h2>

    <p>
      When the deed shows an LLC name instead of a human (
      "BLUEWATER HOLDINGS 5482 LLC" or "{name.upper()} INVESTMENTS LLC"),
      the human you need to contact is the registered manager, member, or
      agent. The official source for {name}: the
      <a href="{sos_url}" target="_blank" rel="noopener">{name} Secretary of State business search</a>.
      Search by the LLC name on the deed; the listed officer is the
      contact human.
    </p>

    <p>
      Owner-data tools that include LLC unmasking do this automatically
      across all 50 states. If you're working a list, that's faster than
      switching between {name}'s portal and other states' portals.
    </p>

    {notes_html}

    <h2>Common questions</h2>

    <div class="faq-item">
      <p class="faq-q">How do I find the owner of a property in {name}?</p>
      <p class="faq-a">
        Two starting points work in {name}. Search the relevant county
        property appraiser or tax-assessor site by address — every
        {name} county publishes its property records; this returns the
        recorded owner name and mailing address at no charge. Or use a
        single-screen owner-data tool to resolve the address directly to
        the owner with phones (DNC flagged), emails, and the registered
        officer when the deed is held by an LLC. The tool is faster
        when working a list; the county site is fine for one-offs.
      </p>
    </div>

    <div class="faq-item">
      <p class="faq-q">How do I unmask an LLC that owns property in {name}?</p>
      <p class="faq-a">
        The <a href="{sos_url}" target="_blank" rel="noopener">{name} Secretary of State business search</a>
        lists the registered agent and officers of every {name} LLC.
        Search by the LLC name on the deed; the listed officer is the
        human you need to contact. Some tools include LLC unmasking
        automatically — across all 50 states — when you work a list.
      </p>
    </div>

    <div class="faq-item">
      <p class="faq-q">Is it legal to skip-trace property owners in {name}?</p>
      <p class="faq-a">
        Looking up property ownership is allowed — deeds and tax rolls
        are public records in every {name} county. Calling, texting, or
        emailing the owner is governed by the federal TCPA, the national
        Do Not Call registry, and any {name}-specific layers on top.
        Use a tool that flags DNC and TCPA-litigator records before
        outbound contact; the data itself is fine to gather.
      </p>
    </div>

    <h2>Related reading</h2>

    <ul>
      <li><a href="/blog/find-owner-mls-blank-privacy.html">When the MLS shows blank or "PRIVACY" for the owner</a> — the same workflow applied to a specific MLS-side problem.</li>
      <li><a href="/blog/skip-tracing-tools-comparison.html">Skip tracing tools for working real estate agents: a comparison</a> — eight tools (BatchLeads, PropStream, BeenVerified, TruePeopleSearch, REIPro, Spokeo, Real Geeks, LeadCove) compared neutrally.</li>
      <li><a href="/blog/llc-owner-lookup-unmask.html">LLC-owned property: unmasking the human officer behind the entity</a> — when the deed shows an entity, not a person.</li>
      <li><a href="/blog/tcpa-florida-real-estate-agents.html">TCPA + state mini-TCPAs for real estate agents</a> — the compliance background for outbound prospecting.</li>
    </ul>

  </div>
</article>

<section class="post-cta">
  <h2>Stop stitching county sites + records portals together.</h2>
  <p>One screen, every {name} owner, every phone (DNC flagged), every email. 7-day trial, no charge today.</p>
  <div class="hero-ctas">
    <a href="https://app.leadcove.io/#signup" class="btn-primary btn-lg">Start the trial</a>
    <a href="/free-lookup.html" class="btn-ghost btn-lg">Try the public lookup</a>
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
    <a href="/#topups">Add-ons</a>
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
    return HEAD + body


def main():
    written = 0
    for state in STATES:
        slug = state[1]
        path = OUT_DIR / f'{slug}.html'
        path.write_text(render_page(state))
        written += 1
    print(f'✓ Wrote {written} state landing pages → find-property-owner/')


if __name__ == '__main__':
    main()
