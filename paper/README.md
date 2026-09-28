# The Paper World

The Brainback Learn campaign, made entirely in code. Plan:
`docs/brainback-learn-paper-world-plan.md`.

Nothing here is filmed, sampled or downloaded, apart from Blender itself
(the `bpy` wheel from PyPI). Every texture, puppet, light, sound and note
is written in these files.

## Setup

```
uv venv -p 3.11 .venv-bpy
VIRTUAL_ENV=.venv-bpy uv pip install bpy==4.2.0 numpy pillow scipy imageio-ffmpeg
```

`bpy` 4.2 needs Python 3.11 exactly. Renders use Cycles on CPU.

## Layout

| Path | What |
|---|---|
| `lib/paper.py` | Paper stocks: ruled, graph, sugar, kraft, and the Doubtling's sheet with its inked eye |
| `lib/stage.py` | Render settings, paper materials, the lamp, the night fill, the camera |
| `lib/puppets.py` | The Doubtling: one dart mesh, every pose computed from five numbers |
| `lib/sound.py` | Paper, fan, whoosh and the four-note motif, synthesised |
| `shots/sNN_*.py` | One script per step or shot |
| `out/` | What gets reviewed: stills and films |
| `build/` | Textures and frames. Not in git; every file there is regenerated |

## Rebuild the pilot

```
python paper/lib/paper.py                     # stocks
python -c "import sys; sys.path.insert(0,'paper/lib'); import paper; paper.night_stocks(); paper.doubtling(eye='open'); paper.doubtling(eye='closed')"
SAMPLES=32 python paper/shots/s04_pilot.py    # 60 frames, resumable
python paper/shots/s04_sound.py               # mix + mux -> paper/out/s04_pilot.mp4
```

`s04_pilot.py first last` renders a range of frames, so a render can be
split across machines or restarted after a container is reclaimed. Each
frame's hand-wobble is seeded by its number, so a re-render matches.
