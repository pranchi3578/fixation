"""The BB Learn owl, sketched on BrainBack's PixelBoard: the LED board behind
the website's 5x7 BRAINBACK wordmark. Every cell of the board is always
faintly lit, and the owl is lit cells at four brightness levels.

    python3 docs/bb-learn-mascot/owl.py   ->  owl.svg

Rough sketches, for planning.
"""
import math
from pathlib import Path

CELL, GAP = 10, 2
STEP = CELL + GAP

# brightness per character on the dark board. 'o' is a pupil: unlit on the
# board, full ink on white. '.' is an empty board cell.
LEVEL = {"1": 0.26, "2": 0.5, "3": 0.78, "4": 1.0, "o": None}
LIGHT = {"1": 0.8, "2": 0.55, "3": 0.3, "4": 0.07, "o": 1.0}
BASE = 0.07  # the always-on grid, as on the site (a touch brighter so it prints)

# Spotted owlet (Athene brama): India's commonest owl. Round, no ear tufts,
# white brows, a white collar, a pale beak, white spots.
# 1 = dark eye rim and wing edge, 2 = plumage, 3 = collar and beak,
# 4 = eyes, brows and spots. The lone cell on top is the cowlick.
REST = [
    "..........3....",
    ".....22222.....",
    "...222222222...",
    ".2444222224442.",
    "214444121444412",
    "214oo41214oo412",
    "214oo41214oo412",
    "214444131444412",
    "221111232111122",
    ".2223333333222.",
    ".1242233322421.",
    ".1422233322241.",
    "..12423332421..",
    "...122333221...",
    "....2224222....",
    ".....33.33.....",
]
assert all(len(r) == 15 for r in REST)
EYES = ((4, 2), (4, 9))  # top-left of each 4x4 eye


def pupils(dr, dc, dr2=None, dc2=None):
    """An open eye with its 2x2 pupil at (dr, dc) inside the 4x4 eye."""
    def eye(r0, c0):
        return ["".join("o" if r0 <= r < r0 + 2 and c0 <= c < c0 + 2 else "4" for c in range(4)) for r in range(4)]
    return eye(dr, dc), eye(dr if dr2 is None else dr2, dc if dc2 is None else dc2)


def with_eyes(left, right=None):
    g = [list(r) for r in REST]
    for (r0, c0), pat in zip(EYES, (left, right or left)):
        for dr in range(4):
            for dc in range(4):
                g[r0 + dr][c0 + dc] = pat[dr][dc]
    return ["".join(r) for r in g]


STATES = [
    ("Resting", "big eyes, pupils centred and soft", REST),
    ("Listening", "pupils up, toward the child who is speaking", with_eyes(*pupils(0, 1))),
    ("Looking at your work", "joint attention: eyes on the lesson, not on you", with_eyes(*pupils(2, 0))),
    ("Hmm", "a wrong answer gets curiosity, never disappointment", with_eyes(pupils(1, 1)[0], ["2222", "4444", "4oo4", "4444"])),
    ("Happy", "crescent eyes, for effort, not for being clever", with_eyes(["2222", "2442", "4224", "2222"])),
    ("Oops", "its own small mistake: likeable, not perfect", with_eyes(*pupils(1, 2, 1, 0))),
    ("Blink", "at random 2-6s gaps; a regular blink looks robotic", with_eyes(["2222", "2222", "4444", "2222"])),
    ("Sleepy", "half-lidded: it's late, go to bed", with_eyes(["2222", "2222", "4oo4", "4444"])),
]

# the 5x7 face from the site's PixelBoard.tsx, plus L and E
FONT = {
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    " ": ["00000"] * 7,
}


def sparkle(i):
    """The site's deterministic scatter: stable, never clustered."""
    r = abs(math.sin(i * 127.1 + 3.7) * 43758.5) % 1
    return 0.14 + 0.18 * (r * 10 % 1) if r < 0.12 else None


def board(x0, y0, cols, rows, lit, step=STEP, cell=CELL, dark=True, sparkles=True):
    """lit: {(col,row): brightness}. Draws the whole board, grid included."""
    ink = "#fff" if dark else "#000"
    out = []
    if dark:
        out.append(f'<rect x="{x0 - 8}" y="{y0 - 8}" width="{cols * step + 14}" height="{rows * step + 14}" rx="10" fill="#050505"/>')
    for r in range(rows):
        for c in range(cols):
            v = lit.get((c, r))
            if v is None:
                s = sparkle(r * cols + c + int(x0)) if sparkles else None
                v = s if s else BASE
            if not dark and v == BASE:
                v = 0.035
            out.append(f'<rect x="{x0 + c * step:.1f}" y="{y0 + r * step:.1f}" width="{cell:.1f}" height="{cell:.1f}" '
                       f'rx="{max(cell / 10, 0.4):.1f}" fill="{ink}" fill-opacity="{v:.2f}"/>')
    return "\n".join(out)


def sprite(grid, dc=0, dr=0, light=False):
    table = LIGHT if light else LEVEL
    lit = {}
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch in table and table[ch] is not None:
                lit[(c + dc, r + dr)] = table[ch]
    return lit


def text_lit(word, dc, dr, level=0.9):
    lit = {}
    for i, ch in enumerate(word):
        for r, row in enumerate(FONT[ch]):
            for c, bit in enumerate(row):
                if bit == "1":
                    lit[(dc + i * 6 + c, dr + r)] = level
    return lit


def main():
    W, H = 1400, 1600
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        '<style>text{font-family:"Geist Sans",Inter,system-ui,sans-serif}'
        ".h{font-size:28px;font-weight:800;letter-spacing:-0.02em}"
        ".a{font-size:17px;font-weight:700}.t{font-size:15px;font-weight:600}"
        ".s{font-size:13px;fill:#696969}"
        '.m{font-family:"Geist Mono",ui-monospace,monospace;font-size:11px;fill:#696969}</style>',
        '<text class="h" x="40" y="58">BB Learn: the owl, on the PixelBoard</text>',
        '<text class="s" x="40" y="84">a spotted owlet (Athene brama), drawn in the same cells as the site\'s 5×7 BRAINBACK · rough sketch for planning</text>',
    ]

    # 1. lockup: the owl standing on the board beside BB LEARN
    y = 120
    p.append(f'<text class="a" x="40" y="{y}">The lockup: the owl lives on the board</text>')
    cols, rows = 70, 18
    lit = sprite(REST, 3, 1)
    lit.update(text_lit("BB LEARN", 22, 6))
    p.append(board(40, y + 24, cols, rows, lit))

    # 2. character at large size, with anatomy notes
    y = 400
    p.append(f'<text class="a" x="40" y="{y}">The character</text>')
    big, bc = 22, 19
    p.append(board(40, y + 24, 17, 18, sprite(REST, 1, 1), step=big, cell=bc))
    notes = [
        ("cowlick", "one feather out of place: the imperfection that makes it feel alive"),
        ("eyes", "half the face, big pupils, a dark rim: baby schema, reads as young and safe"),
        ("brows", "the owlet's real white brows, set high and open: friendly, not stern"),
        ("beak", "two pale cells on the midline, the logo's split between the two halves"),
        ("spots", "the white spots of India's commonest owl, lit like the board's sparkles"),
        ("feet", "two cells, planted: it stays put, it's a companion, not a performer"),
    ]
    for i, (k, v) in enumerate(notes):
        ty = y + 60 + i * 52
        p.append(f'<text class="t" x="470" y="{ty}">{k}</text>')
        p.append(f'<text class="s" x="470" y="{ty + 20}">{v}</text>')

    # light-background version and the eyes-only mark
    p.append(f'<text class="t" x="1000" y="{y + 60}">On white</text>')
    p.append(board(1000, y + 80, 15, 16, sprite(REST, light=True), step=11, cell=9, dark=False, sparkles=False))
    p.append(f'<text class="t" x="1180" y="{y + 60}">Eyes only</text>')
    p.append('<text class="s" x="1180" y="%d">for teens, and the UI corner</text>' % (y + 80))
    eyes = {}
    for (c, r), v in sprite(REST).items():
        if 3 <= r <= 7 and (2 <= c <= 5 or 9 <= c <= 12):
            eyes[(c - 1, r - 2)] = v
    p.append(board(1180, y + 100, 13, 7, eyes, sparkles=False))
    p.append(f'<text class="t" x="1000" y="{y + 330}">At 32px and 16px</text>')
    for i, size in enumerate((32, 16)):
        st = size / 15
        st = size / 16
        p.append(board(1000 + i * 70, y + 350, 15, 16, sprite(REST), step=st, cell=st, sparkles=False))
        p.append(board(1150 + i * 70, y + 350, 15, 16, sprite(REST, light=True), step=st, cell=st, dark=False, sparkles=False))

    # 3. states
    y = 890
    p.append(f'<text class="a" x="40" y="{y}">States: one grid edit each</text>')
    for i, (name, note, grid) in enumerate(STATES):
        x = 40 + (i % 4) * 335
        yy = y + 30 + (i // 4) * 320
        p.append(board(x, yy, 17, 18, sprite(grid, 1, 1), step=11, cell=9))
        p.append(f'<text class="t" x="{x}" y="{yy + 230}">{name}</text>')
        words, line, ly = note.split(), "", yy + 252
        for w in words:
            if len(line) + len(w) > 34:
                p.append(f'<text class="s" x="{x}" y="{ly}">{line}</text>')
                line, ly = "", ly + 18
            line += w + " "
        p.append(f'<text class="s" x="{x}" y="{ly}">{line}</text>')
    p.append("</svg>")
    Path(__file__).with_name("owl.svg").write_text("\n".join(p) + "\n")


if __name__ == "__main__":
    main()
