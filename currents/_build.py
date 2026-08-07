"""
Silver Current Press — Currents build script.

Reads currents/_essays.json, generates:
  1. One HTML page per essay in currents/<slug>.html (from _essay-template.html)
  2. Rewrites the outer currents.html as a browsable index of essay cards

Run this whenever a new essay is added to _essays.json.
"""
import json
import re
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CURRENTS_DIR = ROOT / "currents"
TEMPLATE_PATH = CURRENTS_DIR / "_essay-template.html"
ESSAYS_PATH = CURRENTS_DIR / "_essays.json"
INDEX_PATH = ROOT / "currents.html"

# ---- Load ----
essays = json.loads(ESSAYS_PATH.read_text())["essays"]
template = TEMPLATE_PATH.read_text()

# Sort essays newest first by date_iso
essays.sort(key=lambda e: e["date_iso"], reverse=True)

# ---- Generate individual essay pages ----
for essay in essays:
    html = template
    for key in ["slug", "title", "subtitle", "author", "date_iso", "date_human",
                "issue_label", "description", "keywords"]:
        html = html.replace(f"__{key.upper()}__", essay[key])
    html = html.replace("__BODY__", essay["body"])

    out_path = CURRENTS_DIR / f"{essay['slug']}.html"
    out_path.write_text(html)
    print(f"Wrote {out_path.relative_to(ROOT)}")

# ---- Build the index cards ----
cards = []
for essay in essays:
    cards.append(f'''
  <article class="entry entry-card reveal">
    <p class="eyebrow">{essay["issue_label"]}</p>
    <h3 class="entry-title"><a href="currents/{essay["slug"]}.html" class="entry-title-link">{essay["title"]}</a></h3>
    <p class="attribution">By {essay["author"]} &middot; {essay["date_human"]}</p>
    <div class="body">
      <p>{essay["excerpt"]}</p>
    </div>
    <p class="entry-more"><a href="currents/{essay["slug"]}.html" class="gilt-link">Read the full essay &rarr;</a></p>
  </article>

  <svg class="chevron-divider" viewBox="0 0 60 26" fill="none" stroke="currentColor" stroke-width="1" stroke-linejoin="miter" aria-hidden="true">
    <polyline points="6,4 30,22 54,4"/>
    <polyline points="14,4 30,16 46,4" opacity="0.7"/>
    <polyline points="22,4 30,10 38,4" opacity="0.45"/>
  </svg>
''')

cards_html = "\n".join(cards)

# ---- Rewrite currents.html: replace whatever entries block is there with cards_html ----
index = INDEX_PATH.read_text()

# Match either the original inline entry format OR the previously-generated card format,
# up to (but not including) the contact-closing paragraph.
# Pattern: one or more <article class="entry ..."> blocks, each optionally followed by <svg class="chevron-divider"...>
pattern = re.compile(
    r'(<article class="entry(?:\s+entry-card)?\s+reveal">.*?<svg class="chevron-divider".*?</svg>\s*)+(?=<p class="contact-closing")',
    re.DOTALL
)

if not pattern.search(index):
    raise SystemExit("ERROR: could not find existing entry block to replace in currents.html. Aborting.")

new_index = pattern.sub(cards_html.strip() + "\n\n  ", index)

# Also update the intro to reflect that essays now have their own pages
INDEX_PATH.write_text(new_index)
print(f"\nWrote {INDEX_PATH.relative_to(ROOT)} with {len(essays)} essay cards")
