"""Beat 5 sound: fan, arm, tape, "Why?", and the lantern's answer.

The voice is a SCRATCH track from espeak-ng, only to time the edit. It is
replaced by a real actor (with consent) before anything ships.
"""

import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import imageio_ffmpeg  # noqa: E402

import sound  # noqa: E402

FRAMES = os.environ.get("FRAMES", "paper/build/u05_frames")
OUT = os.environ.get("OUTFILE", "paper/out/u05_why.mp4")
WHY = 3.8
SCRATCH = "paper/build/why_scratch.wav"

subprocess.run(["espeak-ng", "-v", "en-us+f4", "-p", "72", "-s", "115",
                "Why?", "-w", SCRATCH], check=True)

m = sound.Mix(6.2)
m.fan(0.03)
m.rustle(1.2, 0.8, 0.12)                # the hand rises
m.rustle(2.0, 0.35, 0.08)               # ...pulls back
m.rustle(2.4, 0.4, 0.1)                 # ...goes back
m.peel(2.8, 0.8, 0.35)                  # the tape comes off
m.rustle(3.6, 0.35, 0.1)
m.voice(WHY - 0.05, SCRATCH, 0.9)       # the first word of the film
m.pluck(WHY + 0.15, sound.MOTIF[0][0], gain=0.22)   # the lantern lights
m.pluck(WHY + 0.55, sound.MOTIF[1][0], gain=0.2)    # and begins to answer
wav = m.write("paper/build/u05.wav")

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
