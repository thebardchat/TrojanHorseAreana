"""KEYSTONE P2-A-401 ENLARGED PLANS — EVENT LOCKER ROOMS 1-4 (Phase 2, BACKLOG P2-T-010). Tabloid, 1/8" = 1'-0".

Rev A (2026-10-04, Shane 11:24 AM CT): the 4 event locker rooms only (900 SF each = 3,600 SF, D-060; under the upper tier at the tier
line, D-061). Doors placed so the common path is <= 75 ft (IBC 2021 Table 1006.2.1), measured and reported per room. Lockers,
benches, toilets and showers ASSUMED (KEYSTONE); accessible fixture sizes / clearances are ADA 2010 minimums (cited). The L1 public
restroom core waits on D-064 and is noted, not drawn.
Rev B (2026-10-04, Shane 1:21 / 1:22 PM CT, P2-T-012): locker rooms unchanged (Rev A approved, D-068); adds the L1 public restroom
core TEST-FIT for the chairs-only fixture count (D-064 DECIDED Option 2) at 1" = 20', required area vs drawn, D-069 options.
Data: params/phase2_enlarged.yaml, params/phase2_plan_rev_g.yaml (Rev A); + params/phase2_enlarged_rev_b.yaml, phase2_plan_rev_h.yaml (Rev B).
Usage (from the repo root):
  /workspace/.venv-keystone/bin/python blueprints/phase2/src/p2_a_401.py [--rev A|B] [--png PATH] [--out-dir DIR] [--force] [--print]
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


def compute(rev="A"):
    en, plan = rd("phase2_enlarged.yaml"), rd("phase2_plan_rev_g.yaml")
    rb = None
    if rev == "B":
        rb = rd("phase2_enlarged_rev_b.yaml")
        plan = rd(Path(rb["basis"]["plan"]).name)
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
    out = dict(en=en, plan=plan, rooms=rooms, total=total, lim=lim, rev=rev, rb=rb)
    if rev == "B":
        out["core"] = core_calc(rb, plan)
    return out


def core_calc(rb, plan):
    """Chairs-only restroom test-fit: counts, fit checks, net / gross area vs the drawn rooms on plan Rev H."""
    import p2_testfit as tf
    lp = tf.summary_j()[3]["loop"]
    fc, fd = lp["fx1c"], lp["fx1"]
    co = rb["core"]
    mods = co["modules"]
    rects = {r["id"]: r["rect"] for r in plan["level_1"]["rooms"]}
    res = {}
    for key, rm in co["rooms"].items():
        cnt = {k: 0 for k in mods}
        for row in rm["rows"]:
            run = row["x0"]
            for t, n in row["items"]:
                cnt[t] += n
                run += mods[t]["w"] * n
                dep = mods[t]["d"]
                if dep > row["y"][1] - row["y"][0] + 1e-6:
                    sys.exit(f"{key}: {t} {dep} ft deeper than its row")
            if run > rm["L"] + 1e-6:
                sys.exit(f"{key}: row {row['y']} runs {run} ft > room length {rm['L']}")
        lav = rm["lav"]
        if lav["y0"] + lav["n"] * mods["lav"]["w"] > rm["W"] + 1e-6:
            sys.exit(f"{key}: lavatory counter longer than the {rm['W']} ft wall")
        wc = cnt["wc_std"] + cnt["wc_amb"] + cnt["wc_acc"]
        ur = cnt["urinal"] + cnt["urinal_acc"]
        sx = "m" if key == "men" else "f"
        need_wc, need_lav = fc[f"wc_{sx}"], fc[f"lav_{sx}"]
        if wc + ur < need_wc or lav["n"] < need_lav or ur > fc["urinals_max"] or cnt["wc_acc"] < 1 or (wc + ur >= 6 and cnt["wc_amb"] < 1):
            sys.exit(f"{key}: test-fit {wc} WC + {ur} urinals / {lav['n']} lav does not meet {need_wc} / {need_lav} (urinals <= {fc['urinals_max']})")
        r = rects[rm["drawn_id"]]
        drawn = (r[2] - r[0]) * (r[3] - r[1])
        net = rm["L"] * rm["W"]
        gross = net * (1 + co["allowance"])
        res[key] = dict(cnt=cnt, wc=wc, ur=ur, lav=lav["n"], need_wc=need_wc, need_lav=need_lav, drawn=drawn, drawn_wh=(r[2] - r[0], r[3] - r[1]),
                        net=net, gross=gross, short=gross - drawn, drawn_wc=fd[f"wc_{sx}"], drawn_lav=fd[f"lav_{sx}"],
                        plan_sf=(need_wc + need_lav) * co["planning_factor_sf"])
    dfx = co["drinking_fountains"]
    res["df"] = dict(need=fc["df"], drawn=fd["df"], extra=dfx["extra"], sf=dfx["extra"] * dfx["sf_each"])
    if fc["df"] - fd["df"] != dfx["extra"]:
        sys.exit("drinking fountain count drifted from the params")
    res["short"] = res["men"]["short"] + res["women"]["short"] + res["df"]["sf"]
    res["plan_short"] = (fc["in_rooms"] - fd["in_rooms"]) * co["planning_factor_sf"]
    res["fc"], res["fd"] = fc, fd
    return res


def draw_core(sh, key, rm, mods, ox, oy, s):
    """One test-fit room (frame: x = length, y = width), 1 in = rb scale."""
    T = lambda x, y: (ox + x * s, oy + y * s)  # noqa: E731

    def ln(x1, y1, x2, y2, layer=L_PART, lw=0.4):
        a, b = T(x1, y1)
        c, d = T(x2, y2)
        sh.line(a, b, c, d, layer=layer, lw=lw)

    def bx(r, layer=L_PART, lw=0.4):
        for q in ((r[0], r[1], r[2], r[1]), (r[2], r[1], r[2], r[3]), (r[2], r[3], r[0], r[3]), (r[0], r[3], r[0], r[1])):
            ln(*q, layer=layer, lw=lw)

    def ell(cx, cy, ax, ay, layer=L_FIX, lw=0.3, dash=False):
        pts = [T(cx + ax * math.cos(2 * math.pi * k / 20), cy + ay * math.sin(2 * math.pi * k / 20)) for k in range(21)]
        for i, (a, b) in enumerate(zip(pts[:-1], pts[1:])):
            if dash and i % 2:
                continue
            sh.line(a[0], a[1], b[0], b[1], layer=layer, lw=lw)

    L_, W_ = rm["L"], rm["W"]
    e0, e1 = rm["entry"]
    ln(0, 0, e0, 0, L_WALL, 1.0)
    ln(e1, 0, L_, 0, L_WALL, 1.0)
    ln(L_, 0, L_, W_, L_WALL, 1.0)
    ln(L_, W_, 0, W_, L_WALL, 1.0)
    ln(0, W_, 0, 0, L_WALL, 1.0)
    # lavatory counter on the x = 0 wall
    lv = rm["lav"]
    lw_ = mods["lav"]["w"]
    y_end = lv["y0"] + lv["n"] * lw_
    bx((0, lv["y0"], mods["lav"]["d"], y_end), L_FIX, 0.35)
    for i in range(lv["n"]):
        ell(1.0, lv["y0"] + lw_ * (i + 0.5), 0.55, 0.75)
    a, b = T(0.5, lv["y0"] + lw_ * 0.5)
    sh.text(a + 0.06, b - 0.02, "A", size=3.4, bold=True, layer=L_TAG)
    # compartments / urinals
    for row in rm["rows"]:
        y0, y1 = row["y"]
        x = row["x0"]
        for t, n in row["items"]:
            md = mods[t]
            for _ in range(n):
                w, d = md["w"], md["d"]
                if row["face"] == "N":
                    ya, yb, back = y0, y0 + d, y0
                else:
                    ya, yb, back = y1 - d, y1, y1
                if t.startswith("urinal"):
                    ln(x, ya, x, yb)
                    ln(x + w, ya, x + w, yb)
                    ell(x + w / 2, back + (0.55 if row["face"] == "N" else -0.55), 0.6, 0.5)
                else:
                    bx((x, ya, x + w, yb))
                    ell(x + w / 2, back + (1.1 if row["face"] == "N" else -1.1), 0.75, 1.0)
                if md.get("label"):
                    a, b = T(x + w / 2, (ya + yb) / 2)
                    sh.text(a, b - 0.02, md["label"], size=3.2, bold=True, align="center", layer=L_TAG)
                x += w
    for bk in rm["blocks"]:
        r = bk["rect"]
        q = [T(r[0], r[1]), T(r[2], r[1]), T(r[2], r[3]), T(r[0], r[3])]
        sh.poly(q, fill="#D8D8D8" if bk["kind"] == "chase" else "#EEEEEE", layer=L_PART, lw=0.3)
        if bk["label"]:
            a, b = T((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)
            sh.text(a, b - 0.02, bk["label"], size=3.4, align="center", layer=L_TAG)
    ell(rm["turn"][0], rm["turn"][1], 2.5, 2.5, layer=L_CLR, lw=0.3, dash=True)
    a, b = T((e0 + e1) / 2, 0)
    sh.text(a, b - 0.09, "ENTRY", size=3.6, align="center", layer=L_TAG)
    # dimensions
    a, b = T(0, 0)
    c, d = T(L_, W_)
    yd = b - 0.17
    sh.line(a, yd, c, yd, layer=L_DIM, lw=0.3)
    for xx in (a, c):
        sh.line(xx, yd - 0.03, xx, yd + 0.03, layer=L_DIM, lw=0.3)
    sh.text((a + c) / 2, yd - 0.09, ft_in(L_), size=4.8, align="center", layer=L_DIM)
    xd = c + 0.1
    sh.line(xd, b, xd, d, layer=L_DIM, lw=0.3)
    for yy in (b, d):
        sh.line(xd - 0.03, yy, xd + 0.03, yy, layer=L_DIM, lw=0.3)
    sh.text(xd + 0.08, (b + d) / 2, ft_in(W_), size=4.8, align="center", layer=L_DIM, rot=90)


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
    rb = c["rb"]
    if rb:
        em = dict(em, revision=rb["meta"]["revision"])
    sh = Sheet(W, H)
    body_bottom = add_titleblock(sh, {
        "project": f"{meta2['project']}\n{meta2['arena_name']} · {meta2['location']}",
        "phase": "PHASE 2",
        "title": rb["meta"]["title_block"] if rb else "ENLARGED PLANS\nEVENT LOCKER ROOMS 1-4",
        "scale": "AS NOTED" if rb else em["scale_text"],
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
    if rb:
        return build_b(c, sh, body_bottom, top, rooms, en, em, rb, plan)
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


def build_b(c, sh, body_bottom, top, rooms, en, em, rb, plan):
    """Rev B: key plan on plan Rev H, restroom test-fit drawings, fixtures table + restroom core text in the right column."""
    co, cr_ = rb["core"], c["core"]
    # ---------------- key plan (Rev H)
    kx, ky, ks = 5.5, 2.3, 1.0 / 250
    bx0, by0, bx1, by1 = plan["building"]["rect"]
    pj = plan["building"]["projection"]["rect"]
    pts = [(bx0, by0), (bx1, by0), (bx1, pj[3]), (pj[0], pj[3]), (pj[0], by1), (bx0, by1), (bx0, by0)]
    KP = lambda x, y: (kx + x * ks, ky + y * ks)  # noqa: E731
    for (xa, ya), (xb, yb) in zip(pts[:-1], pts[1:]):
        a, b = KP(xa, ya)
        c2, d2 = KP(xb, yb)
        sh.line(a, b, c2, d2, layer=L_WALL, lw=0.9)
    an = plan["building"]["annex"]["rect"]
    sh.poly([KP(an[0], an[1]), KP(an[2], an[1]), KP(an[2], an[3]), KP(an[0], an[3])], fill="#F4F4F4", layer=L_WALL, lw=0.6)
    av = plan["arena_volume"]["rect"]
    a, b = KP(av[0], av[1])
    sh.rect(a, b, (av[2] - av[0]) * ks, (av[3] - av[1]) * ks, layer=L_DIM, lw=0.3)
    for rid, rm in rooms.items():
        r = rm["rect"]
        sh.poly([KP(r[0], r[1]), KP(r[2], r[1]), KP(r[2], r[3]), KP(r[0], r[3])], fill="#BBBBBB", layer=L_TAG, lw=0.3)
        cx, cy = KP((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)
        sh.text(cx, cy - 0.025, rid[-1], size=4.2, bold=True, align="center", layer=L_TAG)
    rr = {r_["id"]: r_["rect"] for r_ in plan["level_1"]["rooms"]}
    for rid, lab in (("rr_m1", "M"), ("rr_w1", "W")):
        r = rr[rid]
        sh.poly([KP(r[0], r[1]), KP(r[2], r[1]), KP(r[2], r[3]), KP(r[0], r[3])], fill="#BFD7EA", layer=L_TAG, lw=0.3)
        cx, cy = KP((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)
        sh.text(cx, cy - 0.025, lab, size=4.2, bold=True, align="center", layer=L_TAG)
    sh.text(kx, ky + plan["building"]["annex"]["rect"][3] * ks + 0.2, "KEY PLAN — L1 (A-101 H)", size=5.2, bold=True)
    sh.text(kx, ky + plan["building"]["annex"]["rect"][3] * ks + 0.09, "1\" = 250' · grey = rooms 1-4", size=4.4, color=GRY)
    sh.text(kx, ky - 0.12, "blue = drawn M / W (L1)", size=4.4, color=GRY)
    # ---------------- restroom test-fit drawings
    s2 = 1.0 / co["scale_ft_per_in"]
    for key, ox in (("women", 7.3), ("men", 9.75)):
        rm, r = co["rooms"][key], cr_[key]
        oy = 2.35
        draw_core(sh, key, rm, co["modules"], ox, oy, s2)
        sh.text(ox, oy + rm["W"] * s2 + 0.22, f"{rm['name']} — TEST-FIT", size=6.2, bold=True)
        u = f"{r['wc']} WC" + (f" + {r['ur']} urinals" if r["ur"] else "") + f" · {r['lav']} lav · {r['net']:,.0f} SF net"
        sh.text(ox, oy + rm["W"] * s2 + 0.1, u, size=4.6, color=GRY)
    sh.text(7.05, 1.95, f"Test-fit plans 1\" = {co['scale_ft_per_in']}'. Rooms NOT redrawn on A-101 Rev H (D-069 OPEN). "
            "A = accessible · AMB = ambulatory · dashed circle = 60 in turning space · grey = chase / janitor.", size=4.4, color=GRY)
    # ---------------- right panel
    sh.line(11.72, top - 0.02, 11.72, body_bottom + 0.1, lw=0.4)
    cr = g2.Col(sh, 11.85, top + 0.12, 4.65, 1.0)
    cr.para(em["disclaimer"], size=5.1, color=GRY)
    cr.head("COMMON PATH — VERIFIED ON THIS LAYOUT (T1006.2.1)", size=6.8)
    cp = en["rules"]["common_path"]
    cr.para(f"{cp['text'][0].upper() + cp['text'][1:]} — {cp['source'].split(' (')[0]}.", size=5.1)
    cr.table([("ROOM", 0, "left"), ("OCC.", 0.62, "right"), ("WORST POINT", 0.72, "left", 1.55), ("CP ft", 2.75, "right"), ("RESULT", 2.85, "left"),
              ("+ TO EXIT", 4.6, "right")],
             [((f"{r_['id'][-1]}", f"{r_['occ']}", r_["worst"]["label"], f"{r_['worst']['length']:.1f}", f"≤ {c['lim']} PASS" if r_["ok"] else "FAIL",
                f"{r_['b']['exit']} {r_['travel']:.0f} ft"), dict(colors={4: GRN if r_["ok"] else RED})) for r_ in c["rooms"]],
             size=5.0, rh=0.108)
    cr.para(f"Rooms 1-4 unchanged from Rev A (approved, D-068); envelopes identical on plan Rev H. Travel to the exit door ≤ "
            f"{max(r_['travel'] for r_ in c['rooms']):.0f} ft vs 250 ft (T1017.2).", size=5.1)
    cr.head("LOCKER ROOMS — FIXTURES (ASSUMED; ADA 2010)", size=6.8)
    r1, r3 = rooms["evl_1"], rooms["evl_3"]
    rows = [(("Water closets", f"{r1['cnt']['wc_acc'] + r1['cnt']['wc_amb']}", f"{r3['cnt']['wc_acc'] + r3['cnt']['wc_amb']}", "1 wheelchair 60x60 (604.8.1) + 1 ambulatory (604.8.2)"), None),
            (("Lavatories", f"{r1['cnt']['lav']}", f"{r3['cnt']['lav']}", f"{r1['cnt']['lav_acc']} accessible (606)"), None),
            (("Showers", f"{r1['cnt']['sh_roll'] + r1['cnt']['sh']}", f"{r3['cnt']['sh_roll'] + r3['cnt']['sh']}", "1 roll-in 30x60 (608.2.2) + 3 at 36x36"), None),
            (("Lockers 15 in", f"{r1['lockers']}", f"{r3['lockers']}", f"{r1['lockers_acc']} accessible ≥ 5 % (225.2.1, 811)"), None),
            (("Benches", f"{r1['cnt']['bench']} + 1", f"{r3['cnt']['bench']} + 1", "+ 1 accessible 24x48 (903)"), None),
            (("Occupant load", f"{r1['occ']}", f"{r3['occ']}", "900 SF / 50 gross (T1004.5): one door"), None)]
    cr.table([("ITEM", 0, "left"), ("RM 1-2", 1.1, "right"), ("RM 3-4", 1.6, "right"), ("BASIS", 1.7, "left", 2.9)], rows, size=4.9, rh=0.105)
    cr.para("Accessibility per Rev A: 604.8, 606, 608, 803, 811, 903; turning space 304 in each room. Wet zones on the inner walls (ASSUMED).", size=5.0, color=GRY)
    cr.head("L1 PUBLIC RESTROOMS — CHAIRS-ONLY (D-064 · D-069 OPEN)", size=6.8)
    fc, fd = cr_["fc"], cr_["fd"]
    m, w = cr_["men"], cr_["women"]
    cr.para(f"D-064 DECIDED Option 2 (Shane 1:22 PM CT): L1 load = chairs-only floor 2,346 + lower seats 1,100 = {fc['load']:,} "
            f"(IBC 2021 T2902.1, 50/50 split 2902.1.1). Drawn rooms (A-101 Rev H) hold the Rev I set ({fd['load']:,}).", size=5.1)
    cr.table([("FIXTURE", 0, "left"), ("REQUIRED", 1.75, "right"), ("DRAWN", 2.45, "right"), ("TEST-FIT", 3.35, "right"), ("SHORT", 4.6, "right")],
             [(("Men WC (urinals ≤ 67 %, IPC 424.2)", f"{fc['wc_m']}", f"{fd['wc_m']}", f"{m['wc']} + {m['ur']} ur", f"+{fc['wc_m'] - fd['wc_m']}"), dict(colors={4: RED})),
              (("Men lavatories", f"{fc['lav_m']}", f"{fd['lav_m']}", f"{m['lav']}", f"+{fc['lav_m'] - fd['lav_m']}"), dict(colors={4: RED})),
              (("Women WC", f"{fc['wc_f']}", f"{fd['wc_f']}", f"{w['wc']}", f"+{fc['wc_f'] - fd['wc_f']}"), dict(colors={4: RED})),
              (("Women lavatories", f"{fc['lav_f']}", f"{fd['lav_f']}", f"{w['lav']}", f"+{fc['lav_f'] - fd['lav_f']}"), dict(colors={4: RED})),
              (("Drinking fountains (hi-lo)", f"{fc['df']}", f"{fd['df']}", "concourse", f"+{cr_['df']['extra']}"), dict(colors={4: RED}))],
             size=5.0, rh=0.108)
    cr.table([("ROOM AREA (SF)", 0, "left"), ("DRAWN", 1.75, "right"), ("TEST-FIT NET", 2.75, "right"), (f"+{co['allowance'] * 100:.0f} %", 3.6, "right"),
              ("SHORT", 4.6, "right")],
             [(("Men (drawn 20 x 35)", f"{m['drawn']:,.0f}", f"{m['net']:,.0f}", f"{m['gross']:,.0f}", f"+{m['short']:,.0f}"), dict(colors={4: RED})),
              (("Women (drawn 23 x 50)", f"{w['drawn']:,.0f}", f"{w['net']:,.0f}", f"{w['gross']:,.0f}", f"+{w['short']:,.0f}"), dict(colors={4: RED})),
              (("2 more fountains (alcoves)", "", "", f"{cr_['df']['sf']:,.0f}", f"+{cr_['df']['sf']:,.0f}"), dict(colors={4: RED})),
              (("TOTAL — tight test-fit", "", "", "", f"+{cr_['short']:,.0f}"), dict(bold=True, colors={4: RED})),
              ((f"TOTAL — {co['planning_factor_sf']} SF / fixture (program)", "", "", "", f"+{cr_['plan_short']:,.0f}"), dict(colors={4: RED}))],
             size=5.0, rh=0.108)
    cr.para(f"FINDING D-069 (OPEN): the drawn L1 rooms are short by about +{cr_['short']:,.0f} SF on a tight test-fit "
            f"(stalls 36 x 60 in, 6 ft aisles, +10 % walls / chases, all ASSUMED) and about +{cr_['plan_short']:,.0f} SF on the program's "
            f"{co['planning_factor_sf']} SF per fixture. The architect's layout lands between. Not redrawn — Shane decides:", size=5.1, color=RED)
    for o in co["options"]:
        cr.para(o, size=5.0, bullet="·", color=RED)
    cr.para(co["interim"], size=5.0, color=RED)
    cr.para("Sources: params/phase2_enlarged.yaml, phase2_enlarged_rev_b.yaml, phase2_plan_rev_h.yaml; IBC 2021 T2902.1, 2902.1.1, 1006.2.1, "
            "T1004.5, T1017.2; IPC 2021 405.3.1, 405.3.5, 424.2 (UpCodes, retrieved 2026-10-04); ADA 2010 213.3, 304.3, 604.8, 605, 606, 608, "
            "811, 903 (www.ada.gov); D-060, D-061, D-064, D-068, D-069; Shane 2026-10-04 1:21 / 1:22 PM CT.", size=4.8, color=GRY)
    return sh, body_bottom, [cr]


def ft_in(v):
    f = int(v)
    i = round((v - f) * 12)
    if i == 12:
        f, i = f + 1, 0
    return f"{f}'-{i}\""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", choices=["A", "B"], default="B")
    ap.add_argument("--png")
    ap.add_argument("--out-dir")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--print", action="store_true", help="print the numbers and exit")
    a = ap.parse_args()
    c = compute(a.rev)
    if a.print:
        print("total", c["total"])
        for r in c["rooms"]:
            print(r["id"], round(r["area"], 1), r["occ"], {q["label"]: round(q["length"], 1) for q in r["routes"]}, "door", r["door_g"],
                  "onward", round(r["onward"], 1), "travel", round(r["travel"], 1), "lockers", r["lockers"], r["lockers_acc"], r["lockers_req"], r["cnt"])
        if a.rev == "B":
            for k in ("men", "women"):
                print(k, {kk: (round(v, 1) if isinstance(v, float) else v) for kk, v in c["core"][k].items()})
            print("df", c["core"]["df"], "short", round(c["core"]["short"], 1), "plan_short", c["core"]["plan_short"])
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
