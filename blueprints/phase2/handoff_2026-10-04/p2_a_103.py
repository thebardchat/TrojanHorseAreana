"""KEYSTONE P2-A-103 FLOOR OVERLAYS — MATS, SEATING + FLOOR CONVERSIONS (Phase 2, BACKLOG P2-T-005). Tabloid, AS NOTED.

Rev A (2026-10-04, Shane 11:45 AM CT): overlays on the P2-A-101 Rev G plan.
  (a) wrestling: 4 x 42 ft mats 2 x 2, NFHS clearances measured on the layout (R-005); tables / benches ASSUMED.
  (b) basketball: the one court already in params (NFHS 84 x 50 + 10 ft runout, R-012); volleyball / 2nd court TBD (not drawn).
  (c) telescopic lower tier open (extended 12 ft) vs closed (3'-6" stack at the upper-tier face): floor zones.
  (d) event-floor occupancy cases from P2-G-002 Rev A as hatched zones with layout notes; D-054 OPEN.
Rev B (2026-10-04, Shane 1:21 / 1:22 PM CT, P2-T-012): plan Rev H; D-054 DECIDED chairs-only design case; posted loads (1004.9);
  standing marked "not a use" (exit margin only); D-067 storage annex + its route to the floor; D-065 screening bay noted.
Data: params/phase2_overlays.yaml, params/phase2_plan_rev_g.yaml, params/phase2_code.yaml (via p2_g_002.compute);
  Rev B: + params/phase2_overlays_rev_b.yaml, phase2_plan_rev_h.yaml, phase2_code_rev_b.yaml.
Rev C (2026-10-04, Shane via Claude Code session): plan Rev I; D-069 closed + D-070 (core 2 east): the chair layouts (tables + chairs,
  chairs only) keep an 8 ft cross-aisle on the V2 line open, floor -> V2 -> EXIT (E) + core-2 corridor. Data: + phase2_overlays_rev_c.yaml,
  phase2_plan_rev_i.yaml, phase2_code_rev_c.yaml (loads unchanged).
Usage (from the repo root):
  /workspace/.venv-keystone/bin/python blueprints/phase2/src/p2_a_103.py [--rev A|B] [--png PATH] [--out-dir DIR] [--force] [--print]
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
from titleblock import Sheet, add_titleblock  # noqa: E402
import p2_g_002 as g2  # noqa: E402

W, H, M = 17.0, 11.0, 0.5
SHEET_NO = "P2-A-103"
RED, GRN, GRY, BLU = "#CC0000", "#1E7B34", "#555555", "#1F4E8C"
L_WALL, L_TIER, L_MAT, L_FURN, L_COURT, L_HATCH, L_TAG, L_DIM, L_ZONE = ("A-WALL", "A-SEAT-TELE", "A-EQPM-MATS", "A-FURN",
                                                                       "A-FLOR-CRT", "A-HATCH", "A-ANNO-TEXT", "A-ANNO-DIMS", "A-AREA-ZONE")
CASE_NAMES = {"sports": "SPORTS", "tables": "TABLES + CHAIRS", "chairs": "CHAIRS ONLY", "standing": "STANDING"}


def rd(n):
    return yaml.safe_load((BP / "params" / n).read_text(encoding="utf-8"))


def r1(a):
    return int(math.floor(a + 0.5))


def ceil_div(a, f):
    return -(-r1(a) // f)


def compute(rev="A"):
    ov, plan = rd("phase2_overlays.yaml"), rd("phase2_plan_rev_g.yaml")
    rb = None
    if rev in ("B", "C"):
        rb = rd("phase2_overlays_rev_b.yaml" if rev == "B" else "phase2_overlays_rev_c.yaml")
        plan = rd(Path(rb["basis"]["plan"]).name)
        d = g2.compute(rev=rev)
    else:
        d = g2.compute()
    fl = plan["event_floor"]["rect"]
    wr = ov["wrestling"]
    m = wr["mat_ft"]
    mats = {q["id"]: [q["origin"][0], q["origin"][1], q["origin"][0] + m, q["origin"][1] + m] for q in plan["mats"]}
    xs = sorted({r[0] for r in mats.values()} | {r[2] for r in mats.values()})
    ys = sorted({r[1] for r in mats.values()} | {r[3] for r in mats.values()})
    gaps_x = [xs[0] - fl[0], xs[2] - xs[1], fl[2] - xs[3]]        # W, between, E
    gaps_y = [ys[0] - fl[1], ys[2] - ys[1], fl[3] - ys[3]]        # S, between, N
    circle_safety = (m - wr["circle_min_ft"]) / 2
    # furniture: tables / benches per mat
    fu = wr["furniture"]
    td, bd, off = fu["table"]["depth_ft"], fu["bench"]["depth_ft"], fu["offset_ft"]
    furn, t_mat, b_mat, b_tab = [], [], [], []
    keep = [("portal", 107.0, 119.0, "S"), ("V1", 123.85, 131.85, "N")]
    for o in plan["tiers"]["lower"]["openings"]:
        if o["id"] == "PORTAL":
            keep[0] = ("portal", o["rect"][0], o["rect"][2], "S")
        if o["id"] == "V1":
            keep[1] = ("V1", o["rect"][0], o["rect"][2], "N")
    clash = []
    for s in fu["sets"]:
        r = mats[s["mat"]]
        if s["side"] == "S":
            y1 = r[1] - off
            yt, yb = (y1 - td, y1), (y1 - bd, y1)
            t_mat.append(r[1] - y1)
        else:
            y0 = r[3] + off
            yt, yb = (y0, y0 + td), (y0, y0 + bd)
            t_mat.append(y0 - r[3])
        tx = s["table_x"]
        furn.append(("table", [tx[0], yt[0], tx[1], yt[1]]))
        for bx in s["benches_x"]:
            furn.append(("bench", [bx[0], yb[0], bx[1], yb[1]]))
            b_mat.append(t_mat[-1])
            b_tab.append(max(tx[0] - bx[1], bx[0] - tx[1]))
            for nm, k0, k1, side in keep:
                if side == s["side"] and bx[0] < k1 and bx[1] > k0:
                    clash.append(f"{s['mat']} bench {bx} hits {nm}")
            if bx[0] < fl[0] or bx[1] > fl[2]:
                clash.append(f"{s['mat']} bench {bx} off the floor")
        for nm, k0, k1, side in keep:
            if side == s["side"] and tx[0] < k1 and tx[1] > k0:
                clash.append(f"{s['mat']} table hits {nm}")
    if clash:
        sys.exit("furniture clash: " + "; ".join(clash))
    # circle to the floor edge / tier fronts (KHSAA recommendation)
    circ = dict(W=gaps_x[0] + circle_safety, E=gaps_x[2] + circle_safety, S=gaps_y[0] + circle_safety, N=gaps_y[2] + circle_safety)
    checks = [
        dict(rule="NFHS 2-1-2", item="Circle + safety area", req=f">= {wr['circle_min_ft']} + 2 x {wr['safety_ft']} = {wr['circle_min_ft'] + 2 * wr['safety_ft']} ft",
             drawn=f"{m} ft mat ({circle_safety:g} ft each side of a 28 ft circle)", ok=m >= wr["circle_min_ft"] + 2 * wr["safety_ft"]),
        dict(rule="NFHS 2-1-5", item="Space around each mat", req=f">= {wr['clear_ft']} ft",
             drawn=f"W {gaps_x[0]:g} · between {gaps_x[1]:g} / {gaps_y[1]:g} · E {gaps_x[2]:g} · S / N {gaps_y[0]:g} / {gaps_y[2]:g}",
             ok=min(gaps_x + gaps_y) >= wr["clear_ft"]),
        dict(rule="NFHS 2-3", item="Scorer's table to mat", req=f">= {wr['table_from_mat_ft']} ft", drawn=f"{min(t_mat):g} ft", ok=min(t_mat) >= wr["table_from_mat_ft"]),
        dict(rule="NFHS 2-1-5", item="Bench to mat / to table", req=f">= {wr['bench_from_mat_ft']} / >= {wr['bench_from_table_ft']} ft",
             drawn=f"{min(b_mat):g} / {min(b_tab):g} ft", ok=min(b_mat) >= wr["bench_from_mat_ft"] and min(b_tab) >= wr["bench_from_table_ft"]),
        dict(rule="KHSAA (rec.)", item="Circle to walls / tier", req=f"about {wr['wall_rec_ft']} ft",
             drawn=f"W {circ['W']:g} (open to corridor) · E {circ['E']:g} · S / N {circ['S']:g} / {circ['N']:g}", ok=min(circ.values()) >= wr["wall_rec_ft"]),
    ]
    # court
    ct = plan["court"]["rect"]
    ro = plan["court"]["runout_ft"]
    box = [ct[0] - ro, ct[1] - ro, ct[2] + ro, ct[3] + ro]
    court = dict(rect=ct, box=box, w=ct[2] - ct[0], l=ct[3] - ct[1],
                 edge=dict(W=box[0] - fl[0], E=fl[2] - box[2], S=box[1] - fl[1], N=fl[3] - box[3]))
    if min(court["edge"].values()) < 0:
        sys.exit("court runout box leaves the floor")
    # tiers
    tl = plan["tiers"]["lower"]
    cd = ov["tiers"]["closed_depth_in"] / 12
    av = plan["arena_volume"]["rect"]
    sides = {b["side"] for b in tl["bands"]}
    closed = [fl[0] - (tl["depth_ft"] - cd if "W" in sides else 0), av[1] + cd if "S" in sides else fl[1],
              av[2] - cd if "E" in sides else fl[2], av[3] - cd if "N" in sides else fl[3]]
    open_sf = (fl[2] - fl[0]) * (fl[3] - fl[1])
    closed_sf = (closed[2] - closed[0]) * (closed[3] - closed[1])
    # occupancy
    code = rd(Path(rb["basis"]["code"]).name if rb else "phase2_code.yaml")
    ef = code["event_floor"]
    fac = code["factors"]
    oc = ov["occupancy"]
    z = oc["zone"]
    zsf = (z[2] - z[0]) * (z[3] - z[1])
    if abs(zsf - ef["area_sf"]) > 0.5:
        sys.exit(f"hatched zone {zsf} SF != G-002 floor {ef['area_sf']} SF")
    cases = []
    for c in d["cases"]:
        cases.append(dict(id=c["id"], factor=fac[c["factor"]], floor=c["floor"], l1=c["l1"]))
    worst = max(cases, key=lambda c: c["l1"])
    drawn_stand = ceil_div(oc["drawn_sf"], fac["standing"]["sf"])
    cl_stand = ceil_div(closed_sf, fac["standing"]["sf"])
    cl_chairs = ceil_div(closed_sf, fac["chairs"]["sf"])
    base_no_lower = d["l1_fixed"] - d["seats_l"]
    sens = dict(drawn_stand=drawn_stand, drawn_l1=d["l1_fixed"] + drawn_stand, cl_stand=cl_stand, cl_stand_l1=base_no_lower + cl_stand,
                cl_chairs=cl_chairs, cl_chairs_l1=base_no_lower + cl_chairs)
    out = dict(ov=ov, plan=plan, d=d, fl=fl, mats=mats, gaps_x=gaps_x, gaps_y=gaps_y, checks=checks, furn=furn, court=court,
               closed=closed, cd=cd, open_sf=open_sf, closed_sf=closed_sf, cases=cases, worst=worst, sens=sens, zsf=zsf, circ=circ, rev=rev, rb=rb)
    if rb:
        out["design"] = next(c for c in cases if c["id"] == rb["occupancy"]["design"])
        if out["design"]["id"] != ef["design_case"]:
            sys.exit(f"A-103 Rev {rev} design case differs from {rb['basis']['code']}")
        wf = rb["occupancy"]["whole_floor_standing"]
        if ceil_div(wf["sf"], fac["standing"]["sf"]) != wf["load"]:
            sys.exit("whole-floor standing load drifted")
        va = rb.get("v2_aisle")
        if va:
            v2 = next(o["rect"] for o in plan["tiers"]["lower"]["openings"] if o["id"] == va["opening"])
            ar = va["rect"]
            if (ar[1], ar[3]) != (v2[1], v2[3]) or ar[2] != fl[2] or ar[0] != fl[0]:
                sys.exit(f"V2 aisle {ar} does not line up with {va['opening']} {v2} across the floor {fl}")
            if abs((min(ar[2], z[2]) - ar[0]) * (ar[3] - ar[1]) - va["area_sf"]) > 1:
                sys.exit("V2 aisle area drifted")
            out["v2"] = v2
    return out


# ---------------------------------------------------------------- drawing helpers
def clip(p0, p1, r):
    """Liang-Barsky: clip segment p0-p1 to rect r = [x0, y0, x1, y1]; returns None or the clipped pair."""
    (x0, y0), (x1, y1) = p0, p1
    dx, dy = x1 - x0, y1 - y0
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, x0 - r[0]), (dx, r[2] - x0), (-dy, y0 - r[1]), (dy, r[3] - y0)):
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


class View:
    def __init__(self, sh, ox, oy, ft_per_in, x0, y0):
        self.sh, self.ox, self.oy, self.k, self.x0, self.y0 = sh, ox, oy, 1.0 / ft_per_in, x0, y0

    def P(self, x, y):
        return self.ox + (x - self.x0) * self.k, self.oy + (y - self.y0) * self.k

    def line(self, x1, y1, x2, y2, layer, lw=0.5):
        a, b = self.P(x1, y1)
        c, d = self.P(x2, y2)
        self.sh.line(a, b, c, d, layer=layer, lw=lw)

    def dashed(self, x1, y1, x2, y2, layer, lw=0.4, dash=0.05, gap=0.035):
        a, b = self.P(x1, y1)
        c, d = self.P(x2, y2)
        self.sh.dashed(a, b, c, d, layer=layer, lw=lw, dash=dash, gap=gap)

    def rect(self, r, layer, lw=0.5, dash=False, **kw):
        f = self.dashed if dash else self.line
        for s in ((r[0], r[1], r[2], r[1]), (r[2], r[1], r[2], r[3]), (r[2], r[3], r[0], r[3]), (r[0], r[3], r[0], r[1])):
            f(*s, layer=layer, lw=lw, **kw)

    def fill(self, r, color, layer, lw=0):
        self.sh.poly([self.P(r[0], r[1]), self.P(r[2], r[1]), self.P(r[2], r[3]), self.P(r[0], r[3])], fill=color, layer=layer, lw=lw)

    def hatch(self, r, angle, step, layer, lw=0.2, cross=False):
        for ang in ((angle, angle + 90) if cross else (angle,)):
            t = math.radians(ang)
            ux, uy = math.cos(t), math.sin(t)
            nx, ny = -uy, ux
            cs = [(r[0], r[1]), (r[2], r[1]), (r[2], r[3]), (r[0], r[3])]
            ss = [x * nx + y * ny for x, y in cs]
            s = math.ceil(min(ss) / step) * step
            while s <= max(ss):
                cx, cy = s * nx, s * ny
                pr = clip((cx - ux * 1e4, cy - uy * 1e4), (cx + ux * 1e4, cy + uy * 1e4), r)
                if pr and math.hypot(pr[1][0] - pr[0][0], pr[1][1] - pr[0][1]) > 1e-6:
                    self.line(pr[0][0], pr[0][1], pr[1][0], pr[1][1], layer, lw=lw)
                s += step

    def circle(self, cx, cy, rad, layer, lw=0.4, dash=False, n=36):
        pts = [(cx + rad * math.cos(2 * math.pi * i / n), cy + rad * math.sin(2 * math.pi * i / n)) for i in range(n + 1)]
        for i, (a, b) in enumerate(zip(pts[:-1], pts[1:])):
            if dash and i % 2:
                continue
            self.line(a[0], a[1], b[0], b[1], layer, lw=lw)

    def text(self, x, y, s, **kw):
        a, b = self.P(x, y)
        self.sh.text(a, b, s, **kw)

    def dim(self, along, at, ticks, labels, size=3.8, layer=L_DIM):
        """Chain dimension: along = 'x' (horizontal line at y = at) or 'y' (vertical at x = at)."""
        if along == "x":
            self.line(ticks[0], at, ticks[-1], at, layer, lw=0.3)
            for t in ticks:
                self.line(t, at - 1.2, t, at + 1.2, layer, lw=0.3)
            for (a, b), lab in zip(zip(ticks[:-1], ticks[1:]), labels):
                self.text((a + b) / 2, at + 1.0, lab, size=size, align="center", layer=layer)
        else:
            self.line(at, ticks[0], at, ticks[-1], layer, lw=0.3)
            for t in ticks:
                self.line(at - 1.2, t, at + 1.2, t, layer, lw=0.3)
            for (a, b), lab in zip(zip(ticks[:-1], ticks[1:]), labels):
                a2, b2 = self.P(at + 1.4, (a + b) / 2)
                self.sh.text(a2, b2, lab, size=size, align="center", layer=layer, rot=90)


def tiers_open(v, plan, fill="#E4E4E4", rows=True, labels=True):
    tl = plan["tiers"]["lower"]
    for b in tl["bands"]:
        r = b["rect"]
        v.fill(r, fill, L_TIER)
        if rows:
            n = tl["rows"]
            for k in range(1, n):
                if b["side"] == "N":
                    v.line(r[0], r[1] + k * tl["row_depth_ft"], r[2], r[1] + k * tl["row_depth_ft"], L_TIER, lw=0.12)
                elif b["side"] == "S":
                    v.line(r[0], r[3] - k * tl["row_depth_ft"], r[2], r[3] - k * tl["row_depth_ft"], L_TIER, lw=0.12)
                else:
                    v.line(r[0] + k * tl["row_depth_ft"], r[1], r[0] + k * tl["row_depth_ft"], r[3], L_TIER, lw=0.12)
    for o in tl["openings"]:
        v.fill(o["rect"], "#FFFFFF", L_TIER)
        r = o["rect"]
        if o["side"] in ("N", "S"):
            v.line(r[0], r[1], r[0], r[3], L_TIER, lw=0.4)
            v.line(r[2], r[1], r[2], r[3], L_TIER, lw=0.4)
        else:
            v.line(r[0], r[1], r[2], r[1], L_TIER, lw=0.4)
            v.line(r[0], r[3], r[2], r[3], L_TIER, lw=0.4)
        if labels:
            cx, cy = (r[0] + r[2]) / 2, (r[1] + r[3]) / 2
            lab = "PORTAL" if o["id"] == "PORTAL" else o["id"]
            if o["side"] == "E":
                a, b = v.P(cx + 1.2, cy)
                v.sh.text(a, b, lab, size=3.6, align="center", layer=L_TAG, rot=90, color=GRY)
            else:
                v.text(cx, cy - 1.2, lab, size=3.6, align="center", layer=L_TAG, color=GRY)


def context(v, plan, size=3.9):
    av = plan["arena_volume"]["rect"]
    v.rect(av, L_WALL, lw=1.1)
    v.rect(plan["event_floor"]["rect"], L_WALL, lw=0.55)
    a, b = v.P(53, 140)
    v.sh.text(a, b, "ATHLETE CORRIDOR (W) — floor edge open", size=size - 0.4, align="center", layer=L_TAG, rot=90, color=GRY)
    v.text((av[0] + av[2]) / 2, av[3] + 1.6, "upper tier (fixed) beyond — L2", size=size - 0.4, align="center", layer=L_TAG, color=GRY)


def panel_title(sh, x, y, s1, s2, col=None):
    sh.text(x, y + 0.13, s1, size=7.0, bold=True)
    sh.text(x, y + 0.02, s2, size=4.8, color=col or GRY)


# ---------------------------------------------------------------- sheet
def build(c):
    ov, plan, d = c["ov"], c["plan"], c["d"]
    p2 = rd("phase2.yaml")
    meta2, om = p2["meta"], ov["meta"]
    rb = c["rb"]
    if rb:
        om = dict(om, revision=rb["meta"]["revision"])
    sh = Sheet(W, H)
    body_bottom = add_titleblock(sh, {
        "project": f"{meta2['project']}\n{meta2['arena_name']} · {meta2['location']}",
        "phase": "PHASE 2",
        "title": "FLOOR OVERLAYS\nMATS, SEATING + CONVERSIONS",
        "scale": om["scale_text"],
        "date": meta2["sheet_date"],
        "revision": om["revision"],
        "drawn_by": (rb or {}).get("meta", {}).get("drawn_by", meta2["drawn_by"]),
        "sheet_no": SHEET_NO,
        "stamp": meta2["stamp"],
    }, margin=M, tb_h=0.95, stamp_h=0.40)
    top = H - M - 0.12
    vx0, vy0, vx1, vy1 = om["view"]
    fps = om["panel_scale_ft_per_in"]
    pw, ph = (vx1 - vx0) / fps, (vy1 - vy0) / fps
    colx = [0.8, 0.8 + pw + 0.42]
    rowy = [top - 0.42 - ph, top - 0.42 - ph - 0.52 - ph]
    fl = c["fl"]
    wr = ov["wrestling"]
    # ---------------- (a) wrestling
    v = View(sh, colx[0], rowy[0], fps, vx0, vy0)
    tiers_open(v, plan)
    context(v, plan)
    tz = plan["event_floor"]["table_zone_ft"]
    v.fill([fl[0], fl[1], fl[2], fl[1] + tz], "#EAF0F8", L_ZONE)
    v.fill([fl[0], fl[3] - tz, fl[2], fl[3]], "#EAF0F8", L_ZONE)
    v.rect(fl, L_WALL, lw=0.55)
    xs = sorted({r[0] for r in c["mats"].values()} | {r[2] for r in c["mats"].values()})
    ys = sorted({r[1] for r in c["mats"].values()} | {r[3] for r in c["mats"].values()})
    cl = wr["clear_ft"]
    v.rect([xs[0] - cl, ys[0] - cl, xs[3] + cl, ys[3] + cl], L_ZONE, lw=0.35, dash=True)
    for mid, r in c["mats"].items():
        v.fill(r, "#F4E6C8", L_MAT, lw=0.8)
        cx, cy = (r[0] + r[2]) / 2, (r[1] + r[3]) / 2
        v.circle(cx, cy, wr["circle_min_ft"] / 2, L_MAT, lw=0.45)
        v.text(cx, cy - 1.5, mid, size=5.0, bold=True, align="center", layer=L_TAG)
    for kind, r in c["furn"]:
        if kind == "table":
            v.fill(r, "#333333", L_FURN)
        else:
            v.rect(r, L_FURN, lw=0.5)
    for o in plan["tiers"]["lower"]["openings"]:
        r = o["rect"]
        if o["id"] == "PORTAL":
            v.rect([r[0], fl[1], r[2], fl[1] + tz], L_ZONE, lw=0.3, dash=True)
        if o["id"] == "V1":
            v.rect([r[0], fl[3] - tz, r[2], fl[3]], L_ZONE, lw=0.3, dash=True)
    v.text(fl[0] + 2, fl[1] + 1.6, "TABLE / BENCH ZONE (15')", size=3.6, layer=L_TAG, color=BLU)
    v.text(fl[0] + 3, fl[3] - 4.0, "TABLE / BENCH ZONE (15')", size=3.6, layer=L_TAG, color=BLU)
    v.dim("x", 52.5, [fl[0], xs[0], xs[1], xs[2], xs[3], fl[2]], [f"{a:g}'" for a in (c["gaps_x"][0], 42, c["gaps_x"][1], 42, c["gaps_x"][2])])
    v.dim("y", 190.5, [fl[1], ys[0], ys[1], ys[2], ys[3], fl[3]], [f"{a:g}'" for a in (c["gaps_y"][0], 42, c["gaps_y"][1], 42, c["gaps_y"][2])])
    allok = all(k["ok"] for k in c["checks"])
    panel_title(sh, colx[0], rowy[0] + ph + 0.06, "(a) WRESTLING — 4 x 42' MATS, 2 x 2",
                f"{om['panel_scale_text']} · tier open · NFHS clearances {'all PASS' if allok else 'FAIL'} (table at right)", GRN if allok else RED)
    # ---------------- (b) basketball
    v = View(sh, colx[1], rowy[0], fps, vx0, vy0)
    tiers_open(v, plan)
    context(v, plan)
    ct, box = c["court"]["rect"], c["court"]["box"]
    v.fill(ct, "#F7EBD8", L_COURT, lw=0.9)
    v.line(ct[0], (ct[1] + ct[3]) / 2, ct[2], (ct[1] + ct[3]) / 2, L_COURT, lw=0.5)
    v.rect(box, L_COURT, lw=0.35, dash=True)
    v.text((ct[0] + ct[2]) / 2, (ct[1] + ct[3]) / 2 + 12, f"{c['court']['l']:g}' x {c['court']['w']:g}'", size=4.6, bold=True, align="center", layer=L_TAG)
    v.text((ct[0] + ct[2]) / 2, (ct[1] + ct[3]) / 2 + 6, "NFHS 1-1 (HS ideal)", size=3.8, align="center", layer=L_TAG)
    v.text((ct[0] + ct[2]) / 2, box[3] - 4.2, f"{plan['court']['runout_ft']}' runout (1-2-1 pref.)", size=3.6, align="center", layer=L_TAG, color=GRY)
    e = c["court"]["edge"]
    v.dim("x", 52.5, [fl[0], box[0], box[2], fl[2]], [f"{e['W']:g}'", f"{box[2] - box[0]:g}'", f"{e['E']:g}'"])
    v.dim("y", 190.5, [fl[1], box[1], box[3], fl[3]], [f"{e['S']:g}'", f"{box[3] - box[1]:g}'", f"{e['N']:g}'"])
    v.text((fl[0] + fl[2]) / 2, fl[1] + 4, "VOLLEYBALL: TBD — not drawn", size=4.2, bold=True, align="center", layer=L_TAG, color=RED)
    v.text((fl[0] + fl[2]) / 2, fl[3] - 7, "2nd court: TBD (params)", size=4.0, align="center", layer=L_TAG, color=RED)
    panel_title(sh, colx[1], rowy[0] + ph + 0.06, "(b) BASKETBALL — 1 COURT (IN PARAMS)", f"{om['panel_scale_text']} · tier open · mats up, court down, seats stay")
    # ---------------- (c) telescopic tier open vs closed
    v = View(sh, colx[0], rowy[1], fps, vx0, vy0)
    av = plan["arena_volume"]["rect"]
    clz = c["closed"]
    tl = plan["tiers"]["lower"]
    gain = [[fl[0], clz[1], clz[2], fl[1]], [fl[0], fl[3], clz[2], clz[3]], [fl[2], fl[1], clz[2], fl[3]]]
    for g in gain:
        v.fill(g, "#DCEFE0", L_ZONE)
        v.hatch(g, 45, 2.5, L_HATCH, lw=0.18)
    for b in tl["bands"]:
        r = b["rect"]
        s = b["side"]
        st = {"N": [r[0], clz[3], r[2], r[3]], "S": [r[0], r[1], r[2], clz[1]], "E": [clz[2], r[1], r[2], r[3]]}[s]
        v.fill(st, "#555555", L_TIER)
    for o in tl["openings"]:
        r = o["rect"]
        q = {"S": [r[0], av[1], r[2], clz[1]], "N": [r[0], clz[3], r[2], av[3]], "E": [clz[2], r[1], av[2], r[3]]}[o["side"]]
        v.fill(q, "#FFFFFF", L_TIER)
    v.rect(av, L_WALL, lw=1.1)
    v.rect(fl, L_WALL, lw=0.9)
    v.rect(clz, L_ZONE, lw=0.6, dash=True)
    a, b = v.P(53, 140)
    sh.text(a, b, "ATHLETE CORRIDOR (W) — floor edge open", size=3.5, align="center", layer=L_TAG, rot=90, color=GRY)
    cx, cy = (fl[0] + fl[2]) / 2, (fl[1] + fl[3]) / 2
    v.text(cx, cy + 9, "TIER OPEN (extended)", size=4.8, bold=True, align="center", layer=L_TAG)
    v.text(cx, cy + 3, f"floor {fl[2] - fl[0]:g}' x {fl[3] - fl[1]:g}' = {c['open_sf']:,.0f} SF", size=4.3, align="center", layer=L_TAG)
    v.text(cx, cy - 8, "TIER CLOSED adds the green band", size=4.6, bold=True, align="center", layer=L_TAG, color=GRN)
    v.text(cx, cy - 14, f"{ft_in(clz[2] - clz[0])} x {ft_in(clz[3] - clz[1])} = {r1(c['closed_sf']):,} SF", size=4.3, align="center", layer=L_TAG, color=GRN)
    v.text(cx, cy - 20, f"(+{r1(c['closed_sf'] - c['open_sf']):,} SF; lower seats stowed)", size=4.0, align="center", layer=L_TAG, color=GRN)
    v.text(cx, av[3] + 1.6, f"closed stack {ft_in(c['cd'])} (dark) at the upper-tier face", size=3.6, align="center", layer=L_TAG, color=GRY)
    v.dim("x", 52.5, [fl[0], fl[2], clz[2]], [f"{fl[2] - fl[0]:g}' open", ft_in(clz[2] - fl[2])], size=3.6)
    v.dim("y", 191.5, [av[1], clz[1], fl[1], fl[3], clz[3], av[3]], ["", ft_in(fl[1] - clz[1]), f"{fl[3] - fl[1]:g}'", ft_in(clz[3] - fl[3]), ""], size=3.6)
    panel_title(sh, colx[0], rowy[1] + ph + 0.06, "(c) TELESCOPIC LOWER TIER — OPEN vs CLOSED", f"{om['panel_scale_text']} · 6 rows x 24 in = 12' open; 3'-6\" closed (Hussey)")
    # ---------------- (d) occupancy cases (4 minis)
    mf = om["mini_scale_ft_per_in"]
    mw, mh = (fl[2] - fl[0]) / mf, (fl[3] - fl[1]) / mf
    mx = [colx[1] + 0.12, colx[1] + 0.12 + mw + 0.38]
    dy_top = rowy[1] + ph - 0.05 - mh
    my = [dy_top, dy_top - mh - 0.42]
    z = ov["occupancy"]["zone"]
    hp = ov["occupancy"]["hatch"]
    for i, cs in enumerate(c["cases"]):
        v = View(sh, mx[i % 2], my[i // 2], mf, fl[0], fl[1])
        v.fill(z, ("#EEEEEE" if cs["id"] == "standing" else "#E3F1E6" if cs is c["design"] else "#F5F5F5") if rb else
               ("#FBEFE6" if cs["id"] == "standing" else "#F5F5F5"), L_ZONE)
        h = hp[cs["id"]]
        va = (rb or {}).get("v2_aisle")
        if va and cs["id"] in va["cases"]:          # Rev C: the V2 aisle stays unhatched (keep clear)
            for zz in ([z[0], z[1], z[2], va["rect"][1]], [z[0], va["rect"][3], z[2], z[3]]):
                v.hatch(zz, h["angle"], h["step_ft"], L_HATCH, lw=0.2, cross=h.get("cross", False))
        else:
            v.hatch(z, h["angle"], h["step_ft"], L_HATCH, lw=0.2, cross=h.get("cross", False))
        v.rect(z, L_ZONE, lw=0.4)
        v.rect(fl, L_WALL, lw=0.7)
        v.dashed(z[2], z[1], z[2], z[3], L_ZONE, lw=0.3)
        po = next(o for o in plan["tiers"]["lower"]["openings"] if o["id"] == "PORTAL")["rect"]
        v.line(po[0], fl[1], po[0], fl[1] - 6, L_WALL, lw=0.5)
        v.line(po[2], fl[1], po[2], fl[1] - 6, L_WALL, lw=0.5)
        va = (rb or {}).get("v2_aisle")
        if va and cs["id"] in va["cases"]:
            ar, v2 = va["rect"], c["v2"]
            v.fill(ar, "#FFFFFF", L_ZONE)
            v.dashed(ar[0], ar[1], ar[2], ar[1], L_ZONE, lw=0.45)
            v.dashed(ar[0], ar[3], ar[2], ar[3], L_ZONE, lw=0.45)
            v.line(v2[0], v2[1], v2[2], v2[1], L_WALL, lw=0.5)
            v.line(v2[0], v2[3], v2[2], v2[3], L_WALL, lw=0.5)
            ym = (ar[1] + ar[3]) / 2
            v.line(ar[2] - 12, ym, v2[2] + 2, ym, L_ZONE, lw=0.7)
            a, b = v.P(v2[2] + 4, ym)
            sh.poly([(a, b), (a - 0.05, b + 0.03), (a - 0.05, b - 0.03)], fill=GRN, layer=L_ZONE, lw=0.3)
            v.text(ar[0] + 3, ym - 1.6, f"KEEP CLEAR {va['width_in'] // 12:g}' → V2 → CORE 2", size=3.6, bold=True, layer=L_TAG, color=GRN)
        x0, y0 = mx[i % 2], my[i // 2]
        if rb:
            col = GRN if cs is c["design"] else GRY if cs["id"] == "standing" else "#000000"
            tag = " · DESIGN (D-054)" if cs is c["design"] else " · NOT A USE (margin)" if cs["id"] == "standing" else " · POSTED"
            sh.text(x0, y0 - 0.11, f"{CASE_NAMES[cs['id']]}: {cs['floor']:,}", size=5.6, bold=True, color=col)
            sh.text(x0, y0 - 0.2, f"{cs['factor']['sf']} {cs['factor']['kind']} · L1 {cs['l1']:,}" + tag, size=4.5, color=col)
            continue
        col = RED if cs is c["worst"] else "#000000"
        sh.text(x0, y0 - 0.11, f"{CASE_NAMES[cs['id']]}: {cs['floor']:,}", size=5.6, bold=True, color=col)
        sh.text(x0, y0 - 0.2, f"{cs['factor']['sf']} {cs['factor']['kind']} · L1 {cs['l1']:,}" + (" · WORST" if cs is c["worst"] else ""), size=4.5, color=col)
    if rb:
        if rb.get("v2_aisle"):
            panel_title(sh, colx[1], rowy[1] + ph + 0.06, f"(d) EVENT-FLOOR CASES — {rb['basis']['code_sheet']}",
                        f"{om['mini_scale_text']} · {c['zsf']:,.0f} SF · chairs = design (D-054) · 8' aisle to V2 kept (D-070)", GRN)
        else:
            panel_title(sh, colx[1], rowy[1] + ph + 0.06, "(d) EVENT-FLOOR CASES — P2-G-002 Rev B",
                        f"{om['mini_scale_text']} · hatched {z[2] - z[0]:g}' x {z[3] - z[1]:g}' = {c['zsf']:,.0f} SF · D-054 DECIDED: chairs = design", GRN)
    else:
        panel_title(sh, colx[1], rowy[1] + ph + 0.06, "(d) EVENT-FLOOR CASES — P2-G-002 Rev A",
                    f"{om['mini_scale_text']} · hatched {z[2] - z[0]:g}' x {z[3] - z[1]:g}' = {c['zsf']:,.0f} SF · D-054 OPEN", RED)
    # ---------------- middle column: checks + tables
    xm = colx[1] + pw + 0.3
    wm = 11.62 - xm
    sh.line(xm - 0.12, top - 0.02, xm - 0.12, body_bottom + 0.1, lw=0.4)
    cm = g2.Col(sh, xm, top + 0.12, wm, 1.07)
    cm.head("(a) WRESTLING — NFHS CLEARANCES ON THIS LAYOUT", size=7.6)
    cm.table([("RULE", 0, "left"), ("ITEM", 0.7, "left"), ("REQUIRED", 1.86, "left"), ("DRAWN", 2.86, "left", 1.1), ("", wm - 0.02, "right")],
             [((k["rule"], k["item"], k["req"], k["drawn"], "PASS" if k["ok"] else "FAIL"), dict(colors={4: GRN if k["ok"] else RED})) for k in c["checks"]],
             size=5.6, rh=0.124)
    cm.para(f"Tables {wr['furniture']['table']['len_ft']}' x {wr['furniture']['table']['depth_ft']}' and benches {wr['furniture']['bench']['len_ft']}' x "
            f"{wr['furniture']['bench']['depth_ft']}' ASSUMED (no size in NFHS text found), front edge {wr['furniture']['offset_ft']}' from the mat. "
            f"Portal and V1 aisles kept clear (egress, P2-A-111). {wr['furniture']['tournament']}. Rule text: NFHS 2014-15 (R-005); current book "
            "UNVERIFIED. 28' circle drawn = NFHS minimum (42' mats are often sold with a 32' circle).", size=5.9)
    cm.head("(b) BASKETBALL / VOLLEYBALL — FROM PARAMS ONLY", size=7.6)
    e = c["court"]["edge"]
    cm.para(f"1 court (phase2.yaml basketball_full_courts: 1): {c['court']['l']:g}' x {c['court']['w']:g}' (NFHS 1-1) + {plan['court']['runout_ft']}' runout "
            f"(1-2-1: >= 3', 10' preferred) = {c['court']['box'][2] - c['court']['box'][0]:g}' x {c['court']['box'][3] - c['court']['box'][1]:g}'; "
            f"to the floor edge W {e['W']:g}' / E {e['E']:g}' / S {e['S']:g}' / N {e['N']:g}'. Clear height >= {ov['court']['height_ft']}' (R-019). "
            f"{ov['court']['markings'][0].upper() + ov['court']['markings'][1:]}; {ov['court']['benches_table']}.", size=5.9)
    cm.para(ov["court"]["volleyball"] + " " + ov["court"]["second_court"] + ".", size=5.9, color=RED)
    cm.head("(c) TELESCOPIC LOWER TIER — FLOOR ZONES", size=7.6)
    cm.table([("STATE", 0, "left"), ("FLOOR ZONE", 1.75, "left"), ("SF", 3.1, "right"), ("LOWER SEATS", wm - 0.02, "right")],
             [(("Open — extended 12' (6 x 24 in)", f"{fl[2] - fl[0]:g}' x {fl[3] - fl[1]:g}'", f"{c['open_sf']:,.0f}", f"{d['seats_l']:,}"), None),
              ((f"Closed — {ft_in(c['cd'])} stack", f"{ft_in(c['closed'][2] - c['closed'][0])} x {ft_in(c['closed'][3] - c['closed'][1])}", f"{r1(c['closed_sf']):,}", "0"), None),
              (("Gain (N, S, E)", f"+{ft_in(c['closed'][2] - fl[2])} each side", f"+{r1(c['closed_sf'] - c['open_sf']):,}", ""), dict(color=GRN))],
             size=5.7, rh=0.126)
    cm.para(f"{ov['tiers']['placement'][0].upper() + ov['tiers']['placement'][1:]}. {ov['tiers']['sides'][0].upper() + ov['tiers']['sides'][1:]}. "
            f"{ov['tiers']['code']}. Portal, V1, V2 stay open through the stack.", size=5.9)
    if rb:
        return build_b_tail(c, sh, body_bottom, top, cm, xm, wm, ov, om, rb, plan, d)
    cm.head("CONVERSIONS (ASSUMED SEQUENCE)", size=7.6)
    for t in ("Wrestling: tier open; mats roll in from EQUIP. STORAGE at the top of the athlete corridor (plan Rev G; S1 service door, D-034).",
              "Basketball: mats up and stored, court surface down (surface type TBD); seats stay (phase2.yaml floor_converts).",
              "Floor events (D-054 OPEN): tier open or closed per event; chairs, tables, stage / platform and their storage are NOT in the "
              "program (TBD) — no room drawn for them.",
              "Occupant load posted per configuration (IBC 1004.9); the building official assigns the loads."):
        cm.para(t, size=5.9, bullet="·")
    # ---------------- right column
    xr = 11.86
    sh.line(xr - 0.12, top - 0.02, xr - 0.12, body_bottom + 0.1, lw=0.4)
    wr_ = W - M - 0.08 - xr
    cr = g2.Col(sh, xr, top + 0.12, wr_, 1.13)
    cr.para(om["disclaimer"], size=5.9, color=GRY)
    cr.head("(d) EVENT-FLOOR OCCUPANCY CASES — D-054 OPEN", size=7.2)
    nt = ov["occupancy"]["notes"]
    rows = [((CASE_NAMES[cs["id"]].title(), f"{cs['factor']['sf']} {cs['factor']['kind']}", f"{cs['floor']:,}", f"{cs['l1']:,}", nt[cs["id"]]),
             dict(color=RED if cs is c["worst"] else None)) for cs in c["cases"]]
    cr.table([("CASE", 0, "left"), ("FACTOR", 0.86, "left"), ("FLOOR", 1.68, "right"), ("L1", 2.06, "right"), ("LAYOUT NOTE", 2.16, "left", wr_ - 2.2)],
             rows, size=5.2, rh=0.115)
    s = c["sens"]
    cr.para(f"Floor = 16,416 SF (G-002, 114' x 144'; hatched from the W edge, the east 6' strip of the drawn floor, D-053, unhatched); L1 = floor + {d['seats_l']:,} lower seats + {d['l1_fixed'] - d['seats_l']:,} other L1 rooms. Sensitivity: whole drawn "
            f"zone 17,280 SF standing = {s['drawn_stand']:,} (L1 {s['drawn_l1']:,}; E1 479.4 in still under 512, P2-A-111). Tier CLOSED: standing {s['cl_stand']:,} / chairs "
            f"{s['cl_chairs']:,} on {r1(c['closed_sf']):,} SF with no lower seats → L1 {s['cl_stand_l1']:,} / {s['cl_chairs_l1']:,}, below the "
            f"{c['worst']['l1']:,} design case the L1 exits were sized for (arithmetic; net = gross ASSUMED). {ov['occupancy']['posting']}.", size=5.45)
    cr.head("OPEN DECISIONS — NOT ASSUMED HERE", size=7.4)
    for it in ov["open_items"]:
        cr.para(f"{it['id']}: {it['text']}.", size=5.9, bullet="·", color=RED)
    cr.para("Floor uses beyond sports wait on Shane (D-054). L1 exits are already sized for the standing worst case (Shane 11:07 AM CT, "
            "P2-A-111 Rev A); restroom fixtures for it are not (D-064).", size=5.9)
    cr.head("LEGEND", size=7.4)
    cr.para("Grey band = telescopic lower tier open (thin lines = 24 in rows) · dark band = closed stack · tan = mat (circle = 28' NFHS "
            "minimum) · black bar = scorer's table · open bar = team bench · blue = table / bench zone · dashed = 10' mat area / "
            "keep-clear aisle / runout · green hatch = floor gained when closed · hatch styles (d): wide = sports, cross = tables, "
            "horizontal = chairs, dense = standing.", size=5.5, color=GRY)
    cr.para("Sources: params/phase2_overlays.yaml; phase2_plan_rev_g.yaml; phase2_code.yaml; R-005 (NFHS Wrestling 2-1-2, 2-1-5, 2-2-1, 2-2-2, 2-3; "
            "KHSAA); R-012 (NFHS Basketball 1-1, 1-2-1); R-019; R-008 / Hussey MAXAM; R-007.2 (IBC 2021 T1004.5); IBC 2021 1004.9, 1030.1.1, "
            "1030.1.1.1, 1030.9.1, 1030.13.1, 1030.13.2, 1030.13.2.1 (UpCodes, retrieved 2026-10-04); P2-G-002 Rev A; P2-A-111 Rev A; P2-A-302 Rev C; "
            "D-009, D-014, D-030, D-053, D-054; Shane 2026-10-04 11:45 AM CT.", size=5.3, color=GRY)
    return sh, body_bottom, [cm, cr]


def build_b_tail(c, sh, body_bottom, top, cm, xm, wm, ov, om, rb, plan, d):
    """Rev B: conversions + storage route diagram (middle column), posted cases, decisions (right column)."""
    st = rb["storage"]
    rooms = {r["id"]: r for r in plan["level_1"]["rooms"]}
    an = rooms[st["annex"]]
    ar = an["rect"]
    cm.head("CONVERSIONS + STORAGE (ASSUMED SEQUENCE)", size=7.6)
    rc = "v2_aisle" in rb
    pr = "I" if rc else "H"
    for t in (f"Wrestling: tier open; mats roll in from EQUIP. STORAGE at the top of the athlete corridor (plan Rev {pr}, unchanged).",
              "Basketball: mats up and stored, court surface down (surface type TBD); seats stay (phase2.yaml floor_converts).",
              f"Floor events: chairs, tables and stage carts come from the new {an['name'].title()} annex ({(ar[2] - ar[0]) * (ar[3] - ar[1]):,.0f} SF, "
              "D-067) — route below. Tier open or closed per event." + (" Every chair layout keeps the 8' V2 cross-aisle open: floor → V2 → EXIT (E) + core-2 corridor (restrooms, DF) → X7 (D-069 / D-070; panel d)." if rc else ""),
              rb["occupancy"]["posting"] + "."):
        cm.para(t, size=5.9, bullet="·")
    # storage route diagram
    vx0, vy0, vx1, vy1 = st["view"]
    k = st["scale_ft_per_in"]
    dh = (vy1 - vy0) / k
    gy = cm.y - 0.32 - dh
    v = View(sh, xm + 0.05, gy, k, vx0, vy0)
    bx0, by0, bx1, by1 = plan["building"]["rect"]
    v.line(vx0, by1, min(vx1, bx1), by1, L_WALL, lw=0.9)
    v.line(bx0, vy0, bx0, by1, L_WALL, lw=0.9)
    v.fill(ar, "#E3F1E6", L_ZONE, lw=0.6)
    v.rect(ar, L_WALL, lw=0.9)
    eq = rooms["equip_storage"]["rect"]
    v.fill(eq, "#F4E6C8", L_ZONE, lw=0.4)
    ath = next(z_ for z_ in plan["level_1"]["zones"] if z_["id"] == "athlete")["rect"]
    v.fill(ath, "#F2F2F2", L_ZONE, lw=0.3)
    fl = c["fl"]
    v.fill([fl[0], max(fl[1], vy0), min(fl[2], vx1), fl[3]], "#FFFFFF", L_ZONE, lw=0.6)
    v.text((ar[0] + ar[2]) / 2, (ar[1] + ar[3]) / 2 + 4, "STORAGE", size=4.4, bold=True, align="center", layer=L_TAG)
    v.text((ar[0] + ar[2]) / 2, (ar[1] + ar[3]) / 2 - 5, f"{(ar[2] - ar[0]) * (ar[3] - ar[1]):,.0f} SF", size=4.0, align="center", layer=L_TAG)
    v.text((eq[0] + eq[2]) / 2, (eq[1] + eq[3]) / 2 - 2, "EQUIP.", size=3.6, align="center", layer=L_TAG)
    a, b = v.P((ath[0] + ath[2]) / 2 - 1, 150)
    sh.text(a, b, "ATHLETE CORR.", size=3.6, align="center", layer=L_TAG, rot=90, color=GRY)
    v.text((fl[0] + min(fl[2], vx1)) / 2 + 4, 150, "EVENT FLOOR", size=4.4, bold=True, align="center", layer=L_TAG)
    s1 = next(e for e in plan["level_1"]["doors"]["items"] if e["id"] == "S1")
    v.fill([s1["at"] - 6, s1["y"] - 0.8, s1["at"] + 6, s1["y"] + 0.8], "#000000", L_WALL)
    v.text(s1["at"], s1["y"] + 2.5, "S1", size=4.2, bold=True, align="center", layer=L_TAG)
    pts = st["route_pts"]
    for (xa, ya), (xb, yb) in zip(pts[:-1], pts[1:]):
        v.line(xa, ya, xb, yb, L_ZONE, lw=1.1)
    xa, ya = pts[-2]
    xb, yb = pts[-1]
    a, b = v.P(xb, yb)
    sh.poly([(a, b), (a - 0.06, b + 0.035), (a - 0.06, b - 0.035)], fill="#000000", layer=L_ZONE, lw=0.3)
    sh.text(xm + 0.05, gy + dh + 0.15, "STORAGE → FLOOR", size=6.2, bold=True)
    sh.text(xm + 0.05, gy + dh + 0.05, f"D-067 · 1\" = {k}' · route ASSUMED", size=4.4, color=GRY)
    cx0 = xm + max((vx1 - vx0) / k, 1.25) + 0.25
    cn = g2.Col(sh, cx0, gy + dh + 0.25, xm + wm - cx0, 1.0)
    cn.para(st["route_text"] + ".", size=5.5)
    cn.para(f"Annex {ar[2] - ar[0]:g}' x {ar[3] - ar[1]:g}', one storey, north wall between X4 and X5; S1 moved to its north wall (y {s1['y']:g}). "
            "Sized for 56 chair / table trucks (42 chairs + 8-10 tables each) + stage carts (D-067, aisle factor ASSUMED).", size=5.5)
    cn.para(rb.get("screening_note", "Screening bay (D-065) is in the lobby, outside these views: P2-A-101 Rev H / P2-A-111 Rev B."), size=5.5, color=GRY)
    cm.y = min(gy - 0.1, cn.y)
    # ---------------- right column
    xr = 11.86
    sh.line(xr - 0.12, top - 0.02, xr - 0.12, body_bottom + 0.1, lw=0.4)
    wr_ = W - M - 0.08 - xr
    cr = g2.Col(sh, xr, top + 0.12, wr_, 1.13)
    cr.para(om["disclaimer"], size=5.9, color=GRY)
    cr.head("(d) EVENT-FLOOR CASES — POSTED LOADS (1004.9)", size=7.2)
    nt = rb["occupancy"]["notes"]
    rows = [((CASE_NAMES[cs["id"]].title(), f"{cs['factor']['sf']} {cs['factor']['kind']}", f"{cs['floor']:,}", f"{cs['l1']:,}", nt[cs["id"]]),
             dict(color=GRN if cs is c["design"] else GRY if cs["id"] == "standing" else None, bold=cs is c["design"])) for cs in c["cases"]]
    cr.table([("CASE", 0, "left"), ("FACTOR", 0.86, "left"), ("FLOOR", 1.68, "right"), ("L1", 2.06, "right"), ("LAYOUT NOTE", 2.16, "left", wr_ - 2.2)],
             rows, size=5.2, rh=0.115)
    s = c["sens"]
    wf = rb["occupancy"]["whole_floor_standing"]
    cr.para(f"Floor = 16,416 SF (G-002 Rev {'C' if rc else 'B'}, 114' x 144'; the east 6' strip, D-053, unhatched); L1 = floor + {d['seats_l']:,} lower seats + "
            f"{d['l1_fixed'] - d['seats_l']:,} other L1 rooms (incl. the storage annex, 300 gross). Design case = chairs: L1 {c['design']['l1']:,}. "
            f"Tier CLOSED, chairs: {s['cl_chairs']:,} on {r1(c['closed_sf']):,} SF with no lower seats → L1 {s['cl_chairs_l1']:,}, below the design "
            f"case; restroom load {s['cl_chairs']:,} < 3,446 (net = gross ASSUMED). Whole drawn zone standing ({wf['sf']:,} SF = {wf['load']:,}) would need "
            f"E1 {wf['e1_need_in']} in vs {wf['e1_clear_in']} in clear beside the screening bay: not permitted (standing is not a use).", size=5.45)
    if rc:
        va = rb["v2_aisle"]
        cr.head("CHAIR LAYOUTS — AISLE TO V2 / CORE 2 (D-069, D-070)", size=7.2)
        cr.para(va["basis"], size=5.45, color=GRN)
    cr.head(rb.get("decisions_head", "DECISIONS — SHANE 1:21 / 1:22 PM CT"), size=7.4)
    for it in rb["decisions"]:
        cr.para(f"{it['id']} {it['status']}: {it['text']}.", size=5.7, bullet="·", color=RED if it["status"] == "OPEN" else None)
    cr.head("LEGEND", size=7.4)
    cr.para("Grey band = telescopic lower tier open (thin lines = 24 in rows) · dark band = closed stack · tan = mat (circle = 28' NFHS "
            "minimum) · black bar = scorer's table · open bar = team bench · blue = table / bench zone · dashed = 10' mat area / "
            "keep-clear aisle / runout · green hatch = floor gained when closed · (d): green = design case, grey = not a use · "
            "route: green = storage annex, tan = equipment storage, line = cart route." + (" (d): white band + arrow = 8' keep-clear aisle to V2." if rc else ""), size=5.5, color=GRY)
    if rc:
        cr.para("Sources: params/phase2_overlays.yaml, phase2_overlays_rev_c.yaml; phase2_plan_rev_i.yaml; phase2_code_rev_c.yaml; R-005 (NFHS Wrestling "
                "2-1-2, 2-1-5, 2-2-1, 2-2-2, 2-3; KHSAA); R-012; R-019; R-008 / Hussey MAXAM; R-007.2 (IBC 2021 T1004.5); IBC 2021 1004.9, 1030.1.1, "
                "1030.9.1, 1030.13.1, 1030.13.2 (UpCodes, retrieved 2026-10-04); P2-G-002 Rev C; P2-A-111 Rev C; P2-A-401 Rev C; D-053, D-054, D-064 to "
                "D-070; Shane 2026-10-04.", size=5.3, color=GRY)
    else:
        cr.para("Sources: params/phase2_overlays.yaml, phase2_overlays_rev_b.yaml; phase2_plan_rev_h.yaml; phase2_code_rev_b.yaml; R-005 (NFHS Wrestling "
                "2-1-2, 2-1-5, 2-2-1, 2-2-2, 2-3; KHSAA); R-012 (NFHS Basketball 1-1, 1-2-1); R-019; R-008 / Hussey MAXAM; R-007.2 (IBC 2021 T1004.5); "
                "IBC 2021 1004.9, 1030.1.1, 1030.9.1, 1030.13.1, 1030.13.2 (UpCodes, retrieved 2026-10-04); P2-G-002 Rev B; P2-A-111 Rev B; "
                "D-053, D-054, D-064 to D-069; Shane 2026-10-04 1:21 / 1:22 PM CT.", size=5.3, color=GRY)
    return sh, body_bottom, [cm, cr]


def ft_in(v):
    f = int(v)
    i = round((v - f) * 12)
    if i == 12:
        f, i = f + 1, 0
    return f"{f}'-{i}\""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", choices=["A", "B", "C"], default="C")
    ap.add_argument("--png")
    ap.add_argument("--out-dir")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--print", action="store_true", help="print the numbers and exit")
    a = ap.parse_args()
    c = compute(a.rev)
    if a.print:
        for k in c["checks"]:
            print(k)
        print("court", c["court"]["edge"], "closed", c["closed"], c["open_sf"], c["closed_sf"])
        print("cases", [(x["id"], x["floor"], x["l1"]) for x in c["cases"]], "sens", c["sens"], "circ", c["circ"])
        return
    p2 = rd("phase2.yaml")
    rv = p2["sheets"][SHEET_NO]["revisions"][a.rev]
    if a.out_dir:
        pdf, dxf = (Path(a.out_dir) / f"{rv['file']}.{e}" for e in ("pdf", "dxf"))
    else:
        pdf = BP / "phase2" / "out" / "pdf" / f"{rv['file']}.pdf"
        dxf = BP / "phase2" / "out" / "dxf" / f"{rv['file']}.dxf"
        if rv.get("frozen") and (pdf.exists() or dxf.exists()) and not a.force:
            sys.exit("Revision is FROZEN; use --out-dir to regenerate for checking.")
    sh, body_bottom, cols = build(c)
    mg = [cl.y - body_bottom - 0.05 for cl in cols]
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
