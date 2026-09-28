# Brainback Learn — Ad Campaign Plan
### "Give it back." · An end-to-end AI tutor, made the way Prakash Varma makes films

---

## 0. What we know about the product, and what we don't

Everything below the creative line rests on one public description of
Brainback (brainback.top, read through a search index because the site is
blocked from this container):

- An AI tutor that gives instant explanations and answers follow-up questions.
- A vertical feed of short lessons ("learn anything in 60 seconds"), each
  followed by a quick quiz and XP.
- Aimed at teens, 13–18. No text comments, parental oversight.
- Core app free; paid micro-courses.

**If that is not your Brainback Learn, stop at §2** — the concept depends on
the feed. Every product claim in a script (languages, syllabus coverage,
"remembers your doubts", pricing) goes on the claims sheet in §7 and is
signed off by the client before it is spoken or written on screen.

---

## 1. Directing like Prakash Varma — the rules, not the look

What his work actually has in common (ZooZoos for Vodafone, Incredible
India, Cadbury, Indian Railways):

| Trait | What it means on our set |
|---|---|
| **Wordless** | No dialogue. The ZooZoos spoke gibberish; we speak none. The only words are the end line. Travels across every Indian language for free. |
| **One idea per film** | Each spot is a single gag or a single feeling, 20–30 seconds, resolved before the logo. |
| **An invented character, built by hand** | The ZooZoos were people in suits, not CGI. Our character is made of something real and cheap, and it looks it. |
| **Series, not a spot** | ZooZoos were ~30 films over one IPL. We plan a hero film plus a run of shorts that can drop daily. |
| **Warmth over cleverness** | The audience smiles before they understand. The product arrives as kindness, not as a feature list. |
| **India that isn't a postcard** | A real bedroom, a real bus, a real tuition-centre corridor. Incredible India scale only once, at the end of the hero film. |
| **Music carries the edit** | One signature tune, whistle-able, the same four notes in every film. |

**What we do not borrow.** No ZooZoo lookalikes (egg heads, white bodies) —
that is Vodafone's IP and it would read as a copy. No use of Varma's name or
Nirvana Films' in the ad or its metadata. We borrow the method, not the
mark.

---

## 2. The idea

Every teen already has a feed that takes something from them. Brainback's
feed gives something back — and when a lesson leaves a doubt, the tutor
answers it right there, however many "but why?"s it takes.

So the character is **the Doubt**.

### The Doubtling

A small creature folded from a page of a ruled school notebook — margin line
down its back, one inked eye, a creased question-mark tail. It appears when a
kid doesn't get something. It sulks, it follows them around, it multiplies
if ignored.

When the tutor answers, the Doubtling **unfolds**, refolds itself into a
paper aeroplane, and flies off. Understanding = a crumpled thing becoming a
thing that flies. That is the whole brand, and it is wordless.

End line: **"Every doubt, answered. Brainback."**
Tagline for the series: **"Give it back."** (to the doom-scroll: time, focus, brain)

### Why paper

- It is Varma-practical: we fold them for real, with stop-motion and
  puppetry, then only clean up with AI and compositing.
- It is every Indian kid's material — ruled Classmate-style pages (unbranded),
  graph paper for maths, a torn back page.
- It scales: one Doubtling in a bedroom, ten thousand paper planes over a
  school ground in the hero film.

---

## 3. The films

### Hero film — "Flight" (60s, cut-downs 30s / 15s)

1. **0–8s.** 11:40 PM, Kochi. A girl in bed, phone light on her face,
   thumb scrolling. Behind her, notebooks on a desk. One page twitches.
2. **8–18s.** A Doubtling tears itself out and climbs onto her pillow. Then
   another. She ignores them; they pile up — on the fan blades, in her
   slippers, one in her tea.
3. **18–30s.** She switches to Brainback. A 60-second lesson plays. She
   frowns, types a follow-up. The tutor answers. The nearest Doubtling
   unfolds, refolds, and glides out of the window.
4. **30–45s.** Montage across India, same beat: a boy on a Mumbai local, a
   girl at a Jaipur tuition-centre bus stop, twins in a Guwahati kitchen.
   Doubtlings everywhere, each resolving into a plane.
5. **45–55s.** Morning assembly, wide. Thousands of paper planes rise off a
   school ground against a monsoon sky. The one Incredible-India frame.
6. **55–60s.** Black. **Every doubt, answered.** Logo. Four-note sting.

### The shorts (15–20s each, drop one a day)

| # | Title | The one gag |
|---|---|---|
| 1 | **Too Shy** | Hand half-raised in class, Doubtling hides in her sleeve. At home she asks Brainback. It flies out of the sleeve. |
| 2 | **But Why?** | A tiny Doubtling asks why; the answer spawns a smaller one; and a smaller one — a matryoshka of doubts — until the tutor answers the last and they all fly off as one flock. *(sells follow-up questions)* |
| 3 | **Doomscroll** | Thumb scrolls; a Doubtling lies on the phone like a sunbather getting paler. Switch to Brainback; it gets its colour back. *(sells "gives back")* |
| 4 | **Exam Morning** | A bag stuffed with Doubtlings, zip straining. Bus ride, five quizzes, zip closes. |
| 5 | **Amma Checks** | Mother peeks at the phone suspiciously; sees a quiz, not comments. The Doubtling salutes her. *(sells parental oversight — claim to confirm)* |
| 6 | **Graph Paper** | A maths Doubtling folded from graph paper is angular and grumpy. It unfolds into a perfect parabola flight path. |

Each short: one location, one kid, one Doubtling, the sting. No dialogue.

---

## 4. The agents

One orchestrating session plays director and holds the treatment; the rest
are subagents with a narrow brief each. Humans sit at three gates.

| Agent | Job | Tools / inputs | Output |
|---|---|---|---|
| **Director (orchestrator)** | Holds the treatment, briefs every other agent, rejects anything that breaks the §1 rules. | This doc, the claims sheet | Shot list, approvals |
| **Brand researcher** | Confirms what Brainback is, audience, tone, competitors' ads (so we don't echo them). | WebSearch/WebFetch, client brief | Brand brief, claims sheet v1 |
| **Script & board writer** | Wordless scripts, beat sheets, storyboard prompts. | Treatment | Scripts, board prompts |
| **Asset scout** | Finds every open asset in §5 and checks its licence *at download time*. | WebSearch, Hugging Face, Wikimedia, Freesound, Poly Haven | `assets/ledger.csv` with URL, licence, author, date |
| **Rights / licence auditor** | Independent second read of the ledger. Rejects NC, ND, unclear, or "free for personal use". | Ledger, licence texts | Pass/fail per asset |
| **Image/board generator** | Storyboards and style frames. | ComfyUI + FLUX.1 [schnell] / SDXL on a GPU box | Boards, style frames |
| **Motion generator** | Doubtling animation passes, plates, crowd planes. | Blender (+ Blender MCP), Wan 2.2 via ComfyUI, stop-motion capture | Shots |
| **Music & sound** | The four-note tune and all foley. | ACE-Step, Freesound CC0, Audacity/Ardour | Stems, sting |
| **Localisation** | End line in 10+ Indian languages, captions. | IndicTrans2, Indic Parler-TTS, Whisper | Supers, VO, SRTs |
| **Editor / finisher** | Assembly, grade, deliverables. | FFmpeg, Kdenlive, Blender VSE, Natron | Masters per platform |
| **QC** | Loudness, safe areas, captions, brand, likeness, child-safety review. | ffmpeg `loudnorm`, checklist | QC report |

**Human gates:** (1) client approves concept + claims sheet; (2) director
approves animatic; (3) client + legal approve final and licence ledger.

**Real people.** Any child on screen is a cast, consented, chaperoned actor —
not a generated face. AI video is for the Doubtlings, the planes and set
extensions only. That keeps the ad honest and keeps us out of likeness and
minor-safety trouble.

---

## 5. Open assets, step by step

Licences as published at the time of writing. The asset scout re-checks each
one on the day it is downloaded and records it in the ledger — model
licences in particular change between versions.

### Step 1 — Research and references

| Need | Source | Licence |
|---|---|---|
| Kerala / Mumbai / Guwahati reference stills for boards | Wikimedia Commons | per-file CC0 / CC BY / CC BY-SA — record each |
| Look references | Pexels, Unsplash, Pixabay | own free-use licences (not CC); fine for boards, check before shipping in-frame |

### Step 2 — Script and storyboard

| Need | Source | Licence |
|---|---|---|
| Board frames | **FLUX.1 [schnell]** (Black Forest Labs) | Apache 2.0 — **not** FLUX.1 [dev], which is non-commercial |
| Alternative | **SDXL base** | CreativeML Open RAIL++-M (commercial allowed with use restrictions) |
| Node pipeline | **ComfyUI** | GPL-3.0 (tool licence; outputs are ours) |
| Animatic | **Blender** Grease Pencil / **OpenToonz** / **Krita** | GPL / BSD / GPL |

### Step 3 — Build the Doubtling

| Need | Source | Licence |
|---|---|---|
| Real paper, real folds, a phone on a copy stand | — (stop-motion, the Varma way) | ours |
| Capture | **Entangle** or **qStopMotion** | GPL |
| 3D double for wide shots | **Blender** (cloth + Rigify) | GPL |
| Paper textures | **ambientCG**, **Poly Haven** | CC0 |
| Studio / bedroom lighting HDRIs | **Poly Haven** | CC0 |
| Props (desk, fan, lamp) | **Poly Haven** models, **Kenney** | CC0 |
| Drive Blender from the agent | **blender-mcp** (open-source MCP server) | MIT — verify repo |

### Step 4 — Shoot plates and generated shots

| Need | Source | Licence |
|---|---|---|
| Live-action plates | Our shoot (cast kids, real homes) | ours, with releases |
| Plane flocks, set extension, sky | **Wan 2.2** (text/image-to-video) via ComfyUI | Apache 2.0 |
| Alternative | **LTX-Video** | open weights, own licence — auditor checks revenue terms |
| Stock sky / monsoon plates | Pexels / Pixabay video | free-use licences, record each |
| Compositing | **Natron** | GPL |
| Tracking / roto | Blender motion tracker; **SAM 2** for masks | GPL; Apache 2.0 |

### Step 5 — Music and sound

| Need | Source | Licence |
|---|---|---|
| The four-note theme | Composed; sketch variations with **ACE-Step** (v1-3.5B Apache 2.0 / 1.5 MIT — **not** 1.5 XL weights) | as noted |
| Paper foley (rustle, fold, flutter) | **Freesound**, filtered to CC0 | CC0 |
| Instruments | **Musical Artifacts**, **VSCO 2 CE** samples | CC0 / check each |
| DAW | **Ardour**, **Audacity** | GPL |
| Do **not** use | MusicGen weights (CC BY-NC), Stable Audio Open without checking its community licence | — |

### Step 6 — End line, languages, captions

| Need | Source | Licence |
|---|---|---|
| Translate "Every doubt, answered." | **IndicTrans2** (AI4Bharat) + a native-speaker check per language | MIT |
| Optional VO for the end line | **Indic Parler-TTS** (21 languages) | Apache 2.0 |
| Captions / SRT | **Whisper** | MIT |
| Type | **Google Fonts**: Baloo 2, Mukta, Noto Sans (Devanagari, Malayalam, Tamil, Bengali, …) | OFL |
| Do **not** use | XTTS-v2 (Coqui Public Model Licence, non-commercial) | — |

### Step 7 — Edit, grade, deliver

| Need | Source | Licence |
|---|---|---|
| Edit | **Kdenlive** or Blender VSE | GPL |
| Encode, loudness, crops | **FFmpeg** (`loudnorm` to −24 LUFS TV / −14 LUFS social) | LGPL/GPL |
| Grade | Kdenlive / Natron LUTs; OpenColorIO ACES config | BSD |
| Motion graphics end card | **Motion Canvas** or **Manim** | MIT |

---

## 6. Connectors

| Connector | Use |
|---|---|
| **GitHub** (connected) | This repo: plan, scripts, ledger, render scripts, reviewable history |
| **Claude Docs** (connected) | The treatment and scripts as a living doc the client can comment on |
| **Google Drive** | Heavy media hand-off (plates, renders) — not in git |
| **Slack** | Daily-drop approvals for the shorts |
| **Figma** | End card, social crops, thumbnails |
| **Hugging Face** (MCP) | Pull models and read model cards / licences from the agent |
| **A GPU box** | Not a connector — this container has none. ComfyUI and Blender renders run on a rented GPU (24 GB+ for Wan 2.2 at 720p) exposed to the agents over its API |

Only GitHub and Claude Docs are connected in this session; the rest need
setting up in claude.ai connectors before the pipeline can use them.

---

## 7. Claims sheet (client signs before scripts lock)

| Claim implied | Film | Status |
|---|---|---|
| Answers follow-up questions | Hero, But Why? | from public description — confirm |
| 60-second lessons + quizzes | Hero, Exam Morning | from public description — confirm |
| Parental oversight / no comments | Amma Checks | from public description — confirm |
| Works in Indian languages | Localised end cards | **unknown** — do not imply until confirmed |
| Free | none (kept out of creative) | — |

---

## 8. Order of work

1. Brand researcher confirms the product; client signs §7.
2. Script agent writes hero + 6 shorts; director cuts to the best 4.
3. Asset scout builds `assets/ledger.csv`; auditor passes it.
4. Fold 20 real Doubtlings; test one unfolding on a copy stand. **If the
   unfold isn't charming in stop-motion, the campaign isn't ready** — no
   amount of generation fixes that.
5. Animatic in Blender with temp music; human gate 2.
6. Shoot plates (two days, four homes, one school ground).
7. Generate flocks and set extensions; composite; theme and foley.
8. Localise end line; QC; human gate 3; deliver 16:9, 9:16, 1:1.
