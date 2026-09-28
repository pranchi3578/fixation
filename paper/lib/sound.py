"""
Sound, synthesised: paper, a ceiling fan, and the four-note motif.

Nothing is sampled. Paper is shaped noise plus crackle (tiny random
impulses) -- the crackle is what makes it paper rather than wind. The motif
is four plucked notes: the first three rise like a question, the last one
lands. It is the brand's sound, so every film ends on it.

All times are seconds; everything mixes into one mono buffer at SR.
"""

import wave

import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000
MOTIF = [(69, 0.0), (74, 0.22), (76, 0.44), (74, 0.9)]   # A4 D5 E5 . D5


def _t(dur):
    return np.arange(int(dur * SR)) / SR


def _band(x, lo, hi, order=2):
    sos = butter(order, [lo, hi], btype="band", fs=SR, output="sos")
    return sosfilt(sos, x)


def _lp(x, hi, order=2):
    return sosfilt(butter(order, hi, btype="low", fs=SR, output="sos"), x)


class Mix:
    def __init__(self, dur, seed=7):
        self.buf = np.zeros(int(dur * SR))
        self.rng = np.random.default_rng(seed)

    def add(self, at, x, gain=1.0):
        i = int(at * SR)
        j = min(len(self.buf), i + len(x))
        if j > i:
            self.buf[i:j] += gain * x[: j - i]

    # ------------------------------------------------------------ beds --
    def fan(self, gain=0.05):
        """A ceiling fan at night: low air, turning at ~3 Hz."""
        n = len(self.buf)
        air = _lp(self.rng.normal(0, 1, n), 700)
        wob = 1 + 0.25 * np.sin(2 * np.pi * 3.1 * np.arange(n) / SR)
        hum = 0.08 * np.sin(2 * np.pi * 100 * np.arange(n) / SR)
        self.add(0, (air / np.abs(air).max() * wob + hum), gain)

    # ----------------------------------------------------------- paper --
    def rustle(self, at, dur, gain=0.3, bright=1.0):
        n = int(dur * SR)
        body = _band(self.rng.normal(0, 1, n), 1500 * bright, 7000)
        crackle = np.zeros(n)
        k = self.rng.integers(0, n, int(dur * 180))
        crackle[k] = self.rng.normal(0, 3, len(k))
        crackle = _band(crackle, 2000, 12000)
        env = np.sin(np.pi * np.linspace(0, 1, n)) ** 0.7
        env *= 0.6 + 0.4 * _lp(self.rng.random(n), 12)  # handled, uneven
        x = (0.5 * body / (np.abs(body).max() + 1e-9)
             + crackle / (np.abs(crackle).max() + 1e-9)) * env
        self.add(at, x, gain)

    def snap(self, at, gain=0.6):
        """A crease snapping flat: a click and a short bright burst."""
        n = int(0.06 * SR)
        x = self.rng.normal(0, 1, n) * np.exp(-np.arange(n) / (0.008 * SR))
        self.add(at, _band(x, 1200, 9000) * 3, gain)

    def tick(self, at, gain=0.15):
        n = int(0.015 * SR)
        x = self.rng.normal(0, 1, n) * np.exp(-np.arange(n) / (0.002 * SR))
        self.add(at, _band(x, 3000, 9000), gain)

    def whoosh(self, at, dur, gain=0.35):
        n = int(dur * SR)
        x = self.rng.normal(0, 1, n)
        out = np.zeros(n)
        step = 1024
        for s in range(0, n, step):               # the band slides upward
            f = 500 + 2500 * (s / n)
            out[s:s + step] = _band(x[s:s + step], f, f * 2.2)
        env = np.sin(np.pi * np.linspace(0, 1, n) ** 0.6) ** 2
        self.add(at, out / (np.abs(out).max() + 1e-9) * env, gain)

    def peel(self, at, dur, gain=0.4):
        """Tape leaving paper: a dense, rising crackle, sticky rather than
        crisp."""
        n = int(dur * SR)
        clicks = np.zeros(n)
        rate = np.linspace(400, 1400, n) / SR
        k = np.nonzero(self.rng.random(n) < rate)[0]
        clicks[k] = self.rng.normal(0, 1, len(k))
        x = _band(clicks, 1500, 10000)
        x += 0.3 * _band(self.rng.normal(0, 1, n), 300, 1200)
        env = np.minimum(1, np.arange(n) / (0.05 * SR)) * \
            np.minimum(1, (n - np.arange(n)) / (0.03 * SR))
        self.add(at, x / (np.abs(x).max() + 1e-9) * env, gain)

    def voice(self, at, path, gain=0.8):
        """A recorded or scratch line, resampled to SR."""
        from math import gcd

        from scipy.signal import resample_poly
        with wave.open(path) as w:
            sr = w.getframerate()
            x = np.frombuffer(w.readframes(w.getnframes()),
                              np.int16).astype(float) / 32768
        g = gcd(SR, sr)
        self.add(at, resample_poly(x, SR // g, sr // g), gain)

    def gibberish(self, at, dur, gain=0.3, rate=6.5, pitch=140,
                  rise_end=False, env=None):
        """Talking without words: a buzzy source through moving vowel
        formants, one syllable at a time. Muted trombone, not a person."""
        n = int(dur * SR)
        out = np.zeros(n)
        pos = 0
        k = 0
        while pos < n:
            syl = int(SR * self.rng.uniform(0.7, 1.3) / rate)
            if self.rng.random() < 0.12:            # breath between phrases
                pos += syl
                continue
            m = min(syl, n - pos)
            t = np.arange(m) / SR
            last = rise_end and pos + syl >= n
            f0 = pitch * self.rng.uniform(0.85, 1.2)
            glide = np.linspace(1, 1.45 if last else self.rng.uniform(0.9, 1.1),
                                m)
            ph = 2 * np.pi * np.cumsum(f0 * glide) / SR
            src = sum(np.sin(h * ph) / h for h in range(1, 14))
            f1 = self.rng.uniform(350, 800)
            f2 = self.rng.uniform(900, 2100)
            x = _band(src, f1 * 0.7, f1 * 1.3) + 0.5 * _band(src, f2 * 0.8,
                                                             f2 * 1.2)
            e = np.minimum(1, t / 0.02) * np.minimum(1, (m - np.arange(m))
                                                      / (0.04 * SR))
            out[pos:pos + m] += x * e
            pos += syl
            k += 1
        out = _lp(out, 2600)
        out /= np.abs(out).max() + 1e-9
        if env is not None:
            out *= env(np.arange(n) / SR + at)
        self.add(at, out, gain)

    def crickets(self, gain=0.02):
        """An Indian night: two crickets, not quite in step."""
        n = len(self.buf)
        t = np.arange(n) / SR
        out = np.zeros(n)
        for f, period, off in ((4400, 0.71, 0.0), (5100, 0.93, 0.31)):
            env = np.zeros(n)
            start = off
            while start < n / SR:
                for p in range(3):
                    a = int((start + p * 0.045) * SR)
                    b = min(n, a + int(0.025 * SR))
                    if a < n:
                        env[a:b] += np.hanning(max(2, b - a))[: b - a]
                start += period * self.rng.uniform(0.9, 1.1)
            out += np.sin(2 * np.pi * f * t) * env
        self.add(0, out, gain)

    def clink(self, at, gain=0.25, f=900):
        """Tin: a few inharmonic partials that die fast."""
        t = _t(0.5)
        x = sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t / d)
                for m, a, d in ((1, 1, 0.12), (2.76, 0.6, 0.07),
                                (5.4, 0.4, 0.04), (8.9, 0.25, 0.02)))
        self.add(at, x * np.minimum(1, t / 0.002), gain)

    def thud(self, at, gain=0.3):
        n = int(0.12 * SR)
        x = self.rng.normal(0, 1, n) * np.exp(-np.arange(n) / (0.02 * SR))
        self.add(at, _lp(x, 400) * 4, gain)

    # ----------------------------------------------------------- music --
    def pluck(self, at, midi, dur=1.6, gain=0.25):
        """A soft kalimba-ish pluck: few partials, fast-decaying top."""
        f = 440 * 2 ** ((midi - 69) / 12)
        t = _t(dur)
        x = np.zeros_like(t)
        for k, (mult, amp, dec) in enumerate(
                [(1, 1, 1.4), (2.0, 0.25, 0.5), (3.01, 0.12, 0.25),
                 (5.4, 0.06, 0.08)]):
            x += amp * np.sin(2 * np.pi * f * mult * t) * np.exp(-t / dec)
        x *= np.minimum(1, t / 0.004)              # no click at the onset
        self.add(at, x / 1.4, gain)

    def motif(self, at, upto=4, gain=0.25):
        for midi, dt in MOTIF[:upto]:
            self.pluck(at + dt, midi, gain=gain)

    # ----------------------------------------------------------- write --
    def write(self, path, peak_db=-3.0):
        x = self.buf / (np.abs(self.buf).max() + 1e-9) * 10 ** (peak_db / 20)
        with wave.open(path, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((x * 32767).astype(np.int16).tobytes())
        return path
