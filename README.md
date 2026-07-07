# AI Documentary Making 101 — Full Project Source

**A ~6-minute documentary — script, narrator, exhibits, voice, SFX, and edit — made entirely with AI tools, and directed almost entirely by Claude Code.** This repo is the complete, reproducible source: every prompt, every script, every asset, in the exact order they were used to build the final video.

Final video: **[link to be added]**

---

## What's in this repo

```
docs/                       planning + prompts (the "how")
  DOCUMENTARY_PLAN.md          original production plan (concept, tone, early draft script)
  SCRIPT_v2_desert.md          the SHOOTING SCRIPT actually used (desert/helicopter structure)
  CHARACTER_SHOTS_veo.md       the narrator shot list + non-repetitive cutting map
  VOX_EXHIBIT_PROMPTS.md       verbatim ChatGPT prompts for all 9 Vox exhibit clips
  VO_SCRIPT_SEGMENTS.md        original voiceover segment map (SEG_01-21)
  GEMINI_VIDEO_PROMPTS.md      copy-paste Gemini/Veo prompts (fallback path, pre-Vertex AI)
scripts/                     the actual assembly pipeline (run in this order)
  build_film.py                 renders all 32 narrative beats (VO + character/exhibit clips + SFX)
  fix_sync_beats.py             re-renders beats where VO was shorter than the clip (removes sped-up motion)
  fix_clip_swap.py              swaps in a more natural walking/gesture clip for 5 beats
preview/
  preview_720p.mp4              compressed 720p preview of the final cut (full quality is on YouTube)
```

Binary assets (character images, Veo clips, Vox exhibit videos, voice, SFX, music, and the pre-rendered beats) are **not** committed to git — they're attached as [GitHub Release](../../releases) downloads instead, so the repo itself stays small and fast to clone. See **Asset bundles** below.

---

## Prerequisites

| Need | Used for | Tier |
|---|---|---|
| Google Cloud project + Vertex AI enabled | Veo 3 (character clips) | Billed, but Veo is the only paid step here |
| ElevenLabs account | Voice (narration) + sound-effects generation | Free tier is enough for ~20 short lines |
| ChatGPT (GPT Image) | Vox exhibit stills | Free tier, ~1-2 images per ~30 min |
| Higgsfield.ai account | Vox exhibit animation (image→video) | Free — use the **Unlimited toggle** models only ("Enhanced Seedance 2.0 Fast"), never paid credits |
| ffmpeg + ffprobe | All video/audio assembly | Free |
| Python 3 | Running the assembly scripts | Free |
| CapCut (desktop) | Final timeline assembly + export | Free |

---

## Step 1 — Character design

The masked narrator ("The Boring Studio") started from two user-supplied reference images (included in the asset bundle as `character/`):
- A full character turnaround/design sheet (palette `#0D0D0D` / `#1A1A1A` / `#2B2B2B` / `#E04A6A` / `#FF7A00` / rust, materials called out on the sheet itself)
- A single canonical reference photo (`Screenshot (498).png`) used as the exact image-to-video seed for every Veo shot, to guarantee the mask/suit/tie design never drifts between clips

If regenerating this character from scratch (no reference images), the working verbal description used throughout is:
> *"A man in a tailored matte-black suit, black leather gloves, a rusted orange-brown metal mask fully hiding his face with narrow dark eye-slits (mesh, not glass), black shirt, dark patterned tie."*

## Step 2 — Generate the narrator (character) clips

All narrator shots are **image-to-video** (not text-to-video) from the single reference photo above — this is the trick that keeps the mask/suit design identical across every clip. Generated via **Vertex AI Veo 3**, model `veo-3.0-fast-generate-001`:

```
POST https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/{LOCATION}/publishers/google/models/veo-3.0-fast-generate-001:predictLongRunning
{
  "instances": [{
    "prompt": "<shot description, see below>",
    "image": {"bytesBase64Encoded": "<base64 of Screenshot (498).png>", "mimeType": "image/png"}
  }]
}
```
Then poll the same model's `:fetchPredictOperation` until done; the result video is at `response.videos[0].bytesBase64Encoded`.

Shot list (full descriptions + the non-repetitive cutting map are in `docs/CHARACTER_SHOTS_veo.md`):

| File | Shot |
|---|---|
| `A1_aerial` | Aerial over dunes, helicopter banking low (reused as-is throughout) |
| `A2_heli_landing` | Helicopter lands, dust rolls toward camera |
| `A3_steps_out_v3` | Hero shot — steps out of the helicopter, walks forward, stops |
| `R1_closeup_v3` | Extreme close-up on the mask, slow push-in |
| `R2_front_medium_v3` | Waist-up "main talking" shot, gesturing |
| `R3_wide_power_v3` | Wide shot — helicopter, guards, SUVs visible behind him |
| `R4_turn_v3` | 3/4 turn shot *(superseded — see Step 2b)* |
| `R5_low_angle_v3` | Low angle, powerful/still |
| `R7_walk_v3` | Slow walk toward camera |
| `R8_golden_v3` | Golden-hour wide, long shadows (reflection scene) |
| `A9_departure_v3` | Walks back to the helicopter, lifts off into the sunset |

## Step 2b — The natural-motion fix

`R4_turn_v3` looked stiff/robotic on review. It was replaced everywhere it was used with a hand-picked 7-second segment (walking + natural hand/head gesture, skipping the helicopter-descent portion) extracted from a separately user-generated reference clip:

```bash
ffmpeg -i "source_clip.mp4" -ss 3.0 -t 7.0 -c:v libx264 -crf 16 -an RNEW_walktalk_v1.mp4
```
This `RNEW_walktalk_v1.mp4` is included in the asset bundle. `scripts/fix_clip_swap.py` re-renders the 5 affected beats using it instead of `R4_turn_v3`.

## Step 3 — Generate the 9 Vox exhibit clips

The "evidence" clips (Vox-style infographic explainer, warm paper/collage look) are a **separate visual world** from the narrator — full prompts (verbatim ChatGPT conversations for both the still image and the Higgsfield animation prompt) are in `docs/VOX_EXHIBIT_PROMPTS.md`.

Pipeline per exhibit: ChatGPT (GPT Image) generates the still → the still is fed to **Higgsfield "Enhanced Seedance 2.0 Fast"** (image-to-video, **Unlimited toggle only — never paid credits**) with a detailed shot-by-shot animation prompt → the resulting 15s 720p clip is upscaled to 2560×1440 (`master/vox_2k/VOX_01...VOX_09`).

Topics, in order: future of filmmaking → old workflow vs AI → Remotion+Higgsfield overview → Remotion deeper → Remotion's limits → Higgsfield deeper → Higgsfield's library → Higgsfield's limits/cost → Claude Code orchestration (the reveal).

## Step 4 — Voiceover

ElevenLabs, voice **Brian** (`nPczCjzI2devNBz1zQrb` — "Deep, Resonant and Comforting"), model `eleven_multilingual_v2`:
```json
{"stability": 0.40, "similarity_boost": 0.85, "style": 0.30, "use_speaker_boost": true, "speed": 0.90}
```
Line-by-line script is in `docs/SCRIPT_v2_desert.md` (current) — `docs/VO_SCRIPT_SEGMENTS.md` has the original numbering (`SEG_04`-`SEG_21` are reused as-is; `SEG_V2_01`-`03` are new desert-arrival lines that replaced the old cold open).

## Step 5 — SFX

ElevenLabs sound-generation API. Cues used: rotor spin-up/spin-down, helicopter idle/takeoff, footsteps in sand, suit rustle, desert wind bed (looped, low), desert ambience, two sub-boom impacts (title card + reveal beat). All included as `sfx/*.mp3` in the asset bundle.

## Step 6 — Music

6 pre-composed 30-second cues (sub-bass drone → exposition pulse → rising reveal → tension drone → reflective piano → climax swell), included as `music/*.mp3`. These are licensed/owned tracks — swap in your own if reproducing this publicly.

## Step 7 — Assemble

Run in this exact order from inside the folder containing `master/`, `narrator/`:

```bash
python scripts/build_film.py        # renders all 32 beats (VO + clips + SFX) into master/final_scenes/
python scripts/fix_sync_beats.py    # re-renders beats where VO was shorter than the clip, at natural speed
python scripts/fix_clip_swap.py     # swaps R4_turn_v3 -> RNEW_walktalk_v1 in the 5 beats that used it
```

Then fix the exhibit/narration order (two Vox clips play out of order relative to the narration otherwise — see below) and build a correctly-numbered copy for import:

```python
ORDER = [
    'S1a_aerial','S1b_title','S1c_landing','S1d_stepsout',
    'S2a_vo1','S2b_vo2','S2c_vo3',
    'S3a_vo04','S3d_vox2','S3c_vo05','S3b_vox1','S3e_vo06',      # vox1/vox2 swapped
    'S4a_vo07','S4b_vox3','S4c_vo08','S4d_vox4','S4f_vo09','S4e_vox5','S4h_vo10','S4g_vox6','S4i_vox7',  # vox5/vo09 and vox6/vo10 swapped
    'S5a_vo11','S5b_vox8',
    'S6a_vo12','S6b_vo13','S6c_vox9','S6d_vo14',
    'S7a_vo15','S7b_vo16','S7c_vo17',
    'S8a_vo18','S8b_vo19','S8c_departure',
]
```
*(Why: the narrator would say "it has a ceiling" or "Higgsfield" a beat **after** the exhibit that illustrates it had already played. The fix reorders so narration always introduces a topic before its exhibit shows it.)*

A separate music timeline (6 cues, crossfaded, matched to the film's exact runtime) is built independently — voice+video+SFX and music are always kept as separate deliverables so music can be re-balanced without re-rendering anything.

## Step 8 — Final cut (CapCut)

1. New project → import all 33 ordered beat clips + the music track.
2. Drag all 33 clips onto the timeline in numeric order (they concatenate automatically, no gaps).
3. Music on its own track, same start point, volume **-15dB** (sits under dialogue/SFX, doesn't compete).
4. Export 1080p, H.264, mp4.

---

## Asset bundles ([v1.0 release](https://github.com/zanni098/ai-documentary-101/releases/tag/v1.0))

| Bundle | Contents | Size |
|---|---|---|
| [`core-assets.zip`](https://github.com/zanni098/ai-documentary-101/releases/download/v1.0/core-assets.zip) | Character images + all 12 narrator Veo clips + all 9 Vox exhibit clips (2K) + voice + SFX + music + the 33 pre-rendered final beats | ~590MB |
| [`archive-exploration.zip`](https://github.com/zanni098/ai-documentary-101/releases/download/v1.0/archive-exploration.zip) | Early sample renders, the rejected Remotion-only attempt, superseded (wrong-character) narrator test clips | ~335MB |
| [`archive-vox-source.zip`](https://github.com/zanni098/ai-documentary-101/releases/download/v1.0/archive-vox-source.zip) | Original 720p Vox stills + raw Higgsfield renders before 2K upscale (the source for `docs/VOX_EXHIBIT_PROMPTS.md`) | ~280MB |

Grab `core-assets.zip` if you just want to reproduce the pipeline above. The archive bundles are kept for transparency/history only — not needed to rebuild the video.

---

## Credits

Built with Claude Code (Anthropic), Google Vertex AI (Veo 3), ElevenLabs, ChatGPT (GPT Image), Higgsfield.ai, ffmpeg, and CapCut.
