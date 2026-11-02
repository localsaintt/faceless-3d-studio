"""House style v1 ("Living Diorama"): palette, materials and colour-management settings.

All colours are authored as sRGB hex and converted to scene-linear for Blender.
Magenta (EVENT) is reserved for "the thing that changed" in every video.
"""
import bpy


def lin(hex_str, alpha=1.0):
    h = hex_str.lstrip("#")
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return (*out, alpha)


PALETTE = {
    "sand": "#EDD5A8", "sand_wet": "#C9AE80",
    "sea_shallow": "#3CC9BE", "sea_deep": "#0F7FA0",
    "sky_top": "#4FA3E3", "sky_horizon": "#D4EEF7",
    "sun": "#FFF1DA",
    "palm_trunk": "#9A7653", "palm_leaf": "#3E9E52", "coconut": "#6B4A2B",
    "concrete": "#DCD6CC", "white": "#F7F5F0", "ink": "#151A1E",
    "tower_red": "#E5484D", "tower_yellow": "#F4C430",
    "event": "#E0217A",
}
SKIN = ["#F3CFAE", "#E6B48C", "#CF9469", "#A86F47", "#7F5133", "#5B3A26"]
SHIRT = ["#E5484D", "#F59E0B", "#FACC15", "#22C55E", "#14B8A6", "#3B82F6",
         "#6366F1", "#EC4899", "#F8FAFC", "#1F2937", "#FB7185", "#84CC16"]
SHORTS = ["#1E3A8A", "#0F766E", "#F97316", "#374151", "#BE185D", "#F5F5F4", "#65A30D"]
HAIR = ["#1B1410", "#3B2416", "#6B4423", "#C59A5B", "#9CA3AF", "#B4462B"]
PASTEL = ["#F9C6CF", "#BFE3DA", "#FCE7A6", "#C9D7F8", "#F7D2B6", "#D9C8F0", "#FFFFFF"]
UMBRELLA = ["#E5484D", "#F59E0B", "#14B8A6", "#3B82F6", "#EC4899", "#FACC15", "#F8FAFC"]

_cache = {}


def _principled(mat):
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    return nt, bsdf


def solid(name, hex_color, rough=0.6, metallic=0.0, emission=0.0):
    key = ("solid", name)
    if key in _cache:
        return _cache[key]
    m = bpy.data.materials.new(name)
    nt, b = _principled(m)
    b.inputs["Base Color"].default_value = lin(hex_color)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metallic
    if emission:
        b.inputs["Emission Color"].default_value = lin(hex_color)
        b.inputs["Emission Strength"].default_value = emission
    m.diffuse_color = lin(hex_color)
    _cache[key] = m
    return m


def _ramp(nt, colors, location):
    cr = nt.nodes.new("ShaderNodeValToRGB")
    cr.location = location
    ramp = cr.color_ramp
    ramp.interpolation = "CONSTANT"
    n = len(colors)
    while len(ramp.elements) < n:
        ramp.elements.new(0.5)
    for i, el in enumerate(ramp.elements):
        el.position = i / n
        el.color = lin(colors[i])
    return cr


def instancer_palette(name, colors, channel, rough=0.65):
    """Material whose colour is picked per character instance.

    Each crowd member is a collection instance (an Empty). The Empty's object colour
    (RGBA) stores four 0–1 keys: R=skin, G=shirt, B=shorts, A=hair. The Attribute
    node (type INSTANCER) reads them, so every part of one character shares a colour.
    """
    key = ("pal", name)
    if key in _cache:
        return _cache[key]
    m = bpy.data.materials.new(name)
    nt, b = _principled(m)
    attr = nt.nodes.new("ShaderNodeAttribute")
    attr.attribute_type = "INSTANCER"
    attr.attribute_name = "color"
    attr.location = (-700, 0)
    if channel == "A":
        src = attr.outputs["Alpha"]
    else:
        sep = nt.nodes.new("ShaderNodeSeparateColor")
        sep.location = (-500, 0)
        nt.links.new(attr.outputs["Color"], sep.inputs["Color"])
        src = sep.outputs[{"R": "Red", "G": "Green", "B": "Blue"}[channel]]
    cr = _ramp(nt, colors, (-300, 0))
    nt.links.new(src, cr.inputs["Fac"])
    nt.links.new(cr.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = rough
    m.diffuse_color = lin(colors[0])
    _cache[key] = m
    return m


def random_palette(name, colors, rough=0.55):
    """Colour picked per instance from Object Info > Random (props such as umbrellas)."""
    key = ("rnd", name)
    if key in _cache:
        return _cache[key]
    m = bpy.data.materials.new(name)
    nt, b = _principled(m)
    info = nt.nodes.new("ShaderNodeObjectInfo")
    info.location = (-600, 0)
    cr = _ramp(nt, colors, (-300, 0))
    nt.links.new(info.outputs["Random"], cr.inputs["Fac"])
    nt.links.new(cr.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = rough
    _cache[key] = m
    return m


def apply_color_management(scene):
    vs = scene.view_settings
    # "Standard" keeps the toy-like saturation of the palette; AgX greys it out.
    vs.view_transform = "Standard"
    vs.look = "None"
    vs.exposure = -0.2
