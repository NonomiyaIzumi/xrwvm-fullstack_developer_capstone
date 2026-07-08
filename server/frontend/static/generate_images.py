"""One-off helper to generate simple placeholder avatar/logo/banner PNGs
for the static About/Contact pages (no network access needed to fetch stock
photos, so these are drawn locally with Pillow)."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(__file__).parent / "images"
OUT_DIR.mkdir(exist_ok=True)


def font(size):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def avatar(filename, initials, bg):
    size = 240
    img = Image.new("RGB", (size, size), bg)
    draw = ImageDraw.Draw(img)
    f = font(90)
    bbox = draw.textbbox((0, 0), initials, font=f)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((size - w) / 2 - bbox[0], (size - h) / 2 - bbox[1]), initials, fill="white", font=f)
    img.save(OUT_DIR / filename)


def logo(filename):
    img = Image.new("RGB", (320, 100), "#1f2a44")
    draw = ImageDraw.Draw(img)
    f = font(34)
    text = "Cars Dealership"
    bbox = draw.textbbox((0, 0), text, font=f)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((320 - w) / 2 - bbox[0], (100 - h) / 2 - bbox[1]), text, fill="white", font=f)
    img.save(OUT_DIR / filename)


def storefront(filename):
    img = Image.new("RGB", (640, 320), "#dbe2f2")
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 200, 640, 320], fill="#8a8f98")
    draw.rectangle([40, 90, 600, 200], fill="#1f2a44")
    for x in range(80, 560, 90):
        draw.rectangle([x, 110, x + 50, 180], fill="#dbe2f2")
    draw.polygon([(20, 90), (620, 90), (560, 30), (80, 30)], fill="#cf4d3b")
    f = font(24)
    text = "Cars Dealership - Main Showroom"
    bbox = draw.textbbox((0, 0), text, font=f)
    w = bbox[2] - bbox[0]
    draw.text(((640 - w) / 2, 250), text, fill="white", font=f)
    img.save(OUT_DIR / filename)


avatar("team-anh.png", "BA", "#1f6feb")
avatar("team-linh.png", "TL", "#cf4d3b")
avatar("team-minh.png", "QM", "#1a7f37")
logo("logo.png")
storefront("storefront.png")

print("Generated:", sorted(p.name for p in OUT_DIR.iterdir()))
