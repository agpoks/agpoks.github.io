# Lab Notes: add a contribution

The site stays compatible with static GitHub Pages hosting. The author editor works in the browser and does not send files to a server.

1. Open `write.html`. Enter an English title and summary, and optionally German versions. Choose GitHub project, idea, tutorial or tool.
2. Add paragraphs, headings, code blocks, images, videos or HTTPS links. Rearrange blocks with the arrow buttons. Add captions and credits.
3. Export the JSON draft. Keep the original file to continue editing later with “Import draft”. Export does not publish anything.
4. To publish, select “Include on the public site” and export again. Upload that JSON file to `content/notes/` in the website repository. After the website files and workflow are installed, select **GitHub Actions** as the GitHub Pages source. The portfolio workflow then builds and deploys the site on a push to `main`. This workflow is prepared locally and has not been installed or activated on GitHub.
5. For a local preview, run `python scripts/render_lab.py` from the site folder and open the site through a local HTTP server.

Images and videos selected in the editor are embedded into the exported draft. Each file is limited to 20 MB. For larger videos, use a hosted HTTPS video link, or put the video in `assets/` and use its path in a video block. A YouTube or Vimeo page should be a link block, rather than the source of a native video player.

The two repository notes describe existing software. The plot-reading tutorial and scalar stability explorer are newly prepared educational content for review. They do not represent additional research achievements or experimental results.

To hide a post, change its `status` to `draft`. Rendering removes the page for that note. Removed source files also remove previously generated note pages on the next build. Draft sources are excluded from the website artifact, but files uploaded to a public GitHub repository remain publicly accessible there. Keep unpublished drafts on your computer. The editor does not save work automatically.

Example:

```json
{
  "slug": "my-new-idea",
  "title": "My new idea",
  "title_de": "Meine neue Idee",
  "category": "idea",
  "summary": "A short introduction.",
  "summary_de": "Eine kurze Einführung.",
  "date": "2026-11-03",
  "status": "draft",
  "blocks": [
    {"type": "paragraph", "text": "First paragraph.", "text_de": "Erster Absatz."},
    {"type": "image", "src": "assets/my-figure.webp", "caption": "Description and credit"},
    {"type": "video", "src": "assets/my-demo.mp4", "caption": "Demo video"},
    {"type": "link", "url": "https://github.com/agpoks", "text": "Code"}
  ]
}
```
