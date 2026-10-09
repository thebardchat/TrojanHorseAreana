#!/usr/bin/env python3
"""P2-G-003 Rev L: PROGRAM + AREA (D-057) after the 29 ft ST-2 drum (D-081, P2-T-017).

New file; p2_g_003.py (Revs A-K, Rev K frozen in Set Rev D) is not touched. Drawn areas come from p2_plan_rev_l_geom.py (the same
numbers as P2-A-101 Rev L / P2-A-102 Rev H); program lines are carried from P2-G-003 Rev K via params/phase2_plan_rev_l.yaml.

  /workspace/.venv-keystone/bin/python blueprints/phase2/src/p2_g_003_rev_l.py --rev L [--out-dir DIR]     (run from the repo root)
"""
import argparse
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import p2_plan_rev_l_geom as g  # noqa: E402
sys.path.insert(0, os.path.join(g.ROOT, "blueprints", "shared"))
from palette import SCHOOL_RED  # noqa: E402
from titleblock import Sheet, add_titleblock, pitch, wrap  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--rev", choices=["L"], required=True)
ap.add_argument("--out-dir", default=os.path.join(g.ROOT, "blueprints", "phase2", "out"))
a = ap.parse_args()

W, H = 17.0, 11.0
sh = Sheet(W, H)
top = add_titleblock(sh, dict(
    project="Hazel Green Regional Athletic Complex\nTrojan Horse Arena · Hazel Green area, Madison County, Alabama (site TBD, D-006)",
    phase="PHASE 2", title="PROGRAM + AREA\nSTAIR DRUM · D-081 · D-057", scale="NTS", date="October\n2026",
    revision="L", drawn_by="Drawn by KEYSTONE (AI) for\nShane Brazelton", sheet_no="P2-G-003",
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
sh.text(0.75, y0 - 0.22, "PROGRAM + AREA — REV L · P2-A-101 REV L / A-102 REV H · NE STAIR DRUM (D-081)", size=11.5, bold=True)
sh.text(0.75, y0 - 0.42, "Program lines unchanged from P2-G-003 Rev K (frozen, Set Rev D). Drawn size (D-057) measured on P2-A-101 Rev L / A-102 Rev H. "
        "No SF cap (D-056). Planning only: architect confirms.", size=6.8)
c1, c2 = Col(0.75, y0 - 0.45, 7.6), Col(8.95, y0 - 0.45, 7.3)
sh.line(8.62, y0 - 0.55, 8.62, top + 0.3, lw=0.4)

G3, BK = g.G3K, g.BASE
c1.head("1  SIZE — D-057: L1 FOOTPRINT · L2 AREA · TOTAL GSF · CHANGE vs LAST REV")
cols = [("", 0, "left"), ("G-003 K", 3.15, "right"), ("REV K / G", 4.15, "right"), ("REV L / H", 5.15, "right"),
        ("vs K / G", 6.25, "right"), ("vs G-003 K", 7.5, "right")]
rows = []
for lab, k3, kg, lv in [("L1 FOOTPRINT", G3["l1_footprint_sf"], g.L1_K, g.L1_L), ("L2 AREA", G3["l2_area_sf"], g.L2_K, g.L2_L),
                        ("TOTAL GSF", G3["total_gsf"], g.TOT_K, g.TOT_L)]:
    rows.append(([lab, n0(k3), n0(kg), n0(lv), sg(lv - kg), sg(lv - k3)], {"bold": lab.startswith("TOTAL")}))
c1.table(cols, rows, size=7.2, rh=0.17)
c1.para("Drawn on: G-003 K = A-101 J / A-102 F (Set Rev D); REV K / G = A-101 K / A-102 G as corrected on A-102 G (D-079); REV L / H = this ticket. "
        "Change vs last rev = vs REV K / G.", size=6.6)

c1.head("2  THE NUMBER YOU EXPECTED vs THE NUMBER COMPUTED")
exp = g.EXPECT
c1.para(f"Expected: +{exp['delta_gsf']:,} -> {exp['total_gsf']:,} GSF. Computed: +{g.TOT_L - g.TOT_K:,} -> {g.TOT_L:,} GSF. The +{g.TOT_L - g.TOT_K:,} "
        f"matches; the base does not. {exp['total_gsf']:,} = {G3['total_gsf']:,} (Set Rev D) + {exp['delta_gsf']:,}, which leaves out the "
        f"+{g.TOT_K - 85794:,} of the R = 20 ft envelope, tower and bay on Rev K / G (D-079: {g.TOT_K:,}). From Set Rev D the drum ticket and Rev K / G "
        f"together add {sg(g.TOT_L - G3['total_gsf'])} SF ({G3['total_gsf']:,} -> {g.TOT_L:,}).", size=7.0, bold=True, color=SCHOOL_RED)
c1.para(f"Rounding: G-003 K prints {G3['total_gsf']:,}; A-101 K / A-102 G use 85,794 for the same Rev J plan (56,861 + 28,933 each rounded).", size=6.4)

c1.head("3  HOW L1 AND L2 ARE MEASURED (Rev G method, D-079)")
c1.para(f"Envelope = 210 x 252 ft box with R = {g.R} ft corners (D-077) united with the {g.D_DIA:.0f} ft drum at ({g.DC[0]:.0f}, {g.DC[1]:.1f}): "
        f"{n0(g.env.area)} SF (Rev K / G: {n0(g.env_k.area)} with the 20 ft tower).", bullet="•")
c1.para(f"L1 = envelope + storage annex 2,100 + mech / elec bay 900 (x 134-164) + restroom bump-out 1,680 = {g.L1_L:,}.", bullet="•")
c1.para(f"L2 = envelope - open-to-below {n0(g.OB_SF)} (arena 132 x 168 + lobby 58 x 34) = {g.L2_L:,}. The drum counts on both levels, "
        f"so each level gains {g.L1_L - g.L1_K:,} SF.", bullet="•")

c1.head("4  PROGRAM (carried from P2-G-003 Rev K; no program line changes)")
P = g.PROG
cols = [("PROGRAM LINE (G-003 K)", 0, "left"), ("SF", 5.2, "right"), ("DRAWN REV L", 6.4, "right"), ("DRAWN - PROG.", 7.55, "right")]
c1.table(cols, [
    (["L1 gross incl. annex + bump-out", n0(P["l1_gross_incl_annex_bump"]), "", ""], None),
    (["L2 gross (rooms x 1.25 + loop)", n0(P["l2_gross"]), "", ""], None),
    (["L1 + L2 gross", n0(P["l1_plus_l2_gross"]), "", ""], None),
    (["Program footprint (max + annex + bump-out) vs L1", n0(P["program_footprint"]), n0(g.L1_L), sg(g.L1_L - P["program_footprint"])], None),
    (["PROGRAM TOTAL GSF vs drawn TOTAL", n0(P["program_total_gsf"]), n0(g.TOT_L), sg(g.TOT_L - P["program_total_gsf"])], {"bold": True}),
], size=6.8)
c1.para("The drum, the R = 20 ft envelope and the bay are circulation / building form, not program lines; the stair line (4 x 76 in, 31 risers, "
        "12.67 x 24.08 ft each) is unchanged. Mech total about 4.1 % vs 5 % stays OPEN (D-072).", size=6.4)

c2.head("5  ROOMS THAT CHANGE (SF net of stairs)")
cols = [("LEVEL / ROOM", 0, "left"), ("REV K / G", 4.6, "right"), ("REV L / H", 5.8, "right"), ("CHANGE", 7.0, "right")]
rws = [([f"L1  {t}  {n}", n0(a0), n0(a1), sg(a1 - a0)], None) for t, n, a0, a1 in g.l1_changed]
rws += [([f"L2  {n}", n0(a0), n0(a1), sg(a1 - a0)], None) for t, n, a0, a1 in g.l2_sched if abs(a1 - a0) > 0.5]
rws.append(([f"L1 + L2  ST-2 stair (20 ft tower -> {g.D_DIA:.0f} ft drum, each level)", n0(g.tower_k.area), n0(g.drum.area), sg(g.drum.area - g.tower_k.area)], None))
c2.table(cols, rws, size=6.6)
c2.para("All other L1 / L2 rooms, tiers, seats (2,200) and the loop are unchanged (P2-A-101 Rev L / A-102 Rev H schedules).", size=6.4)

c2.head("6  EXITS / TRAVEL RECHECK FOR THE DRUM (P2-G-002 Rev E method)")
pr = {f"{p_[0]}-{p_[1]}": p_[2] for p_ in g.pairs}
for t, ok in [
    (f"Stair fit: 12.67 x 24.08 ft stair, diagonal {g.DIAG:.1f} ft in about {g.D_IN:.1f} ft inside: fits, {g.FIT_MARGIN:.2f} ft spare. Closes F1 of Rev E as geometry.", True),
    ("Stair capacity unchanged: 4 x 76 in = 304 in vs 292.0 in (Rev E); L2 load unchanged (loop and rooms the same).", True),
    (f"X6 on the drum east face ({g.X6[0]:.1f}, {g.X6[1]:.1f}): on the outline, outside the box, clear of annex and bay.", g.x6_on_drum and g.x6_outside_box and g.x6_clear),
    (f"X5 / EXIT (N): bay at x 134 leaves a {g.x5_lane:.0f} ft lane between annex and bay ({g.x5_gap_bay:.2f} ft past the passage edge).", g.x5_gap_bay > 0),
    (f"Stair separation: nearest pair ST-1 / ST-2 {pr['ST-1-ST-2']:.0f} ft vs 1/3 diagonal {g.DIAG_BLDG / 3:.0f} ft (Rev E: 136).", g.SEP_MIN > g.DIAG_BLDG / 3),
    (f"L2 travel, worst point {g.worst_at}: about {g.TRAVEL:.0f} ft incl. 15 ft seat access (Rev E: 162).", True),
]:
    c2.para(("PASS (as calculated)  " if ok else "CHECK  ") + t, size=6.6, bullet="•", color=None if ok else SCHOOL_RED)

c2.head("7  FINDINGS + OPTIONS (not redesigned here)")
c2.para(f"F1  Drum fit is tight: {g.FIT_MARGIN:.2f} ft total (about {g.FIT_MARGIN / 2 * 12:.0f} in at each end corner) assumes about 8 in walls. "
        f"Options: (a) keep {g.D_DIA:.0f} ft, architect confirms wall; (b) 30 ft drum, about +{math.pi * (15 ** 2 - 14.5 ** 2):.0f} SF per level (rough); "
        "(c) stair turned / helical in the drum (IBC 1011 not checked).", size=6.5, bold=True, color=SCHOOL_RED)
c2.para(f"F2  Drum door (SW face) is {g.door_to_loop:.1f} ft from the loop edge along its swing line; landing at a 76 in stair door still needs the "
        "architect (Rev E F2, IBC 1010 not checked). Options: (a) door further west on the arc; (b) widen the strip at the drum.", size=6.5)
c2.para(f"F3  Drum to bay gap {g.drum_bay_gap:.1f} ft (x 164 to 167.5): maintenance only, not an exit path. X6 discharges east.", size=6.5)
c2.para("F4  The approved Rev K / G base draws the east side of plan Rev I (bump-out y 161-217, X7 on its east face, no X11; "
        "phase2_plan_rev_i.yaml), not plan Rev J (D-072: bump-out y 119-175, public corridor, X7 on the wall, X11), which Set Rev D froze. "
        "Rev L keeps the approved base. Options: (a) rebase on plan Rev J in the next A-101 rev (areas unchanged); (b) record that Rev K's east side is intended.",
        size=6.5, bold=True, color=SCHOOL_RED)
c2.para(f"F5  The old NE stair strip inside the box (x 185.9-210, y 246-252, about {g.old_st2_left:,.0f} SF on L1) is unassigned on Rev K and Rev L.", size=6.5)

c2.head("8  SOURCES")
c2.para("D-057, D-072, D-077..D-081 (DECISIONS_ARENA); ARENA P2-A-101_RevK / P2-A-102_RevG / P2-G-002_RevE (DXF read, regenerated identical); "
        "params/phase2_plan_rev_i.yaml, _rev_k, _rev_g_l2, _rev_l; P2-G-003 Rev K program lines. Revs A-K of P2-G-003 unchanged.", size=6.4)

os.makedirs(os.path.join(a.out_dir, "pdf"), exist_ok=True)
os.makedirs(os.path.join(a.out_dir, "dxf"), exist_ok=True)
sh.render_pdf(os.path.join(a.out_dir, "pdf", "P2-G-003_RevL.pdf"))
sh.render_dxf(os.path.join(a.out_dir, "dxf", "P2-G-003_RevL.dxf"))
print("G-003 L: L1 %d L2 %d TOTAL %d | vs K/G %+d | vs G-003 K %+d" % (g.L1_L, g.L2_L, g.TOT_L, g.TOT_L - g.TOT_K, g.TOT_L - G3["total_gsf"]))
