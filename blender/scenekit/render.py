"""Render profiles tuned for an Apple M2 / 8 GB (approved "option 1" efficiency plan)."""
PROFILES = {
    # cloud-container smoke tests only (software GL): tiny frames, every 4th frame
    "draft": {"res": (270, 480), "samples": 4, "frame_step": 4, "shadow_rays": 1, "shadow_steps": 2,
              "raytracing": False},
    # quick look: quarter-area frames, every other frame
    "preview": {"res": (540, 960), "samples": 8, "frame_step": 2, "shadow_rays": 1, "shadow_steps": 4,
                "raytracing": False},
    # final delivery
    "final": {"res": (1080, 1920), "samples": 24, "frame_step": 1, "shadow_rays": 1, "shadow_steps": 6,
              "raytracing": False},
    # A/B candidate: render at 720x1280, upscale to 1080x1920 in assembly
    "final_720": {"res": (720, 1280), "samples": 24, "frame_step": 1, "shadow_rays": 1, "shadow_steps": 6,
                  "raytracing": False},
}
FPS = 24


def configure(scene, profile_name, out_pattern):
    p = PROFILES[profile_name]
    r = scene.render
    r.engine = "BLENDER_EEVEE"
    r.resolution_x, r.resolution_y = p["res"]
    r.resolution_percentage = 100
    r.fps = FPS
    scene.frame_step = p["frame_step"]
    e = scene.eevee
    e.taa_render_samples = p["samples"]
    e.use_raytracing = p["raytracing"]
    e.use_shadows = True
    e.shadow_ray_count = p["shadow_rays"]
    e.shadow_step_count = p["shadow_steps"]
    r.image_settings.file_format = "PNG"
    r.image_settings.color_mode = "RGB"
    r.image_settings.compression = 15
    r.filepath = out_pattern
    r.use_overwrite = False     # resume after a crash instead of starting over
    r.use_placeholder = True
    return p
