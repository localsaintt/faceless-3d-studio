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

## "What If" course 3: Make your own (lesson 3.1)
- Course: 3.1 Check the premise first · 3.2 Start from an example, facts first · 3.3 Build, preview, fix · 3.4 Words and sound · 3.5 Render, post, fix · 3.6 Review and deliver. The worked example is "What if oxygen disappeared for 5 seconds?", built by a fresh Claude Code given only the kit.
- **Competitor scan before building:** who posted the premise, when, and growth speed ("demand vs supply"). If a big account posted it in the last 30 days you're late: change the element, place or ending, or post fast with your own angle.
- Our scan for "sound slower than you can run" (2026-11-02, web search): no direct match. Nearest is an older What If video (light and sound switched). Web search indexes TikTok poorly, so the owner should double-check in the TikTok app.

## "What If" course 4: Post and grow (lesson 4.1)
- Pre-post: 61 s+; **the question readable in the first second**; sources.txt ready for comments; watch once with sound and once muted.
- Caption formula: question + 1 emoji / one line placing the viewer / tease of the ending / a question for comments / 8–10 hashtags (their prompt 8 writes it).
- Comment trick: answer a comment's video request with a video reply.
- After posting: one video per account per day; reply to first comments; pin sources; read the top comment for the next premise.
- 4.2 The daily loop: not yet seen.

## Zombie survival (Z1.1) and How it's built (H1.1)
- Skeletons and measured rules are summarised in our own words in `Studio Memory/Format skeletons.md`.
- Zombie: in test at Morrow (no posted results); reference Part 1s by others 710K–4.4M (Oct 15–24 2026). Morrow does it in flat 2D.
- How it's built: one Morrow short passed 245K in 2 days; references 4.3–14.4M (Oct 16–25 2026). Version 2 "autopilot" (H1.1b) not yet seen.

## Weekly drop, Oct 27 2026 (public counts read Oct 26; other creators)
- What-if: Earth stops spinning 28.8M; electrons disappear 5 s 17.3M. **Winning lane: one everyday thing changes for a few seconds, seen through your own eyes (POV, second person), with a number on screen.** New formats nobody asked for (shelters, zippers) got ~1/10 the views of the classic "X disappeared for 5 seconds".
- Zombie: tidal island 1.9M; "Day 1 on the 10th floor" 1.7M. Ordinary place + an inside advantage only the narrator knows.
- How it's built: backyard builds dominate (pool 12.8M, toilet 5.9M) and were copied by dozens of accounts within days; **remakes flop, new topics win.**
- Long-form: 3D "What if you shrank and couldn't stop?" 858,960 YouTube views. Escalation film = one premise that keeps getting bigger.
- Rule of the week: copy the skeleton, never sentences, sets, places or voice; TikTok stops paying Creator Rewards on copies.
- Kit: What If 3D Kit v3 (needs login once per computer); zombie and how-it's-built kits coming.

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
