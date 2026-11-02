# Faceless 3D Studio — Research Report (Phase A)

_2 November 2026. Rendered version: `research_report.html`. Full source notes: `creators.md`, `technical_blender_pipeline.md`, `ai_tools.md`, `platform_policies.md`._

## 0. Summary and how to read this report

**Bottom line:** this is buildable on your own computer with mostly free software. **Blender 5.2 LTS** does all 3D work. It is driven by **Python scripts that Claude Code writes and runs headlessly** from a structured storyboard, and rendered with **EEVEE**. Audio uses local open-source TTS plus a licensed SFX library, captions and counters are added in a separate step, and **FFmpeg** assembles the final 1080×1920 video. Automated QC runs before anything reaches you for approval. The realistic monthly cost is **$20–55**, plus a one-time hardware upgrade only if your computer lacks a reasonable GPU.

**What matters most:** the playbook's own data, and the creators we could verify, both say the premise, hook and escalation decide results, not the render quality. The system should therefore make ideas cheap to test, and keep each video genuinely new so it doesn't trip the platforms' "unoriginal / inauthentic / mass-produced" rules.

**How confident to be in this research:**
- This research ran in a cloud sandbox whose network allowlist **blocked direct access** to tiktok.com, youtube.com, blender.org, support.google.com, Meta pages and most vendor sites. Most findings therefore come from search-engine excerpts of those pages, not the pages themselves.
- Each claim in the appendices carries a label:
  - **VERIFIED** means a cited source (excerpt) supports it.
  - **SECONDARY** means a third-party source.
  - **INFERENCE** means my reasoning.
  - **UNVERIFIED** means claimed but not confirmed.
- Frame-by-frame analysis was only possible for one reference video, through a public GitHub repo containing its extracted frames. Prices and policies should be re-checked on official pages before any spending or launch.
- The playbook's own performance numbers are self-reported marketing claims and are not treated as expected results.

**Report map:**
- §1–3: the playbook, the creators and the formats.
- §4–8: how these videos are made, and the tools.
- §9–12: style, architecture, and a worked storyboard-to-Blender example.
- §13–17: hardware, costs, roadmap, risks and the recommendation.
- Appendices A–D: the full research notes with every source.

## 1. The Faceless 3D Playbook — page-by-page analysis

Source: "The Faceless 3D Playbook", Morrow Studio, 14 pages, 2026. Every number below is self-reported by the authors ("Our results. Not typical."). None of it is independently verified, and pages 13–14 are a sales pitch for a paid Skool community ($67–$99/month), so the document is also marketing.

| Page | Content | What it actually teaches | Critical note |
|---|---|---|---|
| 1 | Cover: 35,374,670 views on 64 shorts, Oct 5–26 2026; 12 past 1M; 4 sample frames (3.1M, 2.6M, 300K, 260.2K) | The four formats in one glance. Every frame is bright and daytime, with a counter or label in the top-left and a serif italic caption at lower-middle. | The frames show the look: simple blocky "Roblox-like" low-poly people, semi-realistic water and sky, real-place props (pier, palm trees). |
| 2 | "Tested on our own accounts": 64 shorts, 2 new TikTok accounts, 3 weeks, all built with Claude Code | Proof that one person plus Claude Code plus Blender-class tools can produce roughly 3 shorts a day. | It says "This is the why, not the how": no prompts, no code. The method is behind the paywall. |
| 3 | Market: other channels (@lunarcheeseee 28.9M, @man_ia_c 17.5M, @youbuiltit 13.0M, @pancarte_media 5.7M); "why it works now" | (a) A question opens a loop in second one. (b) 3D makes the impossible look real: real place plus one impossible change. (c) No face means no ceiling, and the same file can go to TikTok, Shorts, Reels and Facebook. | View counts were "checked Oct 27 2026". See the creator report for what could be verified. |
| 4 | Format 1, 3D what-if: "Everyone on Earth farts at once" (3.1M), "Absolute zero for 5 seconds" (2.6M) | One-line premise a 10-year-old gets; famous sunny place (South Beach, Santa Monica Pier); live counter; ending that triggers arguments; **the 5-second twist** (change something for only ~5 s). All 12 million-view videos were what-ifs. | "Trap": the most copied format, so the look is never the edge. The premise is. |
| 5 | Formats 2 and 3: Zombie survival (their farm video 260.2K vs @pancarte_media 5.7M), How it's built (their underground greenhouse 300K vs @youbuiltit 13.0M) | Zombie: day 1, one place, one plan, each scene a choice with a cost, a day counter, and every episode ends on the next day (built-in Part 2). Build: a cutaway from hole to finished thing; every shot further along; the finish is a reveal (pool full, lights on). | Key line: "The subject wins these, not the graphics". The biggest build videos are things people already dream about (pool, bunker, igloo). |
| 6 | Format 4, long-form: 1,581,626 YouTube views in 28 days; Earth-rotation film frame | Stretch one what-if into a 5–8 min film: "a ladder, not a list" (each step bigger), a clock on screen ("One day lasts 8 months"), "one world, two lengths" (sets reused). They claim a film on reused sets used 1–3% of a Claude Max week. | The shared DNA of all four formats: **a question, a real place, escalation, a payoff**. |
| 7 | Idea rules 1–4 | 1. Change one everyday thing (water 1.5M, absolute zero 1.3M, friction 1M). 2. Bright, busy, famous: beach videos hit 1M+, while space/Moon/night stalled at 51–76K. 3. Comments are the idea list: requested videos did 1.2M and 1M+, while a copied competitor hit stalled at 105K. 4. Something new every 2–3 s, plus a moving on-screen number. | Range on the same look, same account: 24K to 1.5M. The idea is the variable. |
| 8 | Rules 5–7 + one-line test | 5. Running joke ("And yes. There's a tsunami." became a meme; one comment got 37.6K likes). Play with it, don't repeat the video. 6. Write for one country (US units and places), since the audience mix affects TikTok pay. 7. Idea beats polish. One-line test: "wait, then what happens?" means yes; "huh?" means no. | Rule 5 and Mistake 3 pull against each other: a recurring joke is good, a recurring *video* is flagged. |
| 9 | Money: TikTok Creator Rewards needs 61 s+; standard ~$0.25/1K qualified views; "Additional Reward" $2.50–$4.02/1K; US audience, searchable "real knowledge" topics and longer watch time helped | Plan 61 s+ from the first draft (story, not padding). | Their 3.1M "fart" video earned only $4.43 at 1.4M views: wrong audience mix, no bonus. Virality ≠ revenue. |
| 10 | Receipt: one new account's first week, $677.99 ($264.71 standard + $413.28 additional) on 12M post views; 38K followers | Money comes in spikes from 1–2 videos. | Explicitly "best stretch, best account, format's peak". |
| 11 | Mistakes 1–4 + "5 flags in 30 days = out of Creator Rewards" | 1. Re-uploading the same file (both copies disqualified, $619.25 lost). 2. Copying a script word for word (flagged in minutes; TikTok matches words and voice). 3. Same set, opening and ending (the 1.5M tsunami video was flagged "non-original"). 4. Popular free music (suspected cause of a "repurposed" flag), so they dropped music beds entirely. | They reached 4 of 5 flags. Verified against official policy in §Policy. |
| 12 | Mistakes 5–7 + checklist | 5. Under 61 s earns $0. 6. Look-alike accounts get "not recommended" for impersonation. 7. Judging too early: hits took 20–90 h to take off; judge after 24 h by views/hour and like rate (hits 5–15% like rate; under 4% flopped); deleting during an appeal can cost the appeal. Five-question pre-post checklist. | The like-rate thresholds are a useful internal KPI, but they come from one sample. |
| 13 | "One video is easy, one a day is hard" | A clip from one prompt is not a 61-second story; a single video takes a 3D artist, an editor and a sound designer; originality is needed every time. They claim a short costs ~1% of a Claude Max week, on a Mac/Windows machine with **no graphics card**. | Strong hint about their stack: local rendering, no dedicated GPU, which points to Blender EEVEE on integrated/Apple GPU or a WebGL/Three.js renderer (inference). |
| 14 | Sales page (skool.com/morrow) | — | Not a source of technique. We do not need it, and I will not sign up for anything. |

#### What the playbook implies about production (inference, not stated)
- Visuals in the screenshots: blocky low-poly humanoids (box torso, box head, no faces) in large crowds, semi-realistic sky/ocean (reads like Blender's Ocean modifier or a shader ocean, plus an HDRI sky), a real-world-ish pier and palms, cutaway soil cross-sections with rock texture, and a cartoon farm scene with a bearded farmer and dog (this one is a more detailed toon character, likely a stock or AI-generated rigged model).
- Text: small all-caps label plus a large serif counter top-left ("GAS RELEASED 738,000,000 L"), italic serif subtitle lines in the lower third, and bold all-caps meme captions with a single highlighted yellow word for the zombie format.
- "No graphics card" plus "your own computer renders it" means scenes are designed to render cheaply: simple geometry, few lights, no heavy volumetrics.

#### The ten transferable rules (my synthesis)
1. One-sentence premise that passes the "then what?" test.
2. Real, bright, crowded, recognisable place: the contrast between the normal place and the impossible change is the hook.
3. Short, bounded impossibility (5–10 s) with long consequences.
4. A beat every 2–3 s, each one a consequence, never random cuts.
5. A persistent on-screen number (counter, clock, day count).
6. An ending built to be argued about in the comments.
7. A recurring line or element that rewards regulars, varied each time.
8. Target audience defined up front (US units, US places).
9. 61–80 s by design for TikTok monetisation; the extra time is story.
10. Every upload new in set, opening shot, camera path, script and sound, including new relative to our own previous videos.

## 2. Creator analysis (summary)

Full per-creator notes with sources are in Appendix A. 17 creators/channels were checked: 3 of the 4 playbook creators were confirmed to exist, plus 13 more. **None of the playbook's four view counts could be independently confirmed.** The one for @lunarcheeseee is consistent with the 2.5–3.5M likes visible in search excerpts.

| Creator | Platform | Format | Observed style | Scale (source) | Tools (evidence?) |
|---|---|---|---|---|---|
| @lunarcheeseee (Lunar Animation) | TikTok | What-if, planetary disasters | 3D destruction, speed counter (1,037 mph → 0) | Earth-stop video 2.5–3.5M likes; LADbible coverage 2026-10-05 | None disclosed |
| @man_ia_c ("What if?") | TikTok | What-if physics | Blocky low-poly people, semi-real park, then X-ray wireframe, then space, then point cloud; serif type, ms countdown HUD | Electrons video ~80 s, posted 2026-10-06; views unverified | None disclosed. Every frame carries TikTok's **"AI-generated"** label |
| @youbuiltit (You Built It) | TikTok + YouTube | How it's built / how things work | Not verified | ~118K followers, ~2.9M likes (snippet) | None disclosed |
| @pancarte_media | TikTok | Zombie scenario | — | **Could not be found** | — |
| Zack D. Films | YouTube Shorts, TikTok | 3D explainers / survival / what-if | Stylised-realistic, Pixar-ish characters, cinematic camera | 29.3M subs, 81B views; #1 most-viewed channel worldwide, week of Oct 12–18 2026 (Tubefilter) | A freelancer who says he made 100+ of its shorts names Blender, Cascadeur, After Effects, EmberGen (secondary) |
| What If (Underknown) | YouTube | Science what-ifs | 3D CGI + narration (inference) | ~8.9M subs | — |
| the_whatif_animator | TikTok + YouTube | Zombie scenario, multi-part ("…while you're in a mall") | Animated | Mall pt1 ~208K likes, pt2 ~53K | — |
| @moon2animation | TikTok | What-if (cloned the electrons topic 2 days later) | 3D | 148.9K likes | — |
| @thewhatifstudio / @whatif.animation / @pov.what.if0 | TikTok | What-if | 3D | ~279K / ~280K / ~123K followers | — |
| Jared Owen | YouTube | 3D cutaways "how it works" | Clean stylised cutaways | ~4.4M subs | **Blender (his own interviews)** |
| Lesics | YouTube | 3D engineering explainers | Technical 3D | 6.7M subs (self-reported) | — |
| Hashem Al-Ghaili | Multi | Photoreal CGI concepts | Photoreal | 45M+ followers claimed | — |
| The Data Ball | YouTube | 3D scale comparisons | 3D | 275K subs; says 100+ h per video | — |
| @aleksey_nz, @lights.are.off | TikTok | Single viral photoreal CGI | Photoreal | 32.9M views (2021), 1.8M followers (2023) | — |

**Observed patterns (from verifiable material):**
1. **The full question is on screen from frame 1** (e.g. the serif hook title with one highlighted keyword).
2. **A ticking number** is almost universal: countdowns with milliseconds, mph falling, miles-wide growing, day counters.
3. **The script is an escalation ladder** that moves outward in scale (park → your hands → people → planet → Moon → aftermath) and ends on a twist or "nothing left".
4. **Second person** ("You're in Central Park…") plus a **comment prompt** ("Which one next? 👇") and **Part 1/Part 2 series**.
5. **60–80 s length**, consistent with TikTok's 1-minute Creator Rewards rule.
6. **Topics get cloned within 48 hours** (electrons: man_ia_c on Oct 6, moon2animation on Oct 8), so speed-to-publish on *your own* ideas matters, and the look is not a moat.
7. The leading what-if account **self-labels as AI-generated**: AI disclosure does not appear to block reach.

**Frame-by-frame reference: @man_ia_c "What if electrons disappeared for 5 seconds?"** (from the public reverse-engineering repo's extracted frames)

| Time | Phase | What's on screen | Device |
|---|---|---|---|
| 0–8 s | Normal world | Sunny Central Park, picnic blanket, low-poly people, glowing atom icon | Hook title + countdown "ELECTRONS DISAPPEAR IN 0:06.000" |
| 8–42 s | Event + cascade | X-ray wireframe world on black, POV wireframe hands, sand "bombs", people glowing | "ELECTRONS RETURN IN 0:04.821", "TIME SLOWED DOWN 11×" |
| 42–64 s | Planet scale | Glowing expanding Earth, Moon engulfed | Live counter "EARTH IS NOW 353,887 MILES WIDE", "THE MOON IS GONE" |
| 64–72.5 s | Return | Point-cloud park, "5 seconds later", second blast | "ELECTRONS BACK" |
| 72.5–80 s | End card | Title over black + one fact line | Comment CTA in caption |

Takeaways for us: 5 visual "worlds" in 80 s means the *style changes are the escalation*. The text system does most of the storytelling. Audio appears SFX-led (inference).

## 3. The four formats — production breakdown

| | What-if | Zombie/survival scenario | How it's built | Long-form film |
|---|---|---|---|---|
| Core hook | "What if X changed for N seconds?" | "Day 1 of … where would you go?" | "How a hole becomes a ___" | Same what-if, as a ladder of escalating stages |
| Viewer role | Spectator of a disaster | The protagonist making choices | The owner of the dream project | Learner on a journey |
| On-screen device | Live counter (litres, seconds, °F, people) | Day counter, resource icons (water/food/tools/land) | Progress/stage label, "Built" stamp | Clock/scale label ("One day lasts 8 months") |
| Structure | Premise (0–3 s), Normal → Event → 6–12 escalating consequences → Reset/twist → Payoff line | Setup → location choice → 4–6 decisions, each with a cost → cliffhanger "Day 2" | Empty site → excavation → structure → systems (water/power/light) → interior → lights-on reveal | Cold open → 6–10 rungs of escalation, each with an explanation → global consequence → reflective end |
| Length | 61–80 s | 61–90 s per episode | 61–80 s | 5–8 min |
| Typical shots | Wide establishing of famous place, crowd close-ups, aerial of consequences, satellite/global view | Isometric/top-down map with labels, character follow-cams, interiors | Fixed-angle cutaway timelapse, slow push-ins, final orbit reveal | Planet-scale shots, cutaways, recurring "home" location |
| Key 3D tech | Crowds, water/ocean, simple physics (floating, falling, debris), particles | Rigged hero character + walk/run cycles, props, simple NPC zombies, map labels | Boolean/cutaway terrain, modular build pieces animated in sequence, light switching | Planet shader, scale transitions, reuse of short-form sets |
| Hardest part | Believable crowd reactions at scale | Character acting and consistency across episodes | Smooth stage-by-stage modelling | Narrative depth and accuracy; render volume |
| Automation fit | Very high (templated event + consequence library) | Medium (needs a hero character pipeline) | Very high (stages are deterministic geometry operations) | Medium-high once the asset library exists |
| Recommended order | **1st** (playbook data and best automation fit) | 3rd | **2nd** (deterministic, very automatable) | 4th |

## 4. How these videos are technically made

**What the evidence shows:**
- The playbook says every video was built with **Claude Code** and rendered on the creator's own Mac/Windows computer with **no graphics card**.
- A third-party recreation of @man_ia_c's style uses **Three.js/WebGL rendered through a headless browser**, with a **Blender EEVEE** alternative path, **edge-tts** voice, **ASS subtitles** for the HUD and **FFmpeg** assembly.
- A Zack D. Films freelancer cites **Blender + Cascadeur + After Effects + EmberGen**.
- Jared Owen uses **Blender**.
- Several "secret bunker build" Shorts state they are **AI-generated video**, and @man_ia_c carries TikTok's AI label.

**Inference: the niche runs on three production families.**

| Family | How it works | Pros | Cons | Who (likely) |
|---|---|---|---|---|
| **Code-driven 3D** (Blender Python, or Three.js) | An LLM writes scene code from a storyboard; low-poly assets plus procedural geometry; offline render; FFmpeg | Cheap, fast, deterministic, fully original, scales with automation | Character acting is limited; needs an asset library | Playbook authors, the man_ia_c recreation, likely many new TikTok what-if accounts |
| **Hand-animated DCC** (Blender/C4D + Cascadeur + After Effects) | Artists model, animate and composite by hand | Highest craft and acting | Slow and expensive (The Data Ball: 100+ h per video) | Zack D. Films, Jared Owen, Lesics |
| **AI video generation** (Runway, Veo, Kling…) | Text/image-to-video clips stitched together | Photoreal, fast for single shots | Weak continuity and control; needs AI labels; easily templated (YouTube "inauthentic content" risk) | Bunker-build AI Shorts, photoreal CGI-bait |

**Our choice is family 1 (code-driven Blender), with targeted borrowing from family 2** (a proper rigged character and animation library) and **optional, later use of family 3** only as a style pass over our own renders, never as the source of the video.

**The typical shot recipe (code-driven):**
1. **Load a set kit:** terrain/ground, sky (HDRI or procedural Nishita sky), water (Ocean modifier), buildings and props from CC0 libraries.
2. **Scatter variation** with Geometry Nodes (seeded), so each video's layout is new.
3. **Instance characters** with offset animation cycles to form crowds.
4. **Animate the anomaly** with procedural keyframes, shader effects and, only when needed, a baked simulation.
5. **Animate the camera** from a move library: tracking, crane, orbit, crash zoom, with handheld noise.
6. **Render** an EEVEE image sequence.
7. **Overlay the text system** (hook title, HUD counter, captions).
8. **Build the sound design** from cues (impacts, risers, ambience) and add the narration.
9. **Normalise** loudness to −14 LUFS and export.

## 5. Blender and Python automation (analysis)

Full detail and sources are in Appendix B.

**Version:** pin to **Blender 5.2 LTS** (released 14 Jul 2026, supported to Jul 2028). It is GPL and free for any use, and you own your renders. Relevant features:
- Geometry Nodes bundles and closures (5.0).
- EEVEE ray-tracing overhaul and node-based cloth/hair (5.2, experimental).
- An ACES/HDR colour pipeline.

**How Claude Code drives it:**
- Versioned scripts run as `blender -b set.blend -P build_shot.py -- --shot s05.json`.
- Three stages: **build** (assemble the scene from the spec, save a `.blend` per shot for inspection), **bake** (any simulation to disk, with a fixed seed), **render** (EEVEE PNG/EXR sequence, with "placeholder + no overwrite" so a crash resumes instead of restarting).
- A low-resolution **preview render** (540×960, few samples) is checked before the final.
- Claude can **look at the rendered stills** (multimodal) and fix composition before the full render. This is the key quality loop.

**What Python can control:** effectively everything. Object creation and linking from libraries, Geometry Nodes inputs, materials and node trees, lights, world, cameras, constraints, keyframes and F-curve modifiers, drivers, NLA action strips, physics settings and bakes, render settings and output.

**API traps (confirmed changes the agent must know about):**
- Blender 5.0 removed `Action.fcurves`; F-curves now live in action **channelbags/slots**.
- Grease Pencil v3 changed its API.
- 5.0 video output requires `media_type='VIDEO'`.
- 5.2 changed Geometry Nodes modifier input access.
- The EEVEE engine id is `BLENDER_EEVEE_NEXT` in 4.2–4.5 and back to `BLENDER_EEVEE` in 5.x.

Most tutorials and model training data predate these, so the project needs a "Blender 5.2 API notes" file in its CLAUDE.md.

**MCP servers:** the community "blender-mcp" (≈32.7K stars, renamed "MCP for Blender") and Blender Lab's official MCP (5.1+) let Claude drive a *running GUI* Blender. They are useful for interactive look-development of kits and characters, but **not** for batch production, which should be plain headless scripts.

**Headless EEVEE:** EEVEE needs a GPU (it is OpenGL/Vulkan/Metal based). It works on Windows and macOS desktops. On a display-less Linux server it may need EGL or a virtual X server (Xvfb). Smoke-test it on your machine in Stage B; Cycles is the fallback.

**EEVEE vs Cycles:**

| | EEVEE (recommended default) | Cycles |
|---|---|---|
| Quality | Very good for stylised and semi-real; soft shadows, AO, bloom, DOF, ray-traced reflections | Physically accurate GI, caustics, true glass/water |
| Speed, 70 s short (2,100 frames, 1080×1920) | ≈35 min–2.5 h on RTX 4070; ≈1.2–3.5 h on RTX 3060 (estimate) | ≈5–18 h on RTX 4070; days on CPU (estimate) |
| CPU-only | Not possible | Possible but very slow |
| Use for | All shorts | Occasional hero shots or thumbnails, if ever |

**Physics policy:** fake by default (keyframes, noise modifiers, drivers, shader effects, the Ocean modifier needs no bake). Simulate only when the motion *is* the hook, such as building collapse (Cell Fracture + rigid body), splashes (particles; Mantaflow rarely) or cloth (flags, towels). Always bake to disk with a pinned seed before rendering.

**Camera automation:** a library of parameterised moves maps storyboard words to code:
- `establishing_wide`, `crash_zoom`, `track_alongside`, `crane_up`, `orbit_reveal`, `top_down_snap`, `telephoto_static`, `pov_handheld`.
- Implemented with Follow Path / Track To / Damped Track constraints, keyframed focal length and DOF, and a noise F-curve modifier for handheld shake.
- Composition rules (subject in the upper-middle third of a 9:16 frame, clear of the platform UI) are applied automatically and checked in QC.

**Three.js verdict:** deterministic capture is possible but fragile, and it would duplicate the asset pipeline. Use it later for **instant browser previews or an approval page**, not for final renders. Blender renders every final frame.

**Post-production:**
- **FFmpeg** (free) for concat, overlays, ASS subtitles with animated captions and counters, and two-pass loudnorm to −14 LUFS / −1 dBTP.
- **WhisperX / faster-whisper** for word-level caption timing.
- Not recommended for automation:
  - DaVinci Resolve: scripting needs the paid Studio version.
  - CapCut: no API, and its terms reportedly prohibit automation.
  - MoviePy v2: breaking API changes.
- **Remotion** is a good alternative for animated text (free for individuals and companies of 3 or fewer).
- **Blender's VSE** is possible but slower than FFmpeg for this.

## 6. 3D modelling and animation tools compared

| Need | Best option for us | Alternatives | Cost / licence |
|---|---|---|---|
| Main 3D engine | **Blender 5.2 LTS** | Unreal Engine 5 (great real-time, heavier to script and set up; 5% royalty over $1M), Cinema 4D (paid, weaker automation) | Free, GPL |
| Real-time / web preview | Three.js (later, optional) | Babylon.js | Free, MIT |
| Environments | Geometry Nodes + CC0 kits (**Poly Haven, ambientCG, Kenney, Quaternius**); Ocean modifier; Sky texture | BlenderKit free tier, Poly Pizza (per-model, often CC-BY), Sketchfab (per-model licence) | Free |
| Characters | **Our own stylised base mesh** (modelled once) on a standard skeleton; MPFB2 (CC0 output) for humanoid bases | Quaternius characters (CC0), AI-generated (Meshy/Tripo/TRELLIS) + remesh + auto-rig | Free |
| Rigging | Rigify (built-in), **Mixamo auto-rigger**, AccuRIG 2 (free) | Auto-Rig Pro (paid, ~$40), UniRig (open source) | Free |
| Animation clips | **Quaternius Universal Animation Library v2 (CC0, 130+ clips)** + **Mixamo** (free, royalty-free, unmaintained, so download once) | Rokoko Vision (video-to-mocap, free tier), Cascadeur (physics-assisted keyframing; free tier non-commercial, Indie ~$8/mo) | Free |
| Retargeting | Rokoko Blender add-on (free) | Auto-Rig Pro | Free |
| Crowds | Geometry Nodes instancing of baked animated variants with time offsets | iCrowds / Procedural Crowds add-ons | Free |
| Physics | Built-in rigid body, Cell Fracture, cloth, particles, Mantaflow | EmberGen (paid) for fire/smoke | Free |

## 7. AI-assisted production tools compared

Full detail, prices and licence notes are in Appendix C. **Status changes:**
- **Ready Player Me shut down** (31 Jan 2026, after Netflix bought it).
- **OpenAI Sora is discontinued** (API retired 24 Sep 2026).
- **Mixamo** works but is unmaintained.

| Category | Use | Skip / caution | Notes |
|---|---|---|---|
| Script, storyboard, code | **Claude Code (subscription)** for interactive work; the API with batch and caching for unattended jobs | Local LLMs: not needed | Pro $20/mo, Max $100/$200 (verify current pricing) |
| Text/image-to-3D props | **TRELLIS.2** (MIT, local, needs a ~16–24 GB GPU) for free; **Meshy or Tripo Pro (~$20/mo)** if paid | Hunyuan3D (licence excludes EU/UK/South Korea), Stability 3D models (free only under $1M revenue), Luma Genie, CSM | Good for static props; characters need remeshing and rigging |
| Auto-rig / motion | Mixamo, AccuRIG 2, UniRig, Rokoko Vision free | Ready Player Me (dead), MDM/MoMask/MotionGPT for shipped work (non-commercial training data), DeepMotion free tier (non-commercial) | |
| Textures | Poly Haven / ambientCG (CC0); FLUX.2 klein 4B (Apache-2.0) in ComfyUI for custom tileable textures | FLUX dev weights (non-commercial), Ubisoft CHORD (research only) | |
| AI video | **Not in the core pipeline.** Optional later: Runway Aleph or Veo as a stylisation pass over our own renders | Sora (discontinued), Pika (weak control) | Triggers AI-label obligations; continuity problems |
| Voice (TTS) | **Kokoro-82M (Apache-2.0, local, free)**; Chatterbox (MIT, adds a watermark); **ElevenLabs Starter ($5–6/mo)** for the best quality | XTTS-v2 (non-commercial), F5-TTS (non-commercial), Fish/OpenAudio weights (non-commercial), ElevenLabs free (non-commercial + attribution) | Original voice for the channel; no voice cloning of real people |
| SFX | **Sonniss GDC bundles** (royalty-free, no attribution), Freesound **CC0 only**, our own Foley/synthesis; ElevenLabs SFX if subscribed | BBC SFX (non-commercial), AudioGen (non-commercial), Stable Audio Open (free only under $1M revenue) | Keep a licence log for every sound |
| Music | **None by default**, following the playbook's lesson; sound design carries the video. If needed, YouTube Audio Library (YouTube only) or TikTok Commercial Music Library | Popular "free" tracks (Content ID claims; a YouTube Short over 60 s with a claim gets blocked) | |
| Captions | **WhisperX** (BSD) / faster-whisper (MIT) | — | Word-level timestamps |

## 8. Recommended software stack

| Layer | Choice | Cost |
|---|---|---|
| Orchestration and creative | Claude Code (your subscription) + a project repo with CLAUDE.md, Blender API notes and the style guide | $20/mo (Pro) to start |
| 3D | Blender 5.2 LTS, EEVEE, Python `bpy` scripts, Geometry Nodes | Free |
| Assets | Our stylised character + Quaternius UAL2 + Mixamo clips; Poly Haven / ambientCG / Kenney / Quaternius environments; TRELLIS.2 or Meshy for one-off props | Free (Meshy optional $20) |
| Audio | Kokoro TTS (free) or ElevenLabs Starter; Sonniss + CC0 SFX; FFmpeg loudnorm | Free–$6/mo |
| Captions and overlays | WhisperX + generated ASS subtitles (captions, HUD counters, labels) | Free |
| Assembly | FFmpeg | Free |
| QC | Python (ffprobe, blackdetect, freezedetect, silencedetect, ebur128) + Claude visual review of contact sheets | Free |
| Data | YAML/JSON files in git (ideas, scripts, shot specs, asset index with licences, reuse ledger, performance log) | Free |
| Later, optional | Three.js preview page; Runway/Veo style pass; Cascadeur | Paid options |

## 9. Visual style options and recommendation

| Style | Modelling cost | Animation cost | Render time | Appeal / retention | Automation fit |
|---|---|---|---|---|---|
| Stylised low-poly | Low | Low (simple rigs, forgiving) | Very low | Good for comedy/scenario; can look cheap if flat-lit | Excellent |
| Realistic | Very high | Very high (uncanny valley, mocap needed) | High (Cycles) | High "is this real?" factor; unforgiving | Poor |
| Semi-real environments + stylised characters | Medium | Low–medium | Low–medium (EEVEE) | Very good: believable place, readable people. This is the dominant look in the niche | Very good |
| Cartoon simulation (toon shading) | Medium | Medium (needs acting) | Low | Great for zombie/story formats | Good |
| Cinematic educational (Kurzgesagt-3D / planet scale) | Medium-high | Low (few characters) | Medium | High for long-form, weaker as a scroll-stopper | Good |
| Minimalist 3D (clean shapes, few props) | Very low | Low | Very low | Lower on "real place" hooks; strong for science explainers | Excellent |

**Recommendation: "Living Diorama".** Semi-real, sun-drenched environments shot like a **miniature model world** (subtle tilt-shift depth of field, slightly saturated colour, crisp shadows) populated by **our own stylised characters**. These are chunky, rounded "bean-body" people with two-dot eyes, which avoids the blocky "box-head" look many accounts share. Why it fits:
- The miniature look hides low-poly simplicity (viewers read it as a deliberate toy-world), stays readable at phone size, and is cheap in EEVEE (depth of field + bloom + AO).
- The playbook's rule 2 (bright, busy, famous) is native to the look.
- The rounded character design is original, quick to rig once (one Rigify or Mixamo-compatible skeleton), and easy to vary by palette and shape keys.
- It extends to all four formats: diorama cutaways suit "How it's built", map/isometric views suit survival, and a planet-as-diorama suits long-form.

#### House style guide v1 (proposal)
- **Characters:** 1 base mesh, ~2–4k tris; 5 body-shape keys (tall/short/broad/kid/elder); 12 outfit palettes; dot eyes + optional brow decal for expressions (worried, shocked, happy) via swappable textures. No mouths by default (cheap, and it avoids lip-sync); a mouth decal only for close-ups. Shared skeleton so one animation library drives everyone.
- **Environments:** real-place silhouettes (not exact replicas): recognisable skyline cues, colours and landmarks via signage and generic shapes. Clean PBR materials with simplified textures (sand, concrete, water, glass, grass), all from CC0 libraries or procedural.
- **Palette:** daylight base of sky-blue, sea-teal, sand-warm, palm-green; a single **event colour** (signal magenta) reserved for the impossible thing (sound rings, the anomaly, the "change") so viewers learn: magenta = what changed. That recurring visual rule is part of the brand.
- **Lighting:** noon sun at 45–60°, soft shadows, light AO, a gentle bloom; never night as the main setting (playbook data). Golden hour only for the ending.
- **Camera:** every video opens with a low wide establishing shot of a famous place (the first frame must read as "a real place" in 0.5 s). Then aerial/diorama top-down, tracking shots at human height, and an orbit reveal for the finale. 24–35 mm for action, 85–135 mm "telephoto miniature" for scale gags. A light handheld noise layer on every camera.
- **Animation:** snappy and slightly exaggerated (squash/stretch on impacts), crowds desynchronised with per-instance offsets.
- **Text:** top-left HUD counter (small caps label + large tabular-figure number) in a distinctive monospace/grotesk pairing; centred lower-third captions, 2–4 words at a time, max 2 lines, safe-area aware (keep clear of the bottom ~20% and right ~15% where TikTok UI sits). Our own fonts, not the playbook's serif italic.
- **VFX:** stylised, readable (rings, cones, particles, debris chunks) rather than photoreal sims.
- **Audio identity:** a short original 3-note "anomaly" sting when the change happens; no stock music beds.

## 10. Proposed production architecture (smallest working system first)

The 10 modules the brief describes are the right *responsibilities*, but building them as 10 services would be over-engineering. I propose **one Python package + Blender scripts + a single JSON "shot spec" contract**, with Claude Code as the orchestrator and creative brain.

```
idea ─► [1 Concept]  ─► [2 Script+Storyboard] ─► shotspec.json ─┬─► [3 Scene build (Blender, per shot)] ─► [4 Render (EEVEE, per shot)] ─┐
          scoring          (Claude)                              │                                                                         ├─► [6 Assemble (FFmpeg)] ─► [7 QC] ─► [8 Approval]
                                                                 └─► [5 Audio: TTS + SFX + captions + overlays timeline] ─────────────────┘
                              ▲                                                                                                             │
                              └──────────────────────── [Asset library: kits, characters, anims, materials, sfx] ◄───── performance log ◄──┘
```

| Stage | Implementation | Run by | Testable alone? |
|---|---|---|---|
| Concept & scoring | Claude prompt + rubric (8 criteria, weights), ideas stored as YAML in `content/ideas/` | Claude Code | Yes, offline |
| Script & storyboard | Claude writes `script.md` + `shotspec.yaml`; a JSON-schema validator enforces fields, durations sum, ≥61 s | Claude Code + Python | Yes |
| Asset library | `.blend` kits (sets, characters, props), animation library (FBX/actions), material library, `assets.yaml` index with **licence field per asset** | Files + index | Yes |
| Scene build | `blender -b kit.blend -P build_shot.py -- shot.json`: environment scatter (Geometry Nodes, seeded), actors, effects, camera moves from a camera-move library, lighting preset | Blender (headless) | Yes: render a single still per shot |
| Render | Per-shot EEVEE PNG/EXR sequence, low-res preview mode (540×960, fewer samples) before final | Blender | Yes |
| Audio | TTS per narration line → word timestamps → SFX placement from cues → ambience → mix + loudness | Python + FFmpeg | Yes |
| Overlays | Captions (ASS) + counters/labels (ASS or a small overlay renderer) generated from the timeline | Python | Yes |
| Assembly | FFmpeg concat + overlay + mux → 1080×1920, 30 fps, H.264, AAC | Python + FFmpeg | Yes |
| QC | ffprobe checks, blackdetect/freezedetect/silencedetect, loudness, duration ≥ 61 s; contact sheet + Claude vision review against storyboard; originality check (script similarity vs own history, set/seed/camera reuse check) | Python + Claude | Yes |
| Approval & archive | `output/<video>/` with final MP4, preview, report, project files; nothing is posted automatically | Human | n/a |

**Why Blender is the engine and Three.js is not (for now):** Blender gives offline, deterministic, frame-accurate renders with real shadows/AO/DOF, a mature physics/animation/rig system, and a complete Python API. Three.js can render deterministically through a headless browser with a controlled clock, and it is a strong choice for *instant interactive previews*, but it would duplicate the asset pipeline. Possible later use: a web preview/approval page.

## 11. Example storyboard (original): "What if sound moved slower than you can run?"

**One-line test:** "What if sound suddenly moved slower than you can run, for 10 seconds, on Miami Beach?" The natural response is "wait, then what happens?", so it passes.
**Why it fits the rules:** one everyday thing (sound); a bright, busy, famous place (South Beach / Ocean Drive); a live counter (speed of sound, sonic booms); a strong comment hook ("you'd hear your own scream after you"); a sequel ("…what if light was this slow?"). Sound is invisible, so the visual signature becomes **visible sound rings**: translucent expanding shells that crawl slowly through the air. It's cheap to render, unusual, and easy to brand.
**Premise logic (for accuracy):** normal speed of sound in air ≈ 767 mph (343 m/s). In this world it drops to 7 mph (≈3.1 m/s), which is jogging pace. Consequences: speech arrives seconds late; anything faster than 7 mph (cars, bikes, jet skis, a sprinting kid, a thrown ball) outruns its own sound and drags a **sonic boom** (a shock cone, like a jet passing Mach 1). When the 10 seconds end, all the delayed sound still in flight is the payoff.
**Target length:** 72 s (above the 61 s Creator Rewards floor) at 30 fps = 2,160 frames, 1080×1920.
**Running element (ours):** an ice-cream truck whose jingle is always late. In this episode it arrives 40 seconds after the truck has left. It can recur across episodes, done differently each time.

| # | Time | Narration (VO) | Environment / characters / action | Camera | Lighting | On-screen text | SFX | Transition |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:00–0:03 | "What if sound moved slower than you can run?" | South Beach, packed. A lifeguard on a red tower blows a whistle; a visible ring leaves the whistle and *crawls*. | Low wide, slow push toward the tower | Bright noon, warm sun, soft shadows | Top-left: SPEED OF SOUND / **767 mph** | Normal beach ambience; the whistle is NOT heard | Hard cut on ring expansion |
| 2 | 0:03–0:06 | "At 12:00, it drops to 7 miles per hour." | Same place; counter rolls down 767→7. All rings everywhere freeze-slow. | Snap crash zoom-out to aerial | Same | Counter animates to **7 mph** | Audio "squeezes" down to a low hum (pitch-down sweep) | Match cut on counter |
| 3 | 0:06–0:09 | "A kid yells 'Mom!'" | Kid on the sand yells; a ring starts at his mouth. Mom 25 m away keeps reading. | Over-shoulder from mom toward kid | Same | "DELAY: 8 s" small tag near the ring | Silence where the yell should be | Cut |
| 4 | 0:09–0:12 | "She hears it eight seconds later. He's already in the water." | Ring reaches mom; she looks up. Kid is now splashing. | Medium on mom, rack focus to kid | Same | — | Yell "Mom!" arrives, late and Doppler-stretched | Whip pan right |
| 5 | 0:12–0:15 | "Anything faster than 7 miles per hour now breaks the sound barrier." | Ocean Drive: a car at 25 mph drags a cone-shaped shock wave; palms whip as it passes. | Tracking shot alongside the car | Same | SONIC BOOMS: **1** | Silence, then a CRACK as the cone hits camera | Cut on boom flash |
| 6 | 0:15–0:18 | "Every car on Ocean Drive." | Traffic: 8 cars, 8 cones; café umbrellas flip. | Elevated wide down the street | Same | SONIC BOOMS: 1 → **37** (rolling) | Staccato booms | Cut |
| 7 | 0:18–0:21 | "A cyclist." | Cyclist at 15 mph leaves a small cone; sunglasses fly off a pedestrian. | Low side-on dolly | Same | **58** | Smaller boom | Cut |
| 8 | 0:21–0:24 | "A jet ski." | Jet ski carves; a cone throws a curtain of spray. | Drone follow over water | Same, sparkly water | **112** | Water boom | Cut |
| 9 | 0:24–0:27 | "And this guy, who is just jogging a little too fast." | Jogger at 8 mph; a tiny cone; his hat lifts. Beat for comedy. | Front-on tracking, slight shake | Same | **113** "(jogger)" | Comedic tiny "pop" | Cut |
| 10 | 0:27–0:31 | "Meanwhile, nobody can hear a thing they're saying in real time." | Crowd shot: hundreds of people mouthing; rings everywhere overlapping. | Slow crane-up over the crowd | Same | TALKING, BUT LATE: **4,200 people** | Murmur building *behind* the image | Cut |
| 11 | 0:31–0:35 | "The ice-cream truck plays its song, then drives away." | Truck plays jingle (ring visible), pulls away at 10 mph *through its own ring*: a boom. | Wide, static, then pan to follow | Same | — | Boom, no jingle | Cut |
| 12 | 0:35–0:39 | "Out at sea, a cruise ship horn has been travelling toward the beach for 4 minutes." | Giant horn ring crawling across the ocean. | Telephoto from beach to ship | Slight haze | HORN ETA: **4 min** | Low rumble | Cut |
| 13 | 0:39–0:43 | "At 12:00 and 10 seconds, sound snaps back to normal." | Counter jumps 7→767. | Top-down aerial snap | Same | **767 mph** | Sudden full-volume beach ambience | Flash frame |
| 14 | 0:43–0:48 | "But everything already in the air arrives at once." | Every slow ring collapses inward simultaneously; windows rattle, umbrellas fly, gulls scatter. | Fast push-in, heavy shake | Brief white bloom | DELAYED SOUNDS: **1.8 million** | Huge layered impact (yells + horns + booms) | Cut |
| 15 | 0:48–0:54 | "The loudest moment in Miami's history lasts a fraction of a second." | Slow-motion aftermath: sand settling, sunglasses mid-air. | Slow orbit around the lifeguard tower | Golden, dust in the air | PEAK: **~150 dB** (labelled estimate) | Ringing tone, then silence | Cut |
| 16 | 0:54–0:59 | "The kid finally gets out of the water and says 'Mom, did you hear that?'" | Kid and mom; she stares, deadpan. | Two-shot | Normal | — | Normal speech, in sync | Cut |
| 17 | 0:59–1:05 | "And the cruise ship horn? Still four minutes away." | Back to the ship: its ring is still crawling, because it left during the slow window. | Telephoto again | Same | HORN ETA: **3:52** | Distant rumble | Cut |
| 18 | 1:05–1:12 | "Oh, and the ice-cream truck song shows up 40 seconds late. The truck is long gone." (running gag) | Empty street; jingle finally arrives; three kids turn and look around. | Static wide; slow push | Normal | Lower third: "Would you have outrun your own scream?" | Ice-cream jingle (original composition) | End card (loop-friendly cut back to frame 1) |

**Pacing check:** 18 shots in 72 s (avg 4 s/shot) with a new beat (counter tick, gag, boom) every 2–3 s inside longer shots.
**Accuracy notes:** the 150 dB peak and the "1.8 million" counter are dramatised estimates and must be labelled "est." on screen. The physics premise is impossible, so the video must not claim it is real science; the consequence logic follows real shock-wave behaviour.

## 12. How the storyboard becomes Blender scenes

#### 12.1 The contract: a shot-spec file (JSON/YAML)
Claude writes the storyboard as structured data, not prose. Every downstream module reads only this.

```yaml
video: slow_sound_miami
fps: 30
resolution: [1080, 1920]
style: house_style_v1         # palette, materials, text style
sets:
  south_beach: {kit: beach_kit, seed: 4412, crowd: 900, tower: lifeguard_red}
  ocean_drive: {kit: street_kit, seed: 77, cars: 8, palms: 24, umbrellas: 12}
shots:
  - id: s05
    set: ocean_drive
    duration: 3.0
    actors:
      - {id: car1, asset: car_sedan_03, path: street_lane_a, speed_mph: 25}
    effects:
      - {type: shock_cone, attach: car1, start: 0.2}
      - {type: palm_whip, trigger: car1.pass, radius_m: 6}
    camera: {move: track_alongside, target: car1, offset: [-4, 1.2, 1.0], lens_mm: 28}
    lighting: noon_warm
    text: [{slot: counter_tl, label: SONIC BOOMS, from: 0, to: 1}]
    sfx: [{id: boom_crack, at: 2.4}]
    narration: "Anything faster than 7 miles per hour now breaks the sound barrier."
```

#### 12.2 What each module does with it (Blender 4.x/5.x, Python `bpy`, run headless)
| Storyboard element | Blender implementation |
|---|---|
| `sets.*.kit` + `seed` | A **set kit** is a `.blend` library (terrain, road, building, palm and umbrella pieces) linked with `bpy.data.libraries.load`. A Geometry Nodes "scatter" modifier places palms/umbrellas/towels from the seed, so each video gets a new layout from the same kit (originality without rebuilding). |
| Crowd (900 people) | Low-poly character variants (body shape, palette swap via object colour attribute) instanced with Geometry Nodes on a "crowd area" mesh. A few baked animation cycles (idle/talk/point/look-up), with per-instance time offsets so the crowd never moves in unison. |
| Actors on paths | Bezier curve per lane; `Follow Path` constraint; keyframe `offset_factor` so linear velocity matches `speed_mph` (m/s = mph × 0.447, frames = distance / speed × fps). Wheels: driver on rotation = distance / radius. |
| Visible sound rings | Shader-only effect: an icosphere with a transparent Fresnel "ring" material, scale keyframed at the slowed speed (3.1 m/s), opacity fading with radius. Fully procedural, no simulation. |
| Shock cone | A cone mesh parented to the actor, with a noise-displaced transparent material; its angle comes from the Mach number (sin θ = 1/M). The boom is a separate expanding shell plus a camera-shake keyframe set. |
| Palm whip / umbrellas flipping | Not simulated: procedural keyframes (rotation spike + damped oscillation via a Noise/Cycles F-curve modifier) triggered at the frame when the cone passes. Rigid-body only for shot 14 debris, baked to cache before render. |
| Camera `track_alongside` | Camera parented to an Empty that follows the same path with an offset; `Track To` or `Damped Track` on the actor; lens 28 mm; subtle noise modifier for handheld feel. A camera library maps each shot type (`aerial_snap`, `crane_up`, `orbit_reveal`, `crash_zoom`, `telephoto_static`) to a parameterised function. |
| Lighting `noon_warm` | A saved preset: Sun lamp (angle, strength, colour) + Nishita/HDRI sky + EEVEE settings (shadows, AO, bloom). Presets live in `house_style_v1`. |
| Water / spray | Ocean modifier (animated `time`) for the sea; particle spray burst for the jet ski. No Mantaflow, which is too slow and fragile for daily output. |
| Text / counters | **Not** baked into the 3D render. Exported as a timeline (`overlays.json`) and composited afterwards so wording can change without re-rendering 3D. |
| Render | One `.blend` per set, one render job per shot (`blender -b set.blend -P build_shot.py -- --shot s05`), EEVEE, PNG or EXR sequence to `output/shots/s05/`. Failures are retried per shot, not per video. |
| Audio | Narration TTS per line, then word timestamps. SFX cues from `sfx[]` placed at absolute times. Ambience bed per set. Mixed and loudness-normalised. |
| Assembly | FFmpeg: concatenate shot sequences, burn in captions + counters (ASS subtitles or overlay PNG sequences), mux audio, export H.264 1080×1920 30 fps. |
| QC | ffprobe (resolution/fps/duration ≥ 61 s), black-frame and freeze-frame detection, loudness check, caption timing check, then a contact sheet of 1 frame/second that Claude inspects visually against the storyboard. |

#### 12.3 Minimal illustrative bpy (for understanding, not production code)
Keyframing a constraint property like this works in 5.x. Writing F-curves directly must use the 5.0+ channelbag API (see §5).
```python
import bpy, math, sys, json
args = sys.argv[sys.argv.index("--") + 1:]
shot = json.load(open(args[0]))
scn = bpy.context.scene
scn.render.engine = "BLENDER_EEVEE"        # 5.x id ("BLENDER_EEVEE_NEXT" in 4.2–4.5)
scn.render.resolution_x, scn.render.resolution_y = 1080, 1920
scn.render.fps = 30
scn.frame_start, scn.frame_end = 1, int(shot["duration"] * 30)

car = bpy.data.objects[shot["actors"][0]["asset"]]
path = bpy.data.objects[shot["actors"][0]["path"]]
fp = car.constraints.new("FOLLOW_PATH"); fp.target = path; fp.use_fixed_location = True
fp.offset_factor = 0.0; fp.keyframe_insert("offset_factor", frame=1)
dist = shot["actors"][0]["speed_mph"] * 0.447 * shot["duration"]
fp.offset_factor = min(1.0, dist / path.data.splines[0].calc_length())
fp.keyframe_insert("offset_factor", frame=scn.frame_end)

cam = bpy.data.objects["Camera"]
trk = cam.constraints.new("DAMPED_TRACK"); trk.target = car; trk.track_axis = "TRACK_NEGATIVE_Z"
scn.render.filepath = f"//renders/{shot['id']}/frame_"
bpy.ops.render.render(animation=True)
```

## 13. Hardware requirements

These are estimates; I'll measure on your machine in Stage B.

| Tier | Spec | What it can do |
|---|---|---|
| Minimum (may already be what you own) | Apple Silicon M1/M2/M3 with 16 GB unified memory, **or** Windows/Linux with an NVIDIA RTX 3060 12 GB / 4060 8 GB, 16–32 GB RAM, 500 GB free SSD | EEVEE shorts in roughly 1–4 h of render per video; one video per day is feasible |
| Recommended | NVIDIA RTX 4070 Super / 5070 (12–16 GB) or a used RTX 3090 (24 GB), 64 GB RAM, 2 TB NVMe; or Apple M4 Pro/Max | EEVEE short in under ~1 h; local TRELLIS.2 and Kokoro; occasional Cycles |
| Not needed | RTX 4090/5090, workstation cards, render farms | — |

- **The playbook's claim of "no graphics card"** is plausible on Apple Silicon, whose integrated GPU runs EEVEE via Metal, or with a WebGL renderer. It is not plausible for Cycles at volume.
- **Cloud fallback:** RTX 4090 instances on RunPod / Vast.ai are about $0.25–0.70/h (unverified), so a full Cycles render is about $2–4. SheepIt is a free community render farm, fine for overflow but not for deadlines.

## 14. Estimated startup and ongoing costs

These are estimates; prices change, so verify before purchase. Nothing will be bought without your approval.

| | **Free tier** | **Low-cost tier** | **Higher-quality tier** |
|---|---|---|---|
| One-time: hardware | $0 (existing machine) | $0–$350 (e.g. GPU upgrade, if needed) | ~$1,500–2,200 new PC, or an Apple M4 Pro/Max |
| One-time: assets | $0 (CC0) | $0–$50 (one paid add-on such as Auto-Rig Pro) | $100–300 (asset packs, add-ons) |
| Monthly: Claude | $20 (Pro; Claude Code needs a paid plan or API) | $20–100 | $100–200 (Max) + API for batch jobs |
| Monthly: 3D generation | $0 (TRELLIS.2 local) | $0–20 (Meshy or Tripo Pro) | $60–120 (Meshy Studio / Rodin) |
| Monthly: voice + SFX | $0 (Kokoro + Sonniss/CC0) | $5–6 (ElevenLabs Starter) | $22–99 (ElevenLabs Creator/Pro) |
| Monthly: other | $0 | $0 | $35–95 (Runway / Cascadeur Pro), optional |
| **Monthly total** | **≈$20** | **≈$45–55** | **≈$220–500** |
| **Marginal cost per video** | ≈$0.05–0.20 (electricity) | ≈$0.30–1.50 | ≈$3–15 |

Per-video costs assume ~30 videos/month and a 70 s narration of ~1,000 characters. The playbook claims ~1% of a Claude Max week per short, which suggests a $20 plan supports a meaningful but limited number of builds per week. I'll measure actual usage in Stage D.

**My recommendation:** start on the **free tier** (plus your Claude plan). Upgrade a component only when a specific quality gap is shown in a test render or test audio.

## 15. Development roadmap with completion criteria

| Stage | Goal | Done when (measurable) |
|---|---|---|
| A. Research (this document) | Understand niche, tools, policy | You approve the architecture, style and first video concept |
| B. Foundation | Blender 5.2 LTS, Python, FFmpeg, TTS, Whisper installed on your machine; repo scaffold | `make doctor` passes: Blender runs headless, renders a test cube to PNG, FFmpeg encodes 1080×1920, TTS produces a WAV |
| C. First 3D prototype | One beach set, 50 characters, one camera move, house lighting | A 10-second 1080×1920 clip renders headlessly in under ~15 min on your machine; you approve the look |
| D. First complete video | "Slow sound" (or another approved idea) built semi-manually through the pipeline | A 61–80 s MP4 passes all QC checks and you approve it. Render + build time recorded |
| E. Automation | Idea → MP4 with one command, human approval gates at concept, storyboard and final | 3 different videos produced end-to-end with ≤30 min of human time each, all passing QC |
| F. All formats | Kits for survival (hero character + map views), build (cutaway stages), long-form (chaptering) | One passing video per format; one 5-min long-form |
| G. Continuous improvement | Performance log (manual export of platform analytics), comment mining → idea backlog | Weekly report: views/hour at 24 h, like rate, completion where available; idea scores recalibrated against actual results |

## 16. Risks and limitations
- **Content risk > tech risk:** the playbook's own data says the premise decides results. The pipeline must make it cheap to test many ideas, not perfect one.
- **Originality flags:** a templated pipeline naturally produces sameness. Enforce per-video uniqueness (new set seed, new opening composition, new camera path, new script, new sound design) and keep a reuse ledger.
- **Character animation quality** is the hardest visual problem (contacts, hand-object interaction). Mitigate with the stylised design, avoiding close hand interactions, and the animation library.
- **Physics sims** (water, destruction) are slow and non-deterministic. Prefer procedural/keyframed fakes and bake any sim.
- **Licensing drift:** asset/tool licences change. Keep a licence field on every asset and avoid "free for personal use" sources.
- **Platform policy drift:** monetisation rules (TikTok 1-minute rule, YouTube inauthentic content, Meta unoriginal content) change often. Re-check before launch.
- **Accuracy:** what-if science must be plausible. Add a fact-check step and label estimates.
- **Hardware:** without a decent GPU, EEVEE renders slow down. Measure on your machine in Stage B before promising throughput.
- **Real places:** use real place names and generic recreations; avoid trademarked logos, real businesses' signage and real people.
- **Revenue uncertainty:** creator-fund income is volatile and audience-dependent (see the playbook's $4.43 at 1.4M views).
- **This environment:** this cloud session is a temporary container (no GPU, and files are lost unless committed). Production should run on your own computer, with the project in its own git repository.

#### Platform policy check (summary of Appendix D)
| Rule | TikTok | YouTube | Instagram / Facebook |
|---|---|---|---|
| Monetisation entry | Creator Rewards: 18+, 10K followers, 100K views in 30 days, personal account, listed countries (incl. US). Videos must be **over 1 minute** with 1,000+ qualified views | YPP: 1K subs + 4K watch hours (12 mo) **or** 10M Shorts views (90 days). From 2027-02-01: 8K hours / 20M Shorts views for new applicants | Facebook Content Monetization is invite-only (Mar 2026) |
| Originality | Rewards are weighted by originality; 5+ ineligible videos in 30 days means the account *may* be removed from Creator Rewards (the playbook's "5 flags" claim is broadly confirmed, but not automatic) | "Inauthentic content" (renamed Jul 2025) explicitly targets mass-produced, templated and "AI content made with generic or unoriginal templates". This is **the main structural risk for any automated pipeline** | Jul 2025 crackdown: reposters lose monetisation and distribution; duplicates down-ranked |
| AI disclosure | Required for *realistic* AI content; auto-labels via C2PA | Required only for realistic altered content; fully animated / clearly unrealistic content exempt; no reach penalty | Required for photorealistic video / realistic audio |
| Music | Commercial Music Library for commercial use | A claimed track cuts Shorts revenue share; a Short over 1 min with a Content ID claim is blocked | Licensed audio rules vary |
| Accounts | Multiple accounts OK if not deceptive; impersonation banned | Linked-account and ban-evasion rules | 20M+ impersonating accounts removed in 2025 |

**The playbook's seven mistakes against official policy:**
1. Same video twice: partially supported.
2. Copied script: confirmed in principle.
3. Same set, opening and ending: partially supported (templating, not branding, is the problem).
4. Popular free music: partially supported (mainly a YouTube Content ID and revenue issue).
5. Under 61 s earns nothing: confirmed for TikTok Creator Rewards only.
6. Look-alike accounts: confirmed.
7. Deleting during an appeal: partially supported (deleted videos are never paid; "loses the appeal" is anecdotal).

**Legal basics:**
- CC0 assets need no credit; CC-BY needs credit in the description. Avoid NC/ND licences.
- Mixamo output is royalty-free for commercial video.
- Purely AI-generated material is not copyrightable in the US without human authorship (USCO Part 2, Jan 2025). Our human-directed Blender scenes are on firmer ground.
- Real buildings visible from public places may be depicted (17 USC §120(a)). Avoid logos and signage that are trademarks (e.g. the Santa Monica Pier sign, the Hollywood Sign) in branding, thumbnails and merchandise.

## 17. Recommended overall implementation strategy

1. **Idea first, studio second.** Build a lightweight idea engine (rubric scoring + one-line test) at the same time as the render pipeline. Pre-test titles with you before anything is built.
2. **Start with one format and one set.** The first set is **Format 1, what-if** on a **Miami-style beach kit**, because the playbook data, the creator evidence and the automation fit all point to it. The second is "How it's built" (a deterministic cutaway pipeline). Zombie (needs a hero-character pipeline) and long-form come after.
3. **Blender headless + a structured shot-spec** is the backbone. Claude writes specs and code; a fixed library of set kits, camera moves, effects and text styles does the heavy lifting. Every video still gets a new seed, location variant, opening composition, camera paths, script and sound design.
4. **Own the look early:** the "Living Diorama" style (§9) with our own bean-body characters and the magenta "anomaly" colour rule. Approve it on a 10-second prototype before investing in kits.
5. **Visual QC loop:** render previews, have Claude inspect contact sheets against the storyboard, fix, then render the final. No video reaches you without passing automated checks.
6. **Compliance by design:**
   - 61–80 s from the first draft.
   - No re-uploads, no music beds, and a licence log per asset.
   - A reuse ledger and script-similarity check against our own history.
   - A distinct identity per account, and AI disclosure where required.
   - Human approval before every post; nothing is ever deleted automatically.
7. **Measure honestly:** track views/hour at 24 h, like rate and completion (where the platform shows it), and feed comments into the idea backlog. Don't judge a video before 24 h.

**Decisions I need from you before Stage B:**
1. **Your computer:** OS, CPU, GPU model and VRAM, RAM and free disk space. This decides render settings and whether any upgrade is needed at all.
2. **Where the project lives:** this cloud session is attached to your unrelated `tcg-drop-alerts` repository, and its container has no GPU. I recommend a new private repository `faceless-3d-studio`, with production running on your own computer through Claude Code.
3. **Budget tier** to start: my recommendation is Free (+ your Claude plan).
4. **Approval of:**
   - the "Living Diorama" visual direction;
   - the architecture in §10;
   - "What if sound moved slower than you can run?" (or another idea) as the first full video.
5. **Primary audience and platform:** the playbook suggests US / TikTok first; YouTube Shorts and long-form follow.
