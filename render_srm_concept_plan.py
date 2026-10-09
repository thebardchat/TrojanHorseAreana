#!/usr/bin/env python3
"""
Trojan Horse Arena — CONCEPT STUDY Level 1 plan: Set Rev D / P2-A-101 Rev J layout inside the radiused
SRM-language envelope, with the Summertown Metals pop-outs.

Rooms are drawn exactly as in params/phase2_plan_rev_i.yaml and clipped to the radiused outline (R 34 ft
ASSUMED). Rooms that touch a rounded corner are hatched: they lose area and need a redraw in a real
Plan Rev K. Nothing here is a Rev D change.
"""
import numpy as np
import yaml
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, PathPatch, Circle, Polygon
from matplotlib.path import Path
import render_revD_srm_concept as C

P = yaml.safe_load(open(r"blueprints\params\phase2_plan_rev_i.yaml", encoding="utf-8"))
RED, BLACK = "#CC0000", "#1A1A1A"
R = C.RING_R
ring = C.rrect(0, 0, 210, 252, R, n=14)
ring_path = Path(ring + [ring[0]])

fig, ax = plt.subplots(figsize=(11, 14), dpi=130)
fig.patch.set_facecolor("#F6F4EE")
ax.set_aspect("equal")
ax.set_xlim(-22, 285)
ax.set_ylim(-40, 298)
ax.axis("off")

outline = PathPatch(ring_path, fc="#EFEDE6", ec=BLACK, lw=3, zorder=1)
ax.add_patch(outline)


def clipped(p):
    p.set_clip_path(outline)
    ax.add_patch(p)


def room(rect, label, fc, fs=6.5, hatch=None, tag=None):
    x0, y0, x1, y1 = rect
    p = Rectangle((x0, y0), x1 - x0, y1 - y0, fc=fc, ec="#555", lw=0.7, hatch=hatch, zorder=2)
    clipped(p)
    if label:
        ax.text((x0 + x1) / 2, (y0 + y1) / 2, (f"{tag}  " if tag else "") + label, ha="center", va="center",
                fontsize=fs, color="#111", zorder=6, wrap=True)


def touches_corner(rect):
    """True when part of the room falls outside the radiused outline (it loses area)."""
    x0, y0, x1, y1 = rect
    xs, ys = np.linspace(x0 + 0.6, x1 - 0.6, 12), np.linspace(y0 + 0.6, y1 - 0.6, 12)
    return any(not ring_path.contains_point((x, y)) for x in xs for y in ys
               if -0.01 <= x <= 210.01 and -0.01 <= y <= 252.01)


# zones, then rooms (Rev I / Rev J layout)
for z in P["level_1"]["zones"]:
    room(z["rect"], "", "#E4E1D6")
for r in P["level_1"]["rooms"]:
    if r["id"] in ("storage_annex", "rr_mb", "rr_wb", "df_jan"):
        continue
    hatch = "////" if touches_corner(r["rect"]) else None
    room(r["rect"], "", "#D6D2C4", hatch=hatch)

# event floor, mats, tiers
ef = P["event_floor"]["rect"]
clipped(Rectangle((ef[0], ef[1]), ef[2] - ef[0], ef[3] - ef[1], fc="#D9BE8C", ec="#555", lw=0.8, zorder=3))
for mx, my in [(66, 145), (118, 145), (66, 93), (118, 93)]:
    clipped(Rectangle((mx, my), 42, 42, fc="#EAE0BC", ec="#777", lw=0.6, zorder=4))
    ax.add_patch(Circle((mx + 21, my + 21), 14, fc="#B22222", ec="white", lw=1, zorder=5))
for band in P["tiers"]["lower"]["bands"]:
    x0, y0, x1, y1 = band["rect"]
    clipped(Rectangle((x0, y0), x1 - x0, y1 - y0, fc="#C62828", ec="#7A1010", lw=0.5, zorder=3))
# room labels (short names only)
short = {"boys_locker": "BOYS LOCKER", "girls_locker": "GIRLS LOCKER", "rr_m1": "MEN", "rr_w1": "WOMEN",
         "vestibule": "VEST.", "concession": "CONC.", "evl_1": "EVL 1", "evl_2": "EVL 2", "evl_3": "EVL 3",
         "evl_4": "EVL 4", "mech_n": "MECH N", "mech_e": "MECH E", "mech_ne": "", "storage_sw": "FLEX / STORAGE",
         "equip_storage": "EQUIP", "first_aid": "", "mech_nw": "MECH", "equip_room": ""}
for r in P["level_1"]["rooms"]:
    t = short.get(r["id"])
    if t:
        x0, y0, x1, y1 = r["rect"]
        ax.text((x0 + x1) / 2, (y0 + y1) / 2, t, ha="center", va="center", fontsize=6, fontweight="bold", zorder=7,
                rotation=90 if (y1 - y0) > 2.2 * (x1 - x0) else 0)
lb = [z for z in P["level_1"]["zones"] if z["id"] == "lobby"][0]["rect"]
ax.text((lb[0] + lb[2]) / 2, 28, "LOBBY / HALL OF CHAMPIONS", ha="center", fontsize=7, fontweight="bold", zorder=7)
ax.text(116, 140, "EVENT FLOOR  120 x 144 ft", ha="center", fontsize=9, fontweight="bold", color="#222", zorder=7)
ax.text(122, 220, "LOWER TIER (telescopic)", ha="center", fontsize=6, color="white", zorder=7)

# Summertown Metals pop-outs (outside the radiused concrete shell)
for rect, lab in [([52, 252, 122, 282], "STORAGE ANNEX" + chr(10) + "70 x 30 ft · 2,100 SF"),
                  ([210, 161.09, 240, 217.09], "RESTROOM" + chr(10) + "POP-OUT" + chr(10) + "30 x 56")]:
    x0, y0, x1, y1 = rect
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc="#3E444B", ec=BLACK, lw=2, zorder=8))
    ax.text((x0 + x1) / 2, (y0 + y1) / 2, lab, ha="center", va="center", color="white", fontsize=6.5,
            fontweight="bold", zorder=9, rotation=90 if (y1 - y0) > (x1 - x0) else 0)
ax.text(87, 290, "SUMMERTOWN METALS building", ha="center", fontsize=7.5, color=RED, fontweight="bold")
ax.text(264, 189, "SUMMERTOWN" + chr(10) + "METALS", ha="center", va="center", fontsize=7.5, color=RED, fontweight="bold")

# cylindrical NE stair tower (ASSUMED) over the old rectangle
ax.add_patch(Circle((190, 244), 12.3, fc="#B8B29E", ec=BLACK, lw=1.5, zorder=8))
ax.text(190, 244, "ST-2", ha="center", va="center", fontsize=6, fontweight="bold", zorder=9)

# portal + walk (south)
ax.add_patch(Rectangle((99, -30), 28, 30, fc="#A9553C", ec="#555", lw=0.6, zorder=2))
ax.add_patch(Rectangle((93, -30), 6, 30, fc="#D9B79A", ec="#555", lw=0.6, zorder=2))
ax.add_patch(Rectangle((127, -30), 6, 30, fc="#D9B79A", ec="#555", lw=0.6, zorder=2))
ax.text(113, -33, "CHAMPION WALK 40 ft · PORTAL", ha="center", fontsize=7, fontweight="bold")

# title + notes
fig.text(0.5, 0.965, "LEVEL 1 — SRM-LANGUAGE ENVELOPE OVER REV J LAYOUT", ha="center", fontsize=17, fontweight="bold", color=RED)
fig.text(0.5, 0.945, "Concept study (D-074): radiused 34 ft corners; Rev J rooms unchanged; hatched rooms touch a rounded corner and need a redraw",
         ha="center", fontsize=8.5, color="#333")
ax.annotate("N", (240, 40), (240, 15), ha="center", fontsize=12, fontweight="bold", arrowprops=dict(arrowstyle="-|>", lw=2))
lost = 4 * (1 - np.pi / 4) * R ** 2
fig.text(0.5, 0.045, f"Rounding the four corners removes about {lost:,.0f} SF per level from the 210 x 252 ft footprint (Rev J L1 56,861 SF incl. annex + bump-out).",
         ha="center", fontsize=8.5, fontweight="bold")
fig.text(0.5, 0.025, "PRELIMINARY — CONCEPTUAL DESIGN — NOT FOR CONSTRUCTION  |  Not a Rev D change  |  Radius, tower and pop-out roofs ASSUMED  |  Site TBD (D-006)",
         ha="center", fontsize=8, fontweight="bold")
fig.text(0.5, 0.008, "Layout: params/phase2_plan_rev_i.yaml (P2-A-101 Rev J). SRM / Summertown names are descriptive only; no logos or marks used.",
         ha="center", fontsize=7, color="#555")
fig.savefig("concepts/render_srm_concept_plan.png", facecolor=fig.get_facecolor())
print("wrote render_srm_concept_plan.png")
