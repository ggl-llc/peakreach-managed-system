/* PeakReach site JS — nav, FAQ accordion, reveal, and the single lead-capture handler for every form.
   Forms opt in with data-lead="<kind>" (+ optional data-source, data-event, data-success). Fields are read by name.
   Payload always includes: source, page, utm_* / gclid / referrer captured on first landing (sessionStorage). */
(function(){
  var WEBHOOK = "https://services.leadconnectorhq.com/hooks/PU3svlBW3x81ujPelNlV/webhook-trigger/3e6d4a05-cadc-4bf4-ac07-69c952c619c8";

  // --- attribution: remember first-touch params for the session -------------------------------------------
  function attribution(){
    var keys=["utm_source","utm_medium","utm_campaign","utm_term","utm_content","gclid","fbclid","msclkid"], out={}, store={};
    try { store = JSON.parse(sessionStorage.getItem("pr_attr")||"{}"); } catch(e){}
    var qs = new URLSearchParams(location.search), changed=false;
    keys.forEach(function(k){ var v=qs.get(k); if(v && !store[k]){ store[k]=v; changed=true; } });
    if(!store.landing_page){ store.landing_page=location.pathname; store.referrer=document.referrer||"direct"; changed=true; }
    if(changed){ try { sessionStorage.setItem("pr_attr", JSON.stringify(store)); } catch(e){} }
    keys.concat(["landing_page","referrer"]).forEach(function(k){ if(store[k]) out[k]=store[k]; });
    return out;
  }

  // --- lead submit ------------------------------------------------------------------------------------------
  function bindLead(form){
    var statusEl = form.querySelector("[data-status]"), btn = form.querySelector("button[type=submit]");
    var kind = form.getAttribute("data-lead") || "lead";
    var source = form.getAttribute("data-source") || ("Website - " + kind);
    var event = form.getAttribute("data-event") || (kind + "_form_success");
    var okMsg = form.getAttribute("data-success") || "Thanks — your request is in. We reply within one business day.";
    function say(msg){ if(!statusEl) return; statusEl.style.display="block"; statusEl.textContent=msg; }
    form.addEventListener("submit", function(e){
      e.preventDefault();
      var full = ((form.full_name && form.full_name.value) || "").trim().replace(/\s+/g," "), sp = full.indexOf(" ");
      var email = ((form.email && form.email.value) || "").trim();
      if(!full || !email || email.indexOf("@")<1){ say("Please add your name and a work email."); return; }
      var payload = { first_name: sp===-1?full:full.slice(0,sp), last_name: sp===-1?"":full.slice(sp+1), email: email,
                      source: source, form: kind, page: location.pathname, page_title: document.title, submitted_at: new Date().toISOString() };
      Array.prototype.forEach.call(form.elements, function(el){
        if(!el.name || el.name==="full_name" || el.name==="email") return;
        if(el.type==="checkbox") payload[el.name] = !!el.checked;
        else if(el.type!=="submit") payload[el.name] = (el.value||"").trim();
      });
      var attr = attribution(); for (var k in attr) payload[k]=attr[k];
      if(btn) btn.disabled=true; say("Sending…");
      fetch(WEBHOOK, { method:"POST", headers:{ "Content-Type":"application/json" }, body: JSON.stringify(payload) })
        .then(function(res){ if(!res.ok) throw new Error(res.status);
          form.reset(); say(okMsg);
          if(window.gtag){ gtag("event", event, { form: kind, page: location.pathname }); gtag("event", "generate_lead", { form: kind, currency:"USD", value: 0 }); }
          var next = form.getAttribute("data-next"); if(next){ setTimeout(function(){ location.href = next; }, 900); }
          if(btn) btn.disabled=false; })
        .catch(function(){ say("Something went wrong. Please email info@peakreachms.com and we will set it up."); if(btn) btn.disabled=false; });
    });
  }

  // --- nav / faq ---------------------------------------------------------------------------------------------
  document.addEventListener("click", function(e){
    if (e.target.closest("[data-menu]")) { var n=document.querySelector("nav.links"); if(n) n.classList.toggle("open"); return; }
    var link=e.target.closest("nav.links a"); if(link){ var n2=document.querySelector("nav.links"); if(n2) n2.classList.remove("open"); }
    var q=e.target.closest(".qa button");
    if(q){ var qa=q.parentElement, a=qa.querySelector(".a"), open=qa.classList.contains("open");
      document.querySelectorAll(".qa").forEach(function(x){x.classList.remove("open"); x.querySelector(".a").style.maxHeight=null;});
      if(!open){ qa.classList.add("open"); a.style.maxHeight=a.scrollHeight+"px"; } }
  });

  window.addEventListener("DOMContentLoaded", function(){
    attribution();
    var els=document.querySelectorAll(".reveal");
    if ("IntersectionObserver" in window && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
      var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add("in"); io.unobserve(en.target);}})},{threshold:.08, rootMargin:"0px 0px -5% 0px"});
      els.forEach(function(el){io.observe(el);});
    } else { els.forEach(function(el){el.classList.add("in");}); }
    document.querySelectorAll("form[data-lead]").forEach(bindLead);
    var mcta=document.querySelector(".mcta");
    if(mcta){ var onS=function(){ mcta.classList.toggle("show", window.scrollY>520); }; window.addEventListener("scroll", onS, {passive:true}); onS(); }
    if (window.lucide) window.lucide.createIcons();
  });
})();
