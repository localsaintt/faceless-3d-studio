"""House characters: rounded "bean-body" people with dot eyes, animated procedurally.

Each *variant* is a small collection (one character + one animation style + one phase).
Crowds are collection instances of variants, so hundreds of people cost almost no memory.
Per-person colours come from the instancing Empty's object colour (see style.instancer_palette).
"""
import math
import random

from . import geo, style

FWD = -1.0  # characters face local -Y


def _materials():
    return {
        "skin": style.instancer_palette("skin", style.SKIN, "R"),
        "shirt": style.instancer_palette("shirt", style.SHIRT, "G"),
        "shorts": style.instancer_palette("shorts", style.SHORTS, "B"),
        "hair": style.instancer_palette("hair", style.HAIR, "A", rough=0.8),
        "eye": style.solid("eye", style.PALETTE["ink"], rough=0.25),
    }


def build_variant(name, lib, anim="idle", phase=0.0, hair=True, height=1.0, width=1.0):
    """Create one character variant collection under `lib`. Returns the collection."""
    coll = geo.new_collection(name, parent=lib)
    m = _materials()
    S = geo.sphere(12, 8)
    root = geo.empty(f"{name}_root", coll)
    root.scale = (width, width, height)

    # torso (the "bean")
    torso = geo.obj(f"{name}_torso", S, coll, (0, 0, 0.84), (0.28, 0.23, 0.37), mat=m["shirt"], parent=root)
    # head on a neck pivot
    neck = geo.empty(f"{name}_neck", coll, (0, 0, 1.16), parent=root)
    geo.obj(f"{name}_head", S, coll, (0, 0, 0.22), (0.23, 0.22, 0.23), mat=m["skin"], parent=neck)
    for sx in (-1, 1):
        geo.obj(f"{name}_eye{sx}", S, coll, (0.085 * sx, FWD * 0.2, 0.25), (0.032, 0.02, 0.04), mat=m["eye"], parent=neck)
    if hair:
        geo.obj(f"{name}_hair", S, coll, (0, 0.03, 0.31), (0.235, 0.23, 0.15), mat=m["hair"], parent=neck)
    # limbs on pivots
    hips, shoulders = [], []
    for sx in (-1, 1):
        hip = geo.empty(f"{name}_hip{sx}", coll, (0.11 * sx, 0, 0.52), parent=root)
        geo.obj(f"{name}_leg{sx}", S, coll, (0, 0, -0.24), (0.1, 0.1, 0.27), mat=m["shorts"], parent=hip)
        geo.obj(f"{name}_foot{sx}", S, coll, (0, FWD * 0.04, -0.5), (0.085, 0.12, 0.05), mat=m["skin"], parent=hip)
        hips.append(hip)
        sh = geo.empty(f"{name}_shoulder{sx}", coll, (0.245 * sx, 0, 1.02), (0, 0.1 * sx, 0), parent=root)
        geo.obj(f"{name}_arm{sx}", S, coll, (0, 0, -0.2), (0.075, 0.075, 0.22), mat=m["skin"], parent=sh)
        shoulders.append(sh)

    _animate(anim, phase, root, torso, neck, hips, shoulders)
    return coll


def _animate(anim, ph, root, torso, neck, hips, shoulders):
    p = f"{ph:.3f}"
    if anim == "idle":
        geo.drive(torso, "scale", f"0.37*(1+0.025*sin(frame*0.16+{p}))", 2)
        geo.drive(neck, "rotation_euler", f"0.10*sin(frame*0.045+{p})", 2)
        geo.drive(neck, "rotation_euler", f"0.05*sin(frame*0.07+{p})", 0)
        for i, sh in enumerate(shoulders):
            s = 1 if i else -1
            geo.drive(sh, "rotation_euler", f"0.08*sin(frame*0.12+{p}+{i})", 0)
            geo.drive(sh, "rotation_euler", f"{0.1 * s:.2f}", 1)
    elif anim == "talk":
        geo.drive(torso, "scale", f"0.37*(1+0.02*sin(frame*0.2+{p}))", 2)
        geo.drive(neck, "rotation_euler", f"0.12*sin(frame*0.33+{p})", 0)
        geo.drive(neck, "rotation_euler", f"0.18*sin(frame*0.06+{p})", 2)
        geo.drive(shoulders[1], "rotation_euler", f"-0.9+0.35*sin(frame*0.28+{p})", 0)
        geo.drive(shoulders[0], "rotation_euler", f"0.06*sin(frame*0.1+{p})", 0)
    elif anim == "look_up":
        geo.drive(neck, "rotation_euler", f"-0.45+0.04*sin(frame*0.1+{p})", 0)
        geo.drive(torso, "scale", f"0.37*(1+0.02*sin(frame*0.14+{p}))", 2)
        geo.drive(shoulders[0], "rotation_euler", "-2.6", 0)  # one arm pointing up
    elif anim == "walk":
        w = 0.42  # stride frequency (rad/frame) at 24 fps
        geo.drive(root, "location", f"0.035*abs(sin(frame*{w}+{p}))", 2)
        geo.drive(torso, "rotation_euler", f"0.06*sin(frame*{w}+{p})", 1)
        for i, (hip, sh) in enumerate(zip(hips, shoulders)):
            sign = 1 if i else -1
            geo.drive(hip, "rotation_euler", f"{0.55 * sign}*sin(frame*{w}+{p})", 0)
            geo.drive(sh, "rotation_euler", f"{-0.45 * sign}*sin(frame*{w}+{p})", 0)
    else:
        raise ValueError(f"unknown anim {anim}")


def build_library(lib, seed=1, per_anim=4, anims=("idle", "talk", "look_up", "walk")):
    """Build variants for each animation style with random phases and body shapes."""
    rng = random.Random(seed)
    variants = {a: [] for a in anims}
    for a in anims:
        for i in range(per_anim):
            variants[a].append(build_variant(
                f"char_{a}_{i}", lib, anim=a, phase=rng.uniform(0, 2 * math.pi),
                hair=rng.random() < 0.7, height=rng.uniform(0.85, 1.12), width=rng.uniform(0.9, 1.15)))
    return variants


def colour_key(rng):
    """RGBA keys for one person (skin, shirt, shorts, hair), each kept inside its ramp bin."""
    return tuple(rng.random() * 0.999 for _ in range(4))


def place(name, coll, variant, loc, rot_z, rng, scale=1.0):
    e = geo.instance(name, coll, variant, loc, rot_z, scale)
    e.color = colour_key(rng)
    return e
