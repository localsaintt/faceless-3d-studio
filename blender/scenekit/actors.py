"""Scripted actors for a shot: people (static, turning or walking), cars and the truck.

Returns {id: {"obj": empty, "kind": ..., "speed_ms": ..., "dir": radians, "start": seconds}} so
effects (e.g. Mach cones) can attach to them.
"""
import math
import random
import zlib

from . import characters, geo
from .effects import FPS, f

MPH = 0.44704


def _rng(actor_id):
    # same actor id -> same colours in every shot (continuity for the kid, the mom, ...)
    return random.Random(zlib.crc32(actor_id.encode()))


def build(specs, kit, coll):
    out = {}
    for a in specs or []:
        kind = a["type"]
        if kind == "person":
            out[a["id"]] = _person(a, kit, coll)
        elif kind in ("car", "truck"):
            out[a["id"]] = _vehicle(a, kit, coll)
        else:
            raise ValueError(f"unknown actor type {kind}")
    return out


def _person(a, kit, coll):
    variants = kit["variants"][a.get("anim", "idle")]
    rng = _rng(a["id"])
    variant = variants[zlib.crc32(a["id"].encode()) % len(variants)]
    x, y, z = (list(a["pos"]) + [0])[:3]
    if "speed_mph" in a:  # walking/jogging in a straight line
        d = math.radians(a.get("dir_deg", 0))
        v = a["speed_mph"] * MPH
        e = characters.place(a["id"], coll, variant, (x, y, z), d + math.pi / 2, rng, a.get("scale", 1.0))
        geo.drive(e, "location", f"{x}+(frame-{f(0)})*{v * math.cos(d) / FPS:.5f}", 0)
        geo.drive(e, "location", f"{y}+(frame-{f(0)})*{v * math.sin(d) / FPS:.5f}", 1)
        return {"obj": e, "kind": "person", "speed_ms": v, "dir": d, "start": 0.0}
    rot = math.radians(a.get("face_deg", 0))
    e = characters.place(a["id"], coll, variant, (x, y, z), rot, rng, a.get("scale", 1.0))
    t = a.get("turn")
    if t:
        e.keyframe_insert("rotation_euler", frame=f(t["at"]))
        e.rotation_euler.z = math.radians(t["to_deg"])
        e.keyframe_insert("rotation_euler", frame=f(t["at"] + t.get("dur", 0.5)))
    return {"obj": e, "kind": "person", "speed_ms": 0.0, "dir": rot - math.pi / 2, "start": 0.0}


def _vehicle(a, kit, coll):
    veh = kit["vehicles"]
    src = veh["truck"] if a["type"] == "truck" else veh["car"][zlib.crc32(a["id"].encode()) % len(veh["car"])]
    v = a.get("speed_mph", 0) * MPH
    go = a.get("go")
    if go:
        v = go["speed_mph"] * MPH
    heading = 0.0 if v >= 0 else math.pi
    x0, lane = a["start_x"], a["lane"]
    e = geo.instance(a["id"], coll, src, (x0, lane, 0.0), heading)
    e.color = (a.get("color", _rng(a["id"]).random()), 0, 0, 1)
    start = go["at"] if go else 0.0
    geo.drive(e, "location", f"{x0}+max(0,frame-{f(start):.2f})*{v / FPS:.5f}", 0)
    return {"obj": e, "kind": a["type"], "speed_ms": abs(v), "dir": heading, "start": start}
