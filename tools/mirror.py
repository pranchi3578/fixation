#!/usr/bin/env python3
"""Write sandra.html from wedding.html, with Sandra's name first.

Two invitations, one for each side of the family, and the only difference
is the order of the names. That is not a thing to maintain twice: edit
wedding.html and run this, and the other one follows.

The swaps are named and counted rather than done with a blanket
find-and-replace, because the wishes address Joel and Sandra by name —
"Joel, welcome to the family" — and a page that swapped those would be
worse than one that swapped nothing. If a swap stops matching, this fails
loudly instead of quietly shipping half a mirror.
"""

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "wedding.html"
OUT = ROOT / "sandra.html"

# (what to find, what to put in its place, how many times it must appear)
SWAPS = [
    # the head
    ("<title>Joel &amp; Sandra</title>", "<title>Sandra &amp; Joel</title>", 1),
    ("Joel Francis Jose and Sandra Binoy invite you",
     "Sandra Binoy and Joel Francis Jose invite you", 1),
    ('content="Joel &amp; Sandra"', 'content="Sandra &amp; Joel"', 2),
    ("Joel and Sandra together beneath", "Sandra and Joel together beneath", 2),
    ("fixation/wedding.html", "fixation/sandra.html", 1),

    # the calendar entry, which wedding.js reads off the body
    ('data-couple="Joel &amp; Sandra"', 'data-couple="Sandra &amp; Joel"', 1),

    # the envelope, the card in it, the header, the footer
    ("Joel<span class=\"amp\">&amp;</span>Sandra",
     "Sandra<span class=\"amp\">&amp;</span>Joel", 2),
    (">Joel &amp; Sandra<", ">Sandra &amp; Joel<", 1),
    ("Joel &amp; Sandra &middot;", "Sandra &amp; Joel &middot;", 1),

    # the cover
    ("          <span>Joel</span>\n", "          <span>Sandra</span>\n", 1),
    ("          <span>Sandra</span>\n        </h1>", "          <span>Joel</span>\n        </h1>", 1),

    # the last photograph
    ("Joel and Sandra standing together", "Sandra and Joel standing together", 1),
]

# The families block, swapped whole: name, parents and house all travel
# together, so this is a move rather than a substitution.
FAMILY_ONE = """        <div class="family">
          <p class="who">Joel Francis Jose</p>
          <p class="meta meta--ink">Son of<br>T.C. Joseph &amp; Tessy Mol Mathew<br>Thekkumkattil</p>
        </div>"""
FAMILY_TWO = """        <div class="family">
          <p class="who">Sandra Binoy</p>
          <p class="meta meta--ink">Daughter of<br>Binoy Abraham &amp; Ranju Binoy<br>Anchanickal</p>
        </div>"""


def main() -> int:
    html = SRC.read_text()
    problems = []

    both = FAMILY_ONE + '\n        <span class="amp" aria-hidden="true">&amp;</span>\n' + FAMILY_TWO
    if both not in html:
        problems.append("the families block")
    else:
        html = html.replace(
            both,
            FAMILY_TWO + '\n        <span class="amp" aria-hidden="true">&amp;</span>\n' + FAMILY_ONE,
            1,
        )

    for find, put, times in SWAPS:
        found = html.count(find)
        if found != times:
            problems.append("%r: expected %d, found %d" % (find[:48], times, found))
            continue
        html = html.replace(find, put, times)

    if problems:
        print("mirror.py: wedding.html has moved under this script.", file=sys.stderr)
        for p in problems:
            print("  - " + p, file=sys.stderr)
        return 1

    note = ("<!-- Written by tools/mirror.py from wedding.html. Do not edit this\n"
            "     file: edit wedding.html and run the script. -->\n")
    OUT.write_text(note + html)
    print("wrote %s (%d bytes)" % (OUT.name, OUT.stat().st_size))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
