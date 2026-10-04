"""KEYSTONE P2-A-401 ENLARGED PLANS — EVENT LOCKER ROOMS 1-4 (Phase 2, BACKLOG P2-T-010). Tabloid, 1/8" = 1'-0".

Rev A (2026-10-04, Shane 11:24 AM CT): the 4 event locker rooms only (900 SF each = 3,600 SF, D-060; under the upper tier at the tier
line, D-061). Doors placed so the common path is <= 75 ft (IBC 2021 Table 1006.2.1), measured and reported per room. Lockers,
benches, toilets and showers ASSUMED (KEYSTONE); accessible fixture sizes / clearances are ADA 2010 minimums (cited). The L1 public
restroom core waits on D-064 and is noted, not drawn.
Data: params/phase2_enlarged.yaml, params/phase2_plan_rev_g.yaml.
Usage (from the repo root):
  /workspace/.venv-keystone/bin/python blueprints/phase2/src/p2_a_401.py [--rev A] [--png PATH] [--out-dir DIR] [--force] [--print]
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
SHEET_NO = "P2-A-401"
RED, GRN, GRY = "#CC0000", "#1E7B34", "#555555"
L_WALL, L_PART, L_FIX, L_CLR, L_TAG, L_DIM, L_DOOR, L_PATH = ("A-WALL", "A-WALL-PRTN", "P-FIXT", "A-CLER-ADA", "A-ANNO-TEXT",
                                                           "A-ANNO-DIMS", "A-DOOR", "LS-CPTH")
NAMES = {"evl_1": "EVENT LOCKER ROOM 1", "evl_2": "EVENT LOCKER ROOM 2", "evl_3": "EVENT LOCKER ROOM 3", "evl_4": "EVENT LOCKER ROOM 4"}


def rd(n):
    return yaml.safe_load((BP / "params" / n).read_text(encoding="utf-8"))


def plen(pts):
    return sum(abs(b[0] - a[0]) + abs(b[1] - a[1]) for a, b in zip(pts[:-1], pts[1:]))


def compute():
    en, plan = rd("phase2_enlarged.yaml"), rd("phase2_plan_rev_g.yaml")
    rects = {r["id"]: r["rect"] for r in plan["level_1"]["rooms"]}
    doors = {d["id"]: d for d in plan["level_1"]["doors"]["items"]}
    bx1, by1 = plan["building"]["rect"][2], plan["building"]["rect"][3]
    lim = en["rules"]["common_path"]["limit_ft"]
    rooms = []
    for b in en["basis"]["rooms"]:
        r = rects[b["id"]]
        tp = en["templates"][b["template"]]
        w_, d_ = r[2] - r[0], r[3] - r[1]
        if abs(w_ - tp["W"]) > 0.01 or abs(d_ - tp["D"]) > 0.01:
            sys.exit(f"{b['id']}: plan envelope {w_:.2f} x {d_:.2f} differs from template {tp['W']} x {tp['D']}")
        area = w_ * d_
        occ = math.ceil(round(area) / en["basis"]["occupant_factor_sf"])
        routes = [dict(q, length=plen(q["pts"])) for q in tp["cp_routes"]]
        worst = max(routes, key=lambda q: q["length"])
        # door centre (global) and the travel on to the exit door
        lo, hi = tp["door"]["at"]
        if tp["door"]["wall"] == "E":
            lx, ly = tp["W"], (lo + hi) / 2
        else:
            lx, ly = (lo + hi) / 2, 0.0
        mx, my = b["mirror"] == "x", b["mirror"] == "y"
        gx = r[0] + (tp["W"] - lx if mx else lx)
        gy = r[1] + (tp["D"] - ly if my else ly)
        ex = doors[b["exit"]]
        ept = (ex["at"], by1) if ex["wall"] == "N" else (bx1, ex["at"])
        onward = abs(ept[0] - gx) + abs(ept[1] - gy)
        lk = [i for i in tp["items"] if i["t"] == "lockers"]
        nl, na = sum(i["n"] for i in lk), sum(i["acc"] for i in lk)
        cnt = dict(wc_acc=0, wc_amb=0, lav=0, lav_acc=0, sh_roll=0, sh=0, bench=0, bench_acc=0)
        for i in tp["items"]:
            t = i["t"]
            if t == "lav":
                cnt["lav"] += 1
                cnt["lav_acc"] += 1 if i.get("acc") else 0
            elif t == "shower_rollin":
                cnt["sh_roll"] += 1
            elif t == "shower":
                cnt["sh"] += 1
            elif t in cnt:
                cnt[t] += 1
        rooms.append(dict(id=b["id"], b=b, tp=tp, rect=r, area=area, occ=occ, routes=routes, worst=worst, ok=worst["length"] <= lim and occ <= en["rules"]["common_path"]["max_occupants"],
                          door_g=(gx, gy), onward=onward, travel=worst["length"] + onward, lockers=nl, lockers_acc=na,
                          lockers_req=max(1, math.ceil(nl * en["rules"]["lockers"]["accessible_pct"] / 100)), cnt=cnt))
    total = sum(r_["area"] for r_ in rooms)
    if abs(total - 3600) > 1:
        sys.exit(f"event lockers total {total:.1f} SF, not 3,600 (D-060)")
    return dict(en=en, plan=plan, rooms=rooms, total=total, lim=lim)


class Room:
    """Draws one template room at sheet origin (ox, oy) with mirroring; all inputs in template-local feet."""

    def __init__(self, sh, rm, ox, oy, s):
        self.sh, self.rm, self.ox, self.oy, self.s = sh, rm, ox, oy, s
        self.tp = rm["tp"]
        self.mx, self.my = rm["b"]["mirror"] == "x", rm["b"]["mirror"] == "y"

    def T(self, x, y):
        x = self.tp["W"] - x if self.mx else x
        y = self.tp["D"] - y if self.my else y
        return self.ox + x * self.s, self.oy + y * self.s

    def line(self, x1, y1, x2, y2, layer, lw=0.6):
        a, b = self.T(x1, y1)
        c, d = self.T(x2, y2)
        self.sh.line(a, b, c, d, layer=layer, lw=lw)

    def dashed(self, x1, y1, x2, y2, layer, lw=0.4, dash=0.035, gap=0.025):
        a, b = self.T(x1, y1)
        c, d = self.T(x2, y2)
        self.sh.dashed(a, b, c, d, layer=layer, lw=lw, dash=dash, gap=gap)

    def rect(self, r, layer, lw=0.6, dash=False):
        f = self.dashed if dash else self.line
        for a in ((r[0], r[1], r[2], r[1]), (r[2], r[1], r[2], r[3]), (r[2], r[3], r[0], r[3]), (r[0], r[3], r[0], r[1])):
            f(*a, layer=layer, lw=lw)

    def poly(self, pts, layer, lw=0.5, fill=None):
        self.sh.poly([self.T(*p) for p in pts], fill=fill, layer=layer, lw=lw)

    def text(self, x, y, s, **kw):
        a, b = self.T(x, y)
        self.sh.text(a, b, s, **kw)

    def door(self, hx, hy, lx, ly, u, layer=L_DOOR, lw=0.5):
        w = math.hypot(lx - hx, ly - hy)
        ux, uy = u
        self.line(hx, hy, hx + ux * w, hy + uy * w, layer, lw=lw)
        pts = []
        for k in range(13):
            t = math.pi / 2 * k / 12
            pts.append((hx + math.cos(t) * (lx - hx) + math.sin(t) * ux * w, hy + math.cos(t) * (ly - hy) + math.sin(t) * uy * w))
        for a, b in zip(pts[:-1], pts[1:]):
            self.line(a[0], a[1], b[0], b[1], layer, lw=0.25)

    def ellipse(self, cx, cy, ax, ay, layer, lw=0.4, dash=False):
        pts = [(cx + ax * math.cos(2 * math.pi * k / 24), cy + ay * math.sin(2 * math.pi * k / 24)) for k in range(25)]
        for i, (a, b) in enumerate(zip(pts[:-1], pts[1:])):
            if dash and i % 2:
                continue
            self.line(a[0], a[1], b[0], b[1], layer, lw=lw)


DIRS = {"+x": (1, 0), "-x": (-1, 0), "+y": (0, 1), "-y": (0, -1)}


def draw_room(sh, rm, ox, oy, s, show_route=True):
    R = Room(sh, rm, ox, oy, s)
    tp = R.tp
    Wt, Dt = tp["W"], tp["D"]
    dr = tp["door"]
    lo, hi = dr["at"]
    # exterior / room walls with the door gap
    walls = {"S": [(0, 0, Wt, 0)], "E": [(Wt, 0, Wt, Dt)], "N": [(Wt, Dt, 0, Dt)], "W": [(0, Dt, 0, 0)]}
    if dr["wall"] == "E":
        walls["E"] = [(Wt, 0, Wt, lo), (Wt, hi, Wt, Dt)]
        hinge, latch, u = (Wt, dr["hinge"]), (Wt, hi if dr["hinge"] == lo else lo), (-1, 0)
    else:
        walls["S"] = [(0, 0, lo, 0), (hi, 0, Wt, 0)]
        hinge, latch, u = (dr["hinge"], 0), (hi if dr["hinge"] == lo else lo, 0), (0, 1)
    for segs in walls.values():
        for a in segs:
            R.line(*a, layer=L_WALL, lw=2.2)
    R.door(hinge[0], hinge[1], latch[0], latch[1], u, lw=0.9)
    for a in tp["partitions"]["lines"]:
        R.line(*a, layer=L_PART, lw=1.1)
    for hx, hy, lx, ly, _lab, sw in tp["inner_doors"]["items"]:
        R.door(hx, hy, lx, ly, DIRS[sw])
    # under-tier line
    ut = tp["under_tier"]
    if ut["side"] == "S":
        R.dashed(0, ut["depth_ft"], Wt, ut["depth_ft"], L_TAG, lw=0.35, dash=0.08, gap=0.05)
        R.text(Wt * 0.62, ut["depth_ft"] - 0.9, "— — upper tier above this line (to the tier line: 7'-6\" clear, D-061)", size=4.3, align="center", layer=L_TAG, color=GRY)
    else:
        R.dashed(ut["depth_ft"], 0, ut["depth_ft"], Dt, L_TAG, lw=0.35, dash=0.08, gap=0.05)
        a, b = R.T(ut["depth_ft"] - 0.8, Dt * 0.42)
        sh.text(a, b, "upper tier above (west of the dashed line), 7'-6\" clear at the tier line — D-061", size=4.3, align="center", layer=L_TAG, color=GRY, rot=90)
    for it in tp["items"]:
        t = it["t"]
        if t in ("wc_acc", "wc_amb"):
            r = it["r"]
            R.rect(r, L_PART, lw=0.5)
            wx, wy = it["wc"]
            rear = r[3] if wy > (r[1] + r[3]) / 2 else r[1]
            sg = -1 if rear == r[3] else 1
            R.poly([(wx - 0.8, rear), (wx + 0.8, rear), (wx + 0.8, rear + sg * 0.6), (wx - 0.8, rear + sg * 0.6)], L_FIX, lw=0.5)
            R.ellipse(wx, rear + sg * 1.5, 0.6, 0.9, L_FIX)
            R.text((r[0] + r[2]) / 2 + (0.4 if t == "wc_acc" else 0), (r[1] + r[3]) / 2 - 1.6, it["label"].split(" (")[0], size=3.6, align="center", layer=L_TAG)
        elif t == "lav":
            r = it["r"]
            R.rect(r, L_FIX, lw=0.5)
            R.ellipse((r[0] + r[2]) / 2, (r[1] + r[3]) / 2, 0.55, 0.75, L_FIX, lw=0.3)
            if it.get("acc"):
                R.text(r[2] + 0.2, (r[1] + r[3]) / 2 - 0.3, "A", size=4.0, bold=True, layer=L_TAG)
        elif t == "clear":
            R.rect(it["r"], L_CLR, lw=0.3, dash=True)
            r = it["r"]
            R.text((r[0] + r[2]) / 2, (r[1] + r[3]) / 2 - 0.3, it["label"], size=3.4, align="center", layer=L_CLR, color=GRY)
        elif t == "turn":
            cx, cy = it["c"]
            R.ellipse(cx, cy, it["rad"], it["rad"], L_CLR, lw=0.35, dash=True)
            R.text(cx, cy - 0.3, "60\" TURN", size=3.6, align="center", layer=L_CLR, color=GRY)
        elif t in ("shower", "shower_rollin"):
            r = it["r"]
            R.rect(r, L_FIX, lw=0.6)
            R.line(r[0], r[1], r[2], r[3], L_FIX, lw=0.2)
            R.line(r[0], r[3], r[2], r[1], L_FIX, lw=0.2)
            if t == "shower_rollin":
                R.text((r[0] + r[2]) / 2, (r[1] + r[3]) / 2 + 0.25, "ROLL-IN", size=3.6, bold=True, align="center", layer=L_TAG)
        elif t == "label":
            R.text(it["at"][0], it["at"][1], it["label"], size=4.0, align="center", layer=L_TAG, color=GRY)
        elif t == "lockers":
            r = it["r"]
            R.rect(r, L_FIX, lw=0.6)
            horiz = (r[2] - r[0]) > (r[3] - r[1])
            n = it["n"]
            step = ((r[2] - r[0]) if horiz else (r[3] - r[1])) / n
            for k in range(1, n):
                if horiz:
                    R.line(r[0] + k * step, r[1], r[0] + k * step, r[3], L_FIX, lw=0.2)
                else:
                    R.line(r[0], r[1] + k * step, r[2], r[1] + k * step, L_FIX, lw=0.2)
            # accessible locker(s) at the end nearest the room door
            dcx, dcy = (Wt, (lo + hi) / 2) if dr["wall"] == "E" else ((lo + hi) / 2, 0)
            if horiz:
                hi_end = abs(r[2] - dcx) < abs(r[0] - dcx)
                ks = range(n - it["acc"], n) if hi_end else range(it["acc"])
                for k in ks:
                    R.text(r[0] + (k + 0.5) * step, (r[1] + r[3]) / 2 - 0.3, "A", size=3.6, bold=True, align="center", layer=L_TAG)
            else:
                hi_end = abs(r[3] - dcy) < abs(r[1] - dcy)
                ks = range(n - it["acc"], n) if hi_end else range(it["acc"])
                for k in ks:
                    R.text((r[0] + r[2]) / 2, r[1] + (k + 0.5) * step - 0.3, "A", size=3.6, bold=True, align="center", layer=L_TAG)
        elif t in ("bench", "bench_acc", "table"):
            r = it["r"]
            R.rect(r, L_FIX, lw=0.6 if t != "table" else 0.45)
            if t == "bench_acc":
                R.line(r[0], r[1], r[2], r[3], L_FIX, lw=0.2)
                R.line(r[0], r[3], r[2], r[1], L_FIX, lw=0.2)
            lab = it["label"]
            horiz = (r[2] - r[0]) >= (r[3] - r[1])
            if t == "bench_acc":
                pass
            elif horiz:
                R.text((r[0] + r[2]) / 2, (r[1] + r[3]) / 2 - 0.3, lab, size=3.6, align="center", layer=L_TAG)
            else:
                a, b = R.T((r[0] + r[2]) / 2 + 0.25, (r[1] + r[3]) / 2)
                sh.text(a, b, lab, size=3.6, align="center", layer=L_TAG, rot=90)
    # common path (worst route)
    if show_route:
        wr = rm["worst"]["pts"]
        for a, b in zip(wr[:-1], wr[1:]):
            # rectilinear legs: x first, then y
            R.dashed(a[0], a[1], b[0], a[1], L_PATH, lw=0.9, dash=0.05, gap=0.03)
            R.dashed(b[0], a[1], b[0], b[1], L_PATH, lw=0.9, dash=0.05, gap=0.03)
        x0, y0 = wr[0]
        a, b = R.T(x0, y0)
        sh.poly([(a - 0.025, b - 0.025), (a + 0.025, b - 0.025), (a + 0.025, b + 0.025), (a - 0.025, b + 0.025)], fill="#000000", layer=L_PATH, lw=0)
        if "tag_at" in rm["worst"]:
            R.text(*rm["worst"]["tag_at"], f"CP {rm['worst']['length']:.0f}'", size=4.6, bold=True, align="center", layer=L_PATH, color=RED)
    return R


def build(c):
    en, plan = c["en"], c["plan"]
    p2 = rd("phase2.yaml")
    meta2, em = p2["meta"], en["meta"]
    sh = Sheet(W, H)
    body_bottom = add_titleblock(sh, {
        "project": f"{meta2['project']}\n{meta2['arena_name']} · {meta2['location']}",
        "phase": "PHASE 2",
        "title": "ENLARGED PLANS\nEVENT LOCKER ROOMS 1-4",
        "scale": em["scale_text"],
        "date": meta2["sheet_date"],
        "revision": em["revision"],
        "drawn_by": meta2["drawn_by"],
        "sheet_no": SHEET_NO,
        "stamp": meta2["stamp"],
    }, margin=M, tb_h=0.95, stamp_h=0.40)
    top = H - M - 0.12
    s = 1.0 / em["scale_ft_per_in"]
    rooms = {r["id"]: r for r in c["rooms"]}
    pos = {"evl_1": (1.0, 6.55), "evl_2": (1.0, 2.45), "evl_3": (5.65, 4.55), "evl_4": (8.75, 4.55)}
    for rid, (ox, oy) in pos.items():
        rm = rooms[rid]
        tp = rm["tp"]
        draw_room(sh, rm, ox, oy, s)
        wft, dft = tp["W"], tp["D"]
        wi, di = wft * s, dft * s
        # dimensions
        yd = oy - 0.12
        sh.line(ox, yd, ox + wi, yd, layer=L_DIM, lw=0.35)
        for xx in (ox, ox + wi):
            sh.line(xx, yd - 0.04, xx, yd + 0.04, layer=L_DIM, lw=0.35)
        sh.text(ox + wi / 2, yd - 0.1, ft_in(wft), size=5.5, align="center", layer=L_DIM)
        xd = ox - 0.12
        sh.line(xd, oy, xd, oy + di, layer=L_DIM, lw=0.35)
        for yy in (oy, oy + di):
            sh.line(xd - 0.04, yy, xd + 0.04, yy, layer=L_DIM, lw=0.35)
        sh.text(xd - 0.05, oy + di / 2, ft_in(dft), size=5.5, align="center", layer=L_DIM, rot=90)
        # title
        door_side = {"E": "E", "S": "S"}[tp["door"]["wall"]]
        if rm["b"]["mirror"] == "x":
            door_side = "W"
        if rm["b"]["mirror"] == "y":
            door_side = "N"
        ty = oy + di + 0.17
        sh.text(ox, ty, f"{NAMES[rid]} — {rm['area']:,.0f} SF · {rm['occ']} occ.", size=7.6, bold=True)
        wr = rm["worst"]
        col = GRN if rm["ok"] else RED
        sub = (f"{em['scale_text']} · door on the {door_side} wall → {rm['b']['door_to'].split(' →')[0]} · "
               f"common path {wr['length']:.0f} ft ≤ {c['lim']} ({'PASS' if rm['ok'] else 'FAIL'})")
        sh.text(ox, ty - 0.115, sub, size=4.9, color=col)
    # ---------------- key plan
    kx, ky, ks = 5.55, 2.2, 1.0 / 150
    bx0, by0, bx1, by1 = plan["building"]["rect"]
    pj = plan["building"]["projection"]["rect"]
    pts = [(bx0, by0), (bx1, by0), (bx1, pj[3]), (pj[0], pj[3]), (pj[0], by1), (bx0, by1), (bx0, by0)]
    KP = lambda x, y: (kx + x * ks, ky + y * ks)  # noqa: E731
    for (xa, ya), (xb, yb) in zip(pts[:-1], pts[1:]):
        a, b = KP(xa, ya)
        c2, d2 = KP(xb, yb)
        sh.line(a, b, c2, d2, layer=L_WALL, lw=1.0)
    a, b = KP(*plan["arena_volume"]["rect"][:2])
    av = plan["arena_volume"]["rect"]
    sh.rect(a, b, (av[2] - av[0]) * ks, (av[3] - av[1]) * ks, layer=L_DIM, lw=0.3)
    for rid, rm in rooms.items():
        r = rm["rect"]
        q = [KP(r[0], r[1]), KP(r[2], r[1]), KP(r[2], r[3]), KP(r[0], r[3])]
        sh.poly(q, fill="#BBBBBB", layer=L_TAG, lw=0.4)
        cx, cy = KP((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)
        sh.text(cx, cy - 0.03, rid[-1], size=5.0, bold=True, align="center", layer=L_TAG)
    for zid in ("exit_n", "exit_e"):
        z = next(z_ for z_ in plan["level_1"]["zones"] if z_["id"] == zid)["rect"]
        q = [KP(z[0], z[1]), KP(z[2], z[1]), KP(z[2], z[3]), KP(z[0], z[3])]
        sh.poly(q, fill="#E8F2EA", layer=L_TAG, lw=0.3)
    a, b = KP(127.85, 258)
    sh.text(a, b + 0.03, "X5", size=4.6, bold=True, align="center", layer=L_TAG)
    a, b = KP(214, 177)
    sh.text(a, b, "X7", size=4.6, bold=True, layer=L_TAG)
    sh.text(kx, ky + by1 * ks + 0.14, "KEY PLAN — L1 (A-101 G) · 1\" = 150'", size=5.4, bold=True)
    sh.text(kx, ky - 0.13, "grey = rooms 1-4 · green = EXIT (N) / (E) passages", size=4.6, color=GRY)
    # ---------------- schedule (per room)
    cs = g2.Col(sh, 7.45, 4.25, 4.05, 1.0)
    cs.head("FIXTURES + FURNITURE PER ROOM (ASSUMED; ADA 2010 minimums)", size=6.6)
    r1, r3 = rooms["evl_1"], rooms["evl_3"]
    rows = [(("Water closets", f"{r1['cnt']['wc_acc'] + r1['cnt']['wc_amb']}", f"{r3['cnt']['wc_acc'] + r3['cnt']['wc_amb']}", "1 wheelchair 60x60 (604.8.1) + 1 ambulatory 36x60 (604.8.2)"), None),
            (("Lavatories", f"{r1['cnt']['lav']}", f"{r3['cnt']['lav']}", f"{r1['cnt']['lav_acc']} accessible: 30x48 forward, rim ≤ 34 in (606)"), None),
            (("Showers", f"{r1['cnt']['sh_roll'] + r1['cnt']['sh']}", f"{r3['cnt']['sh_roll'] + r3['cnt']['sh']}", "1 roll-in 30x60 + 30x60 clear (608.2.2) + 3 at 36x36"), None),
            (("Lockers 15 in", f"{r1['lockers']}", f"{r3['lockers']}", f"{r1['lockers_acc']} accessible ≥ 5 % = {r1['lockers_req']} / {r3['lockers_req']} (225.2.1, 811)"), None),
            (("Benches", f"{r1['cnt']['bench']} + 1", f"{r3['cnt']['bench']} + 1", "team benches + 1 accessible 24x48, wall-affixed (903)"), None),
            (("Room door", "36 in", "36 in", "34 in clear (404.2.3), swings in (IBC 1010.1.2.1, < 50)"), None),
            (("Occupant load", f"{r1['occ']}", f"{r3['occ']}", "900 SF / 50 gross (T1004.5) ≤ 49: one door OK"), None)]
    cs.table([("ITEM", 0, "left"), ("RM 1-2", 1.15, "right"), ("RM 3-4", 1.65, "right"), ("BASIS", 1.75, "left", 2.4)], rows, size=5.0, rh=0.112)
    # ---------------- right panel
    sh.line(11.72, top - 0.02, 11.72, body_bottom + 0.1, lw=0.4)
    cr = g2.Col(sh, 11.85, top + 0.12, 4.65, 1.0)
    cr.para(em["disclaimer"], size=5.3, color=GRY)
    cr.head("COMMON PATH — VERIFIED ON THIS LAYOUT (T1006.2.1)", size=7.0)
    cp = en["rules"]["common_path"]
    cr.para(f"{cp['text'][0].upper() + cp['text'][1:]} — {cp['source'].split(' (')[0]}. Measured {cp['measure']}.", size=5.3)
    cr.table([("ROOM", 0, "left"), ("OCC.", 0.62, "right"), ("WORST POINT", 0.72, "left", 1.55), ("CP ft", 2.75, "right"), ("RESULT", 2.85, "left"),
              ("+ TO EXIT", 4.6, "right")],
             [((f"{r_['id'][-1]}", f"{r_['occ']}", r_["worst"]["label"], f"{r_['worst']['length']:.1f}", f"≤ {c['lim']} PASS" if r_["ok"] else "FAIL",
                f"{r_['b']['exit']} {r_['travel']:.0f} ft"), dict(colors={4: GRN if r_["ok"] else RED})) for r_ in c["rooms"]],
             size=5.2, rh=0.115)
    cr.para(f"Other points checked per room: {', '.join(q['label'] for q in rooms['evl_1']['routes'][1:])} (rooms 1-2); all shorter. "
            f"Travel to the exit door (CP + passage) ≤ {max(r_['travel'] for r_ in c['rooms']):.0f} ft vs 250 ft (T1017.2). Rectilinear on this "
            "layout; walls, door hardware and fixtures ASSUMED → UNVERIFIED until the architect's layout.", size=5.3)
    cr.head("ACCESSIBILITY (ADA 2010 STANDARDS) — WHAT IS DRAWN", size=7.0)
    ru = en["rules"]
    for k in ("toilets", "showers", "benches", "lockers", "door", "accessible_route"):
        cr.para(ru[k]["text"], size=5.2, bullet="·")
    cr.para("Locker room itself: turning space 304 inside (803.2); door swing leaves 30 x 48 clear beyond the arc (803.3). "
            "Scoping: 5 % / min. 1 of each locker-room type (222.1) — all 4 rooms laid out the same way.", size=5.2, bullet="·")
    cr.head("NOTES", size=7.0)
    cr.para(f"Rooms: {c['total']:,.0f} SF total (4 x 900, D-060 settled), envelopes from P2-A-101 Rev G, unchanged. {en['basis']['headroom'][0].upper() + en['basis']['headroom'][1:]}.", size=5.3, bullet="·")
    cr.para("Wet zone on the inner wall (rooms 1-2) / inner end (rooms 3-4), away from the exterior wall; plumbing walls back onto equipment / "
            "mech rooms (ASSUMED). No urinals: rooms serve either team (ASSUMED). Floor drains, finishes, ventilation: architect / MEP.", size=5.3, bullet="·")
    cr.para("Rooms 2 and 4 are mirror images of rooms 1 and 3 (doors face the shared exit passages).", size=5.3, bullet="·")
    cr.head("RESTROOM CORE — NOT IN THIS REVISION", size=7.0)
    cr.para(f"{en['basis']['restroom_core']}. Drawn later on P2-A-401 once Shane decides.", size=5.3, color=RED)
    cr.para("Legend: A = accessible element · dashed box = ADA clear floor / clearance · dashed circle = 60 in turning space · "
            "X box = shower / accessible bench · red dashed = worst common path (dot = remote point).", size=5.0, color=GRY)
    cr.para("Sources: params/phase2_enlarged.yaml; params/phase2_plan_rev_g.yaml; ADA 2010 Standards 213.3.1, 213.3.6, 222.1, 225.2.1, 304.3, "
            "305.3, 308.2.1, 403.5.1, 404.2.3, 404.2.4.1, 604, 606, 608, 803, 811, 903 (www.ada.gov, retrieved 2026-10-04); IBC 2021 1006.2.1, "
            "1010.1.1, 1010.1.2.1, T1004.5, T1017.2 (UpCodes); D-060, D-061, D-064; Shane 2026-10-04 11:24 AM CT.", size=5.0, color=GRY)
    return sh, body_bottom, [cs, cr]


def ft_in(v):
    f = int(v)
    i = round((v - f) * 12)
    if i == 12:
        f, i = f + 1, 0
    return f"{f}'-{i}\""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", choices=["A"], default="A")
    ap.add_argument("--png")
    ap.add_argument("--out-dir")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--print", action="store_true", help="print the numbers and exit")
    a = ap.parse_args()
    c = compute()
    if a.print:
        print("total", c["total"])
        for r in c["rooms"]:
            print(r["id"], round(r["area"], 1), r["occ"], {q["label"]: round(q["length"], 1) for q in r["routes"]}, "door", r["door_g"],
                  "onward", round(r["onward"], 1), "travel", round(r["travel"], 1), "lockers", r["lockers"], r["lockers_acc"], r["lockers_req"], r["cnt"])
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
