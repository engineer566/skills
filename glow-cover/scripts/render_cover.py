#!/usr/bin/env python3
"""Render a black-background glowing-text tech cover image (WeChat 公众号封面风格).

Layout (all measurements are fractions of canvas height H, width W):
  - kicker   (top line,    regular weight) center y = 0.294H
  - title    (middle line, bold + bloom)   center y = 0.471H, flanked by two light beams
  - subtitle (bottom line, regular weight) center y = 0.649H
Mixed CJK/Latin text is shaped run-by-run: CJK -> Noto Sans CJK SC, Latin -> Liberation Sans.
"""

import argparse
import re

from PIL import Image, ImageDraw, ImageFilter, ImageFont

CJK_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
CJK_REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
LATIN_BOLD = "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"
LATIN_REG = "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"

_CJK_RE = re.compile(
    r"[一-鿿㐀-䶿豈-﫿　-〿＀-￯–—…·「」『』（）《》]"
)


def _sc_index(path: str) -> int:
    """Find the 'Noto Sans CJK SC' face index inside a .ttc collection."""
    for i in range(10):
        try:
            if "SC" in ImageFont.truetype(path, 20, index=i).getname()[0]:
                return i
        except Exception:
            break
    return 2  # fallback: SC is index 2 in Noto Sans CJK ttc builds


def _is_cjk(ch: str) -> bool:
    return bool(_CJK_RE.match(ch))


class RunShaper:
    """Split mixed text into (text, font) runs and measure/draw them."""

    def __init__(self, size: int, bold: bool):
        cjk_path, latin_path = (
            (CJK_BOLD, LATIN_BOLD) if bold else (CJK_REG, LATIN_REG)
        )
        idx = _sc_index(cjk_path)
        self.cjk = ImageFont.truetype(cjk_path, size, index=idx)
        self.latin = ImageFont.truetype(latin_path, size)
        self.size = size

    def runs(self, text: str):
        runs, buf, cur = [], "", None
        for ch in text:
            kind = _is_cjk(ch)
            if cur is None or kind == cur:
                buf += ch
                cur = kind
            else:
                runs.append((buf, cur))
                buf, cur = ch, kind
        if buf:
            runs.append((buf, cur))
        return [(t, self.cjk if cjk else self.latin) for t, cjk in runs]

    def width(self, text: str) -> float:
        return sum(f.getlength(t) for t, f in self.runs(text))

    def height(self, text: str) -> float:
        asc = desc = 0
        for _, f in self.runs(text):
            a, d = f.getmetrics()
            asc, desc = max(asc, a), max(desc, d)
        return asc + desc

    def draw(self, draw: ImageDraw.ImageDraw, x: float, y: float, text: str, fill):
        """Draw with left edge at x, *visual center* (mid of asc+desc) at y."""
        asc = desc = 0
        for _, f in self.runs(text):
            a, d = f.getmetrics()
            asc, desc = max(asc, a), max(desc, d)
        baseline = y + (asc - desc) / 2  # common baseline; visual center lands on y
        for t, f in self.runs(text):
            a, _ = f.getmetrics()
            # draw.text y is the top of THIS font's ascender box -> baseline - a.
            # Each run uses its own ascent so CJK and Latin share one baseline.
            draw.text((x, baseline - a), t, font=f, fill=fill)
            x += f.getlength(t)


def fit_size(text: str, start_px: int, max_width: float, bold: bool) -> RunShaper:
    size = start_px
    while size > 12:
        sh = RunShaper(size, bold)
        if sh.width(text) <= max_width:
            return sh
        size = int(size * 0.94)
    return RunShaper(size, bold)


def draw_beam(img: Image.Image, cy: float, cx: float, W: int, H: int):
    """One horizontal light beam: crisp bright core + soft glow + wide faint halo."""
    import math

    def envelope(t):  # raised-cosine falloff toward both ends
        return (0.5 - 0.5 * math.cos(2 * math.pi * t)) ** 0.7

    for half_w, thickness, blur, alpha in (
        (0.45 * W, max(2, int(0.003 * H)), 0.022 * H, 55),    # wide halo
        (0.225 * W, max(3, int(0.006 * H)), 0.009 * H, 170),  # glow
        (0.225 * W, max(1, int(0.0018 * H)), 0.0012 * H, 255),  # crisp core
    ):
        layer = Image.new("L", (W, H), 0)
        d = ImageDraw.Draw(layer)
        x0, x1 = cx - half_w, cx + half_w
        steps = 400
        for i in range(steps + 1):
            t = i / steps
            x = x0 + (x1 - x0) * t
            d.line([(x, cy - thickness / 2), (x, cy + thickness / 2)],
                   fill=int(alpha * envelope(t)))
        layer = layer.filter(ImageFilter.GaussianBlur(blur))
        img.paste(Image.new("RGB", (W, H), (255, 255, 255)), (0, 0), layer)


def draw_title_glow(img: Image.Image, cx: float, cy: float, W: int, H: int):
    """Very faint radial glow filling the title block."""
    layer = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(layer)
    rx, ry = 0.36 * W, 0.13 * H
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=46)
    layer = layer.filter(ImageFilter.GaussianBlur(0.06 * H))
    img.paste(Image.new("RGB", (W, H), (255, 255, 255)), (0, 0), layer)


def draw_text_line(img: Image.Image, sh: RunShaper, text: str, cy: float,
                   W: int, H: int, bloom: bool):
    x = (W - sh.width(text)) / 2
    if bloom:  # blurred white copy underneath -> soft halo around glyphs
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        sh.draw(d, x, cy, text, (255, 255, 255, 200))
        layer = layer.filter(ImageFilter.GaussianBlur(0.009 * H))
        img.paste(Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img)
    sh.draw(d, x, cy, text, (255, 255, 255))


def render(title: str, kicker: str = "", subtitle: str = "", out: str = "cover.png",
           width: int = 2848, height: int = 1600, beam: bool = True):
    W, H = width, height
    img = Image.new("RGB", (W, H), (0, 0, 0))
    cx = W / 2

    # positions: full 3-line layout; degrade gracefully when lines are missing
    if kicker and subtitle:
        y_k, y_t, y_s = 0.294 * H, 0.471 * H, 0.649 * H
    elif kicker:
        y_k, y_t, y_s = 0.35 * H, 0.53 * H, None
    elif subtitle:
        y_k, y_t, y_s = None, 0.44 * H, 0.62 * H
    else:
        y_k, y_t, y_s = None, 0.5 * H, None

    title_sh = fit_size(title, int(0.122 * H), 0.92 * W, bold=True)
    if beam:  # beams hug the title block: measured offset ±0.094H from title center
        draw_title_glow(img, cx, y_t, W, H)
        draw_beam(img, y_t - 0.094 * H, cx, W, H)
        draw_beam(img, y_t + 0.094 * H, cx, W, H)

    if kicker:
        draw_text_line(img, fit_size(kicker, int(0.094 * H), 0.9 * W, bold=False),
                       kicker, y_k, W, H, bloom=False)
    draw_text_line(img, title_sh, title, y_t, W, H, bloom=True)
    if subtitle:
        draw_text_line(img, fit_size(subtitle, int(0.094 * H), 0.9 * W, bold=False),
                       subtitle, y_s, W, H, bloom=False)

    img.save(out, quality=95)
    return out


def main():
    p = argparse.ArgumentParser(description="Render a glowing-text tech cover image.")
    p.add_argument("--title", required=True, help="Main title (bold, glowing). Keep model/brand names exact.")
    p.add_argument("--kicker", default="", help="Top line, regular weight.")
    p.add_argument("--subtitle", default="", help="Bottom line, regular weight.")
    p.add_argument("--out", default="cover.png", help="Output path (.png/.jpg).")
    p.add_argument("--width", type=int, default=2848)
    p.add_argument("--height", type=int, default=1600)
    p.add_argument("--no-beam", action="store_true", help="Disable light beams and title glow.")
    a = p.parse_args()
    print(render(a.title, a.kicker, a.subtitle, a.out, a.width, a.height, not a.no_beam))


if __name__ == "__main__":
    main()
