"""Build one shot from a shot-spec YAML and render it with EEVEE.

Run through the studio runner (python -m studio.render_shot), or directly:
    .venv/bin/python blender/build_shot.py --spec shots/proto/s01.yaml --profile preview --out output/proto/s01/preview
"""
import argparse
import json
import math
import os
import platform
import resource
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bpy  # noqa: E402
import yaml  # noqa: E402

from scenekit import actors, beach, camera, characters, effects, geo, render, street, style  # noqa: E402

KITS = {"beach": beach, "street": street}


def peak_mb():
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return round(rss / (1024 * 1024) if platform.system() == "Darwin" else rss / 1024)


def add_walkers(spec, scene, kit, f_start, f_end):
    coll = kit["root"]
    rng = kit["rng"]
    dur = (f_end - f_start) / render.FPS
    for i, h in enumerate(spec.get("walkers", [])):
        (x0, y0), (x1, y1) = h["from"], h["to"]
        vx, vy = (x1 - x0) / dur, (y1 - y0) / dur
        e = characters.place(f"walker{i}", coll, kit["variants"]["walk"][i % 4], (x0, y0, 0),
                             math.atan2(vy, vx) + math.pi / 2, rng)
        geo.drive(e, "location", f"{x0}+(frame-{f_start})*{vx / render.FPS:.5f}", 0)
        geo.drive(e, "location", f"{y0}+(frame-{f_start})*{vy / render.FPS:.5f}", 1)


def apply_effects(shot, kit, acts, cam, coll):
    booms = []
    for i, fx in enumerate(shot.get("effects", [])):
        t = fx["type"]
        name = f"fx{i}_{t}"
        if t == "ring":
            effects.ring(coll, name, fx["at"], fx["origin"], fx["speed"], fx["max_r"], fx.get("collapse_at"),
                         ground=fx.get("ground"))
        elif t == "ring_field":
            effects.ring_field(coll, name, fx["at"], fx["count"], fx["area"], fx["speed"], fx["max_r"],
                               fx.get("spread", 2.0), seed=i * 101 + 7, collapse_at=fx.get("collapse_at"))
        elif t == "cone":
            a = acts[fx["attach"]]
            parent = a["obj"]
            if a["kind"] == "person":
                apex, local_rot = (0, -0.35, 0.95), -math.pi / 2
            elif a["kind"] == "truck":
                apex, local_rot = (3.3, 0, 1.6), 0.0
            else:
                apex, local_rot = (2.4, 0, 0.8), 0.0
            effects.mach_cone(coll, name, parent, a["speed_ms"], length=fx.get("length", 9.0), apex=apex,
                              local_rot_z=local_rot, start=fx.get("from", a["start"] or None))
        elif t == "boom":
            effects.boom(coll, name, fx["at"], fx["pos"], fx.get("strength", 1.0))
            booms.append((fx["at"], fx.get("strength", 1.0)))
        elif t == "flip_umbrellas":
            effects.flip(kit.get("umbrellas", []), fx["at"], fx.get("center", (0, 0)), fx.get("radius", 20))
        elif t == "crowd_jump":
            effects.crowd_jump(kit.get("crowd", []), fx["at"])
        else:
            raise ValueError(f"unknown effect {t}")
    effects.camera_kick(cam, booms)


def export_callouts(scene, cam, spec, acts, out_dir):
    """Screen positions (0-1, origin bottom-left) of labelled actors for every frame, for 2D callouts."""
    from bpy_extras.object_utils import world_to_camera_view
    from mathutils import Vector
    labelled = [a for a in spec.get("actors", []) if a.get("label")]
    if not labelled:
        return
    data = {}
    for a in labelled:
        data[a["id"]] = {"label": a["label"], "frames": []}
    for fr in range(scene.frame_start, scene.frame_end + 1):
        scene.frame_set(fr)
        for a in labelled:
            o = acts[a["id"]]["obj"]
            top = o.matrix_world @ Vector((0, 0, 1.75 + a.get("label_height", 0.25)))
            v = world_to_camera_view(scene, cam, top)
            data[a["id"]]["frames"].append([fr, round(v.x, 4), round(v.y, 4), int(v.z > 0 and 0 <= v.x <= 1 and 0 <= v.y <= 1)])
    scene.frame_set(scene.frame_start)
    with open(os.path.join(out_dir, "callouts.json"), "w") as fh:
        json.dump(data, fh)


def clear_camera_path(kit, cam_spec, actor_objs, radius=7.0):
    """Hide set dressing and extras within `radius` metres (horizontally) of the camera path so nothing
    random blocks the lens. Scripted actors are never hidden."""
    pts = [p for p in (cam_spec.get("from"), cam_spec.get("to")) if p]
    if cam_spec.get("move") == "orbit":
        cx, cy, _ = cam_spec["center"]
        r = cam_spec["radius"]
        pts += [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
                for a in range(int(cam_spec["start_deg"]), int(cam_spec["end_deg"]) + 1, 5)]
    if not pts:
        return 0
    keep = set(actor_objs)
    hidden = 0
    for o in kit["root"].objects:
        if o in keep or o.type == "LIGHT":
            continue
        if o.dimensions.length > 30:  # ground, sea, buildings: never hide
            continue
        for p in pts:
            if (o.location.x - p[0]) ** 2 + (o.location.y - p[1]) ** 2 < radius ** 2:
                o.hide_render = True
                hidden += 1
                break
    return hidden


def load_shot(args):
    """Return (shot_spec, set_spec). Supports a whole-video YAML (--video + --shot) or a single shot file."""
    if args.video:
        video = yaml.safe_load(open(args.video))
        shot = next(s for s in video["shots"] if s["id"] == args.shot)
        set_spec = dict(video["sets"][shot["set"]])
        if "sun" in shot:
            set_spec["sun"] = shot["sun"]
        return shot, set_spec
    spec = yaml.safe_load(open(args.spec))
    return spec, spec["set"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec")
    ap.add_argument("--video", help="video YAML containing all shots")
    ap.add_argument("--shot", help="shot id inside --video")
    ap.add_argument("--profile", default="preview")
    ap.add_argument("--out", required=True)
    ap.add_argument("--still", type=int, nargs="*", help="render only these frames (stills)")
    ap.add_argument("--save-blend", action="store_true")
    ap.add_argument("--frames", type=int, help="render only the first N frames (benchmarks)")
    args = ap.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:])

    t0 = time.time()
    spec, set_spec = load_shot(args)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    style.apply_color_management(scene)

    f_start = 1
    f_end = f_start + round(spec["duration"] * render.FPS) - 1
    scene.frame_start, scene.frame_end = f_start, f_end

    kit = KITS[set_spec["kit"]].build(set_spec, scene)
    add_walkers(spec, scene, kit, f_start, f_end)
    shot_coll = geo.new_collection("SHOT")
    acts = actors.build(spec.get("actors"), kit, shot_coll)
    cam, _ = camera.build(spec["camera"], scene, shot_coll, f_start, f_end, acts)
    apply_effects(spec, kit, acts, cam, shot_coll)
    clear_camera_path(kit, spec["camera"], [a["obj"] for a in acts.values()])
    os.makedirs(args.out, exist_ok=True)
    export_callouts(scene, cam, spec, acts, args.out)
    if args.frames:
        scene.frame_end = min(f_end, f_start + args.frames - 1)

    os.makedirs(args.out, exist_ok=True)
    render.configure(scene, args.profile, os.path.join(os.path.abspath(args.out), "frame_####"))
    if args.save_blend:
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(os.path.abspath(args.out), "shot.blend"))
    t_build = time.time() - t0

    # Per-frame timing. The first frame includes one-time shader compilation, so the
    # steady-state speed (used for estimates) excludes it.
    times = []
    marks = {}
    bpy.app.handlers.render_pre.append(lambda *_: marks.__setitem__("t", time.time()))
    bpy.app.handlers.render_post.append(lambda *_: times.append(time.time() - marks["t"]))

    t1 = time.time()
    if args.still:
        for f in args.still:
            scene.frame_set(f)
            scene.render.filepath = os.path.join(os.path.abspath(args.out), f"still_{f:04d}.png")
            bpy.ops.render.render(write_still=True)
    else:
        bpy.ops.render.render(animation=True)
    t_render = time.time() - t1
    frames = len(times)
    steady = times[1:] or times

    report = {
        "spec": args.video or args.spec, "shot": spec.get("id"), "profile": args.profile, "frames": frames,
        "resolution": list(render.PROFILES[args.profile]["res"]),
        "build_s": round(t_build, 1), "render_s": round(t_render, 1),
        "s_per_frame": round(t_render / max(frames, 1), 2),
        "first_frame_s": round(times[0], 2) if times else None,
        "steady_s_per_frame": round(sum(steady) / len(steady), 2) if steady else None,
        "slowest_frame_s": round(max(times), 2) if times else None,
        "last5_s_per_frame": round(sum(times[-5:]) / len(times[-5:]), 2) if times else None,
        "peak_mem_mb": peak_mb(),
        "objects": len(bpy.data.objects), "blender": bpy.app.version_string,
        "machine": f"{platform.system()} {platform.machine()}",
    }
    with open(os.path.join(args.out, "render_report.json"), "w") as fh:
        json.dump(report, fh, indent=2)
    print("RENDER_REPORT " + json.dumps(report))


if __name__ == "__main__":
    main()
