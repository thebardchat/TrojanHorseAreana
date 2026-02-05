#!/usr/bin/env python3
"""
Hazel Green Trojans Sports Complex — Professional 2D Floor Plan Renderer
Generates a high-resolution annotated floor plan PNG for fundraising presentations.

School Colors: Red (#CC0000) and Black (#1A1A1A)
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Arc, Wedge
import matplotlib.patheffects as pe
import numpy as np

# ============================================================
# CONSTANTS — All dimensions in feet for the floor plan
# ============================================================
BLDG_W = 120  # ft
BLDG_D = 250  # ft
WALL_T = 8 / 12  # ft (8 inches)
INT_WALL_T = 6 / 12  # ft

# Colors
BLACK = "#1A1A1A"
RED = "#CC0000"
DARK_RED = "#990000"
DARK_GRAY = "#333333"
LIGHT_GRAY = "#B0B0B0"
LOBBY_FLOOR = "#2A2A2A"
WHITE = "#FFFFFF"
STEEL_GRAY = "#444444"
SEAT_RED = "#CC0000"
MAT_GRAY = "#3A3A3A"
ARENA_FLOOR = "#C8C8C8"
BG_COLOR = "#F5F5F0"

# Zone Y-coordinates
LOBBY_Y = 0
LOBBY_H = 25
SUPPORT_Y = 25
SUPPORT_H = 40
ARENA_Y = 65
ARENA_H = 185  # to Y=250

# Support sub-widths
BOYS_W = 28
SC_W = 30
GIRLS_W = 28
REST_W = BLDG_W - BOYS_W - SC_W - GIRLS_W  # 34

# Mat dimensions
STD_MAT_R = 16  # ft radius
CHAMP_MAT_R = 21  # ft radius


def draw_floorplan():
    fig, ax = plt.subplots(1, 1, figsize=(16, 33), dpi=120)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    # ========== BUILDING OUTLINE ==========
    # Exterior walls
    ext_rect = patches.Rectangle(
        (0, 0), BLDG_W, BLDG_D,
        linewidth=4, edgecolor=BLACK, facecolor="none", zorder=10
    )
    ax.add_patch(ext_rect)

    # ========== LOBBY ZONE ==========
    lobby = patches.Rectangle(
        (WALL_T, WALL_T), BLDG_W - 2 * WALL_T, LOBBY_H - WALL_T,
        facecolor=LOBBY_FLOOR, edgecolor="none", alpha=0.7, zorder=1
    )
    ax.add_patch(lobby)

    # Main entrance doors
    door_w = 12
    door_x = (BLDG_W - door_w) / 2
    ax.plot([door_x, door_x], [-2, 0], color=RED, linewidth=4, zorder=12)
    ax.plot([door_x + door_w, door_x + door_w], [-2, 0], color=RED, linewidth=4, zorder=12)
    ax.plot([door_x, door_x + door_w], [-2, -2], color=RED, linewidth=3, zorder=12)
    # Door swing arcs
    arc1 = Arc((door_x, 0), door_w * 0.4, door_w * 0.4, angle=0,
               theta1=270, theta2=360, color=RED, linewidth=1.5, zorder=12)
    arc2 = Arc((door_x + door_w, 0), door_w * 0.4, door_w * 0.4, angle=0,
               theta1=180, theta2=270, color=RED, linewidth=1.5, zorder=12)
    ax.add_patch(arc1)
    ax.add_patch(arc2)

    # Entrance canopy outline
    canopy = patches.Rectangle(
        (door_x - 9, -8), door_w + 18, 8,
        linewidth=2, edgecolor=STEEL_GRAY, facecolor="none",
        linestyle="--", zorder=10
    )
    ax.add_patch(canopy)
    ax.text(BLDG_W / 2, -4, "ENTRANCE CANOPY", fontsize=7,
            ha="center", va="center", color=STEEL_GRAY, fontstyle="italic")

    # ========== HORIZONTAL DIVIDER: LOBBY / SUPPORT ==========
    ax.plot([WALL_T, BLDG_W - WALL_T], [LOBBY_H, LOBBY_H],
            color=BLACK, linewidth=2.5, zorder=10)

    # ========== SUPPORT ZONE ==========
    sy = SUPPORT_Y
    sx = WALL_T

    # Boys Locker Room
    boys = patches.Rectangle(
        (sx, sy), BOYS_W, SUPPORT_H,
        facecolor="#2D2D2D", edgecolor=BLACK, linewidth=1.5, alpha=0.6, zorder=2
    )
    ax.add_patch(boys)
    ax.text(sx + BOYS_W / 2, sy + SUPPORT_H / 2, "BOYS\nLOCKER\nROOM",
            fontsize=10, fontweight="bold", ha="center", va="center",
            color=WHITE, zorder=15)
    ax.text(sx + BOYS_W / 2, sy + SUPPORT_H - 3, "2,000 SF",
            fontsize=7, ha="center", va="center", color=LIGHT_GRAY, zorder=15)

    # S&C / Weight Room
    sc_x = sx + BOYS_W + INT_WALL_T
    sc = patches.Rectangle(
        (sc_x, sy), SC_W, SUPPORT_H,
        facecolor="#3A1A1A", edgecolor=BLACK, linewidth=1.5, alpha=0.6, zorder=2
    )
    ax.add_patch(sc)
    ax.text(sc_x + SC_W / 2, sy + SUPPORT_H / 2, "S&C /\nWEIGHT\nROOM",
            fontsize=10, fontweight="bold", ha="center", va="center",
            color=RED, zorder=15)
    ax.text(sc_x + SC_W / 2, sy + SUPPORT_H - 3, "3,000 SF",
            fontsize=7, ha="center", va="center", color=LIGHT_GRAY, zorder=15)

    # Girls Locker Room
    girls_x = sc_x + SC_W + INT_WALL_T
    girls = patches.Rectangle(
        (girls_x, sy), GIRLS_W, SUPPORT_H,
        facecolor="#2D2D2D", edgecolor=BLACK, linewidth=1.5, alpha=0.6, zorder=2
    )
    ax.add_patch(girls)
    ax.text(girls_x + GIRLS_W / 2, sy + SUPPORT_H / 2, "GIRLS\nLOCKER\nROOM",
            fontsize=10, fontweight="bold", ha="center", va="center",
            color=WHITE, zorder=15)
    ax.text(girls_x + GIRLS_W / 2, sy + SUPPORT_H - 3, "2,000 SF",
            fontsize=7, ha="center", va="center", color=LIGHT_GRAY, zorder=15)

    # Restrooms & Concessions
    rest_x = girls_x + GIRLS_W + INT_WALL_T
    rest = patches.Rectangle(
        (rest_x, sy), REST_W - WALL_T - INT_WALL_T, SUPPORT_H,
        facecolor="#2A1A1A", edgecolor=BLACK, linewidth=1.5, alpha=0.6, zorder=2
    )
    ax.add_patch(rest)
    ax.text(rest_x + (REST_W - WALL_T) / 2, sy + SUPPORT_H * 0.35, "RESTROOMS",
            fontsize=9, fontweight="bold", ha="center", va="center",
            color=WHITE, zorder=15)
    ax.text(rest_x + (REST_W - WALL_T) / 2, sy + SUPPORT_H * 0.65, "CONCESSIONS",
            fontsize=9, fontweight="bold", ha="center", va="center",
            color=RED, zorder=15)
    ax.text(rest_x + (REST_W - WALL_T) / 2, sy + SUPPORT_H - 3, "1,000 SF",
            fontsize=7, ha="center", va="center", color=LIGHT_GRAY, zorder=15)

    # Divider lines in support zone (vertical)
    for vx in [sx + BOYS_W, sc_x + SC_W, girls_x + GIRLS_W]:
        ax.plot([vx, vx], [sy, sy + SUPPORT_H],
                color=BLACK, linewidth=2, zorder=10)

    # ========== HORIZONTAL DIVIDER: SUPPORT / ARENA ==========
    ax.plot([WALL_T, BLDG_W - WALL_T], [ARENA_Y, ARENA_Y],
            color=BLACK, linewidth=2.5, zorder=10)

    # ========== ARENA ZONE ==========
    arena = patches.Rectangle(
        (WALL_T, ARENA_Y), BLDG_W - 2 * WALL_T, ARENA_H - WALL_T,
        facecolor=ARENA_FLOOR, edgecolor="none", alpha=0.5, zorder=1
    )
    ax.add_patch(arena)

    arena_cx = BLDG_W / 2
    arena_cy = ARENA_Y + ARENA_H / 2

    # Championship center mat
    champ_border = Circle(
        (arena_cx, arena_cy), CHAMP_MAT_R + 1,
        facecolor="none", edgecolor=WHITE, linewidth=3, zorder=5
    )
    ax.add_patch(champ_border)

    champ_mat = Circle(
        (arena_cx, arena_cy), CHAMP_MAT_R,
        facecolor=RED, edgecolor=DARK_RED, linewidth=2, alpha=0.85, zorder=5
    )
    ax.add_patch(champ_mat)

    # Inner circles on championship mat
    for r in [15, 10, 5]:
        inner = Circle(
            (arena_cx, arena_cy), r,
            facecolor="none", edgecolor=WHITE, linewidth=1.5,
            alpha=0.6, linestyle="--", zorder=6
        )
        ax.add_patch(inner)

    ax.text(arena_cx, arena_cy + 2, "CHAMPIONSHIP", fontsize=13,
            fontweight="bold", ha="center", va="center", color=WHITE,
            zorder=7, path_effects=[pe.withStroke(linewidth=3, foreground=DARK_RED)])
    ax.text(arena_cx, arena_cy - 4, "CENTER MAT", fontsize=11,
            fontweight="bold", ha="center", va="center", color=WHITE,
            zorder=7, path_effects=[pe.withStroke(linewidth=3, foreground=DARK_RED)])
    ax.text(arena_cx, arena_cy - 10, "42ft Diameter", fontsize=8,
            ha="center", va="center", color=WHITE, fontstyle="italic",
            zorder=7, path_effects=[pe.withStroke(linewidth=2, foreground=DARK_RED)])

    # Practice mats
    practice_positions = [
        (arena_cx - CHAMP_MAT_R - STD_MAT_R - 4, arena_cy, "MAT 1"),
        (arena_cx + CHAMP_MAT_R + STD_MAT_R + 4, arena_cy, "MAT 2"),
        (arena_cx - STD_MAT_R - 2, arena_cy + CHAMP_MAT_R + STD_MAT_R + 4, "MAT 3"),
        (arena_cx + STD_MAT_R + 2, arena_cy + CHAMP_MAT_R + STD_MAT_R + 4, "MAT 4"),
    ]

    for (px, py, label) in practice_positions:
        border = Circle(
            (px, py), STD_MAT_R + 0.5,
            facecolor="none", edgecolor=WHITE, linewidth=2, zorder=5
        )
        ax.add_patch(border)

        mat = Circle(
            (px, py), STD_MAT_R,
            facecolor=MAT_GRAY, edgecolor=DARK_GRAY, linewidth=1.5,
            alpha=0.85, zorder=5
        )
        ax.add_patch(mat)

        # Inner wrestling circles
        for r in [12, 8, 4]:
            ic = Circle(
                (px, py), r,
                facecolor="none", edgecolor=WHITE, linewidth=1,
                alpha=0.4, linestyle="--", zorder=6
            )
            ax.add_patch(ic)

        ax.text(px, py, label, fontsize=9, fontweight="bold",
                ha="center", va="center", color=WHITE, zorder=7)
        ax.text(px, py - 5, "32ft Dia.", fontsize=6,
                ha="center", va="center", color=LIGHT_GRAY, zorder=7)

    # ========== BLEACHERS ==========
    bleacher_x_left = WALL_T + 1
    bleacher_x_right = BLDG_W - WALL_T - 13
    bleacher_y_start = ARENA_Y + 5
    bleacher_len = ARENA_H - 10

    # Left bleachers
    left_bleach = patches.Rectangle(
        (bleacher_x_left, bleacher_y_start), 12, bleacher_len,
        facecolor=RED, edgecolor=DARK_RED, linewidth=1.5, alpha=0.7, zorder=4
    )
    ax.add_patch(left_bleach)
    # Row lines
    for i in range(1, 8):
        row_x = bleacher_x_left + i * (12 / 8)
        ax.plot([row_x, row_x], [bleacher_y_start, bleacher_y_start + bleacher_len],
                color=DARK_RED, linewidth=0.5, alpha=0.5, zorder=5)
    ax.text(bleacher_x_left + 6, bleacher_y_start + bleacher_len / 2,
            "B\nL\nE\nA\nC\nH\nE\nR\nS", fontsize=8, fontweight="bold",
            ha="center", va="center", color=WHITE, zorder=6, linespacing=1.4)
    ax.text(bleacher_x_left + 6, bleacher_y_start + 8, "~400\nseats",
            fontsize=7, ha="center", va="center", color=WHITE, zorder=6)

    # Right bleachers
    right_bleach = patches.Rectangle(
        (bleacher_x_right, bleacher_y_start), 12, bleacher_len,
        facecolor=RED, edgecolor=DARK_RED, linewidth=1.5, alpha=0.7, zorder=4
    )
    ax.add_patch(right_bleach)
    for i in range(1, 8):
        row_x = bleacher_x_right + i * (12 / 8)
        ax.plot([row_x, row_x], [bleacher_y_start, bleacher_y_start + bleacher_len],
                color=DARK_RED, linewidth=0.5, alpha=0.5, zorder=5)
    ax.text(bleacher_x_right + 6, bleacher_y_start + bleacher_len / 2,
            "B\nL\nE\nA\nC\nH\nE\nR\nS", fontsize=8, fontweight="bold",
            ha="center", va="center", color=WHITE, zorder=6, linespacing=1.4)
    ax.text(bleacher_x_right + 6, bleacher_y_start + 8, "~400\nseats",
            fontsize=7, ha="center", va="center", color=WHITE, zorder=6)

    # ========== LOBBY LABEL ==========
    ax.text(BLDG_W / 2, LOBBY_H / 2, "ENTRANCE LOBBY",
            fontsize=14, fontweight="bold", ha="center", va="center",
            color=WHITE, zorder=15)
    ax.text(BLDG_W / 2, LOBBY_H / 2 - 5, "1,500 SF",
            fontsize=8, ha="center", va="center",
            color=LIGHT_GRAY, zorder=15)

    # ========== DIMENSIONS ==========
    # Overall width
    ax.annotate("", xy=(BLDG_W, -15), xytext=(0, -15),
                arrowprops=dict(arrowstyle="<->", color=STEEL_GRAY, lw=1.5))
    ax.text(BLDG_W / 2, -17, f"{BLDG_W} ft", fontsize=10,
            ha="center", va="center", color=STEEL_GRAY, fontweight="bold")

    # Overall depth
    ax.annotate("", xy=(-12, BLDG_D), xytext=(-12, 0),
                arrowprops=dict(arrowstyle="<->", color=STEEL_GRAY, lw=1.5))
    ax.text(-18, BLDG_D / 2, f"{BLDG_D} ft", fontsize=10,
            ha="center", va="center", color=STEEL_GRAY, fontweight="bold",
            rotation=90)

    # Zone depth dimensions (right side)
    dim_x = BLDG_W + 5
    # Lobby
    ax.annotate("", xy=(dim_x, LOBBY_H), xytext=(dim_x, 0),
                arrowprops=dict(arrowstyle="<->", color=STEEL_GRAY, lw=1))
    ax.text(dim_x + 3, LOBBY_H / 2, f"{LOBBY_H}'", fontsize=8,
            ha="left", va="center", color=STEEL_GRAY)
    # Support
    ax.annotate("", xy=(dim_x, ARENA_Y), xytext=(dim_x, LOBBY_H),
                arrowprops=dict(arrowstyle="<->", color=STEEL_GRAY, lw=1))
    ax.text(dim_x + 3, LOBBY_H + SUPPORT_H / 2, f"{SUPPORT_H}'", fontsize=8,
            ha="left", va="center", color=STEEL_GRAY)
    # Arena
    ax.annotate("", xy=(dim_x, BLDG_D), xytext=(dim_x, ARENA_Y),
                arrowprops=dict(arrowstyle="<->", color=STEEL_GRAY, lw=1))
    ax.text(dim_x + 3, ARENA_Y + ARENA_H / 2, f"{ARENA_H}'", fontsize=8,
            ha="left", va="center", color=STEEL_GRAY)

    # ========== TITLE BLOCK ==========
    title_y = BLDG_D + 8
    ax.text(BLDG_W / 2, title_y + 18, "HAZEL GREEN TROJANS",
            fontsize=28, fontweight="bold", ha="center", va="center",
            color=RED, zorder=20,
            path_effects=[pe.withStroke(linewidth=2, foreground=BLACK)])
    ax.text(BLDG_W / 2, title_y + 10, "SPORTS COMPLEX — PHASE 1",
            fontsize=18, fontweight="bold", ha="center", va="center",
            color=BLACK, zorder=20)
    ax.text(BLDG_W / 2, title_y + 4, "North Alabama Regional Athletic Complex",
            fontsize=11, ha="center", va="center",
            color=STEEL_GRAY, fontstyle="italic", zorder=20)
    ax.text(BLDG_W / 2, title_y, f"Building Footprint: {BLDG_W}' × {BLDG_D}'  |  ~30,000 SF  |  800 Seat Capacity",
            fontsize=9, ha="center", va="center",
            color=STEEL_GRAY, zorder=20)

    # Tagline
    ax.text(BLDG_W / 2, -25, '"Building Champions, One Mat at a Time"',
            fontsize=10, ha="center", va="center",
            color=RED, fontstyle="italic", zorder=20)

    # ========== NORTH ARROW ==========
    arrow_x = BLDG_W + 20
    arrow_y = BLDG_D / 2
    ax.annotate("N", xy=(arrow_x, arrow_y + 15), xytext=(arrow_x, arrow_y),
                fontsize=14, fontweight="bold", ha="center", va="center",
                color=BLACK,
                arrowprops=dict(arrowstyle="->", color=BLACK, lw=2))

    # ========== LEGEND ==========
    legend_x = -35
    legend_y = 20
    legend_items = [
        (RED, "Trojan Red (#CC0000)"),
        (BLACK, "Trojan Black (#1A1A1A)"),
        (MAT_GRAY, "Practice Mats"),
        (ARENA_FLOOR, "Arena Floor"),
        (LOBBY_FLOOR, "Lobby Floor"),
    ]
    ax.text(legend_x, legend_y + 15, "LEGEND", fontsize=9, fontweight="bold",
            color=BLACK, zorder=20)
    for i, (color, label) in enumerate(legend_items):
        ly = legend_y + 10 - i * 5
        box = patches.Rectangle((legend_x, ly - 1), 4, 3,
                                facecolor=color, edgecolor=BLACK, linewidth=0.5)
        ax.add_patch(box)
        ax.text(legend_x + 6, ly + 0.5, label, fontsize=7,
                va="center", color=STEEL_GRAY)

    # ========== AXIS SETUP ==========
    ax.set_xlim(-40, BLDG_W + 30)
    ax.set_ylim(-30, BLDG_D + 35)
    ax.set_aspect("equal")
    ax.axis("off")

    # ========== SAVE ==========
    out_path = "/home/user/TrojanHorseAreana/render_floorplan_2d.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight",
                facecolor=BG_COLOR, edgecolor="none")
    plt.close(fig)
    print(f"✓ Floor plan saved: {out_path}")
    return out_path


if __name__ == "__main__":
    draw_floorplan()
