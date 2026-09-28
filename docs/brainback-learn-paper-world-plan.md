# Brainback Learn — The Paper World
### A campaign with nothing to shoot · made entirely by Claude, in code, in this container

Supersedes the shoot-based plan in `brainback-learn-ad-plan.md` §3–§9. The
idea (§2 there) and the Prakash Varma rules (§1 there) stand.

---

## 0. Constraints, checked

- **Nothing is filmed.** No cast, no locations, no plates.
- **No GPU.** This container: 4 CPU cores, 15 GB RAM, ~30 GB free, Python 3.11.
- **What the network allows** (tested 28 Sep 2026): PyPI and npm are open.
  blender.org, huggingface.co, ambientcg.com, freesound.org and
  fonts.google.com are denied by the environment's network policy.
- **Blender is still available**: the `bpy` 4.2 wheel installs from PyPI
  for Python 3.11 and renders Cycles on CPU, headless.

So the whole film has to be made from code: geometry, textures, animation,
light, music, sound and type. That turns out to be the right answer
creatively, not a compromise.

---

## 1. The format

**A world made of notebook paper, animated like stop-motion.**

Every object — the bed, the fan, the city, the girl, the Doubtlings — is
cut and folded from school paper and lit like a tabletop set. Blender
renders it; the timing is stepped on twos at 12 fps, and every held pose
gets a sub-millimetre nudge so the frame "boils" the way hand-moved puppets
do. It reads as stop-motion because it obeys stop-motion's rules.

Why this beats generating video with an AI model:

| Problem with AI video | Paper world |
|---|---|
| The character drifts shot to shot | The Doubtling is one piece of geometry; it is identical in every frame of every film |
| Hands, faces, children look uncanny | Nobody has a realistic face. The girl is a paper cut-out with two dots for eyes |
| Can't direct a gag to the frame | Every beat is a keyframe in a script; a gag can be retimed by two frames |
| Licence and likeness questions | Every asset is written here. The ledger is one line: "made in this repo" |
| Needs a GPU | Cycles on CPU |

It also *is* Varma: one invented character, handmade texture, wordless,
warm, a series.

---

## 2. Cast and world

- **The Doubtling.** Folded from a ruled page: blue lines, a red margin
  down its back, one inked eye, a creased question-mark tail. Three sizes.
  A graph-paper cousin for maths.
- **Meera.** A paper-doll teen cut from grey sugar paper. Two dots for eyes,
  one black cut-out for hair, a school uniform in two pieces. Deliberately
  not a realistic child, and not an egg-headed ZooZoo.
- **The Glow.** The only light in the world that isn't warm paper colour:
  the phone screen. It is Brainback's colour. When Brainback is on, the
  Glow is on; that is the whole product shot. **We don't fake the app's
  interface.** The screen shows a glowing card whose "?" turns into "!".
  If the client gives us real UI, it goes on the screen instead.
- **The paper city.** Houses, a bus, a school ground, a monsoon sky of
  torn grey tissue. Rain is paper confetti on strings.

---

## 3. The films

Shorter than the shoot plan, because every second is a render cost.

### Hero — "Flight" (40s; 20s cut-down)

| Time | Shot |
|---|---|
| 0–6s | Paper bedroom, night, one warm lamp. Meera in bed; the Glow on her face; a feed scrolling. |
| 6–14s | A notebook on the desk twitches. A Doubtling tears itself out, climbs the pillow. Then five more: on the fan blade, in her slipper. |
| 14–24s | She switches to Brainback — the Glow changes colour. "?" becomes "!". The nearest Doubtling unfolds, refolds into a plane, glides out of the window. |
| 24–34s | Camera pulls out through the window: the paper city at night. From window after window, planes lift off. |
| 34–40s | Dawn. A sky full of planes over the school ground. Black. **Every doubt, answered.** Logo. Four-note sting. |

### Shorts (12–15s each)

1. **But Why?** — A Doubtling answers, and a smaller one pops out of it, and
   a smaller one — until the last is answered and all six fly off as one
   flock. *(follow-up questions)*
2. **Doomscroll** — A Doubtling sunbathes on the phone and fades to blank
   paper as the feed scrolls. Brainback's Glow: the blue lines come back.
   *(gives back)*
3. **Exam Morning** — A school bag's zip strains over a crowd of Doubtlings.
   One quiz at a time, they fly out of the gap until it closes.
4. **Graph Paper** — The grumpy maths Doubtling won't fold; when it gets the
   answer, it unfolds into a perfect parabola flight path.

---

## 4. How each thing gets made

| Element | Method | Tools (all installable here) |
|---|---|---|
| Paper textures | Procedural: fibre noise, tooth, ruled lines, margin, graph grid, torn and deckled edges, pencil smudges | numpy, Pillow |
| Geometry | Python builds every object: folds as hinged planes, the Doubtling's fold states as shape keys; paper thickness with a solidify modifier | `bpy` |
| Unfold → plane | A fixed sequence of fold states; the unfold interpolates through them | `bpy` shape keys |
| Animation | Keyframes written by script; constant interpolation on twos; per-hold jitter ("boil") | `bpy` |
| Light | One warm practical + one cool ambient per shot; the Glow as an emissive plane | `bpy`, Cycles |
| Plane flocks | Blender boids particle system with a paper-plane instance | `bpy` |
| Render | Cycles CPU, ~64 samples + OpenImageDenoise, 1920×1920 master, cropped to 16:9, 9:16 and 1:1 | `bpy` |
| Theme | A four-note motif, composed in code as `tools/compose.py` does: additive synthesis, owes nothing to anyone | numpy |
| Sound | Paper rustle, fold snap, tear, plane whoosh, rain — synthesised from shaped, filtered noise | numpy, scipy |
| Type | Baloo 2 for the end line; Noto Sans Devanagari, Malayalam, Tamil, Telugu, Bengali, Kannada, Gujarati for translations — OFL, via npm's `@fontsource` packages | npm |
| Translation | Claude drafts the end line in each language; **a native speaker checks every one** (IndicTrans2 is on huggingface.co, which is blocked) | — |
| Assembly | Encode, crop, mix, loudness to −14 LUFS | FFmpeg via `imageio-ffmpeg` |

**Where generative AI models could come in, optionally.** If
huggingface.co is added to the environment's allowed domains *and* a GPU
is attached, FLUX.1 [schnell] could paint backdrop skies and Wan 2.2 could
add atmosphere shots. Neither is on the critical path; the plan works
without both.

---

## 5. The agents

One orchestrating session (director) owns the style bible and the shot list.
Subagents get one narrow brief each, and the per-film work runs in parallel
once the pilot shot is locked.

| Agent | Brief | Writes |
|---|---|---|
| **Director** | Holds the rules; approves every shot against §1 of the first plan | `paper/shots.yaml` |
| **Brand researcher** | Confirm the product; claims sheet | `paper/brief/` |
| **Paper-maker** | Texture generator; every paper stock | `paper/lib/paper.py` |
| **Set and character builder** | Doubtling, Meera, bedroom, city, props as Python functions | `paper/lib/puppets.py`, `sets.py` |
| **Animator** (one per film) | Keyframes each shot from `shots.yaml`; timing on twos; boil | `paper/films/<film>/shotNN.py` |
| **Render wrangler** | Queues shots as background jobs; resumes where a render stopped; encodes each finished shot | `paper/renders/` |
| **Composer and sound** | Theme, sting, foley, mix | `paper/audio/` |
| **Localiser** | End cards in 8 languages; routes them to native speakers | `paper/endcards/` |
| **Editor** | Conforms shots, audio, end card; the three crops | `paper/out/` |
| **QC** | Checks every frame for glitches (contact sheets), loudness, crop safety, claims | `paper/out/qc.md` |

The licence auditor from the first plan shrinks to one check: that nothing
entered the repo that wasn't written here, apart from the OFL fonts.

---

## 6. Step by step

| # | Step | Who | Done when |
|---|---|---|---|
| 1 | Install `bpy`; render one lit, textured sheet of paper | Director | A PNG that looks like paper under a lamp |
| 2 | Paper library: ruled, graph, sugar paper, tissue | Paper-maker | Swatch sheet you approve |
| 3 | Build the Doubtling: rest pose, three fold states, the plane | Builder | Turnaround PNG |
| 4 | **Pilot shot: a Doubtling unfolds into a plane and flies off, 4 seconds** | Animator | You watch it. **If it isn't charming, stop and redesign here** — this is the kill test |
| 5 | Measure render time per frame from the pilot; fix the budget (§7) | Render wrangler | Real numbers in §7 |
| 6 | Confirm the product; claims sheet | Brand researcher | You or the client sign it |
| 7 | Style bible: palette, lens, light rules, boil amount, the four notes | Director | One page |
| 8 | Shot lists for hero + four shorts | Director | `shots.yaml` |
| 9 | Animatic: grey-box geometry, workbench render, temp theme | Animator | Every film runs to length |
| 10 | **Gate: you approve the animatics** | You | Locked cut |
| 11 | Build Meera, the bedroom, the city, the bag, props | Builder | Turnarounds |
| 12 | Theme, sting and foley | Composer | Stems |
| 13 | Animate every shot (films in parallel) | Animators | Every shot plays in workbench |
| 14 | Final renders, shot by shot, as background jobs | Render wrangler | Every shot encoded and pushed |
| 15 | End cards in 8 languages | Localiser | Native speaker sign-off each |
| 16 | Conform, mix, crop to 16:9 / 9:16 / 1:1 | Editor | Masters |
| 17 | QC: contact sheets, loudness, crops, claims | QC | No fails |
| 18 | **Gate: you approve the final films** | You | — |

You approve at steps 4, 6, 10 and 18. Nothing else needs you.

---

## 7. Render budget (estimate until step 5 measures it)

- Unique frames: 12 per second (on twos at 24 fps).
- Hero 40s + four shorts at ~14s ≈ 96s → **~1,150 frames**.
- Guess: 40–90 s per frame at 1920×1920 on 4 cores → **13–29 hours**.
- The container is reclaimed when idle, so each shot is encoded and pushed
  as soon as it finishes. Scripts are in git, so any shot can be re-rendered
  from scratch; losing a container loses at most one shot.
- If the budget is too high: drop samples, render the city at lower
  resolution with depth of field, or render only the 9:16 crop first.

---

## 8. Honesty and risk

- **Product claims** stay unconfirmed until step 6; the films only show what
  the claims sheet allows.
- **No fake app UI.** The Glow stands in for the screen.
- **No lookalikes.** The Doubtling and Meera are original; no ZooZoo shapes,
  no use of Varma's or Vodafone's name.
- **Biggest risk is taste, not tech.** Step 4 decides whether this is
  charming. Everything after it is labour.
