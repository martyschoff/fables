"""Local procedural PLACEHOLDER art (no AI): rasterize vector placeholder scenes + paper grain/wash."""
import sys, subprocess, pathlib, numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0, str(pathlib.Path(__file__).parent)); import build_book as B
from reportlab.pdfgen import canvas
art = B.ART; tmp = pathlib.Path("/tmp/immyart"); tmp.mkdir(exist_ok=True)
S = B.TRIM + 2 * B.BLEED
for slot, p in [("cover", 4)] + [(f"p{p:02d}", p) for p in list(range(1, 2)) + list(range(3, 30))]:
    c = canvas.Canvas(str(tmp / "a.pdf"), pagesize=(S, S)); B.placeholder(c, p, B.BLEED, B.BLEED, label=False); c.save()
    subprocess.run(["pdftoppm", "-r", "120", "-png", "-singlefile", str(tmp / "a.pdf"), str(tmp / "a")], check=True)
    im = Image.open(tmp / "a.png").convert("RGB").filter(ImageFilter.GaussianBlur(3))
    a = np.asarray(im).astype(np.float32); rng = np.random.default_rng(p)
    grain = rng.normal(0, 9, a.shape[:2])[..., None]
    wash = np.asarray(Image.fromarray((rng.random((a.shape[0] // 40, a.shape[1] // 40)) * 255).astype(np.uint8)).resize(im.size, Image.BICUBIC), np.float32)[..., None]
    a = np.clip(a + grain + (wash - 128) * .12, 0, 255).astype(np.uint8)
    Image.fromarray(a).save(art / f"{slot}.jpg", quality=85)
(art / "CREDITS.md").write_text("illustrator: [illustrator credit pending]\nNOTE: art/*.jpg are LOCAL PROCEDURAL PLACEHOLDERS (no AI), to be replaced by watercolor art.\n")
