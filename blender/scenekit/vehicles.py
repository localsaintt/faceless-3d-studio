"""Low-poly stylised vehicles. Local forward = +X. Paint colour per instance (object colour R)."""
from . import geo, style

CAR_PAINT = ["#E5484D", "#F59E0B", "#FACC15", "#14B8A6", "#3B82F6", "#F8FAFC", "#1F2937", "#EC4899", "#84CC16", "#A3A3A3"]


def _mats():
    return {
        "paint": style.instancer_palette("car_paint", CAR_PAINT, "R", rough=0.3),
        "glass": style.solid("car_glass", "#22394A", 0.08),
        "tyre": style.solid("tyre", "#1A1A1A", 0.8),
        "chrome": style.solid("chrome", "#D7DCE0", 0.25, metallic=0.8),
        "light": style.solid("headlight", "#FFF6D8", 0.2, emission=1.5),
        "white": style.solid("truck_white", "#F7F5F0", 0.5),
        "pink": style.solid("truck_pink", "#F9A8D4", 0.5),
        "teal": style.solid("truck_teal", "#5EEAD4", 0.5),
        "cone": style.solid("cone_wafer", "#E0B36A", 0.7),
        "scoop": style.solid("scoop", "#FBCFE8", 0.6),
    }


def _wheels(name, coll, m, xs, half_width, r=0.36):
    C = geo.cylinder(14)
    for x in xs:
        for s in (-1, 1):
            geo.obj(f"{name}_wheel", C, coll, (x, s * half_width, r), (r, r, 0.22), (1.5708, 0, 0), mat=m["tyre"])


def build_car(lib, name, length=4.3, width=1.85, height=0.7, cabin=(2.2, 0.62), cabin_x=-0.15):
    coll = geo.new_collection(name, parent=lib)
    m = _mats()
    S, C = geo.sphere(16, 10), geo.cube()
    geo.obj(f"{name}_body", C, coll, (0, 0, 0.36 + height / 2), (length, width, height), mat=m["paint"])
    geo.obj(f"{name}_nose", S, coll, (length / 2 - 0.05, 0, 0.36 + height / 2), (0.25, width / 2, height / 2), mat=m["paint"])
    geo.obj(f"{name}_tail", S, coll, (-length / 2 + 0.05, 0, 0.36 + height / 2), (0.2, width / 2, height / 2), mat=m["paint"])
    cl, ch = cabin
    geo.obj(f"{name}_cabin", S, coll, (cabin_x, 0, 0.36 + height + ch * 0.35), (cl / 2, width / 2 * 0.92, ch), mat=m["glass"])
    geo.obj(f"{name}_roof", C, coll, (cabin_x, 0, 0.36 + height + ch * 0.82), (cl * 0.75, width * 0.86, 0.08), mat=m["paint"])
    for s in (-1, 1):
        geo.obj(f"{name}_lamp", S, coll, (length / 2 + 0.12, s * width * 0.33, 0.36 + height * 0.62), (0.06, 0.16, 0.08), mat=m["light"])
    _wheels(name, coll, m, (length * 0.32, -length * 0.32), width / 2)
    return coll


def build_truck(lib, name="icecream_truck"):
    """Generic ice-cream truck: white box, pastel stripes, a giant cone on the roof (no brand)."""
    coll = geo.new_collection(name, parent=lib)
    m = _mats()
    S, C = geo.sphere(16, 10), geo.cube()
    geo.obj("tr_box", C, coll, (-0.6, 0, 1.75), (4.4, 2.2, 2.3), mat=m["white"])
    geo.obj("tr_cab", C, coll, (2.35, 0, 1.25), (1.6, 2.1, 1.3), mat=m["white"])
    geo.obj("tr_windshield", C, coll, (3.1, 0, 1.75), (0.1, 1.8, 0.6), mat=m["glass"])
    for s in (-1, 1):
        geo.obj("tr_stripe_p", C, coll, (-0.6, s * 1.11, 1.25), (4.4, 0.02, 0.28), mat=m["pink"])
        geo.obj("tr_stripe_t", C, coll, (-0.6, s * 1.11, 1.6), (4.4, 0.02, 0.14), mat=m["teal"])
        geo.obj("tr_window", C, coll, (-0.4, s * 1.115, 2.2), (2.0, 0.02, 0.7), mat=m["glass"])
    geo.obj("tr_cone", geo.cone(12), coll, (-0.6, 0, 3.55), (0.35, 0.35, 0.9), (3.1416, 0, 0), mat=m["cone"])
    geo.obj("tr_scoop", S, coll, (-0.6, 0, 4.15), (0.42, 0.42, 0.38), mat=m["scoop"])
    _wheels("tr", coll, m, (2.2, -1.9), 1.1, r=0.42)
    return coll


def build_library(lib):
    return {
        "car": [build_car(lib, "car_sedan"),
                build_car(lib, "car_hatch", length=3.8, cabin=(1.9, 0.68), cabin_x=-0.3),
                build_car(lib, "car_suv", length=4.6, height=0.95, cabin=(2.6, 0.62), cabin_x=-0.4)],
        "truck": build_truck(lib),
    }
