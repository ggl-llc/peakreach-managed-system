# PeakReach Website — SEO Audit & Phase 3 Build Log
**Site:** https://www.peakreachms.com · **Repo:** `ggl-llc/peakreach-managed-system` (static HTML, Cloudflare Pages)
**Date:** 2026-09-08 · **Project:** PeakReach · **Status:** ✅ LIVE. Phase 3 (`fbaeb97`) + 3b (`1ddf968`) + docs (`a48843e`) deployed via Cloudflare Pages build `b2c48751` (production rolled to it after a stray retry of `97ca7f8` had taken production). Root cause of the initial non-deploy: Pages project was disconnected from GitHub; Joaquin reconnected it.

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
| Analytics | No GA4/GTM tag on any page at audit time → **GA4 `G-Z7E84LTQZ6` added to all 25 pages (Phase 3b)** with key events `rla_form_success` / `contact_form_success` | grep of all 25 HTML files |
| Search Console (Jun 6–Sep 5, 2026) | 27 clicks · 1,260 impressions · CTR 2.2% · avg pos 14.1 · 52 queries, all brand/noise ("peak reach bv" = Dutch company; "raleigh nc seo crm", "marketing advice raleigh" = legacy agency positioning). **Zero impressions for any "[trade] crm" or follow-up query.** | GSC Performance, read 2026-09-08 |
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

## 3. Phase 3 — what was built (deployed 2026-09-08)

**New:** `tools/seo_phase3.py` (idempotent sitewide normalizer), `assets/og-default.png` (1200×630), README conventions.
**Changed:** 24 HTML pages, `sitemap.xml`, `styles.css` (4-col footer + cache-bust `?v=20260908`), `tools/gen_trade_pages.py` (grammar, cross-links, BreadcrumbList, pipes through normalizer).
**Verification done:** dry-run on one page first → full run → second run reports 0 changes (idempotent) → all JSON-LD parses → no `.html` hrefs remain → all 24 indexable pages have og/twitter → headless render of index/contact/landscaping-crm footers desktop+mobile OK → live check confirms Cloudflare serves clean URLs (`/landscaping-crm` 200).
**Live read-back (2026-09-08, production HTML fetched with cache:no-store):** new titles ✓ · Industries footer ✓ · 0 `.html` links ✓ · og-default.png 200 ✓ · GA4 `G-Z7E84LTQZ6` on every page ✓ (gtag loaded in-browser) · sitemap 24 URLs lastmod 2026-09-08 ✓ · contact form wired ✓.
**Contact form E2E:** test submit sent (name "Claude Test Phase3", email `qa-phase3-20260908@peakreachms.com`, company "PeakReach QA") → page confirmed "Thanks — your message is in" (webhook returned 2xx). **Contact NOT yet read back in GHL:** the webhook posts to location `PU3svlBW3x81ujPelNlV`; the LeadConnector MCP is bound to `RS0xfAV3VyR5lj97q0z6` (GGL) and the GHL UI required a login the session cannot perform. Joaquin to confirm the contact exists in PU3svlBW3x81ujPelNlV (then delete the test contact). Until read back, treat the form as "webhook accepted", not "lead lands in CRM".

**Housekeeping:** done by Joaquin before commit; `.gitignore` added.

### Deploy checklist (steps 1–3 done 2026-09-08; 4–5 pending)
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

## 7. Phase 4 — P1 content set (✅ LIVE 2026-09-08, commit `074fb7a`)

**New generator:** `tools/gen_articles.py` (content dicts → article template → `normalize_html`). Edit content there, re-run, commit. Never hand-edit the HTML.
**8 new pages (900–1,100 words each, FAQPage + BreadcrumbList + Article schema, comparison table, intro "second title", one paragraph per sub-point):**

| URL | Primary keyword (vol / KD) | Companion page |
|---|---|---|
| /best-landscaping-crm-software | landscaping crm software (480 / 9) + crm for landscapers, landscape crm | /landscaping-crm |
| /best-hvac-crm-software | hvac crm (720 / 16), hvac crm software (720 / 11) | /hvac-crm |
| /best-plumbing-crm-software | crm for plumbers (590 / 15), plumbing crm software | /plumbing-crm |
| /best-electrician-crm-software | crm for electricians (320 / 5), electrician crm | /electrician-crm |
| /best-roofing-crm-software | roofing crm (1,000 / 28), roofing crm software (480) | /roofing-crm |
| /hvac-estimating-software | hvac estimating software (1,000 / 16) | /hvac-crm |
| /landscaping-estimating-software | landscaping estimating software (390 / 7), landscape estimating software (590 / 7) | /landscaping-crm |
| /landscaping-business-software | landscaping business software (880 / 21), landscaping management software (720 / 19) | /landscaping-crm |

**Also changed:** trade pages now link to their comparison article ("Comparing tools?"); `/resources` gained a "Software guides" grid (8 cards); `styles.css` got table + intro-title styles; stylesheet links are now cache-busted by content hash (`?v=<md5>`); sitemap 32 URLs; all 8 slugs registered in `seo_phase3.ARTICLES` with fixed `datePublished` 2026-09-08.
**Editorial guardrails applied:** no vendor pricing stated (changes too often); positioning summarized with a dated disclaimer; banned vocabulary check passes (no "gohighlevel alternative", "white label crm", "quoting software"); every article reframes to the Revenue Recovery System + Revenue Leak Audit CTA.
**Verified:** normalizer idempotent (0/33 on second run) · all JSON-LD parses · titles ≤72 / descriptions ≤160 · headless render of article intro, comparison table (desktop + mobile scroll) and resources grid OK.
**Live read-back (2026-09-08, cache:no-store):** all 8 URLs 200 with new titles, comparison table, intro-title, GA4 ×1, Article+FAQPage+BreadcrumbList ✓ · sitemap 32 ✓ · trade→article link ✓ · /resources 12 cards ✓ · hashed CSS served with table styles ✓ · roofing table rendered in Chrome ✓.
**Next:** request indexing for the 8 URLs in GSC; check Rich Results for FAQ on one article; in 4–6 weeks read GSC queries for the 8 target terms.

## 8. Semrush project + two Cloudflare findings (2026-09-08)

**Semrush project `www.peakreachms.com` (ID 29064374)** has Site Audit + Position Tracking enabled, but the tracking campaign is **empty** (`targets: null`) — nothing has ever been tracked. The MCP is read-only, so Joaquin configures it: target `*.peakreachms.com/*`, US national, desktop+mobile, paste `docs/semrush-tracking-keywords.txt` (38 keywords, tagged by page), competitors getjobber.com / housecallpro.com / servicetitan.com / pipelinecrm.com / smith.ai. Site Audit: last crawl 2026-09-08 02:07 UTC (pre-Phase 3): 43 errors · 8 warnings · 402 notices · 378 permanent redirects (the `.html` links, fixed) · 20 pages with one internal link (fixed). Re-run the crawl now to re-baseline; turn off "crawl subdomains" so `sites.peakreachms.com` stops polluting it.

**Finding A — Cloudflare Email Address Obfuscation is ON for peakreachms.com.** Every `mailto:info@peakreachms.com` is rewritten to `/cdn-cgi/l/email-protection` → Semrush reports 40 broken internal links + 2 4xx; crawlers never see the email. Same trap already documented for greengardenlandscape.com in the Índice Operativo. Fix: Cloudflare → peakreachms.com → Scrape Shield → Email Address Obfuscation → **Off**.

**Finding B — Cloudflare "Managed robots.txt" (AI bot blocking) is ON.** Live robots.txt is prefixed with Cloudflare content signals (`ai-train=no`) and `Disallow: /` for GPTBot, ClaudeBot, Google-Extended, CCBot, Applebot-Extended, meta-externalagent, Amazonbot, Bytespider. Consequences: (1) Semrush flags the file as malformed (two `User-agent: *` blocks); (2) the site opts out of AI training and of several AI answer engines' crawlers — for a B2B site that wants to be cited when owners ask ChatGPT/Perplexity "best landscaping CRM", this is a real visibility cost. Googlebot/AI Overviews are unaffected. **Decision for Joaquin:** keep the block (privacy/IP stance) or turn it off (Cloudflare → peakreachms.com → AI Audit / Bots → Manage robots.txt → off; optionally also "Block AI bots" → off). Recommendation: turn the managed robots.txt off so the repo's file is served cleanly, and allow AI crawlers — the content is written to be found.

## 9. Phase 5 — conversion UX + lead capture (built 2026-09-08, pending commit/deploy)

**Deep-analysis findings (live site, desktop + mobile):**
- Home is ~18,300 px tall on mobile (~22 screens) with the only form at the very bottom; hero copy was abstract ("visible, assigned, measurable") and never named the product or the trades; no route from the hero to the SEO entry pages.
- Trade pages (the SEO entry) had **no form** — every CTA bounced to /revenue-leak-audit. Articles had no CTA between the table and the end.
- **Bug:** `.usp-list b{color:var(--ink)}` rendered the bold labels invisible (navy on navy) in the dark "Is this a CRM?" section on all 5 trade pages.
- Nav had 8 items and wrapped at 1280 px; three different navs across page types.
- Both audit forms **required** the SMS-consent checkbox — friction, and contradicts the "consent is not a condition of purchase" sentence next to it.
- Three copies of the lead-submit JS (index, audit page, contact) with no attribution capture; GA4 events only on two of them.
- Reveal animation (.6s, 18 px) left sections blank during fast scrolls.

**Built (all through the normalizer/generators — idempotent, 0/33 on second run):**
1. `app.js` → single `data-lead` handler for every form: payload = names + all named fields + `source`, `form`, `page`, `page_title`, `submitted_at`, first-touch **utm_* / gclid / fbclid / msclkid / landing_page / referrer** (sessionStorage), GA4 `rla_form_success`/`contact_form_success` **+ `generate_lead`**. Legacy inline scripts removed. Cache-busted by content hash (`app.js?v=`), same as CSS.
2. **Trade pages:** "Start here" is now a two-column section with an embedded Revenue Leak Audit form (`source: "Website - {Trade} CRM page"`, hidden `trade`, `estimates_per_month`); hero + mid CTAs scroll to it.
3. **Home hero:** concrete sub-copy (what we do, for whom), "Built for:" chips → 7 trade/segment pages, badges updated. H1 kept (approved company-first thesis).
4. **Standard nav sitewide** (Industries · The System · Pricing · Guides · Contact · Login · CTA) with active state; **mobile sticky CTA** bar (appears after 520 px scroll; not on form pages).
5. SMS consent optional on all forms (label now "Text me about my audit…"). Contact form migrated to the shared handler.
6. Audit page: "What happens next — three steps, no sales deck" strip. Articles: callout CTA after the comparison table.
7. Fixes: invisible bold labels; reveal .3s/10 px + `prefers-reduced-motion`; fonts trimmed to used weights (450/Mono 600 dropped); meta descriptions ≤155 on index, crm-for-contractors, crm-for-service-businesses, standard, for-dealers, for-commercial-services.

**Verified locally (Playwright, webhook stubbed — no production writes):** 4 form types submit with correct payloads; attribution persists across pages within a session; validation message on empty submit; GA4 dataLayer receives `rla_form_success` + `generate_lead`; renders checked on desktop/mobile (hero, trade form, dark section, sticky CTA, steps).
**Not done (needs Joaquin):** verified proof numbers for a home-page proof strip / GGL case study (no numbers invented); GHL calendar link for a post-submit "book now" (`data-next` is supported by the handler); LinkedIn company URL; Cloudflare toggles (§8).
