"""Build the TVT logo set as pure-path SVG (no font dependency).

Fonts (SIL OFL): Cormorant Garamond (monogram + wordmark), Montserrat (tagline).
Run:  python build_logo.py      -> writes SVGs into ./svg
"""
import os
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.transformPen import TransformPen
import pathops

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "_fonts")
OUT = os.path.join(HERE, "svg")
os.makedirs(OUT, exist_ok=True)

# ---- palette -------------------------------------------------------------
NAVY, GOLD, IVORY, GRAPHITE = "#0F2D44", "#B69A68", "#F4F2EC", "#292929"

# ---- text content --------------------------------------------------------
NAME = "TALQIN VA TADQIQOTLAR"
TAGLINE = "ILMIY-USLUBIY JURNAL  •  ISSN 2181-3035"

# ---- monogram parameters (font units, cap height = 625) ------------------
MONO_WGHT = 700
V_SCALE = 1.30      # V is taller than the T's
OVERLAP = 0.50      # how far each T slides under the V (fraction of T width)
GAP = 16            # knock-out gap between V and the T's (0 = merged)


_cache = {}
def font(name, wght):
    key = (name, wght)
    if key not in _cache:
        f = TTFont(os.path.join(FONTS, name))
        _cache[key] = instantiateVariableFont(f, {"wght": wght})
    return _cache[key]


def glyph(f, ch, x=0.0, y=0.0, s=1.0):
    """Glyph outline as pathops.Path, scaled by s and moved to (x, y). y-up."""
    gs = f.getGlyphSet()
    gname = f.getBestCmap()[ord(ch)]
    p = pathops.Path()
    gs[gname].draw(TransformPen(p.getPen(), (s, 0, 0, s, x, y)))
    return p, gs[gname].width * s


def union(paths):
    out = pathops.Path()
    for p in paths:
        out = pathops.op(out, p, pathops.PathOp.UNION)
    return out


def bounds(p):
    return p.bounds  # (xmin, ymin, xmax, ymax)


def dilate(p, r, steps=16):
    """Approximate outward offset by r: union of copies shifted around a circle."""
    import math
    copies = [p]
    for i in range(steps):
        a = 2 * math.pi * i / steps
        q = p.transform(1, 0, 0, 1, r * math.cos(a), r * math.sin(a))
        copies.append(q)
    return union(copies)


def to_d(p, ox, oy, k):
    """pathops.Path -> SVG d. Flips y; maps font (x,y) to (ox + k*x, oy - k*y)."""
    def pt(xy):
        return f"{ox + k * xy[0]:.2f} {oy - k * xy[1]:.2f}"
    d = []
    for verb, pts in p.segments:
        if verb == "moveTo":
            d.append("M" + pt(pts[0]))
        elif verb == "lineTo":
            d.append("L" + pt(pts[0]))
        elif verb == "qCurveTo":
            # TrueType-style: n off-curve points + final on-curve, with implied
            # on-curve midpoints between consecutive off-curve points.
            offs, end = pts[:-1], pts[-1]
            for i, c in enumerate(offs):
                if i + 1 < len(offs):
                    n = offs[i + 1]
                    nxt = ((c[0] + n[0]) / 2, (c[1] + n[1]) / 2)
                else:
                    nxt = end
                d.append("Q" + pt(c) + " " + pt(nxt))
        elif verb == "curveTo":
            d.append("C" + " ".join(pt(q) for q in pts))
        elif verb in ("closePath", "endPath"):
            d.append("Z")
    return "".join(d)


# ---- monogram ------------------------------------------------------------
def monogram(wght=MONO_WGHT, v_scale=V_SCALE, overlap=OVERLAP, gap=GAP):
    f = font("CormorantGaramond[wght].ttf", wght)
    t_probe, _ = glyph(f, "T")
    tx0, _, tx1, _ = bounds(t_probe)
    tw = tx1 - tx0
    v, _ = glyph(f, "V", s=v_scale)
    vx0, vy0, vx1, _ = bounds(v)
    vw = vx1 - vx0
    # shift V so its baseline point sits on the baseline (y=0)
    v = v.transform(1, 0, 0, 1, -vx0, -vy0)
    left_t, _ = glyph(f, "T", x=-tx0 - tw + overlap * tw)
    right_t, _ = glyph(f, "T", x=-tx0 + vw - overlap * tw)
    ts = union([left_t, right_t])
    if gap:
        ts = pathops.op(ts, dilate(v, gap), pathops.PathOp.DIFFERENCE)
        ts = drop_slivers(ts, min_area=0.03 * tw * 650)
    m = union([ts, v])
    return m


def drop_slivers(p, min_area):
    """Remove tiny leftover contours (bbox area < min_area) produced by the knock-out."""
    out = pathops.Path()
    for c in p.contours:
        x0, y0, x1, y1 = c.bounds
        if (x1 - x0) * (y1 - y0) >= min_area:
            out = pathops.op(out, c, pathops.PathOp.UNION)
    return out


# ---- text line (outlined, with letter-spacing) -----------------------------
def text_line(fname, wght, s, tracking, size):
    """Return (path, width) for string s at `size` font-units-per-em scaled to `size`."""
    f = font(fname, wght)
    upm = f["head"].unitsPerEm
    k = size / upm
    cmap = f.getBestCmap()
    gs = f.getGlyphSet()
    x = 0.0
    parts = []
    for i, ch in enumerate(s):
        if ch == " ":
            x += gs[cmap[32]].width * k + tracking
            continue
        p, adv = glyph(f, ch, x=x, s=k)
        parts.append(p)
        x += adv + (tracking if i < len(s) - 1 else 0)
    return union(parts), x


def write_svg(name, w, h, layers, bg=None, radius=0):
    """layers: list of (d, fill)."""
    body = []
    if bg:
        body.append(f'<rect width="{w:.0f}" height="{h:.0f}" rx="{radius}" fill="{bg}"/>')
    for d, fill in layers:
        body.append(f'<path fill="{fill}" d="{d}"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" '
           f'width="{w:.0f}" height="{h:.0f}">'
           f'<title>Talqin va tadqiqotlar</title>' + "".join(body) + "</svg>\n")
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(svg)
    return svg


def place(p, x, y_top, height):
    """Scale path p so its bbox height == height, top-left at (x, y_top). Returns (d, width)."""
    x0, y0, x1, y1 = bounds(p)
    k = height / (y1 - y0)
    return to_d(p, x - k * x0, y_top + k * y1, k), (x1 - x0) * k


def build():
    mono = monogram()
    mx0, my0, mx1, my1 = bounds(mono)
    mono_ratio = (mx1 - mx0) / (my1 - my0)

    name_p, _ = text_line("CormorantGaramond[wght].ttf", 600, NAME, 190, 1000)
    tag_p, _ = text_line("Montserrat.ttf", 500, TAGLINE, 330, 1000)

    def ratio(p):
        x0, y0, x1, y1 = bounds(p)
        return (x1 - x0) / (y1 - y0)

    # 1) monogram only ---------------------------------------------------------
    H = 200
    W = H * mono_ratio
    pad = 0
    for suffix, col in (("navy", NAVY), ("gold", GOLD), ("ivory", IVORY), ("graphite", GRAPHITE)):
        d, _ = place(mono, pad, pad, H)
        write_svg(f"tvt-monogram-{suffix}.svg", W + 2 * pad, H + 2 * pad, [(d, col)])

    # 2) stacked full logo --------------------------------------------------------
    W = 1200
    mono_h = 230
    name_h = 38                    # cap height of wordmark
    tag_h = 15
    name_w = name_h * ratio(name_p)
    tag_w = tag_h * ratio(tag_p)
    y = 40
    mono_w = mono_h * mono_ratio
    d_mono, _ = place(mono, (W - mono_w) / 2, y, mono_h)
    y += mono_h + 62
    d_name, _ = place(name_p, (W - name_w) / 2, y, name_h)
    y += name_h + 30
    d_tag, _ = place(tag_p, (W - tag_w) / 2, y, tag_h)
    H = y + tag_h + 40
    for suffix, c1, c2, c3 in (("navy", NAVY, NAVY, GRAPHITE),
                               ("ivory", IVORY, IVORY, IVORY),
                               ("navy-gold", NAVY, NAVY, GOLD)):
        write_svg(f"tvt-logo-stacked-{suffix}.svg", W, H,
                  [(d_mono, c1), (d_name, c2), (d_tag, c3)])

    # 3) horizontal logo (for site header) ---------------------------------------
    mono_h = 120
    mono_w = mono_h * mono_ratio
    name_h = 30
    tag_h = 11.5
    name_w = name_h * ratio(name_p)
    tag_w = tag_h * ratio(tag_p)
    x = 0
    d_mono, _ = place(mono, x, 0, mono_h)
    x += mono_w + 34
    rule_x = x
    x += 34
    block_h = name_h + 24 + tag_h
    y0 = (mono_h - block_h) / 2
    d_name, _ = place(name_p, x, y0, name_h)
    d_tag, _ = place(tag_p, x, y0 + name_h + 24, tag_h)
    W = x + max(name_w, tag_w)
    rule = f"M{rule_x:.2f} 14H{rule_x + 1.5:.2f}V{mono_h - 14:.2f}H{rule_x:.2f}Z"
    for suffix, c1, c2, c3, cr in (("navy", NAVY, NAVY, GRAPHITE, GOLD),
                                   ("ivory", IVORY, IVORY, IVORY, GOLD)):
        write_svg(f"tvt-logo-horizontal-{suffix}.svg", W, mono_h,
                  [(d_mono, c1), (rule, cr), (d_name, c2), (d_tag, c3)])

    # 4) favicon / app icon: ivory monogram on navy tile -------------------------
    fav = monogram(wght=700, v_scale=1.22, overlap=0.42, gap=26)
    fr = ratio(fav)
    S = 512
    w = S * 0.80
    h = w / fr
    d, _ = place(fav, (S - w) / 2, (S - h) / 2 + 8, h)
    write_svg("favicon.svg", S, S, [(d, IVORY)], bg=NAVY, radius=96)
    write_svg("app-icon.svg", S, S, [(d, IVORY)], bg=NAVY, radius=0)

    # 5) small favicon (16-48 px): no knock-out gap, letters fill the tile ------
    small = monogram(wght=700, v_scale=1.12, overlap=0.30, gap=0)
    sr = ratio(small)
    w = S * 0.90
    h = w / sr
    d, _ = place(small, (S - w) / 2, (S - h) / 2 + 6, h)
    write_svg("favicon-small.svg", S, S, [(d, IVORY)], bg=NAVY, radius=72)

    print("monogram ratio", round(mono_ratio, 3), "favicon ratio", round(fr, 3))


if __name__ == "__main__":
    build()
