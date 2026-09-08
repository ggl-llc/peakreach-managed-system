# PeakReach — Managed System (marketing site)

Public marketing and sales site for **PeakReach**: managed operational
Systems (Estimate Recovery Engine, Lead Attribution, and more) for
service businesses. This is the go-to-market front end — the engineering
lives in the private `peakreach` monorepo.

## Stack
Static site — plain HTML, CSS, and vanilla JS. No build step.

## Structure
- `index.html` — home / main landing page
- `crm-for-service-businesses.html` — CRM positioning page
- `estimate-follow-up-system.html` — ERE product page
- `estimating-software-vs-follow-up.html` — comparison page
- `revenue-after-the-quote.html` — value / offer page
- `resources.html` — resources
- `standard.html` — standard/base page
- `contact.html` — contact
- `trust.html` — trust / credibility
- `privacy.html` · `terms.html` — legal
- `landscaping-crm.html` · `hvac-crm.html` · `plumbing-crm.html` · `electrician-crm.html` · `roofing-crm.html` — trade pages (GENERATED — edit `tools/gen_trade_pages.py`, then run it)
- `crm-for-contractors.html` · `for-home-services.html` · `for-commercial-services.html` · `for-dealers.html` · `for-print-shops.html` · `revenue-recovery.html` · `pricing.html` · `revenue-leak-audit.html`
- `styles.css` — global styles
- `app.js` — page interactions
- `assets/` — images and static assets (`og-default.png` = 1200×630 social card)
- `tools/seo_phase3.py` — sitewide SEO normalizer (clean internal links, standard footer, social tags, schema, sitemap). Idempotent; run after adding or editing any page: `python3 tools/seo_phase3.py`
- `tools/gen_trade_pages.py` — trade-page generator (ADR-017); output is piped through the normalizer

## Conventions
- Internal links are root-relative clean URLs (`/pricing`, `/#how`) — never `page.html`. Cloudflare Pages serves clean URLs and 308-redirects `/x.html` → `/x`.
- Canonical host: `https://www.peakreachms.com` (apex 301s to www via `_redirects`).
- Every indexable page: `<title>`, meta description, canonical, og:*/twitter:*, Organization JSON-LD. Trade pages add FAQPage + BreadcrumbList; pricing/revenue-recovery add Service/Offer; articles add Article.
- `sitemap.xml` is generated — do not hand-edit.

## Deploy
Static hosting (serves `index.html` as the entry point).

## Related
- Engineering monorepo (private): `ggl-llc/peakreach`
- Repo index & org rules: CEO Command Center → "GitHub — Repository Index & Organization" (Notion)
