# Currents — Silver Current Press essay series

This folder holds the pieces that generate the Currents section of the site.

## How it works

- **`_essays.json`** — the manifest of all published essays. Each essay is one JSON object.
- **`_essay-template.html`** — the HTML template for individual essay pages.
- **`_build.py`** — the build script. Reads the manifest, writes one HTML page per essay, and rewrites the top-level `../currents.html` as a browsable index of essay cards.
- **`<slug>.html`** — the generated essay pages. Don't edit these directly; they are overwritten by every build.

## Adding a new essay

1. Open `_essays.json`.
2. Add a new object to the `essays` array. Copy the shape of an existing entry.
3. Fields:
   - `slug` — URL-safe kebab-case identifier (becomes the filename)
   - `title` — the essay's title
   - `subtitle` — one-line dek shown under the title on the essay page
   - `author` — usually `"James F. Mulhern"` or `"The Editors"`
   - `date_iso` — YYYY-MM-DD, drives sort order (newest first)
   - `date_human` — e.g. `"August 2026"`, shown in the byline
   - `issue_label` — e.g. `"Vol. I · No. III · MMXXVI"`
   - `description` — one-sentence meta description for search engines
   - `keywords` — comma-separated SEO keywords
   - `excerpt` — 2-4 sentences shown on the index page as a preview
   - `body` — the full essay as HTML. Wrap paragraphs in `<p>...</p>`. Use `&mdash;` for em dashes and `&ldquo;` / `&rdquo;` for curly quotes.
4. Run: `cd .. && python3 currents/_build.py`
5. Commit and push. Cloudflare Pages auto-deploys in ~90 seconds.

## Word-to-Currents pipeline (for James)

Send a `.docx` and I'll:
1. Convert to clean HTML with `pandoc`.
2. Wrap paragraphs, replace straight quotes with curly quotes.
3. Add the entry to `_essays.json`.
4. Run the build, commit, push, verify live.

You never touch the code.

## Directory layout

```
silvercurrentpress/
├── currents.html              ← generated index (do not hand-edit body cards)
├── currents/
│   ├── README.md              ← this file
│   ├── _essay-template.html   ← page template
│   ├── _essays.json           ← manifest
│   ├── _build.py              ← generator
│   └── <slug>.html            ← one file per essay (generated)
```
