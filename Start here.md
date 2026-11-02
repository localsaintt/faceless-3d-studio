# Faceless 3D Studio

This vault is the studio's control room. Claude writes and updates these notes, and you read, edit and approve here.

## Where things are
- **[[Dashboard.base|Dashboard]]**: every video and idea with its status.
- **videos/**: one folder per video. The note inside has the script, storyboard, latest render, quality check and **your approval**.
- **ideas/**: the idea bank. Add your own with the *Idea* template (Command palette → "Templates: Insert template").
- **docs/PROJECT_KNOWLEDGE.md**: what's been decided, tested and learned.
- **research/**: the Phase A research report.

## How approval works
Each video note has a `status` property at the top. Change it to move the video forward. The studio checks it before doing anything.

| Status | Meaning | Who changes it |
|---|---|---|
| `script-review` | Script and storyboard ready for you to read | Claude |
| `script-approved` | You're happy with the script, so the final render may start | **You** |
| `rendering` | Final render in progress | Studio |
| `ready-for-review` | Finished video + quality report are in the note; watch it | Studio |
| `approved` | You're happy with the video, so it may be archived to iCloud | **You** |
| `archived` | Final file is in iCloud Drive › Faceless Studio Archive | Studio |
| `posted` | You posted it yourself | **You** |

Nothing is ever posted automatically.

## Commands (Terminal, in this folder)
```bash
.venv/bin/python -m studio.make_video slow-sound-miami                  # preview render
.venv/bin/python -m studio.make_video slow-sound-miami --profile final  # after script-approved
.venv/bin/python -m studio.archive slow-sound-miami                     # after approved
```
