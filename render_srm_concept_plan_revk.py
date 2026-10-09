#!/usr/bin/env python3
"""
Trojan Horse Arena — PLAN REV K STUDY (concept, not an issued sheet): Level 1 of Set Rev D / P2-A-101 Rev J
inside the radiused SRM-language envelope, corners resolved.

Method: measure what each corner radius removes from every Rev J element (rooms, the four stairs, L2 loop),
then resolve the recommended radius (R = 20 ft, ASSUMED) with the smallest moves:
  - ST-3 (SE) slides west along the south wall into CONCOURSE (E), turned E-W (same 305 SF footprint)
  - ST-4 (SW) slides north along the west wall into the FLEX / TEAM ASSEMBLY zone (unprogrammed)
  - ST-2 (NE) stays a cylindrical tower at the corner (as the concept renders)
  - MECH (NW) / MECH (NE) corner losses (110 SF at R 20) plus the open MEP shortfall are made up in a new
    30 x 30 ft (900 SF) mech / electrical bay next to the storage annex, a second metal-building pop-out
Nothing here is a Rev D change; all positions are ASSUMED until a plan revision is drawn.
"""
import os
import numpy as np
import yaml
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, PathPatch, Circle
from matplotlib.path import Path
import render_revD_srm_concept as C

P = yaml.safe_load(open(os.path.join("blueprints", "params", "phase2_plan_rev_i.yaml"), encoding="utf-8"))
RED, BLACK = "#CC0000", "#1A1A1A"
R_REC = 20.0
NL = chr(10)


def ring_path(R):
    ring = C.rrect(0, 0, 210, 252, R, n=40)
    return Path(ring + [ring[0]]), ring


def lost(rect, rp, step=0.25):
    x0, y0, x1, y1 = rect
    X, Y = np.meshgrid(np.arange(x0 + step / 2, x1, step), np.arange(y0 + step / 2, y1, step))
    return (~rp.contains_points(np.c_[X.ravel(), Y.ravel()])).sum() * step * step


rooms = {r["id"]: r for r in P["level_1"]["rooms"]}
stairs = {s["id"]: s for s in P["vertical"]["stairs"]}

# ---- loss table across radii (rooms / stairs / loop) ----
table = []
for R in (14, 20, 26, 34):
    rp, _ = ring_path(R)
    room_loss = sum(lost(r["rect"], rp) for k, r in rooms.items()
                    if k not in ("storage_annex", "rr_mb", "rr_wb", "df_jan"))
    st_loss = [lost(stairs[k]["rect"], rp) for k in ("ST-3", "ST-4")]
    loop = lost([196, 239, 210, 246], rp)
    table.append((R, 4 * (1 - np.pi / 4) * R * R, room_loss, st_loss[0], loop))

# ---- drawing ----
rp, ring = ring_path(R_REC)
fig, ax = plt.subplots(figsize=(13, 14.5), dpi=130)
fig.patch.set_facecolor("#F6F4EE")
ax.set_aspect("equal")
ax.set_xlim(-24, 300)
ax.set_ylim(-42, 300)
ax.axis("off")
outline = PathPatch(rp, fc="#EFEDE6", ec=BLACK, lw=3, zorder=1)
ax.add_patch(outline)


def clipped(p):
    p.set_clip_path(outline)
    ax.add_patch(p)


def room(rect, fc, hatch=None, z=2, ec="#555", lw=0.7):
    x0, y0, x1, y1 = rect
    clipped(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=fc, ec=ec, lw=lw, hatch=hatch, zorder=z))


for z in P["level_1"]["zones"]:
    room(z["rect"], "#E4E1D6")
SKIP = ("storage_annex", "rr_mb", "rr_wb", "df_jan")
for k, r in rooms.items():
    if k in SKIP:
        continue
    room(r["rect"], "#D6D2C4", hatch="////" if lost(r["rect"], rp) > 1.0 else None)

ef = P["event_floor"]["rect"]
clipped(Rectangle((ef[0], ef[1]), ef[2] - ef[0], ef[3] - ef[1], fc="#D9BE8C", ec="#555", lw=0.8, zorder=3))
for mx, my in [(66, 145), (118, 145), (66, 93), (118, 93)]:
    clipped(Rectangle((mx, my), 42, 42, fc="#EAE0BC", ec="#777", lw=0.6, zorder=4))
    ax.add_patch(Circle((mx + 21, my + 21), 14, fc="#B22222", ec="white", lw=1, zorder=5))
for band in P["tiers"]["lower"]["bands"]:
    x0, y0, x1, y1 = band["rect"]
    clipped(Rectangle((x0, y0), x1 - x0, y1 - y0, fc="#C62828", ec="#7A1010", lw=0.5, zorder=3))

short = {"boys_locker": "BOYS LOCKER", "girls_locker": "GIRLS LOCKER", "rr_m1": "MEN", "rr_w1": "WOMEN", "vestibule": "VEST.",
         "concession": "CONC.", "evl_1": "EVL 1", "evl_2": "EVL 2", "evl_3": "EVL 3", "evl_4": "EVL 4", "mech_n": "MECH N",
         "mech_e": "MECH E", "storage_sw": "FLEX / STORAGE", "equip_storage": "EQUIP", "mech_nw": "MECH", "mech_ne": "MECH"}
for k, t in short.items():
    x0, y0, x1, y1 = rooms[k]["rect"]
    ax.text((x0 + x1) / 2, (y0 + y1) / 2, t, ha="center", va="center", fontsize=6, fontweight="bold", zorder=7,
            rotation=90 if (y1 - y0) > 2.2 * (x1 - x0) else 0)
lb = [z for z in P["level_1"]["zones"] if z["id"] == "lobby"][0]["rect"]
ax.text((lb[0] + lb[2]) / 2, 28, "LOBBY / HALL OF CHAMPIONS", ha="center", fontsize=7, fontweight="bold", zorder=7)
ax.text(116, 140, "EVENT FLOOR  120 x 144 ft", ha="center", fontsize=9, fontweight="bold", color="#222", zorder=7)
ax.text(34, 48, "FLEX / TEAM ASSEMBLY", ha="center", fontsize=6.5, color="#333", zorder=7)

# stairs: ghosts at Rev J positions, new positions solid
STAIR_FC = "#B8B29E"
for sid, new in [("ST-3", [165.917, 0, 190, 12.667]), ("ST-4", [0, 20, 12.667, 44.083])]:
    gx0, gy0, gx1, gy1 = stairs[sid]["rect"]
    ax.add_patch(Rectangle((gx0, gy0), gx1 - gx0, gy1 - gy0, fc="none", ec=RED, lw=1.2, ls="--", zorder=8))
    x0, y0, x1, y1 = new
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=STAIR_FC, ec=BLACK, lw=1.6, zorder=9))
    ax.text((x0 + x1) / 2, (y0 + y1) / 2, sid + NL + "moved", ha="center", va="center", fontsize=6, fontweight="bold", zorder=10)
ax.add_patch(Rectangle((36.333, 227.917), 12.667, 24.083, fc=STAIR_FC, ec=BLACK, lw=1.2, zorder=9))
ax.text(42.7, 240, "ST-1", ha="center", va="center", fontsize=6, fontweight="bold", zorder=10)
ax.add_patch(Circle((192, 262), 10.0, fc=STAIR_FC, ec=BLACK, lw=1.6, zorder=9))
ax.text(192, 262, "ST-2", ha="center", va="center", fontsize=6, fontweight="bold", zorder=10)

# metal pop-outs: storage annex (D-067), restroom core 2 (D-069/D-072), NEW mech bay
for rect, lab, fc in [([52, 252, 122, 282], "STORAGE ANNEX" + NL + "70 x 30 · 2,100 SF", "#3E444B"),
                      ([122, 252, 152, 282], "MECH / ELEC BAY" + NL + "30 x 30 · +900 SF" + NL + "(NEW, study)", "#6A2020"),
                      ([210, 161.09, 240, 217.09], "RESTROOM" + NL + "POP-OUT" + NL + "30 x 56", "#3E444B")]:
    x0, y0, x1, y1 = rect
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=fc, ec=BLACK, lw=2, zorder=8))
    ax.text((x0 + x1) / 2, (y0 + y1) / 2, lab, ha="center", va="center", color="white", fontsize=6.3, fontweight="bold",
            zorder=9, rotation=90 if (y1 - y0) > (x1 - x0) else 0)
ax.text(102, 290, "METAL-BUILDING POP-OUTS (proposed)", ha="center", fontsize=7.5, color=RED, fontweight="bold")

# portal + walk
ax.add_patch(Rectangle((99, -30), 28, 30, fc="#A9553C", ec="#555", lw=0.6, zorder=2))
ax.add_patch(Rectangle((93, -30), 6, 30, fc="#D9B79A", ec="#555", lw=0.6, zorder=2))
ax.add_patch(Rectangle((127, -30), 6, 30, fc="#D9B79A", ec="#555", lw=0.6, zorder=2))
ax.text(113, -34, "CHAMPION WALK 40 ft · PORTAL", ha="center", fontsize=7, fontweight="bold")

# loss table inset (right side)
tx, ty = 252, 238
ax.text(tx - 6, ty + 18, "WHAT EACH CORNER RADIUS COSTS", fontsize=7.5, fontweight="bold", ha="left")
ax.text(tx - 6, ty + 10, "SF per level (Rev J elements)", fontsize=6.3, color="#555", ha="left")
hdr = ["R", "corners", "rooms", "each corner stair"]
xs = [tx - 6, tx + 8, tx + 24, tx + 42]
for x, h in zip(xs, hdr):
    ax.text(x, ty, h, fontsize=6.2, fontweight="bold", ha="left")
for i, (R, cut, rl, sl, lp) in enumerate(table):
    y = ty - 9 * (i + 1)
    rec = R == R_REC
    if rec:
        ax.add_patch(Rectangle((tx - 8, y - 3), 74, 8, fc="#FFF3B0", ec="none", zorder=0))
    for x, v in zip(xs, [f"{R} ft", f"-{cut:,.0f}", f"-{rl:,.0f}", f"-{sl:,.0f} of 305"]):
        ax.text(x, y, v, fontsize=6.5, ha="left", fontweight="bold" if rec else "normal")
ax.text(tx - 6, ty - 50, "Recommended: R = 20 ft", fontsize=7.2, fontweight="bold", color=RED)
ax.text(tx - 6, ty - 58, "Stairs ST-3 / ST-4 slide along their" + NL + "walls (dashed red = Rev J position)." + NL +
        "Hatched rooms lose area; mech made" + NL + "up in the new 900 SF metal bay.", fontsize=6.3, va="top")

fig.text(0.5, 0.968, "LEVEL 1 — PLAN REV K STUDY (R = 20 ft)", ha="center", fontsize=17, fontweight="bold", color=RED)
fig.text(0.5, 0.947, "Rev J layout in the radiused envelope with the corner stairs and mech resolved (concept study, D-077)",
         ha="center", fontsize=8.5, color="#333")
rl20 = [t for t in table if t[0] == 20][0]
fig.text(0.5, 0.052, f"At R = 20 ft the corners remove about {rl20[1]:,.0f} SF per level (R = 34 ft: {table[3][1]:,.0f}). Rooms lose {rl20[2]:,.0f} SF, mostly the two corner mech rooms.",
         ha="center", fontsize=8.2, fontweight="bold")
fig.text(0.5, 0.037, "The two corner stairs relocate instead of shrinking; ST-2 is a cylindrical tower outside the NE corner; the new mech bay adds 900 SF.",
         ha="center", fontsize=8.2, fontweight="bold")
fig.text(0.5, 0.024, "PRELIMINARY — CONCEPTUAL DESIGN — NOT FOR CONSTRUCTION  |  Study, not an issued sheet or a Rev D change  |  "
         "Radius, stair moves and mech bay ASSUMED  |  Site TBD (D-006)", ha="center", fontsize=8, fontweight="bold")
fig.text(0.5, 0.008, "Layout: params/phase2_plan_rev_i.yaml (P2-A-101 Rev J). Company names are descriptive only; no logos or marks used.",
         ha="center", fontsize=7, color="#555")
os.makedirs("concepts", exist_ok=True)
fig.savefig("concepts/render_srm_concept_plan_revk_study.png", facecolor=fig.get_facecolor())
print("wrote concepts/render_srm_concept_plan_revk_study.png")
for t in table:
    print("R=%d corners -%.0f rooms -%.0f stair -%.0f loopNE -%.0f" % (t[0], t[1], t[2], t[3], t[4]))
