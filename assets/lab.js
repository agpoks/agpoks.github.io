function filterLab(){const q=document.getElementById('lab-search').value.toLowerCase(),category=document.getElementById('lab-category').value;let n=0;document.querySelectorAll('.lab-card').forEach(card=>{card.hidden=!(card.textContent.toLowerCase().includes(q)&&(category==='all'||card.dataset.category===category));if(!card.hidden)n++});document.getElementById('lab-count').textContent=n+(document.documentElement.lang==='de'?' Beiträge':' notes');document.getElementById('lab-empty').hidden=n>0;}
document.getElementById('lab-search').addEventListener('input',filterLab);
document.getElementById('lab-category').addEventListener('change',filterLab);
document.addEventListener('site-language-change',filterLab);
filterLab();
