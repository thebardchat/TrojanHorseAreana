"""KEYSTONE P2-A-111 LIFE SAFETY PLAN (SCHEMATIC) — Phase 2, Levels 1 + 2. Tabloid, two plans at 1" = 50'-0" + check panel.

Rev A (2026-10-04, Shane 11:07 AM CT): exits with clear widths and capacities, occupant loads per P2-G-002 Rev A (standing floor =
worst case, D-054 OPEN), L1 checks with the E1 8-pair door bank (Option 1 DECIDED, 512 in clear, 64 in per pair ASSUMED), L2 stairs,
exit access travel distance (diagram measurements, UNVERIFIED), common path, exit separation (1/3 diagonal, sprinklered), findings
with options (security checkpoint D-065, restrooms D-064) and TBDs. Nothing is redesigned here.
Data: params/phase2_life_safety.yaml, params/phase2_plan_rev_g.yaml (L1 = P2-A-101 Rev G, L2 = Rev F), p2_g_002.compute() loads.
Usage (from the repo root):
  /workspace/.venv-keystone/bin/python blueprints/phase2/src/p2_a_111.py [--rev A] [--png PATH] [--out-dir DIR] [--force] [--print]
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
SHEET_NO = "P2-A-111"
RED, GRN, GRY, LRED = "#CC0000", "#1E7B34", "#555555", "#F6D5D5"
L_WALL, L_ROOM, L_TAG, L_SEAT, L_VERT = "A-WALL-BLDG", "A-AREA-BLCK", "A-AREA-IDEN", "A-SEAT", "A-FLOR-STRS"
L_EXIT, L_PATH, L_SEP = "LS-EXIT", "LS-TRAV", "LS-SEPR"
n0, n1 = g2.n0, g2.n1


def occ(width_in, per_occ):
    """occupants a component can serve: width / factor, rounded DOWN."""
    return math.floor(width_in / per_occ + 1e-6)


def rd(n):
    return yaml.safe_load((BP / "params" / n).read_text(encoding="utf-8"))


def plen(pts):
    return sum(abs(b[0] - a[0]) + abs(b[1] - a[1]) for a, b in zip(pts[:-1], pts[1:]))


def rect_gap(a, b):
    dx = max(0.0, max(a[0], b[0]) - min(a[2], b[2]))
    dy = max(0.0, max(a[1], b[1]) - min(a[3], b[3]))
    return math.hypot(dx, dy)


def compute(rev="A"):
    rc = rev == "C"                 # Rev C (Shane 3:31 PM CT): D-069 east restroom bump-out, plan Rev I; Revs A / B stay byte-identical
    rb = rev in ("B", "C")
    d = g2.compute("B" if rb else "A")
    ls, plan = (rd("phase2_life_safety_rev_b.yaml"), rd("phase2_plan_rev_h.yaml")) if rb else (rd("phase2_life_safety.yaml"), rd("phase2_plan_rev_g.yaml"))
    if rc:
        ls, plan = rd("phase2_life_safety_rev_c.yaml"), rd("phase2_plan_rev_i.yaml")
    eg = d["code"]["egress"]
    df, sfac, dw = eg["door_in_per_occ"], eg["stair_in_per_occ"], eg["door_clear_in"]
    wc = d["wc"]
    e1 = next(x for x in plan["level_1"]["doors"]["items"] if x["id"] == "E1")["bank"]
    assert e1["pairs"] * e1["clear_in_per_pair"] == e1["clear_in"]
    nsd = len(eg["stair_discharge"])
    others = [o for o in eg["openings"] if o != eg["main_exit"] and o not in eg["stair_discharge"]]
    l2w = d["l2_worst"]
    tot = wc["l1"] + l2w
    sd_l2 = l2w / nsd * df
    prov = e1["clear_in"] + (len(others) + nsd) * dw
    other_prov = len(others) * dw + nsd * (dw - sd_l2)

    def chk(load_l1, total):
        req, main, oth = total * df, total / 2 * df, load_l1 / 2 * df
        return dict(total=total, req=req, main=main, oth=oth, lose=prov - e1["clear_in"], lose_req=0.5 * req,
                    p_req=prov >= req, p_main=e1["clear_in"] >= main, p_oth=other_prov >= oth, p_lose=prov - e1["clear_in"] >= 0.5 * req)
    c_wc = chk(wc["l1"], tot)
    fs = ls["basis"]["floor_sensitivity"]
    fl_s = -(-fs["area_sf"] // fs["factor_sf"])
    c_fs = chk(d["l1_fixed"] + fl_s, d["l1_fixed"] + fl_s + l2w)
    cases = [dict(c, **chk(c["l1"], c["l1"] + l2w)) for c in d["cases"]]
    st_cap = eg["stair_clear_in"] / sfac
    st_prov = eg["stair_count"] * eg["stair_clear_in"]
    st_req = l2w * sfac
    st = dict(cap=st_cap, prov=st_prov, req=st_req, lose=st_prov - eg["stair_clear_in"], lose_req=0.5 * st_req)
    # per-room occupant loads (same rules as P2-G-002: drawn area less stairs, / factor, round up), on plan Rev G
    stairs = [s_["rect"] for s_ in plan["vertical"]["stairs"]]
    rects = {}
    for lv in ("level_1", "level_2"):
        for grp in ("rooms", "zones"):
            for r in plan[lv].get(grp, []):
                rects[r["id"]] = r["rect"]
    fac = d["fac"]
    room_ol = {}
    for lv in ("level_1", "level_2"):
        for s_ in d["code"][lv]["spaces"]:
            for i in s_["ids"]:
                r = rects[i]
                a = round((r[2] - r[0]) * (r[3] - r[1]) - sum(g2.ov(r, x) for x in stairs))
                room_ol[i] = -(-a // fac[s_["factor"]]["sf"])
    l1_sum = d["seats_l"] + sum(v for k, v in room_ol.items() if k in {i for s_ in d["code"]["level_1"]["spaces"] for i in s_["ids"]})
    if l1_sum != d["l1_fixed"]:
        sys.exit(f"Plan room loads ({l1_sum}) differ from P2-G-002 Rev {'B' if rb else 'A'} ({d['l1_fixed']})")
    paths = [dict(p, length=plen(p["pts"])) for p in ls["travel"]["paths"]]
    (dx0, dy0), (dx1, dy1) = ls["separation"]["diagonal_from"]
    diag = math.hypot(dx1 - dx0, dy1 - dy0)
    corner_d = {}
    if rc:                          # every outline corner (box, NE tower, annex, bump-out): the stated diagonal must be the maximum
        bld = plan["building"]
        pts_ = [(r[i], r[j]) for r in (bld["rect"], bld["projection"]["rect"], bld["annex"]["rect"], bld["bumpout"]["rect"]) for i in (0, 2) for j in (1, 3)]
        dmax = max(math.hypot(a[0] - b[0], a[1] - b[1]) for a in pts_ for b in pts_)
        assert abs(dmax - diag) < 0.01, (dmax, diag)
        bo, ax = bld["bumpout"]["rect"], bld["annex"]["rect"]
        corner_d = dict(bumpout=math.hypot(bo[2], bo[3]), annex=math.hypot(ax[2], ax[3]))
    srect = {s_["id"]: s_["rect"] for s_ in plan["vertical"]["stairs"]}
    seps = []
    for p in ls["separation"]["pairs"]:
        if "a_pt" in p:
            dist = math.hypot(p["b_pt"][0] - p["a_pt"][0], p["b_pt"][1] - p["a_pt"][1])
        else:
            dist = rect_gap(srect[p["a"]], srect[p["b"]])
        seps.append(dict(p, dist=dist, req=diag / 3, ok=dist >= diag / 3))
    c_mc = chk(d["mc"]["l1"], d["mc"]["total"]) if rb else None
    return dict(rev=rev, c_mc=c_mc, d=d, ls=ls, plan=plan, e1=e1, df=df, sfac=sfac, dw=dw, others=others, nsd=nsd, sd_l2=sd_l2, prov=prov,
                other_prov=other_prov, c_wc=c_wc, c_fs=c_fs, fl_s=fl_s, cases=cases, st=st, room_ol=room_ol, paths=paths,
                diag=diag, seps=seps, l2w=l2w, tot=tot, corner_d=corner_d)


class Plan:
    def __init__(self, sh, x0, y0, s):
        self.sh, self.x0, self.y0, self.s = sh, x0, y0, s

    def P(self, x, y):
        return self.x0 + x * self.s, self.y0 + y * self.s

    def rect(self, r, layer, lw=0.6):
        x, y = self.P(r[0], r[1])
        self.sh.rect(x, y, (r[2] - r[0]) * self.s, (r[3] - r[1]) * self.s, layer=layer, lw=lw)

    def line(self, x1, y1, x2, y2, layer, lw=0.6):
        a, b = self.P(x1, y1)
        c, e = self.P(x2, y2)
        self.sh.line(a, b, c, e, layer=layer, lw=lw)

    def dashed(self, x1, y1, x2, y2, layer, lw=0.6, dash=0.06, gap=0.04):
        a, b = self.P(x1, y1)
        c, e = self.P(x2, y2)
        self.sh.dashed(a, b, c, e, layer=layer, lw=lw, dash=dash, gap=gap)

    def fill(self, r, color, layer):
        pts = [self.P(r[0], r[1]), self.P(r[2], r[1]), self.P(r[2], r[3]), self.P(r[0], r[3])]
        self.sh.poly(pts, fill=color, layer=layer, lw=0)

    def text(self, x, y, s, **kw):
        a, b = self.P(x, y)
        self.sh.text(a, b, s, **kw)


def outline(pl, plan, annex=True):
    bx0, by0, bx1, by1 = plan["building"]["rect"]
    pj = plan["building"]["projection"]["rect"]
    pts = [(bx0, by0), (bx1, by0), (bx1, pj[3]), (pj[0], pj[3]), (pj[0], by1), (bx0, by1), (bx0, by0)]
    bo = plan["building"].get("bumpout")
    for (xa, ya), (xb, yb) in zip(pts[:-1], pts[1:]):
        if bo and xa == xb == bx1 and annex:          # Plan Rev I: L1 east wall open where EXIT (E) runs into the bump-out
            ez = next(z["rect"] for z in plan["level_1"]["zones"] if z["id"] == "exit_e")
            pl.line(xa, ya, xb, ez[1], L_WALL, lw=1.8)
            pl.line(xa, ez[3], xb, yb, L_WALL, lw=1.8)
            continue
        pl.line(xa, ya, xb, yb, L_WALL, lw=1.8)
    if annex and bo:                                   # Plan Rev I restroom bump-out (D-069), one storey
        r = bo["rect"]
        for (xa, ya, xb, yb) in ((r[0], r[1], r[2], r[1]), (r[2], r[1], r[2], r[3]), (r[2], r[3], r[0], r[3])):
            pl.line(xa, ya, xb, yb, L_WALL, lw=1.8)
    if annex and "annex" in plan["building"]:            # Plan Rev H storage annex (D-067), one storey
        ax = plan["building"]["annex"]["rect"]
        for (xa, ya, xb, yb) in ((ax[0], ax[1], ax[0], ax[3]), (ax[0], ax[3], ax[2], ax[3]), (ax[2], ax[3], ax[2], ax[1])):
            pl.line(xa, ya, xb, yb, L_WALL, lw=1.8)


def stairs(pl, plan, labels):
    for s_ in plan["vertical"]["stairs"]:
        r = s_["rect"]
        pl.fill(r, "#E4E4E4", L_VERT)
        pl.rect(r, L_VERT, lw=0.9)
        pl.line(r[0], r[1], r[2], r[3], L_VERT, lw=0.3)
        lx, ly, al = labels[s_["id"]]
        pl.text(lx, ly, s_["id"], size=5.0, bold=True, align=al, layer=L_TAG)
    pl.rect(plan["vertical"]["elevator"]["rect"], L_VERT, lw=0.6)


def arrow(pl, x, y, dx, dy, lw=0.9):
    """exit arrow from (x, y) pointing outward along (dx, dy) (unit, feet), 6 ft long."""
    L = 6.0
    ex, ey = x + dx * L, y + dy * L
    pl.line(x, y, ex, ey, L_EXIT, lw=lw)
    px, py = -dy, dx
    pl.line(ex, ey, ex - dx * 2.2 + px * 1.5, ey - dy * 2.2 + py * 1.5, L_EXIT, lw=lw)
    pl.line(ex, ey, ex - dx * 2.2 - px * 1.5, ey - dy * 2.2 - py * 1.5, L_EXIT, lw=lw)


def draw_path(pl, p, color, lx, ly, al="left"):
    pts = p["pts"]
    for a, b in zip(pts[:-1], pts[1:]):
        pl.dashed(a[0], a[1], b[0], b[1], L_PATH, lw=1.1, dash=0.05, gap=0.03)
    x, y = pts[0]
    a, b = pl.P(x, y)
    pl.sh.poly([(a - 0.03, b - 0.03), (a + 0.03, b - 0.03), (a + 0.03, b + 0.03), (a - 0.03, b + 0.03)], fill="#000000", layer=L_PATH, lw=0)
    pl.text(lx, ly, f"{p['id']} {p['length']:.0f}'", size=5.2, bold=True, align=al, layer=L_PATH, color=color)


def build(c):
    d, ls, plan = c["d"], c["ls"], c["plan"]
    p2, meta2, lm = d["p2"], d["p2"]["meta"], ls["meta"]
    sh = Sheet(W, H)
    body_bottom = add_titleblock(sh, {
        "project": f"{meta2['project']}\n{meta2['arena_name']} · {meta2['location']}",
        "phase": "PHASE 2",
        "title": "LIFE SAFETY PLAN\nLEVELS 1 + 2 · SCHEMATIC",
        "scale": lm["scale_text"],
        "date": meta2["sheet_date"],
        "revision": lm["revision"],
        "drawn_by": meta2["drawn_by"],
        "sheet_no": SHEET_NO,
        "stamp": meta2["stamp"],
    }, margin=M, tb_h=0.95, stamp_h=0.40)
    top = H - M - 0.12
    s = 1.0 / lm["scale_ft_per_in"]
    e1, lv1, lv2 = c["e1"], plan["level_1"], plan["level_2"]
    ol = c["room_ol"]
    paths = {p["id"]: p for p in c["paths"]}
    rb = c["rev"] in ("B", "C")
    rc = c["rev"] == "C"
    py0 = 4.62
    # ---------------------------------------------------------------- LEVEL 1
    pl = Plan(sh, 1.0, py0, s)
    if rc:
        sh.text(3.55, top - 0.16, "LEVEL 1 — PLAN REV I", size=9.5, bold=True)
        sh.text(3.55, top - 0.31, "D-065 bay · D-067 annex · D-069 bump-out", size=6.0)
    elif rb:
        sh.text(3.55, top - 0.16, "LEVEL 1 — PLAN REV H", size=9.5, bold=True)
        sh.text(3.55, top - 0.31, "D-065 bay · D-067 annex", size=6.0)
    else:
        sh.text(1.0, top - 0.16, "LEVEL 1 — LIFE SAFETY (PLAN REV G)", size=9.5, bold=True)
        sh.text(1.0, top - 0.31, f"{lm['scale_text']} · north up (approximate) · E1 bank drawn (Option 1 DECIDED)", size=6.0)
    ck = lv1["checkpoint"]["rect"]
    pl.fill(ck, "#DDEFE0" if rb else LRED, L_TAG)
    for r in lv1["rooms"]:
        pl.rect(r["rect"], L_ROOM, lw=0.45)
    for z in lv1["zones"]:
        if z["id"] in ("athlete", "exit_n", "exit_e", "ath_route", "conc_w", "team_asm"):
            pl.rect(z["rect"], L_ROOM, lw=0.3)
    av, fl = plan["arena_volume"]["rect"], plan["event_floor"]["rect"]
    pl.rect(av, L_ROOM, lw=0.5)
    pl.rect(fl, L_ROOM, lw=0.9)
    for b in plan["tiers"]["lower"]["bands"]:
        r = b["rect"]
        horiz = (r[2] - r[0]) >= (r[3] - r[1])
        for k in range(1, 6):
            if horiz:
                yy = r[1] + k * 2
                pl.line(r[0], yy, r[2], yy, L_SEAT, lw=0.15)
            else:
                xx = r[0] + k * 2
                pl.line(xx, r[1], xx, r[3], L_SEAT, lw=0.15)
    for o in plan["tiers"]["lower"]["openings"]:
        pl.fill(o["rect"], "#FFFFFF", L_SEAT)
        pl.rect(o["rect"], L_SEAT, lw=0.4)
    outline(pl, plan)
    stairs(pl, plan, {"ST-1": (42.7, 221, "center"), "ST-2": (176, 250, "right"), "ST-3": (183, 4, "right"), "ST-4": (16, 4, "left")})
    # checkpoint
    pl.rect(ck, L_TAG, lw=0.8)
    if rb:
        cw = lv1["checkpoint"]["clear"]
        pl.text((ck[0] + ck[2]) / 2, ck[1] + 15, "SCREEN", size=4.0, bold=True, align="center", layer=L_TAG, color=GRN)
        pl.text((ck[0] + ck[2]) / 2, ck[1] + 9.5, "BAY", size=4.0, bold=True, align="center", layer=L_TAG, color=GRN)
        pl.line(cw["from_x"], 19, cw["to_x"], 19, L_SEP, lw=0.5)
        for xx_ in (cw["from_x"], cw["to_x"]):
            pl.line(xx_, 17, xx_, 21, L_SEP, lw=0.5)
        pl.text((cw["from_x"] + cw["to_x"]) / 2, 21.5, f"{cw['width_in']} in CLEAR", size=4.0, bold=True, align="center", layer=L_SEP, color=GRN)
    else:
        pl.text((ck[0] + ck[2]) / 2, ck[1] + 6.5, "CHECKPOINT", size=4.0, bold=True, align="center", layer=L_TAG, color=RED)
        pl.text((ck[0] + ck[2]) / 2, ck[1] + 2.2, "CONFLICT (D-065)", size=3.9, bold=True, align="center", layer=L_TAG, color=RED)
    # E1 bank (outer + inner)
    for k in range(e1["pairs"]):
        xa = e1["x0"] + k * (e1["pair_ft"] + e1["mullion_ft"])
        pl.line(xa, 0, xa + e1["pair_ft"], 0, L_EXIT, lw=2.6)
        pl.line(xa + 0.4, e1["inner_bank_y"], xa + e1["pair_ft"] - 0.4, e1["inner_bank_y"], L_EXIT, lw=1.3)
        arrow(pl, xa + e1["pair_ft"] / 2, 0, 0, -1, lw=0.6)
    pl.text(113, -14.5, f"E1 — {e1['pairs']} PAIRS x {e1['clear_in_per_pair']} in = {e1['clear_in']} in CLEAR → {n0(occ(e1['clear_in'], c['df']))} occ.",
            size=5.4, bold=True, align="center", layer=L_EXIT)
    pl.text(113, -20.5, "main exit (1030.2) · vestibule inner bank the same (1003.6) · 64 in / pair ASSUMED", size=4.6, align="center", layer=L_EXIT)
    # other exits
    cap = occ(c["dw"], c["df"])
    bx1, by1 = plan["building"]["rect"][2], plan["building"]["rect"][3]
    for x_ in lv1["doors"]["items"]:
        if x_["kind"] != "exit":
            continue
        w_, at = x_["wall"], x_["at"]
        sd = x_["id"] in d["code"]["egress"]["stair_discharge"]
        lab = f"{x_['id']} 64 in" + (" (ST)" if sd else f" · {n0(cap)}")
        if w_ == "N":
            pl.line(at - 3, by1, at + 3, by1, L_EXIT, lw=2.6); arrow(pl, at, by1, 0, 1)
            pl.text(at + 2.2 if not (rb and x_["id"] == "X4") else at - 2.2, by1 + 4.2, lab, size=4.6, bold=True, layer=L_EXIT,
                    align="right" if rb and x_["id"] == "X4" else "left")
        elif w_ == "S":
            pl.line(at - 3, 0, at + 3, 0, L_EXIT, lw=2.6); arrow(pl, at, 0, 0, -1)
            pl.text(at, -11.5, lab, size=4.6, bold=True, align="center", layer=L_EXIT)
        elif w_ == "W":
            pl.line(0, at - 3, 0, at + 3, L_EXIT, lw=2.6); arrow(pl, 0, at, -1, 0)
            pl.text(-4.5, at + 4, lab, size=4.6, bold=True, align="center", layer=L_EXIT, rot=90)
        else:
            yy = at if x_["id"] != "X6" else at
            xw = x_.get("x", bx1 if at < 252 else 210)
            pl.line(xw, at - 3, xw, at + 3, L_EXIT, lw=2.6); arrow(pl, xw, at, 1, 0)
            pl.text(xw + 3, at + 3.0, lab, size=4.6, bold=True, layer=L_EXIT)
    # occupant loads
    t5 = dict(size=4.6, align="center", layer=L_TAG)
    olp = {"boys_locker": (21, 182), "girls_locker": (21, 120), "evl_1": (107.8, 238), "evl_2": (148, 238),
           "evl_3": (199, 203.5), "evl_4": (199, 154.6), "team_asm": (28, 37), "storage_sw": (38, 9),
           "equip_storage": (68.5, 238), "equip_room": (86.3, 238), "mech_nw": (18, 238), "mech_n": (175, 238),
           "mech_e": (199, 95), "mech_ne": (198, 235), "first_aid": (136, 31.5), "concession": (134.5, 46)}
    if rb:
        olp.update(first_aid=(204, 40.5), concession=(172.5, 45), storage_annex=(87, 265))
    for i, (x_, y_) in olp.items():
        pl.text(x_, y_, f"{ol[i]}", **t5, bold=True)
    if rb:
        pl.text(87, 271, "STORAGE ANNEX", size=4.2, align="center", layer=L_TAG)
        s1 = next(x_ for x_ in lv1["doors"]["items"] if x_["id"] == "S1")
        pl.line(s1["at"] - 3, s1["y"], s1["at"] + 3, s1["y"], L_EXIT, lw=1.6)
        pl.text(s1["at"], s1["y"] + 2.5, "S1", size=4.2, bold=True, align="center", layer=L_TAG)
    if rc:
        pl.text(225, 203, "WOMEN (2)", size=3.9, bold=True, align="center", layer=L_TAG)
        pl.text(225, 197.5, "24 WC · 7 LAV", size=3.6, align="center", layer=L_TAG)
        pl.text(222.5, 166, "MEN (2)", size=3.6, bold=True, align="center", layer=L_TAG)
        draw_path(pl, paths["T7"], RED, 243.5, 207)
    pl.text(116, 150, "EVENT FLOOR 16,416 SF (D-054 CHAIRS-ONLY)" if rb else "EVENT FLOOR 16,416 SF (D-054 OPEN)", size=5.2, bold=True, align="center", layer=L_TAG)
    if rb:
        pl.text(116, 143.5, f"chairs 7 net = {n0(d['wc']['floor'])} occ. (DESIGN, D-054)", size=4.8, align="center", layer=L_TAG, color=GRN)
    else:
        pl.text(116, 143.5, f"standing 5 net = {n0(d['wc']['floor'])} occ. (WORST, design)", size=4.8, align="center", layer=L_TAG, color=RED)
    pl.text(116, 137.5, " / ".join(f"{x_['id']} {n0(x_['floor'])}" for x_ in d["cases"][:3]), size=4.4, align="center", layer=L_TAG)
    pl.text(116, 61.2, f"LOWER TIER {n0(d['seats_l'])} seats (N / S / E)", size=4.4, align="center", layer=L_TAG)
    pl.text(113, 47, "LOBBY", size=4.8, bold=True, align="center", layer=L_TAG)
    pl.text(113, 42, "(not added, 1004)", size=4.0, align="center", layer=L_TAG)
    # travel paths L1 + separation
    draw_path(pl, paths["T1"], RED, 120, 183)
    draw_path(pl, paths["T2"], RED, 150, 71.5)
    draw_path(pl, paths["T3"], RED, 43, 76)
    sp = c["seps"][0]
    pl.line(sp["a_pt"][0], sp["a_pt"][1] + 11, sp["b_pt"][0], sp["b_pt"][1] - 1, L_SEP, lw=0.4)
    pl.text(sp["a_pt"][0] + 1.8, 74, f"SEPARATION E1-X5 {sp['dist']:.0f}' ≥ {sp['req']:.1f}'", size=4.5, layer=L_SEP, color=GRN, rot=90)

    # ---------------------------------------------------------------- LEVEL 2
    xl2 = 6.55 if rc else 6.35                         # Rev C: L2 plan 0.2 in right of the L1 bump-out + X7 label
    pl2 = Plan(sh, xl2, py0, s)
    sh.text(xl2, top - 0.16, "LEVEL 2 — LIFE SAFETY (PLAN REV F, UNCHANGED)", size=9.5, bold=True)
    sh.text(xl2, top - 0.31, f"{lm['scale_text']} · 4 stairs 76 in (D-052) = the L2 exits · loop = upper concourse on event days", size=6.0)
    for ob in lv2["open_below"]:
        r = ob["rect"]
        pl2.rect(r, L_ROOM, lw=0.3)
        pl2.dashed(r[0], r[1], r[2], r[3], L_ROOM, lw=0.2, dash=0.04, gap=0.05)
        pl2.dashed(r[0], r[3], r[2], r[1], L_ROOM, lw=0.2, dash=0.04, gap=0.05)
    for r in lv2["rooms"]:
        pl2.rect(r["rect"], L_ROOM, lw=0.45)
    for z in lv2["zones"]:
        pl2.rect(z["rect"], L_ROOM, lw=0.3)
    lp = lv2["loop"]
    pl2.rect(lp["outer"], L_ROOM, lw=0.6)
    pl2.rect(lp["inner"], L_ROOM, lw=0.6)
    for b in plan["tiers"]["upper"]["bands"]:
        r = b["rect"]
        horiz = (r[2] - r[0]) >= (r[3] - r[1])
        for k in range(1, 5):
            if horiz:
                yy = r[1] + k * 3
                pl2.line(r[0], yy, r[2], yy, L_SEAT, lw=0.15)
            else:
                xx = r[0] + k * 3
                pl2.line(xx, r[1], xx, r[3], L_SEAT, lw=0.15)
    outline(pl2, plan, annex=False)
    stc = occ(d["code"]["egress"]["stair_clear_in"], c["sfac"])
    stairs(pl2, plan, {"ST-1": (42.7, 221, "center"), "ST-2": (176, 250, "right"), "ST-3": (183, 4, "right"), "ST-4": (16, 4, "left")})
    for sid, (x_, y_, al) in {"ST-1": (34, 233, "right"), "ST-2": (176, 261, "right"), "ST-3": (183, 15, "right"), "ST-4": (3, 29, "left")}.items():
        pl2.text(x_, y_, f"76 in · {n0(stc)} occ.", size=4.5, bold=True, align=al, layer=L_EXIT)
    t5b = dict(size=4.6, align="center", layer=L_TAG)
    pl2.text(24.5, 196, f"S&C {ol['sc']}", **t5b, bold=True)
    pl2.text(24.5, 105, f"X-TRAIN {ol['xt']}", **t5b, bold=True)
    pl2.text(32.5, 9, f"ADMIN {ol['admin']}", **t5b, bold=True)
    pl2.text(122, 150, f"UPPER TIER {n0(d['seats_u'])} seats (N / S / E)", size=4.8, bold=True, align="center", layer=L_TAG)
    sens = d["sens"]
    pl2.text(122, 143.5, f"+ loop {sens[0]['load']} + rail {sens[1]['load']} (R-018) → L2 {n0(c['l2w'])} occ.", size=4.6, align="center", layer=L_TAG, color=RED)
    pl2.text(122, 137.5, "OPEN TO ARENA BELOW", size=4.4, align="center", layer=L_TAG)
    draw_path(pl2, paths["T4"], RED, 184, 195, "right")
    draw_path(pl2, paths["T5"], RED, 150, 30)
    draw_path(pl2, paths["T6"], RED, 3, 148)
    st_ = {s_["id"]: s_["rect"] for s_ in plan["vertical"]["stairs"]}
    for sp in c["seps"][1:]:
        a, b = st_[sp["a"]], st_[sp["b"]]
        if sp["a"] == "ST-1":
            p0, p1 = (a[2], a[1]), (b[0], b[3])
        else:
            p0, p1 = (a[0], a[1]), (b[2], b[3])
        pl2.line(p0[0], p0[1], p1[0], p1[1], L_SEP, lw=0.4)
    s1, s2 = c["seps"][1], c["seps"][2]
    pl2.text(112, 118, f"{s1['a']}-{s1['b']} {s1['dist']:.0f}' · {s2['a']}-{s2['b']} {s2['dist']:.0f}' ≥ {s1['req']:.1f}'", size=4.5, align="center",
             layer=L_SEP, color=GRN)

    # ---------------------------------------------------------------- tables under the plans
    yt = py0 - 0.50
    c1 = g2.Col(sh, 0.75, yt, 5.3, 1.0)
    c1.head("L1 EXITS — CAPACITY (0.15 in / occ., 1005.3.2 exc.)", size=7.0)
    rows = [((f"E1 main (bank)", f"{e1['clear_in']}", n0(occ(e1["clear_in"], c["df"])), "lobby, portal, south tier, concourses"), dict(bold=True)),
            ((f"{', '.join(c['others'])}", f"{len(c['others'])} x 64 = {len(c['others']) * 64}", f"{n0(cap)} each", "exit-only doors (64 in pair ASSUMED)"), None),
            ((f"{', '.join(d['code']['egress']['stair_discharge'])}", f"{c['nsd']} x 64 = {c['nsd'] * 64}", f"{c['nsd']} x {n1(64 - c['sd_l2'])} in left",
              f"stair discharge: L2 uses {n1(c['sd_l2'])} in each"), None)]
    cw_ = c["c_wc"]
    pf = lambda ok: ("PASS", GRN) if ok else ("FAIL", RED)  # noqa: E731
    chk = [("Total, building worst " + n0(cw_["total"]), cw_["req"], c["prov"], cw_["p_req"]),
           ("Main exit ≥ 1/2 (1030.2)", cw_["main"], e1["clear_in"], cw_["p_main"]),
           (f"Other L1 exits ≥ 1/2 of L1 {n0(d['wc']['l1'])} (1030.3)", cw_["oth"], c["other_prov"], cw_["p_oth"]),
           ("Lose E1, ≥ 50 % (1005.5)", cw_["lose_req"], cw_["lose"], cw_["p_lose"])]
    if rb:
        cm, cw_b = c["c_mc"], lv1["checkpoint"]["clear"]
        chk += [(f"Standing margin {n0(cm['total'])}: E1 (exits as drawn)", cm["main"], e1["clear_in"], cm["p_main"]),
                ("Lobby beside the screening bay (1003.6)", cm["main"], cw_b["width_in"], cw_b["width_in"] >= cm["main"])]
    for lab, req, prv, ok in chk:
        t_, col = pf(ok)
        rows.append(((lab, f"need {n1(req)}", f"have {n1(prv)}", t_), dict(colors={3: col}, rule=lab.startswith("Total"))))
    c1.table([("EXIT / CHECK", 0, "left", 2.0), ("CLEAR in", 2.75, "right"), ("CAPACITY", 3.5, "right"), ("SERVES / RESULT", 3.62, "left", 1.65)], rows, size=5.3, rh=0.118)
    c2 = g2.Col(sh, 6.25, yt, 4.4, 1.0)
    c2.head("L2 EXITS — STAIRS (0.2 in / occ., 1005.3.1 exc. 1)", size=7.0)
    stv = c["st"]
    corner = d["corner"] * c["sfac"]   # R-018.3 method, as on P2-G-002 Rev A
    rows2 = [(("ST-1 … ST-4", f"4 x 76 = {stv['prov']}", f"{n0(stc)} each", "one per corner, discharge X4 / X6 / X9 / X10"), dict(bold=True))]
    for lab, req, prv in ((f"Total, L2 worst {n0(c['l2w'])}", stv["req"], stv["prov"]), ("Lose one stair, ≥ 50 % (1005.5)", stv["lose_req"], stv["lose"]),
                          ("Loop at the worst corner (R-018.3, 0.2)", corner, 84)):
        t_, col = pf(prv >= req)
        rows2.append(((lab, f"need {n1(req)}", f"have {n1(prv)}", f"{t_} (+{n1(prv - req)})"), dict(colors={3: col}, rule=lab.startswith("Total"))))
    rows2.append((("4 exits from L2 (T1006.3.3, > 1,000)", "", "4 stairs", "PASS"), dict(colors={3: GRN})))
    c2.table([("EXIT / CHECK", 0, "left", 1.75), ("CLEAR in", 2.4, "right"), ("CAPACITY", 3.05, "right"), ("SERVES / RESULT", 3.15, "left", 1.25)], rows2, size=5.3, rh=0.118)

    # ---------------------------------------------------------------- right panel
    sh.line(10.82, top - 0.02, 10.82, body_bottom + 0.1, lw=0.4)
    cr = g2.Col(sh, 10.95, top + 0.12, 5.55, 1.0)
    cr.para(lm["disclaimer"], size=5.3, color=GRY)
    cr.head("LEGEND", size=7.0)
    cr.para("Heavy bar + arrow = exit door (clear in · occupants); E1 = 8 pair bars, outer + inner (vestibule) bank. Grey box = stair. "
            "Red dashed + dot = travel path (dot = remote point; feet, rectilinear). Green line = exit separation. "
            + ("Green zone = screening bay (D-065). " if c["rev"] in ("B", "C") else "Pink zone = checkpoint conflict. ") +
            "Numbers in rooms = occupant load (P2-G-002).", size=5.3)
    rb = c["rev"] in ("B", "C")
    cr.head(f"OCCUPANT LOADS (P2-G-002 REV {'B' if rb else 'A'}, IBC T1004.5)", size=7.0)
    cr.table([("CASE", 0, "left"), ("FLOOR", 1.85, "right"), ("L1", 2.45, "right"), ("BLDG", 3.05, "right"), ("E1 NEED", 3.95, "right")],
             [((x_["label"].replace(" — WORST", " (WORST)").replace(" (exercise 50 gross, ASSUMED)", " (50 gross)"), n0(x_["floor"]), n0(x_["l1"]),
                n0(x_["total"]), n1(x_["main"])), dict(bold=x_["id"] == d["wc"]["id"], color=(GRN if rb else RED) if x_["id"] == d["wc"]["id"] else None)) for x_ in c["cases"]]
             + [((f"Whole floor zone {n0(ls['basis']['floor_sensitivity']['area_sf'])} SF standing", n0(c["fl_s"]), n0(c["c_fs"]["total"] - c["l2w"]),
                  n0(c["c_fs"]["total"]), n1(c["c_fs"]["main"])), dict(rule=True))], size=5.2, rh=0.112)
    cr.para(f"L1 without the floor {n0(d['l1_fixed'])} (seats {n0(d['seats_l'])}); L2 {n0(d['l2_base'])} base, {n0(c['l2w'])} worst. "
            f"All cases pass with the 512 in bank; the whole-floor sensitivity still passes (E1 {n1(c['c_fs']['main'])} ≤ 512 in, total "
            f"{n1(c['c_fs']['req'])} ≤ {n0(c['prov'])} in).", size=5.3)
    cr.head("EXIT SEPARATION (1007.1.1 exc. 2, sprinklered)", size=7.0)
    sps = c["seps"]
    cr.para(f"Max overall diagonal {c['diag']:.1f} ft (SW corner to NE stair tower) → 1/3 = {c['diag'] / 3:.1f} ft "
            f"(1/2 = {c['diag'] / 2:.1f} ft unsprinklered). Measured to any point of a doorway / closest riser (1007.1.1.1)."
            + (f" All outline corners checked: bump-out NE {c['corner_d']['bumpout']:.1f} ft, annex NE {c['corner_d']['annex']:.1f} ft (shorter)." if rc else ""), size=5.3)
    for sp in sps:
        cr.para(f"L{sp['level']} {sp['a']} ↔ {sp['b']}: {sp['dist']:.1f} ft ≥ {sp['req']:.1f} ft — {'PASS' if sp['ok'] else 'FAIL'}. {sp['note']}.",
                size=5.3, bullet="·", color=None if sp["ok"] else RED)
    cr.para("Other exits a reasonable distance apart (1007.1.2): one stair per corner, exits on all four walls.", size=5.3, bullet="·")
    tv = ls["travel"]
    cr.head(f"TRAVEL DISTANCE ({tv['limit_cite'].split(':')[0].replace('IBC 2021 ', '')}: {tv['limit_ft']} FT)", size=7.0)
    cr.para(f"{tv['limit_cite']}. {tv['measure']}", size=5.3)
    for p in c["paths"]:
        ok = p["length"] <= tv["limit_ft"]
        cr.para(f"{p['id']} L{p['level']} {p['label']}: {p['length']:.0f} ft — {'≤ 250, PASS (UNVERIFIED)' if ok else 'FAIL'}", size=5.3, bullet="·")
    cr.para(tv["stair_note"], size=5.3)
    cr.head("COMMON PATH (T1006.2.1, 1030.8)", size=7.0)
    for r in ls["common_path"]["checks"]:
        cr.para(f"{r['space']} ({r['load']}): {r['result']} — {r['status']}.", size=5.3, bullet="·",
                color=GRY if r["status"].startswith("TBD") else None)
    cr.para("Rules: one exit only if ≤ 49 occ. and ≤ 75 ft (T1006.2.1, Group A, sprinklered); seats 30 ft to a choice of two paths (1030.8); "
            "unoccupied mech rooms exempt (1006.2.1 exc. 3).", size=5.3)
    fd = ls["findings"]
    fset = ((("screening", "SCREENING BAY vs EGRESS (D-065 DECIDED) — CHECK"), ("restrooms", "RESTROOMS — CORE 2 BUMP-OUT (D-069 DECIDED, OPTION 2)"),
             ("discharge", "EXIT DISCHARGE — 40 FT WALK (D-066 DECIDED) — CHECK")) if rc else
            (("screening", "SCREENING BAY vs EGRESS (D-065 DECIDED) — CHECK"), ("restrooms", "FINDING — RESTROOM SPACE, CHAIRS-ONLY (D-069 OPEN)"),
             ("discharge", "EXIT DISCHARGE — 40 FT WALK (D-066 DECIDED) — CHECK")) if rb else
            (("checkpoint", "FINDING — SECURITY CHECKPOINT vs EGRESS (OPEN)"), ("restrooms", "FINDING — RESTROOMS AT THE WORST CASE (OPEN)")))
    for k, title in fset:
        f_ = fd[k]
        cr.head(title, size=7.0)
        cr.para(f_["text"], size=5.3, color=(GRN if f_["status"] == "DECIDED" else None if rc and f_["status"] == "CHECK" else RED) if rb else RED)
        for o in f_.get("options", []):
            cr.para(o, size=5.3, bullet="·")
    c1.head("TBD", size=7.0)
    if not rb:
        c1.para(fd["discharge"]["text"], size=5.3, bullet="·")
    c1.para("Door widths, hardware and the 10 ft open space / street frontage at E1 (1030.2): architect. Seating aisles, rails, "
            "smoke-protected seating (1030.6.2): TBD. Structure 1'-6\" ASSUMED (zero margin at 7'-6\").", size=5.3, bullet="·")
    if rc:
        c2.head("EXIT (E) THROUGH THE BUMP-OUT (D-069) — CHECK", size=7.0)
        c2.para(fd["bumpout"]["text"], size=5.3)
    c2.para("Sources: P2-G-002 Rev B; P2-A-101 Rev I / A-102 Rev F (params/phase2_plan_rev_i.yaml); params/phase2_life_safety_rev_c.yaml; IBC 2021 "
            "1003.6, 1006.2.1, 1007.1, 1017.2-3, T1020.3, 1028, 1030.2-3, 2902.3.3; Shane 1:21-1:22 + 3:31 PM CT." if rc else
            "Sources: P2-G-002 Rev B; P2-A-101 Rev H / A-102 Rev F (params/phase2_plan_rev_h.yaml); params/phase2_life_safety_rev_b.yaml; Shane 1:21-1:22 PM CT; " if rb else
            "Sources: P2-G-002 Rev A; P2-A-101 Rev G / A-102 Rev F (params/phase2_plan_rev_g.yaml); params/phase2_life_safety.yaml; "
            "IBC 2021 1003.6, 1005.3, 1005.5, 1006.2.1, 1007.1, 1010.5, 1017.2-3, 1028.3, 1030.2-3, 1030.8 (UpCodes, retrieved 2026-10-04; "
            "R-007, R-015, R-018); Shane 2026-10-04 11:07 AM CT.", size=5.0, color=GRY)
    return sh, body_bottom, [c1, c2, cr]


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
        for k in ("prov", "other_prov", "sd_l2", "fl_s", "diag", "l2w", "tot"):
            print(k, c[k])
        print("wc", {k: (round(v, 1) if isinstance(v, float) else v) for k, v in c["c_wc"].items()})
        print("fs", {k: (round(v, 1) if isinstance(v, float) else v) for k, v in c["c_fs"].items()})
        print("st", c["st"])
        for p in c["paths"]:
            print(p["id"], p["level"], round(p["length"], 1), p["label"])
        for s_ in c["seps"]:
            print(s_["level"], s_["a"], s_["b"], round(s_["dist"], 1), round(s_["req"], 1), s_["ok"])
        print("room_ol", c["room_ol"])
        return
    p2 = c["d"]["p2"]
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
