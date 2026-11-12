"""Make a 1280x720 blog cover: photo on the right, navy panel with headline on the left.

Usage:
  python3 _tools/cover/make_cover.py --headline "Spot a|Fake Identity" \
      --subtitle "Check the photo.|Verify the person." \
      --photo /path/to/photo.jpg --focus "60% 50%" \
      --out assets/images/<slug>.jpg

"|" forces a line break. Without --photo it makes a navy/blue graphic with no photo.
The output is a JPEG (quality 85). Needs Python Playwright (preinstalled in the sandbox).
"""
import argparse
import base64
import html
import mimetypes
import pathlib

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent


def lines(text):
    return "<br>".join(html.escape(part.strip()) for part in text.split("|"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--headline", required=True)
    ap.add_argument("--subtitle", required=True)
    ap.add_argument("--photo", help="Local photo file (jpg/png/webp)")
    ap.add_argument("--focus", default="50% 50%", help="CSS background-position for the photo")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    photo_css = None
    if args.photo:
        data = pathlib.Path(args.photo).read_bytes()
        mime = mimetypes.guess_type(args.photo)[0] or "image/jpeg"
        photo_css = f"url(data:{mime};base64,{base64.b64encode(data).decode()})"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720}, device_scale_factor=1)
        page.goto((HERE / "template.html").as_uri())
        page.evaluate(
            """([h, s, photo, focus]) => {
                document.getElementById('headline').innerHTML = h;
                document.getElementById('subtitle').innerHTML = s;
                const el = document.getElementById('photo');
                if (photo) {
                    el.style.backgroundImage = photo;
                    el.style.backgroundPosition = focus;
                } else {
                    el.classList.add('none');
                }
            }""",
            [lines(args.headline), lines(args.subtitle), photo_css, args.focus],
        )
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(300)
        out = pathlib.Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(out), type="jpeg", quality=85)
        browser.close()
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
