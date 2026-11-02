"""Street set kit (Ocean Drive-inspired, generic: no real businesses, names or logos).

Layout (metres): road along X with lanes at y=+2 (eastbound, +X) and y=-2 (westbound),
hotel-side sidewalk + café terrace at y=-4..-10, Art Deco-style hotels behind (facades at y=-10),
beach-side sidewalk at y=4..7, palm row at y≈8.5, sand beyond.
"""
import math
import random

from . import beach, characters, geo, style, vehicles

P = style.PALETTE


def build(spec, scene):
    rng = random.Random(spec.get("seed", 1))
    root = geo.new_collection("SET_street")
    lib = geo.new_collection("LIB", exclude=True)
    beach._sky(scene)
    beach._sun(root, spec.get("sun", {}))
    _ground(root)
    _hotels(root, rng, spec.get("buildings", 9))
    palms = beach._palm_library(lib)
    for i in range(spec.get("palms", 12)):
        x = -70 + i * (140 / max(spec.get("palms", 12) - 1, 1)) + rng.uniform(-2, 2)
        geo.instance(f"palm{i}", root, rng.choice(palms), (x, rng.uniform(8.2, 9.5), 0.12), rng.uniform(0, geo.TAU),
                     rng.uniform(0.85, 1.1))
    _lamps(root)
    umbrellas = _cafes(root, lib, rng, spec.get("cafes", 8))
    variants = characters.build_library(lib, seed=spec.get("seed", 1))
    people = _pedestrians(root, variants, rng, spec.get("pedestrians", 34))
    veh = vehicles.build_library(lib)
    return {"root": root, "lib": lib, "variants": variants, "vehicles": veh, "umbrellas": umbrellas,
            "crowd": people, "rng": rng}


def _ground(coll):
    C = geo.cube()
    geo.obj("road", C, coll, (0, 0, -0.05), (200, 8, 0.1), mat=style.solid("asphalt", "#4A4F57", 0.85))
    concrete = style.solid("sidewalk", P["concrete"], 0.85)
    geo.obj("walk_hotel", C, coll, (0, -7, 0.06), (200, 6, 0.12), mat=concrete)
    geo.obj("walk_beach", C, coll, (0, 5.5, 0.06), (200, 3, 0.12), mat=concrete)
    geo.obj("curb_a", C, coll, (0, -4.05, 0.07), (200, 0.15, 0.14), mat=style.solid("curb", P["white"], 0.7))
    geo.obj("curb_b", C, coll, (0, 4.05, 0.07), (200, 0.15, 0.14), mat=style.solid("curb", P["white"], 0.7))
    geo.obj("sand_strip", C, coll, (0, 34, 0.0), (200, 54, 0.1), mat=style.solid("street_sand", P["sand"], 0.92))
    yellow = style.solid("line_yellow", "#F4C430", 0.6)
    white = style.solid("line_white", P["white"], 0.6)
    for i in range(-30, 31):
        geo.obj(f"dash{i}", C, coll, (i * 3.2, 0, 0.003), (1.6, 0.14, 0.01), mat=yellow)
    for s in (-1, 1):
        geo.obj(f"edge{s}", C, coll, (0, s * 3.7, 0.003), (200, 0.12, 0.01), mat=white)


def _hotels(coll, rng, n):
    body = style.random_palette("hotel_body", style.PASTEL, 0.75)
    trim = style.solid("hotel_trim", P["white"], 0.6)
    glass = style.solid("hotel_glass", "#2C5C7A", 0.15)
    neon = style.solid("hotel_neon", "#7DD3FC", 0.4, emission=0.6)
    C = geo.cube()
    x = -72
    for i in range(n):
        w, h, d = rng.uniform(12, 18), rng.uniform(10, 20), 12
        cx, y = x + w / 2, -10 - d / 2
        geo.obj(f"hotel{i}", C, coll, (cx, y, h / 2), (w, d, h), mat=body)
        for fl in range(int(h // 3.2)):
            z = 2.6 + fl * 3.2
            geo.obj(f"h{i}_win{fl}", C, coll, (cx, y + d / 2 + 0.03, z), (w * 0.8, 0.06, 1.2), mat=glass)
            geo.obj(f"h{i}_band{fl}", C, coll, (cx, y + d / 2 + 0.12, z + 1.0), (w * 0.92, 0.25, 0.22), mat=trim)
        # deco vertical fin + a blank neon bar (no lettering)
        geo.obj(f"h{i}_fin", C, coll, (cx + w * 0.3, y + d / 2 + 0.4, h * 0.6), (0.6, 0.8, h * 0.8), mat=trim)
        geo.obj(f"h{i}_neon", C, coll, (cx + w * 0.3, y + d / 2 + 0.82, h * 0.6), (0.12, 0.05, h * 0.6), mat=neon)
        geo.obj(f"h{i}_awning", C, coll, (cx, y + d / 2 + 1.2, 3.0), (w * 0.85, 2.4, 0.12), (0.18, 0, 0), mat=trim)
        x += w + rng.uniform(1.0, 2.5)


def _lamps(coll):
    pole = style.solid("lamp_pole", "#2F3B45", 0.5, metallic=0.6)
    head = style.solid("lamp_head", "#FFF6D8", 0.3, emission=0.8)
    for i in range(-6, 7):
        x = i * 14 + 7
        geo.obj(f"lamp{i}", geo.cylinder(8), coll, (x, 4.6, 2.3), (0.07, 0.07, 4.6), mat=pole)
        geo.obj(f"lamp{i}_h", geo.sphere(10, 6), coll, (x, 4.6, 4.65), (0.22, 0.22, 0.18), mat=head)


def _cafes(coll, lib, rng, n):
    canopy = style.random_palette("umbrella", style.UMBRELLA, 0.6)
    pole = style.solid("pole", P["white"], 0.5)
    table = style.solid("cafe_table", P["white"], 0.4)
    src = geo.new_collection("cafe_umbrella_src", parent=lib)
    geo.obj("cu_canopy", geo.cone(10), src, (0, 0, 2.3), (1.3, 1.3, 0.4), mat=canopy)
    geo.obj("cu_pole", geo.cylinder(6), src, (0, 0, 1.15), (0.04, 0.04, 2.3), mat=pole)
    geo.obj("cu_table", geo.cylinder(12), src, (0, 0, 0.75), (0.5, 0.5, 0.05), mat=table)
    out = []
    for i in range(n * 3):
        x = -60 + i * (120 / (n * 3)) + rng.uniform(-0.8, 0.8)
        out.append(geo.instance(f"cafe{i}", coll, src, (x, rng.uniform(-8.6, -7.6), 0.12), rng.uniform(0, geo.TAU)))
    return out


def _pedestrians(coll, variants, rng, n):
    pool = variants["idle"] * 2 + variants["talk"] * 2
    out = []
    for i in range(n):
        side = rng.random()
        x = rng.uniform(-50, 50)
        y = rng.uniform(-6.5, -5) if side < 0.6 else rng.uniform(4.7, 6.6)
        out.append(characters.place(f"ped{i}", coll, rng.choice(pool), (x, y, 0.12), rng.uniform(0, geo.TAU), rng))
    return out
