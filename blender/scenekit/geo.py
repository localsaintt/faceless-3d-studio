"""Shared low-poly mesh datablocks and object helpers (meshes are reused, never duplicated)."""
import math
import bmesh
import bpy

_meshes = {}


def _from_bm(name, build, smooth=False):
    if name in _meshes:
        return _meshes[name]
    bm = bmesh.new()
    build(bm)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    if smooth:
        me.shade_smooth()
    _meshes[name] = me
    return me


def sphere(segments=16, rings=10):
    return _from_bm(f"sphere_{segments}_{rings}",
                    lambda bm: bmesh.ops.create_uvsphere(bm, u_segments=segments, v_segments=rings, radius=1.0),
                    smooth=True)


def cube():
    return _from_bm("cube", lambda bm: bmesh.ops.create_cube(bm, size=1.0))


def cylinder(segments=10):
    return _from_bm(f"cyl_{segments}",
                    lambda bm: bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segments,
                                                     radius1=1.0, radius2=1.0, depth=1.0), smooth=True)


def cone(segments=10):
    return _from_bm(f"cone_{segments}",
                    lambda bm: bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segments,
                                                     radius1=1.0, radius2=0.0, depth=1.0))


def grid(name, x_seg, y_seg, size):
    return _from_bm(name, lambda bm: bmesh.ops.create_grid(bm, x_segments=x_seg, y_segments=y_seg, size=size))


def obj(name, mesh, coll, loc=(0, 0, 0), scale=(1, 1, 1), rot=(0, 0, 0), mat=None, parent=None):
    o = bpy.data.objects.new(name, mesh)
    coll.objects.link(o)
    o.location, o.scale, o.rotation_euler = loc, scale, rot
    if mat is not None:
        # Meshes are shared, so the material is assigned per object (slot link = OBJECT).
        if len(o.data.materials) == 0:
            o.data.materials.append(None)
        o.material_slots[0].link = "OBJECT"
        o.material_slots[0].material = mat
    if parent is not None:
        o.parent = parent
    return o


def empty(name, coll, loc=(0, 0, 0), rot=(0, 0, 0), parent=None, kind="PLAIN_AXES"):
    e = bpy.data.objects.new(name, None)
    e.empty_display_type = kind
    coll.objects.link(e)
    e.location, e.rotation_euler = loc, rot
    if parent is not None:
        e.parent = parent
    return e


def drive(target, path, expression, index=-1):
    """Procedural animation via simple-expression drivers (no Python execution needed)."""
    fc = target.driver_add(path, index) if index >= 0 else target.driver_add(path)
    fc.driver.type = "SCRIPTED"
    fc.driver.expression = expression
    return fc


def new_collection(name, parent=None, exclude=False):
    c = bpy.data.collections.new(name)
    (parent or bpy.context.scene.collection).children.link(c)
    if exclude:
        def find(lc):
            if lc.collection == c:
                return lc
            for ch in lc.children:
                r = find(ch)
                if r:
                    return r
        find(bpy.context.view_layer.layer_collection).exclude = True
    return c


def instance(name, coll, source, loc, rot_z=0.0, scale=1.0):
    e = bpy.data.objects.new(name, None)
    e.instance_type = "COLLECTION"
    e.instance_collection = source
    coll.objects.link(e)
    e.location = loc
    e.rotation_euler = (0, 0, rot_z)
    e.scale = (scale, scale, scale)
    return e


TAU = 2 * math.pi
