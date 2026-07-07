# AI DOCUMENTARY MAKING 101
### Production Plan — Moriarty-style documentary wrapping the Vox "AI filmmaking" clips
*Planning draft — nothing rendered until you say "go".*
*On-screen title: **"AI DOCUMENTARY MAKING 101"** (styled cinematically — neon + glitch — so the tutorial-sounding title lands as a provocative hook against the ominous narration).*

---

## 0. LOGLINE

A masked operator — **The Boring Studio** — sits alone in a neon-lit room and confesses that the film you are watching was directed entirely by a machine. Exhibit by exhibit (your 9 Vox clips) he walks you through *how* the machine works — the code, the models, the single agent pulling every string — and then turns the knife: *if a machine can direct, what is a filmmaker for?*

Two worlds, cut against each other:
- **The Vox world** (your existing clips) = the *evidence* — warm paper, stop-motion, infographic. Stays exactly as-is.
- **The Moriarty world** (new) = the *narrator* — cold, cinematic, neon-and-shadow, deep voice, hard cuts. This is the connective tissue.

**Runtime target:** ~8:00. **Aspect:** 16:9, 2K master. **Tone:** ominous, intelligent, seductive.

---

## 1. THE TWO VISUAL LANGUAGES

| | VOX WORLD (existing) | MORIARTY WORLD (new narrator) |
|---|---|---|
| Look | Warm cream paper, torn edges, gridlines, grain | Near-black, teal-shadow + neon pink/orange accents |
| Motion | Stop-motion "on twos", paper unfold, push-ins | Slow cinematic dolly, rack focus, hard cuts, glitch |
| Framing | Full-frame infographic pages | Extreme close-ups: mask eye-slit, mic, fingers, screen-glow |
| Grade | Editorial, low-sat warm | Cinematic teal/orange, crushed blacks, film grain, 2.35 bars |
| Role | Evidence / B-roll | Narration / spine |

The contrast *is* the style: we cut from a cold masked stare into a warm paper exhibit, and back. The whiplash is the point.

---

## 2. ASSET INVENTORY (confirmed)

**Have (9 Vox clips, 15s each, 1280×720 → ~2:15 total):**
1. `sec_00-15` — "The future of filmmaking" (intro)
2. `sec_15-30` — Old workflow (camera/edit/months) → AI pipeline
3. `sec_30-45` — Remotion + Higgsfield: "one creative flow"
4. `sec_45-60` — Remotion, deeper
5. `sec_60-75` — "Remotion is powerful. But it has limits."
6. `sec_75-90` — Higgsfield, deeper
7. `sec_90-105` — "Higgsfield has a vast library of models."
8. `sec_105-120` — "Higgsfield… but it has limitations." (cost)
9. `sec_120-135` — "One agent. The whole production." (Claude Code)

**Have (character bible):** the 2 uploaded reference images — the cinematic desk shot + the full character sheet (turnaround, close-ups, lighting refs, palette `#0D0D0D / #1A1A1A / #E04A6A / #FF7A00 / rust`, materials). This is enough to generate consistent narrator shots.

**Need to make (new):** ~10–14 narrator shots (see §4), 1 voiceover track, 4–6 music cues, title/lower-third/end cards.

---

## 3. TECHNICAL PIPELINE (all free / zero Higgsfield credits)

| Step | Tool | Notes |
|---|---|---|
| **1. Upscale 720p→2K** | **DaVinci Resolve** (free) — Super Scale 2× → 1440p, or Topaz if you have it | Higgsfield's own upscale costs credits → not used. ffmpeg lanczos is the fallback but softer. |
| **2. Narrator shots** | **Higgsfield free** *Enhanced Seedance 2.0 Fast* (image→video, Unlimited toggle) | From the reference images. **No lip-sync needed — the mask has no mouth** (this is the Moriarty cheat code). Subtle motion only. |
| **3. Voiceover** | **ElevenLabs** (MCP, deep cinematic male voice) | + post: low-EQ boost, plate reverb, −1 to −2 semitone for weight. |
| **4. Music** | **ElevenLabs music-gen** (original, clean rights) *or* your licensed files | ⚠️ I can't rip audio off the YouTube playlist (copyright) — see §5. |
| **5. Assembly / edit** | **Option A:** programmatic first cut (ffmpeg/Remotion timeline — fast, reproducible, frame-perfect audio sync). **Option B:** DaVinci Resolve project you polish by hand. | Recommend A for a full 8-min master fast, then hand you a Resolve project for polish. |
| **6. Style calibration** | Gemini-in-browser review of your Moriarty reference (`qOq2vhBNUA0`) | To lock exact cut-rhythm, voice tone, grade before final. |

**Blender / After Effects:** available if we want 3D mask parallax or advanced glitch/text — optional polish, not required for v1.

---

## 4. THE NARRATOR SYSTEM (how the mask "talks")

The mask has **no mouth**, so we never lip-sync. Instead the character *reads as talking* through:
- **Cutting to him on emphasis beats** (voice hits a hard line → cut to a slow push-in on the mask).
- **Body language:** slow head tilt, lean toward the mic, fingers steepling, hand on keyboard, a slow turn to camera.
- **Environment as punctuation:** neon flicker, screen-glow shifting across the mask, "LIVE ON AIR" buzzing, a wisp of smoke.

**Shot list to generate (Higgsfield free, ~15s each, then trimmed):**
1. Cold-open — extreme close on mask eye-slit, screen glow, tiny head rise
2. Wide studio reveal — pull-back, neon duck logo + mic
3. Push-in — mask centered, slow dolly, LIVE ON AIR behind
4. Hands on keyboard, laptop glow (duck logo)
5. Profile — leaning to the mic, neon rim light
6. Over-shoulder — laptop screen, code reflection on mask
7. Low-angle — mask looking down at camera, menacing
8. Slow turn — 3/4 back to 3/4 front
9. Reflective — mask lit only by one warm bar, still
10. Sign-off — lean back, neon logo bloom, then to black
*(2–4 spare angles from the character-sheet turnaround for variety.)*

**Voice spec (Moriarty):** deep baritone, slow, deliberate, lots of *silence between lines*, near-whisper intensity that swells on the thesis lines, zero hype. Think late-night, close-mic, a little menace. Direct address ("you").

---

## 5. MUSIC PLAN

Moriarty scores lean on: a **sub-bass drone**, a **ticking/pulse** under exposition, a **rising synth** on reveals, a **sparse piano** on the reflective turn, and **one big swell** at the sign-off.

⚠️ **Copyright:** I cannot download audio from your YouTube playlist (`…IdC2nG`) — ripping it would be infringement even for personal use. **Two clean routes:**
- **(Recommended)** I generate an original score with ElevenLabs music-gen to hit those exact moods (6 short cues) — 100% clean, tailored to the cut.
- **Or** you drop licensed track files (from Epidemic/Artlist/Uppbeat or files you own) into `doc_1/music/` and I edit to them.

Cue map: **C1 drone** (cold open) · **C2 pulse** (acts 1–2) · **C3 rising** (Higgsfield reveal) · **C4 tension** (the "cost" turn) · **C5 piano** (reflective) · **C6 swell→cut** (outro).

---

## 6. FULL SCRIPT (≈8:00)

> Format — **[TIME] ON-SCREEN › VO LINE** · *(delivery)* · ENV · ♪ music
> VO = the masked narrator. Vox clips play full-frame with their own internal audio ducked under VO.

### COLD OPEN
**[0:00–0:12]** ON: black → extreme close on mask eye-slit, faint screen glow.
› *"Every film you've ever loved… needed a camera. A crew. A pair of human hands."*
*(slow, near-whisper, a pause after 'hands')* · ENV: near-black, one neon edge · ♪ C1 sub-drone in.

**[0:12–0:28]** ON: slow push-in on the full mask, LIVE ON AIR buzzing behind.
› *"This one needed none of that. No camera. No crew. No director in the room. Only a machine — and a single sentence telling it what to dream."*
*(measured, cold)* · ENV: studio desk, neon pink rim · ♪ drone tightens.

**[0:28–0:35]** ON: hard cut — mask fills frame, dead still.
› *"Let me show you how that's possible. And why it should terrify every filmmaker alive."*
*(flat, threat under it)* · ♪ silence → hit.

### TITLE
**[0:35–0:42]** ON: title card — **AI DOCUMENTARY MAKING 101** (neon/glitch treatment, Vox-yellow slash under it), glitch in/out. ♪ C2 pulse starts.

### ACT 1 — THE CLAIM
**[0:42–0:58]** ON: push-in, narrator leans to mic.
› *"They told you filmmaking was an art. Vision. Instinct. Something a person feels. Watch what happens when you hand that feeling… to code."*
*(building)* · ENV: profile, neon rim · ♪ pulse.

**[0:58–1:18]** ON › **VOX CLIP 1** (`sec_00-15`, full-frame) under VO tail:
› *"They call it the future of filmmaking. It's already here."*
*(let the clip breathe; VO out by 1:04)* · ♪ pulse ducks under clip audio.

### ACT 2 — THE OLD WORLD DIES
**[1:18–1:34]** ON: hands on keyboard, screen glow.
› *"For a hundred years the recipe never changed. Cameras. Editors. Motion designers. Months of work for two minutes of film."*
*(dry, almost bored — 'boring studio')* · ♪ pulse.

**[1:34–1:52]** ON › **VOX CLIP 2** (`sec_15-30`) full-frame.
› *(VO lead-in, then silent under clip)* "Today, one pipeline swallows all of it."* · ♪ duck.

**[1:52–2:10]** ON: low-angle mask, menacing.
› *"Prompt. Network. Image. Video. Code. Five steps that used to be five departments — now they're five words."*
*(slow, landing each word)* · ♪ pulse rises a step.

### ACT 3 — THE TWO TOOLS
**[2:10–2:20]** ON: over-shoulder, code reflected on mask.
› *"It runs on two tools. One writes. One dreams."* *(cryptic)* · ♪ C2.

**[2:20–2:38]** ON › **VOX CLIP 3** (`sec_30-45`) full-frame. *(VO silent — let the 'one creative flow' land.)*

**[2:38–2:55]** ON: narrator, still.
› *"The first is called Remotion. It doesn't shoot video. It *computes* it. Every frame is math. Change one number — the whole film re-renders."*
*(fascinated)* · ♪ pulse.

**[2:55–3:15]** ON › **VOX CLIP 4** (`sec_45-60`) then **CLIP 5** (`sec_60-75`) back-to-back. *(VO out.)*

**[3:15–3:30]** ON: mask, screen-glow shifting.
› *"Powerful. But it has a ceiling. Code can't imagine a face it's never seen. For that… you need the second tool."*
*(turn)* · ♪ C3 rising begins.

### ACT 4 — THE DREAM MACHINE
**[3:30–3:48]** ON › **VOX CLIP 6** (`sec_75-90`) full-frame. ♪ C3 swells under it.

**[3:48–4:05]** ON: slow turn, 3/4 to front.
› *"Higgsfield. A library of models that don't render reality — they hallucinate it. Cinematic. Anime. Game worlds. Ads. One prompt… infinite possibilities."*
*(seductive)* · ♪ C3.

**[4:05–4:22]** ON › **VOX CLIP 7** (`sec_90-105`) full-frame. *(VO out.)*

**[4:22–4:40]** ON: narrator, quieter.
› *"But every dream has a price. And this one bills by the second."*
*(low, warning)* · ♪ C4 tension in — drone + ticking.

**[4:40–5:00]** ON › **VOX CLIP 8** (`sec_105-120`) full-frame. ♪ tension under it.

### ACT 5 — THE ORCHESTRATOR (REVEAL)
**[5:00–5:12]** ON: hard cut, mask dead-center, still.
› *"So who holds it all together? Who reads the script, writes the code, drives the machine, and never sleeps?"*
*(each clause a beat)* · ♪ C4 pulls back to a single note.

**[5:12–5:20]** ON: push-in, faster.
› *"Not a studio. Not a team. One agent."*
*(hard)* · ♪ silence.

**[5:20–5:40]** ON › **VOX CLIP 9** (`sec_120-135`, the Claude orchestration reveal) full-frame. ♪ C3-reprise swells big.

**[5:40–5:58]** ON: low-angle, neon bloom.
› *"It plans the shots. Writes every component. Calls the models. Assembles the cut. One agent — running the entire production."*
*(awe + dread)* · ♪ hold big.

### ACT 6 — THE HUMAN QUESTION (reflective turn)
**[5:58–6:20]** ON: mask lit by a single warm bar, everything else black. Very still.
› *"Which leaves me with a question I can't put down. If the machine writes, shoots, edits, and directs…"*
*(drop to a whisper)* · ♪ C5 sparse piano.

**[6:20–6:42]** ON: extreme close, eye-slit.
› *"…then what, exactly, is left for us? Maybe the taste. Maybe the *why*. Maybe the one thing it can't fake — a reason to press record."*
*(intimate)* · ♪ piano.

**[6:42–7:05]** ON: slow pull-back revealing the whole dark studio, the person small in it.
› *"The camera didn't die. It just… stopped needing us to hold it."*
*(let it hang)* · ♪ piano + low drone.

### OUTRO
**[7:05–7:25]** ON: narrator leans back into shadow.
› *"This video? Written by a machine. Shot by a machine. Edited by a machine. And narrated… by whatever I am."*
*(a dark half-smile in the voice)* · ♪ C6 swell begins.

**[7:25–7:45]** ON: the neon duck logo blooms; "The Boring Studio" resolves.
› *"I'm The Boring Studio. The work speaks for itself. It always did."*
*(final, calm)* · ♪ swell peaks.

**[7:45–8:00]** ON: end card — logo + subscribe beat, glitch, then **cut to black + silence.**
› *(no VO — one last neon buzz, then nothing.)* · ♪ hard cut to silence.

---

## 7. BUILD ORDER (once you say "go")

1. **Upscale** the 9 Vox clips → 2K (DaVinci Super Scale). *(no credits)*
2. **Generate** ~12 narrator shots (Higgsfield free Seedance from the reference images). *(no credits)*
3. **Record VO** (ElevenLabs deep voice) from the script; get word timings.
4. **Score** 6 cues (ElevenLabs music-gen) — or drop in your licensed files.
5. **Grade** narrator shots to the Moriarty look (teal/orange, grain, 2.35 bars).
6. **Assemble** the 8-min master (programmatic first cut) with VO/music/clip sync + text cards + transitions.
7. **Review vs. reference** (Gemini) → tighten cuts → export 2K master + hand off Resolve project.

---

## 8. LOCKED DECISIONS ✅
1. **Title:** **"AI DOCUMENTARY MAKING 101"** — cinematic/neon treatment, ~8 min (flexible).
2. **Music:** **original ElevenLabs score** — 6 clean cues tailored to the cut (no playlist ripping).
3. **Assembly:** **Full DaVinci Resolve build** — final edit assembled/graded in DaVinci Resolve.
4. **Voice:** **I pick a deep ElevenLabs documentary voice** + post (low-EQ, reverb, weight).

### Notes on the DaVinci Resolve build
- I'll generate + grade every asset first (upscaled Vox clips, narrator shots, VO, music, title/end cards), organized in `doc_1/master/`.
- Then build the timeline in Resolve. Two ways to do it, I'll use whichever your setup allows:
  - **Scripted** via Resolve's Python API (`DaVinciResolveScript`) — auto-import media + auto-place clips/VO/music at the script timecodes. *(Requires Resolve installed with scripting enabled; I'll verify first.)*
  - **Guided manual** — I hand you a Resolve project + an EDL/timing sheet and drive the assembly step-by-step.
- Final grade (teal/orange + grain + 2.35 bars on narrator shots), transitions, and audio ducking done in Resolve; export 2K master.
- ⚠️ Requires **DaVinci Resolve installed** on this machine — I'll confirm before the assembly step.
