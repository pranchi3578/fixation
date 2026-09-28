"""
Step 4, the kill test: a Doubtling gets its answer and flies.

  0.0-1.2  "?" sulks: breathing, one blink
  1.0      the Glow comes on from off-screen (the phone; Brainback's colour)
  1.3-2.1  it straightens to "!", overshoots, settles
  2.1-2.6  "!" holds, blinks
  2.6-3.1  tips forward, wings snap open, hops
  3.1-4.6  flies off screen-right
  4.6-5.0  empty table, the Glow still on

Shot on twos: 12 unique frames a second, each its own pose with a little
hand-moved wobble. Renders are resumable -- existing frames are skipped.

Usage: python paper/shots/s04_pilot.py [first last]   (unique-frame range)
Env:   SAMPLES (default 32), RES (default 1080), OUT (frames dir)
"""

import math
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import bpy  # noqa: E402
import numpy as np  # noqa: E402

import puppets  # noqa: E402
import stage  # noqa: E402
from puppets import Pose  # noqa: E402

FPS_UNIQUE = 12
DURATION = 5.0
GLOW = (0.12, 0.85, 0.78)      # placeholder for Brainback's brand colour
OUT = os.environ.get("OUT", "paper/build/s04_frames")
RES = int(os.environ.get("RES", 1080))

Q = Pose(pitch=95, hook=190, droop=55, tail=12, hook_from=0.3)
EX = Pose(pitch=90, hook=0, droop=20, tail=0, hook_from=0.3)
OVER = Pose(pitch=86, hook=-14, droop=14, tail=-4, hook_from=0.3)
TIP = Pose(pitch=12, hook=-4, droop=-10, tail=0, hook_from=0.3)
FLY = Pose(pitch=6, hook=0, droop=-8, tail=0, hook_from=0.3)


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def ease_out(x):
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** 3


def seg(t, a, b):
    return (t - a) / (b - a)


def timeline(t):
    """Pose, position (y, z), roll, eye, glow for time t (seconds)."""
    y0, z = 0.035, 0.0
    y, roll, eye = y0, 0.0, "open"
    if t < 1.3:
        breath = math.sin(t * 2 * math.pi / 1.1)
        p = Pose(Q.pitch + 1.5 * breath, Q.hook + 4 * breath, Q.droop,
                 Q.tail, Q.hook_from)
        if 0.55 <= t < 0.72:
            eye = "closed"
        if t >= 1.05:            # notices the Glow: a small lift of the head
            p = Pose.lerp(p, Pose(97, 175, 52, 10, 0.3), ease(seg(t, 1.05, 1.3)))
    elif t < 1.8:
        p = Pose.lerp(Pose(97, 175, 52, 10, 0.3), OVER,
                      ease_out(seg(t, 1.3, 1.8)))
        z = 0.004 * math.sin(math.pi * seg(t, 1.3, 1.8))
    elif t < 2.1:
        p = Pose.lerp(OVER, EX, ease(seg(t, 1.8, 2.1)))
    elif t < 2.6:
        p = EX
        if 2.3 <= t < 2.42:
            eye = "closed"
    elif t < 3.1:
        k = ease(seg(t, 2.6, 3.1))
        p = Pose.lerp(EX, TIP, k)
        # rises as it tips so the keel clears the table: the launch hop
        z = puppets.K * k + 0.012 * math.sin(math.pi * k)
    else:
        k = seg(t, 3.1, 4.6)
        p = Pose.lerp(TIP, FLY, ease(k * 3))
        a = max(0.0, k)
        y = y0 - 0.55 * a ** 1.6
        z = puppets.K + 0.012 * math.sin(math.pi * min(1, k * 4)) \
            + 0.09 * a ** 1.8
        roll = 10 * math.sin(math.pi * min(1.0, a * 1.4))
    glow = ease(seg(t, 1.0, 1.25))
    return p, y, z, roll, eye, glow


def build_scene(samples):
    stage.reset(samples=samples, res=(RES, RES))
    stage.tabletop()
    stage.ambient(strength=0.05)
    stage.practical(loc=(-0.2, 0.14, 0.16), energy=3.2, size=0.04)
    bpy.ops.mesh.primitive_plane_add(size=1.2, location=(0.3, 0, 0.3),
                                     rotation=(0, math.radians(90), 0))
    bpy.context.object.data.materials.append(
        stage.paper_material("sugar_night_5", translucency=0))

    # the notebook it tore itself out of, behind, out of focus
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.14, 0.19, 0.006))
    nb = bpy.context.object
    nb.scale = (0.15, 0.21, 0.012)
    nb.rotation_euler.z = math.radians(18)
    nb.data.materials.append(stage.paper_material("ruled_1",
                                                  translucency=0.05))

    glow = bpy.data.lights.new("glow", "SPOT")
    glow.spot_size = math.radians(40)
    glow.spot_blend = 0.8
    glow.shadow_soft_size = 0.03
    glow.color = GLOW
    glow.energy = 0
    go = bpy.data.objects.new("glow", glow)
    bpy.context.collection.objects.link(go)
    go.location = (-0.12, 0.0, 0.07)
    stage.aim(go, (0, 0.035, 0.045))

    mats = {e: stage.paper_material(f"doubt_{e}") for e in ("open", "closed")}
    d = puppets.build("doubtling")
    d.data.materials.append(mats["open"])
    stage.camera(loc=(-0.3, -0.035, 0.1), target=(0, -0.03, 0.045),
                 lens=50, fstop=4.5, focus=0.31)
    return d, go, mats


def main():
    samples = int(os.environ.get("SAMPLES", 32))
    n = int(DURATION * FPS_UNIQUE)
    first, last = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 \
        else (0, n - 1)
    os.makedirs(OUT, exist_ok=True)
    d, glow, mats = build_scene(samples)
    for i in range(first, last + 1):
        path = os.path.join(OUT, f"f{i:03d}.png")
        if os.path.exists(path):
            continue
        t = i / FPS_UNIQUE
        rng = np.random.default_rng(1000 + i)     # same boil on re-render
        p, y, z, roll, eye, g = timeline(t)
        puppets.pose(d, p, jitter=0.6, rng=rng)
        d.location = (rng.normal(0, 0.0002), y + rng.normal(0, 0.0002), z)
        d.rotation_euler = (0, math.radians(roll), math.pi)
        d.data.materials[0] = mats[eye]
        glow.data.energy = 1.3 * g
        s = time.time()
        stage.render_still(path)
        print(f"frame {i}/{n - 1} t={t:.2f}s {time.time() - s:.1f}s",
              flush=True)


if __name__ == "__main__":
    main()
