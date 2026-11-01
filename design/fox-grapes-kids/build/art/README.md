# Art slots (designer drop)
Drop the designer's watercolor files here, then run `python layout/build_book.py`.
- `cover.png`: front cover, 8.75x8.75in (8.5in plus 0.125in bleed), 300 ppi = 2625x2625 px.
- `title.png`: p1, same size as the cover. "for Immy" is set as text by the layout; do not bake it into the art.
- `spread-01.png` to `spread-15.png`: 17.25x8.75in (2:1 plus bleed), 300 ppi = 5175x2625 px. The left half is the even page.
- `CREDITS.md`: a line `Illustrator: NAME` sets the illustration credit on p1 and p2.
The .jpg, .jpeg, .tif and .tiff extensions are also accepted. Any missing slot falls back to a labelled vector PLACEHOLDER.
