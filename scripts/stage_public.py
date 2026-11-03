"""Stage visitor-facing files only; exclude draft sources and authoring scripts."""
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1]
def stage(root=ROOT,destination=None):
    target=Path(destination) if destination else root/'_public'
    target.mkdir(parents=True,exist_ok=True)
    for source in root.glob('*.html'):shutil.copy2(source,target/source.name)
    for name in ['publications.bib','publications.json','.nojekyll','LAB_NOTES.md']:
        if (root/name).exists():shutil.copy2(root/name,target/name)
    for name in ['assets','data']:shutil.copytree(root/name,target/name,dirs_exist_ok=True)
    return target
if __name__=='__main__':print(stage())
