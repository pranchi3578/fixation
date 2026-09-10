#!/usr/bin/env python3
"""
Bright grade for the wedding invitation.

The page is white, so the photographs have to sit on white without punching
holes in it. Two rules do most of the work:

  1. Nothing reaches pure black. A matte black point (18-26/255) is what
     makes a photograph look printed rather than pasted onto the page.
  2. Colour is spent once. The colour frame is desaturated until only the
     dress still reads, so it agrees with the claret accent instead of
     competing with it.

The two night frames cannot become daylight — what they can become is a
clean, lifted monochrome that reads as a silver print on a white sheet.

Usage:  python3 tools/grade_light.py
Inputs: assets/source/*.jpg      Outputs: assets/photo/*.webp
"""

import os
from PIL import Image, ImageOps, ImageEnhance, ImageFilter


def _lut(fn):
    return [max(0, min(255, int(fn(i)))) for i in range(256)]


def lift(im, black=20, white=252):
    """Matte the blacks and hold the whites just below paper."""
    span = white - black
    return im.point(_lut(lambda x: black + x * span / 255.0) * len(im.getbands()))


def soften(im, amount=0.18):
    """A gentle inverse S — less contrast, more air. The opposite of a
    filmic curve: midtones open up instead of compressing."""
    def f(x):
        t = x / 255.0
        return 255 * (t - amount * (t * t * (3 - 2 * t) - t))
    return im.point(_lut(f) * len(im.getbands()))


def clean_highlights(im, knee=196, gain=1.06):
    """Bring the near-whites up so the frame meets the page cleanly."""
    def f(x):
        return x if x < knee else knee + (x - knee) * gain
    return im.point(_lut(f) * len(im.getbands()))


def warm(im, r=1.012, g=1.004, b=0.988):
    """A breath of warmth. Any more and it turns cream."""
    ch = im.split()
    return Image.merge("RGB", (
        ch[0].point(_lut(lambda x: x * r)),
        ch[1].point(_lut(lambda x: x * g)),
        ch[2].point(_lut(lambda x: x * b)),
    ))


def mono(im, tone=(1.006, 1.000, 0.992)):
    """Neutral monochrome with the faintest warm tone — a pure neutral
    reads clinical next to warm white paper."""
    g = ImageOps.grayscale(im)
    g = ImageOps.autocontrast(g, cutoff=(0.5, 0.3))
    rgb = Image.merge("RGB", (g, g, g))
    return warm(rgb, *tone)


def crop_to(im, ratio, cx=0.5, cy=0.5):
    w, h = im.size
    tw, th = w, int(w / ratio)
    if th > h:
        th, tw = h, int(h * ratio)
    left = max(0, min(w - tw, int(w * cx - tw / 2)))
    top = max(0, min(h - th, int(h * cy - th / 2)))
    return im.crop((left, top, left + tw, top + th))


def save(im, name, width, quality=82):
    if im.width > width:
        im = im.resize((width, int(im.height * width / im.width)), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.1, percent=42, threshold=3))
    path = f"assets/photo/{name}.webp"
    im.save(path, "WEBP", quality=quality, method=6)
    print(f"  {path:32s} {im.width}x{im.height}  {os.path.getsize(path)/1024:6.1f} KB")
    return im


def main():
    print("hero — colour, high key")
    src = Image.open("assets/source/bouquet.jpg").convert("RGB")
    g = warm(clean_highlights(soften(lift(src, black=22, white=253))))
    g = ImageEnhance.Color(g).enhance(0.58)     # only the dress survives
    hero = crop_to(g, 4 / 5, cx=0.525, cy=0.46)
    save(hero, "hero", 1200)
    save(crop_to(g, 3 / 2, cx=0.525, cy=0.44), "hero-wide", 1400)
    save(crop_to(g, 3 / 2, cx=0.525, cy=0.44), "og", 1200, quality=84)

    print("plates — monochrome, matte")
    for src_name, out, cx in (("proposal", "plate-1", 0.58), ("heart", "plate-2", 0.58)):
        s = Image.open(f"assets/source/{src_name}.jpg").convert("RGB")
        m = clean_highlights(soften(lift(mono(s), black=26, white=250), amount=0.10))
        save(crop_to(m, 4 / 5, cx=cx, cy=0.52), out, 1000)

    print("band — wide monochrome, for white type over it")
    s = Image.open("assets/source/proposal.jpg").convert("RGB")
    m = clean_highlights(soften(lift(mono(s), black=24, white=248), amount=0.08))
    save(crop_to(m, 16 / 9, cx=0.54, cy=0.46), "band", 1600)


if __name__ == "__main__":
    main()
