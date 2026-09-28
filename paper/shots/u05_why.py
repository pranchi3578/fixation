"""
"Unmute", beat 5: the first word of the film.

  0.0-1.2  Meera faces the lantern. It waits: a slow, patient pulse.
           Worried brows. Her hand rests on the desk.
  1.2-2.0  Her hand rises toward the red tape over her mic...
  2.0-2.4  ...and pulls back. She looks down at it.
  2.4-2.8  It goes back. She takes hold of the tape's end.
  2.8-3.6  She peels it off.
  3.6-3.9  Hand drops away, tape with it.
  3.8      "Why?" -- mouth open, brows up. The lantern jumps bright.
           The Doubtling on the desk lifts its head.
  4.3-6.0  She half-smiles. The lantern glows, starting to answer.

Shot on twos; resumable; seeded boil. Same conventions as s04_pilot.py.
"""

import math
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import bpy  # noqa: E402
import numpy as np  # noqa: E402

import cutouts  # noqa: E402
import puppets  # noqa: E402
import stage  # noqa: E402
from puppets import Pose  # noqa: E402

FPS_UNIQUE = 12
DURATION = 6.0
GLOW = (0.12, 0.85, 0.78)     # placeholder for Brainback's colour
OUT = os.environ.get("OUT", "paper/build/u05_frames")
RES = int(os.environ.get("RES", 1080))
WHY = 3.8

BADGE = (0.078, 0.03)
Y_BODY, Y_BADGE, Y_TAPE, Y_ARM = 0.040, 0.034, 0.0335, 0.030


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def seg(t, a, b):
    return (t - a) / (b - a)


def lerp2(a, b, k):
    return (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)


def build(samples):
    stage.reset(samples=samples, res=(RES, RES))
    stage.tabletop()
    stage.ambient(strength=0.05)
    stage.practical(loc=(-0.22, -0.12, 0.2), energy=2.4, size=0.06)
    bpy.ops.mesh.primitive_plane_add(size=1.2, location=(0, 0.16, 0.3),
                                     rotation=(math.radians(90), 0, 0))
    bpy.context.object.data.materials.append(
        stage.paper_material("sugar_night_5", translucency=0))

    meera = cutouts.Meera((-0.012, Y_BODY, 0.052))
    cutouts.mic_badge(BADGE, Y_BADGE)
    tape = cutouts.Tape(BADGE, Y_TAPE)
    body, tutor = cutouts.lantern((0.108, 0.05, 0), GLOW)
    # its light on her face: the lantern's spill, as a soft card-sized source
    spill = bpy.data.lights.new("spill", "AREA")
    spill.size = 0.05
    spill.color = GLOW
    so = bpy.data.objects.new("spill", spill)
    bpy.context.collection.objects.link(so)
    so.location = (0.17, -0.06, 0.1)
    stage.aim(so, (-0.01, 0.04, 0.075))
    tutor["spill"] = so.name

    d = puppets.build("doubtling")
    d.data.materials.append(stage.paper_material("doubt_open"))
    d.scale = (0.75, 0.75, 0.75)
    d.location = (-0.042, 0.0, 0)
    d.rotation_euler.z = math.radians(90)    # faces the lantern

    # the tile: a dark card window right in front of the lens
    bpy.ops.mesh.primitive_plane_add(size=0.108, location=(0.022, -0.13, 0.074),
                                     rotation=(math.radians(90), 0, 0))
    fr = bpy.context.object
    fr.data.materials.append(stage.paper_material("frame", translucency=0))

    stage.camera(loc=(0.022, -0.26, 0.085), target=(0.022, 0.04, 0.06),
                 lens=50, fstop=5.6, focus=0.3)
    return meera, tape, tutor, d


def timeline(t, tape):
    grab = tape.grab_point()
    rest = (0.05, 0.006)
    hover = (grab[0] - 0.006, grab[1] - 0.004)
    retreat = (grab[0] - 0.016, grab[1] - 0.012)
    p, hand = 0.0, rest
    if t < 1.2:
        hand = rest
    elif t < 2.0:
        hand = lerp2(rest, hover, ease(seg(t, 1.2, 2.0)))
    elif t < 2.4:
        hand = lerp2(hover, retreat, ease(seg(t, 2.0, 2.4)))
    elif t < 2.8:
        hand = lerp2(retreat, grab, ease(seg(t, 2.4, 2.8)))
    elif t < 3.6:
        p = ease(seg(t, 2.8, 3.6))
        front = np.array(grab) + tape.d * p * tape.L
        hand = tuple(front + np.array([0.004, 1.0]) * p * tape.L * 0.9)
    else:
        p = 1.0
        k = ease(seg(t, 3.6, 4.0))
        end = np.array(grab) + tape.d * tape.L
        up = tuple(end + np.array([0.004, 1.0]) * tape.L * 0.9)
        hand = lerp2(up, (0.05, -0.03), k)          # drops below the desk

    pulse = 0.5 + 0.12 * math.sin(t * 2 * math.pi / 1.6)
    if t >= WHY:
        k = ease(seg(t, WHY, WHY + 0.17))
        pulse = pulse * (1 - k) + (2.2 + 0.15 * math.sin(t * 17)) * k
    face = dict(mouth="line", brows="worried", gaze=(0.001, 0))
    if 2.0 <= t < 2.8:
        face["gaze"] = (0.0012, -0.0012)             # looks down at the tape
    if WHY <= t < WHY + 0.5:
        face.update(mouth="o", brows="up", gaze=(0.0012, 0.0006))
    elif t >= WHY + 0.5:
        face.update(mouth="smile", brows="brave", gaze=(0.0012, 0.0003))
    head_tilt = -4 * ease(seg(t, WHY - 0.1, WHY + 0.2))
    hop = 0.003 * math.sin(math.pi * min(1, max(0, seg(t, WHY, WHY + 0.3))))
    dq = Pose(pitch=95, hook=190, droop=55, tail=12, hook_from=0.3)
    dup = Pose(pitch=95, hook=120, droop=45, tail=8, hook_from=0.3)
    dpose = Pose.lerp(dq, dup, ease(seg(t, WHY + 0.1, WHY + 0.6)))
    return dict(p=p, hand=hand, pulse=pulse, face=face, tilt=head_tilt,
                hop=hop, dpose=dpose)


def main():
    samples = int(os.environ.get("SAMPLES", 32))
    n = int(DURATION * FPS_UNIQUE)
    first, last = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 \
        else (0, n - 1)
    os.makedirs(OUT, exist_ok=True)
    meera, tape, tutor, d = build(samples)
    for i in range(first, last + 1):
        path = os.path.join(OUT, f"f{i:03d}.png")
        if os.path.exists(path):
            continue
        t = i / FPS_UNIQUE
        rng = np.random.default_rng(5000 + i)
        s = timeline(t, tape)
        j = rng.normal(0, 0.00025, 2)                 # hand-moved boil
        hand = (s["hand"][0] + j[0], s["hand"][1] + j[1])
        meera.reach(hand, Y_ARM)
        tape.peel(s["p"], hand if s["p"] > 0 else None)
        meera.face(**s["face"])
        meera.head.rotation_euler.y = math.radians(s["tilt"]
                                                   + rng.normal(0, 0.4))
        meera.root.location.z = 0.052 + rng.normal(0, 0.0002)
        tutor.data.energy = 0.2 * s["pulse"]
        bpy.data.objects[tutor["spill"]].data.energy = 0.35 * s["pulse"]
        tutor.location.z = 0.034 + s["hop"]
        puppets.pose(d, s["dpose"], jitter=0.5, rng=rng)
        st = time.time()
        stage.render_still(path)
        print(f"frame {i}/{n - 1} t={t:.2f}s {time.time() - st:.1f}s",
              flush=True)


if __name__ == "__main__":
    main()
