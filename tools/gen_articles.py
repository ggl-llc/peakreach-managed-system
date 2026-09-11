#!/usr/bin/env python3
"""Generate the P1 SEO article set for peakreachms.com (comparison + software-gap articles).

Run from repo root:  python3 tools/gen_articles.py
Output is piped through seo_phase3.normalize_html so pages get the standard head/footer/GA4/schema.
Content lives in ARTICLES below — edit there, re-run, commit. Never hand-edit the generated HTML.

Editorial rules (from Joaquin): intro heading right after the H1 ("second title"), one paragraph per
sub-point, honest comparisons (no invented pricing, no bashing), CRM vocabulary is an entry door that
reframes to the Revenue Recovery System. Allowed: "[trade] crm", "crm for contractors/service
businesses". Not allowed: "gohighlevel alternative", "white label crm", "quoting software".
"""
import json, os, sys, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seo_phase3 import normalize_html, HOST, TODAY

def e(s): return H.escape(s, quote=True)

# ---------------------------------------------------------------------------------------------
# Shared blocks
# ---------------------------------------------------------------------------------------------
WHY_TOOLS_DONT_CLOSE = (
    "Every tool above can store a customer, build a quote, and send a reminder. What none of them can do is "
    "<em>own the outcome</em>. A follow-up sequence only recovers revenue if someone configures it for your quote types, "
    "watches the exceptions, adjusts the timing after the first month, and fixes it when a field or an integration breaks. "
    "In most companies that someone is the owner or the office manager, on a busy Tuesday, with a phone that won't stop ringing. "
    "That is why so many CRMs are paid for and half-used: the software is fine; the operating of it never got assigned."
)

def reframe(trade_slug, trade_label):
    return (
        f"PeakReach takes the other side of that line. We don't sell a CRM license; we install and operate a "
        f"<a href=\"/revenue-recovery\">Revenue Recovery System</a> around the tools you already quote from — every estimate tracked, "
        f"followed up on schedule, and accounted for in a weekly report of verified activity. There is a CRM and pipeline underneath; "
        f"you get the outcome, and we run the machinery. See what that looks like for <a href=\"/{trade_slug}\">{trade_label}</a>, "
        f"or start with a 20–30 minute <a href=\"/revenue-leak-audit\">Revenue Leak Audit</a>."
    )

# ---------------------------------------------------------------------------------------------
# Article content
# ---------------------------------------------------------------------------------------------
ARTICLES = [
 dict(
  slug="best-landscaping-crm-software", kw="landscaping CRM software", kicker="Landscaping · Comparison", icon="trees",
  trade_slug="landscaping-crm", trade_label="landscaping companies",
  title="Best Landscaping CRM Software (2026): 6 Options Compared Honestly",
  desc="Jobber, Aspire, LMN, Service Autopilot, SingleOps and RealGreen compared for landscaping companies — who each fits, and the one job none of them does alone.",
  h1="Best landscaping CRM software in 2026: six options, compared honestly",
  intro="The right CRM for a landscaper depends on what you sell — and on who is going to run it",
  lead="Most “best landscaping CRM” lists are written by software companies ranking themselves first. This one was written by a landscaping operator who has used several of these tools on real estimates and real crews. Here is who each one actually fits, and the gap every one of them leaves open.",
  sections=[
   ("What a landscaping CRM has to do", [
     "For a landscaping or lawn care company the CRM is rarely a standalone sales tool. It has to hold the customer record, the property, the estimate, the recurring schedule, and the invoice — or connect cleanly to the system that does. If it can’t see your estimates, it can’t help you follow up on them, and follow-up is where landscapers lose the most money after the quote.",
     "Judge any option on four things: does it track every estimate with a status and an owner; can it run follow-up on a schedule without a person remembering; does it stop automatically when the customer replies or books; and does it show the owner what is still open this week. Everything else — routing, job costing, time tracking — is operations software wearing a CRM badge, which is fine as long as you know what you are buying."]),
   ("The six options", None),   # table goes here
   ("Where landscaping quotes actually die", [
     "Spring estimate season is the test. Forty quotes go out in two weeks. The office is answering the phone and moving crews. Follow-up depends on whoever has a free minute, and nobody does. By the time someone opens the list, half the quotes have gone to whichever competitor called back. None of the six tools above prevents that by itself — they all need a person to set the cadence, watch replies, and keep the pipeline honest.",
     WHY_TOOLS_DONT_CLOSE]),
   ("How to choose", [
     "Under roughly $1M in revenue with mostly residential maintenance and enhancements, Jobber or Service Autopilot will carry the whole business. Growing past $2–3M with design-build or commercial work, Aspire or LMN earn their complexity through estimating and job costing. Lawn care and fertilization programs with route density lean Service Autopilot or RealGreen. Tree care and mixed green-industry companies look at SingleOps. Whatever you pick, decide on day one who owns follow-up — the tool will not decide for you.",
     reframe("landscaping-crm", "landscaping companies")]),
  ],
  table=[
   ("Jobber", "Residential landscaping and lawn care, roughly $300K–$2M", "Fast to set up; quoting, scheduling, invoicing and client communication in one place; automated quote follow-up reminders", "Reminders are generic unless someone tunes them per service and watches replies"),
   ("Aspire", "Commercial and design-build landscaping, typically $3M+", "Deep estimating, job costing and crew management built for landscaping", "Heavy implementation; sales follow-up is not the product’s center of gravity"),
   ("LMN", "Landscapers who want budgeting and estimating discipline", "Budget-based estimating, time tracking, and training content for owners", "CRM and follow-up are lighter than the estimating side"),
   ("Service Autopilot", "Lawn care and maintenance companies with route density", "Routing, recurring billing, automations and forms; strong for maintenance programs", "Automations are powerful but require real configuration and ongoing ownership"),
   ("SingleOps", "Tree care, landscaping and mixed green-industry companies", "Estimating, CRM and scheduling designed around green-industry jobs", "Smaller ecosystem; follow-up still needs an owner"),
   ("RealGreen", "Lawn care and pest programs selling recurring applications", "Marketing, routing and program billing for application-based businesses", "Less suited to project or design-build estimating"),
  ],
  faqs=[
   ("What is the best CRM for a small landscaping business?", "For most landscaping companies under about $1M, Jobber or Service Autopilot cover quoting, scheduling and invoicing in one system. The better question is who will run the follow-up on every estimate — that decision matters more than the brand."),
   ("Do landscaping CRMs follow up on estimates automatically?", "Most can send reminder emails or texts. Whether that recovers revenue depends on someone configuring the cadence for your services, watching replies, and adjusting — which is the part that usually never gets assigned."),
   ("Do I need a landscaping CRM if I already use estimating software?", "Estimating software gets the quote out. Recovering the quotes that go quiet is a different job, and that is where a CRM — or a managed follow-up system — earns its keep."),
   ("Does PeakReach replace my landscaping software?", "Usually no. PeakReach installs and operates the Revenue Recovery System around your approved system of record whenever the data is usable."),
  ]),

 dict(
  slug="best-hvac-crm-software", kw="HVAC CRM software", kicker="HVAC · Comparison", icon="thermometer",
  trade_slug="hvac-crm", trade_label="HVAC companies",
  title="Best HVAC CRM Software (2026): 6 Options Compared for Contractors",
  desc="ServiceTitan, Housecall Pro, FieldEdge, Jobber, Workiz and ServiceTrade compared for HVAC contractors — who fits each, and why replacement quotes still die.",
  h1="Best HVAC CRM software in 2026: six options, compared for contractors",
  intro="Repair calls close on the truck. Replacement quotes don’t — pick the CRM for the second one",
  lead="HVAC is two businesses. Service calls close on the spot; replacement and install quotes go home with the homeowner and get compared against two more bids. Most HVAC CRM reviews rank dispatch features. This one ranks the six common options on what happens after the replacement quote goes out.",
  sections=[
   ("What an HVAC CRM has to handle", [
     "An HVAC company needs dispatch, pricebook, service agreements and invoicing to run the day. The CRM piece — the part that tracks a replacement quote from “sent” to “signed or lost” — is often bolted on. Before comparing brands, ask whether the tool shows every open replacement and install quote with an owner and a next action, and whether follow-up can run on a schedule that stops the moment the homeowner replies.",
     "Maintenance agreements are the second CRM job. Expiring agreements need a nudge before they lapse, not after. If the tool can’t see agreement dates and trigger a touch, renewals will slip quietly every month."]),
   ("The six options", None),
   ("Why replacement quotes go cold in 72 hours", [
     "The homeowner has three bids on the counter. The contractor who follows up is the one who stays in the conversation. Dispatchers can’t chase quotes — they are answering the phone and moving trucks. Comfort advisors are on the next appointment. So the $9,000 system quote sits, and the company that installed a follow-up cadence wins the comparison without being the cheapest.",
     WHY_TOOLS_DONT_CLOSE]),
   ("How to choose", [
     "Under about $2M in residential service, Housecall Pro, Jobber or Workiz will run the company with little implementation. Between $2M and $10M with multiple trucks and a real pricebook, FieldEdge or ServiceTitan earn their cost — ServiceTitan especially if you want marketing attribution and financing built in. Commercial mechanical work points to ServiceTrade. In every case, name the person who owns quote follow-up and agreement renewals before you sign, because the software will not do that assignment for you.",
     reframe("hvac-crm", "HVAC companies")]),
  ],
  table=[
   ("ServiceTitan", "Residential and commercial HVAC, typically $3M+", "Full platform: dispatch, pricebook, proposals, financing, marketing and reporting", "Expensive and implementation-heavy; follow-up still needs an owner inside the shop"),
   ("Housecall Pro", "Residential HVAC and home services under roughly $3M", "Quick setup, sales proposals, online booking and automated customer communication", "Pipeline visibility for big-ticket quotes is lighter than enterprise tools"),
   ("FieldEdge", "HVAC-centric shops that live in QuickBooks", "Service agreements, flat-rate pricebook and tight QuickBooks integration", "Sales follow-up and marketing are not its strong suit"),
   ("Jobber", "Small HVAC companies with mixed home-service work", "Simple quoting, scheduling and invoicing with quote follow-up reminders", "Less HVAC-specific depth (agreements, pricebook)"),
   ("Workiz", "Small service companies that want calls and jobs in one place", "Built-in phone system, scheduling and job management", "Smaller ecosystem for HVAC-specific workflows"),
   ("ServiceTrade", "Commercial mechanical and fire/life-safety contractors", "Commercial service agreements, deficiency quoting and customer portals", "Not designed for residential replacement sales"),
  ],
  faqs=[
   ("What CRM do most HVAC contractors use?", "Smaller residential shops most often run Housecall Pro or Jobber; larger multi-truck companies gravitate to ServiceTitan or FieldEdge. Commercial mechanical contractors more often use ServiceTrade."),
   ("Does an HVAC CRM track maintenance agreements?", "FieldEdge and ServiceTitan handle agreements natively; Housecall Pro and Jobber cover recurring plans more simply. Whichever you use, someone has to own the renewal touch before the agreement lapses."),
   ("How much does an HVAC CRM cost?", "It ranges from a low monthly fee per user for small-business tools to significant implementation plus per-technician pricing for enterprise platforms. Ask each vendor for current pricing; it changes often."),
   ("Does PeakReach replace ServiceTitan or Housecall Pro?", "No. PeakReach connects and manages the follow-up workflow around your approved system of record whenever the data is usable, and reports verified activity every week."),
  ]),

 dict(
  slug="best-plumbing-crm-software", kw="CRM for plumbers", kicker="Plumbing · Comparison", icon="droplets",
  trade_slug="plumbing-crm", trade_label="plumbing companies",
  title="Best CRM for Plumbers (2026): 6 Plumbing CRM Options Compared",
  desc="ServiceTitan, Housecall Pro, Jobber, FieldPulse, Workiz and Service Fusion compared for plumbers — who fits each, and why big quotes leave with the customer.",
  h1="Best CRM for plumbers in 2026: six plumbing CRM options, compared",
  intro="Emergency work closes itself. Water heaters, repipes and sewer lines don’t — that’s what the CRM is for",
  lead="A plumbing CRM earns its money on the quotes that don’t close on the truck: water heaters, repipes, sewer replacements, remodel bids. Those leave with the customer and get compared for days. Here are the six tools plumbing companies most often run, judged on how well they help you stay in that comparison.",
  sections=[
   ("What a plumbing CRM has to do", [
     "Dispatch and invoicing keep the day moving; the CRM has one extra job — make every written quote visible with a status, an owner and a next action, then keep the follow-up running until the customer says yes, no, or stop. If the tech quotes from the truck and the office never sees the open quote, it quietly expires. That visibility gap is the first thing to test in any demo.",
     "Missed-call capture is the second job. A homeowner with a leak calls three plumbers and books the first one who answers. A CRM that triggers an immediate text back on a missed call recovers jobs that would otherwise never appear in any report."]),
   ("The six options", None),
   ("Where plumbing quotes leave with the customer", [
     "Big-ticket plumbing is compared, not bought on the spot. The tech is on the next call; nobody chases the $6,500 repipe. The owner cannot say how many quotes are outstanding this week or who owns them. Each tool above can store the quote — but tracking it to a decision takes a cadence someone configures and watches.",
     WHY_TOOLS_DONT_CLOSE]),
   ("How to choose", [
     "Owner-operators and shops under about $1.5M do well on Housecall Pro, Jobber or FieldPulse. Growing companies with several trucks and a pricebook move to ServiceTitan or Service Fusion. Workiz suits shops that want the phone system inside the CRM. Whatever the platform, write down who owns quote follow-up and missed-call response — that person, not the software, is the difference in close rate.",
     reframe("plumbing-crm", "plumbing companies")]),
  ],
  table=[
   ("ServiceTitan", "Multi-truck plumbing companies, typically $3M+", "Pricebook, dispatch, proposals, financing and marketing in one platform", "Cost and implementation weight; follow-up ownership still lands on your office"),
   ("Housecall Pro", "Residential plumbing under roughly $3M", "Fast setup, online booking, proposals and automated customer messages", "Lighter pipeline view for big-ticket quotes"),
   ("Jobber", "Small plumbing companies and owner-operators", "Simple quoting, scheduling, invoicing and quote follow-up reminders", "Less plumbing-specific depth (pricebook, agreements)"),
   ("FieldPulse", "Small-to-mid service companies wanting flexibility", "Customizable workflows, estimates and QuickBooks sync at a reasonable price", "Smaller ecosystem and support footprint"),
   ("Workiz", "Shops that want calls, jobs and messaging together", "Built-in phone, scheduling and job tracking", "Less depth for large commercial or multi-location work"),
   ("Service Fusion", "Established shops with multiple technicians", "Dispatch, estimates, invoicing and customer communication with flat pricing", "Interface and reporting feel dated to some users"),
  ],
  faqs=[
   ("What is the best CRM for a small plumbing business?", "Housecall Pro, Jobber and FieldPulse are the usual fits under about $1.5M. Choose on how clearly each shows your open quotes and how easily follow-up runs without a person remembering."),
   ("Can a plumbing CRM text back missed calls?", "Several can, including Workiz and Housecall Pro, and it can be added around most systems. The recovered jobs are real, but the message and timing need an owner."),
   ("Will a plumbing CRM work with my dispatch software?", "Usually. Most connect to QuickBooks and common field-service tools; PeakReach also connects its follow-up system around your approved system of record whenever the data is usable."),
   ("Does PeakReach sell plumbing CRM software?", "No. There is a CRM and pipeline underneath, but you buy a managed Revenue Recovery System that PeakReach configures, operates, monitors and reports on."),
  ]),

 dict(
  slug="best-electrician-crm-software", kw="CRM for electricians", kicker="Electrical · Comparison", icon="zap",
  trade_slug="electrician-crm", trade_label="electrical contractors",
  title="Best CRM for Electricians (2026): 6 Electrical CRMs Compared",
  desc="ServiceTitan, Housecall Pro, Jobber, FieldPulse, simPRO and Workiz compared for electricians — who fits each, and why panel and EV quotes stall.",
  h1="Best CRM for electricians in 2026: six electrical contractor CRMs, compared",
  intro="Service calls are easy. The $4,000 panel upgrade and the whole-home rewire are the quotes a CRM has to carry",
  lead="Electrical contractors sell two ways: quick service calls that close on site, and project estimates — panels, EV chargers, generators, rewires, tenant fit-outs — that get compared and postponed. Here are the six CRMs electricians most often choose, judged on the second kind of sale.",
  sections=[
   ("What an electrician CRM has to do", [
     "Beyond scheduling and invoicing, the CRM has to give every written estimate an owner and a next action, run follow-up on a schedule, and route replies to the estimator instead of a shared inbox. Commercial proposals add a second requirement: visibility through long procurement cycles where weeks pass between touches.",
     "Look for how the tool shows aging estimates. If you cannot pull up “every estimate over 10 days old with no reply” in one view, follow-up will depend on memory — and memory loses to a busy week every time."]),
   ("The six options", None),
   ("Why project quotes stall for weeks", [
     "Panels, EV chargers and generators are discretionary for the homeowner and get compared and postponed. The estimator is on the next site; the open quote has no owner. Commercial proposals disappear into procurement with no cadence. Silence loses them — not price.",
     WHY_TOOLS_DONT_CLOSE]),
   ("How to choose", [
     "Residential service and small-project electricians under about $2M run well on Housecall Pro, Jobber or FieldPulse. Multi-truck residential companies with a pricebook lean ServiceTitan. Commercial and project-heavy contractors that need job costing and progress billing look at simPRO. Workiz fits shops that want the phone system inside the CRM. Then assign follow-up ownership — the platform will not.",
     reframe("electrician-crm", "electrical contractors")]),
  ],
  table=[
   ("ServiceTitan", "Multi-truck residential electrical, typically $3M+", "Pricebook, dispatch, proposals, financing and marketing attribution", "Cost and implementation; follow-up still needs an owner"),
   ("Housecall Pro", "Residential electricians under roughly $3M", "Fast setup, proposals, online booking, automated messaging", "Lighter for commercial and project estimating"),
   ("Jobber", "Small electrical companies with service and small projects", "Simple quoting, scheduling, invoicing, quote follow-up reminders", "Limited depth for commercial project work"),
   ("FieldPulse", "Growing service companies wanting configurability", "Custom workflows, estimates, QuickBooks sync", "Smaller ecosystem"),
   ("simPRO", "Commercial and project electrical contractors", "Estimating, job costing, progress billing and inventory for projects", "Heavier setup; overkill for pure residential service"),
   ("Workiz", "Shops that want calls and jobs in one system", "Built-in phone, scheduling and messaging", "Less depth for large projects"),
  ],
  faqs=[
   ("What is the best CRM for a small electrical contractor?", "Housecall Pro, Jobber or FieldPulse for residential service under about $2M; simPRO when commercial projects dominate. Decide who owns estimate follow-up before choosing the brand."),
   ("Do electrician CRMs follow up on estimates automatically?", "Most can send reminders. Recovering stalled panel and EV quotes takes a cadence configured for those quote types and someone watching the replies."),
   ("Can a CRM handle both residential and commercial electrical work?", "ServiceTitan and simPRO span both reasonably well; small-business tools are strongest on residential service. Commercial procurement cycles need long, patient follow-up regardless of tool."),
   ("Does PeakReach replace my estimating tool?", "No. PeakReach installs and operates the follow-up system around your approved system of record whenever the data is usable."),
  ]),

 dict(
  slug="best-roofing-crm-software", kw="roofing CRM software", kicker="Roofing · Comparison", icon="home",
  trade_slug="roofing-crm", trade_label="roofing companies",
  title="Best Roofing CRM Software (2026): 6 Roofing CRMs Compared Honestly",
  desc="AccuLynx, JobNimbus, Roofr, Leap, ServiceTitan and Jobber compared for roofers — retail vs. insurance fit, and why inspections don’t become contracts.",
  h1="Best roofing CRM software in 2026: six roofing CRMs, compared honestly",
  intro="The inspection is free. The estimate is written. The contract is what a roofing CRM has to produce",
  lead="Roofing CRMs are judged on mobile apps, insurance workflows and photo documentation — all fair. But the number that matters is how many inspected roofs turn into signed contracts, and that depends on follow-up between the estimate and the decision. Here are the six roofing CRMs contractors ask about most, compared on that basis.",
  sections=[
   ("What a roofing CRM has to do", [
     "Retail and insurance jobs move differently. Retail estimates are compared against two other roofers for a week or two; insurance files stall between adjuster, supplement and approval. A roofing CRM has to track both paths with a status, an owner and a next action, and keep follow-up running through storm season when hundreds of leads land in two weeks.",
     "Mobile matters because the rep is on the roof, not at a desk — but a great mobile app that nobody uses to log the next action is just a photo album. Ask in the demo how the office sees every estimate over seven days old with no reply."]),
   ("The six options", None),
   ("Why inspections never turn into contracts", [
     "The homeowner said they would think about it. Three other roofers knocked. Insurance files sat between adjuster and approval with nobody owning the next touch. Storm season outran the office, and follow-up depended on memory. Every tool above stores the estimate; none of them assigns a person to chase it.",
     WHY_TOOLS_DONT_CLOSE]),
   ("How to choose", [
     "Insurance-heavy restoration companies usually land on AccuLynx or JobNimbus for their claim workflows and production boards. Retail-focused roofers that sell in the home look at Leap and Roofr for proposals and measurements. Companies that also run service divisions may already have ServiceTitan; small roofers with mixed exterior work often start on Jobber. Then decide who owns follow-up on aging estimates — the CRM will not.",
     reframe("roofing-crm", "roofing companies")]),
  ],
  table=[
   ("AccuLynx", "Insurance-restoration and mid-size roofing companies", "Roofing-specific project management, claims workflows, production tracking and supplier integrations", "Sales follow-up depends on how reps use the pipeline; heavier setup"),
   ("JobNimbus", "Roofers wanting CRM plus project management", "Boards, automations, mobile app and integrations for roofing workflows", "Automation power requires real configuration and an owner"),
   ("Roofr", "Retail roofers selling with measurements and proposals", "Aerial measurements, instant estimates, proposals and a lightweight CRM", "Lighter on production management for large volume"),
   ("Leap", "In-home retail sales teams", "Digital proposals, financing and contracts on the tablet; project workflows", "Less suited to insurance-heavy operations"),
   ("ServiceTitan", "Companies running roofing alongside home-service divisions", "Full platform with dispatch, pricebook, financing and marketing", "Expensive and general-purpose for roofing-only companies"),
   ("Jobber", "Small roofing and exterior companies", "Simple quoting, scheduling, invoicing and quote follow-up reminders", "Not roofing-specific; no insurance workflow"),
  ],
  faqs=[
   ("What CRM do most roofing contractors actually use?", "AccuLynx and JobNimbus dominate insurance-restoration roofing; Roofr and Leap are common with retail-focused sellers; smaller exterior companies often use Jobber."),
   ("Which roofing CRM has the best mobile app?", "JobNimbus, AccuLynx and Roofr all invest heavily in mobile. The better question is whether your reps will log the next action in it — the app is only as good as that habit."),
   ("How much does a roofing CRM cost per month?", "From modest per-user fees for lightweight tools to substantial per-seat and implementation costs for full platforms. Get current quotes; pricing changes frequently."),
   ("Does PeakReach replace AccuLynx or JobNimbus?", "No. PeakReach connects and manages the follow-up workflow around your approved system of record whenever the data is usable, and reports verified activity weekly."),
  ]),

 dict(
  slug="hvac-estimating-software", kw="HVAC estimating software", kicker="HVAC · Software Gap", icon="calculator",
  trade_slug="hvac-crm", trade_label="HVAC companies",
  title="HVAC Estimating Software: 5 Options — and the Step After the Quote",
  desc="ServiceTitan, Housecall Pro, FieldEdge, Jobber and Service Fusion for HVAC proposals — what each does well, and why the quote is only half the sale.",
  h1="HVAC estimating software: five options, and the step after the quote",
  intro="Estimating software gets a good-better-best proposal in front of the homeowner in minutes. Then it stops",
  lead="HVAC estimating software has gotten very good: flat-rate pricebooks, good-better-best proposals, financing on the tablet, e-signature. The replacement quote that used to take an evening now takes ten minutes in the kitchen. What has not changed is what happens after the comfort advisor leaves — and that is where most of the revenue still leaks.",
  sections=[
   ("What HVAC estimating software actually does", [
     "The job of estimating software is speed and consistency: pull equipment and labor from a pricebook, present options with clear pricing, attach financing, capture a signature. Done well, it raises average ticket and removes math errors. Judge any option on pricebook flexibility, proposal presentation, financing integration and how cleanly the quote flows into the job once it is sold."]),
   ("Five common options", None),
   ("The step after the quote", [
     "A replacement proposal that is not signed in the home goes into comparison. The homeowner gets two more bids; the advisor is on the next appointment; the office is dispatching. If no one owns the follow-up, the proposal that looked great on the tablet dies in the inbox. Estimating software does not fix this because it was never its job — its job ends when the proposal is delivered.",
     "The fix is a follow-up system that treats every unsigned proposal as an open pipeline item: a status, an owner, scheduled touches by text and email that stop the moment the homeowner replies, and a weekly view of what is still aging. That is a different tool and a different discipline from estimating — and it is where the recovered revenue actually comes from."]),
   ("How to choose", [
     "Small residential shops get fast value from Housecall Pro or Jobber proposals. Companies that live in QuickBooks and sell agreements lean FieldEdge. Multi-truck companies wanting pricebook depth, financing and attribution pay for ServiceTitan. Service Fusion suits established shops that want flat pricing. Then close the gap after the quote, because none of these will chase the unsigned proposal for you.",
     reframe("hvac-crm", "HVAC companies").replace("See what that looks like", "Read about the CRM side")]),
  ],
  table=[
   ("ServiceTitan", "Multi-truck residential HVAC", "Pricebook Pro, good-better-best proposals, financing, e-signature", "Cost; follow-up ownership still lands in your office"),
   ("Housecall Pro", "Residential HVAC under roughly $3M", "Sales proposals with options, online approval, quick setup", "Lighter pricebook management"),
   ("FieldEdge", "HVAC shops centered on QuickBooks and agreements", "Flat-rate pricebook, agreements, QuickBooks integration", "Proposal presentation is functional rather than sales-driven"),
   ("Jobber", "Small HVAC companies with mixed home-service work", "Fast quotes with optional line items and quote follow-up reminders", "Less HVAC-specific pricebook depth"),
   ("Service Fusion", "Established shops with several technicians", "Estimates, invoicing and dispatch with flat monthly pricing", "Dated interface for some users"),
  ],
  faqs=[
   ("What is the best HVAC estimating software for a small company?", "Housecall Pro and Jobber are the fastest to deploy for residential shops; FieldEdge fits QuickBooks-centered companies; ServiceTitan is the enterprise option. All of them stop when the proposal is delivered."),
   ("Does HVAC estimating software follow up on unsigned proposals?", "Some send reminders. Recovering unsigned replacement quotes needs a cadence configured for that quote type, an owner, and stop rules when the homeowner replies — a follow-up system, not an estimating feature."),
   ("What is good-better-best pricing in HVAC?", "Presenting three equipment and service tiers on one proposal so the homeowner chooses a level rather than a yes/no. Most modern estimating tools support it."),
   ("Does PeakReach do HVAC estimating?", "No. PeakReach installs and operates the follow-up and revenue-recovery system around the estimating tool you already use."),
  ]),

 dict(
  slug="landscaping-estimating-software", kw="landscaping estimating software", kicker="Landscaping · Software Gap", icon="ruler",
  trade_slug="landscaping-crm", trade_label="landscaping companies",
  title="Landscaping Estimating Software: 6 Options and the Follow-Up Gap",
  desc="LMN, Aspire, SingleOps, Service Autopilot, Jobber and Arborgold for landscape estimating — who fits each, and why spring quotes still go quiet.",
  h1="Landscaping estimating software: six options, and the follow-up gap",
  intro="A fast, accurate landscape estimate is a competitive advantage — until it sits unanswered for two weeks",
  lead="Landscape estimating software solves a real problem: production rates, material takeoffs, budget-based pricing and a professional proposal in a fraction of the time. But spring proves every year that a great estimate delivered fast still goes quiet. Here is what each common tool does well, and the gap between the estimate and the signed job.",
  sections=[
   ("What landscaping estimating software actually does", [
     "The core is pricing discipline: build estimates from production rates and material costs against your overhead and profit targets, so the number is right before it goes out. Takeoff and measuring features speed up hardscape and installation bids. Proposal templates keep presentation consistent across estimators. Judge options on how well they model your services — maintenance, enhancements, design-build, tree care — and how cleanly a sold estimate becomes a scheduled job."]),
   ("Six common options", None),
   ("The follow-up gap", [
     "Forty estimates go out in two weeks of spring. The office is buried. Maintenance proposals stall with no decision; enhancement quotes get compared with the neighbor’s landscaper; last year’s mulch customers never hear from you again. Estimating software delivered the number quickly and accurately — and then had nothing to say about whether anyone followed up.",
     "Closing that gap takes a separate system: every estimate tracked with an owner, scheduled follow-up that stops when the customer replies, seasonal reactivation for past customers, and exceptions routed to a person. It is not an estimating feature and it will not appear in a takeoff tool’s roadmap — it is an operating discipline someone has to run."]),
   ("How to choose", [
     "Owners who want estimating and budgeting discipline start with LMN. Commercial and design-build companies past $3M consider Aspire. Tree care and mixed green-industry work fits SingleOps or Arborgold. Maintenance-heavy lawn care companies estimate well inside Service Autopilot. Small residential companies get fast value from Jobber. Whatever you choose, assign follow-up before spring — the software will not.",
     reframe("landscaping-crm", "landscaping companies").replace("See what that looks like", "Read about the CRM side")]),
  ],
  table=[
   ("LMN", "Landscapers who want budget-based pricing discipline", "Budgeting, production-rate estimating, time tracking and owner training", "Follow-up and CRM are secondary to estimating"),
   ("Aspire", "Commercial and design-build landscaping, typically $3M+", "Estimating tied to job costing, crew scheduling and reporting", "Heavy implementation; not a sales follow-up tool"),
   ("SingleOps", "Tree care, landscaping and green-industry companies", "Estimating, proposals, CRM and scheduling built for green-industry jobs", "Smaller ecosystem"),
   ("Service Autopilot", "Lawn care and maintenance companies", "Estimating for recurring services, routing, automations and billing", "Automations need configuration and an owner"),
   ("Jobber", "Small residential landscaping companies", "Fast quotes, optional line items, scheduling and invoicing", "Less production-rate depth for complex bids"),
   ("Arborgold", "Tree care and landscape companies", "Estimating, proposals, scheduling and crew management", "Less known outside tree care"),
  ],
  faqs=[
   ("What is the best estimating software for a landscaping company?", "LMN for pricing discipline, Aspire for larger commercial and design-build, SingleOps or Arborgold for tree care, Service Autopilot for maintenance programs, Jobber for small residential. All of them stop when the estimate is delivered."),
   ("Does landscape estimating software do takeoffs?", "Several include or integrate measuring and takeoff features for hardscape and installation bids; verify with each vendor for your bid types."),
   ("How do landscapers follow up on estimates in spring?", "The ones who do it consistently run a system: every estimate tracked with an owner, scheduled follow-up that stops on reply, and a weekly view of aging quotes. Effort alone does not survive spring."),
   ("Does PeakReach replace my landscaping estimating software?", "No. PeakReach installs and operates the Revenue Recovery System around the estimating and customer tools you already use."),
  ]),

 dict(
  slug="landscaping-business-software", kw="landscaping business software", kicker="Landscaping · Software Gap", icon="layers",
  trade_slug="landscaping-crm", trade_label="landscaping companies",
  title="Landscaping Business Software (2026): What to Buy — and What It Won’t Do",
  desc="Landscaping management, scheduling, estimating and CRM software compared — Jobber, Service Autopilot, Aspire, LMN, SingleOps — and the job none of them owns.",
  h1="Landscaping business software in 2026: what to buy, and what it won’t do",
  intro="Scheduling, estimating, routing, invoicing, CRM — the category is crowded because the business has five jobs. Buy for the one that leaks the most money",
  lead="“Landscaping business software” covers five different jobs: estimating, scheduling and routing, crew and time tracking, invoicing, and customer management. Vendors bundle them differently, which is why comparisons get confusing. This guide sorts the common options by the job they do best — and names the job none of them owns.",
  sections=[
   ("The five jobs landscaping software does", [
     "Estimating prices the work correctly. Scheduling and routing put crews where they should be with the fewest miles. Crew and time tracking tell you what a job actually cost. Invoicing and recurring billing get you paid on schedule. Customer management holds the record and the history. Most tools do two or three of these well and the rest adequately; buying decisions go wrong when a company picks a platform for the job it does adequately.",
     "Start with the leak. If estimates take too long, buy for estimating. If routes are inefficient and crews idle, buy for scheduling. If cash is late, buy for billing. If quoted work goes quiet, that is a follow-up problem — and it is the one no platform in this list actually owns."]),
   ("Common options by strength", None),
   ("The job no platform owns", [
     "Every option above can send a reminder about an open estimate. None of them decides who owns follow-up, sets the cadence for your services, watches the replies, or reports each week on what ran and what came back. That work is operating, not software — and it is where landscaping companies lose the most revenue after the quote.",
     WHY_TOOLS_DONT_CLOSE]),
   ("How to choose", [
     "Under about $1M residential, Jobber or Service Autopilot run the whole business; Service Autopilot pulls ahead for route-dense maintenance and lawn care programs. Growing companies that need estimating and budgeting discipline add LMN. Past $3M with commercial and design-build work, Aspire’s job costing pays for its implementation. Tree care and mixed green-industry companies look at SingleOps. Then assign the fifth job — follow-up — to a person or a managed system.",
     reframe("landscaping-crm", "landscaping companies")]),
  ],
  table=[
   ("Jobber", "Residential landscaping under roughly $1–2M", "Quoting, scheduling, invoicing and client communication in one simple system", "Limited job costing and production-rate estimating"),
   ("Service Autopilot", "Lawn care and maintenance with route density", "Routing, recurring billing, automations, forms", "Configuration-heavy; needs an owner"),
   ("LMN", "Owners who want budgeting and estimating discipline", "Budget-based estimating, time tracking, owner education", "Lighter CRM and scheduling"),
   ("Aspire", "Commercial and design-build, typically $3M+", "Estimating, job costing, crew management and reporting", "Heavy implementation and cost"),
   ("SingleOps", "Tree care and green-industry companies", "Estimating, CRM, scheduling for green-industry jobs", "Smaller ecosystem"),
   ("Yardbook", "Very small lawn care operations", "Free or low-cost scheduling, invoicing and customer records", "Limited depth as the company grows"),
  ],
  faqs=[
   ("What software do most landscaping companies use?", "Small residential companies most often run Jobber or Service Autopilot; maintenance-heavy lawn care leans Service Autopilot; larger commercial and design-build companies use Aspire; LMN is common for estimating discipline."),
   ("What is the difference between landscaping CRM and landscaping management software?", "Management software runs operations — scheduling, routing, billing. A CRM tracks customers and open estimates. Many platforms include both, but the follow-up on open estimates still needs an owner."),
   ("Is there free landscaping business software?", "Yardbook offers a free tier suited to very small operations. Most companies outgrow free tools once routing, estimating and billing volume increase."),
   ("Does PeakReach sell landscaping business software?", "No. PeakReach installs and operates a managed Revenue Recovery System around the tools you already run, so quoted work stops going quiet."),
  ]),
]

# ---------------------------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------------------------
NAV = '''<header class="nav"><div class="wrap">
  <a class="logo" href="/"><img src="assets/mark-color.png" alt="PeakReach" width="42" height="42"><span class="txt"><b>PeakReach</b><span>MANAGED SYSTEMS</span></span></a>
  <nav class="links">
    <a href="/#system">The System</a>
    <a href="/standard">The Standard</a>
    <a href="/pricing">Pricing</a>
    <a class="active" href="/resources">Resources</a>
    <a href="/contact">Contact</a>
    <a class="btn btn-ghost" href="https://app.peakreachms.com" target="_blank" rel="noopener" style="padding:11px 18px">Login</a>
    <a class="btn btn-teal" href="/revenue-leak-audit" style="padding:11px 20px">Revenue Leak Audit</a>
  </nav>
  <button class="menu-btn" data-menu aria-label="Menu">☰</button>
</div></header>'''

ORG = ('{"@context":"https://schema.org","@type":"Organization","name":"PeakReach Managed Systems","legalName":"PeakReach Marketing Solutions LLC",'
       '"url":"https://www.peakreachms.com/","logo":"https://www.peakreachms.com/assets/mark-color.png","email":"info@peakreachms.com",'
       '"slogan":"Built by operators. Run by systems.","description":"PeakReach installs and manages the systems that make revenue, accountability, and operations visible, repeatable, and less dependent on the owner.",'
       '"address":{"@type":"PostalAddress","addressLocality":"Sanford","addressRegion":"NC","addressCountry":"US"},"areaServed":"United States"}')

def table_html(rows):
    head = "<tr><th>Tool</th><th>Best fit</th><th>What it does well</th><th>Where quotes still die</th></tr>"
    body = "\n".join(f"<tr><td><strong>{e(t)}</strong></td><td>{e(f)}</td><td>{e(w)}</td><td>{e(d)}</td></tr>" for t, f, w, d in rows)
    return f'<div class="tablewrap"><table class="cmp">{head}\n{body}</table></div><p class="fine">Positioning summarized from vendor materials and operator experience as of {TODAY[:7]}. Features and pricing change; confirm with each vendor. No vendor paid for placement.</p>'

def page(a):
    url = HOST + "/" + a["slug"]
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in a["faqs"]]}, ensure_ascii=False)
    crumbs = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": HOST + "/"},
        {"@type": "ListItem", "position": 2, "name": "Resources", "item": HOST + "/resources"},
        {"@type": "ListItem", "position": 3, "name": a["h1"], "item": url}]}, ensure_ascii=False)
    body = []
    for h2, paras in a["sections"]:
        body.append(f"  <h2>{e(h2)}</h2>")
        if paras is None:
            body.append("  " + table_html(a["table"]))
            body.append(f'''  <div class="callout"><h3>Not sure which one fits — or whether the one you have is actually being run?</h3><p>A 20–30 minute operator-led Revenue Leak Audit looks at what happens to your quotes after they go out and names up to three observable leaks. Complimentary for qualified {e(a["trade_label"])}. No software to buy.</p><a class="btn btn-teal" href="/revenue-leak-audit" style="padding:11px 20px">Apply for a Revenue Leak Audit →</a></div>''')
        else:
            body.extend(f"  <p>{p}</p>" for p in paras)   # paragraphs may carry trusted inline HTML (links/em)
    faqs = "\n".join(f'    <div class="qa"><button>{e(q)}<span class="plus">+</span></button><div class="a"><p>{e(ans)}</p></div></div>' for q, ans in a["faqs"])
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(a["title"])}</title>
<link rel="canonical" href="{url}">
<meta name="description" content="{e(a["desc"])}">
<meta name="theme-color" content="#0A2440">
<link rel="icon" href="assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;450;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css?v=20260908">
<meta property="og:type" content="article">
<meta property="og:site_name" content="PeakReach Managed Systems">
<meta property="og:title" content="{e(a["title"])}">
<meta property="og:description" content="{e(a["desc"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://www.peakreachms.com/assets/og-default.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(a["title"])}">
<meta name="twitter:description" content="{e(a["desc"])}">
<meta name="twitter:image" content="https://www.peakreachms.com/assets/og-default.png">
<script type="application/ld+json">
{ORG}
</script>
<script type="application/ld+json">
{faq_ld}
</script>
<script type="application/ld+json">
{crumbs}
</script>
</head>
<body>

{NAV}

<section class="pagehero"><div class="wrap">
  <span class="kicker on-dark"><span class="num"><i data-lucide="{a["icon"]}"></i></span>Resources · {e(a["kicker"])}</span>
  <h1>{e(a["h1"])}</h1>
  <p>{e(a["lead"])}</p>
</div></section>

<section class="section"><div class="wrap"><div class="prose" style="margin:0 auto">
  <h2 class="intro-title">{e(a["intro"])}</h2>
{chr(10).join(body)}
</div></div></section>

<section class="section band"><div class="wrap">
  <div class="center"><span class="kicker"><span class="num">?</span>FAQ</span><h2 class="big">Common questions</h2></div>
  <div class="faq">
{faqs}
  </div>
  <p class="center" style="margin-top:32px;font-size:14px;color:var(--muted)">Related: <a href="/{a["trade_slug"]}" style="color:var(--blue)">{e(a["trade_label"][0].upper()+a["trade_label"][1:])} — the Revenue Recovery System</a> · <a href="/estimate-follow-up-system" style="color:var(--blue)">How to follow up on estimates</a> · <a href="/resources" style="color:var(--blue)">All resources</a></p>
</div></section>

<section class="section"><div class="wrap">
  <div class="final">
    <h2>Find out what happens to your quotes after they go out.</h2>
    <p class="lead" style="margin:16px auto 0">A 20–30 minute operator-led Revenue Leak Audit, plus a one-page Revenue Leak Snapshot. No software to buy.</p>
    <div class="cta-row" style="justify-content:center;margin-top:28px;position:relative">
      <a class="btn btn-teal" href="/revenue-leak-audit">Apply for a Revenue Leak Audit</a>
      <a class="btn btn-ghost-d" href="/{a["trade_slug"]}">See the system for {e(a["trade_label"])}</a>
    </div>
  </div>
</div></section>

<footer></footer>
<script src="https://unpkg.com/lucide@0.460.0/dist/umd/lucide.min.js"></script>
<script src="app.js"></script>
</body>
</html>
'''

if __name__ == "__main__":
    for a in ARTICLES:
        assert len(a["title"]) <= 72, (a["slug"], len(a["title"]))
        assert len(a["desc"]) <= 160, (a["slug"], len(a["desc"]))
        open(a["slug"] + ".html", "w", encoding="utf-8").write(normalize_html(a["slug"], page(a)))
        print("wrote", a["slug"] + ".html")
