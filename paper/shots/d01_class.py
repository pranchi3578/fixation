"""
"Unmute", the opening: the class.

  0.0-4.0   Wide. The teacher's slides race past; he talks in gibberish.
            A column of classmate tiles, every mic slashed. One is asleep.
  4.0-6.0   Push in on Meera's tile; her neighbours stay at the edges.
  6.0-6.5   A "?" rises by her head.
  7.0-8.2   Her cursor creeps to the mic and hovers.
  8.2-9.0   Her eyes dart to the faces around her. They look at her.
  9.0-9.4   She bites her lip; the cursor backs off.
  9.4-10.4  She crumples the "?" into a ball. It drops out of sight.
  10.4-11.6 Pull back out.
  11.7      Teacher: "Any questions?"  ...silence.
  13.2-14.6 The tiles go dark one by one. Hers is last.

Everything in the call zooms; the laptop, its toolbar and her cursor don't.
Usage: python paper/shots/d01_class.py [first last]
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import numpy as np  # noqa: E402

import doodle as dd  # noqa: E402
import doodle_cast as cast  # noqa: E402
import paper  # noqa: E402
from doodle import ellipse, rrect, smooth  # noqa: E402

FPS_UNIQUE = 12
DURATION = 15.0
OUT = os.environ.get("OUT", "paper/build/d01_frames")
RES = int(os.environ.get("RES", 1080))

SCR = (0.06, 0.08, 0.94, 0.95)
PRES = (0.08, 0.11, 0.60, 0.80)
TEACH = (0.62, 0.11, 0.92, 0.33)
TW, TH, GAP = 0.0933, 0.093, 0.011
ROWS, COLS = 4, 3
MEERA_RC = (1, 1)
ASLEEP_RC = (0, 2)
MIC = (0.40, 0.875)

Q_RISE, HOVER, DART, BACK, CRUMPLE, OUT_T = 6.0, 7.0, 8.2, 9.0, 9.4, 10.4
ASK, DARK = 11.7, 13.2


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def seg(t, a, b):
    return (t - a) / (b - a)


def lerp(a, b, k):
    return (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)


def tile(r, c):
    x0 = 0.62 + c * (TW + GAP)
    y0 = 0.36 + r * (TH + GAP)
    return (x0, y0, x0 + TW, y0 + TH)


# -------------------------------------------------------------- slides ----

SLIDES = [
    [("Trigonometry", 0.5, 0.35, 0.14), ("Chapter 8", 0.5, 0.55, 0.08)],
    "triangle",
    [("sin A = opp / hyp", 0.5, 0.35, 0.09),
     ("cos A = adj / hyp", 0.5, 0.55, 0.09)],
    [("tan A = sin A / cos A", 0.5, 0.45, 0.085)],
    [("sin²A + cos²A = 1", 0.5, 0.45, 0.1)],
    "wave",
    [("1 + tan²A = sec²A", 0.5, 0.4, 0.09), ("(prove it)", 0.5, 0.58, 0.06)],
    [("Prove:", 0.3, 0.3, 0.08), ("(1 - cos²A) cosec²A = 1", 0.5, 0.48,
                                  0.07)],
    "circle",
]


def slide(pg, n, t):
    body = rrect(0, 0, 1, 1, 0.02)
    pg.fill(body, f"sl{n}", (255, 255, 250), 0.9, grain=0)
    pg.stroke(body, f"sll{n}", 2.2)
    content = SLIDES[n % len(SLIDES)]
    if content == "triangle":
        tri = [(0.2, 0.75), (0.8, 0.75), (0.8, 0.25), (0.2, 0.75)]
        pg.stroke(tri, f"tri{n}", 2.8)
        pg.stroke(rrect(0.75, 0.7, 0.8, 0.75, 0.001), f"sq{n}", 1.8)
        pg.text("A", (0.3, 0.7), 0.08, f"ta{n}")
        pg.text("hyp", (0.44, 0.44), 0.07, f"th{n}")
        pg.text("opp", (0.88, 0.5), 0.07, f"to{n}")
        pg.text("adj", (0.5, 0.83), 0.07, f"tj{n}")
    elif content == "wave":
        pg.stroke([(0.1, 0.5), (0.9, 0.5)], f"ax{n}", 2)
        pg.stroke([(0.15, 0.2), (0.15, 0.8)], f"ay{n}", 2)
        pg.stroke([(0.15 + 0.7 * i / 40,
                    0.5 - 0.22 * math.sin(2 * math.pi * 2 * i / 40))
                   for i in range(41)], f"wv{n}", 2.8)
        pg.text("y = sin x", (0.7, 0.2), 0.07, f"wl{n}")
    elif content == "circle":
        pg.stroke(ellipse(0.5, 0.5, 0.3, 0.3 * 0.75), f"uc{n}", 2.6)
        pg.stroke([(0.5, 0.5), (0.72, 0.35)], f"ur{n}", 2.4)
        pg.text("r = 1", (0.66, 0.5), 0.07, f"ul{n}")
    else:
        for i, (s, x, y, size) in enumerate(content):
            pg.text(s, (x, y), size, f"s{n}{i}", angle=-2)
    pg.text(f"{n + 14}/60", (0.9, 0.93), 0.05, f"pg{n}", bold=False,
            angle=0)


def presentation(pg, t):
    period = 0.55 if t < ASK else 1e9
    n = int(t / period) if t < ASK else int(ASK / 0.55)
    k = (t % period) / 0.15 if t < ASK else 1
    pg.push_rect((0, 0, 1, 1), PRES)
    pg.begin_clip((0, 0, 1, 1))
    slide(pg, n, t)
    if k < 1:                                # the next one slams in
        pg.push(1 - ease(k), 0, 1)
        slide(pg, n + 1, t)
        pg.pop()
        for i in range(3):
            y = 0.3 + 0.2 * i
            pg.stroke([(0.9 - ease(k) * 0.9, y), (1.0, y)], f"spd{i}", 2.0,
                      alpha=150)
    pg.end_clip()
    pg.pop()


# -------------------------------------------------------------- people ----

def meera_tile(pg, t):
    face = dict(mouth="line", brows="brave", gaze=(0.0, -0.004))
    if t >= Q_RISE:
        face["brows"] = "up"
    if t >= HOVER:
        face.update(brows="worried", gaze=(0.0, 0.008))
    if DART <= t < BACK:
        dart = (-1, 1, -1, 1)[int((t - DART) / 0.2) % 4]
        face["gaze"] = (dart * 0.014, 0.0)
    if BACK <= t < CRUMPLE:
        face["mouth"] = "bite"
    if t >= CRUMPLE:
        face.update(mouth="line", brows="worried", gaze=(0.0, 0.01))
    pg.push_rect(SCR, tile(*MEERA_RC))
    pg.begin_clip(SCR)
    pg.fill([(0, 0), (1, 0), (1, 1), (0, 1)], "mbg", (250, 247, 238), 0.6,
            grain=0)
    cast.meera(pg, t, face)
    question(pg, t)
    pg.end_clip()
    pg.pop()


def question(pg, t):
    if t < Q_RISE:
        return
    x, y = 0.62, 0.26 + 0.006 * math.sin(t * 5)
    if t < CRUMPLE:
        s = ease(seg(t, Q_RISE, Q_RISE + 0.4))
        rot = 0
    else:
        s = 1 - ease(seg(t, CRUMPLE, CRUMPLE + 0.4))
        rot = 1
    if s > 0.02:
        pts = [(x - 0.03, y - 0.03), (x - 0.02, y - 0.06), (x + 0.01, y - 0.07),
               (x + 0.035, y - 0.05), (x + 0.03, y - 0.02), (x, y),
               (x, y + 0.03)]
        pts = [(x + (px - x) * s * (1 - 0.3 * rot * (1 - s)),
                y + (py - y) * s) for px, py in pts]
        pg.stroke(smooth(pts), "q", 3.4)
        pg.fill(ellipse(x, y + 0.06 * s, 0.008 * s, 0.008 * s, overshoot=0),
                "qd", dd.INK, 0.95, grain=0)
    if t >= CRUMPLE + 0.25:                    # a scribbled paper ball
        fall = ease(seg(t, CRUMPLE + 0.5, OUT_T))
        bx, by = x - 0.04 * fall, y + 0.75 * fall ** 1.6
        rng = np.random.default_rng(3)
        ball = []
        for i in range(26):
            a = i * 2.4 + rng.random()
            r = 0.03 + 0.018 * rng.random()
            ball.append((bx + r * math.cos(a), by + r * math.sin(a)))
        k = ease(seg(t, CRUMPLE + 0.25, CRUMPLE + 0.45))
        pg.fill(ellipse(bx, by, 0.042, 0.04), "ballf", (245, 245, 240),
                0.9 * k, grain=0)
        pg.stroke(ball, "ball", 2.2, reveal=k)


def classmates(pg, t):
    for r in range(ROWS):
        for c in range(COLS):
            if (r, c) == MEERA_RC:
                continue
            rect = tile(r, c)
            seed = r * COLS + c + 3
            pg.push_rect((0, 0, 1, 1), rect)
            pg.begin_clip((0, 0, 1, 1))
            pg.fill([(0, 0), (1, 0), (1, 1), (0, 1)], f"tbg{seed}",
                    (250, 247, 238), 0.6, grain=0)
            if (r, c) == (ROWS - 1, COLS - 1):
                pg.text("+48", (0.5, 0.5), 0.35, "more")
            else:
                look = 0.0
                if DART <= t < BACK + 0.6 and r == MEERA_RC[0]:
                    look = 0.03 if c < MEERA_RC[1] else -0.03
                if DART <= t < BACK + 0.6 and c == MEERA_RC[1]:
                    look = 0.0
                cast.classmate(pg, t, seed, look=look,
                               asleep=(r, c) == ASLEEP_RC)
                cast.muted_badge(pg, f"t{seed}")
            pg.end_clip()
            pg.stroke(rrect(0, 0, 1, 1, 0.06), f"tb{seed}", 2.2)
            pg.pop()


def teacher_tile(pg, t):
    pg.push_rect((0, 0, 1, 1.0 * (TEACH[3] - TEACH[1]) / (TEACH[2] - TEACH[0])),
                 TEACH)
    h = (TEACH[3] - TEACH[1]) / (TEACH[2] - TEACH[0])
    pg.begin_clip((0, 0, 1, h))
    pg.fill([(0, 0), (1, 0), (1, h), (0, h)], "tchbg", (250, 247, 238), 0.6,
            grain=0)
    pg.push(0.2, -0.02, 0.6)
    cast.teacher(pg, t, talking=t < ASK + 0.5)
    pg.pop()
    pg.end_clip()
    talking = t < ASK + 0.5
    border = rrect(0, 0, 1, h, 0.04)
    if talking:
        pg.stroke(border, "tspk", 5.0, (240, 200, 40), alpha=200)
    pg.stroke(border, "tchb", 2.2)
    pg.pop()


def darkness(pg, t):
    """The call ends, one tile at a time; hers last."""
    order = [PRES, TEACH] + [tile(r, c) for r, c in
                             [(0, 0), (2, 2), (3, 0), (0, 2), (2, 0), (1, 0),
                              (3, 1), (0, 1), (1, 2), (3, 2), (2, 1)]] \
        + [tile(*MEERA_RC)]
    for i, rect in enumerate(order):
        start = DARK + 0.09 * i + (0.35 if i == len(order) - 1 else 0)
        k = ease(seg(t, start, start + 0.12))
        if k > 0:
            x0, y0, x1, y1 = rect
            pg.cover([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], f"dk{i}",
                     (22, 22, 32), 0.93 * k)


def ask_bubble(pg, t):
    k = ease(seg(t, ASK, ASK + 0.25)) * (1 - ease(seg(t, DARK + 0.09,
                                                         DARK + 0.25)))
    if k <= 0:
        return
    b = smooth([(0.40, 0.2), (0.44, 0.13), (0.55, 0.115), (0.62, 0.15),
                (0.61, 0.22), (0.52, 0.24), (0.45, 0.235), (0.40, 0.2)])
    b = b + [(0.61, 0.22), (0.64, 0.24)]
    pg.fill(b, "askf", (255, 255, 255), 0.9 * k, grain=0)
    pg.stroke(b, "ask", 2.6, reveal=k)
    pg.text("Any questions?", (0.51, 0.178), 0.045, "askt",
            reveal=ease(seg(t, ASK + 0.1, ASK + 0.4)))


# -------------------------------------------------------------- screen ----

def toolbar(pg):
    bar = rrect(0.33, 0.835, 0.67, 0.915, 0.035)
    pg.fill(bar, "barf", (250, 248, 240), 0.85, grain=0)
    pg.stroke(bar, "bar", 2.0)
    for x, key in ((0.40, "mic"), (0.50, "vid"), (0.60, "end")):
        c = ellipse(x, 0.875, 0.032, 0.032)
        if key == "end":
            pg.fill(c, "endf", dd.RED, 0.7)
        pg.stroke(c, key)
    pg.stroke(rrect(0.392, 0.852, 0.408, 0.882, 0.008), "micg", 2.2)
    pg.stroke(ellipse(0.40, 0.874, 0.016, 0.016, 10, 170, 12, 0), "micc", 2.0)
    pg.stroke([(0.40, 0.89), (0.40, 0.897)], "mics", 2.0)
    pg.stroke(rrect(0.485, 0.865, 0.508, 0.885, 0.004), "vidg", 2.0)
    pg.stroke([(0.508, 0.875), (0.518, 0.867), (0.518, 0.883),
               (0.508, 0.875)], "vidl", 2.0)
    pg.stroke(smooth([(0.585, 0.88), (0.60, 0.872), (0.615, 0.88)]),
              "endg", 2.6, (255, 255, 255))
    pg.stroke([(0.378, 0.852), (0.422, 0.898)], "slash", 4.2, dd.RED)


def cursor(pg, pos):
    x, y = pos
    arrow = [(x, y), (x, y + 0.045), (x + 0.011, y + 0.034),
             (x + 0.02, y + 0.052), (x + 0.028, y + 0.048),
             (x + 0.019, y + 0.031), (x + 0.033, y + 0.031), (x, y)]
    pg.fill(arrow, "curf", (255, 255, 255), 0.9, boil=0.5, grain=0)
    pg.stroke(arrow, "cur", 2.4, dd.DARK)


def cursor_at(t):
    idle = (0.76 + 0.006 * math.sin(t * 3), 0.62 + 0.004 * math.cos(t * 2))
    hover = (MIC[0] + 0.04, MIC[1] - 0.045)
    back = (0.6, 0.7)
    if t < HOVER:
        return idle
    if t < DART:
        return lerp(idle, hover, ease(seg(t, HOVER, DART)))
    if t < BACK:
        return (hover[0] + 0.002 * math.sin(t * 20), hover[1])
    return lerp(hover, back, ease(seg(t, BACK, BACK + 0.4)))


def view(t):
    """Which part of the call fills the screen."""
    m = tile(*MEERA_RC)
    cx, cy = (m[0] + m[2]) / 2, (m[1] + m[3]) / 2
    w1 = (m[2] - m[0]) * 2.1
    zoom_in = ease(seg(t, 4.0, 6.0))
    zoom_out = ease(seg(t, OUT_T, OUT_T + 1.2))
    k = zoom_in * (1 - zoom_out)
    w0 = SCR[2] - SCR[0]
    w = math.exp(math.log(w0) + (math.log(w1) - math.log(w0)) * k)
    c0 = ((SCR[0] + SCR[2]) / 2, (SCR[1] + SCR[3]) / 2)
    c = lerp(c0, (cx, cy), k)
    h = w * (SCR[3] - SCR[1]) / (SCR[2] - SCR[0])
    return (c[0] - w / 2, c[1] - h / 2, c[0] + w / 2, c[1] + h / 2)


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
        pg.stroke(rrect(0.03, 0.03, 0.97, 0.97, 0.04), "bezel", 3.2)
        pg.stroke(ellipse(0.5, 0.055, 0.007, 0.007, overshoot=40), "cam", 2)
        pg.begin_clip(SCR)
        pg.push_rect(view(t), SCR)
        presentation(pg, t)
        teacher_tile(pg, t)
        classmates(pg, t)
        meera_tile(pg, t)
        pg.stroke(rrect(*tile(*MEERA_RC), 0.006), "mtb", 2.2)
        darkness(pg, t)
        ask_bubble(pg, t)
        pg.pop()
        pg.end_clip()
        pg.stroke(rrect(*SCR, 0.02), "screen", 2.4)
        toolbar(pg)
        cursor(pg, cursor_at(t))
        pg.render(path)
        print(f"frame {i}", flush=True)


if __name__ == "__main__":
    main()
