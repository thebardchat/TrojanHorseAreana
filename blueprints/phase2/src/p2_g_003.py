"""P2-G-003 — Phase 2 PROGRAM TEST-FIT (tabloid 17 x 11 landscape), vector PDF + DXF.

Rev A (FROZEN, build()): one-level area arithmetic against 55,000 SF read as total floor area.
Rev B (FROZEN, build_b()): two levels; ground footprint vs the 55,000 SF FOOTPRINT cap (D-031), total GSF,
stacking, vertical circulation, schematic bowl section.
Rev C (FROZEN, build_c()): suites to keep ~2,200 spectators (Shane 11:26 PM CT); suite level, hybrids. NOT a floor plan.
Rev D (FROZEN, build_d()): LOCKED PROGRAM (D-030): 16,400 SF floor, 2,200 bowl seats, 2 levels, no suites; FIXED vs TELESCOPIC columns.
Rev E (FROZEN, build_e()): LOCKED PROGRAM with MIX seating (D-009): telescopic lower, fixed upper; footprint margin; seats by side/tier.
Rev F (FROZEN 2026-10-04, approved by Shane 5:27 AM CT, part of Phase 2 Schematic Set Rev A, built by p2_set.py) (build_f()): Rev E + the Level 2 running / training loop (D-035): S&C and cross-training trimmed, loop replaces the upper concourse.
All numbers come from params/phase2.yaml + params/phase2_program.yaml via p2_testfit.py.
Layout constants below are sheet geometry only.

Run from the repo root:
  /workspace/.venv-keystone/bin/python blueprints/phase2/src/p2_g_003.py [--rev A|B|C|D|E|F] [--png PATH] [--out-dir DIR] [--force]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

BP = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BP / "shared"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from titleblock import Sheet, add_titleblock, pitch, text_width_in  # noqa: E402
import p2_testfit as tf  # noqa: E402

SHEET_NO = "P2-G-003"
W, H, M = 17.0, 11.0, 0.5
TB = "A-ANNO-TABL"


def n(x):
    return f"{round(x):,}"


def r100(x):
    return f"{int(round(x / 100.0)) * 100:,}"


def section(sh, x, y, s, size=11.5, first=False):
    """Heading below y (or at y for the first heading). Returns y for the next text."""
    if not first:
        y -= 0.34
    sh.text(x, y, s, size=size, bold=True)
    return y - 0.06


def build(p2, prog, ob, out):
    meta2, pm = p2["meta"], prog["meta"]
    sh = Sheet(W, H)
    body_bottom = add_titleblock(sh, {
        "project": f"{meta2['project']}\n{meta2['arena_name']} · {meta2['location']}",
        "phase": "PHASE 2",
        "title": f"{pm['title']}\n{pm['subtitle']}",
        "scale": pm["scale"],
        "date": meta2["sheet_date"],
        "revision": pm["revision"],
        "drawn_by": meta2["drawn_by"],
        "sheet_no": SHEET_NO,
        "stamp": meta2["stamp"],
    }, margin=M, tb_h=0.95, stamp_h=0.40)
    top = H - M - 0.12
    base, lean = out["base"], out["lean"]
    A, AL = base["A"], lean["A"]
    cap = A["cap"]

    # ================= column 1: area table =================
    x0, c1w = M + 0.18, 7.55
    y = section(sh, x0, top - 0.2, "1  AREA TABLE — NET SF (BASE CASE)", first=True) - 0.02
    cols = [x0, x0 + 3.2, x0 + 3.95, x0 + 6.35]       # room | SF | basis | status
    rp = 0.192
    fs = 8.6
    y -= rp
    for cx, lab in zip(cols, ["ROOM / SPACE", "NET SF", "BASIS", "STATUS · CONF."]):
        sh.text(cx + (0.6 if lab == "NET SF" else 0), y + 0.03, lab, size=7.8, bold=True,
                align="right" if lab == "NET SF" else "left", layer=TB)
    sh.line(x0, y - 0.04, x0 + c1w, y - 0.04, layer=TB, lw=0.8)
    groups = [("main", "Five tagged main spaces"), ("bowl", "Event bowl"), ("public", "Public / lobby"),
              ("support", "Support rooms (9 on plan)")]
    for gid, glab in groups:
        rows = [r for r in A["rows"] if r["group"] == gid]
        y -= rp
        sub = sum(r["sf"] or 0 for r in rows)
        sh.text(x0, y, glab.upper(), size=7.8, bold=True, layer=TB)
        if gid != "support":
            sh.text(cols[1] + 0.6, y, n(sub), size=7.8, bold=True, align="right", layer=TB)
        for r in rows:
            y -= rp
            name = r["name"]
            while text_width_in(name, fs) > cols[1] - cols[0] - 0.12:
                name = name[:-2]
            sh.text(x0 + 0.1, y, name, size=fs, layer=TB)
            sf = "TBD" if r["sf"] is None else n(r["sf"])
            sh.text(cols[1] + 0.6, y, sf, size=fs, bold=r["sf"] is None, align="right", layer=TB)
            sh.text(cols[2], y, r["short"], size=7.7, layer=TB)
            st = f"{r['status'].split(' ')[0]} · {r['confidence']}"
            sh.text(cols[3], y, st, size=7.3, layer=TB)
        sh.line(x0, y - 0.05, x0 + c1w, y - 0.05, layer=TB, lw=0.3)
    # totals
    g, mech = A["g"], A["mech"]
    y -= rp + 0.04
    for lab, val, b in [
        ("NET PROGRAM (excl. mechanical; TBD rooms left out)", n(A["net"]), True),
        (f"Mechanical = {mech:.0%} of gross (row above)", n(A["net_with_mech"] - A["net"]), False),
        (f"GROSS SF = {g:.2f} x (net + mechanical): walls, structure, circulation", n(A["gross"]), True),
    ]:
        sh.text(x0, y, lab, size=9, bold=b, layer=TB)
        sh.text(x0 + c1w, y, val, size=9.5, bold=b, align="right", layer=TB)
        y -= rp + 0.02
    sh.line(x0, y + 0.08, x0 + c1w, y + 0.08, layer=TB, lw=0.8)
    y -= 0.08
    y = sh.para(x0, y, c1w, f"Gross-up {g:.2f}: +25% for walls, structure and circulation (Groton MA feasibility study); "
                f"Loudoun County 2014 rec-center standard uses 80% efficiency for program space (÷0.80 = x1.25). "
                f"Mechanical {mech:.0%} of gross: MIL-HDBK-1027/4A (HVAC rooms). Formula: gross = {g:.2f} x net ÷ (1 − {g:.2f} x {mech:.2f}).", size=8.0)
    y = sh.para(x0, y, c1w, f"LEAN CHECK (most favorable cited inputs): telescopic-bleacher seating {AL['seat_sf']:.2f} SF/seat "
                f"and gross-up {AL['g']:.2f} (Loudoun walls/structure allowance only) give {n(AL['net'])} net -> {n(AL['gross'])} GSF. "
                f"Still {n(AL['over'])} SF over.", size=8.0, bold=True)
    col1_bottom = y

    # ================= column 2: seating + fixtures =================
    x2, c2w = x0 + c1w + 0.35, 3.95
    sh.line(x2 - 0.17, body_bottom + 0.12, x2 - 0.17, top, lw=0.5)
    y = section(sh, x2, top - 0.2, f"2  SEATING — {n(A['seats'])} SEATS (R-008)", first=True)
    sp = prog["factors"]["seating"]
    y = sh.para(x2, y, c2w, f"BASE: {sp['base_sf_per_seat']:.1f} SF/seat incl. aisles — Loudoun County 2014 recreation-center "
                f"standard (spectator seating, elevated). {n(A['seats'])} x {sp['base_sf_per_seat']:.1f} = {n(A['seats'] * sp['base_sf_per_seat'])} SF.", size=8.4)
    y = sh.para(x2, y, c2w, f"LEAN: telescopic bleachers {sp['lean_seat_width_in']} in/person (IBC 1004.6) x {sp['lean_row_depth_in']} in rows "
                f"(Hussey MAXAM) = {sp['lean_seat_width_in'] * sp['lean_row_depth_in'] / 144:.1f} SF, + one {sp['lean_aisle_in']} in stepped aisle "
                f"(IBC 1030.9.1) per {sp['lean_seats_between_aisles']} seats (1030.13.2.1) = {AL['seat_sf']:.2f} SF/seat -> "
                f"{n(AL['seats'] * AL['seat_sf'])} SF. No front walkway, cross aisles or wheelchair spaces counted.", size=8.4)
    y = sh.para(x2, y, c2w, "Seating type is OPEN (D-009). Seats stay outside the event floor (locked). IBC 2021 assembly egress is "
                "Section 1030 (1029 in the 2018 edition).", size=8.0)
    y = section(sh, x2, y, "3  OCCUPANT LOAD + FIXTURES (R-009)")
    fx = A["fx"]
    y = sh.para(x2, y, c2w, f"Load = {n(A['seats'])} seats (IBC 1004.6) + event floor {n(A['arena'])} SF ÷ 50 gross "
                f"(T1004.5 'exercise rooms', function ASSUMED) = {n(A['occ_floor'])} -> {n(fx['load'])} total; "
                f"half each sex = {n(fx['per_sex'])} (2902.1.1). IBC 2021 Table 2902.1, arenas (indoor sporting events):", size=8.4)
    rows = [("Water closets — men", "1/75 first 1,500", fx["wc_m"], f"urinals may be up to {fx['urinals_max']} (IPC 424.2, 67%)"),
            ("Water closets — women", "1/40 first 1,520", fx["wc_f"], ""),
            ("Lavatories — men", "1/200", fx["lav_m"], ""),
            ("Lavatories — women", "1/150", fx["lav_f"], ""),
            ("Drinking fountains", "1/1,000 (total)", fx["df"], "in concourse; no SF"),
            ("Service sink", "1", fx["service_sink"], "utility room (TBD)")]
    y -= 0.04
    for a, b, c, d in rows:
        y -= 0.185
        sh.text(x2 + 0.05, y, a, size=8.3, layer=TB)
        sh.text(x2 + 1.75, y, b, size=7.9, layer=TB)
        sh.text(x2 + 3.75, y, str(c), size=9, bold=True, align="right", layer=TB)
        if d:
            y -= 0.15
            sh.text(x2 + 0.25, y, d, size=7.3, layer=TB)
    y -= 0.05
    sfpf = prog["factors"]["restrooms"]["sf_per_fixture"]
    y = sh.para(x2, y, c2w, f"Room fixtures (WC + lav) = {fx['in_rooms']} x {sfpf} SF/fixture (ASSUMED; bare WC module from cited "
                f"minimums ≈ 27 SF) = {n(fx['in_rooms'] * sfpf)} SF. Athletes' toilets assumed inside the locker-room tags. "
                f"Code edition: Shane said IBC/IPC 2021; Madison County's page lists 2018 — same Table 2902.1 ratios. AHJ OPEN (D-008).", size=8.0)
    col2_bottom = y

    # ================= column 3: result + options + sources =================
    x3 = x2 + c2w + 0.35
    c3w = W - M - 0.28 - x3
    sh.line(x3 - 0.17, body_bottom + 0.12, x3 - 0.17, top, lw=0.5)
    y = section(sh, x3, top - 0.2, "4  RESULT", first=True) - 0.04
    bx_h = 1.02
    sh.rect(x3, y - bx_h, c3w, bx_h, lw=1.6)
    sh.text(x3 + c3w / 2, y - 0.32, "DOES NOT FIT IN " + n(cap) + " SF", size=13.5, bold=True, align="center")
    sh.text(x3 + c3w / 2, y - 0.58, f"Needs ≈ {r100(A['gross'])} GSF (base) · ≈ {r100(AL['gross'])} (lean)", size=8.6, bold=True, align="center")
    sh.text(x3 + c3w / 2, y - 0.80, f"Over by ≈ {r100(A['over'])} SF (base) · ≈ {r100(AL['over'])} SF (lean)", size=8.2, align="center")
    five = sum(r["sf"] for r in A["rows"] if r["group"] == "main")
    y -= bx_h + 0.02
    y = sh.para(x3, y, c3w, f"The 5 tagged spaces alone are {n(five)} net SF; grossed up they need ≈ "
                f"{r100(five * g / (1 - g * mech))} GSF before any seats, lockers or lobby.", size=8.2)
    y = section(sh, x3, y, "5  OPTIONS (SF MATH)")
    B, BL = base["B"], lean["B"]
    o = prog["option_b"]
    opts = [
        ("A  GROW THE BUILDING", f"to ≈ {r100(A['gross'])} GSF (base) or ≈ {r100(AL['gross'])} GSF (lean); keeps all {n(A['seats'])} seats and the {n(A['arena'])} SF floor."),
        ("B  SHRINK THE EVENT FLOOR", f"to {ob['ew']} x {ob['ns']} ft = {n(ob['sf'])} SF: 4 mats {o['mat_ft']} ft, 2x2, {o['clear_around_ft']} ft around and between "
         f"(NFHS 2-1-5), {o['table_zone_ft']} ft table strips N + S (ASSUMED); a {o['court_length_ft']}x{o['court_width_ft']} court + {o['court_runout_preferred_ft']} ft runout "
         f"({ob['court'][0]}x{ob['court'][1]}) fits inside. Building ≈ {r100(B['gross'])} GSF (base) / ≈ {r100(BL['gross'])} (lean): still over by "
         f"≈ {r100(B['over'])} / {r100(BL['over'])}."),
        ("C  CUT SEATS", f"not enough alone: with 0 seats the building is still ≈ {r100(base['C0']['gross'])} GSF (base) / ≈ {r100(lean['C0']['gross'])} (lean). "
         f"With B + C: ≈ {n(base['BC'])} seats fit (base) / ≈ {n(lean['BC'])} (lean)."),
    ]
    for t, d in opts:
        y -= 0.04
        y = sh.para(x3, y, c3w, t, size=9, bold=True)
        y = sh.para(x3 + 0.15, y + 0.04, c3w - 0.15, d, size=8.0)
    y = sh.para(x3, y, c3w, "Not credited: a 2nd level, a mezzanine, or rooms under the seating bowl (DR3). "
                "Whether 55,000 SF caps total floor area or footprint is OPEN (D-030).", size=7.8, bold=True)
    y = section(sh, x3, y, "6  SOURCES (retrieved 2026-10-03)", size=10)
    srcs = [
        "IBC 2021 (UpCodes, AL ed.): T1004.5, 1004.6, 1030.9.1, 1030.13.2.1, T2902.1, 2902.1.1; IPC 2021 424.2; IBC 2018 T2902.1 (compared)",
        "Madison County AL, Building Codes page (2018 I-codes)",
        "NFHS Wrestling Rules 2-1-5, 2-3 (2014-15 text; current book paywalled) — R-005",
        "NFHS Basketball Rules 1-1, 1-2-1 — R-012",
        "AHSAA 2026-27 Wrestling (14 weight classes)",
        "Loudoun County VA Capital Facilities Manual 2014, §4.3 Rec Center — R-014",
        "Groton MA Senior Center feasibility study (25% net-to-gross) — R-014",
        "MIL-HDBK-1027/4A in UFC 4-171-01N (HVAC 5% of gross) — R-014",
        "Hussey Seating MAXAM brochure (row spacing); ASI restroom guide (stall sizes)",
    ]
    for s_ in srcs:
        y = sh.para(x3, y + 0.03, c3w, s_, size=7.0, indent=0.12, bullet="·")
    col3_bottom = y

    floor = body_bottom + 0.08
    for nm, yy in (("col1", col1_bottom), ("col2", col2_bottom), ("col3", col3_bottom)):
        if yy < floor:
            raise SystemExit(f"LAYOUT OVERFLOW: {nm} runs {floor - yy:.2f} in into the stamp band")
    print(f"layout margins (in): col1 {col1_bottom - floor:.2f}, col2 {col2_bottom - floor:.2f}, col3 {col3_bottom - floor:.2f}")
    return sh


# ======================================================================================
# REV B — two levels (D-031). Rev A's build() above is frozen; do not edit it.
# ======================================================================================
def build_b(p2, prog, ob, out):
    meta2, pm = p2["meta"], prog["meta_rev_b"]
    sh = Sheet(W, H)
    body_bottom = add_titleblock(sh, {
        "project": f"{meta2['project']}\n{meta2['arena_name']} · {meta2['location']}",
        "phase": "PHASE 2",
        "title": f"{pm['title']}\n{pm['subtitle']}",
        "scale": pm["scale"],
        "date": meta2["sheet_date"],
        "revision": pm["revision"],
        "drawn_by": meta2["drawn_by"],
        "sheet_no": SHEET_NO,
        "stamp": meta2["stamp"],
    }, margin=M, tb_h=0.95, stamp_h=0.40)
    top = H - M - 0.12
    base, lean = out["base"], out["lean"]
    T = base["A50"]                      # table case: base, full program, ASSUMED 50/50 split
    cap = T["cap"]
    vc = prog["vertical_circulation"]
    st = T["stair"]
    rooms = {r["id"]: r for r in prog["rooms"]}
    stat = {"seating_lower": "CITED · MED", "seating_upper": "CITED · MED", "concourse_lower": "ASSUMED · LOW",
            "concourse_upper": "ASSUMED · LOW", "public_restroom_lower": "CITED · MED", "public_restroom_upper": "CITED · MED",
            "vertical_circulation": "CITED/ASSUMED"}

    def status_of(rid):
        if rid in stat:
            return stat[rid]
        r = rooms[rid]
        return f"{r['status'].split(' ')[0]} · {r['confidence'][:3] if r['confidence'] != 'HIGH' else 'HIGH'}"

    def name_of(rid):
        nm = {"seating_lower": f"Lower seating tier ({n(T['sl'])} seats)", "seating_upper": f"Upper seating tier ({n(T['su'])} seats)",
              "concourse_lower": "Lower concourse", "concourse_upper": "Upper concourse + champions wall",
              "public_restroom_lower": f"Public restrooms L1 ({T['fx1']['in_rooms']} fixtures)",
              "public_restroom_upper": f"Public restrooms L2 ({T['fx2']['in_rooms']} fixtures)",
              "vertical_circulation": f"Stairs ({T['exits']}) + elevator (1)", "mechanical": "Mechanical"}
        return nm.get(rid) or rooms[rid]["name"]

    # ================= column 1: stacking table =================
    x0, c1w = M + 0.18, 6.6
    y = section(sh, x0, top - 0.2, f"1  STACKING — NET SF BY LEVEL (BASE, FULL PROGRAM, {int(T['up'] * 100)}/{100 - int(T['up'] * 100)} SEATS)", first=True) - 0.02
    cols = [x0, x0 + 2.95, x0 + 3.6, x0 + 5.5]
    rp, fs = 0.178, 8.3
    y -= rp
    for cx, lab in zip(cols, ["ROOM / SPACE", "NET SF", "WHY THIS LEVEL", "SF STATUS"]):
        sh.text(cx + (0.55 if lab == "NET SF" else 0), y + 0.03, lab, size=7.6, bold=True,
                align="right" if lab == "NET SF" else "left", layer=TB)
    sh.line(x0, y - 0.04, x0 + c1w, y - 0.04, layer=TB, lw=0.8)
    for lvl, key, lab, sub in (("L1", "level_1", "LEVEL 1 (GROUND) — must stay at grade", T["N1"]),
                               ("L2", "level_2", "LEVEL 2 / MEZZANINE — can go up", T["N2"])):
        y -= rp
        sh.text(x0, y, lab.upper(), size=7.8, bold=True, layer=TB)
        sh.text(cols[1] + 0.55, y, n(sub), size=7.8, bold=True, align="right", layer=TB)
        for it in prog["stacking"][key]:
            rid = it["id"]
            if rid == "mechanical":
                continue
            y -= rp
            nm = name_of(rid)
            while text_width_in(nm, fs) > cols[1] - cols[0] - 0.05:
                nm = nm[:-2]
            av = rid in prog["stacking"]["arena_volume"]
            sh.text(x0 + 0.1, y, nm, size=fs, bold=av, layer=TB)
            sh.text(cols[1] + 0.55, y, n(T["sf"][rid]), size=fs, align="right", layer=TB)
            sh.text(cols[2], y, it["short"], size=7.1, layer=TB)
            sh.text(cols[3], y, status_of(rid), size=7.2, layer=TB)
        if lvl == "L1":
            y -= rp
            sh.text(x0 + 0.1, y, f"Mechanical ({T['mech']:.0%} of total gross)", size=fs, layer=TB)
            sh.text(cols[1] + 0.55, y, n(T["M"]), size=fs, align="right", layer=TB)
            sh.text(cols[2], y, "at grade (ASSUMED)", size=7.1, layer=TB)
            sh.text(cols[3], y, "CITED · LOW", size=7.2, layer=TB)
        sh.line(x0, y - 0.05, x0 + c1w, y - 0.05, layer=TB, lw=0.3)
    sh.text(x0, y - 0.2, "Bold rows = ARENA VOLUME (double height). Stage + utility room: no source, left out (TBD).", size=7.2, layer=TB)
    y -= 0.2
    g = T["g"]
    y -= rp + 0.06
    for lab, val, b in [
        (f"L1 GROSS = {g:.2f} x (L1 net + mechanical)", n(T["L1"]), False),
        (f"   of which ARENA VOLUME = {g:.2f} x (event floor + lower tier)", n(T["AV"]), False),
        (f"   of which L1 RING (rooms that can carry L2 above)", n(T["ring"]), False),
        (f"L2 GROSS = {g:.2f} x L2 net (must fit over the L1 ring)", n(T["L2"]), False),
        (f"GROUND FOOTPRINT = max(L1, arena volume + L2)  vs  {n(cap)} cap", n(T["F"]), True),
        ("TOTAL GSF, BOTH LEVELS (no longer capped, D-031)", n(T["G"]), True),
    ]:
        sh.text(x0, y, lab, size=8.8, bold=b, layer=TB)
        sh.text(x0 + c1w, y, val, size=9.2, bold=b, align="right", layer=TB)
        y -= rp + 0.02
    sh.line(x0, y + 0.08, x0 + c1w, y + 0.08, layer=TB, lw=0.8)
    y -= 0.06
    y = sh.para(x0, y, c1w, f"Same factors as Rev A (frozen): gross-up {g:.2f} base / {lean['A50']['g']:.2f} lean (R-014), seats "
                f"{T['seat_sf']:.1f} SF base / {lean['A50']['seat_sf']:.2f} lean (R-008), mechanical {T['mech']:.0%} of gross. "
                f"Each level is grossed up on its own. Rev A (one level) needed ≈ 86,100 GSF base.", size=7.9)
    y = sh.para(x0, y, c1w, "Not credited (conservative): rooms under the lower seating tier, upper-tier overhang past the L1 ring, "
                "rooftop mechanical. Lean case: lower tier is telescopic, so nothing can be built under it.", size=7.9)
    col1_bottom = y

    # ================= column 2: section diagram + vertical circulation =================
    x2, c2w = x0 + c1w + 0.35, 4.0
    sh.line(x2 - 0.17, body_bottom + 0.12, x2 - 0.17, top, lw=0.5)
    y = section(sh, x2, top - 0.2, "2  BOWL GEOMETRY — SECTION (NTS)", first=True)
    dg_h = 2.35
    gy = y - dg_h + 0.25                       # ground line
    dx0, dx1 = x2 + 0.05, x2 + c2w - 0.05
    ring = 1.08                                # L1 ring width each side (schematic)
    a0, a1 = dx0 + ring, dx1 - ring            # arena volume
    h1, h2, hr = 0.55, 1.05, 1.62
    sh.line(dx0 - 0.03, gy, dx1 + 0.03, gy, lw=1.2)
    sh.line(dx0, gy, dx0, gy + h2, lw=0.9); sh.line(dx1, gy, dx1, gy + h2, lw=0.9)
    sh.line(dx0, gy + h2, a0, gy + h2, lw=0.9); sh.line(a1, gy + h2, dx1, gy + h2, lw=0.9)
    sh.line(a0, gy + h2, a0 + 0.15, gy + hr, lw=0.9); sh.line(a1, gy + h2, a1 - 0.15, gy + hr, lw=0.9)
    sh.line(a0 + 0.15, gy + hr, a1 - 0.15, gy + hr, lw=0.9)
    for xa, xb in ((dx0, a0), (a1, dx1)):
        sh.line(xa, gy + h1, xb, gy + h1, lw=0.7)      # L2 floor
    sh.line(a0, gy, a0, gy + h1, lw=0.5); sh.line(a1, gy, a1, gy + h1, lw=0.5)
    fl0, fl1 = a0 + 0.40, a1 - 0.40                       # event floor
    for xs, xe in ((a0, fl0), (a1, fl1)):              # lower tier rake
        sh.line(xe, gy + 0.02, xs, gy + h1 - 0.05, lw=0.8)
    for xs, xe in ((a0 - 0.50, a0), (a1 + 0.50, a1)):    # upper tier rake (inner part of the L1 ring)
        sh.line(xe, gy + h1, xs, gy + h2 - 0.08, lw=0.8)
    sh.dashed(a0, gy + h1 + 0.02, a0, gy + h2, lw=0.4); sh.dashed(a1, gy + h1 + 0.02, a1, gy + h2, lw=0.4)
    cx = (a0 + a1) / 2
    sh.text(cx, gy + 0.08, "EVENT FLOOR", size=6.6, bold=True, align="center")
    sh.text(cx, gy + 0.98, "ARENA VOLUME", size=7.4, bold=True, align="center")
    sh.text(cx, gy + 0.84, "double height —", size=6.6, align="center")
    sh.text(cx, gy + 0.72, "nothing stacked above", size=6.6, align="center")
    sh.text((a0 + fl0) / 2 + 0.06, gy + h1 / 2 + 0.03, "lower tier", size=5.6, align="left")
    sh.text((a1 + fl1) / 2 - 0.06, gy + h1 / 2 + 0.03, "lower tier", size=5.6, align="right")
    for xa, xb in ((dx0, a0), (a1, dx1)):
        sh.text((xa + xb) / 2, gy + 0.30, "L1 RING", size=6.8, bold=True, align="center")
        sh.text((xa + xb) / 2, gy + 0.17, "lockers, foyer,", size=5.8, align="center")
        sh.text((xa + xb) / 2, gy + 0.06, "support", size=5.8, align="center")
        ox = (dx0 + a0 - 0.50) / 2 if xa == dx0 else (a1 + 0.50 + dx1) / 2
        sh.text(ox, gy + h1 + 0.36, "L2 rooms:", size=5.8, bold=True, align="center")
        sh.text(ox, gy + h1 + 0.25, "S&C, X-train,", size=5.8, align="center")
        sh.text(ox, gy + h1 + 0.14, "admin", size=5.8, align="center")
        tx = a0 - 0.12 if xa == dx0 else a1 + 0.12
        tx = a0 - 0.04 if xa == dx0 else a1 + 0.04
        sh.text(tx, gy + h2 - 0.10, "upper tier", size=5.6, align="right" if xa == dx0 else "left")
    yb = gy - 0.16
    sh.line(dx0, yb, dx1, yb, lw=0.4); sh.line(dx0, yb - 0.05, dx0, yb + 0.05, lw=0.4); sh.line(dx1, yb - 0.05, dx1, yb + 0.05, lw=0.4)
    sh.text((dx0 + dx1) / 2, yb - 0.15, "GROUND FOOTPRINT = arena volume + L1 ring", size=7.0, bold=True, align="center")
    y = yb - 0.20
    y = sh.para(x2, y, c2w, "The arena's high volume stays open to the roof, so no rooms go over the event floor or lower tier. The upper tier "
                "and every L2 room sit on the ring of L1 rooms around it (rooms under the seating). Fit needs L2 ≤ L1 ring; "
                "otherwise the ring grows and so does the footprint.", size=7.8)
    y = section(sh, x2, y, f"3  VERTICAL CIRCULATION — ON BOTH LEVELS", size=10.5)
    lvl_sf = T["vc_sf"]
    y = sh.para(x2, y, c2w,
                f"L2 occupant load (base, 50/50) = {n(T['su'])} seats + {T['l2_other']} in S&C, cross-training, admin "
                f"(T1004.5) = {n(T['l2_load'])} -> {T['exits']} exits (T1006.3.3). Stair capacity "
                f"{vc['stair_capacity_in_per_occupant']} in/occupant (1005.3.1 exc.: sprinklers + voice alarm, see below) -> "
                f"{n(T['l2_load'] * vc['stair_capacity_in_per_occupant'])} in total = {T['exits']} stairs x {st['width_in']:.0f} in "
                f"(min {vc['stair_min_width_in']} in, 1011.2; any 1 lost keeps ≥ 50%, 1005.5).", size=7.8)
    y = sh.para(x2, y, c2w,
                f"Each stair: {vc['floor_to_floor_in'] / 12:.0f} ft floor-to-floor (ASSUMED) = {st['risers']} risers of "
                f"{st['riser_in']:.2f} in (≤ 7 in) and 11 in treads (1011.5.2), {st['flights']} flights ≤ 12 ft rise (1011.8), "
                f"landings {st['landing_in']:.0f} in deep (1011.6): ≈ {n(st['sf'])} SF per level. Elevator: 1 (IBC 1104.4 accessible "
                f"route to a story over 3,000 SF), car ≥ 80 x 54 in (ADA T407.4.1), hoistway {vc['elevator_hoistway_sf_per_level']} SF "
                f"per level (ASSUMED). Total ≈ {n(lvl_sf)} net SF on EACH level.", size=7.8)
    y = sh.para(x2, y, c2w,
                "Open stairs OK between only two stories (1019.3 exc.). Sprinklers required: A-4 fire area > 12,000 SF or 300+ "
                "occupants (903.2.1.4); voice/alarm at 1,000+ (907.2.1.1). Sprinklered, the exit stairs serve as accessible means "
                "of egress without areas of refuge (1009.1, 1009.3.2, 1009.3.3); elevator egress only at 4+ stories (1009.2.1).", size=7.8)
    y = section(sh, x2, y, "4  RESTROOMS PER LEVEL (T2902.1)", size=10.5)
    f1, f2 = T["fx1"], T["fx2"]
    y = sh.para(x2, y, c2w,
                f"L1 load {n(f1['load'])} (lower seats + event floor ÷ 50): WC {f1['wc_m']} M / {f1['wc_f']} W, lav {f1['lav_m']} / "
                f"{f1['lav_f']} = {f1['in_rooms']} fixtures. L2 load {n(f2['load'])} seats: WC {f2['wc_m']} / {f2['wc_f']}, lav "
                f"{f2['lav_m']} / {f2['lav_f']} = {f2['in_rooms']}. Sized per level (conservative; 2902.3.3 allows one story of "
                f"travel). 50 SF/fixture ASSUMED. Rev A one-level count: 67.", size=7.8)
    col2_bottom = y

    # ================= column 3: result, smallest change, cited/assumed, sources =================
    x3 = x2 + c2w + 0.35
    c3w = W - M - 0.28 - x3
    sh.line(x3 - 0.17, body_bottom + 0.12, x3 - 0.17, top, lw=0.5)
    y = section(sh, x3, top - 0.2, "5  RESULT — FOOTPRINT VS 55,000 CAP", first=True, size=10.5) - 0.04
    Ab, Al = base["Abest"], lean["Abest"]
    bx_h = 1.10
    sh.rect(x3, y - bx_h, c3w, bx_h, lw=1.6)
    sh.text(x3 + c3w / 2, y - 0.27, "FULL PROGRAM, 2 LEVELS:", size=10.5, bold=True, align="center")
    sh.text(x3 + c3w / 2, y - 0.50, f"BASE ≈ {r100(Ab['F'])} SF — OVER by ≈ {r100(Ab['over'])}", size=10, bold=True, align="center")
    sh.text(x3 + c3w / 2, y - 0.72, f"LEAN ≈ {r100(Al['F'])} SF — FITS ({r100(-Al['over'])} spare)", size=10, bold=True, align="center")
    sh.text(x3 + c3w / 2, y - 0.93, f"Total GSF ≈ {r100(Ab['G'])} base / ≈ {r100(Al['G'])} lean (best seat split)", size=7.9, align="center")
    y -= bx_h + 0.08
    hdr = ["CASE", "SPLIT", "FOOTPRINT", "TOTAL GSF", "FIT?"]
    cx3 = [x3, x3 + 1.42, x3 + 2.75, x3 + 3.47, x3 + c3w]
    y -= 0.16
    for i, h_ in enumerate(hdr):
        sh.text(cx3[i] if i < 2 else cx3[i], y, h_, size=7.2, bold=True, align="left" if i < 2 else "right", layer=TB)
    sh.line(x3, y - 0.05, x3 + c3w, y - 0.05, layer=TB, lw=0.6)
    for sc, lab in (("base", "Base"), ("lean", "Lean")):
        for k, fl in (("A50", "22,000 floor"), ("Abest", "22,000 floor"), ("B50", f"{n(ob['sf'])} floor (B)"), ("Bbest", f"{n(ob['sf'])} floor (B)")):
            d = out[sc][k]
            if k.endswith("best") and abs(d["up"] - out[sc][k[0] + "50"]["up"]) < 1e-9:
                continue
            y -= 0.165
            sh.text(cx3[0], y, f"{lab}, {fl}", size=7.4, layer=TB)
            sh.text(cx3[1], y, f"{int(round(d['up'] * 100))}% up" + (" (best)" if k.endswith("best") else " (assum.)"), size=7.2, layer=TB)
            sh.text(cx3[2], y, n(d["F"]), size=7.6, bold=True, align="right", layer=TB)
            sh.text(cx3[3], y, n(d["G"]), size=7.6, align="right", layer=TB)
            sh.text(cx3[4], y, "YES" if d["fits"] else f"NO +{r100(d['over'])}", size=7.4, bold=True, align="right", layer=TB)
    sh.line(x3, y - 0.06, x3 + c3w, y - 0.06, layer=TB, lw=0.3)
    y -= 0.08
    y = sh.para(x3, y, c3w, "Full program = 22,000 SF floor + 2,200 seats + all 5 tags. Split = share of seats in the upper tier "
                "(50/50 ASSUMED; 'best' = lowest footprint in 30-70%). Sightlines not checked.", size=7.3)
    y = section(sh, x3, y, "6  SMALLEST CHANGE THAT FITS (BASE)", size=10.5)
    for t_, d_ in (
        (f"Option B floor ({n(ob['sf'])} SF, 4 mats 42 ft + tables + 1 court):",
         f"footprint ≈ {r100(base['Bbest']['F'])} — fits with all {n(T['seats'])} seats; total ≈ {r100(base['Bbest']['G'])} GSF."),
        (f"Or keep the floor and cut to ≈ {n(base['seats_max'])} seats",
         f"(−{n(T['seats'] - base['seats_max'])}; best split). Any floor ≤ ≈ {n(base['floor_max'])} SF fits with all seats."),
        ("Or build to the lean inputs", "(telescopic lower tier, 1.15 gross-up): full program fits as is."),
    ):
        y = sh.para(x3, y, c3w, t_, size=7.9, bold=True)
        y = sh.para(x3 + 0.15, y + 0.04, c3w - 0.15, d_, size=7.9)
    y = section(sh, x3, y, "7  CITED vs ASSUMED", size=10.5)
    y = sh.para(x3, y, c3w, "CITED: code rules (IBC 2021 ch. 10, 11, 9; ADA 2010), seat and gross-up factors, fixture ratios, "
                "lockers-at-event-level precedent (Reed, Orleans arenas). ASSUMED (verify): 15 ft floor-to-floor, 64 SF hoistway, "
                "50/50 split, which rooms go up, mechanical at grade, 50 SF/fixture, concourse 25%, A-4 occupancy.", size=7.5)
    y = section(sh, x3, y, "8  SOURCES (retrieved 2026-10-03)", size=10)
    srcs = [
        "IBC 2021 (UpCodes, AL ed.): 903.2.1.4, 907.2.1.1, 1005.3.1, 1005.5, T1006.3.3, 1009, 1011.2/.5.2/.6/.8, 1019.3, 1104.4, 2902.3.3 — R-015",
        "2010 ADA Standards (access-board.gov) 206.2.3, T407.4.1 — R-015",
        "Reed Arena Facility Guide; Orleans Arena Production Guide 2024 (venuecoalition.com) — R-015",
        "Rev A sources: R-008, R-009, R-012, R-014, R-005 (see Rev A)",
    ]
    for s_ in srcs:
        y = sh.para(x3, y + 0.03, c3w, s_, size=6.9, indent=0.12, bullet="·")
    col3_bottom = y

    floor = body_bottom + 0.08
    for nm, yy in (("col1", col1_bottom), ("col2", col2_bottom), ("col3", col3_bottom)):
        if yy < floor:
            raise SystemExit(f"LAYOUT OVERFLOW: {nm} runs {floor - yy:.2f} in into the stamp band")
    print(f"layout margins (in): col1 {col1_bottom - floor:.2f}, col2 {col2_bottom - floor:.2f}, col3 {col3_bottom - floor:.2f}")
    return sh


# ======================================================================================
# REV C — suites to keep ~2,200 spectators (Shane 11:26 PM CT). build() and build_b() are frozen.
# ======================================================================================
def build_c(p2, prog, out):
    meta2, pm = p2["meta"], prog["meta_rev_c"]
    su = prog["suites"]
    sh = Sheet(W, H)
    body_bottom = add_titleblock(sh, {
        "project": f"{meta2['project']}\n{meta2['arena_name']} · {meta2['location']}",
        "phase": "PHASE 2",
        "title": f"{pm['title']}\n{pm['subtitle']}",
        "scale": pm["scale"],
        "date": meta2["sheet_date"],
        "revision": pm["revision"],
        "drawn_by": meta2["drawn_by"],
        "sheet_no": SHEET_NO,
        "stamp": meta2["stamp"],
    }, margin=M, tb_h=0.95, stamp_h=0.40)
    top = H - M - 0.12
    gl = out["guests"]
    target = p2["spaces"]["seating"]["total"]
    cap = p2["building"]["footprint_cap_sf"]
    hc = su["headline_case"]
    best = out[("base", hc["floor_sf"], hc["placement"], hc["guests"])]
    floors = su["floors_checked"]
    full = floors[0]

    # ================= column 1: scenario table + suite module =================
    x0, c1w = M + 0.18, 7.2
    y = section(sh, x0, top - 0.2, f"1  SCENARIOS — BOWL SEATS + SUITES ≈ {n(target)} SPECTATORS (BASE INPUTS)", first=True) - 0.02
    hdr = [("FLOOR SF", 0, "l"), ("BOWL", 1.30, "r"), ("SUITES", 2.15, "r"), ("SPECT.", 2.85, "r"), ("SUITE SF", 3.65, "r"),
           ("FRONT FT", 4.40, "r"), ("FOOTPRINT", 5.30, "r"), ("TOTAL GSF", 6.15, "r"), ("LVL", 6.55, "r"), ("FIT", 7.2, "r")]
    rp = 0.198
    y -= rp
    for lab, dx, al in hdr:
        sh.text(x0 + dx, y + 0.03, lab, size=7.4, bold=True, align="left" if al == "l" else "right", layer=TB)
    sh.line(x0, y - 0.04, x0 + c1w, y - 0.04, layer=TB, lw=0.8)

    def row(cells, bold=False, size=8.2):
        nonlocal y
        y -= rp
        for (lab, dx, al), c in zip(hdr, cells):
            if c is None:
                continue
            sh.text(x0 + dx, y, c, size=size, bold=bold and lab in ("SPECT.", "FOOTPRINT", "FIT"), align="left" if al == "l" else "right", layer=TB)

    def cells(fl_lab, d):
        return [fl_lab, n(d["bowl"]), f"{d['ns']} x {d['guests']}" if d["ns"] else "0 needed", n(d["spectators"]),
                n(d["s_sf"] + d["s_corr"]) if d["ns"] else "0", f"{d['frontage_ft']:.0f}" if d["ns"] else "—",
                n(d["F"]), n(d["G"]), str(d["levels"]), "YES" if d["fits"] else "NO"]

    for fl in floors:
        if fl == full:
            y -= rp
            sh.text(x0, y, f"{n(fl)}  (locked floor): suites up to {n(target)} — NO FIT at 12, 16 or 20 guests, suites on L2 or L3.", size=8.2, bold=True, layer=TB)
            y -= 0.02
            sh.text(x0 + 0.1, y - rp + 0.02, "Most spectators that fit (suites on L3, bowl reduced to make room):", size=7.7, layer=TB)
            y -= rp - 0.02
            for gu in gl:
                d = out["max22"][gu]
                row(cells("   " + n(fl), d))
        elif all(out[("base", fl, "L3_top", gu)]["ns"] == 0 for gu in gl if out[("base", fl, "L3_top", gu)]):
            d = out[("base", fl, "L3_top", gl[0])]
            row(cells(n(fl), d))
        else:
            for gu in gl:
                d = out[("base", fl, "L3_top", gu)]
                if d is None:
                    row([n(fl), None, f"x {gu}", None, None, None, None, None, None, "NO"])
                else:
                    row(cells(n(fl), d), bold=(fl == hc["floor_sf"] and gu == hc["guests"]))
        sh.line(x0, y - 0.05, x0 + c1w, y - 0.05, layer=TB, lw=0.3)
    dl = out[("lean", full, "L3_top", gl[0])]
    row(cells(f"{n(full)} lean", dl))
    sh.line(x0, y - 0.05, x0 + c1w, y - 0.05, layer=TB, lw=0.3)
    y -= 0.06
    y = sh.para(x0, y, c1w, f"Suites on L3 (a suite level just above the top row of the upper tier) unless noted. Suites at the back of the upper "
                f"tier on Level 2 never fit on base inputs: Level 2 is already as big as the L1 ring under it. Bowl = largest bowl that fits "
                f"(10-seat steps, best tier split); suites = (target − bowl) ÷ guests, rounded up. SUITE SF = suites + 44 in corridor (net). "
                f"FRONT FT = total suite frontage. Bold row = headline. Lean inputs fit {n(target)} bowl seats with no suites (Rev B).", size=8.3)
    mx22 = max(out["max22"].values(), key=lambda d: d["spectators"])
    y = section(sh, x0, y, f"2  WHY THE {n(full)} SF FLOOR CAN'T REACH {n(target)} WITH SUITES", size=10.5)
    y = sh.para(x0, y, c1w, f"On base inputs the locked floor already fills the 55,000 footprint at ≈ 1,370 bowl seats (Rev B). A bowl seat "
                f"costs {best['seat_sf']:.1f} SF; a suite guest costs {su['sf_per_guest']} SF plus corridor. Suites on L3 add no footprint by "
                f"themselves, but the added floor area raises mechanical (5% of all gross, at grade) and stair widths on L1, so bowl "
                f"seats must come out to make room. Best mix: {n(mx22['bowl'])} bowl + {mx22['ns']} x {mx22['guests']} = "
                f"{n(mx22['spectators'])} spectators. Rooftop mechanical would help; not credited.", size=8.3)
    y = section(sh, x0, y, "3  SUITE MODULE (CITED SIZING, R-016)", size=10.5)
    mh = [("GUESTS", 0, "l"), ("SUITE SF", 1.25, "r"), ("WIDTH FT", 2.05, "r"), ("CORRIDOR SF", 3.05, "r"), ("CODE LOAD", 3.95, "r"), ("WHEELCHAIR", 4.85, "r"), ("GUEST SOURCE", 5.0, "l")]
    y -= rp
    for lab, dx, al in mh:
        sh.text(x0 + dx, y + 0.03, lab, size=7.4, bold=True, align="left" if al == "l" else "right", layer=TB)
    sh.line(x0, y - 0.04, x0 + c1w, y - 0.04, layer=TB, lw=0.6)
    srcs_g = {gl[0]: "Pitt Petersen (12 guests)", gl[1]: "WKU Diddle (16 tickets)", gl[2]: "Sheldon ISD (20 VIPs)"}
    import p2_testfit as _tf
    for gu in gl:
        m = _tf.suite_module(prog, gu, "base")
        y -= rp
        for (lab, dx, al), c in zip(mh, [str(gu), n(m["sf"]), f"{m['width_ft']:.0f}", n(m["corridor_sf"]), str(m["code_load"]), "1 + companion", srcs_g[gu]]):
            sh.text(x0 + dx, y, c, size=8.2, align="left" if al == "l" else "right", layer=TB)
    y -= 0.06
    y = sh.para(x0, y, c1w, f"Suite SF = {su['sf_per_guest']} SF/guest: Diddle Arena (WKU) suites 400 SF with 16 tickets; Texas Tech's standard suites "
                f"are 276 SF (cross-check). Includes seating ledge + lounge. Kitchenette/pantry: no source, left out (served from the "
                f"concession stand). Width rule (2 ledge rows x 18 in + 2 ft) is ASSUMED. Code load = seats (IBC 1004.6) + lounge ÷ 15 net "
                f"(T1004.5 unconcentrated): higher than the guest count, used for exits and fixtures. Revenue is out of scope: no $ figures.", size=8.3)
    col1_bottom = y

    # ================= column 2: section with suites + placement + 3rd-level flags =================
    x2, c2w = x0 + c1w + 0.35, 3.75
    sh.line(x2 - 0.17, body_bottom + 0.12, x2 - 0.17, top, lw=0.5)
    y = section(sh, x2, top - 0.2, "4  WHERE SUITES GO — SECTION (NTS)", first=True, size=10.5)
    dg_h = 2.45
    gy = y - dg_h + 0.25
    dx0, dx1 = x2 + 0.05, x2 + c2w - 0.05
    ring = 1.02
    a0, a1 = dx0 + ring, dx1 - ring
    h1, h2, h3, hr = 0.50, 0.95, 1.30, 1.72
    sh.line(dx0 - 0.03, gy, dx1 + 0.03, gy, lw=1.2)
    sh.line(dx0, gy, dx0, gy + h2, lw=0.9); sh.line(dx1, gy, dx1, gy + h2, lw=0.9)
    sh.line(dx0, gy + h2, a0 - 0.45, gy + h2, lw=0.9); sh.line(a1 + 0.45, gy + h2, dx1, gy + h2, lw=0.9)
    for xa, xb, s_ in ((dx0 + 0.25, a0 - 0.05, 1), (a1 + 0.05, dx1 - 0.25, -1)):   # suite level boxes
        sh.rect(xa, gy + h2, xb - xa, h3 - h2, lw=1.1)
    sh.line(a0 - 0.05, gy + h3, a0 + 0.12, gy + hr, lw=0.9); sh.line(a1 + 0.05, gy + h3, a1 - 0.12, gy + hr, lw=0.9)
    sh.line(a0 + 0.12, gy + hr, a1 - 0.12, gy + hr, lw=0.9)
    sh.line(dx0, gy + h2, dx0 + 0.25, gy + h2, lw=0.9)
    for xa, xb in ((dx0, a0), (a1, dx1)):
        sh.line(xa, gy + h1, xb, gy + h1, lw=0.7)
    sh.line(a0, gy, a0, gy + h1, lw=0.5); sh.line(a1, gy, a1, gy + h1, lw=0.5)
    fl0, fl1 = a0 + 0.36, a1 - 0.36
    for xs, xe in ((a0, fl0), (a1, fl1)):
        sh.line(xe, gy + 0.02, xs, gy + h1 - 0.05, lw=0.8)
    for xs, xe in ((a0 - 0.45, a0), (a1 + 0.45, a1)):
        sh.line(xe, gy + h1, xs, gy + h2 - 0.04, lw=0.8)
    cx = (a0 + a1) / 2
    sh.text(cx, gy + 0.08, "EVENT FLOOR", size=6.4, bold=True, align="center")
    sh.text(cx, gy + 1.02, "ARENA VOLUME", size=7.0, bold=True, align="center")
    sh.text(cx, gy + 0.89, "nothing above", size=6.3, align="center")
    for xa, xb in ((dx0, a0), (a1, dx1)):
        mx = (xa + xb) / 2
        sh.text(mx, gy + 0.24, "L1 RING", size=6.6, bold=True, align="center")
        sh.text(mx, gy + 0.11, "lockers, foyer", size=5.6, align="center")
        ox = (dx0 + a0 - 0.45) / 2 if xa == dx0 else (a1 + 0.45 + dx1) / 2
        sh.text(ox, gy + h1 + 0.27, "L2 rooms", size=5.8, bold=True, align="center")
        sh.text(ox, gy + h1 + 0.15, "S&C, X-train", size=5.4, align="center")
        sh.text(mx + (0.10 if xa == dx0 else -0.10), gy + h2 + 0.13, "L3 SUITES", size=6.4, bold=True, align="center")
    sh.text(a0 + 0.05, gy + h1 + 0.10, "< upper tier", size=5.4, align="left"); sh.text(a1 - 0.05, gy + h1 + 0.10, "upper tier >", size=5.4, align="right")
    sh.text(a0 + 0.30, gy + h1 / 2 - 0.02, "lower tier", size=5.4, align="left"); sh.text(a1 - 0.30, gy + h1 / 2 - 0.02, "lower tier", size=5.4, align="right")
    yb = gy - 0.15
    sh.line(dx0, yb, dx1, yb, lw=0.4); sh.line(dx0, yb - 0.05, dx0, yb + 0.05, lw=0.4); sh.line(dx1, yb - 0.05, dx1, yb + 0.05, lw=0.4)
    sh.text((dx0 + dx1) / 2, yb - 0.15, "FOOTPRINT unchanged by L3 if L3 ≤ L1 ring", size=6.9, bold=True, align="center")
    y = yb - 0.20
    y = sh.para(x2, y, c2w, f"L3 suites sit over the L2 rooms and the L1 ring, so they add floor area but not footprint "
                f"(headline: L3 ≈ {r100(best['L3'])} GSF vs L1 ring ≈ {r100(best['ring'])}). The catch: every added floor still adds "
                f"mechanical (5% of gross, at grade) and wider stairs on L1, and suites need {su['sf_per_guest']} SF per guest vs "
                f"6 SF per bowl seat. On Level 2 (back of the upper tier) suites never fit: L2 is already ≈ the size of the L1 ring.", size=8.3)
    y = section(sh, x2, y, "5  A SUITE LEVEL = A 3RD STORY", size=10.5)
    st = best["stair"]
    y = sh.para(x2, y, c2w,
                f"Headline case: L2 load {n(best['l2_load'])}, L3 (suites, code load) {n(best['l3_load'])} -> {best['exits']} stairs x "
                f"{st['width_in']:.0f} in on all 3 levels (T1006.3.3; 0.2 in/occ., 1005.3.1; width never reduced downstream, 1005.4).", size=8.3)
    for t_ in ("Open stairs lose the two-story exception (1019.3 exc. 1): enclosed exit stairs, 1-hour for fewer than 4 stories (1023.2).",
               "Elevator must stop at the suite level (1104.4); a wheelchair space + companion seat in every suite (1109.2.2.2, ADA 221.2.1.2), with lines of sight and dispersion (ADA 221.2.3, IBC 1109.2.4).",
               "Elevator egress still not required (< 4 stories, 1009.2.1). Allowed stories for the construction type (IBC ch. 5) NOT checked.",
               "Could the suites be a mezzanine instead of a story? Not checked (architect)."):
        y = sh.para(x2, y + 0.02, c2w, t_, size=7.9, indent=0.12, bullet="·")
    y = section(sh, x2, y, "6  PRECEDENTS (R-016)", size=10.5)
    for t_ in ("Diddle Arena (WKU): 16 suites, 400 SF, 16 tickets each, restrooms for the suite level, suites 'clear at the top of the arena' (2002).",
               "United Supermarkets Arena (Texas Tech): 24 suites at 276 SF + corner suites at 611 SF.",
               "Petersen Events Center (Pitt): 5 courtside suites up to 15; 16 smaller suites, about 12 guests.",
               "Sheldon ISD Panther Stadium (high school): 2 suites, 20 VIPs each; lounge seating, sink, refrigerator; restrooms on the level."):
        y = sh.para(x2, y + 0.02, c2w, t_, size=7.9, indent=0.12, bullet="·")
    col2_bottom = y

    # ================= column 3: headline, why, fixtures, cited/assumed, sources =================
    x3 = x2 + c2w + 0.35
    c3w = W - M - 0.28 - x3
    sh.line(x3 - 0.17, body_bottom + 0.12, x3 - 0.17, top, lw=0.5)
    y = section(sh, x3, top - 0.2, "7  RESULT (BASE INPUTS)", first=True, size=10.5) - 0.04
    bx_h = 1.30
    sh.rect(x3, y - bx_h, c3w, bx_h, lw=1.6)
    lines = [(f"{n(hc['floor_sf'])} SF FLOOR + SUITES:", 10.0, True),
             (f"{n(best['bowl'])} bowl + {best['ns']} suites x {best['guests']} = {n(best['spectators'])}", 9.6, True),
             (f"Footprint ≈ {n(best['F'])} vs {n(cap)}: FITS", 9.2, True),
             (f"Total ≈ {r100(best['G'])} GSF · {best['levels']} levels (suite level)", 8.4, False),
             (f"At {n(full)} SF: suites reach only ≈ {n(max(v['spectators'] for v in out['max22'].values()))}", 8.0, False)]
    yy = y - 0.26
    for t_, sz, b in lines:
        sh.text(x3 + c3w / 2, yy, t_, size=sz, bold=b, align="center")
        yy -= 0.235
    y -= bx_h + 0.04
    mf = out["maxfloor"]
    y = sh.para(x3, y, c3w, f"Largest floor that still reaches {n(target)} with suites: ≈ {n(min(mf.values()))}-{n(max(mf.values()))} SF. "
                f"At 20,000 SF it takes 30-50 suites (≈ 510-550 ft of suite front), beyond the cited arenas' 16-24 suites. "
                f"18,000 SF needs 13-22 suites (≈ 220-240 ft, both long sides). The headline is ≈ 6 SF under the cap: no margin.", size=8.3)
    y = section(sh, x3, y, "8  RESTROOMS + WHEELCHAIR SPACES", size=10.5)
    f1, f2, f3 = best["fx1"], best["fx2"], best["fx3"]
    y = sh.para(x3, y, c3w, f"T2902.1 per level (headline): L1 {f1['in_rooms']}, L2 {f2['in_rooms']}, L3 suites {f3['in_rooms']} fixtures "
                f"(WC {f3['wc_m']} M / {f3['wc_f']} W, lav {f3['lav_m']} / {f3['lav_f']}) = {f1['in_rooms'] + f2['in_rooms'] + f3['in_rooms']} total "
                f"(Rev B: 70). Suite fixtures use the suite code load, not the guest count. Wheelchair spaces: bowl {best['ws_bowl']} "
                f"(T1109.2.2.1) + 1 in each of {best['ns']} suites.", size=8.3)
    y = section(sh, x3, y, "9  CITED vs ASSUMED", size=10.5)
    y = sh.para(x3, y, c3w, "CITED: 12/16/20 guests, 400 SF suite (25 SF/guest), suite-level restrooms, suites at the top of the bowl "
                "(Diddle), IBC 1004.6, T1004.5, T1020.3, 1019.3, 1023.2, 1104.4, 1109.2, ADA 221.2. ASSUMED: suite width rule, "
                "44 in corridor, suite level over the ring, no kitchenette, mechanical at grade, all Rev B assumptions.", size=7.9)
    y = section(sh, x3, y, "10  STILL OPEN (D-030)", size=10.5)
    d16 = out[("base", floors[-1], "L3_top", gl[0])]
    y = sh.para(x3, y, c3w, f"Pick one: (a) {n(hc['floor_sf'])} SF floor + 13-22 suites, 3 levels; (b) {n(floors[-1])} SF floor, all "
                f"{n(target)} in the bowl, no suites, 2 levels (≈ {r100(d16['G'])} GSF); (c) keep {n(full)} SF with lean inputs "
                f"(telescopic lower tier), no suites, 2 levels (≈ {r100(dl['G'])} GSF). ~1,370 seats alone is rejected (D-032).", size=8.3)
    y = section(sh, x3, y, "11  SOURCES (retrieved 2026-10-03)", size=10)
    for s_ in ["WKU College Heights Herald 2002-10-22 (Diddle Arena suites); Texas Tech United Supermarkets Arena facts; Petersen Events Center Production Guide 2020; Sheldon ISD Panther Stadium info — R-016",
               "IBC 2021 (UpCodes) ch. 10, 11; 2010 ADA Standards 221.2 — R-016, R-015",
               "Rev A/B sources: R-008, R-009, R-014, R-015"]:
        y = sh.para(x3, y + 0.03, c3w, s_, size=7.2, indent=0.12, bullet="·")
    col3_bottom = y

    floor = body_bottom + 0.08
    for nm, yy in (("col1", col1_bottom), ("col2", col2_bottom), ("col3", col3_bottom)):
        if yy < floor:
            raise SystemExit(f"LAYOUT OVERFLOW: {nm} runs {floor - yy:.2f} in into the stamp band")
    print(f"layout margins (in): col1 {col1_bottom - floor:.2f}, col2 {col2_bottom - floor:.2f}, col3 {col3_bottom - floor:.2f}")
    return sh


def build_d(p2, prog, ob, out):
    """Rev D: LOCKED PROGRAM (D-030). FIXED vs TELESCOPIC columns (D-009 OPEN)."""
    meta2, pm = p2["meta"], prog["meta_rev_d"]
    lp = prog["locked_program"]
    plan = __import__("yaml").safe_load((BP / "params" / "phase2_plan.yaml").read_text(encoding="utf-8"))
    sh = Sheet(W, H)
    body_bottom = add_titleblock(sh, {
        "project": f"{meta2['project']}\n{meta2['arena_name']} · {meta2['location']}",
        "phase": "PHASE 2",
        "title": f"{pm['title']}\n{pm['subtitle']}",
        "scale": pm["scale"],
        "date": meta2["sheet_date"],
        "revision": pm["revision"],
        "drawn_by": meta2["drawn_by"],
        "sheet_no": SHEET_NO,
        "stamp": meta2["stamp"],
    }, margin=M, tb_h=0.95, stamp_h=0.40)
    top = H - M - 0.12
    F_, T_ = out["base"], out["telescopic"]
    cap = F_["cap"]
    rooms = {r["id"]: r for r in prog["rooms"]}
    floor = p2["spaces"]["arena"]["event_floor_sf"]
    bowl = p2["spaces"]["seating"]["bowl"]
    fx0, fy0, fx1, fy1 = plan["event_floor"]["rect"]
    few, fns = fx1 - fx0, fy1 - fy0

    # ================= column 1: area table by level =================
    x0, c1w = M + 0.18, 7.15
    y = section(sh, x0, top - 0.2, f"1  AREA BY LEVEL — {n(floor)} SF FLOOR, {n(bowl)} BOWL SEATS, 2 LEVELS, NO SUITES", first=True) - 0.02
    hdr = [("SPACE", 0, "l"), ("FIXED", 3.70, "r"), ("TELESCOPIC", 4.75, "r"), ("BASIS", 4.95, "l")]
    rp = 0.172
    y -= rp
    for lab, dx, al in hdr:
        sh.text(x0 + dx, y + 0.03, lab, size=7.4, bold=True, align="left" if al == "l" else "right", layer=TB)
    sh.line(x0, y - 0.04, x0 + c1w, y - 0.04, layer=TB, lw=0.8)

    def row(lab, a, b, basis="", bold=False, rule=False, size=7.9):
        nonlocal y
        y -= rp
        sh.text(x0 + 0.08 if not bold else x0, y, lab, size=size, bold=bold, layer=TB)
        sh.text(x0 + 3.70, y, a, size=size, bold=bold, align="right", layer=TB)
        sh.text(x0 + 4.75, y, b, size=size, bold=bold, align="right", layer=TB)
        if basis:
            while text_width_in(basis, 6.9) > c1w - 4.97 and len(basis) > 4:
                basis = basis[:-2].rstrip() + "…"
            sh.text(x0 + 4.95, y, basis, size=6.9, layer=TB)
        if rule:
            sh.line(x0, y - 0.05, x0 + c1w, y - 0.05, layer=TB, lw=0.4)

    def head(lab):
        nonlocal y
        y -= rp + 0.03
        sh.text(x0, y, lab, size=8.0, bold=True, layer=TB)

    sl, su = F_["sl"], F_["su"]
    label = {
        "arena": (f"Event floor (D-030, locked)", "phase2.yaml · D-030"),
        "seating_lower": (f"Lower tier seats ({n(sl)})", f"{F_['seat_sf']:.1f} / {T_['seat_sf']:.2f} SF/seat (R-008)"),
        "seating_upper": (f"Upper tier seats ({n(su)})", f"{F_['seat_sf']:.1f} / {T_['seat_sf']:.2f} SF/seat (R-008)"),
        "concourse_lower": ("Lower concourse", rooms["concourse"]["short"]),
        "concourse_upper": ("Upper concourse / hall of champions wall", "same factor, upper seats"),
        "public_restroom_lower": (f"Public restrooms L1 ({F_['fx1']['in_rooms']} fixtures)", "T2902.1 x 50 SF (R-009)"),
        "public_restroom_upper": (f"Public restrooms L2 ({F_['fx2']['in_rooms']} fixtures)", "T2902.1 x 50 SF (R-009)"),
        "vertical_circulation": (f"Stairs ({F_['exits']}) + elevator", "R-015"),
    }
    def lab_of(i):
        if i in label:
            return label[i]
        r = rooms[i]
        nm = r["name"].replace(" (as tagged; D-013)", " (D-013)").replace(" (DR3)", "")
        return nm, r["short"]
    head("LEVEL 1 (net SF)")
    for i in F_["l1_ids"]:
        lab, bas = lab_of(i)
        row(lab, n(F_["sf"][i]), n(T_["sf"][i]), bas)
    row("L1 net", n(F_["N1"]), n(T_["N1"]), bold=True)
    row("Mechanical (5% of total gross, at grade)", n(F_["M"]), n(T_["M"]), "R-014 · LOW")
    row(f"L1 GROSS (x {F_['g']:.2f})", n(F_["L1"]), n(T_["L1"]), "R-014 gross-up", bold=True, rule=True)
    head("LEVEL 2 (net SF)")
    for i in F_["l2_ids"]:
        lab, bas = lab_of(i)
        row(lab, n(F_["sf"][i]), n(T_["sf"][i]), bas)
    row("L2 net", n(F_["N2"]), n(T_["N2"]), bold=True)
    row(f"L2 GROSS (x {F_['g']:.2f})", n(F_["L2"]), n(T_["L2"]), bold=True, rule=True)
    head("FIT CHECK")
    row("Arena volume gross (floor + lower tier, double height)", n(F_["AV"]), n(T_["AV"]))
    row("L1 ring = L1 − arena volume (L2 must sit over it)", n(F_["ring"]), n(T_["ring"]))
    row("L2 over the ring?", "YES" if F_["l2_fits_over_ring"] else "NO", "YES" if T_["l2_fits_over_ring"] else "NO",
        f"margin {n(F_['ring'] - F_['L2'])} / {n(T_['ring'] - T_['L2'])}")
    row("FOOTPRINT = max(L1, arena volume + L2)", n(F_["F"]), n(T_["F"]), bold=True)
    row(f"Footprint cap (D-031) · margin", f"{n(cap - F_['F'])}", f"{n(cap - T_['F'])}", f"cap {n(cap)} SF")
    row("FITS 55,000 FOOTPRINT?", "YES" if F_["fits"] else "NO", "YES" if T_["fits"] else "NO", bold=True)
    row("TOTAL GSF (2 levels)", n(F_["G"]), n(T_["G"]), "not capped (D-031)", bold=True, rule=True)
    y -= 0.04
    y = sh.para(x0, y, c1w, f"FIXED = {F_['seat_sf']:.1f} SF/seat elevated seating. TELESCOPIC = every bowl seat on bleacher geometry "
                f"({T_['seat_sf']:.2f} SF/seat). Both columns use the same x {F_['g']:.2f} gross-up, so only the seating type differs. "
                f"Tier split {round(lp['upper_share'] * 100)}/{round((1 - lp['upper_share']) * 100)} ASSUMED. Stage and utility room: no source, "
                f"left out. Seating type stays OPEN (D-009).", size=7.9)
    col1_bottom = y

    # ================= column 2: floor check + fixtures + stairs + wheelchair =================
    x2, c2w = x0 + c1w + 0.35, 4.05
    sh.line(x2 - 0.17, body_bottom + 0.12, x2 - 0.17, top, lw=0.5)
    y = section(sh, x2, top - 0.2, "2  EVENT FLOOR CHECK (R-005, R-012)", first=True, size=10.5)
    s = 0.0155                                    # in per ft (diagram only, NTS on the sheet)
    dw, dh = few * s, fns * s
    gx, gy = x2 + 0.1, y - 0.12 - dh
    sh.rect(gx, gy, dw, dh, lw=1.2)
    tz = plan["event_floor"]["table_zone_ft"]
    sh.dashed(gx, gy + tz * s, gx + dw, gy + tz * s, lw=0.4); sh.dashed(gx, gy + dh - tz * s, gx + dw, gy + dh - tz * s, lw=0.4)
    mft = p2["spaces"]["arena"]["mat_ft"]
    for m in plan["mats"]:
        mx, my = m["origin"]
        sh.rect(gx + (mx - fx0) * s, gy + (my - fy0) * s, mft * s, mft * s, lw=0.9)
        sh.text(gx + (mx - fx0 + 3) * s, gy + (my - fy0 + mft - 3) * s - 0.09, m["id"], size=6.5, bold=True)
    cx0, cy0, cx1, cy1 = plan["court"]["rect"]
    ro = plan["court"]["runout_ft"]
    sh.dashed(gx + (cx0 - fx0) * s, gy + (cy0 - fy0) * s, gx + (cx1 - fx0) * s, gy + (cy0 - fy0) * s, lw=0.6, dash=0.06, gap=0.04)
    sh.dashed(gx + (cx0 - fx0) * s, gy + (cy1 - fy0) * s, gx + (cx1 - fx0) * s, gy + (cy1 - fy0) * s, lw=0.6, dash=0.06, gap=0.04)
    sh.dashed(gx + (cx0 - fx0) * s, gy + (cy0 - fy0) * s, gx + (cx0 - fx0) * s, gy + (cy1 - fy0) * s, lw=0.6, dash=0.06, gap=0.04)
    sh.dashed(gx + (cx1 - fx0) * s, gy + (cy0 - fy0) * s, gx + (cx1 - fx0) * s, gy + (cy1 - fy0) * s, lw=0.6, dash=0.06, gap=0.04)
    sh.text(gx + dw / 2, gy + dh + 0.05, f"{few:g} ft", size=6.5, align="center")
    sh.text(gx - 0.05, gy + dh / 2, f"{fns:g} ft", size=6.5, align="center", rot=90)
    sh.text(gx + (cx0 - fx0) * s + 0.03, gy + (cy0 - fy0) * s + 0.04, "court", size=5.4)
    sh.text(gx + dw / 2, gy + 0.07, "table / bench zone", size=5.4, align="center")
    sh.text(gx + dw / 2, gy + dh - 0.13, "table / bench zone", size=5.4, align="center")
    tx = gx + dw + 0.15
    cw_ = x2 + c2w - tx
    yy = y - 0.1
    ob_ew, ob_ns, ob_sf = ob["ew"], ob["ns"], ob["sf"]
    for t_ in (f"Drawn {few:g} x {fns:g} ft = {n(few * fns)} SF (locked {n(floor)}; +{n(few * fns - floor)} SF).",
               f"E-W: 2 x {mft} ft mats + 3 x {plan['event_floor']['clear_ft']} ft clear (NFHS 2-1-5) = {few:g} ft.",
               f"N-S: same {few:g} ft + two {tz} ft table/bench zones (table ≥ 10 ft from mat, NFHS 2-3; depth ASSUMED).",
               f"Rev A layout {ob_ew} x {ob_ns} = {n(ob_sf)} SF (6 ft tables) fits inside: YES.",
               f"Court 84 x 50 + {ro} ft runout = {ob['court'][0]} x {ob['court'][1]} ft (dashed, long axis N-S): fits, YES."):
        yy = sh.para(tx, yy + 0.02, cw_, t_, size=7.3, indent=0.1, bullet="·")
    y = min(gy - 0.12, yy)
    y = section(sh, x2, y, "3  FIXTURES BY LEVEL (IBC 2021 T2902.1)", size=10.5)
    fh = [("LEVEL", 0, "l"), ("LOAD", 1.05, "r"), ("WC M", 1.55, "r"), ("WC W", 2.05, "r"), ("LAV M", 2.55, "r"), ("LAV W", 3.05, "r"), ("DF", 3.40, "r"), ("SUM", 3.95, "r")]
    y -= rp
    for lab, dx, al in fh:
        sh.text(x2 + dx, y + 0.03, lab, size=7.2, bold=True, align="left" if al == "l" else "right", layer=TB)
    sh.line(x2, y - 0.04, x2 + c2w, y - 0.04, layer=TB, lw=0.6)
    f1, f2 = F_["fx1"], F_["fx2"]
    tot = {k: f1[k] + f2[k] for k in ("load", "wc_m", "wc_f", "lav_m", "lav_f", "df", "in_rooms")}
    for nm, f, b in (("L1", f1, False), ("L2", f2, False), ("TOTAL", tot, True)):
        y -= rp
        for (lab, dx, al), c in zip(fh, [nm, n(f["load"]), str(f["wc_m"]), str(f["wc_f"]), str(f["lav_m"]), str(f["lav_f"]), str(f["df"]), str(f["in_rooms"])]):
            sh.text(x2 + dx, y, c, size=7.8, bold=b, align="left" if al == "l" else "right", layer=TB)
    y -= 0.04
    y = sh.para(x2, y, c2w, f"L1 load = lower seats + {n(F_['occ_floor'])} floor occupants (50 SF each); L2 = upper seats. Same in both columns (load follows seats, not seat type). "
                f"Urinals may replace up to 67% of men's WCs (IPC 424.2). 1 service sink. SUM = WCs + lavatories (50 SF each, ASSUMED).", size=7.6)
    y = section(sh, x2, y, "4  STAIRS + ELEVATOR (R-015)", size=10.5)
    st = F_["stair"]
    y = sh.para(x2, y, c2w, f"L2 load {n(F_['l2_load'])} ({n(su)} seats + {F_['l2_other']} in S&C, cross-training, admin) → "
                f"{F_['exits']} stairs (T1006.3.3) x {st['width_in']:.0f} in (0.2 in/occupant, sprinklered + voice alarm, 1005.3.1), "
                f"≈ {st['sf']:.0f} SF each per level; 1 elevator (1104.4), {F_['elev_sf']} SF hoistway ASSUMED. "
                f"{n(F_['vc_sf'])} SF per level, same on both levels and aligned. Open stairs OK for two stories (1019.3 exc. 1). "
                f"Floor-to-floor 15 ft ASSUMED.", size=7.6)
    y = section(sh, x2, y, "5  WHEELCHAIR SPACES", size=10.5)
    y = sh.para(x2, y, c2w, f"{n(bowl)} bowl seats → {F_['ws']} wheelchair spaces (IBC T1109.2.2.1 / ADA T221.2.1.1: 6 + 1 per 150 over 500), "
                f"each with a companion seat (ADA 221.3), dispersed across both tiers with lines of sight (ADA 221.2.3, 802.2). "
                f"Same count for either seating type; where they sit in a telescopic bank is an architect task.", size=7.6)
    col2_bottom = y

    # ================= column 3: result, locked list, open items, sources =================
    x3 = x2 + c2w + 0.35
    c3w = W - M - 0.28 - x3
    sh.line(x3 - 0.17, body_bottom + 0.12, x3 - 0.17, top, lw=0.5)
    y = section(sh, x3, top - 0.2, "6  RESULT", first=True, size=10.5) - 0.04
    bx_h = 1.30
    sh.rect(x3, y - bx_h, c3w, bx_h, lw=1.6)
    lines = [("LOCKED PROGRAM (D-030)", 10.0, True),
             (f"{n(floor)} SF floor · {n(bowl)} bowl seats", 9.4, True),
             ("2 levels · no suites", 9.4, True),
             (f"Fixed: footprint {n(F_['F'])} · FITS", 8.6, False),
             (f"Telescopic: {n(T_['F'])} · FITS", 8.6, False)]
    yy = y - 0.26
    for t_, sz, b in lines:
        sh.text(x3 + c3w / 2, yy, t_, size=sz, bold=b, align="center")
        yy -= 0.235
    y -= bx_h + 0.04
    y = sh.para(x3, y, c3w, f"Total {n(F_['G'])} GSF fixed / {n(T_['G'])} telescopic. Fixed leaves only {n(cap - F_['F'])} SF under "
                f"the cap; the drawn {n(few * fns)} SF floor uses {n(few * fns - floor)} more. Telescopic frees ≈ {r100(T_['ring'] - T_['L2'])} SF "
                f"over the ring and ≈ {r100(cap - T_['F'])} SF of footprint.", size=7.9)
    y = section(sh, x3, y, "7  LOCKED IN phase2.yaml", size=10.5)
    for t_ in (f"Event floor {n(floor)} SF (D-030); {p2['spaces']['arena']['mats']} x {mft} ft mats, 2 x 2.",
               f"{n(bowl)} seats, all in the bowl; 2 levels; footprint cap {n(cap)} SF (D-031).",
               "S&C + cross-training on Level 2 over the lockers.",
               f"The {n(p2['spaces']['arena']['sf_tagged_superseded'])} SF arena tag is SUPERSEDED for the event floor (kept as history).",
               "Changes only on CHANGE APPROVED."):
        y = sh.para(x3, y + 0.02, c3w, t_, size=7.7, indent=0.12, bullet="·")
    y = section(sh, x3, y, "8  STILL OPEN", size=10.5)
    for t_ in ("Seating type, fixed vs telescopic (D-009): plans P2-A-101/102 show fixed solid, telescopic dashed.",
               "Suites: PARKED, future add-on, study after attendance is proven.",
               "AHJ / code edition (D-008); girls locker size (D-013); concession scope (D-011)."):
        y = sh.para(x3, y + 0.02, c3w, t_, size=7.7, indent=0.12, bullet="·")
    y = section(sh, x3, y, "9  CITED vs ASSUMED", size=10.5)
    y = sh.para(x3, y, c3w, "CITED: seat SF (R-008), fixtures + egress + wheelchair tables (R-009, R-015, R-016), gross-up and "
                "mechanical share (R-014), mat and court clearances (R-005, R-012). ASSUMED: 50/50 tiers, 50 SF/fixture, "
                "15 ft floor-to-floor, table zone depth, concourse share, same gross-up for telescopic.", size=7.4)
    y = section(sh, x3, y, "10  SOURCES (retrieved 2026-10-03)", size=10)
    for s_ in ["Shane 11:39 PM CT (D-030 decision)", "R-005, R-008, R-009, R-012, R-014, R-015, R-016",
               "Rev C (suites) frozen; history in Revs A-C"]:
        y = sh.para(x3, y + 0.03, c3w, s_, size=7.2, indent=0.12, bullet="·")
    col3_bottom = y

    fl = body_bottom + 0.08
    for nm, yy in (("col1", col1_bottom), ("col2", col2_bottom), ("col3", col3_bottom)):
        if yy < fl:
            raise SystemExit(f"LAYOUT OVERFLOW: {nm} runs {fl - yy:.2f} in into the stamp band")
    print(f"layout margins (in): col1 {col1_bottom - fl:.2f}, col2 {col2_bottom - fl:.2f}, col3 {col3_bottom - fl:.2f}")
    return sh


def build_e(p2, prog, ob, out):
    """Rev E: LOCKED PROGRAM with MIX seating (D-009): telescopic lower tier, fixed upper tier."""
    meta2, pm = p2["meta"], prog["meta_rev_e"]
    ms = prog["mixed_seating"]
    plan = out["plan"]
    sh = Sheet(W, H)
    body_bottom = add_titleblock(sh, {
        "project": f"{meta2['project']}\n{meta2['arena_name']} · {meta2['location']}",
        "phase": "PHASE 2",
        "title": f"{pm['title']}\n{pm['subtitle']}",
        "scale": pm["scale"],
        "date": meta2["sheet_date"],
        "revision": pm["revision"],
        "drawn_by": meta2["drawn_by"],
        "sheet_no": SHEET_NO,
        "stamp": meta2["stamp"],
    }, margin=M, tb_h=0.95, stamp_h=0.40)
    top = H - M - 0.12
    X_, F_ = out["mix"], out["fixed"]
    cap = X_["cap"]
    rooms = {r["id"]: r for r in prog["rooms"]}
    floor = p2["spaces"]["arena"]["event_floor_sf"]
    bowl = p2["spaces"]["seating"]["bowl"]
    bx = plan["building"]["rect"]
    bw, bh = bx[2] - bx[0], bx[3] - bx[1]
    box = bw * bh
    fx0, fy0, fx1, fy1 = plan["event_floor"]["rect"]
    few, fns = fx1 - fx0, fy1 - fy0

    # ================= column 1: area table by level =================
    x0, c1w = M + 0.18, 7.15
    y = section(sh, x0, top - 0.2, f"1  AREA BY LEVEL — {n(floor)} SF FLOOR, {n(bowl)} SEATS, MIX SEATING (D-009)", first=True) - 0.02
    hdr = [("SPACE", 0, "l"), ("MIX (D-009)", 3.70, "r"), ("ALL FIXED", 4.75, "r"), ("BASIS", 4.95, "l")]
    rp = 0.172
    y -= rp
    for lab, dx, al in hdr:
        sh.text(x0 + dx, y + 0.03, lab, size=7.4, bold=True, align="left" if al == "l" else "right", layer=TB)
    sh.line(x0, y - 0.04, x0 + c1w, y - 0.04, layer=TB, lw=0.8)

    def row(lab, a, b, basis="", bold=False, rule=False, size=7.9):
        nonlocal y
        y -= rp
        sh.text(x0 + 0.08 if not bold else x0, y, lab, size=size, bold=bold, layer=TB)
        sh.text(x0 + 3.70, y, a, size=size, bold=bold, align="right", layer=TB)
        sh.text(x0 + 4.75, y, b, size=size, bold=bold, align="right", layer=TB)
        if basis:
            while text_width_in(basis, 6.9) > c1w - 4.97 and len(basis) > 4:
                basis = basis[:-2].rstrip() + "…"
            sh.text(x0 + 4.95, y, basis, size=6.9, layer=TB)
        if rule:
            sh.line(x0, y - 0.05, x0 + c1w, y - 0.05, layer=TB, lw=0.4)

    def head(lab):
        nonlocal y
        y -= rp + 0.03
        sh.text(x0, y, lab, size=8.0, bold=True, layer=TB)

    sl, su = X_["sl"], X_["su"]
    label = {
        "arena": ("Event floor (D-030, locked)", "phase2.yaml · D-030"),
        "seating_lower": (f"Lower tier seats ({n(sl)}), TELESCOPIC", f"{X_['seat_sf_lower']:.2f} SF/seat (R-008) · fixed col. 6.0"),
        "seating_upper": (f"Upper tier seats ({n(su)}), FIXED", f"{X_['seat_sf_upper']:.1f} SF/seat (R-008)"),
        "concourse_lower": ("Lower concourse", rooms["concourse"]["short"]),
        "concourse_upper": ("Upper concourse / hall of champions balcony", "same factor, upper seats"),
        "public_restroom_lower": (f"Public restrooms L1 ({X_['fx1']['in_rooms']} fixtures)", "T2902.1 x 50 SF (R-009)"),
        "public_restroom_upper": (f"Public restrooms L2 ({X_['fx2']['in_rooms']} fixtures)", "T2902.1 x 50 SF (R-009)"),
        "vertical_circulation": (f"Stairs ({X_['exits']}) + elevator", "R-015"),
    }

    def lab_of(i):
        if i in label:
            return label[i]
        r = rooms[i]
        nm = r["name"].replace(" (as tagged; D-013)", " (D-013)").replace(" (DR3)", "")
        return nm, r["short"]
    head("LEVEL 1 (net SF)")
    for i in X_["l1_ids"]:
        lab, bas = lab_of(i)
        row(lab, n(X_["sf"][i]), n(F_["sf"][i]), bas)
    row("L1 net", n(X_["N1"]), n(F_["N1"]), bold=True)
    row("Mechanical (5% of total gross, at grade)", n(X_["M"]), n(F_["M"]), "R-014 · LOW")
    row(f"L1 GROSS (x {X_['g']:.2f})", n(X_["L1"]), n(F_["L1"]), "R-014 gross-up", bold=True, rule=True)
    head("LEVEL 2 (net SF)")
    for i in X_["l2_ids"]:
        lab, bas = lab_of(i)
        row(lab, n(X_["sf"][i]), n(F_["sf"][i]), bas)
    row("L2 net", n(X_["N2"]), n(F_["N2"]), bold=True)
    row(f"L2 GROSS (x {X_['g']:.2f})", n(X_["L2"]), n(F_["L2"]), bold=True, rule=True)
    head("FIT CHECK")
    row("Arena volume gross (floor + lower tier, double height)", n(X_["AV"]), n(F_["AV"]))
    row("Arena volume + L2 gross", n(X_["AV"] + X_["L2"]), n(F_["AV"] + F_["L2"]), "L2 sits over the L1 ring")
    row("FOOTPRINT = max(L1, arena volume + L2)", n(X_["F"]), n(F_["F"]), f"mix: set by {X_['governs']}", bold=True)
    row("MARGIN under the 55,000 SF cap (D-031)", n(cap - X_["F"]), n(cap - F_["F"]), f"target ≥ {n(ms['target_margin_sf'])} (Shane)", bold=True)
    row(f"Meets the ≥ {n(ms['target_margin_sf'])} SF target?", "YES" if cap - X_["F"] >= ms["target_margin_sf"] else "NO",
        "YES" if cap - F_["F"] >= ms["target_margin_sf"] else "NO", bold=True)
    row("TOTAL GSF (2 levels)", n(X_["G"]), n(F_["G"]), "not capped (D-031)", bold=True, rule=True)
    y -= 0.04
    y = sh.para(x0, y, c1w, f"MIX = D-009 as decided: lower tier on telescopic bleacher geometry ({X_['seat_sf_lower']:.2f} SF/seat), upper tier "
                f"fixed ({X_['seat_sf_upper']:.1f} SF/seat). ALL FIXED = Rev D base case, for reference. Same x {X_['g']:.2f} gross-up. "
                f"Tier split {round(X_['up'] * 100)}/{round((1 - X_['up']) * 100)} ASSUMED. Mix: L1 alone is {n(X_['L1'])}, so the arena volume "
                f"+ L2 ({n(X_['AV'] + X_['L2'])}) sets the footprint; the L1 ring must be {n(X_['L2'] - X_['ring'])} SF bigger than L1 needs, "
                f"which that footprint gives.", size=7.9)
    col1_bottom = y

    # ================= column 2: seats by side and tier, floor, fixtures, stairs, wheelchair =================
    x2, c2w = x0 + c1w + 0.35, 4.05
    sh.line(x2 - 0.17, body_bottom + 0.12, x2 - 0.17, top, lw=0.5)
    y = section(sh, x2, top - 0.2, f"2  SEATS BY SIDE AND TIER = {n(out['tot']['total'])}", first=True, size=10.5)
    sh_ = [("SIDE", 0, "l"), ("LOWER (TELE.)", 1.55, "r"), ("UPPER (FIXED)", 2.75, "r"), ("TOTAL", 3.55, "r")]
    y -= rp
    for lab, dx, al in sh_:
        sh.text(x2 + dx, y + 0.03, lab, size=7.2, bold=True, align="left" if al == "l" else "right", layer=TB)
    sh.line(x2, y - 0.04, x2 + c2w, y - 0.04, layer=TB, lw=0.6)
    names = {"N": "North", "S": "South", "E": "East"}
    for r_ in out["rows"] + [out["tot"]]:
        y -= rp
        b_ = r_["side"] == "TOTAL"
        for (lab, dx, al), c in zip(sh_, [names.get(r_["side"], "TOTAL"), n(r_["lower"]), n(r_["upper"]), n(r_["total"])]):
            sh.text(x2 + dx, y, c, size=7.9, bold=b_, align="left" if al == "l" else "right", layer=TB)
    y -= rp
    t_ = out["tot"]
    for (lab, dx, al), c in zip(sh_, ["capacity drawn", n(t_["cap_lower"]), n(t_["cap_upper"]), n(t_["cap_lower"] + t_["cap_upper"])]):
        sh.text(x2 + dx, y, c, size=7.2, align="left" if al == "l" else "right", layer=TB)
    lo = plan["tiers"]["lower"]
    up = plan["tiers"]["upper"]
    y -= 0.04
    y = sh.para(x2, y, c2w, f"No west tier (OK'd). Lower: {lo['rows']} rows x {lo['row_depth_ft'] * 12:.0f} in = {lo['depth_ft']} ft extended "
                f"(R-008), less the 12 ft portal and two 8 ft vomitories. Upper: {up['depth_ft']} ft at {X_['seat_sf_upper']:.1f} SF/seat. "
                f"Each tier = {n(sl)}, split by side in proportion to drawn capacity (P2-A-101/102 Rev B). Spare capacity is left for "
                f"wheelchair spaces and aisles; the upper tier has only {n(t_['cap_upper'] - su)} spare.", size=7.5)
    y = section(sh, x2, y, "3  EVENT FLOOR (unchanged, R-005, R-012)", size=10.5)
    y = sh.para(x2, y, c2w, f"{few:g} x {fns:g} ft = {n(few * fns)} SF drawn (locked {n(floor)}): 4 x 42 ft mats 2 x 2 with 10 ft clear, "
                f"15 ft table zones N and S; the {ob['ew']} x {ob['ns']} = {n(ob['sf'])} SF layout and an 84 x 50 court + 10 ft runout "
                f"({ob['court'][0]} x {ob['court'][1]}) fit. Long axis N-S on the entry axis.", size=7.5)
    y = section(sh, x2, y, "4  FIXTURES BY LEVEL (IBC 2021 T2902.1)", size=10.5)
    fh = [("LEVEL", 0, "l"), ("LOAD", 1.05, "r"), ("WC M", 1.55, "r"), ("WC W", 2.05, "r"), ("LAV M", 2.55, "r"), ("LAV W", 3.05, "r"), ("DF", 3.40, "r"), ("SUM", 3.95, "r")]
    y -= rp
    for lab, dx, al in fh:
        sh.text(x2 + dx, y + 0.03, lab, size=7.2, bold=True, align="left" if al == "l" else "right", layer=TB)
    sh.line(x2, y - 0.04, x2 + c2w, y - 0.04, layer=TB, lw=0.6)
    f1, f2 = X_["fx1"], X_["fx2"]
    tot = {k: f1[k] + f2[k] for k in ("load", "wc_m", "wc_f", "lav_m", "lav_f", "df", "in_rooms")}
    for nm, f, b in (("L1", f1, False), ("L2", f2, False), ("TOTAL", tot, True)):
        y -= rp
        for (lab, dx, al), c in zip(fh, [nm, n(f["load"]), str(f["wc_m"]), str(f["wc_f"]), str(f["lav_m"]), str(f["lav_f"]), str(f["df"]), str(f["in_rooms"])]):
            sh.text(x2 + dx, y, c, size=7.8, bold=b, align="left" if al == "l" else "right", layer=TB)
    y -= 0.04
    y = sh.para(x2, y, c2w, f"L1 = lower seats + {n(X_['occ_floor'])} floor occupants (50 SF each); L2 = upper seats. Unchanged from Rev D "
                f"(load follows seats, not seat type). On the plans the restrooms flank the lobby, L2 stacked over L1.", size=7.5)
    y = section(sh, x2, y, "5  STAIRS, ELEVATOR, WHEELCHAIR", size=10.5)
    st = X_["stair"]
    y = sh.para(x2, y, c2w, f"L2 load {n(X_['l2_load'])} → {X_['exits']} stairs (T1006.3.3) x {st['width_in']:.0f} in (0.2 in/occ., 1005.3.1), "
                f"≈ {st['sf']:.0f} SF each per level + 1 elevator (1104.4) = {n(X_['vc_sf'])} SF per level, aligned on both levels. "
                f"{X_['ws']} wheelchair spaces + companions (IBC T1109.2.2.1, ADA 221.3), dispersed (ADA 221.2.3) — placement in the "
                f"telescopic and fixed tiers is an architect task.", size=7.5)
    col2_bottom = y

    # ================= column 3 =================
    x3 = x2 + c2w + 0.35
    c3w = W - M - 0.28 - x3
    sh.line(x3 - 0.17, body_bottom + 0.12, x3 - 0.17, top, lw=0.5)
    y = section(sh, x3, top - 0.2, "6  RESULT", first=True, size=10.5) - 0.04
    bx_h = 1.30
    sh.rect(x3, y - bx_h, c3w, bx_h, lw=1.6)
    lines = [("LOCKED PROGRAM + MIX", 10.0, True),
             (f"{n(floor)} SF floor · {n(bowl)} seats · 2 levels", 9.0, True),
             ("telescopic lower · fixed upper", 8.8, False),
             (f"Footprint {n(X_['F'])} · margin {n(cap - X_['F'])}", 9.2, True),
             (f"Target ≥ {n(ms['target_margin_sf'])} SF: MET", 8.8, True)]
    yy = y - 0.26
    for t2, sz, b in lines:
        sh.text(x3 + c3w / 2, yy, t2, size=sz, bold=b, align="center")
        yy -= 0.235
    y -= bx_h + 0.04
    y = sh.para(x3, y, c3w, f"Total {n(X_['G'])} GSF (Rev D all-fixed: {n(F_['G'])}). Block plan box shrinks from 250 x 220 to "
                f"{bw:g} x {bh:g} ft = {n(box)} SF: {n(cap - box)} SF under the cap and {n(box - X_['F'])} SF over the program "
                f"footprint, so the gross-up allowance stays inside the box (P2-A-101/102 Rev B).", size=7.9)
    y = section(sh, x3, y, "7  LOCKED IN phase2.yaml", size=10.5)
    mft = p2["spaces"]["arena"]["mat_ft"]
    for t2 in (f"Event floor {n(floor)} SF; {p2['spaces']['arena']['mats']} x {mft} ft mats, 2 x 2 (D-030).",
               f"{n(bowl)} seats in the bowl, N, S and E sides; 2 levels; footprint cap {n(cap)} SF (D-031).",
               "Seating MIX: telescopic lower tier, fixed upper tier (D-009, Shane 4:30 AM CT).",
               "S&C + cross-training on Level 2 over the lockers. Changes only on CHANGE APPROVED."):
        y = sh.para(x3, y + 0.02, c3w, t2, size=7.7, indent=0.12, bullet="·")
    y = section(sh, x3, y, "8  STILL OPEN", size=10.5)
    for t2 in ("50/50 tier split and 6 telescopic rows (ASSUMED); sightlines not checked.",
               "AHJ / code edition (D-008); girls locker size (D-013); concession scope (D-011); owner (D-007); site (D-006).",
               "Suites PARKED (future add-on)."):
        y = sh.para(x3, y + 0.02, c3w, t2, size=7.7, indent=0.12, bullet="·")
    y = section(sh, x3, y, "9  CITED vs ASSUMED", size=10.5)
    y = sh.para(x3, y, c3w, "CITED: seat SF and row depth (R-008), fixtures, egress and wheelchair tables (R-009, R-015, R-016), "
                "gross-up and mechanical share (R-014), mat and court clearances (R-005, R-012). ASSUMED: 50/50 tiers, 6 rows, "
                "50 SF/fixture, 15 ft floor-to-floor, table zones, concourse share, box shape.", size=7.4)
    y = section(sh, x3, y, "10  SOURCES (retrieved 2026-10-03)", size=10)
    for s_ in ["Shane 2026-10-04 4:30 AM CT (D-009 mix, Rev E, margin target)", "R-005, R-008, R-009, R-012, R-014, R-015, R-016",
               "Rev D (all fixed vs telescopic) frozen; history in Revs A-D"]:
        y = sh.para(x3, y + 0.03, c3w, s_, size=7.2, indent=0.12, bullet="·")
    col3_bottom = y

    fl = body_bottom + 0.08
    for nm, yy in (("col1", col1_bottom), ("col2", col2_bottom), ("col3", col3_bottom)):
        if yy < fl:
            raise SystemExit(f"LAYOUT OVERFLOW: {nm} runs {fl - yy:.2f} in into the stamp band")
    print(f"layout margins (in): col1 {col1_bottom - fl:.2f}, col2 {col2_bottom - fl:.2f}, col3 {col3_bottom - fl:.2f}")
    return sh


def build_f(p2, prog, ob, out):
    """Rev F: LOCKED PROGRAM + LEVEL 2 RUNNING / TRAINING LOOP (D-035): S&C and cross-training trimmed; loop replaces the upper concourse."""
    meta2, pm = p2["meta"], prog["meta_rev_f"]
    tl = prog["training_loop"]
    lg = out["geom"]
    lsp = p2["spaces"]["training_loop"]
    ms = prog["mixed_seating"]
    plan = out["plan"]
    sh = Sheet(W, H)
    body_bottom = add_titleblock(sh, {
        "project": f"{meta2['project']}\n{meta2['arena_name']} · {meta2['location']}",
        "phase": "PHASE 2",
        "title": f"{pm['title']}\n{pm['subtitle']}",
        "scale": pm["scale"],
        "date": meta2["sheet_date"],
        "revision": pm["revision"],
        "drawn_by": meta2["drawn_by"],
        "sheet_no": SHEET_NO,
        "stamp": meta2["stamp"],
    }, margin=M, tb_h=0.95, stamp_h=0.40)
    top = H - M - 0.12
    X_, F_ = out["loop"], out["mix"]
    cap = X_["cap"]
    rooms = {r["id"]: r for r in prog["rooms"]}
    floor = p2["spaces"]["arena"]["event_floor_sf"]
    bowl = p2["spaces"]["seating"]["bowl"]
    bx = plan["building"]["rect"]
    bw, bh = bx[2] - bx[0], bx[3] - bx[1]
    pj = plan["building"]["projection"]["rect"]
    box = bw * bh + (pj[2] - pj[0]) * (pj[3] - pj[1])
    fx0, fy0, fx1, fy1 = plan["event_floor"]["rect"]
    few, fns = fx1 - fx0, fy1 - fy0

    # ================= column 1: area table by level =================
    x0, c1w = M + 0.18, 7.15
    y = section(sh, x0, top - 0.2, f"1  AREA BY LEVEL — {n(bowl)} SEATS, MIX (D-009), L2 LOOP (D-035)", first=True) - 0.02
    hdr = [("SPACE", 0, "l"), ("REV F LOOP", 3.70, "r"), ("REV E", 4.75, "r"), ("BASIS", 4.95, "l")]
    rp = 0.172
    y -= rp
    for lab, dx, al in hdr:
        sh.text(x0 + dx, y + 0.03, lab, size=7.4, bold=True, align="left" if al == "l" else "right", layer=TB)
    sh.line(x0, y - 0.04, x0 + c1w, y - 0.04, layer=TB, lw=0.8)

    def row(lab, a, b, basis="", bold=False, rule=False, size=7.9):
        nonlocal y
        y -= rp
        sh.text(x0 + 0.08 if not bold else x0, y, lab, size=size, bold=bold, layer=TB)
        sh.text(x0 + 3.70, y, a, size=size, bold=bold, align="right", layer=TB)
        sh.text(x0 + 4.75, y, b, size=size, bold=bold, align="right", layer=TB)
        if basis:
            while text_width_in(basis, 6.9) > c1w - 4.97 and len(basis) > 4:
                basis = basis[:-2].rstrip() + "…"
            sh.text(x0 + 4.95, y, basis, size=6.9, layer=TB)
        if rule:
            sh.line(x0, y - 0.05, x0 + c1w, y - 0.05, layer=TB, lw=0.4)

    def head(lab):
        nonlocal y
        y -= rp + 0.03
        sh.text(x0, y, lab, size=8.0, bold=True, layer=TB)

    sl, su = X_["sl"], X_["su"]
    label = {
        "arena": ("Event floor (D-030, locked)", "phase2.yaml · D-030"),
        "seating_lower": (f"Lower tier seats ({n(sl)}), TELESCOPIC", f"{X_['seat_sf_lower']:.2f} SF/seat (R-008) · fixed col. 6.0"),
        "seating_upper": (f"Upper tier seats ({n(su)}), FIXED", f"{X_['seat_sf_upper']:.1f} SF/seat (R-008)"),
        "concourse_lower": ("Lower concourse", rooms["concourse"]["short"]),
        "concourse_upper": ("Upper concourse / balcony", "Rev E only; the loop replaces it"),
        "public_restroom_lower": (f"Public restrooms L1 ({X_['fx1']['in_rooms']} fixtures)", "T2902.1 x 50 SF (R-009)"),
        "public_restroom_upper": (f"Public restrooms L2 ({X_['fx2']['in_rooms']} fixtures)", "T2902.1 x 50 SF (R-009)"),
        "vertical_circulation": (f"Stairs ({X_['exits']}) + elevator", "R-015"),
    }

    for k_ in ("strength_conditioning", "cross_training"):
        label[k_] = (rooms[k_]["name"].replace(" (as tagged; D-013)", ""), f"D-035: was {n(F_['sf'][k_])} (trimmed for the loop)")

    def lab_of(i):
        if i in label:
            return label[i]
        r = rooms[i]
        nm = r["name"].replace(" (as tagged; D-013)", " (D-013)").replace(" (DR3)", "")
        return nm, r["short"]
    head("LEVEL 1 (net SF)")
    for i in X_["l1_ids"]:
        lab, bas = lab_of(i)
        row(lab, n(X_["sf"][i]), n(F_["sf"][i]), bas)
    row("L1 net", n(X_["N1"]), n(F_["N1"]), bold=True)
    row("Mechanical (5% of total gross, at grade)", n(X_["M"]), n(F_["M"]), "R-014 · LOW")
    row(f"L1 GROSS (x {X_['g']:.2f})", n(X_["L1"]), n(F_["L1"]), "R-014 gross-up", bold=True, rule=True)
    head("LEVEL 2 (net SF)")
    for i in X_["l2_ids"]:
        lab, bas = lab_of(i)
        row(lab, "—" if i == tl["replaces"] else n(X_["sf"][i]), n(F_["sf"][i]), bas)
    row("L2 net rooms (without the loop)", n(X_["N2x"]), n(F_["N2"]), bold=True)
    row(f"Running / training loop (drawn, not grossed up)", n(X_["loop"]), "—", "P2-A-102 Rev D · ASSUMED no x1.25")
    row(f"L2 GROSS (x {X_['g']:.2f} rooms + loop)", n(X_["L2"]), n(F_["L2"]), bold=True, rule=True)
    head("FIT CHECK")
    row("Arena volume gross (floor + lower tier, double height)", n(X_["AV"]), n(F_["AV"]))
    row("Arena volume + L2 gross", n(X_["AV"] + X_["L2"]), n(F_["AV"] + F_["L2"]), "L2 sits over the L1 ring")
    row("FOOTPRINT = max(L1, arena volume + L2)", n(X_["F"]), n(F_["F"]), f"mix: set by {X_['governs']}", bold=True)
    row("MARGIN under the 55,000 SF cap (D-031)", n(cap - X_["F"]), n(cap - F_["F"]), f"target ≥ {n(ms['target_margin_sf'])} (Shane)", bold=True)
    row("  if the loop were grossed up x1.25: footprint / margin", f"{n(X_['alt']['F'])} / {n(X_['alt']['margin'])}", "—", "would miss the target", size=7.4)
    row(f"Meets the ≥ {n(ms['target_margin_sf'])} SF target?", "YES" if cap - X_["F"] >= ms["target_margin_sf"] else "NO",
        "YES" if cap - F_["F"] >= ms["target_margin_sf"] else "NO", bold=True)
    row("TOTAL GSF (2 levels)", n(X_["G"]), n(F_["G"]), "not capped (D-031)", bold=True, rule=True)
    y -= 0.04
    y = sh.para(x0, y, c1w, f"REV F = Rev E (MIX, D-009) with S&C {n(X_['sf']['strength_conditioning'])} and cross-training "
                f"{n(X_['sf']['cross_training'])} SF (D-035) and the loop in place of the upper concourse. Loads, stairs and fixtures recomputed "
                f"(stair width {X_['stair']['width_in']:.1f} in). The loop is circulation drawn at full size, so it is added to L2 gross as drawn "
                f"(ASSUMED). The arena volume + L2 ({n(X_['AV'] + X_['L2'])}) sets the footprint.", size=7.9)
    col1_bottom = y

    # ================= column 2: seats by side and tier, floor, fixtures, stairs, wheelchair =================
    x2, c2w = x0 + c1w + 0.35, 4.05
    sh.line(x2 - 0.17, body_bottom + 0.12, x2 - 0.17, top, lw=0.5)
    y = section(sh, x2, top - 0.2, f"2  SEATS BY SIDE AND TIER = {n(out['tot']['total'])} (= REV E)", first=True, size=10.5)
    sh_ = [("SIDE", 0, "l"), ("LOWER (TELE.)", 1.55, "r"), ("UPPER (FIXED)", 2.75, "r"), ("TOTAL", 3.55, "r")]
    y -= rp
    for lab, dx, al in sh_:
        sh.text(x2 + dx, y + 0.03, lab, size=7.2, bold=True, align="left" if al == "l" else "right", layer=TB)
    sh.line(x2, y - 0.04, x2 + c2w, y - 0.04, layer=TB, lw=0.6)
    names = {"N": "North", "S": "South", "E": "East"}
    for r_ in out["rows"] + [out["tot"]]:
        y -= rp
        b_ = r_["side"] == "TOTAL"
        for (lab, dx, al), c in zip(sh_, [names.get(r_["side"], "TOTAL"), n(r_["lower"]), n(r_["upper"]), n(r_["total"])]):
            sh.text(x2 + dx, y, c, size=7.9, bold=b_, align="left" if al == "l" else "right", layer=TB)
    y -= rp
    t_ = out["tot"]
    for (lab, dx, al), c in zip(sh_, ["capacity drawn", n(t_["cap_lower"]), n(t_["cap_upper"]), n(t_["cap_lower"] + t_["cap_upper"])]):
        sh.text(x2 + dx, y, c, size=7.2, align="left" if al == "l" else "right", layer=TB)
    lo = plan["tiers"]["lower"]
    up = plan["tiers"]["upper"]
    y -= 0.04
    y = sh.para(x2, y, c2w, f"No west tier (OK'd). Lower: {lo['rows']} rows x {lo['row_depth_ft'] * 12:.0f} in = {lo['depth_ft']} ft extended "
                f"(R-008), less the 12 ft portal and two 8 ft vomitories. Upper: {up['depth_ft']} ft at {X_['seat_sf_upper']:.1f} SF/seat. "
                f"Each tier = {n(sl)}, split by side in proportion to drawn capacity (P2-A-101/102 Rev B). Spare capacity is left for "
                f"wheelchair spaces and aisles; the upper tier has only {n(t_['cap_upper'] - su)} spare. Tiers unchanged in Rev D.", size=7.5)
    y = section(sh, x2, y, "3  LEVEL 2 RUNNING / TRAINING LOOP (D-035)", size=10.5)
    y = sh.para(x2, y, c2w, f"{lsp['lanes']} lanes x {lsp['lane_width_in']} in = {lg['width']:g} ft all around, squared corners. Centerline "
                f"{lg['cx']:g} x {lg['cy']:g} ft: 2 x ({lg['cx']:g} + {lg['cy']:g}) = {n(lg['centerline'])} ft; 5,280 / {n(lg['centerline'])} = "
                f"{lg['laps_per_mile']:.2f} laps/mile. Area {n(lg['area'])} SF. Lanes: UFC 4-740-02N 4.1.7 (42 in, min 3 lanes), Athletic "
                f"Business (36-42 in; max 12 laps/mile, 8-10 preferred). 2 lanes is ASSUMED: 3 lanes (10.5 ft) does not fit without moving the "
                f"upper tier. Event days: upper concourse, spectators cross it at the tier entries; non-event days: training. 42 in guards at "
                f"open edges (IBC 1015.2, 1015.3).", size=7.5)
    y = section(sh, x2, y, "4  FIXTURES BY LEVEL (IBC 2021 T2902.1)", size=10.5)
    fh = [("LEVEL", 0, "l"), ("LOAD", 1.05, "r"), ("WC M", 1.55, "r"), ("WC W", 2.05, "r"), ("LAV M", 2.55, "r"), ("LAV W", 3.05, "r"), ("DF", 3.40, "r"), ("SUM", 3.95, "r")]
    y -= rp
    for lab, dx, al in fh:
        sh.text(x2 + dx, y + 0.03, lab, size=7.2, bold=True, align="left" if al == "l" else "right", layer=TB)
    sh.line(x2, y - 0.04, x2 + c2w, y - 0.04, layer=TB, lw=0.6)
    f1, f2 = X_["fx1"], X_["fx2"]
    tot = {k: f1[k] + f2[k] for k in ("load", "wc_m", "wc_f", "lav_m", "lav_f", "df", "in_rooms")}
    for nm, f, b in (("L1", f1, False), ("L2", f2, False), ("TOTAL", tot, True)):
        y -= rp
        for (lab, dx, al), c in zip(fh, [nm, n(f["load"]), str(f["wc_m"]), str(f["wc_f"]), str(f["lav_m"]), str(f["lav_f"]), str(f["df"]), str(f["in_rooms"])]):
            sh.text(x2 + dx, y, c, size=7.8, bold=b, align="left" if al == "l" else "right", layer=TB)
    y -= 0.04
    y = sh.para(x2, y, c2w, f"L1 = lower seats + {n(X_['occ_floor'])} floor occupants (50 SF each); L2 = upper seats. Unchanged from Rev D "
                f"(load follows seats). Restrooms flank the lobby, L2 stacked over L1.", size=7.5)
    y = section(sh, x2, y, "5  STAIRS, ELEVATOR, WHEELCHAIR", size=10.5)
    st = X_["stair"]
    y = sh.para(x2, y, c2w, f"L2 load {n(X_['l2_load'])} → {X_['exits']} stairs (T1006.3.3) x {st['width_in']:.0f} in (0.2 in/occ., 1005.3.1), "
                f"≈ {st['sf']:.0f} SF each per level + 1 elevator (1104.4) = {n(X_['vc_sf'])} SF per level, aligned on both levels. "
                f"{X_['ws']} wheelchair spaces + companions (IBC T1109.2.2.1, ADA 221.3), dispersed (ADA 221.2.3) — placement in the "
                f"telescopic and fixed tiers is an architect task. Rev D moves ST-1, ST-2 and the elevator clear of the loop.", size=7.5)
    col2_bottom = y

    # ================= column 3 =================
    x3 = x2 + c2w + 0.35
    c3w = W - M - 0.28 - x3
    sh.line(x3 - 0.17, body_bottom + 0.12, x3 - 0.17, top, lw=0.5)
    y = section(sh, x3, top - 0.2, "6  RESULT", first=True, size=10.5) - 0.04
    bx_h = 1.30
    sh.rect(x3, y - bx_h, c3w, bx_h, lw=1.6)
    lines = [("LOCKED PROGRAM + LOOP", 10.0, True),
             (f"{n(floor)} SF floor · {n(bowl)} seats · 2 levels", 9.0, True),
             (f"L2 loop {n(lg['centerline'])} ft · {lg['laps_per_mile']:.2f} laps/mile", 8.8, False),
             (f"Footprint {n(X_['F'])} · margin {n(cap - X_['F'])}", 9.2, True),
             (f"Target ≥ {n(ms['target_margin_sf'])} SF: MET", 8.8, True)]
    yy = y - 0.26
    for t2, sz, b in lines:
        sh.text(x3 + c3w / 2, yy, t2, size=sz, bold=b, align="center")
        yy -= 0.235
    y -= bx_h + 0.04
    y = sh.para(x3, y, c3w, f"Total {n(X_['G'])} GSF (Rev E: {n(F_['G'])}). Drawn building (P2-A-101/102 Rev D) = {bw:g} x {bh:g} ft + "
                f"{pj[2] - pj[0]:g} x {pj[3] - pj[1]:g} ft NE stair tower = {n(box)} SF, {n(cap - box)} under the cap. NOTE: the program footprint "
                f"is {n(X_['F'] - box)} SF MORE than the drawn building: the drawn plan fits, but the x {X_['g']:.2f} gross-up allowance no "
                f"longer fully fits inside it.", size=7.9)
    y = section(sh, x3, y, "7  LOCKED IN phase2.yaml", size=10.5)
    mft = p2["spaces"]["arena"]["mat_ft"]
    for t2 in (f"Event floor {n(floor)} SF; {p2['spaces']['arena']['mats']} x {mft} ft mats, 2 x 2 (D-030).",
               f"{n(bowl)} seats in the bowl, N, S and E sides; 2 levels; footprint cap {n(cap)} SF (D-031).",
               "Seating MIX: telescopic lower tier, fixed upper tier (D-009, Shane 4:30 AM CT).",
               f"S&C {n(X_['sf']['strength_conditioning'])} + cross-training {n(X_['sf']['cross_training'])} SF on Level 2 (D-035; were 6,000 / 4,000).",
               f"Continuous L2 loop, {lsp['lanes']} x {lsp['lane_width_in']} in (D-035, Shane 4:55 AM CT). Changes only on CHANGE APPROVED."):
        y = sh.para(x3, y + 0.02, c3w, t2, size=7.7, indent=0.12, bullet="·")
    y = section(sh, x3, y, "8  STILL OPEN", size=10.5)
    for t2 in ("Loop lane count (2 ASSUMED; 3 preferred); 50/50 tier split and 6 telescopic rows (ASSUMED).",
               "AHJ / code edition (D-008); girls locker size (D-013); concession scope (D-011); owner (D-007); site (D-006).",
               "Suites PARKED (future add-on)."):
        y = sh.para(x3, y + 0.02, c3w, t2, size=7.7, indent=0.12, bullet="·")
    y = section(sh, x3, y, "9  CITED vs ASSUMED", size=10.5)
    y = sh.para(x3, y, c3w, "CITED: seat SF and row depth (R-008), fixtures, egress and wheelchair tables (R-009, R-015, R-016), "
                "gross-up and mechanical share (R-014), lane width (UFC 4-740-02N, Athletic Business), guards (IBC 1015). ASSUMED: "
                "2 lanes, loop not grossed up, 50/50 tiers, 6 rows, 50 SF/fixture, box shape.", size=7.4)
    y = section(sh, x3, y, "10  SOURCES (retrieved 2026-10-04)", size=10)
    for s_ in ["Shane 2026-10-04 4:55 AM CT (D-035 loop, Rev F); 4:30 AM CT (D-009 mix, margin target)", "R-008, R-009, R-014, R-015, R-016; UFC 4-740-02N; Athletic Business; IBC 2021 1015",
               "Rev E (mix, no loop) frozen; history in Revs A-E"]:
        y = sh.para(x3, y + 0.03, c3w, s_, size=7.2, indent=0.12, bullet="·")
    col3_bottom = y

    fl = body_bottom + 0.08
    for nm, yy in (("col1", col1_bottom), ("col2", col2_bottom), ("col3", col3_bottom)):
        if yy < fl:
            raise SystemExit(f"LAYOUT OVERFLOW: {nm} runs {fl - yy:.2f} in into the stamp band")
    print(f"layout margins (in): col1 {col1_bottom - fl:.2f}, col2 {col2_bottom - fl:.2f}, col3 {col3_bottom - fl:.2f}")
    return sh


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--png", help="optional PNG preview path (outside the repo)")
    ap.add_argument("--out-dir", help="write PDF/DXF here instead of phase2/out/{pdf,dxf}")
    ap.add_argument("--force", action="store_true", help="allow overwriting a FROZEN revision in the repo")
    ap.add_argument("--rev", choices=["A", "B", "C", "D", "E", "F"], default="F", help="A = one-level (frozen); B = two-level (frozen); C = suites (frozen); D = locked program (frozen); E = MIX seating (frozen); F = MIX + Level 2 loop (default)")
    a = ap.parse_args()
    if a.rev == "A":
        p2, prog, ob, out = tf.summary()
        pm, builder = prog["meta"], build
    elif a.rev == "B":
        p2, prog, ob, out = tf.summary_b()
        pm, builder = prog["meta_rev_b"], build_b
    elif a.rev == "F":
        p2, prog, ob, out = tf.summary_f()
        pm, builder = prog["meta_rev_f"], build_f
    elif a.rev == "E":
        p2, prog, ob, out = tf.summary_e()
        pm, builder = prog["meta_rev_e"], build_e
    elif a.rev == "D":
        p2, prog, ob, out = tf.summary_d()
        pm, builder = prog["meta_rev_d"], build_d
    else:
        p2, prog, out = tf.summary_c()
        ob = None
        pm, builder = prog["meta_rev_c"], (lambda p2_, prog_, ob_, out_: build_c(p2_, prog_, out_))
    rv = p2["sheets"][SHEET_NO]["revisions"][pm["revision"]]
    if a.out_dir:
        pdf, dxf = (Path(a.out_dir) / f"{rv['file']}.{e}" for e in ("pdf", "dxf"))
    else:
        pdf = BP / "phase2" / "out" / "pdf" / f"{rv['file']}.pdf"
        dxf = BP / "phase2" / "out" / "dxf" / f"{rv['file']}.dxf"
        if rv.get("frozen") and (pdf.exists() or dxf.exists()) and not a.force:
            sys.exit("Revision is FROZEN; use --out-dir to regenerate for checking.")
    sh = builder(p2, prog, ob, out)
    pdf.parent.mkdir(parents=True, exist_ok=True)
    dxf.parent.mkdir(parents=True, exist_ok=True)
    sh.render_pdf(pdf, title=f"{SHEET_NO} Rev {pm['revision']} {pm['title']}", png_path=a.png)
    sh.render_dxf(dxf)
    print(f"wrote {pdf}\nwrote {dxf}" + (f"\nwrote {a.png}" if a.png else ""))


if __name__ == "__main__":
    main()
