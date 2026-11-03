# Agnes Poks — academic portfolio

Bilingual static portfolio, English by default. Includes Research, Projects, Funding & Awards, Publications, Teaching, News and Lab Notes.

## Local preview

Run `python -m http.server 8765` in this directory.

## Publishing

This redesign is supplied on a separate review branch. It does not change the live site until merged and deployed. The prepared portfolio workflow builds only pushes to `main` or explicit manual runs. GitHub Pages must be configured to use GitHub Actions when adopting this version.

## Content

- `funding.html`: individual cards for eight projects and one dissertation award, including aws First Incubator / TERESS.
- `content/notes/`: Lab Notes sources. See `LAB_NOTES.md` for authoring and publishing.
- `scripts/render_lab.py`: standard-library note renderer.
- `scripts/render_news.py`: static news renderer.
- `NEWS_SETUP.md`: authorised LinkedIn API setup. Synchronisation is inactive until explicitly configured.
- `sources.html` and `data/image-sources.json`: content and image provenance.

Private CVs, funding contracts, signatures, personal identifiers and confidential client material are not part of this source tree. Project grant ceilings do not represent personal cash payments. Paper figures and project photographs retain source attribution.
