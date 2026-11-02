# Project Knowledge

The running record of what has been learned, tested and decided. Update it at the end of every working session.

_Last updated: 2026-11-02_

## Current status
- **Phase:** A (Research) is delivered (see `research/RESEARCH_REPORT.md`). We are waiting for approval of the visual style, the architecture and the first video concept before Stage B (technical foundation).
- **Nothing installed, bought, signed up for, or published.**

## Decisions made
| Date | Decision | By |
|---|---|---|
| 2026-11-02 | Project lives in the private repo `localsaintt/faceless-3d-studio`; production runs on the owner's Mac | Owner |
| 2026-11-02 | **Render-efficiency strategy approved ("option 1")**: lightweight scene design, cheaper EEVEE settings, 24 fps, low-res previews first, re-render only changed shots, per-shot time budget with automatic downgrade; 720×1280→1080×1920 upscale to be A/B tested and decided by the owner | Owner |
| 2026-11-02 | Recommended (pending approval): Blender 5.2 LTS + EEVEE, headless Python, shot-spec JSON/YAML contract, FFmpeg assembly, Kokoro TTS, WhisperX captions, CC0 assets, no music beds | Claude |

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
- Nothing yet (research phase only).

## Outstanding issues / open questions
- Owner approval of: the "Living Diorama" style, the architecture (report §10), and the first concept ("What if sound moved slower than you can run?").
- Starting budget tier (recommended: free + Claude plan).
- How Claude Code will run on the Mac: Claude Desktop app or `claude remote-control` in the project folder.
- Research gaps: platform, vendor and Blender pages could not be opened directly from the research sandbox. Re-verify prices and policies before spending or launching.

## Next steps
1. Owner approves the direction.
2. Stage B: install Blender 5.2 LTS, FFmpeg, Python env, Kokoro, WhisperX on the Mac; `doctor` check renders a test frame headlessly and measures speed and memory.
3. Stage C: 10 s beach-kit prototype in the house style at 24 fps; measure render time and temperature; A/B 720p-upscaled vs native 1080×1920.
