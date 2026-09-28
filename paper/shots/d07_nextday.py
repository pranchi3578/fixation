"""
"Unmute", beat 7: the next day. The opening again -- until she unmutes.

  0.0-1.5   The same class, the same racing slides. Meera sits up.
  1.5       "Any questions?"  Silence.
  4.0-4.4   Her cursor goes straight to the mic. Click. The slash goes.
  4.6       "Sir, why squared?"
  6.0       His eyebrows go up. Then a smile: "Good question!"
  6.8-10    The other tiles unmute, one by one. The sleeper wakes.
            "?"s pop up; paper planes cross the grid.
  10-12     The grid alive; a slow push in.

Reuses the opening's layout and slides (d01_class.py).
Usage: python paper/shots/d07_nextday.py [first last]
"""

import math
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "lib"))
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402

import d01_class as c  # noqa: E402
import doodle as dd  # noqa: E402
import doodle_cast as cast  # noqa: E402
import paper  # noqa: E402
from doodle import ellipse, rrect, smooth  # noqa: E402

FPS_UNIQUE = 12
DURATION = 12.0
OUT = os.environ.get("OUT", "paper/build/d07_frames")
RES = int(os.environ.get("RES", 1080))

ASK, CLICK, SAY, SAY_END, REPLY, WAVE, PUSH = 1.5, 4.4, 4.6, 5.8, 6.0, 6.8, \
    9.8
ORDER = [(1, 0), (1, 2), (0, 1), (2, 1), (0, 0), (2, 2), (0, 2), (2, 0),
         (3, 0), (3, 1)]                        # who unmutes, in order
ASKERS = {(0, 1), (2, 2), (3, 0), (1, 2)}      # who pops a "?"
PLANES = [(7.2, (1, 0), (0.1, 0.2)), (7.9, (0, 1), (0.3, -0.1)),
          (8.5, (2, 2), (0.2, 0.9)), (9.0, (1, 2), (0.05, 0.6)),
          (9.6, (3, 0), (0.4, 1.1)), (10.1, (0, 0), (0.25, 0.4)),
          (10.6, (2, 1), (0.1, 0.85))]


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def seg(t, a, b):
    return (t - a) / (b - a)


def lerp(a, b, k):
    return (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)


def unmute_time(rc):
    if rc == c.MEERA_RC:
        return CLICK
    if rc in ORDER:
        return WAVE + 0.3 * ORDER.index(rc)
    return 1e9


def centre(rc):
    x0, y0, x1, y1 = c.tile(*rc)
    return ((x0 + x1) / 2, (y0 + y1) / 2)


# ------------------------------------------------------------------ call --

def presentation(pg, t):
    n = int(min(t, ASK) / 0.55)
    k = (t % 0.55) / 0.15 if t < ASK else 1
    pg.push_rect((0, 0, 1, 1), c.PRES)
    pg.begin_clip((0, 0, 1, 1))
    c.slide(pg, n + 3, t)
    if k < 1:
        pg.push(1 - ease(k), 0, 1)
        c.slide(pg, n + 4, t)
        pg.pop()
    pg.end_clip()
    pg.pop()


def teacher_tile(pg, t):
    T = c.TEACH
    h = (T[3] - T[1]) / (T[2] - T[0])
    pg.push_rect((0, 0, 1, h), T)
    pg.begin_clip((0, 0, 1, h))
    pg.fill([(0, 0), (1, 0), (1, h), (0, h)], "tchbg", (250, 247, 238), 0.6,
            grain=0)
    talking = t < ASK + 0.6 or REPLY <= t < REPLY + 1.2
    mood = "plain"
    if SAY <= t < REPLY:
        mood = "surprised"
    elif t >= REPLY:
        mood = "smile"
    pg.push(0.2, -0.02, 0.6)
    cast.teacher(pg, t, talking=talking, mood=mood)
    pg.pop()
    pg.end_clip()
    border = rrect(0, 0, 1, h, 0.04)
    if talking:
        pg.stroke(border, "tspk", 5.0, (240, 200, 40), alpha=200)
    pg.stroke(border, "tchb", 2.2)
    pg.pop()


def tiles(pg, t):
    for r in range(c.ROWS):
        for col in range(c.COLS):
            rc = (r, col)
            rect = c.tile(*rc)
            seed = r * c.COLS + col + 3
            live = t >= unmute_time(rc)
            pg.push_rect((0, 0, 1, 1), rect)
            pg.begin_clip((0, 0, 1, 1))
            pg.fill([(0, 0), (1, 0), (1, 1), (0, 1)], f"tbg{seed}",
                    (250, 247, 238), 0.6, grain=0)
            if rc == c.MEERA_RC:
                pg.pop()
                meera(pg, t, rect)
                pg.push_rect((0, 0, 1, 1), rect)
            elif rc == (c.ROWS - 1, c.COLS - 1):
                pg.text("+48", (0.5, 0.5), 0.35, "more")
            else:
                awake = rc != c.ASLEEP_RC or t >= WAVE + 0.3 * 5 - 0.4
                look = 0.0
                if SAY <= t < REPLY + 0.5:          # everyone turns to her
                    mx, my = centre(c.MEERA_RC)
                    cx, cy = centre(rc)
                    look = 0.03 * np.sign(mx - cx)
                cast.classmate(pg, t, seed, look=look, asleep=not awake)
            if rc != (c.ROWS - 1, c.COLS - 1):
                if live:
                    cast.unmuted_badge(pg, f"t{seed}")
                else:
                    cast.muted_badge(pg, f"t{seed}")
                if live and rc in ASKERS and rc != c.MEERA_RC:
                    k = ease(seg(t, unmute_time(rc) + 0.15,
                                 unmute_time(rc) + 0.35))
                    b = ellipse(0.76, 0.24, 0.2 * k, 0.18 * k)
                    pg.fill(b, f"qb{seed}", (255, 255, 255), 0.9, grain=0)
                    pg.cover(b, f"qbc{seed}", (255, 255, 255), 0.9)
                    pg.stroke(b, f"qbl{seed}", 2.2)
                    if k > 0.8:
                        pg.text("?", (0.76, 0.24), 0.3, f"qbt{seed}")
            pg.end_clip()
            speaking = live and t < unmute_time(rc) + (
                SAY_END - CLICK if rc == c.MEERA_RC else 0.6)
            if rc == c.MEERA_RC and SAY <= t < SAY_END:
                speaking = True
            if speaking:
                pg.stroke(rrect(0, 0, 1, 1, 0.06), f"sp{seed}", 6.0,
                          dd.TEAL, alpha=230)
            pg.stroke(rrect(0, 0, 1, 1, 0.06), f"tb{seed}", 2.2)
            pg.pop()


def meera(pg, t, rect):
    face = dict(mouth="smile", brows="brave", gaze=(0.0, -0.004))
    if ASK <= t < CLICK:
        face.update(mouth="line", brows="brave", gaze=(0.0, 0.008))
    if SAY <= t < SAY_END:
        talking = int((t - SAY) * 9) % 2 == 0
        face.update(mouth="o" if talking else "line", brows="up",
                    gaze=(-0.008, -0.004))
    pg.push_rect(c.SCR, rect)
    pg.begin_clip(c.SCR)
    pg.push(0, -0.012, 1)                        # sitting up
    cast.meera(pg, t, face)
    pg.pop()
    pg.end_clip()
    pg.pop()


def bubbles(pg, t):
    # the teacher asks
    k = ease(seg(t, ASK, ASK + 0.25)) * (1 - ease(seg(t, 3.8, 4.0)))
    if k > 0:
        b = smooth([(0.40, 0.2), (0.44, 0.13), (0.55, 0.115), (0.62, 0.15),
                    (0.61, 0.22), (0.52, 0.24), (0.45, 0.235), (0.40, 0.2)])
        pg.fill(b, "askf", (255, 255, 255), 0.9 * k, grain=0)
        pg.cover(b, "askc", (255, 255, 255), 0.9 * k)
        pg.stroke(b + [(0.61, 0.22), (0.64, 0.24)], "ask", 2.6, reveal=k)
        pg.text("Any questions?", (0.51, 0.178), 0.045, "askt", reveal=k)
    # she asks
    k = ease(seg(t, SAY, SAY + 0.2)) * (1 - ease(seg(t, 7.6, 7.9)))
    if k > 0:
        b = smooth([(0.26, 0.46), (0.29, 0.39), (0.46, 0.375), (0.59, 0.4),
                    (0.61, 0.46), (0.5, 0.52), (0.32, 0.52), (0.26, 0.46)])
        pg.fill(b, "sayf", (255, 255, 255), 0.95 * k, grain=0)
        pg.cover(b, "sayc", (255, 255, 255), 0.9 * k)
        pg.stroke(b + [(0.61, 0.46), (0.728, 0.459)], "say", 2.8, reveal=k)
        pg.text("Sir, why squared?", (0.435, 0.45), 0.055, "sayt",
                reveal=ease(seg(t, SAY + 0.1, SAY + 0.6)))
    # and he's glad she did
    k = ease(seg(t, REPLY, REPLY + 0.25)) * (1 - ease(seg(t, 8.2, 8.5)))
    if k > 0:
        b = smooth([(0.40, 0.2), (0.44, 0.13), (0.55, 0.115), (0.62, 0.15),
                    (0.61, 0.22), (0.52, 0.24), (0.45, 0.235), (0.40, 0.2)])
        pg.fill(b, "gqf", (255, 255, 255), 0.9 * k, grain=0)
        pg.cover(b, "gqc", (255, 255, 255), 0.9 * k)
        pg.stroke(b + [(0.61, 0.22), (0.64, 0.24)], "gq", 2.6, reveal=k)
        pg.text("Good question!", (0.51, 0.178), 0.047, "gqt", reveal=k)


def planes(pg, t):
    for i, (t0, rc, dest) in enumerate(PLANES):
        u = (t - t0) / 1.4
        if not 0 <= u <= 1:
            continue
        a = centre(rc)
        x = a[0] + (dest[0] - a[0]) * ease(u)
        y = a[1] + (dest[1] - a[1]) * u - 0.08 * math.sin(math.pi * u)
        dx, dy = dest[0] - a[0], dest[1] - a[1] - 0.08 * math.pi * math.cos(
            math.pi * u)
        cast.paper_plane(pg, f"pl{i}", x, y, 0.045, math.atan2(dy, dx))


def view(t):
    """A slow push toward the grid as it comes alive."""
    k = ease(seg(t, PUSH, DURATION))
    x0, y0, x1, y1 = c.SCR
    gx, gy = 0.72, 0.5
    s = 1 - 0.18 * k
    w, h = (x1 - x0) * s, (y1 - y0) * s
    cx = (x0 + x1) / 2 + (gx - (x0 + x1) / 2) * 0.35 * k
    cy = (y0 + y1) / 2 + (gy - (y0 + y1) / 2) * 0.2 * k
    return (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)


# ---------------------------------------------------------------- screen --

def toolbar(pg, t):
    muted = t < CLICK + 0.1
    cast.toolbar(pg, muted=muted)
    if CLICK <= t < CLICK + 0.6:                  # the slash, scribbled out
        k = ease(seg(t, CLICK, CLICK + 0.3))
        zig = [(0.375 + 0.05 * i / 11 + (0.012 if i % 2 else -0.012),
                0.85 + 0.05 * i / 11 + (-0.012 if i % 2 else 0.012))
               for i in range(12)]
        pg.stroke(zig, "scribble", 2.2, reveal=k,
                  alpha=int(235 * (1 - ease(seg(t, CLICK + 0.3,
                                                  CLICK + 0.6)))))


def cursor_at(t):
    idle = (0.76, 0.62)
    at = (c.MIC[0] + 0.002, c.MIC[1] - 0.004)
    if t < 4.0:
        return (idle[0] + 0.004 * math.sin(t * 3), idle[1])
    if t < CLICK:
        return lerp(idle, at, ease(seg(t, 4.0, CLICK)))
    return lerp(at, (0.52, 0.78), ease(seg(t, CLICK + 0.4, CLICK + 1.0)))


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
        pg.begin_clip(c.SCR)
        pg.push_rect(view(t), c.SCR)
        presentation(pg, t)
        teacher_tile(pg, t)
        tiles(pg, t)
        bubbles(pg, t)
        planes(pg, t)
        pg.pop()
        pg.end_clip()
        pg.stroke(rrect(*c.SCR, 0.02), "screen", 2.4)
        toolbar(pg, t)
        c.cursor(pg, cursor_at(t))
        pg.render(path)
        print(f"frame {i}", flush=True)


if __name__ == "__main__":
    main()
