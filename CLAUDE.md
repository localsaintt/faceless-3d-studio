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

## Code layout and how to run
- `blender/build_shot.py`: builds one shot from a YAML spec and renders it (runs in a process with `bpy`).
- `blender/scenekit/`:
  - `style.py`: house palette and materials.
  - `geo.py`: shared meshes and driver helpers.
  - `characters.py`: bean-body people, procedural anims (idle/talk/look_up/walk).
  - `beach.py`: beach set kit.
  - `camera.py`: camera-move library.
  - `render.py`: render profiles.
- `studio/render_shot.py`: runner (render → MP4 → contact sheet). `studio/doctor.py`: environment check + speed test.
- `shots/<video>/<shot>.yaml`: shot specs (the contract between storyboard and Blender).
- Run: `.venv/bin/python -m studio.render_shot <spec> --profile preview|final|final_720 [--still N ...] [--fresh]`.
- Always look at stills/contact sheets before a full render.

## Blender notes
- Target **Blender 5.2 LTS**, run headless: `blender -b <file.blend> -P <script.py> -- <args>`.
- Install is `bpy==5.2.3` in `.venv` (Python 3.13), not the Blender app; `blender/build_shot.py` runs with `.venv/bin/python`.
- Procedural animation uses simple-expression **drivers** (`sin(frame*k+phase)`), which avoids the 5.x F-curve API and needs no Python auto-exec.
- Crowd colours: per-instance via the instancing Empty's object colour read by an INSTANCER Attribute node (see `style.instancer_palette`).
- Use the "Standard" view transform (AgX greys out the palette). The miniature look needs an exaggerated camera f-stop (~0.04), because physically correct apertures give no visible blur at these distances.
- Ocean modifier (GENERATE) grid starts at `location - spatial_size/2` and extends `spatial_size*repeat`.
- In a Linux container without a GPU, EEVEE renders via Mesa software GL (`apt install libegl1 libgl1-mesa-dri`). It's slow but fine for checking correctness; measure speed only on the Mac.
- 5.x API changes: `Action.fcurves` was removed (use `bpy_extras.anim_utils.action_ensure_channelbag_for_slot` → `channelbag.fcurves`); engine id is `BLENDER_EEVEE`; video output needs `image_settings.media_type='VIDEO'` (prefer PNG sequences + FFmpeg anyway).
