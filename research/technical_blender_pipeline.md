# Automated 3D Animation Pipeline (Claude Code + headless Blender): Technical Research

Date: 2026-11-02. Researcher role: technical director.

## How to read this report

- **VERIFIED (URL)** means a web search result from that URL backed the claim. In this session WebFetch could not reach `blender.org`, `developer.blender.org` or `phoronix.com` (DNS blocked). So "verified" means confirmed from search-result excerpts of the cited page, not from reading the full page. Check the critical items against the live page before you commit.
- **INFERENCE** means my own engineering judgement or knowledge from before mid-2026 that I could not re-check this session. That includes all the estimates.
- The shared web-search budget ran out partway through. Section 10 (hardware and cloud prices) and a few smaller items therefore rest mostly on INFERENCE and are flagged. Re-verify prices before you spend money.

---

## 1. Blender versions, recent features, license

### Version landscape (Nov 2026)
- **VERIFIED** Blender **5.0** shipped on 18 Nov 2025. It added HDR/wide-gamut display and export, ACES/ACEScg working color spaces, a large VSE refresh, new compositor nodes, and better Vulkan support. Files saved in 5.0 may not open properly in 4.x. https://osarch.org/2025/11/18/blender-5-0-released/ , https://www.phoronix.com/news/Blender-5.0-Released
- **VERIFIED** Blender **5.1** shipped in March 2026. It focused on speed: faster animation playback and shape keys, about 5–10% faster Cycles GPU, faster EEVEE shader compilation and lower EEVEE VRAM use. New nodes include Bone Info and Raycast. https://www.blendernation.com/blender-5-1-released , https://osarch.org/2026/03/17/blender-5-1-released/
- **VERIFIED** Blender **5.2 LTS** shipped on 14 Jul 2026 and is supported until July 2028. **This is the version to pin the pipeline to.** https://www.blender.org/releases/5-2/ , https://www.blender.org/press/blender-5-2-lts-release/
  - Experimental node-based physics (XPBD solver node for hair and cloth), a Mesh Bevel node, Get/Set Geometry Bundle nodes, and a Sound socket for audio-reactive node trees. https://www.cgchannel.com/2026/07/blender-5-2-lts-is-here-discover-its-5-key-features/ , https://digitalproduction.com/2026/07/21/blender-5-2-lts-lands-with-node-physics/
  - EEVEE gets a Screen Space Raytracing overhaul. One outlet reports about 2x speed-up in instance-heavy scenes; treat that as a best case. Principled BSDF gains a "Thin Wall" option. Cycles gains a texture cache, with "up to 80%" memory savings claimed by one outlet as a best case. https://www.heise.de/en/news/Blender-5-2-LTS-New-Simulations-and-Eevee-Improvements-11366897.html
  - The Python API for Geometry Nodes modifier properties changed, so check scripts that set GN modifier inputs. (heise, same URL)
- **VERIFIED (secondary only)** Blender **5.3** was in alpha until about 30 Sep 2026, with release targeted for about 17 Nov 2026. https://www.strayspark.studio/blog/blender-5-3-texture-layers-baking-game-developers , https://80.lv/articles/blender-in-2026-planned-features-projects
- **INFERENCE** Blender 4.5 LTS (Jul 2025) should still be in support until about Jul 2027. 4.2 LTS reached end of life in Jul 2026.

### Features that matter for this pipeline
- **EEVEE Next.** VERIFIED: in 4.2 LTS (16 Jul 2024) EEVEE was rewritten. It brought screen-space ray-traced GI, virtual shadow maps, no hard light cap (4096 visible), velocity-aware temporal AA, and better motion blur. https://www.blendernation.com/2024/07/16/blender-4-2-lts-released-check-out-these-standout-features/ , https://cgchannel.com/2024/07/5-key-features-in-blender-4-2
  - INFERENCE: since 4.2 the engine id is still `BLENDER_EEVEE_NEXT` in 4.2–4.x. It was renamed back to `BLENDER_EEVEE` in 5.0. Check with `bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items.keys()`.
- **Geometry Nodes bundles and closures.** VERIFIED: added in 5.0. Bundles act like structs (Combine/Separate/Join Bundle) and closures inject node logic, evaluated with Evaluate Closure. Both are available in shader nodes and no longer experimental. https://developer.blender.org/docs/release_notes/5.0/geometry_nodes/ , https://code.blender.org/2025/10/geometry-nodes-workshop-september-2025/
  - VERIFIED (aggregator): 5.2 allows recursive closures and bundles attached to geometry. https://releasebot.io/updates/blender
  - Relevance: you can build reusable "procedural kits" (a building generator that takes a closure for facade style) that an agent sets up by changing only inputs.
- **Grease Pencil v3.** VERIFIED: rewritten in 4.3. Old GP Python API add-ons break. Strokes now live at `frame.drawing.strokes`; operators moved `bpy.ops.gpencil.*` → `bpy.ops.grease_pencil.*`; GP modifiers moved into `object.modifiers`; GN works with GP. https://developer.blender.org/docs/release_notes/4.3/grease_pencil_migration/ , https://www.cgchannel.com/2024/10/blender-4-3-lets-you-control-grease-pencil-with-geometry-nodes
  - INFERENCE: most LLM training data still shows the GPv2 API, so the agent will write broken GP code unless you pin it to the 4.3+ docs.
- **Vulkan.** VERIFIED: 5.0 kept OpenGL as default. Vulkan by default was planned for 5.1. One secondary source says the 5.3 notes make Vulkan default on Windows/Linux (not ARM), and that dropping OpenGL in 6.0 is being discussed. https://www.phoronix.com/news/Blender-5.0-Vulkan-OpenGL-RAM , https://www.phoronix.com/news/Blender-5.1-Vulkan-Default , https://hwbusters.com/?p=118866
  - INFERENCE: for headless renders, pin the GPU backend explicitly (`--gpu-backend opengl|vulkan`) and test both. Vulkan cannot spill VRAM to system RAM the way OpenGL drivers can (Phoronix above), so big EEVEE scenes may fail on 8 GB cards under Vulkan.
- **Animation data model (slotted actions).** VERIFIED: 4.4 introduced layered/slotted actions with channelbags. 5.0 **removed `Action.fcurves`, `Action.groups` and `Action.id_root`**. Use `bpy_extras.anim_utils.action_ensure_channelbag_for_slot(action, slot)` then `channelbag.fcurves.ensure()/new()/find()`. https://docs.blender.org/api/5.0/change_log.html , https://docs.blender.org/api/5.0/bpy.types.ActionChannelbagFCurves.html , https://app.cinevva.com/es/guides/blender-5-for-game-artists
  - **This is the single most common way an LLM will break on 5.x.** Older tutorials do `obj.animation_data.action.fcurves`. Put this in the agent's CLAUDE.md.
- **Output "Media Type".** VERIFIED: 5.0 added `ImageFormatSettings.media_type` with values `IMAGE`, `MULTI_LAYER_IMAGE` or `VIDEO`. Video encoding (container and codec) only shows when it is `VIDEO`. https://docs.blender.org/api/5.0/bpy.types.ImageFormatSettings.html , https://docs.blender.org/manual/en/5.0/render/output/properties/output.html

### License and output ownership
- **VERIFIED** Blender is GPL-2.0-or-later and free to use "for any purpose", including commercial animation. Cycles is Apache 2.0. https://www.blender.org/?p=658 (Blender is Free Software), https://www.blender.org/support/faq/
- **VERIFIED** Output (renders, .blend content you make) belongs to the artist, and the GPL does not cover it. https://archive.blender.org/lists/bf-committers/2004-November/008253.html (old but long-standing FAQ position), https://en.wikibooks.org/wiki/Blender_3D:_Noob_to_Pro/Using_proper_copyright_RE:Blender
- **VERIFIED** Python scripts and add-ons that use the bpy API are treated as GPL if you *distribute* them. Internal use inside one company does not require publishing them. https://www.blender.org/support/faq/
- **INFERENCE** Your pipeline scripts are fine to keep private as long as you don't distribute them. Assets bundled with Blender (e.g. some Essentials asset library content) have their own terms; check before shipping them inside renders.

---

## 2. Headless automation

### CLI pattern
- **VERIFIED** `blender -b file.blend -P script.py -- arg1 arg2`. `-b` means background (no UI). `--` stops Blender's argument parsing, and the script reads its own arguments with `sys.argv[sys.argv.index('--')+1:]`. Arguments run **in order**, so set `-o`, `-s`/`-e`, `-F` before `-f`/`-a`. https://docs.blender.org/manual/en/2.80/advanced/command_line/arguments.html , https://archive.blender.org/wiki/2015/index.php/Reference/CL , https://salaivv.notion.site/Blender-Python-Cheatsheet-9cfb88dbc4a34d829d4305982053a05e
- **VERIFIED** `--cycles-device CPU|CUDA|OPTIX|HIP|ONEAPI|METAL` with optional `+CPU` for hybrid rendering. https://docs.blender.org/manual/en/latest/render/cycles/gpu_rendering.html
- **INFERENCE (standard practice)**:
  - Use `--factory-startup` so user prefs and add-ons don't make runs non-reproducible. Use `--python-exit-code 1` so a Python exception gives a non-zero exit code the agent can detect. Use `--log-level` / `-noaudio` as needed.
  - Split jobs into **build** (script → `.blend` saved with `bpy.ops.wm.save_as_mainfile`), **bake** (sims → disk cache) and **render** (`blender -b scene.blend -a`). Each stage is then cacheable and restartable, and the agent can inspect the `.blend`.

### bpy building blocks (INFERENCE, API stable since 2.8 except where noted)
- Objects: `bpy.data.meshes.new` + `bpy.data.objects.new` + `collection.objects.link` (preferred over `bpy.ops` in background mode, because ops depend on context). Primitives: `bpy.ops.mesh.primitive_*_add` work headless.
- Materials: `mat = bpy.data.materials.new(name); mat.use_nodes = True` (INFERENCE: `use_nodes` may be on by default / deprecated in 5.x), then edit `mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value`.
- Lights and cameras: `bpy.data.lights.new(name, type='AREA'|'SUN'|'POINT'|'SPOT')`, `bpy.data.cameras.new`, `scene.camera = cam_obj`.
- Keyframes: `obj.location = (...); obj.keyframe_insert('location', frame=f)`. This high-level call still works on 5.x and creates the slotted action automatically. For direct F-curve editing use the channelbag API (section 1). Set interpolation through `kp.interpolation = 'BEZIER'|'LINEAR'|'CONSTANT'` and easing with `kp.easing`.
- F-curve modifiers: `fc.modifiers.new('NOISE')` with `.strength`, `.scale`, `.phase` for procedural shake and wobble; `'CYCLES'` for loops.
- Drivers: `fc = obj.driver_add('rotation_euler', 2); fc.driver.expression = 'frame/10'`. Simple expressions run without "Auto Run Python Scripts". INFERENCE: complex Python expressions need `--enable-autoexec` in headless runs.
- Render: `scene.frame_start/frame_end/frame_step`, `scene.render.fps`, `resolution_x=1080, resolution_y=1920, resolution_percentage`, `scene.render.filepath='//out/frame_####'`, then `bpy.ops.render.render(animation=True)` (or `-a` on the CLI).
- Output format:
  - **Recommended: PNG (or EXR) sequence**, then FFmpeg assembly. A crash only loses one frame. `render.use_overwrite=False` + `render.use_placeholder=True` lets you resume and run several machines on one frame range. The colour pipeline stays clean.
  - Direct video on 5.x: `image_settings.media_type='VIDEO'` (VERIFIED field), `file_format='FFMPEG'`, `scene.render.ffmpeg.format='MPEG4'`, `codec='H264'`. Use it only for quick previews.
- Validation: the agent should render one still (`-f N`) at 25–50% resolution and look at it (Claude can read PNGs) before launching a full animation run.

### EEVEE headless: needs a GPU, and the display question is OS-specific
- **VERIFIED (historical)**: in 2.8x EEVEE needed an OpenGL context. Blender devs said "there must always be a display even for background rendering". Workarounds were Xvfb (very slow, software GL) or a headless Xorg on NVIDIA. Cycles CUDA/OptiX never needed X. https://devtalk.blender.org/t/blender-2-8-unable-to-open-a-display-by-the-rendering-on-the-background-eevee/1436 , https://developer.blender.org/T61164 , https://gist.github.com/UuuNyaa/f57aa37fc6ed2fbd5c166513a16a40e5
- **VERIFIED (single-source, current)**: a 2026 project reports Blender 5.2 running `blender -b` with EEVEE rendering through **EGL with no DISPLAY/WAYLAND_DISPLAY** on Linux. https://github.com/miyabi-sunny-side/blender-live
- **Conflicting (vendor)**: a 2026 render-farm vendor article claims EEVEE Next still needs a display context, and that headless SaaS boxes crash or render black. https://irendering.net/eevee-next-headless-dilemma-cloud-render-farm-guide/
- **INFERENCE / recommendation**:
  - **Linux + NVIDIA**: current Linux builds create an EGL context when no display is present, so EEVEE works headless on a real GPU with the proprietary driver. Run a 1-frame smoke test on any new box or cloud image. Fallback: `Xvfb` + VirtualGL, or a headless Xorg with the NVIDIA driver.
  - **macOS (Apple Silicon)**: EEVEE uses Metal and `blender -b` works from Terminal/SSH. Stay logged in to a GUI session and disable sleep; launchd jobs without a user session are less reliable.
  - **Windows**: works from a normal user session. Avoid Windows Services and Session 0, which may not have GPU access.
  - **CPU-only**: EEVEE needs a GPU. Software rasterization (Mesa llvmpipe) is technically possible but impractically slow and flaky. CPU-only boxes should use **Cycles CPU**.

### Cycles devices
- **VERIFIED** CUDA and OptiX (NVIDIA; OptiX needs compute capability ≥5.0 and driver ≥535), HIP (AMD RDNA1+), oneAPI (Intel Arc A/B), Metal (Apple Silicon, macOS 13+). No CUDA toolkit install is needed because kernels ship precompiled. https://docs.blender.org/manual/en/latest/render/cycles/gpu_rendering.html
- **INFERENCE**: in headless runs, set devices in the script, because `--factory-startup` resets prefs: `prefs = bpy.context.preferences.addons['cycles'].preferences; prefs.compute_device_type='OPTIX'; prefs.get_devices(); [setattr(d,'use',True) for d in prefs.devices]; scene.cycles.device='GPU'`.

### `bpy` as a pip module
- **VERIFIED** `pip install bpy` gives "Blender as a Python module". 5.0.0 wheels target CPython 3.11; 5.1.x wheels target CPython 3.13. Wheels exist for Win x64/ARM64, manylinux x86-64 and macOS ARM64. Only the current LTS window stays on PyPI; older ones are on download.blender.org. https://pypi.org/project/bpy/ , https://pypi.org/project/bpy/5.0.0/
- **VERIFIED** `fake-bpy-module-5-x` provides type stubs only, useful for IDE and agent autocomplete. https://pypi.org/project/fake-bpy-module-5-1/
- **INFERENCE**: `bpy` in-process is handy for asset inspection and tests. For renders, prefer the `blender` binary in a subprocess: it isolates crashes, supports per-job timeouts, gives an exact version pin and is easier to parallelize. You must match the Python version exactly.

### MCP servers
- **VERIFIED** The community **blender-mcp by ahujasid**, renamed **"MCP for Blender" / `mcp-for-blender`** in Sep 2026, is MIT licensed with about 32.7k stars as of 30 Oct 2026. It works through a Blender add-on that opens a localhost socket plus an MCP server, and integrates Poly Haven and Hyper3D Rodin. Blender must be running (GUI) or tool calls fail. Its tool definitions use about 6.5k tokens of context. It is not affiliated with the Blender Foundation. https://aiwiki.ai/wiki/blender_mcp , https://github.com/ahujasid/blender-mcp/releases , https://ai-heartland.com/tool/blender-mcp-guide/
- **VERIFIED (secondary)** The **official Blender Lab MCP server** lives at projects.blender.org/lab/blender_mcp. It needs Blender ≥5.1, reached v1.0.3 on 11 Sep 2026, and is aimed at analysis, debugging and scripting rather than generative art. https://www.strayspark.studio/blog/official-blender-mcp-server-comparison-2026
- **INFERENCE: usefulness for this pipeline.**
  - MCP is good for **interactive look-dev**: the agent pokes a live scene, takes viewport screenshots and iterates on lighting and layout with a human watching.
  - It is a poor fit for **batch production**. It needs a running GUI Blender, the state is opaque and lives in memory, and it is hard to reproduce, version or parallelize.
  - The robust pattern is that **Claude Code writes `.py` scene scripts into git and runs `blender -b` directly via Bash**. Every shot is then a reproducible script, diffs are reviewable, and failures show up as exit codes and logs.
  - Use MCP (preferably the official one, on 5.2) only as an optional "live preview" side channel.

---

## 3. Render performance

### Relative GPU throughput (Blender Open Data–derived, Cycles)
| Device | Score | Source |
|---|---|---|
| RTX 4090 | ~10,880 | VERIFIED via https://wccftech.com/apple-m4-max-chip-belender-benchmarks-against-rtx-4090/amp/ |
| RTX 4070 | ~5,399 | VERIFIED (Renderjuice, derived from Open Data medians) https://www.renderjuice.com/gpus/compare/rtx-3060-vs-rtx-4070-ti |
| Apple M4 Max (40-core GPU) | ~5,208 (≈ RTX 4070, just under 4080 Laptop) | VERIFIED https://9to5mac.com/2024/11/17/m4-max-blender-benchmark/ |
| RTX 4060 Ti | ~3,833 | VERIFIED (Renderjuice) https://www.development.renderjuice.com/gpus/rtx-4060-ti-for-blender |
| RTX 4060 | ~3,133 | VERIFIED (Renderjuice) https://www.development.renderjuice.com/gpus/compare/rtx-4060-vs-rtx-4060-ti |
| RTX 3060 (12 GB) | ~2,302 | VERIFIED (Renderjuice) https://www.renderjuice.com/gpus/compare/rtx-3060-vs-rtx-4070-ti |
| Apple M4 Pro / M3 Pro | not found | INFERENCE: roughly 1,500–2,500 (≈3060 class) |
| High-end desktop CPU (16-core Ryzen 9 / Core i9) | not found | INFERENCE: roughly 400–700, i.e. 5–10x slower than an RTX 4070 |

Scores are proportional to Cycles throughput. An RTX 4070 is about 2.3x an RTX 3060.

### Denoising
- **VERIFIED** Blender 4.1+ runs **OpenImageDenoise on the GPU** (NVIDIA GTX16xx/RTX, Intel Xe-HPG, Apple Silicon macOS 13+; AMD RDNA2/3 from 4.2). Benchmark: about 0.07–0.08 s per frame on Arc A770 or RTX 3090, against 1.2 s on an i9-13900K CPU. OptiX denoiser is NVIDIA-only; OIDN works on any vendor. https://wiki.blender.org/release_notes/4.1/cycles/ , https://www.cgchannel.com/2024/03/5-key-features-in-blender-4-1/
- **INFERENCE**: for animation, low-sample renders with a per-frame denoiser can "boil" (temporal flicker). Mitigations: higher samples (128–256) with an adaptive threshold of about 0.01–0.02, OIDN "Accurate" prefilter with albedo and normal passes, avoiding tiny noisy light sources, or rendering in EEVEE. Searches found no authoritative flicker data.

### Per-frame time evidence
- **VERIFIED (weak)**: one SEO-style blog says a 250-frame 1080p Cycles animation at 128 samples took about 68 min on an RTX 4060, i.e. **about 16 s/frame**. Scene unknown. https://evezone.evetech.co.za/performance-pulse/rtx-5060-blender-performance-benchmark-real-world-test-2026
- **VERIFIED (anecdotal)**: one shot took 1:26 in Cycles against 0:06 in EEVEE (about 14x). A character scene took 20 min in Cycles against 18 s in EEVEE. https://blenderartists.org/t/cycles-vs-eevee-next-comparison/1540799 , https://dev.to/irender_gpu_render_farm/which-renderer-should-we-choose-cycles-or-eevee-10o9
- **VERIFIED**: EEVEE time varies widely with subdivision levels, and shader compilation adds a startup cost on the first frames. Blender Studio's EEVEE production short showed minutes per frame on heavy scenes. https://studio.blender.org/blog/rendering-snow-parkour-animation-with-eevee

### Estimates for a 70 s @ 30 fps short (2,100 frames, 1080×1920)
1080×1920 is the same 2.07 MP pixel count as 1920×1080. All rows below are **INFERENCE** for a "stylized/semi-real short-form" scene: moderate geometry, a few lights, some instancing, no volumetrics or heavy subsurface. Real times can be 3–5x higher with volumetrics, glass, heavy hair or 4K textures.

| Hardware | EEVEE (64 TAA samples, raytracing on) | Cycles (128 spp adaptive + OIDN GPU) | 2,100 frames, EEVEE | 2,100 frames, Cycles |
|---|---|---|---|---|
| RTX 4070 / 4070 Super (12 GB) | 1–4 s | 8–30 s | **35 min – 2.5 h** | **5 – 18 h** |
| RTX 4060 / 4060 Ti (8–16 GB) | 1.5–5 s | 12–45 s | 50 min – 3 h | 7 – 26 h |
| RTX 3060 12 GB | 2–6 s | 18–60 s | 1.2 – 3.5 h | 10 – 35 h |
| Apple M4 Max | 1.5–5 s | 9–35 s | 50 min – 3 h | 5 – 20 h |
| Apple M-Pro class | 3–10 s | 20–80 s | 1.8 – 6 h | 12 – 47 h |
| CPU-only (16-core desktop) | n/a (needs a GPU) | 1.5–5 min | n/a | **2 – 7 days** |

Add per-frame overhead in background mode: scene sync, BVH build and shader compile, about 0.5–3 s/frame. Persistent Data (`scene.render.use_persistent_data=True`) cuts this for Cycles.

**INFERENCE: practical levers.**
- EEVEE as the default engine.
- Render previews at 50% resolution and 15 fps.
- Use held frames or stepped animation (`frame_step=2`, then duplicate in FFmpeg) for stylized looks.
- Shots with static backgrounds: render the background once and composite the moving layers.
- Split the frame range across machines with placeholders.

---

## 4. Environments

### Geometry Nodes (built in)
- **INFERENCE (well-established)**: GN covers scattering (Distribute Points on Faces + Instance on Points), terrain (Grid + noise textures + Set Position), procedural cities (grids → building footprints → extruded and instanced modules), roads along curves, and simulation zones (3.6+). With 5.x bundles and closures you can package these as reusable node-group assets that the agent drives only through modifier inputs.
  - Gotcha: the 5.2 Python API for GN modifier inputs changed (VERIFIED, heise above). The agent must look up inputs by identifier. INFERENCE: older code does `mod["Input_2"] = ...`; newer access goes through the modifier's interface items.
- **VERIFIED** The 5.2 Sound socket enables audio-reactive geometry: lights or buildings pulsing to the music track. https://www.cgchannel.com/2026/07/blender-5-2-lts-is-here-discover-its-5-key-features/

### Add-ons and tools
| Tool | Status | Label |
|---|---|---|
| **BagaPie** (scatter, booleans, ivy, stairs/railings) | Free, on extensions.blender.org, 4.2+. v11.0.10 fixes a 5.1 issue. The paid BagaPie Assets library is a separate product ($39/$93). | VERIFIED https://extensions.blender.org/add-ons/bagapie/versions/ , https://www.cgchannel.com/2025/05/get-free-blender-modeling-and-scattering-add-on-bagapie-11/ |
| **Buildify** (GN building generator, works with OSM) | Free/pay-what-you-want; coverage dates from 2022 (Blender 3.2). 5.x compatibility unverified. | VERIFIED (dated) https://www.cgchannel.com/2022/07/download-free-blender-3d-building-generator-buildify/ |
| **SceneCity** (road and city generator) | Paid (~$39, seen discounted to $19.50), royalty-free commercial license. Last widely reported version is 1.9 (~2021). 5.x compatibility unverified. | VERIFIED (dated) https://couturier-arnaud.gumroad.com/l/scenecity/v2_0_1s2x55q |
| **A.N.T. Landscape** (noise terrain + erosion) | GPL. Bundled up to 4.1; INFERENCE: moved to extensions.blender.org from 4.2 like other legacy bundled add-ons. | VERIFIED (manual) https://www.blender.org/manual/en/addons/add_mesh/ant_landscape.html |
| **Cell Fracture** | Extension v0.2.1, 4.2+, GPL-3. Some reviews report incomplete splits and 4.3 interior-material bugs. | VERIFIED https://extensions.blender.org/add-ons/cell-fracture/ |
| **Sverchok** | Not verified this session. INFERENCE: free GPL node-based parametric add-on, actively maintained on GitHub. Mostly overlaps GN; skip it unless you need its CAD-style nodes. | INFERENCE |
| **Ocean modifier** | Built in (Physics modifiers). FFT ocean with foam and spray maps, animatable by `time`; fully procedural, so it is deterministic and needs no bake. | VERIFIED (exists) https://docs.blender.org/manual/en/4.0/modeling/modifiers/physics/index.html ; behaviour INFERENCE |
| **Dynamic Paint** | Built in. Waves and ripples on surfaces (e.g. object entering water). Needs a cache bake. | INFERENCE |
| **Blender OSM / BLOSM** | INFERENCE: real-world city footprints from OpenStreetMap. Free and paid tiers; the data is under the ODbL. | INFERENCE |

**INFERENCE recommendation**: favour **plain GN node-group assets you own** (committed .blend asset libraries) over third-party add-ons. Add-ons break across Blender versions, and many register UI and operators that behave badly under `--factory-startup` / background mode. Use BagaPie only if needed; it is free and current.

### Free asset libraries
| Library | License | Label |
|---|---|---|
| **Poly Haven** (HDRIs, PBR textures, models) | CC0: no attribution, commercial OK. Has an API; used by blender-mcp. | VERIFIED (secondary) https://app.cinevva.com/guides/game-assets-guide |
| **ambientCG** (materials, HDRIs) | CC0. API needs no key. 1,700–2,000+ materials. | VERIFIED (secondary) same URL |
| **Kenney** (low-poly kits, 270+ packs, GLB) | CC0, one consistent art style | VERIFIED (secondary) same URL |
| **Quaternius** (stylized low-poly, ~79 packs, GLTF/FBX; many rigged and animated) | CC0 | VERIFIED (secondary) same URL |
| **Poly Pizza** (Google Poly archive + others) | **Per-model**: mostly **CC-BY 3.0** (credit "X by Y [CC-BY] via Poly Pizza"), some CC0 | VERIFIED (secondary) https://app.cinevva.com/hi/guides/free-3d-model-sites , https://flat.social/credits |
| **BlenderKit** free tier (~10k models, 10k materials, 1k HDRIs, no login) | Two licenses: **CC0** or **Royalty Free** (commercial use, no credit; no resale of the asset as-is). Full library $14.90/mo or $108/yr (Sep 2025 price). | VERIFIED https://www.blenderkit.com/docs/licenses/ , https://www.cgchannel.com/2025/09/get-over-48000-free-3d-models-materials-and-hdris-from-blenderkit/ |
| **Sketchfab** "downloadable" models | Per-model CC licenses (CC-BY, CC-BY-SA, CC-BY-NC, CC0, or Sketchfab Standard / editorial). Store the license per asset; BY needs credit and NC is banned for commercial work. | INFERENCE (search did not cover Sketchfab license text) |

**INFERENCE (pipeline rule)**: keep an `assets/manifest.json` with source URL, license, author and attribution string for every imported asset. Have the agent refuse NC/ND/editorial assets automatically, and generate credits from the manifest. Prefer CC0 sources (Poly Haven, ambientCG, Kenney, Quaternius) so credits are optional.

---

## 5. Characters

### Sources
- **Mixamo.** VERIFIED: still online as of late 2026 ("Available" on Adobe status), free with an Adobe ID, no announced end-of-life, but effectively unmaintained. Multi-day outage in Jun 2025; login and download failures reported. Adobe's FAQ (as cited) says characters and animations are royalty-free for commercial and non-commercial use. https://statusgator.com/services/adobe-creative-cloud/mixamo , https://www.edgechat.ai/mixamo , https://www.meshy.ai/blog/mixamo-alternative , https://app.cinevva.com/guides/mixamo-to-blender-2026
  - INFERENCE: commonly understood terms are that you may use it in commercial renders and games, but **not redistribute the raw character or animation files** as stock assets. Mixamo has **no public API**, so automating downloads would scrape an Adobe login flow, which is a ToS risk. Download a curated set by hand once, store it locally, and treat it as a static library.
- **Quaternius Universal Animation Library (UAL).** VERIFIED: one universal humanoid rig, **CC0**. v2 has 130+ clips (locomotion in 8 directions, jog, sprint, crawl, swim, sit, deaths, etc.). The free Standard tier has about 45 clips (v1) or about 70% of v2. The Source (.blend with rig) tier costs ~$14.99 and Pro ~$9.99. Retarget-ready and Mixamo-compatible. The v2.1 re-export fixed a 24 fps vs 30 fps bug. https://quaternius.com/packs/universalanimationlibrary.html , https://quaternius.itch.io/universal-animation-library , https://digitalproduction.com/2026/02/10/130-animations-one-rig-zero-drama/
  - **INFERENCE: best default for an automated pipeline.** It is CC0, has a single consistent rig and local files, and needs no API or login.
- **Kenney.** VERIFIED CC0 (see section 4). INFERENCE: includes animated low-poly character kits, good for stylized crowds.
- **Rigify.** INFERENCE: bundled with Blender (GPL). Generates control rigs from metarigs. Overkill for an agent; most automated work only needs a deform skeleton + actions, so skip control rigs.
- **MakeHuman / MPFB2.** VERIFIED: MPFB code is GPL and MakeHuman is AGPL. The bundled assets and **content created are CC0**, so they are usable commercially with no attribution. The formal MakeHuman exception is worded around exports from official unmodified MakeHuman; how it applies to MPFB2 exports was not confirmed. https://www.cgchannel.com/2025/03/check-out-open-source-blender-character-generation-plugin-mpfb-2 , https://static.makehumancommunity.org/about/license.html , https://scancode-licensedb.aboutcode.org/make-human-exception.html
  - INFERENCE: MPFB2 is scriptable from bpy, so the agent can generate varied realistic humans procedurally. Good for crowds of distinct people.
- **Ready Player Me.** VERIFIED: **shut down**. Netflix acquired it in Dec 2025, and public services and SDKs ended on 31 Jan 2026. Don't use it. https://en.wikipedia.org/wiki/Ready_Player_Me , https://www.pocketgamer.biz/netflix-acquires-avatar-creation-platform-ready-player-me , https://avatarsdk.com/blog/2026/08/31/avatar-platforms-2026-whos-alive-whos-gone/

### Retargeting
- **VERIFIED** The **Rokoko Studio Live** Blender add-on is free and retargets Mixamo and other mocap onto Rigify and other rigs. It can lag behind new Blender versions. **Auto-Rig Pro** is the paid, more robust option (its "Remap"); one guide lists ARP support up to 5.1. A community "Mixamo Rig" extension exists on extensions.blender.org. https://www.blendernation.com/2023/01/14/the-simplest-way-to-retarget-mocap-to-a-rigify-rig-free-and-easy , https://cgdivetest.super.site/sub-categories/blender-retargeting-addons , https://app.cinevva.com/guides/mixamo-to-blender-2026
- **INFERENCE: pipeline recommendation.** Avoid retargeting at runtime. Standardize on **one skeleton** (the Quaternius UAL rig, or Mixamo's) and pre-convert every character and clip to it once, offline, with a human checking the result. Then the agent only:
  1. imports a character,
  2. assigns actions or NLA strips (`obj.animation_data.nla_tracks.new()`, `track.strips.new(name, start, action)` with `blend_in/out`, `repeat`, `scale`),
  3. moves the root along a path.
  - NLA is the agent-friendly way to sequence "walk 0–60 → turn → run 60–120". INFERENCE: on 5.x, every action must have a slot assigned to the object (`animation_data.action_slot`).

### Crowds
- **VERIFIED** GN can instance rigged, animated characters. Add-ons:
  - Bake Instance Animation: GPL, 4.2+, bakes GN instance animation to keyframes.
  - Procedural Crowds by Difffuse: paid GN add-on with 20 characters and formation/follow-curve modes.
  - iCrowds 2.0: ragdoll and painting added Mar 2026.
  - Locomotion add-on: paid; its demo Mixamo characters are not licensed for commercial use.

  https://extensions.blender.org/add-ons/bake-instance-animation/ , https://80.lv/articles/a-new-add-on-for-creating-procedural-crowds-in-blender/ , https://www.cgchannel.com/tag/background-crowd/ , https://blendermarket.com/products/locomotion-addon , https://www.blendernation.com/2022/04/19/crowd-simulation-in-seconds-with-blender-3-1-geometry-nodes/
- **INFERENCE: CrowdMaster** (2.7x era) is abandoned; ignore it.
- **INFERENCE: practical crowd tricks.**
  1. Instances of one animated collection all share the same pose. To desync them, make N (5–10) copies of each character with time-offset NLA strips or different clips. Put them in a collection and let GN "Pick Instance" randomly per point. The eye sees variety.
  2. For large or background crowds, bake each animated character to an **Alembic** or **USD** cache, or a GN Bake node, so the armature isn't evaluated N times.
  3. Distant crowds: use **imposters**: pre-rendered sprite sheets on camera-facing planes, or very low-poly Kenney/Quaternius figures.
  4. Keep crowds under ~200–500 deformed rigs per shot on 12 GB VRAM. Beyond that, use baked or instanced meshes.

### Procedural "physics" animation
- **INFERENCE** Falling and tumbling: rigid bodies (`bpy.ops.rigidbody.object_add()`, `type='ACTIVE'`, mass, friction) plus `bpy.ops.ptcache.bake_all(bake=True)`. Floating or bobbing: noise F-modifiers on location and rotation, or `sin(frame)` drivers. Ragdoll: there is no native ragdoll. Options are rigid-body chains with constraints ("Generic Spring" between bone proxies plus Child Of / Copy Transforms back onto the armature), the iCrowds ragdoll (VERIFIED it exists, above), or a pre-made "death/fall" clip from UAL. Pre-made clips are by far the most reliable.

---

## 6. Physics

- **Rigid body** (Bullet). INFERENCE: set up through bpy; scene-level `scene.rigidbody_world` with `substeps_per_frame` and `solver_iterations`; cache through `point_cache.frame_start/end`. Bake headless with `bpy.ops.ptcache.bake_all(bake=True)` (bakes all point caches), then save the .blend so the bake travels with it. Context: `ptcache` ops may need a context override in background mode, e.g. `with bpy.context.temp_override(scene=scene, ...)`.
- **Cell Fracture.** VERIFIED: extension v0.2.1 (above). INFERENCE: run once in the build stage (`bpy.ops.object.add_fracture_cell_objects(...)` after enabling the extension), then rigid-body the shards. Quality quirks: reviewers report pieces left unsplit. Alternative: a GN Voronoi fracture node group you control.
- **Mantaflow (smoke, fire, liquid).** VERIFIED: "Bake All" works only with the **Final** cache type and cannot be paused or resumed; **Modular** and **Replay** can be resumed. https://docs.blender.org/manual/en/latest/physics/fluid/type/domain/cache.html
  - INFERENCE: in headless runs use `bpy.ops.fluid.bake_all()` with a context override on the domain object, a fixed `cache_directory`, and an explicit `cache_frame_start/end`. Liquids at usable resolution (128–256) take tens of minutes to hours per shot and gigabytes of cache. Results are reproducible on the same build and hardware, but not byte-identical across machines or versions.
- **Cloth.** INFERENCE: classic cloth modifier plus point cache works headless. 5.2's GN XPBD cloth and hair solver is **experimental** (VERIFIED, heise above), so avoid it in production in 2026.
- **When to fake vs simulate (INFERENCE):**
  | Effect | Recommended |
  |---|---|
  | Object drops, bounces, settles | Rigid body sim, bake once |
  | Wobble, float, hover, shake, sway | Keyframes + Noise/Cycles F-modifiers, or drivers (deterministic, free) |
  | Ocean / water surface | Ocean modifier (procedural, no bake) |
  | Splash, pour, liquid interaction | Mantaflow only if it's the hero shot; otherwise stock VFX overlay in post |
  | Smoke/fire background | EEVEE volume with animated noise texture, or stock VFX plates; Mantaflow for hero shots |
  | Explosion debris | Cell Fracture + rigid body, or GN instanced debris with keyframed velocity |
  | Flags, cloth | Shape-key / GN wave deformer (fake) unless close-up |
- **Determinism and caching (INFERENCE):**
  - Pin the Blender version (portable tarball, checksum).
  - Pin seeds (GN Random Value seed, particle seed, Cycles `seed`, `use_animated_seed` off).
  - Bake all simulations to disk in a dedicated "bake" stage and commit or archive the caches with the shot.
  - Never simulate inside the render loop.
  - Render nodes read caches only. Then re-renders after a camera tweak don't change the physics.

---

## 7. Cameras

- **INFERENCE (API long-stable):**
  - **Follow Path**: `c = cam.constraints.new('FOLLOW_PATH'); c.target = curve_obj; c.use_curve_follow = True`. Animate `curve.data.eval_time` or `c.offset_factor` (with `use_fixed_location=True`) from 0→1 over the shot. Use `path_duration` for timing.
  - **Track To / Damped Track**: `t = cam.constraints.new('TRACK_TO'); t.target = empty; t.track_axis='TRACK_NEGATIVE_Z'; t.up_axis='UP_Y'`. Animate the **empty** for smooth reframing. Damped Track is less prone to flips.
  - **Keyframed bezier moves**: keyframe `location`/`rotation_euler` and set `keyframe.interpolation='BEZIER'` with easing for ease-in/out. Using a parent rig (empty "dolly" → empty "pan" → camera "tilt") keeps motion separable.
  - **Camera shake**: add a `NOISE` F-modifier to rotation (and lightly to location) F-curves of a *shake empty* parented between rig and camera. Strength ~0.005–0.02 rad, scale ~10–30 frames. Use `phase` to vary seeds per shot and `use_restricted_range` / blend in and out to ramp it.
  - Lens: `cam.data.lens` (mm), `sensor_width`, `dof.use_dof`, `dof.focus_object`, `aperture_fstop`. Vertical 9:16 means `resolution_x=1080, resolution_y=1920`; keep `sensor_fit='AUTO'` or set `'VERTICAL'` explicitly.
- **Storyboard shot types → code (INFERENCE).** The agent should implement each as a reusable function `make_shot(type, subject, start, end, **params)`:
  | Shot | Implementation |
  |---|---|
  | Establishing / wide | Lens 18–24 mm, high position, slow dolly-in along a 2-point bezier, Track To scene centre |
  | Medium / close-up | Lens 35–50 mm (MS) or 85 mm (CU); distance = subject height × factor; Track To subject head bone or empty; DOF on subject |
  | Extreme close-up | 100–135 mm, small aperture f/1.8–2.8, micro-shake |
  | Dolly / push-in | Keyframe camera along its local −Z; ease in/out |
  | Truck / tracking | Follow Path on a curve offset parallel to the subject's path; same `eval_time` mapping as the subject |
  | Orbit | Camera parented to an empty at the subject; keyframe the empty's Z rotation (with linear interpolation for constant speed) |
  | Crane / boom | Animate parent empty Z plus tilt via Track To |
  | Whip pan / transition | 4–6 frame rotation keyframes plus motion blur (EEVEE and Cycles both support it) |
  | Handheld / POV | Noise F-modifier on a shake empty, stronger strength |
  | Drone / flyover | Follow Path along a long NURBS curve 20–100 m up, Track To terrain points |
  | Cuts | Separate camera objects + **timeline markers bound to cameras** (`marker.camera = cam`), which switch the active camera during `-a` |
- **INFERENCE: shot-list JSON is the contract.** The storyboard becomes `shots.json` (`id, type, duration_frames, subject, lens, move, notes`). The agent builds one scene (or one `.blend` per shot), uses camera markers for cuts, and renders frame ranges per shot. Per-shot renders make it cheap to re-render only one shot.

---

## 8. Post-production

- **FFmpeg (INFERENCE for syntax; well-established):**
  - Image sequence → video: `ffmpeg -framerate 30 -i frame_%04d.png -c:v libx264 -pix_fmt yuv420p -crf 18 -preset slow -movflags +faststart shot01.mp4`
  - Concatenate shots: concat **demuxer** (`-f concat -safe 0 -i list.txt -c copy`) for same-codec clips; use the concat filter for re-encoding or mixed sources.
  - Overlays and branding: `-filter_complex "[0:v][1:v]overlay=W-w-40:40"`; text with `drawtext=fontfile=...:text='...':x=...:y=...:enable='between(t,2,5)'`.
  - Subtitles and captions: `-vf "ass=captions.ass"` (libass) or `subtitles=`. ASS **karaoke** tags `{\k<centiseconds>}` / `\kf` (sweep) / `\ko` give word-by-word highlighting generated from word timestamps. Styles, outline, shadow, `\pos`, `\t()` animation and `\fad` are enough for "TikTok-style" pop captions (scale-pop via `\t(0,80,\fscx120\fscy120)\t(80,160,\fscx100\fscy100)`).
  - Loudness: **VERIFIED** two-pass `loudnorm`. Pass 1 measures with `print_format=json`; pass 2 feeds `measured_*` values with `linear=true`. Common social target is **I=−14 LUFS, TP=−1 dBTP, LRA=11**; FFmpeg's default −24 is a broadcast value. `ffmpeg-normalize` wraps this. https://dev.to/javidjamae/ffmpeg-loudnorm-filter-ebu-r128-loudness-normalization-guide-15d4 , https://www.skills.sh/gooseworks-ai/gooseworks-ads-skills/normalize-loudness , https://github.com/mjhalwa/ffmpeg-normalize
- **Blender VSE scripting.** VERIFIED: 5.0 brought a large VSE refresh. https://osarch.org/2025/11/18/blender-5-0-released/
  - INFERENCE: the VSE is fully scriptable (`scene.sequence_editor`; in 4.4+/5.x the collection was renamed from `sequences` to `strips`, so watch for LLM-generated legacy code). It can assemble shots, audio and text strips in the same headless Blender. It works, but FFmpeg is simpler and faster for an agent; use the VSE only if you want everything in one .blend.
- **DaVinci Resolve.** VERIFIED: the **external** scripting API (Python/Lua driving Resolve from outside) is **Studio-only** (paid, ~$295 one-time, INFERENCE price). The free version runs scripts only from the Console or Workspace → Scripts menu. Community MCP bridges for free Resolve work around this by running a script inside Resolve. https://forum.blackmagicdesign.com/viewtopic.php?p=670352 , https://thepostflow.com/post-production/video-editing/resolve-studio-vs-free/ , https://github.com/hiteshK03/davinci-resolve-mcp
  - INFERENCE: Resolve still needs a GUI instance running, so it is good for human colour and finishing passes, not for unattended agent runs.
- **CapCut.** VERIFIED (secondary): no official editing or rendering API as of Oct 2026. Its terms reportedly ban automated scripts interacting with the service, and bot or auto-upload use risks account restriction. https://www.wireflow.ai/blog/capcut-api , https://json2video.com/how-to/capcut-api/ , https://www.miracamp.com/learn/capcut/account-reinstatement
  - **Don't automate CapCut**; at most, a human uses it manually for final trend-template polish.
- **MoviePy.** VERIFIED: v2.0 broke the API (`moviepy.editor` removed, `.set_*` → `.with_*`, effects via `with_effects()`), and v1 is unmaintained. Slower than raw FFmpeg. https://zulko.github.io/moviepy/getting_started/updating_to_v2.html , https://github.com/Zulko/moviepy
  - INFERENCE: OK for Python-side compositing glue. LLMs still mostly write v1 code, so pin the version and give the agent the migration guide.
- **Remotion.** VERIFIED: free for individuals and for-profit organisations with **≤3 employees** (total headcount, not users). Bigger companies need a Company License: Creators about $25/seat/month, Automators about $0.01/render with a $100/month minimum, Enterprise from $500/month. https://github.com/remotion-dev/remotion/blob/main/LICENSE.md , https://www.remotion.dev/docs/license/pricing , https://www.remotion.dev/docs/license/faq.md , https://www.layer3labs.io/comparisons/claude-motion-vs-remotion
  - Strength: React-based, frame-accurate deterministic rendering of captions, counters, lower thirds and charts, with an agent-friendly codebase. `@remotion/three` must drive animation with `useCurrentFrame()`, never R3F's `useFrame()`. https://convert.remotion.dev/docs/three-webgpu-canvas
- **Motion Canvas.** INFERENCE: MIT-licensed, TypeScript, code-driven 2D animation. A free alternative to Remotion for animated captions, counters and diagrams, with no company license fee.
- **Word timestamps.** VERIFIED: **WhisperX** combines a faster-whisper backend (~70x realtime with large-v2, batched), VAD and **wav2vec2 forced alignment** for accurate word-level times. Raw Whisper segment times can be off by seconds. Limits: numbers and symbols like "£13.60" may get no timestamp, and overlapping speech is handled poorly. https://github.com/m-bain/whisperx
  - INFERENCE: `faster-whisper` alone with `word_timestamps=True` (cross-attention DTW) is usually good enough for captions. Use WhisperX when sync must be tight. If you generate the voice with a TTS that returns timestamps (many do), skip ASR entirely.
- **Captions and counters: options (INFERENCE):**
  1. **ASS karaoke via FFmpeg/libass**: cheapest and fully scriptable; enough for word-pop captions.
  2. **Remotion or Motion Canvas**: richest motion design (springs, counters, emoji pops). Render a transparent ProRes 4444 / WebM overlay and composite with FFmpeg. Mind the Remotion license.
  3. **Blender text objects**: 3D in-scene text and counters (drive `text.body` with a frame-change handler, or GN String to Curves (VERIFIED improved in 5.1) driven by frame). Best for diegetic text; slower to iterate.

---

## 9. Three.js vs Blender

| Dimension | Blender (EEVEE/Cycles) | Three.js (WebGL/WebGPU) |
|---|---|---|
| Procedural scenes | GN, modifiers, sims, huge add-on and asset ecosystem | Write everything yourself; instancing is fast, but no node-based modelling or sims |
| Animation | Full rigging, NLA, IK, shape keys, physics, mocap import | glTF skeletal clips via AnimationMixer; basic blending; no authoring tools |
| Quality | EEVEE: near real-time with raytraced GI. Cycles: physically based path tracing | Good PBR raster; path tracing only via third-party libs (e.g. three-gpu-pathtracer, not verified this session) |
| Headless rendering | Native `blender -b`, frame-exact, writes image sequences | Needs Puppeteer/Playwright + virtual time to be frame-exact; GPU or SwiftShader differences; readiness signalling needed |
| Determinism | High (seeded, baked caches, same binary) | Achievable but fragile: you must override `requestAnimationFrame`/`performance.now()` or drive frames manually; output not byte-identical across machines |
| Speed per frame | EEVEE seconds; Cycles tens of seconds | Milliseconds of render; capture overhead dominates (~5–30 fps capture) |
| Agent ergonomics | Python; LLMs know bpy well but pre-5.0 API habits break | JS/TS; LLMs are very strong; immediate browser preview |

- **VERIFIED**: deterministic Three.js capture tools are puppeteer-capture (HeadlessExperimental virtual time; overrides rAF, Date and performance.now; needs chrome-headless-shell), CCapture.js (fixed-step clock), WebVideoCreator, and BeginFrame-based capture. Output is not byte-identical across machines, so pin the browser version. Headless Chromium often falls back to SwiftShader. https://github.com/alexey-pelykh/puppeteer-capture , https://spite.github.io/ccapture.js/ , https://docs.rs/crate/aether-renderer-capture/0.2.0/source/README.md , https://macmyths.com/how-to-capture-webgl-pages-with-puppeteer/
- **VERIFIED (secondary)**: Three.js r171 (Nov 2024) made WebGPURenderer zero-config with WebGL2 fallback. https://buttondown.com/webgamedev/archive/issue-024/ , https://www.utsubo.com/blog/webgpu-threejs-migration-guide
- **INFERENCE: recommended role.** **Blender for every final frame.** Use Three.js (or Remotion + `@remotion/three`) only for:
  1. instant **animatics and previs**: block shots with primitives, preview camera moves in the browser and get human sign-off on timing before spending GPU hours;
  2. **2.5D/graphic overlays** (stylized UI, charts, counters) that are composited in post;
  3. an optional web "shot reviewer" that loads exported glTF of the blocked scene.
  - Don't build two parallel 3D pipelines. If previs is in Three.js, export camera paths as JSON that the Blender build script consumes, so previs and the final match.

---

## 10. Hardware and cloud (mostly INFERENCE; the search budget ran out before verification)

### Blender requirements (INFERENCE, from Blender's published requirements page; blender.org was unreachable this session)
- Minimum: 64-bit quad-core CPU with SSE4.2 (x86) or Apple Silicon/ARM64, 8 GB RAM, 1080p display, GPU with 2 GB VRAM supporting OpenGL 4.3 (Vulkan 1.2 for the Vulkan backend). GPU drivers less than ~2 years old.
- Recommended: 8+ core CPU, 32 GB RAM, GPU with 8 GB+ VRAM.
- Cycles GPU support levels are VERIFIED in section 2.

### A solid budget build for this workload (INFERENCE)
- **GPU: NVIDIA with 12–16 GB VRAM** is the priority. VRAM caps scene size: crowds, 4K textures and EEVEE shadow pools. 8 GB will hit limits (VERIFIED that VRAM is the bottleneck on the RTX 4060: https://www.databasemart.com/blog/blender-gpu-cpu-benchmark-rtx4060-e5-2667v3).
  - Sweet spots: RTX 4070 Super/5070 (12 GB), RTX 4060 Ti 16 GB or 5060 Ti 16 GB (slower but more VRAM), used RTX 3090 24 GB (great VRAM per dollar).
  - NVIDIA wins because OptiX is the fastest Cycles backend and has the broadest headless Linux support.
- **CPU**: 8–16 cores (Ryzen 7/9). It matters for scene building, sim baking (Mantaflow is CPU-only), FFmpeg encodes and WhisperX on CPU.
- **RAM**: 64 GB recommended (32 GB minimum). Fluid bakes, big .blend files and running ASR, the browser and Blender together.
- **Storage**: 2 TB NVMe for working data plus a big HDD or NAS for archive. One 2,100-frame PNG 1080×1920 sequence is about 4–8 GB (EXR multilayer ~20–60 GB); Mantaflow caches run into tens of GB.
- **OS**: Linux (Ubuntu LTS) for headless reliability, with Docker images pinned to a Blender tarball. Windows works if you want the same box for Resolve.
- **INFERENCE: Apple Silicon vs NVIDIA.**
  - M4 Max ≈ RTX 4070 in Cycles (VERIFIED score above) and has huge unified memory (36–128 GB), so very large scenes don't hit VRAM limits.
  - But it costs about 3–4x as much per unit of render throughput as a 4070 desktop, has no OptiX, and has no cloud parity: cloud farms are Linux/NVIDIA.
  - A Mac works well as the **agent/dev workstation** (EEVEE previews are fine). Use NVIDIA (local or cloud) for bulk renders.

### Cloud rendering (INFERENCE: prices from memory of 2025–2026 listings; verify before buying)
- **SheepIt Render Farm**: free, community-driven, credit/points system. You earn points by rendering others' frames and spend them on yours. Supports Cycles and EEVEE on recent Blender versions with a lag after each release. Limits: projects must be self-contained .blend files (packed textures), there are upload size and per-frame time limits, add-ons and Python are restricted, and the farm is public, so it is not suitable for confidential work. Good for occasional overflow; unreliable for deadlines.
- **GPU cloud (bring your own Blender in Docker):**
  - RunPod: RTX 4090 about $0.35–0.70/h (community vs secure cloud), RTX 3090/A5000 about $0.20–0.45/h, L40S about $0.80–1.00/h.
  - Vast.ai marketplace: RTX 4090 about $0.25–0.60/h, RTX 3090 about $0.15–0.30/h; reliability varies by host.
  - Lambda / Paperspace / AWS g5/g6 are pricier (AWS g6.xlarge L4 about $0.80/h on-demand).
  - Example (INFERENCE): a Cycles short needing ~10 h on a 4070 is about 5 h on a 4090, so about **$2–4 per full render** on RunPod/Vast. EEVEE renders cost cents. Remember EEVEE headless on cloud Linux needs a test (section 2); Cycles OptiX is the safe cloud choice.
- **Commercial Blender farms** (GarageFarm, RebusFarm, iRender, Ranch Computing, Fox Renderfarm): they bill per GHz-hour or per node-hour.
  - iRender rents whole GPU servers at about $1–9/h depending on the number of GPUs.
  - A typical short-form Cycles job costs about $10–100 depending on scene and priority.
  - They are convenient (managed Blender versions, add-on support), but for an agent-driven pipeline, raw GPU rental with your own pinned Docker image is cheaper and more reproducible.

---

## Decision summary (INFERENCE unless noted)
1. **Pin Blender 5.2 LTS** (VERIFIED, supported to Jul 2028) as a portable tarball or Docker image. Hold 5.3 until the pipeline is stable.
2. **The agent writes versioned bpy scripts and runs `blender -b ... -P ... --` via Bash**, in build → bake → render stages. MCP is optional, for interactive look-dev only.
3. **EEVEE is the default engine** for vertical shorts: a 70 s short in about 1–3 h on an RTX 4070-class GPU. Cycles is the hero/upgrade path at about 5–18 h per short on the same card, or a few dollars on a rented 4090.
4. **Put a CLAUDE.md "5.x API gotchas" sheet in front of the agent**:
   - `Action.fcurves` was removed (use channelbags);
   - GPv3 API changes;
   - `media_type` for video output;
   - 5.2 GN modifier input API change;
   - VSE `strips` rename;
   - engine id changes.
5. **Assets: CC0 first** (Poly Haven, ambientCG, Kenney, Quaternius, MPFB2 output). Keep a license manifest. Mixamo is usable but unmaintained; download once, by hand. Ready Player Me is gone.
6. **Characters**: standardize on one skeleton (Quaternius UAL, CC0); sequence clips with NLA; build crowds from time-offset instance variants or baked caches.
7. **Physics**: fake with F-curve noise and drivers by default. Bake rigid body, cloth and fluids once to disk, then render from caches.
8. **Post**: FFmpeg (concat, ASS karaoke captions, two-pass loudnorm to −14 LUFS), WhisperX or faster-whisper for word timing, optional Remotion (free only for companies with ≤3 people) or Motion Canvas (MIT) for motion graphics. No CapCut automation; Resolve's external API needs Studio.
9. **Three.js / Remotion-three for fast animatics and previs only**; Blender produces the final pixels.
10. **Hardware**: Linux box with an NVIDIA 12–16 GB GPU, 64 GB RAM and 2 TB NVMe, about $1.5–2.2k (INFERENCE). Burst to RunPod/Vast for Cycles.

---

## Sources (consulted via search excerpts)

**Blender releases and features**
- https://osarch.org/2025/11/18/blender-5-0-released/
- https://www.phoronix.com/news/Blender-5.0-Released
- https://www.blendernation.com/blender-5-1-released
- https://osarch.org/2026/03/17/blender-5-1-released/
- https://linuxiac.com/?p=209138
- https://www.blender.org/releases/5-2/
- https://www.blender.org/press/blender-5-2-lts-release/
- https://www.heise.de/en/news/Blender-5-2-LTS-New-Simulations-and-Eevee-Improvements-11366897.html
- https://www.cgchannel.com/2026/07/blender-5-2-lts-is-here-discover-its-5-key-features/
- https://digitalproduction.com/2026/07/21/blender-5-2-lts-lands-with-node-physics/
- https://releasebot.io/updates/blender
- https://www.strayspark.studio/blog/blender-5-3-texture-layers-baking-game-developers
- https://80.lv/articles/blender-in-2026-planned-features-projects
- https://developer.blender.org/docs/release_notes/5.0/geometry_nodes/
- https://code.blender.org/2025/10/geometry-nodes-workshop-september-2025/
- https://www.blendernation.com/2024/07/16/blender-4-2-lts-released-check-out-these-standout-features/
- https://cgchannel.com/2024/07/5-key-features-in-blender-4-2
- https://developer.blender.org/docs/release_notes/4.3/grease_pencil_migration/
- https://www.cgchannel.com/2024/10/blender-4-3-lets-you-control-grease-pencil-with-geometry-nodes
- https://www.phoronix.com/news/Blender-5.0-Vulkan-OpenGL-RAM
- https://www.phoronix.com/news/Blender-5.1-Vulkan-Default
- https://hwbusters.com/?p=118866
- https://docs.blender.org/api/5.0/change_log.html
- https://docs.blender.org/api/5.0/bpy.types.ActionChannelbagFCurves.html
- https://app.cinevva.com/es/guides/blender-5-for-game-artists
- https://docs.blender.org/api/5.0/bpy.types.ImageFormatSettings.html
- https://docs.blender.org/manual/en/5.0/render/output/properties/output.html

**License**
- https://www.blender.org/?p=658
- https://www.blender.org/support/faq/
- https://archive.blender.org/lists/bf-committers/2004-November/008253.html
- https://en.wikibooks.org/wiki/Blender_3D:_Noob_to_Pro/Using_proper_copyright_RE:Blender

**Headless, API, MCP**
- https://docs.blender.org/manual/en/2.80/advanced/command_line/arguments.html
- https://archive.blender.org/wiki/2015/index.php/Reference/CL
- https://salaivv.notion.site/Blender-Python-Cheatsheet-9cfb88dbc4a34d829d4305982053a05e
- https://docs.blender.org/manual/en/latest/render/cycles/gpu_rendering.html
- https://devtalk.blender.org/t/blender-2-8-unable-to-open-a-display-by-the-rendering-on-the-background-eevee/1436
- https://developer.blender.org/T61164
- https://gist.github.com/UuuNyaa/f57aa37fc6ed2fbd5c166513a16a40e5
- https://github.com/miyabi-sunny-side/blender-live
- https://irendering.net/eevee-next-headless-dilemma-cloud-render-farm-guide/
- https://projects.blender.org/blender/blender/issues/77339
- https://pypi.org/project/bpy/
- https://pypi.org/project/bpy/5.0.0/
- https://pypi.org/project/fake-bpy-module-5-1/
- https://aiwiki.ai/wiki/blender_mcp
- https://github.com/ahujasid/blender-mcp/releases
- https://ai-heartland.com/tool/blender-mcp-guide/
- https://www.strayspark.studio/blog/official-blender-mcp-server-comparison-2026

**Performance**
- https://9to5mac.com/2024/11/17/m4-max-blender-benchmark/
- https://wccftech.com/apple-m4-max-chip-belender-benchmarks-against-rtx-4090/amp/
- https://www.renderjuice.com/gpus/compare/rtx-3060-vs-rtx-4070-ti
- https://www.development.renderjuice.com/gpus/compare/rtx-4060-vs-rtx-4060-ti
- https://www.development.renderjuice.com/gpus/rtx-4060-ti-for-blender
- https://wiki.blender.org/release_notes/4.1/cycles/
- https://www.cgchannel.com/2024/03/5-key-features-in-blender-4-1/
- https://evezone.evetech.co.za/performance-pulse/rtx-5060-blender-performance-benchmark-real-world-test-2026
- https://blenderartists.org/t/cycles-vs-eevee-next-comparison/1540799
- https://dev.to/irender_gpu_render_farm/which-renderer-should-we-choose-cycles-or-eevee-10o9
- https://studio.blender.org/blog/rendering-snow-parkour-animation-with-eevee
- https://www.databasemart.com/blog/blender-gpu-cpu-benchmark-rtx4060-e5-2667v3

**Environments and assets**
- https://extensions.blender.org/add-ons/bagapie/versions/
- https://www.cgchannel.com/2025/05/get-free-blender-modeling-and-scattering-add-on-bagapie-11/
- https://www.cgchannel.com/2022/07/download-free-blender-3d-building-generator-buildify/
- https://couturier-arnaud.gumroad.com/l/scenecity/v2_0_1s2x55q
- https://www.blender.org/manual/en/addons/add_mesh/ant_landscape.html
- https://extensions.blender.org/add-ons/cell-fracture/
- https://docs.blender.org/manual/en/4.0/modeling/modifiers/physics/index.html
- https://app.cinevva.com/guides/game-assets-guide
- https://app.cinevva.com/hi/guides/free-3d-model-sites
- https://flat.social/credits
- https://www.blenderkit.com/docs/licenses/
- https://www.blenderkit.com/faq-frequently-asked-questions/
- https://www.cgchannel.com/2025/09/get-over-48000-free-3d-models-materials-and-hdris-from-blenderkit/

**Characters and crowds**
- https://statusgator.com/services/adobe-creative-cloud/mixamo
- https://www.edgechat.ai/mixamo
- https://www.meshy.ai/blog/mixamo-alternative
- https://app.cinevva.com/guides/mixamo-to-blender-2026
- https://quaternius.com/packs/universalanimationlibrary.html
- https://quaternius.itch.io/universal-animation-library
- https://digitalproduction.com/2026/02/10/130-animations-one-rig-zero-drama/
- https://www.cgchannel.com/2025/03/check-out-open-source-blender-character-generation-plugin-mpfb-2
- https://static.makehumancommunity.org/about/license.html
- https://scancode-licensedb.aboutcode.org/make-human-exception.html
- https://en.wikipedia.org/wiki/Ready_Player_Me
- https://www.pocketgamer.biz/netflix-acquires-avatar-creation-platform-ready-player-me
- https://avatarsdk.com/blog/2026/08/31/avatar-platforms-2026-whos-alive-whos-gone/
- https://www.blendernation.com/2023/01/14/the-simplest-way-to-retarget-mocap-to-a-rigify-rig-free-and-easy
- https://cgdivetest.super.site/sub-categories/blender-retargeting-addons
- https://extensions.blender.org/add-ons/bake-instance-animation/
- https://80.lv/articles/a-new-add-on-for-creating-procedural-crowds-in-blender/
- https://www.cgchannel.com/tag/background-crowd/
- https://blendermarket.com/products/locomotion-addon
- https://www.blendernation.com/2022/04/19/crowd-simulation-in-seconds-with-blender-3-1-geometry-nodes/

**Physics**
- https://docs.blender.org/manual/en/latest/physics/fluid/type/domain/cache.html

**Post**
- https://dev.to/javidjamae/ffmpeg-loudnorm-filter-ebu-r128-loudness-normalization-guide-15d4
- https://www.skills.sh/gooseworks-ai/gooseworks-ads-skills/normalize-loudness
- https://github.com/mjhalwa/ffmpeg-normalize
- https://forum.blackmagicdesign.com/viewtopic.php?p=670352
- https://thepostflow.com/post-production/video-editing/resolve-studio-vs-free/
- https://github.com/hiteshK03/davinci-resolve-mcp
- https://www.wireflow.ai/blog/capcut-api
- https://json2video.com/how-to/capcut-api/
- https://www.miracamp.com/learn/capcut/account-reinstatement
- https://zulko.github.io/moviepy/getting_started/updating_to_v2.html
- https://github.com/Zulko/moviepy
- https://github.com/remotion-dev/remotion/blob/main/LICENSE.md
- https://www.remotion.dev/docs/license/pricing
- https://www.remotion.dev/docs/license/faq.md
- https://www.layer3labs.io/comparisons/claude-motion-vs-remotion
- https://convert.remotion.dev/docs/three-webgpu-canvas
- https://github.com/m-bain/whisperx

**Three.js**
- https://github.com/alexey-pelykh/puppeteer-capture
- https://spite.github.io/ccapture.js/
- https://docs.rs/crate/aether-renderer-capture/0.2.0/source/README.md
- https://macmyths.com/how-to-capture-webgl-pages-with-puppeteer/
- https://buttondown.com/webgamedev/archive/issue-024/
- https://www.utsubo.com/blog/webgpu-threejs-migration-guide

**Not verified this session (search budget exhausted)**
- Blender min/recommended specs page (blender.org/download/requirements)
- SheepIt, RunPod, Vast.ai and commercial farm pricing
- Sketchfab license text
- Sverchok status
- three-gpu-pathtracer
- ASS karaoke spec details
