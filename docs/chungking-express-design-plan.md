# Chungking Express — Design Plan
### Joel Francis Jose & Sandra Binoy · Fixation / ഉറപ്പീരു · 23 · 05 · 26

---

## 0. The idea in one line

*Chungking Express* is a film about near-misses that almost become meetings.
A wedding invitation is the one document where the near-miss finally lands.

So we don't decorate the page with Hong Kong. We take Wong Kar-wai's four
recurring devices — **the expiry date, the 0.01 cm, the hand-drawn boarding
pass, the song on repeat** — and let the invitation *resolve* each one.
That resolution is the whole concept. Everything below serves it.

---

## 1. Translation table (film → invitation)

| Film | On the invitation |
|---|---|
| Pineapple cans stamped *expires May 1* | The date card carries a rubber-stamp block: `23 · 05 · 26` and under it, in the same stamp face, `EXPIRES — NEVER` |
| "At our closest, we were 0.01 cm apart" | Hero: `Joel` and `Sandra` set on one line with a measured gap that closes to a hairline as you scroll in |
| Faye's hand-drawn boarding pass | Directions + Save-the-date presented as a hand-drawn pass: **KANJIRAPPALLY · 18:30 · SEAT: YOURS** |
| *California Dreamin'* on loop at the Midnight Express | The existing Amen track, muted by default, one tap, loops forever |
| Step-printed blur — one still figure in a smeared crowd | Hero headline resolves out of a 3-layer motion smear; the names land razor-sharp |
| The handwritten menu board | Time / venue / dinner set as a marker-on-board list, not as icon rows |
| Neon read through rain-wet glass | An ambient two-source colour wash. Never a literal neon sign. |

**Restraint clause.** Ship **four** of these seven. Seven is cosplay; four is
a point of view. Recommended four: *expiry stamp · 0.01 cm · boarding pass ·
song on repeat*. The step-print is a free bonus because it costs only CSS.

---

## 2. Art direction

Not a Hong Kong pastiche — the venue is **Tharavad The Farmhouse,
Kanjirappally, at 6:30 PM in May.** That is monsoon green, tungsten porch
bulbs, wet laterite, insects in the lamp cone.

What we borrow from WKW is not his *place*, it is his **lighting logic**:
one warm practical light source against one cool ambient, and nothing else
in the frame competing. Apply that logic to a Kerala evening and the film
reference reads as taste rather than costume.

The invitation is an **evening object**. It is dark, it is quiet, and it
opens once.

---

## 3. Colour

Dark-committed. No light mode — this is a night piece, and a half-hearted
light palette would dilute it. Paint every surface explicitly.

```css
:root {
  /* ground — 70% of the page */
  --night:        #0B0F10;  /* base */
  --night-2:      #141A1B;  /* raised card */
  --night-3:      #1D2526;  /* hairlines, dividers */

  /* the warm source — 20% */
  --tungsten:     #E8A33D;  /* accent, rules, the stamp ring */
  --tungsten-soft:#F3D9A8;  /* body text on night */

  /* the cool ambient — 8% */
  --jade:         #1F5F52;  /* the Midnight Express green */
  --rain:         #7E979B;  /* secondary + meta text */

  /* the single alarm — 2%, twice on the whole page */
  --alarm:        #D8412F;

  /* the one paper moment (boarding pass) */
  --paper:        #EFE9DD;
  --paper-ink:    #171513;
}
```

**Ratio discipline:** 70 night / 20 tungsten / 8 jade / 2 alarm.

**Contrast, checked:**
- `--tungsten-soft` on `--night` → **12.4:1** (body, safe)
- `--rain` on `--night` → **6.9:1** (meta ≥ 14px, safe)
- `--tungsten` on `--night` → **8.6:1** (safe at any size)
- `--alarm` on `--night` → **4.6:1** — **display only, ≥ 20px, never body copy.**

`--alarm` gets exactly two appearances: the expiry stamp, and the seal on the
cover. A third appearance kills it.

---

## 4. Typography

Three faces. Not four.

| Role | Face | Notes |
|---|---|---|
| Names, display | **Cormorant Garamond** 300/400 | already loaded; continuity with the family register. Never bold. |
| Labels, stamps, subtitles | **IBM Plex Mono** 400 | the single strongest CE cue — WKW's subtitle track and the can stamps both read mechanical. Uppercase, `letter-spacing: .18em`, 11–12px. |
| Malayalam | **Noto Serif Malayalam** 400/600 | ഉറപ്പീരു, ആമേൻ. Always `lang="ml"`. |

One handwriting moment only — the boarding pass — and it is a **drawn SVG
path**, not a script font, so it can ink itself in on entry.

**Scale (mobile-first, fluid):**

```css
--t-display-1: clamp(2.4rem, 11vw, 4.4rem);   /* the two names */
--t-display-2: clamp(1.5rem, 6.5vw, 2.4rem);  /* ഉറപ്പീരു, ആമേൻ */
--t-body:      clamp(1rem, 4.2vw, 1.125rem);  /* never below 16px */
--t-meta:      0.875rem;
--t-stamp:     0.6875rem;                      /* mono, tracked +.18em */
```

Line length capped at **34ch** on phones, **52ch** on desktop. Body leading
1.7. Display leading 1.05 with `text-wrap: balance` on the names.

---

## 5. Structure — cover + four scenes

Match the current v4 rhythm. Do not inflate it.

**0 · Cover.** Keep the existing tap-to-open ritual; it works and it earns the
audio gesture. Reskin: a mono subtitle line types in, then the seal. The tap
is a shutter — a 90ms white flash, then the hero.

**1 · Hero — 0.01 cm.** Black. The names smear in step-print and land sharp,
the gap between them closing. Under it, in mono:
`AT OUR CLOSEST, WE WERE 0.01 CM APART`.

**2 · The date, stamped.** Replaces the scratch-card metaphor with a peel —
same interaction, better story. Under the peel: `23 · 05 · 26`, and beneath
it the stamp in `--alarm`: `EXPIRES — NEVER`.

**3 · The board.** Names, parents, time, venue, dinner — set as a marker
board, left-aligned, hairline rules in `--night-3`. This is the scene that
has to be *readable by a grandparent at arm's length.* No cleverness here.

**4 · The pass.** Boarding pass in `--paper`: Save-the-date and Directions
live inside it as the two "stubs". Then the close — ആമേൻ / *Amen.* / "So be it."

---

## 6. Motion

Every effect below is `transform` + `opacity` only. Nothing animates layout.

- **Step-print.** Three copies of the headline at opacity `.55 / .28 / .14`,
  offset `6 / 13 / 21px`, blurred `2 / 5 / 9px`, all animating to zero over
  **900ms** `cubic-bezier(.16,1,.3,1)`. This is the whole WKW look and it is
  ~20 lines of CSS.
- **The 0.01 cm.** A flex `gap` — actually a `translateX` on each name — from
  `±14px` to `±0.5px` over 700ms, tied to scroll entry.
- **Rain glass.** One static grain/rain PNG at 8% opacity on a
  `position: fixed` pseudo-element. **Not** `background-attachment: fixed`
  (broken on iOS).
- **Ink-in.** The boarding-pass handwriting draws via `stroke-dashoffset`,
  1.2s, once.

Everything else: **≤ 400ms**. Two beats are allowed to be slow (the hero
smear, the ink-in); nothing else gets to make someone wait.

```css
@media (prefers-reduced-motion: reduce) {
  /* every animation collapses to a 120ms opacity fade.
     The page must be complete and readable with zero motion. */
}
```

---

## 7. Mobile responsiveness

Design width is **360px**; verify at **320px**.

- `100dvh`, never `100vh` — the repo has already paid for that lesson once
  (`ebf6ee4 Fix iOS Safari scroll stuck issue`). Re-enable scroll by removing
  the lock class, and do not leave `overscroll-behavior` clamped afterwards.
- One gutter, declared once on the page wrapper: `padding-inline: 20px`. Give
  vertical padding with `padding-block`, never a `padding` shorthand that
  quietly zeroes the sides.
- Tap targets ≥ 44×44px. Below 380px the two buttons stack full-width.
- **Scratch/peel canvas:** size to `devicePixelRatio`, use **Pointer Events**
  only (the current mouse + touch double-binding is where double-fire bugs
  live), and `touch-action: none` on the canvas alone — not on an ancestor.
- No horizontal scroll anywhere. The boarding pass is the one element that
  may sit in its own `overflow-x: auto` container.
- Fonts: `preconnect` to `fonts.gstatic.com`, `display=swap`, and subset to
  Latin + Malayalam. Three families is already the ceiling.
- Safe areas: `env(safe-area-inset-bottom)` on the fixed sound toggle.

---

## 8. Performance budget

**≤ 400 KB before first paint**, audio excluded. The repo currently ships:

- `song.mp3` **10.5 MB** and an identical `Amen - ... .mp3` **10.5 MB** — the
  duplicate is dead weight, and `song_trimmed.mp3` (4.0 MB) is the one in use.
- Four PNGs totalling ~4 MB (`church`, `hands`, `hillside`, `window`).

**First task of the build is asset triage:** delete the duplicate mp3, keep
only the trimmed track and load it lazily on the first user gesture (never
before — it also can't autoplay anyway), and convert the PNGs to WebP at
1600px max. That alone is a ~20 MB → ~1 MB repo.

GSAP + ScrollTrigger from CDN is fine; import ScrollTrigger only on the two
scenes that need it.

---

## 9. Accessibility

- Audio is **off by default**, one clearly labelled toggle, `aria-pressed`.
- The date must not be hostage to an interaction: it is present in the DOM for
  screen readers from the start, and the peel auto-completes after 6s, or is
  skipped entirely under `prefers-reduced-motion`.
- All Malayalam runs carry `lang="ml"`; the page is `lang="en"`.
- Contrast pairs are fixed in §3 — `--alarm` is display-only.
- Every scene reachable and complete with JavaScript animation disabled.
- Emoji are decorative: replace the current `🕡` / `📍` rows with real text
  labels, or mark them `aria-hidden`.

---

## 10. What we are deliberately not doing

Literal neon signage · cigarette smoke · a blonde wig · Cantonese text ·
a film-grain video overlay · a second script font · a countdown that ticks
seconds (a ticking clock is a *deadline*; this piece's whole argument is that
there is no expiry date) · anything that makes the venue address harder to
read than it is on paper.

---

## 11. Build plan

New files, so v4 stays live and the two are A/B-able:

| Phase | Deliverable |
|---|---|
| **P1** | `styles_ce.css` — tokens, type scale, reset, reduced-motion block |
| **P2** | `index_ce.html` — full semantic markup, all copy, zero JS needed to read it |
| **P3** | Step-print hero + 0.01 cm (CSS only) |
| **P4** | `script_ce.js` — peel canvas (Pointer Events), audio gesture, ScrollTrigger |
| **P5** | Boarding pass SVG + ink-in |
| **P6** | Asset triage (§8), OG/Twitter card refresh, 320/360/414 + iOS Safari pass |

---

## 12. Copy deck

> **Cover** — `TAP TO OPEN`
>
> **Hero** — Joel · Sandra
> `AT OUR CLOSEST, WE WERE 0.01 CM APART`
>
> **Date** — `23 · 05 · 26` / `EXPIRES — NEVER`
>
> **Board** —
> ഉറപ്പീരു · Fixation Ceremony
> Joel Francis Jose — son of T.C. Joseph & Tessy Mol Mathew
> Sandra Binoy — daughter of Binoy Abraham & Ranju Binoy
> 6:30 PM · Tharavad The Farmhouse, Kanjirappally, Kottayam
> Followed by dinner
>
> **Pass** — `KANJIRAPPALLY · 18:30 · SEAT: YOURS`
>
> **Close** — ആമേൻ / *Amen.* / "So be it."
