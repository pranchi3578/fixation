"""
Paper stocks, made rather than photographed.

Every stock is two maps: colour (RGBA, alpha carries torn edges) and height
(for bump). Everything is seeded, so a stock renders identically every time
and a re-render months later matches the shots around it.

Scale: PX_PER_CM pixels per centimetre of real paper. A Doubtling is folded
from an A6 half-page, 10.5 x 14.8 cm.
"""

import os

import numpy as np
from PIL import Image, ImageFilter

PX_PER_CM = 96
OUT = os.path.join(os.path.dirname(__file__), "..", "build", "tex")


# ---------------------------------------------------------------- noise ----

def _value_noise(h, w, cell, rng):
    """Smooth noise: random lattice, bicubic-upsampled."""
    gh, gw = max(2, h // cell + 2), max(2, w // cell + 2)
    grid = rng.random((gh, gw)).astype(np.float32)
    img = Image.fromarray((grid * 255).astype(np.uint8)).resize(
        (gw * cell, gh * cell), Image.BICUBIC)
    return np.asarray(img, np.float32)[:h, :w] / 255.0


def _fbm(h, w, rng, cells=(96, 48, 24, 12, 6, 3), falloff=0.55):
    out = np.zeros((h, w), np.float32)
    amp, total = 1.0, 0.0
    for c in cells:
        out += amp * _value_noise(h, w, c, rng)
        total += amp
        amp *= falloff
    return out / total


def _fibres(h, w, rng, count):
    """Short pale strands: what separates paper from a flat colour."""
    img = Image.new("L", (w, h), 0)
    px = img.load()
    for _ in range(count):
        x, y = rng.random() * w, rng.random() * h
        ang = rng.random() * np.pi
        length = 6 + rng.random() * 30
        dx, dy = np.cos(ang), np.sin(ang)
        bend = (rng.random() - 0.5) * 0.08
        for t in range(int(length)):
            xi, yi = int(x) % w, int(y) % h
            px[xi, yi] = min(255, px[xi, yi] + 60)
            x, y = x + dx, y + dy
            dx, dy = dx - dy * bend, dy + dx * bend
    return np.asarray(img.filter(ImageFilter.GaussianBlur(0.6)),
                      np.float32) / 255.0


def _base(h, w, rng, tint, fibre_density=1.0):
    """Paper body: colour field, mottling, fibres. Returns rgb, height."""
    mottle = _fbm(h, w, rng)
    fib = _fibres(h, w, rng, int(h * w / 900 * fibre_density))
    tooth = rng.random((h, w)).astype(np.float32)
    tooth = np.asarray(Image.fromarray((tooth * 255).astype(np.uint8))
                       .filter(ImageFilter.GaussianBlur(0.7)), np.float32) / 255
    shade = 1.0 + (mottle - 0.5) * 0.06 + fib * 0.05 - (tooth - 0.5) * 0.03
    rgb = np.clip(np.array(tint, np.float32)[None, None, :] * shade[..., None],
                  0, 1)
    height = 0.55 * tooth + 0.3 * mottle + 0.4 * fib
    return rgb, height


def _ink(rgb, mask, colour, strength=1.0):
    """Printed ink sits in the paper, so it multiplies rather than covers."""
    c = np.array(colour, np.float32)[None, None, :]
    m = np.clip(mask * strength, 0, 1)[..., None]
    return rgb * (1 - m) + rgb * c * m


def _hline(h, w, y, width, rng, wobble=0.35):
    """A printed rule: slightly uneven density along its length."""
    yy = np.arange(h, dtype=np.float32)[:, None]
    along = 0.8 + 0.2 * _value_noise(1, w, 40, rng)[0][None, :]
    d = np.abs(yy - y - wobble * np.sin(np.arange(w) / 170.0)[None, :])
    return np.clip(1.0 - (d - width / 2), 0, 1) * along


def _vline(h, w, x, width, rng):
    return _hline(w, h, x, width, rng).T


def _torn_edge_alpha(h, w, rng, side="left", depth_px=10):
    """Alpha with one torn side, the way a page leaves a notebook."""
    a = np.ones((h, w), np.float32)
    n = h if side in ("left", "right") else w
    edge = (_value_noise(1, n, 24, rng)[0] * 0.7
            + _value_noise(1, n, 5, rng)[0] * 0.3) * depth_px
    idx = np.arange(w if side in ("left", "right") else h,
                    dtype=np.float32)
    if side == "left":
        a = np.clip(idx[None, :] - edge[:, None], 0, 1)
    elif side == "top":
        a = np.clip(idx[:, None] - edge[None, :], 0, 1)
    return a


def _save(name, rgb, height, alpha=None):
    os.makedirs(OUT, exist_ok=True)
    a = np.ones(rgb.shape[:2], np.float32) if alpha is None else alpha
    rgba = np.dstack([rgb, a])
    Image.fromarray((rgba * 255).astype(np.uint8), "RGBA").save(
        os.path.join(OUT, f"{name}_col.png"))
    hmin, hmax = height.min(), height.max()
    hn = (height - hmin) / max(1e-6, hmax - hmin)
    Image.fromarray((hn * 255).astype(np.uint8), "L").save(
        os.path.join(OUT, f"{name}_hgt.png"))
    return os.path.join(OUT, f"{name}_col.png")


# --------------------------------------------------------------- stocks ----

def ruled(w_cm=10.5, h_cm=14.8, seed=1, torn=True):
    """Indian school notebook: pale blue rules, red double margin."""
    rng = np.random.default_rng(seed)
    h, w = int(h_cm * PX_PER_CM), int(w_cm * PX_PER_CM)
    rgb, height = _base(h, w, rng, (0.955, 0.945, 0.915))
    pitch = 0.8 * PX_PER_CM
    lines = np.zeros((h, w), np.float32)
    y = 1.6 * PX_PER_CM
    while y < h:
        lines = np.maximum(lines, _hline(h, w, y, 1.6, rng))
        y += pitch
    rgb = _ink(rgb, lines, (0.55, 0.72, 0.95), 0.75)
    mx = 2.2 * PX_PER_CM
    margin = np.maximum(_vline(h, w, mx, 1.6, rng),
                        _vline(h, w, mx + 5, 1.2, rng))
    rgb = _ink(rgb, margin, (0.95, 0.35, 0.35), 0.8)
    alpha = _torn_edge_alpha(h, w, rng, "left") if torn else None
    return _save(f"ruled_{seed}", rgb, height, alpha)


def graph(w_cm=10.5, h_cm=14.8, seed=2):
    """Maths graph paper: 1 mm green grid, heavier every centimetre."""
    rng = np.random.default_rng(seed)
    h, w = int(h_cm * PX_PER_CM), int(w_cm * PX_PER_CM)
    rgb, height = _base(h, w, rng, (0.95, 0.95, 0.92))
    mm = PX_PER_CM / 10
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)

    def grid(step, width):
        dy = np.abs(((yy + step / 2) % step) - step / 2)
        dx = np.abs(((xx + step / 2) % step) - step / 2)
        return np.clip(1 - (np.minimum(dx, dy) - width / 2), 0, 1)

    rgb = _ink(rgb, grid(mm, 0.7), (0.55, 0.8, 0.6), 0.35)
    rgb = _ink(rgb, grid(10 * mm, 1.5), (0.4, 0.7, 0.5), 0.7)
    return _save(f"graph_{seed}", rgb, height, _torn_edge_alpha(h, w, rng))


def sugar(w_cm=30, h_cm=30, seed=3, tint=(0.52, 0.52, 0.55), name="sugar"):
    """Coloured sugar paper: soft, flecked, heavy fibre."""
    rng = np.random.default_rng(seed)
    h, w = int(h_cm * PX_PER_CM / 2), int(w_cm * PX_PER_CM / 2)
    rgb, height = _base(h, w, rng, tint, fibre_density=2.5)
    flecks = (rng.random((h, w)) > 0.9985).astype(np.float32)
    flecks = np.asarray(Image.fromarray((flecks * 255).astype(np.uint8))
                        .filter(ImageFilter.GaussianBlur(1.2)),
                        np.float32) / 255 * 3
    rgb = np.clip(rgb * (1 - 0.25 * np.clip(flecks, 0, 1)[..., None]), 0, 1)
    return _save(f"{name}_{seed}", rgb, height)


def card(w_cm=40, h_cm=40, seed=4, tint=(0.80, 0.70, 0.55), name="card"):
    """Kraft card for floors, desks, the tabletop itself."""
    rng = np.random.default_rng(seed)
    h, w = int(h_cm * PX_PER_CM / 3), int(w_cm * PX_PER_CM / 3)
    rgb, height = _base(h, w, rng, tint, fibre_density=3.0)
    return _save(f"{name}_{seed}", rgb, height)


def swatch_sheet(path):
    """All stocks side by side, for approval."""
    names = ["ruled_1", "graph_2", "sugar_3", "card_4"]
    tiles = []
    for n in names:
        im = Image.open(os.path.join(OUT, f"{n}_col.png")).convert("RGBA")
        im = im.crop((0, 0, min(im.width, 700), min(im.height, 900)))
        bg = Image.new("RGBA", im.size, (40, 40, 44, 255))
        tiles.append(Image.alpha_composite(bg, im).convert("RGB"))
    W = sum(t.width for t in tiles) + 20 * (len(tiles) + 1)
    H = max(t.height for t in tiles) + 40
    sheet = Image.new("RGB", (W, H), (40, 40, 44))
    x = 20
    for t in tiles:
        sheet.paste(t, (x, 20))
        x += t.width + 20
    sheet.save(path, quality=90)


if __name__ == "__main__":
    ruled()
    graph()
    sugar()
    card()
    swatch_sheet(os.path.join(OUT, "..", "swatches.jpg"))
    print("ok")
