#!/usr/bin/env python3
"""P2-G-003 Rev N: PROGRAM + AREA (D-057) after D-086 (old NE stair strip = MECH (remote)); mechanical % vs 5 % (D-072).

New file; P2-G-003 Revs A-M are not touched. Drawn areas from p2_plan_rev_n_geom.py (same numbers as P2-A-101 Rev N / P2-A-102 Rev I);
program lines carried from P2-G-003 Rev K.

  /workspace/.venv-keystone/bin/python blueprints/phase2/src/p2_g_003_rev_n.py --rev N [--out-dir DIR]     (run from the repo root)
"""
import argparse
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import p2_plan_rev_m_geom as g  # noqa: E402
import p2_plan_rev_n_geom as gn  # noqa: E402
sys.path.insert(0, os.path.join(g.ROOT, "blueprints", "shared"))
from palette import SCHOOL_RED  # noqa: E402
from titleblock import Sheet, add_titleblock, pitch, wrap  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--rev", choices=["N"], required=True)
ap.add_argument("--out-dir", default=os.path.join(g.ROOT, "blueprints", "phase2", "out"))
a = ap.parse_args()

W, H = 17.0, 11.0
sh = Sheet(W, H)
top = add_titleblock(sh, dict(
    project="Hazel Green Regional Athletic Complex\nTrojan Horse Arena · Hazel Green area, Madison County, Alabama (site TBD, D-006)",
    phase="PHASE 2", title="PROGRAM + AREA\nMECHANICAL · D-086", scale="NTS", date="October\n2026",
    revision="N", drawn_by="Drawn by KEYSTONE (AI) for\nShane Brazelton", sheet_no="P2-G-003",
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
sh.text(0.75, y0 - 0.22, "PROGRAM + AREA — REV N · P2-A-101 REV N / A-102 REV I · OLD NE STAIR STRIP = MECH (REMOTE), D-086", size=11.5, bold=True)
sh.text(0.75, y0 - 0.42, "Program lines unchanged from P2-G-003 Rev K (frozen, Set Rev D). Drawn size (D-057) measured on P2-A-101 Rev N / A-102 Rev I. "
        "No SF cap (D-056). Planning only: architect confirms.", size=6.8)
c1, c2 = Col(0.75, y0 - 0.45, 7.6), Col(8.95, y0 - 0.45, 7.3)
sh.line(8.62, y0 - 0.55, 8.62, top + 0.3, lw=0.4)

BD = g.BD
c1.head("1  SIZE — D-057: L1 FOOTPRINT · L2 AREA · TOTAL GSF · CHANGE")
cols = [("", 0, "left"), ("SET REV D", 3.15, "right"), ("REV M / I", 4.15, "right"), ("REV N / I", 5.15, "right"),
        ("vs M / I", 6.25, "right"), ("vs SET REV D", 7.5, "right")]
rows = []
for lab, d, l_, m_ in [("L1 FOOTPRINT", BD["l1_footprint_sf"], g.L1_M, gn.L1_N), ("L2 AREA", BD["l2_area_sf"], g.L2_M, gn.L2_N),
                       ("TOTAL GSF", BD["total_gsf"], g.TOT_M, gn.TOT_N)]:
    rows.append(([lab, n0(d), n0(l_), n0(m_), sg(m_ - l_), sg(m_ - d)], {"bold": lab.startswith("TOTAL")}))
c1.table(cols, rows, size=7.2, rh=0.17)
c1.para("Drawn on: SET REV D = P2-G-003 Rev K (A-101 J / A-102 F); REV M / I = P2-G-003 Rev M (D-082..D-084); REV N / I = this sheet. "
        "Totals are the sum of the rounded levels.", size=6.6)
c1.para(f"GSF unchanged vs Rev M / I: the {gn.STRIP_SF:,.0f} SF strip was already inside the envelope; D-086 only names it.", size=6.8, bold=True, color=SCHOOL_RED)

c1.head("2  HOW L1 AND L2 ARE MEASURED (Rev G method, D-079)")
c1.para(f"Envelope = 210 x 252 ft box with R = {g.R} ft corners (D-077) united with the {g.D_DIA:.0f} ft drum at ({g.DC[0]:.0f}, {g.DC[1]:.1f}): "
        f"{n0(g.env.area)} SF.", bullet="•")
c1.para(f"L1 = envelope + storage annex 2,100 + mech / elec bay 900 (x 134-164) + restroom bump-out 1,680 (y {g.BUMP.bounds[1]:.0f}-{g.BUMP.bounds[3]:.0f}) "
        f"= {gn.L1_N:,}.", bullet="•")
c1.para(f"L2 = envelope - open-to-below {n0(g.OB_SF)} (arena 132 x 168 + lobby 58 x 34) = {gn.L2_N:,}.", bullet="•")

c1.head("3  PROGRAM (carried from P2-G-003 Rev K; no program line changes)")
P = g.PROG
cols = [("PROGRAM LINE (G-003 K)", 0, "left"), ("SF", 5.2, "right"), ("DRAWN REV N", 6.4, "right"), ("DRAWN - PROG.", 7.55, "right")]
c1.table(cols, [
    (["L1 gross incl. annex + bump-out", n0(P["l1_gross_incl_annex_bump"]), "", ""], None),
    (["L2 gross (rooms x 1.25 + loop)", n0(P["l2_gross"]), "", ""], None),
    (["L1 + L2 gross", n0(P["l1_plus_l2_gross"]), "", ""], None),
    (["Program footprint (max + annex + bump-out) vs L1", n0(P["program_footprint"]), n0(gn.L1_N), sg(gn.L1_N - P["program_footprint"])], None),
    (["PROGRAM TOTAL GSF vs drawn TOTAL", n0(P["program_total_gsf"]), n0(gn.TOT_N), sg(gn.TOT_N - P["program_total_gsf"])], {"bold": True}),
], size=6.8)
c1.para("The drum, the R = 20 ft envelope and the bay are circulation / building form, not program lines; the stair line (4 x 76 in, 31 risers, "
        "12.67 x 24.08 ft each) is unchanged. Mechanical is not a separate program line (5 % of gross, R-014); see 5.", size=6.4)

c1.head("4  ROOMS THAT CHANGE vs REV M / I (SF net of stairs)")
cols = [("LEVEL / ROOM", 0, "left"), ("REV M / I", 4.9, "right"), ("REV N / I", 6.1, "right"), ("CHANGE", 7.5, "right")]
c1.table(cols, [([f"L1  {gn.SR['tag']}  {gn.SR['name']} (old NE stair strip)", "0", n0(gn.STRIP_SF), sg(gn.STRIP_SF)], None)], size=6.6)
c1.para("All other rooms on both levels unchanged (P2-A-101 Rev N, P2-A-102 Rev I).", size=6.4)

c2.head("5  MECHANICAL vs 5 % OF GSF (D-072 method, R-014)")
cols = [("TAG / ROOM", 0, "left"), ("REV M", 4.6, "right"), ("REV N", 5.8, "right"), ("CHANGE", 7.0, "right")]
rws = []
for t, n, a1 in gn.mech_rows:
    a0 = 0.0 if t == gn.SR["tag"] else a1
    rws.append(([f"{t}  {n}", n0(a0), n0(a1), sg(a1 - a0)], None))
rws.append((["TOTAL MECHANICAL", n0(gn.MECH_M), n0(gn.MECH_N), sg(gn.MECH_N - gn.MECH_M)], {"bold": True}))
rws.append((["% of TOTAL GSF", f"{gn.PCT_M:.2f} %", f"{gn.PCT_N:.2f} %", f"{gn.PCT_N - gn.PCT_M:+.2f}"], {"bold": True}))
c2.table(cols, rws, size=6.6)
c2.para(f"Target {gn.TARGET:.0f} % of {gn.TOT_N:,} = {gn.TARGET / 100 * gn.TOT_N:,.0f} SF: {gn.SHORT_N:,.0f} SF short. Set Rev D: {gn.BD['mech_sf']:,} / "
        f"{gn.BD['total_gsf']:,} = {gn.PCT_D:.1f} % (D-072). The rise since Set Rev D is mostly the 900 SF MECH / ELEC BAY (D-081). "
        "Planning check only; the MEP engineer sizes the rooms.", size=6.5)

c2.head("6  CARRIED FROM REV M (no change)")
for t in [f"Stair fit {g.FIT_MARGIN:.2f} ft spare in the {g.D_DIA:.0f} ft drum (D-082). Drum door at {g.ANG}°, landing left for the architect (D-085).",
          f"East side: T1 {g.east['T1']['total']:.0f} ft; common path {g.east['T7']['common']:.0f} / {g.east['T8']['common']:.0f} ft; corridor "
          f"{g.CORR_IN:.0f} in; dead end {g.DEAD_END:.1f} ft (P2-G-003 Rev M)."]:
    c2.para(t, size=6.5, bullet="•")

c2.head("7  FINDINGS + OPTIONS (not redesigned here)")
c2.para(f"F1  30 MECH (remote) does not touch the MECH / ELEC BAY ({gn.GAP_TO_BAY:.1f} ft away) and has no door drawn. It shares "
        f"{gn.shared[22][1]:.1f} ft of wall with MECH (NE) 22 and {gn.shared[15][1]:.1f} ft with MECH (N) 15. Options: (a) reach it through "
        "MECH (NE) 22; (b) merge it into 22; (c) MEP engineer decides. It is about 6 ft deep, so equipment fit is TBD.", size=6.4, bold=True, color=SCHOOL_RED)
c2.para(f"F2  Mechanical {gn.PCT_N:.2f} % vs {gn.TARGET:.0f} % ({gn.SHORT_N:,.0f} SF short); MEP OPEN (D-072).", size=6.4)
c2.para("F3  Drum door landing reaches 4.9 in onto the Level 2 loop: left for the architect (D-085). X7 / X11 discharge TBD (D-006).", size=6.4)

c2.head("8  SOURCES")
c2.para("D-057, D-072, D-077..D-086 (DECISIONS_ARENA); R-014; params/phase2_plan_rev_j.yaml (= Set Rev D A-101 J), _rev_k, _rev_g_l2, _rev_m, _rev_n; "
        "phase2_life_safety_rev_d.yaml / phase2_code_rev_d.yaml (handoff, read only); IBC 2021 1010.1.5, T1017.2, T1006.2.1, 1020.5, T1020.3. "
        "Revs A-M of P2-G-003 unchanged.", size=6.3)

os.makedirs(os.path.join(a.out_dir, "pdf"), exist_ok=True)
os.makedirs(os.path.join(a.out_dir, "dxf"), exist_ok=True)
sh.render_pdf(os.path.join(a.out_dir, "pdf", "P2-G-003_RevN.pdf"))
sh.render_dxf(os.path.join(a.out_dir, "dxf", "P2-G-003_RevN.dxf"))
print("G-003 N: L1 %d L2 %d TOTAL %d | vs M/I %+d | vs Set Rev D %+d | mech %.2f %%" % (gn.L1_N, gn.L2_N, gn.TOT_N, gn.TOT_N - g.TOT_M, gn.TOT_N - BD["total_gsf"], gn.PCT_N))
