const translations=JSON.parse(document.getElementById('translations').textContent);
let language='en';
// English is the default on every visit; German is an explicit option.
function setLanguage(lang){
 language=lang==='de'?'de':'en';
 document.documentElement.lang=language;
 document.querySelectorAll('[data-i18n]').forEach(el=>{el.textContent=translations[el.dataset.i18n][language]});
 document.querySelectorAll('[data-lang]').forEach(el=>el.setAttribute('aria-pressed',String(el.dataset.lang===language)));
 document.title='Dr. Agnes Poks | TU Wien';
 updatePublications();
 updateProjects();
 updateMotionLabels();
}
document.querySelectorAll('[data-lang]').forEach(el=>el.addEventListener('click',()=>setLanguage(el.dataset.lang)));
function updatePublications(){
 if(!document.getElementById('publication-search')) return;
 const q=document.getElementById('publication-search').value.toLocaleLowerCase();
 const type=document.getElementById('publication-type').value;
 const papers=[...document.querySelectorAll('.paper')]; let visible=0;
 papers.forEach(el=>{el.hidden=!(el.textContent.toLocaleLowerCase().includes(q)&&(type==='all'||el.dataset.kind===type));if(!el.hidden)visible++});
 document.getElementById('pub-count').textContent=language==='de'?`${visible} von ${papers.length} bibliografischen Einträgen · keine Zitationskennzahl`:`${visible} of ${papers.length} bibliography records · not a citation metric`;
 document.getElementById('no-papers').hidden=visible!==0;
}
document.getElementById('publication-search')?.addEventListener('input',updatePublications);
document.getElementById('publication-type')?.addEventListener('change',updatePublications);
function updateProjects(){
 if(!document.getElementById('project-search'))return;
 const q=document.getElementById('project-search').value.toLowerCase();
 const topic=document.getElementById('project-topic').value;
 const role=document.getElementById('project-role').value;
 let visible=0;const projects=[...document.querySelectorAll('.project')];
 projects.forEach(el=>{el.hidden=!(el.textContent.toLowerCase().includes(q)&&(topic==='all'||el.dataset.topic===topic)&&(role==='all'||el.dataset.role===role));if(!el.hidden)visible++});
 document.querySelectorAll('.group-heading').forEach(heading=>{let next=heading.nextElementSibling;let shown=false;while(next&&!next.classList.contains('group-heading')){if(next.classList.contains('project')&&!next.hidden)shown=true;next=next.nextElementSibling}heading.hidden=!shown});
 document.getElementById('project-count').textContent=language==='de'?`${visible} von ${projects.length} Projekten`:`${visible} of ${projects.length} projects`;
 document.getElementById('no-projects').hidden=visible>0;
}
['project-search','project-topic','project-role'].forEach(id=>document.getElementById(id)?.addEventListener(id==='project-search'?'input':'change',updateProjects));
document.getElementById('reset-projects')?.addEventListener('click',()=>{document.getElementById('project-search').value='';document.getElementById('project-topic').value='all';document.getElementById('project-role').value='all';updateProjects()});
document.querySelectorAll('[data-topic-shortcut]').forEach(button=>button.addEventListener('click',()=>{document.getElementById('project-topic').value=button.dataset.topicShortcut;document.getElementById('project-search').value='';document.getElementById('project-role').value='all';updateProjects();document.getElementById('projects').scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'})}));
let motionPaused=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function updateMotionLabels(){
 document.documentElement.classList.toggle('motion-paused',motionPaused);
 document.querySelectorAll('.motion-toggle,#global-motion').forEach(b=>{b.setAttribute('aria-pressed',String(motionPaused));b.textContent=language==='de'?(motionPaused?'Animationen fortsetzen':'Animationen pausieren'):(motionPaused?'Resume animations':'Pause animations')});
}
document.querySelectorAll('.motion-toggle,#global-motion').forEach(b=>b.addEventListener('click',()=>{motionPaused=!motionPaused;updateMotionLabels()}));
setLanguage(language);
// Source figures open in a keyboard-accessible detail view.
const figureDialog=document.createElement('dialog');
figureDialog.className='figure-dialog';
figureDialog.innerHTML='<form method="dialog"><button aria-label="Close figure">×</button></form><img alt=""><p></p>';
document.body.append(figureDialog);
document.querySelectorAll('[data-figure]').forEach(button=>button.addEventListener('click',()=>{
 const image=figureDialog.querySelector('img');image.src=button.dataset.figure;
 const caption=button.classList.contains('secondary-figure-link')?button.dataset.caption:(button.closest('figure')?.querySelector('figcaption')?.textContent||button.dataset.caption||'');
 image.alt=caption;figureDialog.querySelector('p').textContent=caption;figureDialog.showModal();
}));
figureDialog.addEventListener('click',event=>{if(event.target===figureDialog)figureDialog.close()});

const requestedPublication=new URLSearchParams(window.location.search).get("search");if(requestedPublication&&document.getElementById("publication-search")){document.getElementById("publication-search").value=requestedPublication;updatePublications();}
