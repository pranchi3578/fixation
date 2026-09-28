"""
"Unmute", beat 5, as a doodle: the first word of the film.

We are the laptop's camera. Meera is drawn in ballpoint on a notebook page,
inside a doodled laptop screen; the call's buttons sit along the bottom and
the Brainback tutor is in a small tile, top right.

  0.0-1.2  She waits, worried. A "?" bobs by her head. The tutor waits.
  1.2-2.0  Her cursor drifts toward the muted mic...
  2.0-2.4  ...and backs off. She looks down at it, bites her lip.
  2.4-2.9  It goes back.
  2.9      Click. The red slash is scribbled out; the mic goes teal.
  3.8      "Why?" -- in a speech bubble, and the tutor lights up.
  4.3      She smiles. The tutor starts answering ("...").
  4.6      The "?" pops into a "!".

12 drawings a second, each held for two frames.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import numpy as np  # noqa: E402

import doodle as dd  # noqa: E402
from doodle_cast import meera  # noqa: E402
import paper  # noqa: E402
from doodle import ellipse, rrect, smooth  # noqa: E402

FPS_UNIQUE = 12
DURATION = 6.0
OUT = os.environ.get("OUT", "paper/build/d05_frames")
RES = int(os.environ.get("RES", 1080))
CLICK, WHY, SMILE, POP = 2.9, 3.8, 4.3, 4.6
MIC = (0.40, 0.875)


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def seg(t, a, b):
    return (t - a) / (b - a)


def lerp(a, b, k):
    return (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)


# ------------------------------------------------------------- drawing ----

def laptop(pg):
    pg.stroke(rrect(0.03, 0.03, 0.97, 0.97, 0.04), "bezel", 3.2)
    pg.stroke(rrect(0.06, 0.08, 0.94, 0.95, 0.02), "screen", 2.4)
    pg.stroke(ellipse(0.5, 0.055, 0.007, 0.007, overshoot=40), "cam", 2.0)


def toolbar(pg, t):
    muted = t < CLICK + 0.1
    bar = rrect(0.33, 0.835, 0.67, 0.915, 0.035)
    pg.fill(bar, "barf", (250, 248, 240), 0.85, grain=0)
    pg.stroke(bar, "bar", 2.0)
    for x, key in ((0.40, "mic"), (0.50, "vid"), (0.60, "end")):
        c = ellipse(x, 0.875, 0.032, 0.032)
        if key == "end":
            pg.fill(c, "endf", dd.RED, 0.7)
        if key == "mic" and not muted:
            pg.fill(c, "micon", dd.TEAL, 0.65 * ease(seg(t, CLICK, CLICK + 0.25)))
        pg.stroke(c, key)
    # mic glyph
    pg.stroke(rrect(0.392, 0.852, 0.408, 0.882, 0.008), "micg", 2.2)
    pg.stroke(ellipse(0.40, 0.874, 0.016, 0.016, 10, 170, 12, 0), "micc", 2.0)
    pg.stroke([(0.40, 0.89), (0.40, 0.897)], "mics", 2.0)
    # camera glyph
    pg.stroke(rrect(0.485, 0.865, 0.508, 0.885, 0.004), "vidg", 2.0)
    pg.stroke([(0.508, 0.875), (0.518, 0.867), (0.518, 0.883),
               (0.508, 0.875)], "vidl", 2.0)
    pg.stroke(smooth([(0.585, 0.88), (0.60, 0.872), (0.615, 0.88)]),
              "endg", 2.6, (255, 255, 255))
    # the red slash, then the scribble that kills it
    if t < CLICK + 0.35:
        pg.stroke([(0.378, 0.852), (0.422, 0.898)], "slash", 4.2, dd.RED)
    if CLICK < t:
        k = ease(seg(t, CLICK, CLICK + 0.3))
        zig = []
        for i in range(12):
            a = i / 11
            p = lerp((0.375, 0.85), (0.425, 0.90), a)
            zig.append((p[0] + (0.012 if i % 2 else -0.012),
                        p[1] + (-0.012 if i % 2 else 0.012)))
        if t < CLICK + 0.6:
            pg.stroke(zig, "scribble", 2.2, dd.INK, reveal=k,
                      alpha=int(235 * (1 - ease(seg(t, CLICK + 0.3,
                                                      CLICK + 0.6)))))
    if muted:
        pg.text("unmute", (0.40, 0.935), 0.028, "lblmic", bold=False)


def cursor(pg, pos, clicking):
    x, y = pos
    arrow = [(x, y), (x, y + 0.045), (x + 0.011, y + 0.034),
             (x + 0.02, y + 0.052), (x + 0.028, y + 0.048),
             (x + 0.019, y + 0.031), (x + 0.033, y + 0.031), (x, y)]
    pg.fill(arrow, "curf", (255, 255, 255), 0.9, boil=0.5, grain=0)
    pg.stroke(arrow, "cur", 2.4, dd.DARK)
    if clicking:
        for i, a in enumerate((200, 240, 280, 320)):
            r0, r1 = 0.012, 0.026
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            pg.stroke([(x + ca * r0, y + sa * r0), (x + ca * r1, y + sa * r1)],
                      f"tick{i}", 2.2)


def tutor(pg, t):
    x0, y0, x1, y1 = 0.68, 0.11, 0.92, 0.33
    pg.stroke(rrect(x0, y0, x1, y1, 0.015), "tile", 2.4)
    cx, cy = 0.80, 0.21
    pulse = 0.35 + 0.1 * math.sin(t * 2 * math.pi / 1.6)
    awake = ease(seg(t, WHY, WHY + 0.2))
    glow = pulse * (1 - awake) + 0.85 * awake
    halo = ellipse(cx, cy, 0.075 + 0.01 * awake, 0.075 + 0.01 * awake)
    pg.fill(halo, "halo", dd.TEAL, glow)
    body = ellipse(cx, cy, 0.055, 0.052)
    pg.stroke(body, "tb", 2.6)
    # eyes: patient half-moons while waiting, wide open when she speaks
    blink = 0.8 <= t < 0.95
    for s in (-1, 1):
        ex = cx + s * 0.02
        if blink:
            pg.stroke([(ex - 0.008, cy - 0.006), (ex + 0.008, cy - 0.006)],
                      f"te{s}", 2.4, dd.DARK)
        else:
            r = 0.007 + 0.004 * awake
            pg.fill(ellipse(ex, cy - 0.006, r, r * 1.2, overshoot=0),
                    f"te{s}", dd.DARK, 0.95, boil=0.3, grain=0)
    w = 0.018 + 0.01 * awake
    pg.stroke(smooth([(cx - w, cy + 0.017), (cx, cy + 0.027 + 0.008 * awake),
                      (cx + w, cy + 0.017)]), "tm", 2.4)
    if awake:
        for i in range(3):                       # it heard her
            r = 0.07 + 0.013 * i
            pg.stroke(ellipse(cx, cy, r, r, 200, 250, 8, 0), f"wv{i}", 2.0,
                      reveal=ease(seg(t, WHY + 0.05 * i, WHY + 0.2 + 0.05 * i)))
    if t >= SMILE:                                # and starts to answer
        bub = rrect(0.715, 0.265, 0.785, 0.305, 0.018)
        pg.fill(bub, "tbubf", (255, 255, 255), 0.8, grain=0)
        pg.stroke(bub, "tbub", 2.2)
        n = 1 + int((t - SMILE) * 6) % 3
        for i in range(n):
            pg.fill(ellipse(0.733 + 0.017 * i, 0.285, 0.005, 0.005,
                            overshoot=0), f"dot{i}", dd.INK, 0.95, grain=0)
    pg.text("Brainback tutor", (0.80, 0.355), 0.03, "tlabel", bold=False,
            angle=-2)


def question(pg, t):
    bob = 0.008 * math.sin(t * 2 * math.pi / 1.3)
    x, y = 0.60, 0.25 + bob
    if t < POP:
        pg.stroke(smooth([(x - 0.03, y - 0.03), (x - 0.02, y - 0.06),
                          (x + 0.01, y - 0.07), (x + 0.035, y - 0.05),
                          (x + 0.03, y - 0.02), (x, y), (x, y + 0.03)]),
                  "q", 3.4)
        pg.fill(ellipse(x, y + 0.06, 0.008, 0.008, overshoot=0), "qd",
                dd.INK, 0.95, grain=0)
    else:
        k = ease(seg(t, POP, POP + 0.15))
        s = 0.7 + 0.3 * k
        pg.stroke([(x, y - 0.075 * s), (x, y + 0.03)], "ex", 3.8)
        pg.fill(ellipse(x, y + 0.06, 0.009, 0.009, overshoot=0), "exd",
                dd.INK, 0.95, grain=0)
        if t < POP + 0.5:                        # it pops
            for i, a in enumerate((-160, -120, -60, -20)):
                ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
                pg.stroke([(x + ca * 0.06, y - 0.02 + sa * 0.06),
                           (x + ca * 0.085, y - 0.02 + sa * 0.085)],
                          f"pop{i}", 2.2)


def why_bubble(pg, t):
    k = ease(seg(t, WHY, WHY + 0.25))
    bub = smooth([(0.58, 0.55), (0.60, 0.49), (0.69, 0.465), (0.78, 0.49),
                  (0.79, 0.55), (0.72, 0.585), (0.62, 0.58), (0.555, 0.60),
                  (0.58, 0.55)])
    pg.fill(bub, "wbf", (255, 255, 255), 0.7 * k, grain=0)
    pg.stroke(bub, "wb", 2.6, reveal=k)
    pg.text("Why?", (0.69, 0.525), 0.075, "whytxt",
            reveal=ease(seg(t, WHY + 0.1, WHY + 0.35)))


# ------------------------------------------------------------ timeline ----

def state(t):
    idle = (0.76 + 0.006 * math.sin(t * 3), 0.62 + 0.004 * math.cos(t * 2))
    hover = (MIC[0] + 0.045, MIC[1] - 0.05)
    back = (0.56, 0.74)
    target = (MIC[0] + 0.002, MIC[1] - 0.004)
    if t < 1.2:
        cur = idle
    elif t < 2.0:
        cur = lerp(idle, hover, ease(seg(t, 1.2, 2.0)))
    elif t < 2.4:
        cur = lerp(hover, back, ease(seg(t, 2.0, 2.4)))
    elif t < CLICK:
        cur = lerp(back, target, ease(seg(t, 2.4, CLICK)))
    else:
        cur = lerp(target, (0.47, 0.8), ease(seg(t, CLICK + 0.5, 3.6)))
    face = dict(mouth="line", brows="worried", gaze=(0.004, 0.0))
    if 1.3 <= t < 2.9:
        face["gaze"] = (0.0, 0.008)              # eyes on the button
    if 2.0 <= t < 2.4:
        face["mouth"] = "bite"
    if CLICK <= t < WHY:
        face["brows"] = "up"                     # a breath in
    if WHY <= t < SMILE:
        face.update(mouth="o", brows="up", gaze=(0.008, -0.006))
    elif t >= SMILE:
        face.update(mouth="smile", brows="brave", gaze=(0.008, -0.006))
    return cur, face


def main():
    n = int(DURATION * FPS_UNIQUE)
    first, last = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 \
        else (0, n - 1)
    os.makedirs(OUT, exist_ok=True)
    page_png = paper.ruled(w_cm=14, h_cm=14, seed=41, torn=False)
    for i in range(first, last + 1):
        t = i / FPS_UNIQUE
        pg = dd.Page(page_png, size=RES, frame=i)
        cur, face = state(t)
        laptop(pg)
        tutor(pg, t)
        meera(pg, t, face)
        question(pg, t)
        toolbar(pg, t)
        if t >= WHY:
            why_bubble(pg, t)
        cursor(pg, cur, CLICK <= t < CLICK + 0.25)
        pg.render(os.path.join(OUT, f"f{i:03d}.png"))
        print(f"frame {i}", flush=True)


if __name__ == "__main__":
    main()
