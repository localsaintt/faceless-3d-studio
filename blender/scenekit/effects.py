"""Stylised effects in the EVENT colour (magenta = "the thing that changed").

All motion is driver-based and keyed to absolute frames, so every effect is deterministic.
Times in specs are seconds from the start of the shot; `f(t)` converts them to frames.
"""
import math
import random

import bmesh
import bpy

from . import geo, style

FPS = 24
F0 = 1  # first frame of every shot


def f(t):
    return F0 + t * FPS


# ---------------------------------------------------------------- materials
def event_material(name="event_shell", strength=2.2, edge_power=2.2, core=0.06, hex_color=None):
    """Glowing translucent shell: bright at grazing angles, almost clear face-on.
    Overall opacity follows the object's colour alpha (driven per effect)."""
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    m = bpy.data.materials.new(name)
    m.surface_render_method = "BLENDED"
    m.use_backface_culling = False
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.5
    inv = nt.nodes.new("ShaderNodeMath")
    inv.operation = "SUBTRACT"
    inv.inputs[0].default_value = 1.0
    nt.links.new(lw.outputs["Facing"], inv.inputs[1])            # 1 face-on -> 0 ; edges -> 1
    pw = nt.nodes.new("ShaderNodeMath")
    pw.operation = "POWER"
    pw.inputs[1].default_value = edge_power
    nt.links.new(lw.outputs["Facing"], pw.inputs[0])
    add = nt.nodes.new("ShaderNodeMath")
    add.operation = "ADD"
    add.inputs[1].default_value = core
    nt.links.new(pw.outputs[0], add.inputs[0])
    info = nt.nodes.new("ShaderNodeObjectInfo")
    mul = nt.nodes.new("ShaderNodeMath")
    mul.operation = "MULTIPLY"
    mul.use_clamp = True
    nt.links.new(add.outputs[0], mul.inputs[0])
    nt.links.new(info.outputs["Alpha"], mul.inputs[1])
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = style.lin(hex_color or style.PALETTE["event"])
    em.inputs["Strength"].default_value = strength
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(mul.outputs[0], mix.inputs["Fac"])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    return m


# ---------------------------------------------------------------- rings
def _annulus(inner=0.93, segs=72):
    name = f"annulus_{inner}_{segs}"
    if name in bpy.data.meshes:
        return bpy.data.meshes[name]
    bm = bmesh.new()
    outer_v = [bm.verts.new((math.cos(a / segs * geo.TAU), math.sin(a / segs * geo.TAU), 0)) for a in range(segs)]
    inner_v = [bm.verts.new((inner * math.cos(a / segs * geo.TAU), inner * math.sin(a / segs * geo.TAU), 0))
               for a in range(segs)]
    for a in range(segs):
        b = (a + 1) % segs
        bm.faces.new((outer_v[a], outer_v[b], inner_v[b], inner_v[a]))
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    return me


def ground_ripple_material():
    if "event_ripple" in bpy.data.materials:
        return bpy.data.materials["event_ripple"]
    m = bpy.data.materials.new("event_ripple")
    m.surface_render_method = "BLENDED"
    m.use_backface_culling = False
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    info = nt.nodes.new("ShaderNodeObjectInfo")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = style.lin(style.PALETTE["event"])
    em.inputs["Strength"].default_value = 2.5
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(info.outputs["Alpha"], mix.inputs["Fac"])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    return m


def ring(coll, name, at, origin, speed, max_r, collapse_at=None, floor=0.0, ground=None):
    """Expanding sound shell. Radius = speed * time; fades to `floor` as it reaches max_r
    (floor > 0 keeps "sound still in the air" visible)."""
    o = geo.obj(name, geo.sphere(32, 16), coll, tuple(origin), (0.001,) * 3, mat=event_material())
    k = speed / FPS
    fs = f(at)
    r = f"max(0.001,min({max_r},(frame-{fs:.2f})*{k:.4f}))"
    if collapse_at is not None:
        fc = f(collapse_at)
        r = f"{r}*(1 if frame<{fc:.2f} else max(0.001,1-(frame-{fc:.2f})/5))"
    for i in range(3):
        geo.drive(o, "scale", r, i)
    life = max_r / k  # frames until it reaches max_r
    alpha = f"(frame>={fs:.2f})*clamp(1.15-(frame-{fs:.2f})/{life:.2f},{floor},1)"
    if collapse_at is not None:
        alpha = f"{alpha}*(frame<{f(collapse_at) + 5:.2f})"
    o.color = (1, 1, 1, 1)
    geo.drive(o, "color", alpha, 3)
    o.visible_shadow = False
    if ground is not None:
        # glowing ripple on the ground: shows exactly where the sound front is, even when the shell fills the frame
        g = geo.obj(f"{name}_ripple", _annulus(), coll, (origin[0], origin[1], ground + 0.04), (0.001,) * 3,
                    mat=ground_ripple_material())
        for i in range(2):
            geo.drive(g, "scale", r, i)
        g.color = (1, 1, 1, 1)
        geo.drive(g, "color", f"0.9*({alpha})", 3)
        g.visible_shadow = False
    return o


def ring_field(coll, name, at, count, area, speed, max_r, spread, seed, collapse_at=None, z=1.4):
    rng = random.Random(seed)
    return [ring(coll, f"{name}_{i}", at + rng.uniform(0, spread),
                 (rng.uniform(*area[0]), rng.uniform(*area[1]), z), speed,
                 max_r * rng.uniform(0.6, 1.0), collapse_at, floor=0.4) for i in range(count)]


# ---------------------------------------------------------------- mach cone
def mach_cone(coll, name, parent, speed_ms, sound_ms=3.13, length=9.0, apex=(0, 0, 0), local_rot_z=0.0, start=None):
    """Cone trailing a supersonic object. Half-angle from sin(θ) = 1/M (clamped for readability)."""
    mach = max(abs(speed_ms) / sound_ms, 1.05)
    half = math.asin(1 / mach)
    half = min(half, math.radians(55))
    me_name = f"cone_{round(math.degrees(half))}_{length}"
    if me_name in bpy.data.meshes:
        me = bpy.data.meshes[me_name]
    else:
        bm = bmesh.new()
        segs, rings_ = 32, 6
        tip = bm.verts.new((0, 0, 0))
        prev = [tip] * segs
        for j in range(1, rings_ + 1):
            x = -length * j / rings_
            rad = abs(x) * math.tan(half)
            cur = [bm.verts.new((x, rad * math.cos(a / segs * geo.TAU), rad * math.sin(a / segs * geo.TAU)))
                   for a in range(segs)]
            for a in range(segs):
                b = (a + 1) % segs
                if j == 1:
                    bm.faces.new((tip, cur[a], cur[b]))
                else:
                    bm.faces.new((prev[a], cur[a], cur[b], prev[b]))
            prev = cur
        me = bpy.data.meshes.new(me_name)
        bm.to_mesh(me)
        bm.free()
        me.shade_smooth()
    o = geo.obj(name, me, coll, apex, rot=(0, 0, local_rot_z), mat=event_material("event_cone", 1.6, 1.6, 0.04),
                parent=parent)
    o.color = (1, 1, 1, 0.85)
    if start is not None:
        geo.drive(o, "color", f"0.85*clamp((frame-{f(start):.2f})/6,0,1)", 3)
    o.visible_shadow = False
    return o


# ---------------------------------------------------------------- booms and reactions
def boom(coll, name, at, pos, strength=1.0):
    """Shock flash: a fast expanding bright shell plus a hot core."""
    m = event_material("event_flash", 4.0, 1.2, 0.25, hex_color="#FF7AB8")
    o = geo.obj(name, geo.sphere(24, 12), coll, tuple(pos), (0.001,) * 3, mat=m)
    fs = f(at)
    R = 6 * strength
    r = f"(frame>={fs:.2f})*max(0.001,{R}*(1-exp(-(frame-{fs:.2f})/3)))+0.001"
    for i in range(3):
        geo.drive(o, "scale", r, i)
    o.color = (1, 1, 1, 1)
    geo.drive(o, "color", f"(frame>={fs:.2f})*exp(-(frame-{fs:.2f})/5)", 3)
    o.visible_shadow = False
    return o


def camera_kick(cam, booms):
    """Rotational shake impulses on the camera for each boom (seconds, strength)."""
    if not booms:
        return
    for axis, freq in ((0, 1.9), (1, 2.3)):
        terms = "+".join(f"(frame>{f(t):.2f})*{0.035 * s:.4f}*exp(-(frame-{f(t):.2f})/5)*sin(frame*{freq + axis * 0.3})"
                         for t, s in booms)
        geo.drive(cam, "delta_rotation_euler", terms, axis)


def flip(objs, at, center, radius, wave_speed=40.0):
    """Umbrellas/props kick and wobble as the shock wave passes (delay grows with distance)."""
    cx, cy = center
    for o in objs:
        d = math.hypot(o.location.x - cx, o.location.y - cy)
        if d > radius:
            continue
        fs = f(at) + d / wave_speed * FPS
        amp = 0.9 * max(0.25, 1 - d / radius)
        ax = 0 if (int(d * 10) % 2) else 1
        geo.drive(o, "rotation_euler", f"(frame>{fs:.2f})*{amp:.3f}*exp(-(frame-{fs:.2f})/14)*sin((frame-{fs:.2f})*0.45)", ax)


def crowd_jump(people, at, wave_speed=60.0, center=(0, -10)):
    for p in people:
        d = math.hypot(p.location.x - center[0], p.location.y - center[1])
        fs = f(at) + d / wave_speed * FPS
        base = p.location.z
        geo.drive(p, "location", f"{base}+(frame>{fs:.2f})*(frame<{fs + 13:.2f})*0.55*sin((frame-{fs:.2f})*0.2417)", 2)
