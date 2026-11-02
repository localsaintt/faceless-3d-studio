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

from scenekit import beach, camera, characters, geo, render, style  # noqa: E402

KITS = {"beach": beach}


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--profile", default="preview")
    ap.add_argument("--out", required=True)
    ap.add_argument("--still", type=int, nargs="*", help="render only these frames (stills)")
    ap.add_argument("--save-blend", action="store_true")
    args = ap.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:])

    t0 = time.time()
    spec = yaml.safe_load(open(args.spec))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    style.apply_color_management(scene)

    f_start = 1
    f_end = f_start + round(spec["duration"] * render.FPS) - 1
    scene.frame_start, scene.frame_end = f_start, f_end

    kit = KITS[spec["set"]["kit"]].build(spec["set"], scene)
    add_walkers(spec, scene, kit, f_start, f_end)
    shot_coll = geo.new_collection("SHOT")
    camera.build(spec["camera"], scene, shot_coll, f_start, f_end)

    os.makedirs(args.out, exist_ok=True)
    render.configure(scene, args.profile, os.path.join(os.path.abspath(args.out), "frame_####"))
    if args.save_blend:
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(os.path.abspath(args.out), "shot.blend"))
    t_build = time.time() - t0

    t1 = time.time()
    frames = 0
    if args.still:
        for f in args.still:
            scene.frame_set(f)
            scene.render.filepath = os.path.join(os.path.abspath(args.out), f"still_{f:04d}.png")
            bpy.ops.render.render(write_still=True)
            frames += 1
    else:
        bpy.ops.render.render(animation=True)
        frames = len(range(f_start, f_end + 1, scene.frame_step))
    t_render = time.time() - t1

    report = {
        "spec": args.spec, "profile": args.profile, "frames": frames,
        "resolution": list(render.PROFILES[args.profile]["res"]),
        "build_s": round(t_build, 1), "render_s": round(t_render, 1),
        "s_per_frame": round(t_render / max(frames, 1), 2), "peak_mem_mb": peak_mb(),
        "objects": len(bpy.data.objects), "blender": bpy.app.version_string,
        "machine": f"{platform.system()} {platform.machine()}",
    }
    with open(os.path.join(args.out, "render_report.json"), "w") as fh:
        json.dump(report, fh, indent=2)
    print("RENDER_REPORT " + json.dumps(report))


if __name__ == "__main__":
    main()
