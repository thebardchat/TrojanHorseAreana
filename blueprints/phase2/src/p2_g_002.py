"""KEYSTONE P2-G-002 CODE ANALYSIS (SCHEMATIC) — Phase 2, BACKLOG P2-T-007. Tabloid, text + tables.

Rev A (2026-10-04, Shane 10:48 AM CT): code basis with a 2021 (designed, ASSUMED) / 2018 (county) edition column (R-006),
occupancy (R-007.1), construction type TBD, sprinklers + voice alarm (R-015.5), occupant load by space from the areas drawn
on P2-A-101/102 Rev F (IBC 2021 Table 1004.5 factors, R-007.2), event-floor cases for D-054 (OPEN) with Level 1 exits checked
against the WORST case (standing) and the other cases alongside, Level 2 stairs (R-018, D-052), travel / common path notes,
plumbing fixture basis (IPC 2021 ASSUMED, P2-G-003 Rev I). Door widths are not drawn: ASSUMED pairs (phase2_code.yaml).
Findings are reported with options; nothing is redesigned here.
Data: params/phase2_code.yaml, params/phase2_plan_rev_f.yaml, p2_testfit.summary_h (P2-G-003 Rev I).
Usage (from the repo root):
  /workspace/.venv-keystone/bin/python blueprints/phase2/src/p2_g_002.py [--rev A] [--png PATH] [--out-dir DIR] [--force] [--print]
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import yaml

BP = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BP / "shared"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from titleblock import Sheet, add_titleblock, text_width_in  # noqa: E402
import p2_testfit as tf  # noqa: E402

W, H, M = 17.0, 11.0, 0.5
SHEET_NO = "P2-G-002"
RED, GRN, GRY = "#CC0000", "#1E7B34", "#555555"
L_TAB = "G-ANNO-TABL"


def rd(n):
    return yaml.safe_load((BP / "params" / n).read_text(encoding="utf-8"))


def ov(a, b):
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    return w * h if w > 0 and h > 0 else 0.0


def compute():
    code, p2 = rd("phase2_code.yaml"), rd("phase2.yaml")
    _, _, _, h = tf.summary_h()
    plan = h["plan"]
    stairs = [s["rect"] for s in plan["vertical"]["stairs"]]
    rects = {}
    for lv in ("level_1", "level_2"):
        for grp in ("rooms", "zones"):
            for r in plan[lv].get(grp, []):
                rects[r["id"]] = r["rect"]
    fac = code["factors"]

    def area(i):
        r = rects[i]
        return round((r[2] - r[0]) * (r[3] - r[1]) - sum(ov(r, s) for s in stairs))

    def load(a, f):
        return -(-a // fac[f]["sf"])

    def rows(spaces):
        out = []
        for s in spaces:
            ar = [area(i) for i in s["ids"]]
            out.append(dict(label=s["label"], area=sum(ar), factor=s["factor"], load=sum(load(a, s["factor"]) for a in ar)))
        return out

    seats_l, seats_u = h["tot"]["lower"], h["tot"]["upper"]
    r1, r2 = rows(code["level_1"]["spaces"]), rows(code["level_2"]["spaces"])
    l1_fixed = seats_l + sum(r["load"] for r in r1)
    ef = code["event_floor"]
    cases = []
    for c in ef["cases"]:
        fl = load(ef["area_sf"], c["factor"])
        cases.append(dict(id=c["id"], label=c["label"], factor=c["factor"], floor=fl, l1=l1_fixed + fl))
    lo, li = plan["level_2"]["loop"]["outer"], plan["level_2"]["loop"]["inner"]
    loop_sf = round((lo[2] - lo[0]) * (lo[3] - lo[1]) - (li[2] - li[0]) * (li[3] - li[1]))
    sens = []
    for s in code["level_2"]["sensitivities"]:
        a = loop_sf if s.get("area") == "loop" else s["area_sf"]
        sens.append(dict(label=s["label"], area=a, factor=s["factor"], load=load(a, s["factor"])))
    l2_base = seats_u + sum(r["load"] for r in r2)
    l2_worst = l2_base + sum(s["load"] for s in sens)
    eg = code["egress"]
    dw, df, sf_ = eg["door_clear_in"], eg["door_in_per_occ"], eg["stair_in_per_occ"]
    n_open = len(eg["openings"])
    others = [o for o in eg["openings"] if o != eg["main_exit"] and o not in eg["stair_discharge"]]
    nsd = len(eg["stair_discharge"])
    prov_total = n_open * dw
    stair_door_req = l2_worst / nsd * df
    for c in cases:
        tot = c["l1"] + l2_worst
        c.update(total=tot, req_total=tot * df, main_req=tot / 2 * df, other_req=c["l1"] / 2 * df,
                 other_prov=len(others) * dw + nsd * (dw - stair_door_req), lose_one=prov_total - dw,
                 lose_req=0.5 * tot * df)
        c["pass_total"] = prov_total >= c["req_total"]
        c["pass_main"] = dw >= c["main_req"]
        c["pass_other"] = c["other_prov"] >= c["other_req"]
        c["pass_lose"] = c["lose_one"] >= c["lose_req"]
        c["main_pairs"] = math.ceil(c["main_req"] / dw)
        c["total_pairs"] = math.ceil(c["req_total"] / dw)
    wc = next(c for c in cases if c["id"] == ef["design_case"])
    # Option 1: main-exit bank at E1 (others unchanged); Option 2: distributed (1030.2 last sentence), total >= 100 %
    o1_pairs = wc["main_pairs"]
    o1_total = (n_open - 1 + o1_pairs) * dw
    o2_total_pairs = wc["total_pairs"]
    o2_add = o2_total_pairs - n_open
    st_prov = eg["stair_count"] * eg["stair_clear_in"]
    up = {r["side"]: r["upper"] for r in h["rows"]}
    corner = max(up["N"] / 2 + up["E"] / 2, up["S"] / 2 + up["E"] / 2)
    lp = h["loop"]
    fx1, fx2 = lp["fx1"], lp["fx2"]
    fxw = tf.fixtures(seats_l + wc["floor"])
    return dict(code=code, p2=p2, h=h, seats_l=seats_l, seats_u=seats_u, r1=r1, r2=r2, l1_fixed=l1_fixed, cases=cases,
                loop_sf=loop_sf, sens=sens, l2_base=l2_base, l2_worst=l2_worst, prov_total=prov_total, n_open=n_open,
                others=others, stair_door_req=stair_door_req, wc=wc, o1_pairs=o1_pairs, o1_total=o1_total,
                o2_total_pairs=o2_total_pairs, o2_add=o2_add, st_prov=st_prov, corner=corner, fx1=fx1, fx2=fx2, fxw=fxw,
                dw=dw, df=df, sf=sf_, fac=fac)


def n0(v):
    return f"{v:,.0f}"


def n1(v):
    return f"{v:,.1f}"


class Col:
    """Column cursor: section heads, wrapped paragraphs, simple tables. k scales every text size and row height."""

    def __init__(self, sh, x, y, w, k=1.0):
        self.sh, self.x, self.y, self.w, self.k = sh, x, y, w, k

    def head(self, s, size=7.4):
        size *= self.k
        self.y -= 0.17 * self.k + 0.04
        self.sh.text(self.x, self.y, s, size=size, bold=True)
        self.sh.line(self.x, self.y - 0.045, self.x + self.w, self.y - 0.045, lw=0.6)
        self.y -= 0.06

    def para(self, s, size=5.7, bold=False, bullet=None, color=None, pad=0.3):
        from titleblock import wrap, pitch
        size *= self.k
        ind = 0.1 if bullet else 0.0
        for i, ln in enumerate(wrap(s, self.w - pad - ind, size, bold)):
            self.y -= pitch(size)
            if bullet and i == 0:
                self.sh.text(self.x, self.y, bullet, size=size, bold=bold, color=color)
            self.sh.text(self.x + ind, self.y, ln, size=size, bold=bold, color=color)
        self.y -= 0.25 * pitch(size)

    def table(self, cols, rows, size=5.5, rh=0.128, head=True):
        """cols: [(title, x_offset, align[, wrap_width])]; rows: list of (cells, style) with style dict(bold, color, rule, colors)."""
        from titleblock import wrap
        sh = self.sh
        size, rh = size * self.k, rh * self.k
        if head:
            self.y -= rh
            for c in cols:
                sh.text(self.x + c[1], self.y, c[0], size=size, bold=True, align=c[2], layer=L_TAB)
            sh.line(self.x, self.y - 0.035, self.x + self.w, self.y - 0.035, lw=0.5, layer=L_TAB)
            self.y -= 0.02
        for cells, st in rows:
            st = st or {}
            if st.get("rule"):
                sh.line(self.x, self.y - 0.025, self.x + self.w, self.y - 0.025, lw=0.35, layer=L_TAB)
                self.y -= 0.01
            cc = st.get("colors") or {}
            lines = []
            for c, v in zip(cols, cells):
                v = "" if v is None else str(v)
                lines.append(wrap(v, c[3], size, st.get("bold", False)) if (len(c) > 3 and v) else [v])
            n = max(len(x) for x in lines)
            for j in range(n):
                self.y -= rh if j == 0 else rh * 0.86
                for k, (c, ls) in enumerate(zip(cols, lines)):
                    if j < len(ls) and ls[j]:
                        sh.text(self.x + c[1], self.y, ls[j], size=size, bold=st.get("bold", False), align=c[2], layer=L_TAB,
                                color=cc.get(k, st.get("color")))
            if n > 1:
                self.y -= 0.02
        self.y -= 0.05


def build(d):
    code, p2, meta2 = d["code"], d["p2"], d["p2"]["meta"]
    cm = code["meta"]
    sh = Sheet(W, H)
    body_bottom = add_titleblock(sh, {
        "project": f"{meta2['project']}\n{meta2['arena_name']} · {meta2['location']}",
        "phase": "PHASE 2",
        "title": "CODE ANALYSIS\nSCHEMATIC",
        "scale": cm["scale"],
        "date": meta2["sheet_date"],
        "revision": cm["revision"],
        "drawn_by": meta2["drawn_by"],
        "sheet_no": SHEET_NO,
        "stamp": meta2["stamp"],
    }, margin=M, tb_h=0.95, stamp_h=0.40)
    top = H - M - 0.12
    sh.text(0.75, top - 0.2, "CODE ANALYSIS — SCHEMATIC (REV A) · P2-A-101 / A-102 REV F · P2-G-003 REV I", size=11.5, bold=True)
    sh.text(0.75, top - 0.40, cm["disclaimer"], size=6.6)
    y0 = top - 0.45
    cw = 5.05
    K = 1.19
    c1, c2, c3 = Col(sh, 0.75, y0, cw, K), Col(sh, 6.05, y0, cw, K), Col(sh, 11.35, y0, 4.95, K)
    for xx in (5.92, 11.22):
        sh.line(xx, y0 - 0.05, xx, body_bottom + 0.1, lw=0.4)

    # ---------------- column 1: code basis, occupancy, construction, fire protection
    c1.head("1  CODE BASIS + EDITIONS (R-006)")
    c1.table([("CODE", 0, "left", 0.85), ("DESIGNED TO", 0.95, "left", 1.75), ("COUNTY 2018 / STATE", 2.8, "left", 2.2)],
             [([r["code"], r["designed"], r["county"]], None) for r in code["editions"]["rows"]], size=5.0, rh=0.122)
    c1.para("STATUS of every edition line: 2021 ASSUMED (Shane) — verify with AHJ (D-008 OPEN). Factors read in the 2021 text only; "
            "2018 / NFPA 101 equivalence NOT verified (R-006.2).", size=5.6, bold=True, color=RED)
    c1.para(code["editions"]["ahj"], size=5.6)
    c1.head("2  OCCUPANCY (R-007.1)")
    c1.table([("SPACE", 0, "left", 1.75), ("GROUP", 1.85, "left", 0.7), ("CITE (IBC 2021) / CONFIDENCE", 2.6, "left", 2.4)],
             [([r["space"], r["group"], r["cite"]], None) for r in code["occupancy"]["rows"]], size=5.4)
    c1.para(code["occupancy"]["mixed"], size=5.6)
    c1.head("3  CONSTRUCTION TYPE")
    c1.para(code["construction"]["note"] + f" Drawn size (D-057, P2-A-101/102 Rev F): L1 {n1(d['h']['drawn']['L1'])} / L2 "
            f"{n1(d['h']['drawn']['L2'])} / TOTAL {n1(d['h']['drawn']['G'])} GSF (R-021 method).", size=5.6)
    c1.head("4  FIRE PROTECTION + SYSTEMS (ASSUMED)")
    for it in code["fire_protection"]["items"]:
        c1.para(it, size=5.6, bullet="•")

    c1.head("5  TRAVEL DISTANCE + COMMON PATH")
    for it in code["travel"]["items"]:
        c1.para(it, size=5.6, bullet="•")

    # ---------------- column 2: occupant load
    fac = d["fac"]
    fl = lambda f: f"{fac[f]['sf']} {fac[f]['kind']}"
    c2.head("6  OCCUPANT LOAD BY SPACE (IBC 2021 T1004.5 / 1004.6; R-007.2)")
    cols = [("SPACE (areas drawn, P2-A-101/102 Rev F)", 0, "left", 2.2), ("AREA SF", 2.75, "right"), ("FACTOR", 3.55, "right"),
            ("LOAD", cw - 0.05, "right")]
    rows = [(["LEVEL 1", "", "", ""], dict(bold=True)),
            ([code["level_1"]["seats"]["label"], "", "seats", n0(d["seats_l"])], None)]
    rows += [([r["label"], n0(r["area"]), fl(r["factor"]), n0(r["load"])], None) for r in d["r1"]]
    rows += [(["L1 without the event floor", "", "", n0(d["l1_fixed"])], dict(bold=True, rule=True))]
    ef = code["event_floor"]
    sp = next(c for c in d["cases"] if c["id"] == "sports")
    rows += [([f"Event floor — base case (sports)", n0(ef["area_sf"]), fl(sp["factor"]), n0(sp["floor"])], None),
             ([f"L1 TOTAL, base case (worst: table 7)", "", "", n0(sp["l1"])], dict(bold=True, rule=True)),
             (["LEVEL 2", "", "", ""], dict(bold=True)),
             ([code["level_2"]["seats"]["label"], "", "seats", n0(d["seats_u"])], None)]
    rows += [([r["label"], n0(r["area"]), fl(r["factor"]), n0(r["load"])], None) for r in d["r2"]]
    rows += [(["L2 BASE", "", "", n0(d["l2_base"])], dict(bold=True, rule=True))]
    rows += [([s["label"], n0(s["area"]), fl(s["factor"]), n0(s["load"])], None) for s in d["sens"]]
    rows += [(["L2 WORST CASE (design, D-052)", "", "", n0(d["l2_worst"])], dict(bold=True, rule=True))]
    c2.table(cols, rows, size=5.5, rh=0.125)
    c2.para(code["level_1"]["not_added"] + " Telescopic tier: " + code["level_1"]["seats"]["basis"] + ". Higher posted load by approval up "
            "to 1 per 7 SF with a seating diagram (1004.5.1). Event floor area " + ef["area_basis"] + ".", size=5.5)
    c2.head("7  EVENT FLOOR CASES (D-054 OPEN) — DESIGN TO THE WORST CASE")
    cols = [("CASE (T1004.5)", 0, "left", 1.8), ("FLOOR", 2.25, "right"), ("L1 TOTAL", 3.05, "right"), ("L2", 3.8, "right"),
            ("BUILDING", cw - 0.05, "right")]
    rows = [([c["label"], n0(c["floor"]), n0(c["l1"]), n0(d["l2_worst"]), n0(c["total"])],
             dict(bold=c["id"] == ef["design_case"], color=RED if c["id"] == ef["design_case"] else None)) for c in d["cases"]]
    c2.table(cols, rows, size=5.5)
    c2.para(f"L2 shown at its worst case ({n0(d['l2_worst'])}, design basis, D-052) in every column. The building official assigns the floor load "
            f"from the intended uses (1004.5); Shane decides the uses (D-054).", size=5.5)
    c2.head("8  PLUMBING FIXTURE BASIS (R-009)")
    c2.para(code["plumbing"]["basis"], size=5.5)
    fx1, fx2, fxw = d["fx1"], d["fx2"], d["fxw"]
    cols = [("LEVEL (FIXTURE LOAD)", 0, "left", 1.7), ("WC M", 2.1, "right"), ("WC F", 2.65, "right"), ("LAV M", 3.2, "right"),
            ("LAV F", 3.75, "right"), ("DF", 4.25, "right"), ("SS", cw - 0.05, "right")]
    fr = lambda lab, f: [lab, f["wc_m"], f["wc_f"], f["lav_m"], f["lav_f"], f["df"], f["service_sink"]]
    rows = [(fr(f"L1 (G-003 Rev I: {n0(fx1['load'])})", fx1), None), (fr(f"L2 (G-003 Rev I: {n0(fx2['load'])})", fx2), None),
            (fr(f"L1 if the floor is standing ({n0(fxw['load'])})", fxw), dict(color=RED, rule=True))]
    c2.table(cols, rows, size=5.5)
    c2.para(f"G-003 Rev I counts the floor at 328 (16,400 SF ÷ 50). The standing case would need {fxw['wc_m'] - fx1['wc_m']} more men's "
            f"and {fxw['wc_f'] - fx1['wc_f']} more women's WC on L1 than drawn — not drawn; follows D-054.", size=5.5, color=RED)

    # ---------------- column 3: egress checks, findings, options
    wc, dw, df = d["wc"], d["dw"], d["df"]
    eg = code["egress"]
    c3.head("9  LEVEL 1 EXIT CAPACITY (doors 0.15 in/occ.)")
    c3.para(f"{eg['door_basis']}. {eg['door_basis_width']}. Provided: E1 + X1–X10 = {d['n_open']} openings x {dw} in = "
            f"{n0(d['prov_total'])} in. Stair discharge doors X4 / X6 / X9 / X10 carry the L2 worst case first "
            f"({n0(d['l2_worst'])} ÷ 4 x 0.15 = {n1(d['stair_door_req'])} in each).", size=5.4)
    cs = d["cases"]
    cols = [("CHECK (in)", 0, "left", 1.6)] + [(n0(c["floor"]), 2.0 + i * 0.72, "right") for i, c in enumerate(cs)] + [("PROV.", 4.9, "right")]

    def row(lab, key, pk, prov):
        cells = [lab] + [n1(c[key]) for c in cs] + [n1(prov) if prov is not None else ""]
        return cells, dict(colors={i + 1: (GRN if c[pk] else RED) for i, c in enumerate(cs)})
    rows = [row("Total at grade (L1 + L2)", "req_total", "pass_total", d["prov_total"]),
            row("Main exit E1 >= 1/2 (1030.2)", "main_req", "pass_main", dw),
            ([ "Other L1 exits >= 1/2 L1 (1030.3)"] + [n1(c["other_req"]) for c in cs] + [n1(cs[0]["other_prov"])],
             dict(colors={i + 1: (GRN if c["pass_other"] else RED) for i, c in enumerate(cs)})),
            row("Lose one opening >= 50% (1005.5)", "lose_req", "pass_lose", cs[0]["lose_one"])]
    c3.table(cols, rows, size=5.3, rh=0.125)
    c3.para("Columns = event-floor load (D-054 cases). Green = enough as calculated; red = SHORT. 4 exits needed per story over 1,000 "
            f"(T1006.3.3): {d['n_open']} on L1.", size=5.3)
    c3.head("10  FINDING — L1 DOORS vs THE WORST CASE")
    st_short_main = wc["main_req"] - dw
    st_short_tot = wc["req_total"] - d["prov_total"]
    c3.para(f"SHORT at the worst case (standing floor, {n0(wc['floor'])}; building {n0(wc['total'])}): main exit E1 needs "
            f"{n1(wc['main_req'])} in = {wc['main_pairs']} pairs vs 1 pair ({dw} in): −{n1(st_short_main)} in. Total door capacity needs "
            f"{n1(wc['req_total'])} in vs {n0(d['prov_total'])} in: −{n1(st_short_tot)} in (≈ {wc['total_pairs'] - d['n_open']} pairs). "
            f"Other L1 exits pass (1030.3). Even the sports case needs E1 >= {n1(cs[0]['main_req'])} in ({cs[0]['main_pairs']} pairs).",
            size=5.6, bold=True, color=RED)
    c3.para(f"OPTION 1 — Main-exit door bank at E1 (keeps the single controlled entry, D-033): {d['o1_pairs']} pairs = "
            f"{n0(d['o1_pairs'] * dw)} in across the lobby's south wall (58 ft of frontage; first aid / vestibule edges move — "
            f"architect). Total then {n0(d['o1_total'])} in >= {n1(wc['req_total'])} in. Security lanes stay out of the egress width "
            "(1003.6, 1010.5).", size=5.6, bullet="•")
    c3.para(f"OPTION 2 — Multiple main exits around the perimeter (1030.2 / 1030.3 last sentences; total >= 100%): "
            f"{d['o2_total_pairs']} pairs total = {n0(d['o2_total_pairs'] * dw)} in, i.e. add {d['o2_add']} pairs (e.g. widen E1 and "
            "X5 / X7 / X8 to double pairs). Needs the AHJ to accept that E1 is not the one well-defined main exit; more exterior "
            "doors to alarm and staff.", size=5.6, bullet="•")
    c3.para("No sheet redrawn: door widths are set by the architect once D-054 is answered.", size=5.6)
    c3.head("11  LEVEL 2 EGRESS (R-018, D-052)")
    st = d["st_prov"]
    c3.para(f"{eg['stair_basis']}: 4 stairs x {eg['stair_clear_in']} in = {st} in. Base {n0(d['l2_base'])} x 0.2 = "
            f"{n1(d['l2_base'] * d['sf'])} in; worst {n0(d['l2_worst'])} x 0.2 = {n1(d['l2_worst'] * d['sf'])} in → spare "
            f"{n1(st - d['l2_worst'] * d['sf'])} in (passes as calculated). Lose one stair: {st - eg['stair_clear_in']} in >= "
            f"{n1(0.5 * d['l2_worst'] * d['sf'])} in (1005.5). 4 exits (T1006.3.3). Loop 84 in vs {n1(d['corner'] * 0.2)} in at the "
            "worst corner (R-018.3 method, Rev F seat split). Intermediate handrails on 76 in stairs (1014.9; architect to confirm).",
            size=5.6)
    c3.head("12  OPEN ITEMS FOR THE ARCHITECT / AHJ")
    for it in code["open_items"]["items"]:
        c3.para(it, size=5.6, bullet="•")
    return sh, body_bottom, [c1, c2, c3]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", choices=["A"], default="A")
    ap.add_argument("--png")
    ap.add_argument("--out-dir")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--print", action="store_true", help="print the numbers and exit")
    a = ap.parse_args()
    d = compute()
    if a.print:
        for k in ("seats_l", "seats_u", "l1_fixed", "loop_sf", "l2_base", "l2_worst", "prov_total", "stair_door_req", "o1_pairs",
                  "o1_total", "o2_total_pairs", "o2_add", "corner"):
            print(k, d[k])
        for r in d["r1"] + d["r2"] + d["sens"]:
            print(r)
        for c in d["cases"]:
            print({k: (round(v, 1) if isinstance(v, float) else v) for k, v in c.items()})
        print("fx", d["fx1"], d["fx2"], d["fxw"])
        return
    p2 = d["p2"]
    rv = p2["sheets"][SHEET_NO]["revisions"][a.rev]
    if a.out_dir:
        pdf, dxf = (Path(a.out_dir) / f"{rv['file']}.{e}" for e in ("pdf", "dxf"))
    else:
        pdf = BP / "phase2" / "out" / "pdf" / f"{rv['file']}.pdf"
        dxf = BP / "phase2" / "out" / "dxf" / f"{rv['file']}.dxf"
        if rv.get("frozen") and (pdf.exists() or dxf.exists()) and not a.force:
            sys.exit("Revision is FROZEN; use --out-dir to regenerate for checking.")
    sh, body_bottom, cols = build(d)
    mg = [c.y - body_bottom - 0.05 for c in cols]
    print("column margins (in): " + ", ".join(f"{m:.2f}" for m in mg))
    if min(mg) < 0:
        raise SystemExit(f"LAYOUT OVERFLOW: column {mg.index(min(mg)) + 1} runs {-min(mg):.2f} in into the stamp band")
    pdf.parent.mkdir(parents=True, exist_ok=True)
    dxf.parent.mkdir(parents=True, exist_ok=True)
    sh.render_pdf(pdf, title=f"{SHEET_NO} Rev {a.rev} {p2['sheets'][SHEET_NO]['title']}", png_path=a.png)
    sh.render_dxf(dxf)
    print(f"wrote {pdf}\nwrote {dxf}" + (f"\nwrote {a.png}" if a.png else ""))


if __name__ == "__main__":
    main()
