"""KEYSTONE P2-A-301 BUILDING SECTIONS (Phase 2, P2-T-009). Schematic, color.

Rev A (2026-10-04, Shane 6:45 AM CT): Section A-A (north-south, x = 100, looking west) and Section B-B (east-west,
y = 150, looking north) through the event floor, the bowl and the Level 2 loop (1/32 in = 1 ft); enlarged north bowl
edge (3/32 in = 1 ft); typical exit stair at 70 in clear (1/8 in = 1 ft); key plan with the cut lines.
Heights: params/phase2_elev.yaml (L2 15, ring roof 30, arena structure underside 36, arena roof 42 — ASSUMED; clear
>= 25 CITED, R-019). Plan geometry: params/phase2_plan_rev_d.yaml (P2-A-101/102 Rev D, frozen). Tier / stair / guard
section geometry: params/phase2_sect.yaml (CITED or ASSUMED, each value sourced). Slab, wall and roof thicknesses are
graphic only (not designed). Sight lines NOT checked (TBD). DXF is in paper inches; fills are solid HATCH entities.
Rev A FROZEN 7:24 AM CT (regenerate with --rev A --out-dir; byte-identical).
Rev B (Shane 7:24 AM CT): switchback intermediate landing 70 in = stair width (IBC 2021 1011.6, D-051) in detail 4 with the
per-stair plan footprint; under-tier use (D-049: storage / mech under the low front edge, lockers only at full height) on
A-A, B-B and detail 3; sight-line pointer to P2-A-302 and egress pointer to D-052 (R-018.9). Rev B data: sect yaml rev_b.
Usage (from the repo root):
  /workspace/.venv-keystone/bin/python blueprints/phase2/src/p2_a_301.py [--rev A|B] [--png PATH] [--out-dir DIR] [--force]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

BP = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BP / "shared"))
from titleblock import Sheet, add_titleblock, text_width_in  # noqa: E402

W, H, M = 17.0, 11.0, 0.5
SHEET_NO = "P2-A-301"
L_CUT, L_FILL, L_TAG, L_DAT, L_HID, L_GRD = ("A-SECT-CUTL", "A-SECT-FILL", "A-SECT-IDEN", "A-SECT-DATM", "A-SECT-HIDN",
                                             "A-SECT-GUAR")
# graphic colours only (materials TBD)
C = dict(cut="#3C3C3C", room="#F0ECE4", lobby="#F5E7C6", floor="#D9B77E", air="#E8F0F8", lower="#D88A8A",
         upper="#A7B3C3", loop="#C8693A", struct="#CFCFCF", stair="#BEBEBE", red="#CC0000")
SLAB = 1.0            # graphic slab / roof / wall thickness (ft) — NOT designed


REV = "A"          # set by main(); Rev B branches only (Rev A output stays byte-identical)


def load():
    p2 = yaml.safe_load((BP / "params" / "phase2.yaml").read_text(encoding="utf-8"))
    ev = yaml.safe_load((BP / "params" / "phase2_elev.yaml").read_text(encoding="utf-8"))
    plan = yaml.safe_load((BP / "params" / "phase2_plan_rev_d.yaml").read_text(encoding="utf-8"))
    sc = yaml.safe_load((BP / "params" / "phase2_sect.yaml").read_text(encoding="utf-8"))
    return p2, ev, plan, sc


# ------------------------------------------------------------------ section model (u = ft along the cut, z = ft)
class Model:
    def __init__(self):
        self.items = []

    def poly(self, pts, fill=None, lw=0.0, layer=L_FILL):
        self.items.append(("poly", [tuple(map(float, p)) for p in pts], fill, lw, layer))

    def box(self, u0, z0, u1, z1, fill=None, lw=0.0, layer=L_FILL):
        self.poly([(u0, z0), (u1, z0), (u1, z1), (u0, z1)], fill, lw, layer)

    def line(self, u0, z0, u1, z1, lw=0.6, layer=L_CUT):
        self.items.append(("line", (u0, z0), (u1, z1), lw, layer))

    def dashed(self, u0, z0, u1, z1, lw=0.4, layer=L_HID):
        self.items.append(("dash", (u0, z0), (u1, z1), lw, layer))

    def text(self, u, z, s, size=4.6, align="left", bold=False, color=None, layer=L_TAG, ko=False):
        self.items.append(("text", (u, z), s, size, align, bold, color, layer, ko))


def clip_poly(pts, u0, z0, u1, z1):
    """Sutherland-Hodgman clip of a polygon to the window."""
    def clip(ps, inside, inter):
        out = []
        for i in range(len(ps)):
            a, b = ps[i - 1], ps[i]
            ia, ib = inside(a), inside(b)
            if ib:
                if not ia:
                    out.append(inter(a, b))
                out.append(b)
            elif ia:
                out.append(inter(a, b))
        return out

    def iu(a, b, u):
        t = (u - a[0]) / (b[0] - a[0])
        return (u, a[1] + t * (b[1] - a[1]))

    def iz(a, b, z):
        t = (z - a[1]) / (b[1] - a[1])
        return (a[0] + t * (b[0] - a[0]), z)
    ps = pts
    for inside, inter in ((lambda p: p[0] >= u0, lambda a, b: iu(a, b, u0)), (lambda p: p[0] <= u1, lambda a, b: iu(a, b, u1)),
                          (lambda p: p[1] >= z0, lambda a, b: iz(a, b, z0)), (lambda p: p[1] <= z1, lambda a, b: iz(a, b, z1))):
        if not ps:
            return []
        ps = clip(ps, inside, inter)
    return ps


def clip_line(a, b, u0, z0, u1, z1):
    """Liang-Barsky."""
    (x0, y0), (x1, y1) = a, b
    dx, dy = x1 - x0, y1 - y0
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, x0 - u0), (dx, u1 - x0), (-dy, y0 - z0), (dy, z1 - y0)):
        if p == 0:
            if q < 0:
                return None
            continue
        t = q / p
        if p < 0:
            t0 = max(t0, t)
        else:
            t1 = min(t1, t)
    if t0 > t1:
        return None
    return (x0 + t0 * dx, y0 + t0 * dy), (x0 + t1 * dx, y0 + t1 * dy)


def render(sh, m, x0, y0, ft_per_in, win, text_scale=1.0, skip_text=False):
    """Draw model m with (win[0], 0) at sheet (x0, y0). win = (u0, z0, u1, z1) clip window."""
    s = 1.0 / ft_per_in
    u0w = win[0]

    def P(u, z):
        return x0 + (u - u0w) * s, y0 + z * s
    for it in m.items:
        k = it[0]
        if k == "poly":
            ps = clip_poly(it[1], *win)
            if len(ps) >= 3:
                sh.poly([P(*p) for p in ps], fill=it[2], layer=it[4], lw=it[3])
        elif k in ("line", "dash"):
            c = clip_line(it[1], it[2], *win)
            if c:
                a, b = P(*c[0]), P(*c[1])
                if k == "line":
                    sh.line(a[0], a[1], b[0], b[1], layer=it[4], lw=it[3])
                else:
                    sh.dashed(a[0], a[1], b[0], b[1], layer=it[4], lw=it[3], dash=0.05, gap=0.035)
        elif k == "text" and not skip_text:
            (u, z), st, size, align, bold, color, layer, ko = it[1:]
            if win[0] <= u <= win[2] and win[1] <= z <= win[3]:
                x, y = P(u, z)
                if ko:                                   # white knockout behind the text
                    tw = text_width_in(st, size * text_scale, bold) + 0.06
                    xl = x - tw / 2 if align == "center" else (x - tw + 0.03 if align == "right" else x - 0.03)
                    sh.prims.append(("knockout", dict(x=xl, y=y - 0.02, w=tw, h=size * text_scale / 72 * 0.95)))
                sh.text(x, y, st, size=size * text_scale, align=align, bold=bold, layer=layer, color=color)
    return P


def heights(ev):
    hz = ev["heights"]
    return (hz["l2_ff"]["value"], hz["ring_roof"]["value"], hz["arena_structure_underside"]["value"],
            hz["arena_roof_top"]["value"], hz["arena_clear_min"]["value"])


def lower_tier(m, sc, front, back):
    """Telescopic lower tier, extended; rows step up from the front (at the floor edge) toward the back."""
    lo = sc["seating"]["lower"]
    n, d, r = lo["rows"], lo["row_depth_in"] / 12, lo["rise_in"] / 12
    sgn = 1 if back > front else -1
    pts = [(front, 0)]
    for k in range(n):                                   # row k+1 deck at k * rise (row 1 at the floor)
        ua, ub = front + sgn * k * d, front + sgn * (k + 1) * d
        pts += [(ua, k * r + 0.15), (ub, k * r + 0.15)]
    pts += [(back, 0)]
    m.poly(pts, C["lower"], 0.5, L_CUT)
    # seat symbols (graphic) at each row
    for k in range(n):
        ua = front + sgn * (k + 0.55) * d
        m.line(ua, k * r + 0.15, ua, k * r + 1.4, lw=0.3, layer=L_FILL)
    return (n - 1) * r


def upper_tier(m, sc, l2, front, back):
    """Fixed upper tier stepping DOWN from the loop (back, at L2 FF) toward the arena (front). ASSUMED."""
    up = sc["seating"]["upper"]
    n, d, r = up["rows"], up["row_depth_in"] / 12, up["row_rise_in"] / 12
    sgn = 1 if back > front else -1
    zf = l2 - n * r
    pts = []
    for j in range(n):                                   # row j+1 from the front
        ua, ub = front + sgn * j * d, front + sgn * (j + 1) * d
        z = zf + j * r
        pts += [(ua, z), (ub, z)]
    pts += [(back, l2), (back, l2 - SLAB), (front, zf - SLAB)]
    m.poly(pts, C["upper"], 0.6, L_CUT)
    for j in range(n):
        ua = front + sgn * (j + 0.55) * d
        z = zf + j * r
        m.line(ua, z, ua, z + 1.4, lw=0.3, layer=L_FILL)
    # front fascia / guard (>= 26 in, 1030.17.3)
    g = sc["guards"]["tier_front_in"] / 12
    m.line(front, zf, front, zf + g, lw=1.0, layer=L_GRD)
    return zf


def guard(m, sc, u, z):
    g = sc["guards"]["loop_open_edge_in"] / 12
    m.line(u, z, u, z + g, lw=1.0, layer=L_GRD)
    m.line(u - 0.6, z + g, u + 0.6, z + g, lw=0.8, layer=L_GRD)


def roof_high(m, u0, u1, ring, us, top):
    m.box(u0, us, u1, top, C["struct"], 0.0)
    # truss-like diagonals (graphic only, not engineered)
    step = 6.0
    u = u0
    while u + step <= u1 + 1e-6:
        m.line(u, us, u + step / 2, top - SLAB, lw=0.25, layer=L_FILL)
        m.line(u + step / 2, top - SLAB, u + step, us, lw=0.25, layer=L_FILL)
        u += step
    m.box(u0, top - SLAB, u1, top, C["cut"], 0.0, L_CUT)
    m.line(u0, us, u1, us, lw=0.5)


def ring_roof(m, u0, u1, ring):
    m.box(u0, ring - SLAB, u1, ring, C["cut"], 0.0, L_CUT)


def slab(m, u0, u1, z):
    m.box(u0, z - SLAB, u1, z, C["cut"], 0.0, L_CUT)


def wall(m, u, z0, z1, side=0):
    """Cut wall, SLAB thick, centred on u (side=-1 -> inside to the right of u, +1 -> to the left)."""
    a = u - SLAB / 2 + side * SLAB / 2
    m.box(a, z0, a + SLAB, z1, C["cut"], 0.0, L_CUT)


def loop_strip(m, u0, u1, z):
    m.box(u0, z, u1, z + 0.35, C["loop"], 0.0)


def section_A(ev, plan, sc):
    """N-S at x = 100, looking west: u = y (south at the left)."""
    l2, ring, us, top, clr = heights(ev)
    m = Model()
    bx0, by0, bx1, by1 = plan["building"]["rect"]
    L = by1 - by0
    lob = plan["level_1"]["zones"][0]["rect"]          # lobby [84, 0, 142, 56]
    ob = plan["level_2"]["open_below"][0]["rect"]      # open to lobby below y 0..34
    lp_o, lp_i = plan["level_2"]["loop"]["outer"], plan["level_2"]["loop"]["inner"]
    uS, lS = plan["tiers"]["upper"]["bands"][1]["rect"], plan["tiers"]["lower"]["bands"][1]["rect"]
    uN, lN = plan["tiers"]["upper"]["bands"][0]["rect"], plan["tiers"]["lower"]["bands"][0]["rect"]
    ef = plan["event_floor"]["rect"]
    ct = plan["court"]["rect"]
    evl = plan["level_1"]["rooms"][10]
    av = ev["arena_volume"]["rect"]                    # high roof x 49..204, y 34..246
    sec = plan["level_1"]["checkpoint"]["rect"]
    # background: arena air under the high roof, lobby air (double height)
    m.box(av[1], 0, av[3], us, C["air"])
    m.box(lob[1], 0, ob[3], ring - SLAB, C["lobby"])
    zf = l2 - sc["seating"]["upper"]["rows"] * sc["seating"]["upper"]["row_rise_in"] / 12
    m.poly([(ob[3], 0), (uS[3], 0), (uS[3], zf - SLAB), (uS[1], l2 - SLAB), (ob[3], l2 - SLAB)], C["lobby"])
    m.poly([(evl["rect"][1], 0), (by1, 0), (by1, l2 - SLAB), (uN[3], l2 - SLAB), (uN[1], zf - SLAB)], C["room"])
    m.box(lp_o[3], l2, by1, ring - SLAB, C["room"])       # stretch strip (L2), under the ring roof
    # event floor
    m.box(ef[1], -0.6, ef[3], 0, C["floor"], 0.4, L_CUT)
    for u in (ct[1], ct[3]):
        m.line(u, 0, u, 0.9, lw=0.5, layer=L_TAG)
    m.text((ct[1] + ct[3]) / 2, 0.9, f"COURT {ct[3] - ct[1]:g}' (plan)", size=4.2, align="center")
    m.text((ef[1] + ct[1]) / 2 + 3, 2.2, "EVENT FLOOR", size=4.6, align="center", bold=True)
    # tiers
    lower_tier(m, sc, lS[3], lS[1])
    lower_tier(m, sc, lN[1], lN[3])
    upper_tier(m, sc, l2, uS[3], uS[1])
    upper_tier(m, sc, l2, uN[1], uN[3])
    # walls behind the lower tiers (to the upper-tier soffit)
    zf = l2 - sc["seating"]["upper"]["rows"] * sc["seating"]["upper"]["row_rise_in"] / 12
    wall(m, lS[1], 0, zf - SLAB, side=-1)
    wall(m, lN[3], 0, zf - SLAB, side=1)
    # Level 2 slabs: loop S (over the lobby), loop N + stretch
    slab(m, lp_o[1], lp_i[1], l2)
    loop_strip(m, lp_o[1], lp_i[1], l2)
    slab(m, lp_i[3], by1, l2)
    loop_strip(m, lp_i[3], lp_o[3], l2)
    guard(m, sc, ob[3], l2)                             # G-S
    # roofs, walls
    ring_roof(m, by0, av[1], ring)
    ring_roof(m, av[3], by1, ring)
    roof_high(m, av[1], av[3], ring, us, top)
    wall(m, av[1], ring - SLAB, top, side=-1)
    wall(m, av[3], ring - SLAB, top, side=1)
    wall(m, by0, 0, ring, side=-1)
    wall(m, by1, 0, ring, side=1)
    wall(m, evl["rect"][1], 0, zf - SLAB, side=1)
    m.box(by0 - 8, -1.2, by1 + 8, 0, None, 0)
    m.line(by0 - 8, 0, by0, 0, lw=1.2)
    m.line(by1, 0, by1 + 8, 0, lw=1.2)
    m.line(by0, -SLAB, by1, -SLAB, lw=0.5)
    m.dashed(sec[1], 0, sec[1], 8, lw=0.3)
    m.dashed(sec[3], 0, sec[3], 8, lw=0.3)
    m.dashed(sec[1], 8, sec[3], 8, lw=0.3)
    # labels
    m.text(17, 21.0, "LOBBY / HALL OF", size=4.6, align="center", bold=True)
    m.text(17, 18.6, "CHAMPIONS", size=4.6, align="center", bold=True)
    m.text(17, 16.2, "(double height)", size=4.2, align="center")
    m.text((sec[1] + sec[3]) / 2, 3.4, "SECURITY", size=3.8, align="center")
    m.text((sec[1] + sec[3]) / 2, 1.4, "(size TBD)", size=3.8, align="center")
    m.text(lS[3] + 1.5, 7.0, "< TELESCOPIC LOWER", size=4.4)
    m.text(uS[3] + 1.5, 11.8, "< FIXED UPPER", size=4.4)
    m.text(lN[1] - 1.5, 7.0, "TELESCOPIC LOWER >", size=4.4, align="right")
    m.text(uN[1] - 1.5, 11.8, "FIXED UPPER >", size=4.4, align="right")
    m.text((lp_o[1] + lp_i[1]) / 2, l2 + 4.6, "LOOP", size=4.2, align="center", bold=True)
    m.text((lp_i[3] + lp_o[3]) / 2, l2 + 4.6, "LOOP", size=4.2, align="center", bold=True)
    if REV == "A":
        m.text((evl["rect"][1] + by1) / 2, 5.0, "EVENT LOCKER 1", size=4.4, align="center", bold=True)
        m.text((evl["rect"][1] + by1) / 2, 2.6, "(L1, under the tier)", size=3.9, align="center")
    else:
        # D-049: storage / mech under the low front edge; lockers only under the flat L2 slab (full headroom, ASSUMED)
        m.dashed(uN[3], 0, uN[3], l2 - SLAB, lw=0.4)
        m.text((uN[1] + uN[3]) / 2, 5.0, "STORAGE /", size=4.0, align="center", bold=True)
        m.text((uN[1] + uN[3]) / 2, 2.8, "MECH (D-049)", size=4.0, align="center", bold=True)
        m.text((uN[3] + by1) / 2, 5.0, "LKR 1", size=4.0, align="center", bold=True)
        m.text((uN[3] + by1) / 2, 2.8, "full-ht part", size=3.6, align="center")
    m.text(140, top + 1.0, f"ARENA ROOF {top:g}' (ASSUMED)", size=4.6, align="center", bold=True)
    m.text(140, us + 2.0, f"LONG-SPAN STRUCTURE ZONE {us:g}'–{top:g}' (not engineered)", size=4.0, align="center", ko=True)
    m.text(18, ring + 1.0, f"RING ROOF {ring:g}' (ASSUMED)", size=4.4, align="center")
    # clear-height dimension
    m.line(155, 0, 155, us, lw=0.4, layer=L_DAT)
    for z in (0, us):
        m.line(154, z, 156, z, lw=0.4, layer=L_DAT)
    m.text(157, 22.0, f"{us:g}' TO U/S STRUCTURE (ASSUMED)", size=4.4, bold=True, layer=L_DAT)
    m.text(157, 19.4, f"≥ {clr:g}' CLEAR REQUIRED (CITED, R-019)", size=4.2, layer=L_DAT)
    m.text(by0 - 2.5, -3.6, "S", size=6.0, align="center", bold=True)
    m.text(by1 + 2.5, -3.6, "N", size=6.0, align="center", bold=True)
    return m, L


def section_B(ev, plan, sc):
    """E-W at y = 150, looking north: u = x (west at the left)."""
    l2, ring, us, top, clr = heights(ev)
    m = Model()
    bx0, by0, bx1, by1 = plan["building"]["rect"]
    L = bx1 - bx0
    bl = plan["level_1"]["rooms"][0]["rect"]           # boys locker x 0..41.75
    ac = plan["level_1"]["zones"][1]["rect"]           # athlete corridor x 41.75..56
    e4 = plan["level_1"]["rooms"][13]["rect"]          # event locker 4 x 182..204
    scr = plan["level_2"]["rooms"][0]["rect"]          # S&C x 0..49
    lp_o, lp_i = plan["level_2"]["loop"]["outer"], plan["level_2"]["loop"]["inner"]
    uE, lE = plan["tiers"]["upper"]["bands"][2]["rect"], plan["tiers"]["lower"]["bands"][2]["rect"]
    ef = plan["event_floor"]["rect"]
    av = ev["arena_volume"]["rect"]
    zf = l2 - sc["seating"]["upper"]["rows"] * sc["seating"]["upper"]["row_rise_in"] / 12
    m.box(av[0], 0, av[2], us, C["air"])
    m.box(bl[0], 0, ac[2], l2 - SLAB, C["room"])
    m.box(scr[0], l2, scr[2], ring - SLAB, C["room"])
    m.poly([(e4[0], 0), (e4[2], 0), (e4[2], l2 - SLAB), (uE[2], l2 - SLAB), (uE[0], zf - SLAB)], C["room"])
    m.box(ef[0], -0.6, ef[2], 0, C["floor"], 0.4, L_CUT)
    m.text((ef[0] + ef[2]) / 2, 2.2, "EVENT FLOOR (no west tier, Rev D)", size=4.6, align="center", bold=True)
    lower_tier(m, sc, lE[0], lE[2])
    upper_tier(m, sc, l2, uE[0], uE[2])
    wall(m, lE[2], 0, zf - SLAB, side=1)
    slab(m, bx0, lp_i[0], l2)
    loop_strip(m, lp_o[0], lp_i[0], l2)
    slab(m, lp_i[2], bx1, l2)
    loop_strip(m, lp_i[2], lp_o[2], l2)
    guard(m, sc, lp_i[0], l2)                           # G-W
    wall(m, bl[2], 0, l2 - SLAB)
    wall(m, scr[2], l2, ring - SLAB)
    ring_roof(m, bx0, av[0], ring)
    roof_high(m, av[0], av[2], ring, us, top)
    wall(m, av[0], ring - SLAB, top, side=-1)
    wall(m, bx0, 0, ring, side=-1)
    wall(m, bx1, 0, top, side=1)
    m.line(bx0 - 8, 0, bx0, 0, lw=1.2)
    m.line(bx1, 0, bx1 + 8, 0, lw=1.2)
    m.line(bx0, -SLAB, bx1, -SLAB, lw=0.5)
    m.text((bl[0] + bl[2]) / 2, 5.0, "BOYS LOCKER", size=4.4, align="center", bold=True)
    m.text((ac[0] + ac[2]) / 2, 5.0, "ATH.", size=3.9, align="center", bold=True)
    m.text((ac[0] + ac[2]) / 2, 2.8, "CORR.", size=3.9, align="center", bold=True)
    m.text((scr[0] + scr[2]) / 2, 21.0, "STRENGTH &", size=4.4, align="center", bold=True)
    m.text((scr[0] + scr[2]) / 2, 18.6, "CONDITIONING (L2)", size=4.4, align="center", bold=True)
    m.text((lp_o[0] + lp_i[0]) / 2, l2 + 4.6, "LOOP", size=4.2, align="center", bold=True)
    m.text((lp_i[2] + lp_o[2]) / 2, l2 + 4.6, "LOOP", size=4.2, align="center", bold=True)
    m.text(lE[0] - 1.5, 7.0, "TELESCOPIC LOWER >", size=4.4, align="right")
    m.text(uE[0] - 1.5, 11.8, "FIXED UPPER >", size=4.4, align="right")
    if REV == "A":
        m.text((e4[0] + e4[2]) / 2, 5.0, "EVENT LKR 4", size=4.2, align="center", bold=True)
    else:
        m.dashed(uE[2], 0, uE[2], l2 - SLAB, lw=0.4)
        m.text((uE[0] + uE[2]) / 2, 5.0, "STOR. /", size=3.8, align="center", bold=True)
        m.text((uE[0] + uE[2]) / 2, 2.8, "MECH", size=3.8, align="center", bold=True)
        m.text((uE[2] + e4[2]) / 2, 9.0, "LKR 4", size=3.4, align="center", bold=True)
        m.text((uE[2] + e4[2]) / 2, 7.0, "7' full", size=3.2, align="center")
        m.text((uE[2] + e4[2]) / 2, 5.2, "ht part", size=3.2, align="center")
    m.text(125, top + 1.0, f"ARENA ROOF {top:g}' (ASSUMED)", size=4.6, align="center", bold=True)
    m.text(125, us + 2.0, f"LONG-SPAN STRUCTURE ZONE {us:g}'–{top:g}' (not engineered)", size=4.0, align="center", ko=True)
    m.text(24.5, ring + 1.0, f"RING ROOF {ring:g}' (ASSUMED)", size=4.4, align="center")
    m.text(lp_i[0] + 1.2, l2 + 1.4, "42\" GUARD (G-W)", size=3.9, layer=L_GRD)
    m.line(100, 0, 100, us, lw=0.4, layer=L_DAT)
    for z in (0, us):
        m.line(99, z, 101, z, lw=0.4, layer=L_DAT)
    m.text(102, 22.0, f"{us:g}' TO U/S STRUCTURE (ASSUMED)", size=4.4, bold=True, layer=L_DAT)
    m.text(102, 19.4, f"≥ {clr:g}' CLEAR REQUIRED (CITED, R-019)", size=4.2, layer=L_DAT)
    m.text(bx0 - 2.5, -3.6, "W", size=6.0, align="center", bold=True)
    m.text(bx1 + 2.5, -3.6, "E", size=6.0, align="center", bold=True)
    return m, L


def datums(sh, P, ev, x_lab, size=4.6, long=False, u_line=None, short=False):
    l2, ring, us, top, _ = heights(ev)
    rows = [(0, "L1 FF 0'", "L1 FF 0'-0\" (DATUM)"), (l2, f"L2 {l2:g}' A", f"L2 FF {l2:g}'-0\" (ASSUMED)"),
            (ring, f"RING {ring:g}' A", f"T.O. RING ROOF {ring:g}'-0\" (ASSUMED)"),
            (us, f"U/S {us:g}' A", f"U/S ARENA STRUCT. {us:g}'-0\" (ASSUMED)"),
            (top, f"ROOF {top:g}' A", f"T.O. ARENA ROOF {top:g}'-0\" (ASSUMED)")]
    if short:
        rows = [(z, f"{z:g}'", f"{z:g}'") for z, _, _ in rows]
    for z, s_, l_ in rows:
        x, y = P(u_line, z)
        sh.line(x_lab + 0.03, y, x - 0.03, y, layer=L_DAT, lw=0.35)
        sh.text(x_lab, y - 0.022, l_ if long else s_, size=size, align="right", layer=L_DAT)


def title(sh, x, y, num, name, scale, width):
    sh.text(x, y, f"{num}  {name}", size=7.2, bold=True)
    sh.line(x, y - 0.05, x + width, y - 0.05, lw=0.8)
    sh.text(x, y - 0.17, scale, size=5.4)


def bowl_detail_annot(sh, P, ev, plan, sc):
    """Annotations for the enlarged north bowl edge (detail 3)."""
    l2, ring, us, top, clr = heights(ev)
    lo, up = sc["seating"]["lower"], sc["seating"]["upper"]
    lN, uN = plan["tiers"]["lower"]["bands"][0]["rect"], plan["tiers"]["upper"]["bands"][0]["rect"]
    lp_o, lp_i = plan["level_2"]["loop"]["outer"], plan["level_2"]["loop"]["inner"]
    zf = l2 - up["rows"] * up["row_rise_in"] / 12
    ts = lo["top_seat_height_in"] / 12

    def T(u, z, s, size=5.0, **kw):
        x, y = P(u, z)
        sh.text(x, y, s, size=size, layer=kw.pop("layer", L_TAG), **kw)

    def leader(u0, z0, u1, z1):
        a, b = P(u0, z0), P(u1, z1)
        sh.line(a[0], a[1], b[0], b[1], layer=L_TAG, lw=0.35)
    # lower tier
    T(197, 12.6, "TELESCOPIC LOWER TIER (extended)", 5.2, bold=True)
    T(197, 11.2, f"{lo['rows']} rows × {lo['row_depth_in']}\" = {lo['band_ft']}' band (R-008 / plan)", 4.8)
    T(197, 9.8, "rise 11⅝\"/row — Hussey MAXAM option (CITED);", 4.8)
    T(197, 8.4, "choice of 11⅝\" ASSUMED", 4.8)
    leader(205.0, 7.9, lN[1] + 4, 2.4)
    # top seat height tick
    a, b = P(lN[3] - 1.0, ts), P(lN[3] + 0.0, ts)
    sh.line(a[0] - 0.05, a[1], b[0], b[1], layer=L_DAT, lw=0.5)
    T(197, 6.1, "top seat 6'-3⅛\" (Hussey, 6 rows @ 11⅝\")", 4.4, layer=L_DAT)
    leader(213.2, 6.4, lN[3] - 1.2, ts)
    # closed depth bracket
    cd = lo["closed_depth_in"] / 12
    a, b = P(lN[3] - cd, -0.9), P(lN[3], -0.9)
    sh.line(a[0], a[1], b[0], b[1], layer=L_DAT, lw=0.5)
    for q in (a, b):
        sh.line(q[0], q[1] - 0.03, q[0], q[1] + 0.03, layer=L_DAT, lw=0.5)
    T(lN[3] - cd - 0.3, -2.3, "closed 3'-6\" (Hussey, 6 rows)", 4.4, align="right", layer=L_DAT)
    # upper tier
    T(197, 25.5, "FIXED UPPER TIER (ASSUMED rake)", 5.2, bold=True)
    T(197, 24.1, f"{up['rows']} rows × {up['row_depth_in']}\" = {up['band_ft']}' band (plan)", 4.8)
    T(197, 22.7, f"{up['row_rise_in']}\"/row = 2 aisle risers × {up['aisle_riser_in']}\", {up['aisle_tread_in']}\" treads", 4.8)
    T(197, 21.3, "(IBC 1030.14.2: 4–8\" risers, ≥ 11\" treads)", 4.8)
    T(197, 19.9, f"steps DOWN from the loop; front row {zf:.2f}'", 4.8)
    leader(212.0, 19.5, uN[1] + 5, zf + 2.6)
    T(uN[1] - 0.4, zf + 3.0, "≥ 26\" fascia (1030.17.3)", 4.4, align="right", layer=L_GRD)
    # loop / stretch / guards
    T((lp_i[3] + lp_o[3]) / 2, l2 + 5.4, "LOOP 7'", 5.0, align="center", bold=True)
    T((lp_i[3] + lp_o[3]) / 2, l2 + 4.0, "2 × 42\" lanes", 4.4, align="center")
    T((lp_i[3] + lp_o[3]) / 2, l2 + 2.6, "top cross aisle", 4.4, align="center")
    T((lp_o[3] + 252) / 2, l2 + 9.0, "STRETCH", 4.2, align="center")
    T((lp_o[3] + 252) / 2, l2 + 7.8, "6' (L2)", 4.2, align="center")
    # L1 headroom
    if REV == "A":
        T(uN[1] + 2.0, 4.6, "L1 headroom under the tier front", 4.6, color=C["red"])
        T(uN[1] + 2.0, 3.4, f"≈ {zf:.1f}' less tier structure — TBD", 4.6, color=C["red"])
        T(uN[1] + 2.0, 1.6, "EVENT LOCKER 1 (L1)", 4.6, bold=True)
        # sight lines
        T(197, 32.4, "SIGHT LINES: NOT CHECKED — TBD", 5.2, bold=True, color=C["red"])
        T(197, 31.0, "(C-value, eye height, focal point not set)", 4.6, color=C["red"])
    else:
        T(uN[1] + 1.9, 6.0, "UNDER-TIER (D-049): STORAGE / MECH", 4.4, bold=True, color=C["red"])
        T(uN[1] + 1.9, 4.8, f"front {zf:.2f}' less structure; exits under it", 4.2, color=C["red"])
        T(uN[1] + 1.9, 3.6, "need ≥ 7'-6\" ceiling (1003.2)", 4.2, color=C["red"])
        T(uN[3] + 0.6, 1.6, "LOCKER (full ht)", 4.2, bold=True)
        T(197, 32.4, "SIGHT LINES: see P2-A-302 — upper 14\"/row FAILS", 5.2, bold=True, color=C["red"])
        T(197, 31.0, "(C < 60 mm); proposed 19\"/row, front 7.08' (D-053 OPEN)", 4.6, color=C["red"])
    # roof note
    T(222, us - 2.0, f"1030.6.2.2 (only if smoke-protected): roof ≥ 15' above", 4.4, layer=L_DAT)
    T(222, us - 3.3, f"highest aisle (loop {l2:g}') → ≥ {l2 + 15:g}'; {us:g}' drawn", 4.4, layer=L_DAT)


def stair_detail(sh, x0, y0, sc, ev):
    st = sc["stair"]
    fpi = 8.0
    s = 1.0 / fpi
    r, t = st["riser_in"] / 12, st["tread_in"] / 12
    n_r = st["risers"] // st["flights"]
    land = st["landing_depth_in"] / 12
    land_m = land if REV == "A" else sc["rev_b"]["intermediate_landing_in"] / 12
    run = st["run_per_flight_in"] / 12
    rise = st["rise_ft"]

    def P(u, z):
        return x0 + u * s, y0 + z * s
    L = land + run + land_m
    # floors
    for z0, z1, u0, u1 in ((-SLAB, 0, -2, L + 1), (rise - SLAB, rise, -2, land)):
        sh.poly([P(u0, z0), P(u1, z0), P(u1, z1), P(u0, z1)], fill=C["cut"], layer=L_CUT, lw=0)
    # mid landing
    zm = n_r * r
    sh.poly([P(land + run, zm - 0.6), P(L, zm - 0.6), P(L, zm), P(land + run, zm)], fill=C["cut"], layer=L_CUT, lw=0)
    # flight 1 (cut)
    pts = [(land, 0)]
    z = 0.0
    u = land
    for k in range(n_r):
        z += r
        pts.append((u, z))
        if k < n_r - 1:
            u += t
            pts.append((u, z))
    pts += [(land + run, zm - 0.6), (land + 0.2, -0.0)]
    sh.poly([P(*p) for p in pts], fill=C["stair"], layer=L_CUT, lw=0.6)
    # flight 2 (beyond, dashed)
    z = zm
    u = land + run
    prev = P(u, z)
    for k in range(n_r):
        z += r
        a = P(u, z)
        sh.dashed(prev[0], prev[1], a[0], a[1], layer=L_HID, lw=0.35, dash=0.04, gap=0.03)
        if k < n_r - 1:
            b = P(u - t, z)
            sh.dashed(a[0], a[1], b[0], b[1], layer=L_HID, lw=0.35, dash=0.04, gap=0.03)
            u -= t
            prev = b
    # walls
    for u_ in (-1.0, L):
        sh.poly([P(u_, -SLAB), P(u_ + 1.0, -SLAB), P(u_ + 1.0, rise + 1.5), P(u_, rise + 1.5)], fill=C["cut"], layer=L_CUT, lw=0)
    # annotations
    def T(u, z, s_, size=4.8, **kw):
        x, y = P(u, z)
        sh.text(x, y, s_, size=size, layer=L_TAG, **kw)
    T(land + run / 2 + 2.6, 2.0, f"{n_r} R @ {st['riser_in']}\" = {n_r * st['riser_in'] / 12:.2f}'", 4.6)
    T(land + run / 2 + 2.6, 0.8, f"{st['treads_per_flight']} T @ {st['tread_in']}\" = {run:g}'", 4.6)
    if REV == "A":
        T(land + run + land / 2, zm + 0.8, f"{st['landing_depth_in']}\" landing", 4.2, align="center")
    else:
        T(land + run + land_m / 2, zm + 2.0, f"{sc['rev_b']['intermediate_landing_in']}\" mid", 4.2, align="center", bold=True)
        T(land + run + land_m / 2, zm + 0.8, "landing", 4.2, align="center", bold=True)
        T(land + run + land_m / 2, zm - 1.8, "= width", 4.0, align="center")
        T(land + run + land_m / 2, zm - 3.0, "(1011.6)", 4.0, align="center")
        T(land / 2, 3.0, f"{sc['rev_b']['floor_landing_in']}\" floor", 4.0, align="center")
        T(land / 2, 1.8, "landing", 4.0, align="center")
    T(land / 2, rise + 0.6, "L2 FF 15' (A)", 4.2, align="center")
    T(land / 2, 0.6, "L1 FF 0'", 4.2, align="center")
    T(0.3, rise - 4.2, "flight 2 beyond", 4.4)
    T(0.3, rise - 5.5, "(dashed)", 4.4)
    T(0.3, rise - 7.4, f"{st['risers']} risers total", 4.4)
    T(0.3, rise - 8.7, f"{st['clear_width_in']}\" clear width", 4.4, bold=True)
    T(0.3, rise - 10.0, "(not visible in section)", 4.0)
    return P(L + 1.0, 0)[0]


def key_plan(sh, x0, y0, plan, sc):
    fpi = sc["scales"]["key_plan_ft_per_in"]
    s = 1.0 / fpi

    def P(x, y):
        return x0 + x * s, y0 + y * s
    bx0, by0, bx1, by1 = plan["building"]["rect"]
    pj = plan["building"]["projection"]["rect"]
    for r_, f_ in ((plan["building"]["rect"], C["room"]), (pj, C["room"]), (plan["arena_volume"]["rect"], C["air"]),
                   (plan["event_floor"]["rect"], C["floor"])):
        sh.poly([P(r_[0], r_[1]), P(r_[2], r_[1]), P(r_[2], r_[3]), P(r_[0], r_[3])], fill=f_, layer=L_FILL, lw=0.5)
    for b in plan["tiers"]["lower"]["bands"]:
        r_ = b["rect"]
        sh.poly([P(r_[0], r_[1]), P(r_[2], r_[1]), P(r_[2], r_[3]), P(r_[0], r_[3])], fill=C["lower"], layer=L_FILL, lw=0)
    for b in plan["tiers"]["upper"]["bands"]:
        r_ = b["rect"]
        sh.poly([P(r_[0], r_[1]), P(r_[2], r_[1]), P(r_[2], r_[3]), P(r_[0], r_[3])], fill=C["upper"], layer=L_FILL, lw=0)
    ca, cb = sc["cuts"]["A"]["plane"]["at"], sc["cuts"]["B"]["plane"]["at"]
    a, b = P(ca, by0 - 14), P(ca, by1 + 14)
    sh.dashed(a[0], a[1], b[0], b[1], layer=L_CUT, lw=0.7, dash=0.08, gap=0.04)
    a2, b2 = P(bx0 - 14, cb), P(bx1 + 14, cb)
    sh.dashed(a2[0], a2[1], b2[0], b2[1], layer=L_CUT, lw=0.7, dash=0.08, gap=0.04)
    # view arrows: A-A looks west (-x), B-B looks north (+y)
    for (px, py) in (a, b):
        sh.poly([(px, py + 0.05), (px - 0.12, py), (px, py - 0.05)], fill="#000000", layer=L_CUT, lw=0)
        sh.text(px + 0.04, py - 0.025, "A", size=5.6, bold=True)
    for (px, py) in (a2, b2):
        sh.poly([(px - 0.05, py), (px, py + 0.12), (px + 0.05, py)], fill="#000000", layer=L_CUT, lw=0)
        sh.text(px, py - 0.11, "B", size=5.6, bold=True, align="center")
    n0 = P(bx1 + 30, by1 - 30)
    sh.line(n0[0], n0[1] - 0.18, n0[0], n0[1] + 0.12, lw=0.8)
    sh.poly([(n0[0] - 0.04, n0[1] + 0.06), (n0[0], n0[1] + 0.16), (n0[0] + 0.04, n0[1] + 0.06)], fill="#000000", lw=0)
    sh.text(n0[0], n0[1] + 0.2, "N", size=6, bold=True, align="center")
    return P(bx1, by1)


NOTES1 = [
    ("HEIGHTS USED (ft above L1 FF 0'-0\")", None),
    ("L2 FF 15' — ASSUMED (R-015, 15 ft floor-to-floor).", "•"),
    ("Ring roof 30' — ASSUMED (L2 + 15 ft).", "•"),
    ("Arena structure underside 36' — ASSUMED; ≥ 25' clear over the floor is CITED (R-019: NFHS via Draper, LA RAP) → 11' margin.", "•"),
    ("Arena roof top 42' — ASSUMED (36' + 6' long-span structure zone, not engineered).", "•"),
    ("Slab, wall and roof thicknesses are graphic only (not designed). Parapets TBD.", "•"),
    ("SEATING", None),
    ("Lower tier: telescopic, 6 rows × 24\" (R-008, plan Rev D 12' band). Hussey MAXAM rises 9⅝\", 11⅝\", 16\" (CITED); 11⅝\" drawn (ASSUMED choice): top seat 6'-3⅛\", closed 3'-6\" (Hussey tables). Hussey open depth at 24\" is 11'-3\" vs the 12' band.", "•"),
    ("Upper tier: fixed, 15' band (plan); 5 rows × 36\", 14\"/row (2 × 7\" aisle risers, 18\" treads) — ASSUMED, within IBC 2021 1030.14.2. Steps DOWN from the loop (L2 FF = top cross aisle) to a 9.17' front row. Not drawn: tier on the L2 deck rising to ≈ 21' (the 36' basis in phase2_elev.yaml).", "•"),
    ("L1 headroom under the upper-tier front ≈ 9.2' less structure — TBD (architect / structural).", "•"),
    ("SIGHT LINES: NOT CHECKED — TBD. Rows and rises are placeholders until a sight-line study (C-value, eye height, focal point).", "•"),
]
NOTES2 = [
    ("GUARDS", None),
    ("Loop open edges G-W (x = 56) and G-S (y = 34): 42\" guards, IBC 2021 1015.2 / 1015.3.", "•"),
    ("Upper-tier front: sightline-constrained fascia ≥ 26\" (1030.17.3); 36\" at the foot of aisles (1030.17.4). Type TBD.", "•"),
    ("STAIRS (ST-1..ST-4)", None),
    ("70\" clear — D-038 CLOSED (Shane 6:45 AM CT). Handrail projections ≤ 4½\" each side (1014.8): architect to confirm how 'clear' is measured.", "•"),
    ("26 risers @ 6.92\" (15' ÷ 26), 2 flights of 13, 11\" treads, 48\" landings (1011.5.2, 1011.6). Stairs are not on cut A-A or B-B; typical shown.", "•"),
    ("Plan effect at the next A-101/A-102 revision: ≈ 11.67' × 19' ≈ 221.7 SF per stair per level (+16.5 SF); egress recheck R-018.8. The frozen set stays frozen.", "•"),
    ("ROOF HEIGHT (IBC 2021 1030.6.2.2)", None),
    ("Applies only if smoke-protected seating is used: lowest roof deck ≥ 15' above the highest aisle. Highest aisle = the loop at 15' → ≥ 30'; 36' drawn.", "•"),
    ("CUTS", None),
    ("A-A: x = 100, looking west (south at left). B-B: y = 150, looking north (west at left). Geometry from P2-A-101/102 Rev D (frozen).", "•"),
    ("Colors are graphic only; materials TBD. 'A' = ASSUMED.", "•"),
]


def notes_b():
    """Rev B notes: Rev A lists with the changed entries swapped in place."""
    n1 = list(NOTES1)
    n1[n1.index(("L1 headroom under the upper-tier front ≈ 9.2' less structure — TBD (architect / structural).", "•"))] = (
        "UNDER THE UPPER TIER (D-049 DECIDED): steps DOWN from the loop as drawn; under the low front edge: telescopic stack "
        "(at the tier face), storage, mechanical. Lockers only where headroom is full (under the flat L2 slab — ASSUMED reading). "
        "Front ≈ 9.2' less structure; exit passages under it need ≥ 7'-6\" (1003.2). Event lockers 1–4 re-planned at the next A-101.", "•")
    n1[n1.index(("SIGHT LINES: NOT CHECKED — TBD. Rows and rises are placeholders until a sight-line study (C-value, eye height, focal point).", "•"))] = (
        "SIGHT LINES: P2-A-302 Rev A. Rake unchanged here pending Shane: upper 14\"/row fails (C < 60 mm); proposed 19\"/row + east "
        "tier 6' further out (D-053 OPEN). Closed stack recessed under the tier front conflicts — keep it at the tier face.", "•")
    n2 = list(NOTES2)
    n2[n2.index(("26 risers @ 6.92\" (15' ÷ 26), 2 flights of 13, 11\" treads, 48\" landings (1011.5.2, 1011.6). Stairs are not on cut A-A or B-B; typical shown.", "•"))] = (
        "26 risers @ 6.92\" (15' ÷ 26), 2 flights of 13, 11\" treads (1011.5.2). Intermediate (switchback) landing 70\" = stair width "
        "(1011.6 width rule at the 180° turn; 48\" = straight-run depth) — D-051; floor landings 48\". Typical shown (not on A-A / B-B).", "•")
    n2[n2.index(("Plan effect at the next A-101/A-102 revision: ≈ 11.67' × 19' ≈ 221.7 SF per stair per level (+16.5 SF); egress recheck R-018.8. The frozen set stays frozen.", "•"))] = (
        "Per stair: 11.67' × 20.83' (2 × 70\" by 48 + 132 + 70\") = 243.1 SF per level, clear — +37.9 SF vs the frozen 10.8' × 19' "
        "(205.2); × 4 stairs × 2 levels ≈ +303 GSF at the next A-101/A-102 revision. Egress worst case still 12.4\" short: "
        "proposed 4 × 76\" stairs (D-052 OPEN, R-018.9) — not drawn.", "•")
    return n1, n2


def notes(sh, x, y_top, width, items, floor, size=6.6):
    y = y_top
    for s_, b in items:
        if b is None:
            y -= 0.05
            y = sh.para(x, y, width, s_, size=size + 0.6, bold=True)
        else:
            y = sh.para(x, y, width, s_, size=size, indent=0.10, bullet=b)
    if y < floor:
        raise SystemExit(f"LAYOUT OVERFLOW: notes column bottom {y:.2f} in < {floor:.2f} in")
    return y


def legend(sh, x, y):
    items = [("cut", "CUT: slab / wall / roof (graphic)"), ("air", "ARENA VOLUME"), ("floor", "EVENT FLOOR"),
             ("lower", "TELESCOPIC LOWER TIER"), ("upper", "FIXED UPPER TIER"), ("loop", "LOOP (L2)"),
             ("lobby", "LOBBY"), ("room", "ROOMS / SUPPORT"), ("struct", "LONG-SPAN STRUCTURE ZONE")]
    for i, (k, lab) in enumerate(items):
        cx = x + (i % 3) * 2.15
        cy = y - (i // 3) * 0.17
        sh.poly([(cx, cy), (cx + 0.22, cy), (cx + 0.22, cy + 0.11), (cx, cy + 0.11)], fill=C[k], layer=L_FILL, lw=0.3)
        sh.text(cx + 0.28, cy + 0.015, lab, size=5.0)
    return y - 3 * 0.17


def build(p2, ev, plan, sc):
    meta2, sm = p2["meta"], sc["meta"]
    sh = Sheet(W, H)
    body_bottom = add_titleblock(sh, {
        "project": f"{meta2['project']}\n{meta2['arena_name']} · {meta2['location']}",
        "phase": "PHASE 2",
        "title": "BUILDING SECTIONS\nSCHEMATIC · COLOR",
        "scale": "AS NOTED",
        "date": meta2["sheet_date"],
        "revision": sm["revision"] if REV == "A" else sc["rev_b"]["revision"],
        "drawn_by": meta2["drawn_by"],
        "sheet_no": SHEET_NO,
        "stamp": meta2["stamp"],
    }, margin=M, tb_h=0.95, stamp_h=0.40)
    s32 = sc["scales"]["sections_ft_per_in"]
    l2, ring, us, top, clr = heights(ev)
    # ---- 1: Section A-A
    mA, LA = section_A(ev, plan, sc)
    xA, yA = 1.25, 8.30
    PA = render(sh, mA, xA, yA, s32, (-4, -5, LA + 4, top + 2.5))
    datums(sh, PA, ev, xA - 0.06, size=4.4, u_line=-4)
    title(sh, xA + 0.2, yA - 0.36, "1", sc["cuts"]["A"]["name"] + " — looking west", "1/32\" = 1'-0\"  ·  x = 100 (see key plan)", 4.6)
    # ---- 2: Section B-B
    mB, LB = section_B(ev, plan, sc)
    xB, yB = 9.80, 8.30
    PB = render(sh, mB, xB, yB, s32, (-4, -5, LB + 4, top + 2.5))
    datums(sh, PB, ev, xB - 0.04, size=4.4, u_line=-4, short=True)
    title(sh, xB + 0.2, yB - 0.36, "2", sc["cuts"]["B"]["name"] + " — looking north", "1/32\" = 1'-0\"  ·  y = 150 (see key plan)", 4.4)
    right_B = PB(LB + 4, 0)[0]
    if right_B > W - M - 0.05:
        raise SystemExit(f"LAYOUT OVERFLOW: section B-B right edge {right_B:.2f} in")
    # ---- 3: enlarged north bowl edge (part of A-A)
    fd = sc["scales"]["bowl_detail_ft_per_in"]
    xD, yD = 1.45, 2.75
    win = (196, -3.5, 254, top + 1.6)
    PD = render(sh, mA, xD, yD, fd, win, text_scale=0, skip_text=True)
    datums(sh, PD, ev, xD - 0.08, size=4.6, long=False, u_line=196)
    bowl_detail_annot(sh, PD, ev, plan, sc)
    a_, b_ = PD(254, top + 1.6)
    if b_ > yA - 0.75 or a_ > 7.05:
        raise SystemExit(f"LAYOUT OVERFLOW: bowl detail top/right {a_:.2f}, {b_:.2f}")
    title(sh, xD, yD - 0.55, "3", "NORTH BOWL EDGE (ENLARGED PART OF A-A)", "3/32\" = 1'-0\"  ·  y 196–252 at x = 100", 4.9)
    # ---- 4: typical stair
    xs, ys = (7.40, 5.25) if REV == "A" else (7.20, 5.25)
    right_s = stair_detail(sh, xs, ys, sc, ev)
    if right_s > 9.95:
        raise SystemExit(f"LAYOUT OVERFLOW: stair detail right {right_s:.2f}")
    if REV == "A":
        title(sh, xs - 0.1, ys - 0.33, "4", "TYPICAL EXIT STAIR — 70\" CLEAR", "1/8\" = 1'-0\"  ·  D-038 CLOSED", 2.3)
    else:
        if xs - 0.25 < a_ + 0.02:
            raise SystemExit(f"LAYOUT OVERFLOW: stair detail left {xs - 0.25:.2f} vs bowl detail right {a_:.2f}")
        title(sh, xs - 0.1, ys - 0.33, "4", "TYPICAL EXIT STAIR — 70\" CLEAR", "1/8\" = 1'-0\" · 70\" mid landing (D-051) · 11.67' × 20.83' plan", 2.6)
    # ---- 5: key plan
    xk, yk = 7.75, 2.55
    tr = key_plan(sh, xk, yk, plan, sc)
    if tr[1] > ys - 0.55:
        raise SystemExit(f"LAYOUT OVERFLOW: key plan top {tr[1]:.2f}")
    title(sh, xk - 0.3, yk - 0.30, "5", "KEY PLAN — CUTS", "1\" = 128'  ·  north up", 1.9)
    # ---- notes
    xn = 10.15
    y = legend(sh, xn, 7.30)
    y -= 0.08
    n1, n2 = (NOTES1, NOTES2) if REV == "A" else notes_b()
    yb1 = notes(sh, xn, y, 3.05, n1, body_bottom + 0.06)
    yb2 = notes(sh, xn + 3.2, y, 3.0, n2, body_bottom + 0.06)
    print(f"notes bottoms {yb1:.2f} / {yb2:.2f}; body_bottom {body_bottom:.2f}")
    return sh


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", choices=["A", "B"], default="B")
    ap.add_argument("--png", help="optional PNG preview path (outside the repo)")
    ap.add_argument("--out-dir", help="write PDF/DXF here instead of phase2/out/{pdf,dxf}")
    ap.add_argument("--force", action="store_true", help="allow overwriting a FROZEN revision in the repo")
    a = ap.parse_args()
    global REV
    REV = a.rev
    p2, ev, plan, sc = load()
    rv = p2["sheets"][SHEET_NO]["revisions"][a.rev]
    if a.out_dir:
        pdf, dxf = (Path(a.out_dir) / f"{rv['file']}.{e}" for e in ("pdf", "dxf"))
    else:
        pdf = BP / "phase2" / "out" / "pdf" / f"{rv['file']}.pdf"
        dxf = BP / "phase2" / "out" / "dxf" / f"{rv['file']}.dxf"
        if rv.get("frozen") and (pdf.exists() or dxf.exists()) and not a.force:
            sys.exit("Revision is FROZEN; use --out-dir to regenerate for checking.")
    sh = build(p2, ev, plan, sc)
    pdf.parent.mkdir(parents=True, exist_ok=True)
    dxf.parent.mkdir(parents=True, exist_ok=True)
    sh.render_pdf(pdf, title=f"{SHEET_NO} Rev {a.rev} {p2['sheets'][SHEET_NO]['title']}", png_path=a.png)
    sh.render_dxf(dxf)
    print(f"wrote {pdf}\nwrote {dxf}" + (f"\nwrote {a.png}" if a.png else ""))


if __name__ == "__main__":
    main()
