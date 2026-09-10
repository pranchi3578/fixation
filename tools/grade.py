#!/usr/bin/env python3
"""
Chungking Express grade for the wedding invitation stills.

Wong Kar-wai's look is not a filter, it is a lighting decision: one warm
practical source against one cool ambient, with everything between them
crushed. We reproduce that with a split-tone (teal shadows / tungsten
highlights), a bright-pass bloom so the sparklers and string lights halate
the way they do on film stock, fine grain, and a vignette that keeps the
frame's corners in the dark.

The black-and-white proposal frames get a tritone instead — night, jade,
tungsten — so the neon sign reads amber rather than grey.

Usage:  python3 tools/grade.py
Inputs: assets/source/*.jpg   Outputs: assets/ce/*.webp
"""

import numpy as np
from PIL import Image, ImageOps, ImageFilter, ImageChops, ImageDraw, ImageEnhance

# ── palette (matches docs/chungking-express-design-plan.md §3) ──────────
NIGHT_TINT = (8, 13, 15)
JADE_TINT = (34, 68, 62)
CREAM_TINT = (255, 233, 185)


def _lut(fn):
    return [max(0, min(255, int(fn(i)))) for i in range(256)]


def expose(im, stops=0.88):
    """Pull the frame down before grading — WKW frames sit dark."""
    return im.point(_lut(lambda x: x * stops) * 3)


def split_tone(im, shadow_teal=38.0, highlight_warm=24.0, cool_high=36.0):
    """Teal into the shadows, tungsten into the highlights."""
    r, g, b = im.split()
    r = r.point(_lut(lambda x: x + highlight_warm * (x / 255) ** 2))
    g = g.point(_lut(lambda x: x + shadow_teal * 0.55 * (1 - x / 255) ** 2))
    b = b.point(_lut(lambda x: x + shadow_teal * (1 - x / 255) ** 2
                              - cool_high * (x / 255) ** 2.2))
    return Image.merge("RGB", (r, g, b))


def s_curve(im, amount=0.52):
    """Filmic contrast — lifts the separation without clipping the reds."""
    def f(x):
        t = x / 255.0
        return 255 * (t + amount * (t * t * (3 - 2 * t) - t))
    lut = _lut(f)
    return im.point(lut * 3)


def cool_ambient(im, center=46.0, width=30.0, desat=0.52, cool=10.0):
    """
    Wong Kar-wai never lets the ambient compete with the practical light.
    Here the warm room — the timber wall, the amber spill — is pulled toward
    neutral so the one saturated thing left in frame is the red. Skin and the
    dress sit below the band and are untouched.
    """
    hsv = np.asarray(im.convert("HSV"), dtype=np.float32)
    h = hsv[..., 0] * (360.0 / 255.0)
    band = np.exp(-((h - center) ** 2) / (2 * width ** 2))
    hsv[..., 1] *= (1.0 - desat * band)
    out = Image.fromarray(hsv.astype(np.uint8), "HSV").convert("RGB")

    rgb = np.asarray(out, dtype=np.float32)
    rgb[..., 2] = np.clip(rgb[..., 2] + cool * band, 0, 255)
    rgb[..., 0] = np.clip(rgb[..., 0] - cool * 0.6 * band, 0, 255)
    return Image.fromarray(rgb.astype(np.uint8), "RGB")


def bloom(im, threshold=204, radius=30, strength=0.40):
    """Bright-pass halation. This is what sells the sparklers."""
    bright = im.point(_lut(lambda x: 0 if x < threshold
                           else (x - threshold) * (255 / (255 - threshold))) * 3)
    bright = bright.filter(ImageFilter.GaussianBlur(radius))
    bright = bright.point(_lut(lambda x: x * strength) * 3)
    return ImageChops.screen(im, bright)


def grain(im, sigma=7.0, opacity=0.42):
    noise = Image.effect_noise(im.size, sigma).convert("RGB")
    return Image.blend(im, ImageChops.overlay(im, noise), opacity)


def vignette(im, strength=0.56):
    w, h = im.size
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    inset_x, inset_y = int(w * 0.10), int(h * 0.06)
    d.ellipse([-inset_x, -inset_y, w + inset_x, h + inset_y], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(min(w, h) * 0.16))
    dark = im.point(_lut(lambda x: x * (1 - strength)) * 3)
    return Image.composite(im, dark, mask)


def tritone(gray, black=NIGHT_TINT, mid=JADE_TINT, white=CREAM_TINT, pivot=88):
    """Map a monochrome frame onto night → jade → tungsten."""
    def channel(i):
        lo, md, hi = black[i], mid[i], white[i]
        def f(x):
            if x <= pivot:
                return lo + (md - lo) * (x / pivot)
            return md + (hi - md) * ((x - pivot) / (255 - pivot))
        return _lut(f)
    r, g, b = (gray.point(channel(i)) for i in range(3))
    return Image.merge("RGB", (r, g, b))


def step_print(im, layers=((26, 0.15), (15, 0.28), (7, 0.50)), keep=0.40):
    """
    Wong Kar-wai's step-printing: the frame smears, one thing stays sharp.
    Offset copies are blurred and screened back in, then masked away from
    the centre so the couple holds while the room around them drags.
    """
    w, h = im.size
    smear = im.copy()
    for dx, alpha in layers:
        ghost = ImageChops.offset(im, dx, 0).filter(ImageFilter.GaussianBlur(dx / 3.2))
        smear = Image.blend(smear, ghost, alpha)

    mask = Image.new("L", (w, h), 255)
    d = ImageDraw.Draw(mask)
    rx, ry = int(w * keep), int(h * keep * 1.35)
    d.ellipse([w // 2 - rx, h // 2 - ry, w // 2 + rx, h // 2 + ry], fill=0)
    mask = mask.filter(ImageFilter.GaussianBlur(min(w, h) * 0.10))
    return Image.composite(smear, im, mask)


def fit(im, width, box=None):
    if box:
        im = im.crop(box)
    width = min(width, im.width)
    ratio = width / im.width
    return im.resize((width, max(1, int(im.height * ratio))), Image.LANCZOS)


def save(im, path, quality=78):
    im.save(path, "WEBP", quality=quality, method=6)
    import os
    print(f"  {path:34s} {im.width}x{im.height}  {os.path.getsize(path)/1024:6.1f} KB")


def main():
    print("colour frame — the bouquet")
    src = Image.open("assets/source/bouquet.jpg").convert("RGB")
    g = cool_ambient(split_tone(s_curve(expose(src))))
    g = ImageEnhance.Color(g).enhance(1.38)      # the red dress is the subject
    g = vignette(grain(bloom(g)))
    save(fit(g, 1500), "assets/ce/bouquet.webp")
    save(fit(step_print(g), 1500), "assets/ce/bouquet-smear.webp")

    print("night frames — the proposal")
    for name, keep_box in (("proposal", None), ("heart", None)):
        s = Image.open(f"assets/source/{name}.jpg").convert("L")
        s = ImageOps.autocontrast(s, cutoff=(0.4, 0.6))
        t = s_curve(tritone(s), amount=0.34)
        t = ImageEnhance.Color(t).enhance(1.10)
        t = vignette(grain(bloom(t, threshold=190, radius=34, strength=0.58),
                           opacity=0.44), strength=0.62)
        save(fit(t, 1500), f"assets/ce/{name}.webp")


if __name__ == "__main__":
    main()
