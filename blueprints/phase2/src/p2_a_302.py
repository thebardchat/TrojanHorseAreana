"""KEYSTONE P2-A-302 SIGHT-LINE STUDY (Phase 2, P2-T-009). Schematic, color.

Rev A (2026-10-04, Shane 7:24 AM CT): C-values per row, seated and standing, for both tiers (telescopic lower; fixed upper
stepping DOWN from the Level 2 loop, D-049) toward the near edge of the nearest mat. Cases: AS DRAWN (P2-A-301 geometry) and
PROPOSED (upper riser 19 in + east tier 6 ft further from the mats, D-053 OPEN). Also checks the telescopic closed stack
under the upper-tier front (Hussey recess dimensions vs. headroom).
Method / values: params/phase2_sightlines.yaml (Green Guide C-value formula; eye heights and targets cited or ASSUMED).
Geometry: params/phase2_sect.yaml, params/phase2_plan_rev_d.yaml, params/phase2_elev.yaml. Rev A FROZEN 9:47 AM CT.
Rev B (Shane 9:47 AM CT): the 'as drawn' basis changed — P2-A-101 Rev E / P2-A-301 Rev C draw 19 in upper risers and a
16 ft east focal (D-053) = Rev A's PROPOSED case. Re-cased: AS DRAWN (Rev E) vs REV D BASIS (superseded, Rev A's as
drawn); C-values unchanged. Plan: phase2_plan_rev_e.yaml. Data: phase2_sightlines.yaml rev_b. Low band / exits -> D-061. Rev B FROZEN 10:27 AM CT.
Rev C (Shane 10:27 AM CT): D-061 DECIDED Option B — recheck with L2 FF 17'-9" and 21 in upper risers (front row 9.0 ft) as drawn
on P2-A-101 Rev F / A-301 Rev D; Rev E basis kept for comparison. Each case may carry its own l2_ft. Data: phase2_sightlines.yaml rev_c.
Usage (from the repo root):
  /workspace/.venv-keystone/bin/python blueprints/phase2/src/p2_a_302.py [--rev A|B|C] [--png PATH] [--out-dir DIR] [--force] [--md]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

BP = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BP / "shared"))
from palette import SCHOOL_RED  # noqa: E402
from titleblock import Sheet, add_titleblock, text_width_in  # noqa: E402

W, H, M = 17.0, 11.0, 0.5
SHEET_NO = "P2-A-302"
FT = 0.3048
L_CUT, L_FILL, L_TAG, L_SL = "A-SITE-CUTL", "A-SITE-FILL", "A-SITE-IDEN", "A-SITE-SLIN"
C = dict(cut="#3C3C3C", floor="#D9B77E", mat="#C9A227", lower="#D88A8A", upper="#A7B3C3", loop="#C8693A", room="#F0ECE4",
         air="#E8F0F8", ok="#2B2B2B", mid="#D9822B", bad=SCHOOL_RED, stack="#B9B9B9")
SLAB = 1.0            # graphic only
REV = "A"             # set by main(); Rev B branches only (Rev A output stays byte-identical)
CASES = ("as_drawn", "proposed")
HDR = {"as_drawn": "AS DRAWN (P2-A-301)", "proposed": "PROPOSED (D-053)"}
SHORT = {"as_drawn": "drawn", "proposed": "proposed"}


def load():
    rd = lambda n: yaml.safe_load((BP / "params" / n).read_text(encoding="utf-8"))
    out = [rd("phase2.yaml"), rd("phase2_elev.yaml"), rd("phase2_plan_rev_d.yaml"), rd("phase2_sect.yaml"), rd("phase2_sightlines.yaml")]
    if REV in ("B", "C"):                              # Rev B: Plan Rev E; cases re-labelled (rev_b); Rev C: Plan Rev F (rev_c)
        global CASES, HDR, SHORT
        rb = out[4]["rev_b" if REV == "B" else "rev_c"]
        out[2] = rd(rb["plan_file"])
        out[4]["cases"].update(rb["cases"])
        CASES = tuple(rb["case_order"])
        HDR = {k: rb["cases"][k]["label"] for k in CASES}
        SHORT = {k: rb["cases"][k]["short"] for k in CASES}
    return tuple(out)


def focal_distances(plan, mat_ft):
    """Horizontal distance (ft) from each tier front to the near edge of the nearest mat (plan Rev D)."""
    mats = [m["origin"] for m in plan["mats"]]
    lb = {b["side"]: b["rect"] for b in plan["tiers"]["lower"]["bands"]}
    n = lb["N"][1] - max(y + mat_ft for _, y in mats)
    s = min(y for _, y in mats) - lb["S"][3]
    e = lb["E"][0] - max(x + mat_ft for x, _ in mats)
    return {"N": n, "S": s, "E": e}


def grade(c, sl):
    if c is None:
        return None
    return "ok" if c >= sl["targets"]["c_target_mm"] else ("mid" if c >= sl["targets"]["c_min_mm"] else "bad")


def calc(sl, sc, l2, d0, lower_rise_in, upper_rise_in, standing):
    """Eyes along the section (D = ft from the focal point, z = ft above the floor) and C (mm) of each row over the one in front."""
    lo, up = sc["seating"]["lower"], sc["seating"]["upper"]
    e_sit, e_st = sl["eyes"]["seated_m"] / FT, sl["eyes"]["standing_m"] / FT
    A = sl["eyes"]["offset_from_row_rear_m"] / FT
    E = e_st if standing else e_sit
    T, N, n = lo["row_depth_in"] / 12, lower_rise_in / 12, lo["rows"]
    uT, uN, un = up["row_depth_in"] / 12, upper_rise_in / 12, up["rows"]
    zf = l2 - un * uN
    rows = []
    for k in range(1, n + 1):
        rows.append(dict(name=f"L{k}", D=d0 + k * T - A, deck=(k - 1) * N, x0=d0 + (k - 1) * T, x1=d0 + k * T))
    for j in range(1, un + 1):
        rows.append(dict(name=f"U{j}", D=d0 + n * T + j * uT - A, deck=zf + (j - 1) * uN, x0=d0 + n * T + (j - 1) * uT,
                         x1=d0 + n * T + j * uT))
    for r in rows:
        r["z"] = r["deck"] + E
    rb = d0 + n * T + un * uT + sl["rail"]["standing_back_ft"]
    rows.append(dict(name="RAIL", D=rb, deck=l2, z=l2 + e_st, x0=rb, x1=rb))
    rows[0]["C"] = None
    for f, b in zip(rows, rows[1:]):
        b["C"] = (f["D"] * b["z"] / b["D"] - f["z"]) * FT * 1000
    u1 = rows[n]
    g = sc["guards"]["tier_front_in"] / 12
    fascia = ((d0 + n * T) * u1["z"] / u1["D"] - (zf + g)) * FT * 1000
    return dict(rows=rows, zf=zf, fascia=fascia, d0=d0, lower_back=d0 + n * T, upper_back=d0 + n * T + un * uT,
                loop_end=d0 + n * T + un * uT + sl["loop"]["width_ft"], l2=l2, uN=uN, N=N)


def all_cases(sl, sc, plan, ev, p2):
    l2 = ev["heights"]["l2_ff"]["value"]
    fd = focal_distances(plan, p2["spaces"]["arena"]["mat_ft"])
    out = {}
    for cname in CASES:
        cs = sl["cases"][cname]
        for side, d0 in (("NS", fd["N"]), ("E", cs["east_clear_ft"])):
            for st in (False, True):
                out[(cname, side, st)] = calc(sl, sc, cs.get("l2_ft", l2), d0, cs["lower_rise_in"], cs["upper_rise_in"], st)
    assert fd["N"] == fd["S"], fd
    assert sl["cases"][CASES[0]]["east_clear_ft"] == fd["E"], fd
    return out, fd


def fig_section(sh, x0, y0, fpi, res, sl, sc, title, sub, mat_ft=6.0):
    s = 1.0 / fpi

    def P(u, z):
        return x0 + (u + mat_ft) * s, y0 + z * s
    d0, l2 = res["d0"], res["l2"]
    rows = res["rows"]
    # floor + mat + focus
    sh.poly([P(-mat_ft, -0.5), P(d0, -0.5), P(d0, 0), P(-mat_ft, 0)], fill=C["floor"], layer=L_FILL, lw=0.3)
    sh.poly([P(-mat_ft, 0), P(0, 0), P(0, 0.35), P(-mat_ft, 0.35)], fill=C["mat"], layer=L_FILL, lw=0.3)
    fx, fy = P(0, 0)
    sh.poly([(fx - 0.035, fy - 0.07), (fx + 0.035, fy - 0.07), (fx, fy)], fill=C["bad"], layer=L_SL, lw=0)
    sh.text(fx - 0.02, fy - 0.17, "FOCAL POINT", size=4.2, align="right", layer=L_TAG, bold=True)
    sh.text(fx - 0.02, fy - 0.27, "near mat edge", size=4.0, align="right", layer=L_TAG)
    a, b = P(0, -1.6), P(d0, -1.6)
    sh.line(a[0], a[1], b[0], b[1], layer=L_TAG, lw=0.35)
    for q in (a, b):
        sh.line(q[0], q[1] - 0.03, q[0], q[1] + 0.03, layer=L_TAG, lw=0.35)
    sh.text((a[0] + b[0]) / 2, a[1] - 0.12, f"{d0:g}'", size=4.6, align="center", layer=L_TAG, bold=True)
    # lower tier
    lows = [r for r in rows if r["name"].startswith("L")]
    pts = [P(d0, 0)]
    for r in lows:
        pts += [P(r["x0"], r["deck"] + 0.15), P(r["x1"], r["deck"] + 0.15)]
    pts += [P(res["lower_back"], 0)]
    sh.poly(pts, fill=C["lower"], layer=L_CUT, lw=0.5)
    # upper tier + soffit (graphic) + fascia
    ups = [r for r in rows if r["name"].startswith("U")]
    pts = []
    for r in ups:
        pts += [P(r["x0"], r["deck"]), P(r["x1"], r["deck"])]
    pts += [P(res["upper_back"], l2), P(res["upper_back"], l2 - SLAB), P(res["lower_back"], res["zf"] - SLAB)]
    sh.poly(pts, fill=C["upper"], layer=L_CUT, lw=0.5)
    g = sc["guards"]["tier_front_in"] / 12
    a, b = P(res["lower_back"], res["zf"]), P(res["lower_back"], res["zf"] + g)
    sh.line(a[0], a[1], b[0], b[1], layer=L_CUT, lw=1.0)
    # wall under the upper-tier front, loop slab
    sh.poly([P(res["lower_back"], 0), P(res["lower_back"] + 0.8, 0), P(res["lower_back"] + 0.8, res["zf"] - SLAB),
             P(res["lower_back"], res["zf"] - SLAB)], fill=C["cut"], layer=L_CUT, lw=0)
    sh.poly([P(res["upper_back"], l2 - SLAB), P(res["loop_end"], l2 - SLAB), P(res["loop_end"], l2), P(res["upper_back"], l2)],
            fill=C["cut"], layer=L_CUT, lw=0)
    sh.poly([P(res["upper_back"], l2), P(res["loop_end"], l2), P(res["loop_end"], l2 + 0.35), P(res["upper_back"], l2 + 0.35)],
            fill=C["loop"], layer=L_FILL, lw=0)
    # sightlines (from each eye to the focal point) + eyes
    for r in rows:
        col = C[grade(r["C"], sl)] if r["C"] is not None else C["ok"]
        a = P(r["D"], r["z"])
        sh.line(a[0], a[1], fx, fy, layer=L_SL, lw=0.35 if r["C"] is None or r["C"] >= 90 else 0.55)
        sh.poly([(a[0] - 0.018, a[1] - 0.018), (a[0] + 0.018, a[1] - 0.018), (a[0] + 0.018, a[1] + 0.018), (a[0] - 0.018, a[1] + 0.018)],
                fill=col, layer=L_SL, lw=0)
        sh.text(a[0], a[1] + 0.045, r["name"], size=3.6, align="center", layer=L_TAG, color=col)
    # L2 datum
    a = P(res["loop_end"] + 0.6, l2)
    sh.text(a[0], a[1] - 0.02, f"LOOP / L2 {l2:g}'", size=4.2, layer=L_TAG)
    a = P(res["lower_back"] + 1.0, res["zf"] - 2.2)
    sh.text(a[0], a[1], f"front row {res['zf']:.2f}'", size=4.2, layer=L_TAG)
    sh.text(x0, y0 - 0.42, title, size=6.8, bold=True, layer=L_TAG)
    sh.line(x0, y0 - 0.46, x0 + text_width_in(title, 6.8, True), y0 - 0.46, lw=0.7)
    sh.text(x0, y0 - 0.58, sub, size=5.0, layer=L_TAG)
    return P(res["loop_end"] + 6, l2 + 5.6)


def fig_stack(sh, x0, y0, fpi, sl, sc, res_drawn, res_prop, which):
    """Telescopic stack recessed under the upper-tier front: (a) closed, (b) open. u = ft from the upper-tier front line
    (negative = toward the floor)."""
    s = 1.0 / fpi
    st = sl["stack"]
    hr = (st["overall_seat_height_in"] + st["recess_height_add_in"]) / 12      # min recess height
    dr = (st["closed_depth_in"] + st["recess_depth_add_in"]) / 12              # min recess depth
    zf, uN = res_drawn["zf"], res_drawn["uN"]
    lo = sc["seating"]["lower"]
    T, N, n = lo["row_depth_in"] / 12, lo["rise_in"] / 12, lo["rows"]

    def P(u, z):
        return x0 + (u + 6.0) * s, y0 + z * s
    sh.poly([P(-6, -0.4), P(5.5, -0.4), P(5.5, 0), P(-6, 0)], fill=C["floor"], layer=L_FILL, lw=0.3)
    # upper tier underside (as drawn) — deck top at the front = zf; slope = rise / row depth
    sl_ = uN / (sc["seating"]["upper"]["row_depth_in"] / 12)
    # upper-tier deck line (as drawn, slope = rise / row depth) with a graphic slab below it
    sh.poly([P(0, zf), P(5.5, zf + 5.5 * sl_), P(5.5, zf + 5.5 * sl_ - 0.45), P(0, zf - 0.45)], fill=C["upper"], layer=L_CUT, lw=0.5)
    sh.text(*P(0.3, zf + 0.3 * sl_ + 1.25), f"upper-tier deck (front {zf:.2f}')", size=4.0)
    a, b = P(0, 0), P(0, zf + 1.6)
    sh.dashed(a[0], a[1], b[0], b[1], layer=L_TAG, lw=0.35, dash=0.03, gap=0.03)
    sh.text(*P(-0.1, zf + 1.75), "upper-tier face", size=4.0, align="right")
    # proposed front (19 in riser) dashed
    zp = res_prop["zf"]
    a, b = P(0, zp), P(5.5, zp + 5.5 * res_prop["uN"] / 3.0)
    sh.dashed(a[0], a[1], b[0], b[1], layer=L_SL, lw=0.6, dash=0.05, gap=0.035)
    if which == "closed":
        sh.poly([P(0, 0), P(dr, 0), P(dr, hr), P(0, hr)], fill=C["stack"], layer=L_CUT, lw=0.6)
        sh.text(*P(dr / 2, hr / 2 + 0.6), "CLOSED", size=4.4, align="center", bold=True)
        sh.text(*P(dr / 2, hr / 2 - 0.4), "STACK", size=4.4, align="center", bold=True)
        # zone left for the tier structure + finish between the recess top and the front deck
        sh.poly([P(0, hr), P(dr, hr), P(dr, zf + dr * sl_ - 0.45), P(0, zf - 0.45)], fill="#F3D9A4", layer=L_FILL, lw=0.3)
        q0, q1 = P(dr + 0.35, hr), P(dr + 0.35, zf)
        sh.line(q0[0], q0[1], q1[0], q1[1], layer=L_TAG, lw=0.4)
        for q in (q0, q1):
            sh.line(q[0] - 0.03, q[1], q[0] + 0.03, q[1], layer=L_TAG, lw=0.4)
        room = (zf - hr) * 12
        sh.text(*P(-5.8, zf - 0.1), f"front deck {zf:.2f}' − {hr * 12:.3g}\"", size=4.3)
        sh.text(*P(-5.8, zf - 0.9), f"= {room:.1f}\" structure + finish", size=4.3, bold=True)
        sh.text(*P(-5.8, 2.0), f"recess min {dr * 12:.0f}\" deep x", size=4.2)
        sh.text(*P(-5.8, 1.2), f"{hr * 12:.3g}\" high (Hussey)", size=4.2)
        rp = (zp - hr) * 12
        sh.text(*P(-5.8, zp - 0.6), f"{'Rev D' if REV == 'B' else 'Rev E' if REV == 'C' else 'proposed'} {zp:.2f}' front: {rp:.1f}\" left", size=4.2,
                color=None if REV in ("B", "C") else C["bad"])
        return room, rp, hr, dr
    # open: rear rows stay in the recess
    pts = [P(dr - (n - 1) * T, 0)]
    for k in range(1, n):
        u_a, u_b = dr - n * T + k * T, dr - n * T + (k + 1) * T
        pts += [P(u_a, k * N + 0.15), P(u_b, k * N + 0.15)]
    pts += [P(dr, 0)]
    sh.poly(pts, fill=C["lower"], layer=L_CUT, lw=0.5)
    top = (n - 1) * N
    need = top + 7.5
    a, b = P(dr - 2.0, need), P(dr, need)
    sh.dashed(a[0], a[1], b[0], b[1], layer=L_SL, lw=0.8, dash=0.04, gap=0.03)
    soff = zf + dr * sl_
    sh.text(*P(-5.8, need + 0.3), f"7'-6\" ceiling over row 6 (1003.2) = {need:.2f}'", size=4.3, color=C["bad"], bold=True)
    sh.text(*P(-5.8, need - 0.6), f"deck at recess back {soff:.2f}' − structure", size=4.3, color=C["bad"])
    sh.text(*P(-5.8, 7.0), "rows 5-6 stay in the recess", size=4.2)
    sh.text(*P(-5.8, 6.2), "under the overhang when open", size=4.2)
    sh.text(*P(dr - 1.0, need + 0.3), "need", size=4.0, align="center", color=C["bad"])
    return need, soff


def table(sh, x, y, res, sl, colw, rowh=0.148):
    cols = [(c, sd, st) for c in CASES for sd in ("NS", "E") for st in (False, True)]
    hdr1 = [(HDR[CASES[0]], 0, 4), (HDR[CASES[1]], 4, 8)]
    x0 = x + colw[0]
    w = colw[1]
    for t_, a, b in hdr1:
        sh.text(x0 + (a + b) / 2 * w, y, t_, size=5.6, bold=True, align="center")
        sh.line(x0 + a * w + 0.04, y - 0.04, x0 + b * w - 0.04, y - 0.04, lw=0.5)
    y -= 0.16
    sub = []
    for cn, side, stnd in cols:
        r = res[(cn, side, stnd)]
        sub.append((f"{'N/S' if side == 'NS' else 'E'} {r['d0']:g}'", "stand" if stnd else "seated"))
    for i, (a, b) in enumerate(sub):
        sh.text(x0 + (i + 0.5) * w, y, a, size=4.8, bold=True, align="center")
        sh.text(x0 + (i + 0.5) * w, y - 0.12, b, size=4.6, align="center")
    sh.text(x + 0.02, y - 0.06, "ROW", size=4.8, bold=True)
    y -= 0.17
    sh.line(x, y + 0.02, x0 + 8 * w, y + 0.02, lw=0.5)
    names = [r["name"] for r in res[cols[0]]["rows"]][1:]
    for nm in names:
        y -= rowh
        sh.text(x + 0.02, y, nm + (" (stands)" if nm == "RAIL" else ""), size=4.8, bold=nm.startswith("U1") or nm == "RAIL")
        for i, cc in enumerate(cols):
            r = next(q for q in res[cc]["rows"] if q["name"] == nm)
            g = grade(r["C"], sl)
            sh.text(x0 + (i + 0.5) * w, y, f"{r['C']:.0f}", size=5.0, align="center", bold=g != "ok", color=C[g])
    for lab, key, fmt in (("fascia clr (U1)", "fascia", "{:.0f}"), ("front row (ft)", "zf", "{:.2f}")):
        y -= rowh
        sh.text(x + 0.02, y, lab, size=4.6)
        for i, cc in enumerate(cols):
            v = res[cc][key]
            col = C["bad"] if key == "fascia" and v < 0 else None
            sh.text(x0 + (i + 0.5) * w, y, fmt.format(v), size=4.8, align="center", color=col)
    sh.line(x, y - 0.05, x0 + 8 * w, y - 0.05, lw=0.5)
    return y - 0.05


def summary(res, sl):
    out = {}
    for k, r in res.items():
        cs = [q for q in r["rows"] if q["C"] is not None]
        out[k] = dict(min=min(q["C"] for q in cs), fails=[q["name"] for q in cs if q["C"] < sl["targets"]["c_min_mm"]],
                      marg=[q["name"] for q in cs if sl["targets"]["c_min_mm"] <= q["C"] < sl["targets"]["c_target_mm"]])
    return out


def md_tables(res, sl):
    cols = [(c, sd, st) for c in CASES for sd in ("NS", "E") for st in (False, True)]
    hd = ["Row"] + [f"{SHORT[c]} {'N/S' if s == 'NS' else 'E'} {res[(c, s, t)]['d0']:g} ft {'standing' if t else 'seated'}" for c, s, t in cols]
    lines = ["| " + " | ".join(hd) + " |", "|" + "---|" * len(hd)]
    for nm in [r["name"] for r in res[cols[0]]["rows"]][1:]:
        vals = []
        for cc in cols:
            q = next(r for r in res[cc]["rows"] if r["name"] == nm)
            g = grade(q["C"], sl)
            vals.append(f"{q['C']:.0f}" + ("" if g == "ok" else (" ~" if g == "mid" else " ✗")))
        lines.append(f"| {nm} | " + " | ".join(vals) + " |")
    lines.append("| fascia clearance U1 (mm) | " + " | ".join(f"{res[c]['fascia']:.0f}" for c in cols) + " |")
    lines.append("| upper front row deck (ft) | " + " | ".join(f"{res[c]['zf']:.2f}" for c in cols) + " |")
    return "\n".join(lines)


NOTES = [
    ("METHOD", None),
    ("C = D(N + R)/(D + T) − R (Green Guide 12.3), computed from each actual eye position (also covers the step between tiers and the loop rail). Focal point = near edge of the nearest mat at floor level (Shane). Eyes: seated 1.2 m above the tread, 0.15 m forward of the row's rear edge; standing 1.6 m (5'-3\") — secondary sources, see R-020. Grades: ≥ 90 mm PASS (FIFA preferred, CEN/TR 15913 new stands), 60–90 MARGINAL, < 60 FAIL (FIFA minimum 60).", "•"),
    ("Focal distances from the frozen plan (Rev D): N and S tier fronts 25' from the nearest mat (10' clear + 15' table zone); E tier front 10' (10' clear only). No west tier. Section-only study (2D); corners and wheelchair positions TBD.", "•"),
    ("RESULTS — AS DRAWN", None),
    ("Upper tier (14\" per 36\" row) FAILS on every side: N/S seated 40–49 mm, standing 17–20; E negative (rows hidden). Lower tier PASSES at N/S (149–190 seated) but at E (10' focal) is 46–74 seated (L4–L6 FAIL) and 9–15 standing. U1 sees well over the lower tier (≥ 780) and the 26\" fascia.", "•"),
    ("RISER CHANGES NEEDED (PROPOSED, D-053 OPEN)", None),
    ("Upper riser 14\" → 19\" per row (3 aisle risers of 6⅓\", 12\" treads; IBC 1030.14.2) — front row drops 9.17' → 7.08' because the back stays at the loop (D-049). N/S then seated ≥ 149, standing ≥ 127.", "•"),
    ("East side cannot reach 60 mm with the loop at 15' and a 10' focal distance (best ≈ 46 mm): move the E tier 6' further from the mats (10' → 16') → E seated ≥ 101, standing 72–103 (4 rows MARGINAL). A 16\" Hussey rise fixes the E lower rows alone, but the stepped-down upper tier then collides with it.", "•"),
    ("Lower tier stays at the Hussey 11⅝\" rise (9⅝\" would also pass at N/S: 112–143 seated).", "•"),
    ("TELESCOPIC STACK UNDER THE UPPER-TIER FRONT (D-049)", None),
    ("Closed stack, recessed: Hussey min recess 4'-0\" deep x 6'-5⅜\" high. As drawn (front 9.17') it fits only if the tier structure + finish at the front edge is ≤ 32.6\". With the proposed 7.08' front only 7.6\" remain — does not fit.", "•"),
    ("Open: in a recessed stack the rear rows stay in the recess, so rows 5–6 would sit under the overhang with < 7'-6\" ceiling (1003.2) — CONFLICT either way. Recommendation: keep the stack in front of the upper-tier face (as P2-A-301); use the low zone under the tier for storage / mechanical only.", "•"),
    ("Under-tier front also limits exits: EXIT (N) / (E) passages under the tier need a 7'-6\" ceiling (1003.2) — local raise / vomitory cut at the next A-101/A-102 revision.", "•"),
]


NOTES_B = NOTES[:2] + [
    ("Focal distances from P2-A-101 Rev E: N and S tier fronts 25' from the nearest mat (10' clear + 15' table zone); E tier front 16' (D-053; building 210'). No west tier. Section-only study (2D); corners and wheelchair positions TBD.", "•"),
    ("RESULTS — AS DRAWN (REV E, D-053 DECIDED)", None),
    ("Upper 19\" per 36\" row (3 aisle risers of 6⅓\", 12\" treads; IBC 1030.14.2), front row 7.08' (back stays at the loop, D-049). Every seated row PASSES: N/S ≥ 149 mm, E ≥ 101. Standing: N/S ≥ 127; E ≥ 72 (L4–L6, U4–U5 MARGINAL, none FAIL).", "•"),
    ("Lower tier stays at the Hussey 11⅝\" rise. U1 clears the 26\" fascia (326 mm N/S, 263 E seated).", "•"),
    ("REV D BASIS (SUPERSEDED, P2-A-302 Rev A 'as drawn')", None),
    ("14\"/row upper + 10' east focal: upper FAILS on every side (N/S seated 40–49, E negative); E lower L4–L6 FAIL. Kept for comparison only; fixed by D-053 on Plan Rev E.", "•"),
    ("TELESCOPIC STACK UNDER THE UPPER-TIER FRONT (D-049)", None),
    ("Closed stack, recessed (Hussey min 4'-0\" deep x 6'-5⅜\" high) under the 7.08' front leaves 7.6\" for structure + finish — DOES NOT FIT. Open: rows 5–6 would sit under the overhang (< 7'-6\", 1003.2). Keep the stack in front of the upper-tier face (as P2-A-301 Rev C).", "•"),
    ("LOW BAND + EXIT PATHS (D-061 OPEN, R-022)", None),
    ("1.5' tier structure (ASSUMED) leaves 5.6' / 7.2' under rows 1–2 (6' low band). Exit N, Exit E, SE concourse and the lobby / portal / athlete-route edge run under it. Option A: omit rows 1–2 there (−125 seats; −56 with rails). Option B: L2 17'-9\" + 21\" risers (front 9.0'): C unchanged (149 / 101 seated).", "•"),
]


NOTES_C = NOTES[:2] + [
    ("Focal distances from P2-A-101 Rev F: N and S tier fronts 25' from the nearest mat (10' clear + 15' table zone); E tier front 16' (D-053). No west tier. Section-only study (2D); corners and wheelchair positions TBD.", "•"),
    ("RESULTS — AS DRAWN (REV F, D-061 DECIDED)", None),
    ("L2 FF 17'-9\", upper 21\" per 36\" row (3 aisle risers of 7\", 12\" treads; IBC 1030.14.2), front row 9.0'. Every seated row PASSES: N/S ≥ 149 mm, E ≥ 101 (lower tier governs, same as Rev E). Upper tier seated N/S ≥ 179, E ≥ 105.", "•"),
    ("Standing: N/S ≥ 127; E ≥ 72 (L4–L6 and U3–U5 MARGINAL, none FAIL). U1 clears the 26\" fascia (289 mm N/S, 215 E seated).", "•"),
    ("REV E BASIS (SUPERSEDED, P2-A-302 Rev B 'as drawn')", None),
    ("L2 15', 19\"/row, front 7.08': same lower-tier minimums; upper seated N/S ≥ 175, E ≥ 109; standing E ≥ 81. Kept for comparison only.", "•"),
    ("TELESCOPIC STACK UNDER THE UPPER-TIER FRONT (D-049)", None),
    ("Closed stack, recessed (Hussey min 4'-0\" deep x 6'-5⅜\" high) under the 9.0' front leaves 30.6\" for structure + finish (1.5' = 18\" ASSUMED) — FITS closed. Open: rows 5–6 still sit under the overhang (< 7'-6\", 1003.2): keep the stack in front of the upper-tier face (as P2-A-301 Rev D).", "•"),
    ("EXIT PATHS (D-061 DECIDED, Option B)", None),
    ("1.5' tier structure (ASSUMED) leaves 7'-6\" under row 1 (1003.2 minimum, no margin) and 9.25'+ under rows 2–5: no low band; Exit N, Exit E, SE concourse and the lobby / portal / athlete-route edge are clear. 0 seats lost.", "•"),
]


def build(p2, ev, plan, sc, sl, res, fd):
    meta2, sm = p2["meta"], sl["meta"]
    sh = Sheet(W, H)
    body_bottom = add_titleblock(sh, {
        "project": f"{meta2['project']}\n{meta2['arena_name']} · {meta2['location']}",
        "phase": "PHASE 2",
        "title": "SIGHT-LINE STUDY\nSCHEMATIC · COLOR",
        "scale": "AS NOTED",
        "date": meta2["sheet_date"],
        "revision": sl["rev_b"]["revision"] if REV == "B" else sl["rev_c"]["revision"] if REV == "C" else sm["revision"],
        "drawn_by": meta2["drawn_by"],
        "sheet_no": SHEET_NO,
        "stamp": meta2["stamp"],
    }, margin=M, tb_h=0.95, stamp_h=0.40)
    fpi = sl["scales"]["section_ft_per_in"]
    sec_s = "3/32\" = 1'-0\""
    if REV in ("B", "C"):
        figs = sl["rev_b" if REV == "B" else "rev_c"]["figures"]
        r1, r2, r3 = (fig_section(sh, 0.95, y_, fpi, res[(f_["case"], f_["side"], False)], sl, sc, f_["title"], f"{sec_s} · {f_['sub']}")
                      for f_, y_ in zip(figs, (8.35, 5.55, 2.75) if REV == "B" else (8.25, 5.40, 2.75)))
    else:
        r1 = fig_section(sh, 0.95, 8.35, fpi, res[("as_drawn", "NS", False)], sl, sc,
                         "1  AS DRAWN — NORTH / SOUTH SIDE (seated eyes)", f"{sec_s} · focal 25' (10' clear + 15' table zone) · telescopic 11⅝\" · upper 14\"/row")
        r2 = fig_section(sh, 0.95, 5.55, fpi, res[("as_drawn", "E", False)], sl, sc,
                         "2  AS DRAWN — EAST SIDE (seated eyes)", f"{sec_s} · focal 10' (10' clear) · worst side")
        r3 = fig_section(sh, 0.95, 2.75, fpi, res[("proposed", "E", False)], sl, sc,
                         "3  PROPOSED — EAST SIDE (seated eyes)", f"{sec_s} · focal 16' (+6') · upper 19\"/row, front 7.08' (D-053)")
    for r_, lim in ((r1, 10.45), (r2, 7.6), (r3, 4.8)):
        if r_[1] > lim or r_[0] > 10.25:
            raise SystemExit(f"LAYOUT OVERFLOW: section figure at {r_[0]:.2f}, {r_[1]:.2f}")
    # key for line colours
    kx, ky = 8.6, 10.15
    sh.text(kx, ky, "SIGHTLINE GRADE (C, mm)", size=5.6, bold=True)
    for i, (k, t_) in enumerate((("ok", "≥ 90 PASS"), ("mid", "60–90 MARGINAL"), ("bad", "< 60 FAIL"))):
        yy = ky - 0.17 - i * 0.15
        sh.poly([(kx, yy), (kx + 0.3, yy), (kx + 0.3, yy + 0.06), (kx, yy + 0.06)], fill=C[k], layer=L_SL, lw=0)
        sh.text(kx + 0.38, yy, t_, size=5.2, color=C[k])
    sh.text(kx, ky - 0.68, "Dots = eyes; label colour = C of that row", size=4.6)
    sh.text(kx, ky - 0.80, "over the row in front. Values: table.", size=4.6)
    # stack figures
    sfpi = sl["scales"]["stack_ft_per_in"]
    room, rp, hr, dr = fig_stack(sh, 7.75, 5.05, sfpi, sl, sc, res[(CASES[0], "NS", False)], res[(CASES[1], "NS", False)], "closed")
    need, soff = fig_stack(sh, 7.75, 2.3, sfpi, sl, sc, res[(CASES[0], "NS", False)], res[(CASES[1], "NS", False)], "open")
    t4 = "4  TELESCOPIC STACK UNDER THE UPPER-TIER FRONT"
    sh.text(7.75, 7.62, t4, size=6.4, bold=True)
    sh.line(7.75, 7.58, 7.75 + text_width_in(t4, 6.4, True), 7.58, lw=0.7)
    ssub = sl["rev_b"]["stack_sub"] if REV == "B" else sl["rev_c"]["stack_sub"] if REV == "C" else "3/16\" = 1'-0\" · recessed (Hussey) · N/S as drawn · dashed = proposed 7.08' front"
    sh.text(7.75, 7.46, ssub, size=4.5)
    if REV == "B":
        sh.text(7.75, 4.86, f"(a) CLOSED — only {room:.1f}\" left for structure: DOES NOT FIT", size=5.2, bold=True, color=C["bad"])
    else:
        sh.text(7.75, 4.86, f"(a) CLOSED — fits only if structure ≤ {room:.1f}\" (as drawn)", size=5.2, bold=True)
    sh.text(7.75, 2.11, "(b) OPEN — rows 5-6 under the overhang: CONFLICT", size=5.2, bold=True, color=C["bad"])
    if 7.75 + text_width_in(ssub, 4.5) > 10.4:
        raise SystemExit("LAYOUT OVERFLOW: fig 4 subtitle")
    # table + notes
    xt = 10.55
    colw = (0.78, 0.635)
    y = table(sh, xt, 10.15, res, sl, colw)
    if xt + colw[0] + 8 * colw[1] > W - M - 0.04:
        raise SystemExit("LAYOUT OVERFLOW: table too wide")
    y -= 0.05
    for t_, b in (NOTES_B if REV == "B" else NOTES_C if REV == "C" else NOTES):
        if b is None:
            y = sh.para(xt, y - 0.03, W - M - 0.1 - xt, t_, size=5.9, bold=True)
        else:
            y = sh.para(xt, y, W - M - 0.1 - xt, t_, size=5.6, indent=0.1, bullet=b)
    if y < body_bottom + 0.05:
        raise SystemExit(f"LAYOUT OVERFLOW: notes {body_bottom + 0.05 - y:.2f} in into the stamp band")
    print(f"notes margin {y - body_bottom - 0.05:.2f} in; stack: room {room:.1f} in (proposed {rp:.1f}); open need {need:.2f} vs deck {soff:.2f}")
    return sh


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", choices=["A", "B", "C"], default="C")
    ap.add_argument("--png")
    ap.add_argument("--out-dir")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--md", action="store_true", help="print the C-value tables as markdown and exit")
    a = ap.parse_args()
    global REV
    REV = a.rev
    p2, ev, plan, sc, sl = load()
    res, fd = all_cases(sl, sc, plan, ev, p2)
    if a.md:
        print(md_tables(res, sl))
        for k, v in summary(res, sl).items():
            print(k, f"min {v['min']:.0f}", "FAIL", v["fails"], "MARG", v["marg"])
        return
    rv = p2["sheets"][SHEET_NO]["revisions"][a.rev]
    if a.out_dir:
        pdf, dxf = (Path(a.out_dir) / f"{rv['file']}.{e}" for e in ("pdf", "dxf"))
    else:
        pdf = BP / "phase2" / "out" / "pdf" / f"{rv['file']}.pdf"
        dxf = BP / "phase2" / "out" / "dxf" / f"{rv['file']}.dxf"
        if rv.get("frozen") and (pdf.exists() or dxf.exists()) and not a.force:
            sys.exit("Revision is FROZEN; use --out-dir to regenerate for checking.")
    sh = build(p2, ev, plan, sc, sl, res, fd)
    pdf.parent.mkdir(parents=True, exist_ok=True)
    dxf.parent.mkdir(parents=True, exist_ok=True)
    sh.render_pdf(pdf, title=f"{SHEET_NO} Rev {a.rev} {p2['sheets'][SHEET_NO]['title']}", png_path=a.png)
    sh.render_dxf(dxf)
    print(f"wrote {pdf}\nwrote {dxf}" + (f"\nwrote {a.png}" if a.png else ""))


if __name__ == "__main__":
    main()
