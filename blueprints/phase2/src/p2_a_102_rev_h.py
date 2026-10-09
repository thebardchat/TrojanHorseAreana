#!/usr/bin/env python3
"""P2-A-102 Rev H: Level 2 block plan, concept envelope with the 29 ft ST-2 drum (D-081, P2-T-017).

New file; P2-A-102 Rev G (p2_a_102_rev_g.py), Rev F and the frozen Set Rev D are not touched. Geometry = the approved Rev G
(params/phase2_plan_rev_i.yaml, Level 2 = Rev F, checked against ARENA P2-A-102_RevG.dxf) + phase2_plan_rev_k.yaml + phase2_plan_rev_g_l2.yaml + phase2_plan_rev_l.yaml, through p2_plan_rev_l_geom.py.

  /workspace/.venv-keystone/bin/python blueprints/phase2/src/p2_a_102_rev_h.py --rev H [--out-dir DIR]     (run from the repo root)
"""
import argparse
import math
import os
import sys

from shapely.geometry import box

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import p2_plan_rev_l_geom as g  # noqa: E402
sys.path.insert(0, os.path.join(g.ROOT, "blueprints", "shared"))
from palette import WHITE  # noqa: E402
from titleblock import Sheet, add_titleblock  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--rev", choices=["H"], required=True)
ap.add_argument("--out-dir", default=os.path.join(g.ROOT, "blueprints", "phase2", "out"))
a = ap.parse_args()

J, env, R, RI = g.J, g.env, g.R, g.RI
rc = (R + RI) / 2.0
cl_len = 2 * (154 + 205) - 2 * rc + math.pi / 2 * rc
W, H = 17.0, 11.0
sh = Sheet(W, H)
top = add_titleblock(sh, dict(
    project="Hazel Green Regional Athletic Complex\nTrojan Horse Arena · Hazel Green area, Madison County, Alabama (site TBD, D-006)",
    phase="PHASE 2", title="OVERALL FLOOR PLAN\nLEVEL 2 · BLOCK PLAN", scale="1\" =\n40'-0\"", date="October\n2026",
    revision="H", drawn_by="Drawn by KEYSTONE (AI) for\nShane Brazelton", sheet_no="P2-A-102",
    stamp="PRELIMINARY — CONCEPTUAL DESIGN — NOT FOR CONSTRUCTION"))
S = 1.0 / 40.0
OX, OY = 1.05, top + 0.55


def P(x, y):
    return OX + x * S, OY + y * S


def poly(geo, fill=None, lw=0.6, layer="A-ROOM"):
    if geo.is_empty:
        return
    for gg in ([geo] if geo.geom_type == "Polygon" else list(geo.geoms)):
        sh.poly([P(x, y) for x, y in gg.exterior.coords], fill=fill, lw=lw, layer=layer)


def label(x, y, s, size=6, bold=False, rot=0, align="center"):
    px, py = P(x, y)
    sh.text(px, py - size / 72 * 0.35, s, size=size, bold=bold, align=align, rot=rot, layer="A-ANNO-TEXT")


def dline(x1, y1, x2, y2, lw=0.4, layer="A-ANNO-GHOST"):
    (p1, q1), (p2, q2) = P(x1, y1), P(x2, y2)
    sh.dashed(p1, q1, p2, q2, layer=layer, lw=lw)


def dpoly(geo, lw=0.4, layer="A-ANNO-GHOST"):
    c = list(geo.exterior.coords)
    for (p1, q1), (p2, q2) in zip(c, c[1:]):
        dline(p1, q1, p2, q2, lw=lw, layer=layer)


for z in g.L2_ZONES.values():
    geo = g.stretch if z["id"] == "stretch_n" else box(*z["rect"]).intersection(env).difference(g.stairs_l)
    poly(geo, fill="#EFEDE6", lw=0.3)
poly(g.landing, fill="#E3DDC9", lw=0.3)
for r in g.L2_ROOMS.values():
    poly(box(*r["rect"]).intersection(env).difference(g.stairs_l), fill="#DAD6C9", lw=0.45)
for ob in g.open_ob:
    poly(ob, fill=WHITE, lw=0.5, layer="A-OPEN")
    x0, y0, x1, y1 = ob.bounds
    dline(x0, y0, x1, y1)
    dline(x0, y1, x1, y0)
poly(g.loop, fill="#F6F1E1", lw=0.5, layer="A-LOOP")
pts = [(52.5, 37.5), (206.5, 37.5)]
arc = [(206.5 - rc + rc * math.cos(math.radians(t)), 242.5 - rc + rc * math.sin(math.radians(t))) for t in range(0, 91, 5)]
pts += [(206.5, 242.5 - rc)] + arc + [(52.5, 242.5), (52.5, 37.5)]
for (p1, q1), (p2, q2) in zip(pts, pts[1:]):
    if (p1, q1) != (p2, q2):
        dline(p1, q1, p2, q2, lw=0.45)
for side, geo in g.UP:
    poly(geo, fill="#F2D6D6", lw=0.6, layer="A-TIER")
dpoly(g.tower_k)                                   # Rev G 20 ft tower, ghost
for sid, geo in (("ST-1", g.ST1), ("ST-3", g.ST3), ("ST-4", g.ST4)):
    poly(geo, fill="#B9B3A0", lw=0.9, layer="A-STAIR")
    b = geo.bounds
    label((b[0] + b[2]) / 2, (b[1] + b[3]) / 2, sid, size=5.5, bold=True, rot=90)
poly(g.drum, fill="#B9B3A0", lw=0.9, layer="A-STAIR")
dpoly(g.stair_rect, lw=0.4, layer="A-STAIR")
label(g.DC[0], g.DC[1] + 1.5, "ST-2", size=6, bold=True)
label(g.DC[0], g.DC[1] - 3.2, "29 FT DRUM", size=4.8)
ex, ey = g.DOOR
ux, uy = (ex - g.DC[0]) / (g.D_DIA / 2), (ey - g.DC[1]) / (g.D_DIA / 2)
(p1, q1), (p2, q2) = P(ex, ey), P(ex + ux * 3.5, ey + uy * 3.5)
sh.line(p1, q1, p2, q2, layer="A-EXIT", lw=2.2)
el = box(*J["vertical"]["elevator"]["rect"])
poly(el, fill=WHITE, lw=0.8, layer="A-STAIR")
dline(*el.bounds[:2], el.bounds[2], el.bounds[3], lw=0.4)
dline(el.bounds[0], el.bounds[3], el.bounds[2], el.bounds[1], lw=0.4)
label(60, 22.5, "EL", size=5.5, bold=True)
for gd in J["level_2"]["loop"]["guards"]:
    (x1, y1, x2, y2) = gd["line"] if len(gd["line"]) == 4 else (*gd["line"][0], *gd["line"][1])
    (p1, q1), (p2, q2) = P(x1, y1), P(x2, y2)
    sh.line(p1, q1, p2, q2, layer="A-GUARD", lw=2.0)
ext = list(env.exterior.coords)
for (ax, ay), (bx, by) in zip(ext, ext[1:]):
    (x1, y1), (x2, y2) = P(ax, ay), P(bx, by)
    sh.line(x1, y1, x2, y2, layer="A-WALL-EXT", lw=2.4)

sch = {t: (n, a0, a1) for t, n, a0, a1 in g.l2_sched}
label(32, 192, "17  STRENGTH & COND.", size=5.5, bold=True, rot=90)
label(37, 192, f"{sch['17'][2]:,.0f} SF", size=5.5, rot=90)
label(24.5, 105, "18  CROSS-TRAINING MAT", size=5.5, bold=True)
label(24.5, 100, f"{sch['18'][2]:,.0f} SF", size=5.5)
label(26, 44, "L2 CORRIDOR", size=5.5, bold=True)
label(74, 19, "19  MEN", size=5.5, bold=True)
label(74, 14, f"{sch['19'][2]:,.0f} SF", size=5.5)
label(155.5, 17, "20  WOMEN", size=5.5, bold=True)
label(155.5, 12, f"{sch['20'][2]:,.0f} SF", size=5.5)
label(32.5, 9.4, "21  ADMIN", size=5.5, bold=True)
label(32.5, 4.8, f"{sch['21'][2]:,.0f} SF", size=5.5)
label(200, 22, "UPPER", size=5.5, bold=True)
label(200, 17, "CONC. (E)", size=5.5, bold=True)
label(118, 6, "OPEN TO LOBBY BELOW", size=5.5, bold=True)
label(116, 140, "OPEN TO ARENA BELOW", size=8, bold=True)
label(116, 133, "event floor + telescopic lower tier (double height)", size=6)
label(108, 249, "STRETCH / WARM-UP (N) · 6 FT", size=5.5, bold=True)
label(116, 231.5, "UPPER (N) · FIXED · 314 SEATS", size=6, bold=True)
label(116, 48.5, "UPPER (S) · FIXED · 314 SEATS", size=6, bold=True)
label(195.5, 140, "UPPER (E) · FIXED · 472 SEATS", size=6, bold=True, rot=90)
label(116, 100, "RUNNING / TRAINING LOOP (D-035) · 2 LANES x 42 IN", size=5.5)
label(116, 87, f"centreline {cl_len:,.0f} FT · {g.loop.area:,.0f} SF", size=5.5)
label(59.5, 140, "42 IN GUARD (G-W)", size=5, rot=90)
px, py = P(ex, ey)
sh.text(px - 0.45, py + 0.3, "DRUM DOOR (SW FACE)", size=5.2, bold=True, align="right")
sh.line(px - 0.42, py + 0.32, px, py, layer="A-ANNO-TEXT", lw=0.4)
sx0, sy0 = P(0, -9)
sx1, _ = P(210, -9)
sh.line(sx0, sy0, sx1, sy0, layer="A-ANNO-DIMS", lw=0.5)
sh.text((sx0 + sx1) / 2, sy0 - 0.13, "210'-0\" (box; R = 20'-0\" corners; L2 FF 17'-9\")", size=7, align="center", layer="A-ANNO-DIMS")
dx0, dy0 = P(-9, 0)
_, dy1 = P(-9, 252)
sh.line(dx0, dy0, dx0, dy1, layer="A-ANNO-DIMS", lw=0.5)
sh.text(dx0 - 0.1, (dy0 + dy1) / 2, "252'-0\"", size=7, align="center", rot=90, layer="A-ANNO-DIMS")
nx, ny = P(262, 40)
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
sh.text(RX, y, "LEVEL 2 — OVERALL FLOOR PLAN (REV H)", size=11, bold=True)
y -= 0.2
y = sh.para(RX, y, RW, "Rev G (approved, D-080) with ST-2 as the 29 ft drum of P2-A-101 Rev L (D-081). Rooms, tiers, guards, seat counts and the "
            "R 13 NE loop corner are Rev G unless listed under CHANGES. Rev G tower shown dashed.", size=7.5)
y -= 0.2
sh.text(RX, y, "CHANGES FROM REV G (all ASSUMED)", size=9, bold=True)
y -= 0.05
for c in [
    f"ST-2: {g.D_DIA:.0f} ft drum centred ({g.DC[0]:.0f}, {g.DC[1]:.1f}), same as Level 1; holds the 12.67 x 24.08 ft 76 in stair (dashed) with "
    f"{g.FIT_MARGIN:.2f} ft spare on the diagonal. +{g.L2_L - g.L2_K:,} SF on this level.",
    f"North stretch strip now ends at x {g.L['level_2']['stretch_n']['rect'][2]:.0f} (was 168); drum door on the SW face at "
    f"({g.DOOR[0]:.1f}, {g.DOOR[1]:.1f}), opening into the strip landing, not onto the loop.",
    f"Drum south edge y {g.DC[1] - g.D_DIA / 2:.1f}: clear of the loop's north edge (y 246) by {g.DC[1] - g.D_DIA / 2 - 246:.1f} ft; the loop, its "
    f"R {RI:.0f} ft NE corner and the upper tiers do not change.",
]:
    y = sh.para(RX, y, RW, c, size=7.2, bullet="•", indent=0.14)
y -= 0.2
sh.text(RX, y, "ROOM SCHEDULE — LEVEL 2 (SF net of stairs, inside the envelope)", size=9, bold=True)
y -= 0.2
cols = [RX, RX + 0.35, RX + 3.6, RX + 4.7, RX + 5.8]
for x, t in zip(cols, ["TAG", "ROOM", "REV G", "REV H", "CHANGE"]):
    sh.text(x, y, t, size=7, bold=True)
sh.line(RX, y - 0.04, RX + RW, y - 0.04, lw=0.5)
y -= 0.17
upper = sum(b.area for _, b in g.UP)
rows = [("—", "Upper tier, fixed (1,100 seats)", upper, upper)] + list(g.l2_sched)
for t, nm, a0, a1 in rows:
    chg = "0" if abs(a1 - a0) < 0.5 else f"{a1 - a0:+,.0f}"
    for x, v in zip(cols, [t, nm, f"{a0:,.0f}", f"{a1:,.0f}", chg]):
        sh.text(x, y, v, size=6.8)
    y -= 0.14
y -= 0.06
sh.text(RX, y, "AREA CHECK (no SF cap, D-056; L1, L2, total vs last rev, D-057)", size=9, bold=True)
y -= 0.2
for x, t in zip([RX, RX + 3.0, RX + 4.4, RX + 5.8], ["", "REV K / G", "REV L / H", "CHANGE"]):
    sh.text(x, y, t, size=7, bold=True)
sh.line(RX, y - 0.04, RX + RW, y - 0.04, lw=0.5)
y -= 0.17
for lab, v0, v1 in [("L1 footprint (P2-A-101 Rev L)", g.L1_K, g.L1_L), ("L2 area (envelope - open-to-below)", g.L2_K, g.L2_L),
                    ("TOTAL GSF", g.TOT_K, g.TOT_L)]:
    bold = lab.startswith("TOTAL")
    sh.text(RX, y, lab, size=7, bold=bold)
    for x, v in zip([RX + 3.0, RX + 4.4, RX + 5.8], [f"{v0:,}", f"{v1:,}", f"{v1 - v0:+,}"]):
        sh.text(x, y, v, size=7, bold=bold)
    y -= 0.15
y -= 0.04
y = sh.para(RX, y, RW, f"L2 = envelope {env.area:,.0f} SF - open-to-below {g.OB_SF:,.0f} SF (arena 132 x 168 + lobby 58 x 34), the Rev F / G method. "
            "Rev K / G baseline = D-079. Carried to P2-G-003 Rev L.", size=6.8)
y -= 0.14
sh.text(RX, y, "OPEN (not decided here)", size=9, bold=True)
y -= 0.04
for c in [f"Drum door: {g.door_to_loop:.1f} ft from the door to the loop edge along its swing line; landing at a 76 in stair door needs the architect (IBC 1010 not checked; P2-G-002 Rev E F2).",
          "Drum floor-to-floor, wall and roof; structure of the curved shell; tier depth 1'-6\" or less (D-061).",
          "SRM / Summertown Metals roles are not agreed; names are descriptive, no marks used (D-042)."]:
    y = sh.para(RX, y, RW, c, size=7.0, bullet="•", indent=0.14)
sh.text(RX, 2.62, "Sources: ARENA P2-A-102_RevG.dxf; params/phase2_plan_rev_i.yaml (L2 as Rev F); phase2_plan_rev_k.yaml; phase2_plan_rev_g_l2.yaml; phase2_plan_rev_l.yaml; D-079..D-081.",
        size=6.3)

os.makedirs(os.path.join(a.out_dir, "pdf"), exist_ok=True)
os.makedirs(os.path.join(a.out_dir, "dxf"), exist_ok=True)
sh.render_pdf(os.path.join(a.out_dir, "pdf", "P2-A-102_RevH.pdf"))
sh.render_dxf(os.path.join(a.out_dir, "dxf", "P2-A-102_RevH.dxf"))
g.true_circle_dxf(os.path.join(a.out_dir, "dxf", "P2-A-102_RevH.dxf"), P, S)    # drum as a true circle / arc (D-074)
print("L2 %d | L1 %d | TOTAL %d (Rev K/G %d, %+d)" % (g.L2_L, g.L1_L, g.TOT_L, g.TOT_K, g.TOT_L - g.TOT_K))
