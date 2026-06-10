#!/usr/bin/env python3
"""
Programmatic SEO: city-level landing pages for "find property owner in
{city}, {state}".

Output: find-property-owner/<city-slug>-<state-abbr>.html

The cities list is extracted from the state landing pages' data
(top cities per state) plus a handful of high-population additions.
Each page links back to its state page and to the comparison + workflow
posts.

Built 2026-06-10 alongside the auto-regen automation, so adding new
cities here + running the script triggers downstream sitemap + OG image
+ IndexNow submission automatically.

Usage:
    python3 scripts/generate_city_landing_pages.py
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


# (city, state_abbr, state_name, sos_url for the state)
# Pulled from state landing pages + augmented. Where multiple cities
# share a state, all use the same SOS URL.
SOS_URLS = {
    'AL': 'https://arc-sos.state.al.us/CGI/CORPNAME.MBR/INPUT',
    'AK': 'https://www.commerce.alaska.gov/cbp/main/search/entities',
    'AZ': 'https://ecorp.azcc.gov/EntitySearch/Index',
    'AR': 'https://www.sos.arkansas.gov/corps/search_all.php',
    'CA': 'https://bizfileonline.sos.ca.gov/search/business',
    'CO': 'https://www.sos.state.co.us/biz/BusinessEntityCriteriaExt.do',
    'CT': 'https://service.ct.gov/business/s/onlinebusinesssearch',
    'DE': 'https://icis.corp.delaware.gov/Ecorp/EntitySearch/NameSearch.aspx',
    'FL': 'https://search.sunbiz.org/Inquiry/CorporationSearch/ByName',
    'GA': 'https://ecorp.sos.ga.gov/BusinessSearch',
    'HI': 'https://hbe.ehawaii.gov/documents/search.html',
    'ID': 'https://sosbiz.idaho.gov/search/business',
    'IL': 'https://apps.ilsos.gov/businessentitysearch/',
    'IN': 'https://bsd.sos.in.gov/PublicBusinessSearch',
    'IA': 'https://sos.iowa.gov/search/business/(S(jjzlbwfnbkqs50yzkayoqg45))/search.aspx',
    'KS': 'https://www.sos.ks.gov/eforms/BusinessEntity/Search.aspx',
    'KY': 'https://web.sos.ky.gov/ftsearch/',
    'LA': 'https://coraweb.sos.la.gov/CommercialSearch/CommercialSearch.aspx',
    'ME': 'https://icrs.informe.org/nei-sos-icrs/ICRS',
    'MD': 'https://egov.maryland.gov/BusinessExpress/EntitySearch',
    'MA': 'https://corp.sec.state.ma.us/CorpWeb/CorpSearch/CorpSearch.aspx',
    'MI': 'https://cofs.lara.state.mi.us/SearchApi/Search/Search',
    'MN': 'https://mblsportal.sos.mn.gov/Business/Search',
    'MS': 'https://corp.sos.ms.gov/corp/portal/c/page/corpBusinessIdSearch/portal.aspx',
    'MO': 'https://bsd.sos.mo.gov/BusinessEntity/BESearch.aspx?SearchType=0',
    'MT': 'https://biz.sosmt.gov/search/business',
    'NE': 'https://www.nebraska.gov/sos/corp/corpsearch.cgi',
    'NV': 'https://esos.nv.gov/EntitySearch/OnlineEntitySearch',
    'NH': 'https://quickstart.sos.nh.gov/online/BusinessInquire',
    'NJ': 'https://www.njportal.com/DOR/BusinessNameSearch/',
    'NM': 'https://portal.sos.state.nm.us/BFS/online/Account',
    'NY': 'https://apps.dos.ny.gov/publicInquiry/',
    'NC': 'https://www.sosnc.gov/online_services/search/by_title/_Business_Registration',
    'ND': 'https://firststop.sos.nd.gov/search',
    'OH': 'https://www5.sos.state.oh.us/ords/f?p=100:7:0::NO:7:P7_FILING_NUMBER',
    'OK': 'https://www.sos.ok.gov/corp/corpInquiryFind.aspx',
    'OR': 'https://sos.oregon.gov/business/Pages/find.aspx',
    'PA': 'https://www.corporations.pa.gov/search/corpsearch',
    'RI': 'https://business.sos.ri.gov/CorpWeb/CorpSearch/CorpSearch.aspx',
    'SC': 'https://businessfilings.sc.gov/BusinessFiling/Entity/Search',
    'SD': 'https://sosenterprise.sd.gov/BusinessServices/Business/RegistrationSearch',
    'TN': 'https://tnbear.tn.gov/Ecommerce/FilingSearch.aspx',
    'TX': 'https://mycpa.cpa.state.tx.us/coa/search.do',
    'UT': 'https://secure.utah.gov/bes/index.html',
    'VT': 'https://www.vermontbusinessregistry.com/businesssearch.aspx',
    'VA': 'https://cis.scc.virginia.gov/EntitySearch/BusinessSearch',
    'WA': 'https://ccfs.sos.wa.gov/#/AdvancedSearch',
    'WV': 'https://apps.sos.wv.gov/business/corporations/',
    'WI': 'https://www.wdfi.org/apps/CorpSearch/Search.aspx',
    'WY': 'https://wyobiz.wy.gov/Business/FilingSearch.aspx',
    'DC': 'https://corponline.dcra.dc.gov/BizEntity.aspx/ViewEntityData?entityId=',
}

STATE_NAMES = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
    'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut',
    'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii',
    'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
    'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine',
    'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan',
    'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri',
    'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
    'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico',
    'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota',
    'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon',
    'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas',
    'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia',
    'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin',
    'WY': 'Wyoming', 'DC': 'District of Columbia',
}

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

# Top cities to generate pages for. (city, state-abbr).
# Includes the top 200+ US cities by population plus selected
# higher-volume real estate markets.
CITIES = [
    ('Birmingham','AL'), ('Huntsville','AL'), ('Mobile','AL'), ('Montgomery','AL'), ('Tuscaloosa','AL'),
    ('Anchorage','AK'), ('Fairbanks','AK'), ('Juneau','AK'),
    ('Phoenix','AZ'), ('Tucson','AZ'), ('Mesa','AZ'), ('Scottsdale','AZ'), ('Chandler','AZ'), ('Glendale','AZ'), ('Gilbert','AZ'), ('Tempe','AZ'), ('Peoria','AZ'), ('Surprise','AZ'),
    ('Little Rock','AR'), ('Fayetteville','AR'), ('Fort Smith','AR'), ('Springdale','AR'),
    ('Los Angeles','CA'), ('San Diego','CA'), ('San Jose','CA'), ('San Francisco','CA'), ('Sacramento','CA'), ('Fresno','CA'), ('Long Beach','CA'), ('Oakland','CA'), ('Bakersfield','CA'), ('Anaheim','CA'), ('Santa Ana','CA'), ('Riverside','CA'), ('Stockton','CA'), ('Irvine','CA'), ('Chula Vista','CA'), ('Fremont','CA'), ('San Bernardino','CA'), ('Modesto','CA'), ('Fontana','CA'), ('Oxnard','CA'), ('Moreno Valley','CA'), ('Huntington Beach','CA'), ('Glendale','CA'), ('Santa Clarita','CA'),
    ('Denver','CO'), ('Colorado Springs','CO'), ('Aurora','CO'), ('Fort Collins','CO'), ('Lakewood','CO'), ('Thornton','CO'), ('Arvada','CO'), ('Westminster','CO'), ('Pueblo','CO'), ('Boulder','CO'),
    ('Bridgeport','CT'), ('Hartford','CT'), ('New Haven','CT'), ('Stamford','CT'), ('Waterbury','CT'),
    ('Wilmington','DE'), ('Dover','DE'),
    ('Miami','FL'), ('Orlando','FL'), ('Tampa','FL'), ('Jacksonville','FL'), ('St Petersburg','FL'), ('Fort Lauderdale','FL'), ('Hialeah','FL'), ('Cape Coral','FL'), ('Port St Lucie','FL'), ('Tallahassee','FL'), ('Pembroke Pines','FL'), ('Hollywood','FL'), ('Gainesville','FL'), ('Coral Springs','FL'), ('Clearwater','FL'),
    ('Atlanta','GA'), ('Augusta','GA'), ('Columbus','GA'), ('Savannah','GA'), ('Athens','GA'), ('Macon','GA'),
    ('Honolulu','HI'), ('Hilo','HI'),
    ('Boise','ID'), ('Meridian','ID'), ('Nampa','ID'),
    ('Chicago','IL'), ('Aurora','IL'), ('Rockford','IL'), ('Joliet','IL'), ('Naperville','IL'), ('Springfield','IL'), ('Peoria','IL'), ('Elgin','IL'),
    ('Indianapolis','IN'), ('Fort Wayne','IN'), ('Evansville','IN'), ('South Bend','IN'), ('Carmel','IN'), ('Bloomington','IN'),
    ('Des Moines','IA'), ('Cedar Rapids','IA'), ('Davenport','IA'),
    ('Wichita','KS'), ('Overland Park','KS'), ('Kansas City','KS'), ('Topeka','KS'),
    ('Louisville','KY'), ('Lexington','KY'), ('Bowling Green','KY'),
    ('New Orleans','LA'), ('Baton Rouge','LA'), ('Shreveport','LA'), ('Lafayette','LA'),
    ('Portland','ME'), ('Bangor','ME'),
    ('Baltimore','MD'), ('Frederick','MD'), ('Rockville','MD'), ('Gaithersburg','MD'),
    ('Boston','MA'), ('Worcester','MA'), ('Springfield','MA'), ('Cambridge','MA'), ('Lowell','MA'),
    ('Detroit','MI'), ('Grand Rapids','MI'), ('Warren','MI'), ('Ann Arbor','MI'), ('Lansing','MI'), ('Sterling Heights','MI'),
    ('Minneapolis','MN'), ('St Paul','MN'), ('Rochester','MN'), ('Duluth','MN'),
    ('Jackson','MS'), ('Gulfport','MS'),
    ('Kansas City','MO'), ('St Louis','MO'), ('Springfield','MO'), ('Columbia','MO'),
    ('Billings','MT'), ('Missoula','MT'), ('Bozeman','MT'),
    ('Omaha','NE'), ('Lincoln','NE'),
    ('Las Vegas','NV'), ('Henderson','NV'), ('Reno','NV'), ('North Las Vegas','NV'),
    ('Manchester','NH'), ('Nashua','NH'),
    ('Newark','NJ'), ('Jersey City','NJ'), ('Paterson','NJ'), ('Elizabeth','NJ'), ('Edison','NJ'),
    ('Albuquerque','NM'), ('Las Cruces','NM'), ('Santa Fe','NM'),
    ('New York','NY'), ('Buffalo','NY'), ('Rochester','NY'), ('Syracuse','NY'), ('Yonkers','NY'), ('Albany','NY'),
    ('Charlotte','NC'), ('Raleigh','NC'), ('Greensboro','NC'), ('Durham','NC'), ('Winston Salem','NC'), ('Fayetteville','NC'),
    ('Fargo','ND'), ('Bismarck','ND'),
    ('Columbus','OH'), ('Cleveland','OH'), ('Cincinnati','OH'), ('Toledo','OH'), ('Akron','OH'), ('Dayton','OH'),
    ('Oklahoma City','OK'), ('Tulsa','OK'), ('Norman','OK'),
    ('Portland','OR'), ('Salem','OR'), ('Eugene','OR'), ('Gresham','OR'),
    ('Philadelphia','PA'), ('Pittsburgh','PA'), ('Allentown','PA'), ('Erie','PA'), ('Reading','PA'),
    ('Providence','RI'), ('Warwick','RI'),
    ('Columbia','SC'), ('Charleston','SC'), ('Greenville','SC'),
    ('Sioux Falls','SD'), ('Rapid City','SD'),
    ('Nashville','TN'), ('Memphis','TN'), ('Knoxville','TN'), ('Chattanooga','TN'),
    ('Houston','TX'), ('San Antonio','TX'), ('Dallas','TX'), ('Austin','TX'), ('Fort Worth','TX'), ('El Paso','TX'), ('Arlington','TX'), ('Corpus Christi','TX'), ('Plano','TX'), ('Lubbock','TX'), ('Garland','TX'), ('Irving','TX'), ('Amarillo','TX'), ('Grand Prairie','TX'), ('Brownsville','TX'), ('McKinney','TX'), ('Frisco','TX'),
    ('Salt Lake City','UT'), ('West Valley City','UT'), ('Provo','UT'), ('West Jordan','UT'),
    ('Burlington','VT'),
    ('Virginia Beach','VA'), ('Norfolk','VA'), ('Richmond','VA'), ('Arlington','VA'), ('Newport News','VA'), ('Alexandria','VA'),
    ('Seattle','WA'), ('Spokane','WA'), ('Tacoma','WA'), ('Bellevue','WA'), ('Kent','WA'), ('Everett','WA'),
    ('Charleston','WV'), ('Huntington','WV'),
    ('Milwaukee','WI'), ('Madison','WI'), ('Green Bay','WI'),
    ('Cheyenne','WY'), ('Casper','WY'),
    ('Washington','DC'),
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


def render(city, abbr):
    state_name = STATE_NAMES[abbr]
    state_slug = STATE_SLUGS[abbr]
    sos_url = SOS_URLS[abbr]
    slug = f'{slugify(city)}-{abbr.lower()}'
    title = f'Find a property owner in {city}, {state_name} (free address lookup, 2026)'
    description = (
        f'Look up the verified owner of any {city} property by address — '
        f'including the registered LLC officer when the deed is held by an '
        f'entity. Pulls from {state_name} county records + licensed B2B data, '
        f'with DNC and TCPA-litigator flags applied before any outreach.'
    )
    url = f'https://leadcove.io/find-property-owner/{slug}.html'
    og_image = f'https://leadcove.io/assets/og/find-property-owner-{slug}.png'

    article_schema = {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': f'Find a property owner in {city}, {state_name}',
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
                'name': f'How do I find the owner of a property in {city}?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': (
                        f'Two starting points work in {city}. The county property '
                        f'appraiser website serving {city} publishes the recorded '
                        f'owner name and mailing address for every property at no '
                        f'charge; this is the official, public source. For a list '
                        f'of {city} addresses, a single-screen owner-data tool '
                        f'resolves each address directly to the verified owner '
                        f'with phones (DNC flagged), emails, and the registered '
                        f'LLC officer when the property is entity-owned. The tool '
                        f'route is faster for multi-address workflows; the county '
                        f'route is fine for single one-off lookups.'
                    ),
                },
            },
            {
                '@type': 'Question',
                'name': f'How do I find the owner of an LLC-owned property in {city}?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': (
                        f'The deed shows the LLC name. The registered manager or '
                        f'member is the human you contact, and that data lives in '
                        f'the {state_name} Secretary of State business records at '
                        f'{sos_url}. Search by the LLC name on the deed; the listed '
                        f'officer is the contact. Tools that include LLC unmasking '
                        f'do this automatically across all 50 states.'
                    ),
                },
            },
            {
                '@type': 'Question',
                'name': f'Is it legal to look up property owners in {city}?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': (
                        f'Yes. Property ownership records (deed, tax roll) are '
                        f'public information in {state_name}. The {city} county '
                        f'property appraiser publishes them directly. Contacting '
                        f'the owner is governed by the federal TCPA, the national '
                        f'Do Not Call registry, and any {state_name}-specific layers. '
                        f'Use a tool that flags DNC and TCPA-litigator records '
                        f'before outbound contact.'
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
  <p class="post-eyebrow">Location guide · {city}, {abbr}</p>
  <h1>Find a property owner in {city}, {state_name}</h1>
  <p class="post-meta">Updated 2026 · {state_name} state portal + the workflow that works at scale</p>

  <div class="post-body">

    <p>
      Looking up who owns a {city} property takes one of two starting
      points: the county property appraiser site that covers {city},
      or a single-screen owner-data tool that resolves the address
      directly to the verified owner with phones (DNC flagged) and
      emails. For a single one-off lookup, the county records site is
      the no-charge path. For a list of {city} addresses, a tool that
      handles everything in one pass saves hours.
    </p>

    <h2>Try the free address lookup on any {city} property</h2>

    <p>
      We built a <a href="/free-lookup.html">free address lookup tool</a>
      anyone can test before paying. Paste a {city} address; get the
      verified owner name plus phones and emails returned in seconds.
      No account, no card.
    </p>

    <p style="text-align:center; margin: 36px 0;">
      <a href="/free-lookup.html" class="btn-primary btn-lg">Look up any {city} address</a>
    </p>

    <h2>Unmask an LLC that owns a {city} property</h2>

    <p>
      When the deed shows an LLC name instead of a human, the registered
      manager or member is the contact. {state_name}'s LLC records are
      at the
      <a href="{sos_url}" target="_blank" rel="noopener">{state_name} Secretary of State business search</a>.
      Search by the LLC name on the deed; the listed officer is the
      contact human. Tools with built-in LLC unmasking do this
      automatically across all 50 states.
    </p>

    <h2>Common questions</h2>

    <div class="faq-item">
      <p class="faq-q">How do I find the owner of a property in {city}?</p>
      <p class="faq-a">
        The county property appraiser site serving {city} publishes
        the recorded owner name and mailing address for every property
        at no charge. For a list of addresses, an owner-data tool
        resolves each one directly with phones (DNC flagged) and
        emails. The tool route is faster for multi-address workflows.
      </p>
    </div>

    <div class="faq-item">
      <p class="faq-q">How do I unmask an LLC that owns property in {city}?</p>
      <p class="faq-a">
        Search the
        <a href="{sos_url}" target="_blank" rel="noopener">{state_name} Secretary of State business search</a>
        by the LLC name on the deed. The listed officer is the contact
        human. Owner-data tools include LLC unmasking automatically
        across all 50 states.
      </p>
    </div>

    <div class="faq-item">
      <p class="faq-q">Is it legal to look up property owners in {city}?</p>
      <p class="faq-a">
        Yes — deed and tax records are public in {state_name}.
        Contacting the owner is governed by the federal TCPA, the
        national Do Not Call registry, and any {state_name}-specific
        layers. Use a tool that flags DNC and TCPA-litigator records
        before outbound contact.
      </p>
    </div>

    <h2>Related</h2>

    <ul>
      <li><a href="/find-property-owner/{state_slug}.html">Find a property owner in {state_name}</a> — the state-level guide</li>
      <li><a href="/blog/skip-tracing-tools-comparison.html">Skip tracing tools for working agents: a neutral comparison</a></li>
      <li><a href="/blog/find-owner-mls-blank-privacy.html">When the MLS shows blank or "PRIVACY" for the owner</a></li>
      <li><a href="/blog/expired-listings-prospecting-playbook.html">Expired listings playbook: MLS pull to listing appointment</a></li>
    </ul>

  </div>
</article>

<section class="post-cta">
  <h2>One screen. Every {city} owner. Every phone (DNC flagged).</h2>
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
    return HEAD + body, slug


def main():
    state_slugs_set = set(STATE_SLUGS.values())
    written = 0
    skipped = 0
    seen_slugs = set()
    for city, abbr in CITIES:
        html, slug = render(city, abbr)
        # Skip if this slug collides with a state-level slug (would shadow it)
        if slug in state_slugs_set:
            skipped += 1
            continue
        # De-dup across same-name cities in different states (already
        # disambiguated by -<abbr> suffix so should be unique).
        if slug in seen_slugs:
            skipped += 1
            continue
        seen_slugs.add(slug)
        path = OUT_DIR / f'{slug}.html'
        path.write_text(html)
        written += 1
    print(f'✓ Wrote {written} city landing pages → find-property-owner/')
    if skipped:
        print(f'⋯ Skipped {skipped} (collision with state slug or duplicate)')


if __name__ == '__main__':
    main()
