#!/usr/bin/env python3
"""SEO Phase 3 — sitewide normalization for www.peakreachms.com (ADR-017 follow-up).

Run from repo root:  python3 tools/seo_phase3.py [--only FILE.html] [--dry]

What it does (idempotent — safe to re-run):
  1. Internal links  -> root-relative clean URLs (/pricing, /#how) matching canonicals.
  2. Footer          -> one standard footer on every page, with an Industries column
                        (trade pages, hubs, Revenue Recovery, Pricing) for internal linking.
  3. Social tags     -> og:*/twitter:* on every indexable page; og:image -> /assets/og-default.png (1200x630).
  4. Lucide          -> pinned version instead of @latest.
  5. Images          -> width/height (+lazy on founder photo) to avoid CLS.
  6. Schema          -> WebSite + Person (index), Service/Offer (pricing, revenue-recovery),
                        Article (3 resource articles), BreadcrumbList (for-* hubs).
  7. Contact form    -> wired to the same LeadConnector webhook as the audit form (was a demo alert).
  8. sitemap.xml     -> regenerated from the HTML files on disk (404 excluded).
  9. styles.css      -> 4-column footer grid + cache-bust version.

The trade-page generator (tools/gen_trade_pages.py) imports normalize_html() from here so
generated pages come out already normalized.
"""
import re, sys, os, glob, json, datetime, html as H

HOST = "https://www.peakreachms.com"
TODAY = datetime.date.today().isoformat()
def css_ver():
    """Cache-bust token = hash of styles.css content, so any CSS change invalidates caches (Cloudflare + browser)."""
    import hashlib
    try: return hashlib.md5(open("styles.css", "rb").read()).hexdigest()[:8]
    except FileNotFoundError: return TODAY.replace("-", "")
def js_ver():
    import hashlib
    try: return hashlib.md5(open("app.js", "rb").read()).hexdigest()[:8]
    except FileNotFoundError: return TODAY.replace("-", "")
OG_IMG = f"{HOST}/assets/og-default.png"
LUCIDE = "https://unpkg.com/lucide@0.460.0/dist/umd/lucide.min.js"
WEBHOOK = "https://services.leadconnectorhq.com/hooks/PU3svlBW3x81ujPelNlV/webhook-trigger/3e6d4a05-cadc-4bf4-ac07-69c952c619c8"

GA4_ID = "G-Z7E84LTQZ6"   # GA4 stream "www.peakreachms website" (stream 15737071187). NOT GGL G-VREXTTBG84, NOT RGB G-D2XBKMYMGY. None = no tag.
PERSON_SAMEAS = ["https://www.linkedin.com/in/joaquin-santiz-26830683/"]
ORG_SAMEAS = []   # add LinkedIn company page URL once it exists

FOUNDER = {"@type": "Person", "name": "Joaquin Santiz", "jobTitle": "Founder & Operator",
           "worksFor": {"@type": "Organization", "name": "PeakReach Managed Systems", "url": HOST + "/"},
           "image": HOST + "/assets/joaquin.jpg", "url": HOST + "/#philosophy", "sameAs": PERSON_SAMEAS}
PUBLISHER = {"@type": "Organization", "name": "PeakReach Managed Systems", "url": HOST + "/",
             "logo": {"@type": "ImageObject", "url": HOST + "/assets/mark-color.png"}}

STANDARD_FOOTER = '''<footer><div class="wrap">
  <div class="foot-grid">
    <div>
      <div class="foot-logo"><img src="assets/mark-color.png" alt="PeakReach" width="44" height="44"><span class="ftxt"><b>PeakReach</b><span>MANAGED SYSTEMS</span></span></div>
      <p style="max-width:360px">We install and manage the systems that make revenue, accountability, and operations visible, repeatable, and less dependent on the owner.</p>
      <p class="legal-interim">PeakReach Managed Systems is operated by PeakReach Marketing Solutions LLC.</p>
    </div>
    <div>
      <h4>Explore</h4>
      <ul>
        <li><a href="/#what">What We Do</a></li>
        <li><a href="/#how">How It Works</a></li>
        <li><a href="/revenue-recovery">The Revenue Recovery System</a></li>
        <li><a href="/pricing">Pricing</a></li>
        <li><a href="/standard">The Standard</a></li>
        <li><a href="/trust">Trust &amp; Security</a></li>
        <li><a href="/resources">Resources</a></li>
      </ul>
    </div>
    <div>
      <h4>Industries</h4>
      <ul>
        <li><a href="/landscaping-crm">Landscaping CRM</a></li>
        <li><a href="/hvac-crm">HVAC CRM</a></li>
        <li><a href="/plumbing-crm">Plumbing CRM</a></li>
        <li><a href="/electrician-crm">Electrician CRM</a></li>
        <li><a href="/roofing-crm">Roofing CRM</a></li>
        <li><a href="/crm-for-contractors">CRM for Contractors</a></li>
        <li><a href="/for-home-services">Home Services &amp; Contractors</a></li>
        <li><a href="/for-commercial-services">Commercial Services</a></li>
        <li><a href="/for-dealers">Dealers &amp; High-Ticket</a></li>
        <li><a href="/for-print-shops">Print &amp; Sign Shops</a></li>
      </ul>
    </div>
    <div>
      <h4>Get in touch</h4>
      <ul>
        <li><a href="/contact">Contact</a></li>
        <li><a href="mailto:info@peakreachms.com">info@peakreachms.com</a></li>
        <li>Sanford, North Carolina</li>
        <li><a href="/privacy">Privacy</a> · <a href="/terms">Terms</a></li>
      </ul>
      <p class="verse">Romans 5:8</p>
    </div>
  </div>
  <div class="foot-bottom">
    <span>© 2026 PeakReach Managed Systems. All rights reserved.</span>
    <span><a href="/revenue-leak-audit" style="color:inherit">Revenue Leak Audit</a> · <a href="/contact" style="color:inherit">Contact</a> · <a href="/privacy" style="color:inherit">Privacy</a> · <a href="/terms" style="color:inherit">Terms</a></span>
  </div>
</div></footer>'''

STANDARD_NAV = '''<header class="nav"><div class="wrap">
  <a class="logo" href="/"><img src="assets/mark-color.png" alt="PeakReach" width="42" height="42"><span class="txt"><b>PeakReach</b><span>MANAGED SYSTEMS</span></span></a>
  <nav class="links">
    <a href="/for-home-services" data-nav="industries">Industries</a>
    <a href="/revenue-recovery" data-nav="system">The System</a>
    <a href="/pricing" data-nav="pricing">Pricing</a>
    <a href="/resources" data-nav="guides">Guides</a>
    <a href="/contact" data-nav="contact">Contact</a>
    <a class="btn btn-ghost" href="https://app.peakreachms.com" target="_blank" rel="noopener" style="padding:11px 18px">Login</a>
    <a class="btn btn-teal" href="/revenue-leak-audit" style="padding:11px 20px">Find My Revenue Leaks</a>
  </nav>
  <button class="menu-btn" data-menu aria-label="Menu">☰</button>
</div></header>'''
NAV_ACTIVE = {"for-home-services": "industries", "for-commercial-services": "industries", "for-dealers": "industries", "for-print-shops": "industries",
              "landscaping-crm": "industries", "hvac-crm": "industries", "plumbing-crm": "industries", "electrician-crm": "industries", "roofing-crm": "industries",
              "crm-for-contractors": "industries", "crm-for-service-businesses": "guides", "revenue-recovery": "system", "standard": "system", "trust": "system",
              "pricing": "pricing", "resources": "guides", "contact": "contact"}
NO_STICKY = {"revenue-leak-audit", "contact", "404", "privacy", "terms"}
STICKY_CTA = '''<div class="mcta"><a class="btn btn-teal" href="/revenue-leak-audit">Find my revenue leaks →</a></div>'''
FONTS = "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap"
META_FIX = {   # descriptions trimmed to <=155 chars (Google truncates ~155-160)
 "index": "PeakReach installs and runs the systems that make revenue, accountability and operations visible and measurable for service businesses — then stays to run them.",
 "crm-for-contractors": "A contractor CRM only matters if the bids get followed up. PeakReach installs and operates the Revenue Recovery System: every proposal tracked and followed up.",
 "standard": "The PeakReach Standard™ is the methodology behind every managed system we install: Diagnose, Install, Operate, Improve — measured, documented, improved.",
 "for-dealers": "Managed lead-response and opportunity follow-up for dealers and high-ticket sellers: respond fast, assign opportunities, monitor salesperson follow-up.",
 "for-commercial-services": "Managed proposal follow-up for commercial service companies. Proposals, decision-makers and next actions stop disappearing in long sales cycles.",
 "crm-for-service-businesses": "A CRM for service businesses only pays off if it runs: a visible pipeline, follow-up that fires on schedule, clear ownership — and someone operating it.",
}

CONTACT_FORM = '''<form id="contact-form" novalidate data-lead="contact" data-source="Website - Contact Page" data-event="contact_form_success" data-success="Thanks — your message is in. We reply within one business day.">
      <div class="field"><label>Name *</label><input type="text" name="full_name" placeholder="Your name" required></div>
      <div class="field"><label>Company</label><input type="text" name="company" placeholder="Your company"></div>
      <div class="field"><label>Work email *</label><input type="email" name="email" placeholder="you@company.com" required></div>
      <div class="field"><label>Mobile phone</label><input type="tel" name="phone" placeholder="(919) 555-0123"></div>
      <div class="field"><label>How can we help?</label><textarea name="message" rows="3" placeholder="..."></textarea></div>
      <button type="submit" class="btn btn-teal" style="width:100%;justify-content:center;margin-top:18px">Send message</button>
      <p class="fine" data-status role="status" aria-live="polite" style="display:none;margin-top:12px"></p>
      <p class="fine" style="text-align:center;margin-top:12px">Prefer a review of your follow-up? <a href="/revenue-leak-audit" style="color:var(--blue);font-weight:600">Apply for a Revenue Leak Audit →</a></p>
    </form>'''

PRIORITY = {"index": "1.0", "revenue-recovery": "0.9", "pricing": "0.9", "revenue-leak-audit": "0.8",
            "for-home-services": "0.8", "for-commercial-services": "0.7", "for-dealers": "0.7", "for-print-shops": "0.7",
            "landscaping-crm": "0.8", "hvac-crm": "0.8", "plumbing-crm": "0.8", "electrician-crm": "0.8", "roofing-crm": "0.8",
            "crm-for-contractors": "0.8", "crm-for-service-businesses": "0.7", "privacy": "0.2", "terms": "0.2",
            "best-landscaping-crm-software": "0.7", "best-hvac-crm-software": "0.7", "best-plumbing-crm-software": "0.7", "best-electrician-crm-software": "0.7",
            "best-roofing-crm-software": "0.7", "hvac-estimating-software": "0.7", "landscaping-estimating-software": "0.7", "landscaping-business-software": "0.7"}
ARTICLES = {"estimate-follow-up-system": "2026-08-14", "estimating-software-vs-follow-up": "2026-08-14",
            "revenue-after-the-quote": "2026-08-14", "crm-for-service-businesses": "2026-09-02", "crm-for-contractors": "2026-09-02",
            # P1 content set (tools/gen_articles.py) — datePublished is fixed here, never TODAY
            "best-landscaping-crm-software": "2026-09-08", "best-hvac-crm-software": "2026-09-08", "best-plumbing-crm-software": "2026-09-08",
            "best-electrician-crm-software": "2026-09-08", "best-roofing-crm-software": "2026-09-08",
            "hvac-estimating-software": "2026-09-08", "landscaping-estimating-software": "2026-09-08", "landscaping-business-software": "2026-09-08"}
HUBS = {"for-home-services": "Home Services & Contractors", "for-commercial-services": "Commercial Services",
        "for-dealers": "Dealers & High-Ticket Sellers", "for-print-shops": "Print, Sign & Promotional Shops"}


def _first(pat, t, flags=re.S | re.I):
    m = re.search(pat, t, flags); return H.unescape(m.group(1).strip()) if m else ""


def _ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=1) + '\n</script>'


def _href(m):
    name, anchor = m.group(1), m.group(2) or ""
    return 'href="/' + ("" if name == "index" else name) + anchor + '"'


def normalize_html(name, t):
    """name = slug without .html; t = full HTML. Returns normalized HTML."""
    # 1. clean internal links
    t = re.sub(r'href="([a-z0-9-]+)\.html(#[^"]*)?"', _href, t)
    if name == "index":
        t = t.replace('<a class="logo" href="#top">', '<a class="logo" href="/">')
    # 2. standard footer + standard nav (+ active state) + mobile sticky CTA
    t = re.sub(r"<footer>.*?</footer>", lambda m: STANDARD_FOOTER, t, count=1, flags=re.S)
    nav = STANDARD_NAV
    act = NAV_ACTIVE.get(name) or ("guides" if name in ARTICLES else None)
    if act:
        nav = nav.replace(f'data-nav="{act}"', f'class="active" data-nav="{act}"')
    t = re.sub(r'<header class="nav">.*?</header>', lambda m: nav, t, count=1, flags=re.S)
    t = re.sub(r'\n?<div class="mcta">.*?</div>', '', t, flags=re.S)
    if name not in NO_STICKY:
        t = t.replace("<footer>", STICKY_CTA + "\n<footer>", 1)
    # 2b. fonts: only the weights the CSS uses
    t = re.sub(r'<link href="https://fonts\.googleapis\.com/css2\?[^"]*" rel="stylesheet">', f'<link href="{FONTS}" rel="stylesheet">', t)
    # 2c. lead forms: one handler (app.js prLead) — strip legacy inline scripts, tag forms, make SMS consent optional
    t = re.sub(r'\n?\s*<script>\s*\(function \(\) \{\s*var WEBHOOK_URL.*?\}\)\(\);\s*</script>', '', t, flags=re.S)
    t = re.sub(r'\n?\s*<script>\s*\(function \(\) \{\s*var form = document\.getElementById\("contact-form"\).*?</script>', '', t, flags=re.S)
    t = t.replace('<form class="form-card" id="audit" novalidate>',
                  '<form class="form-card" id="audit" novalidate data-lead="audit" data-source="Website - Revenue Leak Audit" data-event="rla_form_success" data-success="Thanks — your Revenue Leak Audit request is in. We reach out within one business day to schedule it.">')
    t = t.replace('<p class="fine" id="rla-status" role="status"', '<p class="fine" data-status role="status"')
    t = t.replace('<form id="contact-form" novalidate>', CONTACT_FORM.split("\n")[0])   # upgrade Phase-3 contact form tag to data-lead attrs
    t = t.replace('<p class="fine" id="contact-status" role="status"', '<p class="fine" data-status role="status"')
    t = t.replace('<input type="checkbox" name="consent_sms" value="true" required>', '<input type="checkbox" name="consent_sms" value="true">')
    # 2d. meta description fixes (hand-maintained pages)
    if name in META_FIX:
        t = re.sub(r'(<meta\s+name="description"\s+content=")[^"]*(")', lambda m: m.group(1) + H.escape(META_FIX[name], True) + m.group(2), t, count=1)
        t = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m: m.group(1) + H.escape(META_FIX[name], True) + m.group(2), t, count=1)
        t = re.sub(r'(<meta name="twitter:description" content=")[^"]*(")', lambda m: m.group(1) + H.escape(META_FIX[name], True) + m.group(2), t, count=1)
    # 4. lucide pinned
    t = re.sub(r'https://unpkg\.com/lucide@[^"]+', LUCIDE, t)
    # 5. image dimensions
    t = t.replace('<img src="assets/mark-color.png" alt="PeakReach">', '<img src="assets/mark-color.png" alt="PeakReach" width="42" height="42">')
    t = re.sub(r'<img src="assets/joaquin\.jpg" alt="([^"]*)"(?![^>]*width)', r'<img src="assets/joaquin.jpg" alt="\1" width="560" height="746" loading="lazy"', t)
    # 9. css cache bust
    t = re.sub(r'href="styles\.css(\?v=[0-9a-f]+)?"', f'href="styles.css?v={css_ver()}"', t)
    t = re.sub(r'src="app\.js(\?v=[0-9a-f]+)?"', f'src="app.js?v={js_ver()}"', t)
    # 10. GA4 (gtag) — one block per page, right after <head> opening tags; replaced on every run so the ID is single-sourced here
    t = re.sub(r'\n<!-- ga4:start -->.*?<!-- ga4:end -->', '', t, flags=re.S)
    if GA4_ID:
        ga = (f'\n<!-- ga4:start -->\n<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>\n'
              f'<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","{GA4_ID}");</script>\n<!-- ga4:end -->')
        t = t.replace('<meta name="viewport" content="width=device-width, initial-scale=1">',
                      '<meta name="viewport" content="width=device-width, initial-scale=1">' + ga, 1)
    if name == "404":
        return t
    # 3. social tags
    title = _first(r"<title>(.*?)</title>", t)
    desc = _first(r'<meta\s+name="description"\s+content="(.*?)"', t)
    url = HOST + ("/" if name == "index" else "/" + name)
    if 'property="og:title"' not in t:
        block = ('\n<meta property="og:type" content="website">\n<meta property="og:site_name" content="PeakReach Managed Systems">'
                 f'\n<meta property="og:title" content="{H.escape(title, True)}">\n<meta property="og:description" content="{H.escape(desc, True)}">'
                 f'\n<meta property="og:url" content="{url}">\n<meta property="og:image" content="{OG_IMG}">'
                 f'\n<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:title" content="{H.escape(title, True)}">'
                 f'\n<meta name="twitter:description" content="{H.escape(desc, True)}">\n<meta name="twitter:image" content="{OG_IMG}">')
        t = re.sub(r'(<meta\s+name="description"\s+content="[^"]*">)', lambda m: m.group(1) + block, t, count=1)
    if 'name="twitter:card"' not in t:   # pages that had og:* but no twitter:* (4 articles)
        tw = (f'\n<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:title" content="{H.escape(title, True)}">'
              f'\n<meta name="twitter:description" content="{H.escape(desc, True)}">\n<meta name="twitter:image" content="{OG_IMG}">')
        t = re.sub(r'(<meta property="og:image" content="[^"]*">)', lambda m: m.group(1) + tw, t, count=1)
    t = re.sub(r'(<meta (?:property="og:image"|name="twitter:image") content=")https://www\.peakreachms\.com/assets/mark-color\.png(")', r'\g<1>' + OG_IMG + r'\2', t)
    if 'og:image:width' not in t:
        t = t.replace(f'<meta property="og:image" content="{OG_IMG}">',
                      f'<meta property="og:image" content="{OG_IMG}">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">', 1)
    # 6. schema
    extra = []
    if name == "index" and '"@type": "WebSite"' not in t and '"@type":"WebSite"' not in t:
        extra.append({"@context": "https://schema.org", "@type": "WebSite", "name": "PeakReach Managed Systems", "url": HOST + "/", "publisher": PUBLISHER})
        extra.append(dict({"@context": "https://schema.org"}, **FOUNDER, description="Founder and operator of PeakReach Managed Systems and CEO of Green Garden Landscaping (Sanford, NC). Built the Revenue Recovery System inside a real landscaping company before standardizing it for other trades."))
    if name in ("pricing", "revenue-recovery") and '"@type": "Service"' not in t:
        extra.append({"@context": "https://schema.org", "@type": "Service", "name": "PeakReach Revenue Recovery System",
                      "serviceType": "Managed estimate follow-up and revenue recovery system", "provider": PUBLISHER,
                      "areaServed": "United States", "url": HOST + "/revenue-recovery",
                      "audience": {"@type": "BusinessAudience", "name": "Service businesses that sell through estimates, quotes, or proposals"},
                      "offers": [
                          {"@type": "Offer", "name": "Implementation", "price": "2500", "priceCurrency": "USD", "url": HOST + "/pricing"},
                          {"@type": "Offer", "name": "Managed service", "priceCurrency": "USD", "url": HOST + "/pricing",
                           "priceSpecification": {"@type": "UnitPriceSpecification", "price": "1497", "priceCurrency": "USD", "billingDuration": "P1M", "unitText": "month"}}]})
    if name in ARTICLES and '"@type": "Article"' not in t:
        h1 = re.sub(r"<.*?>", "", _first(r"<h1[^>]*>(.*?)</h1>", t))
        extra.append({"@context": "https://schema.org", "@type": "Article", "headline": h1 or title, "description": desc,
                      "mainEntityOfPage": url, "image": OG_IMG, "datePublished": ARTICLES[name], "dateModified": TODAY,
                      "author": FOUNDER, "publisher": PUBLISHER})
    if name in HUBS and '"@type": "BreadcrumbList"' not in t:
        extra.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": HOST + "/"},
            {"@type": "ListItem", "position": 2, "name": HUBS[name], "item": url}]})
    if extra:
        t = t.replace("</head>", "\n".join(_ld(x) for x in extra) + "\n</head>", 1)
    # Organization sameAs (site-wide Organization block, both pretty and compact JSON forms)
    t = re.sub(r'("url": "https://www\.peakreachms\.com/#philosophy"),\s*"sameAs":\s*\[[^\]]*\]', r'\1', t)
    if PERSON_SAMEAS:   # Person block (index + article authors) — single-sourced from PERSON_SAMEAS
        t = re.sub(r'("url": "https://www\.peakreachms\.com/#philosophy")', lambda m: m.group(1) + ', "sameAs": ' + json.dumps(PERSON_SAMEAS), t)
    t = re.sub(r'("areaServed":\s*"United States"),\s*"sameAs":\s*\[[^\]]*\]', r'\1', t)
    if ORG_SAMEAS:
        t = re.sub(r'("areaServed":\s*"United States")', lambda m: m.group(1) + ', "sameAs": ' + json.dumps(ORG_SAMEAS), t)
    # 7. contact form
    if name == "contact":
        t = re.sub(r"<form data-demo>.*?</form>", lambda m: CONTACT_FORM, t, count=1, flags=re.S)
    return t


def write_sitemap(dry=False):
    rows = []
    for f in sorted(glob.glob("*.html")):
        slug = f[:-5]
        if slug == "404":
            continue
        loc = HOST + ("/" if slug == "index" else "/" + slug)
        rows.append(f"  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><priority>{PRIORITY.get(slug, '0.6')}</priority></url>")
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(rows) + "\n</urlset>\n"
    if not dry:
        open("sitemap.xml", "w", encoding="utf-8").write(xml)
    return len(rows)


def patch_css(dry=False):
    css = open("styles.css", encoding="utf-8").read()
    new = css.replace(".foot-grid{display:grid;grid-template-columns:1.7fr 1fr 1fr;gap:42px}",
                      ".foot-grid{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr;gap:36px}\n@media(max-width:960px){.foot-grid{grid-template-columns:1fr 1fr}}")
    ARTICLE_CSS = ("\n/* articles (tools/gen_articles.py) */\n"
                   ".prose h2.intro-title{font-family:var(--display);font-size:28px;line-height:1.2;color:var(--navy-2);margin:0 0 22px;padding-bottom:16px;border-bottom:1px solid var(--line)}\n"
                   ".tablewrap{overflow-x:auto;margin:6px 0 10px}\n"
                   "table.cmp{width:100%;border-collapse:collapse;font-size:14px;line-height:1.45}\n"
                   "table.cmp th{text-align:left;font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--blue);padding:10px 12px;border-bottom:2px solid var(--line-2);background:var(--sky-2)}\n"
                   "table.cmp td{padding:12px;border-bottom:1px solid var(--line);vertical-align:top;color:var(--body)}\n"
                   "table.cmp td:first-child{color:var(--ink);white-space:nowrap}\n"
                   "@media(max-width:720px){table.cmp{min-width:640px}}\n")
    if "table.cmp" not in new:
        new = new.rstrip("\n") + "\n" + ARTICLE_CSS
    P5_CSS = ("\n/* phase 5: conversion UX (tools/seo_phase3.py) */\n"
              ".usp-list.on-dark b{color:#fff}\n"                                                     # bugfix: navy bold on navy bg
              ".reveal{transition:opacity .3s ease,transform .3s ease;transform:translateY(10px)}\n"
              "@media(prefers-reduced-motion:reduce){.reveal{opacity:1;transform:none;transition:none}}\n"
              ".mcta{display:none}\n"
              "@media(max-width:720px){.mcta{display:block;position:fixed;left:0;right:0;bottom:0;z-index:70;padding:10px 14px calc(10px + env(safe-area-inset-bottom));background:rgba(255,255,255,.96);border-top:1px solid var(--line);box-shadow:0 -8px 24px -16px rgba(10,36,64,.35);transform:translateY(120%);transition:transform .25s ease}.mcta.show{transform:none}"
              ".mcta .btn{width:100%;justify-content:center}body{padding-bottom:72px}}\n"
              ".chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:22px}\n"
              ".chips span{font-family:var(--mono);font-size:11.5px;color:#9fb3c8;align-self:center;margin-right:2px}\n"
              ".chips a{font-size:13px;font-weight:600;color:#dbe8f4;padding:7px 12px;border:1px solid rgba(255,255,255,.18);border-radius:100px;background:rgba(255,255,255,.05)}\n"
              ".chips a:hover{border-color:var(--teal);color:#fff}\n"
              ".callout{margin:28px 0;padding:22px 24px;border:1px solid var(--line-2);border-left:4px solid var(--teal);border-radius:14px;background:var(--sky-2)}\n"
              ".callout h3{font-size:18px;color:var(--ink);margin:0 0 6px}.callout p{margin:0 0 12px;font-size:15px}\n"
              ".lead-grid{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start}\n"
              "@media(max-width:900px){.lead-grid{grid-template-columns:1fr}}\n"
              ".lead-grid .form-card{margin:0}\n"
              ".steps{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:28px}\n"
              "@media(max-width:720px){.steps{grid-template-columns:1fr}}\n"
              ".steps div{background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px 20px}\n"
              ".steps .n{font-family:var(--mono);font-size:12px;color:var(--blue);letter-spacing:.08em}.steps h4{margin:6px 0 4px;font-size:16px;color:var(--ink)}.steps p{margin:0;font-size:14px;color:var(--body)}\n")
    new = re.sub(r"\n/\* phase 5: conversion UX \(tools/seo_phase3\.py\) \*/\n.*", "", new, flags=re.S)   # replace the whole block each run
    new = new.rstrip("\n") + "\n" + P5_CSS
    if new != css and not dry:
        open("styles.css", "w", encoding="utf-8").write(new)
    return new != css


if __name__ == "__main__":
    args = sys.argv[1:]
    dry = "--dry" in args
    only = args[args.index("--only") + 1] if "--only" in args else None
    files = [only] if only else sorted(glob.glob("*.html"))
    css_changed = patch_css(dry) if not only else False
    changed = 0
    for f in files:
        src = open(f, encoding="utf-8").read()
        out = normalize_html(f[:-5], src)
        if out != src:
            changed += 1
            if not dry:
                open(f, "w", encoding="utf-8").write(out)
        print(("would change" if dry else "normalized") if out != src else "unchanged", f)
    if not only:
        n = write_sitemap(dry); print(f"sitemap.xml: {n} URLs")
        print("styles.css:", "patched" if css_changed else "unchanged", f"(v={css_ver()})")
    print(f"{changed}/{len(files)} pages changed" + (" (dry run)" if dry else ""))
