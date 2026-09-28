"""Round 4: the first, softer owlet (redrawn), and a robot owl, square and
pixelled, with WALL-E-like traits. Same PixelBoard cells and brightness
levels as owl.py.

    python3 docs/bb-learn-mascot/owl_round4.py   ->  owl_round4.svg

Rough sketches, for choosing a direction.
"""
from pathlib import Path

from owl import board, text_lit

LEVEL = {"1": 0.26, "2": 0.5, "3": 0.78, "4": 1.0}  # 'o' and '.' are unlit
LIGHT = {"1": 0.8, "2": 0.55, "3": 0.3, "4": 0.07, "o": 1.0}


def lit(grid, dc=0, dr=0, light=False):
    t = LIGHT if light else LEVEL
    return {(c + dc, r + dr): t[ch] for r, row in enumerate(grid) for c, ch in enumerate(row) if ch in t}


def paint(grid, spots):
    """spots: {(row, col): patch rows}. Returns a new grid."""
    g = [list(r) for r in grid]
    for (r0, c0), patch in spots.items():
        for dr, row in enumerate(patch):
            for dc, ch in enumerate(row):
                if ch != "_":
                    g[r0 + dr][c0 + dc] = ch
    return ["".join(r) for r in g]


# ── The owlet, as first drawn (round 3's first render) ──────────────────────
FIRST = [
    "........3....",
    "....22222....",
    "..222222222..",
    ".22333233322.",
    ".23444244432.",
    "2234o424o4322",
    "2234o424o4322",
    "2233331333322",
    ".22223332222.",
    ".12422222421.",
    ".12223332221.",
    ".14223332241.",
    "..122333221..",
    "...2224222...",
    "....33.33....",
]

# ── Refined: same body and softness. The eyes are wider (4x3) with rounded
# corners, and the pupils sit low and toward the middle: the "looking up at
# you" look of a very young animal.
OWLET = [
    "........3....",
    "....22222....",
    "..222222222..",
    ".23333233332.",
    "2334432344332",
    "2344o424o4432",
    "2334o323o4332",
    "2233331333322",
    ".22223332222.",
    ".12422222421.",
    ".12223332221.",
    ".14223332241.",
    "..122333221..",
    "...2224222...",
    "....33.33....",
]
OWLET_EYES = ((4, 2), (4, 7))  # 3 rows x 4 cols each


def owlet(left, right=None):
    return paint(OWLET, {pos: pat for pos, pat in zip(OWLET_EYES, (left, right or left))})


OWLET_STATES = [
    ("Resting", OWLET),
    ("Listening", owlet(["34o3", "44o4", "3443"], ["3o43", "4o44", "3443"])),
    ("Your work", owlet(["3443", "4o44", "3o43"], ["3443", "o444", "o443"])),
    ("Happy", owlet(["3443", "4334", "3333"])),
    ("Blink", owlet(["3333", "4444", "3333"])),
    ("Sleepy", owlet(["3333", "3333", "4o44"], ["3333", "3333", "44o4"])),
]


# ── Robot owl A, "Hoo-bot": binocular eyes on a neck, a boxy body, treads.
# Owl traits become machine parts: ear tufts are antennae, the chest feathers
# are a chevron grille, the wings are side flaps, the feet are treads.
def hoobot(eye_l=None, eye_r=None, antenna="2", tilt=0):
    body_panel = ["111111111", "131111131", "113111311", "111313111", "111131111"]
    rows = [
        "..%s.........%s.." % (antenna, antenna),
        "..%s%s.......%s%s.." % (antenna, antenna, antenna, antenna),
        ".22222...22222.",
        ".34oo3...34oo3.",
        ".3ooo3.3.3ooo3.",
        ".3ooo3.3.3ooo3.",
        "..333..2..333..",
        ".......2.......",
        "..22222222222..",
    ]
    rows += ["12" + "2" + p + "2" + "21" if i in (1, 2) else ".1" + "2" + p + "2" + "1." for i, p in enumerate(body_panel)]
    rows += ["..22222222222..", "..33333.33333..", "..23232.23232.."]
    g = rows
    if eye_l or eye_r:
        g = paint(g, {(3, 2): eye_l or ["_"], (3, 10): eye_r or ["_"]})
    if tilt:  # the WALL-E head tilt: one eye barrel rides a row higher
        g = [list(r) for r in g]
        for r in range(0, 7):  # lift the right barrel and antenna by one row
            for c in range(9, 15):
                g[r][c] = g[r + 1][c] if r + 1 < 7 else "."
        g = ["".join(r) for r in g]
    return g


HOOBOT = hoobot()
assert all(len(r) == 15 for r in HOOBOT), [len(r) for r in HOOBOT]

HOOBOT_STATES = [
    ("Resting", HOOBOT),
    ("Listening", hoobot(antenna="4")),
    ("Curious", hoobot(tilt=1)),
    ("Happy", hoobot(["333", "3o3", "ooo"], ["333", "3o3", "ooo"])),
    ("Blink", hoobot(["333", "444", "333"], ["333", "444", "333"])),
    ("Your work", hoobot(["4oo", "ooo", "ooo"], ["4oo", "ooo", "ooo"]) if False else
     paint(HOOBOT, {(3, 2): ["_o4", "ooo", "ooo"], (3, 10): ["_o4", "ooo", "ooo"]})),
]


# ── Robot owl B, "Cube": the whole owl is one box (WALL-E's compacted cube).
def cube(eyes=None, meter=3):
    W = 13
    g = [["."] * W for _ in range(14)]
    g[0][2] = g[0][10] = "2"                      # tufts as bolts
    for r in range(1, 12):
        for c in range(W):
            edge = r in (1, 11) or c in (0, W - 1)
            g[r][c] = "2" if edge else "1"
    for c0 in (2, 7):                              # binocular lenses, 4x4
        for dr, row in enumerate(eyes or ["3333", "34o3", "3oo3", "3333"]):
            for dc, ch in enumerate(row):
                g[3 + dr][c0 + dc] = ch
    g[7][6] = "3"                                  # beak sensor
    for c in range(1, W - 1):                      # a seam, like a lid
        g[8][c] = "2"
    for i in range(5):                             # the learning meter
        g[9][4 + i] = "4" if i < meter else "2"
    g[12] = list("..3333.3333..")
    g[13] = list("..2323.2323..")
    return ["".join(r) for r in g]


CUBE = cube()

CUBE_STATES = [
    ("Resting", CUBE),
    ("Happy", cube(["3333", "3oo3", "o33o", "3333"], meter=5)),
    ("Blink", cube(["3333", "3333", "4444", "3333"])),
]


def main():
    W, H = 1400, 1680
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        '<style>text{font-family:"Geist Sans",Inter,system-ui,sans-serif}'
        ".h{font-size:28px;font-weight:800;letter-spacing:-0.02em}"
        ".a{font-size:17px;font-weight:700}.t{font-size:15px;font-weight:600}"
        ".s{font-size:13px;fill:#696969}</style>",
        '<text class="h" x="40" y="58">BB Learn: the cute owlet, and a robot owl</text>',
        '<text class="s" x="40" y="84">on the PixelBoard · rough sketches · same cells and brightness levels as the site\'s 5×7 BRAINBACK</text>',
    ]

    def big(x, y, grid, cols, rows, title, note, step=20, cell=17):
        p.append(board(x, y, cols, rows, lit(grid, 1, 1), step=step, cell=cell))
        p.append(f'<text class="t" x="{x}" y="{y + rows * step + 34}">{title}</text>')
        p.append(f'<text class="s" x="{x}" y="{y + rows * step + 56}">{note}</text>')

    def strip(x, y, states, cols, rows):
        for i, (name, g) in enumerate(states):
            xx = x + i * 150
            p.append(board(xx, y, cols, rows, lit(g, 1, 1), step=7.5, cell=6.3, sparkles=False))
            p.append(f'<text class="s" x="{xx}" y="{y + rows * 7.5 + 24}">{name}</text>')

    # 1. the owlet
    y = 120
    p.append(f'<text class="a" x="40" y="{y}">1 · The owlet: round 3\'s first drawing, and a refined version</text>')
    big(40, y + 24, FIRST, 15, 17, "As first drawn", "soft, low contrast, small tall pupils")
    big(420, y + 24, OWLET, 15, 17, "Refined", "wider rounded eyes, pupils low and inward")
    lk = lit(OWLET, 3, 1)
    lk.update(text_lit("BB LEARN", 20, 5))
    p.append(board(800, y + 24, 70, 17, lk, step=7.8, cell=6.5))
    p.append(f'<text class="t" x="800" y="{y + 24 + 17 * 7.8 + 34}">On the board, as the BB LEARN lockup</text>')
    y2 = y + 24 + 17 * 11 + 70
    p.append(board(800, y2, 15, 16, lit(OWLET, 1, 0, light=True), step=11, cell=9, dark=False, sparkles=False))
    p.append(f'<text class="t" x="980" y="{y2 + 20}">On white, and at 32 / 16px</text>')
    for i, s in enumerate((32, 16)):
        st = s / 15
        p.append(board(980 + i * 60, y2 + 40, 15, 16, lit(OWLET, 1, 0), step=st, cell=st, sparkles=False))
        p.append(board(1100 + i * 60, y2 + 40, 15, 16, lit(OWLET, 1, 0, light=True), step=st, cell=st, dark=False, sparkles=False))
    y = y + 24 + 17 * 20 + 90
    strip(40, y, OWLET_STATES, 15, 17)

    # 2. the robot owls
    y += 17 * 7.5 + 80
    p.append(f'<text class="a" x="40" y="{y}">2 · Robot owl: square, pixelled, WALL-E-like</text>')
    p.append(f'<text class="s" x="40" y="{y + 22}">ear tufts become antennae, chest feathers a chevron grille, wings side flaps, feet treads</text>')
    y += 44
    big(40, y, HOOBOT, 17, 19, "A · Hoo-bot", "binocular eyes on a neck, a boxy body, treads")
    big(460, y, CUBE, 15, 16, "B · Cube", "the whole owl is one box; the meter fills as you learn")
    p.append(f'<text class="t" x="860" y="{y + 16}">A at 32 / 16px</text>')
    for i, s in enumerate((32, 16)):
        st = s / 17
        p.append(board(860 + i * 60, y + 36, 15, 17, lit(HOOBOT), step=st, cell=st, sparkles=False))
    p.append(f'<text class="t" x="1060" y="{y + 16}">B at 32 / 16px</text>')
    for i, s in enumerate((32, 16)):
        st = s / 14
        p.append(board(1060 + i * 60, y + 36, 13, 14, lit(CUBE), step=st, cell=st, sparkles=False))
    p.append(board(860, y + 120, 13, 14, lit(CUBE, light=True), step=11, cell=9, dark=False, sparkles=False))
    p.append(board(1060, y + 120, 15, 17, lit(HOOBOT, light=True), step=9, cell=7.5, dark=False, sparkles=False))
    p.append(f'<text class="s" x="860" y="{y + 300}">B on white</text>')
    p.append(f'<text class="s" x="1060" y="{y + 300}">A on white</text>')
    y += 19 * 20 + 90
    strip(40, y, HOOBOT_STATES, 17, 19)
    strip(40 + 6 * 150 + 20, y, CUBE_STATES[1:], 15, 16)
    p.append("</svg>")
    Path(__file__).with_name("owl_round4.svg").write_text("\n".join(p) + "\n")


if __name__ == "__main__":
    main()
