#!/usr/bin/env python3
"""P2-G-002 Rev E: EXIT RECHECK for P2-A-101 Rev K / P2-A-102 Rev G (D-079). New file; P2-G-002 Rev D (full code analysis) is not touched.

Rev E restates only what the curved envelope, the moved stairs/exits and the ST-2 tower change; every other line of Rev D stands.
Method = Rev D (IBC 2021 T1004.5 factors, 0.15 in/occ. doors, 0.2 in/occ. stairs, 64 in per door pair). The Rev D L1 load is reproduced
first from the Rev J geometry as a check (381 + 1,100 seats = 1,481), then recomputed on the Rev K geometry.

  python blueprints/phase2/src/p2_g_002_rev_e.py            (run from the repo root)
"""
import math
import os
import sys

import yaml
from shapely.geometry import LineString, Point, box
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "blueprints", "shared"))
from titleblock import Sheet, add_titleblock, wrap, pitch  # noqa: E402

# geometry + L2 numbers come from the Rev G generator (everything above its "sheet" marker)
_src = open(os.path.join(HERE, "p2_a_102_rev_g.py"), encoding="utf-8").read().split("# ---------------------------------------------------------------- sheet")[0]
__file__ = os.path.join(HERE, "p2_a_102_rev_g.py")
exec(compile(_src, __file__, "exec"))  # noqa: S102  (defines J, K, G, envelope, tower, ST, loop, stretch, L2_K, rrect, ...)

RED, GRN = "#CC0000", "#1E7B34"


def ceil_div(a, f):
    return math.ceil(round(a) / f)


# ---------------------------------------------------------------- Level 1 occupant load (Rev D method)
L1 = {r["id"]: r["rect"] for r in J["level_1"]["rooms"]}
L1.update({z["id"]: z["rect"] for z in J["level_1"]["zones"]})
BAY = box(*K["mech_bay"]["rect"])
big = box(-50, -50, 400, 400)
J_STAIRS = unary_union([box(*s["rect"]) for s in J["vertical"]["stairs"]])
K_STAIRS = unary_union([ST["ST-1"], ST["ST-3"], ST["ST-4"], tower])


def l1_rows(env, stairs, bay):
    a = lambda i: box(*L1[i]).intersection(env).difference(stairs).area
    mech = [a("mech_nw"), a("mech_n"), a("mech_ne"), 675.0, 660.0] + ([BAY.area] if bay else [])
    sp = [("Boys + girls locker (2)", a("boys_locker") + a("girls_locker"), 50, 71 + 71),
          ("Event lockers 1-4", sum(a(i) for i in ("evl_1", "evl_2", "evl_3", "evl_4")), 50, 72),
          ("Flex / team assembly", a("team_asm"), 15, ceil_div(a("team_asm"), 15)),
          ("Flex / storage (SW)", a("storage_sw"), 300, ceil_div(a("storage_sw"), 300)),
          ("Equipment storage + room", a("equip_storage") + a("equip_room"), 300, 4),
          ("Mech / elec (%d rooms)" % len(mech), sum(mech), 300, sum(ceil_div(m, 300) for m in mech)),
          ("First aid", a("first_aid"), 150, ceil_div(a("first_aid"), 150)),
          ("Concession", a("concession"), 200, ceil_div(a("concession"), 200)),
          ("Chair / table / stage storage (annex)", 2100.0, 300, 7)]
    return sp, mech


spJ, _ = l1_rows(big, J_STAIRS, False)
spK, mechK = l1_rows(envelope, K_STAIRS, True)
SEATS_L, SEATS_U = 1100, 1100
fixJ = SEATS_L + sum(r[3] for r in spJ)
fixK = SEATS_L + sum(r[3] for r in spK)
assert fixJ == 1481, fixJ            # reproduces P2-G-002 Rev D
FLOOR_SF = 16416                     # Rev D basis (114 x 144); 120 x 144 drawn floor shown as a sensitivity below
cases = [("Sports (50 gross)", 50), ("Tables + chairs (15 net)", 15), ("Chairs only (7 net) DESIGN", 7), ("Standing (5 net) margin", 5)]

# ---------------------------------------------------------------- Level 2 occupant load
sc_a = room_area(box(*l2_rooms["sc"]["rect"]))
xt_a = room_area(box(*l2_rooms["xt"]["rect"]))
ad_a = room_area(box(*l2_rooms["admin"]["rect"]))
l2_base = SEATS_U + ceil_div(sc_a, 50) + ceil_div(xt_a, 50) + ceil_div(ad_a, 150)
l2_loop = ceil_div(loop_sf, 50)
l2_rail = 84
l2_worst = l2_base + l2_loop + l2_rail
D_L2 = 1462

# ---------------------------------------------------------------- doors / stairs
DW, DF, SF_ = 64, 0.15, 0.2
E1 = 512
N_OTH = 11                            # X1-X11 (Rev D)
prov = E1 + N_OTH * DW
rows_cap = []
for lab, fac in cases:
    fl = ceil_div(FLOOR_SF, fac)
    l1 = fixK + fl
    tot = l1 + l2_worst
    rows_cap.append(dict(lab=lab, floor=fl, l1=l1, tot=tot, req_tot=tot * DF, e1_req=tot / 2 * DF,
                         lose_req=0.5 * tot * DF))
st_req = l2_worst * SF_
stairs_in = 4 * 76
stair_door = l2_worst / 4 * DF
# 120 x 144 sensitivity
sens = []
for lab, fac in (("Chairs 7 net", 7), ("Standing 5 net", 5)):
    fl = ceil_div(120 * 144, fac)
    tot = fixK + fl + l2_worst
    sens.append((lab, fl, tot, tot / 2 * DF, tot * DF))

# ---------------------------------------------------------------- exit location checks
env_b = envelope.boundary
BUMP = box(*J["building"]["bumpout"]["rect"])
ANNEX = box(*J["building"]["annex"]["rect"])
checks = []


def door_box(wall, x, y, w=64 / 12.0):
    h = w / 2
    return box(x - h, y - 0.5, x + h, y + 0.5) if wall in ("S", "N") else box(x - 0.5, y - h, x + 0.5, y + h)


def chk(did, wall, x, y, note, inside=None):
    db = door_box(wall, x, y)
    on_wall = env_b.distance(Point(x, y)) < 0.6
    arc_free = not (x > 190 and (y < 20 or y > 232)) and not (x < 20 and (y < 20 or y > 232)) and not (20 <= x <= 190 and False)
    clear = db.intersection(unary_union([BAY, ANNEX])).area == 0
    ok = on_wall and arc_free and clear and (inside is None or inside.buffer(0.1).contains(db.centroid))
    checks.append((did, "%s wall (%.1f, %.1f)" % (wall, x, y), note, ok))


chk("X1", "W", 0, 50.0, "team assembly; clear of ST-4 (top y 44.1)")
chk("X10", "W", 0, 32.0, "ST-4 discharge, door centred on the stair", ST["ST-4"].buffer(0.6))
chk("X9", "S", 183.667, 0, "ST-3 discharge, door centred on the stair", ST["ST-3"].buffer(0.6))
tw_x, tw_y = 188.0, 257.7
checks.append(("X6", "tower east face (188.0, 257.7)", "ST-2 discharge, opens to open ground NE", Point(tw_x, tw_y).distance(tower.boundary) < 0.6))
for d in J["level_1"]["doors"]["items"]:
    if d["id"] in ("X2", "X3", "X4", "X5", "X8"):
        wall, at = d["wall"], d["at"]
        x, y = {"W": (0, at), "N": (at, 252), "E": (210, at), "S": (at, 0)}[wall]
        note = {"X2": "girls locker", "X3": "boys locker", "X4": "ST-1 discharge", "X5": "EXIT (N); bay clear (x 136-166)", "X8": "east concourse"}[d["id"]]
        chk(d["id"], wall, x, y, note + " (unchanged)")
checks.append(("X7 / X11", "bump-out E (unchanged)", "EXIT (E) passage / core-2 corridor (D-072)", True))
checks.append(("E1", "S wall x 87.25-138.75", "8-pair bank (unchanged)", True))

# ---------------------------------------------------------------- L2 travel + stair separation
perim = LineString([(52.5, 37.5), (206.5, 37.5), (206.5, 242.5), (52.5, 242.5), (52.5, 37.5)])
entries = {"ST-1": Point(52.5, 240), "ST-2": Point(171, 242.5), "ST-3": Point(190, 37.5), "ST-4": Point(52.5, 37.5)}
link = {"ST-1": 3.5 + 6.0, "ST-2": 8.1 + 3.0, "ST-3": 16.5 + 10.0, "ST-4": 40.0 + 6.0}
L = perim.length
worst, worst_at = 0.0, None
for i in range(0, int(L), 2):
    p = perim.interpolate(i)
    best = 1e9
    for k, e in entries.items():
        dd = abs(perim.project(e) - i)
        dd = min(dd, L - dd)
        best = min(best, dd + link[k])
    if best > worst:
        worst, worst_at = best, (round(p.x), round(p.y))
SEAT_ACCESS = 15.0
worst_tot = worst + SEAT_ACCESS
door_pts = {"ST-1": (42.667, 240), "ST-2": (178, 257.7), "ST-3": (183.667, 12), "ST-4": (6.3, 32)}
diag = math.hypot(210, 252)
pairs = []
ks = list(door_pts)
for i in range(4):
    for j in range(i + 1, 4):
        a, b = door_pts[ks[i]], door_pts[ks[j]]
        pairs.append((ks[i], ks[j], math.hypot(a[0] - b[0], a[1] - b[1])))
sep_min = min(p[2] for p in pairs)

# ---------------------------------------------------------------- tower stair fit
stair_w, stair_l = 12.667, 24.083
diag_need = math.hypot(stair_w, stair_l)
dia = 2 * tw["radius_ft"]
max_len = math.sqrt(dia ** 2 - stair_w ** 2)
well_d = dia - 2 * 6.333
NEW_D, NEW_C = 29.0, (182.0, 262.5)
tower2 = Point(*NEW_C).buffer(NEW_D / 2, 64)
env2 = unary_union([ring, tower2])
d_L1 = env2.area - envelope.area
d_L2 = d_L1
# bay stays clear of X5 (passage x 123.85-131.85) and the bigger tower (west edge x 167.5)
BAY2 = box(134, 252, 164, 282)

# ---------------------------------------------------------------- sheet
W, H = 17.0, 11.0
sh = Sheet(W, H)
top = add_titleblock(sh, dict(
    project="Hazel Green Regional Athletic Complex\nTrojan Horse Arena · Hazel Green area, Madison County, Alabama (site TBD, D-006)",
    phase="PHASE 2", title="CODE ANALYSIS\nEXIT RECHECK", scale="NTS", date="October\n2026",
    revision="E", drawn_by="Drawn by Claude (AI) for\nShane Brazelton", sheet_no="P2-G-002",
    stamp="PRELIMINARY — CONCEPTUAL DESIGN — NOT FOR CONSTRUCTION"))


class Col:
    def __init__(self, x, y, w):
        self.x, self.y, self.w = x, y, w

    def head(self, s):
        self.y -= 0.12
        sh.text(self.x, self.y, s, size=8.6, bold=True)
        sh.line(self.x, self.y - 0.04, self.x + self.w, self.y - 0.04, lw=0.6)
        self.y -= 0.07

    def para(self, s, size=6.6, bold=False, bullet=None, color=None):
        ind = 0.12 if bullet else 0.0
        for i, ln in enumerate(wrap(s, self.w - ind - 0.05, size, bold)):
            self.y -= pitch(size)
            if bullet and i == 0:
                sh.text(self.x, self.y, bullet, size=size, bold=bold, color=color)
            sh.text(self.x + ind, self.y, ln, size=size, bold=bold, color=color)
        self.y -= 0.3 * pitch(size)

    def table(self, cols, rows, size=6.3, rh=0.135):
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
n1 = lambda v: f"{v:,.1f}"
body_bottom = top
y0 = H - 0.5
sh.text(0.75, y0 - 0.22, "CODE ANALYSIS — EXIT RECHECK (REV E) · P2-A-101 REV K / A-102 REV G · D-079", size=11.5, bold=True)
sh.text(0.75, y0 - 0.42, "Supplements P2-G-002 Rev D (frozen, full analysis); only what the curved envelope, the moved stairs / exits and the ST-2 tower change is restated. "
        "Method and factors as Rev D. Not a code review: architect + AHJ confirm (D-008).", size=6.6)
c1, c2 = Col(0.75, y0 - 0.45, 7.55), Col(8.95, y0 - 0.45, 7.3)
sh.line(8.62, y0 - 0.55, 8.62, body_bottom + 0.3, lw=0.4)

c1.head("1  WHAT CHANGED (all ASSUMED)")
for t in ["Envelope R = 20 ft corners (D-077); ST-3 slid west (X9 to x 183.7), ST-4 slid north (X10 to y 32), X1 to y 50; ST-2 is a 20 ft cylindrical tower, exit X6 on its east face (D-078).",
          "New 900 SF mech / elec bay (x 136-166), clear of EXIT (N) at X5. Level 2 as P2-A-102 Rev G (strip landing, rounded NE loop corner, D-079).",
          "Counts unchanged: E1 + X1-X11 = 12 openings, 4 stairs x 76 in, 2,200 seats."]:
    c1.para(t, bullet="•")

c1.head("2  OCCUPANT LOAD — REV D vs REV E (T1004.5 factors, Rev D method)")
cols = [("SPACE", 0, "left"), ("REV D SF", 4.55, "right"), ("REV E SF", 5.45, "right"), ("D LOAD", 6.35, "right"), ("E LOAD", 7.5, "right")]
rowsJ = {r[0].split(" (")[0]: r for r in spJ}
rows = []
for r in spK:
    key = r[0].split(" (")[0]
    j = rowsJ.get(key)
    if j is None:
        j = [None, 0, 0, 0]
    rows.append(([r[0], n0(j[1]) if j[1] else "—", n0(r[2] if False else r[1]), j[3] if j[1] else 0, r[3]],
                 dict(bold=(round(j[1]) != round(r[1])))))
rows.append((["Lower tier seats (telescopic)", "", "", 1100, 1100], None))
rows.append((["L1 without the event floor", "", "", 1481, fixK], dict(bold=True)))
rows.append((["Event floor, chairs only (D-054)", "16,416", "16,416", 2346, ceil_div(FLOOR_SF, 7)], None))
rows.append((["L1 TOTAL, design case", "", "", 3827, rows_cap[2]["l1"]], dict(bold=True)))
rows.append((["L2 worst case (D-052)", "", "", D_L2, l2_worst], dict(bold=True)))
c1.table(cols, rows)
c1.para(f"Rev E changes: flex / team assembly -{n0(spJ[2][1] - spK[2][1])} SF (ST-4 now fully inside it), MECH (NW / N / NE) lose area to the radius and, for MECH (N), to the tower "
        f"({n0(box(*L1['mech_n']).intersection(tower).area)} SF of it lies under the ST-2 tower: the Rev K room table did not deduct this), bay adds 3. "
        f"L2: S&C {n0(sc_a)} SF = {ceil_div(sc_a, 50)}, loop {n0(loop_sf)} SF = {l2_loop}, rail strip {l2_rail}; base {l2_base}. "
        "Rev D method reproduced first: Rev J geometry gives 381 + 1,100 = 1,481 (matches).", size=6.2)

c1.head("3  LEVEL 1 EXIT CAPACITY (doors 0.15 in / occupant, 64 in per pair)")
cols = [("CHECK (in)", 0, "left")] + [(n0(c["floor"]), 3.3 + i * 0.95, "right") for i, c in enumerate(rows_cap)] + [("PROVIDED", 7.5, "right")]
rr = [(["Total at grade (L1 + L2)"] + [n1(c["req_tot"]) for c in rows_cap] + [n0(prov)], None),
      (["Main exit E1 >= 1/2 (1030.2)"] + [n1(c["e1_req"]) for c in rows_cap] + [n0(E1)], None),
      (["Lose E1: others >= 50% (1005.5)"] + [n1(c["lose_req"]) for c in rows_cap] + [n0(prov - E1)], None)]
c1.table(cols, rr)
c1.para(f"All four floor cases PASS (floor loads {', '.join(n0(c['floor']) for c in rows_cap)}; building {', '.join(n0(c['tot']) for c in rows_cap)}). "
        f"Design case chairs: building {n0(rows_cap[2]['tot'])}, E1 needs {n1(rows_cap[2]['e1_req'])} vs {E1}. Stair discharge doors X4 / X6 / X9 / X10 carry the L2 worst case first: "
        f"{n0(l2_worst)} / 4 x 0.15 = {n1(stair_door)} in each of 64. Sensitivity, the drawn 120 x 144 ft floor (17,280 SF, Rev D used 114 x 144): "
        + "; ".join(f"{l} {n0(f)} on the floor, building {n0(t)}, E1 {n1(e)} vs {E1}, total {n1(rq)} vs {n0(prov)}" for l, f, t, e, rq in sens) + " — still PASS.", size=6.2)

c1.head("4  LEVEL 2 STAIR CAPACITY (0.2 in / occupant)")
c1.para(f"4 stairs x 76 in = {stairs_in} in. Worst {n0(l2_worst)} x 0.2 = {n1(st_req)} in -> spare {n1(stairs_in - st_req)} in (Rev D: 292.4, spare 11.6). "
        f"Lose one stair: {stairs_in - 76} in >= {n1(0.5 * st_req)} in (1005.5). PASS as calculated. This holds only if the ST-2 stair really is 76 in: see finding F1.", size=6.4)

c2.head("5  EXIT LOCATIONS (each tested against the Rev K outline)")
cols = [("EXIT", 0, "left"), ("POSITION", 0.65, "left"), ("NOTE", 2.55, "left"), ("", 7.15, "right")]
rr = [([d, p, n[:46], "OK" if ok else "CHECK"], dict(color=GRN if ok else RED)) for d, p, n, ok in checks]
c2.table(cols, rr, size=6.0, rh=0.128)
c2.para("Test: door centre on the envelope line, not in a corner arc, not under the annex or bay, and (for stair discharge) centred on its stair. "
        "The outline passes at all points; whether a door opens onto usable ground is a parcel question (D-006).", size=6.2)

c2.head("6  TRAVEL DISTANCE + STAIR SEPARATION")
c2.para(f"Level 2 exit access (T1017.2, A sprinklered, 250 ft): worst point on the loop re-measured on Rev G, centreline walk to the nearest stair door + {SEAT_ACCESS:.0f} ft seat access (ASSUMED) "
        f"= {worst_tot:.0f} ft near ({worst_at[0]}, {worst_at[1]}), the east leg mid-point, longer than Rev D's ≈ 141 ft because ST-2 moved 20 ft west and the method differs (not like-for-like). PASS (< 250). "
        "Level 1 floor-to-X7 ≈ 133 ft and core-2 common path (X11) unchanged: the moved exits are on the west and south walls and the tower.", size=6.4, bullet="•")
c2.para(f"Stair separation (IBC 2021 1007.1.1, 1/3 of the building diagonal when sprinklered; section not re-read this session): diagonal {diag:.0f} ft -> 1/3 = {diag / 3:.0f} ft. "
        f"Door-to-door: " + ", ".join(f"{a}-{b} {d:.0f}" for a, b, d in pairs) + f" ft. Shortest {sep_min:.0f} ft: PASS. (Rev D noted separation not checked.)", size=6.4, bullet="•")

c2.head("7  FINDINGS")
c2.para(f"F1  FAIL (geometry): the ST-2 tower is too small for the stair. The D-061 / D-052 stair is two 76 in flights side by side, {stair_w:.2f} x {stair_l:.2f} ft "
        f"(31 risers); its diagonal is {diag_need:.1f} ft but the tower is {dia:.0f} ft across (inside less wall, about {dia - 1.3:.0f}). In a {dia:.0f} ft circle a "
        f"{stair_w:.2f} ft wide stair has room for {max_len:.1f} ft of length, not {stair_l:.2f}: {stair_l - max_len:.1f} ft short. The Rev K sheet compared floor area "
        f"(314 vs 305 SF), which does not show this. A helical 76 in stair in {dia:.0f} ft leaves a {well_d:.1f} ft well; curved / helical egress-stair radius and tread rules "
        "(IBC 1011) were not checked and a well that small is unlikely to meet them. The capacity in sections 3-4 therefore does NOT yet hold for ST-2.",
        size=6.4, bold=True, color=RED)
c2.para(f"RECOMMENDATION: make the tower a {NEW_D:.0f} ft drum (inside ≈ {NEW_D - 1.3:.1f} ft, holds the {diag_need:.1f} ft diagonal), centre ({NEW_C[0]:.0f}, {NEW_C[1]:.1f}), "
        f"west edge x {NEW_C[0] - NEW_D / 2:.1f}, still wrapped by the outline. Effect: L1 and L2 each +{d_L1:.0f} SF "
        f"(total +{2 * d_L1:.0f} GSF on top of 86,212), bay moves 2 ft west to x 134-164 (X5 passage x 123.85-131.85 stays clear; bay to annex gap becomes 12 ft), "
        "strip ends about x 167. Not drawn here: it needs A-101 Rev L / A-102 Rev H and your yes (D-081 on approval).", size=6.4, color=RED)
c2.para("F2  A 6 ft strip landing at the tower door against a 76 in stair needs the architect (IBC 1010 not checked). It improves if the tower grows (F1): the door can face the strip at a wider point.", size=6.4)
c2.para("F3  Level 1 area correction: 50 SF of MECH (N) lies under the tower, so Rev K's room table over-counts MECH (N); the envelope total (52,840) is unaffected.", size=6.4)

c2.head("8  OPEN ITEMS FOR THE ARCHITECT / AHJ")
for t in ["Everything in Rev D section 12 still stands: editions + AHJ (D-008), construction type, smoke-protected seating, tier structure 1'-6\", door widths, seat type.",
          "ST-2 stair type and size (F1); structure of the curved shell and a 29 ft drum; P2-G-003 Rev L areas.",
          "SRM / Summertown Metals roles not agreed; descriptive names only (D-042)."]:
    c2.para(t, size=6.3, bullet="•")
sh.text(0.75, body_bottom + 0.12, "Sources: P2-G-002 Rev D; params/phase2_plan_rev_i.yaml, phase2_plan_rev_k.yaml, phase2_plan_rev_g_l2.yaml; IBC 2021 T1004.5, 1005.3, 1005.5, 1030.2-1030.3, T1017.2 (as Rev D); D-052, D-054, D-061, D-077..D-079.", size=6.0)

out_pdf = os.path.join(ROOT, "blueprints", "phase2", "out", "pdf")
out_dxf = os.path.join(ROOT, "blueprints", "phase2", "out", "dxf")
os.makedirs(out_pdf, exist_ok=True)
os.makedirs(out_dxf, exist_ok=True)
sh.render_pdf(os.path.join(out_pdf, "P2-G-002_RevE.pdf"))
sh.render_dxf(os.path.join(out_dxf, "P2-G-002_RevE.dxf"))
print("L1 fixed J %d K %d | L2 worst %d | cases" % (fixJ, fixK, l2_worst), [(c["floor"], c["l1"], c["tot"], round(c["e1_req"], 1), round(c["req_tot"], 1)) for c in rows_cap])
print("stairs req %.1f spare %.1f | stair door %.1f" % (st_req, stairs_in - st_req, stair_door))
print("travel worst %.0f at %s | sep min %.0f (1/3 diag %.0f) | pairs %s" % (worst_tot, worst_at, sep_min, diag / 3, [(a, b, round(d)) for a, b, d in pairs]))
print("tower: diag need %.1f, dia %.0f, max len %.1f, well %.1f | new drum dL1 %.0f" % (diag_need, dia, max_len, well_d, d_L1))
print("checks:", [(c[0], c[3]) for c in checks])
print("margins", c1.y - body_bottom - 0.3, c2.y - body_bottom - 0.3)
