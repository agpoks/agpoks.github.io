const siteMenu=document.querySelector('.menu-button');
siteMenu?.addEventListener('click',()=>{const open=document.querySelector('.site-header').classList.toggle('menu-open');siteMenu.setAttribute('aria-expanded',String(open))});
function translateShell(lang){document.documentElement.lang=lang;document.querySelectorAll('[data-lang]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.lang===lang)));document.querySelectorAll('[data-en][data-de]').forEach(el=>{el.textContent=el.dataset[lang]});document.dispatchEvent(new CustomEvent('site-language-change'));}
document.querySelectorAll('[data-lang]').forEach(b=>b.addEventListener('click',()=>translateShell(b.dataset.lang)));
translateShell('en');

document.querySelector('#topic-type')?.addEventListener('change',e=>{document.querySelectorAll('[data-topic-kind]').forEach(card=>{card.hidden=e.target.value!=='all'&&card.dataset.topicKind!==e.target.value})});
