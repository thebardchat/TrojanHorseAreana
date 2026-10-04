"""KEYSTONE P2-A-901 3D MASSING MODEL — VIEWS (Phase 2, BACKLOG P2-T-011). Tabloid, NOT TO SCALE.

Rev A (2026-10-04, Shane 12:10 PM CT): massing only, from current params (plan Rev G L1 / Rev F L2, A-201 Rev G heights + portal +
brand + walk, C-101 Rev C site diagram, A-301 / A-302 tier basis). Axonometric views drawn as vector polygons (box model, painter's
order from pairwise box separation), plus a cutaway at L2 FF. Writes a deterministic OBJ + MTL massing model to phase2/out/3d/.
Nothing modelled that implies a choice on D-054 / D-064 / D-065 / D-066.
Data: params/phase2_massing.yaml (+ the files listed under its `inputs`).
Usage (from the repo root):
  /workspace/.venv-keystone/bin/python blueprints/phase2/src/p2_a_901.py [--rev A] [--png PATH] [--out-dir DIR] [--force] [--print]
"""
from __future__ import annotations

import argparse
import heapq
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
SHEET_NO = "P2-A-901"
RED, GRY = "#CC0000", "#555555"
L_MASS, L_GRND, L_TAG, L_VIEW = "A-MASS", "C-SITE-DIAG", "A-ANNO-TEXT", "A-ANNO-VIEW"
FACES = ("top", "B", "S", "N", "W", "E")
NORM = {"top": (0, 0, 1), "B": (0, 0, -1), "S": (0, -1, 0), "N": (0, 1, 0), "W": (-1, 0, 0), "E": (1, 0, 0)}


def rd(n):
    return yaml.safe_load((BP / "params" / n).read_text(encoding="utf-8"))


def hex2rgb(h):
    return tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))


def rgb2hex(c):
    return "#" + "".join(f"{max(0, min(255, int(round(v * 255)))):02X}" for v in c)


def shade(h, f):
    return rgb2hex(tuple(v * f for v in hex2rgb(h)))


# ---------------------------------------------------------------- model
class Box:
    def __init__(self, name, lo, hi, color, face_colors=None, decals=None, group=None, custom=None):
        self.name, self.lo, self.hi, self.color = name, tuple(lo), tuple(hi), color
        self.custom = custom or {}            # face -> polygon (3D) drawn instead of the rectangle; None = skip the face
        self.face_colors = face_colors or {}
        self.decals = decals or []          # (face, [(x, y, z), ...], fill) or (face, "line", [(x,y,z),(x,y,z)], color, lw)
        self.group = group or name

    def face_pts(self, f):
        (x0, y0, z0), (x1, y1, z1) = self.lo, self.hi
        return {"top": [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)],
                "B": [(x0, y0, z0), (x0, y1, z0), (x1, y1, z0), (x1, y0, z0)],
                "S": [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)],
                "N": [(x1, y1, z0), (x0, y1, z0), (x0, y1, z1), (x1, y1, z1)],
                "W": [(x0, y1, z0), (x0, y0, z0), (x0, y0, z1), (x0, y1, z1)],
                "E": [(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)]}[f]

    def face_area(self, f):
        d = [self.hi[i] - self.lo[i] for i in range(3)]
        return {"top": d[0] * d[1], "B": d[0] * d[1], "S": d[0] * d[2], "N": d[0] * d[2], "W": d[1] * d[2], "E": d[1] * d[2]}[f]


def build_model(mode):
    ms, plan = rd("phase2_massing.yaml"), rd("phase2_plan_rev_g.yaml")
    ev, eb, site, sect = rd("phase2_elev_rev_g.yaml"), rd("phase2_elev.yaml"), rd("phase2_site.yaml"), rd("phase2_sect.yaml")
    fin = {f["id"]: f["hex"] for f in eb["finishes"]}
    col = {k: (fin[v["finish"]] if "finish" in v else v["hex"]) for k, v in ms["colors"].items() if isinstance(v, dict) and ("finish" in v or "hex" in v)}
    md = ms["model"]
    l2 = ev["heights_override"]["l2_ff"]["value"]
    ring = ev["heights_override"]["ring_roof"]["value"]
    aroof = eb["heights"]["arena_roof_top"]["value"]
    bx = plan["building"]["rect"]
    tw = plan["building"]["projection"]["rect"]
    av = ev["arena_volume_override"]["rect"]
    boxes, ground, glines, labels = [], [], [], {}
    dh, dw = md["door_height_ft"], md["door_width_ft"]

    # doors as decals on the building faces (exterior)
    def door_decals():
        out = []
        for d in plan["level_1"]["doors"]["items"]:
            if "bank" in d:
                b = d["bank"]
                out.append(("S", [(b["x0"], bx[1], 0), (b["x1"], bx[1], 0), (b["x1"], bx[1], dh), (b["x0"], bx[1], dh)], col["glazing"]))
                continue
            a, w = d["at"], d["wall"]
            if w == "S":
                out.append(("S", [(a - dw / 2, bx[1], 0), (a + dw / 2, bx[1], 0), (a + dw / 2, bx[1], dh), (a - dw / 2, bx[1], dh)], col["door"]))
            elif w == "N":
                yy = tw[3] if tw[0] <= a <= tw[2] else bx[3]
                out.append(("N", [(a + dw / 2, yy, 0), (a - dw / 2, yy, 0), (a - dw / 2, yy, dh), (a + dw / 2, yy, dh)], col["door"]))
            elif w == "W":
                out.append(("W", [(bx[0], a + dw / 2, 0), (bx[0], a - dw / 2, 0), (bx[0], a - dw / 2, dh), (bx[0], a + dw / 2, dh)], col["door"]))
            else:
                out.append(("E", [(bx[2], a - dw / 2, 0), (bx[2], a + dw / 2, 0), (bx[2], a + dw / 2, dh), (bx[2], a - dw / 2, dh)], col["door"]))
        return out

    # portal (freestanding), from C-101 Rev C + A-201 Rev G
    pt, po = site["portal"], ev["portal_override"]
    cx, pw, pdp, gap = pt["center_x"], pt["width"], pt["depth"], pt["gap_to_building"]
    op = eb["portal"]["opening_width"]
    py0, py1 = bx[1] - gap - pdp, bx[1] - gap
    ph = po["overall_height"]
    xa, xb = cx - pw / 2, cx + pw / 2
    oa, ob = cx - op / 2, cx + op / 2
    boxes.append(Box("portal_pier_w", (xa, py0, 0), (oa, py1, ph), col["portal"], group="portal"))
    boxes.append(Box("portal_pier_e", (ob, py0, 0), (xb, py1, ph), col["portal"], group="portal"))
    n = md["spandrel_slices"] * 4
    half, rise, spr = op / 2, po["arch_rise"], po["springline"]
    arc = [(oa + i * op / n, spr + rise * math.sqrt(max(0.0, 1 - ((oa + i * op / n - cx) / half) ** 2))) for i in range(n + 1)]
    bd_ = dict(c=(cx, py0, ev["mark"]["center_z"]), r=ev["mark"]["diameter"] / 2)
    badge_pts = [(bd_["c"][0] + bd_["r"] * math.cos(2 * math.pi * k / 48), py0, bd_["c"][2] + bd_["r"] * math.sin(2 * math.pi * k / 48)) for k in range(48)]
    face_s = [(x, py0, z) for x, z in arc] + [(ob, py0, ph), (oa, py0, ph)]
    face_n = [(x, py1, z) for x, z in reversed(arc)] + [(oa, py1, ph), (ob, py1, ph)]
    dec = [("S", "poly", [(x, py0, z) for x, z in arc], col["trim"], 1.3), ("N", "poly", [(x, py1, z) for x, z in arc], col["trim"], 1.3),
           ("S", badge_pts, ev["mark"]["fill"])]
    boxes.append(Box("portal_spandrel", (oa, py0, spr), (ob, py1, ph), col["portal"], face_colors={"B": col["soffit"]}, decals=dec, group="portal",
                     custom={"S": face_s, "N": face_n, "W": None, "E": None, "B": None}))
    # walk (ground)
    cw = site["champion_walk"]["rect"]
    ground.append(([(cw[0], cw[1], 0), (cw[2], cw[1], 0), (cw[2], cw[3], 0), (cw[0], cw[3], 0)], ev["champion_walk"]["brick_hex"], "walk"))
    labels["walk"] = ((cw[0] + cw[2]) / 2, (cw[1] + cw[3]) / 2, 0)
    labels["portal"] = (cx, py0, ph)
    labels["badge"] = (cx, py0, ev["mark"]["center_z"])
    # site diagram lines
    bd = site["bus_drop"]
    k = 48
    loop = [(bd["loop_center"][0] + bd["loop_rx"] * math.cos(2 * math.pi * i / k), bd["loop_center"][1] + bd["loop_ry"] * math.sin(2 * math.pi * i / k), 0) for i in range(k + 1)]
    glines.append(("bus", loop, True))
    glines.append(("road", [(-30, site["road"]["y"], 0), (bx[2] + 40, site["road"]["y"], 0)], False))
    glines.append(("walk_ext", [(cw[0], py0, 0), (cw[0], site["road"]["y"] + 14, 0)], True))
    glines.append(("walk_ext", [(cw[2], py0, 0), (cw[2], site["road"]["y"] + 14, 0)], True))
    sa = site["service"]["apron"]
    glines.append(("apron", [(sa[0], sa[1], 0), (sa[2], sa[1], 0), (sa[2], sa[3], 0), (sa[0], sa[3], 0), (sa[0], sa[1], 0)], True))
    labels["bus"] = (bd["loop_center"][0], bd["loop_center"][1], 0)
    labels["road"] = (bx[2] - 20, site["road"]["y"], 0)
    labels["apron"] = ((sa[0] + sa[2]) / 2, sa[3], 0)

    if mode in ("exterior", "portal"):
        sp = ev["side_panel"]
        r = sp["rect"]
        dec = door_decals() + [("S", [(r[0], bx[1], r[1]), (r[2], bx[1], r[1]), (r[2], bx[1], r[3]), (r[0], bx[1], r[3])], sp["panel"]),
                               ("S", [(r[0], bx[1], r[1]), (r[2], bx[1], r[1]), (r[2], bx[1], r[1] + 0.8), (r[0], bx[1], r[1] + 0.8)], sp["stripe"])]
        boxes.append(Box("building_ring", (bx[0], bx[1], 0), (bx[2], bx[3], ring), col["wall"], decals=dec))
        tdec = [d for d in door_decals() if d[0] == "N" and abs(d[1][0][1] - tw[3]) < 1e-6]
        boxes.append(Box("ne_stair_tower", (tw[0], tw[1], 0), (tw[2], tw[3], ring), col["wall"], decals=tdec))
        boxes.append(Box("arena_volume", (av[0], av[1], ring), (av[2], av[3], aroof), col["arena"]))
        labels.update(arena=((av[0] + av[2]) / 2, (av[1] + av[3]) / 2, aroof), ring=(bx[0], bx[1], ring), tower=((tw[0] + tw[2]) / 2, tw[3], ring),
                      e1=(cx, bx[1], dh), s1=(next(d["at"] for d in plan["level_1"]["doors"]["items"] if d["id"] == "S1"), bx[3], dh),
                      panel=((r[0] + r[2]) / 2, bx[1], r[3]))
    else:
        # cutaway: L1 ring solid to L2 FF, minus the arena (tiers drawn) and the lobby open-to-below
        cut = md["cut_z_ft"]
        hole = plan["level_2"]["loop"]["inner"]
        lob = next(o for o in plan["level_2"]["open_below"] if o["id"] == "ob_lobby")["rect"]
        pieces = [(bx[0], bx[1], hole[0], bx[3]), (hole[0], hole[3], bx[2], bx[3]), (hole[2], bx[1], bx[2], hole[3]),
                  (hole[0], bx[1], lob[0], hole[1]), (lob[2], bx[1], hole[2], hole[1]), (lob[0], lob[3], lob[2], hole[1])]
        for i, p in enumerate(pieces):
            boxes.append(Box(f"ring_cut_{i}", (p[0], p[1], 0), (p[2], p[3], cut), col["slab"]))
        boxes.append(Box("ne_stair_tower_cut", (tw[0], tw[1], 0), (tw[2], tw[3], cut), col["slab"]))
        ground.append(([(lob[0], lob[1], 0), (lob[2], lob[1], 0), (lob[2], lob[3], 0), (lob[0], lob[3], 0)], "#EFEFEF", "lobby"))
        fl = plan["event_floor"]["rect"]
        arena = next(o for o in plan["level_2"]["open_below"] if o["id"] == "ob_arena")["rect"]
        ground.append(([(arena[0], arena[1], 0), (arena[2], arena[1], 0), (arena[2], arena[3], 0), (arena[0], arena[3], 0)], col["floor"], "arena_floor"))
        mft = rd("phase2.yaml")["spaces"]["arena"]["mat_ft"]
        for m in plan["mats"]:
            x0, y0 = m["origin"]
            ground.append(([(x0, y0, 0), (x0 + mft, y0, 0), (x0 + mft, y0 + mft, 0), (x0, y0 + mft, 0)], col["mat"], "mat"))
        tl, tu = plan["tiers"]["lower"], plan["tiers"]["upper"]
        rise = sect["seating"]["lower"]["rise_in"] / 12
        rd_ = tl["row_depth_ft"]
        ops = tl["openings"]
        for b in tl["bands"]:
            r, s = b["rect"], b["side"]
            for kk in range(2, tl["rows"] + 1):
                z = (kk - 1) * rise
                if s == "N":
                    rr = [r[0], r[1] + (kk - 1) * rd_, r[2], r[1] + kk * rd_]
                elif s == "S":
                    rr = [r[0], r[3] - kk * rd_, r[2], r[3] - (kk - 1) * rd_]
                else:
                    rr = [r[0] + (kk - 1) * rd_, r[1], r[0] + kk * rd_, r[3]]
                segs = [rr]
                for o in ops:
                    if o["side"] != s:
                        continue
                    orr = o["rect"]
                    new = []
                    for q in segs:
                        if s in ("N", "S"):
                            if orr[0] < q[2] and orr[2] > q[0]:
                                new += [x for x in ([q[0], q[1], orr[0], q[3]], [orr[2], q[1], q[2], q[3]]) if x[2] - x[0] > 1e-6]
                            else:
                                new.append(q)
                        else:
                            if orr[1] < q[3] and orr[3] > q[1]:
                                new += [x for x in ([q[0], q[1], q[2], orr[1]], [q[0], orr[3], q[2], q[3]]) if x[3] - x[1] > 1e-6]
                            else:
                                new.append(q)
                    segs = new
                for j, q in enumerate(segs):
                    boxes.append(Box(f"lower_{s}_{kk}_{j}", (q[0], q[1], 0), (q[2], q[3], z), col["tier_lower"], group=f"lower_{s}"))
        rz = tu["riser_in"] / 12
        rdu = tu["row_depth_in"] / 12
        for b in tu["bands"]:
            r, s = b["rect"], b["side"]
            for kk in range(1, tu["rows"] + 1):
                z = tu["front_row_ft"] + (kk - 1) * rz
                if s == "N":
                    rr = [r[0], r[1] + (kk - 1) * rdu, r[2], r[1] + kk * rdu]
                elif s == "S":
                    rr = [r[0], r[3] - kk * rdu, r[2], r[3] - (kk - 1) * rdu]
                else:
                    rr = [r[0] + (kk - 1) * rdu, r[1], r[0] + kk * rdu, r[3]]
                boxes.append(Box(f"upper_{s}_{kk}", (rr[0], rr[1], 0), (rr[2], rr[3], z), col["tier_upper"], group=f"upper_{s}"))
        labels.update(floor=((fl[0] + fl[2]) / 2, (fl[1] + fl[3]) / 2, 0), upper_n=((56 + 188) / 2, 239, l2), lower_s=(140, 62, 0),
                      loop=(hole[0] - 3.5, (hole[1] + hole[3]) / 2, cut), lobby=((lob[0] + lob[2]) / 2, lob[1] + 4, 0))
    return dict(boxes=boxes, ground=ground, glines=glines, labels=labels, col=col, ms=ms,
                h=dict(l2=l2, ring=ring, aroof=aroof, portal=ph, crown=po["crown"], spr=spr, badge=ev["mark"]["diameter"]),
                walk=cw, bx=bx, tw=tw, av=av, portal=(xa, py0, xb, py1))


# ---------------------------------------------------------------- projection + ordering
class Cam:
    def __init__(self, az, el):
        a, e = math.radians(az), math.radians(el)
        self.c = (math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e))
        self.r = (-math.sin(a), math.cos(a), 0.0)
        c, r = self.c, self.r
        self.u = (c[1] * r[2] - c[2] * r[1], c[2] * r[0] - c[0] * r[2], c[0] * r[1] - c[1] * r[0])

    def p(self, q):
        return (q[0] * self.r[0] + q[1] * self.r[1] + q[2] * self.r[2], q[0] * self.u[0] + q[1] * self.u[1] + q[2] * self.u[2])

    def depth(self, q):
        return -(q[0] * self.c[0] + q[1] * self.c[1] + q[2] * self.c[2])


def corners(lo, hi):
    return [(x, y, z) for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])]


def sbox(cam, lo, hi):
    ps = [cam.p(q) for q in corners(lo, hi)]
    return min(p[0] for p in ps), min(p[1] for p in ps), max(p[0] for p in ps), max(p[1] for p in ps)


def hull(pts):
    pts = sorted(set(pts))
    if len(pts) < 3:
        return pts

    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def poly_overlap(A, B):
    for P in (A, B):
        n = len(P)
        for i in range(n):
            ex, ey = P[(i + 1) % n][0] - P[i][0], P[(i + 1) % n][1] - P[i][1]
            nx, ny = -ey, ex
            a = [q[0] * nx + q[1] * ny for q in A]
            b = [q[0] * nx + q[1] * ny for q in B]
            if max(a) <= min(b) + 1e-9 or max(b) <= min(a) + 1e-9:
                return False
    return True


def before(cam, A, B):
    """True if A must be drawn before B (A behind B); None if undetermined."""
    v = tuple(-x for x in cam.c)
    verdicts = []
    for i in range(3):
        if A[1][i] <= B[0][i] + 1e-9:          # A at lower coordinate on axis i
            gap = B[0][i] - A[1][i]
            if abs(v[i]) > 1e-9:
                verdicts.append((gap * abs(v[i]) + abs(v[i]), v[i] < 0))
        elif B[1][i] <= A[0][i] + 1e-9:
            gap = A[0][i] - B[1][i]
            if abs(v[i]) > 1e-9:
                verdicts.append((gap * abs(v[i]) + abs(v[i]), v[i] > 0))
    if not verdicts:
        return None
    if all(x[1] == verdicts[0][1] for x in verdicts):
        return verdicts[0][1]
    return max(verdicts)[1]


def order(cam, items):
    """items: list of (key, lo, hi). Returns indices in painter's order (far first)."""
    n = len(items)
    hulls = [hull([cam.p(q) for q in corners(it[1], it[2])]) for it in items]
    sb = [sbox(cam, it[1], it[2]) for it in items]
    cen = [cam.depth(tuple((it[1][k] + it[2][k]) / 2 for k in range(3))) for it in items]
    succ = [[] for _ in range(n)]
    indeg = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            a, b = sb[i], sb[j]
            if a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1]:
                continue
            if not poly_overlap(hulls[i], hulls[j]):
                continue
            r = before(cam, (items[i][1], items[i][2]), (items[j][1], items[j][2]))
            if r is None:
                r = cen[i] > cen[j]
            if r:
                succ[i].append(j)
                indeg[j] += 1
            else:
                succ[j].append(i)
                indeg[i] += 1
    heap = [(-cen[i], items[i][0], i) for i in range(n) if indeg[i] == 0]
    heapq.heapify(heap)
    out, done = [], [False] * n
    while len(out) < n:
        if not heap:                              # cycle: break at the farthest remaining
            i = max((k for k in range(n) if not done[k]), key=lambda k: (cen[k], items[k][0]))
            indeg[i] = 0
            heap.append((-cen[i], items[i][0], i))
            heapq.heapify(heap)
        _, _, i = heapq.heappop(heap)
        if done[i]:
            continue
        done[i] = True
        out.append(i)
        for j in succ[i]:
            indeg[j] -= 1
            if indeg[j] == 0 and not done[j]:
                heapq.heappush(heap, (-cen[j], items[j][0], j))
    return out


# ---------------------------------------------------------------- draw a view
def draw_view(sh, v, mdl, crop=None):
    cam = Cam(v["az"], v["el"])
    x0, y0, x1, y1 = v["box"]
    boxes = mdl["boxes"]
    if crop:
        lo, hi = crop[:3], crop[3:]
        cl = []
        for b in boxes:
            if not all(b.lo[k] < hi[k] and b.hi[k] > lo[k] for k in range(3)):
                continue
            nlo = tuple(max(b.lo[k], lo[k]) for k in range(3))
            nhi = tuple(min(b.hi[k], hi[k]) for k in range(3))
            dec = []
            for d in b.decals:
                if d[1] == "poly":
                    dec.append(d)
                    continue
                q = [tuple(min(max(c[k], lo[k]), hi[k]) for k in range(3)) for c in d[1]]
                if len({(c[0], c[1], c[2]) for c in q}) >= 3:
                    dec.append((d[0], q, d[2]))
            cl.append(Box(b.name, nlo, nhi, b.color, b.face_colors, dec, b.group, b.custom))
        boxes = cl
    ground = [g for g in mdl["ground"] if not crop or all(crop[0] <= q[0] <= crop[3] and crop[1] <= q[1] <= crop[4] for q in g[0])]
    glines = mdl["glines"] if v.get("site") else []
    pts = []
    for b in boxes:
        pts += [cam.p(q) for q in corners(b.lo, b.hi)]
    for g in ground:
        pts += [cam.p(q) for q in g[0]]
    for g in glines:
        pts += [cam.p(q) for q in g[1]]
    if crop:
        pts = [cam.p(q) for q in corners(crop[:3], crop[3:])]
    mnx, mny = min(p[0] for p in pts), min(p[1] for p in pts)
    mxx, mxy = max(p[0] for p in pts), max(p[1] for p in pts)
    bw, bh = x1 - x0, y1 - y0 - 0.3
    s = min(bw / (mxx - mnx), bh / (mxy - mny))
    ox = x0 + (bw - (mxx - mnx) * s) / 2 - mnx * s
    oy = y0 + (bh - (mxy - mny) * s) / 2 - mny * s

    def P(q):
        a, b = cam.p(q)
        return ox + a * s, oy + b * s

    shf = mdl["ms"]["colors"]["shade"]
    gl = mdl["col"]["ground_line"]
    for pts3, colr, _k in ground:
        sh.poly([P(q) for q in pts3], fill=colr, layer=L_GRND, lw=0.3)
    for name, pl, dashed in glines:
        for a, b in zip(pl[:-1], pl[1:]):
            pa, pb = P(a), P(b)
            if dashed:
                sh.dashed(pa[0], pa[1], pb[0], pb[1], layer=L_GRND, lw=0.35, dash=0.04, gap=0.03)
            else:
                sh.line(pa[0], pa[1], pb[0], pb[1], layer=L_GRND, lw=0.5)
    _ = gl
    items = [(b.name, b.lo, b.hi) for b in boxes]
    vis = [f for f in FACES if sum(NORM[f][k] * cam.c[k] for k in range(3)) > 1e-9]
    for i in order(cam, items):
        b = boxes[i]
        for f in vis:
            if f in b.custom and b.custom[f] is None:
                continue
            if b.face_area(f) <= 1e-9:
                continue
            c = b.face_colors.get(f, b.color)
            sh.poly([P(q) for q in b.custom.get(f, b.face_pts(f))], fill=shade(c, shf[f]), layer=L_MASS, lw=0.25)
        for d in b.decals:
            if d[0] not in vis:
                continue
            if d[1] == "poly":
                pp = [P(q) for q in d[2]]
                for pa, pb in zip(pp[:-1], pp[1:]):
                    sh.poly([pa, pb, pb, pa], fill=None, layer=L_MASS, lw=d[4], edge=d[3])
            else:
                sh.poly([P(q) for q in d[1]], fill=shade(d[2], shf[d[0]]), layer=L_MASS, lw=0.15)
    # north arrow
    ax_, ay_ = x1 - 0.25, y0 + 0.3
    n2 = cam.p((0, 1, 0))
    L = math.hypot(*n2) or 1
    dx, dy = n2[0] / L * 0.18, n2[1] / L * 0.18
    sh.line(ax_ - dx, ay_ - dy, ax_ + dx, ay_ + dy, layer=L_TAG, lw=0.8)
    sh.poly([(ax_ + dx, ay_ + dy), (ax_ + dx * 0.55 - dy * 0.3, ay_ + dy * 0.55 + dx * 0.3), (ax_ + dx * 0.55 + dy * 0.3, ay_ + dy * 0.55 - dx * 0.3)], fill="#000000", layer=L_TAG, lw=0.3)
    sh.text(ax_ + dx * 1.6, ay_ + dy * 1.6 - 0.03, "N", size=5.5, bold=True, align="center", layer=L_TAG)
    return P


def leader(sh, P, q, dx, dy, txt, size=4.6, color=None):
    a, b = P(q)
    sh.line(a, b, a + dx, b + dy, layer=L_TAG, lw=0.3)
    al = "left" if dx >= 0 else "right"
    sh.text(a + dx + (0.03 if dx >= 0 else -0.03), b + dy - 0.03, txt, size=size, align=al, layer=L_TAG, color=color)


# ---------------------------------------------------------------- OBJ
def write_obj(path, models):
    mats = {}
    lines = ["# KEYSTONE P2-A-901 Rev A massing model (feet; origin = SW building corner; x east, y north, z up). Massing only.",
             f"mtllib {path.stem}.mtl"]
    vi = 1
    extra = []
    for mname, mdl in models:
        for b in mdl["boxes"]:
            lines.append(f"o {mname}_{b.name}")
            cs = corners(b.lo, b.hi)
            for q in cs:
                lines.append("v %.3f %.3f %.3f" % (q[0], q[2], -q[1]))     # Y-up export
            idx = {q: vi + k for k, q in enumerate(cs)}
            for f in FACES:
                if b.face_area(f) <= 1e-9:
                    continue
                c = b.face_colors.get(f, b.color)
                mn = "m_" + c[1:]
                mats[mn] = c
                if f in b.custom:
                    if b.custom[f] is None:
                        continue
                    extra.append((mn, b.custom[f]))
                    continue
                lines.append(f"usemtl {mn}")
                lines.append("f " + " ".join(str(idx[q]) for q in b.face_pts(f)))
            vi += 8
            for mn, poly in extra:
                for q in poly:
                    lines.append("v %.3f %.3f %.3f" % (q[0], q[2], -q[1]))
                lines.append(f"usemtl {mn}")
                lines.append("f " + " ".join(str(vi + i) for i in range(len(poly))))
                vi += len(poly)
            extra.clear()
        for k, (pts3, c, kind) in enumerate(mdl["ground"]):
            lines.append(f"o {mname}_ground_{kind}_{k}")
            for q in pts3:
                lines.append("v %.3f %.3f %.3f" % (q[0], q[2], -q[1]))
            mn = "m_" + c[1:]
            mats[mn] = c
            lines.append(f"usemtl {mn}")
            lines.append("f " + " ".join(str(vi + i) for i in range(len(pts3))))
            vi += len(pts3)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    ml = ["# KEYSTONE P2-A-901 Rev A massing materials (drafting colours from params/phase2_massing.yaml)"]
    for mn in sorted(mats):
        r, g, b = hex2rgb(mats[mn])
        ml += [f"newmtl {mn}", "Kd %.4f %.4f %.4f" % (r, g, b), "illum 1", ""]
    path.with_suffix(".mtl").write_text("\n".join(ml), encoding="utf-8")


# ---------------------------------------------------------------- sheet
def build():
    ms = rd("phase2_massing.yaml")
    p2 = rd("phase2.yaml")
    meta2, mm = p2["meta"], ms["meta"]
    ext, cut, por = build_model("exterior"), build_model("cutaway"), build_model("portal")
    sh = Sheet(W, H)
    body_bottom = add_titleblock(sh, {
        "project": f"{meta2['project']}\n{meta2['arena_name']} · {meta2['location']}",
        "phase": "PHASE 2",
        "title": "3D MASSING MODEL\nVIEWS",
        "scale": mm["scale_text"],
        "date": meta2["sheet_date"],
        "revision": mm["revision"],
        "drawn_by": meta2["drawn_by"],
        "sheet_no": SHEET_NO,
        "stamp": meta2["stamp"],
    }, margin=M, tb_h=0.95, stamp_h=0.40)
    hh = ext["h"]
    for v in ms["views"]:
        mdl = {"exterior": ext, "cutaway": cut, "portal": por}[v["mode"]]
        P = draw_view(sh, v, mdl, crop=v.get("crop"))
        x0, y0, x1, y1 = v["box"]
        sh.text(x0, y1 + 0.02, f"{v['id']}  {v['title']}", size=6.8, bold=True, layer=L_VIEW)
        sh.text(x0, y1 - 0.1, "axonometric · not to scale" + (" · roofs removed, L1 ring cut solid at L2 FF" if v["mode"] == "cutaway" else ""), size=4.6, color=GRY, layer=L_VIEW)
        lb = mdl["labels"]
        if v["id"] == "V1":
            leader(sh, P, lb["arena"], 0.35, 0.25, f"ARENA VOLUME — roof {hh['aroof']:g}' ASSUMED (wall / roof TBD)")
            leader(sh, P, (150, 249, hh["ring"]), 0.3, 0.3, f"RING — roof {hh['ring']:g}' ASSUMED · L2 FF {hh['l2']:g}' DECIDED", size=4.4)
            leader(sh, P, lb["apron"], 0.05, 0.4, "service apron at S1 — diagram (D-034)", size=4.2, color=GRY)
            leader(sh, P, lb["portal"], -0.35, 0.2, f"FREESTANDING PORTAL {hh['portal']:g}' max (D-043, D-050)")
            leader(sh, P, lb["walk"], 0.75, -0.3, "CHAMPION WALK 28' x 30' brick, as drawn (D-046)")
            leader(sh, P, lb["bus"], 0.15, 0.3, "BUS DROP LOOP — diagram (D-034; C-101 Rev C)", size=4.2, color=GRY)
            leader(sh, P, lb["road"], -0.1, -0.2, "ROAD assumed south (site TBD, D-006)", size=4.2, color=GRY)
        elif v["id"] == "V2":
            leader(sh, P, lb["floor"], 0.9, 0.55, "EVENT FLOOR 120' x 144' + 4 x 42' mats (A-103 Rev A)", size=4.4)
            leader(sh, P, lb["upper_n"], 0.55, 0.3, "FIXED UPPER TIER — 5 rows, 21\" risers, front row 9.0' (D-061)", size=4.4)
            leader(sh, P, lb["lower_s"], 0.55, -0.35, "TELESCOPIC LOWER TIER — extended, 6 rows (D-009)", size=4.4)
            leader(sh, P, lb["loop"], -0.2, 0.75, f"L1 RING (rooms not modelled) CUT AT L2 FF {hh['l2']:g}'", size=4.4)
            leader(sh, P, lb["lobby"], -0.45, -0.3, "LOBBY — open to below (no checkpoint modelled, D-065)", size=4.4)
        elif v["id"] == "V3":
            leader(sh, P, lb["panel"], 0.15, 0.6, "side panel (A-201 Rev G)", size=4.2)
            leader(sh, P, lb["arena"], 0.1, 0.3, "arena volume flush with the east wall", size=4.2)
        elif v["id"] == "V4":
            leader(sh, P, lb["s1"], 0.3, -0.35, "S1 SERVICE / LOADING (D-034)", size=4.4)
            leader(sh, P, lb["tower"], 0.2, 0.3, "NE STAIR TOWER", size=4.2)
        elif v["id"] == "V5":
            leader(sh, P, lb["badge"], 0.45, 0.25, f"official mark Ø {hh['badge']:g}' (D-041, D-047)", size=4.4)
            leader(sh, P, lb["portal"], 0.35, 0.1, f"{hh['portal']:g}' max · crown {hh['crown']:g}' · springline {hh['spr']:g}' (D-050)", size=4.4)
            leader(sh, P, (126.5, -36, 24.5), 0.35, -0.12, "gold trim (D-045)", size=4.4)
            leader(sh, P, lb["walk"], -0.4, -0.35, "walk at the drawn 28' (D-066 OPEN)", size=4.4, color=RED)
            leader(sh, P, lb["e1"], 0.5, -0.45, "E1 door bank, 30' behind the portal (D-046)", size=4.4)
    # notes panel
    cr = g2.Col(sh, 12.6, 5.95, W - M - 0.08 - 12.6, 1.0)
    sh.line(12.48, 6.05, 12.48, body_bottom + 0.1, lw=0.4)
    cr.para(mm["disclaimer"], size=5.1, color=GRY)
    cr.head("HEIGHTS MODELLED", size=6.6)
    cr.para(f"L2 FF {hh['l2']:g}' DECIDED (D-061) · ring roof {hh['ring']:g}' ASSUMED · arena roof {hh['aroof']:g}' ASSUMED (P2-A-201 Rev G) · "
            f"portal {hh['portal']:g}' max, crown {hh['crown']:g}', springline {hh['spr']:g}' (D-050) · tiers per P2-A-301 Rev D / A-302 Rev C. Door symbols "
            f"{ms['model']['door_width_ft']:g}' x {ms['model']['door_height_ft']:g}' ASSUMED.", size=5.1)
    cr.head("OPEN — NOT MODELLED AS A CHOICE", size=6.6)
    for it in ms["open_items"]:
        cr.para(f"{it['id']}: {it['text']}.", size=5.0, bullet="·", color=RED)
    cr.head("NOTES", size=6.6)
    cr.para(ms["not_shown"], size=5.0, bullet="·")
    cr.para("Colours: limestone / crimson / gold / brick / brand red + black from P2-A-201 Rev G finishes (hex ASSUMED swatches); greys "
            "= material TBD. Arch drawn as a 56-segment polyline; the crimson underside faces down and does not show in views from above.", size=5.0, bullet="·")
    cr.para(f"Model file: phase2/out/3d/{mm['model_file']}.obj + .mtl (feet, Y-up export; exterior, cutaway and portal sets).", size=5.0, bullet="·")
    cr.para("Sources: params/phase2_massing.yaml; phase2_plan_rev_g.yaml; phase2_elev_rev_g.yaml; phase2_elev.yaml; phase2_site.yaml; "
            "phase2_sect.yaml; D-009, D-034, D-041, D-043, D-045, D-046, D-047, D-050, D-061; Shane 2026-10-04 12:10 PM CT.", size=4.7, color=GRY)
    return sh, body_bottom, [cr], [("exterior", ext), ("cutaway", cut)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", choices=["A"], default="A")
    ap.add_argument("--png")
    ap.add_argument("--out-dir")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--print", action="store_true")
    a = ap.parse_args()
    if a.print:
        for m in ("exterior", "cutaway", "portal"):
            mdl = build_model(m)
            print(m, len(mdl["boxes"]), "boxes", mdl["h"])
        return
    p2 = rd("phase2.yaml")
    rv = p2["sheets"][SHEET_NO]["revisions"][a.rev]
    ms = rd("phase2_massing.yaml")
    if a.out_dir:
        od = Path(a.out_dir)
        pdf, dxf, obj = od / f"{rv['file']}.pdf", od / f"{rv['file']}.dxf", od / f"{ms['meta']['model_file']}.obj"
    else:
        pdf = BP / "phase2" / "out" / "pdf" / f"{rv['file']}.pdf"
        dxf = BP / "phase2" / "out" / "dxf" / f"{rv['file']}.dxf"
        obj = BP / "phase2" / "out" / "3d" / f"{ms['meta']['model_file']}.obj"
        if rv.get("frozen") and (pdf.exists() or dxf.exists()) and not a.force:
            sys.exit("Revision is FROZEN; use --out-dir to regenerate for checking.")
    sh, body_bottom, cols, models = build()
    mg = [cl.y - body_bottom - 0.05 for cl in cols]
    print("column margins (in): " + ", ".join(f"{m:.2f}" for m in mg))
    if min(mg) < 0:
        raise SystemExit(f"LAYOUT OVERFLOW: {-min(mg):.2f} in into the stamp band")
    for f in (pdf, dxf, obj):
        f.parent.mkdir(parents=True, exist_ok=True)
    sh.render_pdf(pdf, title=f"{SHEET_NO} Rev {a.rev} {p2['sheets'][SHEET_NO]['title']}", png_path=a.png)
    sh.render_dxf(dxf)
    write_obj(obj, models)
    print(f"wrote {pdf}\nwrote {dxf}\nwrote {obj}" + (f"\nwrote {a.png}" if a.png else ""))


if __name__ == "__main__":
    main()
