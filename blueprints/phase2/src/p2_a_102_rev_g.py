#!/usr/bin/env python3
"""P2-A-102 Rev G: Level 2 block plan inside the radiused concept envelope (D-074 / D-077 / D-078 / D-079).

New file; P2-A-102 Rev F and the frozen Set Rev D are not touched. Geometry = params/phase2_plan_rev_i.yaml (Level 2 as Rev F)
with the overrides in params/phase2_plan_rev_k.yaml (envelope, stairs) and params/phase2_plan_rev_g_l2.yaml (this sheet).

  python blueprints/phase2/src/p2_a_102_rev_g.py            (run from the repo root)
"""
import math
import os
import sys

import yaml
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "blueprints", "shared"))
from titleblock import Sheet, add_titleblock  # noqa: E402

PAR = os.path.join(ROOT, "blueprints", "params")
J = yaml.safe_load(open(os.path.join(PAR, "phase2_plan_rev_i.yaml"), encoding="utf-8"))
K = yaml.safe_load(open(os.path.join(PAR, "phase2_plan_rev_k.yaml"), encoding="utf-8"))
G = yaml.safe_load(open(os.path.join(PAR, "phase2_plan_rev_g_l2.yaml"), encoding="utf-8"))
R = K["envelope"]["corner_radius_ft"]


def rrect(x0, y0, x1, y1, r, n=24):
    pts = []
    for cx, cy, a0 in [(x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180), (x1 - r, y0 + r, 270)]:
        for i in range(n + 1):
            a = math.radians(a0 + 90.0 * i / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return Polygon(pts)


# ---------------------------------------------------------------- geometry (feet)
ring = rrect(0, 0, 210, 252, R)
tw = K["stairs"]["ST-2"]
tower = Point(*tw["centre"]).buffer(tw["radius_ft"], 64)
envelope = unary_union([ring, tower])
ST = {s["id"]: box(*s["rect"]) for s in J["vertical"]["stairs"]}
ST["ST-3"] = box(*K["stairs"]["ST-3"]["rect"])
ST["ST-4"] = box(*K["stairs"]["ST-4"]["rect"])
stairs_all = unary_union(list(ST.values()) + [tower])
lo, li = J["level_2"]["loop"]["outer"], J["level_2"]["loop"]["inner"]
CX, CY = G["loop_corner"]["centre"]
RI = G["loop_corner"]["inner_radius_ft"]
inner_box = box(*li)
inner_round = inner_box.difference(box(CX, CY, li[2], li[3]).difference(Point(CX, CY).buffer(RI, 64)))
loop = (box(*lo).intersection(envelope)).difference(inner_round)
open_ob = [box(*o["rect"]) for o in J["level_2"]["open_below"]]
UP = [(b["side"], box(*b["rect"])) for b in J["tiers"]["upper"]["bands"]]
SEATS = {"N": 314, "S": 314, "E": 472}

l2_rooms = {r["id"]: r for r in J["level_2"]["rooms"]}
zones = {z["id"]: z for z in J["level_2"]["zones"]}
stretch = box(*G["stretch_n"]["rect"]).intersection(envelope).difference(tower)
landing = box(*G["landing"]["rect"]).intersection(envelope).difference(tower)

# ---------------------------------------------------------------- areas
ob_area = sum(g.area for g in open_ob)
L2_K = envelope.area - ob_area                     # same basis as Rev F: footprint minus open-to-below
L1_K = 57520.0                                     # P2-A-101 Rev K
J_L1, J_L2 = 56861.0, 28933.0
upper_sf = sum(g.area for _, g in UP)
loop_sf = loop.area
loop_cl = unary_union([box(*lo)]).bounds
cl = Polygon([(52.5, 37.5), (206.5, 37.5), (206.5, 242.5), (52.5, 242.5)])
# centreline length: rectangle 154 x 205 with the NE corner replaced by an arc of R = (outer + inner)/2 about the corner centre
rc = (R + RI) / 2.0
cl_len = 2 * (154 + 205) - 2 * rc + math.pi / 2 * rc
corner_w = R - Point(CX, CY).distance(Point(li[2], li[3]))
corner_w_sq = R - Point(CX, CY).distance(Point(li[2], li[3]))
corner_cut = box(CX, CY, li[2], li[3]).area - box(CX, CY, li[2], li[3]).intersection(Point(CX, CY).buffer(RI, 64)).area
strip_loss = box(*J["level_2"]["zones"][2]["rect"]).intersection(tower).area


def room_area(g):
    return g.intersection(envelope).difference(stairs_all).area


sched = []
for rid in ("sc", "xt", "rr_m2", "rr_w2", "admin"):
    r = l2_rooms[rid]
    sched.append((r["tag"], r["name"].title() if rid not in ("sc",) else "Strength & Conditioning", room_area(box(*r["rect"])),
                  box(*r["rect"]).area))
corr = box(*zones["l2corr"]["rect"])
conc = box(*zones["conc_e2"]["rect"])
sched_z = [("", "L2 Corridor", room_area(corr)), ("", "Upper Concourse (E)", room_area(conc)),
           ("", "Stretch / Warm-up (N)", stretch.area), ("", "ST-2 landing / NE corner (not programmed)", landing.area)]

# ---------------------------------------------------------------- sheet
W, H = 17.0, 11.0
sh = Sheet(W, H)
top = add_titleblock(sh, dict(
    project="Hazel Green Regional Athletic Complex\nTrojan Horse Arena · Hazel Green area, Madison County, Alabama (site TBD, D-006)",
    phase="PHASE 2", title="OVERALL FLOOR PLAN\nLEVEL 2 · BLOCK PLAN", scale="1\" =\n40'-0\"", date="October\n2026",
    revision="G", drawn_by="Drawn by Claude (AI) for\nShane Brazelton", sheet_no="P2-A-102",
    stamp="PRELIMINARY — CONCEPTUAL DESIGN — NOT FOR CONSTRUCTION"))
S = 1.0 / 40.0
OX, OY = 1.05, top + 0.55


def P(x, y):
    return OX + x * S, OY + y * S


def poly(g, fill=None, lw=0.6, layer="A-ROOM"):
    if g.is_empty:
        return
    geoms = [g] if g.geom_type == "Polygon" else list(g.geoms)
    for gg in geoms:
        sh.poly([P(x, y) for x, y in gg.exterior.coords], fill=fill, lw=lw, layer=layer)


def label(x, y, s, size=6, bold=False, rot=0, align="center"):
    px, py = P(x, y)
    sh.text(px, py - size / 72 * 0.35, s, size=size, bold=bold, align=align, rot=rot, layer="A-ANNO-TEXT")


def dline(x1, y1, x2, y2, lw=0.4, layer="A-ANNO-GHOST"):
    (a, b), (c, d) = P(x1, y1), P(x2, y2)
    sh.dashed(a, b, c, d, layer=layer, lw=lw)


def dpoly(g, lw=0.4, layer="A-ANNO-GHOST"):
    c = list(g.exterior.coords)
    for (a, b), (cc, d) in zip(c, c[1:]):
        dline(a, b, cc, d, lw=lw, layer=layer)


# zones and rooms
for z in zones.values():
    g = box(*z["rect"]).intersection(envelope).difference(stairs_all)
    if z["id"] == "stretch_n":
        g = stretch
    poly(g, fill="#EFEDE6", lw=0.3)
poly(landing, fill="#E3DDC9", lw=0.3)
for r in l2_rooms.values():
    poly(box(*r["rect"]).intersection(envelope).difference(stairs_all), fill="#DAD6C9", lw=0.45)
# open to below
for g in open_ob:
    poly(g, fill="#FFFFFF", lw=0.5, layer="A-OPEN")
    x0, y0, x1, y1 = g.bounds
    dline(x0, y0, x1, y1)
    dline(x0, y1, x1, y0)
# loop (fill + lane line) and upper tiers
poly(loop, fill="#F6F1E1", lw=0.5, layer="A-LOOP")
pts = [(52.5, 37.5), (206.5, 37.5)]
arc = [(206.5 - rc + rc * math.cos(math.radians(a)), 242.5 - rc + rc * math.sin(math.radians(a))) for a in range(0, 91, 5)]
pts += [(206.5, 242.5 - rc)] + arc + [(52.5, 242.5), (52.5, 37.5)]
for (a, b), (c, d) in zip(pts, pts[1:]):
    if (a, b) != (c, d):
        dline(a, b, c, d, lw=0.45)
for side, g in UP:
    poly(g, fill="#F2D6D6", lw=0.6, layer="A-TIER")
# stairs: Rev F ST-2 as ghost, Rev G solid
dpoly(box(*[s for s in J["vertical"]["stairs"] if s["id"] == "ST-2"][0]["rect"]))
for sid in ("ST-1", "ST-3", "ST-4"):
    poly(ST[sid], fill="#B9B3A0", lw=0.9, layer="A-STAIR")
    b = ST[sid].bounds
    label((b[0] + b[2]) / 2, (b[1] + b[3]) / 2, sid, size=5.5, bold=True, rot=90)
poly(tower, fill="#B9B3A0", lw=0.9, layer="A-STAIR")
label(tw["centre"][0], tw["centre"][1], "ST-2", size=6, bold=True)
label(tw["centre"][0], tw["centre"][1] - 4.2, "TOWER", size=5)
ex, ey = G["tower_door"]["at"]
dx, dy = ex - tw["centre"][0], ey - tw["centre"][1]
ux, uy = dx / math.hypot(dx, dy), dy / math.hypot(dx, dy)
(a, b), (c, d) = P(ex, ey), P(ex + ux * 3.5, ey + uy * 3.5)
sh.line(a, b, c, d, layer="A-EXIT", lw=2.2)
# elevator
el = box(*J["vertical"]["elevator"]["rect"])
poly(el, fill="#FFFFFF", lw=0.8, layer="A-STAIR")
dline(*el.bounds[:2], el.bounds[2], el.bounds[3], lw=0.4)
dline(el.bounds[0], el.bounds[3], el.bounds[2], el.bounds[1], lw=0.4)
label(60, 22.5, "EL", size=5.5, bold=True)
# guards (42 in) at open edges
for gd in J["level_2"]["loop"]["guards"]:
    (x1, y1, x2, y2) = gd["line"] if len(gd["line"]) == 4 else (*gd["line"][0], *gd["line"][1])
    (a, b), (c, d) = P(x1, y1), P(x2, y2)
    sh.line(a, b, c, d, layer="A-GUARD", lw=2.0)
# exterior outline
ext = list(envelope.exterior.coords)
for (ax, ay), (bx, by) in zip(ext, ext[1:]):
    (x1, y1), (x2, y2) = P(ax, ay), P(bx, by)
    sh.line(x1, y1, x2, y2, layer="A-WALL-EXT", lw=2.4)

# labels
label(32, 192, "17  STRENGTH & COND.", size=5.5, bold=True, rot=90)
label(37, 192, f"{sched[0][2]:,.0f} SF", size=5.5, rot=90)
label(24.5, 105, "18  CROSS-TRAINING MAT", size=5.5, bold=True)
label(24.5, 100, f"{sched[1][2]:,.0f} SF", size=5.5)
label(26, 44, "L2 CORRIDOR", size=5.5, bold=True)
label(74, 19, "19  MEN", size=5.5, bold=True)
label(74, 14, "550 SF", size=5.5)
label(155.5, 17, "20  WOMEN", size=5.5, bold=True)
label(155.5, 12, "900 SF", size=5.5)
label(32.5, 9.4, "21  ADMIN", size=5.5, bold=True)
label(32.5, 4.8, "470 SF", size=5.5)
label(200, 22, "UPPER", size=5.5, bold=True)
label(200, 17, "CONC. (E)", size=5.5, bold=True)
label(118, 6, "OPEN TO LOBBY BELOW", size=5.5, bold=True)
label(116, 140, "OPEN TO ARENA BELOW", size=8, bold=True)
label(116, 133, "event floor + telescopic lower tier (double height)", size=6)
label(110, 249, "STRETCH / WARM-UP (N) · 6 FT", size=5.5, bold=True)
label(116, 231.5, "UPPER (N) · FIXED · 314 SEATS", size=6, bold=True)
label(116, 48.5, "UPPER (S) · FIXED · 314 SEATS", size=6, bold=True)
label(195.5, 140, "UPPER (E) · FIXED · 472 SEATS", size=6, bold=True, rot=90)
label(116, 100, "RUNNING / TRAINING LOOP (D-035) · 2 LANES x 42 IN", size=5.5)
label(116, 87, f"centreline {cl_len:,.0f} FT · {loop_sf:,.0f} SF", size=5.5)
label(59.5, 140, "42 IN GUARD (G-W)", size=5, rot=90)
# NE loop-corner callout
nx, ny = P(CX + 9.5, CY + 6.5)
sh.text(nx + 0.55, ny + 0.2, "NE LOOP CORNER", size=5.5, bold=True, align="left")
sh.text(nx + 0.55, ny + 0.08, f"inner edge R {RI:.0f}'-0\" → {R - RI:.0f} ft clear", size=5.2, align="left")
sh.text(nx + 0.55, ny - 0.04, f"(square edge: {corner_w:.1f} ft)", size=5.2, align="left")
sh.line(nx + 0.53, ny + 0.2, nx, ny, layer="A-ANNO-TEXT", lw=0.4)
# dimensions
sx0, sy0 = P(0, -9)
sx1, _ = P(210, -9)
sh.line(sx0, sy0, sx1, sy0, layer="A-ANNO-DIMS", lw=0.5)
sh.text((sx0 + sx1) / 2, sy0 - 0.13, "210'-0\" (box; R = 20'-0\" corners; L2 FF 17'-9\")", size=7, align="center", layer="A-ANNO-DIMS")
dx0, dy0 = P(-9, 0)
_, dy1 = P(-9, 252)
sh.line(dx0, dy0, dx0, dy1, layer="A-ANNO-DIMS", lw=0.5)
sh.text(dx0 - 0.1, (dy0 + dy1) / 2, "252'-0\"", size=7, align="center", rot=90, layer="A-ANNO-DIMS")
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
sh.text(RX, y, "LEVEL 2 — OVERALL FLOOR PLAN (REV G)", size=11, bold=True)
y -= 0.2
y = sh.para(RX, y, RW, "Rev F Level 2 (frozen) inside the Rev K envelope (R = 20 ft, D-077; P2-A-101 Rev K approved, D-079). Rooms, tiers, "
            "guards and seat counts are Rev F unless listed under CHANGES. Rev F dashed outline shows the old NE stair projection.", size=7.5)
y -= 0.2
sh.text(RX, y, "CHANGES FROM REV F (all ASSUMED)", size=9, bold=True)
y -= 0.05
changes = [
    "Envelope: box with R = 20 ft corners; S&C (17) and the L2 corridor lose the NW / SW corner area; upper concourse (E) loses the SE corner.",
    "ST-2 is the 20 ft cylindrical tower (centre 178, 257.7). It replaces the 24.08 x 12.67 ft NE stair, so the north stretch strip now ends at x 168 "
    "and the tower is entered from the strip by a door on its SW face (no L2 door on the loop).",
    "ST-3 and ST-4 as Rev K (slid along their walls); same L2 position as L1, rooms trimmed around them.",
    f"NE loop corner: the 20 ft arc cuts the loop's outer corner; with a square inner edge the clear width drops to {corner_w:.1f} ft "
    f"(7 ft = 2 lanes x 42 in needed). Inner edge rounded to R {RI:.0f} ft keeps {R - RI:.0f} ft; the tier corner loses {corner_cut:.1f} SF (under 1 seat).",
]
for c in changes:
    y = sh.para(RX, y, RW, c, size=7.2, bullet="•", indent=0.14)
y -= 0.2
sh.text(RX, y, "ROOM SCHEDULE — LEVEL 2 (SF net of stairs, inside the Rev G envelope)", size=9, bold=True)
y -= 0.2
cols = [RX, RX + 0.35, RX + 3.4, RX + 4.5, RX + 5.6]
for x, t in zip(cols, ["TAG", "ROOM", "REV F", "REV G", "CHANGE"]):
    sh.text(x, y, t, size=7, bold=True)
sh.line(RX, y - 0.04, RX + RW, y - 0.04, lw=0.5)
y -= 0.17
F_ROWS = {"17": 5124, "18": 3500, "19": 550, "20": 900, "21": 470}
rows = [("—", "Upper tier, fixed (1,100 seats)", 6930, upper_sf), ("—", "Running / training loop", 5026, loop_sf)]
for t, nm, a_drawn, _unclipped in sched:
    rows.append((t, nm, F_ROWS[t], a_drawn))
for t, nm, a in sched_z[:3]:
    rows.append(("—", nm, {"L2 Corridor": 0, "Upper Concourse (E)": 0, "Stretch / Warm-up (N)": 0}[nm], a))
for t, nm, a0, a1 in rows:
    base = "" if a0 == 0 else f"{a0:,.0f}"
    chg = "" if a0 == 0 else ("0" if abs(a1 - a0) < 0.5 else f"{a1 - a0:+,.0f}")
    for x, v, al in zip(cols, [t, nm, base, f"{a1:,.0f}", chg], ["left"] * 5):
        sh.text(x, y, v, size=6.8)
    y -= 0.14
sh.text(RX + 0.35, y, "ST-2 landing / NE corner (not programmed)", size=6.8)
sh.text(cols[3], y, f"{landing.area:,.0f}", size=6.8)
y -= 0.14
y -= 0.06
sh.text(RX, y, "AREA CHECK (no SF cap, D-056; L1, L2, total vs Rev J, D-057)", size=9, bold=True)
y -= 0.2
for x, t in zip([RX, RX + 3.0, RX + 4.4, RX + 5.8], ["", "REV J", "REV K/G", "CHANGE"]):
    sh.text(x, y, t, size=7, bold=True)
sh.line(RX, y - 0.04, RX + RW, y - 0.04, lw=0.5)
y -= 0.17
for lab, a, b in [("L1 footprint (P2-A-101 Rev K)", J_L1, L1_K), ("L2 area (envelope - open-to-below)", J_L2, L2_K),
                  ("TOTAL GSF", J_L1 + J_L2, L1_K + L2_K)]:
    bold = lab.startswith("TOTAL")
    sh.text(RX, y, lab, size=7, bold=bold)
    for x, v in zip([RX + 3.0, RX + 4.4, RX + 5.8], [f"{a:,.0f}", f"{b:,.0f}", f"{b - a:+,.0f}"]):
        sh.text(x, y, v, size=7, bold=bold)
    y -= 0.15
y -= 0.04
y = sh.para(RX, y, RW, f"L2 = envelope {envelope.area:,.0f} SF - open-to-below {ob_area:,.0f} SF (arena 132 x 168 + lobby 58 x 34), the Rev F method. "
            f"This corrects the P2-A-101 Rev K sheet (L2 28,736, TOTAL 86,256): that figure kept the Rev J NE projection and did not count the tower floor; "
            f"use {L2_K:,.0f} / {L1_K + L2_K:,.0f}. Carry to P2-G-003 Rev L.", size=6.8)
y -= 0.14
sh.text(RX, y, "OPEN (not decided here)", size=9, bold=True)
y -= 0.04
for c in ["Exit capacity and travel distance with ST-2 as the only NE stair and X1, X6, X9, X10 moved: P2-G-002 recheck (Rev F).",
          "Tower floor-to-floor and the strip landing: 6 ft landing at a 76 in stair door needs architect confirmation (IBC 1010 not checked).",
          "Structure of the curved shell and tier depth of 1'-6\" or less (D-061); seat counts re-verified after the corner cut.",
          "SRM / Summertown Metals roles are not agreed; names are descriptive, no marks used (D-042)."]:
    y = sh.para(RX, y, RW, c, size=7.0, bullet="•", indent=0.14)
sh.text(RX, 2.62, "Sources: params/phase2_plan_rev_i.yaml (L2 as Rev F); phase2_plan_rev_k.yaml; phase2_plan_rev_g_l2.yaml; D-035, D-061, D-077..D-079.",
        size=6.3)

out_pdf = os.path.join(ROOT, "blueprints", "phase2", "out", "pdf")
out_dxf = os.path.join(ROOT, "blueprints", "phase2", "out", "dxf")
os.makedirs(out_pdf, exist_ok=True)
os.makedirs(out_dxf, exist_ok=True)
sh.render_pdf(os.path.join(out_pdf, "P2-A-102_RevG.pdf"))
sh.render_dxf(os.path.join(out_dxf, "P2-A-102_RevG.dxf"))
print("L2 %.0f | L1 %.0f | TOTAL %.0f (Rev J %.0f, %+.0f)" % (L2_K, L1_K, L1_K + L2_K, J_L1 + J_L2, L1_K + L2_K - J_L1 - J_L2))
print("loop %.0f cl %.0f | corner width sq %.2f | cut %.2f | stretch %.0f landing %.0f | upper %.0f" % (
    loop_sf, cl_len, corner_w, corner_cut, stretch.area, landing.area, upper_sf))
print([(t, n, round(a)) for t, n, a, _ in sched], [(n, round(a)) for _, n, a in sched_z])
