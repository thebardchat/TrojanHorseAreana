"""Shared geometry + area arithmetic for P2-A-101 Rev M, P2-A-102 Rev I, P2-G-003 Rev M (D-082 30 ft drum, D-083 drum door,
D-084 east side = plan Rev J). No sheet output of its own.

Base = params/phase2_plan_rev_j.yaml (plan Rev J, D-072, Set Rev D); overrides = phase2_plan_rev_k.yaml (envelope R, ST-3, ST-4, moved exits),
phase2_plan_rev_g_l2.yaml (L2 loop corner) and phase2_plan_rev_m.yaml. Rev L / H numbers come from p2_plan_rev_l_geom.py and are checked
against the Rev L baseline in phase2_plan_rev_m.yaml.
"""
import math
import os
import sys

import yaml
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import p2_plan_rev_l_geom as gl  # noqa: E402  (Rev L / H = previous revision)

ROOT = gl.ROOT
PAR = gl.PAR


def _y(name):
    with open(os.path.join(PAR, name), encoding="utf-8") as f:
        return yaml.safe_load(f)


M = _y("phase2_plan_rev_m.yaml")
J = _y(M["meta"]["base_plan"])
K, G = gl.K, gl.G
R = gl.R
rrect, ring = gl.rrect, gl.ring

# ---------------------------------------------------------------- envelope with the 30 ft drum
DR = M["stairs"]["ST-2"]
DC = tuple(DR["centre"])
D_DIA = DR["diameter_ft"]
RAD = D_DIA / 2.0
drum = Point(*DC).buffer(RAD, 64)
env = unary_union([ring, drum])
ST1 = box(*[s for s in J["vertical"]["stairs"] if s["id"] == "ST-1"][0]["rect"])
ST3, ST4 = gl.ST3, gl.ST4
stairs_m = unary_union([ST1, ST3, ST4, drum])
ANNEX = box(*J["building"]["annex"]["rect"])
BUMP = box(*J["building"]["bumpout"]["rect"])
BUMP_L = gl.BUMP                                   # Rev L (plan Rev I) bump-out position, for the ghost
BAY = box(*M["mech_bay"]["rect"])

# ---------------------------------------------------------------- areas
open_ob = [box(*o["rect"]) for o in J["level_2"]["open_below"]]
OB_SF = sum(g_.area for g_ in open_ob)
L1_M = round(unary_union([env, ANNEX, BAY, BUMP]).area)
L2_M = round(env.area - OB_SF)
TOT_M = L1_M + L2_M
BL, BD = M["baseline"]["rev_lh"], M["baseline"]["set_rev_d"]
L1_L, L2_L, TOT_L = gl.L1_L, gl.L2_L, gl.TOT_L
assert (L1_L, L2_L, TOT_L) == (BL["l1_footprint_sf"], BL["l2_area_sf"], BL["total_gsf"]), (L1_L, L2_L, TOT_L)
assert abs(OB_SF - gl.OB_SF) < 1e-6
PROG = M["program_rev_k"]

# ---------------------------------------------------------------- rooms
BUMP_ROOMS = set(M["meta"]["bump_rooms"])
L1_ROOMS = [r for r in J["level_1"]["rooms"] if r["id"] not in set(M["meta"]["skip_l1_rooms"])]


def l1_geo(r):
    g_ = box(*r["rect"])
    return g_ if r["id"] in BUMP_ROOMS else g_.intersection(env).difference(stairs_m)


l1_sched = sorted([(int(r["tag"]), r["name"], l1_geo(r).area) for r in L1_ROOMS] +
                  [(24, "CHAIR / TABLE / STAGE STORAGE", ANNEX.area), (29, "MECH / ELEC BAY", BAY.area)], key=lambda t: t[0])
# Rev L room areas (plan Rev I east side) for the change table
l1_prev = {t: a1 for t, n, a0, a1 in gl.l1_sched}
old_st2 = box(*[s for s in J["vertical"]["stairs"] if s["id"] == "ST-2"][0]["rect"])
old_st2_left = old_st2.intersection(ring).difference(drum).area

# ---------------------------------------------------------------- Level 2
lo, li = J["level_2"]["loop"]["outer"], J["level_2"]["loop"]["inner"]
CX, CY, RI = gl.CX, gl.CY, gl.RI
loop = box(*lo).intersection(env).difference(gl.inner_round)
stretch = box(*M["level_2"]["stretch_n"]["rect"]).intersection(env).difference(drum)
landing = box(*M["level_2"]["landing"]["rect"]).intersection(env).difference(drum)
UP = gl.UP
L2_ROOMS = {r["id"]: r for r in J["level_2"]["rooms"]}
L2_ZONES = {z["id"]: z for z in J["level_2"]["zones"]}
l2_sched = []
prev = {n: a1 for t, n, a0, a1 in gl.l2_sched}
for rid, nm in (("sc", "Strength & Conditioning"), ("xt", "Cross-Training Mat"), ("rr_m2", "Men"), ("rr_w2", "Women"), ("admin", "Admin")):
    l2_sched.append((L2_ROOMS[rid]["tag"], nm, prev[nm], box(*L2_ROOMS[rid]["rect"]).intersection(env).difference(stairs_m).area))
for zid, nm in (("l2corr", "L2 Corridor"), ("conc_e2", "Upper Concourse (E)")):
    l2_sched.append(("—", nm, prev[nm], box(*L2_ZONES[zid]["rect"]).intersection(env).difference(stairs_m).area))
l2_sched.append(("—", "Stretch / Warm-up (N)", prev["Stretch / Warm-up (N)"], stretch.area))
l2_sched.append(("—", "ST-2 landing / NE corner (not programmed)", prev["ST-2 landing / NE corner (not programmed)"], landing.area))
l2_sched.append(("—", "Running / training loop", prev["Running / training loop"], loop.area))

# ---------------------------------------------------------------- stair fit (D-082)
SL_, SW_ = M["stairs"]["stair_in_drum"]["size_ft"]
DIAG = math.hypot(SW_, SL_)
D_IN = D_DIA - DR["wall_allowance_ft"]
FIT_MARGIN = D_IN - DIAG
FIT_PREV = gl.FIT_MARGIN
stair_rect = box(DC[0] - SL_ / 2, DC[1] - SW_ / 2, DC[0] + SL_ / 2, DC[1] + SW_ / 2)
assert Point(*DC).buffer(D_IN / 2.0, 128).contains(stair_rect)

# ---------------------------------------------------------------- drum door + landing (D-083, IBC 2021 1010.1.5)
DD = M["level_2"]["drum_door"]
LR = M["level_2"]["door_landing_rule"]
ANG = DD["angle_deg"]
_t = math.radians(ANG)
NRM = (math.cos(_t), math.sin(_t))
DOOR = (DC[0] + RAD * NRM[0], DC[1] + RAD * NRM[1])
HALF = math.degrees(math.asin(DD["width_in"] / 24.0 / RAD))
JAMB_W = (DC[0] + RAD * math.cos(math.radians(ANG - HALF)), DC[1] + RAD * math.sin(math.radians(ANG - HALF)))
JAMB_E = (DC[0] + RAD * math.cos(math.radians(ANG + HALF)), DC[1] + RAD * math.sin(math.radians(ANG + HALF)))
door_inside = max(JAMB_W[1], JAMB_E[1]) <= 252.0 + 1e-6
LOOP_EDGE = lo[3]
CL_CENTRE_IN = (DOOR[1] - LOOP_EDGE) / abs(NRM[1]) * 12           # along the door's normal, door centre to the loop edge
_tp = math.radians(gl.L["level_2"]["drum_door"]["angle_deg"])
_dl = (gl.DC[1] + gl.D_DIA / 2 * math.sin(_tp))
CL_CENTRE_PREV_IN = (_dl - LOOP_EDGE) / abs(math.sin(_tp)) * 12     # Rev H, same measure
# full landing: 76 in wide (perpendicular to travel) x 44 in deep, square to the door, from the door chord
mid = ((JAMB_W[0] + JAMB_E[0]) / 2, (JAMB_W[1] + JAMB_E[1]) / 2)
TG = (-NRM[1], NRM[0])
W_, D_ = LR["min_width_in"] / 12.0, LR["min_length_in"] / 12.0
p1 = (mid[0] - TG[0] * W_ / 2, mid[1] - TG[1] * W_ / 2)
p2 = (mid[0] + TG[0] * W_ / 2, mid[1] + TG[1] * W_ / 2)
land = Polygon([p1, p2, (p2[0] + NRM[0] * D_, p2[1] + NRM[1] * D_), (p1[0] + NRM[0] * D_, p1[1] + NRM[1] * D_)]).difference(drum)
land_out_bldg = land.difference(env).area                     # SF outside the building (west corner past the north wall)
land_in_loop = land.intersection(box(-10, -10, 300, LOOP_EDGE)).area
LOOP_INTRUDE_IN = max(0.0, LOOP_EDGE - land.bounds[1]) * 12
STRIP_ONLY_EAST_JAMB_IN = (JAMB_E[1] - LOOP_EDGE) * 12         # N-S, east jamb to the loop edge (shallowest point of the strip)

# ---------------------------------------------------------------- L2 travel + separation (Rev E method)
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
TRAVEL_L2 = worst + 15.0
door_pts = {"ST-1": (42.667, 240), "ST-2": DC, "ST-3": (183.667, 12), "ST-4": (6.3, 32)}
DIAG_BLDG = math.hypot(210, 252)
pairs = []
ks = list(door_pts)
for i in range(4):
    for j in range(i + 1, 4):
        a, b = door_pts[ks[i]], door_pts[ks[j]]
        pairs.append((ks[i], ks[j], math.hypot(a[0] - b[0], a[1] - b[1])))
SEP_MIN = min(p[2] for p in pairs)

# ---------------------------------------------------------------- exits on the L1 perimeter (X6 + D-084 east side)
X6 = tuple(M["exits"]["X6"]["at"])
x6_on_drum = drum.boundary.distance(Point(*X6)) < 0.6
x6_clear = Point(*X6).buffer(64 / 24.0).intersection(unary_union([BAY, ANNEX])).area == 0
EXN = [z["rect"] for z in J["level_1"]["zones"] if z["id"] == "exit_n"][0]
x5_lane = BAY.bounds[0] - ANNEX.bounds[2]
x5_gap_bay = BAY.bounds[0] - EXN[2]
drum_bay_gap = drum.distance(BAY)
DOORS = {d["id"]: d for d in J["level_1"]["doors"]["items"]}
ES = M["east_side_checks"]
LIM = ES["limits"]


def plen(pts):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


east = {}
for pth in ES["paths"]:
    pts = pth["pts"]
    east[pth["id"]] = dict(total=plen(pts), common=plen(pts[:pth["branch_at"] + 1]) if "branch_at" in pth else None, label=pth["label"])
env_b = env.boundary
east_doors = {}
for did in ("X7", "X11", "X8"):
    y_ = DOORS[did]["at"]
    on_straight = R <= y_ - 64 / 24.0 and y_ + 64 / 24.0 <= 252 - R      # whole 64 in door on the straight east wall
    hit_bump = box(209.5, y_ - 64 / 24.0, 210.5, y_ + 64 / 24.0).intersection(BUMP).area > 0
    east_doors[did] = dict(y=y_, on_wall=env_b.distance(Point(210, y_)) < 0.6 and on_straight, clear_of_bump=not hit_bump)
X7_GAP_BUMP = (DOORS["X7"]["at"] - 64 / 24.0) - BUMP.bounds[3]           # X7 jamb to the bump-out north face
PC = [z["rect"] for z in J["level_1"]["zones"] if z["id"] == "pc_e"][0]
CORR_IN = (PC[2] - PC[0]) * 12
DEAD_END = PC[3] - ES["women_door_y"][1]
pc_inside = env.contains(box(*PC))
bump_on_wall = BUMP.bounds[0] == 210 and R <= BUMP.bounds[1] and BUMP.bounds[3] <= 252 - R


def true_circle_dxf(path, P, S):
    """Drum as a true CIRCLE / ARC in the DXF (D-074), same method as Rev L / H."""
    save = (gl.DC, gl.D_DIA)
    gl.DC, gl.D_DIA = DC, D_DIA
    try:
        gl.true_circle_dxf(path, P, S)
    finally:
        gl.DC, gl.D_DIA = save
