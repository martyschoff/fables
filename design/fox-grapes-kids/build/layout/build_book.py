#!/usr/bin/env python3
"""Fern and the High Grapes: builds the 32-page interior (p1 + 15 spreads + p32).
Outputs: exports/fern-print-interior-8.75sq-bleed.pdf (8.5in trim + 0.125in bleed),
exports/fern-reading-8.5sq.pdf (trimmed single pages), exports/fern-reading-spreads.pdf.
Art is a vector PLACEHOLDER; final watercolor art is not yet produced."""
import re, random, pathlib
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import Color
from reportlab.lib.utils import simpleSplit

ROOT = pathlib.Path(__file__).resolve().parent.parent
TRIM, BLEED, SAFE = 8.5 * inch, 0.125 * inch, 0.5 * inch
CREAM = Color(.98, .95, .88); INK = Color(.18, .14, .12)
SKY = Color(.80, .89, .95, .55); HILL = Color(.45, .55, .70, .35)
GRASS = Color(.85, .73, .38, .45); LEAF = Color(.55, .66, .45, .45)
PLUM = Color(.45, .22, .45, .6); RUSSET = Color(.78, .36, .15, .75)
WOOD = Color(.55, .40, .28, .7); CREEK = Color(.45, .65, .80, .5)

def story():
    pages = {}
    for line in (ROOT / "content/story.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"- \*\*p(\d+):\*\* (.+)", line)
        if m: pages[int(m.group(1))] = m.group(2)
    assert sorted(pages) == list(range(4, 30)), sorted(pages)
    return pages

def scripture():
    """Exact BSB text from berea-verses.txt; only the inline verse numbers are removed."""
    txt = (ROOT / "content/berea-verses.txt").read_text(encoding="utf-8")
    out = {}
    for ref, key in (("Galatians 5:22-23", "gal"), ("Philippians 4:11-12", "phil")):
        body = txt.split(ref, 1)[1].splitlines()[1]
        out[key] = (ref, re.sub(r"(^| )\d+ ", r"\1", body).strip())
    return out

SPREAD_BEATS = {1: "quiet farm lane", 2: "vineyard reveal; grapes out of reach", 3: "robin; first jump",
 4: "repeated attempts", 5: "big jump; soft landing", 6: "resting below the grapes", 7: "sour-grapes claim",
 8: "pause; backward glance", 9: "honest admission", 10: "prayer beneath the vine", 11: "calm look up",
 12: "toward the creek", 13: "willow shade", 14: "broad peaceful landscape", 15: "Scripture spread"}

def spread_of(p): return None if p in (1, 32) else p // 2

def art(c, p, ox, oy):
    """Watercolor-like placeholder: translucent washes. Same arbor height every page."""
    rnd = random.Random(p)
    c.saveState()
    c.setFillColor(CREAM); c.rect(ox - BLEED, oy - BLEED, TRIM + 2 * BLEED, TRIM + 2 * BLEED, 0, 1)
    if p in (2, 30, 31, 32):  # quiet text pages: small vine motif only
        c.setFillColor(LEAF)
        for i in range(5): c.circle(ox + TRIM / 2 - 40 + i * 20, oy + 1.1 * inch, 9, 0, 1)
        c.setFillColor(PLUM)
        for i in range(4): c.circle(ox + TRIM / 2 - 30 + i * 20, oy + 0.85 * inch, 6, 0, 1)
        c.restoreState(); return
    for _ in range(6):
        c.setFillColor(SKY); c.ellipse(ox + rnd.uniform(-60, TRIM - 100), oy + TRIM * .55 + rnd.uniform(0, 150),
                                       ox + rnd.uniform(100, TRIM + 60), oy + TRIM + BLEED, 0, 1)
    c.setFillColor(HILL); c.ellipse(ox - 80, oy + TRIM * .38, ox + TRIM * .7, oy + TRIM * .62, 0, 1)
    c.ellipse(ox + TRIM * .4, oy + TRIM * .36, ox + TRIM + 80, oy + TRIM * .58, 0, 1)
    c.setFillColor(GRASS); c.rect(ox - BLEED, oy - BLEED, TRIM + 2 * BLEED, TRIM * .45 + BLEED, 0, 1)
    if p in (25, 26, 27):
        c.setFillColor(CREEK); c.ellipse(ox - 40, oy + TRIM * .30, ox + TRIM + 40, oy + TRIM * .40, 0, 1)
    if p < 25 or p in (28, 29):  # arbor: fixed height on every vineyard page
        c.setFillColor(WOOD)
        for x in (.12, .88): c.rect(ox + TRIM * x, oy + TRIM * .42, 8, TRIM * .40, 0, 1)
        c.rect(ox + TRIM * .12, oy + TRIM * .82, TRIM * .76 + 8, 8, 0, 1)
        for _ in range(14):
            c.setFillColor(LEAF); c.circle(ox + TRIM * rnd.uniform(.14, .86), oy + TRIM * rnd.uniform(.80, .88), rnd.uniform(14, 24), 0, 1)
        c.setFillColor(PLUM)
        for gx in (.3, .5, .7):
            for k in range(6): c.circle(ox + TRIM * gx + (k % 3 - 1) * 7, oy + TRIM * .78 - (k // 3) * 10, 6, 0, 1)
    # Fern: simple russet fox mark; jumps on the jump pages
    fx = ox + TRIM * (.32 + .3 * ((p * 37) % 10) / 10); fy = oy + TRIM * (.60 if p in (7, 10, 11) else .44)
    c.setFillColor(RUSSET); c.ellipse(fx - 40, fy, fx + 40, fy + 34, 0, 1); c.circle(fx + 44, fy + 36, 16, 0, 1)
    c.ellipse(fx - 85, fy + 10, fx - 36, fy + 26, 0, 1)
    c.setFont("Helvetica", 7); c.setFillColor(Color(.4, .4, .4))
    s = spread_of(p)
    c.drawRightString(ox + TRIM - SAFE, oy + TRIM - SAFE + 14,
                      f"ART PLACEHOLDER: spread {s}: {SPREAD_BEATS.get(s, 'title')}" if s else "ART PLACEHOLDER")
    c.restoreState()

def text_block(c, ox, oy, text, size=20, top=None, font="Times-Roman", panel=True):
    w = TRIM - 2 * SAFE; lines = simpleSplit(text, font, size, w - 24); lead = size * 1.3
    h = len(lines) * lead + 20; y0 = oy + SAFE if top is None else oy + top - h
    if panel:
        c.setFillColor(Color(.99, .97, .92, .85)); c.roundRect(ox + SAFE, y0, w, h, 10, 0, 1)
    c.setFillColor(INK); c.setFont(font, size)
    for i, ln in enumerate(lines): c.drawCentredString(ox + TRIM / 2, y0 + h - 10 - size - i * lead + 4, ln)

def page(c, p, ox, oy, S, V, credits):
    art(c, p, ox, oy)
    if p == 1:
        text_block(c, ox, oy, "Fern and the High Grapes", 34, top=TRIM - SAFE, font="Times-Bold")
        text_block(c, ox, oy, "A new retelling of The Fox and the Grapes", 16, font="Times-Italic")
    elif p == 2:
        text_block(c, ox, oy, "Copyright \u00a9 2026 [COPYRIGHT HOLDER PLACEHOLDER]. All rights reserved. "
                   "Scripture quotations: Berean Standard Bible (public domain).", 11, top=TRIM / 2, panel=False)
    elif p == 3:
        text_block(c, ox, oy, "A new retelling of The Fox and the Grapes", 22, top=TRIM * .4, font="Times-Italic")
    elif p in S:
        text_block(c, ox, oy, S[p], 20)
    elif p in (30, 31):
        ref, body = V["gal" if p == 30 else "phil"]
        text_block(c, ox, oy, body, 19, top=TRIM - 1.4 * inch, panel=False)
        text_block(c, ox, oy, ref + " (BSB)", 16, top=1.9 * inch, font="Times-Italic", panel=False)
    elif p == 32:
        text_block(c, ox, oy, credits, 11, top=TRIM - SAFE, panel=False)
    if p not in (1,):
        c.setFont("Times-Roman", 9); c.setFillColor(INK)
        c.drawCentredString(ox + TRIM / 2, oy + 0.28 * inch, str(p))

def marks(c):
    c.setStrokeColor(Color(0, 0, 0)); c.setLineWidth(.25); b, t = BLEED, BLEED + TRIM; L = 0.1 * inch
    # bleed is only 0.125in, so marks sit inside the bleed zone, short of the trim line
    for x in (b, t):
        c.line(x, 0, x, b - 0.03 * inch); c.line(x, t + 0.03 * inch, x, t + b)
    for y in (b, t):
        c.line(0, y, b - 0.03 * inch, y); c.line(t + 0.03 * inch, y, t + b, y)

def build():
    S, V = story(), scripture()
    credits = " ".join((ROOT / "content/credits.md").read_text(encoding="utf-8").split("\n\n")[1:]).replace("\n", " ")
    out = ROOT / "exports"; out.mkdir(exist_ok=True)
    meta = lambda c: (c.setTitle("Fern and the High Grapes"), c.setSubject("NOT YET INSTALLED: proof, placeholder art"))
    pr = canvas.Canvas(str(out / "fern-print-interior-8.75sq-bleed.pdf"), pagesize=(TRIM + 2 * BLEED,) * 2); meta(pr)
    rd = canvas.Canvas(str(out / "fern-reading-8.5sq.pdf"), pagesize=(TRIM, TRIM)); meta(rd)
    for p in range(1, 33):
        page(pr, p, BLEED, BLEED, S, V, credits); marks(pr); pr.showPage()
        page(rd, p, 0, 0, S, V, credits); rd.showPage()
    pr.save(); rd.save()
    sp = canvas.Canvas(str(out / "fern-reading-spreads.pdf"), pagesize=(2 * TRIM, TRIM)); meta(sp)
    sheets = [[1]] + [[2 * s, 2 * s + 1] for s in range(1, 16)] + [[32]]
    for sh in sheets:
        if len(sh) == 1: page(sp, sh[0], TRIM / 2, 0, S, V, credits)
        else: page(sp, sh[0], 0, 0, S, V, credits); page(sp, sh[1], TRIM, 0, S, V, credits)
        sp.showPage()
    sp.save(); print("pages=32 spreads=15 sheets=", len(sheets))

if __name__ == "__main__": build()
