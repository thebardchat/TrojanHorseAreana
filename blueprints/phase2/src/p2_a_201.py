"""KEYSTONE P2-A-201 EXTERIOR ELEVATIONS (Phase 2, P2-T-009). Schematic, color.

Rev A (FROZEN 2026-10-04 6:16 AM CT): BRAND / SIGNAGE — TBD placeholders. Inputs phase2_elev.yaml (unchanged since Rev A).
Rev B: official Trojan Horse Arena mark (brand/THA_logo_black.svg, D-041) on the portal above the arch + TROJAN HORSE ARENA
wordmark, side panel, enlarged brand detail; freestanding portal over Champion Walk, key plan. FROZEN 2026-10-04 6:45 AM CT.
Inputs phase2_elev.yaml + phase2_elev_rev_b.yaml (overlay).
Rev C: 11 ft badge, portal raised to 56 ft (ASSUMED), Champion Walk 28 x 30 ft + brick tiers, crimson underside + gold trim
(D-045..D-047). Inputs phase2_elev.yaml + phase2_elev_rev_c.yaml (overlay). FROZEN 2026-10-04 7:24 AM CT.
Rev D: portal capped at 50 ft (D-050): arch crown 34 ft, springline 22.1 ft (26 x 34/40, ASSUMED), semi-elliptical arch
(rise 11.9 ft); 11 ft badge 34.4-45.4 ft; wordmark baseline 46.1 ft, caps top 48.35 ft, under the 48.8-50 ft cornice.
Inputs phase2_elev.yaml + phase2_elev_rev_d.yaml (overlay).
Rev E: coordinated with P2-A-101/102 Rev E: 210 ft width, arena volume flush with the new east wall, NE stair tower
21.33 x 6.67 ft, doors from Rev E (phase2_elev_rev_e.yaml `plan_file`). Portal / brand unchanged from Rev D.

South elevation (primary, 1/16 in = 1 ft) with the south portal; north, east and west (1/32 in = 1 ft).
Heights and finishes: params/phase2_elev.yaml. Building outline, arena volume and doors: params/phase2_plan_rev_d.yaml
(P2-A-101/102 Rev D, frozen in Phase 2 Schematic Set Rev A). DXF is in paper inches; fills are solid HATCH entities.
Usage (from the repo root):
  /workspace/.venv-keystone/bin/python blueprints/phase2/src/p2_a_201.py [--rev A|B|C|D|E] [--png PATH] [--out-dir DIR] [--force]
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


def load(rev="A"):
    p2 = yaml.safe_load((BP / "params" / "phase2.yaml").read_text(encoding="utf-8"))
    ev = yaml.safe_load((BP / "params" / "phase2_elev.yaml").read_text(encoding="utf-8"))
    plan = yaml.safe_load((BP / "params" / "phase2_plan_rev_d.yaml").read_text(encoding="utf-8"))
    evb = None
    if rev in ("B", "C", "D", "E"):
        evb = yaml.safe_load((BP / "params" / f"phase2_elev_rev_{rev.lower()}.yaml").read_text(encoding="utf-8"))
        if evb.get("plan_file"):                   # Rev E: P2-A-101/102 Rev E geometry (210 ft, 6.67 ft NE tower)
            plan = yaml.safe_load((BP / "params" / evb["plan_file"]).read_text(encoding="utf-8"))
        if evb.get("arena_volume_override"):
            ev["arena_volume"]["rect"] = evb["arena_volume_override"]["rect"]
        po = evb.get("portal_override")
        if po:                                     # Rev C: taller portal / attic; Rev D: lower arch, 50 ft cap (ASSUMED)
            for k, v in po.items():
                if k not in ("basis", "status", "source"):
                    ev["portal"][k] = v
    return p2, ev, plan, evb


CAP = 0.729          # DejaVu Sans Bold cap height / em (sheet font)


def cap_pt(cap_ft, ft_per_in):
    """Font size (pt) whose cap height is cap_ft at the given scale."""
    return cap_ft / ft_per_in / CAP * 72.0


def draw_brand(sh, el, ev, evb, ft_per_in, detail=False):
    """Rev B: official mark above the arch + wordmark on the attic (D-041). Sizes ASSUMED (phase2_elev_rev_b.yaml)."""
    pt, mk, wm = ev["portal"], evb["mark"], evb["wordmark"]
    cx = pt["center_x"]
    x, y = el.P(cx, mk["center_z"])
    sh.mark("THA_MARK", BP / mk["file"], x, y, mk["diameter"] / ft_per_in, mk["fill"], layer=L_SIGN)
    size = cap_pt(wm["cap_height"], ft_per_in)
    tw = text_width_in(wm["text"], size, True) * ft_per_in
    lim = pt["overall_width"] - 4
    if tw > lim:
        raise SystemExit(f"LAYOUT OVERFLOW: wordmark {tw:.1f} ft wider than the portal attic ({lim} ft)")
    el.text(cx, wm["baseline_z"], wm["text"], size=size, bold=True, align="center", layer=L_SIGN, color=wm["color"])
    return tw


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


def arch_pts(pt, cu, cz, r, off, a0, a1, n=48):
    """Arch intrados offset inward by `off`: semicircle (Revs A-C) or, when the portal carries `arch_rise` (Rev D), a
    semi-ellipse with half-span r and rise arch_rise (crown lowered, springline scaled; ASSUMED)."""
    a, b = r, pt.get("arch_rise", r)
    for o in off:                                  # applied one by one so Revs A-C keep their exact floats
        a, b = a - o, b - o
    if "arch_rise" not in pt:
        return arc_pts(cu, cz, a, a0, a1, n)
    return [(cu + a * math.cos(math.radians(a0 + (a1 - a0) * k / n)), cz + b * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]


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


def draw_portal(sh, el, ev, fin, evb=None):
    pt = ev["portal"]
    cx, ow, oh, op = pt["center_x"], pt["overall_width"], pt["overall_height"], pt["opening_width"]
    sp, cr = pt["springline"], pt["crown"]
    r = op / 2
    u0, u1 = cx - ow / 2, cx + ow / 2
    i0, i1 = cx - r, cx + r
    lime, crim, gold = fin["limestone"]["hex"], fin["crimson"]["hex"], fin["gold"]["hex"]
    # limestone frame with the arch opening cut out (one polygon, traced around)
    arch = arch_pts(pt, cx, sp, r, (), 0, 180)
    outline = [(u0, 0), (i0, 0), (i0, sp)] + arch[::-1] + [(i1, sp), (i1, 0), (u1, 0), (u1, oh), (u0, oh)]
    if evb is None:
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
    else:
        # Rev B: FREESTANDING portal (D-043) — the opening is open; the building's E1 entry glazing shows behind it
        eg = evb["entry_glazing_building"]
        gh = eg["height"]
        g0, g1 = cx - eg["width"] / 2, cx + eg["width"] / 2
        el.box(g0, 0, g1, gh, fill=fin["glazing"]["hex"], layer=L_OUT, lw=0.5)
        for k in range(1, 6):
            uu = g0 + (g1 - g0) * k / 6
            el.line(uu, 0, uu, gh, layer=L_OUT, lw=0.3)
        el.line(g0, 9, g1, 9, layer=L_OUT, lw=0.3)
        # crimson soffit band inside the arch with a thin gold edge (split TBD)
        band, ge = 1.6, 0.4
        inner = arch_pts(pt, cx, sp, r, (band,), 0, 180)
        inner2 = arch_pts(pt, cx, sp, r, (band, ge), 0, 180)
        sh.poly([el.P(a, b) for a, b in arch + inner[::-1]], fill=crim, layer=L_FILL, lw=0)
        sh.poly([el.P(a, b) for a, b in [(i0, 0), (i0 + band, 0), (i0 + band, sp), (i0, sp)]], fill=crim, layer=L_FILL, lw=0)
        sh.poly([el.P(a, b) for a, b in [(i1 - band, 0), (i1, 0), (i1, sp), (i1 - band, sp)]], fill=crim, layer=L_FILL, lw=0)
        sh.poly([el.P(a, b) for a, b in inner + inner2[::-1]], fill=gold, layer=L_FILL, lw=0)
        sh.poly([el.P(a, b) for a, b in [(i0 + band, 0), (i0 + band + ge, 0), (i0 + band + ge, sp), (i0 + band, sp)]], fill=gold, layer=L_FILL, lw=0)
        sh.poly([el.P(a, b) for a, b in [(i1 - band - ge, 0), (i1 - band, 0), (i1 - band, sp), (i1 - band - ge, sp)]], fill=gold, layer=L_FILL, lw=0)
    sh.poly([el.P(a, b) for a, b in outline], fill=lime, layer=L_FILL, lw=0)
    sh.poly([el.P(a, b) for a, b in outline], fill=None, layer=L_OUT, lw=1.2)
    # piers, imposts, attic and cornice lines (limestone articulation, schematic)
    for uu in (u0 + 2, u1 - 2):
        el.line(uu, 0, uu, pt["attic_band"][0], layer=L_OUT, lw=0.35)
    el.line(u0, sp, i0, sp, layer=L_OUT, lw=0.45); el.line(i1, sp, u1, sp, layer=L_OUT, lw=0.45)
    if evb is None:
        el.line(u0, pt["attic_band"][0], u1, pt["attic_band"][0], layer=L_OUT, lw=0.6)
    else:                                       # Rev B: attic line stops either side of the mark
        rr = evb["mark"]["diameter"] / 2 + 0.6
        el.line(u0, pt["attic_band"][0], cx - rr, pt["attic_band"][0], layer=L_OUT, lw=0.6)
        el.line(cx + rr, pt["attic_band"][0], u1, pt["attic_band"][0], layer=L_OUT, lw=0.6)
    el.line(u0 - 1, oh - 1.2, u1 + 1, oh - 1.2, layer=L_OUT, lw=0.5)
    el.box(u0 - 1, oh - 1.2, u1 + 1, oh, fill=lime, layer=L_OUT, lw=0.6)
    if evb is None:
        ks = arc_pts(cx, sp, r + 2.2, 82, 98, 4)
        sh.poly([el.P(a, b) for a, b in [arch[22], arch[26]] + ks[::-1]], fill=lime, layer=L_OUT, lw=0.5)   # keystone
        # brand / signage placeholder on the attic
        a0, a1 = pt["attic_band"]
        el.box(cx - 15, a0 + 1.4, cx + 15, a1 - 2.4, fill=fin["brand_red"]["hex"], layer=L_SIGN, lw=0.8)
        el.text(cx, (a0 + a1) / 2 - 1.55, ev["signage"]["text"], size=6.4, bold=True, align="center", layer=L_SIGN, color="#FFFFFF")
    else:
        draw_brand(sh, el, ev, evb, 1.0 / el.s)
    if evb is None:
        el.text(cx, gh + 1.0, "E1 MAIN ENTRY / EXIT", size=5.2, bold=True, align="center", layer=L_TAG, color="#FFFFFF")
    else:
        el.text(cx, gh + 1.0, "E1 MAIN ENTRY (building, behind)", size=5.0, bold=True, align="center", layer=L_TAG)
        cw = evb["champion_walk"]
        el.box(cx - cw["width"] / 2, -1.3, cx + cw["width"] / 2, 0, fill=cw["brick_hex"], layer=L_FILL, lw=0.4)
        for k in range(1, 14):
            uu = cx - cw["width"] / 2 + cw["width"] * k / 14
            el.line(uu, -1.3, uu, 0, layer=L_FILL, lw=0.2)


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


def side_panel(sh, el, evb, ft_per_in):
    """Rev B: 'Hazel Green Regional Athletic Complex' panel on the west ring wall (ASSUMED size)."""
    sp = evb["side_panel"]
    u0, z0, u1, z1 = sp["rect"]
    el.box(u0, z0, u1, z1, fill=sp["panel"], layer=L_SIGN, lw=0.6)
    el.box(u0, z0, u1, z0 + 0.8, fill=sp["stripe"], layer=L_SIGN, lw=0)
    size = cap_pt(sp["cap_height"], ft_per_in)
    for k, ln in enumerate(sp["lines"]):
        tw = text_width_in(ln, size, True) * ft_per_in
        if tw > (u1 - u0) - 2:
            raise SystemExit(f"LAYOUT OVERFLOW: side panel line '{ln}' {tw:.1f} ft > panel {u1 - u0 - 2} ft")
        el.text((u0 + u1) / 2, z1 - 2.6 - k * 2.6, ln, size=size, bold=True, align="center", layer=L_SIGN, color=sp["text_color"])
    el.text((u0 + u1) / 2, z0 - 2.8, "SIDE PANEL (size ASSUMED)", size=4.8, align="center", layer=L_TAG)


def key_plan(sh, ev, evb, plan):
    """Rev B: schematic key plan (north up, 1 in = 60 ft) of the freestanding portal over Champion Walk in front of the
    building's south entrance (D-043). Gap, portal depth and walk width ASSUMED; walk length TBD. Site plan follows on A-101."""
    kp, pf, cw, pt = evb["key_plan"], evb["portal_freestanding"], evb["champion_walk"], ev["portal"]
    fpi = kp["ft_per_in"]
    cx = pt["center_x"]
    bx0, by0, bx1, by1 = plan["building"]["rect"]
    xc, yw = 3.30, kp.get("y_wall", 10.26)                 # sheet x of the entry axis, sheet y of the south wall

    def P(u, d):                                           # u = ft east (plan x), d = ft south of the south wall
        return xc + (u - cx) / fpi, yw - d / fpi
    d_end = (yw - kp.get("y_bottom", 9.47)) * fpi
    # walk (brick), from the wall south through the portal
    w0, w1 = cx - cw["width"] / 2, cx + cw["width"] / 2
    d_brick = d_end
    if "extension" in cw:                              # Rev C: 28 x 30 walk (D-046) + paving under the portal; extension dashed
        d_brick = pf["gap_to_building"] + pf["depth"]
        for dd0, dd1 in ((d_brick, d_end),):
            for uu in (w0, w1):
                a, b = P(uu, dd0), P(uu, dd1)
                sh.dashed(a[0], a[1], b[0], b[1], layer=L_HID, lw=0.4, dash=0.04, gap=0.03)
    sh.poly([P(w0, 0), P(w1, 0), P(w1, d_brick), P(w0, d_brick)], fill=cw["brick_hex"], layer=L_FILL, lw=0)
    d = 3.0
    while d < d_brick:
        a, b = P(w0, d), P(w1, d)
        sh.line(a[0], a[1], b[0], b[1], layer=L_FILL, lw=0.15)
        d += 3.0
    a, b = P(w0, 0), P(w0, d_brick); sh.line(a[0], a[1], b[0], b[1], layer=L_OUT, lw=0.5)
    a, b = P(w1, 0), P(w1, d_brick); sh.line(a[0], a[1], b[0], b[1], layer=L_OUT, lw=0.5)
    # break line at the south end
    zz = [P(w0 - 2, d_end), P(cx - 3, d_end), P(cx - 1.5, d_end - 2.5), P(cx + 1.5, d_end + 2.5), P(cx + 3, d_end), P(w1 + 2, d_end)]
    for q0, q1 in zip(zz, zz[1:]):
        sh.line(q0[0], q0[1], q1[0], q1[1], layer=L_OUT, lw=0.4)
    # building south wall + corners, E1
    a, b = P(bx0, 0), P(bx1, 0); sh.line(a[0], a[1], b[0], b[1], layer=L_OUT, lw=1.2)
    for u in (bx0, bx1):
        a, b = P(u, 0), P(u, -2.4); sh.line(a[0], a[1], b[0], b[1], layer=L_OUT, lw=1.2)
    x_, y_ = P(bx0 + 3, -1.4)
    sh.text(x_, y_, evb.get("text_rev_e", {}).get("key_wall", "BUILDING — SOUTH WALL (P2-A-101 Rev D)"), size=4.4, layer=L_TAG)
    x_, y_ = P(cx, -1.4)
    sh.text(x_, y_, "E1", size=4.6, bold=True, align="center", layer=L_TAG)
    # freestanding portal: two piers + arch over (dashed)
    g, dp, ow, op = pf["gap_to_building"], pf["depth"], pt["overall_width"], pt["opening_width"]
    for u0, u1 in ((cx - ow / 2, cx - op / 2), (cx + op / 2, cx + ow / 2)):
        sh.poly([P(u0, g), P(u1, g), P(u1, g + dp), P(u0, g + dp)], fill=ev["finishes"][0]["hex"], layer=L_OUT, lw=0.6)
    for dd in (g, g + dp):
        a, b = P(cx - op / 2, dd), P(cx + op / 2, dd)
        sh.dashed(a[0], a[1], b[0], b[1], layer=L_HID, lw=0.35, dash=0.03, gap=0.025)
    # gap dimension (west side)
    ud = cx - ow / 2 - 6
    a, b = P(ud, 0), P(ud, g); sh.line(a[0], a[1], b[0], b[1], layer=L_DAT, lw=0.4)
    for dd in (0, g):
        a, b = P(ud - 1.5, dd), P(ud + 1.5, dd); sh.line(a[0], a[1], b[0], b[1], layer=L_DAT, lw=0.4)
    x_, y_ = P(ud - 2, g / 2 + 0.6)
    sh.text(x_, y_, f"GAP ≈ {g:g}' (ASSUMED)", size=4.6, align="right", layer=L_DAT)
    # walk labels (east side)
    xl, _ = P(cx + ow / 2 + 3, 0)
    lab = ([(l["text"], l["bold"]) for l in cw["labels"]] if cw.get("labels") else
           [(f"{cw['name']} — BRICK", True), (cw["note"], False),
            (f"width {cw['width']:g}' (= arch opening, ASSUMED) · length TBD", False),
            ("continues south (way in) — low walls / planters TBD", False),
            (f"FREESTANDING PORTAL (2 piers, depth {dp:g}' ASSUMED)", True)])
    for k, (t_, b_) in enumerate(lab):
        _, y_ = P(0, 9 + k * 6.2)
        sh.text(xl, y_, t_, size=4.8 if b_ else 4.5, bold=b_, layer=L_TAG)
    if "extension" in cw:
        x_, y_ = P(cx + cw["width"] / 2 + 2, (d_brick + d_end) / 2 + 2)
        sh.text(x_, y_, cw["ext_label"], size=4.5, layer=L_TAG)
        x_, y_ = P(cx - ow / 2 - 2, (d_brick + d_end) / 2 + 2)
        sh.text(x_, y_, cw["bus_label"], size=4.5, align="right", layer=L_TAG)
    ty = kp.get("title_y", 9.60)
    sh.text(0.62, ty, kp["title"], size=5.4, bold=True, layer=L_TAG)
    sh.text(0.62, ty - 0.115, evb.get("text_rev_e", {}).get("key_sub", "north up · site plan on the next A-101 revision"), size=4.5, layer=L_TAG)
    if 0.62 + text_width_in(kp["title"], 5.4, True) > P(cx - ow / 2, 0)[0] - 0.05:
        raise SystemExit("LAYOUT OVERFLOW: key plan title runs into the portal piers")


def brand_detail(sh, ev, evb, fin):
    """Rev B: enlarged portal attic (3/32 in = 1 ft-0 in) in the free band above the south elevation, right of the portal."""
    dt, pt = evb["detail"], ev["portal"]
    fpi = 32.0 / 3.0
    assert abs(fpi - dt["ft_per_in"]) < 1e-3
    cx, ow = pt["center_x"], pt["overall_width"]
    z0, z1 = dt["z_range"]
    u0, u1 = cx - ow / 2, cx + ow / 2
    x_left = 11.62
    el = Elev(sh, x_left - u0 / fpi, dt.get("y_bottom", 9.43) - z0 / fpi, fpi)
    lime = fin["limestone"]["hex"]
    oh = pt["overall_height"]
    el.box(u0, z0, u1, oh, fill=lime, layer=L_FILL, lw=0)
    el.box(u0 - 1, oh - 1.2, u1 + 1, oh, fill=lime, layer=L_OUT, lw=0.6)
    for uu in (u0 + 2, u1 - 2):
        el.line(uu, z0, uu, pt["attic_band"][0], layer=L_OUT, lw=0.35)
    rr = evb["mark"]["diameter"] / 2 + 0.6
    a0 = pt["attic_band"][0]
    el.line(u0, a0, cx - rr, a0, layer=L_OUT, lw=0.5)
    el.line(cx + rr, a0, u1, a0, layer=L_OUT, lw=0.5)
    el.line(u0, z0, u0, oh, layer=L_OUT, lw=0.9); el.line(u1, z0, u1, oh, layer=L_OUT, lw=0.9)
    el.dashed(u0, z0, u1, z0, layer=L_HID, lw=0.4)
    tw = draw_brand(sh, el, ev, evb, fpi, detail=True)
    mk, wm = evb["mark"], evb["wordmark"]
    xr, _ = el.P(u1 + 1.6, 0)
    for k, t_ in enumerate(dt["title_lines"]):
        _, y_ = el.P(0, oh - 0.9 - k * 0.95)
        sh.text(xr, y_, t_, size=4.8, bold=True, layer=L_TAG)
    for zz, t_ in ((wm["baseline_z"] - 1.3, "WORDMARK"), (wm["baseline_z"] - 2.2, f"CAP {wm['cap_height'] * 12:g}\""),
                   (mk["center_z"] - 0.9, f"MARK Ø {mk['diameter']:g}'-0\""),
                   (mk["center_z"] - 1.8, "SIZES ASSUMED"), (z0 + 0.5, f"CROWN {pt['crown']}'")):
        _, y_ = el.P(0, zz)
        sh.text(xr, y_, t_, size=4.4, layer=L_TAG)
    wmax = max(text_width_in(t, 4.8, True) for t in dt["title_lines"])
    if xr + wmax > W - M - 0.04:
        raise SystemExit(f"LAYOUT OVERFLOW: brand detail labels run past the border ({xr + wmax:.2f} in)")
    print(f"brand detail: wordmark {tw:.1f} ft wide; detail right edge x {el.P(u1 + 1, 0)[0]:.2f} in")


def build(p2, ev, plan, evb=None):
    meta2, em = p2["meta"], ev["meta"]
    fin = {f["id"]: f for f in ev["finishes"]}
    sh = Sheet(W, H)
    body_bottom = add_titleblock(sh, {
        "project": f"{meta2['project']}\n{meta2['arena_name']} · {meta2['location']}",
        "phase": "PHASE 2",
        "title": "EXTERIOR ELEVATIONS\nSCHEMATIC · COLOR",
        "scale": "AS NOTED",
        "date": meta2["sheet_date"],
        "revision": evb["meta"]["revision"] if evb else em["revision"],
        "drawn_by": meta2["drawn_by"],
        "sheet_no": SHEET_NO,
        "stamp": meta2["stamp"],
    }, margin=M, tb_h=0.95, stamp_h=0.40)
    F = faces(plan, ev)
    s16, s32 = em["scales"]["south_ft_per_in"], em["scales"]["others_ft_per_in"]
    pt = ev["portal"]

    # ---------- SOUTH (primary) ----------
    xS, yS = 2.95, (evb.get("layout", {}).get("south_y0", 6.70) if evb else 6.70)
    elS = Elev(sh, xS, yS, s16)
    draw_face(sh, elS, F["S"], ev, fin, primary=True)
    # arena volume south-face signage zone (placeholder)
    ar = ev["arena_volume"]["rect"]
    elS.box(150, 36.8, 196, 41.2, fill=None, layer=L_SIGN, lw=0.7)
    elS.text(173, 38.3, evb["arena_sign"]["text"] if evb else ev["signage"]["text"], size=5.6, bold=True, align="center", layer=L_SIGN, color=fin["brand_black"]["hex"])
    draw_portal(sh, elS, ev, fin, evb)
    if evb:
        side_panel(sh, elS, evb, s16)
        key_plan(sh, ev, evb, plan)
        brand_detail(sh, ev, evb, fin)
    datums(sh, elS, ev, F["S"]["length"], side="left", size=5.6)
    # tags
    elS.text(178, 8.0, "WALL MATERIAL TBD", size=6.0, align="center", layer=L_TAG)
    elS.text(30, 31.3, "PARAPET TBD", size=5.0, align="center", layer=L_TAG)
    elS.text(60, 43.3, "PARAPET TBD", size=5.0, align="center", layer=L_TAG)
    elS.text(25, 22.5, "WALL MATERIAL TBD", size=6.0, align="center", layer=L_TAG)
    elS.text((ar[0] + 91) / 2, 32.2, f"ARENA VOLUME BEHIND (set back {F['S']['set_back'][1]:g}')", size=5.4, align="center", layer=L_TAG)
    cx = pt["center_x"]
    ttl = ((("GRAND ENTRANCE PORTAL (FREESTANDING)", pt["overall_height"] + 3.6, 7.0),
            (evb.get("title2") or f"stands ≈ {evb['portal_freestanding']['gap_to_building']:g}' south of the entrance (gap ASSUMED) · see key plan", pt["overall_height"] + 1.3, 5.2))
           if evb else (("SOUTH PORTAL — LIMESTONE ARCH", pt["overall_height"] + 3.6, 7.0),))
    for t_, zz, sz in ttl:
        elS.text(cx, zz, t_, size=sz, bold=True, align="center", layer=L_TAG)
    # callouts at the right of the portal
    xR, _ = elS.P(cx + pt["overall_width"] / 2 + 3, 0)
    if evb is None:
        for zz, t_ in ((pt["crown"] - 3, "CRIMSON inside the arch (Shane)"), (pt["springline"] - 4, "GOLD soffit / intrados band (Shane)"),
                       (pt["entry_glazing_height"] - 6, "ENTRY GLAZING TBD (E1)")):
            x_, y_ = elS.P(cx + pt["overall_width"] / 2 + 3, zz)
            x2_, y2_ = elS.P(cx + pt["opening_width"] / 2 - 2, zz + 0.6)
            sh.line(x2_, y2_, x_ - 0.04, y_ + 0.03, layer=L_TAG, lw=0.35)
            sh.text(x_, y_, t_, size=5.4, layer=L_TAG)
    else:
        rr = pt["opening_width"] / 2
        co = [c["text"] for c in evb["callouts"]] if evb.get("callouts") else [
            "CRIMSON soffit, inside the arch (Shane; ref. photo)", "GOLD edge (Shane: 'gold soffit'; split TBD)",
            "E1 ENTRY GLAZING TBD (building face, behind)"]
        tg = evb.get("callout_targets") or [[9.0, 36.2], [rr - 1.8, 22.6], [6, 10.6]]     # Rev D: arch lowered
        for zz, tu, tz, t_ in ((pt["crown"] - 3, cx + tg[0][0], tg[0][1], co[0]),
                               (pt["springline"] - 4, cx + tg[1][0], tg[1][1], co[1]),
                               (pt["entry_glazing_height"] - 6, cx + tg[2][0], tg[2][1], co[2])):
            x_, y_ = elS.P(cx + pt["overall_width"] / 2 + 3, zz)
            x2_, y2_ = elS.P(tu, tz)
            sh.line(x2_, y2_, x_ - 0.04, y_ + 0.03, layer=L_TAG, lw=0.35)
            sh.text(x_, y_, t_, size=5.4, layer=L_TAG)
        cw = evb["champion_walk"]
        elS.text(cx, -3.6, f"{cw['name']} — BRICK, in front · {cw['note']}", size=5.4, bold=True, align="center", layer=L_TAG)
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
    te = (evb or {}).get("text_rev_e", {})
    elN.text(0 + te.get("tower_u", 9.5), 31.6, te.get("tower_label", "NE STAIR TOWER (+5')"), size=4.4, align="center", layer=L_TAG)
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
    for f in ev["finishes"] + ([evb["finish_brick"]] if evb else []):
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
             ("PORTAL: FREESTANDING limestone arch in front of the south entrance over the brick Champion Walk (Shane, D-043); "
              f"gap {evb['portal_freestanding']['gap_to_building']:g}' + depth ASSUMED; crimson soffit, gold edge (split TBD). Walk size + donor "
              "bricks OPEN (D-044)." if evb else
              "PORTAL: limestone, crimson inside the arch, gold soffit (Shane). Size ASSUMED from his render's proportions; projects "
              "south of the façade, depth TBD."),
             ("BRAND: official Trojan Horse Arena mark (horse-head badge, Greek key border; Shane, D-041) above the arch, "
              f"Ø {evb['mark']['diameter']:g}' ASSUMED, replaces the keystone; wordmark + side panel ASSUMED sizes. No school logo. "
              "Trademark search before signage / apparel: OPEN (D-042)." if evb else
              "BRAND: placeholders only — no school logo (Phase 2 is Shane's build, D-028). HGHS badge? OPEN (D-040)."),
             ((evb or {}).get("text_rev_e", {}).get("doors_note") or
              "DOORS: symbols (6' x 8' ASSUMED) from P2-A-101 Rev D; X# EXIT ONLY (D-033); S1 size TBD (D-034)."),
             "NOT SHOWN: ETFE roof / solar (aspirations), rooftop units, grading, lighting."]
    no = evb.get("notes_override") if evb else None
    if no:
        notes = [n for n in notes if not n.startswith(("PORTAL:", "BRAND:"))]
        notes[1:1] = [no["portal"], no["brand"], no["walk"]]
        if no.get("heights"):                      # Rev D: D-049 tier rake (highest aisle = the loop)
            notes[0] = no["heights"]
    for t_ in notes:
        y = sh.para(nx, y + 0.02, nw, t_, size=5.6, indent=0.1, bullet="·")
    fl = body_bottom + 0.06
    if y < fl:
        raise SystemExit(f"LAYOUT OVERFLOW: notes run {fl - y:.2f} in into the stamp band")
    print(f"layout margin notes (in): {y - fl:.2f}")
    return sh


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", choices=["A", "B", "C", "D", "E"], default="E")
    ap.add_argument("--png", help="optional PNG preview path (outside the repo)")
    ap.add_argument("--out-dir", help="write PDF/DXF here instead of phase2/out/{pdf,dxf}")
    ap.add_argument("--force", action="store_true", help="allow overwriting a FROZEN revision in the repo")
    a = ap.parse_args()
    p2, ev, plan, evb = load(a.rev)
    rv = p2["sheets"][SHEET_NO]["revisions"][a.rev]
    if a.out_dir:
        pdf, dxf = (Path(a.out_dir) / f"{rv['file']}.{e}" for e in ("pdf", "dxf"))
    else:
        pdf = BP / "phase2" / "out" / "pdf" / f"{rv['file']}.pdf"
        dxf = BP / "phase2" / "out" / "dxf" / f"{rv['file']}.dxf"
        if rv.get("frozen") and (pdf.exists() or dxf.exists()) and not a.force:
            sys.exit("Revision is FROZEN; use --out-dir to regenerate for checking.")
    sh = build(p2, ev, plan, evb)
    pdf.parent.mkdir(parents=True, exist_ok=True)
    dxf.parent.mkdir(parents=True, exist_ok=True)
    sh.render_pdf(pdf, title=f"{SHEET_NO} Rev {a.rev} {p2['sheets'][SHEET_NO]['title']}", png_path=a.png)
    sh.render_dxf(dxf)
    print(f"wrote {pdf}\nwrote {dxf}" + (f"\nwrote {a.png}" if a.png else ""))


if __name__ == "__main__":
    main()
