"""Rasterize SVGs to PNG with headless Chrome, then pack favicon.ico.

Run after build_logo.py:  python render_png.py
"""
import os, subprocess, tempfile, pathlib
from PIL import Image

HERE = pathlib.Path(__file__).parent
SVG = HERE / "svg"
PNG = HERE / "png"
PNG.mkdir(exist_ok=True)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

JOBS = [  # (svg, out png, width, height)
    ("favicon-small.svg", "favicon-16.png", 16, 16),
    ("favicon-small.svg", "favicon-32.png", 32, 32),
    ("favicon-small.svg", "favicon-48.png", 48, 48),
    ("favicon.svg", "icon-192.png", 192, 192),
    ("favicon.svg", "icon-512.png", 512, 512),
    ("app-icon.svg", "apple-touch-icon.png", 180, 180),
    ("tvt-logo-horizontal-navy.svg", "tvt-logo-horizontal-navy.png", None, 120 * 2),
    ("tvt-logo-horizontal-ivory.svg", "tvt-logo-horizontal-ivory.png", None, 120 * 2),
    ("tvt-logo-stacked-navy.svg", "tvt-logo-stacked-navy.png", 1200, None),
    ("tvt-logo-stacked-ivory.svg", "tvt-logo-stacked-ivory.png", 1200, None),
    ("tvt-monogram-navy.svg", "tvt-monogram-navy.png", None, 400),
    ("tvt-monogram-gold.svg", "tvt-monogram-gold.png", None, 400),
]


def svg_size(path):
    import re
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', path.read_text(encoding="utf-8"))
    return float(m.group(1)), float(m.group(2))


def render(svg, out, w, h):
    vw, vh = svg_size(SVG / svg)
    if w is None:
        w = round(h * vw / vh)
    if h is None:
        h = round(w * vh / vw)
    uri = (SVG / svg).resolve().as_uri()
    html = (f'<!doctype html><style>html,body{{margin:0;background:transparent}}'
            f'img{{display:block;width:{w}px;height:{h}px}}</style><img src="{uri}">')
    with tempfile.TemporaryDirectory() as td:
        page = pathlib.Path(td) / "p.html"
        page.write_text(html, encoding="utf-8")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--allow-file-access-from-files",
                        "--default-background-color=00000000",
                        f"--window-size={w},{h}", f"--screenshot={PNG / out}",
                        page.as_uri()], check=True, capture_output=True)
    im = Image.open(PNG / out)
    if im.size != (w, h):  # crop any extra window area
        im.crop((0, 0, w, h)).save(PNG / out)
    print(out, (w, h))


for job in JOBS:
    render(*job)

# favicon.ico with 16/32/48 frames
frames = [Image.open(PNG / f"favicon-{s}.png").convert("RGBA") for s in (16, 32, 48)]
frames[2].save(HERE / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)],
               append_images=frames[:2])
print("favicon.ico")
