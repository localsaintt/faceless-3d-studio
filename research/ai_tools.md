# AI Tools for an Automated Faceless 3D Animation Studio (Blender + Python + Claude Code)

Research date: 2026-11-02. Research only; nothing was signed up for or purchased.

## Method and confidence labels

- **VERIFIED (URL)**: the claim appears in a search-engine snippet or summary of the linked page, and the page is the vendor's own (official site, docs, GitHub/Hugging Face model card, help center) or a named news outlet.
- **SECONDARY (URL)**: the claim comes from aggregators, review blogs or affiliate pricing trackers (costbench, stacksheriff, eesel, etc.). Treat these as directional. They often disagree with each other.
- **INFERENCE**: my own reasoning or prior knowledge, not confirmed this session.

**Important limitation:** in this sandbox WebFetch could not resolve vendor domains (docs.meshy.ai, hyper3d.ai, tripo3d.ai and others failed with DNS errors, so the session's network allowlist blocks them). Everything below comes from WebSearch result summaries. Before spending money, open each vendor's pricing page and license page yourself. Prices move monthly in this space. Several vendors changed plans in 2026 (Runway, Pika, Meshy).

---

## A. Text/Image-to-3D

| Tool | Status (Nov 2026) | Pricing | API | Free-tier commercial? | Local run |
|---|---|---|---|---|---|
| Meshy | Operating (Meshy 6) | Free / Pro $20/mo (1,000 cr) / Studio $60/mo (~4,000 cr) / Enterprise | Yes (Pro+) | Free = CC BY 4.0 (commercial allowed with attribution; assets public) | No |
| Tripo (Tripo3D) | Operating (v3.x, Smart Mesh) | Paid from about $20/mo (figures conflict); API credits about $0.01 each | Yes (separate credit billing) | Free = CC BY 4.0, reported as not for commercial use | No (though UniRig is open source, see B) |
| Rodin (Hyper3D) | Operating (Gen-2 / Gen-2.5) | Creator about $24–30/mo, Business about $96–120/mo (API is Business tier) | Yes (Business, also via fal.ai) | Unclear; check ToS | No |
| Hunyuan3D 2.1 (Tencent) | Open weights; 3.0 is hosted/API | Free weights; Tencent Cloud API for 3.0 | Tencent Cloud | Community license; **EU/UK/South Korea excluded** | 10 GB shape, 21 GB texture, 29 GB both |
| TRELLIS.2 (Microsoft) | Released Dec 2025, MIT | Free | Self-host / HF demo | MIT, commercial OK | 24 GB practical (16 GB at 512³; 40–80 GB at high res); Linux only |
| Stable Fast 3D / SPAR3D | Open weights | Free under $1M annual revenue | Stability API | Stability Community License | Low VRAM (INFERENCE: about 6–8 GB) |
| Luma Genie | Appears live in the Luma API (Pro tier) | Unclear | Luma API | Unclear | No |
| CSM (csm.ai) | **Possibly acquired by Google (Jan 2026), unconfirmed** | $20 / $60 / $499 / $2,000 tiers (secondary) | Yes | Unclear | No |
| Sloyd | Operating | Free (1 gen/day, personal) / Plus $15/mo / Pro about $50/mo | Yes, prepaid credits | Free = personal use only | No |

### Meshy
- **What it does:** text/image-to-3D, AI texturing, auto-rigging (humanoid and quadruped), and 500+ animation presets, with FBX/GLB export. It has an official Blender plugin. VERIFIED: https://docs.meshy.ai/en/webapp/guides/animate , https://www.meshy.ai/features/ai-auto-rigging
- **Pricing:** Free $0; Pro $20/mo or $240/yr with 1,000 credits/mo (credits do not roll over); Studio $60/mo or $576/yr; Enterprise is custom. VERIFIED via a snippet of https://meshy.ai/pricing . A text/image-to-3D generation costs about 10–15 credits (secondary, conflicting): https://stacksheriff.com/ai-tools/meshy-ai-pricing/ . I did not find a dollar price per API credit (see https://docs.meshy.ai/pricing).
- **License:** Free tier outputs are CC BY 4.0. Commercial use is allowed with attribution, and the assets are public. Paid tiers are private with full commercial rights. VERIFIED (official docs per snippet): https://docs.meshy.ai/en/webapp/pricing . CostBench says free excludes commercial use, which contradicts the docs: https://costbench.com/software/ai-3d-generation/meshy/free-plan/
- **Quality:** strongest all-in-one pipeline for indie use (generate, texture, rig, animate). Raw meshes are dense triangles, so plan on remeshing or retopology for deforming characters. SECONDARY: https://levelup.gitconnected.com/building-game-ready-3d-assets-fast-the-best-ai-generators-for-production-workflows-in-2026-f1f725ff5df0
- **Verdict:** **Useful.** It is the best single paid tool for background characters and props. Pro at $20 is enough to evaluate. Hero characters still need hand cleanup in Blender, or a Rigify/Mixamo pass.

### Tripo (Tripo3D)
- **What it does:** text/image-to-3D, "Smart Mesh" quad retopology (shipped at GDC in March 2026), auto-rigging and animation. SECONDARY: https://pasqualepillitteri.it/en/news/7811/tripo-ai-review-3d-model-generator
- **Pricing:** consumer plans conflict across sources. Pro is about $19.90–20/mo, and higher tiers run up to about $90–110/mo. SECONDARY: https://costbench.com/software/ai-3d-generation/tripo-ai/ . The API uses its own credit system at $0.01/credit, with add-ons (Smart Mesh +65 credits, Ultra +15 credits). VERIFIED: https://aws.amazon.com/marketplace/pp/prodview-hwlbvx7vubh7c , https://developers.tripo3d.com/en/docs/billing
- **License:** Free tier is CC BY 4.0, and sources say commercial use needs a paid plan. VERIFIED via Tripo's own blog: https://www.tripo3d.ai/blog/commercial-use-ai-3d-models . I could not read the exact free-tier wording.
- **Quality:** best topology of the hosted tools if you pay for Smart Mesh. Rigging is good for humanoids and inconsistent for unusual anatomy. SECONDARY.
- **Verdict:** **Useful as an alternative to Meshy.** Pick one of the two, not both. Tripo co-developed UniRig (open source, see B).

### Rodin (Hyper3D, by Deemos)
- **What it does:** high-fidelity image/text-to-3D (Gen-2, Gen-2.5) with quad mode and 4K PBR. It is integrated into blender-mcp, so Claude Code can call it from Blender. VERIFIED: https://github.com/ahujasid/blender-mcp/wiki , https://github.com/DeemosTech/blender-mcp-rodin-integration
- **Pricing:** Creator is about $24 or $30/mo (sources conflict). Business is $120/mo ($96/mo billed yearly) and includes the API, 4K textures and high-poly quads. The free tier has about 10 credits, and one high-density Gen-2 download is about 40 credits. SECONDARY: https://costbench.com/software/ai-3d-generation/rodin-hyper3d/ . I could not confirm the official prices at https://hyper3d.ai/pricing.
- **License:** Hyper3D's pricing page says paid plans grant broader usage rights. I found no clear free-tier license text. VERIFIED that the license is unclear: https://hyper3d.ai/pricing
- **Verdict:** **Best quality for hero props and statues, but expensive for API automation.** The blender-mcp trial key has a daily cap. Use it selectively.

### Hunyuan3D 2.x (Tencent)
- **Status:** 2.0/2.1 weights are open on Hugging Face under the "tencent-hunyuan-community" license (https://huggingface.co/tencent/Hunyuan3D-2.1/tree/main). 3.0 launched in Sept 2025 as a hosted platform and Tencent Cloud API. I found no evidence that 3.0 weights are public. SECONDARY: https://www.notebookcheck.net/Tencent-s-new-Hunyuan-3D-3-0-brings-realistic-AI-model-generation-to-developers-and-creators.1116964.0.html
- **License, territory:** the 2.1 license defines "Territory" as worldwide **excluding the EU, UK and South Korea**. You may not use or distribute the model there. The text comes from a mirror of the LICENSE: https://gitserver.onethingai.com/ai-models/Hunyuan3D-2.1/raw/branch/main/LICENSE . The 2.0 license says it "does not apply in the European Union, United Kingdom": https://huggingface.co/tencent/Hunyuan3D-2/blob/main/LICENSE . Products with more than 1M MAU need a separate license. Free commercial use is otherwise allowed inside the Territory.
- **Hardware:** 10 GB VRAM for shape, 21 GB for texture, 29 GB for both. A `--low_vram_mode` exists, and people have generated meshes on 6 GB. SECONDARY: https://www.sourcepulse.org/projects/10592187 , https://www.tspi.at/2026/05/01/opensource3dassets.html
- **Verdict:** **Best free local option for users outside the EU/UK/South Korea.** It is supported in blender-mcp and ComfyUI. If the studio operates from or sells into excluded territories, have the license reviewed before use, and use TRELLIS.2 instead.

### Microsoft TRELLIS / TRELLIS.2
- **Status:** TRELLIS.2-4B was released around Dec 18, 2025 under MIT (code and weights). It handles 512³–1536³ resolution with PBR. SECONDARY: https://comfyui-wiki.com/news/2025-12-18-microsoft-trellis2-3d-generation , https://www.codesota.com/news/trellis-2-3d-generation . TRELLIS v1 is also MIT (INFERENCE).
- **Hardware:** 24 GB NVIDIA GPU is the practical minimum. 16 GB works at 512³, and 40–80 GB is needed for higher resolutions. Linux only. Reported times on an H100 are about 3 s, 17 s and 60 s.
- **Verdict:** **The safest free license (MIT) for 3D generation.** It is the default pick for an open-source local pipeline if you have a 24 GB card. Output is triangle soup, so remesh it in Blender (Quadriflow/Instant Meshes) for anything that deforms.

### Stable Fast 3D / SPAR3D (Stability AI)
- **License:** Stability AI Community License. It is free for commercial use if the organization's total annual revenue is under $1M. Above that you need an Enterprise license. VERIFIED: https://stability.ai/license , https://huggingface.co/stabilityai/stable-fast-3d . SPAR3D launched under the same license: https://alternativeto.net/news/2025/1/stability-ai-unveils-stable-point-aware-3d-for-real-time-3d-object-creation-from-images
- **Quality:** fast (under a second), low-poly, UV-unwrapped single objects. Quality is below TRELLIS.2 and Hunyuan (INFERENCE). Fine for quick background props.
- **Verdict:** **Optional.** It fits low-VRAM machines. Otherwise TRELLIS.2 is better and MIT-licensed.

### Luma Genie
- **Status:** I found no shutdown announcement. Genie 3D appears in the Luma API, limited to the Pro tier. SECONDARY: https://www.llmreference.com/model/genie-3d/luma-api , https://gappsy.com/tools/luma-ai/ . I could not find pricing or license terms.
- **Verdict:** **Skip.** Luma's focus is video (Ray3), and Genie is clearly lower priority.

### CSM (Common Sense Machines)
- **Status:** one source claims Alphabet/Google acquired CSM in January 2026 and the team joined DeepMind. **Unconfirmed.** SECONDARY: https://costbench.com/software/ai-3d-generation/csm/ . Listed tiers are Free (10 one-time credits), Maker $20, Creative Pro $60, Startup $499 and Studio $2,000.
- **Verdict:** **Skip.** Its status is uncertain and there is no advantage over Meshy, Tripo or TRELLIS.

### Sloyd
- **What it does:** parametric, template-based generation, with clean low-poly game-ready topology for props, buildings and weapons. It has an API.
- **Pricing and license:** the free Guest plan gives 1 AI generation per day and a personal-use license. Plus is $15/mo ($12.50/mo annual) and Pro is about $50/mo; both include a commercial license. The API is billed separately with prepaid credits, and I found no per-credit price. SECONDARY: https://costbench.com/software/ai-3d-generation/sloyd/ , https://www.sloyd.ai/blog/ai-3d-model-generator-pricing
- **Verdict:** **Niche.** It is good for clean stylized props. Not for characters.

### Topology and rigging summary (A)
- Raw AI meshes are typically 100K–500K+ triangles with no edge flow. That is fine for **static props** after decimation, and **not fine for deforming characters** without quad remesh plus weight cleanup. SECONDARY: https://www.3daistudio.com/blog/best-ai-game-asset-generators-2026
- For characters, the best options are Tripo Smart Mesh or Rodin quad mode (paid), then auto-rig. Free alternative: TRELLIS.2/Hunyuan, then Blender Quadriflow or Instant Meshes, then Mixamo/AccuRIG/UniRig.
- **Blender integration:** blender-mcp (`claude mcp add blender uvx blender-mcp`) exposes Poly Haven, Sketchfab, Hyper3D Rodin and Hunyuan3D to Claude Code. VERIFIED: https://github.com/ahujasid/blender-mcp/wiki . Its execute-Python tool is powerful, so save your work before using it.

---

## B. Characters, Rigging, Motion

### Mixamo (Adobe)
- **Status:** still free with an Adobe ID as of Sept 2026, but unmaintained. There was a multi-day outage in June 2025 and no announced end-of-life. It is not available to Enterprise/Federated IDs or China accounts. The official Blender add-on was built for Blender 3.6. A community fork supports Blender 4.2–5.4. SECONDARY: https://app.cinevva.com/guides/mixamo-to-blender-2026 , https://app.cinevva.com/guides/free-character-animations-rigging
- **License:** characters and animations are royalty-free for commercial projects. You may not redistribute raw files. VERIFIED (Adobe community FAQ): https://community.adobe.com/t5/mixamo-discussions/mixamo-faq-licensing-royalties-ownership-eula-and-tos/m-p/13234775
- **API:** no official API (INFERENCE; the web UI only. Unofficial scripts exist, but they are fragile and may breach the ToS).
- **Verdict:** **Use it, but don't depend on it.** It is the free humanoid auto-rig and motion library, but it is a single point of failure. Keep a local copy of the clips you need and a fallback (AccuRIG, UniRig, Rigify).

### Ready Player Me
- **Status:** **shut down.** Netflix acquired it in late 2025. Public services, the API and SDKs ended on Jan 31, 2026, and avatars can no longer be exported. VERIFIED: https://www.pocketgamer.biz/netflix-acquires-avatar-creation-platform-ready-player-me , https://en.wikipedia.org/wiki/Ready_Player_Me , https://genies.com/blog/ready-player-me-shutdown
- **Verdict:** **Skip. It no longer exists.**

### Meshy / Tripo auto-rigging
- Meshy auto-rigs humanoids and quadrupeds and offers 500+ presets. It works best with a clean T-pose or A-pose. VERIFIED: https://docs.meshy.ai/en/webapp/guides/3d-model/rigging
- Tripo's rigging is good for humanoids and weak on unusual limb counts. Both bill rigging and animation as separate credit tasks. SECONDARY.
- **Verdict:** convenient for background extras. For main characters, use a Blender rig (Rigify, or Auto-Rig Pro, a paid add-on) for control and consistency.

### AccuRIG 2 (Reallusion)
- **What it does:** free standalone auto-rigger (v2.0 released July 2025). It exports FBX/USD with presets for Blender, Unreal and Unity. It needs a free ActorCore account to export. ActorCore motions can only be used inside AccuRIG, and most of them are paid (32 are free). VERIFIED: https://www.cgchannel.com/2025/07/rig-and-animate-3d-characters-for-free-with-accurig-2-0/
- **License:** forum guidance says rigging your own meshes for commercial use is fine, and that restrictions apply to Reallusion content. I did not read the EULA text. SECONDARY: https://forum.reallusion.com/PrintTopic522024.aspx
- **Verdict:** **Useful free fallback to Mixamo** for humanoid rigging. It is GUI-only and hard to automate (INFERENCE).

### UniRig (open source, VAST-AI and Tsinghua)
- SIGGRAPH 2025 auto-rigging (skeleton and skinning). Reported as MIT or permissive. Its checkpoints were being released in stages. Needs an NVIDIA GPU. SECONDARY: https://github.com/VAST-AI-Research/UniRig
- **Verdict:** **Worth testing** as a scriptable, local auto-rigger for a Python pipeline. Check the current LICENSE and checkpoint availability first.

### Rokoko Vision / Rokoko Video
- **What it does:** browser-based AI mocap from single- or dual-camera video. VERIFIED (2023 launch): https://www.cgchannel.com/2023/09/check-out-free-browser-based-ai-mocap-tool-rokoko-vision/
- **Pricing:** free single-camera capture (one listing says clips are capped at 15 s). Studio software runs from about $10/mo (Basic) to $50/mo (Pro), and Pro includes a 3,000 s/mo Vision quota. SECONDARY: https://rokoko.com/pricing/ , https://www.rokoko.com/ja/pricing
- **License:** Rokoko's pricing page says library motions can be used commercially. A secondary listing says Video-to-Motion output is commercial-OK, but I did not confirm this in the ToS.
- **Verdict:** **Good free way to perform your own motions** with a phone. There is no public API, so it is a manual step.

### DeepMotion (Animate 3D)
- Free plan: 60 s of animation per month, 20 s per clip, **personal/non-commercial only**. Paid plans start around $9–17/mo (prices conflict). The API is available for high-volume users or on request. SECONDARY: https://toolradar.com/tools/deepmotion/pricing , https://www.itechguides.com/compare/deepmotion-animate-3d-vs-plask-motion/
- **Verdict:** **Optional paid tier** if you need video-to-mocap with an API. The free tier is unusable commercially.

### Move AI (Move One / Move Pro)
- Free plan has 30 one-time credits (1 credit = 1 person for 1 second). The help pages conflict: Starter is $15/mo with 180 credits or $18/mo with 60 credits. Teams is $75/user/mo. Gen-2 costs 12 credits/s versus 6 for Gen-1. VERIFIED (help center, but inconsistent): https://help.move.ai/en/articles/8851451-move-one-pricing , https://docs.move.ai/knowledge/move-ai-pricing-plans-credits
- **Verdict:** **Highest quality markerless mocap,** but expensive per second. Use it only for the higher-quality tier.

### Plask
- Still operating as of Oct 2026. Free plan has 15 s of capture per day. Paid plans are about $18–40/mo (prices conflict). A Sept 2026 review reported an "Error running AI motion capture" outage. SECONDARY: https://plask.ai/pricing , https://umatechnology.org/platforms/plask-motion/
- **Verdict:** **Skip or keep as a low priority.** It is less reliable than Rokoko or Move.

### Text-to-motion research models
- **MDM, MoMask, MotionGPT:** the code is MIT. **But** they train on HumanML3D/AMASS (AMASS is "free for non-commercial scientific research, education or artistic projects") and output SMPL bodies, and the SMPL model license is also non-commercial unless you buy a commercial license. So **commercial use of their outputs is legally murky.** SECONDARY: https://huggingface.co/spaces/MeYourHint/MoMask/blob/609f3a501f2b67fb4dd7c97acb19c24bc54b5392/README.md , https://uthana.com/resources/human-motion-datasets
- **HY-Motion 1.0 (Tencent, Dec 2025):** a 1B-parameter flow-matching text-to-motion model with SMPL-H 22-joint output and no hands. It uses Tencent's own HY-Motion 1.0 community license: free commercial use except for platforms over 100M MAU (per Japanese press). VERIFIED for the paper: https://arxiv.org/html/2512.23464v1 ; license SECONDARY: https://cgworld.jp/flashnews/01-202601-HY-Motion.html . **Check whether the license carries the usual Hunyuan EU/UK/South Korea exclusion** (INFERENCE: likely, given the other Hunyuan licenses).
- **Verdict:** HY-Motion is the most promising text-to-motion option to script from Python. You need to retarget SMPL-H to your rig in Blender. The academic models (MDM, MoMask) are for prototyping only.

### Cascadeur
- Free tier is **non-commercial only**. Indie is $8/mo billed annually, for annual revenue plus funding under $100K. Pro is $33/mo billed annually with unlimited commercial use. VERIFIED: https://cascadeur.com/plans , https://cascadeur.com/education , https://cascadeur.com/blog/general/cascadeurs-new-licensing-structure-comprehensive-faq
- **Verdict:** **Good low-cost polish tool** (physics-assisted keyframing, AI auto-posing). It is manual and GUI-based, so it is not in the automated path. Indie at $8/mo fits the low tier.

---

## C. Textures and Materials

| Source | License | Notes |
|---|---|---|
| Poly Haven | CC0, no attribution | VERIFIED: https://docs.polyhaven.com/en/faq . HDRIs, textures and models. Built into blender-mcp. |
| ambientCG | CC0 | 2,013 materials reachable via its public API (Oct 2026). SECONDARY: https://learnarchitecture.net/?p=40549 . Scriptable downloads fit a Python pipeline. |
| ShareTextures, cgbookcase, 3DTextures.me | CC0 (secondary) | https://app.cinevva.com/guides/free-textures-hdris-materials |
| Adobe Substance 3D (Sampler, Painter) | Subscription | Collection went to $59.99/mo in Mar 2025 (VERIFIED: https://blog.adobe.com/en/publish/2025/02/20/substance-3d-innovations-pricing-updates). Texturing plan is about 25 generative credits/mo, Collection 100. Adobe announced an indie offering, but I found no 2026 indie price. |
| Meshy AI Texturing | Meshy credits (about 5 credits/texture, secondary) | Projects textures onto existing meshes, including your own Blender meshes. |
| ComfyUI + FLUX.2 [klein] 4B / FLUX.1 schnell | Apache 2.0 | VERIFIED: https://github.com/black-forest-labs/flux2/wiki (klein 4B Apache 2.0; klein 9B and FLUX.2 dev are non-commercial). About 8–13 GB VRAM. |
| Ubisoft CHORD (PBR decomposition) | **Research-only license** | VERIFIED: https://blog.comfy.org/p/ubisoft-open-sources-the-chord-model . **Not for commercial output.** |

- **ComfyUI seamless-texture workflow:** generate a tileable albedo with FLUX.2 klein 4B or FLUX.1 schnell (both Apache 2.0) using circular padding or a seamless node. Derive normal, height and roughness with TextureAlchemy nodes (https://github.com/amtarr/ComfyUI-TextureAlchemy) or classic filters. Avoid the CHORD and FLUX.1/FLUX.2 [dev] weights for commercial work. Note on FLUX.1 [dev]: its license says outputs can be used commercially, but running the model commercially needs a BFL license, so that is a grey zone (SECONDARY: https://open.windriver.com/info/uni-license-list/licenses/flux-1-nc.html).
- **Verdict:** **CC0 libraries (Poly Haven, ambientCG) cover about 90% of needs at $0** and are fully scriptable. Add the Apache-licensed FLUX workflow for stylized or custom materials. Substance is only worth it for a hand-texturing artist.

---

## D. AI Video (supplements only)

General limits (INFERENCE, consistent with all reviews): clips are 5–10 s, character identity drifts between shots, there is no frame-accurate camera control, and AI video does not respect your Blender scene's geometry. Best uses: b-roll, establishing shots, and **video-to-video restyling of Blender renders** (Runway Aleph, Luma Modify). Every pass costs money and can break continuity.

| Tool | Status | Price | Notes |
|---|---|---|---|
| Runway | Operating; Gen-4.5, Aleph 2.0 | Standard $15/mo ($12 annual), Pro $35 ($28), Max $76 (replaced Unlimited, 1 Jun 2026). API at $0.01/credit: Gen-4 Turbo $0.05/s, Gen-4.5 $0.12/s, Aleph 2.0 about $0.28/s | SECONDARY: https://eesel.ai/blog/runway-ai-pricing , https://openrouter.ai/runway . Aleph is the strongest video-to-video option for restyling renders. |
| Google Veo 3.1 | Operating (Gemini API, Vertex) | Veo 3.1 $0.40/s (720p/1080p), Fast about $0.10–0.12/s, Lite about $0.05/s (720p); no free API tier | SECONDARY: https://benchlm.ai/media-pricing/veo . Native audio. Outputs carry a SynthID watermark (INFERENCE). |
| OpenAI Sora | **Discontinued.** Announced 24 Mar 2026; app closed about 26 Apr 2026; API (sora-2, sora-2-pro) retired 24 Sep 2026 | n/a | VERIFIED: https://www.axios.com/2026/03/24/openai-discontinue-sora-video-app , https://engadget.com/ai/openai-is-shutting-down-its-sora-video-generation-app-211023358.html . Some reports say Sora 2 may remain inside ChatGPT, which is disputed. **Skip.** |
| Kling (3.0) | Operating | Free about 66 credits/day (watermarked, **non-commercial**); Standard is the first tier with commercial use. API about $0.075–0.17/s via resellers | SECONDARY: https://eesel.ai/blog/kling-ai-pricing , https://crepal.ai/blog/aivideo/is-kling-ai-free-pricing/ . Free-tier clips may not become commercial after you upgrade. |
| Luma Dream Machine (Ray3 / Ray3.14) | Operating | Plus about $24–30/mo, with commercial use only on paid plans and only while subscribed; free is watermarked | SECONDARY: https://magichour.ai/blog/luma-dream-machine-pricing . Ray3 "Modify" restyles real footage. |
| Pika (2.5) | Operating; plans reshuffled several times in 2026 | Starter about $8/mo annual (commercial license added Oct 2026), Creator about $28; free tier now 0 credits | SECONDARY: https://www.usagepricing.com/blueprint/activity/pika-labs-2026-10-23-starter-commercial-license . Social effects, weak control. **Skip.** |

**Platform AI-label implications (YouTube):**
- The "altered or synthetic content" disclosure is required for **realistic** content that could be mistaken for a real person, place or event. Clearly animated or stylized content usually only gets a label in the expanded description. Photorealistic AI content gets a label below the player, and YouTube may add a label creators cannot remove if they don't disclose. SECONDARY: https://minimatters.com/youtube-ai-content-labeling-update-in-may-2026/ , https://blog.google/intl/en-in/products/platforms/how-were-helping-creators-disclose-altered-or-synthetic-content/
- **The bigger risk for a faceless studio is the YPP "inauthentic content" policy.** "Repetitious content" was renamed to inauthentic content on 15 July 2025, with an enforcement wave in Jan 2026. It targets mass-produced, templated uploads, whether or not they use AI. SECONDARY: https://eliro.pro/blog/youtube-ai-content-policy-faceless-creators-2026 . Mitigation (INFERENCE): give each episode a distinct story and real editorial value, keep human creative direction, and don't upload many near-identical variants.
- Realistic AI voices of real people and realistic AI video both raise disclosure risk. Stylized Blender animation with a synthetic narrator is low risk for labelling. Disclose AI voice if it could be mistaken for a real person.

---

## E. Voice / TTS

| Tool | License / terms | Price | Commercial on free? | Local HW |
|---|---|---|---|---|
| ElevenLabs | Proprietary SaaS | Free about 10K credits/mo; Starter $5–6/mo (about 30K credits, commercial license); Creator $22/mo (about 100–121K); Pro $99/mo (about 500–600K) | **No.** Free is non-commercial and requires attribution | n/a |
| OpenAI TTS | API ToS | tts-1 $15/1M chars, tts-1-hd $30/1M; gpt-4o-mini-tts $0.60/1M text-in + $12/1M audio-out (about $0.015/min) | Paid API, commercial OK | n/a |
| Azure Neural TTS | API ToS | about $15–16/1M chars standard neural, Neural HD $22/1M; 500K chars/mo free | Yes (paid) | n/a |
| Google Cloud TTS | API ToS | Chirp 3 HD about $30/1M chars; free-tier amount conflicts | Yes (paid) | n/a |
| Kokoro-82M | **Apache 2.0** | Free | Yes | CPU-capable; tiny GPU |
| Piper | Code: rhasspy/piper MIT (archived); current OHF-Voice/piper1-gpl is **GPL-3.0** (embeds eSpeak NG GPL) | Free | Yes for generated audio (INFERENCE: GPL governs the code, not the audio); check each voice's model-card license | CPU / Raspberry Pi |
| Chatterbox (Resemble; Original, Multilingual 23+ langs, Turbo English-only 350M) | **MIT**; every output carries an inaudible PerTh watermark | Free | Yes | GPU recommended (INFERENCE about 6–8 GB) |
| F5-TTS | Code MIT; **weights CC-BY-NC-4.0** (Emilia data) | Free | **No** | GPU |
| XTTS-v2 (Coqui) | **CPML, non-commercial**; Coqui shut down around Dec 2023/Jan 2024, so a commercial license can no longer be bought | Free | **No** | GPU |
| Fish Speech / OpenAudio S1-mini | Weights widely reported as **CC-BY-NC-SA-4.0**; the official LICENSE has a research/non-commercial tier plus a revenue-capped community commercial license; flagship S1/S2 are hosted-only | API paid | **No** (without an agreement) | GPU |

Sources:
- ElevenLabs: SECONDARY https://bigvu.tv/blog/elevenlabs-pricing-2026-plans-credits-commercial-rights-api-costs/ ; official pricing page https://www.elevenlabs.io/pricing (not readable here).
- OpenAI: SECONDARY https://costgoat.com/pricing/openai-tts , https://www.s-anand.net/blog/openai-tts-cost/ . INFERENCE: OpenAI's usage policies require you to tell listeners the voice is AI-generated.
- Azure: SECONDARY https://perkstack.co/blog/cheapest-azure-tts-api . Google: https://cloud.google.com/text-to-speech/pricing
- Kokoro and Piper: SECONDARY https://github.com/captivus/Kokoro-82M , https://www.promptquorum.com/power-local-llm/piper-vs-kokoro-tts
- Chatterbox: VERIFIED https://resemble.ai/chatterbox
- F5-TTS: VERIFIED https://huggingface.co/SWivid/F5-TTS/commit/346ef6cee7235a7d1039b30dc7d3edc77d59bd45
- XTTS: VERIFIED https://huggingface.co/coqui/XTTS-v2/discussions/65
- Fish: VERIFIED https://github.com/fishaudio/fish-speech/blob/main/LICENSE

**Verdict:** **$0 tier: Kokoro (narration) plus Chatterbox (expressive voices and cloning your own voice).** Both are permissive and run locally. Low tier: ElevenLabs Starter or Creator for the best quality. **Skip XTTS, F5-TTS and Fish/OpenAudio open weights for commercial work.**

---

## F. Sound Effects and Music

| Source | License | Commercial? |
|---|---|---|
| ElevenLabs Sound Effects | Paid plans (Starter+) | Yes on paid; free needs attribution and is non-commercial. Help center: 40 credits/s when you set the duration, max 30 s (other pages say 200 credits/generation). VERIFIED: https://help.elevenlabs.io/hc/en-us/articles/25735337678481 |
| Eleven Music | Paid plans | "Cleared for nearly all commercial uses" (film/TV, podcasts, social, ads, games); about 900 credits/min. SECONDARY: https://www.elevenlabs.io/pricing |
| Stable Audio Open 1.0 | Stability Community License | Yes if org revenue under $1M/yr. VERIFIED: https://huggingface.co/stabilityai/stable-audio-open-1.0 . Best at short SFX and textures, weak at music (INFERENCE). |
| AudioCraft (MusicGen, AudioGen) | Code MIT; **weights CC-BY-NC 4.0** | **No.** VERIFIED: https://github.com/nusic-fm/audiocraft/blob/main/README.md (mirror of the official README) |
| MMAudio (video-to-audio Foley) | Code MIT; official weight license **unclear** (a third-party repackage is tagged CC-BY-NC; it depends on Apple DFN5B CLIP, which has a research license) | **Treat as non-commercial** until confirmed. https://huggingface.co/hkchengrex/MMAudio/tree/main |
| Freesound | Per file: CC0, CC BY, CC BY-NC (plus legacy Sampling+) | CC0 yes; CC BY yes with credit; CC BY-NC no. Filter search by license. https://en.wikipedia.org/wiki/Freesound |
| Sonniss GDC bundles (2015–2026) | Royalty-free, no attribution, unlimited projects; no resale of raw SFX; **no AI/ML training** (2024+) | Yes. SECONDARY: https://rekkerd.org/sonniss-releases-gdc-2026-game-audio-bundle/ , https://gamefromscratch.com/sonniss-27-5gb-sound-effect-giveaway-at-gdc-2024/ . 200 GB+ archive. |
| Pixabay audio | Pixabay Content License | Commercial OK with no attribution, **but some tracks are registered in Content ID by their composers**, so claims happen. Keep the license certificate for disputes. SECONDARY: https://quasa.io/fr/media/musique-gratuite-sur-youtube-pixabay-peut-declencher-une-reclamation |
| BBC Sound Effects | RemArc licence: personal, education and research only | **No commercial use.** Commercial licensing goes through Pro Sound Effects. VERIFIED: https://mixmag.net/read/bbc-sound-effect-archive-free-audio-samples-news |

**Content ID risk:** Content ID matches audio fingerprints regardless of who or what made the track. Popular "free" music from Pixabay, YouTube-favourite NCS-style tracks, and some AI-music services whose outputs were registered in Content ID can all cause claims that divert revenue. SECONDARY: https://hellothematic.com/ai-music-for-youtube/ . Mitigations (INFERENCE):
- Use the YouTube Audio Library.
- Use music you generate yourself with clear commercial rights (Eleven Music on a paid plan).
- Use a subscription library that whitelists your channel (Epidemic, Artlist; not researched here).
- Keep a per-asset license log.

**Verdict:** **$0 tier: Sonniss GDC archive plus CC0 Freesound for SFX; Stable Audio Open for custom SFX** (if revenue is under $1M); YouTube Audio Library for music. **Skip AudioCraft, MMAudio (until its license is clear) and BBC SFX for monetized output.**

---

## G. LLMs for Scripting and Storyboarding

**Claude API pricing per 1M tokens, input/output.** From the Claude API skill's model table (cached 2026-10-06), matching https://www.anthropic.com/pricing :

| Model | Input | Output |
|---|---|---|
| Claude Fable 5.1 / Fable 5 (most capable) | $10 | $50 |
| Claude Opus 5.5 (current Opus) | $4 | $20 |
| Claude Opus 5 / 4.8 / 4.7 / 4.6 | $5 | $25 |
| Claude Sonnet 5.5 / Sonnet 5 | $2 | $10 |
| Claude Sonnet 4.6 | $3 | $15 |
| Claude Haiku 5.5 | $0.10 | $0.50 (up to 100K-token prompts) |
| Claude Haiku 4.5 | $1 | $5 |

- Batch API is about 50% off. Prompt-cache reads are about 90% off; for Opus 5.5 and Sonnet 5.5, cache reads are $0.20/MTok.
- **Subscriptions** (SECONDARY, consistent across sources: https://www.superblocks.com/blog/claude-code-pricing , https://pricepertoken.com/subscriptions/claude):
  - Pro $20/mo (about $17 annual)
  - Max 5x $100/mo
  - Max 20x $200/mo
  - Claude Code is included from Pro up. Usage is shared with chat, with a 5-hour rolling window plus weekly caps. Sources report Claude Code's 5-hour limits were doubled in May 2026 (unconfirmed by Anthropic here).
- **Cost logic (INFERENCE):**
  - An interactive Claude Code session that writes Blender/bpy code, pipeline glue and scripts is far cheaper on a subscription than on API tokens. Pro at $20 is enough to start; Max 5x is for daily heavy agentic use.
  - Use the **API** for unattended batch jobs such as nightly script generation, shot lists and metadata. With Sonnet 5.5 or Haiku 5.5 plus batch and caching, a 1,500-word script plus a JSON storyboard costs cents per episode.
- **Local LLMs needed?** **No** for quality scripting. They are only worth it for offline or high-volume trivial tasks such as tagging or captions cleanup, or if you need zero marginal cost. In that case, a 7–14B open model (Qwen, Llama class; INFERENCE) runs on a 12–16 GB GPU, which competes with Blender, TRELLIS and TTS for VRAM. Recommendation: no local LLM at first.

---

## H. Captions

| Tool | License | Word timestamps | Notes |
|---|---|---|---|
| OpenAI Whisper (incl. large-v3-turbo, Oct 2024) | MIT (code and weights) | `word_timestamps=True` gives cross-attention-based timings that are approximate (INFERENCE) | SECONDARY: https://vantaige.io/ai-tool/whisper |
| faster-whisper (CTranslate2) | MIT | Yes (`word_timestamps=True`); about 4x faster, int8 on CPU or GPU | SECONDARY: https://brasstranscripts.com/licenses |
| whisperX | BSD (PyPI says BSD-2-Clause, another source says BSD-4) | **Most accurate word-level timing** (wav2vec2 forced alignment) and VAD batching | https://depscope.dev/pkg/pypi/whisperx . Optional pyannote diarization: code MIT, gated HF models need you to accept their terms. |

- **Pipeline note (INFERENCE):** you already have the script text. Forced alignment of the known script against the TTS audio gives perfect captions. Use whisperX's alignment model or aeneas. Many TTS engines also return timings: ElevenLabs and Azure return word or character timestamps.
- **Verdict:** **whisperX (or faster-whisper) at $0** for burned-in, word-by-word captions and .srt/.vtt. Feed them into Blender's VSE text strips or ffmpeg.

---

## Ranked Recommendation

### (1) $0 tier (open source and CC0, local GPU 12–24 GB)
1. **Claude Code on Pro ($20)** is the one unavoidable cost for the "Claude Code" orchestrator. Otherwise use free Claude.ai for planning only.
2. **3D:** TRELLIS.2 (MIT). Add Hunyuan3D 2.1 only if you are outside the EU/UK/South Korea. Stable Fast 3D on low-VRAM machines. Remesh with Blender Quadriflow.
3. **Rigging and motion:** Mixamo (keep local copies), AccuRIG 2, UniRig (test it), Rokoko Vision free (self-performed mocap), HY-Motion 1.0 (check the license). Rigify for hero characters.
4. **Materials:** Poly Haven and ambientCG (CC0, scriptable). FLUX.2 klein 4B or FLUX.1 schnell (Apache 2.0) in ComfyUI for custom tiles.
5. **Voice:** Kokoro-82M plus Chatterbox (MIT).
6. **SFX and music:** Sonniss GDC archive, Freesound CC0, Stable Audio Open (under $1M revenue), YouTube Audio Library.
7. **Captions:** whisperX or faster-whisper.
8. Glue it together with **blender-mcp**, which gives Claude Code control of Blender and access to Poly Haven and Hunyuan.

### (2) Low-cost tier (under $50/mo)
- Claude Pro $20
- Meshy Pro $20 **or** Tripo Pro about $20 (generation, texture, auto-rig, Smart Mesh)
- ElevenLabs Starter $5–6 (commercial TTS, SFX and music)
- Cascadeur Indie $8 (annual billing)

That totals about $53–54. Drop Cascadeur or use ElevenLabs Starter instead of Creator to stay under $50. An alternative is to swap Meshy for API pay-as-you-go (Tripo API at $0.01/credit) for scripted generation.

### (3) Higher-quality tier (about $150–400/mo)
- Claude Max 5x ($100), plus the API for batch jobs on Sonnet 5.5 or Opus 5.5
- Rodin Business ($96–120, API, quad and 4K) or Meshy Studio ($60)
- ElevenLabs Creator ($22) or Pro ($99)
- Move One (markerless mocap)
- Runway Pro or Max ($35–76) for Aleph restyle passes and b-roll, or Veo 3.1 Fast via the API ($0.10–0.12/s)
- Cascadeur Pro ($33)
- A licensed music library

### Skip, and why
- **Ready Player Me:** shut down on 31 Jan 2026.
- **OpenAI Sora:** app and API discontinued (API retired 24 Sep 2026).
- **XTTS-v2, F5-TTS, Fish/OpenAudio open weights, AudioCraft (MusicGen/AudioGen), CHORD, FLUX dev weights, BBC SFX:** non-commercial or research-only licenses.
- **MMAudio:** weight license unclear and depends on research-licensed CLIP. Skip until clarified.
- **MDM, MoMask, MotionGPT** for shipped content: their AMASS and SMPL data and body-model licenses are non-commercial.
- **Hunyuan3D, HY-Motion** if you operate in or distribute to the EU, UK or South Korea (territory exclusion).
- **Luma Genie and CSM:** de-prioritized or uncertain status, no advantage.
- **Plask:** reliability issues. **Pika:** weak control and churning plans.
- **DeepMotion, Kling, Luma** free tiers: non-commercial or watermarked. Only their paid tiers are usable.
- **Free tiers of Meshy and Tripo** for shipped assets: CC BY attribution, public assets, and for Tripo reportedly non-commercial.
- **Pixabay or "free" popular music** on monetized channels: Content ID claim risk.
