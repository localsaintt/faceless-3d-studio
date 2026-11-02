---
type: research
source: Morrow "What If 3D Kit v3" (code-only copy shared by the owner, read-only analysis 2026-11-02)
updated: 2026-11-02
---
# What If 3D Kit v3: analysis and comparison

**Licence (their TERMS):** the kit is licensed to the owner personally while a paying member. It may be modified for own use, but **may not be shared, re-uploaded or published, in whole or in part** (including modified copies), or used for a competing product. Standard includes 15 finished videos/month and a membership check gates every new video. The kit's code was read for analysis only; **none of it is copied into this repository.** What follows is our own description and our own conclusions.

## What the kit is
- **Engine:** "Frontier 3D", a large three.js (WebGL) engine run in headless Chromium on the computer's GPU (Metal on Mac). Spec-driven (JSON scene specs); output 1080p, motion blur by sub-frames; final What If videos at 60 fps. Reported ~10 min for a 61 s video on an M-series Mac.
- **Library:** dozens of effect and set modules (tsunami wall, megatsunami, hurricane, tornado, lightning, volcano, quake, wildfire, asteroid, blast, shock, space) and location sets (Miami, NYC, Chicago, Las Vegas, Coney Island, Golden Gate, a ballpark, Titanic, Yellowstone, Dubai…), plus a large human/vehicle/props library (crowds, cars, boats, homes, furniture), **first-person hands**, and look presets (documentary, diorama, cel, clay, noir, hologram, a game look).
- **Camera system:** first-person (FPV) runs with eye height, glances, stumbles and breathing bob; keyed composed shots; lens tracks; dolly zoom; **rack focus** with physically placed focus; designed impact shakes; handheld drift; a QA pass that rejects bumps, jumps, flips, too-fast head turns and cameras inside solids.
- **World clock:** world time separate from screen time, with eased rate keys (real → ~6× slower → real; fast-forward allowed). Every effect is timed in world time.
- **Automatic QA:** checks that walkers face where they go and feet don't slide, vehicles stay on roads with turning wheels, nothing floats or sinks, and focus sits on the subject; exposure meters.
- **Post tools:** grade (tremor/shake and impact hits from an overscanned render), sound mix, overlay (title card, counters, subtitles, end card), QC (frame per caption, loudness, true peak), peak fixer, contact sheets, a competitor scan (yt-dlp), a **twin check** (per-second visual similarity vs posted videos), and **Gemini review** (Gemini watches and listens; free API key).
- **Sound:** a CC0 Freesound library with picks by "need", real-place recordings, Freesound fetch; no music; no narrator (only a spoken title).
- **Four example projects** (tsunamis, water, electrons, friction): Morrow's own posted videos, all on one Santa Monica pier set, for learning only.

## Comparison with our studio
| | Morrow kit | Our studio |
|---|---|---|
| Ownership | Licensed while paying; gated; 15 videos/month (Standard) | Owned outright; no limits |
| Renderer | three.js in Chromium (WebGL) | Blender 5.2 EEVEE (offline renderer) |
| Speed (owner's M2 8 GB) | unmeasured on this Mac (~10 min / 61 s on "M-series") | 1.15 s/frame at 24 fps ≈ 32 min / 70 s |
| Library depth | Very large: months of sets, disasters, people, vehicles, hands | Small: beach + street kits, bean characters, cars, rings/cones/booms |
| Camera | FPV with hands, rack focus, dolly zoom, QA'd paths | Push/crane/orbit/pan-follow, tilt-shift DOF, path clearing |
| Motion QA | Automatic (feet, wheels, contact, focus) | Visual review only |
| Look | Several presets; members told to vary style | One distinctive house look ("Living Diorama") |
| Sound | Real CC0 recordings + synthesis; no voice | Fully synthesised SFX + optional local TTS voice |
| Review | Gemini watches/listens (free key) + side-by-side vs a viral video | Contact sheets + waveform/spectrogram, Claude review |
| Originality tools | Twin check vs posted videos | Script and camera overlap check only |
| Same-look risk | Every member uses the same engine, people and FX → videos across members can look alike | Our look and assets exist only on this channel |

**Honest verdict:** for the What If format specifically, their engine is more mature than ours: more disasters, more places, first-person hands, better camera tooling and automatic motion QA, refined over 165 logged lessons. Our advantages are ownership, no monthly cap, a look nobody else has, and Blender's lighting. The gap is in **content library and tooling**, not in the method, which we now have.

## Rules worth adopting (our wording)
1. **Structure:** title card 0–3.4 s (spoken title) → countdown to the moment → the impossible seconds on a world clock (~6× slower) → snap back with a flash + hit → consequences you watch → twist → end card (question, one sourced fact, our own follow line).
2. **No narrator through the video;** 15–22 second-person captions (≤10 words, every 2–3 s), each with its own picture. No readable text inside the 3D.
3. **First person**, and **your own hands** are the strongest single image (e.g. a phone alert in your hand).
4. **The whole world changes look at the exact frame** of the event; snap back with a white flash and a hit.
5. **When nothing happens during the seconds, keep real time**; slow motion with nothing in it reads as stretching. Big falls belong after the return.
6. **Counters must be true when their caption appears,** and must come from the same curve that drives the 3D.
7. **The 9:16 frame is only ~±21° wide:** story elements must sit near the centre of the camera's aim; scale objects must be big enough at 540 px.
8. **Sound:** no music; real sounds of the real place; a hard drop to near-silence at the vanish, a soft steady ping under the slow part, a riser into the return; spot sounds need the beds ducked under them; check combinations, not just single files.
9. **Loudness:** never two-pass loudnorm (it goes dynamic and flattens calm → silence → boom). Use one linear gain + soft saturation + limiter; calm ≈ −20 LUFS short-term, climax ≈ −13.
10. **Quality rubric per shot (0–10):** story, subject, motion, craft, life; hard fails for sliding feet / backward walking, cars off-road or wheels still, floating or sunk contact, narration naming something not on screen, unreadable heroes (< 5 % of frame height), camera bumps or fast head turns, broken anatomy, repeated sets.
11. **Originality:** new famous place, set, camera path, type style and colours every video; twin check under 5 % against everything posted.
12. **Topic choice from measured competitor numbers and comments,** on the day.

## Options for the owner
- **A: Our studio only** (adopt the rules above; build the missing tools: twin check, hands, world clock, motion QA, sound changes). Fully owned and distinctive, but it takes longer to match their effects library.
- **B: Their kit for What If videos.** The fastest route to their quality, within the licence (15/month on Standard), but it needs ~15 GB of disk (owner has ~29 GB), a running membership, and every location and look built new to avoid twin flags with other members.
- **C: Hybrid.** Our studio stays the main engine; their kit is used for comparison renders or specific effects only (never copied into our repo).
