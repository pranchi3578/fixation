"""
The Doubtling: a paper dart that sulks in the shape of a question mark.

It is one mesh, folded from the dart crease pattern: a keel and two wings
meeting along a spine. A pose is five numbers; `pose()` computes every
vertex from them. Nothing is keyframed on the mesh -- each rendered frame
is its own replacement pose, the way a stop-motion puppet is moved and shot.

Local frame: the spine runs in the Y-Z plane from the tail (u=0) to the
nose (u=1); X is across the wings. Seen from -X, the spine's silhouette is
the character: a "?" when it doesn't understand, a "!" when it does.
"""

import math

import bmesh
import bpy
import numpy as np

import paper

L = paper.DOUBT_L / 100          # metres
W = paper.DOUBT_W / 100
K = paper.DOUBT_K / 100
NU, NA, NS = 48, 6, 5            # grid resolution: along, across wing, keel


def _uv(cm):
    return (cm[0] / paper.DOUBT_SHEET[0], 1 - cm[1] / paper.DOUBT_SHEET[1])


def build(name="doubtling"):
    """Make the mesh once, flat. Returns the object; call pose() per frame.

    Vertices are keyed by their flat position, so the spine is shared by
    keel and both wings (it is the fold) and the nose closes to a point."""
    bm = bmesh.new()
    uvl = bm.loops.layers.uv.new()
    params, index = [], {}
    flat = Pose(pitch=0, hook=0, droop=0, tail=0)

    def vert(kind, u, a, side):
        co = _positions(np.array([u]), np.array([a]), np.array([side]),
                        np.array([kind == "keel"]), flat)[0]
        key = tuple(np.round(co, 7))
        if key not in index:
            index[key] = bm.verts.new(co)
            params.append((kind, u, a, side))
        return index[key]

    def face(vs, uvs):
        uniq, seen = [], set()
        for v, uv in zip(vs, uvs):
            if v not in seen:
                seen.add(v)
                uniq.append((v, uv))
        if len(uniq) < 3:
            return
        f = bm.faces.new([v for v, _ in uniq])
        for loop, (_, uv) in zip(f.loops, uniq):
            loop[uvl].uv = uv

    for side in (-1, 1):
        for i in range(NU):
            for j in range(NA):
                ks = [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]
                if side > 0:
                    ks.reverse()
                face([vert("wing", a / NU, b / NA, side) for a, b in ks],
                     [_uv(paper.doubt_wing_cm(a / NU, b / NA, side))
                      for a, b in ks])
    for i in range(NU):
        for j in range(NS):
            ks = [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]
            face([vert("keel", a / NU, b / NS, 0) for a, b in ks],
                 [_uv(paper.doubt_keel_cm(a / NU, b / NS)) for a, b in ks])

    me = bpy.data.meshes.new(name)
    bm.verts.index_update()
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    for p in me.polygons:
        p.use_smooth = True
    sol = ob.modifiers.new("paper", "SOLIDIFY")
    sol.thickness = 0.00012
    sol.offset = 0
    kind = np.array([q[0] == "keel" for q in params])
    _PARAMS[ob.name] = (np.array([q[1] for q in params]),
                        np.array([q[2] for q in params]),
                        np.array([q[3] for q in params], float), kind)
    return ob


_PARAMS = {}


class Pose:
    """pitch: angle of the tail section from horizontal (deg; 90 = upright)
    hook:  how far the front of the spine curls over (deg)
    droop: wings hanging down from the spine (deg; 0 flat, -8 flight)
    tail:  a small upward flick at the tail (deg)
    hook_from: where along the spine the curl starts (0..1)"""

    def __init__(self, pitch=90, hook=150, droop=60, tail=0, hook_from=0.45):
        self.pitch, self.hook, self.droop = pitch, hook, droop
        self.tail, self.hook_from = tail, hook_from

    @staticmethod
    def lerp(a, b, t):
        return Pose(*(x + (y - x) * t for x, y in
                      zip(a.astuple(), b.astuple())))

    def astuple(self):
        return (self.pitch, self.hook, self.droop, self.tail, self.hook_from)


def _smooth(e0, e1, x):
    t = np.clip((x - e0) / max(1e-6, e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def _positions(u, a, side, keel, p):
    # spine angle along its length
    uu = np.linspace(0, 1, 400)
    th = (math.radians(p.pitch)
          - math.radians(p.hook) * _smooth(p.hook_from, 1.0, uu)
          + math.radians(p.tail) * (1 - _smooth(0.0, 0.2, uu)))
    dy = np.cos(th) * L / (len(uu) - 1)
    dz = np.sin(th) * L / (len(uu) - 1)
    cy = np.concatenate([[0], np.cumsum(dy[:-1])])
    cz = np.concatenate([[0], np.cumsum(dz[:-1])])
    t = np.interp(u, uu, th)
    y0, z0 = np.interp(u, uu, cy), np.interp(u, uu, cz)
    # cross-section in (x, n): wings rotate down about the spine
    d = math.radians(p.droop)
    r = a * W * (1 - u)
    x = np.where(keel, 0.0, side * r * math.cos(d))
    n = np.where(keel, -a * K * (1 - u), -r * math.sin(d))
    # n is along the spine's normal (-sin t, cos t) in (y, z)
    return np.stack([x, y0 - n * np.sin(t), z0 + n * np.cos(t)], 1)


def pose(ob, p, jitter=0.0, rng=None):
    """Set every vertex for pose p. jitter adds the hand-moved wobble
    (degrees) that makes held frames 'boil'."""
    if jitter and rng is not None:
        p = Pose(*(v + rng.normal(0, jitter) if i < 4 else v
                   for i, v in enumerate(p.astuple())))
    u, a, side, keel = _PARAMS[ob.name]
    co = _positions(u, a, side, keel, p)
    ob.data.vertices.foreach_set("co", co.ravel())
    ob.data.update()
