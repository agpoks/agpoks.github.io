"""Build Lab Notes with the Python standard library: python scripts/render_lab.py."""
from pathlib import Path
import html,json,re
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
def esc(value): return html.escape(str(value),quote=True)
def translated(block,tag='p'):
    text=block.get('text','');de=block.get('text_de',text)
    return f'<{tag} data-en="{esc(text)}" data-de="{esc(de)}">{esc(text)}</{tag}>'
def safe_url(value,media=False):
    value=str(value)
    if value.startswith('https://') and urlsplit(value).netloc:return esc(value)
    if media and re.match(r'^data:(image/(png|jpeg|webp|gif)|video/(mp4|webm));base64,[A-Za-z0-9+/=]+$',value):return value
    if re.match(r'^assets/[A-Za-z0-9_./-]+$',value) and '..' not in value:return esc(value)
    raise ValueError('Use an HTTPS URL or a file inside assets/.')
def render_block(block):
    kind=block['type']
    if kind in ['paragraph','heading']:return translated(block,'h2' if kind=='heading' else 'p')
    if kind=='code':return '<pre><code>'+esc(block.get('text',''))+'</code></pre>'
    if kind=='image':return f'<figure><img src="{safe_url(block["src"],True)}" alt="{esc(block.get("caption",""))}" loading="lazy"><figcaption>{esc(block.get("caption",""))}</figcaption></figure>'
    if kind=='video':return f'<figure><video controls preload="metadata" src="{safe_url(block["src"],True)}"></video><figcaption>{esc(block.get("caption",""))}</figcaption></figure>'
    if kind=='link':return f'<p><a href="{safe_url(block["url"])}" rel="noopener noreferrer">{esc(block.get("text","Open link"))} ↗</a></p>'
    if kind=='tool' and block.get('name')=='scalar-stability':return '''<div class="stability-tool"><label>Parameter a: <output id="scalar-value">0.8</output><input id="scalar-a" aria-label="Parameter a" type="range" min="-1.2" max="1.2" step="0.01" value="0.8"></label><p>x[k+1] = a x[k], x[0] = 1 · 30 steps</p><svg id="scalar-plot" viewBox="0 0 700 300" role="img" aria-label="State response over thirty discrete steps"></svg><p id="scalar-status" aria-live="polite"></p><button type="button" id="scalar-reset">Reset</button></div><script src="assets/stability.js"></script>'''
    raise ValueError('Unsupported content block: '+str(kind))
def render(root=ROOT):
    template=(root/'scripts/lab-template.html').read_text(encoding='utf-8')
    def page(title,body):return template.replace('__LAB_TITLE__',esc(title)+' — Dr. Agnes Poks').replace('__LAB_BODY__',body)
    posts=[];generated=set()
    for file in sorted((root/'content/notes').glob('*.json'),reverse=True):
        post=json.loads(file.read_text(encoding='utf-8'))
        if post.get('status')!='published':continue
        slug=post['slug']
        if not re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',slug):raise ValueError('Invalid slug')
        if post['category'] not in ['project','idea','tutorial','tool']:raise ValueError('Invalid category')
        body='<article class="lab-article"><a href="lab.html">← Lab Notes</a><p class="eyebrow">'+esc(post['category'])+' · '+esc(post.get('date',''))+'</p>'+translated({'text':post['title'],'text_de':post.get('title_de',post['title'])},'h1')+translated({'text':post['summary'],'text_de':post.get('summary_de',post['summary'])})+''.join(render_block(b) for b in post['blocks'])+'</article>'
        filename='note-'+slug+'.html';generated.add(filename)
        (root/filename).write_text('<!-- LAB_GENERATED -->\n'+page(post['title'],body),encoding='utf-8');posts.append(post)
    posts.sort(key=lambda post:({'project':0,'idea':1,'tutorial':2,'tool':3}[post['category']],post['slug']))
    cards=[]
    for post in posts:
        cover=f'<img src="{safe_url(post["cover"],True)}" alt="" loading="lazy">' if post.get('cover') else ''
        cards.append('<article class="lab-card" data-category="'+esc(post['category'])+'"><a href="note-'+esc(post['slug'])+'.html">'+cover+'<div><p class="eyebrow">'+esc(post['category'])+' · '+esc(post.get('date',''))+'</p>'+translated({'text':post['title'],'text_de':post.get('title_de',post['title'])},'h2')+translated({'text':post['summary'],'text_de':post.get('summary_de',post['summary'])})+'</div></a></article>')
    controls='<div class="lab-filters"><label>Search / Suche <input id="lab-search" type="search" aria-label="Search Lab Notes"></label><label>Category / Kategorie <select id="lab-category"><option value="all">All / Alle</option><option value="project">GitHub projects / GitHub-Projekte</option><option value="idea">Ideas / Ideen</option><option value="tutorial">Tutorials</option><option value="tool">Tools</option></select></label></div><p id="lab-count" class="small" aria-live="polite"></p>'
    body='<section class="lab-index"><p class="eyebrow">CODE · IDEAS · HOW-TO</p><h1>Lab Notes</h1>'+translated({'text':'A space for independent GitHub projects, ideas, tutorials and small interactive tools.','text_de':'Ein eigener Bereich für unabhängige GitHub-Projekte, Ideen, Tutorials und kleine interaktive Werkzeuge.'})+controls+'<div class="lab-grid">'+''.join(cards)+'</div><p id="lab-empty" hidden>No notes in this category yet. / Noch keine Beiträge in dieser Kategorie.</p><p class="author-link"><a href="write.html">Create a draft / Entwurf erstellen →</a></p></section><script src="assets/lab.js"></script>'
    (root/'lab.html').write_text(page('Lab Notes',body),encoding='utf-8')
    for file in root.glob('note-*.html'):
        if file.name not in generated and file.read_text(encoding='utf-8').startswith('<!-- LAB_GENERATED -->'):
            file.unlink()
    return len(posts)
if __name__=='__main__':print('Rendered',render(),'Lab Notes.')
