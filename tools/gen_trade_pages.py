#!/usr/bin/env python3
"""Generate /[trade]-crm pages for peakreachms.com per ADR-017. Run from repo root."""
import json, re, html as H

HOST = "https://www.peakreachms.com/"

TRADES = {
 "landscaping": dict(
   name="Landscaping", slug="landscaping-crm", kw="landscaping CRM",
   icon="trees",
   hero_h1="Landscaping CRM that actually follows up — so quoted jobs don't die in the inbox.",
   hero_lead="Most landscaping companies don't need another CRM login. They need the follow-up to happen after every estimate, every week, without the owner chasing it. PeakReach installs and operates that system — the CRM is the machinery underneath, and we run it.",
   proof="This is where PeakReach started: inside a real landscaping company, on real estimates, crews, and office handoffs.",
   pains=[("Spring estimate season buries the office","Forty quotes go out in two weeks. Follow-up depends on whoever has a free minute — and nobody does."),
          ("Maintenance proposals stall silently","Recurring-contract proposals sit with no decision. No one knows which ones are still alive."),
          ("Past customers never hear from you again","Last year's mulch and cleanup clients would rebook — if anyone asked.")],
   does=[("clipboard-list","Every estimate tracked","Sent estimates enter one visible pipeline with status, owner, and next action."),
         ("repeat","Follow-up runs on schedule","Approved email and text sequences fire on time and stop the moment the customer replies."),
         ("rotate-ccw","Seasonal reactivation","Eligible past customers get a second touch before the season, not after it."),
         ("flag","Exceptions land on a person","Replies, aging quotes, and opt-outs are routed to the office — flagged, not remembered.")],
   fit=["Landscaping, lawn care, or hardscape company, roughly $500K–$2M+ in revenue","Sends estimates consistently — enough volume for follow-up to matter","Has an office or sales owner who can handle the human exceptions","Uses a system of record (or has usable estimate/customer data)"],
   faqs=[("Is this a landscaping CRM or a service?","Both, in a specific way: there is a CRM and pipeline underneath, but you don't buy software. You buy a managed Revenue Recovery System — PeakReach configures, operates, monitors, and reports on it."),
         ("Do I have to switch off my estimating software?","Usually no. PeakReach connects the follow-up system around the tools you already quote from, whenever the data is usable."),
         ("How fast can it go live?","Most installations launch within 2–4 weeks after access and onboarding information are complete. That is an operating estimate, not a guaranteed SLA."),
         ("What does it cost?","$2,500 implementation plus $1,497 per month, 12-month initial term, then month-to-month with 30 days' written notice.")]),
 "hvac": dict(
   name="HVAC", slug="hvac-crm", kw="HVAC CRM",
   icon="thermometer",
   hero_h1="HVAC CRM built around one job: the replacement quote that never gets a follow-up.",
   hero_lead="Repair calls close on the spot. Replacement and install quotes don't — they sit for days while the homeowner gets two more bids. PeakReach installs and operates the system that follows up on every one of them, on schedule, and flags the ones that need a comfort advisor.",
   proof="Built and validated inside a real quote-driven service business, then standardized for HVAC and other trades that sell through estimates.",
   pains=[("Replacement quotes go cold in 72 hours","The homeowner has three bids. The one that follows up is the one that stays in the conversation."),
          ("Dispatchers can't chase quotes","The office is answering the phone and moving trucks. Follow-up is nobody's job — so it's no one's."),
          ("Maintenance-agreement renewals slip","Expiring agreements don't get a nudge until the customer is already gone.")],
   does=[("clipboard-list","Every quote tracked","Replacement, install, and IAQ quotes enter one visible pipeline with owner and next action."),
         ("repeat","Follow-up that keeps you in the bid","Approved email and text touches run on schedule and stop the moment the customer answers."),
         ("phone-call","Missed-call capture","A missed call during peak season triggers a response before the caller dials the next company."),
         ("flag","Advisor alerts","Replies and aging quotes route to the right comfort advisor — flagged, not remembered.")],
   fit=["Residential or light-commercial HVAC company, roughly $500K–$3M in revenue","Sells replacements and installs through written quotes","Has an office manager or sales lead who owns follow-up exceptions","Uses a field-service or estimating system of record"],
   faqs=[("Is this an HVAC CRM?","There is a CRM and pipeline underneath, configured for quote follow-up. But you don't license software from PeakReach — you get a managed system that we operate, monitor, and report on every week."),
         ("Does it replace ServiceTitan, Housecall Pro, or Jobber?","No. PeakReach connects and manages the follow-up workflow around your approved system of record whenever the data is usable."),
         ("How fast can it go live?","Most installations launch within 2–4 weeks after access and onboarding information are complete. That is an operating estimate, not a guaranteed SLA."),
         ("What does it cost?","$2,500 implementation plus $1,497 per month, 12-month initial term, then month-to-month with 30 days' written notice.")]),
 "plumbing": dict(
   name="Plumbing", slug="plumbing-crm", kw="plumbing CRM",
   icon="droplets",
   hero_h1="Plumbing CRM for the quotes that don't close on the truck.",
   hero_lead="Emergency work closes itself. Water heaters, repipes, sewer lines, and remodel bids don't — they go home with the customer and get compared. PeakReach installs and operates the system that follows up on every written quote and flags the ones that need a human.",
   proof="Built and validated inside a real quote-driven service business, then standardized for plumbing and other trades that sell through estimates.",
   pains=[("Big-ticket quotes leave with the customer","Water heater, repipe, and sewer quotes get compared for days. Whoever follows up wins the comparison."),
          ("Techs quote, nobody chases","The tech is on the next call. The office never sees the open quote. It quietly expires."),
          ("No visibility into what's still open","The owner can't say how many quotes are outstanding this week, or who owns them.")],
   does=[("clipboard-list","Every written quote tracked","Quotes from the field enter one visible pipeline with status, owner, and next action."),
         ("repeat","Follow-up that runs itself","Approved email and text touches go out on schedule and stop when the customer replies or books."),
         ("phone-call","Missed-call capture","Missed calls trigger an immediate response so the caller doesn't move on to the next plumber."),
         ("flag","Office alerts","Replies, aging quotes, and opt-outs route to the office — flagged, not remembered.")],
   fit=["Residential or commercial plumbing company, roughly $500K–$3M in revenue","Issues written quotes for water heaters, repipes, sewer, or remodel work","Has an office owner who can handle the human exceptions","Uses a field-service or estimating system of record"],
   faqs=[("Is this a plumbing CRM?","Underneath, yes — a CRM and pipeline configured for quote follow-up. But you don't buy software. PeakReach installs and operates the system and reports verified activity every week."),
         ("Will it work with my dispatch software?","Usually. PeakReach connects the follow-up workflow around your approved system of record whenever the data is usable."),
         ("How fast can it go live?","Most installations launch within 2–4 weeks after access and onboarding information are complete. That is an operating estimate, not a guaranteed SLA."),
         ("What does it cost?","$2,500 implementation plus $1,497 per month, 12-month initial term, then month-to-month with 30 days' written notice.")]),
 "electrician": dict(
   name="Electrical", slug="electrician-crm", kw="electrician CRM",
   icon="zap",
   hero_h1="Electrician CRM that follows up on panel upgrades, EV chargers, and rewires — every time.",
   hero_lead="Service calls are easy. The $4,000 panel upgrade and the whole-home rewire are not — the homeowner takes the quote and waits. PeakReach installs and operates the system that follows up on every written estimate and flags the ones that need your estimator.",
   proof="Built and validated inside a real quote-driven service business, then standardized for electrical and other trades that sell through estimates.",
   pains=[("Project quotes stall for weeks","Panels, EV chargers, generators, and rewires get compared and postponed. Silence loses them."),
          ("Estimators quote, then move on","The estimator is on the next site. The open quote has no owner and no next action."),
          ("Commercial proposals disappear into procurement","Tenant fit-outs and maintenance proposals sit with no visibility and no cadence.")],
   does=[("clipboard-list","Every estimate tracked","Residential and commercial estimates enter one visible pipeline with owner and next action."),
         ("repeat","Follow-up on a schedule","Approved email and text touches go out on time and stop the moment the customer answers."),
         ("phone-call","Missed-call capture","Missed calls trigger a response so the homeowner doesn't call the next electrician."),
         ("flag","Estimator alerts","Replies and aging estimates route to the right estimator — flagged, not remembered.")],
   fit=["Residential or commercial electrical contractor, roughly $500K–$3M in revenue","Issues written estimates for panels, EV chargers, generators, rewires, or projects","Has an office or estimating owner who can handle exceptions","Uses a field-service or estimating system of record"],
   faqs=[("Is this an electrician CRM?","There is a CRM and pipeline underneath, configured for estimate follow-up. But you don't license software — you get a managed system PeakReach operates, monitors, and reports on."),
         ("Does it replace my estimating tool?","No. PeakReach connects the follow-up workflow around your approved system of record whenever the data is usable."),
         ("How fast can it go live?","Most installations launch within 2–4 weeks after access and onboarding information are complete. That is an operating estimate, not a guaranteed SLA."),
         ("What does it cost?","$2,500 implementation plus $1,497 per month, 12-month initial term, then month-to-month with 30 days' written notice.")]),
 "roofing": dict(
   name="Roofing", slug="roofing-crm", kw="roofing CRM",
   icon="home",
   hero_h1="Roofing CRM for the inspections that never turn into a signed contract.",
   hero_lead="You inspected the roof, wrote the estimate, and the homeowner said they'd think about it. Then three other roofers knocked. PeakReach installs and operates the system that follows up on every estimate — retail and insurance — on schedule, and flags the ones that need your sales rep.",
   proof="Built and validated inside a real quote-driven service business, then standardized for roofing and other trades that sell through estimates.",
   pains=[("Retail estimates go quiet after the inspection","The homeowner is comparing. Without a cadence, yours is the estimate that gets forgotten."),
          ("Insurance jobs stall between adjuster and approval","Weeks pass. Nobody owns the next touch. The file goes cold."),
          ("Storm season outruns the office","Hundreds of leads in two weeks. Follow-up depends on memory, and memory fails.")],
   does=[("clipboard-list","Every estimate tracked","Retail and insurance estimates enter one visible pipeline with status, owner, and next action."),
         ("repeat","Follow-up on a schedule","Approved email and text touches go out on time and stop the moment the homeowner replies or signs."),
         ("phone-call","Missed-call capture","Storm-season missed calls trigger a response before the caller dials the next roofer."),
         ("flag","Rep alerts","Replies and aging estimates route to the assigned rep — flagged, not remembered.")],
   fit=["Residential roofing company, roughly $1M–$5M in revenue","Writes estimates after inspections and has real volume in season","Has a sales manager or office owner who can handle exceptions","Uses a roofing CRM or estimating system of record with usable data"],
   faqs=[("Is this a roofing CRM?","There is a CRM and pipeline underneath, configured for estimate follow-up. But you don't license software from PeakReach — you get a managed system we operate, monitor, and report on every week."),
         ("Does it replace AccuLynx or JobNimbus?","No. PeakReach connects and manages the follow-up workflow around your approved system of record whenever the data is usable."),
         ("How fast can it go live?","Most installations launch within 2–4 weeks after access and onboarding information are complete. That is an operating estimate, not a guaranteed SLA."),
         ("What does it cost?","$2,500 implementation plus $1,497 per month, 12-month initial term, then month-to-month with 30 days' written notice.")]),
}

ORG = '{"@context":"https://schema.org","@type":"Organization","name":"PeakReach Managed Systems","legalName":"PeakReach Marketing Solutions LLC","url":"https://www.peakreachms.com/","logo":"https://www.peakreachms.com/assets/mark-color.png","email":"info@peakreachms.com","slogan":"Built by operators. Run by systems.","description":"PeakReach installs and manages the systems that make revenue, accountability, and operations visible, repeatable, and less dependent on the owner.","address":{"@type":"PostalAddress","addressLocality":"Sanford","addressRegion":"NC","addressCountry":"US"},"areaServed":"United States"}'

def e(s): return H.escape(s, quote=True)

def page(t):
    url = HOST + t["slug"]
    title = f'{t["kw"]} — stop losing the jobs you already quoted | PeakReach'
    desc = f'A {t["kw"]} that follows up: PeakReach installs and operates the Revenue Recovery System for {t["name"].lower()} companies — every estimate tracked, followed up, and accounted for. $2,500 + $1,497/mo.'
    faq_ld = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in t["faqs"]]}, ensure_ascii=False)
    pains = "\n".join(f'    <div class="card"><h3>{e(h)}</h3><p>{e(p)}</p></div>' for h,p in t["pains"])
    does = "\n".join(f'    <div class="card"><div class="ico"><i data-lucide="{i}"></i></div><h3>{e(h)}</h3><p>{e(p)}</p></div>' for i,h,p in t["does"])
    fit = "\n".join(f'        <li><span class="m">✓</span>{e(x)}</li>' for x in t["fit"])
    faqs = "\n".join(f'    <div class="qa"><button>{e(q)}<span class="plus">+</span></button><div class="a"><p>{e(a)}</p></div></div>' for q,a in t["faqs"])
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<link rel="canonical" href="{url}">
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#0A2440">
<link rel="icon" href="assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;450;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css?v=20260902">
<meta property="og:type" content="website">
<meta property="og:site_name" content="PeakReach Managed Systems">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://www.peakreachms.com/assets/mark-color.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="https://www.peakreachms.com/assets/mark-color.png">
<script type="application/ld+json">
{ORG}
</script>
<script type="application/ld+json">
{faq_ld}
</script>
</head>
<body>


<header class="nav"><div class="wrap">
  <a class="logo" href="index.html">
    <img src="assets/mark-color.png" alt="PeakReach">
    <span class="txt"><b>PeakReach</b><span>MANAGED SYSTEMS</span></span>
  </a>
  <nav class="links">
    <a href="index.html#what">What We Do</a>
    <a href="index.html#how">How It Works</a>
    <a href="index.html#start">Start Here</a>
    <a href="standard.html">The Standard</a>
    <a href="pricing.html">Pricing</a>
    <a href="resources.html">Resources</a>
    <a class="btn btn-ghost" href="https://app.peakreachms.com" target="_blank" rel="noopener" style="padding:11px 18px">Login</a>
    <a class="btn btn-teal" href="revenue-leak-audit.html" style="padding:11px 20px">Find My Revenue Leaks</a>
  </nav>
  <button class="menu-btn" data-menu aria-label="Menu">☰</button>
</div></header>

<section class="section" style="padding-top:120px"><div class="wrap">
  <div class="center">
    <span class="kicker"><span class="num"><i data-lucide="{t["icon"]}"></i></span>{e(t["kw"])} · Revenue Recovery System</span>
    <h1 class="big">{e(t["hero_h1"])}</h1>
    <p class="lead">{e(t["hero_lead"])}</p>
    <div class="cta-row" style="justify-content:center"><a class="btn btn-teal" href="revenue-leak-audit.html">Find My Revenue Leaks</a><a class="btn btn-ghost" href="pricing.html">See pricing</a></div>
    <p class="fine" style="margin-top:18px;color:var(--muted)">{e(t["proof"])}</p>
  </div>
</div></section>

<section class="section band"><div class="wrap">
  <div class="center"><span class="kicker"><span class="num">01</span>What a CRM alone doesn't fix</span><h2 class="big">You already paid for the lead. Don't lose it after the estimate.</h2></div>
  <div class="cards">
{pains}
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="center"><span class="kicker"><span class="num">02</span>What PeakReach runs for {e(t["name"].lower())} companies</span><h2 class="big">Every estimate, accounted for</h2></div>
  <div class="cards" style="grid-template-columns:repeat(4,1fr)">
{does}
  </div>
  <div class="center" style="margin-top:40px"><a class="btn btn-teal" href="revenue-leak-audit.html">Find My Revenue Leaks &#8594;</a></div>
</div></section>

<section class="section dark"><div class="wrap">
  <div class="split">
    <div>
      <span class="kicker on-dark"><span class="num">03</span>Is this a CRM?</span>
      <h2 class="big">Yes, there's a CRM underneath. No, you don't buy software.</h2>
      <p style="margin-top:18px;font-size:16px;color:#c9d8e8">A CRM is a filing cabinet with reminders. It only recovers revenue if someone configures the follow-up, watches the exceptions, and fixes it when it breaks. That someone is PeakReach. You get the outcome — every estimate tracked, followed up, and accounted for — and we run the machinery: CRM, pipeline, compliant text and email, call tracking, dashboards, monitoring.</p>
      <ul class="usp-list on-dark">
        <li><span class="dot">✓</span><span><b>Installed and operated.</b> Configure → Integrate → QA → Launch → Stabilize, then managed every week.</span></li>
        <li><span class="dot">✓</span><span><b>Reported, not assumed.</b> A weekly report of verified activity and outcomes; a monthly review.</span></li>
        <li><span class="dot">✓</span><span><b>Your data stays yours.</b> Client-owned accounts; PeakReach operates under license with a defined Standard Exit.</span></li>
      </ul>
      <div class="cta-row"><a class="btn btn-ghost-d" href="crm-for-service-businesses.html">What actually matters in a CRM for service businesses →</a></div>
    </div>
    <div class="fit good">
      <h3>✓ Good fit for {e(t["name"].lower())}</h3>
      <ul>
{fit}
      </ul>
      <p class="fine" style="margin-top:18px;color:var(--muted)">Not a fit: startups, very low estimate volume, or companies that want advertising as the only service.</p>
    </div>
  </div>
</div></section>

<section class="section band"><div class="wrap">
  <div class="center">
    <span class="kicker"><span class="num">04</span>Start here</span>
    <h2 class="big">One system. One clear price.</h2>
    <p class="lead">$2,500 implementation · $1,497 per month · 12-month initial term, then month-to-month with 30 days' written notice. The first step is a 20–30 minute Revenue Leak Audit — complimentary for qualified companies.</p>
    <div class="cta-row" style="justify-content:center"><a class="btn btn-teal" href="revenue-leak-audit.html">Apply for a Revenue Leak Audit</a><a class="btn btn-ghost" href="pricing.html">Review full pricing</a></div>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="center"><span class="kicker"><span class="num">?</span>FAQ</span><h2 class="big">Common questions from {e(t["name"].lower())} owners</h2></div>
  <div class="faq">
{faqs}
  </div>
  <p class="center" style="margin-top:32px;font-size:14px;color:var(--muted)">Other trades: <a href="for-home-services.html" style="color:var(--blue)">home services &amp; contractors hub</a></p>
</div></section>

<footer><div class="wrap">
  <div class="foot-grid">
    <div>
      <div class="foot-logo"><img src="assets/mark-color.png" alt="PeakReach"><span class="ftxt"><b>PeakReach</b><span>MANAGED SYSTEMS</span></span></div>
      <p style="max-width:360px">We install and manage the systems that make revenue, accountability, and operations visible, repeatable, and less dependent on the owner.</p>
      <p class="legal-interim">PeakReach Managed Systems is operated by PeakReach Marketing Solutions LLC.</p>
    </div>
    <div>
      <h4>Explore</h4>
      <ul>
        <li><a href="index.html#what">What We Do</a></li>
        <li><a href="index.html#how">How It Works</a></li>
        <li><a href="index.html#start">Start Here</a></li>
        <li><a href="standard.html">The Standard</a></li>
        <li><a href="trust.html">Trust &amp; Security</a></li>
        <li><a href="for-home-services.html">Home Services &amp; Contractors</a></li>
      </ul>
    </div>
    <div>
      <h4>Get in touch</h4>
      <ul>
        <li><a href="contact.html">Contact</a></li>
        <li><a href="mailto:info@peakreachms.com">info@peakreachms.com</a></li>
        <li>Sanford, North Carolina</li>
        <li><a href="privacy.html">Privacy</a> · <a href="terms.html">Terms</a></li>
      </ul>
      <p class="verse">Romans 5:8</p>
    </div>
  </div>
  <div class="foot-bottom">
    <span>© 2026 PeakReach Managed Systems. All rights reserved.</span>
    <span><a href="revenue-leak-audit.html" style="color:inherit">Revenue Leak Audit</a> · <a href="mailto:info@peakreachms.com" style="color:inherit">Contact</a> · <a href="privacy.html" style="color:inherit">Privacy</a> · <a href="terms.html" style="color:inherit">Terms</a></span>
  </div>
</div></footer>
<script src="https://unpkg.com/lucide@latest"></script>
<script src="app.js"></script>
</body>
</html>
'''

if __name__ == "__main__":
    for t in TRADES.values():
        open(t["slug"] + ".html", "w").write(page(t))
        print("wrote", t["slug"] + ".html")
