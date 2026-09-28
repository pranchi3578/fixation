"""The Cube in blue: one hue (the logo's #195589, ~208 deg), at four lightness
levels, so it keeps the PixelBoard's rule that everything is light and shade.

    python3 docs/bb-learn-mascot/cube_blue.py   ->  cube_blue_sheet.svg

The prototype (cube.html) gets the same palette from cube.py.
"""
import math
from pathlib import Path

from cube import STATES, SMALL, lit
from owl import text_lit

HERE = Path(__file__).parent

# on the dark board: 1 box, 2 edge and bolts, 3 lens ring and trim, 4 lit parts and glint
DARK = {"1": "#195589", "2": "#2f7fc4", "3": "#6cb8f2", "4": "#e3f3ff"}
# on white: the box stays logo navy, the lens ring goes pale so the pupils read
LIGHT = {"1": "#195589", "2": "#0f3d66", "3": "#9fd0f7", "4": "#eaf6ff", "o": "#0b2238"}
MONO = {"1": "rgba(255,255,255,.26)", "2": "rgba(255,255,255,.5)", "3": "rgba(255,255,255,.78)", "4": "#fff"}
BASE = "rgba(255,255,255,.07)"


def sparkle(i):
    r = abs(math.sin(i * 127.1 + 3.7) * 43758.5) % 1
    return f"rgba(255,255,255,{0.14 + 0.18 * (r * 10 % 1):.2f})" if r < 0.12 else None


def board(x0, y0, cols, rows, grid, pal, dc=1, dr=1, step=12, cell=10, dark=True, sparkles=True, extra=None):
    cells = {(c + dc, r + dr): ch for r, row in enumerate(grid) for c, ch in enumerate(row) if ch in pal}
    out = []
    if dark:
        out.append(f'<rect x="{x0 - 8}" y="{y0 - 8}" width="{cols * step + 14}" height="{rows * step + 14}" rx="10" fill="#050505"/>')
    for r in range(rows):
        for c in range(cols):
            key = (c, r)
            if extra and key in extra:
                fill = extra[key]
            elif key in cells:
                fill = pal[cells[key]]
            else:
                fill = (sparkle(r * cols + c + int(x0)) if sparkles else None) or (BASE if dark else "rgba(0,0,0,.035)")
            out.append(f'<rect x="{x0 + c * step:.1f}" y="{y0 + r * step:.1f}" width="{cell:.1f}" height="{cell:.1f}" '
                       f'rx="{max(cell / 10, .4):.1f}" fill="{fill}"/>')
    return "\n".join(out)


def main():
    Wd, Ht = 1400, 1700
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wd}" height="{Ht}" viewBox="0 0 {Wd} {Ht}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        '<style>text{font-family:"Geist Sans",Inter,system-ui,sans-serif}'
        ".h{font-size:28px;font-weight:800;letter-spacing:-0.02em}"
        ".a{font-size:17px;font-weight:700}.t{font-size:15px;font-weight:600}"
        ".s{font-size:13px;fill:#696969}"
        '.m{font-family:"Geist Mono",ui-monospace,monospace;font-size:12px;fill:#333}</style>',
        '<text class="h" x="40" y="58">BB Learn: the Cube, in blue</text>',
        '<text class="s" x="40" y="84">one hue, the logo\'s blue (#195589, 208°), at four lightness levels · white catchlights · rough sketch</text>',
    ]

    def note(x, y, title, text, width=40):
        p.append(f'<text class="t" x="{x}" y="{y}">{title}</text>')
        line, ly = "", y + 20
        for w in text.split():
            if len(line) + len(w) > width:
                p.append(f'<text class="s" x="{x}" y="{ly}">{line}</text>')
                line, ly = "", ly + 17
            line += w + " "
        p.append(f'<text class="s" x="{x}" y="{ly}">{line}</text>')

    rest = STATES["rest"][2]
    # 1. mono vs blue, side by side
    y = 120
    p.append(f'<text class="a" x="40" y="{y}">1 · Mono and blue</text>')
    p.append(board(40, y + 24, 17, 17, rest, MONO, step=19, cell=16))
    note(40, y + 24 + 17 * 19 + 34, "Mono", "the brand's default: light and shade only")
    p.append(board(420, y + 24, 17, 17, rest, DARK, step=19, cell=16))
    note(420, y + 24 + 17 * 19 + 34, "Blue (recommended for students)", "calm, trusted, the world's most-liked colour; the logo's own hue")

    # the ramp
    x = 820
    p.append(f'<text class="t" x="{x}" y="{y + 40}">The ramp: one hue, four lightness steps</text>')
    ramp = [("1", "box", "the logo navy, exactly"), ("2", "edge, bolts", "outline and ears"),
            ("3", "lens ring, trim", "frames the eyes"), ("4", "lit, glint", "near-white: catchlights stay white")]
    for i, (k, name, why) in enumerate(ramp):
        yy = y + 64 + i * 58
        p.append(f'<rect x="{x}" y="{yy}" width="44" height="44" rx="4" fill="{DARK[k]}"/>')
        p.append(f'<text class="t" x="{x + 60}" y="{yy + 18}">{name}</text>')
        p.append(f'<text class="m" x="{x + 60}" y="{yy + 37}">{DARK[k]}  ·  {why}</text>')
    p.append(f'<text class="s" x="{x}" y="{y + 316}">pupils stay unlit (the board shows through), so the eyes</text>')
    p.append(f'<text class="s" x="{x}" y="{y + 333}">read as deep and dark: big dark pupils read as young</text>')

    # 2. states
    y += 24 + 17 * 19 + 110
    p.append(f'<text class="a" x="40" y="{y}">2 · States</text>')
    for i, key in enumerate(STATES):
        name, _, g = STATES[key]
        x = 40 + (i % 6) * 222
        yy = y + 24 + (i // 6) * 210
        p.append(board(x, yy, 17, 17, g, DARK, step=9, cell=7.6, sparkles=False))
        p.append(f'<text class="t" x="{x}" y="{yy + 17 * 9 + 30}">{name}</text>')

    # 3. lockup, on white, sizes
    y += 24 + 2 * 210 + 20
    p.append(f'<text class="a" x="40" y="{y}">3 · Lockup, on white, and small sizes</text>')
    word = {k: "#fff" for k in text_lit("BB LEARN", 20, 5)}
    p.append(board(40, y + 24, 70, 17, rest, DARK, dc=2, dr=1, step=11, cell=9, extra=word))
    y2 = y + 24 + 17 * 11 + 40
    p.append(board(40, y2, 15, 15, rest, LIGHT, dc=0, dr=0, step=12, cell=10, dark=False, sparkles=False))
    p.append(f'<text class="s" x="40" y="{y2 + 15 * 12 + 24}">on white: resting</text>')
    p.append(board(260, y2, 15, 15, STATES["happy"][2], LIGHT, dc=0, dr=0, step=12, cell=10, dark=False, sparkles=False))
    p.append(f'<text class="s" x="260" y="{y2 + 15 * 12 + 24}">on white: happy</text>')
    x = 480
    for size in (64, 32, 24):
        st = size / 15
        p.append(board(x, y2, 15, 15, rest, DARK, dc=0, dr=0, step=st, cell=st * (0.86 if size >= 64 else 1), sparkles=False))
        p.append(f'<text class="s" x="{x}" y="{y2 + size + 28}">{size}px</text>')
        x += size + 50
    st = 16 / 9
    p.append(board(x, y2, 9, 9, SMALL, DARK, dc=0, dr=0, step=st, cell=st, sparkles=False))
    p.append(board(x + 50, y2, 9, 9, SMALL, LIGHT, dc=0, dr=0, step=st, cell=st, dark=False, sparkles=False))
    p.append(f'<text class="s" x="{x}" y="{y2 + 44}">16px</text>')
    p.append(board(x + 130, y2, 9, 9, SMALL, DARK, dc=0, dr=0, step=13, cell=11, sparkles=False))
    p.append(f'<text class="s" x="{x + 130}" y="{y2 + 140}">16px cut, enlarged</text>')
    p.append("</svg>")
    (HERE / "cube_blue_sheet.svg").write_text("\n".join(p) + "\n")


if __name__ == "__main__":
    main()
