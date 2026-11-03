"""Render public news as static HTML. No runtime API key or fetch required."""
from pathlib import Path
import html,json,re

ROOT=Path(__file__).resolve().parents[1]
def esc(value):return html.escape(str(value),quote=True)
def render(root=ROOT):
 data=json.loads((root/'data/news.json').read_text(encoding='utf-8'))
 items=sorted(data['items'],key=lambda x:x['date'],reverse=True)
 cards=[]
 for item in items:
  if not item['url'].startswith('https://'):raise ValueError('News URL must use HTTPS')
  cards.append(f'''<article class="news-card" data-category="{esc(item['category'])}"><span class="news-tag">{esc(item['category'])}</span><time>{esc(item['date'])}</time><h2 data-en="{esc(item['title'])}" data-de="{esc(item.get('title_de',item['title']))}">{esc(item['title'])}</h2><p data-en="{esc(item['text'])}" data-de="{esc(item.get('text_de',item['text']))}">{esc(item['text'])}</p><p class="news-meta">{esc(item.get('date_label','Publication date'))} · {esc(item['source'])}</p><a href="{esc(item['url'])}" rel="noopener noreferrer">View original ↗</a></article>''')
 categories=sorted({x['category'] for x in items})
 options=''.join(f'<option>{esc(c)}</option>' for c in categories)
 page=(root/'scripts/news-template.html').read_text(encoding='utf-8').replace('__NEWS_CARDS__',''.join(cards))
 (root/'news.html').write_text(page,encoding='utf-8')
 home=root/'index.html'
 if home.exists():
  content=home.read_text(encoding='utf-8')
  latest=''.join(cards[:3])
  content=re.sub(r'<!-- NEWS_START -->.*?<!-- NEWS_END -->',lambda _: '<!-- NEWS_START -->'+latest+'<!-- NEWS_END -->',content,count=1,flags=re.S)
  home.write_text(content,encoding='utf-8')
 return len(items)
if __name__=='__main__':print(f'Rendered {render()} public news items.')
