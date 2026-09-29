#!/usr/bin/env python3
"""The one photograph on the letter, in black and white.

A printed letter has no backlight to carry a colour image, and one
monochrome frame on warm paper is the whole look. This reuses the grading
in grade_light.py — matte blacks, an open midtone, the faintest warm tone
— and cuts a panoramic band rather than a full frame, because a band
belongs to a sheet of stationery in a way a photograph pasted at the top
does not.

Usage:  python3 tools/letter_photo.py
Input:  assets/source/bouquet.jpg      Output: assets/photo/letter.webp
"""

from PIL import Image

from grade_light import clean_highlights, crop_to, lift, mono, save, soften


def main():
    src = Image.open("assets/source/bouquet.jpg").convert("RGB")
    m = clean_highlights(soften(lift(mono(src), black=28, white=249), amount=0.10))
    # The left fifth of the frame is sparklers and empty wall. Dropping it
    # first puts the two of them on the sheet's centre line, which a formal
    # letter wants, and keeps the arch around them.
    m = m.crop((int(m.width * 0.19), 0, m.width, m.height))
    save(crop_to(m, 2.4, cx=0.52, cy=0.44), "letter", 1400)


if __name__ == "__main__":
    main()
