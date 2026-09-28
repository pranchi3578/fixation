"""
Flat paper cut-outs: Meera, her mic badge, the red tape, the lantern.

A cut-out is a hand-cut outline in the X-Z plane (facing the camera, which
looks along +Y), given paper thickness. Layers are separated by fractions
of a millimetre in Y, the way pieces overlap on an animation table. Joints
are brass split pins, and they show, on purpose.

Outlines are in centimetres, relative to the piece's pivot.
"""

import math

import bmesh
import bpy
import numpy as np

import stage

RNG = np.random.default_rng(77)


# ------------------------------------------------------------ outlines ----

def _cut(pts, wobble=0.03):
    """Scissors never follow the line exactly."""
    out = []
    for x, z in pts:
        out.append((x + RNG.normal(0, wobble), z + RNG.normal(0, wobble)))
    return out


def ellipse(cx, cz, rx, rz, n=40, a0=0.0, a1=2 * math.pi):
    return [(cx + rx * math.cos(a0 + (a1 - a0) * i / n),
             cz + rz * math.sin(a0 + (a1 - a0) * i / n))
            for i in range(n + (0 if a1 - a0 >= 2 * math.pi - 1e-6 else 1))]


def capsule_down(length, w0, w1=None, n=10):
    """A limb hanging from its pivot at (0,0) down to (0,-length)."""
    w1 = w0 if w1 is None else w1
    top = ellipse(0, 0, w0 / 2, w0 / 2, n, 0, math.pi)
    bot = ellipse(0, -length, w1 / 2, w1 / 2, n, math.pi, 2 * math.pi)
    return top + bot


def rounded_poly(pts, r=0.3, n=4):
    """Round every corner of a polygon a little."""
    out = []
    k = len(pts)
    for i in range(k):
        p0, p1, p2 = (np.array(pts[(i - 1) % k]), np.array(pts[i]),
                      np.array(pts[(i + 1) % k]))
        a = p1 + (p0 - p1) / max(1e-6, np.linalg.norm(p0 - p1)) * r
        b = p1 + (p2 - p1) / max(1e-6, np.linalg.norm(p2 - p1)) * r
        for j in range(n + 1):
            t = j / n
            q = (1 - t) ** 2 * a + 2 * (1 - t) * t * p1 + t ** 2 * b
            out.append(tuple(q))
    return out


# -------------------------------------------------------------- pieces ----

def cutout(name, pts_cm, stock, loc=(0, 0, 0), parent=None, thick=0.0003,
           translucency=0.08, wobble=0.03, material=None):
    pts = _cut(pts_cm, wobble)
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new()
    vs = [bm.verts.new((x / 100, 0, z / 100)) for x, z in pts]
    f = bm.faces.new(vs)
    ox, oz = RNG.random(2)
    for loop in f.loops:
        co = loop.vert.co
        loop[uv].uv = (co.x * 100 / 14 + ox, co.z * 100 / 14 + oz)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    ob.data.materials.append(material or stage.paper_material(
        stock, translucency=translucency, bump=0.3))
    s = ob.modifiers.new("paper", "SOLIDIFY")
    s.thickness = thick
    s.offset = 0
    if parent:
        ob.parent = parent
    ob.location = loc
    return ob


def split_pin(name, parent, loc):
    """Brass paper fastener at a joint."""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.0024, segments=16,
                                         ring_count=8)
    p = bpy.context.object
    p.name = name
    p.scale = (1, 0.35, 1)
    if "brass" not in bpy.data.materials:
        m = bpy.data.materials.new("brass")
        m.use_nodes = True
        b = m.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = (0.78, 0.56, 0.24, 1)
        b.inputs["Metallic"].default_value = 1.0
        b.inputs["Roughness"].default_value = 0.35
    p.data.materials.append(bpy.data.materials["brass"])
    p.parent = parent
    p.location = loc
    return p


# --------------------------------------------------------------- Meera ----

class Meera:
    """Paper-doll teen. Pivots: neck base (root), head (neck top),
    right shoulder and elbow (screen-right arm, the one that reaches)."""

    UPPER, FORE = 0.040, 0.047          # arm lengths to elbow / fingertip

    def __init__(self, loc):
        self.root = bpy.data.objects.new("meera", None)
        bpy.context.collection.objects.link(self.root)
        self.root.location = loc
        r = self.root
        cutout("torso", rounded_poly(
            [(-3.9, -9), (-3.7, -0.9), (-2.6, 0), (2.6, 0), (3.7, -0.9),
             (3.9, -9)], 0.5), "shirt_32", (0, 0, 0), r)
        cutout("collar_l", [(-1.5, 0.05), (0, -1.5), (-0.1, 0.05)],
               "white_34", (0, -0.0004, 0), r)
        cutout("collar_r", [(1.5, 0.05), (0.1, 0.05), (0, -1.5)],
               "white_34", (0, -0.0004, 0), r)
        cutout("neck", rounded_poly([(-0.7, -0.6), (-0.65, 1.3),
                                     (0.65, 1.3), (0.7, -0.6)], 0.2),
               "skin_31", (0, 0.0006, 0), r)
        cutout("arm_l", capsule_down(6.2, 1.6, 1.3), "shirt_32",
               (-0.034, 0.0003, -0.008), r).rotation_euler.y = \
            math.radians(-8)

        self.head = bpy.data.objects.new("head", None)
        bpy.context.collection.objects.link(self.head)
        self.head.parent = r
        self.head.location = (0, -0.0006, 0.011)
        h = self.head
        cutout("face", ellipse(0, 2.3, 2.05, 2.35, 48), "skin_31",
               (0, 0, 0), h)
        cap = (ellipse(0, 2.45, 2.2, 2.45, 30, math.radians(-8),
                       math.radians(188))
               + [(-1.9, 2.6), (-0.9, 3.35), (0.3, 3.05), (1.3, 3.25),
                  (2.0, 2.4)])
        cutout("hair", cap, "hair_33", (0, -0.0003, 0), h)
        for side in (-1, 1):                      # two plaits, two ribbons
            for k in range(5):
                z = 1.3 - k * 0.95
                x = side * (2.05 - 0.05 * k)
                cutout(f"plait{side}{k}",
                       rounded_poly([(x - 0.5, z), (x, z + 0.6),
                                     (x + 0.5, z), (x, z - 0.6)], 0.2),
                       "hair_33", (0, -0.0003 - 0.0001 * k, 0), h)
            z = 1.3 - 5 * 0.95 + 0.2
            x = side * 1.8
            cutout(f"ribbon{side}", [(x, z), (x - 0.7, z + 0.45),
                                     (x - 0.7, z - 0.45), (x, z),
                                     (x + 0.7, z + 0.45),
                                     (x + 0.7, z - 0.45)],
                   "ribbon_36", (0, -0.0009, 0), h)
        ink = stage.flat_material("ink", (0.03, 0.03, 0.04), roughness=0.5)
        self.eyes = [cutout(f"eye{s}", ellipse(0, 0, 0.17, 0.19, 16),
                            None, (s * 0.0075, -0.0005, 0.022), h,
                            material=ink, wobble=0.005) for s in (-1, 1)]
        self.brows = [cutout(f"brow{s}", rounded_poly(
            [(-0.38, -0.06), (-0.38, 0.06), (0.38, 0.06), (0.38, -0.06)],
            0.05), None, (s * 0.0078, -0.0005, 0.0285), h, material=ink,
            wobble=0.004) for s in (-1, 1)]
        self.mouths = {
            "line": cutout("m_line", rounded_poly(
                [(-0.3, -0.05), (-0.3, 0.05), (0.3, 0.05), (0.3, -0.05)],
                0.04), None, (0, -0.0005, 0.0125), h, material=ink,
                wobble=0.003),
            "o": cutout("m_o", ellipse(0, 0, 0.26, 0.34, 20), None,
                        (0, -0.0005, 0.0122), h, material=ink,
                        wobble=0.004),
            "smile": cutout("m_smile",
                            ellipse(0, 0.12, 0.48, 0.3, 14,
                                    math.radians(200), math.radians(340))
                            + ellipse(0, 0.12, 0.44, 0.1, 14,
                                      math.radians(340), math.radians(200)),
                            None, (0, -0.0005, 0.0125), h, material=ink,
                            wobble=0.003),
        }

        # the reaching arm is its own layer, in front of the badge
        self.upper = cutout("arm_r_up", capsule_down(4.0, 1.7, 1.4),
                            "shirt_32", (0, 0, 0))
        self.fore = cutout("arm_r_fore", capsule_down(3.4, 1.15, 1.05),
                           "skin_31", (0, 0, 0))
        cutout("hand_r", rounded_poly([(-0.65, -3.1), (-0.7, -4.4),
                                       (-0.2, -4.75), (0.5, -4.5),
                                       (0.62, -3.1), (0.95, -3.6),
                                       (1.05, -3.2), (0.6, -2.8)], 0.15),
               "skin_31", (0, 0.0001, 0), self.fore)
        split_pin("pin_sh", self.upper, (0, -0.0006, 0))
        split_pin("pin_el", self.fore, (0, -0.0006, 0))
        self.shoulder_local = (0.033, -0.006)

    def shoulder(self):
        r = self.root.location
        return (r.x + self.shoulder_local[0], r.z + self.shoulder_local[1])

    def reach(self, target, y, bend=-1):
        """Two-bone IK in the X-Z plane: fingertip to target (x, z)."""
        sx, sz = self.shoulder()
        tx, tz = target
        a, b = self.UPPER, self.FORE
        d = min(max(math.hypot(tx - sx, tz - sz), abs(a - b) + 1e-4),
                a + b - 1e-4)
        base = math.atan2(tz - sz, tx - sx)
        th = base + bend * math.acos((a * a + d * d - b * b) / (2 * a * d))
        ex, ez = sx + a * math.cos(th), sz + a * math.sin(th)
        th2 = math.atan2(tz - ez, tx - ex)

        def rot(t):                       # a limb hangs along -Z at rest
            return math.atan2(-math.cos(t), -math.sin(t))

        self.upper.location = (sx, y, sz)
        self.upper.rotation_euler = (0, rot(th), 0)
        self.fore.location = (ex, y - 0.0003, ez)
        self.fore.rotation_euler = (0, rot(th2), 0)

    def face(self, mouth="line", brows="worried", gaze=(0, 0)):
        for k, m in self.mouths.items():
            m.hide_render = k != mouth
        tilt = {"worried": 16, "brave": -6, "up": 4}[brows]
        lift = {"worried": 0.0, "brave": 0.0012, "up": 0.0018}[brows]
        for s, b in zip((-1, 1), self.brows):
            b.rotation_euler.y = math.radians(s * tilt)
            b.location.z = 0.0285 + lift
        for s, e in zip((-1, 1), self.eyes):
            e.location.x = s * 0.0075 + gaze[0]
            e.location.z = 0.022 + gaze[1]


# --------------------------------------------------------------- props ----

def mic_badge(center, y):
    b = cutout("badge", ellipse(0, 0, 2.5, 2.5, 60), "badge", (0, 0, 0),
               wobble=0.0)
    # map the badge texture straight on (not the tiled default)
    uvl = b.data.uv_layers.active.data
    for loop, poly_loop in zip(uvl, b.data.loops):
        co = b.data.vertices[poly_loop.vertex_index].co
        loop.uv = (co.x * 100 / 5 + 0.5, co.z * 100 / 5 + 0.5)
    b.location = (center[0], y, center[1])
    cutout("badge_tab", [(-0.8, 0), (0.8, 0), (0.8, -2.6), (-0.8, -2.6)],
           "card_4", (center[0], y + 0.002, center[1] - 0.018))
    return b


class Tape:
    """Red tape over the mic. peel(p, hand) lifts it from the end at s=0,
    the free part running taut from the peel front to the hand."""

    L, W, N = 0.055, 0.012, 40

    def __init__(self, center, y, angle_deg=-40):
        self.c = np.array(center)
        a = math.radians(angle_deg)
        self.d = np.array([math.cos(a), math.sin(a)])
        self.n = np.array([-self.d[1], self.d[0]])
        self.y = y
        bm = bmesh.new()
        uv = bm.loops.layers.uv.new()
        rows = []
        for i in range(self.N + 1):
            rows.append([bm.verts.new((0, 0, 0)) for _ in range(2)])
        for i in range(self.N):
            f = bm.faces.new([rows[i][0], rows[i + 1][0], rows[i + 1][1],
                              rows[i][1]])
            for loop, (u, v) in zip(f.loops, [(i, 0), (i + 1, 0),
                                              (i + 1, 1), (i, 1)]):
                loop[uv].uv = (u / self.N, v)
        me = bpy.data.meshes.new("tape")
        bm.to_mesh(me)
        bm.free()
        self.ob = bpy.data.objects.new("tape", me)
        bpy.context.collection.objects.link(self.ob)
        self.ob.data.materials.append(stage.paper_material(
            "tape", translucency=0.15, roughness=0.45, bump=0.2))
        s = self.ob.modifiers.new("paper", "SOLIDIFY")
        s.thickness = 0.0002
        self.p0 = self.c - self.d * self.L / 2

    def grab_point(self):
        return tuple(self.p0)

    def peel(self, p, hand=None, lift=0.004):
        s = np.linspace(0, 1, self.N + 1)
        front = self.p0 + self.d * p * self.L
        co = []
        for si in s:
            if si >= p or hand is None:
                c = self.p0 + self.d * si * self.L
                y = self.y
            else:
                k = (p - si) / max(p, 1e-6)       # 0 at front, 1 at hand
                c = front + (np.array(hand) - front) * k
                y = self.y - lift * math.sin(math.pi * k * 0.9) - 0.002 * k
            for side in (-1, 1):
                q = c + self.n * side * self.W / 2
                co += [q[0], y, q[1]]
        self.ob.data.vertices.foreach_set("co", co)
        self.ob.data.update()


def lantern(loc, glow_rgb):
    """The tutor: a paper lantern with the Glow inside. No face."""
    x, y, z = loc
    bpy.ops.mesh.primitive_cylinder_add(radius=0.024, depth=0.064,
                                        vertices=48, end_fill_type="NOTHING",
                                        location=(x, y, z + 0.036))
    body = bpy.context.object
    body.name = "lantern"
    bpy.ops.object.shade_smooth()
    body.data.materials.append(stage.paper_material(
        "lantern_35", translucency=0.75, bump=0.2))
    s = body.modifiers.new("paper", "SOLIDIFY")
    s.thickness = 0.0003
    for k, zz in enumerate((z + 0.004, z + 0.068)):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.0252, depth=0.006,
                                            vertices=48,
                                            location=(x, y, zz))
        rim = bpy.context.object
        rim.data.materials.append(stage.paper_material(
            "hair_33", translucency=0.0))
        rim.parent = None
    light = bpy.data.lights.new("tutor", "POINT")
    light.color = glow_rgb
    light.shadow_soft_size = 0.01
    lo = bpy.data.objects.new("tutor", light)
    bpy.context.collection.objects.link(lo)
    lo.location = (x, y, z + 0.034)
    return body, lo
