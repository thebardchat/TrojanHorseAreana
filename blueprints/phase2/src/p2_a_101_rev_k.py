#!/usr/bin/env python3
"""P2-A-101 Rev K: Level 1 block plan inside the radiused concept envelope (D-074 / D-077).

New file; Rev J (and the frozen Set Rev D) are not touched. Geometry = params/phase2_plan_rev_i.yaml (Rev J) with the
overrides in params/phase2_plan_rev_k.yaml. Output: PDF + DXF through the KEYSTONE sheet kit (shared/titleblock.py).

  python blueprints/phase2/src/p2_a_101_rev_k.py            (run from the repo root)
"""
import math
import os
import sys

import yaml
from shapely.geometry import Point, Polygon, box
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "blueprints", "shared"))
from titleblock import Sheet, add_titleblock, text_width_in  # noqa: E402

J = yaml.safe_load(open(os.path.join(ROOT, "blueprints", "params", "phase2_plan_rev_i.yaml"), encoding="utf-8"))
K = yaml.safe_load(open(os.path.join(ROOT, "blueprints", "params", "phase2_plan_rev_k.yaml"), encoding="utf-8"))
R = K["envelope"]["corner_radius_ft"]

# ---------------------------------------------------------------- geometry (feet)
def rrect(x0, y0, x1, y1, r, n=24):
    pts = []
    for cx, cy, a0 in [(x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180), (x1 - r, y0 + r, 270)]:
        for i in range(n + 1):
            a = math.radians(a0 + 90.0 * i / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return Polygon(pts)


ring = rrect(0, 0, 210, 252, R)
tw = K["stairs"]["ST-2"]
tower = Point(*tw["centre"]).buffer(tw["radius_ft"], 48)
envelope = unary_union([ring, tower])
ST3 = box(*K["stairs"]["ST-3"]["rect"])
ST4 = box(*K["stairs"]["ST-4"]["rect"])
BAY = box(*K["mech_bay"]["rect"])
ANNEX = box(*J["building"]["annex"]["rect"])
BUMP = box(*J["building"]["bumpout"]["rect"])

SKIP = {"storage_annex", "rr_mb", "rr_wb", "df_jan"}
rooms = {r["id"]: r for r in J["level_1"]["rooms"] if r["id"] not in SKIP}
zones = J["level_1"]["zones"]


def area(g):
    return g.area


# ---------------------------------------------------------------- areas
changed = []
for rid, r in rooms.items():
    g = box(*r["rect"])
    clip = g.intersection(envelope)
    if g.area - clip.area > 0.5:
        changed.append((r["tag"], r["name"], g.area, clip.area))
l1_envelope = envelope.area
l1_total = l1_envelope + ANNEX.area + BAY.area + BUMP.area
J_L1 = 56861.0
J_L2 = 28933.0
l2_rects = [box(*r["rect"]) for r in J["level_2"]["rooms"]] + [box(*z["rect"]) for z in J["level_2"]["zones"]]
lo, li = J["level_2"]["loop"]["outer"], J["level_2"]["loop"]["inner"]
l2_rects.append(box(*lo).difference(box(*li)))
l2_union = unary_union(l2_rects)
l2_loss = l2_union.area - l2_union.intersection(envelope).area
K_L2 = J_L2 - l2_loss
K_TOT = l1_total + K_L2
J_TOT = J_L1 + J_L2

# ---------------------------------------------------------------- sheet
W, H = 17.0, 11.0
sh = Sheet(W, H)
top = add_titleblock(sh, dict(
    project="Hazel Green Regional Athletic Complex\nTrojan Horse Arena · Hazel Green area, Madison County, Alabama (site TBD, D-006)",
    phase="PHASE 2", title="OVERALL FLOOR PLAN\nLEVEL 1 · BLOCK PLAN", scale="1\" =\n40'-0\"", date="October\n2026",
    revision="K", drawn_by="Drawn by Claude (AI) for\nShane Brazelton", sheet_no="P2-A-101",
    stamp="PRELIMINARY — CONCEPTUAL DESIGN — NOT FOR CONSTRUCTION"))

S = 1.0 / 40.0          # inches per foot
OX, OY = 1.05, top + 0.55   # plan origin (feet 0,0) on the sheet; y grows up


def P(x, y):
    return OX + x * S, OY + y * S


def poly(g, fill=None, lw=0.6, layer="A-ROOM"):
    geoms = [g] if g.geom_type == "Polygon" else list(g.geoms)
    for gg in geoms:
        sh.poly([P(x, y) for x, y in gg.exterior.coords], fill=fill, lw=lw, layer=layer)


def label(x, y, s, size=6, bold=False, rot=0, align="center"):
    px, py = P(x, y)
    sh.text(px, py - size / 72 * 0.35, s, size=size, bold=bold, align=align, rot=rot, layer="A-ANNO-TEXT")


# zones then rooms (clipped to the envelope)
for z in zones:
    poly(box(*z["rect"]).intersection(envelope), fill="#EFEDE6", lw=0.3)
for rid, r in rooms.items():
    g = box(*r["rect"]).intersection(envelope)
    poly(g, fill="#DAD6C9", lw=0.45)
# event floor, mats, tiers
ef = box(*J["event_floor"]["rect"])
for band in J["tiers"]["lower"]["bands"]:
    poly(box(*band["rect"]), fill="#E9B4B4", lw=0.4)
poly(ef, fill="#EAD9B5", lw=0.5)
for m in J["mats"]:
    ox, oy = m["origin"]
    poly(box(ox, oy, ox + 42, oy + 42), fill="#F4ECD0", lw=0.3)
    c = Point(ox + 21, oy + 21).buffer(14, 32)
    poly(c, fill="#C93A3A", lw=0.3)
# stairs (ghosts of Rev J dashed, Rev K solid)
for sid, g in (("ST-3", ST3), ("ST-4", ST4)):
    rx0, ry0, rx1, ry1 = [s for s in J["vertical"]["stairs"] if s["id"] == sid][0]["rect"]
    pts = [(rx0, ry0), (rx1, ry0), (rx1, ry1), (rx0, ry1), (rx0, ry0)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        (x1, y1), (x2, y2) = P(ax, ay), P(bx, by)
        sh.dashed(x1, y1, x2, y2, layer="A-ANNO-GHOST", lw=0.35)
    poly(g, fill="#B9B3A0", lw=0.9, layer="A-STAIR")
    label((g.bounds[0] + g.bounds[2]) / 2, (g.bounds[1] + g.bounds[3]) / 2, sid, size=5.5, bold=True, rot=90)
st1 = [s for s in J["vertical"]["stairs"] if s["id"] == "ST-1"][0]["rect"]
poly(box(*st1), fill="#B9B3A0", lw=0.9, layer="A-STAIR")
label((st1[0] + st1[2]) / 2, (st1[1] + st1[3]) / 2, "ST-1", size=5.5, bold=True, rot=90)
poly(tower, fill="#B9B3A0", lw=0.9, layer="A-STAIR")
label(tw["centre"][0], tw["centre"][1], "ST-2", size=6, bold=True)
# pop-outs
poly(ANNEX, fill="#8E949B", lw=1.0, layer="A-ANNEX")
poly(BAY, fill="#A55A5A", lw=1.0, layer="A-ANNEX")
poly(BUMP, fill="#8E949B", lw=1.0, layer="A-ANNEX")
# envelope outline on top
ext = envelope.exterior.coords
for (ax, ay), (bx, by) in zip(list(ext), list(ext)[1:]):
    (x1, y1), (x2, y2) = P(ax, ay), P(bx, by)
    sh.line(x1, y1, x2, y2, layer="A-WALL-EXT", lw=2.4)

# exits (symbols only, as Rev J; moved ones per phase2_plan_rev_k.yaml)
EXIT_FIX = {"X1": ("W", 0, 50.0), "X10": ("W", 0, 32.0), "X9": ("S", 183.667, 0), "X6": ("T", 188, 257.7)}
for d in J["level_1"]["doors"]["items"]:
    if d["id"] in ("S1",) or d["id"].startswith("E1"):
        continue
    wall, at = d["wall"], d["at"]
    if d["id"] in EXIT_FIX:
        wall, ex, ey = EXIT_FIX[d["id"]]
    elif wall == "S":
        ex, ey = at, 0
    elif wall == "N":
        ex, ey = at, 252
    elif wall == "W":
        ex, ey = 0, at
    else:
        ex, ey = d.get("x", 210), at
    px, py = P(ex, ey)
    out = {"S": (0, -0.16), "N": (0, 0.16), "W": (-0.16, 0), "E": (0.16, 0), "T": (0.16, 0.05)}[wall]
    sh.line(px, py, px + out[0] * 0.6, py + out[1] * 0.6, layer="A-EXIT", lw=2.2)
    sh.text(px + out[0] * 1.35, py + out[1] * 1.35 - 0.03, d["id"], size=5.5, bold=True, align="center")
# tags: room number at centre of each (clipped) room
for rid, r in rooms.items():
    g = box(*r["rect"]).intersection(envelope)
    c = g.representative_point()
    label(c.x, c.y, str(r["tag"]), size=6, bold=True)
label(116, 140, "EVENT FLOOR", size=8, bold=True)
label(116, 133, "120 x 144 ft · 4 x 42 ft mats", size=6)
label(87, 267, "24  CHAIR / TABLE / STAGE", size=5.5, bold=True)
label(87, 261, "STORAGE · 2,100 SF", size=5.5)
label(151, 270, "29  MECH / ELEC BAY", size=5.5, bold=True)
label(151, 264, "900 SF · NEW", size=5.5)
label(225, 189, "25 / 26 / 27", size=5.5, bold=True, rot=90)
label(84, 5, "E1 MAIN ENTRY", size=6, bold=True)
# dimensions
sx0, sy0 = P(0, -9)
sx1, _ = P(210, -9)
sh.line(sx0, sy0, sx1, sy0, layer="A-ANNO-DIMS", lw=0.5)
sh.text((sx0 + sx1) / 2, sy0 - 0.13, "210'-0\" (box; R = 20'-0\" corners)", size=7, align="center", layer="A-ANNO-DIMS")
dx, dy0 = P(-9, 0)
_, dy1 = P(-9, 252)
sh.line(dx, dy0, dx, dy1, layer="A-ANNO-DIMS", lw=0.5)
sh.text(dx - 0.1, (dy0 + dy1) / 2, "252'-0\"", size=7, align="center", rot=90, layer="A-ANNO-DIMS")
# north arrow + scale bar
nx, ny = P(252, 40)
sh.line(nx, ny, nx, ny + 0.5, layer="A-ANNO-TEXT", lw=1.0)
sh.line(nx, ny + 0.5, nx - 0.07, ny + 0.38, layer="A-ANNO-TEXT", lw=1.0)
sh.line(nx, ny + 0.5, nx + 0.07, ny + 0.38, layer="A-ANNO-TEXT", lw=1.0)
sh.text(nx, ny + 0.57, "N", size=10, bold=True, align="center")
sh.text(nx, ny - 0.15, "approx. · site TBD", size=6, align="center")

# ---------------------------------------------------------------- right panel
RX, RW = 8.05, 8.45
y = H - 0.85
sh.text(RX, y - 0.05, "SCHEMATIC — BLOCK PLAN, CONCEPT ENVELOPE", size=13, bold=True)
y -= 0.3
sh.text(RX, y, "LEVEL 1 — OVERALL FLOOR PLAN (REV K)", size=11, bold=True)
y -= 0.2
y = sh.para(RX, y, RW, "Rev J layout (frozen, D-073) inside the radiused SRM-language envelope approved at R = 20 ft (D-077). Rooms, tiers, mats, "
            "exits and areas are Rev J unless listed under CHANGES. Rev J dashed outlines show where the corner stairs were.", size=7.5)
y -= 0.12
sh.text(RX, y, "CHANGES FROM REV J (all ASSUMED)", size=9, bold=True)
y -= 0.05
changes = [
    "Envelope: 210 x 252 ft box with R = 20 ft corners (removes about %d SF per level at the four corners)." % round(
        210 * 252 - ring.area),
    "ST-3 (SE) slides west along the south wall to x 177.3-190; same 12.667 x 24.083 ft, exit X9 to x 183.7. Clears L2 WOMEN (2).",
    "ST-4 (SW) slides north along the west wall into the FLEX / TEAM ASSEMBLY zone (no program); exit X10 on the west wall; exit X1 moves to y 50 beside it.",
    "ST-2 (NE) is a 20 ft diameter cylindrical tower INSIDE the building envelope: the outline wraps it, it lands on the L2 loop "
    "north leg, exit X6 on its east face. Replaces the 24.08 x 6.67 ft NE projection.",
    "NEW 29 MECH / ELEC BAY 30 x 30 ft (900 SF), one storey, metal-building pop-out 14 ft east of the storage annex so the EXIT (N) passage at X5 stays clear (D-074).",
    "MECH (NW) and MECH (NE) lose corner area to the radius (below); the bay makes it up.",
]
for c in changes:
    y = sh.para(RX, y, RW, c, size=7.2, bullet="•", indent=0.14)
y -= 0.14
sh.text(RX, y, "ROOMS CHANGED (SF drawn)", size=9, bold=True)
y -= 0.2
cols = [RX, RX + 0.35, RX + 3.6, RX + 4.7, RX + 5.8]
for x, t in zip(cols, ["TAG", "ROOM", "REV J", "REV K", "CHANGE"]):
    sh.text(x, y, t, size=7, bold=True)
sh.line(RX, y - 0.04, RX + RW, y - 0.04, lw=0.5)
y -= 0.17
rows = [(str(t), n, a, c) for t, n, a, c in changed] + [("29", "MECH / ELEC BAY (new)", 0.0, BAY.area)]
for t, n, a, c in rows:
    for x, v in zip(cols, [t, n, f"{a:,.0f}", f"{c:,.0f}", f"{c - a:+,.0f}"]):
        sh.text(x, y, v, size=7)
    y -= 0.15
y -= 0.1
sh.text(RX, y, "AREA CHECK (no SF cap, D-056; L1, L2, total vs Rev J, D-057)", size=9, bold=True)
y -= 0.2
for x, t in zip([RX, RX + 3.0, RX + 4.4, RX + 5.8], ["", "REV J", "REV K", "CHANGE"]):
    sh.text(x, y, t, size=7, bold=True)
sh.line(RX, y - 0.04, RX + RW, y - 0.04, lw=0.5)
y -= 0.17
for lab, a, b in [("L1 footprint (envelope + annex + bay + bump-out)", J_L1, l1_total), ("L2 area", J_L2, K_L2),
                  ("TOTAL GSF", J_TOT, K_TOT)]:
    bold = lab.startswith("TOTAL")
    sh.text(RX, y, lab, size=7, bold=bold)
    for x, v in zip([RX + 3.0, RX + 4.4, RX + 5.8], [f"{a:,.0f}", f"{b:,.0f}", f"{b - a:+,.0f}"]):
        sh.text(x, y, v, size=7, bold=bold)
    y -= 0.15
y -= 0.05
y = sh.para(RX, y, RW, "L1 = envelope polygon (box with R = 20 ft corners + tower) %s SF + annex 2,100 + bay 900 + bump-out 1,680. "
            "L2 = Rev J 28,933 less %s SF where Rev J L2 rooms and the loop fall outside the radius; the tower is not added to L2 (ASSUMED, as the "
            "Rev J projection). Recompute on P2-G-003 Rev L." % (f"{l1_envelope:,.0f}", f"{l2_loss:,.0f}"), size=6.8)
y -= 0.16
sh.text(RX, y, "ROOM SCHEDULE — LEVEL 1 (SF inside the Rev K envelope)", size=9, bold=True)
y -= 0.18
sched = sorted(((int(r["tag"]), r["name"], box(*r["rect"]).intersection(envelope).area) for r in rooms.values()), key=lambda t: t[0])
sched.append((29, "MECH / ELEC BAY (new)", BAY.area))
sched.append((24, "CHAIR / TABLE / STAGE STORAGE", ANNEX.area))
sched.append((25, "RESTROOM POP-OUT (25-27)", BUMP.area))
sched = sorted(set(sched), key=lambda t: t[0])
half = (len(sched) + 1) // 2
y_top = y
for ci, chunk in enumerate((sched[:half], sched[half:])):
    cx = RX + ci * 4.25
    yy = y_top
    for t, n, a in chunk:
        sh.text(cx, yy, str(t), size=6.3, bold=True)
        sh.text(cx + 0.28, yy, n[:34], size=6.3)
        sh.text(cx + 3.95, yy, f"{a:,.0f}", size=6.3, align="right")
        yy -= 0.125
y = y_top - 0.125 * half - 0.12
sh.text(RX, y, "OPEN (not decided here)", size=9, bold=True)
y -= 0.04
for c in ["Structure of the curved shell and the 120 ft roof span; tier depth still needs <= 1'-6\" (D-061).",
          "Egress / exit capacity with X6, X9, X10 moved: recheck on P2-G-002 (Rev E).",
          "A-102 Level 2 needs a matching Rev (loop corners, ST-2 landing).",
          "SRM / Summertown Metals roles are not agreed; names are descriptive, no marks used (D-042)."]:
    y = sh.para(RX, y, RW, c, size=7.0, bullet="•", indent=0.14)
sh.text(RX, 2.62, "Sources: params/phase2_plan_rev_i.yaml (Rev J); params/phase2_plan_rev_k.yaml; D-070..D-077 (DECISIONS_ARENA).",
        size=6.3)

out_pdf = os.path.join(ROOT, "blueprints", "phase2", "out", "pdf")
out_dxf = os.path.join(ROOT, "blueprints", "phase2", "out", "dxf")
os.makedirs(out_pdf, exist_ok=True)
os.makedirs(out_dxf, exist_ok=True)
sh.render_pdf(os.path.join(out_pdf, "P2-A-101_RevK.pdf"))
sh.render_dxf(os.path.join(out_dxf, "P2-A-101_RevK.dxf"))
print("L1 envelope %.0f | L1 total %.0f | L2 loss %.0f | L2 %.0f | TOTAL %.0f (Rev J %.0f, %+.0f)" % (
    l1_envelope, l1_total, l2_loss, K_L2, K_TOT, J_TOT, K_TOT - J_TOT))
print("changed rooms:", [(t, n, round(a), round(c)) for t, n, a, c in changed])
