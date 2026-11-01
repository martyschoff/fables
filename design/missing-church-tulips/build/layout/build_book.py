#!/usr/bin/env python3
"""The Missing Church Tulips: 36-page interior (p1-32 main book + p33-36 devotional
"The Gift That Honors God"). Fern pipeline (build/fox-grapes-kids layout/build_book.py) adapted.
Text source of truth: ../DESIGN.md page table (p1-32), ../DEVOTIONAL.md (verbatim, p33-36).
Outputs exports/: tulips-print-interior-8.75sq-bleed.pdf, tulips-reading-8.5sq.pdf,
tulips-reading-spreads.pdf, tulips-cover-front-8.75sq-bleed.pdf.
Art: vector PLACEHOLDER unless art/<slot>.(png|jpg) exists. The church photo in
references/ is a PRIVATE reference and is never placed in the book."""
import re, random, pathlib
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import Color
from reportlab.lib.utils import simpleSplit

BUILD = pathlib.Path(__file__).resolve().parent.parent
DESIGN = BUILD.parent
ART = BUILD / "art"
SERIES = "Stories My Mother Read Me"  # Martin t451u
TITLE, HOLDER, YEAR = "The Missing Church Tulips", "Martin Schoffstall", 2026
TRIM, BLEED, SAFE = 8.5 * inch, 0.125 * inch, 0.5 * inch
CREAM = Color(.98, .95, .88); INK = Color(.18, .14, .12)
SKY = Color(.80, .89, .95, .55); GRASS = Color(.55, .70, .40, .45)
TULIP = Color(.82, .12, .15, .8); LEAF = Color(.35, .58, .30, .6)
BRICK = Color(.97, .97, .95, .95); SPIRE = Color(.30, .50, .35, .9); GOLD = Color(.85, .70, .25, .9)
OCHRE = Color(.80, .58, .22, .45)
PAGES = 36
SPEAKERS = {21: "Exodus 20:15 (BSB)", 23: "Proverbs 15:3 (BSB)"}

def strip_md(s): return re.sub(r"\*\*|\*", "", s).strip()

def main_text():
    """p1..p32 text from the DESIGN.md page table, verbatim except p2 (credits, typeset below)."""
    pages = {}
    for row in (DESIGN / "DESIGN.md").read_text(encoding="utf-8").splitlines():
        if not row.startswith("|") or "**p" not in row: continue
        cell = row.split("|")[2]
        for n, t in re.findall(r"\*\*p(\d+):\*\*\s*(.*?)(?=\s*\*\*p\d+:\*\*|$)", cell):
            pages[int(n)] = strip_md(t)
    assert sorted(pages) == list(range(1, 33)), sorted(pages)
    return pages

def scripture_check(S):
    """Spoken verses must equal SCRIPTURE.md BSB text exactly."""
    sc = (DESIGN / "SCRIPTURE.md").read_text(encoding="utf-8")
    for p, ref in ((21, "Exodus 20:15"), (23, "Proverbs 15:3")):
        verse = re.search(re.escape(ref) + r" \([^)]*\): (.+)", sc).group(1).strip()
        assert verse in S[p].replace("\u2019", "'").replace("\u2018", "'") or verse in S[p], (p, verse, S[p])

def devotional():
    """Sections of DEVOTIONAL.md, text kept verbatim."""
    txt = (DESIGN / "DEVOTIONAL.md").read_text(encoding="utf-8")
    secs, cur = {}, None
    for ln in txt.splitlines():
        if ln.startswith("## "): cur = ln[3:].strip(); secs[cur] = []
        elif cur and ln.strip(): secs[cur].append(ln.strip())
    assert "PLACEHOLDER" not in txt.upper()
    return re.match(r"# Devotional: (.+)", txt).group(1).strip(), secs

BEATS = {1: "title: one red tulip, small church view", 3: "St. Thomas UCC exterior + tulip bed (fiction)",
 4: "Leo admires tulips", 5: "memory: Mom loves red", 6: "card in pocket", 7: "empty church doors",
 8: "hesitation", 9: "picks three tulips", 10: "hurrying home", 11: "shoulders sink", 12: "tulips in water",
 13: "troubled face", 14: "realization", 15: "turns to the door", 16: "Mr. & Mrs. Davis tending bed",
 17: "Leo approaches", 18: "confession, open hands", 19: "\"I'm sorry\"", 20: "Mr. Davis at eye level",
 21: "Mr. Davis: Ex 20:15", 22: "kind correction", 23: "Mrs. Davis speaks Prov 15:3", 24: "vase for the church",
 25: "bulb packet", 26: "\"Plant in fall\"", 27: "relief", 28: "Mother's Day card + truth", 29: "Mom's hug",
 30: "autumn planting", 31: "moral, quiet page", 32: "card + bulbs vignette"}

def art_file(name):
    for ext in (".png", ".jpg", ".jpeg"):
        f = ART / (name + ext)
        if f.exists(): return f
MISSING = []

def placeholder(c, p, ox, oy):
    rnd = random.Random(p); c.saveState()
    c.setFillColor(CREAM); c.rect(ox - BLEED, oy - BLEED, TRIM + 2 * BLEED, TRIM + 2 * BLEED, 0, 1)
    quiet = p in (2, 31, 32) or p >= 33
    if quiet:
        for i in range(3):
            x = ox + TRIM / 2 - 24 + i * 24
            c.setFillColor(LEAF); c.rect(x - 1, oy + 0.55 * inch, 2, 0.45 * inch, 0, 1)
            c.setFillColor(TULIP); c.ellipse(x - 7, oy + 0.95 * inch, x + 7, oy + 1.2 * inch, 0, 1)
        c.restoreState(); return
    for _ in range(5):
        c.setFillColor(SKY); c.ellipse(ox + rnd.uniform(-60, TRIM - 100), oy + TRIM * .6 + rnd.uniform(0, 120),
                                       ox + rnd.uniform(100, TRIM + 60), oy + TRIM + BLEED, 0, 1)
    c.setFillColor(OCHRE if p == 30 else GRASS); c.rect(ox - BLEED, oy - BLEED, TRIM + 2 * BLEED, TRIM * .42 + BLEED, 0, 1)
    if p in (1, 3, 4, 5, 6, 7, 8, 9, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27):  # church (generic, not the photo)
        bx = ox + TRIM * .52
        c.setFillColor(BRICK); c.rect(bx, oy + TRIM * .42, TRIM * .36, TRIM * .26, 0, 1)
        c.rect(bx - TRIM * .16, oy + TRIM * .42, TRIM * .16, TRIM * .15, 0, 1)
        c.rect(bx + TRIM * .13, oy + TRIM * .68, TRIM * .1, TRIM * .1, 0, 1)
        c.setFillColor(SPIRE); pth = c.beginPath(); pth.moveTo(bx + TRIM * .13, oy + TRIM * .78)
        pth.lineTo(bx + TRIM * .18, oy + TRIM * .92); pth.lineTo(bx + TRIM * .23, oy + TRIM * .78); c.drawPath(pth, 0, 1)
        c.setFillColor(GOLD); c.rect(bx + TRIM * .177, oy + TRIM * .92, 3, 14, 0, 1); c.rect(bx + TRIM * .17, oy + TRIM * .935, 15, 3, 0, 1)
    n = 3 if p in (17, 18, 19, 20, 21, 22, 23) else 14   # three missing from the bed
    for i in range(n):
        x = ox + TRIM * (.08 + i * .028)
        c.setFillColor(LEAF); c.rect(x, oy + TRIM * .40, 2, 22, 0, 1)
        c.setFillColor(TULIP); c.ellipse(x - 6, oy + TRIM * .40 + 20, x + 8, oy + TRIM * .40 + 38, 0, 1)
    c.setFont("Helvetica", 7); c.setFillColor(Color(.4, .4, .4))
    c.drawRightString(ox + TRIM - SAFE, oy + TRIM - SAFE + 14, f"ART SLOT art/p{p:02d} (PLACEHOLDER): {BEATS.get(p, '')}")
    c.restoreState()

def art(c, p, ox, oy):
    f = art_file(f"p{p:02d}")
    if f:
        c.drawImage(str(f), ox - BLEED, oy - BLEED, TRIM + 2 * BLEED, TRIM + 2 * BLEED); return
    if p <= 32 and p not in (2, 31, 32): MISSING.append(f"p{p:02d}")
    placeholder(c, p, ox, oy)

def text_block(c, ox, oy, text, size=20, top=None, font="Times-Roman", panel=True, align="c", lead=1.3):
    w = TRIM - 2 * SAFE; lines = []
    for para in text.split("\n"): lines += simpleSplit(para, font, size, w - 24) or [""]
    ld = size * lead; h = len(lines) * ld + 20; y0 = oy + SAFE if top is None else oy + top - h
    if panel: c.setFillColor(Color(.99, .97, .92, .88)); c.roundRect(ox + SAFE, y0, w, h, 10, 0, 1)
    c.setFillColor(INK); c.setFont(font, size)
    for i, ln in enumerate(lines):
        y = y0 + h - 10 - size - i * ld + 4
        (c.drawCentredString(ox + TRIM / 2, y, ln) if align == "c" else c.drawString(ox + SAFE + 12, y, ln))
    return y0

def fit(c, ox, oy, chunks, top, bottom=0.75 * inch, start=15):
    """chunks: list of (text, font). Shrink until all fit between top and bottom."""
    w = TRIM - 2 * SAFE - 24
    for size in range(start, 7, -1):
        h = sum(len(simpleSplit(t, f, size, w) or [""]) * size * 1.3 + size * .6 for t, f in chunks)
        if oy + top - h >= oy + bottom: break
    y = oy + top
    for t, f in chunks:
        c.setFont(f, size); c.setFillColor(INK)
        for ln in simpleSplit(t, f, size, w) or [""]:
            y -= size * 1.3; c.drawString(ox + SAFE + 12, y, ln)
        y -= size * .6
    return size

def page(c, p, ox, oy, S, D):
    art(c, p, ox, oy)
    dtitle, sec = D
    if p == 1:
        y = text_block(c, ox, oy, SERIES, 16, top=TRIM - SAFE, font="Times-Italic")
        text_block(c, ox, oy, TITLE, 36, top=y - 8, font="Times-Bold")
        text_block(c, ox, oy, f"by {HOLDER}", 18, font="Times-Italic")
    elif p == 2:
        text_block(c, ox, oy, f"Text copyright \u00a9 {YEAR} {HOLDER}. All rights reserved. {SERIES}. Written by {HOLDER}. "
                   f"Illustrated by {illustrator()}.\nScripture quotations are from the Berean Standard Bible (BSB), public domain: "
                   "Exodus 20:15 (p21) and Proverbs 15:3 (p23).\nSet near St. Thomas United Church of Christ, Linglestown, Pennsylvania. "
                   "Story, characters, and the church tulip bed are fiction.", 11, top=TRIM / 2 + 0.6 * inch, panel=False)
    elif p == 31:
        text_block(c, ox, oy, S[p], 22, top=TRIM * .72, font="Times-Italic", panel=False)
    elif p == 32:
        text_block(c, ox, oy, S[p], 18, top=TRIM * .7, panel=False)
    elif p in S:
        text_block(c, ox, oy, S[p], 19 if len(S[p]) < 140 else 16)
        if p in SPEAKERS:
            c.setFont("Times-Italic", 9); c.setFillColor(INK); c.drawRightString(ox + TRIM - SAFE, oy + 0.28 * inch, SPEAKERS[p])
    elif p == 33:
        c.setFont("Times-Bold", 26); c.setFillColor(INK); c.drawCentredString(ox + TRIM / 2, oy + TRIM - SAFE - 30, dtitle)
        c.setFont("Times-Italic", 11); c.drawCentredString(ox + TRIM / 2, oy + TRIM - SAFE - 50, f"A devotional for families \u00b7 \u00a9 {HOLDER}")
        fit(c, ox, oy, [("Scripture Reading", "Times-Bold")] + [(strip_md(x).lstrip("- "), "Times-Roman") for x in sec["Scripture Reading"]]
            + [("The Big Idea", "Times-Bold")] + [(x, "Times-Italic") for x in sec["The Big Idea"]], TRIM - SAFE - 70, start=17)
    elif p in (34, 35):
        key = next(k for k in sec if k.startswith("The Message"))
        paras = sec[key]; half = (len(paras) + 1) // 2
        part = paras[:half] if p == 34 else paras[half:]
        hd = [(key.replace("The Message: ", "The Message: \n"), "Times-Bold")] if p == 34 else []
        fit(c, ox, oy, [(h.replace("\n", ""), f) for h, f in hd] + [(x, "Times-Roman") for x in part], TRIM - SAFE, start=16)
    elif p == 36:
        fit(c, ox, oy, [("Family Discussion Questions", "Times-Bold")] + [(strip_md(x), "Times-Roman") for x in sec["Family Discussion Questions"]]
            + [("Closing Prayer", "Times-Bold")] + [(x, "Times-Italic") for x in sec["Closing Prayer"]], TRIM - SAFE, start=15)
    if p != 1:
        c.setFont("Times-Roman", 9); c.setFillColor(INK); c.drawCentredString(ox + TRIM / 2, oy + 0.28 * inch, str(p))

def illustrator():
    f = ART / "CREDITS.md"
    if f.exists():
        for ln in f.read_text(encoding="utf-8").splitlines():
            if ln.lower().startswith("illustrator:"): return ln.split(":", 1)[1].strip()
    return "[illustrator credit pending]"

def marks(c):
    c.setStrokeColor(Color(0, 0, 0)); c.setLineWidth(.25); b, t = BLEED, BLEED + TRIM
    for x in (b, t): c.line(x, 0, x, b - 0.03 * inch); c.line(x, t + 0.03 * inch, x, t + b)
    for y in (b, t): c.line(0, y, b - 0.03 * inch, y); c.line(t + 0.03 * inch, y, t + b, y)

def cover(out):
    c = canvas.Canvas(str(out / "tulips-cover-front-8.75sq-bleed.pdf"), pagesize=(TRIM + 2 * BLEED,) * 2)
    c.setTitle(TITLE + " (cover)"); f = art_file("cover")
    if f: c.drawImage(str(f), 0, 0, TRIM + 2 * BLEED, TRIM + 2 * BLEED)
    else:
        placeholder(c, 3, BLEED, BLEED); MISSING.insert(0, "cover")
    y = text_block(c, BLEED, BLEED, SERIES, 18, top=TRIM - 0.6 * inch, font="Times-Italic")
    text_block(c, BLEED, BLEED, TITLE, 38, top=y - 8, font="Times-Bold")
    text_block(c, BLEED, BLEED, HOLDER, 18)
    marks(c); c.save()

def build():
    S, D = main_text(), devotional(); scripture_check(S)
    out = BUILD / "exports"; out.mkdir(exist_ok=True)
    meta = lambda c: (c.setTitle(f"{SERIES}: {TITLE}"), c.setAuthor(HOLDER), c.setSubject("DRAFT proof, NOT YET INSTALLED; placeholder art"))
    pr = canvas.Canvas(str(out / "tulips-print-interior-8.75sq-bleed.pdf"), pagesize=(TRIM + 2 * BLEED,) * 2); meta(pr)
    rd = canvas.Canvas(str(out / "tulips-reading-8.5sq.pdf"), pagesize=(TRIM, TRIM)); meta(rd)
    for p in range(1, PAGES + 1):
        page(pr, p, BLEED, BLEED, S, D); marks(pr); pr.showPage()
        page(rd, p, 0, 0, S, D); rd.showPage()
    pr.save(); rd.save()
    sp = canvas.Canvas(str(out / "tulips-reading-spreads.pdf"), pagesize=(2 * TRIM, TRIM)); meta(sp)
    sheets = [[1]] + [[2 * s, 2 * s + 1] for s in range(1, PAGES // 2)] + [[PAGES]]
    for sh in sheets:
        if len(sh) == 1: page(sp, sh[0], TRIM / 2, 0, S, D)
        else: page(sp, sh[0], 0, 0, S, D); page(sp, sh[1], TRIM, 0, S, D)
        sp.showPage()
    sp.save(); cover(out)
    print(f"pages={PAGES} sheets={len(sheets)}"); print("missing art slots:", ",".join(dict.fromkeys(MISSING)) or "none")

if __name__ == "__main__": build()
