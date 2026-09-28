"""The pencil box, sound: night, a rattling tin, paper, and a new light."""

import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import imageio_ffmpeg  # noqa: E402

import sound  # noqa: E402

FRAMES = os.environ.get("FRAMES", "paper/build/d04_frames")
OUT = os.environ.get("OUTFILE", "paper/out/d04_box.mp4")
OPEN0, OPEN1, SPILL, UNCRUMPLE, GLOW, HOP = 0.8, 1.8, 1.9, 2.6, 3.6, 3.8

m = sound.Mix(6.2)
m.fan(0.02)
m.crickets(0.018)
for k in range(9):                               # something in there
    m.tick(0.12 + k * 0.075, 0.12)
m.clink(OPEN0, 0.2, f=1100)                      # the lid unlatches
m.clink(OPEN1 - 0.05, 0.14, f=700)               # ...and lands open
m.rustle(OPEN1 - 0.2, 0.5, 0.18, bright=1.2)     # weeks of paper, loosening
for k in range(3):
    m.rustle(SPILL + 0.08 * k, 0.35, 0.12, bright=1.5)
    m.thud(SPILL + 0.55 + 0.08 * k, 0.06)
m.rustle(UNCRUMPLE, 0.6, 0.3, bright=1.8)        # one of them opens up
m.pluck(GLOW, sound.MOTIF[0][0], gain=0.2)       # the screen lights
for k in range(3):                               # hop, hop, hop
    m.tick(HOP + 0.3 + k * 0.6, 0.18)
wav = m.write("paper/build/d04.wav")

ff = imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([
    ff, "-y", "-loglevel", "error",
    "-framerate", "12", "-i", f"{FRAMES}/f%03d.png", "-i", wav,
    "-vf", "fps=24,format=yuv420p",
    "-c:v", "libx264", "-crf", "18", "-preset", "slow",
    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000",
    "-c:a", "aac", "-b:a", "160k", "-shortest",
    "-movflags", "+faststart", OUT], check=True)
print(OUT)
