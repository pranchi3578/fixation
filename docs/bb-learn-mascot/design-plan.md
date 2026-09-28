# BB Learn — Character Logo, Design Plan
### A small character for BrainBack's voice tutor, the way Claude Code has Clawd

Status: **plan, for review.** Nothing final is drawn yet. `concepts.svg` / `concepts.png`
are rough sketches for choosing a direction (regenerate with `python3 concepts.py`).

> **Round 3, the owl, is in [`owl-design-plan.md`](owl-design-plan.md)** (sheet: `owl.png`), and it is the current direction. The Unmute mic is parked.
>
> **Round 2 is in [`concepts-round-2.md`](concepts-round-2.md)** (sheet: `concepts_v2.png`).
> It has fourteen concepts from five angles, scored side by side. The recommendation
> there moves from the Bubble (§2–3 below) to **Patti, the slate**, with Basta and
> Bubble as runners-up. §4–§6 (colour, open assets, deliverables) apply to
> whichever character wins; §3 will be redrawn for the winner.

---

## 0. The idea in one line

BB Learn is a teacher you can talk to. It **talks**, **shows**, and **helps fix
mistakes**, in the child's own language, and it stops the moment the child speaks.
So the character is **a speech bubble that teaches**: one of BrainBack's pixels
turned into a voice, with a face.

---

## 1. What we take from Claude's character, and what we don't

| Claude / Clawd does | We do |
|---|---|
| Made from a handful of square pixels, so it reads at 16px and scales to a billboard | Same, and our pixels are **BrainBack's own grid cells** (10px cell, 2px gap, 1px radius; `visual/patterns.md`). The logo is built from the brand texture, not added on top of it |
| One flat colour, no gradients or outlines | One flat ink, **black or white**. BrainBack is strictly monochrome; a lighter tone comes from the opacity scale (35%), not a new hue |
| Personality comes from very few parts: eyes, a little posture | Eyes (two 1×2 slots), one mouth row, the bubble tail. Nothing else |
| Animates by moving whole pixels, never by tweening curves | Same. Every pose is a grid edit, so animation stays crisp and cheap |
| Friendly without being childish | Friendly for a 7-year-old, calm enough for a school's procurement deck |

**What we don't copy:** Clawd's shape, its terracotta/orange, a body with legs,
or the Claude spark. Our silhouette is a speech bubble, and it's black and white.
Clawd and the spark are Anthropic's marks: we borrow the *approach* (few pixels,
one colour, a strong silhouette), never the look. That gets checked in §7.

---

## 2. Directions (see `concepts.png`)

| | Direction | Story | Why / why not |
|---|---|---|---|
| **A** | **Pixel Doubtling**: the folded-paper doubt from the *Unmute* ad, one eye, a `?` tail | The student's doubt | Ties straight to the ad. But it's the *problem*, not the tutor. A logo of a doubt reads as "confusion". Keep it as a **supporting character** |
| **B** | **Bubble**: a speech bubble with eyes, a dog-eared corner (35% ink), and a tail | The tutor itself: it talks | The most direct image of a voice-native teacher. A clear silhouette at 16px. The folded corner nods to the Doubtling's paper. **Recommended** |
| **C** | **Answered**: the Doubtling refolded into a paper plane | Understanding takes off | A good *end state*, weak as a character: no face, and it reads as "send". Use it as B's **exit animation** and in the ad's sting |

**Recommendation: B as the logo character, with A and C as its world.** The doubt
(A) arrives, the bubble (B) talks it through, and the doubt folds into a plane (C)
and flies off. That is the ad's story, told with three pixel sprites that share
one grid.

---

## 3. The character (direction B)

### 3.1 Construction
- **Master grid: 12 × 11 cells.** The body is 12×9 with 2-cell rounded corners.
  The tail is 2 cells, bottom-left (the side the *Unmute* bubble came from).
- **Eyes:** two vertical 1×2 slots, cut out of the body (negative space, so the
  eyes invert correctly on black). In the final pass, try 2×2 eyes at large
  sizes. The sketch shows the gap texture eating 1-cell eyes at 128px.
- **Mouth:** one row, 2 cells wide at rest. The only part that animates for speech.
- **Folded corner:** top-right, 3 cells at 35% ink. The one nod to paper and to
  the Doubtling. Drop it under 24px.
- **Gaps:** the 2px grid gap shows at 64px and up (the brand texture). At 32px and
  under the cells merge solid, or the face turns to noise.

### 3.2 States (one grid edit each, and each is a product move)

| State | Pixels | Product move |
|---|---|---|
| **Talks** | mouth steps 2 → 4 → 2 cells, 3 frames | "It talks" |
| **Listens** | mouth closes, eyes go up one row, body rises 1 cell | "Interrupt anytime": the moment the child speaks, it stops |
| **Shows** | a 3×3 pixel board appears beside it with a tick, a letter or a sum | "It shows" |
| **Waits** | slow blink every ~4s (eyes 2 → 1 → 2 rows) | "It waits until he can say it himself" |
| **Fixes** | a single cell drops out of a line and is put back in place | "one typo at a time" |
| **Proud** | eyes become `^ ^` (3-cell chevrons), one hop | "You nailed it" |
| **Thinking** | three pixels pulse in the brand's `sin³` rhythm (`patterns.md` §1.5) | loading, instead of a spinner |

### 3.3 Name
A working name for review, not a decision: **"Bit"**. It's one pixel of
BrainBack, a *bit* of teaching at a time, and easy to say in every Indian
language. Other names: *Boli* (बोली, "speech"), *Sabak* ("lesson").

### 3.4 Lockups
- **Character alone:** app icon, favicon, avatar in the tutor UI, stickers.
- **Character + "BB Learn"** in Geist Sans 800, −0.045em, the same cap-height rule
  as the wordmark. Character on the left, 1 B-height of clear space between them.
- **Never merged into the BRAINBACK wordmark.** `brand/logo-usage.md` says the
  company logo is wordmark-only, with no icon. The character belongs to the
  **product** (BB Learn), so the company wordmark stays untouched. See §8, Q1.

---

## 4. Colour

- **Default:** `#000` on white, `#FFF` on black (only these two, per `logo-usage.md`).
- **Tones:** only from the opacity scale (the 35% fold, 8–15% for a shadow row).
- **Open question, not assumed:** the kids' audience may argue for one Learn
  accent colour (the ad used a placeholder teal). That would be BrainBack's first
  hue, so it's the brand owner's call (§8, Q2). The character must work in pure
  black and white first either way.

---

## 5. Open-source assets and tools

Everything is either made by us in code (as in `brainback-ad`) or comes from a
permissive source. **No NC, ND, "personal use only" or unclear licences.** Each
item is recorded in `ledger.csv` (source, licence, author, date checked) when it's used.

| Need | Asset / tool | Licence | Note |
|---|---|---|---|
| Display type for lockups | **Geist Sans / Geist Mono** (Vercel) | SIL OFL 1.1 | Already in `design_guidelines/assets/fonts` |
| Handwritten notes around the character (kid-facing only) | **Caveat** | SIL OFL 1.1 | Already used in `brainback-ad/paper/fonts` |
| Indic script labels ("hello" in 10 languages beside Bit) | **Noto Sans** Devanagari, Tamil, Telugu, Bengali, Malayalam… | SIL OFL 1.1 | Google Fonts |
| Pixel drawing | **Pixelorama** | MIT | or **LibreSprite** (GPL-2.0). *Not Aseprite*: its binary is under a proprietary EULA |
| Vector cleanup / export | **Inkscape** | GPL-3.0 | Tool licence only; our output is ours |
| Source of truth | A **Python script → SVG**, like `concepts.py` | ours | Grids as text, so every pose is diffable and reviewable in git |
| Web animation | **Lottie** JSON played by **lottie-web** | MIT | or plain CSS/SVG step animation, which needs no dependency |
| Interactive states (in-app) | **Rive runtime** | MIT runtime | Optional. The Rive *editor* is a hosted product, so keep the source in our script and export |
| Video / GIF exports | **FFmpeg** | LGPL/GPL | Also through `imageio-ffmpeg`, as the ad pipeline does |
| Four-note sting under the logo animation | the ad's own motif (`brainback-ad/paper/lib/sound.py`) | ours | Synthesised, so no licence to check |
| Blip SFX for talk / listen | **Kenney** UI Audio, or **Freesound** CC0 only | CC0 | Freesound's CC-BY and CC-BY-NC files are excluded |
| Reference for pixel proportion | **Kenney** 1-Bit Pack | CC0 | **Reference only.** Nothing is traced or copied |

Not using: AI image generators for the mark itself. A logo has to be
trademark-clean and exactly reproducible, so it's drawn cell by cell.

---

## 6. Deliverables

```
bb-learn-mascot/
  src/bit.py            grids for every pose → all outputs
  svg/  bit.svg, bit-reversed.svg, bit-{16,24,32}.svg (gapless small-size cuts)
  png/  favicon 16/32/48, app icon 192/512/1024, apple-touch 180
  lockup/  bit-bblearn-horizontal.svg, -stacked.svg (black and white)
  motion/  talk, listen, wait, proud, thinking, exit-to-plane
           each as .json (Lottie), .svg (CSS steps), .gif, .mp4
  sheet.html            the character sheet: construction grid, states, sizes, dos and don'ts
  ledger.csv            every third-party asset and its licence
  usage.md              rules, in the style of design_guidelines/brand/logo-usage.md
```

---

## 7. Steps

1. **Choose a direction.** Review this plan and `concepts.png`, and answer §8.
2. **Master drawing.** Refine B on the 12×11 grid, with 2 or 3 variants of the
   eyes, fold and tail. Test at 16/24/32/64/512 and on black.
3. **Distinctness check.** Put it side by side with Clawd, the Claude spark, the
   iMessage/WhatsApp/Discord bubbles and the Duolingo owl. It has to read as its
   own thing at 16px. Also run a trademark search (India IP office class 9/41, USPTO/WIPO).
4. **States.** Draw the 7 poses as grid edits, and animate at 8–12 fps, stepped (no easing).
5. **Lockups and usage rules.** Write `usage.md` and add a Learn section to `design_guidelines`.
6. **Exports and ledger.** Run `bit.py` for every output and fill the licence ledger.
7. **In context.** Put it in the proposal hero, the tutor avatar, the favicon and the
   ad end card, and check it with 3–5 kids in the target age range (does it read as
   "friendly teacher"?).

---

## 8. Questions for you

1. **Brand rule:** `logo-usage.md` says "wordmark only, no icon". Is a *product*
   character for BB Learn allowed, as long as the BRAINBACK wordmark is untouched?
2. **Colour:** pure monochrome (recommended to start), or one Learn accent?
3. **Direction:** from round 2's shortlist: Patti (slate), Basta (bag), or Bubble? Or something from outside the shortlist?
4. **Name:** follows the direction (Patti, Basta, Bit, …), or unnamed?
5. **Where this lives:** this plan sits in `fixation/docs/` because that's this
   session's branch. The real work should go in `brainback-ad` or
   `design_guidelines`. Which one?
