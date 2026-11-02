# Faceless 3D "What-If" / Simulation Short-Form Creators: Research Notes

Research date: 2026-11-02. Analyst: Claude (subagent).

## Method and limits (read first)

- **WebFetch was blocked for every host tried** (tiktok.com, youtube.com, ladbible.com, wikipedia.org returned `ENOTFOUND`, meaning the session's network allowlist blocks them). No profile page, video page, or article was opened directly.
- Evidence therefore comes from **WebSearch result snippets**, which a search model summarises. I treat a snippet as VERIFIED only when it quotes a specific URL, a caption, or a number tied to a source. Snippet numbers can be stale or cached.
- **The WebSearch budget ran out** (200 calls per turn, shared by all agents) before I could search Animagraffs, more zombie-scenario channels, and the Zack D. Blender tutorial contents. More searches need a follow-up turn.
- **One primary artifact was obtained:** a public GitHub repo, `zNightmare15/what_if_project` (cloned via git, last commit 2026-10-25). It is a **third-party reverse-engineering** of the @man_ia_c electrons video. It contains frames extracted from the original TikTok, which carry the TikTok watermark, `@man_ia_c`, and TikTok's **"AI-generated"** label. It also contains the original audio, with TikTok metadata and a duration of 80.09 s. I viewed those frames directly. Claims based on the frames are **VERIFIED (frames)**. The repo author's timing measurements are **third-party measurements**.
- TikTok video IDs encode the posting time (`id >> 32` = Unix seconds). Dates marked "ID-decoded" come from that method.
- Labels: **VERIFIED** = backed by the cited URL or artifact. **INFERENCE** = my reading or extrapolation, not confirmed. **UNVERIFIED** = claimed somewhere (e.g. the playbook PDF) but not confirmed.

---

## Comparison table

| # | Creator / handle | Platform(s) | Content type | Visual style | Scale evidence (source, date) | Exists? |
|---|---|---|---|---|---|---|
| 1 | **Lunar Animation, @lunarcheeseee** | TikTok | 3D "what if" planetary disasters (Earth stops spinning, Moon hits Earth, rogue planet, Sun explodes, tsunami hits NYC, second sun) | 3D simulation, city/ship destruction (INFERENCE: realistic-leaning) | Earth-stop video: ~2.5M likes (one discover page), 2.8M–3.5M likes (others, Oct 2026). An unlabelled "25.2M" also appears. Covered by LADbible on 2026-10-05. **PDF's 28.9M views: UNVERIFIED** (consistent in magnitude) | VERIFIED |
| 2 | **"What if?", @man_ia_c** | TikTok | 3D physics what-ifs (electrons vanish 5 s; pop star 10 billion× taller) | Low-poly blocky people + semi-real grass/skyline, then X-ray wireframe, then space, then LiDAR point cloud. Elegant serif typography | Electrons video posted 2026-10-06 (ID-decoded), ~80 s long. **PDF's 17.5M views: UNVERIFIED** | VERIFIED (video URL + frames) |
| 3 | **You Built It, @youbuiltit** | TikTok + YouTube (@youbuilt_it) | "How everyday objects work / how things are built" | Not verified (INFERENCE: 3D construction cutaway) | TikTok snippet: ~117.9K followers, ~2.9M likes (layout ambiguous). YouTube structured-data count 55,800 (possibly subscribers). **Pool video (13.0M): UNVERIFIED, not found** | VERIFIED (account) |
| 4 | **@pancarte_media** | TikTok (claimed) | Zombie-apocalypse scenario | Unknown | The handle appeared only in one hashtag/tag list snippet. **Cruise-ship video (5.7M): UNVERIFIED, not found** | NOT VERIFIED |
| 5 | **Zack D. Films, @zackdfilms** | YouTube (Shorts-heavy), TikTok | 3D explainer shorts: body, science, survival, "what would happen if" | Stylised-realistic 3D (Pixar-ish characters), cinematic camera | 29.3M subs, 80.98B views, 4,109 videos (vidIQ, 2026-10-21). #1 most-viewed channel worldwide, week of Oct 12–18 2026: 1,106,821,498 views (Tubefilter) | VERIFIED |
| 6 | **What If, @whatifscienceshow** (Underknown) | YouTube, plus ES/JP/ZH channels | Science what-ifs (cosmic catastrophes, planetary physics) | Not verified (INFERENCE: 3D CGI + narration) | ~8.9M subs, 1.7B views (OutlierKit snippet). Social Blade ~8.95M. Webby People's Voice 2020. ES channel ~3.15M (Apr 2025) | VERIFIED |
| 7 | **the_whatif_animator, @the_what_if_animator** | TikTok + YouTube | Multi-part "If the zombie apocalypse starts while you're in a [mall / ski trip / hospital / aquarium]…" | Animated (3D vs. 2D not verified) | Mall Part 1: ~208K likes, 781 comments. Mall Part 2: ~53K likes, 474 comments (snippets, Oct 2026) | VERIFIED |
| 8 | **@moon2animation** | TikTok | 3D physics what-ifs (POV, beach/sunset) | 3D (#3danimation) | "Every electron disappeared for 1 second": 148.9K likes, 1,624 comments, posted 2026-10-08 (ID-decoded) | VERIFIED |
| 9 | **The What If Studio, @thewhatifstudio** | TikTok | 3D science simulations ("every human clapped at the same time") | 3D (#3danimation) | ~279.2K followers (discover snippet, Oct 2026) | VERIFIED (snippet only) |
| 10 | **POV: What If, @pov.what.if0** (also @pov.what.if2) | TikTok | POV what-if simulations | Not verified | ~123.1K followers (snippet) | VERIFIED (snippet only) |
| 11 | **What if Animation, @whatif.animation** | TikTok | What-if animations | Not verified | ~280.4K followers (snippet) | VERIFIED (snippet only) |
| 12 | **Jared Owen** | YouTube | 3D "how it works / what's inside" cutaways (buildings, vehicles, landmarks) | Clean stylised 3D cutaway, Blender | ~4.4M subs, 529M views, 120 videos (2026 trackers). 3M (Dec 2023, Avid wiki) | VERIFIED |
| 13 | **Lesics** | YouTube | 3D engineering explainers | 3D technical animation | 6.74M subs, 1,022,235,067 views (self-reported on lesics.com) | VERIFIED (self-reported) |
| 14 | **Hashem Al-Ghaili** | FB, YouTube, TikTok, IG | Realistic CGI "concept" futurism (EctoLife artificial-womb facility, nuclear sky hotel) | Photoreal CGI, mistaken for real | Claims 45M+ followers across platforms (Khaleej Times). Older: FB 32M+ | VERIFIED |
| 15 | **The Data Ball** | YouTube | 3D scale/size comparisons | 3D | 275K subs, 143 videos. Says each video takes 100+ hours (vidIQ snippet) | VERIFIED (snippet only) |
| 16 | **Aleksey Patrev, @aleksey_nz** | TikTok / YouTube | CGI "supermoon at the North Pole" | Photoreal CGI | Original TikTok "over 32.9 million views" (fact-checkers, 2021) | VERIFIED |
| 17 | **@lights.are.off** | TikTok | 3D "giant statues at the bottom of the ocean" | Realistic 3D | 1.8M followers (Lead Stories, Dec 2023) | VERIFIED (2023 data) |
| — | Kurzgesagt (adjacent, **2D**, not 3D) | YouTube | Science explainers | 2D vector (INFERENCE / general knowledge) | ~25.6M–25.7M subs (Oct 2026 trackers) | VERIFIED |

**Count:** of the 4 starting creators, 3 were verified to exist (lunarcheeseee, man_ia_c, youbuiltit) and pancarte_media was not. None of the 4 PDF view counts could be confirmed exactly. 13 additional relevant creators/channels were verified to exist with some scale data (rows 5–17), plus Kurzgesagt as a 2D reference.

---

## Per-creator notes

### 1. Lunar Animation (@lunarcheeseee), TikTok, https://www.tiktok.com/@lunarcheeseee
- **Existence/identity:** VERIFIED. Search snippets name the account "Lunar Animation (@lunarcheeseee)", which posts 3D "what if" disaster simulations. Topics: rogue planet, Sun exploding, tsunami hitting New York, Moon crashing into Earth, Earth stopping its spin, second sun. Source: TikTok discover page https://www.tiktok.com/discover/lunarcheese (snippet, listing updated 2026-10-05).
- **Press:** VERIFIED. LADbible, "Horrifying simulation shows what would happen if the Earth stopped spinning", 2026-10-05 (https://www.ladbible.com/news/science/horrifying-simulation-earth-stop-spinning-712101-20261005), credits TikTok/lunarcheeseee. LADbible also tweeted it (https://x.com/ladbible/status/2107068745856254136).
- **Script / hook / counter (from article snippets):** VERIFIED (via snippet). The video shows Earth going "from spinning 1037 miles per hour to zero". It counts down the equatorial speed: "once speeds get down to 1028, that's when the terror truly begins". Buildings and street signs peel away and fly east, and structures crumble around 800 mph. A tsunami and cargo ships appear. The creator argues the Earth "wouldn't just stop to a firm halt immediately", so it shows a gradual slowdown. **INFERENCE:** the on-screen element is an escalating speed counter (mph ticking down), similar to the man_ia_c countdown device.
- **Numbers:** Earth-stop video ~2.5M likes on one discover page and 2.8M–3.5M likes on others (Oct 2026). Moon-hits-Earth ~163K likes on one listing. Rogue planet ~16.3K likes. An unlabelled "25.2M" appears on one discover page. **PDF claim of 28.9M views as of Oct 27: UNVERIFIED.** It is plausible given 2.5–3.5M likes (INFERENCE: typical like/view ratios of 8–12%).
- **Hashtags:** #simulation, #animation, #3danimation (snippet).
- **Tools:** no evidence. Camera, audio, environment: not verifiable without the video. **INFERENCE:** realistic city scenes with physics-driven destruction (Blender/Houdini-type sims or AI video). Unconfirmed.
- **Precedent:** Zack D Films made an Earth-stops-spinning short in 2025 ("thrown east at over 1,000 miles an hour", per UNILAD Tech 2025-08-06: https://www.uniladtech.com/social-media/simulation-shows-what-happens-if-earth-stopped-spinning-757987-20250806). Topics recycle across creators.

### 2. "What if?" (@man_ia_c), TikTok, https://www.tiktok.com/@man_ia_c
- **Existence:** VERIFIED. Video URL https://www.tiktok.com/@man_ia_c/video/7693494009494342945, posted 2026-10-06 10:06 UTC (ID-decoded). Caption (verbatim from search): *"What if electrons disappeared for 5 seconds? You're in Central Park when every electron on Earth vanishes. The sky turns black at noon. Light passes straight through everything, even your hands. Every atom becomes pure positive charge, and positive charges repel. One grain of sand releases the energy of a 10-megaton bomb. Every person outshines the Sun. Earth comes apart at nearly the speed of light. When the electrons come back, there's nothing left to come back to. Which one next? 👇 #whatif #pov #simulation #science #physics"*. Another post: "What if a pop star grew 10 billion times taller?" (snippet).
- **Views:** PDF claims 17.5M. **UNVERIFIED** (no view or like count surfaced).
- **Length:** ~80 s. VERIFIED: the original audio file in the repo, carrying TikTok metadata (`vid:v26044gc…`, `aigc_info`), is 80.09 s.
- **AI disclosure:** VERIFIED (frames). Every extracted frame shows TikTok's **"AI-generated"** label at bottom-left. This means the creator self-disclosed AI content or TikTok detected AI provenance. It does **not** say which parts are AI. INFERENCE: some mix of AI-assisted generation and 3D.
- **Visual style (VERIFIED from frames):**
  - Opens on a sunny Central Park scene with semi-realistic grass, low-poly trees, and generic glass skyscrapers. Characters are **blocky low-poly people** (box torsos, no faces) on a red-and-white checkered picnic blanket. A glowing Bohr-atom icon with "e⁻" electrons floats above.
  - After the event: an **X-ray / white-line wireframe** look on black (trees, buildings and people drawn as outlines, starfield visible through the ground), a lens-flared Sun, and **first-person POV wireframe hands** ("You can see the stars through your hands.").
  - Later a soft white glowing Earth fills the frame with the Moon silhouetted, then (per repo) a LiDAR-style point cloud of the park "5 seconds later", then a black end card.
- **Text/caption system (VERIFIED from frames):**
  - Hook title centred upper-third in a **serif font** (Georgia-like), white with the key noun highlighted light blue ("What if **electrons** disappeared for 5 seconds?"), visible ~0–4 s.
  - **Countdown HUD** at left-centre: a small caps label ("ELECTRONS DISAPPEAR IN" → "ELECTRONS RETURN IN"), large serif digits with milliseconds ("0:06.000", "0:04.821", "0:01.071"), and a small caps footer ("EVERY ATOM ON EARTH HAS THEM" → "TIME SLOWED DOWN 11×" → "EARTH IS NOW 353,887 MILES WIDE").
  - **Italic serif subtitle** lines at lower-middle ("Light now passes straight through everything.", "More than the Milky Way will ever shine.").
  - End card repeats the title over black with a small monospaced fact line ("ELECTRONS ARE 0.03% OF YOUR MASS AND EVERY CHEMICAL BOND IN YOUR BODY").
- **Structure / pacing:** third-party measurement from the repo's `stories/electrons_5s.json`, whose author says it mirrors the reference. Five phases:
  1. Daylight park + real-time countdown, 0–8.0 s.
  2. X-ray cascade with "time slowed 11×" and a slow-motion countdown, 8.0–42.2 s: POV hands, sand "bombs", people glowing, eruption, whiteout.
  3. Orbital expansion, 42.2–64 s, with a **live telemetry counter** ("EARTH IS NOW {value} MILES WIDE") → Moon engulfed → "THE MOON IS GONE".
  4. Return in LiDAR point-cloud form, 64–72.5 s ("ELECTRONS BACK", "CENTRAL PARK, 5 SECONDS LATER", second blast).
  5. Outro card, 72.5–80 s.

  The script is a clean **escalation ladder** (local → personal POV → people → planet → Moon → aftermath) with a twist ending, and a comment-bait CTA in the caption ("Which one next? 👇").
- **Audio:** INFERENCE. The repo's sound-cue sheet, which says it mirrors the reference video's loudness/spectral map, is labelled "Ambient sound-design … (no narration)". It lists park ambience with dog barks, reverse swells, impacts, low drones (41–55 Hz), whooshes, crackle/sizzle, risers, blasts and data ticks, mastered to −14 LUFS. The repo treats `original_audio.mp3` as "ORIGINAL_SFX" and adds its own edge-tts voice ("en-US-ChristopherNeural"). This suggests, but does not prove, that the original is SFX/ambient-led with on-screen subtitles carrying the script. Whether the original has a voiceover is **not verified**.
- **Tools:** none disclosed by the creator. The repo shows a working recreation in **Three.js/WebGL → headless browser → FFmpeg**, with an alternative **Blender EEVEE** path (`blender/scene_master.blend`), procedural textures, bloom/ACES post, and an ASS subtitle HUD. That is the recreator's toolchain, **not** man_ia_c's.
- **Copycat signal:** VERIFIED. @moon2animation posted "What if every electron disappeared for 1 second?" on 2026-10-08, two days later (148.9K likes). Snippets also list @pov.what.if2 (5-second version), @whatifsims2 and @lowpolyyn. The repo itself was built specifically to clone the style (commit 2026-10-25).

### 3. You Built It (@youbuiltit), TikTok, https://www.tiktok.com/@youbuiltit
- **Existence:** VERIFIED (snippet). "You Built It (@youbuiltit)". Bio says it is the official page and warns about copycats. The snippet suggests ~117.9K followers and ~2.9M likes, but the layout was ambiguous.
- **YouTube:** "You Built It", https://www.youtube.com/@youbuilt_it (channel UCNMUzfDYWY329ftlf25Acuw). The description says it explains how everyday objects work, and its structured data links the TikTok as `sameAs`. It shows an unlabelled interaction count of 55,800 (possibly subscribers).
- **Do not confuse with** X/GETTR @YouBuiltIt ("Signs of the Times"), a religious/political account that is unrelated.
- **"How a Hole in Your Yard Becomes a Swimming Pool", 13.0M views:** **UNVERIFIED.** No search result matched the title.
- **Style, tools:** not verifiable. INFERENCE: 3D process/cutaway animation (dig → rebar → gunite → tile → fill), the same genre as Jared Owen-style cutaways and the AI "secret bunker build" timelapses.
- **Note on the follower gap:** INFERENCE. ~118K followers alongside a claimed 13M-view video would fit a single breakout hit. Confirm directly on TikTok.

### 4. @pancarte_media, NOT VERIFIED
- Exact-match searches for "pancarte_media" and "pancarte media" returned nothing about the account. "Pancarte" is French for "placard/sign", so results were swamped by that word. The handle appeared only once, in a tag-list snippet ("FieldLedger, pancarte_media") with no content.
- **"If the zombie apocalypse starts while you're on a cruise ship", 5.7M: UNVERIFIED.** A cruise-ship title does exist in the same title family (snippet listed plane/train/**cruise ship**/aquarium variants) but it was **not attributed** to pancarte_media.
- **The title format itself is VERIFIED** as an active multi-creator trend (see #7). Comparable creators: the_whatif_animator, "Doodle Animation" (plane, Part 1), and Stickstories24 (@moofyyy, school, stick-figure). There is also an automated interactive zombie Reels pipeline on GitHub, https://github.com/anshdeepofficial1/ZMB (vector animation, comment-driven).

### 5. Zack D. Films, YouTube https://www.youtube.com/@zackdfilms (UCvz84_Q0BbvZThy75mbd-Dg)
- **Scale:**
  - VERIFIED. vidIQ (snippet, 2026-10-21): 29,300,000 subs, 80,981,273,242 views, 4,109 videos, and 3,939,468,327 views from 2026-09-24 to 2026-10-21. A later vidIQ snippet says ~29.5M.
  - Tubefilter, week of 10/12–10/18/2026: **#1 most-viewed channel worldwide**, 1,106,821,498 weekly views, all-time 80,425,322,383 (https://www.tubefilter.com/?p=194709).
  - Social Blade ~27.6M (mid-2026). NamuWiki 27.4M (June 2026).
- **Top videos:** all with caveats.
  - Most-watched Short as of Sept 2023 was the McDonald's McFlurry spoon explainer (Tubefilter 2023, no count given).
  - An AGT magic-trick explainer Short from May 2022 is reported at "over 70 million views" (GoldApp, weak source).
  - OutlierKit lists "Ohio's 1986 Balloon Disaster" at 16.0M (conflicts with the other two).
  - No reliable per-Short count for 2026 was found.
- **Evolution:** NamuWiki (wiki, medium reliability) says early videos used real photos with Zack on camera, Blender/CGI grew from mid-2023, and videos were fully CGI from late 2023.
- **Tools:** VERIFIED as a self-claim by a contractor, not by the channel. A freelance 3D artist's portfolio (Chris Reilly, https://supersets.chrisreillyportfolio.com/zackdfilms.php, via snippet) claims 100+ shorts for the channel. It names **Blender** as the main tool, plus **Cascadeur** (physics-assisted character animation), **BlenderKit**, **After Effects**, **EmberGen**, royalty-free assets, templated compositing and "some physics simulation", with a "mechanized" pipeline. The Gumroad course by Chris Reilly (https://80lv.gumroad.com/l/robotic-wolf-vfx-in-blender) says he has worked for "viral media like Zack D." **Narration:** no primary source confirms whether it is AI or human (an article explicitly says so).
- **Style:** INFERENCE plus secondary sources. Stylised-realistic 3D characters ("Pixar-style"), cinematic close-ups, fast cuts, first-person "you" narration about body, survival and science scenarios, a dark-humor/"nightmare fuel" tone. Widely imitated: there are Fiverr/Upwork "Zack D Films style" gigs and Gumroad Blender project files (zyckwealth.gumroad.com), and a meme culture remixes his narration.

### 6. What If (Underknown), YouTube @whatifscienceshow
- VERIFIED: ~8.9M subs and 1.7B views (OutlierKit snippet). Social Blade ~8.95M. Channel created 2018-07-18 per Social Blade.
- Underknown (Toronto) also makes Spanish, Japanese and Mandarin versions, and claims 14M+ monthly cross-platform followers (2022 press release). The series began in a co-founder's living room and won the Webby People's Voice award in 2020 (https://en.wikipedia.org/wiki/Underknown). The Spanish channel "Qué pasaría si" had ~3.15M subs (vidIQ, Apr 2025).
- Style and tools: **not verified** by search. INFERENCE: 3D CGI space/planet visuals with a narrator. One tracker says a presenter named "Peter" hosts (weak).

### 7. the_whatif_animator (@the_what_if_animator), TikTok + YouTube
- VERIFIED from snippets:
  - "If the zombie apocalypse starts while you're in a mall (Part 1) 🧟🛍️ Would you tell them?": ~208K likes, 781 comments.
  - Part 2 ("Would you go through that room?"): ~53K likes, 474 comments. YouTube copy: https://www.youtube.com/watch?v=1jzo3Na5WaY.
  - Ski trip, "don't make a sound" (Part 2): https://www.youtube.com/watch?v=MIFYi5JlJrU.
  - Hospital, "always go up" (Part 2): https://www.youtube.com/watch?v=2Sejj1aVqL8 (hashtags #zombieapocalypse #survival #zombie #whatif #animation).
- **Script pattern (VERIFIED from titles):** a fixed title template ("If the zombie apocalypse starts while you're [location]…"), a survival **rule** as subtitle ("don't make a sound", "always go up"), **multi-part** serialization, and a **question CTA** ("Would you tell them?"). This drives comments and binge-following. Part 2 gets fewer likes than Part 1 (drop-off between parts).
- Visual style (3D vs. 2D) and tools: **not verified** (search budget ran out).

### 8. @moon2animation, TikTok
- VERIFIED: https://www.tiktok.com/@moon2animation/video/7694128821317995790, posted 2026-10-08 (ID-decoded), 148.9K likes, 1,624 comments. Caption: "What if every electron disappeared for 1 second? Light stops. Sound stops. Nothing is solid anymore… Would you notice before it ended?" Tags: #pov #simulation #3danimation, with a beach/sunset setting. Shows fast topic-cloning within 48 hours.

### 9. The What If Studio (@thewhatifstudio), TikTok
- VERIFIED (snippet): ~279.2K followers. Posts 3D science sims, e.g. "what if every human clapped at the same time". Caption hook: "👏 You asked for it (4,142 of you)…", a comment-request loop used as social proof. A secondary "2.4M/2.2M" figure is unlabelled.

### 10–11. POV: What If (@pov.what.if0, ~123.1K followers); What if Animation (@whatif.animation, ~280.4K followers); @what.if.animation (~25.7K)
- VERIFIED (snippets only). Generic what-if POV accounts. Style not verified. They show how crowded the handle space is.

### 12. Jared Owen, YouTube
- VERIFIED: makes 3D animations in **Blender** (BlenderNation "Meet the artist", https://www.blendernation.com/2018/11/19/meet-the-artist-jared-owen/, and other coverage). He has said he picked Blender because it is free. ~4.4M subs, 529M views, 120 videos (2026 trackers). The TubeTalk podcast (https://tubetalk.buzzsprout.com/271511/episodes/19196651-how-jared-owen-builds-3d-videos-that-last) credits 500M+ views to evergreen "how it works" topics over trend-chasing.
- Style (INFERENCE / general knowledge): clean, bright stylised 3D cutaways, an orbiting camera revealing internals, narrated. This is the closest established analogue for the "@youbuiltit" construction-process genre.

### 13. Lesics, YouTube
- VERIFIED (self-reported on https://lesics.com/engineering-animation.html): 6.74M subs, 1,022,235,067 views. 3D engineering explainers. Also sells animation services.

### 14. Hashem Al-Ghaili
- VERIFIED: science communicator and filmmaker. Realistic CGI **concept videos** (EctoLife artificial-womb facility, which viewers mistook for real; he told AFP it was a concept film). Claims 45M+ followers across platforms (Khaleej Times). Facebook 32M+ in older coverage. Also made the animated short "Punch Monkey" and is developing the feature *Orbital*. Relevance: "realistic futurist hypothetical" adjacent to 3D what-ifs. Not strictly faceless shorts.

### 15. The Data Ball, YouTube
- VERIFIED (vidIQ snippet): 275K subs, 143 videos. 3D scale comparisons. Says each 3D video takes 100+ hours. Useful as a cost benchmark for hand-made 3D.

### 16–17. Viral single-video 3D CGI creators (reference points)
- **@aleksey_nz (Aleksey Patrev):** CGI "giant Moon at the North Pole" TikTok with "over 32.9 million views". Fact-checkers (Logically, The Quint, Snopes) flagged it as animation mistaken for real.
- **@lights.are.off:** 3D "giant statues on the ocean floor", 1.8M followers (Lead Stories, Dec 2023).
- Lesson (INFERENCE): photoreal 3D what-ifs can outperform but risk misinformation flags, which is one reason TikTok's AI/CGI labels matter.

### Niche: AI "secret underground bunker build" timelapse Shorts (YouTube)
- VERIFIED that the niche exists, via multiple Shorts:
  - https://www.youtube.com/watch?v=KmCmWFWLrZ4 (#aitimelapse #aibuild)
  - https://www.youtube.com/shorts/4DMhtq2ia3A ("1 minute to Build a Completely Invisible Underground Concrete Bunker…")
  - https://www.youtube.com/shorts/O6YsbNQQ-sA
  - Several self-describe as **AI-generated** construction timelapses.
- View counts and channel names were not surfaced. Format: zero-to-finished construction in under 60 s, "300× speed" framing, luxury reveal at the end.

---

## Cross-cutting findings

### What appears to drive retention (evidence quality noted)
1. **Hook in 0–3 s.** Third-party vendor blogs only; there is no official YouTube data, and YouTube does not expose swipe-away directly.
   - Claimed benchmarks: <30% swipe-away in the first 3 s = strong hook; ~80% retention at 3 s as a target; "~70% decide in first 2 s" (attributed to TikTok, unsourced). Examples: bytecap.io, quso.ai and shortsfast.com blogs.
   - Treat all of these as rules of thumb.
   - VERIFIED exemplar: man_ia_c puts the full question on screen at frame 0 with one highlighted keyword and starts a countdown immediately.
2. **Countdown / telemetry counters.** VERIFIED in man_ia_c: an ms-precision countdown, "time slowed 11×", and a live "EARTH IS NOW X MILES WIDE" counter. VERIFIED via article in lunarcheeseee: an mph countdown from 1,037 with named thresholds (1,028, 800). INFERENCE: counters create an implicit "watch until it hits zero" contract.
3. **Escalation ladder plus a twist ending.** VERIFIED in man_ia_c: park → hands → people → planet → Moon → "nothing left to come back to". Lunarcheeseee escalates by speed thresholds.
4. **POV / second person ("You're in Central Park…").** VERIFIED in captions (man_ia_c, moon2animation, #pov tags).
5. **Comment-bait and serialization.** VERIFIED: "Which one next? 👇" (man_ia_c), "Would you tell them?" and Part 1/Part 2 (the_whatif_animator), "You asked for it (4,142 of you)" (The What If Studio).
6. **Topic recycling.** VERIFIED: "Earth stops spinning" (Zack D 2025 → lunarcheeseee 2026). Electrons-vanish was cloned within 2 days.
7. **Long for a "short".** VERIFIED: the man_ia_c video is ~80 s. TikTok rewards longer completions. INFERENCE: these are not 15 s clips.

### Public tutorials and tooling evidence
| Source | What it shows | Status |
|---|---|---|
| YouTube: "How to Make Viral Animations Like Zack D. Films (Full Blender Guide)", https://www.youtube.com/watch?v=CHDc3dwdso0 | Blender workflow | Exists (contents not viewed) |
| YouTube: "I Finally Made A Zack D Film Youtube shorts In Blender 3D", https://www.youtube.com/watch?v=GtIkLLgDFpQ | Blender | Exists (contents not viewed) |
| YouTube: "How to Create Zack D. Film style videos with AI", https://www.youtube.com/watch?v=JZc6ezIx0Ec | AI pipeline | Exists |
| YouTube: "How to Create Zack D Films Style 3D Shorts With AI", https://www.youtube.com/watch?v=q4IlJA0mC_I | **OpenArt** | VERIFIED (snippet) |
| TikTok discover "What Software Does Zack D Use" | AI recreations using **ChatGPT, Nano Banana, ElevenLabs** | VERIFIED (snippet) |
| Medium: "How I Create Zack D Films Style 3D Shorts With AI" (https://medium.com/@lazargrr1/how-i-create-zack-d-films-style-3d-shorts-with-ai-its-easy-3dd9450b4f0a) | AI pipeline | Exists |
| Vendors: Snaplama, autoclips.app, getziztu.com, starpop.ai ("Zack D. Films ad format explained"), Higgsfield "Content Factory" (topic → script → visuals → voiceover → edit, 15 s–5 min) | AI video generators | Vendor claims |
| YouTube: "How to Make Viral What If Stickman Videos With ONE Prompt", https://www.youtube.com/watch?v=q9SSp373RQQ | AI | Exists |
| GitHub zNightmare15/what_if_project | **Three.js + Blender EEVEE + edge-tts + FFmpeg**, JSON story templates, subtitle HUD | VERIFIED (cloned and read) |
| Chris Reilly (Zack D contractor) | **Blender, Cascadeur, BlenderKit, After Effects, EmberGen** | VERIFIED as contractor self-claim (snippet) |
| Jared Owen | **Blender** | VERIFIED (interviews) |
| Fiverr / Upwork gigs ("Zack D Films style Blender 3D animation", "low poly 3d shorts") | Blender outsourcing market | VERIFIED (listings exist) |

Summary of the toolchain evidence: the only **creator-attributed** tooling is Blender (Jared Owen; Zack D via a contractor). For the newer TikTok what-if accounts (man_ia_c, lunarcheeseee, moon2animation), **no tooling is disclosed**. man_ia_c's video carries TikTok's "AI-generated" label, so AI involvement is confirmed but the method is not.

---

## Sources (all accessed via WebSearch snippets on 2026-11-02 unless noted)
- TikTok discover, Lunarcheese: https://www.tiktok.com/discover/lunarcheese
- LADbible (2026-10-05): https://www.ladbible.com/news/science/horrifying-simulation-earth-stop-spinning-712101-20261005
- LADbible on X: https://x.com/ladbible/status/2107068745856254136/photo/1
- UNILAD Tech (2025-08-06, Zack D Earth-stop): https://www.uniladtech.com/social-media/simulation-shows-what-happens-if-earth-stopped-spinning-757987-20250806
- man_ia_c electrons video: https://www.tiktok.com/@man_ia_c/video/7693494009494342945
- moon2animation electrons video: https://www.tiktok.com/@moon2animation/video/7694128821317995790
- GitHub what_if_project (cloned; frames and audio inspected): https://github.com/zNightmare15/what_if_project
- You Built It TikTok: https://www.tiktok.com/@youbuiltit ; YouTube: https://www.youtube.com/@youbuilt_it , https://www.youtube.com/channel/UCNMUzfDYWY329ftlf25Acuw/about
- the_whatif_animator YouTube copies: https://www.youtube.com/watch?v=1jzo3Na5WaY , https://www.youtube.com/watch?v=MIFYi5JlJrU , https://www.youtube.com/watch?v=2Sejj1aVqL8
- Zombie Reels automation repo: https://github.com/anshdeepofficial1/ZMB
- Zack D. Films: https://vidiq.com/youtube-stats/channel/@zackdfilms/ ; https://socialblade.com/youtube/handle/zackdfilms ; https://en.namu.wiki/w/Zack%20D.%20Films ; https://www.tubefilter.com/?p=194709 ; https://www.tubefilter.com/2023/09/19/top-50-most-viewed-us-youtube-channels-week-of-09-17-2023/ ; https://outlierkit.com/channel/zackdfilms ; https://goldapp.it.com/people/zack-d--films.html ; https://supersets.chrisreillyportfolio.com/zackdfilms.php ; https://80lv.gumroad.com/l/robotic-wolf-vfx-in-blender ; https://celebtechbuzz.com/zack-d-films/ ; https://zackdfilms.fandom.com/wiki/Zack_D._Films
- What If / Underknown: https://en.wikipedia.org/wiki/Underknown ; https://socialblade.com/youtube/handle/whatifscienceshow/videos ; https://outlierkit.com/channel/whatifscienceshow ; https://www.tubefilter.com/2022/03/18/underknown-educational-youtube-content-acquire-aperture/ ; https://vidiq.com/youtube-stats/channel/UC5BW1w7JyJW3r8rpR3BhqKA
- TikTok what-if accounts: https://www.tiktok.com/@pov.what.if0 ; https://www.tiktok.com/@whatif.animation ; https://www.tiktok.com/@what.if.animation ; https://www.tiktok.com/discover/what-if-animations ; https://www.tiktok.com/discover/what-happens-if-electrons-disappear
- Jared Owen: https://www.blendernation.com/2018/11/19/meet-the-artist-jared-owen/ ; https://tubetalk.buzzsprout.com/271511/episodes/19196651-how-jared-owen-builds-3d-videos-that-last ; https://avid.wiki/Jared_Owen_Animations ; https://outlierkit.com/channel/jaredowen
- Lesics: https://lesics.com/engineering-animation.html
- Hashem Al-Ghaili: https://en.wikipedia.org/wiki/Hashem_Al-Ghaili ; https://www.khaleejtimes.com/uae/kt150-judge-hashem-al-ghaili-viral-science-filmmaking-global-influencer ; https://www.cartoonbrew.com/cgi/fertility-factory-animated-video-fools-thousands-224823.html
- The Data Ball: https://vidiq.com/youtube-stats/channel/UCMxWtY5Wd_h8MohaM0gDWHQ
- Kurzgesagt: https://en.wikipedia.org/wiki/Kurzgesagt ; https://aifreeforever.com/chart/youtube/top-education-channels
- Moon CGI fact-checks: https://www.logically.ai/factchecks/all/8384e274 ; https://www.thequint.com/amp/story/news/webqoof/animated-video-used-to-show-supermoon-blocking-sun-at-arctic-fact-check
- @lights.are.off: https://korean.leadstories.com/hoax-alert/2024/01/fact-check-video-does-not-show-giant-statues-at-the-bottom-of-the-ocean.html
- Bunker AI Shorts: https://www.youtube.com/watch?v=KmCmWFWLrZ4 ; https://www.youtube.com/shorts/4DMhtq2ia3A ; https://www.youtube.com/shorts/O6YsbNQQ-sA
- Tutorials: https://www.youtube.com/watch?v=CHDc3dwdso0 ; https://www.youtube.com/watch?v=GtIkLLgDFpQ ; https://www.youtube.com/watch?v=JZc6ezIx0Ec ; https://www.youtube.com/watch?v=q4IlJA0mC_I ; https://www.youtube.com/watch?v=q9SSp373RQQ ; https://www.tiktok.com/discover/what-software-does-zack-d-use ; https://medium.com/@lazargrr1/how-i-create-zack-d-films-style-3d-shorts-with-ai-its-easy-3dd9450b4f0a ; https://www.snaplama.com/blog/how-to-create-animation-videos-like-zack-d-films-in-2026 ; https://starpop.ai/blog/articles/zack-d-films-ad-format-explained ; https://higgsfield.ai/blog/higgsfield-introduces-content-factory ; https://www.upwork.com/services/product/video-audio-zack-d-filmsstyle-cinematic-short-blender-3d-animation-simulations-1983070890520437486
- Retention (vendor blogs, low reliability): https://www.bytecap.io/research/youtube-shorts-retention-benchmarks ; https://quso.ai/research/video-retention-benchmarks ; https://shortsfast.com/blog/faceless-shorts-hooks-retention-2026/ ; https://subscribr.ai/youtube-strategy/youtube-shorts-low-watch-time-boost

## Open items for a follow-up turn
- Get tiktok.com, youtube.com and ladbible.com allowed in the session network settings so view counts can be read directly. This is needed to confirm the PDF's 28.9M / 17.5M / 13.0M / 5.7M figures.
- Search again (budget exhausted) for: @pancarte_media on other platforms; the_whatif_animator's visual style; Animagraffs; the contents of the Zack D Blender tutorials; @youbuiltit's top videos.
