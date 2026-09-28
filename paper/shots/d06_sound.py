"""The montage, sound. The tutor murmurs; the instant she speaks, it stops.

Her lines are SCRATCH voice (espeak-ng), for timing only; a real actor
replaces them before anything ships. The tutor is a warm, higher murmur,
never words -- it is only ever answering. Each answer is a note of the
motif and a paper plane leaving.
"""

import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import imageio_ffmpeg  # noqa: E402

import sound  # noqa: E402
from d06_montage import LINES, PLANES, TALK  # noqa: E402

FRAMES = os.environ.get("FRAMES", "paper/build/d06_frames")
OUT = os.environ.get("OUTFILE", "paper/out/d06_montage.mp4")

m = sound.Mix(12.7)
m.fan(0.02)
for i, (a, b) in enumerate(TALK):              # the tutor, cut off cleanly
    if b - a > 0.2:
        m.gibberish(a, b - a, 0.16, rate=5.5, pitch=210)
for i, (a, b, text) in enumerate(LINES):       # her, scratch voice
    path = f"paper/build/d06_line{i}.wav"
    subprocess.run(["espeak-ng", "-v", "en-us+f4", "-p", "72", "-s", "150",
                    text.replace("—", ","), "-w", path], check=True)
    m.voice(a, path, 0.85)
laugh = "paper/build/d06_laugh.wav"
subprocess.run(["espeak-ng", "-v", "en-us+f4", "-p", "85", "-s", "170",
                "ha ha ha", "-w", laugh], check=True)
m.voice(11.2, laugh, 0.5)
notes = [sound.MOTIF[k % 4][0] for k in range(len(PLANES))]
for (t0, _), midi in zip(PLANES, notes):
    m.rustle(t0, 0.3, 0.12, bright=1.6)         # a crumpled one lets go
    m.pluck(t0 + 0.35, midi, gain=0.17)
    m.whoosh(t0 + 0.4, 1.0, 0.1)
for t0 in (6.0, 7.0):                            # pages: forward, and back
    m.rustle(t0, 0.18, 0.1, bright=2.0)
wav = m.write("paper/build/d06.wav")

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
