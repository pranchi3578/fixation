#!/usr/bin/env python3
"""
Trim a full track down to a loop for the invitation.

A page loop is not a fade-out — it comes round every minute or so, and any
seam gets noticed on the third pass. So this cuts on the beat grid and
crossfades the tail back over the head, which makes the join inaudible
rather than merely quiet.

Usage:  python3 tools/trim_track.py <source.mp3> [seconds]
Output: assets/audio/wedding.mp3   (mono, 128 kbps)
"""

import io
import os
import subprocess
import sys
import wave

import numpy as np
import imageio_ffmpeg

SR = 44100
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def decode(path):
    raw = subprocess.run(
        [FFMPEG, "-v", "quiet", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "wav", "-"],
        capture_output=True).stdout
    w = wave.open(io.BytesIO(raw))
    return np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32) / 32768


def onset_envelope(x, hop=512, win=2048):
    """Spectral flux: how much new energy appears frame to frame."""
    frames = 1 + (len(x) - win) // hop
    mag = np.empty((frames, win // 2 + 1), dtype=np.float32)
    window = np.hanning(win).astype(np.float32)
    for i in range(frames):
        seg = x[i * hop:i * hop + win] * window
        mag[i] = np.abs(np.fft.rfft(seg))
    flux = np.diff(mag, axis=0)
    flux[flux < 0] = 0                      # only rises count as onsets
    env = flux.sum(axis=1)
    return env / (env.max() + 1e-9)


def estimate_bpm(env, hop=512, lo=60, hi=110):
    """Autocorrelate the onset envelope and read the strongest period."""
    env = env - env.mean()
    ac = np.correlate(env, env, mode="full")[len(env) - 1:]
    fps = SR / hop
    lag_lo, lag_hi = int(fps * 60 / hi), int(fps * 60 / lo)
    lag = lag_lo + int(np.argmax(ac[lag_lo:lag_hi]))
    return 60.0 * fps / lag


def main():
    src = sys.argv[1]
    want = float(sys.argv[2]) if len(sys.argv) > 2 else 82.0

    x = decode(src)
    print(f"  source        {len(x)/SR:.1f}s")

    env = onset_envelope(x)
    bpm = estimate_bpm(env)
    beat = 60.0 / bpm
    bar = beat * 4
    print(f"  tempo         {bpm:.1f} BPM  ·  bar {bar:.2f}s")

    # Where the track settles: first point holding above half the median
    # energy for a full bar.
    hop = 512
    rms = np.sqrt(np.convolve(x ** 2, np.ones(hop) / hop, mode="same"))
    thresh = np.median(rms) * 0.5
    run = int(bar * SR)
    start = 0
    for i in range(0, len(rms) - run, hop):
        if np.all(rms[i:i + run] > thresh):
            start = i
            break
    # Snap to the bar grid so the loop starts on a downbeat.
    start = int(round(start / (bar * SR)) * bar * SR)
    print(f"  enters at     {start/SR:.1f}s")

    bars = max(4, int(round(want / bar)))
    length = int(bars * bar * SR)
    cross = int(min(2.2, bar) * SR)         # crossfade region

    if start + length + cross > len(x):
        start = max(0, len(x) - length - cross)

    seg = x[start:start + length + cross].copy()

    # Fold the tail back over the head with equal-power curves, so the
    # loop point is a continuous mix rather than a cut.
    t = np.linspace(0, 1, cross, dtype=np.float32)
    head, tail = seg[:cross].copy(), seg[length:length + cross]
    seg = seg[:length]
    seg[:cross] = head * np.sqrt(t) + tail * np.sqrt(1 - t)

    peak = np.max(np.abs(seg))
    seg = seg / peak * 0.85
    rms_db = 20 * np.log10(np.sqrt(np.mean(seg ** 2)))
    print(f"  loop          {bars} bars · {length/SR:.1f}s · peak -1.4 dBFS · rms {rms_db:.1f} dBFS")

    tmp = "/tmp/trim.wav"
    with wave.open(tmp, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((seg * 32767).astype("<i2").tobytes())

    os.makedirs("assets/audio", exist_ok=True)
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", tmp,
                    "-ac", "1", "-b:a", "128k", "assets/audio/wedding.mp3"], check=True)
    os.remove(tmp)
    size = os.path.getsize("assets/audio/wedding.mp3") / 1024
    print(f"  wrote         assets/audio/wedding.mp3  {size:.0f} KB")


if __name__ == "__main__":
    main()
