"""
"Unmute": the whole film, from the scene files in paper/out/.

Dissolves between scenes, a fade through black for "the next day", audio
crossfaded to match, then one loudness pass over the whole thing so no scene
jumps out.
"""

import os
import subprocess

import imageio_ffmpeg

OUT = "paper/out/unmute_full.mp4"
# scene file, its length in seconds, transition INTO the next one
SCENES = [
    ("paper/out/d01_class.mp4", 15.0, "fade", 0.5),      # to night
    ("paper/out/d04_box.mp4", 6.0, "fade", 0.3),         # into the laptop
    ("paper/out/d05_why.mp4", 6.0, "fade", 0.3),
    ("paper/out/d06_montage.mp4", 12.5, "fadeblack", 0.6),   # next day
    ("paper/out/d07_nextday.mp4", 12.0, "fade", 0.4),
    ("paper/out/d08_endcard.mp4", 6.0, None, 0),
]


def main():
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    args = [ff, "-y", "-loglevel", "error"]
    for path, *_ in SCENES:
        args += ["-i", path]
    v, a, parts = "[0:v]", "[0:a]", []
    t = SCENES[0][1]
    for i in range(1, len(SCENES)):
        kind, dur = SCENES[i - 1][2], SCENES[i - 1][3]
        off = t - dur
        parts.append(f"{v}[{i}:v]xfade=transition={kind}:duration={dur}"
                     f":offset={off:.3f}[v{i}]")
        parts.append(f"{a}[{i}:a]acrossfade=d={dur}[a{i}]")
        v, a = f"[v{i}]", f"[a{i}]"
        t = off + SCENES[i][1]
    parts.append(f"{a}loudnorm=I=-16:TP=-1.5:LRA=11[aout]")
    args += ["-filter_complex", ";".join(parts), "-map", v, "-map", "[aout]",
             "-c:v", "libx264", "-crf", "19", "-preset", "slow",
             "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
             "-ar", "48000", "-movflags", "+faststart", OUT]
    subprocess.run(args, check=True)
    print(OUT, f"{t:.1f}s")


if __name__ == "__main__":
    main()
