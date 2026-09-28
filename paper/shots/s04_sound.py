"""Step 4 sound, cued to the pilot's timeline, then muxed with the frames.

The motif is split across the story: the Glow asks the first two notes,
"!" adds the third, and the flight lands the fourth.
"""

import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import imageio_ffmpeg  # noqa: E402

import sound  # noqa: E402

FRAMES = os.environ.get("FRAMES", "paper/build/s04_frames")
OUT = os.environ.get("OUTFILE", "paper/out/s04_pilot.mp4")

m = sound.Mix(5.2)
m.fan(0.035)
m.rustle(0.05, 0.9, 0.10)            # breathing: barely there
m.tick(0.58)                          # blink
m.pluck(1.0, sound.MOTIF[0][0])       # the Glow: a question begins
m.pluck(1.22, sound.MOTIF[1][0])
m.rustle(1.3, 0.55, 0.45, bright=1.4)  # the long unbend
m.pluck(1.8, sound.MOTIF[2][0])       # "!"
m.tick(2.32)
m.rustle(2.6, 0.45, 0.35)             # tipping
m.snap(3.0, 0.7)                      # wings crack open
m.whoosh(3.05, 1.5, 0.3)
m.pluck(3.9, sound.MOTIF[3][0], dur=1.3, gain=0.3)   # lands
wav = m.write("paper/build/s04.wav")

ff = imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([
    ff, "-y", "-loglevel", "error",
    "-framerate", "12", "-i", f"{FRAMES}/f%03d.png",
    "-i", wav,
    "-vf", "fps=24,format=yuv420p",          # each frame held for two: on twos
    "-c:v", "libx264", "-crf", "18", "-preset", "slow",
    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000",
    "-c:a", "aac", "-b:a", "160k", "-shortest",
    "-movflags", "+faststart", OUT], check=True)
print(OUT)
