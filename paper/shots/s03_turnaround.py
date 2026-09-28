"""Step 3: the Doubtling's three states side by side — ?  !  plane."""

import math
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import bpy  # noqa: E402

import puppets  # noqa: E402
import stage  # noqa: E402
from puppets import Pose  # noqa: E402

out = sys.argv[-1] if sys.argv[-1].endswith(".png") else \
    "paper/out/s03_turnaround.png"
stage.reset(samples=int(os.environ.get("SAMPLES", 48)), res=(1600, 900))
stage.tabletop()
stage.ambient(strength=0.06)
stage.practical(loc=(-0.2, 0.12, 0.16), energy=3.5, size=0.04)
# a dark paper wall behind, so the key falls off into night
bpy.ops.mesh.primitive_plane_add(size=1.2, location=(0.3, 0, 0.3),
                                 rotation=(0, math.radians(90), 0))
bpy.context.object.data.materials.append(
    stage.paper_material("sugar_night_5", translucency=0))

mat = stage.paper_material("doubt_open")
poses = [
    ("question", Pose(pitch=95, hook=190, droop=55, tail=12,
                      hook_from=0.3), 0.11, 0.0),
    ("exclaim", Pose(pitch=90, hook=0, droop=20, tail=0), 0.0, 0.0),
    ("plane", Pose(pitch=4, hook=0, droop=-8, tail=0), -0.09, 0.03),
]
for name, p, y, z in poses:
    ob = puppets.build(name)
    ob.data.materials.append(mat)
    puppets.pose(ob, p)
    ob.location = (0, y, z)
    ob.rotation_euler.z = math.pi          # face screen-right: reads ? ! >
    if name == "plane":
        ob.location.y += puppets.L / 2

stage.camera(loc=(-0.42, 0.0, 0.07), target=(0, 0, 0.035), lens=50,
             fstop=8)

t = time.time()
stage.render_still(out)
print(f"render {time.time() - t:.1f}s")
