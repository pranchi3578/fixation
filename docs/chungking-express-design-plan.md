# Chungking Express — Design Plan
### Joel Francis Jose & Sandra Binoy · Wedding · വിവാഹം
### Saturday 7 November 2026 · Ponkunnam Church, 3:30 PM · Base 11, Pala

---

## 0. The idea in one line

*Chungking Express* is built out of misses: cans that expire before anyone
eats them, two people who pass within 0.01 cm and don't turn around, a
boarding pass drawn by hand for a flight that isn't booked.

A wedding invitation is the opposite document. So we don't decorate the page
with Hong Kong — we take Wong Kar-wai's recurring devices and let the
invitation **resolve** each one. That resolution is the concept.

---

## 1. Translation table (film → invitation)

| Film | Invitation | |
|---|---|---|
| Pineapple cans stamped *expires May 1* | The date carries a rubber-stamp block: `7 November 2026`, and under it in the same face, `EXPIRES — NEVER` | **ship** |
| "At our closest, we were 0.01 cm apart" | Hero: the two names on one line, the gap closing to a hairline on scroll | **ship** |
| Faye's hand-drawn boarding pass | Save-the-date and Directions as the two stubs of a drawn pass | **ship** |
| *California Dreamin'* on loop | The existing Amen track. Muted by default, one tap, loops forever | **ship** |
| Neon read through rain-wet glass | **They already own the neon.** The proposal photographs have a real `WILL YOU MARRY ME?` sign in them — we echo *that* sign's glow, not an invented one | **ship** |
| Step-printed blur — one still figure in a smeared crowd | The headline resolves out of a three-layer smear; the hero photograph is step-printed for real (§3) | free |
| The handwritten menu board | Time, venue and dinner as a marker board rather than emoji icon rows | free |

**Restraint clause.** Five devices, not seven, and the last two cost nothing
because they are technique rather than content.

The neon line is the one that changed after seeing the photographs. We were
going to gesture at Wong Kar-wai's neon; instead the invitation uses the sign
that was actually standing in their garden. That is the difference between a
reference and a fact about them.

---

## 2. Art direction

Not a Hong Kong pastiche. The venue is Kerala — monsoon green, tungsten
bulbs on a wire, wet laterite, palms against a black sky. The photographs
already contain exactly that.

What we borrow from Wong Kar-wai is not his *place*, it is his **lighting
logic**: one warm practical source against one cool ambient, and nothing else
in the frame competing. Both photo sets obey it already — the sparklers and
the string lights are the practicals; everything else is ambient and gets
pushed out of the way.

The invitation is an evening object. It is dark, it is quiet, and it opens
once.

---

## 3. Photography

Three frames from the proposal, graded to one look. Script: `tools/grade.py`
(Pillow + numpy, reproducible from `assets/source/`). Outputs in
`assets/ce/`, all under 105 KB.

**The grade, in order:**

1. **Expose down** to 0.88 — Wong Kar-wai frames sit dark.
2. **Filmic S-curve** at 0.52, which separates without clipping the reds.
3. **Split-tone** — teal into the shadows (+38), tungsten into the highlights
   (+24 red, −36 blue).
4. **Ambient cool** — a hue-selective desaturation of the 46° band (the
   timber wall, the amber spill) at 52%, leaving skin and the dress alone.
   *This is the move that makes it read as the film:* it strips saturation
   from everything except the one red thing in the frame.
5. **Bloom** — a bright-pass at 204, blurred 30px, screened back at 40%. This
   is what sells the sparklers and the bulbs.
6. **Grain** at σ7 / 42%, then a 56% vignette.

**The black-and-white frames get a tritone instead** — night `#080D0F` →
jade `#22443E` → tungsten `#FFE9B9`, pivoting at 88 so the jade stays in the
shadows. The neon sign comes back amber rather than grey, which is the whole
point of doing it.

**The hero is step-printed for real.** Three offset copies (7 / 15 / 26px),
blurred proportionally, screened back at 50 / 28 / 15%, then masked away from
an elliptical centre so the couple holds sharp while the room around them
drags. That is Wong Kar-wai's signature done to the photograph itself rather
than faked in CSS — the CSS version stays for the headline only.

| File | Use |
|---|---|
| `assets/ce/bouquet-smear.webp` | Hero, scene 01 |
| `assets/ce/bouquet.webp` | Scene 03, behind the board at low opacity |
| `assets/ce/proposal.webp` | Scene 02, behind the date |
| `assets/ce/heart.webp` | Scene 04, the close |

Every photograph sits under a `--night` scrim at 55–70% wherever type runs
over it. No text is ever placed on an ungraded, unscrimmed frame.

---

## 4. Colour

Dark-committed. No light mode. Ratio: **70 night · 20 tungsten · 8 jade ·
2 alarm.**

```css
:root {
  --night:        #0B0F10;   /* base            */
  --night-2:      #141A1B;   /* raised card     */
  --night-3:      #1D2526;   /* hairlines       */

  --tungsten:     #E8A33D;   /* the source      */
  --tungsten-soft:#F3D9A8;   /* body text       */

  --jade:         #1F5F52;   /* ambient         */
  --rain:         #7E979B;   /* secondary text  */

  --alarm:        #D8412F;   /* twice, no more  */

  --paper:        #EFE9DD;   /* the pass        */
  --paper-ink:    #171513;
}
```

**Contrast, checked:**
- `--tungsten-soft` on `--night` → **12.4:1** (body)
- `--tungsten` on `--night` → **8.6:1** (any size)
- `--rain` on `--night` → **6.9:1** (meta ≥ 14px)
- `--alarm` on `--night` → **4.6:1** — **display only, ≥ 20px, never body.**

`--alarm` appears exactly twice on the whole invitation: the expiry stamp and
the cover seal. It is also the dress, which is why the palette works with the
photographs rather than against them.

---

## 5. Typography

Three faces. Not four.

| Role | Face | Notes |
|---|---|---|
| Names, display | **Cormorant Garamond** 300/400 | already loaded. Never bold. |
| Labels, stamps, subtitles | **IBM Plex Mono** 400 | the strongest reference in the piece — the film's subtitles and the can stamps both read mechanical. Uppercase, `+0.18em`, 11–12px. |
| Malayalam | **Noto Serif Malayalam** 400/600 | വിവാഹം, ആമേൻ. Always `lang="ml"`. |

One handwriting moment only, on the boarding pass, and it is a drawn SVG path
rather than a script font so it can ink itself in.

```css
--t-display-1: clamp(2.4rem, 11vw, 4.4rem);
--t-display-2: clamp(1.5rem, 6.5vw, 2.4rem);
--t-body:      clamp(1rem, 4.2vw, 1.125rem);   /* never below 16px */
--t-stamp:     0.6875rem;                       /* mono, +0.18em    */
```

Line length 34ch on phones, 52ch on desktop. Body leading 1.7, display 1.05,
`text-wrap: balance` on the names.

---

## 6. Structure — cover + four scenes

**0 · Cover.** Keep the existing tap-to-open ritual; it works and it earns the
audio gesture. A mono line types in, then the seal. The tap is a shutter.

**1 · 0.01 cm.** The step-printed hero frame. The names land sharp over it,
the gap between them closing.

**2 · The date, stamped.** Over the proposal frame. The scratch card becomes a
peel — same interaction, better story. Under it: the date, and the stamp that
says it doesn't expire.

**3 · The board.** Names, parents, Nuptial Mass, reception. This is the scene
a grandparent has to read at arm's length. No cleverness here — the
photograph drops to 12% behind it.

**4 · The pass, then ആമേൻ.** Save-the-date and Directions as the two stubs.
Then the close, over the heart frame.

---

## 7. Motion

`transform` and `opacity` only. Nothing animates layout.

- **Step-print (headline).** Three copies at opacity .55 / .28 / .14, offset
  7 / 15 / 24px, blurred 2 / 5 / 9px, resolving to zero over **900ms** on
  `cubic-bezier(.16,1,.3,1)`.
- **The 0.01 cm.** `translateX` on each name from ±14px to ±0.5px over 700ms,
  on scroll entry.
- **Neon flicker.** The one echo of their sign: a two-frame `text-shadow`
  stutter on the cover word, 90ms, **once on load only** — never looping. A
  looping flicker is a novelty; a single stutter is a light warming up.
- **Ink-in.** Boarding-pass handwriting via `stroke-dashoffset`, 1.2s, once.
- Everything else **≤ 400ms**. Under `prefers-reduced-motion` every animation
  collapses to a 120ms fade and the page stays complete.

---

## 8. Mobile

Design width **360px**; verify at 320.

- `100dvh`, never `100vh` — this repo already paid for that lesson in
  `ebf6ee4 Fix iOS Safari scroll stuck issue`.
- One gutter on the wrapper: `padding-inline: 20px`, vertical space via
  `padding-block` — never a `padding` shorthand that zeroes the sides.
- Tap targets ≥ 44×44px. Below 380px the two buttons stack full-width.
- Photographs: `object-fit: cover` with an explicit `aspect-ratio`, and an
  art-directed crop at ≤ 480px so the couple stays centred when the frame
  goes tall. Ship a 900px and a 1500px source in a `srcset`.
- Peel canvas: sized to `devicePixelRatio`, **Pointer Events only** — the
  current mouse-plus-touch double binding is where the double-fire bugs live.
  `touch-action: none` on the canvas alone, not an ancestor.
- No horizontal scroll anywhere. The boarding pass is the one element allowed
  its own `overflow-x` container.
- `env(safe-area-inset-bottom)` on the fixed sound toggle.

---

## 9. Weight

Budget **≤ 400 KB before first paint**, audio excluded. The four graded
frames total **~348 KB** at 1500px, so they fit — but only the hero is
eager; the rest are `loading="lazy"`.

What the repo still carries:

| Asset | Size | |
|---|---|---|
| `song.mp3` | 10.5 MB | byte-identical duplicate |
| `Amen - … .mp3` | 10.5 MB | byte-identical duplicate |
| `song_trimmed.mp3` | 4.0 MB | the one actually in use |
| `church/hands/hillside/window.png` | ~4.0 MB | superseded by the real photographs |

Delete the duplicate track, load the trimmed one lazily on the first user
gesture (it cannot autoplay anyway), and drop the stock PNGs now that there
are real frames. That takes the repo from ~29 MB to roughly 1 MB.

---

## 10. Accessibility

- Audio off by default, one labelled toggle with `aria-pressed`.
- The date is never hostage to an interaction: present in the DOM from the
  start, peel auto-completes after 6s, skipped under reduced motion.
- Every photograph gets real alt text describing the moment, not "image".
- Malayalam runs carry `lang="ml"`; the page is `lang="en"`.
- The current `🕡` / `📍` rows become text labels, or are `aria-hidden`.
- Every scene readable with animation disabled.

---

## 11. What we are not doing

Literal Hong Kong signage · cigarette smoke · a blonde wig · Cantonese text ·
a film-grain *video* overlay · a second script font · a looping neon flicker ·
a countdown that ticks seconds (a ticking clock is a deadline, and the whole
argument is that there is no expiry date) · anything that makes the church
address harder to read than it is on paper.

---

## 12. Build

New files, so v4 stays live and the two are A/B-able.

| Phase | Deliverable |
|---|---|
| **P0** | The grade — `tools/grade.py`, `assets/ce/` · **done** |
| **P1** | `styles_ce.css` — tokens, type scale, reset, reduced-motion block · **done** |
| **P2** | `index_ce.html` — full markup and copy, readable with zero JS · **done** |
| **P3** | Step-print hero and the 0.01 cm close — CSS only · **done** |
| **P4** | `script_ce.js` — peel canvas, audio gesture, scene reveals · **done** |
| **P5** | Boarding-pass line and the ink-in · **done** |
| **P6** | Asset triage, OG card from `bouquet.webp`, real-device iOS Safari pass |

**GSAP is gone.** The reveals and the 0.01 cm close run on
`IntersectionObserver`; the ink-in is a `stroke-dashoffset` transition. That
removes two CDN scripts from the critical path and one more thing that can
fail offline. The page is fully readable with `script_ce.js` deleted.

---

## 13. Copy deck

> **Cover** — `TAP TO OPEN`
>
> **Hero** — Joel · Sandra
> `AT OUR CLOSEST, WE WERE 0.01 CM APART`
>
> **Date** — `7 NOVEMBER 2026` / `EXPIRES — NEVER`
>
> **The board** —
> വിവാഹം · Wedding
> Joel Francis Jose — son of T.C. Joseph & Tessy Mol Mathew
> Sandra Binoy — daughter of Binoy Abraham & Ranju Binoy
> Nuptial Mass — Ponkunnam Church, 3:30 PM
> Reception — Base 11, Pala
>
> **The pass** — `PONKUNNAM · 15:30 · SEAT: YOURS`
> `BASE 11 · PALA · DINNER TO FOLLOW`
>
> **Close** — ആമേൻ / *Amen.* / "So be it."
