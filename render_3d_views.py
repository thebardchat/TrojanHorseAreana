#!/usr/bin/env python3
"""
Hazel Green Trojans Sports Complex — 3D Rendered Views Generator
Uses matplotlib 3D + VTK (via CadQuery) to produce presentation-quality renders.

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
BLACK = "#1A1A1A"
DARK_GRAY = "#333333"
LIGHT_GRAY = "#B0B0B0"
STEEL = "#444444"
WHITE = "#FFFFFF"
ROOF_COLOR = "#363636"


def box_faces(x0, y0, z0, dx, dy, dz):
    """Return 6 faces (list of 4-vertex polygons) for an axis-aligned box."""
    x1, y1, z1 = x0 + dx, y0 + dy, z0 + dz
    verts = [
        # bottom
        [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)],
        # top
        [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)],
        # front (y=y0)
        [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)],
        # back (y=y1)
        [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)],
        # left (x=x0)
        [(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)],
        # right (x=x1)
        [(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)],
    ]
    return verts


def cylinder_top(cx, cy, z, r, n=40):
    """Return a polygon approximation of a filled circle at height z."""
    angles = np.linspace(0, 2 * np.pi, n)
    verts = [(cx + r * np.cos(a), cy + r * np.sin(a), z) for a in angles]
    return [verts]


def render_view(elev, azim, title, filename, show_interior=False, zoom=1.0):
    """Render a 3D view of the complex."""
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
    ax = fig.add_subplot(111, projection="3d", computed_zorder=False)
    fig.patch.set_facecolor("#E8E8E8")
    ax.set_facecolor("#E8E8E8")

    wall_alpha = 0.35 if show_interior else 0.85

    # ---- Floor slab ----
    floor = box_faces(0, 0, -0.5, BLDG_W, BLDG_D, 0.5)
    ax.add_collection3d(Poly3DCollection(
        floor, alpha=0.6, facecolor=LIGHT_GRAY, edgecolor="#999999", linewidth=0.3
    ))

    # ---- Exterior walls ----
    # Front wall (south, y=0) with door cutout
    door_w = 12
    door_x = (BLDG_W - door_w) / 2
    door_h = 10

    # Left section of front wall
    lw = box_faces(0, 0, 0, door_x, WALL_T, BLDG_H)
    ax.add_collection3d(Poly3DCollection(
        lw, alpha=wall_alpha, facecolor=BLACK, edgecolor="#333", linewidth=0.3
    ))
    # Right section of front wall
    rw = box_faces(door_x + door_w, 0, 0, BLDG_W - door_x - door_w, WALL_T, BLDG_H)
    ax.add_collection3d(Poly3DCollection(
        rw, alpha=wall_alpha, facecolor=BLACK, edgecolor="#333", linewidth=0.3
    ))
    # Above door
    ad = box_faces(door_x, 0, door_h, door_w, WALL_T, BLDG_H - door_h)
    ax.add_collection3d(Poly3DCollection(
        ad, alpha=wall_alpha, facecolor=BLACK, edgecolor="#333", linewidth=0.3
    ))

    # Back wall (north, y=BLDG_D)
    bw = box_faces(0, BLDG_D - WALL_T, 0, BLDG_W, WALL_T, BLDG_H)
    ax.add_collection3d(Poly3DCollection(
        bw, alpha=wall_alpha, facecolor=BLACK, edgecolor="#333", linewidth=0.3
    ))

    # Left wall (west, x=0)
    lww = box_faces(0, 0, 0, WALL_T, BLDG_D, BLDG_H)
    ax.add_collection3d(Poly3DCollection(
        lww, alpha=wall_alpha, facecolor=BLACK, edgecolor="#333", linewidth=0.3
    ))

    # Right wall (east, x=BLDG_W)
    rww = box_faces(BLDG_W - WALL_T, 0, 0, WALL_T, BLDG_D, BLDG_H)
    ax.add_collection3d(Poly3DCollection(
        rww, alpha=wall_alpha, facecolor=BLACK, edgecolor="#333", linewidth=0.3
    ))

    # ---- Roof ----
    roof = box_faces(-1, -1, BLDG_H, BLDG_W + 2, BLDG_D + 2, 1)
    roof_alpha = 0.15 if show_interior else 0.7
    ax.add_collection3d(Poly3DCollection(
        roof, alpha=roof_alpha, facecolor=ROOF_COLOR, edgecolor="#555", linewidth=0.3
    ))

    # ---- Interior walls (red accent) ----
    int_wall_h = BLDG_H * 0.55
    # Lobby/support divider
    iw1 = box_faces(WALL_T, LOBBY_H, 0, BLDG_W - 2 * WALL_T, 0.5, int_wall_h)
    ax.add_collection3d(Poly3DCollection(
        iw1, alpha=0.6, facecolor=RED, edgecolor=RED, linewidth=0.3
    ))
    # Support/arena divider
    iw2 = box_faces(WALL_T, ARENA_Y, 0, BLDG_W - 2 * WALL_T, 0.5, int_wall_h)
    ax.add_collection3d(Poly3DCollection(
        iw2, alpha=0.6, facecolor=RED, edgecolor=RED, linewidth=0.3
    ))

    # ---- Championship mat (red circle) ----
    arena_cy = ARENA_Y + (BLDG_D - ARENA_Y) / 2
    champ_r = 21
    champ_top = cylinder_top(BLDG_W / 2, arena_cy, 0.4, champ_r, 60)
    ax.add_collection3d(Poly3DCollection(
        champ_top, alpha=0.9, facecolor=RED, edgecolor="#990000", linewidth=1
    ))
    # White border
    border_top = cylinder_top(BLDG_W / 2, arena_cy, 0.35, champ_r + 1, 60)
    ax.add_collection3d(Poly3DCollection(
        border_top, alpha=0.5, facecolor=WHITE, edgecolor=WHITE, linewidth=0.5
    ))

    # ---- Practice mats (dark gray circles) ----
    practice_r = 16
    practice_positions = [
        (BLDG_W / 2 - champ_r - practice_r - 4, arena_cy),
        (BLDG_W / 2 + champ_r + practice_r + 4, arena_cy),
        (BLDG_W / 2 - practice_r - 2, arena_cy + champ_r + practice_r + 4),
        (BLDG_W / 2 + practice_r + 2, arena_cy + champ_r + practice_r + 4),
    ]
    for (px, py) in practice_positions:
        pt = cylinder_top(px, py, 0.4, practice_r, 40)
        ax.add_collection3d(Poly3DCollection(
            pt, alpha=0.85, facecolor=DARK_GRAY, edgecolor="#555", linewidth=0.5
        ))
        bt = cylinder_top(px, py, 0.35, practice_r + 0.5, 40)
        ax.add_collection3d(Poly3DCollection(
            bt, alpha=0.4, facecolor=WHITE, edgecolor=WHITE, linewidth=0.3
        ))

    # ---- Bleachers (stepped red blocks) ----
    bleacher_y_start = ARENA_Y + 5
    bleacher_len = BLDG_D - ARENA_Y - 10
    for row in range(8):
        row_h = row * 1.0
        row_w = 1.5
        # Left
        lb = box_faces(WALL_T + 1 + row * row_w, bleacher_y_start, row_h,
                        row_w - 0.1, bleacher_len, 1.0)
        ax.add_collection3d(Poly3DCollection(
            lb, alpha=0.7, facecolor=RED, edgecolor="#990000", linewidth=0.2
        ))
        # Right
        rb = box_faces(BLDG_W - WALL_T - 1 - (row + 1) * row_w, bleacher_y_start, row_h,
                        row_w - 0.1, bleacher_len, 1.0)
        ax.add_collection3d(Poly3DCollection(
            rb, alpha=0.7, facecolor=RED, edgecolor="#990000", linewidth=0.2
        ))

    # ---- Entrance canopy ----
    canopy = box_faces((BLDG_W - 30) / 2, -8, door_h + 1, 30, 8, 0.3)
    ax.add_collection3d(Poly3DCollection(
        canopy, alpha=0.6, facecolor=BLACK, edgecolor="#333", linewidth=0.5
    ))
    # Canopy columns
    for dx in [-12, 12]:
        col = box_faces(BLDG_W / 2 + dx - 0.5, -7, 0, 1, 1, door_h + 1)
        ax.add_collection3d(Poly3DCollection(
            col, alpha=0.7, facecolor=STEEL, edgecolor="#555", linewidth=0.3
        ))

    # ---- Steel beams (simplified as bars under roof) ----
    beam_h = 2
    beam_z = BLDG_H - beam_h - 0.5
    for y_off in range(0, BLDG_D, 25):
        beam = box_faces(WALL_T, y_off + WALL_T, beam_z,
                          BLDG_W - 2 * WALL_T, 0.5, beam_h)
        ax.add_collection3d(Poly3DCollection(
            beam, alpha=0.3, facecolor=STEEL, edgecolor=STEEL, linewidth=0.2
        ))

    # ---- Title text ----
    ax.text2D(0.5, 0.96, title,
              transform=ax.transAxes, fontsize=20, fontweight="bold",
              ha="center", va="top", color=RED,
              bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    ax.text2D(0.5, 0.02,
              "Hazel Green Trojans Sports Complex — Phase 1  |  120' × 250'  |  ~30,000 SF",
              transform=ax.transAxes, fontsize=10, ha="center", va="bottom",
              color=STEEL, fontstyle="italic")

    # ---- Camera ----
    ax.view_init(elev=elev, azim=azim)

    # Set axis limits with zoom
    pad = 30 / zoom
    ax.set_xlim(-pad, BLDG_W + pad)
    ax.set_ylim(-pad, BLDG_D + pad)
    ax.set_zlim(-2, BLDG_H + 5)

    ax.set_axis_off()

    # Save
    out = f"/home/user/TrojanHorseAreana/{filename}"
    fig.savefig(out, dpi=100, bbox_inches="tight",
                facecolor="#E8E8E8", edgecolor="none")
    plt.close(fig)
    print(f"✓ Render saved: {out}")
    return out


def main():
    print("Generating 3D rendered views...")
    print("=" * 50)

    # Aerial view — bird's eye
    render_view(
        elev=70, azim=-60,
        title="AERIAL VIEW — Hazel Green Trojans Sports Complex",
        filename="render_aerial.png",
        show_interior=True,
        zoom=0.9
    )

    # Entrance perspective — low angle from south
    render_view(
        elev=15, azim=-80,
        title="ENTRANCE VIEW — Hazel Green Trojans Sports Complex",
        filename="render_entrance.png",
        show_interior=False,
        zoom=1.2
    )

    # Arena interior — angled from inside looking at championship mat
    render_view(
        elev=35, azim=-45,
        title="ARENA INTERIOR — Championship Center Mat",
        filename="render_arena.png",
        show_interior=True,
        zoom=1.0
    )

    print("\n✓ All 3D renders complete!")


if __name__ == "__main__":
    main()
