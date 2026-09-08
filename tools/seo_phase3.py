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
CSS_VER = TODAY.replace("-", "")
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

CONTACT_FORM = '''<form id="contact-form" novalidate>
      <div class="field"><label>Name *</label><input type="text" name="full_name" placeholder="Your name" required></div>
      <div class="field"><label>Company</label><input type="text" name="company" placeholder="Your company"></div>
      <div class="field"><label>Work email *</label><input type="email" name="email" placeholder="you@company.com" required></div>
      <div class="field"><label>Mobile phone</label><input type="tel" name="phone" placeholder="(919) 555-0123"></div>
      <div class="field"><label>How can we help?</label><textarea name="message" rows="3" placeholder="..."></textarea></div>
      <button type="submit" class="btn btn-teal" style="width:100%;justify-content:center;margin-top:18px">Send message</button>
      <p class="fine" id="contact-status" role="status" aria-live="polite" style="display:none;margin-top:12px"></p>
      <p class="fine" style="text-align:center;margin-top:12px">Prefer a review of your follow-up? <a href="/revenue-leak-audit" style="color:var(--blue);font-weight:600">Apply for a Revenue Leak Audit →</a></p>
    </form>
    <script>
    (function () {
      var form = document.getElementById("contact-form"); if (!form) return;
      var statusEl = document.getElementById("contact-status"), btn = form.querySelector("button[type=submit]");
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var full = (form.full_name.value || "").trim().replace(/\\s+/g, " "), sp = full.indexOf(" ");
        var email = (form.email.value || "").trim();
        if (!full || !email) { statusEl.style.display = "block"; statusEl.textContent = "Please add your name and work email."; return; }
        var payload = { first_name: sp === -1 ? full : full.slice(0, sp), last_name: sp === -1 ? "" : full.slice(sp + 1),
          email: email, phone: (form.phone.value || "").trim(), company: (form.company.value || "").trim(),
          message: (form.message.value || "").trim(), source: "Website - Contact Page", page: location.pathname };
        btn.disabled = true; statusEl.style.display = "block"; statusEl.textContent = "Sending…";
        fetch("''' + WEBHOOK + '''", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) })
          .then(function (res) { if (!res.ok) throw new Error(res.status); form.reset();
            statusEl.textContent = "Thanks — your message is in. We reply within one business day."; btn.disabled = false; })
          .catch(function () { statusEl.textContent = "Something went wrong. Please email info@peakreachms.com."; btn.disabled = false; });
      });
    })();
    </script>'''

PRIORITY = {"index": "1.0", "revenue-recovery": "0.9", "pricing": "0.9", "revenue-leak-audit": "0.8",
            "for-home-services": "0.8", "for-commercial-services": "0.7", "for-dealers": "0.7", "for-print-shops": "0.7",
            "landscaping-crm": "0.8", "hvac-crm": "0.8", "plumbing-crm": "0.8", "electrician-crm": "0.8", "roofing-crm": "0.8",
            "crm-for-contractors": "0.8", "crm-for-service-businesses": "0.7", "privacy": "0.2", "terms": "0.2"}
ARTICLES = {"estimate-follow-up-system": "2026-08-14", "estimating-software-vs-follow-up": "2026-08-14",
            "revenue-after-the-quote": "2026-08-14", "crm-for-service-businesses": "2026-09-02", "crm-for-contractors": "2026-09-02"}
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
    # 2. standard footer
    t = re.sub(r"<footer>.*?</footer>", lambda m: STANDARD_FOOTER, t, count=1, flags=re.S)
    # 4. lucide pinned
    t = re.sub(r'https://unpkg\.com/lucide@[^"]+', LUCIDE, t)
    # 5. image dimensions
    t = t.replace('<img src="assets/mark-color.png" alt="PeakReach">', '<img src="assets/mark-color.png" alt="PeakReach" width="42" height="42">')
    t = re.sub(r'<img src="assets/joaquin\.jpg" alt="([^"]*)"(?![^>]*width)', r'<img src="assets/joaquin.jpg" alt="\1" width="560" height="746" loading="lazy"', t)
    # 9. css cache bust
    t = re.sub(r'styles\.css\?v=\d+', f'styles.css?v={CSS_VER}', t)
    # 10. GA4 (gtag) — one block per page, right after <head> opening tags; replaced on every run so the ID is single-sourced here
    t = re.sub(r'\n<!-- ga4:start -->.*?<!-- ga4:end -->', '', t, flags=re.S)
    if GA4_ID:
        ga = (f'\n<!-- ga4:start -->\n<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>\n'
              f'<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","{GA4_ID}");</script>\n<!-- ga4:end -->')
        t = t.replace('<meta name="viewport" content="width=device-width, initial-scale=1">',
                      '<meta name="viewport" content="width=device-width, initial-scale=1">' + ga, 1)
    # form success events (GA4 key events). Idempotent: only inserted where the success string exists without the event.
    t = t.replace('form.reset();\n            statusEl.textContent = "Thanks — your Revenue Leak Audit request is in.',
                  'form.reset(); if (window.gtag) gtag("event", "rla_form_success", { form: "revenue_leak_audit", page: location.pathname });\n            statusEl.textContent = "Thanks — your Revenue Leak Audit request is in.')
    t = t.replace('form.reset();\n            statusEl.textContent = "Thanks — your message is in.',
                  'form.reset(); if (window.gtag) gtag("event", "contact_form_success", { form: "contact", page: location.pathname });\n            statusEl.textContent = "Thanks — your message is in.')
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
    if new != css and not dry:
        open("styles.css", "w", encoding="utf-8").write(new)
    return new != css


if __name__ == "__main__":
    args = sys.argv[1:]
    dry = "--dry" in args
    only = args[args.index("--only") + 1] if "--only" in args else None
    files = [only] if only else sorted(glob.glob("*.html"))
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
        print("styles.css:", "patched" if patch_css(dry) else "unchanged")
    print(f"{changed}/{len(files)} pages changed" + (" (dry run)" if dry else ""))
