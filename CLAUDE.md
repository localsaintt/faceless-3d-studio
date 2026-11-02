# Faceless 3D Studio — instructions for Claude

An automated studio that turns one idea into an original, finished vertical 3D animated video (Blender + Python + FFmpeg), always delivered for the owner's approval.

## Read first, every session
- `docs/PROJECT_KNOWLEDGE.md`: status, decisions, hardware limits, open questions. **Update it before ending a session.**
- `research/RESEARCH_REPORT.md`: research, recommended architecture, style and roadmap.

## Hard rules (from the owner)
- Ask before: purchases, subscriptions, creating accounts, paid API usage, connecting external accounts, publishing anything, irreversible changes.
- Never publish or post content. Never delete videos because they performed poorly.
- Every video must be original: own script, own scenario, new set layout/seed, new opening shot, new camera paths, own sound design. Never copy another creator's script or exact scenes. Log asset licences.
- Test everything before claiming it works. A script or storyboard is not a video.

## Machine constraints (owner's Mac)
- Apple M2, **8 GB unified memory**, macOS Tahoe 26.6.2, ~100 GB free.
- EEVEE only (no Cycles for production). 1K textures, instanced crowds, render per shot, previews at 540×960 before final renders, 24 fps, per-shot render-time budget.
- Keep the project and all render output **outside iCloud-synced folders**; render frames and outputs are git-ignored.

## Blender notes
- Target **Blender 5.2 LTS**, run headless: `blender -b <file.blend> -P <script.py> -- <args>`.
- 5.x API changes: `Action.fcurves` was removed (use `bpy_extras.anim_utils.action_ensure_channelbag_for_slot` → `channelbag.fcurves`); engine id is `BLENDER_EEVEE`; video output needs `image_settings.media_type='VIDEO'` (prefer PNG sequences + FFmpeg anyway).
