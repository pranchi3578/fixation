"""The next day, sound: the same lecture, the same silence -- then a click,
her voice, and a room that starts talking.

Her line is SCRATCH voice (espeak-ng); replaced by a real actor before
anything ships. Classmates are soft, higher gibberish, one after another.
The four-note motif finally plays whole, rising into the end card.
"""

import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import imageio_ffmpeg  # noqa: E402

import sound  # noqa: E402
from d07_nextday import (ASK, CLICK, ORDER, PLANES, REPLY, SAY,  # noqa: E402
                         WAVE)

FRAMES = os.environ.get("FRAMES", "paper/build/d07_frames")
OUT = os.environ.get("OUTFILE", "paper/out/d07_nextday.mp4")

m = sound.Mix(12.2)
m.fan(0.022)
m.gibberish(0.05, ASK - 0.1, 0.3)
for k in range(3):
    m.rustle(k * 0.55, 0.09, 0.05, bright=2.2)
m.gibberish(ASK, 1.0, 0.34, rate=4.5, pitch=150, rise_end=True)
m.tick(CLICK, 0.5)                                 # no hesitation this time
m.rustle(CLICK + 0.02, 0.3, 0.2, bright=2.0)
line = "paper/build/d07_line.wav"
subprocess.run(["espeak-ng", "-v", "en-us+f4", "-p", "72", "-s", "140",
                "Sir, why squared?", "-w", line], check=True)
m.voice(SAY, line, 0.9)
m.gibberish(REPLY, 1.1, 0.3, rate=5, pitch=160)    # "Good question!"
for i in range(len(ORDER)):                        # the room unmutes
    t0 = WAVE + 0.3 * i
    m.tick(t0, 0.18)
    m.gibberish(t0 + 0.1, 0.5, 0.07 + 0.01 * i, rate=8,
                pitch=260 + 15 * (i % 4))
for t0, _, _ in PLANES:
    m.whoosh(t0, 1.2, 0.08)
for k, (midi, dt) in enumerate(sound.MOTIF):       # the whole motif, at last
    m.pluck(10.2 + dt * 1.3, midi, gain=0.26, dur=2.0)
wav = m.write("paper/build/d07.wav")

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
