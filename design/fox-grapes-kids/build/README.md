# Fern and the High Grapes: build (NOT YET INSTALLED)

**NOT YET INSTALLED / proof only.** This build has not been reviewed, installed, published, or sent to a printer. The art is vector PLACEHOLDER only; the final watercolor art is not yet produced.

- Design: `../DESIGN.md` (branch design/fox-grapes-kids @ 93bd8d16, approved by Martin, t424u).
- To build: `pip install reportlab && python3 layout/build_book.py`
- Outputs in `exports/`:
  - `fern-print-interior-8.75sq-bleed.pdf`: 32 pages, 8.75in square (8.5in trim + 0.125in bleed, trim marks in the bleed).
  - `fern-reading-8.5sq.pdf`: 32 trimmed pages.
  - `fern-reading-spreads.pdf`: 17 sheets (p1, spreads 1–15 = pp2–31, p32).
  - `preview/sheet-NN.png`: 40 dpi previews.
- Pagination matches DESIGN §5 exactly: p1 + 15 spreads + p32 = 32 pages. No deviation.
- Scripture (pp30–31) is read from `content/berea-verses.txt` (byte copy of `../scripture/berea-verses.txt`). Only the inline verse numbers are stripped. The result matches the DESIGN §7 BSB text exactly.
- Latin is omitted and there is no dedication. The added reconsideration and prayer are credited as new adaptation material on p32.
- Open items: copyright holder placeholder on p2; creator credits; printer spec, gutter, and binding are unverified; there is no cover yet; final art is needed.
- Write ladder: rung 1 qwen2.5-coder:7b and rung 2 qwen3-coder:30b drafts were not usable (see `layout/ladder/`); rung 3 basicCoder rewrite. Codex was not used.
