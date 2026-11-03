"""Read authorized PUBLIC personal LinkedIn posts, then render static news.

Credentials come exclusively from environment variables. No browser scraping.
Provider/network failures preserve the last successful public snapshot.
"""
from pathlib import Path
from datetime import datetime,timezone
from urllib.request import Request,urlopen
from urllib.parse import urlencode,quote
import json,os,re,sys
from render_news import render

ROOT=Path(__file__).resolve().parents[1]
def normalize(posts,author):
 result=[]
 for post in posts:
  if post.get('author')!=author or post.get('visibility')!='PUBLIC' or post.get('lifecycleState')!='PUBLISHED':continue
  if post.get('distribution',{}).get('feedDistribution')!='MAIN_FEED':continue
  urn=post.get('id','')
  if not re.fullmatch(r'urn:li:(share|ugcPost):\d+',urn):continue
  body=post.get('commentary','').strip()
  if not body:continue
  published=post.get('publishedAt')
  if not isinstance(published,(int,float)):continue
  date=datetime.fromtimestamp(published/1000,tz=timezone.utc).date().isoformat()
  title=body.splitlines()[0][:180]
  result.append({'id':urn,'date':date,'category':'LinkedIn','title':title,'text':body,'url':'https://www.linkedin.com/feed/update/'+quote(urn,safe=':'),'source':'LinkedIn','date_label':'Publication date'})
 return result
def sync(root=ROOT):
 token=os.environ.get('LINKEDIN_ACCESS_TOKEN');author=os.environ.get('LINKEDIN_AUTHOR_URN');version=os.environ.get('LINKEDIN_API_VERSION')
 if not token or not author or not version:raise ValueError('Configure LINKEDIN_ACCESS_TOKEN, LINKEDIN_AUTHOR_URN and LINKEDIN_API_VERSION before enabling sync.')
 if not re.fullmatch(r'urn:li:person:[A-Za-z0-9_-]+',author):raise ValueError('A verified personal author URN is required.')
 if not re.fullmatch(r'\d{6}',version):raise ValueError('LinkedIn API version must be YYYYMM.')
 all_posts=[];start=0;complete=False
 for _ in range(20):
  url='https://api.linkedin.com/rest/posts?'+urlencode({'q':'author','author':author,'count':100,'start':start,'sortBy':'LAST_MODIFIED'})
  req=Request(url,headers={'Authorization':'Bearer '+token,'Linkedin-Version':version,'X-Restli-Protocol-Version':'2.0.0','X-RestLi-Method':'FINDER'})
  with urlopen(req,timeout=45) as response:data=json.load(response)
  if not isinstance(data.get('elements'),list):raise ValueError('Unexpected LinkedIn response; preserving previous news.')
  page=data['elements'];all_posts.extend(page)
  if not any(link.get('rel')=='next' for link in data.get('paging',{}).get('links',[])):complete=True;break
  start=data.get('paging',{}).get('start',start)+data.get('paging',{}).get('count',100)
 if not complete:raise ValueError('Import exceeded page limit; preserving previous news.')
 current=json.loads((root/'data/news.json').read_text(encoding='utf-8'))
 curated=[x for x in current['items'] if not x['id'].startswith(('urn:li:share:','urn:li:ugcPost:'))]
 # Replace only after a complete retrieval, so deleted/non-public posts are removed.
 imported=normalize(all_posts,author)
 unique={x['id']:x for x in curated+imported}
 payload={'items':sorted(unique.values(),key=lambda x:x['date'],reverse=True),'sync':{'status':'ok','last_success':datetime.now(timezone.utc).isoformat()}}
 target=root/'data/news.json';temporary=target.with_suffix('.tmp');temporary.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8');temporary.replace(target)
 render(root)
 return len(imported)
if __name__=='__main__':
 try:print(f'Synced {sync()} authorized public LinkedIn posts.')
 except Exception as error:
  # Avoid printing token-bearing request objects or provider response bodies.
  print('LinkedIn news sync failed: '+type(error).__name__+'. Previous news preserved.',file=sys.stderr)
  sys.exit(1)
