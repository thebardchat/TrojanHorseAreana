"""KEYSTONE P2-A-201 EXTERIOR ELEVATIONS, Rev A (Phase 2, P2-T-009). Schematic, color.

South elevation (primary, 1/16 in = 1 ft) with the south portal; north, east and west (1/32 in = 1 ft).
Heights and finishes: params/phase2_elev.yaml. Building outline, arena volume and doors: params/phase2_plan_rev_d.yaml
(P2-A-101/102 Rev D, frozen in Phase 2 Schematic Set Rev A). DXF is in paper inches; fills are solid HATCH entities.
Usage (from the repo root):
  /workspace/.venv-keystone/bin/python blueprints/phase2/src/p2_a_201.py [--rev A] [--png PATH] [--out-dir DIR] [--force]
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import yaml

BP = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BP / "shared"))
from titleblock import Sheet, add_titleblock, text_width_in  # noqa: E402

W, H, M = 17.0, 11.0, 0.5
SHEET_NO = "P2-A-201"
L_OUT, L_FILL, L_TAG, L_DAT, L_HID, L_DOOR, L_SIGN = ("A-ELEV-OTLN", "A-ELEV-FILL", "A-ELEV-IDEN", "A-ELEV-DATM",
                                                      "A-ELEV-HIDN", "A-ELEV-DOOR", "A-ELEV-SIGN")


def load():
    p2 = yaml.safe_load((BP / "params" / "phase2.yaml").read_text(encoding="utf-8"))
    ev = yaml.safe_load((BP / "params" / "phase2_elev.yaml").read_text(encoding="utf-8"))
    plan = yaml.safe_load((BP / "params" / "phase2_plan_rev_d.yaml").read_text(encoding="utf-8"))
    return p2, ev, plan


class Elev:
    """Maps elevation coordinates (u = ft along the face from the viewer's left, z = ft above L1 FF) to paper inches."""

    def __init__(self, sh, x0, y0, ft_per_in):
        self.sh, self.x0, self.y0, self.s = sh, x0, y0, 1.0 / ft_per_in

    def P(self, u, z):
        return self.x0 + u * self.s, self.y0 + z * self.s

    def box(self, u0, z0, u1, z1, fill=None, layer=L_OUT, lw=0.8):
        pts = [self.P(u0, z0), self.P(u1, z0), self.P(u1, z1), self.P(u0, z1)]
        self.sh.poly(pts, fill=fill, layer=L_FILL if fill and not lw else layer, lw=lw)

    def line(self, u0, z0, u1, z1, layer=L_OUT, lw=0.6):
        a, b = self.P(u0, z0), self.P(u1, z1)
        self.sh.line(a[0], a[1], b[0], b[1], layer=layer, lw=lw)

    def dashed(self, u0, z0, u1, z1, layer=L_HID, lw=0.4, dash=0.06, gap=0.045):
        a, b = self.P(u0, z0), self.P(u1, z1)
        self.sh.dashed(a[0], a[1], b[0], b[1], layer=layer, lw=lw, dash=dash, gap=gap)

    def text(self, u, z, s, **kw):
        x, y = self.P(u, z)
        self.sh.text(x, y, s, **kw)


def arc_pts(cu, cz, r, a0, a1, n=48):
    return [(cu + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)), cz + r * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]


def faces(plan, ev):
    """Per face: list of (u0, u1, z_top, depth_rank) masses, door list (u, id, kind), face length."""
    bx0, by0, bx1, by1 = plan["building"]["rect"]
    pj = plan["building"]["projection"]["rect"]
    ar = ev["arena_volume"]["rect"]
    hz = ev["heights"]
    ring, top = hz["ring_roof"]["value"], hz["arena_roof_top"]["value"]
    doors = plan["level_1"]["doors"]["items"]
    by1p = pj[3]
    F = {}
    # SOUTH: viewer looks north; u = x
    F["S"] = dict(length=bx1 - bx0, masses=[(bx0, bx1, ring, 0), (ar[0], ar[2], top, 1)],
                  doors=[(d["at"], d["id"], d["kind"]) for d in doors if d["wall"] == "S"], set_back={1: ar[1] - by0},
                  label_l="W", label_r="E")
    # NORTH: viewer looks south; u = bx1 - x
    F["N"] = dict(length=bx1 - bx0, masses=[(0, bx1 - bx0, ring, 0), (bx1 - pj[2], bx1 - pj[0], ring, -1), (bx1 - ar[2], bx1 - ar[0], top, 1)],
                  doors=[(bx1 - d["at"], d["id"], d["kind"]) for d in doors if d["wall"] == "N"], set_back={1: by1 - ar[3]},
                  label_l="E", label_r="W")
    # EAST: viewer looks west; u = y
    F["E"] = dict(length=by1p - by0, masses=[(by0, ar[1], ring, 0), (ar[3], by1p, ring, 0), (ar[1], ar[3], top, 0)],
                  doors=[(d["at"], d["id"], d["kind"]) for d in doors if d["wall"] == "E"], set_back={0: bx1 - ar[2]},
                  label_l="S", label_r="N")
    # WEST: viewer looks east; u = by1p - y (the NE stair tower shows as a sliver at the north end, far back)
    F["W"] = dict(length=by1p - by0, masses=[(by1p - by1, by1p - by0, ring, 0), (0, by1p - by1, ring, 2), (by1p - ar[3], by1p - ar[1], top, 1)],
                  doors=[(by1p - d["at"], d["id"], d["kind"]) for d in doors if d["wall"] == "W"], set_back={1: ar[0] - bx0},
                  label_l="N", label_r="S")
    return F


def draw_face(sh, el, f, ev, fin, primary=False):
    hz = ev["heights"]
    ring, top, us = hz["ring_roof"]["value"], hz["arena_roof_top"]["value"], hz["arena_structure_underside"]["value"]
    # back to front: arena volume (rank 1 / 2) first, then the ring (rank 0), then forward projections (rank < 0)
    ms = sorted(f["masses"], key=lambda m: -m[3])
    for u0, u1, zt, rk in ms:
        col = fin["arena"]["hex"] if zt == top else fin["wall"]["hex"]
        el.box(u0, 0, u1, zt, fill=col, lw=0)
    for u0, u1, zt, rk in ms:
        el.box(u0, 0, u1, zt, layer=L_OUT, lw=1.0 if rk <= 0 else 0.7)
    # arena structure underside (hidden) inside the arena mass
    for u0, u1, zt, rk in ms:
        if zt == top:
            el.dashed(u0 + 1, us, u1 - 1, us)
    # L2 floor line (hidden) across the ring
    el.dashed(0, hz["l2_ff"]["value"], f["length"], hz["l2_ff"]["value"], lw=0.3, dash=0.04, gap=0.05)
    # doors
    dw, dh = ev["doors"]["symbol_width"], ev["doors"]["symbol_height"]
    for u, i, k in f["doors"]:
        if k == "main":
            continue
        if k == "service":
            el.dashed(u - dw, 0, u - dw, dh * 1.25, layer=L_DOOR, lw=0.6); el.dashed(u + dw, 0, u + dw, dh * 1.25, layer=L_DOOR, lw=0.6)
            el.dashed(u - dw, dh * 1.25, u + dw, dh * 1.25, layer=L_DOOR, lw=0.6)
            el.text(u, dh * 1.25 + 1.2, f"{i} SERVICE · SIZE TBD", size=4.6 if not primary else 5.4, bold=True, align="center", layer=L_TAG)
        else:
            el.box(u - dw / 2, 0, u + dw / 2, dh, fill="#5A5A5A", layer=L_DOOR, lw=0.5)
            el.text(u, dh + 1.2, i, size=4.6 if not primary else 5.6, bold=True, align="center", layer=L_TAG)
    # ground line
    ov = 4 if primary else 2
    el.line(-ov, 0, f["length"] + ov, 0, layer=L_OUT, lw=1.8)


def draw_portal(sh, el, ev, fin):
    pt = ev["portal"]
    cx, ow, oh, op = pt["center_x"], pt["overall_width"], pt["overall_height"], pt["opening_width"]
    sp, cr = pt["springline"], pt["crown"]
    r = op / 2
    u0, u1 = cx - ow / 2, cx + ow / 2
    i0, i1 = cx - r, cx + r
    lime, crim, gold = fin["limestone"]["hex"], fin["crimson"]["hex"], fin["gold"]["hex"]
    # limestone frame with the arch opening cut out (one polygon, traced around)
    arch = arc_pts(cx, sp, r, 0, 180)
    outline = [(u0, 0), (i0, 0), (i0, sp)] + arch[::-1] + [(i1, sp), (i1, 0), (u1, 0), (u1, oh), (u0, oh)]
    # arch opening: crimson back plane, gold soffit band on the intrados, entry glazing below
    sh.poly([el.P(a, b) for a, b in [(i0, 0), (i1, 0), (i1, sp)] + arch + [(i0, sp)]], fill=crim, layer=L_FILL, lw=0)
    band = 1.2
    inner = arc_pts(cx, sp, r - band, 0, 180)
    sh.poly([el.P(a, b) for a, b in arch + inner[::-1]], fill=gold, layer=L_FILL, lw=0)
    sh.poly([el.P(a, b) for a, b in [(i0, 0), (i0 + band, 0), (i0 + band, sp), (i0, sp)]], fill=gold, layer=L_FILL, lw=0)
    sh.poly([el.P(a, b) for a, b in [(i1 - band, 0), (i1, 0), (i1, sp), (i1 - band, sp)]], fill=gold, layer=L_FILL, lw=0)
    gh = pt["entry_glazing_height"]
    g0, g1 = i0 + band + 1.5, i1 - band - 1.5
    el.box(g0, 0, g1, gh, fill=fin["glazing"]["hex"], layer=L_OUT, lw=0.5)
    for k in range(1, 6):
        uu = g0 + (g1 - g0) * k / 6
        el.line(uu, 0, uu, gh, layer=L_OUT, lw=0.3)
    el.line(g0, 9, g1, 9, layer=L_OUT, lw=0.3)
    sh.poly([el.P(a, b) for a, b in outline], fill=lime, layer=L_FILL, lw=0)
    sh.poly([el.P(a, b) for a, b in outline], fill=None, layer=L_OUT, lw=1.2)
    # piers, imposts, attic and cornice lines (limestone articulation, schematic)
    for uu in (u0 + 2, u1 - 2):
        el.line(uu, 0, uu, pt["attic_band"][0], layer=L_OUT, lw=0.35)
    el.line(u0, sp, i0, sp, layer=L_OUT, lw=0.45); el.line(i1, sp, u1, sp, layer=L_OUT, lw=0.45)
    el.line(u0, pt["attic_band"][0], u1, pt["attic_band"][0], layer=L_OUT, lw=0.6)
    el.line(u0 - 1, oh - 1.2, u1 + 1, oh - 1.2, layer=L_OUT, lw=0.5)
    el.box(u0 - 1, oh - 1.2, u1 + 1, oh, fill=lime, layer=L_OUT, lw=0.6)
    ks = arc_pts(cx, sp, r + 2.2, 82, 98, 4)
    sh.poly([el.P(a, b) for a, b in [arch[22], arch[26]] + ks[::-1]], fill=lime, layer=L_OUT, lw=0.5)   # keystone
    # brand / signage placeholder on the attic
    a0, a1 = pt["attic_band"]
    el.box(cx - 15, a0 + 1.4, cx + 15, a1 - 2.4, fill=fin["brand_red"]["hex"], layer=L_SIGN, lw=0.8)
    el.text(cx, (a0 + a1) / 2 - 1.55, ev["signage"]["text"], size=6.4, bold=True, align="center", layer=L_SIGN, color="#FFFFFF")
    el.text(cx, gh + 1.0, "E1 MAIN ENTRY / EXIT", size=5.2, bold=True, align="center", layer=L_TAG, color="#FFFFFF")


def datums(sh, el, ev, length, side="left", size=5.4, which=None, short=False):
    hz = ev["heights"]
    rows = [("l1_ff", "L1 FF 0'-0\""), ("l2_ff", "L2 FF 15'-0\" (ASSUMED)"), ("ring_roof", "T.O. RING ROOF 30'-0\" (ASSUMED)"),
            ("arena_structure_underside", "U/S ARENA STRUCT. 36'-0\" (ASSUMED)"),
            ("arena_roof_top", "T.O. ARENA ROOF 42'-0\" (ASSUMED)")]
    if short:
        rows = [(k, f"{hz[k]['value']}'-0\"") for k, _ in rows]
    if which:
        rows = [r for r in rows if r[0] in which]
    for k, lab in rows:
        z = hz[k]["value"]
        if side == "left":
            el.line(-9, z, -2, z, layer=L_DAT, lw=0.5)
            x, y = el.P(-10, z)
            sh.text(x, y - 0.025, lab, size=size, align="right", layer=L_DAT)
        else:
            el.line(length + 2, z, length + 9, z, layer=L_DAT, lw=0.5)
            x, y = el.P(length + 10, z)
            sh.text(x, y - 0.025, lab, size=size, layer=L_DAT)


def build(p2, ev, plan):
    meta2, em = p2["meta"], ev["meta"]
    fin = {f["id"]: f for f in ev["finishes"]}
    sh = Sheet(W, H)
    body_bottom = add_titleblock(sh, {
        "project": f"{meta2['project']}\n{meta2['arena_name']} · {meta2['location']}",
        "phase": "PHASE 2",
        "title": "EXTERIOR ELEVATIONS\nSCHEMATIC · COLOR",
        "scale": "AS NOTED",
        "date": meta2["sheet_date"],
        "revision": em["revision"],
        "drawn_by": meta2["drawn_by"],
        "sheet_no": SHEET_NO,
        "stamp": meta2["stamp"],
    }, margin=M, tb_h=0.95, stamp_h=0.40)
    F = faces(plan, ev)
    s16, s32 = em["scales"]["south_ft_per_in"], em["scales"]["others_ft_per_in"]
    pt = ev["portal"]

    # ---------- SOUTH (primary) ----------
    xS, yS = 2.95, 6.70
    elS = Elev(sh, xS, yS, s16)
    draw_face(sh, elS, F["S"], ev, fin, primary=True)
    # arena volume south-face signage zone (placeholder)
    ar = ev["arena_volume"]["rect"]
    elS.box(150, 36.8, 196, 41.2, fill=None, layer=L_SIGN, lw=0.7)
    elS.text(173, 38.3, ev["signage"]["text"], size=5.6, bold=True, align="center", layer=L_SIGN, color=fin["brand_black"]["hex"])
    draw_portal(sh, elS, ev, fin)
    datums(sh, elS, ev, F["S"]["length"], side="left", size=5.6)
    # tags
    elS.text(178, 8.0, "WALL MATERIAL TBD", size=6.0, align="center", layer=L_TAG)
    elS.text(30, 31.3, "PARAPET TBD", size=5.0, align="center", layer=L_TAG)
    elS.text(60, 43.3, "PARAPET TBD", size=5.0, align="center", layer=L_TAG)
    elS.text(25, 22.5, "WALL MATERIAL TBD", size=6.0, align="center", layer=L_TAG)
    elS.text((ar[0] + 91) / 2, 32.2, f"ARENA VOLUME BEHIND (set back {F['S']['set_back'][1]:g}')", size=5.4, align="center", layer=L_TAG)
    cx = pt["center_x"]
    for t_, zz, sz in (("SOUTH PORTAL — LIMESTONE ARCH", pt["overall_height"] + 3.6, 7.0),):
        elS.text(cx, zz, t_, size=sz, bold=True, align="center", layer=L_TAG)
    # callouts at the right of the portal
    xR, _ = elS.P(cx + pt["overall_width"] / 2 + 3, 0)
    for zz, t_ in ((pt["crown"] - 3, "CRIMSON inside the arch (Shane)"), (pt["springline"] - 4, "GOLD soffit / intrados band (Shane)"),
                   (pt["entry_glazing_height"] - 6, "ENTRY GLAZING TBD (E1)")):
        x_, y_ = elS.P(cx + pt["overall_width"] / 2 + 3, zz)
        x2_, y2_ = elS.P(cx + pt["opening_width"] / 2 - 2, zz + 0.6)
        sh.line(x2_, y2_, x_ - 0.04, y_ + 0.03, layer=L_TAG, lw=0.35)
        sh.text(x_, y_, t_, size=5.4, layer=L_TAG)
    x_, y_ = elS.P(0, -5.6)
    sh.text(x_, y_, "SOUTH ELEVATION (PRIMARY) — SCALE 1/16\" = 1'-0\"", size=8.5, bold=True, layer=L_TAG)
    x_, y_ = elS.P(F["S"]["length"], -5.6)
    sh.text(x_, y_, f"portal {pt['overall_width']}' w x {pt['overall_height']}' h, {pt['opening_width']}' arch, crown {pt['crown']}' (ASSUMED, render proportions) · W ← → E",
            size=6.0, align="right", layer=L_TAG)
    for u, lab in ((0, "W"), (F["S"]["length"], "E")):
        elS.text(u, -2.6, lab, size=5.6, bold=True, align="center", layer=L_TAG)

    # ---------- NORTH ----------
    xN, yN = 1.20, 4.30
    elN = Elev(sh, xN, yN, s32)
    draw_face(sh, elN, F["N"], ev, fin)
    datums(sh, elN, ev, F["N"]["length"], side="left", size=4.6, which=("ring_roof", "arena_roof_top", "l2_ff"), short=True)
    elN.text(0 + 9.5, 31.6, "NE STAIR TOWER (+5')", size=4.4, align="center", layer=L_TAG)
    x_, y_ = elN.P(0, -8.5)
    sh.text(x_, y_, "NORTH ELEVATION — 1/32\" = 1'-0\"  (E ← → W)", size=7.2, bold=True, layer=L_TAG)

    # ---------- EAST ----------
    xE, yE = 8.30, 4.30
    elE = Elev(sh, xE, yE, s32)
    draw_face(sh, elE, F["E"], ev, fin)
    elE.text((ar[1] + ar[3]) / 2, 38.6, "ARENA VOLUME (flush with the east wall)", size=4.8, align="center", layer=L_TAG)
    x_, y_ = elE.P(0, -8.5)
    datums(sh, elE, ev, F["E"]["length"], side="left", size=4.6, which=("ring_roof", "arena_roof_top", "l2_ff"), short=True)
    sh.text(x_, y_, "EAST ELEVATION — 1/32\" = 1'-0\"  (S ← → N)", size=7.2, bold=True, layer=L_TAG)

    # ---------- WEST ----------
    xW, yW = 1.20, 2.40
    elW = Elev(sh, xW, yW, s32)
    draw_face(sh, elW, F["W"], ev, fin)
    elW.text((F["W"]["length"]) / 2, 38.6, f"ARENA VOLUME BEHIND (set back {F['W']['set_back'][1]:g}')", size=4.8, align="center", layer=L_TAG)
    x_, y_ = elW.P(0, -8.5)
    datums(sh, elW, ev, F["W"]["length"], side="left", size=4.6, which=("ring_roof", "arena_roof_top", "l2_ff"), short=True)
    sh.text(x_, y_, "WEST ELEVATION — 1/32\" = 1'-0\"  (N ← → S)", size=7.2, bold=True, layer=L_TAG)

    # ---------- legend + notes ----------
    lx, ly = 10.35, 3.80
    sh.text(lx, ly, "FINISHES", size=7.6, bold=True)
    y = ly - 0.05
    for f in ev["finishes"]:
        y -= 0.145
        sh.poly([(lx, y - 0.02), (lx + 0.28, y - 0.02), (lx + 0.28, y + 0.09), (lx, y + 0.09)], fill=f["hex"], layer=L_FILL, lw=0.4)
        sh.text(lx + 0.36, y, f"{f['name']} — {f['status'].split(';')[0]}", size=5.6)
    nx = 13.05
    nw = W - M - 0.15 - nx
    y = ly + 0.13
    sh.text(nx, ly, "NOTES", size=7.6, bold=True)
    y = ly - 0.02
    hz = ev["heights"]
    notes = [f"HEIGHTS: L2 FF 15' (R-015) and ring roof 30' are ASSUMED. Arena clear ≥ {hz['arena_clear_min']['value']}' over the court "
             "(NFHS court specs via Draper; LA RAP gym standard; R-019). U/S arena structure 36' and roof 42' ASSUMED (≈ 15' over an "
             "assumed 21' top aisle, IBC 1030.6.2.2 if smoke-protected). Parapet TBD.",
             "PORTAL: limestone, crimson inside the arch, gold soffit (Shane). Size ASSUMED from his render's proportions; projects "
             "south of the façade, depth TBD.",
             "BRAND: placeholders only — no school logo (Phase 2 is Shane's build, D-028). HGHS badge? OPEN (D-040).",
             "DOORS: symbols (6' x 8' ASSUMED) from P2-A-101 Rev D; X# EXIT ONLY (D-033); S1 size TBD (D-034).",
             "NOT SHOWN: ETFE roof / solar (aspirations), rooftop units, grading, lighting."]
    for t_ in notes:
        y = sh.para(nx, y + 0.02, nw, t_, size=5.6, indent=0.1, bullet="·")
    fl = body_bottom + 0.06
    if y < fl:
        raise SystemExit(f"LAYOUT OVERFLOW: notes run {fl - y:.2f} in into the stamp band")
    print(f"layout margin notes (in): {y - fl:.2f}")
    return sh


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", choices=["A"], default="A")
    ap.add_argument("--png", help="optional PNG preview path (outside the repo)")
    ap.add_argument("--out-dir", help="write PDF/DXF here instead of phase2/out/{pdf,dxf}")
    ap.add_argument("--force", action="store_true", help="allow overwriting a FROZEN revision in the repo")
    a = ap.parse_args()
    p2, ev, plan = load()
    rv = p2["sheets"][SHEET_NO]["revisions"][a.rev]
    if a.out_dir:
        pdf, dxf = (Path(a.out_dir) / f"{rv['file']}.{e}" for e in ("pdf", "dxf"))
    else:
        pdf = BP / "phase2" / "out" / "pdf" / f"{rv['file']}.pdf"
        dxf = BP / "phase2" / "out" / "dxf" / f"{rv['file']}.dxf"
        if rv.get("frozen") and (pdf.exists() or dxf.exists()) and not a.force:
            sys.exit("Revision is FROZEN; use --out-dir to regenerate for checking.")
    sh = build(p2, ev, plan)
    pdf.parent.mkdir(parents=True, exist_ok=True)
    dxf.parent.mkdir(parents=True, exist_ok=True)
    sh.render_pdf(pdf, title=f"{SHEET_NO} Rev {a.rev} {p2['sheets'][SHEET_NO]['title']}", png_path=a.png)
    sh.render_dxf(dxf)
    print(f"wrote {pdf}\nwrote {dxf}" + (f"\nwrote {a.png}" if a.png else ""))


if __name__ == "__main__":
    main()
