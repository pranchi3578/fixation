"""Concept sheet for the BB Learn character: three directions, drawn on
BrainBack's own pixel grid (10px cell, 2px gap). Rough on purpose; this is
for choosing a direction, not the final mark.

    python3 docs/bb-learn-mascot/concepts.py   ->  concepts.svg
"""
from pathlib import Path

CELL, GAP = 10, 2
STEP = CELL + GAP

# '#' ink, '+' half ink (the brand's opacity system, not a new colour), '.' empty
CONCEPTS = {
    "A · Pixel Doubtling": (
        "the ad's doubt, one eye, ? tail",
        [
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
        ],
    ),
    "B · Bubble (recommended)": (
        "a speech bubble that teaches",
        [
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
        ],
    ),
    "C · Answered": (
        "the doubt, refolded into a plane",
        [
            "##..............",
            ".####...........",
            "..#######.......",
            "...###.#######..",
            "....###########.",
            "...#########....",
            "..######........",
            ".###............",
            "##..............",
        ],
    ),
}

# B at small sizes: gaps closed, the same grid
BUBBLE = CONCEPTS["B · Bubble (recommended)"][1]


def pixels(grid, x0, y0, step, cell, ink="#000"):
    out = []
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == ".":
                continue
            op = "1" if ch == "#" else "0.35"
            out.append(
                f'<rect x="{x0 + c * step}" y="{y0 + r * step}" width="{cell}" '
                f'height="{cell}" rx="{cell / 10:.1f}" fill="{ink}" fill-opacity="{op}"/>'
            )
    return "\n".join(out)


def main():
    W, H = 1200, 640
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        '<style>text{font-family:"Geist Sans",Inter,system-ui,sans-serif}'
        ".t{font-size:18px;font-weight:600}.s{font-size:13px;fill:#696969}"
        ".m{font-family:\"Geist Mono\",ui-monospace,monospace;font-size:11px;fill:#696969}</style>",
    ]
    for i, (name, (note, grid)) in enumerate(CONCEPTS.items()):
        x = 60 + i * 380
        w = len(grid[0]) * STEP
        h = len(grid) * STEP
        ox = x + (260 - w) / 2
        oy = 80 + (160 - h) / 2
        parts.append(f'<rect x="{x - 20}" y="40" width="340" height="300" rx="12" fill="none" stroke="#e8e8e8"/>')
        parts.append(pixels(grid, ox, oy, STEP, CELL))
        parts.append(f'<text class="t" x="{x}" y="290">{name}</text>')
        parts.append(f'<text class="s" x="{x}" y="314">{note}</text>')

    # size test for B: 16, 24, 32, 64px, gapless under 64
    parts.append('<text class="t" x="40" y="400">B at size</text>')
    parts.append('<text class="s" x="40" y="424">gapless at and under 32px; the 2px gap returns at 64px and up</text>')
    x = 40
    for size in (16, 24, 32, 64, 128):
        cols = len(BUBBLE[0])
        step = size / cols
        gap = step * GAP / STEP if size >= 64 else 0
        parts.append(pixels(BUBBLE, x, 460, step, step - gap))
        parts.append(f'<text class="m" x="{x}" y="{460 + len(BUBBLE) * step + 20}">{size}px</text>')
        x += size + 60
    # reversed, on black
    parts.append(f'<rect x="{x}" y="440" width="190" height="170" rx="12" fill="#000"/>')
    parts.append(pixels(BUBBLE, x + 31, 455, 128 / 12, 128 / 12 - 2, ink="#fff"))
    parts.append("</svg>")
    Path(__file__).with_name("concepts.svg").write_text("\n".join(parts) + "\n")


if __name__ == "__main__":
    main()
