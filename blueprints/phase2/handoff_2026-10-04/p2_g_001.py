"""P2-G-001 COVER SHEET — Phase 2 Schematic Set Rev B. Tabloid, text + tables + the official mark.

Rev A (2026-10-04 5:03 PM CT, Shane "go, keep core 2 east"; Claude Code covering for KEYSTONE, BACKLOG P2-T-012):
project block, sheet index with the current revision of every sheet and its approval state (params/phase2.yaml),
size per D-057 (drawn: plan Rev I / A-102 Rev F, vs Rev H and vs Set Rev A = plan Rev D), decisions summary,
open items, general notes. Data: params/phase2_cover.yaml, params/phase2.yaml, params/phase2_plan_rev_{d,h,i}.yaml.
Rev B (2026-10-04): index carries P2-A-103 Rev C; set name Rev C (params/phase2_cover_rev_b.yaml).
Usage (from the repo root):
  python blueprints/phase2/src/p2_g_001.py [--png PATH] [--out-dir DIR]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

BP = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BP / "shared"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from titleblock import Sheet, add_titleblock  # noqa: E402
import p2_testfit as tf  # noqa: E402
from p2_g_002 import Col, n0  # noqa: E402

W, H, M = 17.0, 11.0, 0.5
SHEET_NO = "P2-G-001"
RED, GRN, GRY = "#CC0000", "#1E7B34", "#555555"


def rd(n):
    return yaml.safe_load((BP / "params" / n).read_text(encoding="utf-8"))


def build(cv, p2):
    meta2, cm = p2["meta"], cv["meta"]
    sh = Sheet(W, H)
    body_bottom = add_titleblock(sh, {
        "project": f"{meta2['project']}\n{meta2['arena_name']} · {meta2['location']}",
        "phase": "PHASE 2",
        "title": "COVER SHEET\nSHEET INDEX + DECISIONS",
        "scale": "NTS",
        "date": meta2["sheet_date"],
        "revision": cm["revision"],
        "drawn_by": cm["drawn_by"],
        "sheet_no": SHEET_NO,
        "stamp": meta2["stamp"],
    }, margin=M, tb_h=0.95, stamp_h=0.40)
    top = H - M - 0.12

    # ---------------- column 1: identity
    x1, w1 = 0.75, 4.55
    mk = cv["mark"]
    sh.mark("THA_MARK", BP / mk["file"], x1 + w1 / 2, top - 1.55, mk["diameter_in"], mk["fill"])
    y = top - 3.05
    for s, size, bold, color in [(meta2["arena_name"].upper(), 20, True, RED),
                                 (meta2["project"], 11, True, None),
                                 (meta2["location"], 8.5, False, None)]:
        sh.text(x1 + w1 / 2, y, s, size=size, bold=bold, align="center", color=color)
        y -= 0.30 if size > 15 else 0.22
    y -= 0.12
    sh.line(x1, y, x1 + w1, y, lw=1.2)
    y -= 0.32
    sh.text(x1 + w1 / 2, y, cm["set_name"], size=12.5, bold=True, align="center")
    y -= 0.22
    sh.text(x1 + w1 / 2, y, cm["set_sub"], size=8, align="center")
    c1 = Col(sh, x1, y - 0.05, w1, 1.12)
    c1.head("PROJECT")
    c1.table([("ITEM", 0, "left", 1.15), ("", 1.25, "left", 3.25)],
             [([r["k"], r["v"]], None) for r in cv["project_rows"]], size=5.6, rh=0.13, head=False)
    c1.head("GENERAL NOTES")
    for it in cv["general_notes"]:
        c1.para(it, size=5.5, bullet="•")
    sh.line(5.5, top - 0.05, 5.5, body_bottom + 0.1, lw=0.4)
    sh.line(11.0, top - 0.05, 11.0, body_bottom + 0.1, lw=0.4)

    # ---------------- column 2: sheet index + size
    c2 = Col(sh, 5.7, top + 0.05, 5.1, 1.12)
    c2.head(cm.get("index_head", "SHEET INDEX — PHASE 2 SCHEMATIC SET REV B (sheet-number order)"))
    rows = []
    for e in cv["index"]:
        sid, rv = e["sheet"], e["revision"]
        reg = p2["sheets"].get(sid, {}).get("revisions", {})
        appr = [r for r, x in reg.items() if x.get("approved")]
        if e.get("status"):
            st = e["status"]
        elif reg.get(rv, {}).get("approved"):
            st = "APPROVED"
        else:
            st = "IN REVIEW" + (f" (last approved Rev {appr[-1]})" if appr else " (no rev approved yet)")
        rows.append(([sid, e["title"], rv, st], dict(bold=sid == SHEET_NO)))
    c2.table([("SHEET", 0, "left"), ("TITLE", 0.72, "left", 2.45), ("REV", 3.25, "left"), ("STATUS", 3.55, "left", 1.55)],
             rows, size=5.6, rh=0.135)
    c2.para(cv["index_note"], size=5.4, color=GRY)

    d, h, i = (tf.drawn_size(rd(f"phase2_plan_rev_{r}.yaml")) for r in ("d", "h", "i"))
    c2.head("SIZE — D-057 (drawn, R-021 method; no SF cap, D-056)")
    sg = lambda v: f"{v:+,.0f}" if round(v) else "0"
    c2.table([("", 0, "left", 1.3), (cm.get("size_col", "SET REV B"), 1.95, "right"), ("REV H", 2.65, "right"), ("CHANGE", 3.35, "right"),
              ("SET REV A", 4.25, "right"), ("CHANGE", 5.05, "right")],
             [([lab, n0(i[k]), n0(h[k]), sg(i[k] - h[k]), n0(d[k]), sg(i[k] - d[k])], dict(bold=k == "G", rule=k == "G"))
              for lab, k in (("Level 1 footprint", "L1"), ("Level 2 area", "L2"), ("TOTAL GSF", "G"))], size=5.7, rh=0.14)
    c2.para(cv["size_note"], size=5.4)
    c2.head("KEY FACTS (as drawn)")
    for it in cv["facts"]:
        c2.para(it, size=5.5, bullet="•")

    # ---------------- column 3: decisions + open items
    c3 = Col(sh, 11.2, top + 0.05, 5.1, 1.12)
    c3.head("DECISIONS SUMMARY (DECIDED — Shane; full log: DECISIONS.md)")
    c3.table([("D-###", 0, "left", 0.75), ("DECISION", 0.82, "left", 4.25)],
             [([r["d"], r["t"]], None) for r in cv["decisions"]], size=5.35, rh=0.122)
    c3.head("OPEN — OWNER / ARCHITECT / ENGINEER")
    for r in cv["open_items"]:
        c3.para(f"{r['d']}: {r['t']}", size=5.4, bullet="•", color=RED if r.get("owner") else None)
    c3.para(cv["open_note"], size=5.2, color=GRY)
    return sh, body_bottom, [c1, c2, c3]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", choices=["A", "B"], default="B")
    ap.add_argument("--png")
    ap.add_argument("--out-dir")
    a = ap.parse_args()
    cv, p2 = rd({"A": "phase2_cover.yaml", "B": "phase2_cover_rev_b.yaml"}[a.rev]), rd("phase2.yaml")
    rv = cv["meta"]["revision"]
    out = Path(a.out_dir) if a.out_dir else BP / "phase2" / "out"
    pdf = (out if a.out_dir else out / "pdf") / f"{SHEET_NO}_Rev{rv}.pdf"
    dxf = (out if a.out_dir else out / "dxf") / f"{SHEET_NO}_Rev{rv}.dxf"
    sh, body_bottom, cols = build(cv, p2)
    mg = [c.y - body_bottom - 0.05 for c in cols]
    print("column margins (in): " + ", ".join(f"{m:.2f}" for m in mg))
    if min(mg) < 0:
        raise SystemExit(f"LAYOUT OVERFLOW: column {mg.index(min(mg)) + 1} runs {-min(mg):.2f} in into the stamp band")
    pdf.parent.mkdir(parents=True, exist_ok=True)
    dxf.parent.mkdir(parents=True, exist_ok=True)
    sh.render_pdf(pdf, title=f"{SHEET_NO} Rev {rv} COVER SHEET", png_path=a.png)
    sh.render_dxf(dxf)
    print(f"wrote {pdf}\nwrote {dxf}" + (f"\nwrote {a.png}" if a.png else ""))


if __name__ == "__main__":
    main()
