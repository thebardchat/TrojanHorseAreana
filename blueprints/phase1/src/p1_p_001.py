"""P1-P-001 — Phase 1 plumbing / water restore scope narrative (11x17 landscape).

Rev A = SCOPE NARRATIVE ONLY for work item W2 (Priority 1):
  * existing-condition narrative (from existing.plumbing)
  * fixture inventory table (TBDs where unknown)
  * scope-of-work bullets (diagnose / restore / repair as plumber directs — NOT design)
  * BY LICENSED PLUMBER / ENGINEER OF RECORD note (R-004.3 cite in params)
  * open asks + cross-refs to frozen P1-G-001 Rev D / P1-A-101 Rev A package

Every value comes from blueprints/params/phase1.yaml. Unknowns print TBD.
No pipe sizes, no layouts, no costs. Regenerated from params — never hand-edit PDF/DXF.

Run from the repo root:
  /workspace/.venv-keystone/bin/python blueprints/phase1/src/p1_p_001.py --rev A [--png PATH]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

BP = Path(__file__).resolve().parents[2]          # blueprints/
sys.path.insert(0, str(BP / "shared"))
from titleblock import TEXT, Sheet, add_titleblock, pitch, text_width_in, wrap  # noqa: E402

SHEET_NO = "P1-P-001"
W, H = 17.0, 11.0
M = 0.5
GAP = 0.12
BODY = 9.6
HEAD = 12.0
SMALL = 8.6

OVERFLOW = []


def load():
    return yaml.safe_load((BP / "params" / "phase1.yaml").read_text(encoding="utf-8"))


def tbd(v):
    return "TBD" if v in (None, "", "TBD") else str(v)


def sentence(s: str) -> str:
    s = str(s).strip()
    if not s:
        return s
    s = s[0].upper() + s[1:]
    return s if s.endswith(".") else s + "."


def fits(name, y, bottom):
    if y < bottom + 0.03:
        OVERFLOW.append(f"{name}: {bottom + 0.03 - y:.2f} in too tall")


def box(sh: Sheet, x, y, w, h, title):
    sh.rect(x, y, w, h, lw=1.0)
    hb = 0.32
    sh.line(x, y + h - hb, x + w, y + h - hb, lw=0.8)
    hs = HEAD
    while text_width_in(title, hs, True) > w - 0.2 and hs > 8.5:
        hs -= 0.4
    sh.text(x + 0.1, y + h - hb + 0.09, title, size=hs, bold=True)
    return x + 0.12, y + h - hb - 0.04, w - 0.24


def labeled(sh: Sheet, x, y, w, label, value, size=BODY):
    lab = f"{label}:"
    lw = text_width_in(lab, size, True) + 0.33 * size / 72
    first_w = w - lw
    words = str(value).split()
    first, rest = "", []
    for i, word in enumerate(words):
        trial = f"{first} {word}".strip()
        if first and text_width_in(trial, size) > first_w:
            rest = words[i:]
            break
        first = trial
    y -= pitch(size)
    sh.text(x, y, lab, size=size, bold=True)
    sh.text(x + lw, y, first, size=size)
    if rest:
        for ln in wrap(" ".join(rest), w - 0.2, size):
            y -= pitch(size)
            sh.text(x + 0.2, y, ln, size=size)
    return y - 0.05


def callout(sh: Sheet, x, y, w, s, size=BODY + 0.4, lw=2.0):
    lines = wrap(s, w - 0.24, size, True)
    h = len(lines) * pitch(size) + 0.16
    sh.rect(x, y - h, w, h, lw=lw)
    yy = y - 0.05
    for ln in lines:
        yy -= pitch(size)
        sh.text(x + 0.12, yy + 0.02, ln, size=size, bold=True)
    return y - h - 0.08


def build(p1: dict, rev: str = "A") -> Sheet:
    meta, site = p1["meta"], p1["site"]
    wi = {w["id"]: w for w in p1["work_items"]}
    w2 = wi["W2"]
    plumb = p1["existing"]["plumbing"]
    sp = p1["sheets"][SHEET_NO]
    rv = sp["revisions"][rev]
    inv = [f for f in plumb["fixture_inventory"]["items"] if isinstance(f, dict) and "fixture" in f]
    scope = [s for s in plumb["scope_of_work"]["items"] if isinstance(s, str)]
    asks = [a for a in plumb["open_asks"]["items"] if isinstance(a, str)]
    xrefs = [x for x in plumb["cross_refs"]["items"] if isinstance(x, str)]

    sh = Sheet(W, H)
    body_bottom = add_titleblock(sh, {
        "project": f"{meta['project']}\n{site['location']}",
        "phase": f"PHASE {meta['phase']}\n{meta['type'].upper()}",
        "title": f"{sp['title']}\n{sp['subtitle']}",
        "sheet_no": SHEET_NO,
        "scale": sp["scale"],
        "date": meta["sheet_date"],
        "revision": rev,
        "drawn_by": meta["drawn_by"],
        "stamp": meta["stamp"],
    })

    # Body area above stamp
    top = H - M - 0.08
    left = M + 0.08
    right = W - M - 0.08
    usable_w = right - left
    usable_h = top - body_bottom - 0.06

    # Two-column layout: left ~58% narrative+scope+license; right fixture table + asks + xrefs
    col_gap = GAP
    left_w = usable_w * 0.56
    right_w = usable_w - left_w - col_gap
    lx = left
    rx = left + left_w + col_gap

    # --- LEFT column heights ---
    # Row stack: banner, condition, scope, license (fills left height)
    banner_h = 0.55
    cond_h = 2.55
    lic_h = 1.55
    scope_h = usable_h - banner_h - cond_h - lic_h - 3 * GAP

    y_cur = body_bottom + 0.02

    # License callout at bottom of left
    lic_y = y_cur
    x, y, w = box(sh, lx, lic_y, left_w, lic_h, "BY LICENSED PLUMBER / ENGINEER OF RECORD")
    y = sh.para(x, y, w, plumb["licensed_trade"]["note"], size=SMALL)
    y = sh.para(x, y - 0.02, w,
                f"Cite: {plumb["licensed_trade"]["cite"]}. District confirmation still needed.",
                size=SMALL - 0.4)
    fits("LICENSE", y, lic_y)

    # Scope of work above license
    scope_y = lic_y + lic_h + GAP
    x, y, w = box(sh, lx, scope_y, left_w, scope_h, "SCOPE OF WORK (NARRATIVE — NOT A DESIGN)")
    y = labeled(sh, x, y, w, "Work item", f"{w2['id']} — {w2['name']}  ·  PRIORITY {w2['priority']}")
    y = labeled(sh, x, y, w, "KEYSTONE role", sp["keystone_role"])
    y = labeled(sh, x, y, w, "Why", sentence(w2["why"]))
    y -= 0.04
    sh.text(x, y - pitch(BODY), "Plumber / EOR to:", size=BODY, bold=True)
    y -= pitch(BODY) + 0.04
    for i, bullet in enumerate(scope, 1):
        y = sh.para(x, y, w, bullet, size=BODY - 0.3, indent=0.22, bullet=f"{i}.")
    fits("SCOPE", y, scope_y)

    # Existing condition above scope
    cond_y = scope_y + scope_h + GAP
    x, y, w = box(sh, lx, cond_y, left_w, cond_h, "EXISTING CONDITION (SOURCED)")
    y = labeled(sh, x, y, w, "Status", sentence(w2["status"]))
    y = labeled(sh, x, y, w, "Detail", sentence(w2.get("status_detail", "")))
    y = labeled(sh, x, y, w, "Where", sentence(plumb["failure_location"]))
    y = labeled(sh, x, y, w, "Problem spots", sentence(plumb["leak_or_damage_spots"]))
    y = labeled(sh, x, y, w, "Cause", tbd(plumb.get("cause", "TBD")) + " — plumber to diagnose")
    y = labeled(sh, x, y, w, "Water lines", tbd(plumb["water_lines"]))
    y = labeled(sh, x, y, w, "Drain lines", tbd(plumb["drain_lines"]))
    y = labeled(sh, x, y, w, "Before 2026-10-03", sentence(plumb["condition_before_2026_10_03"]))
    fits("CONDITION", y, cond_y)

    # Banner at top of left
    ban_y = cond_y + cond_h + GAP
    sh.rect(lx, ban_y, left_w, banner_h, lw=1.8)
    ban_txt = "PRIORITY 1 — RESTORE WATER  ·  NO RUNNING WATER  ·  ALL FIXTURES OUT OF SERVICE"
    sh.text(lx + left_w / 2, ban_y + banner_h / 2 - 0.07, ban_txt, size=10.5, bold=True, align="center")

    # --- RIGHT column ---
    asks_h = 2.35
    xref_h = 1.35
    table_h = usable_h - asks_h - xref_h - 2 * GAP

    # Cross-refs at bottom right
    xref_y = y_cur
    x, y, w = box(sh, rx, xref_y, right_w, xref_h, "CROSS-REFERENCES (FROZEN — DO NOT REGENERATE)")
    for xr in xrefs:
        y = sh.para(x, y, w, xr, size=SMALL, indent=0.18, bullet="•")
    y = sh.para(x, y - 0.02, w,
                f"Package: {sp['cross_ref_package']}. This sheet adds W2 detail only.",
                size=SMALL - 0.3)
    fits("XREF", y, xref_y)

    # Open asks above xrefs
    asks_y = xref_y + xref_h + GAP
    x, y, w = box(sh, rx, asks_y, right_w, asks_h, "OPEN ITEMS / ASKS")
    for i, ask in enumerate(asks, 1):
        y = sh.para(x, y, w, ask, size=BODY - 0.4, indent=0.22, bullet=f"{i}.")
    fits("ASKS", y, asks_y)

    # Fixture inventory table at top right
    tbl_y = asks_y + asks_h + GAP
    x, y, w = box(sh, rx, tbl_y, right_w, table_h, "FIXTURE INVENTORY (ALL OUT OF SERVICE)")
    # Column headers
    cols = [
        ("#", 0.08),
        ("FIXTURE", 0.38),
        ("QTY", 0.12),
        ("STATUS", 0.22),
        ("NOTE", 0.20),
    ]
    # normalize shares
    total_share = sum(c[1] for c in cols)
    col_ws = [c[1] / total_share * w for c in cols]
    header_y = y - pitch(SMALL)
    cx = x
    for (lab, _), cw in zip(cols, col_ws):
        sh.text(cx + 0.02, header_y, lab, size=SMALL, bold=True)
        cx += cw
    y = header_y - 0.04
    sh.line(x, y, x + w, y, lw=0.6)
    y -= 0.06

    row_pt = SMALL + 0.2
    for i, row in enumerate(inv, 1):
        vals = [
            str(i),
            row["fixture"],
            tbd(row["count"]),
            row["status"],
            row.get("note") or "—",
        ]
        # measure row height (wrap note)
        note_lines = wrap(vals[4], col_ws[4] - 0.04, row_pt)
        row_h = max(pitch(row_pt), len(note_lines) * pitch(row_pt)) + 0.06
        if y - row_h < tbl_y + 0.08:
            OVERFLOW.append(f"FIXTURE TABLE: ran out of room at row {i}")
            break
        # light rule
        sh.line(x, y, x + w, y, lw=0.3)
        cy = y - pitch(row_pt)
        cx = x
        # draw cells
        sh.text(cx + 0.02, cy, vals[0], size=row_pt)
        cx += col_ws[0]
        sh.text(cx + 0.02, cy, vals[1], size=row_pt, bold=True)
        cx += col_ws[1]
        sh.text(cx + 0.02, cy, vals[2], size=row_pt)
        cx += col_ws[2]
        sh.text(cx + 0.02, cy, vals[3], size=row_pt)
        cx += col_ws[3]
        ny = cy
        for j, ln in enumerate(note_lines):
            if j:
                ny -= pitch(row_pt)
            sh.text(cx + 0.02, ny, ln, size=row_pt)
        y -= row_h

    y -= 0.06
    foot = ("Source: Shane, firsthand 2026-10-03. Sink count and line routing still TBD. "
            "No pipe sizes on this sheet.")
    y = sh.para(x, y, w, foot, size=SMALL - 0.5)
    fits("TABLE", y, tbl_y)

    return sh


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", default="A", choices=["A"], help="revision letter (default A)")
    ap.add_argument("--png", help="optional PNG preview path (outside the repo)")
    ap.add_argument("--out-dir", help="write PDF/DXF here instead of phase1/out/{pdf,dxf}")
    ap.add_argument("--force", action="store_true", help="allow overwriting a FROZEN revision in the repo")
    a = ap.parse_args()
    p1 = load()
    rv = p1["sheets"][SHEET_NO]["revisions"][a.rev]
    if a.out_dir:
        pdf = Path(a.out_dir) / f"{rv['file']}.pdf"
        dxf = Path(a.out_dir) / f"{rv['file']}.dxf"
    else:
        pdf = BP / "phase1" / "out" / "pdf" / f"{rv['file']}.pdf"
        dxf = BP / "phase1" / "out" / "dxf" / f"{rv['file']}.dxf"
        if rv.get("frozen") and (pdf.exists() or dxf.exists()) and not a.force:
            sys.exit(f"Rev {a.rev} is FROZEN; its committed files stay as issued. Use --out-dir to regenerate for checking.")
    global OVERFLOW
    OVERFLOW = []
    sh = build(p1, a.rev)
    pdf.parent.mkdir(parents=True, exist_ok=True)
    dxf.parent.mkdir(parents=True, exist_ok=True)
    sh.render_pdf(pdf, title=f"{SHEET_NO} Rev {a.rev} {p1['sheets'][SHEET_NO]['title']}", png_path=a.png)
    sh.render_dxf(dxf)
    if OVERFLOW:
        print("LAYOUT OVERFLOW:\n  " + "\n  ".join(OVERFLOW))
        sys.exit(1)
    print(f"wrote {pdf}\nwrote {dxf}" + (f"\nwrote {a.png}" if a.png else ""))


if __name__ == "__main__":
    main()
