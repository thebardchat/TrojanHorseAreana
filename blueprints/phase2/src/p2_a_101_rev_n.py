#!/usr/bin/env python3
"""P2-A-101 Rev N: Level 1 block plan, Rev M + the old NE stair strip as MECH (remote) (D-086).

New file; P2-A-101 Rev M / L / K and the frozen Set Rev D are not touched. Geometry = p2_plan_rev_m_geom.py + params/phase2_plan_rev_n.yaml
through p2_plan_rev_n_geom.py. Output: PDF + DXF (shared/titleblock.py).

  /workspace/.venv-keystone/bin/python blueprints/phase2/src/p2_a_101_rev_n.py --rev N [--out-dir DIR]     (run from the repo root)
"""
import argparse
import os
import sys

from shapely.geometry import box

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import p2_plan_rev_m_geom as g  # noqa: E402
import p2_plan_rev_n_geom as gn  # noqa: E402
sys.path.insert(0, os.path.join(g.ROOT, "blueprints", "shared"))
from titleblock import Sheet, add_titleblock  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--rev", choices=["N"], required=True)
ap.add_argument("--out-dir", default=os.path.join(g.ROOT, "blueprints", "phase2", "out"))
a = ap.parse_args()

J, env = g.J, g.env
W, H = 17.0, 11.0
sh = Sheet(W, H)
top = add_titleblock(sh, dict(
    project="Hazel Green Regional Athletic Complex\nTrojan Horse Arena · Hazel Green area, Madison County, Alabama (site TBD, D-006)",
    phase="PHASE 2", title="OVERALL FLOOR PLAN\nLEVEL 1 · BLOCK PLAN", scale="1\" =\n40'-0\"", date="October\n2026",
    revision="N", drawn_by="Drawn by KEYSTONE (AI) for\nShane Brazelton", sheet_no="P2-A-101",
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


def dpoly(geo, lw=0.35, layer="A-ANNO-GHOST"):
    c = list(geo.exterior.coords)
    for (ax, ay), (bx, by) in zip(c, c[1:]):
        (x1, y1), (x2, y2) = P(ax, ay), P(bx, by)
        sh.dashed(x1, y1, x2, y2, layer=layer, lw=lw)


def label(x, y, s, size=6, bold=False, rot=0, align="center"):
    px, py = P(x, y)
    sh.text(px, py - size / 72 * 0.35, s, size=size, bold=bold, align=align, rot=rot, layer="A-ANNO-TEXT")


# zones, rooms (clipped to the envelope, net of stairs), bump-out rooms
for z in J["level_1"]["zones"]:
    poly(box(*z["rect"]).intersection(env).difference(g.stairs_m), fill="#EFEDE6", lw=0.3)
for r in g.L1_ROOMS:
    geo = box(*r["rect"]) if r["id"] in g.BUMP_ROOMS else box(*r["rect"]).intersection(env).difference(g.stairs_m)
    poly(geo, fill="#DAD6C9", lw=0.45)
for band in J["tiers"]["lower"]["bands"]:
    poly(box(*band["rect"]), fill="#E9B4B4", lw=0.4)
poly(box(*J["event_floor"]["rect"]), fill="#EAD9B5", lw=0.5)
for m in J["mats"]:
    ox, oy = m["origin"]
    poly(box(ox, oy, ox + 42, oy + 42), fill="#F4ECD0", lw=0.3)
    poly(g.Point(ox + 21, oy + 21).buffer(14, 32), fill="#C93A3A", lw=0.3)
poly(gn.STRIP, fill="#DAD6C9", lw=0.45)                         # 30 MECH (remote), D-086
for sid, geo in (("ST-1", g.ST1), ("ST-3", g.ST3), ("ST-4", g.ST4)):
    poly(geo, fill="#B9B3A0", lw=0.9, layer="A-STAIR")
    b = geo.bounds
    label((b[0] + b[2]) / 2, (b[1] + b[3]) / 2, sid, size=5.5, bold=True, rot=90)
poly(g.drum, fill="#B9B3A0", lw=0.9, layer="A-STAIR")
dpoly(g.stair_rect, lw=0.4, layer="A-STAIR")
label(g.DC[0], g.DC[1] + 1.5, "ST-2", size=6, bold=True)
label(g.DC[0], g.DC[1] - 3.2, "30 FT DRUM", size=4.8)
_c = gn.STRIP.representative_point()
label(_c.x - 4, _c.y, str(gn.SR["tag"]), size=5, bold=True)
# pop-outs
poly(g.ANNEX, fill="#8E949B", lw=1.0, layer="A-ANNEX")
poly(g.BAY, fill="#A55A5A", lw=1.0, layer="A-ANNEX")
poly(g.BUMP, fill="#8E949B", lw=1.0, layer="A-ANNEX")
for r in g.L1_ROOMS:
    if r["id"] in g.BUMP_ROOMS:
        poly(box(*r["rect"]), fill="#DAD6C9", lw=0.45)
ext = list(env.exterior.coords)
for (ax, ay), (bx, by) in zip(ext, ext[1:]):
    (x1, y1), (x2, y2) = P(ax, ay), P(bx, by)
    sh.line(x1, y1, x2, y2, layer="A-WALL-EXT", lw=2.4)

# exits: plan Rev J doors (X7 on the wall, X11); X1 / X9 / X10 as Rev K (phase2_plan_rev_k.yaml); X6 on the drum east face (phase2_plan_rev_m.yaml)
KX = g.K["exits_moved"]
FIX = {"X1": ("W", 0, KX["X1"]["at"]), "X10": ("W", 0, KX["X10"]["at"]), "X9": ("S", KX["X9"]["at"], 0), "X6": ("T", g.X6[0], g.X6[1])}
for d in J["level_1"]["doors"]["items"]:
    if d["id"] == "S1" or d["id"].startswith("E1"):
        continue
    wall, at = d["wall"], d["at"]
    if d["id"] in FIX:
        wall, ex, ey = FIX[d["id"]]
    else:
        ex, ey = {"S": (at, 0), "N": (at, 252), "W": (0, at)}.get(wall, (d.get("x", 210), at))
    px, py = P(ex, ey)
    out = {"S": (0, -0.16), "N": (0, 0.16), "W": (-0.16, 0), "E": (0.16, 0), "T": (0.16, 0.0)}[wall]
    sh.line(px, py, px + out[0] * 0.6, py + out[1] * 0.6, layer="A-EXIT", lw=2.2)
    sh.text(px + out[0] * 1.35, py + out[1] * 1.35 - 0.03, d["id"], size=5.5, bold=True, align="center")
for r in g.L1_ROOMS:
    geo = box(*r["rect"]) if r["id"] in g.BUMP_ROOMS else box(*r["rect"]).intersection(env).difference(g.stairs_m)
    c = geo.representative_point()
    label(c.x, c.y, str(r["tag"]), size=6, bold=True)
label(116, 140, "EVENT FLOOR", size=8, bold=True)
label(116, 133, "120 x 144 ft · 4 x 42 ft mats", size=6)
label(87, 267, "24  CHAIR / TABLE / STAGE", size=5.5, bold=True)
label(87, 261, "STORAGE · 2,100 SF", size=5.5)
label(149, 271, "29  MECH / ELEC", size=5, bold=True)
label(149, 265.5, "BAY · 900 SF", size=5)
label(149, 260, "x 134-164", size=5)
label(206, 95, "PUBLIC CORR. (E) 8 FT", size=4.6, bold=True, rot=90)
label(84, 5, "E1 MAIN ENTRY", size=6, bold=True)
sx0, sy0 = P(0, -9)
sx1, _ = P(210, -9)
sh.line(sx0, sy0, sx1, sy0, layer="A-ANNO-DIMS", lw=0.5)
sh.text((sx0 + sx1) / 2, sy0 - 0.13, "210'-0\" (box; R = 20'-0\" corners)", size=7, align="center", layer="A-ANNO-DIMS")
dx, dy0 = P(-9, 0)
_, dy1 = P(-9, 252)
sh.line(dx, dy0, dx, dy1, layer="A-ANNO-DIMS", lw=0.5)
sh.text(dx - 0.1, (dy0 + dy1) / 2, "252'-0\"", size=7, align="center", rot=90, layer="A-ANNO-DIMS")
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
sh.text(RX, y, "LEVEL 1 — OVERALL FLOOR PLAN (REV N)", size=11, bold=True)
y -= 0.2
y = sh.para(RX, y, RW, "Rev M (30 ft drum D-082, plan Rev J east side D-084) with the old NE stair strip made mechanical (D-086). "
            "Nothing else moves; Level 2 (P2-A-102 Rev I) is unchanged.", size=7.5)
y -= 0.12
sh.text(RX, y, "CHANGES FROM REV M (all ASSUMED unless cited)", size=9, bold=True)
y -= 0.05
for c in [
    f"30 MECH (remote): the old ST-2 strip inside the box, x 185.9-{gn.STRIP.bounds[2]:.1f}, y 246-{gn.STRIP.bounds[3]:.1f} (to the drum and the R 20 corner), "
    f"{gn.STRIP_SF:,.0f} SF. It does not touch the MECH / ELEC BAY 29 ({gn.GAP_TO_BAY:.1f} ft away), so it is marked remote (D-086). "
    f"It shares {gn.shared[22][1]:.1f} ft of wall with MECH (NE) 22 and {gn.shared[15][1]:.1f} ft with MECH (N) 15. No door drawn; access TBD.",
    f"Mechanical: {gn.MECH_M:,.0f} -> {gn.MECH_N:,.0f} SF = {gn.PCT_M:.2f} % -> {gn.PCT_N:.2f} % of {gn.TOT_N:,} GSF vs {gn.TARGET:.0f} % (D-072); "
    f"{gn.SHORT_N:,.0f} SF short. Set Rev D: {gn.PCT_D:.1f} %.",
    "GSF unchanged: the strip was already inside the envelope.",
]:
    y = sh.para(RX, y, RW, c, size=7.2, bullet="•", indent=0.14)
y -= 0.12
sh.text(RX, y, "MECHANICAL ROOMS (SF net of stairs; D-072 method)", size=9, bold=True)
y -= 0.2
cols = [RX, RX + 0.35, RX + 3.6, RX + 4.7, RX + 5.8]
for x, t in zip(cols, ["TAG", "ROOM", "REV M", "REV N", "CHANGE"]):
    sh.text(x, y, t, size=7, bold=True)
sh.line(RX, y - 0.04, RX + RW, y - 0.04, lw=0.5)
y -= 0.17
for t, n, a1 in gn.mech_rows:
    a0 = 0.0 if t == gn.SR["tag"] else a1
    for x, v in zip(cols, [str(t), n, f"{a0:,.0f}", f"{a1:,.0f}", f"{a1 - a0:+,.0f}"]):
        sh.text(x, y, v, size=7)
    y -= 0.14
for x, v in zip(cols, ["", "TOTAL MECH  (% of GSF)", f"{gn.MECH_M:,.0f} ({gn.PCT_M:.2f} %)", f"{gn.MECH_N:,.0f} ({gn.PCT_N:.2f} %)", f"{gn.MECH_N - gn.MECH_M:+,.0f}"]):
    sh.text(x, y, v, size=7, bold=True)
y -= 0.14
y -= 0.1
sh.text(RX, y, "AREA CHECK (no SF cap, D-056; L1, L2, total vs last rev, D-057)", size=9, bold=True)
y -= 0.2
for x, t in zip([RX, RX + 3.0, RX + 4.4, RX + 5.8], ["", "REV M / I", "REV N / I", "CHANGE"]):
    sh.text(x, y, t, size=7, bold=True)
sh.line(RX, y - 0.04, RX + RW, y - 0.04, lw=0.5)
y -= 0.17
for lab, v0, v1 in [("L1 footprint (envelope + annex + bay + bump-out)", g.L1_M, gn.L1_N), ("L2 area (envelope - open-to-below)", g.L2_M, gn.L2_N),
                    ("TOTAL GSF", g.TOT_M, gn.TOT_N)]:
    bold = lab.startswith("TOTAL")
    sh.text(RX, y, lab, size=7, bold=bold)
    for x, v in zip([RX + 3.0, RX + 4.4, RX + 5.8], [f"{v0:,}", f"{v1:,}", f"{v1 - v0:+,}"]):
        sh.text(x, y, v, size=7, bold=bold)
    y -= 0.15
y -= 0.04
y = sh.para(RX, y, RW, f"L1 = envelope polygon {g.env.area:,.0f} SF + annex 2,100 + bay 900 + bump-out 1,680. L2 = envelope - open-to-below "
            f"{g.OB_SF:,.0f} SF (Rev G method, D-079). Rev M / I = P2-G-003 Rev M. Vs Set Rev D and program lines: P2-G-003 Rev N.", size=6.8)
y -= 0.14
sh.text(RX, y, "ROOM SCHEDULE — LEVEL 1 (SF net of stairs, Rev N)", size=9, bold=True)
y -= 0.18
sched = list(gn.l1_sched)
half = (len(sched) + 1) // 2
y_top = y
for ci, chunk in enumerate((sched[:half], sched[half:])):
    cx = RX + ci * 4.25
    yy = y_top
    for t, n, ar in chunk:
        sh.text(cx, yy, str(t), size=6.3, bold=True)
        sh.text(cx + 0.28, yy, n[:34], size=6.3)
        sh.text(cx + 3.95, yy, f"{ar:,.0f}", size=6.3, align="right")
        yy -= 0.125
y = y_top - 0.125 * half - 0.1
sh.text(RX, y, "OPEN (not decided here)", size=9, bold=True)
y -= 0.04
for c in [f"East exits (Rev D method): X7 path {g.east['T1']['total']:.0f} ft, women (2) common path {g.east['T7']['common']:.0f} ft, men (2) "
          f"{g.east['T8']['common']:.0f} ft (75 ft max), corridor dead end {g.DEAD_END:.1f} ft. Details: P2-G-003 Rev N.",
          "Structure of the curved shell and the 30 ft drum; tier depth 1'-6\" or less (D-061). X7 / X11 discharge TBD (D-006).",
          f"Mechanical {gn.PCT_N:.2f} % vs {gn.TARGET:.0f} % (MEP OPEN, D-072); access to 30 MECH (remote) TBD."]:
    y = sh.para(RX, y, RW, c, size=7.0, bullet="•", indent=0.14)
sh.text(RX, 2.62, "Sources: params/phase2_plan_rev_j.yaml (= ARENA Set Rev D A-101 J); phase2_plan_rev_k.yaml; phase2_plan_rev_m.yaml; phase2_plan_rev_n.yaml; D-072, D-077..D-086.", size=6.3)

os.makedirs(os.path.join(a.out_dir, "pdf"), exist_ok=True)
os.makedirs(os.path.join(a.out_dir, "dxf"), exist_ok=True)
sh.render_pdf(os.path.join(a.out_dir, "pdf", "P2-A-101_RevN.pdf"))
sh.render_dxf(os.path.join(a.out_dir, "dxf", "P2-A-101_RevN.dxf"))
g.true_circle_dxf(os.path.join(a.out_dir, "dxf", "P2-A-101_RevN.dxf"), P, S)    # drum as a true circle / arc (D-074)
print("L1 %d | L2 %d | TOTAL %d (Rev M/I %d, %+d) | mech %.0f = %.2f %%" % (gn.L1_N, gn.L2_N, gn.TOT_N, g.TOT_M, gn.TOT_N - g.TOT_M, gn.MECH_N, gn.PCT_N))
