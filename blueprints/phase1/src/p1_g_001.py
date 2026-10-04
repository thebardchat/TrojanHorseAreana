"""P1-G-001 — Phase 1 one-page scope sheet (11x17 landscape), vector PDF + DXF.

Two revisions, both from phase1.yaml `sheets.P1-G-001.revisions`:
  A = INTERNAL copy, FROZEN as issued 2026-10-03 (codes shown). Its committed
      PDF/DXF are kept as-is; regenerate only to check (use --out-dir).
  B = PRINCIPAL version (plain words, no D-/R- codes, requester line, asks list).

Every value comes from blueprints/params/phase1.yaml (plus the Phase 2 building
total from phase2.yaml, used ONLY in the "NOT INCLUDED" list). Unknowns print TBD.
Layout constants below are sheet geometry in inches, not project dimensions.

Run from the repo root:
  /workspace/.venv-keystone/bin/python blueprints/phase1/src/p1_g_001.py --rev B [--png PATH]
  /workspace/.venv-keystone/bin/python blueprints/phase1/src/p1_g_001.py --rev A --out-dir /tmp/check
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

BP = Path(__file__).resolve().parents[2]          # blueprints/
sys.path.insert(0, str(BP / "shared"))
from titleblock import TEXT, Sheet, add_titleblock, pitch, text_width_in, wrap  # noqa: E402

SHEET_NO = "P1-G-001"
W, H = 17.0, 11.0                                  # 11x17 tabloid, landscape
M = 0.5                                            # border margin
GAP = 0.12
BODY = 10.5                                        # body text size (pt)
HEAD = 13.5                                        # box heading size (pt)


def load():
    p1 = yaml.safe_load((BP / "params" / "phase1.yaml").read_text(encoding="utf-8"))
    p2 = yaml.safe_load((BP / "params" / "phase2.yaml").read_text(encoding="utf-8"))
    return p1, p2


def tbd(v):
    return "TBD" if v in (None, "", "TBD") else str(v)


def sentence(s: str) -> str:
    s = str(s).strip()
    s = s[0].upper() + s[1:]
    s = ". ".join(part[:1].upper() + part[1:] for part in s.split("; "))
    return s if s.endswith(".") else s + "."


def rng(v, unit="in", sep="–"):
    if isinstance(v, list):
        return f"{v[0]}{sep}{v[1]} {unit}"
    return f"{v} {unit}"


OVERFLOW = []


def fits(name, y, bottom):
    """Record text that runs past the bottom of its box (checked in main)."""
    if y < bottom + 0.03:
        OVERFLOW.append(f"{name}: {bottom + 0.03 - y:.2f} in too tall")


def box(sh: Sheet, x, y, w, h, title):
    """Section box with a heading bar. Returns (inner_x, y_top_of_content, inner_w)."""
    sh.rect(x, y, w, h, lw=1.0)
    hb = 0.34
    sh.line(x, y + h - hb, x + w, y + h - hb, lw=0.8)
    hs = HEAD
    while text_width_in(title, hs, True) > w - 0.2 and hs > 9:
        hs -= 0.5                                   # shrink long headings to fit the box
    sh.text(x + 0.1, y + h - hb + 0.1, title, size=hs, bold=True)
    return x + 0.12, y + h - hb - 0.04, w - 0.24


def labeled(sh: Sheet, x, y, w, label, value, size=BODY):
    """'Label: value' with a bold label and hanging wrap. Returns new y."""
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
    return y - 0.06


def callout(sh: Sheet, x, y, w, s, size=BODY + 0.5, lw=1.8):
    """Heavy-bordered note box. Returns new y below it."""
    lines = wrap(s, w - 0.24, size, True)
    h = len(lines) * pitch(size) + 0.18
    sh.rect(x, y - h, w, h, lw=lw)
    yy = y - 0.06
    for ln in lines:
        yy -= pitch(size)
        sh.text(x + 0.12, yy + 0.02, ln, size=size, bold=True)
    return y - h - 0.1


def build(p1: dict, p2: dict, rev: str = "B") -> Sheet:
    meta, site = p1["meta"], p1["site"]
    wi = {w["id"]: w for w in p1["work_items"]}
    w1, w2, w3 = wi["W1"], wi["W2"], wi["W3"]
    sp = p1["sheets"][SHEET_NO]
    rv = sp["revisions"][rev]
    codes = rv["show_codes"]
    pads, ada, gov = (p1["standards"][k] for k in ("wall_pads", "ada_single_user_restroom", "governing"))
    cites = ada["cites"]
    plumb = p1["existing"]["plumbing"]

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
    }, margin=M, tb_h=0.95, stamp_h=0.40)

    # ---- header ----------------------------------------------------------
    x0, x1 = M + GAP, W - M - GAP
    top = H - M
    sh.text(x0, top - 0.40, meta["project"].upper(), size=22, bold=True)
    sh.text(x0, top - 0.74, sp["subtitle"], size=16, bold=True)
    hx = 0.0                                        # extra header height (Rev B requester line)
    if rv["show_requester"]:
        hx = 0.26
        sh.text(x0, top - 1.0, p1["contacts"]["requester"]["sheet_line"], size=12, bold=True)
    sh.text(x1, top - 0.32, f"Location: {site['location']}", size=BODY, align="right")
    sh.text(x1, top - 0.54, f"Rooms: {site['rooms_in_scope']}", size=BODY, align="right")
    sh.text(x1, top - 0.76, f"For review by: {sp['audience']}", size=BODY, align="right")
    sh.line(x0, top - 0.88 - hx, x1, top - 0.88 - hx, lw=1.2)
    sh.text(x0, top - 1.035 - hx, "WHAT THIS PROJECT DOES — 3 WORK ITEMS", size=12, bold=True)

    # ---- row 1: the three work items ------------------------------------
    r1_top = top - 1.12 - hx
    r2_h = 2.3 - hx
    r2_y = body_bottom + GAP
    r1_y = r2_y + r2_h + GAP
    r1_h = r1_top - r1_y
    avail = x1 - x0 - 2 * GAP
    ws = [avail * f for f in (0.27, 0.215, 0.515)]
    xs = [x0, x0 + ws[0] + GAP, x0 + ws[0] + ws[1] + 2 * GAP]

    # W1
    x, y, w = box(sh, xs[0], r1_y, ws[0], r1_h, f"{w1['id']} — {w1['name'].upper()}")
    y = sh.para(x, y, w, sentence(w1["description"]), size=BODY)
    if rv["show_why"]:
        y = labeled(sh, x, y, w, "Why", w1["why"])
    y = labeled(sh, x, y, w, "Walls to pad", tbd(w1["walls"]))
    y = labeled(sh, x, y, w, "Pad height", rv.get("pad_height_label") or tbd(w1["pad_height"]))
    y = labeled(sh, x, y, w, "Pad thickness", tbd(w1["pad_thickness"]))
    y = labeled(sh, x, y, w, "Who buys or donates", f"{tbd(w1['supplied_by'])} ({w1['supplied_by_options']})")
    y = labeled(sh, x, y, w, "Door hardware", sentence(pads["doors_and_hardware"]))
    y -= 0.08
    sh.text(x, y - pitch(BODY), "FIRE SAFETY — BEFORE BUYING PADS", size=BODY, bold=True)
    y = callout(sh, x, y - pitch(BODY) - 0.08, w, w1["purchase_note"])
    basis = f"Basis: {pads['sheet_basis']}." if codes else f"Code basis: {pads['sheet_basis_plain']}."
    y = sh.para(x, y, w, basis, size=8.5)
    fits("W1", y, r1_y)

    # W2
    x, y, w = box(sh, xs[1], r1_y, ws[1], r1_h, f"{w2['id']} — {w2['name'].upper()}")
    y = sh.para(x, y, w, sentence(f"repair {plumb['condition']}"), size=BODY)
    if rv["show_why"]:
        y = labeled(sh, x, y, w, "Why", w2["why"])
    y = labeled(sh, x, y, w, "Where", tbd(w2["location"]))
    y = labeled(sh, x, y, w, "Problem spots", tbd(plumb["leak_or_damage_spots"]))
    y = labeled(sh, x, y, w, "Existing fixtures", tbd(plumb["existing_fixtures"]))
    y = labeled(sh, x, y, w, "Water / drain lines", f"{tbd(plumb['water_lines'])} / {tbd(plumb['drain_lines'])}")
    y -= 0.08
    sh.text(x, y - pitch(BODY), "WHO DESIGNS IT", size=BODY, bold=True)
    y = callout(sh, x, y - pitch(BODY) - 0.08, w, w2["design_by"], size=BODY + 1.5)
    y = sh.para(x, y, w, f"This package gives: {w2['keystone_output']}.", size=BODY)
    y = sh.para(x, y, w, f"Plumbing code: {gov['plumbing_code']} (Alabama).", size=8.5)
    fits("W2", y, r1_y)

    # W3
    x, y, w = box(sh, xs[2], r1_y, ws[2], r1_h, f"{w3['id']} — {w3['name'].upper()}")
    y = labeled(sh, x, y, w, "Why", sentence(w3["reason"]))
    y = labeled(sh, x, y, w, "Result", f"{w3['result']} ({w3['restroom_type']}).")
    y = labeled(sh, x, y, w, "Accessibility", f"{w3['ada_compliance']}.")
    y = labeled(sh, x, y, w, "Where / room sizes", f"{tbd(w3['location'])} — waiting on measurements.")
    # key-number table
    y -= 0.06
    sh.text(x, y - pitch(BODY), rv["table_heading"], size=BODY, bold=True)
    y -= pitch(BODY) + 0.08
    rows = [
        ("Turning space", f"{ada['turning_space_diameter_in']} in circle (or T-shape)", cites["turning_space_diameter_in"]),
        ("Clear space at toilet", f"{ada['wc_clearance_from_side_wall_in']} in wide × {ada['wc_clearance_from_rear_wall_in']} in deep, min", cites["wc_clearance"]),
        ("Toilet centerline to side wall", rng([ada['wc_centerline_from_side_wall_min_in'], ada['wc_centerline_from_side_wall_max_in']]), cites["wc_centerline"]),
        ("Toilet seat height", rng([ada['wc_seat_height_min_in'], ada['wc_seat_height_max_in']]), cites["wc_seat_height"]),
        ("Side grab bar", f"{ada['grab_bar_side_length_min_in']} in long min; starts ≤ {ada['grab_bar_side_max_from_rear_wall_in']} in from rear wall", cites["grab_bar_side"]),
        ("Rear grab bar", f"{ada['grab_bar_rear_length_min_in']} in long min", cites["grab_bar_rear"]),
        ("Grab bar height (top)", rng([ada['grab_bar_height_min_in'], ada['grab_bar_height_max_in']]), cites["grab_bar_height"]),
        ("Sink clear floor space", f"{ada['lav_clear_floor_space_in'][0]} × {ada['lav_clear_floor_space_in'][1]} in, forward", cites["lav_clear_floor_space_in"]),
        ("Sink rim height", f"{ada['lav_rim_height_max_in']} in max", cites["lav_rim_height_max_in"]),
        ("Mirror bottom edge", f"{ada['mirror_bottom_over_lav_max_in']} in max above floor", cites["mirror_bottom_over_lav_max_in"]),
        ("Door clear width", f"{ada['door_clear_width_min_in']} in min", cites["door_clear_width_min_in"]),
        ("Door handle height", rng(ada["door_hardware_height_in"]), cites["door_hardware_height_in"]),
        ("Door swing", f"not over toilet/sink clear space unless a {ada['lav_clear_floor_space_in'][0]} × {ada['lav_clear_floor_space_in'][1]} in space is beyond the swing", cites["door_swing_rule"]),
        ("Room sign", f"tactile, {rng(ada['tactile_sign_baseline_height_in'])} high, latch side", cites["tactile_sign_baseline_height_in"]),
    ]
    ts = 9.2
    fits("W3 text", y, r1_y)
    c0, c2 = w * 0.36, w * 0.14
    c1 = w - c0 - c2
    rh = pitch(ts) + 0.02
    # header row
    sh.line(x, y, x + w, y, lw=0.9)
    sh.text(x + 0.05, y - rh + 0.06, "Item", size=ts, bold=True)
    sh.text(x + c0 + 0.05, y - rh + 0.06, "Requirement", size=ts, bold=True)
    sh.text(x + c0 + c1 + 0.05, y - rh + 0.06, "2010 ADA §", size=ts, bold=True)
    yy = y - rh
    sh.line(x, yy, x + w, yy, lw=0.9)
    for item, req, cite in rows:
        lines = wrap(req, c1 - 0.1, ts)
        hh = rh + (len(lines) - 1) * pitch(ts)
        sh.text(x + 0.05, yy - rh + 0.06, item, size=ts)
        for i, ln in enumerate(lines):
            sh.text(x + c0 + 0.05, yy - rh + 0.06 - i * pitch(ts), ln, size=ts)
        sh.text(x + c0 + c1 + 0.05, yy - rh + 0.06, cite, size=ts)
        yy -= hh
        sh.line(x, yy, x + w, yy, lw=0.4)
    for cx in (x, x + c0, x + c0 + c1, x + w):
        sh.line(cx, y, cx, yy, lw=0.6)
    fits("W3 table", sh.para(x, yy - 0.02, w, rv["table_footnote"], size=8.5), r1_y)

    # ---- row 2: not included / who approves / waiting on / photos --------
    ws2 = [avail * f for f in ((0.19, 0.25, 0.33) if codes else (0.17, 0.335, 0.275))]
    ws2.append(avail + 2 * GAP - sum(ws2) - 3 * GAP + GAP)   # photos column
    xs2 = [x0]
    for wv in ws2[:-1]:
        xs2.append(xs2[-1] + wv + GAP)
    ws2[-1] = x1 - xs2[-1]

    x, y, w = box(sh, xs2[0], r2_y, ws2[0], r2_h, "NOT INCLUDED")
    total = p2["building"]["total_sf"]
    items = []
    for it in p1["not_in_phase1"]["items"]:
        if "Phase 2" in it and isinstance(total, int):
            it = f"{it} ({total:,} SF)"
        items.append(sentence(it).rstrip("."))
    for it in items:
        y = sh.para(x, y, w, it, size=BODY + 0.5, indent=0.2, bullet="✕")
    y = sh.para(x, y - 0.05, w, "Phase 1 is a remodel of existing rooms only.", size=BODY)
    fits("NOT INCLUDED", y, r2_y)

    x, y, w = box(sh, xs2[1], r2_y, ws2[1], r2_h, rv["approvals_heading"])
    chain = rv.get("approvals_chain") or p1["approvals"]["chain_plain"]
    for i, step in enumerate(chain, 1):
        y = sh.para(x, y, w, step, size=BODY + 0.5, indent=0.25, bullet=f"{i}.")
    note = rv.get("approvals_note")
    if rv.get("approvals_note_from") == "approvals.note_plain":
        note = p1["approvals"]["note_plain"]
    if note:
        y = sh.para(x, y - 0.03, w, note, size=BODY if codes else BODY - 1)
    sch = p1["schedule"]
    y = labeled(sh, x, y, w, "Scope confirmation expected", f"{sch['scope_confirmation_expected']} ({sch['confirming_parties']})")
    fits("WHO APPROVES", y, r2_y)

    x, y, w = box(sh, xs2[2], r2_y, ws2[2], r2_h, rv["waiting_heading"])
    for i, it in enumerate(rv["waiting_on"], 1):
        if codes:
            y = sh.para(x, y, w, it, size=BODY, indent=0.2, bullet="□")
        else:
            y = sh.para(x, y, w, it, size=BODY + 0.5, indent=0.25, bullet=f"{i}.")
    fits("WAITING ON", y, r2_y)

    x, y, w = box(sh, xs2[3], r2_y, ws2[3], r2_h, "PHOTOS")
    n = len(sp["photo_boxes"])
    bw = (w - (n - 1) * 0.12) / n
    bh = y - (r2_y + 0.42)
    for i, name in enumerate(sp["photo_boxes"]):
        bx = x + i * (bw + 0.12)
        sh.placeholder(bx, r2_y + 0.4, bw, bh - 0.04, "PHOTOS TBD", size=11)
        sh.text(bx + bw / 2, r2_y + 0.18, name, size=BODY, align="center")

    return sh


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", default="B", help="A (internal, frozen) or B (principal); default B")
    ap.add_argument("--png", help="optional PNG preview path (outside the repo)")
    ap.add_argument("--out-dir", help="write PDF/DXF here instead of phase1/out/{pdf,dxf}")
    ap.add_argument("--force", action="store_true", help="allow overwriting a FROZEN revision in the repo")
    a = ap.parse_args()
    p1, p2 = load()
    rv = p1["sheets"][SHEET_NO]["revisions"][a.rev]
    if a.out_dir:
        pdf = Path(a.out_dir) / f"{rv['file']}.pdf"
        dxf = Path(a.out_dir) / f"{rv['file']}.dxf"
    else:
        pdf = BP / "phase1" / "out" / "pdf" / f"{rv['file']}.pdf"
        dxf = BP / "phase1" / "out" / "dxf" / f"{rv['file']}.dxf"
        if rv.get("frozen") and (pdf.exists() or dxf.exists()) and not a.force:
            sys.exit(f"Rev {a.rev} is FROZEN; its committed files stay as issued. Use --out-dir to regenerate for checking.")
    sh = build(p1, p2, a.rev)
    pdf.parent.mkdir(parents=True, exist_ok=True)
    dxf.parent.mkdir(parents=True, exist_ok=True)
    sh.render_pdf(pdf, title=f"{SHEET_NO} Rev {a.rev} {p1['sheets'][SHEET_NO]['title']} ({rv['audience_label']})", png_path=a.png)
    sh.render_dxf(dxf)
    if OVERFLOW:
        print("LAYOUT OVERFLOW:\n  " + "\n  ".join(OVERFLOW))
        sys.exit(1)
    print(f"wrote {pdf}\nwrote {dxf}" + (f"\nwrote {a.png}" if a.png else ""))


if __name__ == "__main__":
    main()
