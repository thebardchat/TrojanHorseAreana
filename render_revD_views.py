#!/usr/bin/env python3
"""
Trojan Horse Arena — Phase 2 Rev D massing renders (presentation views).

Replaces the superseded Feb 2026 120x250 concept renders (render_3d_views.py).
Geometry is taken from the approved Rev D set (feet; x east, y north, building SW corner = 0,0,
south = lobby / main entry side):
  P2-A-101 Rev J / phase2_plan_rev_i.yaml, P2-A-901 Rev D (massing), P2-C-101 Rev F (site).

MASSING ONLY. Heights not marked DECIDED are ASSUMED. The arena-volume footprint is read from the
P2-A-901 Rev D views, not dimensioned. Not a rendering of a final design.
  DECIDED : 210 x 252 ft footprint, L2 FF 17'-9", ring roof 32.75 ft, arena roof 42 ft (D-061)
            storage annex 70 x 30 (D-067), restroom bump-out 30 x 56 (D-069/D-072),
            portal <= 50 ft, arch crown 34 ft (D-050), walk 40 ft at the doors (D-066)
  ASSUMED : annex / bump-out height 16 ft, NE stair tower height, portal width 44 ft / pier 8 ft,
            arena-volume footprint (x 42-210, y 56-232)
Outputs: render_revD_aerial_sw.png, render_revD_aerial_se.png, render_revD_portal.png
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

LIME = "#D9D3C1"
LIME_DK = "#B8B29E"
ROOF = "#8A8D91"
ROOF_ARENA = "#6F7378"
CRIMSON = "#CC0000"
BLACK = "#1A1A1A"
GOLD = "#C9A227"
BRICK = "#A9553C"
BAND = "#D9B79A"
GROUND = "#E9E7DF"

LIGHT = np.array([-0.45, -0.6, 0.66])
LIGHT /= np.linalg.norm(LIGHT)

polys = []  # (verts, color)


def shade(hexcol, normal, floor=0.55):
    n = np.asarray(normal, float)
    n /= np.linalg.norm(n) + 1e-9
    k = floor + (1 - floor) * max(0.0, float(n @ LIGHT))
    c = np.array(matplotlib.colors.to_rgb(hexcol)) * k
    return np.clip(c, 0, 1)


def _tiles(p, step=14.0):
    """Subdivide a quad into tiles so the painter's sort stays correct for large faces."""
    if len(p) != 4:
        return [p]
    u, v = p[1] - p[0], p[3] - p[0]
    nu = max(1, int(np.ceil(np.linalg.norm(u) / step)))
    nv = max(1, int(np.ceil(np.linalg.norm(v) / step)))
    out = []
    for i in range(nu):
        for j in range(nv):
            a = p[0] + u * i / nu + v * j / nv
            out.append(np.array([a, a + u / nu, a + u / nu + v / nv, a + v / nv]))
    return out


def add_poly(pts, col, center=None):
    p = np.array(pts, float)
    nrm = np.cross(p[1] - p[0], p[2] - p[0])
    if center is not None and np.dot(nrm, p.mean(axis=0) - center) < 0:
        nrm = -nrm
    for t in _tiles(p):
        polys.append((t, shade(col, nrm), nrm if center is not None else None))


def box(x0, y0, z0, x1, y1, z1, wall=LIME, roof=ROOF):
    c = np.array([(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2])
    add_poly([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], roof, c)
    add_poly([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], wall, c)  # south
    add_poly([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], wall, c)  # north
    add_poly([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], wall, c)  # west
    add_poly([(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)], wall, c)  # east


def flat(x0, y0, x1, y1, col, z=0.02):
    add_poly([(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)], col)


def arch_front(xc, y, z0, hw, spring, crown, col, n=28):
    """Filled arch opening in the plane y (portal underside / opening, viewed from the south)."""
    t = np.linspace(0, np.pi, n)
    r = hw
    zc = spring
    rise = crown - spring
    pts = [(xc - hw, y, z0), (xc + hw, y, z0)]
    for a in t:
        pts.append((xc + r * np.cos(a), y, zc + rise * np.sin(a)))
    add_poly(pts, col)


def build():
    polys.clear()
    global GROUND_N
    GROUND_N = 0

    # --- building volumes (P2-A-901 Rev D) ---
    box(0, 0, 0, 210, 252, 32.75, LIME, ROOF)                       # ring volume (L1 + L2 loop) 32.75
    box(42, 56, 32.75, 210, 232, 42.0, LIME_DK, ROOF_ARENA)         # arena volume 42 ft (footprint ASSUMED)
    box(185.917, 252, 0, 210, 258.667, 32.75, LIME_DK, ROOF)        # NE stair tower (ST-2)
    global ANNEX_R, BUMP_R
    n0 = len(polys)
    box(52, 252, 0, 122, 282, 16, LIME, ROOF)                       # storage annex 70 x 30, 16 ft ASSUMED
    ANNEX_R = (n0, len(polys))
    n0 = len(polys)
    box(210, 161.09, 0, 240, 217.09, 16, LIME, ROOF)                # restroom bump-out 30 x 56, 16 ft ASSUMED
    BUMP_R = (n0, len(polys))

    # crimson reveal band + black base so the volume reads as the brand, not a gray box
    for (xa, xb, ya, yb) in [(0, 210, 0, 0.0)]:
        add_poly([(xa, ya - 0.05, 17.75), (xb, ya - 0.05, 17.75), (xb, ya - 0.05, 19.25), (xa, ya - 0.05, 19.25)], CRIMSON)
    add_poly([(0, -0.05, 0), (210, -0.05, 0), (210, -0.05, 3), (0, -0.05, 3)], BLACK)

    # --- site: Champion Walk (D-066) 40 ft at the doors: 28 brick + 2 x 6 paved bands, portal 30 ft out ---
    flat(99, -30, 127, 0, BRICK, 0.03)
    flat(93, -30, 99, 0, BAND, 0.03)
    flat(127, -30, 133, 0, BAND, 0.03)
    flat(85, -36, 91, -24, BAND, 0.03)
    flat(135, -36, 141, -24, BAND, 0.03)
    flat(85, -36, 141, -30, BAND, 0.03)

    global PORTAL_N
    PORTAL_N = len(polys)
    # --- freestanding portal (D-043/D-050): piers 8 ft, 44 ft wide ASSUMED, <= 50 ft, crown 34, spring 22.1 ---
    py0, py1 = -36.0, -30.0   # 6 ft deep ASSUMED
    xc = 113.0
    for xa, xb in [(xc - 22, xc - 14), (xc + 14, xc + 22)]:
        box(xa, py0, 0, xb, py1, 50, LIME, LIME)
    # lintel / arch spandrel above the opening up to 50 ft
    box(xc - 22, py0, 34, xc + 22, py1, 50, LIME, LIME)
    global DETAIL_N
    DETAIL_N = len(polys)
    # arch opening (shadowed crimson soffit) + gold trim
    arch_front(xc, py0 - 0.05, 0, 14, 22.1, 34, "#6E1414")
    t = np.linspace(0, np.pi, 28)
    trim = [(xc + 14.3 * np.cos(a), py0 - 0.1, 22.1 + 12.4 * np.sin(a)) for a in t]
    trim2 = [(xc + 13.0 * np.cos(a), py0 - 0.1, 22.1 + 11.2 * np.sin(a)) for a in t]
    add_poly(trim + trim2[::-1], GOLD)
    # official badge, 11 ft dia (D-047) on the spandrel
    ang = np.linspace(0, 2 * np.pi, 40)
    add_poly([(xc + 5.5 * np.cos(a), py0 - 0.15, 42 + 5.5 * np.sin(a)) for a in ang], BLACK)
    add_poly([(xc + 4.6 * np.cos(a), py0 - 0.2, 42 + 4.6 * np.sin(a)) for a in ang], CRIMSON)

    global PORTAL_END
    PORTAL_END = len(polys)
    # --- south entry face: 8-pair door bank (x 87.25-138.75), dark glazing ---
    add_poly([(87.25, -0.1, 0), (138.75, -0.1, 0), (138.75, -0.1, 9), (87.25, -0.1, 9)], "#2B3139")


def render(name, cam, elev, span, title, sub, size=(13, 9)):
    """cam = camera position azimuth in degrees (0 = east of building, 90 = north, 180 = west, 270 = south)."""
    build()
    az, el = np.radians(cam), np.radians(elev)
    c = np.array([np.cos(el) * np.cos(az), np.cos(el) * np.sin(az), np.sin(el)])
    r = np.array([-np.sin(az), np.cos(az), 0.0])
    u = np.array([-np.sin(el) * np.cos(az), -np.sin(el) * np.sin(az), np.cos(el)])
    items = []
    for i, (p, col, nrm) in enumerate(polys):
        if nrm is not None and np.dot(nrm, c) <= 0:
            continue  # back face of a closed solid
        d = float(p.mean(axis=0) @ c)
        layer = 1
        if (ANNEX_R[0] <= i < ANNEX_R[1] and c[1] > 0) or (BUMP_R[0] <= i < BUMP_R[1] and c[0] > 0):
            layer = 2  # annex / bump-out are in front of the ring wall they abut
        if PORTAL_N <= i < PORTAL_END and c[1] < 0:
            layer = 3 if i >= DETAIL_N else 2  # portal body over the building, its face details over the body
        items.append((layer, d, i, p, col))
    items.sort(key=lambda t: (t[0], t[1]))
    fig = plt.figure(figsize=size, dpi=130)
    ax = fig.add_axes([0, 0.06, 1, 0.86])
    g = np.array([(-600, -600, -0.05), (800, -600, -0.05), (800, 900, -0.05), (-600, 900, -0.05)], float)
    ax.add_patch(plt.Polygon(np.c_[g @ r, g @ u], closed=True, fc=GROUND, ec=GROUND, lw=0))
    for _, _, _, p, col in items:
        xy = np.c_[p @ r, p @ u]
        ax.add_patch(plt.Polygon(xy, closed=True, fc=col, ec=col, lw=0.4))
    allp = np.vstack([p for _, _, _, p, _ in items])
    ctr = np.array([span[0], span[1], span[2]])
    ax.set_aspect("equal")
    cx, cy = ctr @ r, ctr @ u
    ax.set_xlim(cx - span[3], cx + span[3])
    ax.set_ylim(cy - span[3] * 0.69, cy + span[3] * 0.69)
    ax.set_axis_off()
    fig.patch.set_facecolor(GROUND)
    fig.text(0.5, 0.955, title, ha="center", fontsize=20, fontweight="bold", color=CRIMSON)
    fig.text(0.5, 0.925, sub, ha="center", fontsize=10.5, color="#333")
    fig.text(0.5, 0.03, "PRELIMINARY — CONCEPTUAL DESIGN — NOT FOR CONSTRUCTION  |  Massing only, from Phase 2 Set Rev D "
             "(P2-A-901 Rev D / P2-A-101 Rev J)  |  Site TBD (D-006)", ha="center", fontsize=9, fontweight="bold", color="#222")
    fig.text(0.5, 0.008, "Trojan Horse Arena · Hazel Green Regional Athletic Complex · 210 × 252 ft · 2 levels · 85,793 GSF · "
             "2,200 seats · Heights not marked DECIDED are ASSUMED", ha="center", fontsize=8, color="#555")
    fig.savefig(name, facecolor=fig.get_facecolor())
    plt.close(fig)
    print("wrote", name)


if __name__ == "__main__":
    # span = (target x, target y, target z, half-width of the view in ft)
    render("concepts/render_revD_aerial_sw.png", 235, 28, (115, 130, 15, 190),
           "AERIAL FROM SOUTHWEST", "Main entry, portal and Champion Walk on the south; storage annex north; restroom bump-out east")
    render("concepts/render_revD_aerial_se.png", 305, 28, (115, 130, 15, 190),
           "AERIAL FROM SOUTHEAST", "East restroom bump-out (D-069/D-072) and arena volume flush with the east wall")
    render("concepts/render_revD_portal.png", 250, 17, (113, -20, 22, 80),
           "PORTAL + CHAMPION WALK", "Freestanding limestone portal (50 ft max, crown 34 ft), 40 ft walk at the doors (D-066)",
           size=(13, 8))
