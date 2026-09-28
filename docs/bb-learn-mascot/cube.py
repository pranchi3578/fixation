"""The BB Learn Cube: a square robot owl on BrainBack's PixelBoard.

    python3 docs/bb-learn-mascot/cube.py
        -> cube_sheet.svg   variants, states, lockup, sizes
        -> cube.html        a live prototype: idle life plus every state

Grids are text. 1 = box, 2 = box edge / shutter, 3 = lens and trim,
4 = glint and lit parts, o = pupil (unlit on the board, full ink on white).
"""
import json
from pathlib import Path

from owl import board, text_lit

HERE = Path(__file__).parent
LEVEL = {"1": 0.26, "2": 0.5, "3": 0.78, "4": 1.0}
LIGHT = {"1": 0.8, "2": 0.55, "3": 0.3, "4": 0.07, "o": 1.0}
W, H = 15, 15


def pupil_eye(r, c, bg="3"):
    """A 4x4 lens with a 2x2 pupil at (r, c); its top-left cell is the glint."""
    return ["".join(("4" if (y, x) == (r, c) else "o") if r <= y < r + 2 and c <= x < c + 2 else bg
                    for x in range(4)) for y in range(4)]


REST_EYE = pupil_eye(1, 1)


def cube(variant="bolts", eyes=None, right=None, tufts="2", meter="44422",
         wings=(5, 5), extra=None):
    g = [["."] * W for _ in range(H)]
    for r in range(2, 13):                         # the box, cols 1-13
        for c in range(1, 14):
            g[r][c] = "2" if r in (2, 12) or c in (1, 13) else "1"
    if variant == "tufted":                        # the box's corners grow ear tufts
        g[0][1] = g[0][13] = tufts
        g[1][1] = g[1][2] = g[1][12] = g[1][13] = tufts
    elif variant == "bolts":
        g[1][4] = g[1][10] = tufts
    elif variant == "soft":
        g[2][1] = g[2][13] = g[12][1] = g[12][13] = "."
        g[1][3] = g[1][4] = g[1][10] = g[1][11] = tufts
    for c0, pat in ((3, eyes or REST_EYE), (8, right or eyes or REST_EYE)):
        for dr, row in enumerate(pat):
            for dc, ch in enumerate(row):
                g[4 + dr][c0 + dc] = ch
    g[8][7] = "3"                                  # beak sensor
    for c in range(2, 13):                         # lid seam
        g[9][c] = "2"
    for i, ch in enumerate(meter):                 # learning meter
        g[10][5 + i] = ch
    if variant != "bolts":
        lw, rw = wings                             # side flaps: top row of each
        for r in range(lw, lw + 4):
            g[r][0] = "1"
        for r in range(rw, rw + 4):
            g[r][14] = "1"
    g[13] = list("..3333...3333..")
    g[14] = list("..2323...2323..")
    for (r, c), ch in (extra or {}).items():
        g[r][c] = ch
    return ["".join(r) for r in g]


VARIANTS = [
    ("Bolts (chosen)", "round 4's cube: the ear tufts become two bolts", cube("bolts")),
    ("Tufted", "the corners grow ear tufts; wing flaps", cube("tufted")),
    ("Soft", "rounded corners, tufts as soft bumps", cube("soft")),
]

SHUT = ["3333", "3333", "4444", "3333"]
HAPPY = ["1111", "1441", "4114", "1111"]
HALF = ["2222", "2222", "34o3", "3oo3"]

STATES = {
    "rest":      ("Resting", "pupils centred, meter shows progress", cube()),
    "hello":     ("Hello", "happy eyes, the bolts glow on", cube(eyes=HAPPY, tufts="3")),
    "listen":    ("Listening", "bolts light up, pupils up: it stops the moment you speak", cube(eyes=pupil_eye(0, 1), tufts="4")),
    "talk":      ("Talking", "the meter becomes its voice", cube(meter="34243")),
    "work":      ("Your work", "eyes on the lesson, not on you", cube(eyes=pupil_eye(2, 0))),
    "hmm":       ("Hmm", "one shutter half down: curious, never disappointed", cube(right=HALF)),
    "happy":     ("Happy", "for effort: a hop, bolts lit, meter jumps", cube(eyes=HAPPY, tufts="4", meter="44442")),
    "oops":      ("Oops", "crossed eyes; a meter cell drops out", cube(eyes=pupil_eye(1, 2), right=pupil_eye(1, 0), meter="4442.", extra={(11, 9): "4"})),
    "think":     ("Thinking", "pupils up and aside, meter pulses", cube(eyes=pupil_eye(0, 2), meter="24222")),
    "sleepy":    ("Sleepy", "shutters half down, bolts dim: go to bed", cube(eyes=HALF, tufts="1")),
    "blink":     ("Blink", "random 2-6 s gaps", cube(eyes=SHUT)),
}
for _, _, g in list(STATES.values()) + VARIANTS:
    assert len(g) == H and all(len(r) == W for r in g)

# a hand-cut 9x9 for 16px, where the full grid turns to mush
SMALL = [
    "..2...2..",
    "222222222",
    "211111112",
    "233313332",
    "24o313o42",
    "211131112",
    "214441112",
    "222222222",
    ".33...33.",
]


def lit(grid, dc=0, dr=0, light=False):
    t = LIGHT if light else LEVEL
    return {(c + dc, r + dr): t[ch] for r, row in enumerate(grid) for c, ch in enumerate(row) if ch in t}


def sheet():
    Wd, Ht = 1400, 1640
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wd}" height="{Ht}" viewBox="0 0 {Wd} {Ht}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        '<style>text{font-family:"Geist Sans",Inter,system-ui,sans-serif}'
        ".h{font-size:28px;font-weight:800;letter-spacing:-0.02em}"
        ".a{font-size:17px;font-weight:700}.t{font-size:15px;font-weight:600}"
        ".s{font-size:13px;fill:#696969}</style>",
        '<text class="h" x="40" y="58">BB Learn: the Cube</text>',
        '<text class="s" x="40" y="84">a square robot owl on the PixelBoard · master variants, states, lockup, sizes · live prototype in cube.html</text>',
    ]

    def note(x, y, title, text, width=34):
        p.append(f'<text class="t" x="{x}" y="{y}">{title}</text>')
        line, ly = "", y + 20
        for w in text.split():
            if len(line) + len(w) > width:
                p.append(f'<text class="s" x="{x}" y="{ly}">{line}</text>')
                line, ly = "", ly + 17
            line += w + " "
        p.append(f'<text class="s" x="{x}" y="{ly}">{line}</text>')

    y = 120
    p.append(f'<text class="a" x="40" y="{y}">1 · Master variants</text>')
    for i, (name, txt, g) in enumerate(VARIANTS):
        x = 40 + i * 450
        p.append(board(x, y + 24, 17, 17, lit(g, 1, 1), step=19, cell=16))
        note(x, y + 24 + 17 * 19 + 34, name, txt, 50)

    y += 24 + 17 * 19 + 100
    p.append(f'<text class="a" x="40" y="{y}">2 · States (bolts)</text>')
    for i, key in enumerate(STATES):
        name, txt, g = STATES[key]
        x = 40 + (i % 6) * 222
        yy = y + 24 + (i // 6) * 250
        p.append(board(x, yy, 17, 17, lit(g, 1, 1), step=9, cell=7.6, sparkles=False))
        note(x, yy + 17 * 9 + 30, name, txt, 28)

    y += 24 + 2 * 250 + 20
    p.append(f'<text class="a" x="40" y="{y}">3 · Lockup, on white, and small sizes</text>')
    lk = lit(STATES["rest"][2], 2, 1)
    lk.update(text_lit("BB LEARN", 20, 5))
    p.append(board(40, y + 24, 70, 17, lk, step=11, cell=9))
    y2 = y + 24 + 17 * 11 + 40
    p.append(board(40, y2, 15, 15, lit(STATES["rest"][2], light=True), step=12, cell=10, dark=False, sparkles=False))
    p.append(board(240, y2, 15, 15, lit(STATES["happy"][2], light=True), step=12, cell=10, dark=False, sparkles=False))
    p.append(f'<text class="s" x="40" y="{y2 + 15 * 12 + 24}">on white: resting</text>')
    p.append(f'<text class="s" x="240" y="{y2 + 15 * 12 + 24}">on white: happy</text>')
    x = 460
    for size in (64, 32, 24):
        st = size / 15
        p.append(board(x, y2, 15, 15, lit(STATES["rest"][2]), step=st, cell=st * 0.86 if size >= 64 else st, sparkles=False))
        p.append(f'<text class="s" x="{x}" y="{y2 + size + 28}">{size}px</text>')
        x += size + 50
    for size in (16,):
        st = size / 9
        p.append(board(x, y2, 9, 9, lit(SMALL), step=st, cell=st, sparkles=False))
        p.append(board(x + 50, y2, 9, 9, lit(SMALL, light=True), step=st, cell=st, dark=False, sparkles=False))
        p.append(f'<text class="s" x="{x}" y="{y2 + size + 28}">16px, hand-cut 9×9</text>')
    st = 9
    p.append(board(x + 150, y2, 9, 9, lit(SMALL), step=st * 1.3, cell=st * 1.1, sparkles=False))
    p.append(f'<text class="s" x="{x + 150}" y="{y2 + 140}">the 9×9 cut, enlarged</text>')
    p.append("</svg>")
    (HERE / "cube_sheet.svg").write_text("\n".join(p) + "\n")


HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BB Learn Cube</title>
<style>
  :root { --bg:#fff; --fg:#000; --muted:#696969; --line:#e8e8e8; }
  @media (prefers-color-scheme: dark) { :root { --bg:#0b0b0b; --fg:#fff; --muted:#9a9a9a; --line:#222; } }
  * { box-sizing: border-box; }
  body { margin:0; background:var(--bg); color:var(--fg);
         font:15px/1.5 "Geist Sans", Inter, system-ui, sans-serif; }
  main { max-width: 760px; margin: 0 auto; padding: 32px 16px 48px; }
  h1 { font-size: 26px; font-weight: 800; letter-spacing: -0.02em; margin: 0 0 4px; }
  p.sub { color: var(--muted); margin: 0 0 24px; }
  .stage { background:#050505; border-radius: 14px; padding: 14px; display:flex; justify-content:center; }
  canvas { width: 100%; max-width: 440px; height: auto; image-rendering: pixelated; cursor: pointer; }
  .states { display:flex; flex-wrap:wrap; gap:8px; margin: 18px 0 8px; }
  button { font: inherit; font-size: 14px; padding: 7px 12px; border-radius: 999px;
           border: 1px solid var(--line); background: transparent; color: var(--fg); cursor: pointer; }
  button[aria-pressed="true"] { background: var(--fg); color: var(--bg); border-color: var(--fg); }
  #why { color: var(--muted); min-height: 1.5em; }
  footer { color: var(--muted); font-size: 13px; margin-top: 28px; }
</style>
</head>
<body>
<main>
  <h1>BB Learn Cube</h1>
  <p class="sub">A live sketch of the idle loop and every state, on the PixelBoard. Tap the Cube to say hello.</p>
  <div class="stage"><canvas id="c" width="440" height="440" aria-label="The BB Learn Cube, animated"></canvas></div>
  <div class="states" id="states"></div>
  <div id="why"></div>
  <footer>Stepped at 10 fps, whole cells only. Blinks at random 2–6 s gaps, the box breathes, the pupils glance, the bolts twinkle. States return to rest after a few seconds.</footer>
</main>
<script>
const DATA = __DATA__;
const LEVEL = {"1":0.26,"2":0.5,"3":0.78,"4":1};
const COLS = 17, ROWS = 17, BASE = 0.07;
const cv = document.getElementById("c"), ctx = cv.getContext("2d");
const step = cv.width / COLS, cell = step * 0.84;

let state = "rest", until = 0, t = 0;
let nextBlink = 2 + Math.random() * 4, blinkEnd = -1;
let glance = null, glanceEnd = -1, hop = 0;

const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

function hash(i) { const r = Math.abs(Math.sin(i * 127.1 + 3.7) * 43758.5); return r - Math.floor(r); }

function frame() {
  let g = DATA.states[state].grid.map(r => r.split(""));
  if (state === "rest" && t < blinkEnd) g = DATA.states.blink.grid.map(r => r.split(""));
  if (state === "rest" && glance && t < glanceEnd) g = glance.map(r => r.split(""));
  if (state === "talk") {                       // the meter is its voice
    for (let i = 0; i < 5; i++) g[10][5 + i] = "234"[Math.floor(Math.random() * 3)];
  }
  if (state === "think") {                      // the meter pulses, one cell at a time
    const k = Math.floor(t * 4) % 5;
    for (let i = 0; i < 5; i++) g[10][5 + i] = i === k ? "4" : "2";
  }
  return g;
}

function draw() {
  const g = frame();
  const breath = reduce ? 0 : 0.05 * (Math.sin(t * 1.6) + 1) / 2;
  const dy = hop > 0 ? -1 : 0;
  ctx.fillStyle = "#050505"; ctx.fillRect(0, 0, cv.width, cv.height);
  for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) {
    const gr = r - 1 - dy, gc = c - 1;
    let v = BASE;
    const h = hash(r * COLS + c);
    if (h < 0.1) v = 0.1 + 0.12 * Math.pow(Math.max(0, Math.sin(t * (0.6 + h * 20) + h * 50)), 3);
    const ch = g[gr] && g[gr][gc];
    if (ch && LEVEL[ch] !== undefined) {
      v = LEVEL[ch];
      if (ch === "1") v += breath;
      if (ch === "2" && (gr <= 1) && state !== "listen" && state !== "sleepy")
        v += 0.25 * Math.pow(Math.max(0, Math.sin(t * 2.3 + gc)), 8);   // tufts twinkle
    }
    ctx.fillStyle = `rgba(255,255,255,${v.toFixed(3)})`;
    const x = c * step + (step - cell) / 2, y = r * step + (step - cell) / 2;
    ctx.beginPath(); ctx.roundRect ? ctx.roundRect(x, y, cell, cell, cell * 0.1) : ctx.rect(x, y, cell, cell); ctx.fill();
  }
}

function tick() {
  t += 0.1;
  if (hop > 0) hop--;
  if (state !== "rest" && t > until) setState("rest");
  if (state === "rest" && !reduce) {
    if (t > nextBlink) {
      blinkEnd = t + 0.15 + (Math.random() < 0.2 ? 0.3 : 0);   // sometimes a double
      nextBlink = t + 2 + Math.random() * 4;
    }
    if (t > glanceEnd && Math.random() < 0.012) {
      glance = DATA.glances[Math.floor(Math.random() * DATA.glances.length)];
      glanceEnd = t + 0.8 + Math.random();
    }
  }
  draw();
}

function setState(s, hold) {
  state = s; until = t + (hold || 3.2);
  document.querySelectorAll("#states button").forEach(b => b.setAttribute("aria-pressed", b.dataset.s === s));
  document.getElementById("why").textContent = s === "rest" ? "" : DATA.states[s].why;
  if (s === "hello" || s === "happy") hop = 3;
}

const box = document.getElementById("states");
for (const [k, v] of Object.entries(DATA.states)) {
  if (k === "blink") continue;
  const b = document.createElement("button");
  b.textContent = v.name; b.dataset.s = k; b.setAttribute("aria-pressed", k === "rest");
  b.onclick = () => setState(k); box.appendChild(b);
}
cv.onclick = () => setState("hello", 2);
setState("hello", 2);
setInterval(tick, 100);
</script>
</body>
</html>
"""


def prototype():
    data = {
        "states": {k: {"name": n, "why": w, "grid": g} for k, (n, w, g) in STATES.items()},
        "glances": [cube(eyes=pupil_eye(r, c)) for r, c in ((1, 0), (1, 2), (2, 1), (0, 1))],
    }
    (HERE / "cube.html").write_text(HTML.replace("__DATA__", json.dumps(data)))


if __name__ == "__main__":
    sheet()
    prototype()
