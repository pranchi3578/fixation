"""
The cast, as doodles. Each character draws itself in "screen" coordinates
(the laptop screen is roughly 0.06-0.94 across); to put one inside a video
tile, push_rect() the screen onto the tile first.
"""

import math

import numpy as np

import doodle as dd
from doodle import ellipse, rrect, smooth

SCREEN = (0.06, 0.08, 0.94, 0.95)


def meera(pg, t, face):
    gx, gy = face["gaze"]
    # shoulders and shirt
    body = smooth([(0.12, 0.95), (0.16, 0.75), (0.26, 0.67), (0.36, 0.64)]) \
        + smooth([(0.44, 0.64), (0.54, 0.67), (0.64, 0.75), (0.68, 0.95)])
    pg.fill(body + [(0.12, 0.95)], "shirt", dd.SHIRT, 0.55)
    pg.stroke(smooth([(0.12, 0.95), (0.16, 0.75), (0.26, 0.67),
                      (0.36, 0.64)]), "shL")
    pg.stroke(smooth([(0.44, 0.64), (0.54, 0.67), (0.64, 0.75),
                      (0.68, 0.95)]), "shR")
    pg.stroke([(0.34, 0.64), (0.40, 0.72), (0.46, 0.64)], "collarV")
    pg.stroke([(0.34, 0.64), (0.31, 0.70), (0.38, 0.70)], "collarL", 2.0)
    pg.stroke([(0.46, 0.64), (0.49, 0.70), (0.42, 0.70)], "collarR", 2.0)
    # neck
    pg.fill([(0.37, 0.57), (0.43, 0.57), (0.43, 0.65), (0.37, 0.65)],
            "neckf", dd.SKIN, 0.5)
    pg.stroke([(0.37, 0.575), (0.37, 0.645)], "neckL", 2.2)
    pg.stroke([(0.43, 0.575), (0.43, 0.645)], "neckR", 2.2)
    # plaits behind the shoulders, ribbons at the ends
    for side, x0 in ((-1, 0.285), (1, 0.515)):
        for k in range(5):
            cx = x0 + side * 0.006 * k
            cy = 0.50 + 0.043 * k
            loop = ellipse(cx, cy, 0.022, 0.026, overshoot=20)
            pg.fill(loop, f"plf{side}{k}", dd.DARK, 0.8)
            pg.stroke(loop, f"pl{side}{k}", 2.0, dd.DARK)
        bx, by = x0 + side * 0.026, 0.708
        for s in (-1, 1):
            bow = [(bx, by), (bx + s * 0.035, by - 0.02),
                   (bx + s * 0.035, by + 0.02), (bx, by)]
            pg.fill(bow, f"bow{side}{s}", dd.RED, 0.75)
            pg.stroke(bow, f"bowl{side}{s}", 2.0)
    # face
    head = ellipse(0.40, 0.44, 0.125, 0.145)
    pg.fill(head, "skin", dd.SKIN, 0.68)
    pg.stroke(head, "head", 2.8)
    pg.stroke(ellipse(0.273, 0.46, 0.014, 0.025, 90, 270, 12, 0), "earL")
    pg.stroke(ellipse(0.527, 0.46, 0.014, 0.025, -90, 90, 12, 0), "earR")
    # hair: a cap over the top, a fringe with a side parting
    cap = ellipse(0.40, 0.43, 0.14, 0.165, 185, 355, 30, 0)
    fringe = smooth([(0.54, 0.41), (0.47, 0.37), (0.41, 0.35),
                     (0.36, 0.39), (0.30, 0.40), (0.26, 0.42)])
    pg.fill(cap + fringe, "hairf", dd.DARK, 0.85)
    pg.stroke(cap, "hair", 2.8, dd.DARK)
    pg.stroke(fringe, "fringe", 2.4, dd.DARK)
    # brows
    tilt = {"worried": 0.012, "up": -0.004, "brave": -0.002}[face["brows"]]
    lift = {"worried": 0.0, "up": -0.012, "brave": -0.006}[face["brows"]]
    for s, ex in ((-1, 0.355), (1, 0.445)):
        inner = (ex - s * 0.022, 0.415 + lift - tilt)
        outer = (ex + s * 0.022, 0.418 + lift + tilt * 0.3)
        pg.stroke([outer, ((inner[0] + outer[0]) / 2,
                           (inner[1] + outer[1]) / 2 - 0.004), inner],
                  f"brow{s}", 2.6, dd.DARK)
    # eyes: two dots, and they move
    for s, ex in ((-1, 0.355), (1, 0.445)):
        e = ellipse(ex + gx, 0.45 + gy, 0.011, 0.013, overshoot=0)
        pg.fill(e, f"eye{s}", dd.DARK, 0.95, boil=0.3, grain=0)
    # nose
    pg.stroke(smooth([(0.402, 0.47), (0.41, 0.50), (0.398, 0.505)]),
              "nose", 2.0)
    # mouth
    m = face["mouth"]
    if m == "line":
        pg.stroke(smooth([(0.375, 0.535), (0.40, 0.538), (0.425, 0.533)]),
                  "mouth", 2.4)
    elif m == "bite":
        pg.stroke(smooth([(0.378, 0.536), (0.39, 0.532), (0.40, 0.538),
                          (0.41, 0.532), (0.422, 0.536)]), "mouth", 2.4)
    elif m == "o":
        o = ellipse(0.40, 0.54, 0.016, 0.022, overshoot=0)
        pg.fill(o, "mo", dd.DARK, 0.9, grain=0)
        pg.stroke(o, "mouth", 2.2)
    else:
        pg.stroke(smooth([(0.365, 0.528), (0.40, 0.548), (0.435, 0.528)]),
                  "mouth", 2.6)
        for s, cx in ((-1, 0.33), (1, 0.47)):
            pg.fill(ellipse(cx, 0.505, 0.022, 0.014), f"blush{s}", dd.PINK,
                    0.35)


def teacher(pg, t, talking=True, bubble=None):
    """Sir: bald on top, side hair, glasses, a moustache, and a lot to say."""
    cx, cy = 0.5, 0.46
    pg.fill(smooth([(0.1, 0.95), (0.18, 0.72), (0.5, 0.66), (0.82, 0.72),
                    (0.9, 0.95)]) + [(0.1, 0.95)], "tsh", (230, 225, 200),
            0.6)
    pg.stroke(smooth([(0.1, 0.95), (0.18, 0.72), (0.5, 0.66), (0.82, 0.72),
                      (0.9, 0.95)]), "tshl", 2.6)
    head = ellipse(cx, cy, 0.2, 0.24)
    pg.fill(head, "tsk", dd.SKIN, 0.65)
    pg.stroke(head, "th", 2.8)
    for s in (-1, 1):
        side = ellipse(cx + s * 0.19, cy - 0.04, 0.05, 0.09)
        pg.fill(side, f"tsd{s}", (140, 140, 150), 0.8)
        g = ellipse(cx + s * 0.085, cy - 0.01, 0.06, 0.045, overshoot=4)
        pg.stroke(g, f"tg{s}", 2.4, dd.DARK)
        pg.fill(ellipse(cx + s * 0.085, cy - 0.005, 0.014, 0.016,
                        overshoot=0), f"te{s}", dd.DARK, 0.95, grain=0)
    pg.stroke([(cx - 0.025, cy - 0.015), (cx + 0.025, cy - 0.015)], "tgb",
              2.2, dd.DARK)
    pg.fill(smooth([(cx - 0.08, cy + 0.08), (cx, cy + 0.06),
                    (cx + 0.08, cy + 0.08), (cx, cy + 0.1)]), "tmo",
            dd.DARK, 0.85)
    open_ = talking and (int(t * 12) % 2 == 0)
    if open_:
        pg.fill(ellipse(cx, cy + 0.14, 0.035, 0.03, overshoot=0), "tmth",
                dd.DARK, 0.9, grain=0)
    else:
        pg.stroke([(cx - 0.035, cy + 0.14), (cx + 0.035, cy + 0.14)], "tmth",
                  2.4)
    if bubble:
        text, k = bubble
        b = smooth([(0.2, 0.2), (0.5, 0.06), (0.85, 0.16), (0.88, 0.3),
                    (0.55, 0.36), (0.25, 0.32), (0.2, 0.2)])
        pg.fill(b, "tbub", (255, 255, 255), 0.85 * k, grain=0)
        pg.stroke(b, "tbubl", 2.6, reveal=k)
        pg.text(text, (0.54, 0.21), 0.11, "tbubt", reveal=k)


HAIR = ["short", "plaits", "bun", "spiky", "cap", "long", "curly", "short"]


def classmate(pg, t, seed, look=0.0, dark=0.0, asleep=False):
    """A generic classmate, drawn in tile coordinates (0..1)."""
    rng = np.random.default_rng(seed)
    style = HAIR[seed % len(HAIR)]
    skin = tuple(int(c * rng.uniform(0.8, 1.08)) for c in dd.SKIN)
    shirt = [(150, 190, 235), (240, 240, 235), (190, 225, 190),
             (240, 210, 170)][seed % 4]
    cx, cy = 0.5 + rng.uniform(-0.05, 0.05), 0.47 + rng.uniform(-0.03, 0.03)
    tilt = 0.06 if asleep else 0.0
    body = smooth([(0.08, 1.0), (0.18, 0.8), (0.5, 0.73), (0.82, 0.8),
                   (0.92, 1.0)])
    pg.fill(body + [(0.08, 1.0)], f"cb{seed}", shirt, 0.55)
    pg.stroke(body, f"cbl{seed}", 2.4)
    head = ellipse(cx + tilt, cy, 0.2, 0.23)
    pg.fill(head, f"cs{seed}", skin, 0.65)
    pg.stroke(head, f"ch{seed}", 2.6)
    hx = cx + tilt
    if style in ("short", "spiky", "curly", "plaits", "bun", "long"):
        cap = ellipse(hx, cy - 0.02, 0.215, 0.235, 185, 355, 20, 0)
        fr = smooth([(hx + 0.21, cy - 0.04), (hx + 0.05, cy - 0.12),
                     (hx - 0.1, cy - 0.1), (hx - 0.21, cy - 0.04)])
        pg.fill(cap + fr, f"chr{seed}", dd.DARK, 0.85)
        if style == "spiky":
            pg.stroke([(hx - 0.15, cy - 0.2), (hx - 0.1, cy - 0.3),
                       (hx - 0.04, cy - 0.22), (hx + 0.02, cy - 0.32),
                       (hx + 0.07, cy - 0.22), (hx + 0.13, cy - 0.29),
                       (hx + 0.16, cy - 0.18)], f"csp{seed}", 2.4, dd.DARK)
        if style == "bun":
            b = ellipse(hx, cy - 0.29, 0.08, 0.06)
            pg.fill(b, f"cbn{seed}", dd.DARK, 0.85)
        if style == "plaits":
            for s in (-1, 1):
                for k in range(3):
                    lp = ellipse(hx + s * 0.22, cy + 0.08 + 0.09 * k, 0.04,
                                 0.045)
                    pg.fill(lp, f"cpl{seed}{s}{k}", dd.DARK, 0.85)
        if style == "long":
            for s in (-1, 1):
                pg.fill([(hx + s * 0.2, cy - 0.05), (hx + s * 0.25, cy + 0.3),
                         (hx + s * 0.15, cy + 0.3), (hx + s * 0.17, cy)],
                        f"clg{seed}{s}", dd.DARK, 0.85)
        if style == "curly":
            for k in range(6):
                a = math.radians(200 + 28 * k)
                pg.fill(ellipse(hx + 0.2 * math.cos(a),
                                cy - 0.03 + 0.22 * math.sin(a), 0.06, 0.055),
                        f"ccu{seed}{k}", dd.DARK, 0.85)
    elif style == "cap":
        c = ellipse(hx, cy - 0.06, 0.22, 0.2, 180, 360, 16, 0)
        pg.fill(c + [(hx + 0.32, cy - 0.06)], f"ccap{seed}",
                (200, 60, 60), 0.75)
        pg.stroke(c + [(hx + 0.32, cy - 0.06), (hx - 0.22, cy - 0.06)],
                  f"ccapl{seed}", 2.2)
    for s in (-1, 1):
        ex, ey = hx + s * 0.075 + look, cy + 0.02
        if asleep:
            pg.stroke(ellipse(ex, ey, 0.03, 0.015, 10, 170, 8, 0),
                      f"cey{seed}{s}", 2.2, dd.DARK)
        else:
            pg.fill(ellipse(ex, ey, 0.022, 0.026, overshoot=0),
                    f"cey{seed}{s}", dd.DARK, 0.95, grain=0)
    pg.stroke(smooth([(hx - 0.05, cy + 0.12), (hx, cy + 0.13),
                      (hx + 0.05, cy + 0.12)]), f"cm{seed}", 2.2)
    if asleep:
        pg.text("z", (0.8, 0.22 - 0.03 * math.sin(t * 3)), 0.14,
                f"cz{seed}", bold=False)
    if dark > 0:
        pg.fill([(0, 0), (1, 0), (1, 1), (0, 1)], f"cdark{seed}",
                (25, 25, 35), 0.9 * dark, grain=0.35)


def muted_badge(pg, key):
    """The tiny slashed mic in a tile's corner."""
    c = ellipse(0.87, 0.87, 0.08, 0.08)
    pg.fill(c, f"{key}mbf", (250, 250, 250), 0.85, grain=0)
    pg.stroke(rrect(0.855, 0.82, 0.885, 0.895, 0.015), f"{key}mbg", 2.0)
    pg.stroke([(0.82, 0.82), (0.92, 0.92)], f"{key}mbs", 2.6, dd.RED)


def tutor_face(pg, cx, cy, r, key, glow=0.4, wide=0.0, talking=False, t=0.0,
               blink=False):
    """The Brainback tutor: a round, patient face in its own light."""
    halo = ellipse(cx, cy, r * (1.35 + 0.15 * wide), r * (1.35 + 0.15 * wide))
    pg.fill(halo, key + "halo", dd.TEAL, min(0.95, glow))
    body = ellipse(cx, cy, r, r * 0.95)
    pg.stroke(body, key + "b", 2.6)
    for s in (-1, 1):
        ex = cx + s * r * 0.36
        if blink:
            pg.stroke([(ex - r * 0.15, cy - r * 0.1), (ex + r * 0.15,
                                                       cy - r * 0.1)],
                      f"{key}e{s}", 2.4, dd.DARK)
        else:
            er = r * (0.13 + 0.07 * wide)
            pg.fill(ellipse(ex, cy - r * 0.1, er, er * 1.2, overshoot=0),
                    f"{key}e{s}", dd.DARK, 0.95, boil=0.3, grain=0)
    if talking and int(t * 10) % 2 == 0:
        pg.fill(ellipse(cx, cy + r * 0.38, r * 0.2, r * 0.16, overshoot=0),
                key + "mo", dd.DARK, 0.9, grain=0)
    else:
        w = r * (0.33 + 0.18 * wide)
        pg.stroke(smooth([(cx - w, cy + r * 0.3),
                          (cx, cy + r * (0.48 + 0.15 * wide)),
                          (cx + w, cy + r * 0.3)]), key + "m", 2.4)


def toolbar(pg, muted=True):
    bar = rrect(0.33, 0.835, 0.67, 0.915, 0.035)
    pg.fill(bar, "barf", (250, 248, 240), 0.85, grain=0)
    pg.stroke(bar, "bar", 2.0)
    for x, key in ((0.40, "mic"), (0.50, "vid"), (0.60, "end")):
        c = ellipse(x, 0.875, 0.032, 0.032)
        if key == "end":
            pg.fill(c, "endf", dd.RED, 0.7)
        if key == "mic" and not muted:
            pg.fill(c, "micon", dd.TEAL, 0.65)
        pg.stroke(c, key)
    pg.stroke(rrect(0.392, 0.852, 0.408, 0.882, 0.008), "micg", 2.2)
    pg.stroke(ellipse(0.40, 0.874, 0.016, 0.016, 10, 170, 12, 0), "micc", 2.0)
    pg.stroke([(0.40, 0.89), (0.40, 0.897)], "mics", 2.0)
    pg.stroke(rrect(0.485, 0.865, 0.508, 0.885, 0.004), "vidg", 2.0)
    pg.stroke([(0.508, 0.875), (0.518, 0.867), (0.518, 0.883),
               (0.508, 0.875)], "vidl", 2.0)
    pg.stroke(smooth([(0.585, 0.88), (0.60, 0.872), (0.615, 0.88)]),
              "endg", 2.6, (255, 255, 255))
    if muted:
        pg.stroke([(0.378, 0.852), (0.422, 0.898)], "slash", 4.2, dd.RED)


def paper_plane(pg, key, x, y, size, heading, alpha=235):
    """A doodled dart, nose along heading (radians, screen coords)."""
    c, s = math.cos(heading), math.sin(heading)

    def P(u, v):
        return (x + size * (u * c - v * s), y + size * (u * s + v * c))
    outline = [P(1, 0), P(-0.7, -0.55), P(-0.45, 0), P(-0.7, 0.55), P(1, 0)]
    pg.fill(outline, key + "f", (250, 250, 245), 0.9, grain=0)
    pg.cover(outline, key + "c", (250, 250, 245), 0.95)
    pg.stroke(outline, key, 2.2, alpha=alpha)
    pg.stroke([P(1, 0), P(-0.45, 0)], key + "k", 1.6, alpha=alpha)
