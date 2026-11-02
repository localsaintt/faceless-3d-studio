---
type: research
source: Morrow Studio (paid Skool community, owner's membership)
updated: 2026-11-02
---
# Morrow Studio: our notes

Our own summary of what the owner shares from the Morrow Studio classroom. Their raw lesson text, files and kits are paid content and **are not stored in this repository**. Claims below are Morrow's self-reported numbers unless marked as ours.

## What Morrow is
- A small studio running its own faceless channels with Claude Code: 2 TikTok accounts of 3D shorts, a YouTube channel of 3D films, Facebook reel pages, and a "how it's made" YouTube channel.
- Reported bests: 3D short 3.1M views; 3D film 384K; motion-control reel 179K; animal story reel 126K ("not typical").
- House rules: every style comes with a cost receipt; members build their own look ("copies earn nothing"); no sponsors in lessons.
- **Their kit needs an active membership to make new videos** (lesson 1.6 "Log in to the kit"). Our studio must stay independent of it: we adopt techniques, not a dependency.

## Course map (seen so far)
- 1 Start Here: 1.1 Welcome · 1.2 How it works · 1.3 Pick your first style · 1.4 Set up your computer · 1.5 Video 1: every prompt and file · 1.6 Log in to the kit
- 2 The Receipts: 2.1 Why every video gets a receipt (cost sheet PDF + spreadsheet attached) · 2.2 Cost sheet · 2.3 Which Claude plan? · 2.4 Where the usage really goes · 2.5 Log your own receipt

## "What If" style course: kit install (lesson 1.2)
- Course 1 "Install the kit": 1.0 The What If style in 2 minutes · 1.1 How this works · 1.2 Install the kit · 1.3 Your first render · Downloads (the kit, the playbook, the prompts).
- **The kit is a folder opened in Claude Code** ("Set up the kit"). It installs itself, runs a check list with ticks/crosses and fixes printed under each, and renders one real frame. This is the same pattern as our `setup/mac_setup.sh` + `studio.doctor`.
- Requirements: Mac/Windows/Linux running Claude Code, Claude subscription, **8 GB RAM minimum (16 GB "comfier")**, **~15 GB free disk**.
- **Licence gate:** a one-time login per computer with the Skool email + a member code (lesson 1.6). The member code is a credential: never store it in this repo or paste it in chats.
- Owner impact: ~29 GB free means installing the kit (~15 GB) would drop below our 15 GB render guard. Free space first, and install it in its own folder (not inside this project).

## "What If" course 2: What wins (lesson 2.1, their first-week TikTok data, Oct 3–9 2026)
- Top performers: absolute zero 1.1M, friction 971K, carbon 845K, all "an everyday thing changes" premises.
- **Their pattern:** (1) an everyday thing changes for **5 seconds**; (2) a famous, busy place **by the water, in daylight**; (3) **a new picture every 2–3 s**; (4) **61 s or more**; (5) the same closing line every time ("And yes. There's a tsunami.", **their signature: never copy it**).
- Our first video vs the pattern: (2) and (4) match; (1) is 10 s rather than 5; **(3) is the gap: ~6 s per shot**; (5) we have our own running gag (the ice-cream truck).
- Remaining lessons in this course: 2.2 Pick a premise that can win · 2.3 The tsunami ending · 2.4 Be original (or don't get paid).

## Costs (lesson 2.2) vs. ours
| | Morrow | Us |
|---|---|---|
| 3D short: cash | $0–2 (optional AI SFX) | $0 (procedural SFX, local Kokoro voice) |
| 3D short: Claude | ~1% of a Max 20x week once the format is locked | not yet measured, so start logging |
| 3D short: render | 3,108 frames in 13 min on a 16 GB laptop (~0.25 s/frame) | 1.15 s/frame on the owner's M2 8 GB (~32 min / 70 s) |
| 3D film 5–8 min | $0 + 1–7% of a Max week | not built yet |
| Story reel / talking-animal / motion-control reel | $0.55 / $0.64–2.08 / ~$0.90 (paid AI images and clips) | not in scope (would need a paid AI video account and the owner's approval) |
| Presenter video | 2.5–5.6¢ per on-camera second | not applicable |

They label numbers "measured" (own ledgers) vs "rate card" (provider list price), date every line, and re-measure within a week of price changes. **We should do the same: a receipt per video.**

## Ideas to adopt / test
1. **Per-video receipt** in each video note: cash spent, Claude usage, render minutes, machine. Add to `make_video` QC output.
2. **"Fast final" render profile**: test fewer EEVEE samples / cheaper shadows on the Mac against current final; their 0.25 s/frame suggests our look may survive much lighter settings.
3. New formats to research later: motion-control reels, animal story reels (Facebook). Both depend on paid AI image/video tools.

## Open questions
- ~~What is the kit?~~ A Claude Code project folder with a licence login (see above). Still unknown: its renderer, scene code and prompts. Next step: read the Downloads files (read-only, never run here).
- Which renderer do they use for 3D (Blender EEVEE vs Three.js/WebGL)?
