"""P1-G-002 Rev A — Phase 1 cost sheet (wrestling room mats + wall pads), one page, PRELIMINARY. Shane 2026-10-09 4:49 PM CT.

Low / Mid / High from published list prices (params/phase1_cost.yaml, each with a URL; research R-026). Not a quote or bid.
Run from the repo root:
  /workspace/.venv-keystone/bin/python blueprints/phase1/src/p1_g_002.py --rev {A,B} [--out-dir DIR]  (B = A + supersede note)
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import yaml

BP = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BP / "shared"))
from titleblock import Sheet, add_titleblock  # noqa: E402
from palette import SCHOOL_RED, INK_MUTED  # noqa: E402

SHEET_NO = "P1-G-002"
W, H, M = 17.0, 11.0, 0.5
B = ("low", "mid", "high")


def rd(n):
    return yaml.safe_load((BP / "params" / n).read_text(encoding="utf-8"))


def money(v):
    return f"${v:,.0f}"


def compute(c):
    q = c["quantities"]
    assert q["pad_lf"] == q["perimeter_lf"] - q["doors"] * q["door_width_ft"]
    assert q["pad_panels"] == q["pad_lf"] // 2 and q["tape_rolls"] == math.ceil(q["tape_seam_lf"] / q["tape_roll_lf"])
    mp = c["mat_prices"]
    psf = {k: mp[c["mat_bands"][k]]["price"] / mp[c["mat_bands"][k]]["sf"] for k in B}
    pad = {k: next(p for p in c["pad_prices"] if p["band"] == k)["price"] for k in B}
    rows = [
        ("Wrestling mat, wall to wall", f"{q['mat_sf']:,} SF", {k: psf[k] * q["mat_sf"] for k in B}, {k: f"${psf[k]:.2f}/SF" for k in B}),
        ("Mat tape (3 in x 60 yd rolls)", f"{q['tape_rolls']} rolls", {k: c["tape_per_roll"][k] * q["tape_rolls"] for k in B}, {k: f"${c['tape_per_roll'][k]:.2f}/roll" for k in B}),
        ("Mat freight", "1 lot", {k: float(c["mat_freight"][k]) for k in B}, {k: "" for k in B}),
        ("Wall pads 2 x 6 ft, NFPA 286 / Class A", f"{q['pad_panels']} panels ({q['pad_lf']} LF)", {k: pad[k] * q["pad_panels"] for k in B}, {k: f"${pad[k]:.2f}/panel" for k in B}),
        ("Pad mounting hardware (Z-clip kits)", f"{q['pad_panels']} panels", {k: c["pad_hardware_per_panel"][k] * q["pad_panels"] for k in B}, {k: f"${c['pad_hardware_per_panel'][k]:.2f}/panel" for k in B}),
        ("LED 4 ft wrap fixtures (count ASSUMED)", "{low}-{high} fixtures".format(**c["led"]["count"]), {k: c["led"]["price"][k] * c["led"]["count"][k] for k in B},
         {k: f"{c['led']['count'][k]} x ${c['led']['price'][k]:.2f}" for k in B}),
    ]
    sub = {k: sum(r[2][k] for r in rows) for k in B}
    con = {k: sub[k] * c["contingency_pct"] / 100 for k in B}
    tot = {k: sub[k] + con[k] for k in B}
    return rows, sub, con, tot, psf, pad


def build(rev):
    p1, c = rd("phase1.yaml"), rd("phase1_cost.yaml")
    meta, site = p1["meta"], p1["site"]
    q = c["quantities"]
    rows, sub, con, tot, psf, pad = compute(c)
    sh = Sheet(W, H)
    bb = add_titleblock(sh, {
        "project": f"{meta['project']}\n{site['location']}",
        "phase": f"PHASE {meta['phase']}\n{meta['type'].upper()}",
        "title": "COST SHEET\nMATS, PADS, LED",
        "sheet_no": SHEET_NO, "scale": "NTS", "date": meta["sheet_date"], "revision": rev,
        "drawn_by": meta["drawn_by"], "stamp": meta["stamp"],
    }, margin=M, tb_h=0.95, stamp_h=0.40)
    x0, top = 0.85, H - M - 0.45
    sh.text(x0, top, "PHASE 1 WRESTLING ROOM — MATERIALS COST (mats, wall pads, LED)", size=18, bold=True)
    sh.text(x0, top - 0.3, f"Room cleared: 100 % of the {q['mat_sf']:,} SF floor (55' x 45') gets mat. Pads 6 ft high on the whole perimeter less {q['doors']} doors: "
            f"{q['perimeter_lf']} - {q['doors']} x {q['door_width_ft']} ft = {q['pad_lf']} LF = {q['pad_panels']} panels.", size=10.5)
    if rev == "B":
        sh.text(x0 + 10.4, top - 0.5 + 0.25 * 2, "Supersedes Rev A (pre-scope change, included install)", size=10.5, color="#C00000")
    sh.text(x0, top - 0.5, "Materials only: the team clears, relocates and installs ($0, by owner). Water / restrooms out of scope. List prices 2026-10-09; not a quote. Tax, pad freight, custom sizes extra.", size=10.5, color=INK_MUTED)
    # table
    cx = [x0, x0 + 3.7, x0 + 5.6, x0 + 7.15, x0 + 8.7, x0 + 10.25]
    y = top - 0.95
    for t_, xx, al in (("ITEM", cx[0], "left"), ("QTY", cx[1], "left"), ("LOW", cx[3], "right"), ("MID", cx[4], "right"), ("HIGH", cx[5], "right")):
        sh.text(xx, y, t_, size=11, bold=True, align=al)
    sh.line(x0, y - 0.07, cx[5] + 0.05, y - 0.07, lw=0.8)
    for name, qty, val, unit in rows:
        y -= 0.32
        sh.text(cx[0], y, name, size=10.5)
        sh.text(cx[1], y, qty, size=10)
        for k, xx in zip(B, cx[3:]):
            sh.text(xx, y, money(val[k]), size=10.5, align="right")
            if unit[k]:
                sh.text(xx, y - 0.14, unit[k], size=7.5, align="right", color=INK_MUTED)
    y -= 0.36
    sh.line(x0, y + 0.2, cx[5] + 0.05, y + 0.2, lw=0.5)
    for lab, d, bold in (("Subtotal, materials", sub, True), (f"Contingency {c['contingency_pct']} %", con, False), ("TOTAL, materials", tot, True)):
        sh.text(cx[0], y, lab, size=11.5 if bold else 10.5, bold=bold)
        for k, xx in zip(B, cx[3:]):
            sh.text(xx, y, money(d[k]), size=11.5 if bold else 10.5, bold=bold, align="right", color=SCHOOL_RED if lab.startswith("TOTAL") else None)
        y -= 0.3
    sh.line(x0, y + 0.42, cx[5] + 0.05, y + 0.42, lw=0.8)
    y -= 0.05
    sh.text(x0, y, "BY OWNER / NOTES — NOT IN THE TOTAL", size=12, bold=True)
    for t in c["tbd_lines"]:
        y -= 0.25
        sh.text(x0, y, f"{t['id']}  {t['text']}: {t['value']} ({t['note']})", size=9.5)
    y -= 0.32
    sh.text(x0, y, "USED / TRADE-IN", size=12, bold=True)
    for u in c["used_options"]:
        y -= 0.25
        pr = money(u["price"]) if u["price"] else "call for price"
        sh.text(x0, y, f"{u['name']}: {pr}", size=9.5)
    y -= 0.3
    sh.para(x0, y, 11.0, "PROCUREMENT: " + c["procurement_note"], size=9.5, bold=False)
    # sources column
    sx, sy = 12.25, top - 0.95
    sh.text(sx, sy, "SOURCES (list prices, 2026-10-09)", size=11, bold=True)
    sy -= 0.08
    srcs = [(m["brand"], f"${m['price']:,.2f} / {m['sf']:,} SF" if m["price"] else m["note"], m["url"] or "") for m in c["mat_prices"]]
    srcs += [(p["name"], f"${p['price']:,.2f} / panel", p["url"]) for p in c["pad_prices"]]
    srcs += [(i_["name"], f"${c['led']['price'][i_['band']]:.2f} each", i_["url"]) for i_ in c["led"]["items"]]
    srcs += [("Z-clip hardware", c["pad_hardware_per_panel"]["note"], c["pad_hardware_per_panel"]["urls"][1]),
             ("Mat freight", c["mat_freight"]["note"], c["mat_freight"]["urls"][0]),
             ("Mat tape", c["tape_per_roll"]["note"], c["tape_per_roll"]["url"])]
    for i, (n, v, u) in enumerate(srcs, 1):
        sy = sh.para(sx, sy, W - M - 0.1 - sx, f"{n}: {v}", size=7.2, bullet=f"{i}.", indent=0.2)
        if u:
            for k in range(0, len(u), 78):                 # URLs have no spaces: hard-wrap
                sh.text(sx + 0.2, sy - 0.07, u[k:k + 78], size=6.0, color=INK_MUTED)
                sy -= 0.1
            sy -= 0.03
    if sy < bb + 0.1 or y < bb + 0.1:
        raise SystemExit(f"LAYOUT OVERFLOW sources {sy:.2f} body {y:.2f} vs {bb:.2f}")
    return sh, tot, sub


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", choices=["A", "B"], required=True)
    ap.add_argument("--out-dir")
    a = ap.parse_args()
    out = Path(a.out_dir) if a.out_dir else None
    pdf = (out or BP / "phase1" / "out" / "pdf") / f"P1-G-002_Rev{a.rev}.pdf"
    pdf.parent.mkdir(parents=True, exist_ok=True)
    sh, tot, sub = build(a.rev)
    sh.render_pdf(pdf, title="P1-G-002 Rev A Phase 1 cost sheet")
    print(f"wrote {pdf}; subtotal {sub}; total {tot}")


if __name__ == "__main__":
    main()
