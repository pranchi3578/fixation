"""
Doodles: ballpoint lines and marker fills on a notebook page, animated the
way hand-drawn animation is -- every frame is redrawn, so every line
wobbles a little ("line boil").

Coordinates are normalised: (0,0) top-left, (1,1) bottom-right of a square
page. Drawing happens at SS x the output size and is shrunk at the end,
which is what makes the ink soft-edged rather than pixel-hard.
"""

import math
import os
import zlib

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONTS = os.path.join(os.path.dirname(__file__), "..", "fonts")

INK = (38, 52, 128)          # blue ballpoint
DARK = (28, 28, 40)          # black marker
RED = (205, 40, 38)
TEAL = (31, 217, 199)        # placeholder for Brainback's colour
SKIN = (196, 140, 104)
SHIRT = (150, 190, 235)
PINK = (240, 140, 150)


def _seed(*parts):
    return zlib.crc32(repr(parts).encode()) & 0xFFFFFFFF


# -------------------------------------------------------------- shapes ----

def ellipse(cx, cy, rx, ry, a0=0.0, a1=360.0, n=48, overshoot=12.0):
    """A drawn ellipse: the pen goes a little past where it started."""
    a1 = a1 + (overshoot if a1 - a0 >= 360 else 0)
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


def smooth(pts, n=8):
    """Catmull-Rom through the given points."""
    p = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = map(np.array, (p[i - 1], p[i], p[i + 1], p[i + 2]))
        for k in range(n):
            t = k / n
            out.append(tuple(0.5 * ((2 * p1) + (-p0 + p2) * t
                                    + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                                    + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3)))
    out.append(tuple(pts[-1]))
    return out


def rrect(x0, y0, x1, y1, r, n=6):
    pts = []
    for cx, cy, a in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0),
                      (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        pts += ellipse(cx, cy, r, r, a, a + 90, n, 0)
    return pts + [pts[0]]


# ---------------------------------------------------------------- page ----

class Page:
    def __init__(self, paper_png, size=1080, ss=2, frame=0):
        self.size, self.ss, self.S = size, ss, size * ss
        bg = Image.open(paper_png).convert("RGB")
        side = min(bg.size)
        bg = bg.crop((0, 0, side, side)).resize((self.S, self.S),
                                               Image.BICUBIC)
        self.base = np.asarray(bg, np.float32) / 255
        self.ink = Image.new("RGBA", (self.S, self.S), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.ink)
        self.frame = frame

    def px(self, p):
        return (p[0] * self.S, p[1] * self.S)

    # a line, redrawn by hand every frame
    def stroke(self, pts, key, width=2.6, color=INK, boil=1.0, reveal=1.0,
               alpha=235):
        pts = [self.px(p) for p in pts]
        if len(pts) < 2:
            return
        seg = np.array(pts, np.float32)
        d = np.r_[0, np.cumsum(np.hypot(*np.diff(seg, axis=0).T))]
        total = d[-1]
        if total < 1:
            return
        step = 3.0 * self.ss
        s = np.linspace(0, total, max(2, int(total / step)))
        s = s[s <= total * reveal]
        if len(s) < 2:
            return
        x = np.interp(s, d, seg[:, 0])
        y = np.interp(s, d, seg[:, 1])
        rng = np.random.default_rng(_seed(key, self.frame))
        amp = boil * 1.1 * self.ss
        f1, f2 = rng.uniform(1.5, 3.5, 2)
        ph = rng.uniform(0, 6.28, 4)
        u = s / max(total, 1)
        x = x + amp * (np.sin(6.28 * f1 * u + ph[0])
                       + 0.4 * np.sin(6.28 * 7 * u + ph[2]))
        y = y + amp * (np.cos(6.28 * f2 * u + ph[1])
                       + 0.4 * np.cos(6.28 * 6 * u + ph[3]))
        taper = np.minimum(1, np.minimum(u, 1 - u) / 0.06) ** 0.5
        press = 0.8 + 0.2 * np.sin(6.28 * rng.uniform(1, 3) * u + ph[1])
        w = width * self.ss * press * (0.45 + 0.55 * taper)
        c = (*color, alpha)
        for i in range(len(x) - 1):
            self.draw.line((x[i], y[i], x[i + 1], y[i + 1]), fill=c,
                           width=max(1, int(round(w[i]))))
            r = w[i] / 2
            self.draw.ellipse((x[i] - r, y[i] - r, x[i] + r, y[i] + r),
                              fill=c)

    # a marker or pencil fill: goes over the lines, never quite inside
    def fill(self, pts, key, color, alpha=0.55, boil=1.0, grain=0.25):
        rng = np.random.default_rng(_seed(key, self.frame, "fill"))
        m = Image.new("L", (self.S, self.S), 0)
        j = boil * 2.0 * self.ss
        off = rng.normal(0, j, 2)
        ImageDraw.Draw(m).polygon(
            [(x * self.S + off[0] + rng.normal(0, j * 0.4),
              y * self.S + off[1] + rng.normal(0, j * 0.4)) for x, y in pts],
            fill=255)
        m = np.asarray(m.filter(ImageFilter.GaussianBlur(1.2 * self.ss)),
                       np.float32) / 255
        if grain:
            g = rng.random((self.S // 4, self.S // 4)).astype(np.float32)
            g = np.asarray(Image.fromarray((g * 255).astype(np.uint8))
                           .resize((self.S, self.S), Image.BILINEAR),
                           np.float32) / 255
            m = m * (1 - grain + grain * g)
        col = np.array(color, np.float32) / 255
        a = (m * alpha)[..., None]
        self.base = self.base * (1 - a) + self.base * col * a   # multiply

    def text(self, s, at, size, key, color=INK, bold=True, reveal=1.0,
             angle=-4.0):
        """Handwriting: Caveat, nudged per frame so it boils with the rest."""
        font = ImageFont.truetype(os.path.join(
            FONTS, f"caveat-latin-{700 if bold else 400}-normal.woff"),
            int(size * self.S))
        rng = np.random.default_rng(_seed(key, self.frame, "text"))
        layer = Image.new("RGBA", (self.S, self.S), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        x, y = self.px(at)
        x += rng.normal(0, 0.8 * self.ss)
        y += rng.normal(0, 0.8 * self.ss)
        d.text((x, y), s, font=font, fill=(*color, 240), anchor="mm")
        if reveal < 1:
            bbox = d.textbbox((x, y), s, font=font, anchor="mm")
            cut = bbox[0] + (bbox[2] - bbox[0]) * reveal
            layer.paste((0, 0, 0, 0), (int(cut), 0, self.S, self.S))
        layer = layer.rotate(angle + rng.normal(0, 0.3), center=(x, y),
                             resample=Image.BICUBIC)
        self.ink.alpha_composite(layer)

    def render(self, path):
        img = Image.fromarray((np.clip(self.base, 0, 1) * 255)
                              .astype(np.uint8)).convert("RGBA")
        img.alpha_composite(self.ink)
        img = img.convert("RGB").resize((self.size, self.size),
                                        Image.LANCZOS)
        img.save(path)
        return img
