---
type: memory
updated: 2026-11-02
---
# Lessons learned

Claude reads this before writing or building any video and adds to it after every video. Newest first within each section.

## Framing and camera
- **Nothing random may sit between the lens and the subject.** The builder hides extras, palms and umbrellas within 7 m of the camera path (`clear_camera_path`). Scripted actors are never hidden. (Video 1: a pedestrian blocked s04/s07; a palm blocked s05.)
- **Only small props may be auto-hidden.** A bug that measured object sizes before Blender evaluated them hid the whole beach floor and the road, so the sky showed through as a pale-blue "ground". Always `view_layer.update()` before reading `dimensions`. (Video 1: s02, s11, s12.)
- **Two characters far apart need an elevated, side-on camera.** Over-the-shoulder from 5 m made the foreground person a blur that hid the other one. (Video 1, s03.)
- **Viewers must know who's who.** Use `label:` callouts ("KID", "MOM") on story characters in wide shots.
- **Miniature blur is distance-dependent.** f-stop ~0.04–0.09 for cameras 15–40 m away, ~0.25 at ~10 m, ~0.7 for close two-shots. One value for everything makes close shots unreadable.
- **Moving subjects look best with `pan_follow`**: a static (or slightly drifting) camera that tracks the actor, placed where the subject approaches the lens.

## Effects
- **A big translucent sphere becomes invisible once it fills the frame.** Pair sound shells with a glowing ground ripple (`ground: 0.0`) so the wavefront is always readable.
- **Fewer, smaller rings read better.** 40 overlapping shells turned shots into pink fog; ~20–22 at max radius 7–8 m with a 0.28 opacity floor reads clearly.
- **Waves on a flat beach flood it.** Keep crests below the sand and use a ~6° seabed slope; the shoreline then laps ±1 m.

## Look
- "Standard" view transform: AgX made the palette grey.
- High, diorama-style cameras (8–15 m up) are the house look; ground-level shots need a clear reason.

## Sound
- Check every mix visually (waveform + spectrogram), since Claude can't listen. Sweeps and engines came out too loud at first.
- Loudness: loudnorm alone overshot true peak (+1.8 dBTP). A limiter after loudnorm is required.
- Muffling the world during the "impossible" window (low-pass + quieter beds) sells the premise.

## Story and script
- **Cut to a new picture every 2–3 s** (Morrow's first-week data: all winners did). Split long shots into extra camera angles on the same set; render time doesn't change. Video 1 averaged ~6 s per shot, too slow.
- **Signature closing line, every episode, our own:** a recurring ice-cream-truck line (never anyone else's catchphrase, e.g. Morrow's "And yes. There's a tsunami.").
- Strongest premises so far (Morrow data): an everyday thing changes for ~5 s, at a famous busy waterfront in daylight, 61 s+.
- Narration at ~2.6–3.6 words/s fits 4.5–8 s shots; budget ~12 words per 5 s shot.
- Every shot needs one new beat (counter change, effect, gag) every 2–3 s; counters carry the story when narration pauses.
- Physics claims get a science check in the note, and estimates on screen get "est.".

## Pipeline and process
- Container renders are ~40× slower than the Mac. Use the `draft` profile for full end-to-end tests in the cloud; measure speed only on the Mac.
- Render stills of the riskiest shots before any full render; review a contact sheet of the finished video every time.
