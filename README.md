# faceless-3d-studio

An AI-assisted, local 3D animation studio that turns one idea into an original, finished 1080×1920 vertical video: concept → script → storyboard → Blender scenes → render → audio and captions → assembly → quality check → owner approval.

**Status:** Stage B (foundation) built and tested in the cloud; waiting for the first run on the owner's Mac. Stage C prototype (beach kit in the house style) renders.

## Quick start (Mac)
See **[docs/MAC_SETUP.md](docs/MAC_SETUP.md)**. In short:
```bash
bash setup/mac_setup.sh                       # installs tools in the project folder + doctor check
.venv/bin/python -m studio.render_shot shots/proto/s01_beach_establishing.yaml --profile preview
```

## Layout
| Where | What |
|---|---|
| `blender/build_shot.py`, `blender/scenekit/` | Scene builder: house style, characters, beach kit, camera moves, render profiles |
| `studio/` | Runner (render → MP4 → contact sheet) and doctor check |
| `shots/` | Shot specs (YAML), the contract between storyboard and Blender |
| `setup/mac_setup.sh` | One-time Mac setup |
| `docs/PROJECT_KNOWLEDGE.md` | Running log: decisions, what's tested, open issues, next steps |
| `research/` | Phase A research report and source notes |
| `CLAUDE.md` | Working rules for Claude Code sessions |

Stack: Blender 5.2.3 LTS as a Python module (EEVEE), FFmpeg, PyYAML; later Kokoro TTS and WhisperX. Everything is free and runs locally.
