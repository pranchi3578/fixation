# BB Learn: the owl, design plan
### Pixelled like BrainBack's board, lively like Claude's mark, a friend a student would choose

Status: **plan, for review.** The sketch sheet is `owl.png` (from `python3 owl.py`), a
rough drawing for planning. The **Unmute mic is parked**, not dropped (see
`concepts-round-2.md` #06). Its best idea, *it stops the moment you speak*, lives
on in this owl as the Listening state (§6).

---

## 0. The idea in one line

**A small owl that lives on BrainBack's LED board: the best listener in nature,
lit up one pixel at a time.**

---

## 1. Reading the brief

| You said | What it means here | Source |
|---|---|---|
| "Pixelled like the BrainBack logo" | The **PixelBoard**: the site's hero, where BRAINBACK is set in a 5×7 LED font. Every cell on the board is always faintly lit (3%), letters glow at several brightness levels, scattered cells sparkle, and letters "breathe" on their own phase | `landing-page-demo/src/components/PixelBoard.tsx`, `pixelboard-static-2x.png` |
| "Lively like the Claude logo" | Claude's mark feels alive because it's **slightly irregular** (hand-made, not geometric) and it **moves like it's thinking**: small, organic, never looping. Clawd, the Claude Code character, is alive in a few pixels: a blink, a shift, a hop | Approach only. No shape, colour or motion is copied |
| "Something any student would befriend" | Every choice below is backed by a known finding in developmental or social psychology (§4), and there's a list of what the owl will **never** do (§8) | |

**A brand inconsistency I found, which you should know about:**
`design_guidelines/brand/logo-usage.md` says the logo is "wordmark only, no icon,
monochrome". But `assets/logos/logo.svg` is a **brain icon** whose right half forms
a "B", drawn in black and **blue (`#195589`)**, with the tagline *Architecting
Intelligence*. The owl works with either. I've kept it monochrome and made one
blue option (§7), but the guidelines and the logo files should be reconciled.

---

## 2. Why an owl works for BB Learn (and two risks to design around)

**What owls really are, and what BB Learn does:**

| Real owl | BB Learn |
|---|---|
| The **best listener** among birds: its face is a dish that gathers sound, and it can pinpoint a mouse under snow | Voice-native. It hears the child, and it **stops the moment they speak** |
| **Sees in the dark** | Sees where the child is stuck, even when they can't say it |
| **Silent flight**: it never startles | Patient, never loud, never rushes |
| **Awake at night** | The late-night study companion, and the one who tells you to sleep (§6) |
| **Wise**, in the Western story | Knows a lot, but acts like a friend, not a professor (§4) |

**Risk 1: Duolingo owns "the owl" in learning apps.** So distinctness is a design
requirement, not a nice-to-have:

| Duo (Duolingo) | Our owl |
|---|---|
| Green, smooth vector, cartoon | Monochrome **LED pixels** on a dark board. It's made of light |
| Round blob body, small tufts | A **spotted owlet**: no tufts, white brows, white collar, spotted wings |
| Famous for guilt: streak threats, the "sad owl", passive-aggressive reminders | **Never guilt-trips** (§8). Our owl is the opposite personality: *the owl that doesn't nag* |
| Performs for you | Listens to you |

**Risk 2: Indian cultural readings of the owl.**
- **"Ullu"** (उल्लू) is a common Hindi/Urdu insult meaning *fool*, and *ullu banana*
  means to make a fool of someone. Children will make that joke. **Never name it
  Ullu**, and test for teasing in user research (§11).
- In some regions the owl is an **ill omen**; elsewhere it's **Lakshmi's vahana**
  (auspicious, but religious). Keep the character **secular**: no religious
  styling, no festival lore.
- **What helps:** we draw India's own **spotted owlet**, the small, friendly owl
  that lives in city trees, temples and school compounds and is often seen in
  pairs. It's the owl Indian kids actually meet, not the storybook eagle-owl.

---

## 3. The species: spotted owlet (*Athene brama*)

- **India's commonest owl**, found almost everywhere except the high Himalaya and
  dense forest. It's small (~20 cm), round-headed, with **no ear tufts** (unlike
  Duo, and unlike the "scary" horned owls).
- **White spots on brown**: on our board, the spots are **lit pixels**, the same
  as the PixelBoard's sparkles. The species' own markings *are* the brand texture.
- **White brows** and a **white collar**: natural high-contrast features that read
  at pixel scale.
- Known for **bobbing its head** when curious. That's a real, lively behaviour
  we can animate (§6).

---

## 4. The psychology: finding → design decision

| Finding | What it says | Decision |
|---|---|---|
| **Baby schema** (*Kindchenschema*; Lorenz 1943; Glocker et al. 2009) | A big head, large low-set eyes, a round face and a short body trigger care and approach | Head ≈ half the body height. Eyes take ~half the face. It's an **owlet**, not an adult owl |
| **Curved contours** (Bar & Neta 2006) | People prefer curves, and sharp angles read as threat | Stepped-round silhouette. The **beak is two pale cells, never a point**. No talons |
| **Watching-eyes effect** (Bateson, Nettle & Roberts 2006) | Images of eyes make people feel observed | Owls stare, and a staring tutor feels like surveillance. So its **default gaze is on the lesson, not the child** (joint attention). Direct eye contact is short and warm: greeting, praise, listening |
| **Gaze cueing / joint attention** (Frischen, Bayliss & Tipper 2007) | We automatically look where a face looks | Its pupils **point at what matters**: the typo, the next step, the diagram. The eyes are a teaching tool |
| **Social contingency** (Kuhl 2007; Roseberry, Hirsh-Pasek & Golinkoff 2014) | Children learn from partners who respond *to them*, in time | It reacts in **under 200 ms** when the child speaks (pupils up, body still). A pre-recorded animation would not |
| **Persona effect** (Lester et al. 1997) | A lifelike on-screen agent makes learning feel more positive | Always present, always alive (idle motion, §6), even when it's quiet |
| **Uncanny valley** (Mori 1970) | Near-human faces feel creepy | The pixels keep it abstract. **Never** add realistic textures or human features |
| **Growth mindset praise** (Mueller & Dweck 1998) | Praising effort beats praising intelligence, and "you're so smart" makes kids avoid challenge | *Happy* fires on **effort and progress**. A wrong answer gets **curiosity** (*Hmm*: a head tilt, eyes on the work), never a frown, a red X or disappointment |
| **Pratfall effect** (Aronson, Willerman & Floyd 1966) | A competent person who makes a small blunder becomes more likeable | It sometimes makes **its own small, harmless mistake** (*Oops*: crossed eyes, a pixel falls off and it sticks it back). Never in the lesson's content |
| **Near-peer effect** | Kids open up to a slightly older companion more than to an authority | A **didi/bhaiya** (older sister/brother), not a teacher. No mortarboard, no glasses, no pointer stick |
| **Self-determination theory** (Deci & Ryan) | Motivation needs autonomy, competence and relatedness | *Autonomy:* the child names it and can hide it. *Competence:* it celebrates small steps. *Relatedness:* it remembers the child's name and last lesson |
| **IKEA / endowment effect** (Norton, Mochon & Ariely 2012) | We value what we helped make | The **child names their owl** and picks one detail (which feather is the cowlick) |
| **Mere exposure** (Zajonc 1968) | Familiarity breeds liking | The same **hello ritual** every session (a two-blink greeting and a hop), and the same silhouette everywhere |
| **Teens reject "babyish"** | Cute characters lose kids around age 11–13 | **It grows up with the student** (§6.3). Teens can drop down to **eyes only** |

---

## 5. The character (see `owl.png`)

- **Grid: 15 × 16 cells**, the **same cell as the PixelBoard's letters** (10px cell,
  2px gap, 1px radius). So it can stand on the board next to the wordmark, 16 rows
  tall against 7-row letters.
- **Four brightness levels plus off**, the board's own language (it breathes
  through brightness, not colour):
  - 100%: eyes, brows, spots
  - 78%: collar and beak
  - 50%: plumage
  - 26%: eye rims and wing edges
  - off: pupils, which go dark on the dark board and full ink on white
- **Anatomy, and the reason for each part:**
  - **Eyes (4×4 with a 2×2 pupil, inside a dark rim):** the whole personality. Baby
    schema, and they point at the lesson.
  - **White brows, high and open:** friendly, not stern. Lowered brows read as angry.
  - **Two-cell pale beak on the midline:** this is where the **logo's two
    hemispheres** meet (a quiet link to the brain/B mark).
  - **Spots:** the species' markings and the board's sparkle, the same thing.
  - **Cowlick (one cell sticking up, off-centre):** the **one imperfection**. Claude's mark
    is alive partly because it isn't perfectly regular, and this is our version. It's also
    the part the child can personalise.
  - **Feet planted:** it stays with you. A companion, not a performer.
- **Sizes:** full owl at 32px and up (tested on the sheet), **eyes only** under 32px
  and in the UI corner.
- **On white:** the brightness scale inverts to ink, but the **eyes stay light with
  dark pupils** (a plain inversion would make black eyes with white pupils, which is creepy).
- **Known issues from the sketch, for the drawing pass:** the eyes are too square
  (they read as goggles), so soften the corners with 78% cells. The *Happy* crescent is
  weak at small sizes. Several states differ by one pupil move, so **motion has to carry them**.

---

## 6. Alive: behaviour and motion

### 6.1 The idle loop (the "Claude" part)
It never loops the same way twice. Timings are drawn from ranges and seeded, like
the PixelBoard's `hash()`:
- **Breathing:** the body brightness swells 50% → 58% → 50% over about 4 s. It
  breathes the way the board breathes.
- **Blinks:** at random 2–6 s gaps, sometimes a double blink. A regular blink looks
  robotic.
- **Glances:** the pupils shift one cell toward whatever just changed on screen.
- **Spots twinkle** in the board's `sin³` flash, out of sync.
- **Head-bob** (the real owlet's curiosity move): one cell down and back, a few
  times a minute.
- **Stepped motion only:** whole cells, 8–12 fps, no smooth tweening. Anticipation
  (a 1-cell squash before a hop) and follow-through (the cowlick lands a frame late).

### 6.2 States (on the sheet, plus the motion that sells each one)

| State | Trigger | Pixels | Motion |
|---|---|---|---|
| **Hello** | session start | resting | two blinks and a hop: the same ritual every time |
| **Listening** | the child starts speaking | pupils up | **freezes mid-anything in <200 ms**; spots stop twinkling. This is the Unmute idea |
| **Talking** | it speaks | resting | the collar row pulses with the voice's loudness. The beak stays still: a flapping beak reads as a puppet |
| **Looking at your work** | content on screen | pupils toward it | slow glance, then hold |
| **Hmm** | wrong answer | one eye narrows | head tilt, the owlet bob, eyes to the mistake, *"let's look at this together"* |
| **Happy** | effort or progress | crescent eyes | a hop, and the spots flash once in sequence |
| **Oops** | its own tiny slip (rare) | crossed pupils | a spot falls off and it pops it back on |
| **Thinking** | waiting on the model | pupils up-side | three board cells beside it pulse in `sin³`. No spinner |
| **Sleepy** | late at night | half-lidded | yawns, *"I'm the night owl, not you. Sleep!"* |

### 6.3 It grows up with the student

| Stage | Grades | Expression |
|---|---|---|
| **Owlet** | 1–4 | fullest: hops, big reactions, spots twinkle a lot |
| **Young owl** | 5–8 | calmer, drier humour, fewer hops (the real-lesson students in the proposal are here) |
| **Eyes only** | 9–12 (opt-in anytime) | just the two eyes glowing in the corner. Present, not cute |

It also **mirrors the child's energy, then leads it**, as in the proposal's two real
lessons. For **the shy one**, it's smaller and quieter and waits longer before
prompting. For **the one who couldn't sit still**, it matches the energy for a
beat, then slows its own motion, and the child tends to follow.

---

## 7. Colour

- **Default: monochrome on the board** (white light on black, and ink on white).
  It's the PixelBoard's own language, so it needs no new brand rule.
- **Option: the logo's blue `#195589` in the irises only.** It ties the owl to the
  brain/B logo, and one colour on a monochrome owl makes the eyes the focus.
  It's your call, and it only makes sense once §1's inconsistency is settled.
- **Never** yellow irises or brown plumage (realism breaks the LED language), and
  never green (Duolingo).

---

## 8. What it will never do

Using psychology on children means it has to earn trust, not attention. These
rules are part of the design:

- **No guilt:** no streak threats, no sad owl when you leave, no "I miss you" notifications.
- **No fear of missing out**, no artificial scarcity, no loot boxes or random rewards.
- **No dependence:** it points kids to their real teacher, parents and friends ("ask
  your teacher about this tomorrow!"). It's a companion, not a replacement.
- **No shame:** mistakes get curiosity. Never red crosses, never a public score.
- **It never pretends to be human**, and it says "I'm your BB Learn owl" if asked.
- **It tells kids to sleep** rather than keeping them up.
- Aligns with the **UK Age Appropriate Design Code** (no nudge techniques against a
  child's interest) and **India's DPDP Act 2023** (verifiable parental consent, no
  behavioural tracking or targeted ads for children).

---

## 9. Name

- **Not "Ullu"** (§2).
- **The child names their own owl** (§4, IKEA effect). The default name is just a placeholder.
- Default candidates:
  - **Hoo:** the owl's call, and English "who?", the question word. Short and
    gender-neutral, and the same in every language.
  - **Tara** ("star", understood across most Indian languages; a lit pixel in a night
    sky). It reads as a girl's name, which could be a deliberate choice (girls in STEM).
  - **Nishi** ("night"). Also a given name.
- Recommendation: **Hoo** as the default, and the child can rename it.

---

## 10. Open-source assets and tools

The same licence rules as round 1: only permissive licences, and every item logged
in `ledger.csv`.

| Need | Asset / tool | Licence | Note |
|---|---|---|---|
| The board, the 5×7 font, the breathing/sparkle maths | BrainBack's own `PixelBoard.tsx`, `lattice.ts` | ours | The owl renders **inside the real component**, not a copy of it |
| Pixel drawing and animation frames | **Pixelorama** | MIT | or LibreSprite (GPL-2.0). Not Aseprite (proprietary binary) |
| Source of truth | `owl.py`-style grids → SVG, Lottie, sprite sheets | ours | Every pose is diffable text |
| Web playback | **lottie-web** | MIT | or a canvas renderer inside `PixelBoard.tsx` itself (no dependency) |
| In-app state machine | **Rive runtime** | MIT | optional |
| Type in lockups | **Geist Sans / Mono** | SIL OFL 1.1 | |
| Script greetings ("Hoo" says hello in 22 scheduled languages) | **Noto Sans** Indic families | SIL OFL 1.1 | |
| Owlet anatomy reference | **Wikimedia Commons** photos of *Athene brama* | per file (CC BY / BY-SA) | **Reference only**, never traced or shipped |
| Owlet calls | **xeno-canto** | mostly CC BY-NC-SA | **Listen only.** NC is excluded, so the hoot is **synthesised** instead |
| Hoot, hop and blip sounds | synthesised, as `brainback-ad/paper/lib/sound.py` does | ours | |
| Research | the papers cited in §4 | citation only | |

---

## 11. Steps and testing

1. **Settle the brand questions** (§12, Q1–Q2).
2. **Drawing pass:** three versions of the owl (eye shapes, how many spots, where the
   cowlick sits), fixing §5's known issues. Test at 16/32/64/512px, on black and on white.
3. **Distinctness check:** side by side with Duo, Hootsuite's Owly and the
   Tripadvisor owl. It must read as *not them* at 16px. Run a trademark search
   (India class 9/41, WIPO).
4. **Motion:** the idle loop plus all 9 states, rendered inside `PixelBoard.tsx`.
5. **Kid testing** (with consent, chaperoned), 3 age bands (6–9, 10–13, 14–17), 3 variants:
   - **Smileyometer** (Read & MacFarlane's *Fun Toolkit*): "would you be friends with it?"
   - **Draw-it-from-memory** after 5 minutes: is it memorable and simple enough?
   - **Naming test:** what do they call it without prompting? (This catches "ullu" early.)
   - **Multiple regions** (at least North, South, East, and Hindi and non-Hindi belts) for cultural readings.
   - **Teens:** is the eyes-only mode acceptable?
6. **Parent and teacher read:** does it feel safe, calm and trustworthy? And does it
   feel like a teacher's helper rather than a replacement?
7. **Usage guide and exports:** `usage.md`, the lockups, favicon/app icon (eyes only), Lottie files.

---

## 12. Questions for you

1. **The brand:** which is the real logo, the brain/B mark (with blue) or the
   wordmark-only rule in the guidelines? It decides whether the owl can borrow the blue.
2. **Colour:** pure monochrome, or blue irises?
3. **Species:** spotted owlet (recommended), or would you prefer a different owl?
4. **Name:** Hoo as the default, with the child renaming it? Or one fixed brand name?
5. **Age range:** what grades does BB Learn serve? That sets how far the "grows up" stages need to go.

---

## Round 4: back to the cuter owlet, plus a robot owl

Sheet: `owl_round4.png` (from `python3 owl_round4.py`).

### The owlet (preferred over §5's version)
The first drawing was cuter than §5's "fixed" one, and the reasons are useful
for the final drawing:
- **Soft over crisp.** No dark eye rims and no white brows. The eyes glow out
  of a bright, low-contrast face instead of being framed. Framing made it look
  alert, where softness looks young.
- **Small, tall pupils** (1×2 cells) in big eyes. 2×2 pupils made it look like
  it was staring.
- **Narrower (13 cells).** Compact reads as small.

The refined version keeps all three and changes only the eyes: **4×3 with
rounded corners**, pupils **low and turned slightly inward**. That's the
"looking up at you" look of a very young animal, and it fixes round 3's
first draft, where the eyes merged into the face. It has six states (resting,
listening, your work, happy, blink, sleepy), and it reads at 32px and on white.

### The robot owl: square, pixelled, WALL-E-like
Each owl trait becomes a machine part: **ear tufts → antennae** (they light up
when it listens), **chest feathers → a chevron grille**, **wings → side flaps**,
**feet → treads**.
- **A · Hoo-bot:** two binocular eye barrels on a neck, with dark lenses and a
  bright glint (big dark pupils are baby schema too), a boxy body, and treads.
  It has the **head tilt** (one barrel rides a row higher) as its curious state.
- **B · Cube:** the whole owl is one box, with a lid seam and a **learning meter**
  that fills as the lesson goes. It's the sturdiest silhouette at 16px.

**Where it fits:** the robot owl is more honest about being a machine (§8: it never
pretends to be human), and teens may find it less babyish than the owlet. The owlet
is warmer for younger kids. One option is for both to be the same character: the
owlet for grades 1–4, the robot as its "grown-up" look (§6.3).

**IP caution:** WALL-E belongs to Disney/Pixar. We borrow *traits* (binocular eyes,
treads, a boxy body, the head tilt), never its exact eye shape, its yellow body,
its trash-compactor story or its name. Put it through the same distinctness check
as Duo (§11.3), side by side with WALL-E and EVE.
