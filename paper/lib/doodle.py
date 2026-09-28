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
        self.tf = [(0.0, 0.0, 1.0)]     # (ox, oy, scale), composed
        self.clip = None                # pixel rect, while clipping
        self._clips = []

    # ---------------------------------------------------- transforms ----
    def push(self, ox, oy, s):
        """Draw the next things into a sub-frame: p -> (ox,oy) + s*p."""
        cx, cy, cs = self.tf[-1]
        self.tf.append((cx + cs * ox, cy + cs * oy, cs * s))

    def push_rect(self, src, dst):
        """Map rect src (x0,y0,x1,y1) onto rect dst, uniform scale by width."""
        s = (dst[2] - dst[0]) / (src[2] - src[0])
        self.push(dst[0] - src[0] * s, dst[1] - src[1] * s, s)

    def pop(self):
        self.tf.pop()

    @property
    def scale(self):
        return self.tf[-1][2]

    def begin_clip(self, rect):
        """Until end_clip, nothing lands outside rect (current coords).
        Clips nest: an inner clip is intersected with the outer one."""
        a, b = self.px(rect[:2]), self.px(rect[2:])
        c = (max(0, int(a[0])), max(0, int(a[1])),
             min(self.S, int(b[0])), min(self.S, int(b[1])))
        if self.clip:
            c = (max(c[0], self.clip[0]), max(c[1], self.clip[1]),
                 min(c[2], self.clip[2]), min(c[3], self.clip[3]))
        self._clips.append((self.ink, self.draw, self.clip))
        self.clip = c
        self.ink = Image.new("RGBA", (self.S, self.S), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.ink)

    def end_clip(self):
        x0, y0, x1, y1 = self.clip
        inner = self.ink
        self.ink, self.draw, self.clip = self._clips.pop()
        if x1 > x0 and y1 > y0:
            self.ink.alpha_composite(inner.crop((x0, y0, x1, y1)), (x0, y0))

    def px(self, p):
        ox, oy, sc = self.tf[-1]
        return ((ox + sc * p[0]) * self.S, (oy + sc * p[1]) * self.S)

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
        k = min(1.6, max(0.35, self.scale))
        amp = boil * 1.1 * self.ss * k
        f1, f2 = rng.uniform(1.5, 3.5, 2)
        ph = rng.uniform(0, 6.28, 4)
        u = s / max(total, 1)
        x = x + amp * (np.sin(6.28 * f1 * u + ph[0])
                       + 0.4 * np.sin(6.28 * 7 * u + ph[2]))
        y = y + amp * (np.cos(6.28 * f2 * u + ph[1])
                       + 0.4 * np.cos(6.28 * 6 * u + ph[3]))
        taper = np.minimum(1, np.minimum(u, 1 - u) / 0.06) ** 0.5
        press = 0.8 + 0.2 * np.sin(6.28 * rng.uniform(1, 3) * u + ph[1])
        w = width * self.ss * min(1.6, max(0.4, self.scale)) * press * \
            (0.45 + 0.55 * taper)
        c = (*color, alpha)
        for i in range(len(x) - 1):
            self.draw.line((x[i], y[i], x[i + 1], y[i + 1]), fill=c,
                           width=max(1, int(round(w[i]))))
            r = w[i] / 2
            self.draw.ellipse((x[i] - r, y[i] - r, x[i] + r, y[i] + r),
                              fill=c)

    # a marker or pencil fill: goes over the lines, never quite inside
    def fill(self, pts, key, color, alpha=0.55, boil=1.0, grain=0.25):
        if alpha <= 0:
            return
        rng = np.random.default_rng(_seed(key, self.frame, "fill"))
        k = min(1.6, max(0.35, self.scale))
        j = boil * 2.0 * self.ss * k
        off = rng.normal(0, j, 2)
        P = np.array([self.px(p) for p in pts], np.float32)
        P += off + rng.normal(0, j * 0.4, P.shape)
        pad = int(6 * self.ss)
        x0, y0 = np.floor(P.min(0)).astype(int) - pad
        x1, y1 = np.ceil(P.max(0)).astype(int) + pad
        cx0, cy0, cx1, cy1 = self.clip or (0, 0, self.S, self.S)
        x0, y0 = max(x0, cx0), max(y0, cy0)
        x1, y1 = min(x1, cx1), min(y1, cy1)
        if x1 <= x0 or y1 <= y0:
            return
        m = Image.new("L", (x1 - x0, y1 - y0), 0)
        ImageDraw.Draw(m).polygon([(x - x0, y - y0) for x, y in P], fill=255)
        m = np.asarray(m.filter(ImageFilter.GaussianBlur(1.2 * self.ss * k)),
                       np.float32) / 255
        if grain:
            h, w = m.shape
            g = rng.random((max(2, h // 4), max(2, w // 4))).astype(np.float32)
            g = np.asarray(Image.fromarray((g * 255).astype(np.uint8))
                           .resize((w, h), Image.BILINEAR), np.float32) / 255
            m = m * (1 - grain + grain * g)
        col = np.array(color, np.float32) / 255
        a = (m * alpha)[..., None]
        reg = self.base[y0:y1, x0:x1]
        self.base[y0:y1, x0:x1] = reg * (1 - a) + reg * col * a  # multiply

    def cover(self, pts, key, color, alpha=0.92):
        """Opaque marker over everything drawn so far (lines included)."""
        rng = np.random.default_rng(_seed(key, self.frame, "cover"))
        j = 1.5 * self.ss
        P = [(x + rng.normal(0, j), y + rng.normal(0, j))
             for x, y in (self.px(p) for p in pts)]
        layer = Image.new("RGBA", (self.S, self.S), (0, 0, 0, 0))
        ImageDraw.Draw(layer).polygon(P, fill=(*color, int(255 * alpha)))
        if self.clip:
            x0, y0, x1, y1 = self.clip
            m = Image.new("L", (self.S, self.S), 0)
            m.paste(255, (x0, y0, x1, y1))
            layer.putalpha(Image.fromarray(np.minimum(
                np.asarray(layer.getchannel("A")), np.asarray(m))))
        self.ink.alpha_composite(layer)

    def text(self, s, at, size, key, color=INK, bold=True, reveal=1.0,
             angle=-4.0, alpha=240):
        """Handwriting: Caveat, nudged per frame so it boils with the rest."""
        px_size = int(size * self.S * self.scale)
        if px_size < 4:
            return
        font = ImageFont.truetype(os.path.join(
            FONTS, f"caveat-latin-{700 if bold else 400}-normal.woff"),
            px_size)
        rng = np.random.default_rng(_seed(key, self.frame, "text"))
        x, y = self.px(at)
        x += rng.normal(0, 0.8 * self.ss)
        y += rng.normal(0, 0.8 * self.ss)
        l, t, r, b = font.getbbox(s, anchor="mm")
        pad = int(px_size * 0.4)
        W, H = int(r - l) + 2 * pad, int(b - t) + 2 * pad
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        d.text((W / 2, H / 2), s, font=font, fill=(*color, alpha),
               anchor="mm")
        if reveal < 1:
            cut = pad + (r - l) * max(0.0, reveal)
            layer.paste((0, 0, 0, 0), (int(cut), 0, W, H))
        layer = layer.rotate(angle + rng.normal(0, 0.3), expand=True,
                             resample=Image.BICUBIC)
        px0, py0 = int(x - layer.width / 2), int(y - layer.height / 2)
        box = (px0, py0, px0 + layer.width, py0 + layer.height)
        cx0, cy0, cx1, cy1 = self.clip or (0, 0, self.S, self.S)
        ix0, iy0 = max(box[0], cx0), max(box[1], cy0)
        ix1, iy1 = min(box[2], cx1), min(box[3], cy1)
        if ix1 > ix0 and iy1 > iy0:
            piece = layer.crop((ix0 - px0, iy0 - py0, ix1 - px0, iy1 - py0))
            self.ink.alpha_composite(piece, (ix0, iy0))

    def render(self, path, post=None):
        """post(rgb float array HxWx3 in 0..1) -> same, applied to the whole
        drawing: lighting passes such as night and lamplight."""
        img = Image.fromarray((np.clip(self.base, 0, 1) * 255)
                              .astype(np.uint8)).convert("RGBA")
        img.alpha_composite(self.ink)
        if post is not None:
            a = np.asarray(img.convert("RGB"), np.float32) / 255
            a = np.clip(post(a), 0, 1)
            img = Image.fromarray((a * 255).astype(np.uint8)).convert("RGBA")
        img = img.convert("RGB").resize((self.size, self.size),
                                        Image.LANCZOS)
        img.save(path)
        return img
