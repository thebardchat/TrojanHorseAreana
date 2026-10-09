#!/usr/bin/env python3
"""
Trojan Horse Arena — CONCEPT STUDY interior cutaway (SRM-language shell, Rev D bowl).

Cut at the Level 2 floor, 17'-9" (D-061), roofs removed, like P2-A-901 Rev D view V2.
Bowl geometry is Set Rev D as drawn (params/phase2_plan_rev_i.yaml, P2-A-101 Rev J):
  event floor 120 x 144 ft [56,68]-[176,212]; 4 mats 42 x 42 ft (2 x 2, origins M1-M4)
  lower tier: telescopic, 6 rows x 2 ft, N / S / E, portal S, vomitories V1 (N) and V2 (E)
  upper tier: fixed, 5 rows x 3 ft, 21 in risers, front row 9.0 ft stepping UP to the L2 loop at 17.75 ft
  L2 running loop 7 ft wide, outer [49,34]-[210,246], inner [56,41]-[203,239]
Only the shell is the concept: radiused outline (R 34 ft ASSUMED). Lower-tier riser height 9.6 in ASSUMED
(rows up to 4.8 ft). Tier structure beneath is shown solid (massing only). Not a Rev D change.
"""
import numpy as np
from matplotlib.path import Path
import render_revD_srm_concept as C
import render_revD_views as B

NL = chr(10)
FLOOR_WOOD, MAT, MAT_CIRCLE = "#C9A56B", "#E6D7A8", "#B22222"
SEAT_RED, SEAT_BLACK, RISER = "#B01010", "#2A2A2A", "#8F8B82"
POCHE, TRACK, PIT = "#A29E94", "#A8402F", "#BDB9AE"
LOWER_RISE = 0.8


def cells(x0, y0, x1, y1, step, keep):
    for x in np.arange(x0, x1, step):
        for y in np.arange(y0, y1, step):
            if keep(x + step / 2, y + step / 2):
                yield x, y


def slab(x0, y0, x1, y1, z, col, sub=4, grp=1):
    C.add(grp, sub, [(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)], col)


def box(x0, y0, x1, y1, z0, z1, wall, top, grp=1):
    ctr = np.array([(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2])
    C.add(grp, 4, [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], top)
    for a, b in [((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))]:
        C.add(grp, 4, [(a[0], a[1], z0), (b[0], b[1], z0), (b[0], b[1], z1), (a[0], a[1], z1)], wall, ctr)


def spans(a0, a1, gaps):
    """Split [a0, a1] around the (g0, g1) gaps."""
    out, cur = [], a0
    for g0, g1 in sorted(gaps):
        if g0 > cur:
            out.append((cur, g0))
        cur = max(cur, g1)
    if cur < a1:
        out.append((cur, a1))
    return out


def build():
    C.polys.clear()
    ring = C.rrect(0, 0, 210, 252, C.RING_R)
    outline = Path(ring)

    def in_pit(x, y):
        return 56 <= x <= 203 and 41 <= y <= 239

    def in_loop(x, y):
        return 49 <= x <= 210 and 34 <= y <= 246 and not in_pit(x, y)

    # shell walls (both faces visible in the cutaway: no culling)
    o = np.array(ring)
    for i in range(len(o)):
        a, b = o[i], o[(i + 1) % len(o)]
        for z0, z1, cols in [(0, 3, (B.BLACK, B.BLACK)), (3, 17.75, (C.CONC_A, C.CONC_B))]:
            C.add(1, 4, [(a[0], a[1], z0), (b[0], b[1], z0), (b[0], b[1], z1), (a[0], a[1], z1)], cols[i % 2])

    # Level 2 deck: poche over lockers / lobby, running loop in track colour
    for x, y in cells(0, 0, 210, 252, 4.0, lambda cx, cy: outline.contains_point((cx, cy)) and not in_pit(cx, cy)):
        slab(x, y, x + 4, y + 4, 17.75, TRACK if in_loop(x + 2, y + 2) else POCHE)

    # pit floor + event floor + mats
    slab(56, 41, 203, 239, 0.0, PIT, sub=0)
    slab(56, 68, 176, 212, 0.04, FLOOR_WOOD, sub=1)
    ang = np.linspace(0, 2 * np.pi, 48)
    for mx, my in [(66, 145), (118, 145), (66, 93), (118, 93)]:
        slab(mx, my, mx + 42, my + 42, 0.08, MAT, sub=2)
        cx, cy = mx + 21, my + 21
        C.add(1, 3, [(cx + 14 * np.cos(a), cy + 14 * np.sin(a), 0.12) for a in ang], MAT_CIRCLE)

    # lower tier (telescopic, extended): rows step up away from the court
    lo_gaps = {"N": [(123.85, 131.85)], "S": [(107, 119)], "E": [(175.09, 183.09)]}
    for k in range(6):
        top = LOWER_RISE * (k + 1)
        col = SEAT_RED if k % 2 == 0 else "#8E0C0C"
        for a0, a1 in spans(56, 188, lo_gaps["N"]):
            box(a0, 212 + 2 * k, a1, 214 + 2 * k, 0, top, RISER, col)
        for a0, a1 in spans(56, 188, lo_gaps["S"]):
            box(a0, 66 - 2 * k, a1, 68 - 2 * k, 0, top, RISER, col)
        for a0, a1 in spans(68, 212, lo_gaps["E"]):
            box(176 + 2 * k, a0, 178 + 2 * k, a1, 0, top, RISER, col)

    # upper tier (fixed): front row 9.0 ft, 21 in risers, 3 ft treads, back at the L2 loop
    for k in range(5):
        top = 9.0 + 1.75 * k
        col = SEAT_BLACK if k % 2 == 0 else "#3D3D3D"
        box(56, 224 + 3 * k, 188, 227 + 3 * k, 0, top, RISER, col)       # N, front at y 224
        box(56, 53 - 3 * k, 188, 56 - 3 * k, 0, top, RISER, col)         # S, front at y 56
        box(188 + 3 * k, 41, 191 + 3 * k, 239, 0, top, RISER, col)       # E, front at x 188


C.build = build

if __name__ == "__main__":
    C.render("concepts/render_srm_concept_interior.png", 232, 50, (125, 140, 8), 175,
             "ARENA INTERIOR — CUTAWAY AT L2 FLOOR",
             "Cut at 17'-9" + chr(34) + ", roofs removed: 120 x 144 ft event floor, 4 x 42 ft mats, 1,100 lower + 1,100 upper seats",
             [((116, 140, 0.5), "event floor 120 x 144 ft" + NL + "4 mats (2 x 2)", (-0.5, 0.3)),
              ((182, 150, 3.5), "lower telescopic tier" + NL + "1,100 seats", (0.35, -0.3)),
              ((120, 232, 12), "upper fixed tier" + NL + "steps down from the L2 loop", (-0.12, 0.14)),
              ((206, 120, 17.75), "L2 running loop" + NL + "7 ft, 2 lanes", (0.45, 0.12))])
