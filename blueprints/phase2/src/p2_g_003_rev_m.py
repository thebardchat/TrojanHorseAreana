#!/usr/bin/env python3
"""P2-G-003 Rev M: PROGRAM + AREA (D-057) after D-082 (30 ft drum), D-083 (drum door west) and D-084 (east side = plan Rev J).

New file; P2-G-003 Revs A-L are not touched. Drawn areas come from p2_plan_rev_m_geom.py (same numbers as P2-A-101 Rev M /
P2-A-102 Rev I); program lines carried from P2-G-003 Rev K via params/phase2_plan_rev_m.yaml.

  /workspace/.venv-keystone/bin/python blueprints/phase2/src/p2_g_003_rev_m.py --rev M [--out-dir DIR]     (run from the repo root)
"""
import argparse
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import p2_plan_rev_m_geom as g  # noqa: E402
sys.path.insert(0, os.path.join(g.ROOT, "blueprints", "shared"))
from palette import SCHOOL_RED  # noqa: E402
from titleblock import Sheet, add_titleblock, pitch, wrap  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--rev", choices=["M"], required=True)
ap.add_argument("--out-dir", default=os.path.join(g.ROOT, "blueprints", "phase2", "out"))
a = ap.parse_args()

W, H = 17.0, 11.0
sh = Sheet(W, H)
top = add_titleblock(sh, dict(
    project="Hazel Green Regional Athletic Complex\nTrojan Horse Arena · Hazel Green area, Madison County, Alabama (site TBD, D-006)",
    phase="PHASE 2", title="PROGRAM + AREA\nD-082 · D-083 · D-084", scale="NTS", date="October\n2026",
    revision="M", drawn_by="Drawn by KEYSTONE (AI) for\nShane Brazelton", sheet_no="P2-G-003",
    stamp="PRELIMINARY — CONCEPTUAL DESIGN — NOT FOR CONSTRUCTION"))


class Col:
    def __init__(self, x, y, w):
        self.x, self.y, self.w = x, y, w

    def head(self, s):
        self.y -= 0.14
        sh.text(self.x, self.y, s, size=8.8, bold=True)
        sh.line(self.x, self.y - 0.04, self.x + self.w, self.y - 0.04, lw=0.6)
        self.y -= 0.07

    def para(self, s, size=6.8, bold=False, bullet=None, color=None):
        ind = 0.12 if bullet else 0.0
        for i, ln in enumerate(wrap(s, self.w - ind - 0.05, size, bold)):
            self.y -= pitch(size)
            if bullet and i == 0:
                sh.text(self.x, self.y, bullet, size=size, bold=bold, color=color)
            sh.text(self.x + ind, self.y, ln, size=size, bold=bold, color=color)
        self.y -= 0.3 * pitch(size)

    def table(self, cols, rows, size=6.8, rh=0.15):
        self.y -= rh
        for t, dx, al in cols:
            sh.text(self.x + dx, self.y, t, size=size, bold=True, align=al)
        sh.line(self.x, self.y - 0.035, self.x + self.w, self.y - 0.035, lw=0.5)
        self.y -= 0.02
        for cells, st in rows:
            st = st or {}
            self.y -= rh
            for (t, dx, al), v in zip(cols, cells):
                sh.text(self.x + dx, self.y, str(v), size=size, bold=st.get("bold", False), align=al, color=st.get("color"))
        self.y -= 0.06


n0 = lambda v: f"{v:,.0f}"
sg = lambda v: "±0" if round(v) == 0 else f"{v:+,.0f}"
y0 = H - 0.5
sh.text(0.75, y0 - 0.22, "PROGRAM + AREA — REV M · P2-A-101 REV M / A-102 REV I · 30 FT DRUM, DRUM DOOR, EAST SIDE = PLAN REV J", size=11.5, bold=True)
sh.text(0.75, y0 - 0.42, "Program lines unchanged from P2-G-003 Rev K (frozen, Set Rev D). Drawn size (D-057) measured on P2-A-101 Rev M / A-102 Rev I. "
        "No SF cap (D-056). Planning only: architect confirms.", size=6.8)
c1, c2 = Col(0.75, y0 - 0.45, 7.6), Col(8.95, y0 - 0.45, 7.3)
sh.line(8.62, y0 - 0.55, 8.62, top + 0.3, lw=0.4)

BD = g.BD
c1.head("1  SIZE — D-057: L1 FOOTPRINT · L2 AREA · TOTAL GSF · CHANGE")
cols = [("", 0, "left"), ("SET REV D", 3.15, "right"), ("REV L / H", 4.15, "right"), ("REV M / I", 5.15, "right"),
        ("vs L / H", 6.25, "right"), ("vs SET REV D", 7.5, "right")]
rows = []
for lab, d, l_, m_ in [("L1 FOOTPRINT", BD["l1_footprint_sf"], g.L1_L, g.L1_M), ("L2 AREA", BD["l2_area_sf"], g.L2_L, g.L2_M),
                       ("TOTAL GSF", BD["total_gsf"], g.TOT_L, g.TOT_M)]:
    rows.append(([lab, n0(d), n0(l_), n0(m_), sg(m_ - l_), sg(m_ - d)], {"bold": lab.startswith("TOTAL")}))
c1.table(cols, rows, size=7.2, rh=0.17)
c1.para("Drawn on: SET REV D = P2-G-003 Rev K (A-101 J / A-102 F); REV L / H = P2-G-003 Rev L (29 ft drum, D-081); REV M / I = this sheet. "
        "Totals are the sum of the rounded levels.", size=6.6)
c1.para(f"Why +{g.TOT_M - g.TOT_L} vs Rev L / H: the drum grows from 29 to {g.D_DIA:.0f} ft on both levels (+{g.L1_M - g.L1_L} each). The east side "
        "moves back to plan Rev J (D-084) with the same bump-out size (1,680 SF), so L1 does not change from it.", size=6.8, bold=True, color=SCHOOL_RED)

c1.head("2  HOW L1 AND L2 ARE MEASURED (Rev G method, D-079)")
c1.para(f"Envelope = 210 x 252 ft box with R = {g.R} ft corners (D-077) united with the {g.D_DIA:.0f} ft drum at ({g.DC[0]:.0f}, {g.DC[1]:.1f}): "
        f"{n0(g.env.area)} SF.", bullet="•")
c1.para(f"L1 = envelope + storage annex 2,100 + mech / elec bay 900 (x 134-164) + restroom bump-out 1,680 (y {g.BUMP.bounds[1]:.0f}-{g.BUMP.bounds[3]:.0f}) "
        f"= {g.L1_M:,}.", bullet="•")
c1.para(f"L2 = envelope - open-to-below {n0(g.OB_SF)} (arena 132 x 168 + lobby 58 x 34) = {g.L2_M:,}.", bullet="•")

c1.head("3  PROGRAM (carried from P2-G-003 Rev K; no program line changes)")
P = g.PROG
cols = [("PROGRAM LINE (G-003 K)", 0, "left"), ("SF", 5.2, "right"), ("DRAWN REV M", 6.4, "right"), ("DRAWN - PROG.", 7.55, "right")]
c1.table(cols, [
    (["L1 gross incl. annex + bump-out", n0(P["l1_gross_incl_annex_bump"]), "", ""], None),
    (["L2 gross (rooms x 1.25 + loop)", n0(P["l2_gross"]), "", ""], None),
    (["L1 + L2 gross", n0(P["l1_plus_l2_gross"]), "", ""], None),
    (["Program footprint (max + annex + bump-out) vs L1", n0(P["program_footprint"]), n0(g.L1_M), sg(g.L1_M - P["program_footprint"])], None),
    (["PROGRAM TOTAL GSF vs drawn TOTAL", n0(P["program_total_gsf"]), n0(g.TOT_M), sg(g.TOT_M - P["program_total_gsf"])], {"bold": True}),
], size=6.8)
c1.para("The drum, the R = 20 ft envelope and the bay are circulation / building form, not program lines; the stair line (4 x 76 in, 31 risers, "
        "12.67 x 24.08 ft each) is unchanged. Mech total about 4.1 % vs 5 % stays OPEN (D-072).", size=6.4)

c1.head("4  ROOMS THAT CHANGE vs REV L / H (SF net of stairs)")
cols = [("LEVEL / ROOM", 0, "left"), ("REV L / H", 4.9, "right"), ("REV M / I", 6.1, "right"), ("CHANGE", 7.5, "right")]
rws = []
for t, n, a1 in g.l1_sched:
    a0 = 0.0 if t == 25 else g.l1_prev.get(t, 0.0)      # Rev L tag 25 = the whole pop-out block, listed on its own row
    if abs(a1 - a0) > 0.5:
        rws.append(([f"L1  {t}  {n}", n0(a0), n0(a1), sg(a1 - a0)], None))
rws.append((["L1  25-27  Restroom pop-out block (Rev L)", "1,680", "0", "-1,680"], None))
rws += [([f"L2  {n}", n0(a0), n0(a1), sg(a1 - a0)], None) for t, n, a0, a1 in g.l2_sched if abs(a1 - a0) > 0.5]
rws.append(([f"L1 + L2  ST-2 drum (29 -> {g.D_DIA:.0f} ft, each level)", n0(g.gl.drum.area), n0(g.drum.area), sg(g.drum.area - g.gl.drum.area)], None))
c1.table(cols, rws, size=6.4, rh=0.14)

c2.head("5  STAIR FIT · DRUM DOOR LANDING (D-082, D-083)")
c2.para(f"Stair fit: 12.67 x 24.08 ft stair, diagonal {g.DIAG:.2f} ft in {g.D_IN:.1f} ft inside ({g.D_DIA:.0f} ft less "
        f"{g.DR['wall_allowance_ft']} ft walls, ASSUMED): {g.FIT_MARGIN:.2f} ft spare, about {g.FIT_MARGIN / 2 * 12:.0f} in at each end corner "
        f"(Rev L {g.FIT_PREV:.2f} ft).", size=6.6, bullet="•")
c2.para(f"Door: 64 in pair at {g.ANG}° (Rev H 240°), centre ({g.DOOR[0]:.1f}, {g.DOOR[1]:.1f}), swings into the drum. {g.ANG}° is the most westerly "
        f"point that keeps both jambs inside the north wall.", size=6.6, bullet="•")
c2.para("Rule, IBC 2021 1010.1.5 (1010.1.6 in IBC 2018): landing width not less than the stair or door width, whichever is greater (76 in), "
        "length in the direction of travel at least 44 in; door swing may reduce it by no more than 7 in.", size=6.6, bullet="•")
c2.para(f"Clearance: door centre to the loop edge along the door line {g.CL_CENTRE_IN:.1f} in (Rev H {g.CL_CENTRE_PREV_IN:.1f}) vs 44 in. "
        f"The 76 x 44 in rectangle square to the door reaches {g.LOOP_INTRUDE_IN:.1f} in onto the loop's outer edge at one corner; "
        f"the strip alone at the east jamb is {g.STRIP_ONLY_EAST_JAMB_IN:.1f} in.", size=6.6, bullet="•", bold=True, color=SCHOOL_RED)

c2.head("6  EXITS / TRAVEL / COMMON PATH RECHECK (east side = plan Rev J, D-084)")
e, rd = g.east, g.ES["rev_d_results"]
for t, ok in [
    (f"T1 event floor -> X7: {e['T1']['total']:.0f} ft vs {g.LIM['travel_ft']} (Set Rev D {rd['T1_ft']}).", e["T1"]["total"] <= g.LIM["travel_ft"]),
    (f"Women (2) common path {e['T7']['common']:.0f} ft (to X11 {e['T7']['total']:.0f}); men (2) {e['T8']['common']:.0f} ft "
     f"(to X11 {e['T8']['total']:.0f}); limit {g.LIM['common_path_ft']} (Set Rev D {rd['common_women_ft']} / {rd['common_men_ft']}).",
     max(e["T7"]["common"], e["T8"]["common"]) <= g.LIM["common_path_ft"]),
    (f"Public corridor (E) {g.CORR_IN:.0f} in vs {g.LIM['corridor_min_in']}; inside the envelope; dead end {g.DEAD_END:.1f} ft vs {g.LIM['dead_end_ft']}.",
     g.CORR_IN >= g.LIM["corridor_min_in"] and g.DEAD_END <= g.LIM["dead_end_ft"] and g.pc_inside),
    ("X7 (y {:.2f}), X11 (y {:.0f}), X8 (y {:.0f}) on the straight east wall, clear of the bump-out; X7 jamb {:.2f} ft north of it.".format(
        g.east_doors["X7"]["y"], g.east_doors["X11"]["y"], g.east_doors["X8"]["y"], g.X7_GAP_BUMP),
     all(d["on_wall"] and d["clear_of_bump"] for d in g.east_doors.values()) and g.bump_on_wall),
    (f"L2 travel, worst point {g.worst_at}: about {g.TRAVEL_L2:.0f} ft incl. 15 ft seat access. Stair separation {g.SEP_MIN:.0f} ft vs "
     f"1/3 diagonal {g.DIAG_BLDG / 3:.0f} ft.", g.TRAVEL_L2 <= g.LIM["travel_ft"] and g.SEP_MIN > g.DIAG_BLDG / 3),
    (f"X6 on the drum east face ({g.X6[0]:.1f}, {g.X6[1]:.1f}), clear of annex and bay; drum to bay {g.drum_bay_gap:.1f} ft; X5 lane {g.x5_lane:.0f} ft.",
     g.x6_on_drum and g.x6_clear and g.x5_gap_bay > 0),
]:
    c2.para(("PASS (as calculated)  " if ok else "CHECK  ") + t, size=6.5, bullet="•", color=None if ok else SCHOOL_RED)

c2.head("7  FINDINGS + OPTIONS (not redesigned here)")
c2.para(f"F1  Drum door landing: a 76 x 44 in landing square to the door reaches {g.LOOP_INTRUDE_IN:.1f} in onto the loop at one corner. "
        "Options: (a) architect counts that corridor corner as landing (door swings away from it); (b) widen the strip locally at the drum; "
        "(c) smaller door leaf (not checked vs capacity).", size=6.4, bold=True, color=SCHOOL_RED)
c2.para("F2  X7 / X11 discharge to the public way is TBD (D-006, site not chosen); not checked here.", size=6.4)
c2.para(f"F3  The old NE stair strip inside the box (about {g.old_st2_left:,.0f} SF on L1) stays unassigned.", size=6.4)
c2.para("F4  Mech total about 4.1 % vs 5 % stays OPEN (D-072). Drum structure / roof not drawn.", size=6.4)

c2.head("8  SOURCES")
c2.para("D-057, D-072, D-077..D-084 (DECISIONS_ARENA); params/phase2_plan_rev_j.yaml (= Set Rev D A-101 J), _rev_k, _rev_g_l2, _rev_l, _rev_m; "
        "phase2_life_safety_rev_d.yaml / phase2_code_rev_d.yaml (handoff, read only); IBC 2021 1010.1.5, T1017.2, T1006.2.1, 1020.5, T1020.3. "
        "Revs A-L of P2-G-003 unchanged.", size=6.3)

os.makedirs(os.path.join(a.out_dir, "pdf"), exist_ok=True)
os.makedirs(os.path.join(a.out_dir, "dxf"), exist_ok=True)
sh.render_pdf(os.path.join(a.out_dir, "pdf", "P2-G-003_RevM.pdf"))
sh.render_dxf(os.path.join(a.out_dir, "dxf", "P2-G-003_RevM.dxf"))
print("G-003 M: L1 %d L2 %d TOTAL %d | vs L/H %+d | vs Set Rev D %+d" % (g.L1_M, g.L2_M, g.TOT_M, g.TOT_M - g.TOT_L, g.TOT_M - BD["total_gsf"]))
