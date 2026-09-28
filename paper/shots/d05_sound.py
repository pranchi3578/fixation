"""Doodle beat 5 sound: room, pencil, the click, "Why?", the tutor.

The voice is a SCRATCH track from espeak-ng, only to time the edit. It is
replaced by a real actor (with consent) before anything ships.

The motif rides the story: the tutor wakes on the first note, answers on
the second, and the "?" becomes "!" on the third.
"""

import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import imageio_ffmpeg  # noqa: E402

import sound  # noqa: E402

FRAMES = os.environ.get("FRAMES", "paper/build/d05_frames")
OUT = os.environ.get("OUTFILE", "paper/out/d05_why.mp4")
CLICK, WHY, SMILE, POP = 2.9, 3.8, 4.3, 4.6
SCRATCH = "paper/build/why_scratch.wav"

subprocess.run(["espeak-ng", "-v", "en-us+f4", "-p", "72", "-s", "115",
                "Why?", "-w", SCRATCH], check=True)

m = sound.Mix(6.2)
m.fan(0.03)
m.rustle(1.2, 0.8, 0.06, bright=1.6)     # the pencil redraws her hand move
m.tick(2.05, 0.08)
m.tick(CLICK, 0.5)                       # click
m.rustle(CLICK + 0.02, 0.3, 0.25, bright=2.0)   # the slash scribbled out
m.voice(WHY - 0.05, SCRATCH, 0.9)        # the first word of the film
m.pluck(WHY + 0.15, sound.MOTIF[0][0], gain=0.22)
m.pluck(SMILE + 0.05, sound.MOTIF[1][0], gain=0.2)
m.pluck(POP, sound.MOTIF[2][0], gain=0.24)
m.snap(POP, 0.25)
wav = m.write("paper/build/d05.wav")

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
