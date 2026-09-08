# PeakReach Website — SEO Audit & Phase 3 Build Log
**Site:** https://www.peakreachms.com · **Repo:** `ggl-llc/peakreach-managed-system` (static HTML, Cloudflare Pages)
**Date:** 2026-09-08 · **Project:** PeakReach · **Status:** Phase 3 built locally, uncommitted, NOT deployed — awaiting approval.

> Freeze note: PeakReach product launch is frozen until 2026-09-15 (Índice Operativo §4); the marketing site was already ruled outside the freeze (2026-09-02) and Joaquin re-confirmed audit + in-repo fixes today. No push/deploy until his go.

---

## 1. Baseline (evidence, not documentation)

| Signal | Value | Source |
|---|---|---|
| Semrush Rank (US) | 10,171,020 | domain_rank |
| Organic keywords / traffic | 6 kw / ~4 visits/mo | resource_organic |
| Keywords ranking | only brand noise ("peak reach bv" — a Dutch company), `peak org login` via `sites.peakreachms.com` | resource_organic |
| Backlinks | 650 links / 164 domains, Authority Score 6 | backlinks_overview |
| Real referring domains | ~2: greengardenlandscape.com (300 sitewide), pglandscapingnc.com (60). Rest = directory/scraper spam | backlinks_refdomains |
| Analytics | **No GA4/GTM tag on any page.** Search Console exists (verified 2026-09-02, sitemap submitted) but is not readable from this session | grep of all 25 HTML files; Notion/memory |
| Pages | 24 indexable + 404 | repo |
| Content age | first content 2026-08-14; SEO Phase 0–2 shipped 2026-09-03 | git log |

Translation: the site is 3 weeks old with zero measurement and zero authority. Ranking work is possible (keyword difficulty is low, see §4) but nothing can be proven without GA4 + Search Console.

## 2. Issues found (repo + live)

| # | Issue | Impact | Status |
|---|---|---|---|
| 1 | **No GA4 / GTM** anywhere (GSC exists, unread) | Cannot measure clicks or leads; GSC data unseen | ⛔ needs GA4/GTM ID + GSC export or access |
| 2 | **Contact form was a demo** (`alert('not connected')`) — every contact-page lead was dropped | Lead loss | ✅ fixed (wired to LeadConnector webhook) |
| 3 | 581 internal links pointed to `page.html` while canonicals/sitemap use clean URLs → redirect hop on every click, split signals | Crawl/PageRank waste | ✅ fixed (root-relative clean URLs) |
| 4 | Home page linked to **zero** trade pages; 5 trade CRM pages + 4 `for-*` hubs reachable only via one hub link | Orphan-ish money pages | ✅ fixed (Industries footer column sitewide) |
| 5 | Sitemap missing 4 pages added Sep 4 (`revenue-recovery`, `for-commercial-services`, `for-dealers`, `for-print-shops`) | Not discovered | ✅ fixed (24 URLs, generated) |
| 6 | Trade page titles/descriptions had template grammar bugs: "landscaping CRM — …", "A HVAC CRM", "for hvac companies" | CTR / trust | ✅ fixed in generator |
| 7 | 6 pages without og:*/twitter:*; 4 with og but no twitter; og:image was a 320×320 logo | Poor social previews | ✅ fixed (all pages, new 1200×630 card) |
| 8 | Footers inconsistent across pages (3 variants, some pointing to anchors that differ) | Inconsistent internal linking | ✅ fixed (one standard footer) |
| 9 | `lucide@latest` from unpkg, unpinned | Fragile dependency | ✅ pinned 0.460.0 |
| 10 | No structured data beyond Organization + FAQ | Missed rich results / entity signals | ✅ added WebSite, Person (founder), Service+Offer, Article ×5, BreadcrumbList ×9 |
| 11 | Images without width/height (CLS) | Core Web Vitals | ✅ fixed (logo, founder photo lazy) |
| 12 | 3 Google Font families / 12 weights loaded on every page | LCP | ⏳ P1 |
| 13 | Meta descriptions >160 ch on index, crm-for-contractors, standard, for-dealers/commercial | Truncated snippets | ⏳ P2 copy pass |
| 14 | `sites.peakreachms.com` (GHL funnels) is indexed for junk queries | Brand dilution | ⏳ P2 — set noindex in GHL or drop subdomain from search |
| 15 | Only 5 informational articles; SERPs for target terms are listicles/Reddit | Intent mismatch — product pages alone won't rank | ⏳ P1 content plan (§4) |

## 3. Phase 3 — what was built (repo, uncommitted)

**New:** `tools/seo_phase3.py` (idempotent sitewide normalizer), `assets/og-default.png` (1200×630), README conventions.
**Changed:** 24 HTML pages, `sitemap.xml`, `styles.css` (4-col footer + cache-bust `?v=20260908`), `tools/gen_trade_pages.py` (grammar, cross-links, BreadcrumbList, pipes through normalizer).
**Verification done:** dry-run on one page first → full run → second run reports 0 changes (idempotent) → all JSON-LD parses → no `.html` hrefs remain → all 24 indexable pages have og/twitter → headless render of index/contact/landscaping-crm footers desktop+mobile OK → live check confirms Cloudflare serves clean URLs (`/landscaping-crm` 200).
**Not verified (needs deploy):** contact form end-to-end (submit → contact appears in GHL location `PU3svlBW3x81ujPelNlV` with source "Website - Contact Page"). Do one real test submit after deploy and read the contact back.

**Housekeeping needed (delete permission was not granted to the session):** remove `tools/__pycache__/` and `tools/_patch_generator_phase3.py` before committing.

### Deploy checklist (after approval)
1. `git add -A && git commit -m "SEO Phase 3: clean internal links, standard footer w/ Industries, social tags + OG card, schema (WebSite/Person/Service/Article/Breadcrumb), contact form wired, sitemap 24 URLs"` → push `main` → Cloudflare Pages auto-deploys.
2. Live read-back: `curl -sI https://www.peakreachms.com/pricing.html` → expect 308 → `/pricing`; view-source of `/hvac-crm` → new title; `/sitemap.xml` → 24 URLs.
3. Test contact form once; confirm contact in GHL.
4. Google Search Console: resubmit sitemap, request indexing for the 5 trade pages + `/revenue-recovery` + the 3 `for-*` pages missing before.
5. Rich Results Test on `/pricing` (Service/Offer), `/landscaping-crm` (FAQ + Breadcrumb), `/estimate-follow-up-system` (Article).

## 4. Keyword reality (Semrush US, Sept 2026)

Low difficulty, real volume, commercial intent — this is winnable within 3–6 months with content + a handful of real links.

| Keyword | Vol | KD | Page today | Gap |
|---|---|---|---|---|
| roofing crm | 1,000 | 28 | /roofing-crm | SERP = listicles → needs comparison article |
| hvac estimating software | 1,000 | 16 | — | new article: "HVAC estimating software vs. follow-up" |
| crm for contractors | 880 | 25 | /crm-for-contractors | ok, needs links |
| landscaping business software | 880 | 21 | — | new guide |
| hvac crm | 720 | 16 | /hvac-crm | comparison article |
| field service crm | 720 | 39 | — | later |
| crm for plumbers | 590 | 15 | /plumbing-crm | add "for plumbers" H2 + FAQ |
| landscaping crm software | 480 | 9 | /landscaping-crm | add "software" variant to title/H2 |
| roofing crm software | 480 | 38 | /roofing-crm | — |
| crm for landscapers / landscape crm | 390+390 | 8–9 | /landscaping-crm | H2 variants |
| landscaping estimating software | 390 | 7 | — | new article |
| missed call text back | 390 | 18 | — | new feature page (it's in the product) |
| crm for home services | 390 | 15 | /for-home-services | retitle hub |
| crm for electricians | 320 | 5 | /electrician-crm | H2 variant |
| lead follow up system | 210 | 24 | /estimate-follow-up-system | retitle |
| hvac business consultant | 140 | 5 | — | founder/consulting angle |
| automated follow up system | 140 | 21 | /estimate-follow-up-system | — |

Dead ends: "estimate follow up" (0 vol), "revenue recovery" (1,000 vol but healthcare intent — do not chase).

**Who ranks for "landscaping crm":** Reddit ×2, HoneyBook, Grow Group blog, Jobber Academy, Pipeline CRM, Aspire, Smith.ai — all "best CRM for X" listicles. **Who ranks for "hvac crm":** Reddit, FieldPulse, ServiceTrade, WebFX, Workiz, Housecall Pro, ServiceTitan. Product pages alone will not enter these SERPs; a companion "Best X CRM (2026): compared honestly, and why most fail after the quote" per trade will.

## 5. Roadmap

**P0 — this week (blocked on Joaquin)**
- Provide GA4 measurement ID (or GTM container) for PeakReach → I add the tag to the normalizer so every page gets it; wire `contact_form_success` / `rla_form_success` dataLayer events (same pattern as GGL's `quote_form_success`).
- Search Console: resubmit the regenerated sitemap after deploy; export Performance (last 28d) so the next pass starts from real queries, not Semrush estimates.
- Approve deploy of Phase 3.
- LinkedIn URL (personal + company) → `sameAs` on Organization/Person schema; create Google Business Profile for PeakReach Managed Systems (Sanford, NC) — free entity signal + local pack for "business consultant sanford nc".

**P1 — next 30 days (content + links)**
- 5 comparison articles ("best {trade} CRM software 2026") linking to each trade page; 3 software-gap articles (HVAC estimating software, landscaping estimating software, landscaping business software); 1 feature page (missed-call text back).
- Add keyword variants as H2s on trade pages (generator field `alt_kws`): "landscaping CRM software", "CRM for landscapers", "CRM for plumbers", "CRM for electricians".
- Links: fix the 300 sitewide GGL footer links → one contextual "Powered by PeakReach" link (sitewide footer links are discounted); ask pglandscapingnc.com for a case-study link; list on GoHighLevel partner directory, Clutch, Crunchbase; 2 guest posts (Lawn & Landscape, Total Landscape Care, ACHR News); 1 podcast/mo.
- Fonts: drop IBM Plex Mono weights not used, self-host or limit to 2 families/6 weights.

**P2 — 60–90 days**
- Case study page per live client (GGL first: estimates recovered, verified numbers only).
- Spanish versions of trade pages (`/es/…`, hreflang) — Spanish-speaking landscaping owners are an underserved segment.
- noindex `sites.peakreachms.com`.
- Meta description trim pass; quarterly rerun of `seo_phase3.py` after any page edit.

## 6. Decisions needed from Joaquin
1. Approve deploy of Phase 3 (git push → Cloudflare). 
2. GA4/GTM ID (or create the property) + a GSC Performance export / access.
3. LinkedIn URLs for `sameAs`.
4. OK to test the contact form against production GHL once deployed.
5. Grant delete permission (or remove `tools/__pycache__/` + `tools/_patch_generator_phase3.py` manually) before commit.
