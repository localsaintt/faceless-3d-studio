"""Beach set kit (South Beach-inspired, generic, no real logos or businesses).

World layout (metres): X runs along the shoreline, +Y is out to sea, the waterline is at Y≈0,
and the hotel promenade sits behind the beach at Y≈-34. Everything is seeded, so the same kit
gives a different layout per video.
"""
import math
import random

import bpy

from . import characters, geo, style

P = style.PALETTE


def build(spec, scene):
    rng = random.Random(spec.get("seed", 1))
    root = geo.new_collection("SET_beach")
    lib = geo.new_collection("LIB", exclude=True)

    _sky(scene)
    _sun(root, spec.get("sun", {}))
    _sand(root)
    _ocean(root)
    _clouds(root, rng)
    palms = _palm_library(lib)
    _hotels(root, rng, spec.get("buildings", 9))
    _scatter_palms(root, palms, rng, spec.get("palms", 14))
    blocked, umbrellas = _umbrellas(root, lib, rng, spec.get("umbrellas", 16), spec.get("clear", []))
    tower = _lifeguard_tower(root, spec.get("tower", {"loc": [6, -6, 0]}))
    tx, ty = spec.get("tower", {"loc": [6, -6, 0]})["loc"][:2]
    blocked = blocked + [(tx, ty, 2.6)] + [tuple(c) for c in spec.get("clear", [])]
    variants = characters.build_library(lib, seed=spec.get("seed", 1))
    crowd = _crowd(root, variants, rng, spec.get("crowd", 150), blocked)
    return {"root": root, "lib": lib, "variants": variants, "tower": tower, "crowd": crowd, "rng": rng,
            "umbrellas": umbrellas}


# ---------------------------------------------------------------- environment
def _sky(scene):
    w = bpy.data.worlds.new("Sky")
    scene.world = w
    nt = w.node_tree
    bg = next(n for n in nt.nodes if n.type == "BACKGROUND")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["From Min"].default_value = -0.02
    mr.inputs["From Max"].default_value = 0.55
    cr = nt.nodes.new("ShaderNodeValToRGB")
    cr.color_ramp.elements[0].color = style.lin(P["sky_horizon"])
    cr.color_ramp.elements[1].color = style.lin(P["sky_top"])
    nt.links.new(tc.outputs["Generated"], sep.inputs["Vector"])
    nt.links.new(sep.outputs["Z"], mr.inputs["Value"])
    nt.links.new(mr.outputs["Result"], cr.inputs["Fac"])
    nt.links.new(cr.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = 1.0


def _sun(coll, cfg):
    d = bpy.data.lights.new("Sun", "SUN")
    d.energy = cfg.get("strength", 4.2)
    d.color = style.lin(P["sun"])[:3]
    d.angle = math.radians(cfg.get("softness_deg", 3.0))
    o = bpy.data.objects.new("Sun", d)
    coll.objects.link(o)
    o.rotation_euler = (math.radians(cfg.get("elevation_tilt", 42)), math.radians(12),
                        math.radians(cfg.get("azimuth", 155)))


def _sand(coll):
    me = geo.grid("sand_grid", 60, 30, 1.0)
    # dry beach: y from -54 to 0 (grid spans -1..1 before scaling)
    o = geo.obj("Sand", me, coll, (0, -27, 0), (90, 27, 1), mat=None)
    # seabed slopes down from the waterline so waves lap onto the shore
    geo.obj("Seabed", me, coll, (0, 30, -3.14), (90, 30, 1), (math.radians(-6), 0, 0),
            mat=style.solid("seabed", P["sand_wet"], 0.95))
    m = bpy.data.materials.new("sand")
    nt = m.node_tree
    b = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 0.35
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.25
    # wet sand band near the water: object-space Y gradient
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["From Min"].default_value = 0.86
    mr.inputs["From Max"].default_value = 0.97
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.inputs["A"].default_value = style.lin(P["sand"])
    mix.inputs["B"].default_value = style.lin(P["sand_wet"])
    nt.links.new(tc.outputs["Object"], sep.inputs["Vector"])
    nt.links.new(sep.outputs["Y"], mr.inputs["Value"])
    nt.links.new(mr.outputs["Result"], mix.inputs["Factor"])
    nt.links.new(mix.outputs["Result"], b.inputs["Base Color"])
    nt.links.new(tc.outputs["Object"], noise.inputs["Vector"])
    nt.links.new(noise.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    b.inputs["Roughness"].default_value = 0.92
    o.material_slots[0].link = "OBJECT"  # mesh is shared with the seabed
    o.material_slots[0].material = m
    # promenade strip behind the beach
    geo.obj("Promenade", geo.cube(), coll, (0, -32.5, 0.05), (90, 3, 0.1), mat=style.solid("concrete", P["concrete"], 0.85))


def _ocean(coll):
    # the generated ocean grid starts at (loc - spatial_size/2) and extends size*repeat:
    # this places it from x=-90..110, y=-1..79 so the water meets the sand at the waterline
    o = geo.obj("Ocean", geo.grid("ocean_seed", 1, 1, 1.0), coll, (-70, 19, -0.2))
    mod = o.modifiers.new("ocean", "OCEAN")
    mod.geometry_mode = "GENERATE"
    mod.spatial_size = 40
    mod.resolution = 9
    mod.repeat_x = 5
    mod.repeat_y = 2
    mod.wave_scale = 0.2
    mod.choppiness = 0.9
    mod.wind_velocity = 9
    geo.drive(o, 'modifiers["ocean"].time', "frame/24")
    m = bpy.data.materials.new("sea")
    nt = m.node_tree
    b = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.35
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.inputs["A"].default_value = style.lin(P["sea_shallow"])
    mix.inputs["B"].default_value = style.lin(P["sea_deep"])
    nt.links.new(lw.outputs["Facing"], mix.inputs["Factor"])
    nt.links.new(mix.outputs["Result"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.08
    b.inputs["Specular IOR Level"].default_value = 0.6
    o.data.materials.append(m)
    o.modifiers.new("smooth", "SMOOTH")


def _clouds(coll, rng):
    mat = style.solid("cloud", P["white"], 1.0, emission=0.25)
    S = geo.sphere(12, 8)
    for i in range(7):
        cx, cy, cz = rng.uniform(-120, 120), rng.uniform(140, 220), rng.uniform(28, 55)
        for j in range(rng.randint(3, 5)):
            r = rng.uniform(5, 10)
            geo.obj(f"cloud{i}_{j}", S, coll, (cx + j * r * 0.9, cy + rng.uniform(-3, 3), cz + rng.uniform(-1, 2)),
                    (r, r * 0.8, r * 0.55), mat=mat)


# ---------------------------------------------------------------- props
def _palm_library(lib, count=3):
    trunk_m = style.solid("palm_trunk", P["palm_trunk"], 0.9)
    leaf_m = style.solid("palm_leaf", P["palm_leaf"], 0.7)
    nut_m = style.solid("coconut", P["coconut"], 0.6)
    S = geo.sphere(10, 6)
    out = []
    for k in range(count):
        coll = geo.new_collection(f"palm_{k}", parent=lib)
        lean = 0.6 + 0.5 * k
        h = 7.5 + 1.2 * k
        cu = bpy.data.curves.new(f"trunk_{k}", "CURVE")
        cu.dimensions = "3D"
        cu.bevel_depth = 0.2
        cu.bevel_resolution = 1
        sp = cu.splines.new("BEZIER")
        sp.bezier_points.add(2)
        for i, (x, z, r) in enumerate([(0, 0, 1.25), (lean * 0.45, h * 0.5, 0.95), (lean, h, 0.7)]):
            bp = sp.bezier_points[i]
            bp.co = (x, 0, z)
            bp.radius = r
            bp.handle_left_type = bp.handle_right_type = "AUTO"
        cu.materials.append(trunk_m)
        tr = bpy.data.objects.new(f"trunk_{k}", cu)
        coll.objects.link(tr)
        top = (lean, 0, h)
        for i in range(8):
            a = i / 8 * geo.TAU + k
            droop = 0.55 + 0.25 * ((i * 7 + k) % 3) / 2
            geo.obj(f"frond_{k}_{i}", S, coll,
                    (top[0] + math.cos(a) * 1.5, math.sin(a) * 1.5, top[2] - 0.6 * droop),
                    (1.9, 0.42, 0.06), (0, droop, a), mat=leaf_m)
        for i in range(3):
            a = i / 3 * geo.TAU
            geo.obj(f"nut_{k}_{i}", S, coll, (top[0] + math.cos(a) * 0.3, math.sin(a) * 0.3, top[2] - 0.35),
                    (0.2, 0.2, 0.22), mat=nut_m)
        out.append(coll)
    return out


def _scatter_palms(coll, palms, rng, n):
    for i in range(n):
        x = -60 + i * (120 / max(n - 1, 1)) + rng.uniform(-3, 3)
        y = rng.uniform(-30, -26)
        geo.instance(f"palm{i}", coll, rng.choice(palms), (x, y, 0), rng.uniform(0, geo.TAU), rng.uniform(0.85, 1.15))


def _hotels(coll, rng, n):
    """Art Deco-inspired pastel blocks: rounded corners suggested with stacked bands, no real names."""
    body = style.random_palette("hotel_body", style.PASTEL, 0.75)
    trim = style.solid("hotel_trim", P["white"], 0.6)
    glass = style.solid("hotel_glass", "#2C5C7A", 0.15)
    C = geo.cube()
    x = -70
    for i in range(n):
        w = rng.uniform(10, 18)
        h = rng.uniform(9, 22)
        d = 10
        cx = x + w / 2
        y = -42
        geo.obj(f"hotel{i}", C, coll, (cx, y, h / 2), (w, d, h), mat=body)
        floors = int(h // 3.2)
        for f in range(floors):
            z = 2.2 + f * 3.2
            geo.obj(f"hotel{i}_win{f}", C, coll, (cx, y + d / 2 + 0.03, z), (w * 0.8, 0.06, 1.2), mat=glass)
            geo.obj(f"hotel{i}_band{f}", C, coll, (cx, y + d / 2 + 0.12, z + 1.0), (w * 0.92, 0.25, 0.22), mat=trim)
        # deco "eyebrow" fin on the roof line
        geo.obj(f"hotel{i}_fin", C, coll, (cx, y + d / 2 - 0.5, h + 1.2), (1.0, 1.0, 2.4), mat=trim)
        x += w + rng.uniform(1.5, 4)


def _umbrellas(coll, lib, rng, n, clear=()):
    canopy = style.random_palette("umbrella", style.UMBRELLA, 0.6)
    towel = style.random_palette("towel", style.UMBRELLA + style.PASTEL, 0.9)
    pole = style.solid("pole", P["white"], 0.5)
    ucoll = geo.new_collection("umbrella_src", parent=lib)
    geo.obj("u_canopy", geo.cone(10), ucoll, (0, 0, 2.15), (1.25, 1.25, 0.45), mat=canopy)
    geo.obj("u_pole", geo.cylinder(6), ucoll, (0, 0, 1.0), (0.04, 0.04, 2.1), mat=pole)
    blocked, out = [], []
    while len(out) < n:
        x, y = rng.uniform(-45, 45), rng.uniform(-24, -6)
        if any((x - cx) ** 2 + (y - cy) ** 2 < (cr + 2) ** 2 for cx, cy, cr in clear):
            continue
        out.append(geo.instance(f"umbrella{len(out)}", coll, ucoll, (x, y, 0), rng.uniform(0, geo.TAU),
                                rng.uniform(0.9, 1.1)))
        i = len(out) - 1
        geo.obj(f"towel{i}", geo.cube(), coll, (x + rng.uniform(-1.4, 1.4), y + 1.6, 0.02), (1.0, 1.9, 0.02),
                (0, 0, rng.uniform(-0.4, 0.4)), mat=towel)
        blocked.append((x, y, 1.8))
    return blocked, out


def _lifeguard_tower(coll, cfg):
    red = style.solid("tower_red", P["tower_red"], 0.55)
    yellow = style.solid("tower_yellow", P["tower_yellow"], 0.55)
    white = style.solid("tower_white", P["white"], 0.6)
    C = geo.cube()
    x, y, z = cfg.get("loc", [6, -6, 0])
    t = geo.empty("Tower", coll, (x, y, z), (0, 0, math.radians(cfg.get("rot_deg", 0))))
    for sx in (-1, 1):
        for sy in (-1, 1):
            geo.obj("tw_leg", C, coll, (sx * 1.1, sy * 1.1, 1.0), (0.18, 0.18, 2.0), mat=white, parent=t)
    geo.obj("tw_deck", C, coll, (0, 0, 2.05), (3.0, 3.0, 0.15), mat=white, parent=t)
    geo.obj("tw_cabin", C, coll, (0, 0.2, 3.05), (2.4, 2.0, 1.9), mat=red, parent=t)
    geo.obj("tw_window", C, coll, (0, 1.22, 3.25), (1.7, 0.05, 0.8), mat=style.solid("tw_glass", "#2C5C7A", 0.1), parent=t)
    geo.obj("tw_stripe", C, coll, (0, 1.24, 2.4), (2.42, 0.06, 0.25), mat=yellow, parent=t)
    geo.obj("tw_roof", C, coll, (0, 0.2, 4.15), (2.9, 2.5, 0.25), mat=yellow, parent=t)
    geo.obj("tw_ramp", C, coll, (0, -2.6, 1.0), (1.0, 3.4, 0.1), (math.radians(-36), 0, 0), mat=white, parent=t)
    return t


def _crowd(coll, variants, rng, n, blocked):
    """Scatter people with simple rejection sampling; most face the sea (+Y)."""
    pool = variants["idle"] * 3 + variants["talk"] * 2 + variants["look_up"]
    placed, out, tries = [], [], 0
    while len(out) < n and tries < n * 40:
        tries += 1
        x, y = rng.uniform(-40, 40), rng.uniform(-22, 1.5)
        if any((x - bx) ** 2 + (y - by) ** 2 < br ** 2 for bx, by, br in blocked):
            continue
        if any((x - px) ** 2 + (y - py) ** 2 < 0.8 ** 2 for px, py in placed):
            continue
        placed.append((x, y))
        face = math.pi + rng.uniform(-0.9, 0.9) if rng.random() < 0.75 else rng.uniform(0, geo.TAU)
        out.append(characters.place(f"person{len(out)}", coll, rng.choice(pool), (x, y, 0), face, rng))
    return out
