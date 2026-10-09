#!/usr/bin/env python3
"""
Trojan Horse Arena — CONCEPT STUDY: "SRM headquarters language" arena + Summertown Metals pop-outs.

Design direction (Shane, 2026-10-08): the main arena emulates the SRM Concrete corporate headquarters
(curvilinear, no right angles, radiused corners, cylindrical forms, board-formed / exposed concrete,
slender exposed columns, floor-to-deck glass) because SRM supplies the concrete, aggregate and trucking;
Summertown Metals (SRM's customer) supplies the metal-building "pop-outs": storage annex (D-067) and
restroom bump-out (D-069/D-072).

Same bounding box and heights as the approved Rev D set (P2-A-101 Rev J / P2-A-901 Rev D); this is NOT a
Rev D change. All shape changes below are ASSUMED until a plan revision is drawn:
  ring corner radius 34 ft, arena-volume corner radius 30 ft and footprint x 42-210, y 56-212,
  NE stair tower as a 12.3 ft-radius cylinder, slender columns on the south face, pop-out roof pitch.
Corner rounding removes about 4 x (1 - pi/4) x 34^2 = 995 SF per level from the 210 x 252 footprint.
Reuses helpers from render_revD_views.py (same repo folder).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import render_revD_views as B

CONC_A, CONC_B = "#C9C5BB", "#BDB9AE"      # board-formed concrete, two tones for the form-board rhythm
GLASS_A, GLASS_B = "#6F8FA6", "#5F8099"    # floor-to-deck glass, mullion rhythm
METAL_A, METAL_B = "#3E444B", "#353A40"    # Summertown-style ribbed metal panel
METAL_ROOF = "#A31515"
RING_R, ARENA_R = 34.0, 30.0

polys = []   # (group, sub, pts, color, normal-or-None)


def add(group, sub, pts, col, center=None):
    p = np.array(pts, float)
    nrm = np.cross(p[1] - p[0], p[2] - p[0])
    if center is not None and np.dot(nrm, p.mean(axis=0) - center) < 0:
        nrm = -nrm
    for t in B._tiles(p, 12.0):
        polys.append((group, sub, t, B.shade(col, nrm), nrm if center is not None else None))


def rrect(x0, y0, x1, y1, r, n=9):
    pts = []
    for cx, cy, a0 in [(x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180), (x1 - r, y0 + r, 270)]:
        for a in np.radians(np.linspace(a0, a0 + 90, n)):
            pts.append((cx + r * np.cos(a), cy + r * np.sin(a)))
    return pts


def prism(group, outline, bands, roof_col, z_top):
    """Vertical-walled prism. bands = [(z0, z1, (colA, colB))]; roof is a flat top polygon."""
    o = np.array(outline, float)
    ctr = np.array([o[:, 0].mean(), o[:, 1].mean(), 0.0])
    for z0, z1, (ca, cb) in bands:
        c3 = ctr.copy(); c3[2] = (z0 + z1) / 2
        for i in range(len(o)):
            a, b = o[i], o[(i + 1) % len(o)]
            add(group, 1, [(a[0], a[1], z0), (b[0], b[1], z0), (b[0], b[1], z1), (a[0], a[1], z1)],
                ca if i % 2 == 0 else cb, c3)
    add(group, 0, [(x, y, z_top) for x, y in o], roof_col)


def gable(group, x0, y0, x1, y1, eave, rise, ridge_along_x):
    c = np.array([(x0 + x1) / 2, (y0 + y1) / 2, eave / 2])
    for k, (a, b) in enumerate([((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))]):
        add(group, 1, [(a[0], a[1], 0), (b[0], b[1], 0), (b[0], b[1], eave), (a[0], a[1], eave)],
            METAL_A if k % 2 == 0 else METAL_B, c)
    if ridge_along_x:
        ym = (y0 + y1) / 2
        add(group, 0, [(x0, y0, eave), (x1, y0, eave), (x1, ym, eave + rise), (x0, ym, eave + rise)], METAL_ROOF)
        add(group, 0, [(x0, ym, eave + rise), (x1, ym, eave + rise), (x1, y1, eave), (x0, y1, eave)], METAL_ROOF)
        add(group, 1, [(x0, y0, eave), (x0, y1, eave), (x0, ym, eave + rise)], METAL_B)   # gable ends
        add(group, 1, [(x1, y0, eave), (x1, y1, eave), (x1, ym, eave + rise)], METAL_B)
    else:
        xm = (x0 + x1) / 2
        add(group, 0, [(x0, y0, eave), (xm, y0, eave + rise), (xm, y1, eave + rise), (x0, y1, eave)], METAL_ROOF)
        add(group, 0, [(xm, y0, eave + rise), (x1, y0, eave), (x1, y1, eave), (xm, y1, eave + rise)], METAL_ROOF)
        add(group, 1, [(x0, y0, eave), (x1, y0, eave), (xm, y0, eave + rise)], METAL_B)
        add(group, 1, [(x0, y1, eave), (x1, y1, eave), (xm, y1, eave + rise)], METAL_B)


def build():
    polys.clear()
    # group 1: ring volume — black base / board-formed concrete / crimson reveal / floor-to-deck glass
    ring = rrect(0, 0, 210, 252, RING_R)
    prism(1, ring, [(0, 3, (B.BLACK, B.BLACK)), (3, 17.75, (CONC_A, CONC_B)),
                    (17.75, 19.25, (B.CRIMSON, B.CRIMSON)), (19.25, 32.75, (GLASS_A, GLASS_B))], "#7B7E82", 32.75)
    # group 2: arena volume — board-formed concrete drum above the ring
    arena = rrect(42, 56, 210, 212, ARENA_R)
    prism(2, arena, [(32.75, 42, (CONC_A, CONC_B))], "#5E6267", 42.0)
    # group 3: NE stair tower as a cylinder (ASSUMED), slender exposed columns on the south face
    t = np.radians(np.linspace(0, 360, 28, endpoint=False))
    tower = [(190 + 12.3 * np.cos(a), 244 + 12.3 * np.sin(a)) for a in t]
    prism(3, tower, [(0, 36, (CONC_A, CONC_B))], "#6A6E73", 36)
    for cx in (44, 74, 152, 172):
        c = np.array([cx, -5, 16.4])
        for k, (a, b) in enumerate([((cx - .7, -5.7), (cx + .7, -5.7)), ((cx + .7, -5.7), (cx + .7, -4.3)),
                                    ((cx + .7, -4.3), (cx - .7, -4.3)), ((cx - .7, -4.3), (cx - .7, -5.7))]):
            add(3, 1, [(a[0], a[1], 0), (b[0], b[1], 0), (b[0], b[1], 32.75), (a[0], a[1], 32.75)], CONC_A if k % 2 else CONC_B, c)
        add(3, 0, [(cx - .7, -5.7, 32.75), (cx + .7, -5.7, 32.75), (cx + .7, -4.3, 32.75), (cx - .7, -4.3, 32.75)], "#8C8F93")
    # group 4: Summertown metal pop-outs (annex north, bump-out east), group order set per camera in render
    gable(4, 52, 252, 122, 282, 16, 5, True)       # storage annex 70 x 30 (D-067)
    gable(5, 210, 161.09, 240, 217.09, 16, 4, False)  # restroom bump-out 30 x 56 (D-069)
    # group 6: Champion Walk + portal (limestone, as Rev D)
    for (x0, y0, x1, y1, col) in [(99, -30, 127, 0, B.BRICK), (93, -30, 99, 0, B.BAND), (127, -30, 133, 0, B.BAND),
                                  (85, -36, 91, -24, B.BAND), (135, -36, 141, -24, B.BAND), (85, -36, 141, -30, B.BAND)]:
        add(0, 2, [(x0, y0, .03), (x1, y0, .03), (x1, y1, .03), (x0, y1, .03)], col)
    xc, py0, py1 = 113.0, -36.0, -30.0
    for xa, xb in [(xc - 22, xc - 14), (xc + 14, xc + 22), (xc - 22, xc + 22)]:
        z0, z1 = (34, 50) if xa == xc - 22 and xb == xc + 22 else (0, 50)
        c = np.array([(xa + xb) / 2, (py0 + py1) / 2, (z0 + z1) / 2])
        for k, (a, b) in enumerate([((xa, py0), (xb, py0)), ((xb, py0), (xb, py1)), ((xb, py1), (xa, py1)), ((xa, py1), (xa, py0))]):
            add(6, 1, [(a[0], a[1], z0), (b[0], b[1], z0), (b[0], b[1], z1), (a[0], a[1], z1)], B.LIME, c)
        add(6, 0, [(xa, py0, z1), (xb, py0, z1), (xb, py1, z1), (xa, py1, z1)], B.LIME)
    tt = np.linspace(0, np.pi, 28)
    add(7, 0, [(xc - 14, py0 - .05, 0), (xc + 14, py0 - .05, 0)] +
        [(xc + 14 * np.cos(a), py0 - .05, 22.1 + 11.9 * np.sin(a)) for a in tt], "#6E1414")
    add(7, 1, [(xc + 14.3 * np.cos(a), py0 - .1, 22.1 + 12.4 * np.sin(a)) for a in tt] +
        [(xc + 13.0 * np.cos(a), py0 - .1, 22.1 + 11.2 * np.sin(a)) for a in tt[::-1]], B.GOLD)
    ang = np.linspace(0, 2 * np.pi, 40)
    add(7, 2, [(xc + 5.5 * np.cos(a), py0 - .15, 42 + 5.5 * np.sin(a)) for a in ang], B.BLACK)
    add(7, 3, [(xc + 4.6 * np.cos(a), py0 - .2, 42 + 4.6 * np.sin(a)) for a in ang], B.CRIMSON)


def render(name, cam, elev, target, half, title, sub, callouts, size=(13, 9)):
    build()
    az, el = np.radians(cam), np.radians(elev)
    c = np.array([np.cos(el) * np.cos(az), np.cos(el) * np.sin(az), np.sin(el)])
    r = np.array([-np.sin(az), np.cos(az), 0.0])
    u = np.array([-np.sin(el) * np.cos(az), -np.sin(el) * np.sin(az), np.cos(el)])
    items = []
    for g, sub_, p, col, nrm in polys:
        if nrm is not None and np.dot(nrm, c) <= 0:
            continue
        grp = g
        if g in (4, 5):       # pop-outs: in front of the ring wall they abut only when the camera is on their side
            front = (g == 4 and c[1] > 0) or (g == 5 and c[0] > 0)
            grp = 1.5 if front else 0.5
        if g == 6 or g == 7:  # portal over the building only from the south
            grp = (6 + (g - 6) * .1) if c[1] < 0 else 0.6
        items.append((grp, sub_, float(p.mean(axis=0) @ c), p, col))
    items.sort(key=lambda t: (t[0], t[1], t[2]))
    fig = plt.figure(figsize=size, dpi=130)
    ax = fig.add_axes([0, 0.06, 1, 0.86])
    gq = np.array([(-600, -600, -.05), (800, -600, -.05), (800, 900, -.05), (-600, 900, -.05)], float)
    ax.add_patch(plt.Polygon(np.c_[gq @ r, gq @ u], closed=True, fc=B.GROUND, ec=B.GROUND, lw=0))
    for _, _, _, p, col in items:
        ax.add_patch(plt.Polygon(np.c_[p @ r, p @ u], closed=True, fc=col, ec=col, lw=0.4))
    tgt = np.array(target, float)
    cx, cy = tgt @ r, tgt @ u
    ax.set_aspect("equal")
    ax.set_xlim(cx - half, cx + half)
    ax.set_ylim(cy - half * .69, cy + half * .69)
    ax.set_axis_off()
    for pt, text, off in callouts:
        p = np.array(pt, float)
        x, y = p @ r, p @ u
        ax.annotate(text, (x, y), (x + off[0] * half, y + off[1] * half), fontsize=8.5, fontweight="bold", color="#222",
                    ha="center", va="center", bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=B.CRIMSON, lw=1.2),
                    arrowprops=dict(arrowstyle="-|>", color=B.CRIMSON, lw=1.4))
    fig.patch.set_facecolor(B.GROUND)
    fig.text(0.5, 0.955, title, ha="center", fontsize=20, fontweight="bold", color=B.CRIMSON)
    fig.text(0.5, 0.925, sub, ha="center", fontsize=10.5, color="#333")
    fig.text(0.5, 0.03, "PRELIMINARY — CONCEPTUAL DESIGN — NOT FOR CONSTRUCTION  |  Concept study (D-074 direction), not a Rev D change  |  "
             "Same 210 x 252 ft envelope and heights as Set Rev D  |  Site TBD (D-006)", ha="center", fontsize=8.5, fontweight="bold", color="#222")
    fig.text(0.5, 0.008, "Curvilinear forms, radii, columns and pop-out roof pitch are ASSUMED until a plan revision is drawn  ·  "
             "SRM / Summertown Metals names are descriptive only; no logos or marks used", ha="center", fontsize=8, color="#555")
    fig.savefig(name, facecolor=fig.get_facecolor())
    plt.close(fig)
    print("wrote", name)


NL = chr(10)

if __name__ == "__main__":
    render("concepts/render_srm_concept_aerial_ne.png", 38, 30, (115, 130, 15), 190,
           "ARENA — SRM CONCRETE LANGUAGE", "Radiused board-formed concrete arena; floor-to-deck glass ring; Summertown Metals pop-outs",
           [((87, 267, 21), "SUMMERTOWN METALS" + NL + "storage annex (D-067)", (0.2, -0.38)),
            ((225, 190, 20), "SUMMERTOWN METALS" + NL + "restroom pop-out (D-069)", (-0.35, -0.3)),
            ((100, 150, 42), "SRM-style concrete arena" + NL + "no right angles · board-formed", (0.0, 0.42)),
            ((190, 244, 36), "cylindrical stair tower", (-0.02, -0.46))])
    render("concepts/render_srm_concept_aerial_se.png", 305, 28, (115, 130, 15), 190,
           "ARENA — SOUTHEAST VIEW", "Slender exposed columns and floor-to-deck glass; east pop-out in Summertown Metals",
           [((225, 190, 20), "SUMMERTOWN METALS" + NL + "restroom pop-out", (0.3, -0.38)),
            ((74, -5, 32), "slender exposed columns" + NL + "+ floor-to-deck glass", (-0.3, 0.4)),
            ((205, 40, 30), "radiused corner", (0.35, -0.42))])
    render("concepts/render_srm_concept_portal.png", 250, 17, (113, -20, 22), 80,
           "PORTAL + CHAMPION WALK", "Limestone portal and 40 ft walk (D-066) in front of the glass-and-concrete arena", [], size=(13, 8))
