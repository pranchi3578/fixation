#!/usr/bin/env python3
"""
Line ornaments for the invitation.

The wool is generated rather than hand-drawn: guessing bezier control points
for eleven scallops by eye is how you get a lumpy sheep. Here the fleece is a
ring of outward arcs around an ellipse, which is even by construction.

Everything else — head, legs, halo, staff — is placed by hand against that.

Usage:  python3 tools/ornaments.py     Writes: /tmp/orn/*.svg
"""

import math
import os


def fleece(cx, cy, rx, ry, scallops=11, bulge=0.62, start=-100):
    """A closed path of outward arcs around an ellipse."""
    pts = []
    for i in range(scallops):
        a = math.radians(start + 360 * i / scallops)
        pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))

    d = f"M {pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(1, scallops + 1):
        x, y = pts[i % scallops]
        px, py = pts[i - 1]
        chord = math.hypot(x - px, y - py)
        r = chord * bulge
        d += f" A {r:.1f},{r:.1f} 0 0 1 {x:.1f},{y:.1f}"
    return d + " Z"


def lamb():
    """
    Agnus Dei, reduced to line. No staff or banner: at the size this sits on
    the page they collapse into scribble, and the brief was subtle.

    The head sits clear of the fleece rather than overlapping it, and the
    halo is concentric with the head — the two earlier attempts read as a
    cloud with a second circle stuck to it because neither was true.
    """
    body = fleece(95, 57, 29, 17, scallops=10)
    return f"""<svg viewBox="0 0 150 104" fill="none" aria-hidden="true">
  <g stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    <!-- halo, concentric with the head -->
    <circle cx="48" cy="57" r="16" stroke-width="1" opacity=".6"/>
    <!-- fleece -->
    <path d="{body}"/>
    <!-- head in profile, clear of the fleece -->
    <path d="M62 50 C 56 44, 44 45, 39 52
             C 34 59, 36 66, 43 67
             C 50 68, 58 63, 62 56 Z"/>
    <!-- ear, tucked to the skull -->
    <path d="M56 47 q-3 -7 -10 -7 q1 7 9 9" stroke-width="1.2"/>
    <!-- eye, kept small: at page size a larger dot becomes a blot -->
    <circle cx="47" cy="55" r="1.15" fill="currentColor" stroke="none"/>
    <!-- legs, short -->
    <path d="M78 72 L76 88"/>
    <path d="M89 73 L88 88"/>
    <path d="M103 73 L104 88"/>
    <path d="M114 71 L117 87"/>
  </g>
</svg>"""


def sprig():
    """A small botanical mark: a stem with paired leaves."""
    return '''<svg viewBox="0 0 120 40" fill="none" aria-hidden="true">
  <g stroke="currentColor" stroke-width="1.3" stroke-linecap="round" fill="none">
    <path d="M10 20 H110"/>
    <path d="M60 20 q-9 -12 -20 -12 q3 12 20 12"/>
    <path d="M60 20 q9 -12 20 -12 q-3 12 -20 12"/>
    <path d="M60 20 q-7 10 -16 11 q1 -10 16 -11"/>
    <path d="M60 20 q7 10 16 11 q-1 -10 -16 -11"/>
  </g>
</svg>'''


def rule():
    """A hairline with a small diamond, for separating movements."""
    return '''<svg viewBox="0 0 200 12" fill="none" aria-hidden="true">
  <g stroke="currentColor" stroke-width="1">
    <path d="M0 6 H88" opacity=".55"/>
    <path d="M112 6 H200" opacity=".55"/>
    <path d="M100 1.5 L104.5 6 L100 10.5 L95.5 6 Z" fill="currentColor" stroke="none"/>
  </g>
</svg>'''


if __name__ == "__main__":
    os.makedirs("/tmp/orn", exist_ok=True)
    for name, svg in (("lamb", lamb()), ("sprig", sprig()), ("rule", rule())):
        open(f"/tmp/orn/{name}.svg", "w").write(svg)
        print(f"  /tmp/orn/{name}.svg")
