# Project Knowledge

The running record of what has been learned, tested and decided. Update it at the end of every working session.

_Last updated: 2026-11-02_

## Current status
- **Stage B (foundation):** built and tested in the cloud container. Waiting for the first run on the owner's Mac (`docs/MAC_SETUP.md` → `bash setup/mac_setup.sh`, which ends with the doctor speed test).
- **Stage C (prototype):** beach kit + house characters + camera move render correctly (EEVEE). A 6 s preview clip has been produced; real speed/memory numbers must come from the Mac.
- **Nothing bought, signed up for, or published.** Only free, open-source tools are used.

## Decisions made
| Date | Decision | By |
|---|---|---|
| 2026-11-02 | Project lives in the private repo `localsaintt/faceless-3d-studio`; production runs on the owner's Mac | Owner |
| 2026-11-02 | **Render-efficiency strategy approved ("option 1")**: lightweight scene design, cheaper EEVEE settings, 24 fps, low-res previews first, re-render only changed shots, per-shot time budget with automatic downgrade; 720×1280→1080×1920 upscale to be A/B tested and decided by the owner | Owner |
| 2026-11-02 | **Approved ("go ahead")**: "Living Diorama" style, the architecture in report §10, and first video concept "What if sound moved slower than you can run?" | Owner |
| 2026-11-02 | Stack: Blender 5.2.3 LTS **as the `bpy` Python module** in `.venv` (same version on Mac and cloud), EEVEE, YAML shot specs, FFmpeg; later Kokoro TTS and WhisperX; CC0 assets; no music beds | Claude |
| 2026-11-02 | Animation is procedural via simple-expression drivers. Crowds are collection instances of character variants; per-person colours come from the instancer's object colour | Claude |
| 2026-11-02 | Colour: "Standard" view transform (AgX looked grey). Miniature look: camera f-stop ~0.04 on purpose | Claude |

## Hardware profile (owner's machine)
| Item | Value | Implication |
|---|---|---|
| Computer | Apple M2, **8 GB unified memory** | EEVEE via Metal works. Memory is the main constraint: 1K textures, instanced crowds, render per shot, close other apps while rendering |
| OS | macOS Tahoe 26.6.2 | Supported by current Blender |
| Free disk | ~100 GB | Enough (budget ~20–30 GB for tools, models and assets, plus 4–8 GB of temporary frames per video, deleted after assembly) |
| iCloud | 200 GB paid plan (2.99/mo) | **Do not put the project inside iCloud-synced folders** (Desktop/Documents if "Desktop & Documents Folders" sync is on). Render frames would upload gigabytes to iCloud and fill the plan. Use `~/Projects/faceless-3d-studio`. Rendered frames and outputs are git-ignored |
| Not possible locally | Cycles at volume, TRELLIS.2 / local AI 3D generation (needs NVIDIA 16 GB+) | Use CC0 asset libraries; a paid generator or cloud GPU only if a real gap appears, with the owner's approval |
| Thermal | macOS throttles when hot, which costs speed but does no damage | Render overnight, hard surface/stand, plugged in; Low Power Mode is optional for cooler overnight runs |

Render-time estimate for a 70 s short on this Mac: **~1–4 h** (unmeasured). Measure in Stage C.

## Key learnings (from research)
- The premise, hook and escalation drive results far more than render quality. Topics get cloned within ~48 h, so speed on our own ideas matters.
- Universal devices in the niche: the question on screen from frame 1, a ticking counter, an escalation ladder, a twist ending, a comment prompt, 60–80 s length.
- Platform risk: YouTube "inauthentic content" (mass-produced/templated), Meta's unoriginal-content crackdown, and TikTok Creator Rewards originality rules (5+ ineligible videos in 30 days → may be removed). Every video needs a new set seed, opening, camera paths, script and sound.
- TikTok Creator Rewards needs videos **over 1 minute**. Plan 61–80 s.
- Ready Player Me (shut down Jan 2026) and OpenAI Sora (API retired Sep 2026) are gone. Mixamo works but is unmaintained, so download clips once.
- Blender 5.x API changes: `Action.fcurves` removed (use channelbags), EEVEE engine id `BLENDER_EEVEE`, video output needs `media_type='VIDEO'`.

## What has been tested
| Date | Test | Result |
|---|---|---|
| 2026-11-02 | `bpy==5.2.3` wheels | Exist for macOS arm64 (Python 3.13), Linux, Windows |
| 2026-11-02 | EEVEE headless in the cloud container (no GPU) | Works only after installing Mesa EGL (software GL). Cycles CPU works out of the box |
| 2026-11-02 | Prototype shot s01 (beach, 160 people, 14 palms, 16 umbrellas, 9 hotels, tower, 2 walkers, dolly push), preview 540×960 | Renders correctly. Container (4 vCPU, software GL): ~9 s/frame, peak ~4.3–4.9 GB RAM over the animation (~1.8 GB for a single still). **Not representative of the M2. Check peak memory on the Mac first** |
| 2026-11-02 | Visual QC loop (stills → fixes → contact sheet) | Caught and fixed: grey AgX colours, sky-heavy framing, inverted seabed, detached arms, invisible DOF, ocean offset, and waves flooding the beach (crests now kept below sand on a 6° shore) |
| 2026-11-02 | `studio/render_shot.py` (render → MP4 → contact sheet), `studio/doctor.py --quick`, `setup/mac_setup.sh` syntax | Pass in the container. Setup script not yet run on a Mac |

## Outstanding issues / open questions
- First Mac run: setup + doctor speed test + peak memory on 8 GB (the container peaked at ~4.3 GB; if the Mac swaps heavily, reduce crowd size or split renders).
- How Claude Code will run on the Mac: Claude Desktop app or `claude remote-control` in the project folder.
- Characters have no rig yet (procedural limb pivots). Fine for the stylised look; revisit if close-up acting is needed.
- Polish: thin dark seam along the waterline (sand/seabed join).
- Not built yet: text/counter overlays, audio (TTS + SFX), captions, multi-shot assembly, QC checks (Stage D).
- Research gaps: platform, vendor and Blender pages could not be opened directly from the research sandbox. Re-verify prices and policies before spending or launching.

## Next steps
1. Owner runs `docs/MAC_SETUP.md` and sends the doctor output (speed + memory).
2. Stage C on the Mac: render s01 in `final` and `final_720`; owner picks native vs upscaled; record s/frame and temperature notes here.
3. Stage D: storyboard → shot specs for "slow sound"; Ocean Drive street kit (cars, cafés); effects (sound rings, shock cones); HUD counter + captions overlay; Kokoro narration + SFX; multi-shot assembly; QC checks; first complete 61–80 s video for approval.
