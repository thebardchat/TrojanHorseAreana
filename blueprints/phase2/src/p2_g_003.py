"""P2-G-003 — Phase 2 PROGRAM TEST-FIT (tabloid 17 x 11 landscape), vector PDF + DXF.

One page of area arithmetic: area table, seating, occupant load + fixtures, gross-up,
fit check against the locked 55,000 SF, options A/B/C, sources. NOT a floor plan.
All numbers come from params/phase2.yaml + params/phase2_program.yaml via p2_testfit.py.
Layout constants below are sheet geometry only.

Run from the repo root:
  /workspace/.venv-keystone/bin/python blueprints/phase2/src/p2_g_003.py [--png PATH] [--out-dir DIR] [--force]
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--png", help="optional PNG preview path (outside the repo)")
    ap.add_argument("--out-dir", help="write PDF/DXF here instead of phase2/out/{pdf,dxf}")
    ap.add_argument("--force", action="store_true", help="allow overwriting a FROZEN revision in the repo")
    a = ap.parse_args()
    p2, prog, ob, out = tf.summary()
    rv = p2["sheets"][SHEET_NO]["revisions"][prog["meta"]["revision"]]
    if a.out_dir:
        pdf, dxf = (Path(a.out_dir) / f"{rv['file']}.{e}" for e in ("pdf", "dxf"))
    else:
        pdf = BP / "phase2" / "out" / "pdf" / f"{rv['file']}.pdf"
        dxf = BP / "phase2" / "out" / "dxf" / f"{rv['file']}.dxf"
        if rv.get("frozen") and (pdf.exists() or dxf.exists()) and not a.force:
            sys.exit("Revision is FROZEN; use --out-dir to regenerate for checking.")
    sh = build(p2, prog, ob, out)
    pdf.parent.mkdir(parents=True, exist_ok=True)
    dxf.parent.mkdir(parents=True, exist_ok=True)
    sh.render_pdf(pdf, title=f"{SHEET_NO} Rev {prog['meta']['revision']} {prog['meta']['title']}", png_path=a.png)
    sh.render_dxf(dxf)
    print(f"wrote {pdf}\nwrote {dxf}" + (f"\nwrote {a.png}" if a.png else ""))


if __name__ == "__main__":
    main()
