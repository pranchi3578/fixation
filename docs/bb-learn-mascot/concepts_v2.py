"""Round 2 concept sheet: fourteen BB Learn characters from five angles, all
drawn on BrainBack's pixel grid (10px cell, 2px gap). These are rough sketches,
for choosing a direction.

    python3 docs/bb-learn-mascot/concepts_v2.py   ->  concepts_v2.svg
"""
from pathlib import Path

CELL, GAP = 10, 2
STEP = CELL + GAP

# '#' ink, '+' 35% ink (the brand's opacity scale, not a new colour), '.' empty


def wave():
    """Voice bars, centred on a middle line; the eyes are cut into the two tallest bars."""
    heights = [2, 6, 10, 8, 4]
    rows = 10
    g = [["."] * 14 for _ in range(rows)]
    for i, h in enumerate(heights):
        top = (rows - h) // 2
        for r in range(top, top + h):
            for c in (i * 3, i * 3 + 1):
                g[r][c] = "#"
    for c in (7, 10):  # eyes
        for r in (3, 4):
            g[r][c] = "."
    return ["".join(r) for r in g]


ANGLES = [
    ("1 · The name", "BrainBack sounds like backpack, and learning that comes back", [
        ("Basta", "the school bag (बस्ता) that talks", [
            "....####....",
            "...#....#...",
            "..########..",
            ".##########.",
            ".##.####.##.",
            ".##.####.##.",
            ".##########.",
            ".#++++++++#.",
            ".#+######+#.",
            ".#+######+#.",
            ".##########.",
            "..##....##..",
        ]),
        ("Wapas", "a boomerang: learning comes back", [
            "###.........",
            "####........",
            ".####.......",
            "..####......",
            "...#.##.....",
            "...#.###....",
            "..######....",
            ".######.....",
            "#####.......",
            "###.........",
        ]),
    ]),
    ("2 · What it does", "talks, shows, fixes, waits, stops when you speak", [
        ("Bubble", "round 1's pick: it talks", [
            "..#######+..",
            ".#########++",
            "############",
            "###.####.###",
            "###.####.###",
            "############",
            "#####..#####",
            ".##########.",
            "..########..",
            "..##........",
            "..#.........",
        ]),
        ("Tarang", "a voice wave (तरंग) with a face", wave()),
        ("Blink", "the text cursor: it waits for you", [
            "########",
            "########",
            ".######.",
            ".#.##.#.",
            ".#.##.#.",
            ".######.",
            ".######.",
            ".##..##.",
            ".######.",
            ".######.",
            "########",
            "########",
        ]),
        ("Unmute", "the mic from the ad: ask anything", [
            "...####...",
            "..######..",
            "..#.##.#..",
            "..#.##.#..",
            "..######..",
            "..##..##..",
            "#.######.#",
            "#..####..#",
            ".#......#.",
            "..######..",
            "....##....",
            "..######..",
        ]),
    ]),
    ("3 · The brand system", "one pixel of the grid, and compounding growth", [
        ("Bit", "one active cell of the grid wakes up", [
            "+.+.+.+.+.+",
            "...........",
            "+.######.++",
            "..######...",
            "+.#.##.#.++",
            "..#.##.#...",
            "+.######.++",
            "..######...",
            "+.+.+.+.+.+",
        ]),
        ("Ankur", "a sprout (अंकुर) that grows weekly", [
            ".......##.#.",
            "......####..",
            "..##...##...",
            ".####.##....",
            "..##.##.....",
            ".....##.....",
            "..########..",
            ".##########.",
            ".##.####.##.",
            ".##.####.##.",
            ".##########.",
            "..########..",
        ]),
    ]),
    ("4 · India's classroom", "the objects every Indian child already knows", [
        ("Patti", "the slate: chalk face, any script", [
            ".....++.....",
            "....+..+....",
            "++++++++++++",
            "+##########+",
            "+###.##.###+",
            "+###.##.###+",
            "+##########+",
            "+###....###+",
            "+####..####+",
            "+##########+",
            "++++++++++++",
        ]),
        ("Pulli", "a kolam drawn around the dots", [
            "+.+.+#+.+.+",
            "...##.##...",
            "+.#+.+.+#.+",
            ".#.......#.",
            "#.+.#.#.+.#",
            ".#.......#.",
            "+.#+.+.+#.+",
            "...##.##...",
            "+.+.+#+.+.+",
        ]),
        ("Akshar", "one letter, any script, same eyes", [
            "..#....#....",
            "############",
            "..##....##..",
            ".#..#...##..",
            "....#...##..",
            "..##....##..",
            "....#.####..",
            ".#..#...##..",
            "..##....##..",
            "........##..",
        ]),
    ]),
    ("5 · The ad's story", "the doubt arrives, the tutor answers, the doubt flies", [
        ("Doubtling", "the doubt: folded paper, one eye", [
            "............##..",
            ".....#.....#..#.",
            "....###.......#.",
            "...#####.....#..",
            "..#######...#...",
            ".####.####..#...",
            "#####.#####.....",
            "###########.#...",
            ".#########......",
            "..##...##.......",
        ]),
        ("Answered", "the doubt, refolded into a plane", [
            "##..............",
            ".####...........",
            "..#######.......",
            "...###.#######..",
            "....###########.",
            "...#########....",
            "..######........",
            ".###............",
            "##..............",
        ]),
        ("Duo", "the tutor and the doubt, together", [
            "..........#.#",
            "...........#.",
            ".#######.....",
            "#########....",
            "##.###.##....",
            "##.###.##....",
            "#########....",
            "###...###....",
            ".#######.....",
            ".##..........",
            ".#...........",
        ]),
    ]),
]


def pixels(grid, x0, y0, step, cell, ink="#000"):
    out = []
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == ".":
                continue
            op = "1" if ch == "#" else "0.35"
            out.append(
                f'<rect x="{x0 + c * step:.1f}" y="{y0 + r * step:.1f}" width="{cell:.1f}" '
                f'height="{cell:.1f}" rx="{cell / 10:.1f}" fill="{ink}" fill-opacity="{op}"/>'
            )
    return "\n".join(out)


def main():
    LABEL_W, TILE_W, TILE_H, PAD = 250, 270, 250, 20
    W = 40 + LABEL_W + 4 * (TILE_W + PAD)
    H = 110 + len(ANGLES) * (TILE_H + PAD) + 110
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        '<style>text{font-family:"Geist Sans",Inter,system-ui,sans-serif}'
        ".h{font-size:28px;font-weight:800;letter-spacing:-0.02em}"
        ".a{font-size:17px;font-weight:700}.t{font-size:17px;font-weight:600}"
        ".s{font-size:13px;fill:#696969}"
        '.m{font-family:"Geist Mono",ui-monospace,monospace;font-size:11px;fill:#696969}</style>',
        '<text class="h" x="40" y="58">BB Learn: fourteen characters, five angles</text>',
        '<text class="s" x="40" y="84">rough sketches on BrainBack\'s pixel grid · black, and 35% black · for choosing a direction</text>',
    ]
    y = 110
    n = 0
    for angle, why, concepts in ANGLES:
        parts.append(f'<text class="a" x="40" y="{y + 30}">{angle}</text>')
        words, line, ly = why.split(), "", y + 54
        for w in words:  # wrap the angle note to the label column
            if len(line) + len(w) > 30:
                parts.append(f'<text class="s" x="40" y="{ly}">{line}</text>')
                line, ly = "", ly + 18
            line += w + " "
        parts.append(f'<text class="s" x="40" y="{ly}">{line}</text>')
        for i, (name, note, grid) in enumerate(concepts):
            n += 1
            x = 40 + LABEL_W + i * (TILE_W + PAD)
            gw, gh = len(grid[0]) * STEP, len(grid) * STEP
            parts.append(f'<rect x="{x}" y="{y}" width="{TILE_W}" height="{TILE_H}" rx="12" fill="none" stroke="#e8e8e8"/>')
            parts.append(pixels(grid, x + (TILE_W - gw) / 2, y + 20 + (150 - gh) / 2, STEP, CELL))
            parts.append(f'<text class="m" x="{x + 18}" y="{y + 198}">{n:02d}</text>')
            parts.append(f'<text class="t" x="{x + 44}" y="{y + 198}">{name}</text>')
            parts.append(f'<text class="s" x="{x + 18}" y="{y + 224}">{note}</text>')
        y += TILE_H + PAD

    # every concept at 16px and 32px: the favicon test
    parts.append(f'<text class="a" x="40" y="{y + 30}">The favicon test</text>')
    parts.append(f'<text class="s" x="40" y="{y + 54}">every concept at 32px, and at 16px</text>')
    x = 40 + LABEL_W
    for _, _, concepts in ANGLES:
        for name, _, grid in concepts:
            for size, dy in ((32, 0), (16, 48)):
                step = size / max(len(grid[0]), len(grid))
                parts.append(pixels(grid, x, y + 10 + dy, step, step))
            x += 64
    parts.append("</svg>")
    Path(__file__).with_name("concepts_v2.svg").write_text("\n".join(parts) + "\n")


if __name__ == "__main__":
    main()
