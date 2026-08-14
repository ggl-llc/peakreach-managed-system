(function(){
  document.addEventListener('click', function(e){
    if (e.target.closest('[data-menu]')) { var n=document.querySelector('nav.links'); if(n) n.classList.toggle('open'); return; }
    var link=e.target.closest('nav.links a'); if(link){ var n2=document.querySelector('nav.links'); if(n2) n2.classList.remove('open'); }
    var q=e.target.closest('.qa button');
    if(q){ var qa=q.parentElement, a=qa.querySelector('.a'), open=qa.classList.contains('open');
      document.querySelectorAll('.qa').forEach(function(x){x.classList.remove('open'); x.querySelector('.a').style.maxHeight=null;});
      if(!open){ qa.classList.add('open'); a.style.maxHeight=a.scrollHeight+'px'; } }
  });
  window.addEventListener('DOMContentLoaded', function(){
    var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in'); io.unobserve(en.target);}})},{threshold:.12});
    document.querySelectorAll('.reveal').forEach(function(el){io.observe(el);});
    document.querySelectorAll('form[data-demo]').forEach(function(f){ f.addEventListener('submit', function(ev){ ev.preventDefault(); alert('Thank you! This form is not connected yet — we will wire it to the CRM.'); }); });
    if (window.lucide) window.lucide.createIcons();
  });
})();
