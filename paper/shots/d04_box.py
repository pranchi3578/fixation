"""
"Unmute", beat 4: the pencil box. Night, top-down on Meera's desk.

  0.0-0.8  A tin pencil box under the lamp. It rattles.
  0.8-1.8  The lid swings open.
  1.8-2.6  It's crammed with crumpled paper: weeks of unasked questions.
           Three spill onto the desk.
  2.6-3.4  One uncrumples into a "?" -- with an eye. It looks around.
  3.6      The laptop at the edge of the desk lights up: Brainback.
  3.8-6.0  The "?" turns and hops toward the light.

Usage: python paper/shots/d04_box.py [first last]
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import numpy as np  # noqa: E402

import doodle as dd  # noqa: E402
import paper  # noqa: E402
from doodle import ellipse, rrect, smooth  # noqa: E402

FPS_UNIQUE = 12
DURATION = 6.0
OUT = os.environ.get("OUT", "paper/build/d04_frames")
RES = int(os.environ.get("RES", 1080))

BOX = (0.14, 0.44, 0.62, 0.66)            # the tin, top-down
TIN = (240, 170, 50)
OPEN0, OPEN1, SPILL, UNCRUMPLE, GLOW, HOP = 0.8, 1.8, 1.9, 2.6, 3.6, 3.8
LAMP = (0.36, 0.52)
SCREEN = (0.68, 0.14, 0.97, 0.40)

NOTES = ["why?", "sin A??", "what is sec?", "how??", "but why", "??",
         "cos 90 = 0 ?", "why 1?"]


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def seg(t, a, b):
    return (t - a) / (b - a)


def lerp(a, b, k):
    return (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)


def paper_ball(pg, key, x, y, r, t, note=None, squash=1.0):
    """A crumpled sheet: a jagged outline and a few angular creases."""
    rng = np.random.default_rng(abs(hash(key)) % (2 ** 32))
    n = 13
    out = []
    for i in range(n + 1):
        a = 2 * math.pi * (i % n) / n + rng.normal(0, 0.12)
        rr = r * (0.82 + 0.3 * rng.random())
        out.append((x + rr * math.cos(a), y + rr * squash * math.sin(a)))
    out[-1] = out[0]
    pg.fill(out, key + "f", (246, 244, 238), 0.95, grain=0.1)
    pg.cover(out, key + "c", (246, 244, 238), 0.97)
    pg.stroke(out, key + "o", 2.0)
    for j in range(4):
        a = rng.uniform(0, 2 * math.pi)
        p0 = (x + 0.15 * r * math.cos(a), y + 0.15 * r * math.sin(a))
        p1 = (x + 0.75 * r * math.cos(a + 0.4), y + 0.75 * r * math.sin(a + 0.4))
        p2 = (x + 0.55 * r * math.cos(a + 1.1), y + 0.55 * r * math.sin(a + 1.1))
        pg.stroke([p0, p1, p2], f"{key}cr{j}", 1.3, alpha=150)
    if note:
        pg.text(note, (x, y), r * 0.62, key + "t", bold=True,
                angle=rng.uniform(-20, 20))


def balls_layout():
    """Where the crumpled questions sit in the box, packed tight."""
    rng = np.random.default_rng(9)
    out = []
    x0, y0, x1, y1 = BOX
    for r in range(2):
        for c in range(7):
            x = x0 + 0.045 + c * (x1 - x0 - 0.09) / 6 + rng.normal(0, 0.006)
            y = y0 + 0.055 + r * (y1 - y0 - 0.11) + rng.normal(0, 0.006)
            out.append((x, y, 0.044 + 0.008 * rng.random()))
    return out


SPILLERS = {2: (0.20, 0.82), 9: (0.36, 0.86), 12: (0.53, 0.83)}
HERO = 9


def desk(pg, t):
    # a notebook and a pencil, left
    nb = [(0.02, 0.06), (0.30, 0.03), (0.33, 0.36), (0.05, 0.39)]
    pg.fill(nb, "nbf", (250, 250, 245), 0.8, grain=0)
    pg.stroke(nb + [nb[0]], "nb")
    for i in range(6):
        a = lerp(nb[0], nb[3], 0.15 + 0.13 * i)
        b = lerp(nb[1], nb[2], 0.15 + 0.13 * i)
        pg.stroke([a, b], f"nbl{i}", 1.4, (120, 150, 210), alpha=180)
    pencil = [(0.08, 0.43), (0.36, 0.38)]
    pg.stroke(pencil, "pc", 6.0, (230, 190, 60))
    pg.stroke([(0.36, 0.38), (0.39, 0.375)], "pct", 3.0, dd.DARK)
    # the laptop, right: keyboard below, screen tipped up above
    base = rrect(0.66, 0.42, 0.99, 0.80, 0.015)
    pg.fill(base, "lbf", (200, 205, 215), 0.6)
    pg.stroke(base, "lb")
    for r in range(4):
        for c in range(7):
            x, y = 0.685 + c * 0.042, 0.46 + r * 0.045
            pg.stroke(rrect(x, y, x + 0.034, y + 0.035, 0.005), f"k{r}{c}",
                      1.4, alpha=170)
    pg.stroke(rrect(0.76, 0.66, 0.89, 0.76, 0.01), "tp", 1.6)
    scr = rrect(*SCREEN, 0.015)
    k = ease(seg(t, GLOW, GLOW + 0.4))
    pg.fill(scr, "scrd", (40, 42, 55), 0.85 * (1 - k))
    pg.fill(scr, "scrg", dd.TEAL, 0.8 * k)
    pg.stroke(scr, "scr", 2.4)
    if k > 0:                                  # the tutor, waiting
        cx, cy = 0.825, 0.27
        face = ellipse(cx, cy, 0.045, 0.043)
        pg.fill(face, "tuf", (255, 255, 255), 0.5 * k, grain=0)
        pg.stroke(face, "tu", 2.2, reveal=k)
        for s in (-1, 1):
            pg.fill(ellipse(cx + s * 0.016, cy - 0.006, 0.006, 0.007,
                            overshoot=0), f"tue{s}", dd.DARK, 0.95 * k,
                    grain=0)
        pg.stroke(smooth([(cx - 0.016, cy + 0.014), (cx, cy + 0.022),
                          (cx + 0.016, cy + 0.014)]), "tum", 2.0, reveal=k)


def box(pg, t):
    x0, y0, x1, y1 = BOX
    rattle = 0.004 * math.sin(t * 60) if 0.1 < t < OPEN0 else 0.0
    pg.push(rattle, 0, 1)
    inner = rrect(x0, y0, x1, y1, 0.02)
    pg.fill(inner, "inn", (150, 110, 60), 0.75)
    pg.stroke(inner, "inl", 2.8)
    # the questions inside
    pg.begin_clip((x0, y0, x1, y1))
    for i, (bx, by, r) in enumerate(balls_layout()):
        if i in SPILLERS and t >= SPILL:
            continue
        rise = 0.004 * ease(seg(t, OPEN1 - 0.3, OPEN1)) * math.sin(i * 1.7)
        paper_ball(pg, f"b{i}", bx, by - rise, r, t,
                   NOTES[i % len(NOTES)] if i % 2 == 0 else None)
    pg.end_clip()
    # the lid, hinged at the top edge, swinging up past vertical
    th = math.pi * 0.62 * ease(seg(t, OPEN0, OPEN1))
    h = (y1 - y0) * math.cos(th)
    ly0, ly1 = (y0, y0 + h) if h >= 0 else (y0 + h, y0)
    if abs(h) > 0.004:
        lid = rrect(x0, ly0, x1, ly1, min(0.02, abs(h) / 2.1))
        inside = h < 0
        pg.cover(lid, "lidf", (205, 205, 212) if inside else TIN, 1.0)
        pg.stroke(lid, "lid", 2.8)
        if not inside:
            s = h / (y1 - y0)
            for i in range(5):                      # tin stripes
                yy = y0 + (0.2 + 0.15 * i) * (y1 - y0) * s
                pg.stroke([(x0 + 0.02, yy), (x1 - 0.02, yy)], f"st{i}", 1.6,
                          (200, 120, 30), alpha=190)
            if s > 0.4:
                pg.push(0, 0, 1)
                pg.text("MEERA  9-B", ((x0 + x1) / 2, y0 + h * 0.5),
                        0.05 * s, "lbl", angle=-2)
                pg.pop()
    pg.pop()


def spill(pg, t):
    lay = balls_layout()
    for i, dest in SPILLERS.items():
        if t < SPILL:
            continue
        bx, by, r = lay[i]
        k = ease(seg(t, SPILL + 0.08 * (i % 3), SPILL + 0.6 + 0.08 * (i % 3)))
        x, y = lerp((bx, by), dest, k)
        y -= 0.05 * math.sin(math.pi * k)            # arcs out of the box
        if i == HERO and t >= UNCRUMPLE:
            doubt(pg, t, (x, y), r)
        else:
            paper_ball(pg, f"b{i}", x, y, r, t,
                       NOTES[i % len(NOTES)] if i % 2 == 0 else None)


def doubt(pg, t, at, r):
    """The ball uncrumples into a "?" with one eye, then hops to the light."""
    k = ease(seg(t, UNCRUMPLE, UNCRUMPLE + 0.6))
    x, y = at
    if t >= HOP:
        n_hops = 3
        u = min(1.0, (t - HOP) / 1.8)
        x = at[0] + (0.64 - at[0]) * u
        hop = abs(math.sin(math.pi * n_hops * u)) * 0.05 * (1 - 0.3 * u)
        y = at[1] - hop - 0.08 * u
    if k < 1:
        paper_ball(pg, "hero", x, y, r * (1 - k * 0.8), t)
    s = k * 1.6
    if s <= 0.02:
        return
    land = t >= HOP and abs(math.sin(math.pi * 3 * min(1, (t - HOP) / 1.8))) \
        < 0.25
    sy = s * (0.85 if land else 1.0)
    pts = [(x - 0.03 * s, y - 0.04 * sy), (x - 0.018 * s, y - 0.075 * sy),
           (x + 0.012 * s, y - 0.085 * sy), (x + 0.036 * s, y - 0.062 * sy),
           (x + 0.03 * s, y - 0.03 * sy), (x, y - 0.012 * sy),
           (x, y + 0.02 * sy)]
    pg.stroke(smooth(pts), "q", 6.0, dd.INK)
    pg.fill(ellipse(x, y + 0.045 * sy, 0.011 * s, 0.011 * s, overshoot=0),
            "qd", dd.INK, 0.95, grain=0)
    # one eye, sitting on the top of the curve: looks around, then at
    # the light
    look = 1.0 if t >= GLOW + 0.1 else math.sin(t * 7) * 0.8
    ex, ey = x + 0.012 * s, y - 0.085 * sy
    white = ellipse(ex, ey, 0.014 * s, 0.016 * s, overshoot=0)
    pg.cover(white, "qew", (255, 255, 255), 1.0)
    pg.stroke(white, "qewl", 2.0, dd.INK)
    pg.cover(ellipse(ex + 0.006 * look * s, ey - 0.002 * s, 0.006 * s,
                     0.007 * s, overshoot=0), "qe", dd.DARK, 1.0)


def night(t):
    """Lamplight in a dark room, and the laptop's glow once it's on."""
    g = ease(seg(t, GLOW, GLOW + 0.4))

    def post(a):
        S = a.shape[0]
        yy, xx = np.mgrid[0:S, 0:S].astype(np.float32) / S
        lamp = np.exp(-((xx - LAMP[0]) ** 2 + (yy - LAMP[1]) ** 2) / 0.09)
        dark = np.array([0.22, 0.25, 0.42], np.float32)
        warm = np.array([1.0, 0.93, 0.78], np.float32)
        light = dark + (warm - dark) * lamp[..., None]
        if g > 0:
            cx, cy = (SCREEN[0] + SCREEN[2]) / 2, (SCREEN[1] + SCREEN[3]) / 2
            glow = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / 0.05)
            teal = np.array(dd.TEAL, np.float32) / 255
            light = light + teal * glow[..., None] * 0.9 * g
            # the screen itself is a light, not a lit thing
            on = ((xx > SCREEN[0]) & (xx < SCREEN[2]) & (yy > SCREEN[1])
                  & (yy < SCREEN[3])).astype(np.float32)
            light = light * (1 - on[..., None]) + on[..., None] * \
                (1.0 + 0.2 * g)
        return a * light
    return post


def main():
    n = int(DURATION * FPS_UNIQUE)
    first, last = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 \
        else (0, n - 1)
    os.makedirs(OUT, exist_ok=True)
    page_png = paper.ruled(w_cm=14, h_cm=14, seed=41, torn=False)
    for i in range(first, last + 1):
        path = os.path.join(OUT, f"f{i:03d}.png")
        if os.path.exists(path):
            continue
        t = i / FPS_UNIQUE
        pg = dd.Page(page_png, size=RES, frame=i)
        desk(pg, t)
        box(pg, t)
        spill(pg, t)
        pg.render(path, post=night(t))
        print(f"frame {i}", flush=True)


if __name__ == "__main__":
    main()
