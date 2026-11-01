#!/usr/bin/env python3
"""Immy and Hunter Mountain: A Catskills Fable. 32-page interior (Martin t461u/t464u).
Tulips/Fern pipeline adapted. Text source of truth: ../DESIGN.md page table (pp4-25),
../SCRIPTURE.md (pp26-27, exact BSB), ../source/emerson-mountain-squirrel.txt (pp28-29 verbatim),
../DEVOTIONAL.md (pp30-32 verbatim, faded illustration behind text).
Outputs exports/: immy-print-interior-8.75sq-bleed.pdf, immy-reading-8.5sq.pdf,
immy-reading-spreads.pdf, immy-cover-front-8.75sq-bleed.pdf.
Art: vector PLACEHOLDER unless art/<slot>.(png|jpg) exists."""
import re, random, pathlib
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import Color
from reportlab.lib.utils import simpleSplit

BUILD = pathlib.Path(__file__).resolve().parent.parent
DESIGN = BUILD.parent
ART = BUILD / "art"
SERIES = "Stories My Mother Read Me"  # Martin t451u; BOTTOM of cover t454u
TITLE, SUB = "Immy and Hunter Mountain", "A Catskills Fable"  # Martin t464u
HOLDER, YEAR = "Martin Schoffstall", 2026
TRIM, BLEED, SAFE = 8.5 * inch, 0.125 * inch, 0.5 * inch
CREAM = Color(.98, .95, .88); INK = Color(.18, .14, .12)
SKY = Color(.72, .80, .90, .55); FOREST = Color(.33, .50, .33, .75); MOSS = Color(.55, .66, .40, .55)
SLATE = Color(.45, .52, .60, .8); RUST = Color(.72, .38, .18, .8); NUT = Color(.50, .33, .18, .95)
SQ = Color(.50, .50, .52, 1); LAV = Color(.70, .62, .80, .45)
PAGES = 32

def strip_md(s): return re.sub(r"\*\*|\*", "", s).strip()

def story_text():
    pages = {}
    for row in (DESIGN / "DESIGN.md").read_text(encoding="utf-8").splitlines():
        if not row.startswith("|"): continue
        cells = row.split("|")
        if len(cells) < 3 or not re.match(r"\s*\d+[–-]\d+\s*$", cells[1]): continue
        for n, t in re.findall(r"\*\*(\d+):\*\*\s*(.*?)(?=\s*\*\*\d+:\*\*|$)", cells[2]):
            n = int(n)
            if 4 <= n <= 25:
                t = t.strip()
                if t.startswith("\u201c") and t.endswith("\u201d"): t = t[1:-1]
                pages[n] = t
    assert sorted(pages) == list(range(4, 26)), sorted(pages)
    for p, t in pages.items():
        assert "Bun" not in t and "Slide" not in t and "Peekamoose" not in t, (p, t)
    return pages

def scripture():
    sc = (DESIGN / "SCRIPTURE.md").read_text(encoding="utf-8")
    ps = re.search(r"Psalm 139:14 \([^)]*\): (.+)", sc).group(1).strip()
    co = re.search(r"1 Corinthians 12:18-20 \([^)]*\): (.+)", sc).group(1).strip()
    d = (DESIGN / "DESIGN.md").read_text(encoding="utf-8")
    assert ps in d and co in d
    return ps, co

def poem():
    lines = (DESIGN / "source/emerson-mountain-squirrel.txt").read_text(encoding="utf-8").splitlines()
    i = lines.index("The mountain and the squirrel")
    body = [l for l in lines[i:] if l.strip()]
    assert len(body) == 19 and body[-1] == "Neither can you crack a nut.'", body
    return body

def devotional():
    txt = (DESIGN / "DEVOTIONAL.md").read_text(encoding="utf-8")
    assert "PLACEHOLDER" not in txt.upper()
    secs, cur, pre = {}, None, []
    for ln in txt.splitlines()[1:]:
        if ln.startswith("## "): cur = ln[3:].strip(); secs[cur] = []
        elif ln.strip(): (secs[cur] if cur else pre).append(ln.strip())
    return re.match(r"# Devotional: (.+)", txt).group(1).strip(), pre, secs

BEATS = {1: "tiny Immy with nut; distant Hunter Mtn", 2: "quiet front matter", 3: "size contrast",
 4: "forested Catskills, Immy small", 5: "Hunter Mtn booms", 6: "boastful mountain face", 7: "Immy composed",
 8: "spring rain/summer sun", 9: "autumn leaf, winter snowcap", 10: "seasons gather", 11: "Immy warm focal",
 12: "size contrast", 13: "Immy zips along branch", 14: "mountain carries forest", 15: "woodland path",
 16: "warm pause", 17: "Immy lifts nut", 18: "Crack!", 19: "forest on back", 20: "shared landscape",
 21: "mountain softens", 22: "small neighbor", 23: "Immy springs root to rock", 24: "nut under leaves",
 25: "evening good night", 26: "scripture spread", 27: "scripture spread", 28: "poem border", 29: "poem border",
 30: "faded story illus.", 31: "faded story illus.", 32: "faded story illus."}

def art_file(name):
    for ext in (".png", ".jpg", ".jpeg"):
        f = ART / (name + ext)
        if f.exists(): return f
MISSING = []

def scene(c, p, ox, oy, fade=1.0):
    rnd = random.Random(p)
    def col(k): return Color(k.red, k.green, k.blue, k.alpha * fade)
    evening = p in (24, 25)
    for _ in range(4):
        c.setFillColor(col(LAV if evening else SKY))
        c.ellipse(ox + rnd.uniform(-60, TRIM - 120), oy + TRIM * .62 + rnd.uniform(0, 100), ox + rnd.uniform(120, TRIM + 60), oy + TRIM + BLEED, 0, 1)
    # rounded Catskills ridges, Hunter Mountain largest
    for k, (cx, w, h, colr) in enumerate(((.15, .55, .38, SLATE), (.62, .95, .62, FOREST), (1.0, .5, .34, SLATE))):
        c.setFillColor(col(colr)); pth = c.beginPath(); x0 = ox + TRIM * (cx - w / 2); x1 = ox + TRIM * (cx + w / 2)
        pth.moveTo(x0 - BLEED, oy + TRIM * .30); pth.curveTo(x0 + (x1 - x0) * .25, oy + TRIM * (.30 + h), x0 + (x1 - x0) * .75, oy + TRIM * (.30 + h), x1, oy + TRIM * .30)
        pth.close(); c.drawPath(pth, 0, 1)
    if p == 9: c.setFillColor(Color(1, 1, 1, .9 * fade)); c.ellipse(ox + TRIM * .52, oy + TRIM * .84, ox + TRIM * .72, oy + TRIM * .93, 0, 1)
    c.setFillColor(col(MOSS)); c.rect(ox - BLEED, oy - BLEED, TRIM + 2 * BLEED, TRIM * .32 + BLEED, 0, 1)
    for i in range(12):  # evergreen accents
        x = ox + TRIM * rnd.uniform(.02, .98); y = oy + TRIM * rnd.uniform(.26, .34)
        c.setFillColor(col(FOREST)); pth = c.beginPath(); pth.moveTo(x - 8, y); pth.lineTo(x, y + 26); pth.lineTo(x + 8, y); pth.close(); c.drawPath(pth, 0, 1)
    if p in (9, 10, 14, 15) or 26 <= p:
        for i in range(6):
            c.setFillColor(col(RUST)); x = ox + TRIM * rnd.uniform(.1, .9); y = oy + TRIM * rnd.uniform(.1, .3); c.ellipse(x, y, x + 9, y + 5, 0, 1)
    # Immy: tiny eastern gray squirrel, always legible
    sx, sy = ox + TRIM * (.18 + (p % 5) * .03), oy + TRIM * .33
    c.setFillColor(col(SQ)); c.ellipse(sx, sy, sx + 16, sy + 12, 0, 1); c.circle(sx + 18, sy + 13, 5, 0, 1)
    c.ellipse(sx - 12, sy + 2, sx + 2, sy + 26, 0, 1)
    if p in (1, 17, 18, 24): c.setFillColor(col(NUT)); c.circle(sx + 24, sy + 9, 3, 0, 1)

def placeholder(c, p, ox, oy, fade=1.0, label=True):
    c.saveState(); c.setFillColor(CREAM); c.rect(ox - BLEED, oy - BLEED, TRIM + 2 * BLEED, TRIM + 2 * BLEED, 0, 1)
    if p in (2, 26, 27, 28, 29): fade = min(fade, .3)
    scene(c, p, ox, oy, fade)
    if label:
        c.setFont("Helvetica", 7); c.setFillColor(Color(.4, .4, .4))
        c.drawRightString(ox + TRIM - SAFE, oy + TRIM - SAFE + 14, f"ART SLOT art/p{p:02d} (PLACEHOLDER): {BEATS.get(p, '')}")
    c.restoreState()

def art(c, p, ox, oy):
    fade = .22 if p >= 30 else 1.0  # devotion: faded illustration behind text
    f = art_file(f"p{p:02d}") or (art_file("p25") if p >= 30 else None)
    if f:
        c.drawImage(str(f), ox - BLEED, oy - BLEED, TRIM + 2 * BLEED, TRIM + 2 * BLEED)
        if fade < 1: c.setFillColor(Color(.98, .95, .88, 1 - fade)); c.rect(ox - BLEED, oy - BLEED, TRIM + 2 * BLEED, TRIM + 2 * BLEED, 0, 1)
        return
    if p not in (2,): MISSING.append(f"p{p:02d}")
    placeholder(c, 25 if p >= 30 else p, ox, oy, fade)
    if p >= 30:
        c.setFont("Helvetica", 7); c.setFillColor(Color(.4, .4, .4))
        c.drawRightString(ox + TRIM - SAFE, oy + TRIM - SAFE + 14, f"ART SLOT art/p{p:02d} (PLACEHOLDER): faded story illustration")

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

def fit(c, ox, oy, chunks, top, bottom=0.7 * inch, start=15):
    w = TRIM - 2 * SAFE - 24
    for size in range(start, 7, -1):
        h = sum(len(simpleSplit(t, f, size, w) or [""]) * size * 1.25 + size * .5 for t, f in chunks)
        if oy + top - h >= oy + bottom: break
    y = oy + top
    for t, f in chunks:
        c.setFont(f, size); c.setFillColor(INK)
        for ln in simpleSplit(t, f, size, w) or [""]:
            y -= size * 1.25; c.drawString(ox + SAFE + 12, y, ln)
        y -= size * .5
    return size

def dev_header(c, ox, oy, txt):
    c.setFillColor(Color(.45, .52, .60)); c.rect(ox + SAFE, oy + TRIM - SAFE - 6, TRIM - 2 * SAFE, 2, 0, 1)
    c.setFont("Helvetica-Bold", 9); c.setFillColor(Color(.35, .42, .50))
    c.drawCentredString(ox + TRIM / 2, oy + TRIM - SAFE + 2, "FAMILY DEVOTIONAL \u00b7 " + txt)

def page(c, p, ox, oy, S, SC, PO, D):
    art(c, p, ox, oy); dtitle, dpre, sec = D; ps, co = SC
    if p == 1:
        text_block(c, ox, oy, f"{TITLE}:\n{SUB}", 32, top=TRIM - SAFE, font="Times-Bold")
    elif p == 2:
        text_block(c, ox, oy, f"Text and illustrations copyright \u00a9 {YEAR} {HOLDER}. All rights reserved.\n"
                   f"Written by {HOLDER}. Illustrated by {illustrator()}.\n"
                   "Adapted from Ralph Waldo Emerson\u2019s \u201cFable\u201d (Poems, 1847), later anthologized as \u201cThe Mountain and the Squirrel.\u201d "
                   "Emerson\u2019s poem is in the public domain; text per the Academy of American Poets and the Poetry Foundation.\n"
                   "Scripture quotations are from the Berean Standard Bible (BSB): Psalm 139:14 and 1 Corinthians 12:18-20.\n"
                   f"{SERIES}: Fern and the High Grapes \u00b7 The Missing Church Tulips \u00b7 {TITLE}: {SUB}.",
                   11, top=TRIM / 2 + 1.2 * inch, panel=False)
    elif p == 3:
        y = text_block(c, ox, oy, f"{TITLE}:\n{SUB}", 34, top=TRIM - SAFE - 10, font="Times-Bold")
        y = text_block(c, ox, oy, SERIES, 16, top=y - 6, font="Times-Italic")
        y = text_block(c, ox, oy, HOLDER, 20, top=y - 6)
        text_block(c, ox, oy, "A retelling of Ralph Waldo Emerson\u2019s \u201cFable.\u201d", 13, font="Times-Italic")
    elif p in S:
        text_block(c, ox, oy, S[p], 20 if len(S[p]) < 120 else 17)
    elif p == 26:
        text_block(c, ox, oy, ps, 24, top=TRIM * .68, font="Times-Italic", panel=True)
        text_block(c, ox, oy, "Psalm 139:14 (BSB)", 14, top=TRIM * .30, panel=False)
    elif p == 27:
        text_block(c, ox, oy, co, 20, top=TRIM * .74, font="Times-Italic", panel=True)
        text_block(c, ox, oy, "1 Corinthians 12:18-20 (BSB)", 14, top=TRIM * .24, panel=False)
    elif p == 28:
        text_block(c, ox, oy, "Fable", 40, top=TRIM * .72, font="Times-Bold", panel=False)
        text_block(c, ox, oy, "Ralph Waldo Emerson", 20, top=TRIM * .58, font="Times-Italic", panel=False)
        text_block(c, ox, oy, "Emerson\u2019s original poem, from Poems (1847), later called \u201cThe Mountain and the Squirrel.\u201d "
                   "In it the squirrel is named Bun; in our retelling she is Immy.", 13, top=TRIM * .40, panel=False)
    elif p == 29:
        c.setStrokeColor(Color(.45, .52, .60)); c.setLineWidth(1); c.rect(ox + SAFE * .7, oy + SAFE * .7, TRIM - 1.4 * SAFE, TRIM - 1.4 * SAFE, 0, 0)
        y = oy + TRIM - SAFE - 18; c.setFont("Times-Roman", 15.5); c.setFillColor(INK)
        for ln in PO: c.drawString(ox + 1.25 * inch, y, ln); y -= 15.5 * 1.42
    elif p == 30:
        dev_header(c, ox, oy, "Honoring God\u2019s Good Design")
        c.setFont("Times-Bold", 24); c.setFillColor(INK); c.drawCentredString(ox + TRIM / 2, oy + TRIM - SAFE - 40, dtitle)
        fit(c, ox, oy, [(strip_md(x), "Times-Italic") for x in dpre] + [("Scripture Reading", "Times-Bold")]
            + [(strip_md(x).lstrip("- "), "Times-Roman") for x in sec["Scripture Reading"]]
            + [("The Big Idea", "Times-Bold")] + [(x, "Times-Italic") for x in sec["The Big Idea"]], TRIM - SAFE - 60, start=15)
    elif p == 31:
        dev_header(c, ox, oy, "The Message")
        fit(c, ox, oy, [("The Message", "Times-Bold")] + [(x, "Times-Roman") for x in sec["The Message"]], TRIM - SAFE - 20, start=16)
    elif p == 32:
        dev_header(c, ox, oy, "Talk and Pray Together")
        fit(c, ox, oy, [("Family Discussion Questions", "Times-Bold")] + [(strip_md(x), "Times-Roman") for x in sec["Family Discussion Questions"]]
            + [("Closing Prayer", "Times-Bold")] + [(x, "Times-Italic") for x in sec["Closing Prayer"]], TRIM - SAFE - 20, start=15)
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
    c = canvas.Canvas(str(out / "immy-cover-front-8.75sq-bleed.pdf"), pagesize=(TRIM + 2 * BLEED,) * 2)
    c.setTitle(f"{TITLE}: {SUB} (cover)"); f = art_file("cover")
    if f: c.drawImage(str(f), 0, 0, TRIM + 2 * BLEED, TRIM + 2 * BLEED)
    else: placeholder(c, 4, BLEED, BLEED, label=False); MISSING.insert(0, "cover")
    y = text_block(c, BLEED, BLEED, TITLE, 40, top=TRIM - 0.7 * inch, font="Times-Bold")   # individual title primary
    text_block(c, BLEED, BLEED, SUB, 22, top=y - 6, font="Times-Italic")
    y = text_block(c, BLEED, BLEED, SERIES, 18, font="Times-Italic")   # series = lowest line, BOTTOM (t454u)
    text_block(c, BLEED, BLEED, HOLDER, 20, top=(y - BLEED) + (18 * 1.3 + 20) + 8 + (20 * 1.3 + 20))
    marks(c); c.save()

def build():
    S, SC, PO, D = story_text(), scripture(), poem(), devotional()
    out = BUILD / "exports"; out.mkdir(exist_ok=True)
    meta = lambda c: (c.setTitle(f"{SERIES}: {TITLE}: {SUB}"), c.setAuthor(HOLDER), c.setSubject("DRAFT proof, NOT YET INSTALLED; placeholder art"))
    pr = canvas.Canvas(str(out / "immy-print-interior-8.75sq-bleed.pdf"), pagesize=(TRIM + 2 * BLEED,) * 2); meta(pr)
    rd = canvas.Canvas(str(out / "immy-reading-8.5sq.pdf"), pagesize=(TRIM, TRIM)); meta(rd)
    for p in range(1, PAGES + 1):
        page(pr, p, BLEED, BLEED, S, SC, PO, D); marks(pr); pr.showPage()
        page(rd, p, 0, 0, S, SC, PO, D); rd.showPage()
    pr.save(); rd.save()
    sp = canvas.Canvas(str(out / "immy-reading-spreads.pdf"), pagesize=(2 * TRIM, TRIM)); meta(sp)
    sheets = [[1]] + [[2 * s, 2 * s + 1] for s in range(1, PAGES // 2)] + [[PAGES]]
    for sh in sheets:
        if len(sh) == 1: page(sp, sh[0], TRIM / 2, 0, S, SC, PO, D)
        else: page(sp, sh[0], 0, 0, S, SC, PO, D); page(sp, sh[1], TRIM, 0, S, SC, PO, D)
        sp.showPage()
    sp.save(); cover(out)
    print(f"pages={PAGES} sheets={len(sheets)}"); print("missing art slots:", ",".join(dict.fromkeys(MISSING)) or "none")

if __name__ == "__main__": build()
