"""P2-G-003 — Phase 2 PROGRAM TEST-FIT (tabloid 17 x 11 landscape), vector PDF + DXF.

Rev A (FROZEN, build()): one-level area arithmetic against 55,000 SF read as total floor area.
Rev B (build_b()): two levels; ground footprint vs the 55,000 SF FOOTPRINT cap (D-031), total GSF,
stacking, vertical circulation, schematic bowl section. NOT a floor plan.
All numbers come from params/phase2.yaml + params/phase2_program.yaml via p2_testfit.py.
Layout constants below are sheet geometry only.

Run from the repo root:
  /workspace/.venv-keystone/bin/python blueprints/phase2/src/p2_g_003.py [--rev A|B] [--png PATH] [--out-dir DIR] [--force]
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--png", help="optional PNG preview path (outside the repo)")
    ap.add_argument("--out-dir", help="write PDF/DXF here instead of phase2/out/{pdf,dxf}")
    ap.add_argument("--force", action="store_true", help="allow overwriting a FROZEN revision in the repo")
    ap.add_argument("--rev", choices=["A", "B"], default="B", help="A = frozen one-level sheet; B = two-level sheet (default)")
    a = ap.parse_args()
    if a.rev == "A":
        p2, prog, ob, out = tf.summary()
        pm, builder = prog["meta"], build
    else:
        p2, prog, ob, out = tf.summary_b()
        pm, builder = prog["meta_rev_b"], build_b
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
