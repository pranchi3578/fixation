"""
"Unmute": the best-quality master, built from source, compressed once.

final_cut.py joins the review MP4s, which were already compressed once each.
This goes back to the PNG frames and the raw scene audio instead: every
scene is encoded losslessly first, the transitions are made on those, and
only the final file is compressed -- H.264 High, tuned for flat drawn
animation, at a quality setting well past what the eye can separate.

Usage:
    python paper/shots/master.py          # from the 1080 frames
    python paper/shots/master.py 4k       # from paper/build/*_frames_4k
Writes paper/out/unmute_master_<res>.mp4 and a WAV of the soundtrack.
"""

import os
import subprocess
import sys

import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
BUILD = "paper/build"
FPS_UNIQUE = 12
# scene, transition into the next, its length
SCENES = [("d01", "fade", 0.5), ("d04", "fade", 0.3), ("d05", "fade", 0.3),
          ("d06", "fadeblack", 0.6), ("d07", "fade", 0.4), ("d08", None, 0)]


def run(args):
    subprocess.run([FF, "-y", "-loglevel", "error"] + args, check=True)


def main():
    tag = sys.argv[1] if len(sys.argv) > 1 else "1080"
    suffix = "_4k" if tag == "4k" else ""
    work = os.path.join(BUILD, f"master_{tag}")
    os.makedirs(work, exist_ok=True)

    parts, lengths = [], []
    for name, _, _ in SCENES:
        frames = os.path.join(BUILD, f"{name}_frames{suffix}")
        n = len([f for f in os.listdir(frames) if f.endswith(".png")])
        lengths.append(n / FPS_UNIQUE)
        out = os.path.join(work, f"{name}.mkv")
        run(["-framerate", str(FPS_UNIQUE), "-i", f"{frames}/f%03d.png",
             "-i", os.path.join(BUILD, f"{name}.wav"),
             "-vf", "fps=24", "-c:v", "libx264", "-crf", "0",
             "-preset", "veryfast", "-pix_fmt", "yuv444p",
             "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000",
             "-ac", "2", "-c:a", "pcm_s24le",
             "-t", f"{n / FPS_UNIQUE:.3f}", out])
        parts.append(out)
        print(f"{name}: {n} drawings, {n / FPS_UNIQUE:.1f}s", flush=True)

    args = []
    for p in parts:
        args += ["-i", p]
    v, a, graph = "[0:v]", "[0:a]", []
    t = lengths[0]
    for i in range(1, len(SCENES)):
        kind, dur = SCENES[i - 1][1], SCENES[i - 1][2]
        off = t - dur
        graph.append(f"{v}[{i}:v]xfade=transition={kind}:duration={dur}"
                     f":offset={off:.3f}[v{i}]")
        graph.append(f"{a}[{i}:a]acrossfade=d={dur}[a{i}]")
        v, a = f"[v{i}]", f"[a{i}]"
        t = off + lengths[i]
    graph.append(f"{v}format=yuv420p[vout]")
    graph.append(f"{a}loudnorm=I=-16:TP=-1.0:LRA=11,aresample=48000[aout]")

    film = f"paper/out/unmute_master_{tag}.mp4"
    wav = f"paper/out/unmute_master_{tag}.wav"
    run(args + ["-filter_complex", ";".join(graph),
                "-map", "[vout]", "-map", "[aout]",
                "-c:v", "libx264", "-crf", "12", "-preset", "slow",
                "-tune", "animation", "-profile:v", "high",
                "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart",
                film])
    run(["-i", film, "-vn", "-c:a", "pcm_s24le", wav])
    print(film, f"{t:.2f}s")


if __name__ == "__main__":
    main()
