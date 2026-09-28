"""End card sound: hops, a pop, pen on paper, and a chord to close on."""

import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import imageio_ffmpeg  # noqa: E402

import sound  # noqa: E402

FRAMES = os.environ.get("FRAMES", "paper/build/d08_frames")
OUT = os.environ.get("OUTFILE", "paper/out/d08_endcard.mp4")

m = sound.Mix(6.2)
m.fan(0.012)
for k in range(3):
    m.tick(0.15 + k * 0.26, 0.15)                 # hop hop hop
m.snap(0.8, 0.3)                                  # ? -> !
m.pluck(0.8, sound.MOTIF[2][0], gain=0.2)
m.rustle(1.1, 0.8, 0.07, bright=2.2)              # pen: "Ask anything."
m.rustle(2.0, 0.8, 0.07, bright=2.2)              # "Interrupt anytime."
m.rustle(3.1, 0.4, 0.05, bright=1.2)              # highlighter
for midi in (62, 66, 69, 74):                     # D major, to close
    m.pluck(3.4, midi, dur=2.6, gain=0.18)
wav = m.write("paper/build/d08.wav")

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
