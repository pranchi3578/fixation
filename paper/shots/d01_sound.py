"""The class, sound: the teacher's gibberish, pages flying, her silence.

The teacher is the only voice, and it isn't words. It ducks while we are in
Meera's head, and comes back for "Any questions?" -- then nothing but the
fan, and the soft clicks of a call ending tile by tile.
"""

import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import imageio_ffmpeg  # noqa: E402
import numpy as np  # noqa: E402

import sound  # noqa: E402

FRAMES = os.environ.get("FRAMES", "paper/build/d01_frames")
OUT = os.environ.get("OUTFILE", "paper/out/d01_class.mp4")
Q_RISE, HOVER, CRUMPLE, OUT_T, ASK, DARK = 6.0, 7.0, 9.4, 10.4, 11.7, 13.2


def duck(t):
    """The lecture recedes while we're with her."""
    down = np.clip((t - 4.0) / 1.5, 0, 1)
    up = np.clip((t - OUT_T) / 1.0, 0, 1)
    return 1 - 0.65 * down * (1 - up)


m = sound.Mix(15.2)
m.fan(0.025)
m.gibberish(0.1, ASK - 0.4, 0.34, env=duck)
for k in range(int(ASK / 0.55)):              # every slide slams in
    m.rustle(k * 0.55, 0.09, 0.05 * duck(np.array([k * 0.55]))[0],
             bright=2.2)
m.gibberish(ASK, 1.0, 0.36, rate=4.5, pitch=150, rise_end=True)  # "…questions?"
m.pluck(Q_RISE, sound.MOTIF[0][0], gain=0.12)   # a question forms
m.rustle(CRUMPLE, 0.5, 0.3, bright=1.8)         # ...and is crumpled
m.thud(CRUMPLE + 0.9, 0.12)
order = 14
for i in range(order):
    start = DARK + 0.09 * i + (0.35 if i == order - 1 else 0)
    m.tick(start, 0.12 if i < order - 1 else 0.3)
wav = m.write("paper/build/d01.wav")

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
