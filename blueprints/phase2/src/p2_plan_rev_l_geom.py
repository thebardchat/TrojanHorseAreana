"""Shared geometry + area arithmetic for P2-T-017 (D-081): P2-A-101 Rev L, P2-A-102 Rev H, P2-G-003 Rev L.

No sheet output of its own. Base = the plan file named in phase2_plan_rev_l.yaml meta.base_plan (phase2_plan_rev_i.yaml, as the approved
P2-A-101 Rev K / A-102 Rev G DXFs); overrides = phase2_plan_rev_k.yaml (envelope R,
ST-3, ST-4, moved exits), phase2_plan_rev_g_l2.yaml (L2 loop corner) and phase2_plan_rev_l.yaml (29 ft ST-2 drum, bay x 134-164).
The Rev K / G baseline is recomputed here from the same files and checked against D-079 (57,520 / 28,692 / 86,212).
"""
import math
import os

import yaml
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
PAR = os.path.join(ROOT, "blueprints", "params")


def _y(name):
    with open(os.path.join(PAR, name), encoding="utf-8") as f:
        return yaml.safe_load(f)


L = _y("phase2_plan_rev_l.yaml")
J = _y(L["meta"]["base_plan"])
K = _y("phase2_plan_rev_k.yaml")
G = _y("phase2_plan_rev_g_l2.yaml")
R = K["envelope"]["corner_radius_ft"]


def rrect(x0, y0, x1, y1, r, n=24):
    pts = []
    for cx, cy, a0 in [(x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180), (x1 - r, y0 + r, 270)]:
        for i in range(n + 1):
            a = math.radians(a0 + 90.0 * i / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return Polygon(pts)


# ---------------------------------------------------------------- envelopes (Rev K/G tower vs Rev L drum)
ring = rrect(0, 0, 210, 252, R)
TW_K = K["stairs"]["ST-2"]
tower_k = Point(*TW_K["centre"]).buffer(TW_K["radius_ft"], 64)
env_k = unary_union([ring, tower_k])
DR = L["stairs"]["ST-2"]
DC = tuple(DR["centre"])
D_DIA = DR["diameter_ft"]
drum = Point(*DC).buffer(D_DIA / 2.0, 64)
env = unary_union([ring, drum])

ST1 = box(*[s for s in J["vertical"]["stairs"] if s["id"] == "ST-1"][0]["rect"])
ST3 = box(*K["stairs"]["ST-3"]["rect"])
ST4 = box(*K["stairs"]["ST-4"]["rect"])
stairs_k = unary_union([ST1, ST3, ST4, tower_k])
stairs_l = unary_union([ST1, ST3, ST4, drum])
ANNEX = box(*J["building"]["annex"]["rect"])
BUMP = box(*J["building"]["bumpout"]["rect"])
BAY_K = box(*K["mech_bay"]["rect"])
BAY = box(*L["mech_bay"]["rect"])

# ---------------------------------------------------------------- areas
open_ob = [box(*o["rect"]) for o in J["level_2"]["open_below"]]
OB_SF = sum(g.area for g in open_ob)
L1_K = round(unary_union([env_k, ANNEX, BAY_K, BUMP]).area)
L2_K = round(env_k.area - OB_SF)
TOT_K = L1_K + L2_K                           # totals = sum of the rounded levels (as D-079: 57,520 + 28,692)
L1_L = round(unary_union([env, ANNEX, BAY, BUMP]).area)
L2_L = round(env.area - OB_SF)
TOT_L = L1_L + L2_L
BASE = L["baseline"]["rev_kg"]
G3K = L["baseline"]["g003_k"]
EXPECT = L["baseline"]["expected_by_request"]
PROG = L["program_rev_k"]
assert (L1_K, L2_K, TOT_K) == (BASE["l1_footprint_sf"], BASE["l2_area_sf"], BASE["total_gsf"]), (L1_K, L2_K, TOT_K)

# ---------------------------------------------------------------- rooms (net of stairs, inside the envelope)
BUMP_ROOMS = set()                          # Rev K draws the bump-out as one block (rooms 25-27), as here
L1_ROOMS = [r for r in J["level_1"]["rooms"] if r["id"] not in set(L["meta"]["skip_l1_rooms"])]


def l1_area(r, envelope, stairs):
    g = box(*r["rect"])
    if r["id"] in BUMP_ROOMS:
        return g.area
    return g.intersection(envelope).difference(stairs).area


l1_sched = [(int(r["tag"]), r["name"], l1_area(r, env_k, stairs_k), l1_area(r, env, stairs_l)) for r in L1_ROOMS]
l1_sched += [(24, "CHAIR / TABLE / STAGE STORAGE", ANNEX.area, ANNEX.area), (25, "RESTROOM POP-OUT (25-27)", BUMP.area, BUMP.area),
             (29, "MECH / ELEC BAY", BAY_K.area, BAY.area)]
l1_sched.sort(key=lambda t: t[0])
l1_changed = [t for t in l1_sched if abs(t[3] - t[2]) > 0.5]
# leftover of the Rev F-J ST-2 strip inside the box (x 185.9-210, y 246-252): not a room on Rev K or Rev L
old_st2 = box(*[s for s in J["vertical"]["stairs"] if s["id"] == "ST-2"][0]["rect"])
old_st2_left = old_st2.intersection(ring).difference(drum).area

# ---------------------------------------------------------------- Level 2
lo, li = J["level_2"]["loop"]["outer"], J["level_2"]["loop"]["inner"]
CX, CY = G["loop_corner"]["centre"]
RI = G["loop_corner"]["inner_radius_ft"]
inner_round = box(*li).difference(box(CX, CY, li[2], li[3]).difference(Point(CX, CY).buffer(RI, 64)))
loop = box(*lo).intersection(env).difference(inner_round)
loop_k = box(*lo).intersection(env_k).difference(inner_round)
stretch = box(*L["level_2"]["stretch_n"]["rect"]).intersection(env).difference(drum)
landing = box(*L["level_2"]["landing"]["rect"]).intersection(env).difference(drum)
stretch_k = box(*G["stretch_n"]["rect"]).intersection(env_k).difference(tower_k)
landing_k = box(*G["landing"]["rect"]).intersection(env_k).difference(tower_k)
UP = [(b["side"], box(*b["rect"])) for b in J["tiers"]["upper"]["bands"]]
L2_ROOMS = {r["id"]: r for r in J["level_2"]["rooms"]}
L2_ZONES = {z["id"]: z for z in J["level_2"]["zones"]}


def l2_area(g, envelope, stairs):
    return g.intersection(envelope).difference(stairs).area


l2_sched = []
for rid, nm in (("sc", "Strength & Conditioning"), ("xt", "Cross-Training Mat"), ("rr_m2", "Men"), ("rr_w2", "Women"), ("admin", "Admin")):
    g = box(*L2_ROOMS[rid]["rect"])
    l2_sched.append((L2_ROOMS[rid]["tag"], nm, l2_area(g, env_k, stairs_k), l2_area(g, env, stairs_l)))
for zid, nm in (("l2corr", "L2 Corridor"), ("conc_e2", "Upper Concourse (E)")):
    g = box(*L2_ZONES[zid]["rect"])
    l2_sched.append(("—", nm, l2_area(g, env_k, stairs_k), l2_area(g, env, stairs_l)))
l2_sched.append(("—", "Stretch / Warm-up (N)", stretch_k.area, stretch.area))
l2_sched.append(("—", "ST-2 landing / NE corner (not programmed)", landing_k.area, landing.area))
l2_sched.append(("—", "Running / training loop", loop_k.area, loop.area))

# ---------------------------------------------------------------- stair fit in the drum
SW_, SL_ = L["stairs"]["stair_in_drum"]["size_ft"][1], L["stairs"]["stair_in_drum"]["size_ft"][0]
DIAG = math.hypot(SW_, SL_)
D_IN = D_DIA - DR["wall_allowance_ft"]
FIT_MARGIN = D_IN - DIAG                      # total, ft (corner clearance each end = half)
stair_rect = box(DC[0] - SL_ / 2, DC[1] - SW_ / 2, DC[0] + SL_ / 2, DC[1] + SW_ / 2)
stair_in_drum = Point(*DC).buffer(D_IN / 2.0, 128).contains(stair_rect)
# 20 ft tower (Rev K): room for a 12.67 ft wide stair
MAXLEN_K = math.sqrt((2 * TW_K["radius_ft"]) ** 2 - SW_ ** 2)

# ---------------------------------------------------------------- doors + exit checks
ang = math.radians(L["level_2"]["drum_door"]["angle_deg"])
DOOR = (DC[0] + D_DIA / 2 * math.cos(ang), DC[1] + D_DIA / 2 * math.sin(ang))
door_to_loop = (DOOR[1] - lo[3]) / abs(math.sin(ang))          # along the door normal to the loop's north edge
X6 = tuple(L["exits"]["X6"]["at"])
x6_on_drum = drum.boundary.distance(Point(*X6)) < 0.6
x6_outside_box = X6[1] > 252 or X6[0] > 210
x6_clear = Point(*X6).buffer(64 / 24.0).intersection(unary_union([BAY, ANNEX])).area == 0
EXN = [z["rect"] for z in J["level_1"]["zones"] if z["id"] == "exit_n"][0]       # EXIT (N) passage, X5
x5_gap_bay = BAY.bounds[0] - EXN[2]
x5_gap_annex = EXN[0] - ANNEX.bounds[2]
x5_lane = BAY.bounds[0] - ANNEX.bounds[2]
drum_bay_gap = drum.distance(BAY)
drum_west = DC[0] - D_DIA / 2

# L2 travel (P2-G-002 Rev E method: loop centreline, nearest stair entry + link + 15 ft seat access)
perim = LineString([(52.5, 37.5), (206.5, 37.5), (206.5, 242.5), (52.5, 242.5), (52.5, 37.5)])
entries = {"ST-1": Point(52.5, 240), "ST-2": Point(DOOR[0], 242.5), "ST-3": Point(190, 37.5), "ST-4": Point(52.5, 37.5)}
link = {"ST-1": 3.5 + 6.0, "ST-2": (DOOR[1] - 242.5) + 3.0, "ST-3": 16.5 + 10.0, "ST-4": 40.0 + 6.0}
PL = perim.length
worst, worst_at = 0.0, None
for i in range(0, int(PL), 2):
    p = perim.interpolate(i)
    best = 1e9
    for k_, e in entries.items():
        dd = abs(perim.project(e) - i)
        dd = min(dd, PL - dd)
        best = min(best, dd + link[k_])
    if best > worst:
        worst, worst_at = best, (round(p.x), round(p.y))
TRAVEL = worst + 15.0
door_pts = {"ST-1": (42.667, 240), "ST-2": DC, "ST-3": (183.667, 12), "ST-4": (6.3, 32)}
DIAG_BLDG = math.hypot(210, 252)
pairs = []
ks = list(door_pts)
for i in range(4):
    for j in range(i + 1, 4):
        a, b = door_pts[ks[i]], door_pts[ks[j]]
        pairs.append((ks[i], ks[j], math.hypot(a[0] - b[0], a[1] - b[1])))
SEP_MIN = min(p[2] for p in pairs)


def true_circle_dxf(path, P, S, layers=("A-STAIR", "A-WALL-EXT")):
    """D-074 language: write the ST-2 drum into the DXF as a true CIRCLE / ARC (the PDF draws it as a 256-segment polygon).

    Replaces the drum's polyline (+ its hatch) on A-STAIR with a CIRCLE + circular hatch, and the drum's outline segments on
    A-WALL-EXT with one ARC. Areas are measured on the shapely polygon (difference to a true circle < 0.1 SF)."""
    import ezdxf
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()
    cx, cy = P(*DC)
    r = D_DIA / 2.0 * S
    tol = 0.002

    def on_c(x, y):
        return abs(math.hypot(x - cx, y - cy) - r) < tol

    hatch_drop, angles = [], []
    for e in list(msp):
        lay, t = e.dxf.layer, e.dxftype()
        if t == "LWPOLYLINE" and lay == "A-STAIR":
            pts = list(e.get_points("xy"))
            if len(pts) > 64 and all(on_c(x, y) for x, y in pts):
                msp.delete_entity(e)
                hatch_drop.append(True)
        elif t == "HATCH" and lay == "A-STAIR":
            for bp in e.paths:
                vs = getattr(bp, "vertices", None)
                if vs and len(vs) > 64 and all(on_c(v[0], v[1]) for v in vs):
                    fill = e.dxf.get("true_color")
                    msp.delete_entity(e)
                    h = msp.add_hatch(dxfattribs={"layer": "A-STAIR"})
                    if fill is not None:
                        h.dxf.true_color = fill
                    h.paths.add_edge_path().add_arc((cx, cy), r, 0, 360)
                    break
        elif t == "LINE" and lay == "A-WALL-EXT":
            (x1, y1), (x2, y2) = (e.dxf.start.x, e.dxf.start.y), (e.dxf.end.x, e.dxf.end.y)
            if on_c(x1, y1) and on_c(x2, y2):
                angles += [math.degrees(math.atan2(y1 - cy, x1 - cx)) % 360, math.degrees(math.atan2(y2 - cy, x2 - cx)) % 360]
                msp.delete_entity(e)
    if hatch_drop:
        msp.add_circle((cx, cy), r, dxfattribs={"layer": "A-STAIR"})
    if angles:
        # outline arc runs over the outside of the drum: the gap (inside the ring) is the largest jump between sorted angles
        a = sorted(set(round(v, 6) for v in angles))
        gaps = [((a[(i + 1) % len(a)] - a[i]) % 360, i) for i in range(len(a))]
        g_, i = max(gaps)
        start, end = a[(i + 1) % len(a)], a[i]
        msp.add_arc((cx, cy), r, start, end, dxfattribs={"layer": "A-WALL-EXT"})
    doc.saveas(path)
