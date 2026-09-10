#!/usr/bin/env python3
"""
An original piece for the invitation.

Written here rather than licensed, because a cleared free instrumental of a
copyrighted song does not exist — a cover clears the recording but not the
composition. This owes nothing to anyone: a I–vi–IV–V movement, which is the
common property of most of Western music, under an arpeggio with no melody
over it. Deliberately no tune: a melody competes with reading, an arpeggio
sits underneath it.

The piano is additive — twelve partials per note, the higher ones decaying
faster, with a touch of inharmonicity so the octaves are not perfectly in
tune with themselves. That imperfection is most of what separates a piano
from an organ.

Usage:  python3 tools/compose.py     Output: assets/audio/wedding.mp3
"""

import os
import subprocess
import wave

import numpy as np
import imageio_ffmpeg

SR = 44100
BPM = 66.0
BEAT = 60.0 / BPM
BAR = BEAT * 4


def hz(semitones_from_a4):
    return 440.0 * (2.0 ** (semitones_from_a4 / 12.0))


# Note names to semitone offsets from A4.
STEP = {'C': -9, 'D': -7, 'E': -5, 'F': -4, 'G': -2, 'A': 0, 'B': 2}


def pitch(name):
    letter, rest = name[0], name[1:]
    accidental = 0
    while rest and rest[0] in '#b':
        accidental += 1 if rest[0] == '#' else -1
        rest = rest[1:]
    octave = int(rest)
    return hz(STEP[letter] + accidental + (octave - 4) * 12)


def note(freq, dur, amp=1.0, partials=12):
    """One struck string. Higher partials start louder and die sooner."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    out = np.zeros(n)

    for k in range(1, partials + 1):
        # Slight stretch: real strings are stiff, so overtones run sharp.
        f = freq * k * (1.0 + 0.0007 * k * k)
        if f > SR * 0.45:
            break
        weight = 1.0 / (k ** 1.35)
        decay = 1.6 + 0.55 * k
        out += weight * np.sin(2 * np.pi * f * t + np.random.rand() * 6.28) * np.exp(-decay * t)

    # A soft hammer, not a click.
    attack = 1.0 - np.exp(-t / 0.006)
    body = np.exp(-1.1 * t)
    return out * attack * body * amp


def reverb(x, seconds=1.9, mix=0.34):
    """A dark room. Exponentially decaying noise, low-passed, FFT-convolved."""
    n = int(seconds * SR)
    ir = np.random.randn(n) * np.exp(-4.2 * np.arange(n) / SR)
    # Roll the highs off so it reads as a room and not as hiss.
    kernel = np.ones(28) / 28.0
    ir = np.convolve(ir, kernel, mode='same')
    ir[0] = 1.0

    size = 1
    while size < len(x) + n:
        size *= 2
    wet = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size))[:len(x) + n]
    wet /= (np.max(np.abs(wet)) + 1e-9)

    out = np.zeros(len(x) + n)
    out[:len(x)] += x * (1 - mix)
    out += wet * mix
    return out


def main():
    np.random.seed(7)

    # I – vi – IV – V in F, four bars, played four times.
    chords = [
        ['F2', 'F3', 'A3', 'C4', 'F4'],
        ['D2', 'D3', 'F3', 'A3', 'D4'],
        ['Bb1', 'Bb2', 'D3', 'F3', 'Bb3'],
        ['C2', 'C3', 'E3', 'G3', 'C4'],
    ]

    bars = 16
    total = int(bars * BAR * SR) + SR
    track = np.zeros(total)

    for bar in range(bars):
        chord = chords[bar % 4]
        # Eighth notes, rocking up and back down the chord.
        order = [0, 1, 2, 3, 4, 3, 2, 1]
        for i, step in enumerate(order):
            at = int((bar * BAR + i * BEAT / 2) * SR)
            # The bass note on the beat is fuller; the rest sit back.
            amp = 0.52 if i == 0 else 0.30 if i % 2 == 0 else 0.22
            # Ease off in the last bar so the loop can breathe.
            if bar == bars - 1:
                amp *= 0.75
            n = note(pitch(chord[step]), 3.4, amp)
            end = min(at + len(n), total)
            track[at:end] += n[:end - at]

    track = reverb(track)

    # Wrap the tail into the head so the loop has no seam.
    tail = int(1.6 * SR)
    body = int(bars * BAR * SR)
    loop = track[:body].copy()
    over = track[body:body + tail]
    loop[:len(over)] += over

    # Two seconds in, one out, so a tap on the button is never abrupt.
    fade_in = int(1.8 * SR)
    loop[:fade_in] *= np.linspace(0, 1, fade_in) ** 1.6

    peak = np.max(np.abs(loop))
    loop = loop / peak * 0.72
    rms = np.sqrt(np.mean(loop ** 2))
    print(f"  {len(loop)/SR:.1f}s · peak {20*np.log10(0.72):.1f} dBFS · rms {20*np.log10(rms):.1f} dBFS")

    os.makedirs("assets/audio", exist_ok=True)
    tmp = "/tmp/compose.wav"
    with wave.open(tmp, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((loop * 32767).astype("<i2").tobytes())

    exe = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([exe, "-y", "-loglevel", "error", "-i", tmp,
                    "-ac", "1", "-b:a", "128k", "assets/audio/wedding.mp3"], check=True)
    os.remove(tmp)
    print(f"  assets/audio/wedding.mp3  {os.path.getsize('assets/audio/wedding.mp3')/1024:.0f} KB")


if __name__ == "__main__":
    main()
