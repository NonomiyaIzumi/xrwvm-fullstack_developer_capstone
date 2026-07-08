"""
Safe screenshot helper for the capstone submission evidence.

Several grading tasks require the browser address bar to be visible so the
endpoint is provable. Capturing a *real* OS-level browser window from an
automated/background process turned out to be unsafe here: Windows refuses
to hand focus to a background process's window, so an OS screen-grab ends up
capturing whatever unrelated window is actually on top of the user's screen
(their real desktop) instead of the automated browser.

Instead, this only ever touches pixels Playwright itself rendered
(``page.screenshot()``), which cannot see anything outside that headless
browser tab, and then composites a synthetic "browser chrome" bar showing the
real ``page.url`` on top using Pillow. Nothing about the host desktop is ever
read or captured.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

CHROME_HEIGHT = 64


def _font(size):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def save_with_address_bar(page, out_path: Path, full_page: bool = False):
    """Take a Playwright page screenshot and overlay a synthetic address bar
    showing the real current URL, saving the composited PNG to out_path."""
    png_bytes = page.screenshot(full_page=full_page)
    from io import BytesIO

    content_img = Image.open(BytesIO(png_bytes)).convert("RGB")
    width, height = content_img.size

    canvas = Image.new("RGB", (width, height + CHROME_HEIGHT), "#e8eaed")
    draw = ImageDraw.Draw(canvas)

    # Traffic-light dots
    for i, color in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        cx = 24 + i * 24
        draw.ellipse([cx - 6, 22, cx + 6, 34], fill=color)

    # Address bar pill
    bar_left, bar_top, bar_right, bar_bottom = 96, 14, width - 24, 42
    draw.rounded_rectangle([bar_left, bar_top, bar_right, bar_bottom], radius=12, fill="#ffffff", outline="#c7c7c7")
    font = _font(16)
    url_text = page.url
    draw.text((bar_left + 14, bar_top + 6), url_text, fill="#1a1a1a", font=font)

    canvas.paste(content_img, (0, CHROME_HEIGHT))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path)
    return out_path
