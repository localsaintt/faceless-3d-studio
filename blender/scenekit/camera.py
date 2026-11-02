"""Camera-move library: storyboard words -> keyframed camera + look-at target.

Every move eases in and out (Bezier keys), tracks a moving target, adds subtle handheld
drift, and uses shallow depth of field for the "miniature diorama" look.
"""
import bpy

from . import geo


def _key(obj, path, frames_values):
    for f, v in frames_values:
        setattr(obj, path, v)
        obj.keyframe_insert(path, frame=f)


def build(spec, scene, coll, f_start, f_end):
    data = bpy.data.cameras.new("Cam")
    data.lens = spec.get("lens", 32)
    data.sensor_fit = "VERTICAL"
    data.sensor_height = 24 * 16 / 9 / 1.5  # ~28.4 mm: wide-ish vertical framing
    data.clip_end = 1000
    cam = bpy.data.objects.new("Cam", data)
    coll.objects.link(cam)
    tgt = geo.empty("CamTarget", coll, kind="SPHERE")
    scene.camera = cam

    move = spec.get("move", "dolly_push")
    a, b = spec["from"], spec.get("to", spec["from"])
    ta, tb = spec["target_from"], spec.get("target_to", spec["target_from"])
    if move in ("dolly_push", "crane_up", "track", "static", "pull_back"):
        _key(cam, "location", [(f_start, a), (f_end, b)])
        _key(tgt, "location", [(f_start, ta), (f_end, tb)])
    elif move == "orbit":
        import math
        cx, cy, cz = spec["center"]
        r, h = spec["radius"], spec["height"]
        a0, a1 = math.radians(spec["start_deg"]), math.radians(spec["end_deg"])
        steps = 8
        for i in range(steps + 1):
            t = i / steps
            ang = a0 + (a1 - a0) * t
            f = f_start + (f_end - f_start) * t
            cam.location = (cx + r * math.cos(ang), cy + r * math.sin(ang), cz + h)
            cam.keyframe_insert("location", frame=f)
        _key(tgt, "location", [(f_start, (cx, cy, cz + spec.get("look_height", 1.0)))])
    else:
        raise ValueError(f"unknown camera move {move}")

    c = cam.constraints.new("TRACK_TO")
    c.target = tgt
    c.track_axis = "TRACK_NEGATIVE_Z"
    c.up_axis = "UP_Y"

    shake = spec.get("shake", 0.015)
    if shake:
        for i, (f1, f2, ph) in enumerate([(0.071, 0.137, 0.0), (0.053, 0.161, 1.7), (0.089, 0.113, 3.1)]):
            geo.drive(cam, "delta_location",
                      f"{shake:.4f}*(sin(frame*{f1}+{ph})+0.6*sin(frame*{f2}+{ph * 2}))", i)

    dof = spec.get("fstop")
    if dof:
        data.dof.use_dof = True
        data.dof.focus_object = tgt
        data.dof.aperture_fstop = dof
    return cam, tgt
