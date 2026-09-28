"""
"Unmute", the end card.

  0.0-0.8  The one-eyed "?" from the pencil box hops onto a blank page.
  0.8-1.1  It pops into a "!".
  1.1-2.0  "Ask anything."
  2.0-2.9  "Interrupt anytime."
  3.1-3.5  A teal highlighter swipe...
  3.3-4.1  ...and "Brainback", handwritten over it. (Placeholder wordmark:
           swap in the real logo when we have it.)
  4.3      "the AI tutor that loves questions"
  -6.0     Hold.

Usage: python paper/shots/d08_endcard.py [first last]
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

import doodle as dd  # noqa: E402
import paper  # noqa: E402
from doodle import ellipse, smooth  # noqa: E402

FPS_UNIQUE = 12
DURATION = 6.0
OUT = os.environ.get("OUT", "paper/build/d08_frames")
RES = int(os.environ.get("RES", 1080))
POP = 0.8


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def seg(t, a, b):
    return (t - a) / (b - a)


def character(pg, t):
    """The Doubtling, as a doodle: "?" with one eye, then "!"."""
    u = min(1.0, t / POP)
    x = -0.05 + (0.5 - -0.05) * ease(u)
    hop = abs(math.sin(math.pi * 3 * u)) * 0.05 * (1 - u)
    y = 0.2 - hop + 0.006 * math.sin(t * 4) * (t > 1.2)
    s = 1.3
    if t < POP:
        pts = [(x - 0.03 * s, y - 0.04 * s), (x - 0.018 * s, y - 0.075 * s),
               (x + 0.012 * s, y - 0.085 * s), (x + 0.036 * s, y - 0.062 * s),
               (x + 0.03 * s, y - 0.03 * s), (x, y - 0.012 * s),
               (x, y + 0.02 * s)]
        eye = (x + 0.012 * s, y - 0.085 * s)
    else:
        k = ease(seg(t, POP, POP + 0.15))
        pts = [(x, y - (0.06 + 0.035 * k) * s), (x, y + 0.02 * s)]
        eye = (x, y - (0.06 + 0.035 * k) * s)
        if t < POP + 0.45:
            for i, a in enumerate((-160, -120, -60, -20)):
                ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
                pg.stroke([(x + ca * 0.07, y - 0.04 + sa * 0.07),
                           (x + ca * 0.1, y - 0.04 + sa * 0.1)], f"pop{i}",
                          2.4)
    pg.stroke(smooth(pts), "q", 6.0)
    pg.fill(ellipse(x, y + 0.045 * s, 0.011 * s, 0.011 * s, overshoot=0),
            "qd", dd.INK, 0.95, grain=0)
    white = ellipse(eye[0], eye[1], 0.014 * s, 0.016 * s, overshoot=0)
    pg.cover(white, "qew", (255, 255, 255), 1.0)
    pg.stroke(white, "qewl", 2.0)
    pg.cover(ellipse(eye[0] + 0.004 * s, eye[1] + 0.002, 0.006 * s,
                     0.007 * s, overshoot=0), "qe", dd.DARK, 1.0)


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
        character(pg, t)
        pg.text("Ask anything.", (0.5, 0.40), 0.085, "l1",
                reveal=ease(seg(t, 1.1, 1.9)), angle=-2)
        pg.text("Interrupt anytime.", (0.5, 0.51), 0.085, "l2",
                reveal=ease(seg(t, 2.0, 2.8)), angle=-2)
        k = ease(seg(t, 3.1, 3.5))
        if k > 0:
            x0, x1 = 0.24, 0.24 + 0.52 * k
            pg.fill([(x0, 0.64), (x1, 0.625), (x1 + 0.01, 0.705),
                     (x0 - 0.01, 0.715)], "hl", dd.TEAL, 0.7)
        pg.text("Brainback", (0.5, 0.665), 0.11, "logo",
                reveal=ease(seg(t, 3.3, 4.1)), angle=-2)
        pg.text("the AI tutor that loves questions", (0.5, 0.78), 0.042,
                "sub", bold=False, reveal=ease(seg(t, 4.3, 4.9)), angle=-1)
        pg.render(path)
        print(f"frame {i}", flush=True)


if __name__ == "__main__":
    main()
