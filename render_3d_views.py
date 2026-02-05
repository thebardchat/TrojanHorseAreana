#!/usr/bin/env python3
"""
Hazel Green Trojans Sports Complex — 3D Rendered Views Generator
Uses matplotlib 3D to produce presentation-quality renders.

Generates:
  - render_aerial.png    — Bird's eye view
  - render_entrance.png  — Front entrance perspective
  - render_arena.png     — Interior arena view
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.patheffects as pe
import numpy as np

# ============================================================
# CONSTANTS — Feet
# ============================================================
BLDG_W = 120
BLDG_D = 250
BLDG_H = 24
WALL_T = 8 / 12
LOBBY_H = 25
SUPPORT_H = 40
ARENA_Y = 65

# Colors
RED = "#CC0000"
DARK_RED = "#990000"
BLACK = "#1A1A1A"
DARK_GRAY = "#333333"
LIGHT_GRAY = "#B0B0B0"
STEEL = "#444444"
WHITE = "#FFFFFF"
ROOF_COLOR = "#363636"
LOBBY_FLOOR = "#2A2A2A"
SUPPORT_FLOOR = "#383838"


def box_faces(x0, y0, z0, dx, dy, dz):
    """Return 6 faces (list of 4-vertex polygons) for an axis-aligned box."""
    x1, y1, z1 = x0 + dx, y0 + dy, z0 + dz
    verts = [
        [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)],  # bottom
        [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)],  # top
        [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)],  # front
        [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)],  # back
        [(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)],  # left
        [(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)],  # right
    ]
    return verts


def cylinder_top(cx, cy, z, r, n=40):
    """Return a polygon approximation of a filled circle at height z."""
    angles = np.linspace(0, 2 * np.pi, n)
    verts = [(cx + r * np.cos(a), cy + r * np.sin(a), z) for a in angles]
    return [verts]


def cylinder_side(cx, cy, z0, z1, r, n=40):
    """Return strip faces for cylinder sides."""
    angles = np.linspace(0, 2 * np.pi, n)
    faces = []
    for i in range(n - 1):
        a0, a1 = angles[i], angles[i + 1]
        x0c, y0c = cx + r * np.cos(a0), cy + r * np.sin(a0)
        x1c, y1c = cx + r * np.cos(a1), cy + r * np.sin(a1)
        faces.append([(x0c, y0c, z0), (x1c, y1c, z0), (x1c, y1c, z1), (x0c, y0c, z1)])
    return faces


def add_building(ax, show_interior=False, show_roof=True):
    """Add all building geometry to axes."""
    wall_alpha = 0.30 if show_interior else 0.85
    roof_alpha = 0.12 if show_interior else 0.65

    # ---- Ground plane (parking/site) ----
    ground = box_faces(-40, -40, -1.5, BLDG_W + 80, BLDG_D + 80, 1.0)
    ax.add_collection3d(Poly3DCollection(
        ground, alpha=0.15, facecolor="#8B8B6B", edgecolor="none"
    ))

    # ---- Floor slab ----
    # Lobby floor (dark polished)
    lobby_floor = box_faces(WALL_T, WALL_T, -0.3, BLDG_W - 2 * WALL_T, LOBBY_H - WALL_T, 0.3)
    ax.add_collection3d(Poly3DCollection(
        lobby_floor, alpha=0.7, facecolor=LOBBY_FLOOR, edgecolor="#333", linewidth=0.2
    ))
    # Support floor
    sup_floor = box_faces(WALL_T, LOBBY_H, -0.3, BLDG_W - 2 * WALL_T, SUPPORT_H, 0.3)
    ax.add_collection3d(Poly3DCollection(
        sup_floor, alpha=0.6, facecolor=SUPPORT_FLOOR, edgecolor="#444", linewidth=0.2
    ))
    # Arena floor (light gray)
    arena_floor = box_faces(WALL_T, ARENA_Y, -0.3, BLDG_W - 2 * WALL_T, BLDG_D - ARENA_Y - WALL_T, 0.3)
    ax.add_collection3d(Poly3DCollection(
        arena_floor, alpha=0.5, facecolor=LIGHT_GRAY, edgecolor="#999", linewidth=0.2
    ))

    # ---- Exterior walls ----
    door_w = 12
    door_x = (BLDG_W - door_w) / 2
    door_h = 10

    # Front wall with door cutout
    lw = box_faces(0, 0, 0, door_x, WALL_T, BLDG_H)
    rw = box_faces(door_x + door_w, 0, 0, BLDG_W - door_x - door_w, WALL_T, BLDG_H)
    ad = box_faces(door_x, 0, door_h, door_w, WALL_T, BLDG_H - door_h)
    for w in [lw, rw, ad]:
        ax.add_collection3d(Poly3DCollection(
            w, alpha=wall_alpha, facecolor=BLACK, edgecolor="#2A2A2A", linewidth=0.3
        ))

    # Back wall
    bw = box_faces(0, BLDG_D - WALL_T, 0, BLDG_W, WALL_T, BLDG_H)
    ax.add_collection3d(Poly3DCollection(
        bw, alpha=wall_alpha, facecolor=BLACK, edgecolor="#2A2A2A", linewidth=0.3
    ))

    # Side walls
    lww = box_faces(0, 0, 0, WALL_T, BLDG_D, BLDG_H)
    rww = box_faces(BLDG_W - WALL_T, 0, 0, WALL_T, BLDG_D, BLDG_H)
    for w in [lww, rww]:
        ax.add_collection3d(Poly3DCollection(
            w, alpha=wall_alpha, facecolor=BLACK, edgecolor="#2A2A2A", linewidth=0.3
        ))

    # ---- Red accent band on exterior (stripe at 16-18ft height) ----
    band_z = 16
    band_h = 2
    # Front band
    fb = box_faces(0, -0.1, band_z, BLDG_W, 0.2, band_h)
    ax.add_collection3d(Poly3DCollection(
        fb, alpha=0.8, facecolor=RED, edgecolor=RED, linewidth=0.5
    ))
    # Side bands
    sb_l = box_faces(-0.1, 0, band_z, 0.2, BLDG_D, band_h)
    sb_r = box_faces(BLDG_W - 0.1, 0, band_z, 0.2, BLDG_D, band_h)
    for sb in [sb_l, sb_r]:
        ax.add_collection3d(Poly3DCollection(
            sb, alpha=0.7, facecolor=RED, edgecolor=RED, linewidth=0.3
        ))

    # ---- Roof with slight parapet ----
    if show_roof:
        roof = box_faces(-1, -1, BLDG_H, BLDG_W + 2, BLDG_D + 2, 1)
        ax.add_collection3d(Poly3DCollection(
            roof, alpha=roof_alpha, facecolor=ROOF_COLOR, edgecolor="#555", linewidth=0.3
        ))
        # Parapet edges
        for parapet in [
            box_faces(-1, -1, BLDG_H + 1, BLDG_W + 2, 1, 2),
            box_faces(-1, BLDG_D + 1, BLDG_H + 1, BLDG_W + 2, 1, 2),
            box_faces(-1, 0, BLDG_H + 1, 1, BLDG_D, 2),
            box_faces(BLDG_W, 0, BLDG_H + 1, 1, BLDG_D, 2),
        ]:
            ax.add_collection3d(Poly3DCollection(
                parapet, alpha=roof_alpha * 0.8, facecolor="#2A2A2A", edgecolor="#444", linewidth=0.2
            ))

    # ---- Interior walls (red accent) ----
    int_wall_h = BLDG_H * 0.55
    iw1 = box_faces(WALL_T, LOBBY_H, 0, BLDG_W - 2 * WALL_T, 0.5, int_wall_h)
    iw2 = box_faces(WALL_T, ARENA_Y, 0, BLDG_W - 2 * WALL_T, 0.5, int_wall_h)
    for iw in [iw1, iw2]:
        ax.add_collection3d(Poly3DCollection(
            iw, alpha=0.5, facecolor=RED, edgecolor=DARK_RED, linewidth=0.3
        ))

    # Vertical support zone partitions
    boys_x = WALL_T + 28
    sc_x = boys_x + 0.5 + 30
    girls_x = sc_x + 0.5 + 28
    for vx in [boys_x, sc_x, girls_x]:
        vw = box_faces(vx, LOBBY_H, 0, 0.5, SUPPORT_H, int_wall_h)
        ax.add_collection3d(Poly3DCollection(
            vw, alpha=0.4, facecolor=RED, edgecolor=DARK_RED, linewidth=0.2
        ))

    # ---- Championship mat ----
    arena_cy = ARENA_Y + (BLDG_D - ARENA_Y) / 2
    champ_r = 21

    # White border
    border = cylinder_top(BLDG_W / 2, arena_cy, 0.05, champ_r + 1.5, 72)
    ax.add_collection3d(Poly3DCollection(
        border, alpha=0.6, facecolor=WHITE, edgecolor="#DDD", linewidth=0.5
    ))
    # Main red mat
    champ = cylinder_top(BLDG_W / 2, arena_cy, 0.1, champ_r, 72)
    ax.add_collection3d(Poly3DCollection(
        champ, alpha=0.9, facecolor=RED, edgecolor=DARK_RED, linewidth=1
    ))
    # Inner circles
    for r in [15, 10, 5]:
        ring = cylinder_top(BLDG_W / 2, arena_cy, 0.12, r, 48)
        ax.add_collection3d(Poly3DCollection(
            ring, alpha=0.15, facecolor=WHITE, edgecolor=WHITE, linewidth=0.8
        ))
    # Mat sides (give it thickness)
    mat_sides = cylinder_side(BLDG_W / 2, arena_cy, 0, 0.4, champ_r, 72)
    ax.add_collection3d(Poly3DCollection(
        mat_sides, alpha=0.7, facecolor=DARK_RED, edgecolor=DARK_RED, linewidth=0.2
    ))

    # ---- Practice mats ----
    practice_r = 16
    practice_positions = [
        (BLDG_W / 2 - champ_r - practice_r - 4, arena_cy),
        (BLDG_W / 2 + champ_r + practice_r + 4, arena_cy),
        (BLDG_W / 2 - practice_r - 2, arena_cy + champ_r + practice_r + 4),
        (BLDG_W / 2 + practice_r + 2, arena_cy + champ_r + practice_r + 4),
    ]
    for (px, py) in practice_positions:
        bt = cylinder_top(px, py, 0.05, practice_r + 1, 48)
        ax.add_collection3d(Poly3DCollection(
            bt, alpha=0.4, facecolor=WHITE, edgecolor=WHITE, linewidth=0.3
        ))
        pt = cylinder_top(px, py, 0.1, practice_r, 48)
        ax.add_collection3d(Poly3DCollection(
            pt, alpha=0.85, facecolor=DARK_GRAY, edgecolor="#444", linewidth=0.5
        ))
        sides = cylinder_side(px, py, 0, 0.35, practice_r, 48)
        ax.add_collection3d(Poly3DCollection(
            sides, alpha=0.5, facecolor="#444", edgecolor="#444", linewidth=0.1
        ))

    # ---- Bleachers (stepped red) ----
    bleacher_y_start = ARENA_Y + 5
    bleacher_len = BLDG_D - ARENA_Y - 10
    for row in range(8):
        row_h = row * 1.0
        row_w = 1.5
        # Left
        lb = box_faces(WALL_T + 1 + row * row_w, bleacher_y_start, row_h,
                        row_w - 0.1, bleacher_len, 1.0)
        ax.add_collection3d(Poly3DCollection(
            lb, alpha=0.7, facecolor=RED, edgecolor=DARK_RED, linewidth=0.2
        ))
        # Right
        rb = box_faces(BLDG_W - WALL_T - 1 - (row + 1) * row_w, bleacher_y_start, row_h,
                        row_w - 0.1, bleacher_len, 1.0)
        ax.add_collection3d(Poly3DCollection(
            rb, alpha=0.7, facecolor=RED, edgecolor=DARK_RED, linewidth=0.2
        ))

    # ---- Entrance canopy ----
    canopy = box_faces((BLDG_W - 36) / 2, -10, door_h + 1, 36, 10, 0.5)
    ax.add_collection3d(Poly3DCollection(
        canopy, alpha=0.7, facecolor=BLACK, edgecolor="#333", linewidth=0.5
    ))
    # Red underside accent
    canopy_under = box_faces((BLDG_W - 34) / 2, -9, door_h + 0.5, 34, 9, 0.3)
    ax.add_collection3d(Poly3DCollection(
        canopy_under, alpha=0.5, facecolor=RED, edgecolor=RED, linewidth=0.2
    ))
    # Support columns
    for dx in [-14, 14]:
        col = box_faces(BLDG_W / 2 + dx - 0.5, -9, 0, 1, 1, door_h + 1)
        ax.add_collection3d(Poly3DCollection(
            col, alpha=0.8, facecolor=STEEL, edgecolor="#555", linewidth=0.3
        ))

    # ---- Signage placeholder (red banner above door) ----
    sign = box_faces(door_x - 8, -0.2, door_h + 2, door_w + 16, 0.3, 4)
    ax.add_collection3d(Poly3DCollection(
        sign, alpha=0.85, facecolor=RED, edgecolor=DARK_RED, linewidth=0.5
    ))

    # ---- Steel beams ----
    beam_h = 2
    beam_z = BLDG_H - beam_h - 0.5
    for y_off in range(0, BLDG_D, 25):
        beam = box_faces(WALL_T, y_off + WALL_T, beam_z,
                          BLDG_W - 2 * WALL_T, 0.5, beam_h)
        ax.add_collection3d(Poly3DCollection(
            beam, alpha=0.25, facecolor=STEEL, edgecolor=STEEL, linewidth=0.2
        ))

    return door_x, door_w, door_h, arena_cy


def render_view(elev, azim, title, subtitle, filename, show_interior=False,
                show_roof=True, zoom=1.0, xlim=None, ylim=None, zlim=None):
    """Render a 3D view of the complex."""
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
    ax = fig.add_subplot(111, projection="3d", computed_zorder=False)

    bg = "#EAEAEA"
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)

    add_building(ax, show_interior=show_interior, show_roof=show_roof)

    # Camera
    ax.view_init(elev=elev, azim=azim)

    # Axis limits
    pad = 30 / zoom
    if xlim:
        ax.set_xlim(*xlim)
    else:
        ax.set_xlim(-pad, BLDG_W + pad)
    if ylim:
        ax.set_ylim(*ylim)
    else:
        ax.set_ylim(-pad, BLDG_D + pad)
    if zlim:
        ax.set_zlim(*zlim)
    else:
        ax.set_zlim(-2, BLDG_H + 5)

    ax.set_axis_off()

    # Title bar
    ax.text2D(0.5, 0.97, title,
              transform=ax.transAxes, fontsize=22, fontweight="bold",
              ha="center", va="top", color=RED,
              path_effects=[pe.withStroke(linewidth=3, foreground="white")],
              bbox=dict(boxstyle="round,pad=0.4", facecolor="white", alpha=0.85,
                        edgecolor=RED, linewidth=2))

    # Subtitle bar
    ax.text2D(0.5, 0.03, subtitle,
              transform=ax.transAxes, fontsize=11, ha="center", va="bottom",
              color=STEEL, fontstyle="italic",
              bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7))

    # Branding
    ax.text2D(0.02, 0.02, "HAZEL GREEN TROJANS",
              transform=ax.transAxes, fontsize=9, fontweight="bold",
              ha="left", va="bottom", color=RED, alpha=0.6)
    ax.text2D(0.98, 0.02, "Phase 1 | $4M-$6M Budget",
              transform=ax.transAxes, fontsize=8,
              ha="right", va="bottom", color=STEEL, alpha=0.5)

    # Save
    out = f"/home/user/TrojanHorseAreana/{filename}"
    fig.savefig(out, dpi=100, bbox_inches="tight",
                facecolor=bg, edgecolor="none")
    plt.close(fig)
    print(f"  -> {out}")
    return out


def main():
    print("Generating 3D rendered views (v2)...")
    print("=" * 55)

    # 1. Aerial view
    print("[1/3] Aerial view...")
    render_view(
        elev=65, azim=-55,
        title="AERIAL VIEW",
        subtitle="Hazel Green Trojans Sports Complex  |  Phase 1  |  120' x 250'  |  ~30,000 SF  |  800 Seats",
        filename="render_aerial.png",
        show_interior=True,
        show_roof=True,
        zoom=0.85
    )

    # 2. Entrance perspective
    print("[2/3] Entrance perspective...")
    render_view(
        elev=20, azim=-70,
        title="ENTRANCE PERSPECTIVE",
        subtitle="Main Public Entry — South Elevation  |  \"Building Champions, One Mat at a Time\"",
        filename="render_entrance.png",
        show_interior=False,
        show_roof=True,
        zoom=1.8,
        ylim=(-30, 100),
        zlim=(-2, 30)
    )

    # 3. Arena interior
    print("[3/3] Arena interior...")
    render_view(
        elev=40, azim=-50,
        title="ARENA INTERIOR — Championship Center Mat",
        subtitle="4 Practice Mats + 1 Championship Mat (42ft)  |  800-Seat Bleacher Seating  |  24ft Ceiling",
        filename="render_arena.png",
        show_interior=True,
        show_roof=True,
        zoom=1.0
    )

    print("\n  All 3D renders complete!")


if __name__ == "__main__":
    main()
