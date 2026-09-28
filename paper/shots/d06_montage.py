"""
"Unmute", beat 6: the interruption montage. At her pace, not the class's.

The screen splits: Meera on the left, the tutor top-right, its lesson board
below. Every time she speaks, the tutor stops mid-stroke and turns to her.
Every answer lets one crumpled question out of her box: it rises into
frame, opens into a paper plane and flies.

  0-3     "wait -- why squared?"   pen stops mid-line; tutor answers with a
                                   triangle; plane 1
  3-6     "but why?"               stops again; "Pythagoras!"; plane 2
  6-9     "go back!"               the page flips straight back; plane 3
  9-12.5  "and cos?" "tan?" "sec??" -- it keeps up, tick tick tick;
                                   a little flock; she's laughing

Usage: python paper/shots/d06_montage.py [first last]
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

import doodle as dd  # noqa: E402
import doodle_cast as cast  # noqa: E402
import paper  # noqa: E402
from doodle import ellipse, rrect, smooth  # noqa: E402

FPS_UNIQUE = 12
DURATION = 12.5
OUT = os.environ.get("OUT", "paper/build/d06_frames")
RES = int(os.environ.get("RES", 1080))

SCR = (0.06, 0.08, 0.94, 0.95)
M_TILE = (0.07, 0.10, 0.48, 0.82)
M_SRC = (0.20, 0.25, 0.60, 0.95)          # the part of her webcam we show
BOARD = (0.51, 0.34, 0.93, 0.82)
T_TILE = (0.62, 0.11, 0.86, 0.31)

# her lines: (start, end, text)
LINES = [(1.0, 2.1, "wait — why squared?"), (4.0, 4.9, "but why?"),
         (6.6, 7.3, "go back!"), (9.0, 9.6, "and cos?"),
         (9.7, 10.3, "tan?"), (10.4, 11.0, "sec??")]
# the tutor talks whenever she doesn't, in these windows
TALK = [(0.1, 1.0), (2.2, 4.0), (5.0, 6.6), (7.3, 9.0), (9.6, 9.7),
        (10.3, 10.4), (11.0, 12.5)]
# planes: (launch time, from x)
PLANES = [(2.5, 0.30), (5.4, 0.22), (8.1, 0.36), (9.7, 0.26), (10.4, 0.32),
          (11.1, 0.20), (11.3, 0.38)]


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def seg(t, a, b):
    return (t - a) / (b - a)


def speaking(t):
    return next((ln for ln in LINES if ln[0] <= t < ln[1]), None)


def interrupted(t):
    """The tutor has just been cut off: from her first word until she
    finishes (it waits for the whole question)."""
    return speaking(t) is not None


# ------------------------------------------------------------------ board --

def reveal(t, spans):
    """Reveal progress for a board item written in pieces: spans are
    (t0, t1, from, to). Frozen between spans -- that's an interruption."""
    r = 0.0
    for t0, t1, a, b in spans:
        if t >= t0:
            r = a + (b - a) * ease(seg(t, t0, t1))
    return r


def page_one(pg, t, ticks):
    r1 = reveal(t, [(0.1, 1.0, 0, 0.62), (2.2, 2.5, 0.62, 1.0)])
    pg.text("sin²A + cos²A = 1", (0.5, 0.14), 0.085, "b1", reveal=r1,
            angle=-1)
    if 1.0 <= t < 2.2:                         # the pen stops, mid-line
        pg.stroke([(0.63, 0.1), (0.63, 0.18)], "pz1", 3.0, dd.TEAL)
        pg.stroke([(0.65, 0.1), (0.65, 0.18)], "pz2", 3.0, dd.TEAL)
    rt = ease(seg(t, 2.3, 2.9))
    if rt > 0:
        pg.stroke([(0.15, 0.62), (0.55, 0.62), (0.55, 0.3), (0.15, 0.62)],
                  "tri", 2.6, reveal=rt)
        if rt >= 1:
            pg.text("hyp", (0.3, 0.42), 0.055, "th")
            pg.text("opp", (0.63, 0.47), 0.055, "to")
            pg.text("adj", (0.35, 0.68), 0.055, "ta")
    r2 = reveal(t, [(3.2, 4.0, 0, 0.7), (5.0, 5.3, 0.7, 1.0)])
    pg.text("opp² + adj² = hyp²", (0.5, 0.8), 0.07, "b2", reveal=r2,
            angle=-1)
    if 4.0 <= t < 5.0:
        pg.stroke([(0.66, 0.76), (0.66, 0.84)], "pz3", 3.0, dd.TEAL)
        pg.stroke([(0.68, 0.76), (0.68, 0.84)], "pz4", 3.0, dd.TEAL)
    rp = ease(seg(t, 5.2, 5.6))
    if rp > 0:
        pg.text("Pythagoras!", (0.78, 0.33), 0.06, "py", reveal=rp,
                angle=-8)
        star = [(0.93 + 0.035 * math.cos(math.radians(-90 + 144 * i)),
                 0.24 + 0.035 * math.sin(math.radians(-90 + 144 * i)))
                for i in range(6)]
        pg.stroke(star, "star", 2.2, (230, 170, 30), reveal=rp)
    if t >= 7.5:                               # back here, and again, slower
        k = ease(seg(t, 7.5, 8.0))
        pg.fill(ellipse(0.5, 0.14, 0.45, 0.075), "hl", dd.TEAL, 0.45 * k)
    for i, (tt, text, y) in enumerate(ticks):
        if t >= tt:
            k = ease(seg(t, tt, tt + 0.3))
            pg.stroke([(0.08, y), (0.11, y + 0.025), (0.17, y - 0.03)],
                      f"tk{i}", 2.8, (40, 150, 70), reveal=k)
            pg.text(text, (0.45, y), 0.058, f"tt{i}", reveal=k, bold=True,
                    angle=0)


def page_two(pg, t):
    r = reveal(t, [(6.25, 6.6, 0, 0.55)])
    pg.text("tan A = sin A / cos A", (0.5, 0.14), 0.075, "p2", reveal=r,
            angle=-1)


def board(pg, t):
    h = (BOARD[3] - BOARD[1]) / (BOARD[2] - BOARD[0])
    pg.push_rect((0, 0, 1, h), BOARD)
    card = rrect(0, 0, 1, h, 0.03)
    pg.fill(card, "bdf", (255, 255, 252), 0.9, grain=0)
    pg.begin_clip((0, 0, 1, h))
    ticks = [(9.65, "cos A = adj / hyp", 0.9), (10.35, "tan A = opp / adj",
                                                 0.98),
             (11.05, "sec A = 1 / cos A", 1.06)]
    pg.push(0, -0.06 * ease(seg(t, 9.3, 9.8)), 1)   # make room for ticks
    # page turn forward at 6.0, and straight back at 7.0
    fwd = ease(seg(t, 6.0, 6.2)) * (1 - ease(seg(t, 7.0, 7.25)))
    if fwd < 1:
        pg.push(-fwd, 0, 1)
        page_one(pg, t, ticks)
        pg.pop()
    if fwd > 0:
        pg.push(1 - fwd, 0, 1)
        page_two(pg, t)
        pg.pop()
        if 0 < fwd < 1:
            for i in range(3):
                y = 0.2 + 0.15 * i
                pg.stroke([(0.1, y), (0.9, y)], f"sp{i}", 1.8, alpha=110)
    pg.pop()
    pg.end_clip()
    pg.stroke(card, "bd", 2.4)
    pg.pop()


# ------------------------------------------------------------ characters --

def meera_face(t):
    ln = speaking(t)
    face = dict(mouth="smile", brows="brave", gaze=(0.01, -0.004))
    if ln:
        talking = int((t - ln[0]) * 9) % 2 == 0
        face["mouth"] = "o" if talking else "line"
        face["brows"] = "up"
    if t >= 11.2:
        face.update(mouth="o" if int(t * 8) % 2 else "smile", brows="brave")
    return face


def her_tile(pg, t):
    pg.begin_clip(M_TILE)
    pg.push_rect(M_SRC, M_TILE)
    pg.fill([(0, 0), (1, 0), (1, 1), (0, 1)], "mbg", (250, 247, 238), 0.5,
            grain=0)
    lift = 0.012 * ease(seg(t, 0, 12.5))       # she sits up, bit by bit
    pg.push(0, -lift, 1)
    cast.meera(pg, t, meera_face(t))
    pg.pop()
    pg.pop()
    pg.end_clip()
    pg.stroke(rrect(*M_TILE, 0.015), "mt", 2.4)


def her_bubble(pg, t):
    ln = speaking(t)
    if not ln:
        return
    k = ease(seg(t, ln[0], ln[0] + 0.15))
    size = 0.052 if len(ln[2]) > 10 else 0.065
    w = 0.12 + 0.012 * len(ln[2])
    cx, cy = 0.33 + w / 2, 0.52
    b = smooth([(cx - w / 2, cy), (cx - w / 2 + 0.02, cy - 0.06),
                (cx + w / 2 - 0.02, cy - 0.065), (cx + w / 2, cy),
                (cx + w / 2 - 0.03, cy + 0.06), (cx - w / 2 + 0.05, cy + 0.06),
                (cx - w / 2, cy)]) + [(cx - w / 2 + 0.02, cy - 0.04),
                                      (0.3, 0.41)]
    pg.fill(b[:-2], "hbf" + ln[2], (255, 255, 255), 0.95 * k, grain=0)
    pg.cover(b[:-2], "hbc" + ln[2], (255, 255, 255), 0.9 * k)
    pg.stroke(b, "hb" + ln[2], 2.6, reveal=k)
    pg.text(ln[2], (cx, cy), size, "ht" + ln[2],
            reveal=ease(seg(t, ln[0] + 0.05, ln[0] + 0.3)), angle=-3)


def tutor_tile(pg, t):
    pg.stroke(rrect(*T_TILE, 0.015), "tt", 2.4)
    cut = interrupted(t)
    talking = any(a <= t < b for a, b in TALK) and not cut
    wide = 1.0 if cut else 0.2
    glow = 0.9 if cut else 0.5 + 0.08 * math.sin(t * 4)
    cast.tutor_face(pg, 0.74, 0.205, 0.058, "tu", glow=glow, wide=wide,
                    talking=talking, t=t)
    if cut:                                    # all ears
        for i in range(3):
            r = 0.075 + 0.014 * i
            pg.stroke(ellipse(0.74, 0.205, r, r, 150, 210, 8, 0), f"ear{i}",
                      2.0)
    pg.text("Brainback tutor", (0.74, 0.335), 0.028, "tlab", bold=False,
            angle=-2)


def planes(pg, t):
    for i, (t0, x0) in enumerate(PLANES):
        if t < t0:
            continue
        u = t - t0
        if u < 0.35:                            # a crumpled ball rises
            k = ease(u / 0.35)
            x, y = x0, 0.95 - 0.2 * k
            rr = 0.042
            pts = [(x + rr * (0.85 + 0.3 * ((j * 7) % 5) / 5)
                    * math.cos(2 * math.pi * j / 11),
                    y + rr * (0.85 + 0.3 * ((j * 3) % 5) / 5)
                    * math.sin(2 * math.pi * j / 11)) for j in range(12)]
            pg.cover(pts, f"pb{i}", (246, 244, 238), 1.0)
            pg.stroke(pts, f"pbl{i}", 2.0)
        elif u < 1.6:                           # opens, and flies
            k = (u - 0.35) / 1.25
            x = x0 + (1.1 - x0) * ease(k) ** 1.3
            y = 0.75 - 0.8 * k + 0.08 * math.sin(math.pi * k)
            heading = math.atan2(-0.8, (1.1 - x0) * 1.3) - 0.2 * math.cos(
                math.pi * k)
            size = 0.055 * (0.5 + 0.5 * min(1, k * 4))
            trail = [(x0 + (1.1 - x0) * ease(max(0, k - d)) ** 1.3,
                      0.75 - 0.8 * max(0, k - d)
                      + 0.08 * math.sin(math.pi * max(0, k - d)))
                     for d in (0.25, 0.18, 0.11, 0.05)]
            pg.stroke(trail, f"tr{i}", 1.6, alpha=120)
            cast.paper_plane(pg, f"pl{i}", x, y, size, heading)


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
        pg.stroke(rrect(*SCR, 0.02), "screen", 2.4)
        her_tile(pg, t)
        tutor_tile(pg, t)
        board(pg, t)
        cast.toolbar(pg, muted=False)
        her_bubble(pg, t)
        planes(pg, t)
        pg.render(path)
        print(f"frame {i}", flush=True)


if __name__ == "__main__":
    main()
