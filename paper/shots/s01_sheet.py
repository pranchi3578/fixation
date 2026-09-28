"""Step 1: one torn ruled sheet on a kraft desk under a lamp."""

import math
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import bpy  # noqa: E402

import stage  # noqa: E402

stage.reset(samples=64, res=(1080, 1080))
stage.tabletop()
stage.ambient()
stage.practical()

# A5-ish sheet, 10.5 x 14.8 cm, lying with a soft curl
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0.0004))
sheet = bpy.context.object
sheet.scale = (0.105, 0.148, 1)
sheet.rotation_euler = (0, 0, math.radians(-12))
bpy.ops.object.transform_apply(scale=True)
bpy.ops.object.mode_set(mode="EDIT")
bpy.ops.mesh.subdivide(number_cuts=30)
bpy.ops.object.mode_set(mode="OBJECT")
for v in sheet.data.vertices:  # the torn edge lifts, as paper does
    v.co.z += 0.012 * max(0.0, (-v.co.x - 0.02) / 0.0325) ** 2
sheet.data.materials.append(stage.paper_material("ruled_1"))
sol = sheet.modifiers.new("thick", "SOLIDIFY")
sol.thickness = 0.0001
bpy.ops.object.shade_smooth()

stage.camera(loc=(0.02, -0.26, 0.2), target=(0, 0, 0.0))

t = time.time()
stage.render_still(sys.argv[-1] if sys.argv[-1].endswith(".png")
                   else "paper/out/s01_sheet.png")
print(f"render {time.time() - t:.1f}s")
