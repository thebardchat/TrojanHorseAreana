"""P2-A-101 (Level 1) / P2-A-102 (Level 2) — Phase 2 OVERALL FLOOR PLANS, SCHEMATIC BLOCK PLANS (P2-T-004).

Tabloid 17 x 11 landscape, plan drawn to scale 1/32 in = 1 ft-0 in (printed at 100%), vector PDF + DXF.
Geometry: params/phase2_plan.yaml (KEYSTONE block layout, ASSUMED). Program SF: p2_testfit.compute_locked
(P2-G-003 Rev D, D-030). Locked values: params/phase2.yaml. Fixed seating = solid tiers; telescopic = dashed
overlay (seating type OPEN, D-009). DXF is in paper inches (1 in = 32 ft).

Run from the repo root:
  /workspace/.venv-keystone/bin/python blueprints/phase2/src/p2_a_plan.py --sheet P2-A-101|P2-A-102 [--rev A|B|C|D] [--png PATH] [--out-dir DIR] [--force]
Rev A (FROZEN, build()): params/phase2_plan.yaml. Rev B (FROZEN, build_b()): params/phase2_plan_rev_b.yaml, MIX seating (D-009),
entry south-center on the arena N-S axis, restrooms flank the lobby, mech off the west side (Shane 2026-10-04 4:30 AM CT).
Rev C (FROZEN, build_c()): params/phase2_plan_rev_c.yaml, single controlled entry (D-033, Shane 4:43 AM CT): security
checkpoint, controlled door to the athlete route, EXIT ONLY perimeter doors (IBC 2021 1010.2), service door (D-034 OPEN).
Rev D (FROZEN 2026-10-04, approved by Shane 5:27 AM CT, part of Phase 2 Schematic Set Rev A, built by p2_set.py; FLEX labels D-039
are a label-only re-issue before the freeze) (build_d()): params/phase2_plan_rev_d.yaml, continuous Level 2 running / training loop (D-035, Shane 4:55 AM CT);
S&C + cross-training trimmed 7 ft; ST-1, ST-2 (NE stair tower) and the elevator moved clear; program = P2-G-003 Rev F.
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
from titleblock import Sheet, add_titleblock, pitch, text_width_in  # noqa: E402
import p2_testfit as tf  # noqa: E402

W, H, M = 17.0, 11.0, 0.5
TB = "A-ANNO-TABL"
L_WALL, L_ROOM, L_TAG, L_MAT, L_CORT = "A-WALL-BLDG", "A-AREA-BLCK", "A-AREA-IDEN", "A-FLOR-MATS", "A-FLOR-CORT"
L_FIX, L_TEL, L_VERT, L_DIM, L_HID = "A-SEAT-FIXD", "A-SEAT-TELE", "A-FLOR-STRS", "A-ANNO-DIMS", "A-AREA-OPEN"
L_LOOP, L_GRD = "A-FLOR-TRAK", "A-FLOR-GRDR"   # Rev D: Level 2 running / training loop, guards
LEVEL_OF = {"P2-A-101": 1, "P2-A-102": 2}


def n(x):
    return f"{round(x):,}"


def area(r):
    return (r[2] - r[0]) * (r[3] - r[1])


def tel_depth(seats, sps, a, b):
    """Depth d of a 3-sided band (two arms of length a+d, one side of length b) holding seats x sps SF."""
    A = seats * sps
    return (-(2 * a + b) + math.sqrt((2 * a + b) ** 2 + 8 * A)) / 4


class Plan:
    def __init__(self, sh, x0, y0, s):
        self.sh, self.x0, self.y0, self.s = sh, x0, y0, s

    def P(self, x, y):
        return self.x0 + x * self.s, self.y0 + y * self.s

    def rect(self, r, layer, lw=0.8):
        x, y = self.P(r[0], r[1])
        self.sh.rect(x, y, (r[2] - r[0]) * self.s, (r[3] - r[1]) * self.s, layer=layer, lw=lw)

    def line(self, x1, y1, x2, y2, layer, lw=0.6):
        a, b = self.P(x1, y1)
        c, d = self.P(x2, y2)
        self.sh.line(a, b, c, d, layer=layer, lw=lw)

    def dashed(self, x1, y1, x2, y2, layer, lw=0.6, dash=0.08, gap=0.05):
        a, b = self.P(x1, y1)
        c, d = self.P(x2, y2)
        self.sh.dashed(a, b, c, d, layer=layer, lw=lw, dash=dash, gap=gap)

    def drect(self, r, layer, lw=0.6, dash=0.08, gap=0.05):
        x0, y0, x1, y1 = r
        for a in ((x0, y0, x1, y0), (x1, y0, x1, y1), (x1, y1, x0, y1), (x0, y1, x0, y0)):
            self.dashed(*a, layer=layer, lw=lw, dash=dash, gap=gap)

    def tag(self, r, lines, sizes=(7.0, 6.5, 6.0, 5.5, 5.0), fallback=None, bold_first=True, allow_rot=True):
        """Centered multi-line label inside rect r (feet). Tries sizes, then rotated, then fallback lines. Returns True if placed."""
        w, h = (r[2] - r[0]) * self.s, (r[3] - r[1]) * self.s
        cx, cy = self.P((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)
        for cand in (lines, fallback) if fallback else (lines,):
            for rot in ((0, 90) if allow_rot else (0,)):
                bw, bh = (w, h) if rot == 0 else (h, w)
                for sz in sizes:
                    p = pitch(sz)
                    tw = max(text_width_in(t, sz, bold_first and i == 0) for i, t in enumerate(cand))
                    th = p * len(cand)
                    if tw <= bw - 0.07 and th <= bh - 0.04:
                        for i, t in enumerate(cand):
                            off = th / 2 - p * (i + 1) + p * 0.28
                            if rot == 0:
                                self.sh.text(cx, cy + off, t, size=sz, bold=bold_first and i == 0, align="center", layer=L_TAG)
                            else:
                                self.sh.text(cx - off, cy, t, size=sz, bold=bold_first and i == 0, align="center", layer=L_TAG, rot=90)
                        return True
        return False


def tier_labels(sh, pl, bands, word, inner):
    """Label each band in its outer 30% (beyond the telescopic dashed line). bands = N, S, E."""
    for b, side, sd in zip(bands, ("N", "S", "E"), inner):
        if side == "N":
            y_ = b[1] + 0.78 * (b[3] - b[1])
            x_, yy = pl.P(b[0] + 3, y_)
            sh.text(x_, yy - 0.035, f"{word} TIER ({side}) · FIXED", size=5.4, bold=True, layer=L_TAG)
        elif side == "S":
            y_ = b[1] + 0.22 * (b[3] - b[1])
            x_, yy = pl.P(b[0] + 3, y_)
            sh.text(x_, yy - 0.035, f"{word} TIER ({side}) · FIXED", size=5.4, bold=True, layer=L_TAG)
        else:
            x_ = b[0] + 0.78 * (b[2] - b[0])
            xx, y_ = pl.P(x_, (b[1] + b[3]) / 2 - 20)
            sh.text(xx + 0.035, y_, f"{word} TIER ({side}) · FIXED", size=5.4, bold=True, align="center", layer=L_TAG, rot=90)


def load_all():
    p2, prog = tf.load()
    plan = yaml.safe_load((BP / "params" / "phase2_plan.yaml").read_text(encoding="utf-8"))
    F_ = tf.compute_locked(p2, prog, "base")
    T_ = tf.compute_locked(p2, prog, "telescopic")
    return p2, prog, plan, F_, T_


def prog_sf(F_, key, share):
    if key == "mechanical":
        return F_["M"] * share
    return F_["sf"][key] * share


def fixture_lines(F_, key):
    f = F_["fx1"] if key.endswith("1") else F_["fx2"]
    if key.startswith("men"):
        return f["wc_m"], f["lav_m"], f["urinals_max"]
    return f["wc_f"], f["lav_f"], None


def build(sheet_no, p2, prog, plan, F_, T_):
    lvl = LEVEL_OF[sheet_no]
    meta2 = p2["meta"]
    sm = p2["sheets"][sheet_no]
    rv_letter = "A"                              # Rev A is FROZEN; Rev B is build_b()
    pm = plan["meta"]
    sh = Sheet(W, H)
    body_bottom = add_titleblock(sh, {
        "project": f"{meta2['project']}\n{meta2['arena_name']} · {meta2['location']}",
        "phase": "PHASE 2",
        "title": f"OVERALL FLOOR PLAN\nLEVEL {lvl} · BLOCK PLAN",
        "scale": "1/32\" = 1'-0\"",
        "date": meta2["sheet_date"],
        "revision": rv_letter,
        "drawn_by": meta2["drawn_by"],
        "sheet_no": sheet_no,
        "stamp": meta2["stamp"],
    }, margin=M, tb_h=0.95, stamp_h=0.40)
    top = H - M - 0.12
    s = 1.0 / pm["scale_ft_per_in"]
    bx0, by0, bx1, by1 = plan["building"]["rect"]
    px0, py0 = M + 0.62, body_bottom + 0.78
    pl = Plan(sh, px0, py0, s)
    floor = plan["event_floor"]["rect"]
    av = plan["arena_volume"]["rect"]
    lv = plan["level_1"] if lvl == 1 else plan["level_2"]
    sched = []                                  # (tag, name, drawn, program, note)

    # ---- title over the plan
    sh.text(px0, top - 0.22, f"LEVEL {lvl} — OVERALL FLOOR PLAN", size=14, bold=True)
    sh.text(px0, top - 0.48, f"{pm['label']} · scale 1/32\" = 1'-0\" on 17 x 11 in · north approximate, site TBD", size=8.5)

    # ---- building outline + overall dimensions
    pl.rect(plan["building"]["rect"], L_WALL, lw=2.2)
    yd = by0 - 9
    pl.line(bx0, yd, bx1, yd, L_DIM, lw=0.4)
    for xx in (bx0, bx1):
        pl.line(xx, yd - 2.5, xx, yd + 2.5, L_DIM, lw=0.4)
    tx, ty = pl.P((bx0 + bx1) / 2, yd)
    sh.text(tx, ty - 0.14, f"{bx1 - bx0:g}'-0\"  (building {bx1 - bx0:g} x {by1 - by0:g} ft = {n(area(plan['building']['rect']))} SF footprint)", size=7, align="center", layer=L_DIM)
    xd = bx0 - 9
    pl.line(xd, by0, xd, by1, L_DIM, lw=0.4)
    for yy in (by0, by1):
        pl.line(xd - 2.5, yy, xd + 2.5, yy, L_DIM, lw=0.4)
    tx, ty = pl.P(xd, (by0 + by1) / 2)
    sh.text(tx - 0.06, ty, f"{by1 - by0:g}'-0\"", size=7, align="center", layer=L_DIM, rot=90)

    sps_f, sps_t = F_["seat_sf"], T_["seat_sf"]
    if lvl == 1:
        # ---- arena volume, floor, lower tier (fixed solid) + telescopic overlay (dashed)
        pl.rect(av, L_FIX, lw=0.9)
        pl.rect(floor, L_MAT, lw=1.4)
        fx0, fy0, fx1, fy1 = floor
        ax0, ay0, ax1, ay1 = av
        bands = [(ax0, fy1, ax1, ay1), (ax0, ay0, ax1, fy0), (fx1, fy0, ax1, fy1)]
        pl.line(fx1, fy0, ax1, fy0, L_FIX, lw=0.6); pl.line(fx1, fy1, ax1, fy1, L_FIX, lw=0.6)
        pl.line(fx1, fy0, fx1, fy1, L_FIX, lw=0.6)
        d_t = tel_depth(F_["sl"], sps_t, fx1 - fx0, fy1 - fy0)
        pl.dashed(fx0, fy1 + d_t, fx1 + d_t, fy1 + d_t, L_TEL, lw=0.9)
        pl.dashed(fx1 + d_t, fy1 + d_t, fx1 + d_t, fy0 - d_t, L_TEL, lw=0.9)
        pl.dashed(fx1 + d_t, fy0 - d_t, fx0, fy0 - d_t, L_TEL, lw=0.9)
        lower_fixed = sum(area(b) for b in bands)
        # tier labels
        tier_labels(sh, pl, bands, "LOWER", inner=("S", "N", "W"))
        # mats + court
        mft = p2["spaces"]["arena"]["mat_ft"]
        for m in plan["mats"]:
            mx, my = m["origin"]
            pl.rect((mx, my, mx + mft, my + mft), L_MAT, lw=1.0)
            left = mx + mft / 2 < (floor[0] + floor[2]) / 2
            x_, y_ = pl.P(mx + 2 if left else mx + mft - 2, my + mft - 2.5)
            sh.text(x_, y_ - 0.09, m["id"], size=6.2, bold=True, align="left" if left else "right", layer=L_TAG)
        cr = plan["court"]["rect"]
        ro = plan["court"]["runout_ft"]
        pl.drect(cr, L_CORT, lw=0.7, dash=0.07, gap=0.04)
        pl.drect((cr[0] - ro, cr[1] - ro, cr[2] + ro, cr[3] + ro), L_CORT, lw=0.35, dash=0.03, gap=0.04)
        pl.dashed(cr[0], (cr[1] + cr[3]) / 2, cr[2], (cr[1] + cr[3]) / 2, L_CORT, lw=0.4, dash=0.07, gap=0.04)
        x_, y_ = pl.P((fx0 + fx1) / 2, fy1 - 6)
        sh.text(x_, y_, f"EVENT FLOOR {fx1 - fx0:g}' x {fy1 - fy0:g}' = {n(area(floor))} SF", size=6.6, bold=True, align="center", layer=L_TAG)
        sh.text(x_, y_ - 0.12, "table / bench zone (15')", size=5.4, align="center", layer=L_TAG)
        x_, y_ = pl.P((fx0 + fx1) / 2, fy0 + 7.5)
        sh.text(x_, y_, "table / bench zone (15')", size=5.4, align="center", layer=L_TAG)
        x_, y_ = pl.P((cr[0] + cr[2]) / 2, (cr[1] + cr[3]) / 2 + 2.5)
        sh.text(x_, y_, "COURT 84' x 50' (OVERLAY)", size=5.4, align="center", layer=L_TAG)
        sched.append(("—", "Event floor (D-030 locked)", area(floor), F_["sf"]["arena"], "114' x 144'"))
        sched.append(("—", f"Lower tier, fixed (~{n(F_['sl'])} seats)", lower_fixed, F_["sf"]["seating_lower"], f"telescopic line {d_t:.1f}' deep"))
        # voms
        for v in lv["voms"]:
            pl.drect(v["rect"], L_ROOM, lw=0.5, dash=0.04, gap=0.03)
            x_, y_ = pl.P((v["rect"][0] + v["rect"][2]) / 2, (v["rect"][1] + v["rect"][3]) / 2)
            sh.text(x_, y_ - 0.03, v["id"], size=5.2, bold=True, align="center", layer=L_TAG)
        # spine separation (public concourse / athlete corridor)
        pl.dashed(81.5, 134, 101.5, 134, L_ROOM, lw=0.7, dash=0.05, gap=0.03)
        # entry arrow
        fr = next(r for r in lv["rooms"] if r["id"] == "foyer")["rect"]
        ex = (fr[0] + fr[2]) / 2
        pl.line(ex, -6, ex, 0, L_DIM, lw=1.0)
        pl.line(ex, 0, ex - 1.8, -2.6, L_DIM, lw=1.0); pl.line(ex, 0, ex + 1.8, -2.6, L_DIM, lw=1.0)
        x_, y_ = pl.P(ex - 3, -5.2)
        sh.text(x_, y_, "MAIN ENTRY", size=6.4, bold=True, align="right", layer=L_TAG)
    else:
        # ---- level 2: open-to-below areas, upper tier (fixed solid) + telescopic overlay (dashed)
        for ob in lv["open_below"]:
            r = ob["rect"]
            pl.rect(r, L_HID, lw=0.5)
            for (xa, ya, xb, yb) in ((r[0], r[1], r[2], r[3]), (r[0], r[3], r[2], r[1])):   # X with a gap for the label
                for t0, t1 in ((0.0, 0.36), (0.64, 1.0)):
                    pl.dashed(xa + (xb - xa) * t0, ya + (yb - ya) * t0, xa + (xb - xa) * t1, ya + (yb - ya) * t1, L_HID, lw=0.25, dash=0.06, gap=0.06)
        pl.drect(floor, L_HID, lw=0.4, dash=0.05, gap=0.05)
        ax0, ay0, ax1, ay1 = av
        ud = plan["tiers"]["upper_depth_ft"]
        bands = [(ax0, ay1, ax1, ay1 + ud), (ax0, ay0 - ud, ax1, ay0), (ax1, ay0, ax1 + ud, ay1)]
        for b in bands:
            pl.rect(b, L_FIX, lw=0.9)
        d_t = F_["su"] * sps_t / (2 * (ax1 - ax0) + (ay1 - ay0))   # bands do not wrap the NE/SE corners on L2
        pl.dashed(ax0, ay1 + d_t, ax1, ay1 + d_t, L_TEL, lw=0.9)
        pl.dashed(ax1 + d_t, ay1, ax1 + d_t, ay0, L_TEL, lw=0.9)
        pl.dashed(ax1, ay0 - d_t, ax0, ay0 - d_t, L_TEL, lw=0.9)
        upper_fixed = sum(area(b) for b in bands)
        tier_labels(sh, pl, bands, "UPPER", inner=("S", "N", "W"))
        oba = next(o for o in lv["open_below"] if o["id"] == "ob_arena")["rect"]
        x_, y_ = pl.P((oba[0] + oba[2]) / 2, (oba[1] + oba[3]) / 2)
        sh.text(x_, y_ + 0.05, "OPEN TO ARENA BELOW", size=8, bold=True, align="center", layer=L_TAG)
        sh.text(x_, y_ - 0.10, "(event floor + lower tier, double height)", size=6, align="center", layer=L_TAG)
        obl = next(o for o in lv["open_below"] if o["id"] == "ob_lobby")["rect"]
        pl.tag(obl, ["OPEN TO LOBBY BELOW", "(hall of champions,", "double height)"], sizes=(6.4, 6.0, 5.5), bold_first=True, allow_rot=False)
        sched.append(("—", f"Upper tier, fixed (~{n(F_['su'])} seats)", upper_fixed, F_["sf"]["seating_upper"], f"telescopic line {d_t:.1f}' deep"))

    # ---- rooms
    for r in lv["rooms"]:
        pl.rect(r["rect"], L_ROOM, lw=0.9)
        a_ = area(r["rect"])
        ps = prog_sf(F_, r["prog"], r["share"])
        if "fixtures" in r:
            wc_, lav_, _ = fixture_lines(F_, r["fixtures"])
            ps = (wc_ + lav_) * prog["factors"]["restrooms"]["sf_per_fixture"]
        extra = []
        note = r.get("note", "")
        if "fixtures" in r:
            wc, lav, ur = fixture_lines(F_, r["fixtures"])
            extra = [f"WC {wc} · LAV {lav}"]
            note = f"{wc + lav} fixtures (WC {wc}, LAV {lav}" + (f"; urinals ≤ {ur} of the WCs)" if ur is not None else ")")
        if r["id"] in ("sc", "xt"):
            note = "Level 2 over the lockers (D-030)" if r["id"] == "sc" else "Level 2 over girls locker + mech (D-030)"
        full = [f"{r['tag']}  {r['name']}", f"{n(a_)} SF"] + extra
        short = [r["tag"]]
        if not pl.tag(r["rect"], full, fallback=[f"{r['tag']}", f"{n(a_)}"]):
            pl.tag(r["rect"], short, sizes=(5.5, 5.0, 4.5))
        sched.append((r["tag"], r["name"].title().replace("(Se)", "(SE)").replace("Mat", "Mat Area"), a_, ps, note))
    # ---- zones (circulation, label only)
    for z in lv["zones"]:
        lines = [z["name"]]
        if z.get("vertical"):
            r = z["rect"]
            x_, y_ = pl.P((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)
            sz = 6.2
            while text_width_in(z["name"], sz, True) > (r[3] - r[1]) * s - 0.1 and sz > 4.5:
                sz -= 0.3
            sh.text(x_ + 0.03, y_, z["name"], size=sz, bold=True, align="center", layer=L_TAG, rot=90)
        else:
            pl.tag(z.get("label_rect", z["rect"]), z["name"].replace(" / ", " /|").split("|"), sizes=(6.4, 6.0, 5.5, 5.0), allow_rot=False)
    # ---- stairs + elevator (same rectangles both levels)
    for st in plan["vertical"]["stairs"]:
        r = st["rect"]
        pl.rect(r, L_VERT, lw=1.0)
        mxs = (r[0] + r[2]) / 2
        pl.line(mxs, r[1] + 2, mxs, r[3] - 2, L_VERT, lw=0.4)
        for k in range(1, 6):
            yy = r[1] + 2 + k * (r[3] - r[1] - 4) / 6
            pl.line(r[0], yy, r[2], yy, L_VERT, lw=0.2)
        x_, y_ = pl.P(mxs, by1 + 1.6) if r[1] > 100 else pl.P(mxs, by0 - 4.6)
        sh.text(x_, y_, st["id"], size=5.6, bold=True, align="center", layer=L_TAG)
    el = plan["vertical"]["elevator"]
    pl.rect(el["rect"], L_VERT, lw=1.0)
    pl.line(el["rect"][0], el["rect"][1], el["rect"][2], el["rect"][3], L_VERT, lw=0.4)
    pl.line(el["rect"][0], el["rect"][3], el["rect"][2], el["rect"][1], L_VERT, lw=0.4)
    x_, y_ = pl.P((el["rect"][0] + el["rect"][2]) / 2, by0 - 4.6)
    sh.text(x_, y_, "EL", size=5.6, bold=True, align="center", layer=L_TAG)

    # ---- north arrow + graphic scale (below the plan, right of the dimension)
    nx, ny = pl.P(bx1 + 9, by1 - 30)
    sh.line(nx, ny, nx, ny + 0.55, layer=L_DIM, lw=1.1)
    sh.line(nx, ny + 0.55, nx - 0.09, ny + 0.36, layer=L_DIM, lw=1.1)
    sh.line(nx, ny + 0.55, nx + 0.09, ny + 0.36, layer=L_DIM, lw=1.1)
    sh.text(nx, ny + 0.62, "N", size=10, bold=True, align="center", layer=L_DIM)
    sh.text(nx, ny - 0.13, "APPROX.", size=5.6, align="center", layer=L_DIM)
    sh.text(nx, ny - 0.24, "SITE TBD", size=5.6, align="center", layer=L_DIM)
    gx0, gy0 = pl.P(bx1 - 64, by0 - 9)
    gy0 -= 0.0
    for a_, b_, k in ((0, 16, 0), (16, 32, 1), (32, 64, 2)):
        sh.rect(gx0 + a_ * s, gy0 - 0.30, (b_ - a_) * s, 0.06, layer=L_DIM, lw=0.6)
        if k != 1:
            sh.line(gx0 + a_ * s, gy0 - 0.30, gx0 + b_ * s, gy0 - 0.24, layer=L_DIM, lw=0.3)
    for v in (0, 16, 32, 64):
        sh.text(gx0 + v * s, gy0 - 0.42, f"{v}'", size=5.6, align="center", layer=L_DIM)

    # ================= right panel =================
    rx = px0 + (bx1 - bx0) * s + 1.05
    rw = W - M - 0.22 - rx
    sh.line(rx - 0.2, body_bottom + 0.12, rx - 0.2, top, lw=0.5)
    y = top - 0.05
    sh.rect(rx, y - 0.42, rw, 0.42, lw=1.6)
    sh.text(rx + rw / 2, y - 0.29, pm["label"], size=14, bold=True, align="center")
    y -= 0.62
    sh.text(rx, y, "LEGEND", size=9.5, bold=True)
    y -= 0.05
    leg = [("solid", f"{'Lower' if lvl == 1 else 'Upper'} tier, FIXED seating ({sps_f:.1f} SF/seat) — base"),
           ("dash", f"TELESCOPIC overlay: tier depth if bleachers ({sps_t:.2f} SF/seat) — D-009 OPEN"),
           ("box", "Room block (tag number + drawn SF)"),
           ("stair", "Stair (4) / elevator (X), aligned on both levels")]
    if lvl == 1:
        leg[2:2] = [("mat", "42' wrestling mat (4, 2 x 2)"), ("court", "84' x 50' court + 10' runout (overlay)")]
    else:
        leg[2:2] = [("open", "Open to below")]
    for kind, t_ in leg:
        y -= 0.19
        lx = rx + 0.05
        if kind == "solid":
            sh.line(lx, y + 0.04, lx + 0.4, y + 0.04, lw=0.9)
        elif kind == "dash":
            sh.dashed(lx, y + 0.04, lx + 0.4, y + 0.04, lw=0.9, dash=0.08, gap=0.05)
        elif kind in ("box", "mat"):
            sh.rect(lx + 0.08, y - 0.03, 0.24, 0.14, lw=1.0)
        elif kind == "court":
            sh.dashed(lx, y + 0.04, lx + 0.4, y + 0.04, lw=0.7, dash=0.07, gap=0.04)
        elif kind == "open":
            sh.rect(lx + 0.08, y - 0.03, 0.24, 0.14, lw=0.5); sh.line(lx + 0.08, y - 0.03, lx + 0.32, y + 0.11, lw=0.25)
        elif kind == "stair":
            sh.rect(lx + 0.08, y - 0.03, 0.12, 0.14, lw=1.0); sh.rect(lx + 0.24, y - 0.03, 0.12, 0.14, lw=1.0)
            sh.line(lx + 0.24, y - 0.03, lx + 0.36, y + 0.11, lw=0.4)
        sh.text(lx + 0.55, y, t_, size=7.2)
    # room schedule
    y -= 0.30
    sh.text(rx, y, f"ROOM SCHEDULE — LEVEL {lvl} (drawn vs locked program, P2-G-003 Rev D, fixed)", size=9.5, bold=True)
    hdr = [("TAG", 0, "l"), ("ROOM", 0.36, "l"), ("DRAWN SF", 2.65, "r"), ("PROGRAM", 3.35, "r"), ("NOTE", 3.5, "l")]
    rp = 0.158
    y -= rp
    for lab, dx, al in hdr:
        sh.text(rx + dx, y + 0.02, lab, size=6.8, bold=True, align="left" if al == "l" else "right", layer=TB)
    sh.line(rx, y - 0.04, rx + rw, y - 0.04, layer=TB, lw=0.6)
    for tg, nm, a_, ps, note in sched:
        y -= rp
        while text_width_in(note, 6.4) > rw - 3.52 and len(note) > 4:
            note = note[:-2].rstrip() + "…"
        for (lab, dx, al), c in zip(hdr, [tg, nm, n(a_), n(ps), note]):
            sh.text(rx + dx, y, c, size=6.4 if lab == "NOTE" else 7.0, align="left" if al == "l" else "right", layer=TB)
    sh.line(rx, y - 0.05, rx + rw, y - 0.05, layer=TB, lw=0.4)
    # area summary
    lv1 = plan["level_1"]; lv2 = plan["level_2"]
    fp = area(plan["building"]["rect"])
    l2_drawn = fp - sum(area(o["rect"]) for o in lv2["open_below"])
    y -= 0.08
    sh.text(rx, y - 0.16, "AREA CHECK", size=9.5, bold=True)
    y -= 0.18
    cap = p2["building"]["footprint_cap_sf"]
    if lvl == 1:
        txt = (f"Drawn footprint {n(fp)} SF = cap {n(cap)} (D-031). Program L1 gross {n(F_['L1'])} fixed / {n(T_['L1'])} telescopic "
               f"(P2-G-003 Rev D): the block uses all of it; space beyond the program is lobby and concourse. "
               f"Mechanical drawn {n(sum(area(r['rect']) for r in lv1['rooms'] if r['prog'] == 'mechanical'))} vs {n(F_['M'])} program. "
               f"Fixtures: L1 load {n(F_['fx1']['load'])} → {F_['fx1']['in_rooms']} in two rooms; 2 drinking fountains + 1 service sink in "
               f"concourse alcoves (not drawn). {F_['ws']} wheelchair spaces + companions across both tiers (not drawn).")
    else:
        txt = (f"Drawn L2 floor {n(l2_drawn)} SF (footprint minus open-to-below) vs program L2 gross {n(F_['L2'])} fixed / "
               f"{n(T_['L2'])} telescopic; the extra is rear walkways and the upper concourse. Total drawn ≈ {n(fp + l2_drawn)} vs "
               f"{n(F_['G'])} program GSF. L2 sits over the L1 ring, nothing over the arena volume. Fixtures: L2 load "
               f"{n(F_['fx2']['load'])} → {F_['fx2']['in_rooms']}, stacked over L1 rooms. Stair widths: {F_['stair']['width_in']:.0f} in (R-015).")
    y = sh.para(rx, y, rw, txt, size=7.3)
    sh.text(rx, y - 0.14, "LAYOUT NOTES (KEYSTONE, ASSUMED — architect to confirm)", size=9.0, bold=True)
    y -= 0.16
    notes1 = ["Lockers west next to the floor via the athlete corridor, kept off the public concourse (DR1). Girls drawn equal to boys (D-013).",
              "Entry + foyer at the south end of the west wing (reference plan: south-center); concourse spine runs north along the floor.",
              "Event lockers split north (1-2) and east (3-4); vomitories V1/V2 through the tier are TBD. No tier on the west; stage TBD (no source).",
              "Table/bench zones 15 ft N and S; court overlay long axis N-S. Exit separation, travel distance and sightlines NOT checked."]
    notes2 = ["S&C + cross-training on Level 2 over the lockers (D-030); gym floor loads → structural engineer.",
              "Restrooms + admin stacked over L1 restrooms; L2 corridor + bridge connect the stairs, elevator and upper concourse.",
              "Upper tier 15 ft deep on N, S and E over the L1 ring; rear walkways N and S. Suites PARKED (none drawn).",
              "Exit separation, travel distance, sightlines and structure NOT checked. Floor-to-floor 15 ft ASSUMED."]
    for t_ in (notes1 if lvl == 1 else notes2):
        y = sh.para(rx, y + 0.02, rw, t_, size=7.0, indent=0.12, bullet="·")
    y = sh.para(rx, y - 0.02, rw, "Sources: phase2.yaml (locked, D-030, D-031); P2-G-003 Rev D; R-005, R-008, R-009, R-012, R-014, R-015; "
                "reference plan (Shane). Geometry: params/phase2_plan.yaml.", size=6.6)
    fl = body_bottom + 0.08
    if y < fl:
        raise SystemExit(f"LAYOUT OVERFLOW: right panel runs {fl - y:.2f} in into the stamp band")
    print(f"layout margin right panel (in): {y - fl:.2f}")
    return sh, rv_letter


# ============================ REV B (Shane 2026-10-04 4:30 AM CT) ============================
# Entry south-center on the arena N-S axis, restrooms flank the lobby, mech off the west side, MIX seating (D-009).
# Geometry: params/phase2_plan_rev_b.yaml. Program: p2_testfit.compute_mix (P2-G-003 Rev E). Rev A (build) is FROZEN.

def overlap(a, b):
    return max(0.0, min(a[2], b[2]) - max(a[0], b[0])) * max(0.0, min(a[3], b[3]) - max(a[1], b[1]))


def check_overlaps(lv, vert):
    """Rooms must not overlap each other; a stair or the elevator may sit inside a room only if listed in `allow`."""
    probs = []
    rs = lv["rooms"]
    for i in range(len(rs)):
        for j in range(i + 1, len(rs)):
            if overlap(rs[i]["rect"], rs[j]["rect"]) > 0.01:
                probs.append(f"{rs[i]['id']} x {rs[j]['id']}")
    return probs


def build_b(sheet_no, p2, prog, plan, X_, seats):
    lvl = LEVEL_OF[sheet_no]
    meta2 = p2["meta"]
    pm = plan["meta"]
    rows, tot = seats
    bys = {r["side"]: r for r in rows}
    sh = Sheet(W, H)
    body_bottom = add_titleblock(sh, {
        "project": f"{meta2['project']}\n{meta2['arena_name']} · {meta2['location']}",
        "phase": "PHASE 2",
        "title": f"OVERALL FLOOR PLAN\nLEVEL {lvl} · BLOCK PLAN",
        "scale": "1/32\" = 1'-0\"",
        "date": meta2["sheet_date"],
        "revision": "B",
        "drawn_by": meta2["drawn_by"],
        "sheet_no": sheet_no,
        "stamp": meta2["stamp"],
    }, margin=M, tb_h=0.95, stamp_h=0.40)
    top = H - M - 0.12
    s = 1.0 / pm["scale_ft_per_in"]
    bx0, by0, bx1, by1 = plan["building"]["rect"]
    px0, py0 = M + 0.62, body_bottom + 0.50
    pl = Plan(sh, px0, py0, s)
    floor = plan["event_floor"]["rect"]
    av = plan["arena_volume"]["rect"]
    lv = plan["level_1"] if lvl == 1 else plan["level_2"]
    vert = plan["vertical"]
    axis = plan["entry_axis_x"]["value"]
    sched = []
    probs = check_overlaps(lv, vert)
    if probs:
        raise SystemExit(f"ROOM OVERLAP on level {lvl}: {probs}")


    pl.rect(plan["building"]["rect"], L_WALL, lw=2.2)
    yd = by0 - 9
    pl.line(bx0, yd, bx1, yd, L_DIM, lw=0.4)
    for xx in (bx0, bx1):
        pl.line(xx, yd - 2.5, xx, yd + 2.5, L_DIM, lw=0.4)
    tx, ty = pl.P((bx0 + bx1) / 2, yd)
    sh.text(tx, ty - 0.14, f"{bx1 - bx0:g}'-0\"  (building {bx1 - bx0:g} x {by1 - by0:g} ft = {n(area(plan['building']['rect']))} SF footprint)", size=7, align="center", layer=L_DIM)
    xd = bx0 - 9
    pl.line(xd, by0, xd, by1, L_DIM, lw=0.4)
    for yy in (by0, by1):
        pl.line(xd - 2.5, yy, xd + 2.5, yy, L_DIM, lw=0.4)
    tx, ty = pl.P(xd, (by0 + by1) / 2)
    sh.text(tx - 0.06, ty, f"{by1 - by0:g}'-0\"", size=7, align="center", layer=L_DIM, rot=90)

    lo, up = plan["tiers"]["lower"], plan["tiers"]["upper"]
    names = {"N": "N", "S": "S", "E": "E"}
    if lvl == 1:
        pl.rect(av, L_FIX, lw=0.9)
        pl.rect(floor, L_MAT, lw=1.4)
        fx0, fy0, fx1, fy1 = floor
        for b in lo["bands"]:
            r = b["rect"]
            pl.rect(r, L_TEL, lw=0.9)
            horiz = (r[2] - r[0]) >= (r[3] - r[1])
            ops = [o["rect"] for o in lo["openings"] if o["side"] == b["side"]]
            # back-half row lines (rows 4-6), broken at openings; label in the front half
            for k in range(lo["rows"] // 2, lo["rows"]):
                dk = k * lo["row_depth_ft"]
                if horiz:
                    yy = r[1] + dk if b["side"] == "N" else r[3] - dk
                    xs = [r[0]] + sum(([o[0], o[2]] for o in sorted(ops)), []) + [r[2]]
                    for a_, b_ in zip(xs[0::2], xs[1::2]):
                        pl.line(a_, yy, b_, yy, L_TEL, lw=0.2)
                else:
                    xx = r[0] + dk
                    ys = [r[1]] + sum(([o[1], o[3]] for o in sorted(ops, key=lambda o: o[1])), []) + [r[3]]
                    for a_, b_ in zip(ys[0::2], ys[1::2]):
                        pl.line(xx, a_, xx, b_, L_TEL, lw=0.2)
            t_ = f"LOWER ({b['side']}) · TELESCOPIC · {n(bys[b['side']]['lower'])} SEATS"
            if horiz:
                yy = r[1] + 2.4 if b["side"] == "N" else r[3] - 3.6
                x_lab = r[0] + 2.5 if b["side"] == "N" else lo["openings"][0]["rect"][2] + 3   # S: east of the portal
                x_, y_ = pl.P(x_lab, yy)
                sh.text(x_, y_ - 0.035, t_, size=5.2, bold=True, layer=L_TAG)
            else:
                x_, y_ = pl.P(r[0] + 3.4, (r[1] + r[3]) / 2 - 22)
                sh.text(x_ + 0.035, y_, t_, size=5.2, bold=True, align="center", layer=L_TAG, rot=90)
        for o in lo["openings"]:
            pl.drect(o["rect"], L_ROOM, lw=0.5, dash=0.04, gap=0.03)
            r = o["rect"]
            horiz = (r[2] - r[0]) < (r[3] - r[1])           # openings run through the band
            x_, y_ = pl.P((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)
            if o["id"] == "PORTAL":
                sh.text(x_, y_ + 0.0, "PORTAL", size=4.8, bold=True, align="center", layer=L_TAG)
            else:
                sh.text(x_, y_ - 0.03, o["id"], size=5.0, bold=True, align="center", layer=L_TAG)
        mft = p2["spaces"]["arena"]["mat_ft"]
        for m in plan["mats"]:
            mx, my = m["origin"]
            pl.rect((mx, my, mx + mft, my + mft), L_MAT, lw=1.0)
            left = mx + mft / 2 < (floor[0] + floor[2]) / 2
            x_, y_ = pl.P(mx + 2 if left else mx + mft - 2, my + mft - 2.5)
            sh.text(x_, y_ - 0.09, m["id"], size=6.2, bold=True, align="left" if left else "right", layer=L_TAG)
        cr = plan["court"]["rect"]
        ro = plan["court"]["runout_ft"]
        pl.drect(cr, L_CORT, lw=0.7, dash=0.07, gap=0.04)
        pl.drect((cr[0] - ro, cr[1] - ro, cr[2] + ro, cr[3] + ro), L_CORT, lw=0.35, dash=0.03, gap=0.04)
        pl.dashed(cr[0], (cr[1] + cr[3]) / 2, cr[2], (cr[1] + cr[3]) / 2, L_CORT, lw=0.4, dash=0.07, gap=0.04)
        x_, y_ = pl.P((fx0 + fx1) / 2, fy1 - 6)
        sh.text(x_, y_, f"EVENT FLOOR {fx1 - fx0:g}' x {fy1 - fy0:g}' = {n(area(floor))} SF", size=6.6, bold=True, align="center", layer=L_TAG)
        sh.text(x_, y_ - 0.12, "table / bench zone (15')", size=5.4, align="center", layer=L_TAG)
        x_, y_ = pl.P((fx0 + fx1) / 2, fy0 + 7.5)
        sh.text(x_, y_, "table / bench zone (15')", size=5.4, align="center", layer=L_TAG)
        x_, y_ = pl.P((cr[0] + cr[2]) / 2, (cr[1] + cr[3]) / 2 + 2.5)
        sh.text(x_, y_, "COURT 84' x 50' (OVERLAY)", size=5.4, align="center", layer=L_TAG)
        lower_drawn = sum(area(b["rect"]) for b in lo["bands"])
        sched.append(("—", "Event floor (D-030 locked)", area(floor), X_["sf"]["arena"], "114' x 144'"))
        sched.append(("—", f"Lower tier, telescopic ({n(tot['lower'])} seats)", lower_drawn, X_["sf"]["seating_lower"],
                      f"{lo['rows']} rows; N {bys['N']['lower']} / S {bys['S']['lower']} / E {bys['E']['lower']}"))
        # team / public separation (gate) and entry arrow on the axis
        pl.dashed(56, 0, 56, 56, L_ROOM, lw=0.7, dash=0.05, gap=0.03)
        pl.line(axis, -6, axis, 0, L_DIM, lw=1.0)
        pl.line(axis, 0, axis - 1.8, -2.6, L_DIM, lw=1.0); pl.line(axis, 0, axis + 1.8, -2.6, L_DIM, lw=1.0)
        x_, y_ = pl.P(axis - 3, -5.2)
        sh.text(x_, y_, "MAIN ENTRY (ARENA N-S AXIS; ROAD ASSUMED SOUTH)", size=6.0, bold=True, align="right", layer=L_TAG)
    else:
        for ob in lv["open_below"]:
            r = ob["rect"]
            pl.rect(r, L_HID, lw=0.5)
            for (xa, ya, xb, yb) in ((r[0], r[1], r[2], r[3]), (r[0], r[3], r[2], r[1])):
                for t0, t1 in ((0.0, 0.36), (0.64, 1.0)):
                    pl.dashed(xa + (xb - xa) * t0, ya + (yb - ya) * t0, xa + (xb - xa) * t1, ya + (yb - ya) * t1, L_HID, lw=0.25, dash=0.06, gap=0.06)
        pl.drect(floor, L_HID, lw=0.4, dash=0.05, gap=0.05)
        for b in up["bands"]:
            r = b["rect"]
            pl.rect(r, L_FIX, lw=0.9)
            t_ = f"UPPER ({b['side']}) · FIXED · {n(bys[b['side']]['upper'])} SEATS"
            if (r[2] - r[0]) >= (r[3] - r[1]):
                x_, y_ = pl.P(r[0] + 3, (r[1] + r[3]) / 2)
                sh.text(x_, y_ - 0.035, t_, size=5.6, bold=True, layer=L_TAG)
            else:
                x_, y_ = pl.P((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)
                sh.text(x_ + 0.035, y_, t_, size=5.6, bold=True, align="center", layer=L_TAG, rot=90)
        oba = next(o for o in lv["open_below"] if o["id"] == "ob_arena")["rect"]
        x_, y_ = pl.P((oba[0] + oba[2]) / 2, (oba[1] + oba[3]) / 2)
        sh.text(x_, y_ + 0.05, "OPEN TO ARENA BELOW", size=8, bold=True, align="center", layer=L_TAG)
        sh.text(x_, y_ - 0.10, "(event floor + telescopic lower tier, double height)", size=6, align="center", layer=L_TAG)
        obl = next(o for o in lv["open_below"] if o["id"] == "ob_lobby")["rect"]
        pl.tag(obl, ["OPEN TO LOBBY BELOW", "(hall of champions,", "double height)"], sizes=(6.4, 6.0, 5.5), bold_first=True, allow_rot=False)
        upper_drawn = sum(area(b["rect"]) for b in up["bands"])
        sched.append(("—", f"Upper tier, fixed ({n(tot['upper'])} seats)", upper_drawn, X_["sf"]["seating_upper"],
                      f"N {bys['N']['upper']} / S {bys['S']['upper']} / E {bys['E']['upper']}"))

    # rooms (stairs / elevator inside a room are subtracted from its drawn SF)
    mech_rooms = [r for r in plan["level_1"]["rooms"] if r["prog"] == "mechanical"]
    mech_drawn = sum(area(r["rect"]) for r in mech_rooms)
    vrects = [st_["rect"] for st_ in vert["stairs"]] + [vert["elevator"]["rect"]]
    for r in lv["rooms"]:
        pl.rect(r["rect"], L_ROOM, lw=0.9)
        a_ = area(r["rect"]) - sum(overlap(r["rect"], v) for v in vrects)
        if r["prog"] == "mechanical":
            ps = X_["M"] * area(r["rect"]) / mech_drawn
        else:
            ps = X_["sf"][r["prog"]] * r.get("share", 1)
        note = r.get("note", "")
        extra = []
        if "fixtures" in r:
            wc, lav, ur = fixture_lines(X_, r["fixtures"])
            ps = (wc + lav) * prog["factors"]["restrooms"]["sf_per_fixture"]
            extra = [f"WC {wc} · LAV {lav}"]
            note = f"{wc + lav} fixtures (WC {wc}, LAV {lav}" + (f"; urinals ≤ {ur} of the WCs)" if ur is not None else ")")
        if r["id"] == "sc":
            note = "over boys locker + NW mech; ST-1 inside"
        if r["id"] == "xt":
            note = "over girls locker (D-030)"
        full = [f"{r['tag']}  {r['name']}", f"{n(a_)} SF"] + extra
        if not pl.tag(r["rect"], full, fallback=[f"{r['tag']}", f"{n(a_)}"]):
            pl.tag(r["rect"], [r["tag"]], sizes=(5.5, 5.0, 4.5))
        nm = r["name"].title().replace("(Nw)", "(NW)").replace("(Se)", "(SE)").replace("Mat", "Mat Area")
        sched.append((r["tag"], nm, a_, ps, note))
    for z in lv["zones"]:
        if z.get("vertical"):
            r = z["rect"]
            x_, y_ = pl.P((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)
            sz = 6.2
            while text_width_in(z["name"], sz, True) > (r[3] - r[1]) * s - 0.1 and sz > 4.5:
                sz -= 0.3
            sh.text(x_ + 0.03, y_, z["name"], size=sz, bold=True, align="center", layer=L_TAG, rot=90)
        else:
            lines = z["name"].replace(" / ", " /|").split("|")
            if z["id"] == "lobby":
                lines = lines + ["(double height)"]
            pl.tag(z.get("label_rect", z["rect"]), lines, sizes=(6.4, 6.0, 5.5, 5.0, 4.6), allow_rot=False)
    for st in vert["stairs"]:
        r = st["rect"]
        pl.rect(r, L_VERT, lw=1.0)
        horiz = (r[2] - r[0]) > (r[3] - r[1])
        if horiz:
            my_ = (r[1] + r[3]) / 2
            pl.line(r[0] + 2, my_, r[2] - 2, my_, L_VERT, lw=0.4)
            for k in range(1, 6):
                xx = r[0] + 2 + k * (r[2] - r[0] - 4) / 6
                pl.line(xx, r[1], xx, r[3], L_VERT, lw=0.2)
        else:
            mxs = (r[0] + r[2]) / 2
            pl.line(mxs, r[1] + 2, mxs, r[3] - 2, L_VERT, lw=0.4)
            for k in range(1, 6):
                yy = r[1] + 2 + k * (r[3] - r[1] - 4) / 6
                pl.line(r[0], yy, r[2], yy, L_VERT, lw=0.2)
        cxs = (r[0] + r[2]) / 2
        x_, y_ = pl.P(cxs, by1 + 1.6) if r[1] > 100 else pl.P(cxs, by0 - 4.6)
        sh.text(x_, y_, st["id"], size=5.6, bold=True, align="center", layer=L_TAG)
    el = vert["elevator"]
    pl.rect(el["rect"], L_VERT, lw=1.0)
    pl.line(el["rect"][0], el["rect"][1], el["rect"][2], el["rect"][3], L_VERT, lw=0.4)
    pl.line(el["rect"][0], el["rect"][3], el["rect"][2], el["rect"][1], L_VERT, lw=0.4)
    ex_, ey_ = pl.P(el["rect"][0] - 0.8, (el["rect"][1] + el["rect"][3]) / 2)
    sh.text(ex_, ey_ - 0.03, "EL", size=5.6, bold=True, align="right", layer=L_TAG)

    nx, ny = pl.P(bx1 + 9, by1 - 30)
    sh.line(nx, ny, nx, ny + 0.55, layer=L_DIM, lw=1.1)
    sh.line(nx, ny + 0.55, nx - 0.09, ny + 0.36, layer=L_DIM, lw=1.1)
    sh.line(nx, ny + 0.55, nx + 0.09, ny + 0.36, layer=L_DIM, lw=1.1)
    sh.text(nx, ny + 0.62, "N", size=10, bold=True, align="center", layer=L_DIM)
    sh.text(nx, ny - 0.13, "APPROX.", size=5.6, align="center", layer=L_DIM)
    sh.text(nx, ny - 0.24, "SITE TBD", size=5.6, align="center", layer=L_DIM)
    gx0, gy0 = pl.P(bx1 + 4, by0 + 40)
    for a_, b_, k in ((0, 8, 0), (8, 16, 1), (16, 32, 2)):
        sh.rect(gx0 + a_ * s, gy0 - 0.30, (b_ - a_) * s, 0.06, layer=L_DIM, lw=0.6)
        if k != 1:
            sh.line(gx0 + a_ * s, gy0 - 0.30, gx0 + b_ * s, gy0 - 0.24, layer=L_DIM, lw=0.3)
    for v in (0, 8, 16, 32):
        sh.text(gx0 + v * s, gy0 - 0.42, f"{v}'", size=5.6, align="center", layer=L_DIM)
    sh.text(gx0, gy0 - 0.14, "GRAPHIC SCALE (FT)", size=5.6, layer=L_DIM)

    # ================= right panel =================
    rx = max(px0 + (bx1 - bx0) * s + 1.05, 9.35)
    rw = W - M - 0.22 - rx
    sh.line(rx - 0.2, body_bottom + 0.12, rx - 0.2, top, lw=0.5)
    y = top - 0.05
    sh.rect(rx, y - 0.42, rw, 0.42, lw=1.6)
    sh.text(rx + rw / 2, y - 0.29, pm["label"], size=14, bold=True, align="center")
    sh.text(rx, y - 0.68, f"LEVEL {lvl} — OVERALL FLOOR PLAN (REV B)", size=12, bold=True)
    sh.text(rx, y - 0.88, "scale 1/32\" = 1'-0\" on 17 x 11 in · north approximate, road assumed south, site TBD", size=7.8)
    y -= 1.18
    sh.text(rx, y, "LEGEND", size=9.5, bold=True)
    y -= 0.05
    if lvl == 1:
        leg = [("box", f"Lower tier, TELESCOPIC (extended, {lo['rows']} rows x 24 in; {X_['seat_sf_lower']:.2f} SF/seat) — D-009"),
               ("mat", "42' wrestling mat (4, 2 x 2)"), ("court", "84' x 50' court + 10' runout (overlay)"),
               ("dash", "Portal / vomitory through the telescopic tier (V1, V2)")]
    else:
        leg = [("box", f"Upper tier, FIXED ({X_['seat_sf_upper']:.1f} SF/seat) on the Level 2 deck — D-009"),
               ("open", "Open to below (arena; lobby double height)")]
    leg += [("box", "Room block (tag number + drawn SF)"), ("stair", "Stair (4) / elevator (X), same position on both levels")]
    for kind, t_ in leg:
        y -= 0.19
        lx = rx + 0.05
        if kind == "dash":
            sh.dashed(lx, y + 0.04, lx + 0.4, y + 0.04, lw=0.6, dash=0.04, gap=0.03)
        elif kind in ("box", "mat"):
            sh.rect(lx + 0.08, y - 0.03, 0.24, 0.14, lw=1.0)
        elif kind == "court":
            sh.dashed(lx, y + 0.04, lx + 0.4, y + 0.04, lw=0.7, dash=0.07, gap=0.04)
        elif kind == "open":
            sh.rect(lx + 0.08, y - 0.03, 0.24, 0.14, lw=0.5); sh.line(lx + 0.08, y - 0.03, lx + 0.32, y + 0.11, lw=0.25)
        elif kind == "stair":
            sh.rect(lx + 0.08, y - 0.03, 0.12, 0.14, lw=1.0); sh.rect(lx + 0.24, y - 0.03, 0.12, 0.14, lw=1.0)
            sh.line(lx + 0.24, y - 0.03, lx + 0.36, y + 0.11, lw=0.4)
        sh.text(lx + 0.55, y, t_, size=7.2)
    y -= 0.30
    sh.text(rx, y, f"ROOM SCHEDULE — LEVEL {lvl} (drawn vs locked program, P2-G-003 Rev E)", size=9.5, bold=True)
    hdr = [("TAG", 0, "l"), ("ROOM", 0.36, "l"), ("DRAWN SF", 2.65, "r"), ("PROGRAM", 3.35, "r"), ("NOTE", 3.5, "l")]
    rp = 0.155
    y -= rp
    for lab, dx, al in hdr:
        sh.text(rx + dx, y + 0.02, lab, size=6.8, bold=True, align="left" if al == "l" else "right", layer=TB)
    sh.line(rx, y - 0.04, rx + rw, y - 0.04, layer=TB, lw=0.6)
    for tg, nm, a_, ps, note in sched:
        y -= rp
        while text_width_in(note, 6.4) > rw - 3.52 and len(note) > 4:
            note = note[:-2].rstrip() + "…"
        for (lab, dx, al), c in zip(hdr, [tg, nm, n(a_), n(ps), note]):
            sh.text(rx + dx, y, c, size=6.4 if lab == "NOTE" else 7.0, align="left" if al == "l" else "right", layer=TB)
    sh.line(rx, y - 0.05, rx + rw, y - 0.05, layer=TB, lw=0.4)
    lv2 = plan["level_2"]
    fp = area(plan["building"]["rect"])
    l2_drawn = fp - sum(area(o["rect"]) for o in lv2["open_below"])
    cap = p2["building"]["footprint_cap_sf"]
    y -= 0.08
    sh.text(rx, y - 0.16, "AREA CHECK", size=9.5, bold=True)
    y -= 0.18
    if lvl == 1:
        txt = (f"Box {bx1 - bx0:g} x {by1 - by0:g} ft = {n(fp)} SF (Rev A 250 x 220): {n(cap - fp)} SF under the {n(cap)} cap (target ≥ 2,000). "
               f"Program footprint {n(X_['F'])} (P2-G-003 Rev E) fits inside with {n(fp - X_['F'])} to spare. Seats: lower {n(tot['lower'])} "
               f"+ upper {n(tot['upper'])} = {n(tot['total'])} (N {bys['N']['total']}, S {bys['S']['total']}, E {bys['E']['total']}). "
               f"Mech drawn {n(mech_drawn)} vs {n(X_['M'])}. L1 fixtures {X_['fx1']['in_rooms']} flank the lobby; drinking fountains, "
               f"service sink and {X_['ws']} wheelchair spaces not drawn.")
    else:
        txt = (f"Drawn L2 floor {n(l2_drawn)} SF (box minus open-to-below) vs program L2 gross {n(X_['L2'])}; the extra is the "
               f"corridor, walkways and balcony. Total drawn ≈ {n(fp + l2_drawn)} vs {n(X_['G'])} program GSF. Upper tier sits over the "
               f"L1 ring; L2 restrooms ({X_['fx2']['in_rooms']} fixtures) stack over L1's; balcony over the lobby carries the hall of champions wall.")
    y = sh.para(rx, y, rw, txt, size=7.2)
    sh.text(rx, y - 0.14, "LAYOUT NOTES (KEYSTONE, ASSUMED — architect to confirm)", size=9.0, bold=True)
    y -= 0.16
    notes1 = ["Entry, vestibule, lobby and portal on the arena N-S axis; lobby under the south upper tier, double height to its south.",
              "Restrooms flank the lobby: men west, women east. Concession in the lobby under the tier; first aid at the entry.",
              "West side = lockers + athlete corridor only; team / service entry at the SW, gated from the public side (dashed).",
              "Mech moved to the NW corner, north wall and east ring (behind the bowl). Event lockers N + E via V1/V2.",
              "Exit separation, travel distance and sightlines NOT checked."]
    notes2 = ["S&C + cross-training on Level 2 over the lockers (D-030); gym floor loads → structural engineer.",
              "Restrooms stacked over L1's; admin over the team entry; balcony links west and east over the lobby.",
              "Upper tier 15 ft on N, S, E over the L1 ring; the south tier sits over the lobby. Suites PARKED.",
              "Exit separation, travel distance, sightlines and structure NOT checked. Floor-to-floor 15 ft ASSUMED."]
    for t_ in (notes1 if lvl == 1 else notes2):
        y = sh.para(rx, y + 0.02, rw, t_, size=6.9, indent=0.12, bullet="·")
    y = sh.para(rx, y - 0.02, rw, "Sources: phase2.yaml (D-009, D-030, D-031); Shane 2026-10-04 4:30 AM CT; P2-G-003 Rev E; R-005, R-008, "
                "R-009, R-012, R-014, R-015. Geometry: params/phase2_plan_rev_b.yaml.", size=6.6)
    fl = body_bottom + 0.08
    if y < fl:
        raise SystemExit(f"LAYOUT OVERFLOW: right panel runs {fl - y:.2f} in into the stamp band")
    print(f"layout margin right panel (in): {y - fl:.2f}")
    return sh



# ============================ REV C (Shane 2026-10-04 4:43 AM CT) ============================
# Single controlled entry (D-033): checkpoint, controlled door to the athlete route, EXIT ONLY perimeter doors, service door
# (D-034 OPEN), SW entry removed. Geometry: params/phase2_plan_rev_c.yaml. Rev B (build_b) is FROZEN.

def build_c(sheet_no, p2, prog, plan, X_, seats):
    """Rev C (Shane 2026-10-04 4:43 AM CT, D-033): single controlled entry, checkpoint, EXIT ONLY perimeter doors."""
    lvl = LEVEL_OF[sheet_no]
    meta2 = p2["meta"]
    pm = plan["meta"]
    rows, tot = seats
    bys = {r["side"]: r for r in rows}
    sh = Sheet(W, H)
    body_bottom = add_titleblock(sh, {
        "project": f"{meta2['project']}\n{meta2['arena_name']} · {meta2['location']}",
        "phase": "PHASE 2",
        "title": f"OVERALL FLOOR PLAN\nLEVEL {lvl} · BLOCK PLAN",
        "scale": "1/32\" = 1'-0\"",
        "date": meta2["sheet_date"],
        "revision": "C",
        "drawn_by": meta2["drawn_by"],
        "sheet_no": sheet_no,
        "stamp": meta2["stamp"],
    }, margin=M, tb_h=0.95, stamp_h=0.40)
    top = H - M - 0.12
    s = 1.0 / pm["scale_ft_per_in"]
    bx0, by0, bx1, by1 = plan["building"]["rect"]
    px0, py0 = M + 0.62, body_bottom + 0.50
    pl = Plan(sh, px0, py0, s)
    floor = plan["event_floor"]["rect"]
    av = plan["arena_volume"]["rect"]
    lv = plan["level_1"] if lvl == 1 else plan["level_2"]
    vert = plan["vertical"]
    axis = plan["entry_axis_x"]["value"]
    sched = []
    probs = check_overlaps(lv, vert)
    if probs:
        raise SystemExit(f"ROOM OVERLAP on level {lvl}: {probs}")


    pl.rect(plan["building"]["rect"], L_WALL, lw=2.2)
    yd = by0 - 9
    pl.line(bx0, yd, bx1, yd, L_DIM, lw=0.4)
    for xx in (bx0, bx1):
        pl.line(xx, yd - 2.5, xx, yd + 2.5, L_DIM, lw=0.4)
    tx, ty = pl.P((bx0 + bx1) / 2, yd)
    sh.text(tx, ty - 0.14, f"{bx1 - bx0:g}'-0\"  (building {bx1 - bx0:g} x {by1 - by0:g} ft = {n(area(plan['building']['rect']))} SF footprint)", size=7, align="center", layer=L_DIM)
    xd = bx0 - 9
    pl.line(xd, by0, xd, by1, L_DIM, lw=0.4)
    for yy in (by0, by1):
        pl.line(xd - 2.5, yy, xd + 2.5, yy, L_DIM, lw=0.4)
    tx, ty = pl.P(xd, (by0 + by1) / 2)
    sh.text(tx - 0.06, ty, f"{by1 - by0:g}'-0\"", size=7, align="center", layer=L_DIM, rot=90)

    lo, up = plan["tiers"]["lower"], plan["tiers"]["upper"]
    names = {"N": "N", "S": "S", "E": "E"}
    if lvl == 1:
        pl.rect(av, L_FIX, lw=0.9)
        pl.rect(floor, L_MAT, lw=1.4)
        fx0, fy0, fx1, fy1 = floor
        for b in lo["bands"]:
            r = b["rect"]
            pl.rect(r, L_TEL, lw=0.9)
            horiz = (r[2] - r[0]) >= (r[3] - r[1])
            ops = [o["rect"] for o in lo["openings"] if o["side"] == b["side"]]
            # back-half row lines (rows 4-6), broken at openings; label in the front half
            for k in range(lo["rows"] // 2, lo["rows"]):
                dk = k * lo["row_depth_ft"]
                if horiz:
                    yy = r[1] + dk if b["side"] == "N" else r[3] - dk
                    xs = [r[0]] + sum(([o[0], o[2]] for o in sorted(ops)), []) + [r[2]]
                    for a_, b_ in zip(xs[0::2], xs[1::2]):
                        pl.line(a_, yy, b_, yy, L_TEL, lw=0.2)
                else:
                    xx = r[0] + dk
                    ys = [r[1]] + sum(([o[1], o[3]] for o in sorted(ops, key=lambda o: o[1])), []) + [r[3]]
                    for a_, b_ in zip(ys[0::2], ys[1::2]):
                        pl.line(xx, a_, xx, b_, L_TEL, lw=0.2)
            t_ = f"LOWER ({b['side']}) · TELESCOPIC · {n(bys[b['side']]['lower'])} SEATS"
            if horiz:
                yy = r[1] + 2.4 if b["side"] == "N" else r[3] - 3.6
                x_lab = r[0] + 2.5 if b["side"] == "N" else lo["openings"][0]["rect"][2] + 3   # S: east of the portal
                x_, y_ = pl.P(x_lab, yy)
                sh.text(x_, y_ - 0.035, t_, size=5.2, bold=True, layer=L_TAG)
            else:
                x_, y_ = pl.P(r[0] + 3.4, (r[1] + r[3]) / 2 - 22)
                sh.text(x_ + 0.035, y_, t_, size=5.2, bold=True, align="center", layer=L_TAG, rot=90)
        for o in lo["openings"]:
            pl.drect(o["rect"], L_ROOM, lw=0.5, dash=0.04, gap=0.03)
            r = o["rect"]
            horiz = (r[2] - r[0]) < (r[3] - r[1])           # openings run through the band
            x_, y_ = pl.P((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)
            if o["id"] == "PORTAL":
                sh.text(x_, y_ + 0.0, "PORTAL", size=4.8, bold=True, align="center", layer=L_TAG)
            else:
                sh.text(x_, y_ - 0.03, o["id"], size=5.0, bold=True, align="center", layer=L_TAG)
        mft = p2["spaces"]["arena"]["mat_ft"]
        for m in plan["mats"]:
            mx, my = m["origin"]
            pl.rect((mx, my, mx + mft, my + mft), L_MAT, lw=1.0)
            left = mx + mft / 2 < (floor[0] + floor[2]) / 2
            x_, y_ = pl.P(mx + 2 if left else mx + mft - 2, my + mft - 2.5)
            sh.text(x_, y_ - 0.09, m["id"], size=6.2, bold=True, align="left" if left else "right", layer=L_TAG)
        cr = plan["court"]["rect"]
        ro = plan["court"]["runout_ft"]
        pl.drect(cr, L_CORT, lw=0.7, dash=0.07, gap=0.04)
        pl.drect((cr[0] - ro, cr[1] - ro, cr[2] + ro, cr[3] + ro), L_CORT, lw=0.35, dash=0.03, gap=0.04)
        pl.dashed(cr[0], (cr[1] + cr[3]) / 2, cr[2], (cr[1] + cr[3]) / 2, L_CORT, lw=0.4, dash=0.07, gap=0.04)
        x_, y_ = pl.P((fx0 + fx1) / 2, fy1 - 6)
        sh.text(x_, y_, f"EVENT FLOOR {fx1 - fx0:g}' x {fy1 - fy0:g}' = {n(area(floor))} SF", size=6.6, bold=True, align="center", layer=L_TAG)
        sh.text(x_, y_ - 0.12, "table / bench zone (15')", size=5.4, align="center", layer=L_TAG)
        x_, y_ = pl.P((fx0 + fx1) / 2, fy0 + 7.5)
        sh.text(x_, y_, "table / bench zone (15')", size=5.4, align="center", layer=L_TAG)
        x_, y_ = pl.P((cr[0] + cr[2]) / 2, (cr[1] + cr[3]) / 2 + 2.5)
        sh.text(x_, y_, "COURT 84' x 50' (OVERLAY)", size=5.4, align="center", layer=L_TAG)
        lower_drawn = sum(area(b["rect"]) for b in lo["bands"])
        sched.append(("—", "Event floor (D-030 locked)", area(floor), X_["sf"]["arena"], "114' x 144'"))
        sched.append(("—", f"Lower tier, telescopic ({n(tot['lower'])} seats)", lower_drawn, X_["sf"]["seating_lower"],
                      f"{lo['rows']} rows; N {bys['N']['lower']} / S {bys['S']['lower']} / E {bys['E']['lower']}"))
        # team side / public side walls (Rev C): team assembly vs west concourse, athlete route vs west concourse
        pl.line(56, 35, 56, 48, L_ROOM, lw=0.9)
        pl.line(56, 48, 84, 48, L_ROOM, lw=0.9)
        # single controlled entry (D-033): entry arrow on the axis
        pl.line(axis, -6, axis, 0, L_DIM, lw=1.0)
        pl.line(axis, 0, axis - 1.8, -2.6, L_DIM, lw=1.0); pl.line(axis, 0, axis + 1.8, -2.6, L_DIM, lw=1.0)
        x_, y_ = pl.P(axis - 3, -5.2)
        sh.text(x_, y_, "ARENA N-S AXIS · ROAD ASSUMED SOUTH", size=5.6, align="right", layer=L_TAG)
        x_, y_ = pl.P(axis + 3, -5.2)
        sh.text(x_, y_, "E1 MAIN ENTRY / EXIT (D-033)", size=6.0, bold=True, layer=L_TAG)
        # security checkpoint (location only; size TBD)
        ck = lv["checkpoint"]
        pl.drect(ck["rect"], L_TAG, lw=0.9, dash=0.06, gap=0.035)
        x_, y_ = pl.P((ck["rect"][0] + ck["rect"][2]) / 2, (ck["rect"][1] + ck["rect"][3]) / 2)
        sh.text(x_, y_ + 0.015, "SECURITY CHECKPOINT", size=5.6, bold=True, align="center", layer=L_TAG)
        sh.text(x_, y_ - 0.085, "— size TBD (ASSUMED)", size=5.0, align="center", layer=L_TAG)
        # controlled door off the lobby to the athlete route
        cdx, cdy = lv["controlled_door"]["at"]
        pl.line(cdx, cdy - 4, cdx, cdy + 4, L_TAG, lw=2.4)
        x_, y_ = pl.P(cdx + 1.2, cdy - 7.2)
        sh.text(x_, y_, "CD-1 CONTROLLED DOOR", size=5.0, bold=True, layer=L_TAG)
        sh.text(x_, y_ - 0.08, "(staff / teams)", size=4.8, layer=L_TAG)
        # perimeter doors: symbols only (widths not drawn)
        stair_exit = {}
        for d_ in lv["doors"]["items"]:
            w_, at = d_["wall"], d_["at"]
            if d_["kind"] == "main":
                continue
            if w_ in ("N", "S"):
                yy = by1 if w_ == "N" else by0
                pl.line(at - 2.5, yy, at + 2.5, yy, L_TAG, lw=3.0)
                o = 1 if w_ == "N" else -1
                if d_["kind"] == "exit":
                    pl.line(at, yy, at, yy + 3.2 * o, L_TAG, lw=0.8)
                    pl.line(at, yy + 3.2 * o, at - 1.2, yy + 1.8 * o, L_TAG, lw=0.8); pl.line(at, yy + 3.2 * o, at + 1.2, yy + 1.8 * o, L_TAG, lw=0.8)
            else:
                xx = bx0 if w_ == "W" else bx1
                pl.line(xx, at - 2.5, xx, at + 2.5, L_TAG, lw=3.0)
                o = -1 if w_ == "W" else 1
                if d_["kind"] == "exit":
                    pl.line(xx, at, xx + 3.2 * o, at, L_TAG, lw=0.8)
                    pl.line(xx + 3.2 * o, at, xx + 1.8 * o, at - 1.2, L_TAG, lw=0.8); pl.line(xx + 3.2 * o, at, xx + 1.8 * o, at + 1.2, L_TAG, lw=0.8)
            if "ST-" in d_.get("serves", ""):
                stair_exit[d_["serves"].split()[0]] = d_["id"]
                continue
            if d_["kind"] == "service":
                x_, y_ = pl.P(at - 3, by1 + 1.6)
                sh.text(x_, y_, "S1 SERVICE / LOADING · D-034 OPEN", size=5.2, bold=True, layer=L_TAG)
            elif w_ == "N":
                x_, y_ = pl.P(at + 2.2, by1 + 1.6)
                sh.text(x_, y_, f"{d_['id']} EXIT ONLY", size=5.4, bold=True, layer=L_TAG)
            elif w_ == "W":
                x_, y_ = pl.P(bx0 - 4.6, at + 12)
                sh.text(x_ + 0.03, y_, f"{d_['id']} EXIT ONLY", size=5.4, bold=True, align="center", layer=L_TAG, rot=90)
            elif w_ == "E":
                x_, y_ = pl.P(bx1 + 4.4, at)
                sh.text(x_, y_ - 0.03, f"{d_['id']} EXIT ONLY", size=5.4, bold=True, layer=L_TAG)
    else:
        for ob in lv["open_below"]:
            r = ob["rect"]
            pl.rect(r, L_HID, lw=0.5)
            for (xa, ya, xb, yb) in ((r[0], r[1], r[2], r[3]), (r[0], r[3], r[2], r[1])):
                for t0, t1 in ((0.0, 0.36), (0.64, 1.0)):
                    pl.dashed(xa + (xb - xa) * t0, ya + (yb - ya) * t0, xa + (xb - xa) * t1, ya + (yb - ya) * t1, L_HID, lw=0.25, dash=0.06, gap=0.06)
        pl.drect(floor, L_HID, lw=0.4, dash=0.05, gap=0.05)
        for b in up["bands"]:
            r = b["rect"]
            pl.rect(r, L_FIX, lw=0.9)
            t_ = f"UPPER ({b['side']}) · FIXED · {n(bys[b['side']]['upper'])} SEATS"
            if (r[2] - r[0]) >= (r[3] - r[1]):
                x_, y_ = pl.P(r[0] + 3, (r[1] + r[3]) / 2)
                sh.text(x_, y_ - 0.035, t_, size=5.6, bold=True, layer=L_TAG)
            else:
                x_, y_ = pl.P((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)
                sh.text(x_ + 0.035, y_, t_, size=5.6, bold=True, align="center", layer=L_TAG, rot=90)
        oba = next(o for o in lv["open_below"] if o["id"] == "ob_arena")["rect"]
        x_, y_ = pl.P((oba[0] + oba[2]) / 2, (oba[1] + oba[3]) / 2)
        sh.text(x_, y_ + 0.05, "OPEN TO ARENA BELOW", size=8, bold=True, align="center", layer=L_TAG)
        sh.text(x_, y_ - 0.10, "(event floor + telescopic lower tier, double height)", size=6, align="center", layer=L_TAG)
        obl = next(o for o in lv["open_below"] if o["id"] == "ob_lobby")["rect"]
        pl.tag(obl, ["OPEN TO LOBBY BELOW", "(hall of champions,", "double height)"], sizes=(6.4, 6.0, 5.5), bold_first=True, allow_rot=False)
        upper_drawn = sum(area(b["rect"]) for b in up["bands"])
        sched.append(("—", f"Upper tier, fixed ({n(tot['upper'])} seats)", upper_drawn, X_["sf"]["seating_upper"],
                      f"N {bys['N']['upper']} / S {bys['S']['upper']} / E {bys['E']['upper']}"))

    # rooms (stairs / elevator inside a room are subtracted from its drawn SF)
    mech_rooms = [r for r in plan["level_1"]["rooms"] if r["prog"] == "mechanical"]
    mech_drawn = sum(area(r["rect"]) for r in mech_rooms)
    vrects = [st_["rect"] for st_ in vert["stairs"]] + [vert["elevator"]["rect"]]
    for r in lv["rooms"]:
        pl.rect(r["rect"], L_ROOM, lw=0.9)
        a_ = area(r["rect"]) - sum(overlap(r["rect"], v) for v in vrects)
        if r["prog"] == "mechanical":
            ps = X_["M"] * area(r["rect"]) / mech_drawn
        elif r["prog"] is None:
            ps = None
        else:
            ps = X_["sf"][r["prog"]] * r.get("share", 1)
        note = r.get("note", "")
        extra = []
        if "fixtures" in r:
            wc, lav, ur = fixture_lines(X_, r["fixtures"])
            ps = (wc + lav) * prog["factors"]["restrooms"]["sf_per_fixture"]
            extra = [f"WC {wc} · LAV {lav}"]
            note = f"{wc + lav} fixtures (WC {wc}, LAV {lav}" + (f"; urinals ≤ {ur} of the WCs)" if ur is not None else ")")
        if r["id"] == "sc":
            note = "over boys locker + NW mech; ST-1 inside"
        if r["id"] == "xt":
            note = "over girls locker (D-030)"
        full = [f"{r['tag']}  {r['name']}", f"{n(a_)} SF"] + extra
        if not pl.tag(r["rect"], full, fallback=[f"{r['tag']}", f"{n(a_)}"]):
            pl.tag(r["rect"], [r["tag"]], sizes=(5.5, 5.0, 4.5))
        nm = r["name"].title().replace("(Nw)", "(NW)").replace("(Ne)", "(NE)").replace("(Sw)", "(SW)").replace("(Se)", "(SE)").replace("Mat", "Mat Area")
        sched.append((r["tag"], nm, a_, ps, note))
    for z in lv["zones"]:
        if z.get("vertical"):
            r = z["rect"]
            x_, y_ = pl.P((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)
            sz = 6.2
            while text_width_in(z["name"], sz, True) > (r[3] - r[1]) * s - 0.1 and sz > 4.5:
                sz -= 0.3
            sh.text(x_ + 0.03, y_, z["name"], size=sz, bold=True, align="center", layer=L_TAG, rot=90)
        else:
            lines = z["name"].replace(" / ", " /|").split("|")
            if z["id"] == "lobby":
                lines = lines + ["(double height)"]
            if z.get("sub"):
                lines = lines + z["sub"].split("|")
            pl.tag(z.get("label_rect", z["rect"]), lines, sizes=(6.4, 6.0, 5.5, 5.0, 4.6), allow_rot=False)
    for st in vert["stairs"]:
        r = st["rect"]
        pl.rect(r, L_VERT, lw=1.0)
        horiz = (r[2] - r[0]) > (r[3] - r[1])
        if horiz:
            my_ = (r[1] + r[3]) / 2
            pl.line(r[0] + 2, my_, r[2] - 2, my_, L_VERT, lw=0.4)
            for k in range(1, 6):
                xx = r[0] + 2 + k * (r[2] - r[0] - 4) / 6
                pl.line(xx, r[1], xx, r[3], L_VERT, lw=0.2)
        else:
            mxs = (r[0] + r[2]) / 2
            pl.line(mxs, r[1] + 2, mxs, r[3] - 2, L_VERT, lw=0.4)
            for k in range(1, 6):
                yy = r[1] + 2 + k * (r[3] - r[1] - 4) / 6
                pl.line(r[0], yy, r[2], yy, L_VERT, lw=0.2)
        cxs = (r[0] + r[2]) / 2
        x_, y_ = pl.P(cxs, by1 + 1.6) if r[1] > 100 else pl.P(cxs, by0 - 4.6)
        lab = st["id"] + (f" · {stair_exit[st['id']]} EXIT ONLY" if lvl == 1 and st["id"] in stair_exit else "")
        al_ = "center"
        if lvl == 1 and st["id"] == "ST-2":
            lab = st["id"]
        elif lvl == 1 and st["id"] in stair_exit:
            al_ = "right" if st["id"] == "ST-1" else "left"
            x_, y_ = pl.P(cxs - 2.2 if al_ == "right" else cxs + 2.2, by1 + 1.6 if r[1] > 100 else by0 - 4.6)
        sh.text(x_, y_, lab, size=5.6, bold=True, align=al_, layer=L_TAG)
    el = vert["elevator"]
    pl.rect(el["rect"], L_VERT, lw=1.0)
    pl.line(el["rect"][0], el["rect"][1], el["rect"][2], el["rect"][3], L_VERT, lw=0.4)
    pl.line(el["rect"][0], el["rect"][3], el["rect"][2], el["rect"][1], L_VERT, lw=0.4)
    ex_, ey_ = pl.P(el["rect"][0] - 0.8, (el["rect"][1] + el["rect"][3]) / 2)
    sh.text(ex_, ey_ - 0.03, "EL", size=5.6, bold=True, align="right", layer=L_TAG)

    if lvl == 1:
        x_, y_ = pl.P(bx1 + 4.4, 246.6)
        sh.text(x_, y_ - 0.03, f"{stair_exit.get('ST-2', '')} EXIT ONLY (ST-2)", size=5.4, bold=True, layer=L_TAG)
    nx, ny = pl.P(bx1 + 9, by1 - 52)
    sh.line(nx, ny, nx, ny + 0.55, layer=L_DIM, lw=1.1)
    sh.line(nx, ny + 0.55, nx - 0.09, ny + 0.36, layer=L_DIM, lw=1.1)
    sh.line(nx, ny + 0.55, nx + 0.09, ny + 0.36, layer=L_DIM, lw=1.1)
    sh.text(nx, ny + 0.62, "N", size=10, bold=True, align="center", layer=L_DIM)
    sh.text(nx, ny - 0.13, "APPROX.", size=5.6, align="center", layer=L_DIM)
    sh.text(nx, ny - 0.24, "SITE TBD", size=5.6, align="center", layer=L_DIM)
    gx0, gy0 = pl.P(bx1 + 4, by0 + 100)
    for a_, b_, k in ((0, 8, 0), (8, 16, 1), (16, 32, 2)):
        sh.rect(gx0 + a_ * s, gy0 - 0.30, (b_ - a_) * s, 0.06, layer=L_DIM, lw=0.6)
        if k != 1:
            sh.line(gx0 + a_ * s, gy0 - 0.30, gx0 + b_ * s, gy0 - 0.24, layer=L_DIM, lw=0.3)
    for v in (0, 8, 16, 32):
        sh.text(gx0 + v * s, gy0 - 0.42, f"{v}'", size=5.6, align="center", layer=L_DIM)
    sh.text(gx0, gy0 - 0.14, "GRAPHIC SCALE (FT)", size=5.6, layer=L_DIM)

    # ================= right panel =================
    rx = max(px0 + (bx1 - bx0) * s + 1.05, 9.35)
    rw = W - M - 0.22 - rx
    sh.line(rx - 0.2, body_bottom + 0.12, rx - 0.2, top, lw=0.5)
    y = top - 0.05
    sh.rect(rx, y - 0.42, rw, 0.42, lw=1.6)
    sh.text(rx + rw / 2, y - 0.29, pm["label"], size=14, bold=True, align="center")
    sh.text(rx, y - 0.68, f"LEVEL {lvl} — OVERALL FLOOR PLAN (REV C)", size=12, bold=True)
    sh.text(rx, y - 0.88, "scale 1/32\" = 1'-0\" on 17 x 11 in · north approximate, road assumed south, site TBD", size=7.8)
    y -= 1.18
    sh.text(rx, y, "LEGEND", size=9.5, bold=True)
    y -= 0.05
    if lvl == 1:
        leg = [("box", f"Lower tier, TELESCOPIC (extended, {lo['rows']} rows x 24 in; {X_['seat_sf_lower']:.2f} SF/seat) — D-009"),
               ("mat", "42' wrestling mat (4, 2 x 2)"), ("court", "84' x 50' court + 10' runout (overlay)"),
               ("dash", "Portal / vomitory through the telescopic tier (V1, V2)"),
               ("exit", "X# = EXIT ONLY — alarmed, no exterior entry hardware (symbol; width not drawn)"),
               ("svc", "S1 = SERVICE / LOADING door (staff-controlled, not a people entrance; D-034 OPEN)"),
               ("ck", "Security checkpoint zone (size TBD) · CD-1 controlled door (staff / teams)")]
    else:
        leg = [("box", f"Upper tier, FIXED ({X_['seat_sf_upper']:.1f} SF/seat) on the Level 2 deck — D-009"),
               ("open", "Open to below (arena; lobby double height)")]
    leg += [("box", "Room block (tag number + drawn SF)"), ("stair", "Stair (4) / elevator (X), same position on both levels")]
    for kind, t_ in leg:
        y -= 0.165
        lx = rx + 0.05
        if kind == "dash":
            sh.dashed(lx, y + 0.04, lx + 0.4, y + 0.04, lw=0.6, dash=0.04, gap=0.03)
        elif kind in ("box", "mat"):
            sh.rect(lx + 0.08, y - 0.03, 0.24, 0.14, lw=1.0)
        elif kind == "court":
            sh.dashed(lx, y + 0.04, lx + 0.4, y + 0.04, lw=0.7, dash=0.07, gap=0.04)
        elif kind == "open":
            sh.rect(lx + 0.08, y - 0.03, 0.24, 0.14, lw=0.5); sh.line(lx + 0.08, y - 0.03, lx + 0.32, y + 0.11, lw=0.25)
        elif kind == "exit":
            sh.line(lx + 0.08, y + 0.04, lx + 0.24, y + 0.04, lw=3.0); sh.line(lx + 0.16, y + 0.04, lx + 0.16, y + 0.14, lw=0.8)
            sh.line(lx + 0.16, y + 0.14, lx + 0.12, y + 0.10, lw=0.8); sh.line(lx + 0.16, y + 0.14, lx + 0.20, y + 0.10, lw=0.8)
        elif kind == "svc":
            sh.line(lx + 0.08, y + 0.04, lx + 0.24, y + 0.04, lw=3.0)
        elif kind == "ck":
            sh.dashed(lx + 0.02, y - 0.03, lx + 0.30, y - 0.03, lw=0.9, dash=0.05, gap=0.03); sh.dashed(lx + 0.02, y + 0.11, lx + 0.30, y + 0.11, lw=0.9, dash=0.05, gap=0.03)
            sh.line(lx + 0.40, y - 0.04, lx + 0.40, y + 0.12, lw=2.4)
        elif kind == "stair":
            sh.rect(lx + 0.08, y - 0.03, 0.12, 0.14, lw=1.0); sh.rect(lx + 0.24, y - 0.03, 0.12, 0.14, lw=1.0)
            sh.line(lx + 0.24, y - 0.03, lx + 0.36, y + 0.11, lw=0.4)
        sh.text(lx + 0.55, y, t_, size=7.2)
    y -= 0.30
    sh.text(rx, y, f"ROOM SCHEDULE — LEVEL {lvl} (drawn vs locked program, P2-G-003 Rev E)", size=9.5, bold=True)
    hdr = [("TAG", 0, "l"), ("ROOM", 0.36, "l"), ("DRAWN SF", 2.65, "r"), ("PROGRAM", 3.35, "r"), ("NOTE", 3.5, "l")]
    rp = 0.138
    y -= rp
    for lab, dx, al in hdr:
        sh.text(rx + dx, y + 0.02, lab, size=6.8, bold=True, align="left" if al == "l" else "right", layer=TB)
    sh.line(rx, y - 0.04, rx + rw, y - 0.04, layer=TB, lw=0.6)
    for tg, nm, a_, ps, note in sched:
        y -= rp
        while text_width_in(note, 6.4) > rw - 3.52 and len(note) > 4:
            note = note[:-2].rstrip() + "…"
        for (lab, dx, al), c in zip(hdr, [tg, nm, n(a_), "—" if ps is None else n(ps), note]):
            sh.text(rx + dx, y, c, size=6.4 if lab == "NOTE" else 7.0, align="left" if al == "l" else "right", layer=TB)
    sh.line(rx, y - 0.05, rx + rw, y - 0.05, layer=TB, lw=0.4)
    lv2 = plan["level_2"]
    fp = area(plan["building"]["rect"])
    l2_drawn = fp - sum(area(o["rect"]) for o in lv2["open_below"])
    cap = p2["building"]["footprint_cap_sf"]
    y -= 0.06
    sh.text(rx, y - 0.16, "AREA CHECK", size=9.0, bold=True)
    y -= 0.18
    team = next(z for z in plan["level_1"]["zones"] if z["id"] == "team_asm")
    sw = next(r for r in plan["level_1"]["rooms"] if r["id"] == "storage_sw")
    if lvl == 1:
        txt = (f"Box {bx1 - bx0:g} x {by1 - by0:g} ft = {n(fp)} SF (unchanged): {n(cap - fp)} SF under the {n(cap)} cap (target ≥ 2,000). "
               f"Program unchanged, P2-G-003 Rev E stands (footprint {n(X_['F'])}). Seats {n(tot['lower'])} + {n(tot['upper'])} = {n(tot['total'])} "
               f"(N {bys['N']['total']}, S {bys['S']['total']}, E {bys['E']['total']}); V1/V2 moved, same widths. Mech drawn {n(mech_drawn)} vs "
               f"{n(X_['M'])} (exit passages N + E). Unprogrammed: team assembly ≈ {n(area(team['rect']))} SF, storage (SW) {n(area(sw['rect']))} SF.")
    else:
        txt = (f"Drawn L2 floor {n(l2_drawn)} SF (box minus open-to-below) vs program L2 gross {n(X_['L2'])}; the extra is the "
               f"corridor, walkways and balcony. Total drawn ≈ {n(fp + l2_drawn)} vs {n(X_['G'])} program GSF. Level 2 unchanged from Rev B "
               f"except notes: the 4 stairs discharge at L1 through EXIT ONLY doors X4, X6, X9, X10.")
    y = sh.para(rx, y, rw, txt, size=6.9)
    sh.text(rx, y - 0.14, "ACCESS CONTROL + EGRESS (D-033 DECIDED; layout ASSUMED)", size=9.0, bold=True)
    y -= 0.16
    acc1 = ["ONE WAY IN for public, teams and staff: E1 grand entrance → security checkpoint (size TBD) → lobby. Teams then go west "
            "through CD-1 (controlled door) along the athlete route to team assembly, the athlete corridor and lockers. SW entry removed.",
            "X1-X10 EXIT ONLY — alarmed, no exterior entry hardware. Egress side opens without a key or special knowledge (IBC 2021 1010.2; "
            "2018 1010.1.9); panic hardware only (1010.2.9); stair discharge doors lock from outside only (1010.2.7 exc. 1). Delayed "
            "egress is not allowed in Group A (1010.2.13): alarm only, no delay.",
            "Count: > 1,000 occupants per story → 4 exits (T1006.3.3); L1 = E1 + X1-X10, L2 = 4 stairs (R-015). Main exit ≥ 1/2 of "
            "the occupant load, fronting a street (1030.2); other exits ≥ 1/2 (1030.3). Seats alone: E1 ≥ 1,100 x 0.15 in = 165 in "
            "clear (1005.3.2 exc. 1, sprinklers + EVACS per R-015); final load TBD (R-007).",
            "Checkpoint must not narrow the main exit (1003.6; turnstiles 1010.5). S1 service / loading: deliveries and buses OPEN (D-034)."]
    acc2 = ["Single controlled entry (D-033): everyone enters at the L1 grand entrance (E1) through the security checkpoint; no "
            "entry from Level 2. The 4 stairs discharge at L1 through EXIT ONLY doors (alarmed, no exterior entry hardware).",
            "IBC 2021 (Alabama), Group A-4 ASSUMED (R-007): egress doors open from the egress side without a key or special knowledge "
            "(1010.2; 2018 1010.1.9); panic hardware only on Group A doors serving 50+ (1010.2.9; 2018 1010.1.10); stair discharge doors "
            "may lock from the outside only (1010.2.7 exc. 1); delayed egress not permitted in Group A (1010.2.13), so alarm only.",
            "Exits: 4 per story above 1,000 occupants (T1006.3.3); stairs 4 x 65 in at 0.2 in/occupant (1005.3.1 exc. 1, R-015). "
            "Assembly main exit ≥ 1/2 of the occupant load (1030.2); other exits ≥ 1/2 (1030.3). Electric locks only per 1010.2.11 / "
            "1010.2.12. Checkpoint equipment may not reduce exit width (1003.6, 1010.5). Final occupant load + widths → architect (R-007).",
            "Admin now sits over the SW storage / team assembly (the team entry is gone)."]
    for t_ in (acc1 if lvl == 1 else acc2):
        y = sh.para(rx, y + 0.02, rw, t_, size=6.6, indent=0.12, bullet="·")
    if lvl == 2:
        sh.text(rx, y - 0.14, "LAYOUT NOTES (KEYSTONE, ASSUMED — architect to confirm)", size=9.0, bold=True)
        y -= 0.16
    notes1 = ["Layout (ASSUMED): exit passages N + E line up with V1 / V2; event lockers open onto them. Exit separation, travel distance, sightlines NOT checked."]
    notes2 = ["S&C + cross-training on Level 2 over the lockers (D-030); upper tier 15 ft on N, S, E; restrooms stacked over L1's. Suites PARKED.",
              "Exit separation, travel distance, sightlines and structure NOT checked. Floor-to-floor 15 ft ASSUMED."]
    for t_ in (notes1 if lvl == 1 else notes2):
        y = sh.para(rx, y + 0.02, rw, t_, size=6.6, indent=0.12, bullet="·")
    y = sh.para(rx, y - 0.02, rw, "Sources: phase2.yaml (D-009, D-030, D-031, D-033); Shane 2026-10-04 4:30 + 4:43 AM CT; P2-G-003 Rev E; R-005, R-008, "
                "R-009, R-012, R-014, R-015; IBC 2021 Ch. 10 (UpCodes, Alabama, retrieved 2026-10-04). Geometry: params/phase2_plan_rev_c.yaml.", size=6.3)
    fl = body_bottom + 0.08
    if y < fl:
        raise SystemExit(f"LAYOUT OVERFLOW: right panel runs {fl - y:.2f} in into the stamp band")
    print(f"layout margin right panel (in): {y - fl:.2f}")
    return sh



def build_d(sheet_no, p2, prog, plan, X_, seats, lg):
    """Rev D (Shane 2026-10-04 4:55 AM CT, D-035): continuous Level 2 running / training loop; S&C + cross-training trimmed."""
    lvl = LEVEL_OF[sheet_no]
    meta2 = p2["meta"]
    pm = plan["meta"]
    rows, tot = seats
    bys = {r["side"]: r for r in rows}
    sh = Sheet(W, H)
    body_bottom = add_titleblock(sh, {
        "project": f"{meta2['project']}\n{meta2['arena_name']} · {meta2['location']}",
        "phase": "PHASE 2",
        "title": f"OVERALL FLOOR PLAN\nLEVEL {lvl} · BLOCK PLAN",
        "scale": "1/32\" = 1'-0\"",
        "date": meta2["sheet_date"],
        "revision": "D",
        "drawn_by": meta2["drawn_by"],
        "sheet_no": sheet_no,
        "stamp": meta2["stamp"],
    }, margin=M, tb_h=0.95, stamp_h=0.40)
    top = H - M - 0.12
    s = 1.0 / pm["scale_ft_per_in"]
    bx0, by0, bx1, by1 = plan["building"]["rect"]
    px0, py0 = M + 0.62, body_bottom + 0.50
    pl = Plan(sh, px0, py0, s)
    floor = plan["event_floor"]["rect"]
    av = plan["arena_volume"]["rect"]
    lv = plan["level_1"] if lvl == 1 else plan["level_2"]
    vert = plan["vertical"]
    axis = plan["entry_axis_x"]["value"]
    sched = []
    probs = check_overlaps(lv, vert)
    lvr = [st_["rect"] for st_ in vert["stairs"]] + [vert["elevator"]["rect"]]
    probs += [f"loop {k_} x stair/elevator {v_}" for k_, leg in lg["legs"].items() for v_ in lvr if overlap(leg, v_) > 0.01]
    probs += [f"loop {k_} x room {r_['id']}" for k_, leg in lg["legs"].items() for r_ in plan["level_2"]["rooms"] if overlap(leg, r_["rect"]) > 0.01]
    if probs:
        raise SystemExit(f"ROOM OVERLAP on level {lvl}: {probs}")


    pj = plan["building"]["projection"]["rect"]
    outline = [(bx0, by0), (bx1, by0), (bx1, pj[3]), (pj[0], pj[3]), (pj[0], by1), (bx0, by1), (bx0, by0)]
    for (xa, ya), (xb, yb) in zip(outline[:-1], outline[1:]):
        pl.line(xa, ya, xb, yb, L_WALL, lw=2.2)
    fp = area(plan["building"]["rect"]) + area(pj)
    yd = by0 - 9
    pl.line(bx0, yd, bx1, yd, L_DIM, lw=0.4)
    for xx in (bx0, bx1):
        pl.line(xx, yd - 2.5, xx, yd + 2.5, L_DIM, lw=0.4)
    tx, ty = pl.P((bx0 + bx1) / 2, yd)
    sh.text(tx, ty - 0.14, f"{bx1 - bx0:g}'-0\"  (building {bx1 - bx0:g} x {by1 - by0:g} ft + {pj[2] - pj[0]:g} x {pj[3] - pj[1]:g} ft NE stair tower = {n(fp)} SF footprint)", size=7, align="center", layer=L_DIM)
    xd = bx0 - 9
    pl.line(xd, by0, xd, by1, L_DIM, lw=0.4)
    for yy in (by0, by1):
        pl.line(xd - 2.5, yy, xd + 2.5, yy, L_DIM, lw=0.4)
    tx, ty = pl.P(xd, (by0 + by1) / 2)
    sh.text(tx - 0.06, ty, f"{by1 - by0:g}'-0\"", size=7, align="center", layer=L_DIM, rot=90)

    lo, up = plan["tiers"]["lower"], plan["tiers"]["upper"]
    names = {"N": "N", "S": "S", "E": "E"}
    if lvl == 1:
        pl.rect(av, L_FIX, lw=0.9)
        pl.rect(floor, L_MAT, lw=1.4)
        fx0, fy0, fx1, fy1 = floor
        for b in lo["bands"]:
            r = b["rect"]
            pl.rect(r, L_TEL, lw=0.9)
            horiz = (r[2] - r[0]) >= (r[3] - r[1])
            ops = [o["rect"] for o in lo["openings"] if o["side"] == b["side"]]
            # back-half row lines (rows 4-6), broken at openings; label in the front half
            for k in range(lo["rows"] // 2, lo["rows"]):
                dk = k * lo["row_depth_ft"]
                if horiz:
                    yy = r[1] + dk if b["side"] == "N" else r[3] - dk
                    xs = [r[0]] + sum(([o[0], o[2]] for o in sorted(ops)), []) + [r[2]]
                    for a_, b_ in zip(xs[0::2], xs[1::2]):
                        pl.line(a_, yy, b_, yy, L_TEL, lw=0.2)
                else:
                    xx = r[0] + dk
                    ys = [r[1]] + sum(([o[1], o[3]] for o in sorted(ops, key=lambda o: o[1])), []) + [r[3]]
                    for a_, b_ in zip(ys[0::2], ys[1::2]):
                        pl.line(xx, a_, xx, b_, L_TEL, lw=0.2)
            t_ = f"LOWER ({b['side']}) · TELESCOPIC · {n(bys[b['side']]['lower'])} SEATS"
            if horiz:
                yy = r[1] + 2.4 if b["side"] == "N" else r[3] - 3.6
                x_lab = r[0] + 2.5 if b["side"] == "N" else lo["openings"][0]["rect"][2] + 3   # S: east of the portal
                x_, y_ = pl.P(x_lab, yy)
                sh.text(x_, y_ - 0.035, t_, size=5.2, bold=True, layer=L_TAG)
            else:
                x_, y_ = pl.P(r[0] + 3.4, (r[1] + r[3]) / 2 - 22)
                sh.text(x_ + 0.035, y_, t_, size=5.2, bold=True, align="center", layer=L_TAG, rot=90)
        for o in lo["openings"]:
            pl.drect(o["rect"], L_ROOM, lw=0.5, dash=0.04, gap=0.03)
            r = o["rect"]
            horiz = (r[2] - r[0]) < (r[3] - r[1])           # openings run through the band
            x_, y_ = pl.P((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)
            if o["id"] == "PORTAL":
                sh.text(x_, y_ + 0.0, "PORTAL", size=4.8, bold=True, align="center", layer=L_TAG)
            else:
                sh.text(x_, y_ - 0.03, o["id"], size=5.0, bold=True, align="center", layer=L_TAG)
        mft = p2["spaces"]["arena"]["mat_ft"]
        for m in plan["mats"]:
            mx, my = m["origin"]
            pl.rect((mx, my, mx + mft, my + mft), L_MAT, lw=1.0)
            left = mx + mft / 2 < (floor[0] + floor[2]) / 2
            x_, y_ = pl.P(mx + 2 if left else mx + mft - 2, my + mft - 2.5)
            sh.text(x_, y_ - 0.09, m["id"], size=6.2, bold=True, align="left" if left else "right", layer=L_TAG)
        cr = plan["court"]["rect"]
        ro = plan["court"]["runout_ft"]
        pl.drect(cr, L_CORT, lw=0.7, dash=0.07, gap=0.04)
        pl.drect((cr[0] - ro, cr[1] - ro, cr[2] + ro, cr[3] + ro), L_CORT, lw=0.35, dash=0.03, gap=0.04)
        pl.dashed(cr[0], (cr[1] + cr[3]) / 2, cr[2], (cr[1] + cr[3]) / 2, L_CORT, lw=0.4, dash=0.07, gap=0.04)
        x_, y_ = pl.P((fx0 + fx1) / 2, fy1 - 6)
        sh.text(x_, y_, f"EVENT FLOOR {fx1 - fx0:g}' x {fy1 - fy0:g}' = {n(area(floor))} SF", size=6.6, bold=True, align="center", layer=L_TAG)
        sh.text(x_, y_ - 0.12, "table / bench zone (15')", size=5.4, align="center", layer=L_TAG)
        x_, y_ = pl.P((fx0 + fx1) / 2, fy0 + 7.5)
        sh.text(x_, y_, "table / bench zone (15')", size=5.4, align="center", layer=L_TAG)
        x_, y_ = pl.P((cr[0] + cr[2]) / 2, (cr[1] + cr[3]) / 2 + 2.5)
        sh.text(x_, y_, "COURT 84' x 50' (OVERLAY)", size=5.4, align="center", layer=L_TAG)
        lower_drawn = sum(area(b["rect"]) for b in lo["bands"])
        sched.append(("—", "Event floor (D-030 locked)", area(floor), X_["sf"]["arena"], "114' x 144'"))
        sched.append(("—", f"Lower tier, telescopic ({n(tot['lower'])} seats)", lower_drawn, X_["sf"]["seating_lower"],
                      f"{lo['rows']} rows; N {bys['N']['lower']} / S {bys['S']['lower']} / E {bys['E']['lower']}"))
        # team side / public side walls (Rev C): team assembly vs west concourse, athlete route vs west concourse
        pl.line(56, 34, 56, 48, L_ROOM, lw=0.9)
        pl.line(56, 48, 84, 48, L_ROOM, lw=0.9)
        # single controlled entry (D-033): entry arrow on the axis
        pl.line(axis, -6, axis, 0, L_DIM, lw=1.0)
        pl.line(axis, 0, axis - 1.8, -2.6, L_DIM, lw=1.0); pl.line(axis, 0, axis + 1.8, -2.6, L_DIM, lw=1.0)
        x_, y_ = pl.P(axis - 3, -5.2)
        sh.text(x_, y_, "ARENA N-S AXIS · ROAD ASSUMED SOUTH", size=5.6, align="right", layer=L_TAG)
        x_, y_ = pl.P(axis + 3, -5.2)
        sh.text(x_, y_, "E1 MAIN ENTRY / EXIT (D-033)", size=6.0, bold=True, layer=L_TAG)
        # security checkpoint (location only; size TBD)
        ck = lv["checkpoint"]
        pl.drect(ck["rect"], L_TAG, lw=0.9, dash=0.06, gap=0.035)
        x_, y_ = pl.P((ck["rect"][0] + ck["rect"][2]) / 2, (ck["rect"][1] + ck["rect"][3]) / 2)
        sh.text(x_, y_ + 0.015, "SECURITY CHECKPOINT", size=5.0, bold=True, align="center", layer=L_TAG)
        sh.text(x_, y_ - 0.085, "— size TBD (ASSUMED)", size=5.0, align="center", layer=L_TAG)
        # controlled door off the lobby to the athlete route
        cdx, cdy = lv["controlled_door"]["at"]
        pl.line(cdx, cdy - 4, cdx, cdy + 4, L_TAG, lw=2.4)
        x_, y_ = pl.P(cdx + 1.2, cdy - 7.2)
        sh.text(x_, y_, "CD-1 CONTROLLED DOOR", size=5.0, bold=True, layer=L_TAG)
        sh.text(x_, y_ - 0.08, "(staff / teams)", size=4.8, layer=L_TAG)
        # perimeter doors: symbols only (widths not drawn)
        stair_exit = {}
        for d_ in lv["doors"]["items"]:
            w_, at = d_["wall"], d_["at"]
            if d_["kind"] == "main":
                continue
            if w_ in ("N", "S"):
                yy = by1 if w_ == "N" else by0
                pl.line(at - 2.5, yy, at + 2.5, yy, L_TAG, lw=3.0)
                o = 1 if w_ == "N" else -1
                if d_["kind"] == "exit":
                    pl.line(at, yy, at, yy + 3.2 * o, L_TAG, lw=0.8)
                    pl.line(at, yy + 3.2 * o, at - 1.2, yy + 1.8 * o, L_TAG, lw=0.8); pl.line(at, yy + 3.2 * o, at + 1.2, yy + 1.8 * o, L_TAG, lw=0.8)
            else:
                xx = bx0 if w_ == "W" else bx1
                pl.line(xx, at - 2.5, xx, at + 2.5, L_TAG, lw=3.0)
                o = -1 if w_ == "W" else 1
                if d_["kind"] == "exit":
                    pl.line(xx, at, xx + 3.2 * o, at, L_TAG, lw=0.8)
                    pl.line(xx + 3.2 * o, at, xx + 1.8 * o, at - 1.2, L_TAG, lw=0.8); pl.line(xx + 3.2 * o, at, xx + 1.8 * o, at + 1.2, L_TAG, lw=0.8)
            if "ST-" in d_.get("serves", ""):
                stair_exit[d_["serves"].split()[0]] = d_["id"]
                continue
            if d_["kind"] == "service":
                x_, y_ = pl.P(at - 3, by1 + 1.6)
                sh.text(x_, y_, "S1 SERVICE / LOADING · D-034 OPEN", size=5.2, bold=True, layer=L_TAG)
            elif w_ == "N":
                x_, y_ = pl.P(at + 2.2, by1 + 1.6)
                sh.text(x_, y_, f"{d_['id']} EXIT ONLY", size=5.4, bold=True, layer=L_TAG)
            elif w_ == "W":
                x_, y_ = pl.P(bx0 - 4.6, at + 12)
                sh.text(x_ + 0.03, y_, f"{d_['id']} EXIT ONLY", size=5.4, bold=True, align="center", layer=L_TAG, rot=90)
            elif w_ == "E":
                x_, y_ = pl.P(bx1 + 4.4, at)
                sh.text(x_, y_ - 0.03, f"{d_['id']} EXIT ONLY", size=5.4, bold=True, layer=L_TAG)
    else:
        for ob in lv["open_below"]:
            r = ob["rect"]
            pl.rect(r, L_HID, lw=0.5)
            for (xa, ya, xb, yb) in ((r[0], r[1], r[2], r[3]), (r[0], r[3], r[2], r[1])):
                for t0, t1 in ((0.0, 0.36), (0.64, 1.0)):
                    pl.dashed(xa + (xb - xa) * t0, ya + (yb - ya) * t0, xa + (xb - xa) * t1, ya + (yb - ya) * t1, L_HID, lw=0.25, dash=0.06, gap=0.06)
        pl.drect(floor, L_HID, lw=0.4, dash=0.05, gap=0.05)
        for b in up["bands"]:
            r = b["rect"]
            pl.rect(r, L_FIX, lw=0.9)
            t_ = f"UPPER ({b['side']}) · FIXED · {n(bys[b['side']]['upper'])} SEATS"
            if (r[2] - r[0]) >= (r[3] - r[1]):
                x_, y_ = pl.P(r[0] + 3, (r[1] + r[3]) / 2)
                sh.text(x_, y_ - 0.035, t_, size=5.6, bold=True, layer=L_TAG)
            else:
                x_, y_ = pl.P((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)
                sh.text(x_ + 0.035, y_, t_, size=5.6, bold=True, align="center", layer=L_TAG, rot=90)
        oba = next(o for o in lv["open_below"] if o["id"] == "ob_arena")["rect"]
        x_, y_ = pl.P((oba[0] + oba[2]) / 2, (oba[1] + oba[3]) / 2)
        sh.text(x_, y_ + 0.05, "OPEN TO ARENA BELOW", size=8, bold=True, align="center", layer=L_TAG)
        sh.text(x_, y_ - 0.10, "(event floor + telescopic lower tier, double height)", size=6, align="center", layer=L_TAG)
        obl = next(o for o in lv["open_below"] if o["id"] == "ob_lobby")["rect"]
        pl.tag(obl, ["OPEN TO LOBBY BELOW", "(hall of champions,", "double height)"], sizes=(6.4, 6.0, 5.5), bold_first=True, allow_rot=False)
        upper_drawn = sum(area(b["rect"]) for b in up["bands"])
        sched.append(("—", f"Upper tier, fixed ({n(tot['upper'])} seats)", upper_drawn, X_["sf"]["seating_upper"],
                      f"N {bys['N']['upper']} / S {bys['S']['upper']} / E {bys['E']['upper']}"))
        # ---- Level 2 running / training loop (D-035) ----
        lp = lv["loop"]
        lo_, li_ = lp["outer"], lp["inner"]
        pl.rect(lo_, L_LOOP, lw=1.3)
        pl.rect(li_, L_LOOP, lw=0.7)
        w2 = lp["width_ft"] / 2
        cl = [lo_[0] + w2, lo_[1] + w2, lo_[2] - w2, lo_[3] - w2]
        # lane line (2 lanes -> one line on the centerline), broken where the leg labels sit
        legtxt = {"S": (f"LOOP (S) · UPPER CONCOURSE / HALL OF CHAMPIONS BALCONY · 2 LANES x {lp['lane_width_in']} IN = {lp['width_ft']:g} FT", 115),
                  "N": (f"LOOP (N) · REAR CONCOURSE ON EVENT DAYS · 2 LANES x {lp['lane_width_in']} IN", 110),
                  "E": (f"LOOP (E) · 2 LANES x {lp['lane_width_in']} IN = {lp['width_ft']:g} FT", 140),
                  "W": ("LOOP (W) · NEW LEG (D-035)", 105)}
        szl = 4.6
        gaps = {}
        for k_, (t_, c_) in legtxt.items():
            half = (text_width_in(t_, szl, True) / s) / 2 + 2
            gaps[k_] = (c_ - half, c_ + half)
            if k_ in ("N", "S"):
                x_, y_ = pl.P(c_, cl[1] if k_ == "S" else cl[3])
                sh.text(x_, y_ - 0.022, t_, size=szl, bold=True, align="center", layer=L_LOOP)
            else:
                x_, y_ = pl.P(cl[0] if k_ == "W" else cl[2], c_)
                sh.text(x_ + 0.022, y_, t_, size=szl, bold=True, align="center", layer=L_LOOP, rot=90)
        for k_, (a0, a1, fixed, horiz) in {"S": (cl[0], cl[2], cl[1], True), "N": (cl[0], cl[2], cl[3], True),
                                            "W": (cl[1], cl[3], cl[0], False), "E": (cl[1], cl[3], cl[2], False)}.items():
            g0, g1 = gaps[k_]
            for u0, u1 in ((a0, g0), (g1, a1)):
                if horiz:
                    pl.dashed(u0, fixed, u1, fixed, L_LOOP, lw=0.35, dash=0.06, gap=0.04)
                else:
                    pl.dashed(fixed, u0, fixed, u1, L_LOOP, lw=0.35, dash=0.06, gap=0.04)
        # guards at open edges (IBC 1015.2 / 1015.3)
        for g_ in lp["guards"]:
            xa, ya, xb, yb = g_["line"]
            pl.line(xa, ya, xb, yb, L_GRD, lw=2.0)
        gw = next(g_ for g_ in lp["guards"] if g_["id"] == "G-W")["line"]
        x_, y_ = pl.P(gw[0] + 2.2, (gw[1] + gw[3]) / 2 + 40)
        sh.text(x_ + 0.03, y_, "42 IN GUARD (IBC 1015.2, 1015.3)", size=4.8, bold=True, align="center", layer=L_GRD, rot=90)
        gs = next(g_ for g_ in lp["guards"] if g_["id"] == "G-S")["line"]
        x_, y_ = pl.P((gs[0] + gs[2]) / 2, gs[1] - 2.6)
        sh.text(x_, y_, "42 IN GUARD (IBC 1015)", size=4.8, bold=True, align="center", layer=L_GRD)
        # event-day crossings at the upper-tier entries (locations ASSUMED: mid-side)
        for (xa, ya, xb, yb) in ((172, li_[3], 172, lo_[3]), (172, lo_[1], 172, li_[1]), (li_[2], 100, lo_[2], 100)):
            pl.line(xa, ya, xb, yb, L_TAG, lw=0.6)
            if xa == xb:
                for yy_, o_ in ((ya, 1), (yb, -1)):
                    pl.line(xa, yy_, xa - 1, yy_ + 1.4 * o_, L_TAG, lw=0.6); pl.line(xa, yy_, xa + 1, yy_ + 1.4 * o_, L_TAG, lw=0.6)
            else:
                for xx_, o_ in ((xa, 1), (xb, -1)):
                    pl.line(xx_, ya, xx_ + 1.4 * o_, ya - 1, L_TAG, lw=0.6); pl.line(xx_, ya, xx_ + 1.4 * o_, ya + 1, L_TAG, lw=0.6)
        x_, y_ = pl.P(170, li_[3] - 3.2)
        sh.text(x_, y_, "event-day crossing (typ.)", size=4.4, align="right", layer=L_TAG)
        sn = next(z for z in lv["zones"] if z["id"] == "stretch_n")["rect"]
        x_, y_ = pl.P((sn[0] + sn[2]) / 2, (sn[1] + sn[3]) / 2)
        sh.text(x_, y_ - 0.02, f"STRETCH / WARM-UP STRIP (N) · {sn[3] - sn[1]:g} FT · ASSUMED", size=4.4, bold=True, align="center", layer=L_TAG)
        # loop summary in the arena void
        oba_ = next(o for o in lv["open_below"] if o["id"] == "ob_arena")["rect"]
        x_, y_ = pl.P((oba_[0] + oba_[2]) / 2, (oba_[1] + oba_[3]) / 2 - 22)
        sh.text(x_, y_ + 0.05, "CONTINUOUS RUNNING / TRAINING LOOP (D-035)", size=7.0, bold=True, align="center", layer=L_LOOP)
        sh.text(x_, y_ - 0.09, f"centerline {lg['cx']:g}' x {lg['cy']:g}' = {n(lg['centerline'])} FT · 5,280 / {n(lg['centerline'])} = {lg['laps_per_mile']:.2f} LAPS / MILE",
                size=6.0, align="center", layer=L_LOOP)
        sh.text(x_, y_ - 0.21, f"{lp['lanes']} lanes x {lp['lane_width_in']} in = {lp['width_ft']:g} ft all around · squared corners · {n(lg['area'])} SF",
                size=6.0, align="center", layer=L_LOOP)
        sh.text(x_, y_ - 0.33, "non-event days: training · event days: upper concourse (spectators cross at tier entries)",
                size=5.6, align="center", layer=L_LOOP)
        sched.append(("—", "Running / training loop", lg["area"], X_["loop"], f"{lp['lanes']} x {lp['lane_width_in']} in; {n(lg['centerline'])} ft CL; {lg['laps_per_mile']:.2f} laps/mi"))

    # rooms (stairs / elevator inside a room are subtracted from its drawn SF)
    mech_rooms = [r for r in plan["level_1"]["rooms"] if r["prog"] == "mechanical"]
    mech_drawn = sum(area(r["rect"]) for r in mech_rooms)
    vrects = [st_["rect"] for st_ in vert["stairs"]] + [vert["elevator"]["rect"]]
    for r in lv["rooms"]:
        pl.rect(r["rect"], L_ROOM, lw=0.9)
        a_ = area(r["rect"]) - sum(overlap(r["rect"], v) for v in vrects)
        if r["prog"] == "mechanical":
            ps = X_["M"] * area(r["rect"]) / mech_drawn
        elif r["prog"] is None:
            ps = None
        else:
            ps = X_["sf"][r["prog"]] * r.get("share", 1)
        note = r.get("note", "")
        extra = []
        if "fixtures" in r:
            wc, lav, ur = fixture_lines(X_, r["fixtures"])
            ps = (wc + lav) * prog["factors"]["restrooms"]["sf_per_fixture"]
            extra = [f"WC {wc} · LAV {lav}"]
            note = f"{wc + lav} fixtures (WC {wc}, LAV {lav}" + (f"; urinals ≤ {ur} of the WCs)" if ur is not None else ")")
        if r["id"] == "sc":
            note = "trimmed 7 ft for the loop (D-035, was 6,000); ST-1 inside"
        if r["id"] == "xt":
            note = "trimmed 7 ft for the loop (D-035, was 4,000)"
        full = [f"{r['tag']}  {r['name']}", f"{n(a_)} SF"] + extra
        if not pl.tag(r["rect"], full, fallback=[f"{r['tag']}", f"{n(a_)}"]):
            pl.tag(r["rect"], [r["tag"]], sizes=(5.5, 5.0, 4.5))
        nm = r["name"].title().replace("(Nw)", "(NW)").replace("(Ne)", "(NE)").replace("(Sw)", "(SW)").replace("(Se)", "(SE)").replace("Mat", "Mat Area")
        sched.append((r["tag"], nm, a_, ps, note))
    for z in lv["zones"]:
        if z["id"] == "stretch_n":
            continue
        if z.get("vertical"):
            r = z["rect"]
            x_, y_ = pl.P((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)
            sz = 6.2
            while text_width_in(z["name"], sz, True) > (r[3] - r[1]) * s - 0.1 and sz > 4.5:
                sz -= 0.3
            sh.text(x_ + 0.03, y_, z["name"], size=sz, bold=True, align="center", layer=L_TAG, rot=90)
        else:
            lines = z["name"].replace(" / ", " /|").split("|")
            if z["id"] == "lobby":
                lines = lines + ["(double height)"]
            if z.get("sub"):
                lines = lines + z["sub"].split("|")
            pl.tag(z.get("label_rect", z["rect"]), lines, sizes=(6.4, 6.0, 5.5, 5.0, 4.6), allow_rot=False)
    for st in vert["stairs"]:
        r = st["rect"]
        pl.rect(r, L_VERT, lw=1.0)
        horiz = (r[2] - r[0]) > (r[3] - r[1])
        if horiz:
            my_ = (r[1] + r[3]) / 2
            pl.line(r[0] + 2, my_, r[2] - 2, my_, L_VERT, lw=0.4)
            for k in range(1, 6):
                xx = r[0] + 2 + k * (r[2] - r[0] - 4) / 6
                pl.line(xx, r[1], xx, r[3], L_VERT, lw=0.2)
        else:
            mxs = (r[0] + r[2]) / 2
            pl.line(mxs, r[1] + 2, mxs, r[3] - 2, L_VERT, lw=0.4)
            for k in range(1, 6):
                yy = r[1] + 2 + k * (r[3] - r[1] - 4) / 6
                pl.line(r[0], yy, r[2], yy, L_VERT, lw=0.2)
        cxs = (r[0] + r[2]) / 2
        x_, y_ = pl.P(cxs, max(by1, r[3]) + 1.6) if r[1] > 100 else pl.P(cxs, by0 - 4.6)
        lab = st["id"] + (f" · {stair_exit[st['id']]} EXIT ONLY" if lvl == 1 and st["id"] in stair_exit else "")
        al_ = "center"
        if lvl == 1 and st["id"] == "ST-2":
            lab = st["id"]
        elif lvl == 1 and st["id"] in stair_exit:
            al_ = "right" if st["id"] == "ST-1" else "left"
            x_, y_ = pl.P(cxs - 2.2 if al_ == "right" else cxs + 2.2, by1 + 1.6 if r[1] > 100 else by0 - 4.6)
        sh.text(x_, y_, lab, size=5.6, bold=True, align=al_, layer=L_TAG)
    el = vert["elevator"]
    pl.rect(el["rect"], L_VERT, lw=1.0)
    pl.line(el["rect"][0], el["rect"][1], el["rect"][2], el["rect"][3], L_VERT, lw=0.4)
    pl.line(el["rect"][0], el["rect"][3], el["rect"][2], el["rect"][1], L_VERT, lw=0.4)
    ex_, ey_ = pl.P(el["rect"][0] - 0.8, (el["rect"][1] + el["rect"][3]) / 2)
    sh.text(ex_, ey_ - 0.03, "EL", size=5.6, bold=True, align="right", layer=L_TAG)

    if lvl == 1:
        x_, y_ = pl.P(bx1 + 4.4, next(d_["at"] for d_ in lv["doors"]["items"] if d_["id"] == stair_exit.get("ST-2")))
        sh.text(x_, y_ - 0.03, f"{stair_exit.get('ST-2', '')} EXIT ONLY (ST-2)", size=5.4, bold=True, layer=L_TAG)
    nx, ny = pl.P(bx1 + 9, by1 - 52)
    sh.line(nx, ny, nx, ny + 0.55, layer=L_DIM, lw=1.1)
    sh.line(nx, ny + 0.55, nx - 0.09, ny + 0.36, layer=L_DIM, lw=1.1)
    sh.line(nx, ny + 0.55, nx + 0.09, ny + 0.36, layer=L_DIM, lw=1.1)
    sh.text(nx, ny + 0.62, "N", size=10, bold=True, align="center", layer=L_DIM)
    sh.text(nx, ny - 0.13, "APPROX.", size=5.6, align="center", layer=L_DIM)
    sh.text(nx, ny - 0.24, "SITE TBD", size=5.6, align="center", layer=L_DIM)
    gx0, gy0 = pl.P(bx1 + 4, by0 + 100)
    for a_, b_, k in ((0, 8, 0), (8, 16, 1), (16, 32, 2)):
        sh.rect(gx0 + a_ * s, gy0 - 0.30, (b_ - a_) * s, 0.06, layer=L_DIM, lw=0.6)
        if k != 1:
            sh.line(gx0 + a_ * s, gy0 - 0.30, gx0 + b_ * s, gy0 - 0.24, layer=L_DIM, lw=0.3)
    for v in (0, 8, 16, 32):
        sh.text(gx0 + v * s, gy0 - 0.42, f"{v}'", size=5.6, align="center", layer=L_DIM)
    sh.text(gx0, gy0 - 0.14, "GRAPHIC SCALE (FT)", size=5.6, layer=L_DIM)

    # ================= right panel =================
    rx = max(px0 + (bx1 - bx0) * s + 1.05, 9.35)
    rw = W - M - 0.22 - rx
    sh.line(rx - 0.2, body_bottom + 0.12, rx - 0.2, top, lw=0.5)
    y = top - 0.05
    sh.rect(rx, y - 0.42, rw, 0.42, lw=1.6)
    sh.text(rx + rw / 2, y - 0.29, pm["label"], size=14, bold=True, align="center")
    sh.text(rx, y - 0.68, f"LEVEL {lvl} — OVERALL FLOOR PLAN (REV D)", size=12, bold=True)
    sh.text(rx, y - 0.88, "scale 1/32\" = 1'-0\" on 17 x 11 in · north approximate, road assumed south, site TBD", size=7.8)
    y -= 1.18
    sh.text(rx, y, "LEGEND", size=9.5, bold=True)
    y -= 0.05
    if lvl == 1:
        leg = [("box", f"Lower tier, TELESCOPIC (extended, {lo['rows']} rows x 24 in; {X_['seat_sf_lower']:.2f} SF/seat) — D-009"),
               ("mat", "42' wrestling mat (4, 2 x 2)"), ("court", "84' x 50' court + 10' runout (overlay)"),
               ("dash", "Portal / vomitory through the telescopic tier (V1, V2)"),
               ("exit", "X# = EXIT ONLY — alarmed, no exterior entry hardware (symbol; width not drawn)"),
               ("svc", "S1 = SERVICE / LOADING door (staff-controlled, not a people entrance; D-034 OPEN)"),
               ("ck", "Security checkpoint zone (size TBD) · CD-1 controlled door (staff / teams)")]
    else:
        leg = [("box", f"Upper tier, FIXED ({X_['seat_sf_upper']:.1f} SF/seat) on the Level 2 deck — D-009"),
               ("open", "Open to below (arena; lobby double height)"),
               ("loop", "Running / training loop, 2 lanes x 42 in (dashed = lane line) — D-035"),
               ("guard", "42 in guard at an open edge (IBC 2021 1015.2, 1015.3)")]
    leg += [("box", "Room block (tag number + drawn SF)"), ("stair", "Stair (4) / elevator (X), same position on both levels")]
    for kind, t_ in leg:
        y -= 0.165
        lx = rx + 0.05
        if kind == "dash":
            sh.dashed(lx, y + 0.04, lx + 0.4, y + 0.04, lw=0.6, dash=0.04, gap=0.03)
        elif kind in ("box", "mat"):
            sh.rect(lx + 0.08, y - 0.03, 0.24, 0.14, lw=1.0)
        elif kind == "court":
            sh.dashed(lx, y + 0.04, lx + 0.4, y + 0.04, lw=0.7, dash=0.07, gap=0.04)
        elif kind == "open":
            sh.rect(lx + 0.08, y - 0.03, 0.24, 0.14, lw=0.5); sh.line(lx + 0.08, y - 0.03, lx + 0.32, y + 0.11, lw=0.25)
        elif kind == "exit":
            sh.line(lx + 0.08, y + 0.04, lx + 0.24, y + 0.04, lw=3.0); sh.line(lx + 0.16, y + 0.04, lx + 0.16, y + 0.14, lw=0.8)
            sh.line(lx + 0.16, y + 0.14, lx + 0.12, y + 0.10, lw=0.8); sh.line(lx + 0.16, y + 0.14, lx + 0.20, y + 0.10, lw=0.8)
        elif kind == "svc":
            sh.line(lx + 0.08, y + 0.04, lx + 0.24, y + 0.04, lw=3.0)
        elif kind == "ck":
            sh.dashed(lx + 0.02, y - 0.03, lx + 0.30, y - 0.03, lw=0.9, dash=0.05, gap=0.03); sh.dashed(lx + 0.02, y + 0.11, lx + 0.30, y + 0.11, lw=0.9, dash=0.05, gap=0.03)
            sh.line(lx + 0.40, y - 0.04, lx + 0.40, y + 0.12, lw=2.4)
        elif kind == "loop":
            sh.rect(lx + 0.02, y - 0.03, 0.40, 0.14, lw=1.0); sh.dashed(lx + 0.02, y + 0.04, lx + 0.42, y + 0.04, lw=0.35, dash=0.06, gap=0.04)
        elif kind == "guard":
            sh.line(lx + 0.02, y + 0.04, lx + 0.42, y + 0.04, lw=2.0)
        elif kind == "stair":
            sh.rect(lx + 0.08, y - 0.03, 0.12, 0.14, lw=1.0); sh.rect(lx + 0.24, y - 0.03, 0.12, 0.14, lw=1.0)
            sh.line(lx + 0.24, y - 0.03, lx + 0.36, y + 0.11, lw=0.4)
        sh.text(lx + 0.55, y, t_, size=7.2)
    y -= 0.30
    sh.text(rx, y, f"ROOM SCHEDULE — LEVEL {lvl} (drawn vs locked program, P2-G-003 Rev F)", size=9.5, bold=True)
    hdr = [("TAG", 0, "l"), ("ROOM", 0.36, "l"), ("DRAWN SF", 2.65, "r"), ("PROGRAM", 3.35, "r"), ("NOTE", 3.5, "l")]
    rp = 0.138
    y -= rp
    for lab, dx, al in hdr:
        sh.text(rx + dx, y + 0.02, lab, size=6.8, bold=True, align="left" if al == "l" else "right", layer=TB)
    sh.line(rx, y - 0.04, rx + rw, y - 0.04, layer=TB, lw=0.6)
    for tg, nm, a_, ps, note in sched:
        y -= rp
        while text_width_in(note, 6.4) > rw - 3.52 and len(note) > 4:
            note = note[:-2].rstrip() + "…"
        for (lab, dx, al), c in zip(hdr, [tg, nm, n(a_), "—" if ps is None else n(ps), note]):
            sh.text(rx + dx, y, c, size=6.4 if lab == "NOTE" else 7.0, align="left" if al == "l" else "right", layer=TB)
    sh.line(rx, y - 0.05, rx + rw, y - 0.05, layer=TB, lw=0.4)
    lv2 = plan["level_2"]
    lp2 = lv2["loop"]
    l2_drawn = fp - sum(area(o["rect"]) for o in lv2["open_below"])
    cap = p2["building"]["footprint_cap_sf"]
    y -= 0.06
    sh.text(rx, y - 0.16, "AREA CHECK", size=9.0, bold=True)
    y -= 0.18
    team = next(z for z in plan["level_1"]["zones"] if z["id"] == "team_asm")
    sw = next(r for r in plan["level_1"]["rooms"] if r["id"] == "storage_sw")
    if lvl == 1:
        txt = (f"Building {n(fp)} SF ({bx1 - bx0:g} x {by1 - by0:g} + NE stair tower): {n(cap - fp)} under the {n(cap)} cap. P2-G-003 Rev F "
               f"footprint {n(X_['F'])} (margin {n(cap - X_['F'])}), {n(X_['F'] - fp)} SF more than drawn. Seats {n(tot['total'])} (N {bys['N']['total']}, "
               f"S {bys['S']['total']}, E {bys['E']['total']}), unchanged. Rev D at L1: ST-1 3.55 ft west, ST-2 5 ft north (tower), elevator "
               f"1 ft south, to clear the L2 loop. Mech drawn {n(mech_drawn)} vs {n(X_['M'])}. FLEX (kept as-is): team assembly ≈ "
               f"{n(area(team['rect']))}, storage {n(area(sw['rect']))} SF.")
    else:
        txt = (f"Drawn L2 floor {n(l2_drawn)} SF (building minus open-to-below) vs program L2 gross {n(X_['L2'])} (loop {n(X_['loop'])} "
               f"as drawn). Total drawn ≈ {n(fp + l2_drawn)} vs {n(X_['G'])} program GSF (P2-G-003 Rev F). S&C {n(X_['sf']['strength_conditioning'])} "
               f"and cross-training {n(X_['sf']['cross_training'])} SF after the 7 ft trim (were 6,000 / 4,000).")
    y = sh.para(rx, y, rw, txt, size=6.9)
    sh.text(rx, y - 0.14, "ACCESS CONTROL + EGRESS (D-033 DECIDED; layout ASSUMED)" if lvl == 1 else
            "LEVEL 2 LOOP (D-035 DECIDED; geometry ASSUMED) + EGRESS", size=9.0, bold=True)
    y -= 0.16
    acc1 = ["ONE WAY IN for public, teams and staff: E1 grand entrance → security checkpoint (size TBD) → lobby. Teams then go west "
            "through CD-1 (controlled door) to team assembly, the athlete corridor and lockers.",
            "X1-X10 EXIT ONLY — alarmed, no exterior entry hardware. Egress side opens without a key or special knowledge (IBC 2021 1010.2; "
            "2018 1010.1.9); panic hardware only (1010.2.9); stair discharge doors lock from outside only (1010.2.7 exc. 1). Delayed "
            "egress is not allowed in Group A (1010.2.13): alarm only, no delay.",
            "Count: > 1,000 occupants per story → 4 exits (T1006.3.3); L1 = E1 + X1-X10, L2 = 4 stairs (R-015). Main exit ≥ 1/2 of "
            "the occupant load, fronting a street (1030.2); other exits ≥ 1/2 (1030.3). Seats alone: E1 ≥ 1,100 x 0.15 in = 165 in "
            "clear (1005.3.2 exc. 1, sprinklers + EVACS per R-015); final load TBD (R-007).",
            "Checkpoint must not narrow the main exit (1003.6, 1010.5). S1 service / loading: deliveries and buses OPEN (D-034)."]
    acc2 = [f"LOOP (D-035, Shane 4:55 AM CT): continuous around the top of Level 2 — rear walkway (N), walkway (E), upper concourse / "
            f"balcony (S) and a new west leg cut from S&C + cross-training. {lp2['lanes']} lanes x {lp2['lane_width_in']} in = {lp2['width_ft']:g} ft "
            f"everywhere, squared corners; {n(lg['centerline'])} ft centerline = {lg['laps_per_mile']:.2f} laps/mile.",
            "Lane width: UFC 4-740-02N 4.1.7 (indoor track ≥ 12 ft, 3 lanes x 42 in); Athletic Business (3 lanes of 36-42 in; max 12 "
            "laps/mile, 8-10 preferred). 2 lanes ASSUMED (3 would need 10.5 ft; the upper tier would move).",
            "Event days the loop is the upper concourse: spectators cross it at the upper-tier entries (marked, locations ASSUMED) and at "
            "the stairs / elevator, which open onto it. Training on non-event days; crossing users are a known track hazard (Athletic Business).",
            "Guards 42 in min. where the loop is open more than 30 in above the floor below (IBC 2021 1015.2, 1015.3; 4 in sphere 1015.4): "
            "west edge over the arena, south edge over the lobby. Tier backs: rail / guard per 1030.17 (architect).",
            "Clear of stairs / elevator: ST-1 3.55 ft west, ST-2 5 ft north in a 19 x 5 ft NE stair tower, elevator 1 ft south (both levels). "
            "Egress: 4 stairs discharge at L1 through EXIT ONLY doors X4, X6, X9, X10 (D-033)."]
    for t_ in (acc1 if lvl == 1 else acc2):
        y = sh.para(rx, y + 0.02, rw, t_, size=6.6, indent=0.12, bullet="·")
    if lvl == 2:
        sh.text(rx, y - 0.14, "LAYOUT NOTES (KEYSTONE, ASSUMED — architect to confirm)", size=9.0, bold=True)
        y -= 0.16
    notes1 = ["Layout (ASSUMED): exit passages N + E line up with V1 / V2; event lockers open onto them. Exit separation, travel distance, sightlines NOT checked."]
    notes2 = ["Upper tier 15 ft on N, S, E, unchanged; 6 ft stretch strip left on the N side. Exit separation, travel distance, sightlines, "
              "structure NOT checked. Floor-to-floor 15 ft ASSUMED."]
    for t_ in (notes1 if lvl == 1 else notes2):
        y = sh.para(rx, y + 0.02, rw, t_, size=6.6, indent=0.12, bullet="·")
    y = sh.para(rx, y - 0.02, rw, "Sources: phase2.yaml (D-009, D-030, D-031, D-033, D-035); Shane 2026-10-04 4:30, 4:43, 4:55 AM CT; P2-G-003 Rev F; "
                "R-008, R-009, R-014, R-015; IBC 2021 Ch. 10 (UpCodes, Alabama); UFC 4-740-02N; Athletic Business (retrieved 2026-10-04). "
                "Geometry: params/phase2_plan_rev_d.yaml.", size=6.3)
    fl = body_bottom + 0.08
    if y < fl:
        raise SystemExit(f"LAYOUT OVERFLOW: right panel runs {fl - y:.2f} in into the stamp band")
    print(f"layout margin right panel (in): {y - fl:.2f}")
    return sh


def build_e(sheet_no, p2, prog, plan, X_, seats, lg, DR, DD, rows_f):
    """Rev E (Shane 2026-10-04 9:10 AM CT, reviewer C-1..C-4): 76 in stairs (D-052), east tier +6 ft (D-053), under-tier rule (D-049), D-057 areas."""
    lvl = LEVEL_OF[sheet_no]
    meta2 = p2["meta"]
    pm = plan["meta"]
    rows, tot = seats
    bys = {r["side"]: r for r in rows}
    sh = Sheet(W, H)
    body_bottom = add_titleblock(sh, {
        "project": f"{meta2['project']}\n{meta2['arena_name']} · {meta2['location']}",
        "phase": "PHASE 2",
        "title": f"OVERALL FLOOR PLAN\nLEVEL {lvl} · BLOCK PLAN",
        "scale": "1/32\" = 1'-0\"",
        "date": meta2["sheet_date"],
        "revision": "E",
        "drawn_by": meta2["drawn_by"],
        "sheet_no": sheet_no,
        "stamp": meta2["stamp"],
    }, margin=M, tb_h=0.95, stamp_h=0.40)
    top = H - M - 0.12
    s = 1.0 / pm["scale_ft_per_in"]
    bx0, by0, bx1, by1 = plan["building"]["rect"]
    px0, py0 = M + 0.62, body_bottom + 0.50
    pl = Plan(sh, px0, py0, s)
    floor = plan["event_floor"]["rect"]
    av = plan["arena_volume"]["rect"]
    lv = plan["level_1"] if lvl == 1 else plan["level_2"]
    vert = plan["vertical"]
    axis = plan["entry_axis_x"]["value"]
    sched = []
    probs = check_overlaps(lv, vert)
    lvr = [st_["rect"] for st_ in vert["stairs"]] + [vert["elevator"]["rect"]]
    probs += [f"loop {k_} x stair/elevator {v_}" for k_, leg in lg["legs"].items() for v_ in lvr if overlap(leg, v_) > 0.01]
    probs += [f"loop {k_} x room {r_['id']}" for k_, leg in lg["legs"].items() for r_ in plan["level_2"]["rooms"] if overlap(leg, r_["rect"]) > 0.01]
    if probs:
        raise SystemExit(f"ROOM OVERLAP on level {lvl}: {probs}")


    pj = plan["building"]["projection"]["rect"]
    outline = [(bx0, by0), (bx1, by0), (bx1, pj[3]), (pj[0], pj[3]), (pj[0], by1), (bx0, by1), (bx0, by0)]
    for (xa, ya), (xb, yb) in zip(outline[:-1], outline[1:]):
        pl.line(xa, ya, xb, yb, L_WALL, lw=2.2)
    fp = area(plan["building"]["rect"]) + area(pj)
    yd = by0 - 9
    pl.line(bx0, yd, bx1, yd, L_DIM, lw=0.4)
    for xx in (bx0, bx1):
        pl.line(xx, yd - 2.5, xx, yd + 2.5, L_DIM, lw=0.4)
    tx, ty = pl.P((bx0 + bx1) / 2, yd)
    sh.text(tx, ty - 0.14, f"{bx1 - bx0:g}'-0\"  (building {bx1 - bx0:g} x {by1 - by0:g} ft + {pj[2] - pj[0]:.2f} x {pj[3] - pj[1]:.2f} ft NE stair tower = {n(fp)} SF footprint)", size=7, align="center", layer=L_DIM)
    xd = bx0 - 9
    pl.line(xd, by0, xd, by1, L_DIM, lw=0.4)
    for yy in (by0, by1):
        pl.line(xd - 2.5, yy, xd + 2.5, yy, L_DIM, lw=0.4)
    tx, ty = pl.P(xd, (by0 + by1) / 2)
    sh.text(tx - 0.06, ty, f"{by1 - by0:g}'-0\"", size=7, align="center", layer=L_DIM, rot=90)

    lo, up = plan["tiers"]["lower"], plan["tiers"]["upper"]
    names = {"N": "N", "S": "S", "E": "E"}
    if lvl == 1:
        pl.rect(av, L_FIX, lw=0.9)
        pl.rect(floor, L_MAT, lw=1.4)
        fx0, fy0, fx1, fy1 = floor
        for b in lo["bands"]:
            r = b["rect"]
            pl.rect(r, L_TEL, lw=0.9)
            horiz = (r[2] - r[0]) >= (r[3] - r[1])
            ops = [o["rect"] for o in lo["openings"] if o["side"] == b["side"]]
            # back-half row lines (rows 4-6), broken at openings; label in the front half
            for k in range(lo["rows"] // 2, lo["rows"]):
                dk = k * lo["row_depth_ft"]
                if horiz:
                    yy = r[1] + dk if b["side"] == "N" else r[3] - dk
                    xs = [r[0]] + sum(([o[0], o[2]] for o in sorted(ops)), []) + [r[2]]
                    for a_, b_ in zip(xs[0::2], xs[1::2]):
                        pl.line(a_, yy, b_, yy, L_TEL, lw=0.2)
                else:
                    xx = r[0] + dk
                    ys = [r[1]] + sum(([o[1], o[3]] for o in sorted(ops, key=lambda o: o[1])), []) + [r[3]]
                    for a_, b_ in zip(ys[0::2], ys[1::2]):
                        pl.line(xx, a_, xx, b_, L_TEL, lw=0.2)
            t_ = f"LOWER ({b['side']}) · TELESCOPIC · {n(bys[b['side']]['lower'])} SEATS"
            if horiz:
                yy = r[1] + 2.4 if b["side"] == "N" else r[3] - 3.6
                x_lab = r[0] + 2.5 if b["side"] == "N" else lo["openings"][0]["rect"][2] + 3   # S: east of the portal
                x_, y_ = pl.P(x_lab, yy)
                sh.text(x_, y_ - 0.035, t_, size=5.2, bold=True, layer=L_TAG)
            else:
                x_, y_ = pl.P(r[0] + 3.4, (r[1] + r[3]) / 2 - 22)
                sh.text(x_ + 0.035, y_, t_, size=5.2, bold=True, align="center", layer=L_TAG, rot=90)
        for o in lo["openings"]:
            pl.drect(o["rect"], L_ROOM, lw=0.5, dash=0.04, gap=0.03)
            r = o["rect"]
            horiz = (r[2] - r[0]) < (r[3] - r[1])           # openings run through the band
            x_, y_ = pl.P((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)
            if o["id"] == "PORTAL":
                sh.text(x_, y_ + 0.0, "PORTAL", size=4.8, bold=True, align="center", layer=L_TAG)
            else:
                sh.text(x_, y_ - 0.03, o["id"], size=5.0, bold=True, align="center", layer=L_TAG)
        mft = p2["spaces"]["arena"]["mat_ft"]
        for m in plan["mats"]:
            mx, my = m["origin"]
            pl.rect((mx, my, mx + mft, my + mft), L_MAT, lw=1.0)
            left = mx + mft / 2 < (floor[0] + floor[2]) / 2
            x_, y_ = pl.P(mx + 2 if left else mx + mft - 2, my + mft - 2.5)
            sh.text(x_, y_ - 0.09, m["id"], size=6.2, bold=True, align="left" if left else "right", layer=L_TAG)
        cr = plan["court"]["rect"]
        ro = plan["court"]["runout_ft"]
        pl.drect(cr, L_CORT, lw=0.7, dash=0.07, gap=0.04)
        pl.drect((cr[0] - ro, cr[1] - ro, cr[2] + ro, cr[3] + ro), L_CORT, lw=0.35, dash=0.03, gap=0.04)
        pl.dashed(cr[0], (cr[1] + cr[3]) / 2, cr[2], (cr[1] + cr[3]) / 2, L_CORT, lw=0.4, dash=0.07, gap=0.04)
        x_, y_ = pl.P((fx0 + fx1) / 2, fy1 - 6)
        sh.text(x_, y_, f"EVENT FLOOR {fx1 - fx0:g}' x {fy1 - fy0:g}' = {n(area(floor))} SF", size=6.6, bold=True, align="center", layer=L_TAG)
        sh.text(x_, y_ - 0.12, "table / bench zone (15')", size=5.4, align="center", layer=L_TAG)
        x_, y_ = pl.P((fx0 + fx1) / 2, fy0 + 7.5)
        sh.text(x_, y_, "table / bench zone (15')", size=5.4, align="center", layer=L_TAG)
        x_, y_ = pl.P((cr[0] + cr[2]) / 2, (cr[1] + cr[3]) / 2 + 2.5)
        sh.text(x_, y_, "COURT 84' x 50' (OVERLAY)", size=5.4, align="center", layer=L_TAG)
        # upper tier above (D-049): outline dashed; low-headroom band under rows 1-2
        lbf = up["low_band_ft"]
        lows = {"N": [56, 224, 188, 224 + lbf], "E": [188, 56, 188 + lbf, 239], "S": [56, 56 - lbf, 188, 56]}
        for k_, lr in lows.items():
            pl.drect(lr, L_TAG, lw=0.5, dash=0.03, gap=0.03)
        for z in lv["zones"]:
            if z.get("under_tier"):
                r_ = z["rect"]
                for t_ in range(1, 12):
                    u_ = t_ / 12
                    if (r_[2] - r_[0]) >= (r_[3] - r_[1]):
                        xa = r_[0] + (r_[2] - r_[0]) * u_
                        pl.line(xa - 3, r_[1], xa, r_[3], L_HID, lw=0.2)
                    else:
                        ya = r_[1] + (r_[3] - r_[1]) * u_
                        pl.line(r_[0], ya - 3, r_[2], ya, L_HID, lw=0.2)
        x_, y_ = pl.P(116, 197.5)
        sh.text(x_, y_, "UPPER TIER ABOVE steps DOWN to the court · fine dash = LOW BAND under its rows 1-2, < 7'-6\": storage / mech only (D-049)", size=4.4, align="center", layer=L_TAG)
        lower_drawn = sum(area(b["rect"]) for b in lo["bands"])
        sched.append(("—", "Event floor + east zone (D-053)", area(floor), X_["sf"]["arena"], f"{floor[2] - floor[0]:g}' x {floor[3] - floor[1]:g}'; east tier 16 ft from mats"))
        sched.append(("—", f"Lower tier, telescopic ({n(tot['lower'])} seats)", lower_drawn, X_["sf"]["seating_lower"],
                      f"{lo['rows']} rows; N {bys['N']['lower']} / S {bys['S']['lower']} / E {bys['E']['lower']}"))
        # team side / public side walls (Rev C): team assembly vs west concourse, athlete route vs west concourse
        pl.line(56, 34, 56, 48, L_ROOM, lw=0.9)
        pl.line(56, 48, 84, 48, L_ROOM, lw=0.9)
        # single controlled entry (D-033): entry arrow on the axis
        pl.line(axis, -6, axis, 0, L_DIM, lw=1.0)
        pl.line(axis, 0, axis - 1.8, -2.6, L_DIM, lw=1.0); pl.line(axis, 0, axis + 1.8, -2.6, L_DIM, lw=1.0)
        x_, y_ = pl.P(axis - 3, -5.2)
        sh.text(x_, y_, "ARENA N-S AXIS · ROAD ASSUMED SOUTH", size=5.6, align="right", layer=L_TAG)
        x_, y_ = pl.P(axis + 3, -4.4)
        sh.text(x_, y_, "E1 MAIN ENTRY / EXIT (D-033)", size=6.0, bold=True, layer=L_TAG)
        x_, y_ = pl.P(axis + 3, -7.0)
        sh.text(x_, y_, "↓ 30' S: FREESTANDING PORTAL + 28' x 30' CHAMPION WALK (D-043, D-046; P2-C-101)", size=4.4, layer=L_TAG)
        # security checkpoint (location only; size TBD)
        ck = lv["checkpoint"]
        pl.drect(ck["rect"], L_TAG, lw=0.9, dash=0.06, gap=0.035)
        x_, y_ = pl.P((ck["rect"][0] + ck["rect"][2]) / 2, (ck["rect"][1] + ck["rect"][3]) / 2)
        sh.text(x_, y_ + 0.015, "SECURITY CHECKPOINT", size=5.0, bold=True, align="center", layer=L_TAG)
        sh.text(x_, y_ - 0.085, "— size TBD (ASSUMED)", size=5.0, align="center", layer=L_TAG)
        # controlled door off the lobby to the athlete route
        cdx, cdy = lv["controlled_door"]["at"]
        pl.line(cdx, cdy - 4, cdx, cdy + 4, L_TAG, lw=2.4)
        x_, y_ = pl.P(cdx + 1.2, cdy - 7.2)
        sh.text(x_, y_, "CD-1 CONTROLLED DOOR", size=5.0, bold=True, layer=L_TAG)
        sh.text(x_, y_ - 0.08, "(staff / teams)", size=4.8, layer=L_TAG)
        # perimeter doors: symbols only (widths not drawn)
        stair_exit = {}
        for d_ in lv["doors"]["items"]:
            w_, at = d_["wall"], d_["at"]
            if d_["kind"] == "main":
                continue
            if w_ in ("N", "S"):
                yy = by1 if w_ == "N" else by0
                pl.line(at - 2.5, yy, at + 2.5, yy, L_TAG, lw=3.0)
                o = 1 if w_ == "N" else -1
                if d_["kind"] == "exit":
                    pl.line(at, yy, at, yy + 3.2 * o, L_TAG, lw=0.8)
                    pl.line(at, yy + 3.2 * o, at - 1.2, yy + 1.8 * o, L_TAG, lw=0.8); pl.line(at, yy + 3.2 * o, at + 1.2, yy + 1.8 * o, L_TAG, lw=0.8)
            else:
                xx = bx0 if w_ == "W" else bx1
                pl.line(xx, at - 2.5, xx, at + 2.5, L_TAG, lw=3.0)
                o = -1 if w_ == "W" else 1
                if d_["kind"] == "exit":
                    pl.line(xx, at, xx + 3.2 * o, at, L_TAG, lw=0.8)
                    pl.line(xx + 3.2 * o, at, xx + 1.8 * o, at - 1.2, L_TAG, lw=0.8); pl.line(xx + 3.2 * o, at, xx + 1.8 * o, at + 1.2, L_TAG, lw=0.8)
            if "ST-" in d_.get("serves", ""):
                stair_exit[d_["serves"].split()[0]] = d_["id"]
                continue
            if d_["kind"] == "service":
                x_, y_ = pl.P(at - 3, by1 + 1.6)
                sh.text(x_, y_, "S1 SERVICE / LOADING (D-034)", size=5.2, bold=True, layer=L_TAG)
            elif w_ == "N":
                x_, y_ = pl.P(at + 2.2, by1 + 1.6)
                sh.text(x_, y_, f"{d_['id']} EXIT ONLY", size=5.4, bold=True, layer=L_TAG)
            elif w_ == "W":
                x_, y_ = pl.P(bx0 - 4.6, at + 12)
                sh.text(x_ + 0.03, y_, f"{d_['id']} EXIT ONLY", size=5.4, bold=True, align="center", layer=L_TAG, rot=90)
            elif w_ == "E":
                x_, y_ = pl.P(bx1 + 4.4, at)
                sh.text(x_, y_ - 0.03, f"{d_['id']} EXIT ONLY", size=5.4, bold=True, layer=L_TAG)
    else:
        for ob in lv["open_below"]:
            r = ob["rect"]
            pl.rect(r, L_HID, lw=0.5)
            for (xa, ya, xb, yb) in ((r[0], r[1], r[2], r[3]), (r[0], r[3], r[2], r[1])):
                for t0, t1 in ((0.0, 0.36), (0.64, 1.0)):
                    pl.dashed(xa + (xb - xa) * t0, ya + (yb - ya) * t0, xa + (xb - xa) * t1, ya + (yb - ya) * t1, L_HID, lw=0.25, dash=0.06, gap=0.06)
        pl.drect(floor, L_HID, lw=0.4, dash=0.05, gap=0.05)
        for b in up["bands"]:
            r = b["rect"]
            pl.rect(r, L_FIX, lw=0.9)
            t_ = f"UPPER ({b['side']}) · FIXED · {n(bys[b['side']]['upper'])} SEATS"
            if (r[2] - r[0]) >= (r[3] - r[1]):
                x_, y_ = pl.P(r[0] + 3, (r[1] + r[3]) / 2)
                sh.text(x_, y_ - 0.035, t_, size=5.6, bold=True, layer=L_TAG)
            else:
                x_, y_ = pl.P((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)
                sh.text(x_ + 0.035, y_, t_, size=5.6, bold=True, align="center", layer=L_TAG, rot=90)
        oba = next(o for o in lv["open_below"] if o["id"] == "ob_arena")["rect"]
        x_, y_ = pl.P((oba[0] + oba[2]) / 2, (oba[1] + oba[3]) / 2)
        sh.text(x_, y_ + 0.05, "OPEN TO ARENA BELOW", size=8, bold=True, align="center", layer=L_TAG)
        sh.text(x_, y_ - 0.10, "(event floor + telescopic lower tier, double height)", size=6, align="center", layer=L_TAG)
        obl = next(o for o in lv["open_below"] if o["id"] == "ob_lobby")["rect"]
        pl.tag(obl, ["OPEN TO LOBBY BELOW", "(hall of champions,", "double height)"], sizes=(6.4, 6.0, 5.5), bold_first=True, allow_rot=False)
        upper_drawn = sum(area(b["rect"]) for b in up["bands"])
        sched.append(("—", f"Upper tier, fixed ({n(tot['upper'])} seats)", upper_drawn, X_["sf"]["seating_upper"],
                      f"N {bys['N']['upper']} / S {bys['S']['upper']} / E {bys['E']['upper']}"))
        # ---- Level 2 running / training loop (D-035) ----
        lp = lv["loop"]
        lo_, li_ = lp["outer"], lp["inner"]
        pl.rect(lo_, L_LOOP, lw=1.3)
        pl.rect(li_, L_LOOP, lw=0.7)
        w2 = lp["width_ft"] / 2
        cl = [lo_[0] + w2, lo_[1] + w2, lo_[2] - w2, lo_[3] - w2]
        # lane line (2 lanes -> one line on the centerline), broken where the leg labels sit
        legtxt = {"S": (f"LOOP (S) · UPPER CONCOURSE / HALL OF CHAMPIONS BALCONY · 2 LANES x {lp['lane_width_in']} IN = {lp['width_ft']:g} FT", 115),
                  "N": (f"LOOP (N) · REAR CONCOURSE ON EVENT DAYS · 2 LANES x {lp['lane_width_in']} IN", 110),
                  "E": (f"LOOP (E) · 2 LANES x {lp['lane_width_in']} IN = {lp['width_ft']:g} FT", 140),
                  "W": ("LOOP (W) · NEW LEG (D-035)", 105)}
        szl = 4.6
        gaps = {}
        for k_, (t_, c_) in legtxt.items():
            half = (text_width_in(t_, szl, True) / s) / 2 + 2
            gaps[k_] = (c_ - half, c_ + half)
            if k_ in ("N", "S"):
                x_, y_ = pl.P(c_, cl[1] if k_ == "S" else cl[3])
                sh.text(x_, y_ - 0.022, t_, size=szl, bold=True, align="center", layer=L_LOOP)
            else:
                x_, y_ = pl.P(cl[0] if k_ == "W" else cl[2], c_)
                sh.text(x_ + 0.022, y_, t_, size=szl, bold=True, align="center", layer=L_LOOP, rot=90)
        for k_, (a0, a1, fixed, horiz) in {"S": (cl[0], cl[2], cl[1], True), "N": (cl[0], cl[2], cl[3], True),
                                            "W": (cl[1], cl[3], cl[0], False), "E": (cl[1], cl[3], cl[2], False)}.items():
            g0, g1 = gaps[k_]
            for u0, u1 in ((a0, g0), (g1, a1)):
                if horiz:
                    pl.dashed(u0, fixed, u1, fixed, L_LOOP, lw=0.35, dash=0.06, gap=0.04)
                else:
                    pl.dashed(fixed, u0, fixed, u1, L_LOOP, lw=0.35, dash=0.06, gap=0.04)
        # guards at open edges (IBC 1015.2 / 1015.3)
        for g_ in lp["guards"]:
            xa, ya, xb, yb = g_["line"]
            pl.line(xa, ya, xb, yb, L_GRD, lw=2.0)
        gw = next(g_ for g_ in lp["guards"] if g_["id"] == "G-W")["line"]
        x_, y_ = pl.P(gw[0] + 2.2, (gw[1] + gw[3]) / 2 + 40)
        sh.text(x_ + 0.03, y_, "42 IN GUARD (IBC 1015.2, 1015.3)", size=4.8, bold=True, align="center", layer=L_GRD, rot=90)
        gs = next(g_ for g_ in lp["guards"] if g_["id"] == "G-S")["line"]
        x_, y_ = pl.P((gs[0] + gs[2]) / 2, gs[1] - 2.6)
        sh.text(x_, y_, "42 IN GUARD (IBC 1015)", size=4.8, bold=True, align="center", layer=L_GRD)
        # event-day crossings at the upper-tier entries (locations ASSUMED: mid-side)
        for (xa, ya, xb, yb) in ((172, li_[3], 172, lo_[3]), (172, lo_[1], 172, li_[1]), (li_[2], 100, lo_[2], 100)):
            pl.line(xa, ya, xb, yb, L_TAG, lw=0.6)
            if xa == xb:
                for yy_, o_ in ((ya, 1), (yb, -1)):
                    pl.line(xa, yy_, xa - 1, yy_ + 1.4 * o_, L_TAG, lw=0.6); pl.line(xa, yy_, xa + 1, yy_ + 1.4 * o_, L_TAG, lw=0.6)
            else:
                for xx_, o_ in ((xa, 1), (xb, -1)):
                    pl.line(xx_, ya, xx_ + 1.4 * o_, ya - 1, L_TAG, lw=0.6); pl.line(xx_, ya, xx_ + 1.4 * o_, ya + 1, L_TAG, lw=0.6)
        x_, y_ = pl.P(170, li_[3] - 3.2)
        sh.text(x_, y_, "event-day crossing (typ.)", size=4.4, align="right", layer=L_TAG)
        sn = next(z for z in lv["zones"] if z["id"] == "stretch_n")["rect"]
        x_, y_ = pl.P((sn[0] + sn[2]) / 2, (sn[1] + sn[3]) / 2)
        sh.text(x_, y_ - 0.02, f"STRETCH / WARM-UP STRIP (N) · {sn[3] - sn[1]:g} FT · ASSUMED", size=4.4, bold=True, align="center", layer=L_TAG)
        # loop summary in the arena void
        oba_ = next(o for o in lv["open_below"] if o["id"] == "ob_arena")["rect"]
        x_, y_ = pl.P((oba_[0] + oba_[2]) / 2, (oba_[1] + oba_[3]) / 2 - 22)
        sh.text(x_, y_ + 0.05, "CONTINUOUS RUNNING / TRAINING LOOP (D-035)", size=7.0, bold=True, align="center", layer=L_LOOP)
        sh.text(x_, y_ - 0.09, f"centerline {lg['cx']:g}' x {lg['cy']:g}' = {n(lg['centerline'])} FT · 5,280 / {n(lg['centerline'])} = {lg['laps_per_mile']:.2f} LAPS / MILE",
                size=6.0, align="center", layer=L_LOOP)
        sh.text(x_, y_ - 0.21, f"{lp['lanes']} lanes x {lp['lane_width_in']} in = {lp['width_ft']:g} ft all around · squared corners · {n(lg['area'])} SF",
                size=6.0, align="center", layer=L_LOOP)
        sh.text(x_, y_ - 0.33, "non-event days: training · event days: upper concourse (spectators cross at tier entries)",
                size=5.6, align="center", layer=L_LOOP)
        sched.append(("—", "Running / training loop", lg["area"], X_["loop"], f"{lp['lanes']} x {lp['lane_width_in']} in; {n(lg['centerline'])} ft CL; {lg['laps_per_mile']:.2f} laps/mi"))

    if lvl == 1:
        ut = [z for z in lv["zones"] if z.get("under_tier")]
        sched.append(("—", "Under-tier storage (hatched)", sum(area(z["rect"]) for z in ut), None, "low band in front of event lockers 1-4 (D-049)"))
    # rooms (stairs / elevator inside a room are subtracted from its drawn SF)
    mech_rooms = [r for r in plan["level_1"]["rooms"] if r["prog"] == "mechanical"]
    mech_drawn = sum(area(r["rect"]) for r in mech_rooms)
    vrects = [st_["rect"] for st_ in vert["stairs"]] + [vert["elevator"]["rect"]]
    for r in lv["rooms"]:
        pl.rect(r["rect"], L_ROOM, lw=0.9)
        a_ = area(r["rect"]) - sum(overlap(r["rect"], v) for v in vrects)
        if r["prog"] == "mechanical":
            ps = X_["M"] * area(r["rect"]) / mech_drawn
        elif r["prog"] is None:
            ps = None
        else:
            ps = X_["sf"][r["prog"]] * r.get("share", 1)
        note = r.get("note", "")
        extra = []
        if "fixtures" in r:
            wc, lav, ur = fixture_lines(X_, r["fixtures"])
            ps = (wc + lav) * prog["factors"]["restrooms"]["sf_per_fixture"]
            extra = [f"WC {wc} · LAV {lav}"]
            note = f"{wc + lav} fixtures (WC {wc}, LAV {lav}" + (f"; urinals ≤ {ur} of the WCs)" if ur is not None else ")")
        if r["id"] == "sc":
            note = f"ST-1 (76 in) inside: {'+' if a_ >= ps else '−'}{n(abs(a_ - ps))} vs program (C-3)"
        if r["id"] == "xt":
            note = "trimmed 7 ft for the loop (D-035)"
        if r["id"].startswith("evl_"):
            note = f"behind the low band (D-049): {'+' if a_ >= ps else '−'}{n(abs(a_ - ps))}"
        if r["id"] == "storage_sw":
            note = "FLEX, unprogrammed, label kept (D-039, C-1)"
        full = [f"{r['tag']}  {r['name']}", f"{n(a_)} SF"] + extra
        if not pl.tag(r["rect"], full, fallback=[f"{r['tag']}", f"{n(a_)}"]):
            pl.tag(r["rect"], [r["tag"]], sizes=(5.5, 5.0, 4.5))
        nm = r["name"].title().replace("(Nw)", "(NW)").replace("(Ne)", "(NE)").replace("(Sw)", "(SW)").replace("(Se)", "(SE)").replace("Mat", "Mat Area")
        sched.append((r["tag"], nm, a_, ps, note))
    for z in lv["zones"]:
        if z["id"] == "stretch_n" or z.get("under_tier"):
            continue
        if z.get("vertical"):
            r = z["rect"]
            x_, y_ = pl.P((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)
            sz = 6.2
            while text_width_in(z["name"], sz, True) > (r[3] - r[1]) * s - 0.1 and sz > 4.5:
                sz -= 0.3
            sh.text(x_ + 0.03, y_, z["name"], size=sz, bold=True, align="center", layer=L_TAG, rot=90)
        else:
            lines = z["name"].replace(" / ", " /|").split("|")
            if z["id"] == "lobby":
                lines = lines + ["(double height)"]
            if z.get("sub"):
                lines = lines + z["sub"].split("|")
            pl.tag(z.get("label_rect", z["rect"]), lines, sizes=(6.4, 6.0, 5.5, 5.0, 4.6), allow_rot=False)
    for st in vert["stairs"]:
        r = st["rect"]
        pl.rect(r, L_VERT, lw=1.0)
        horiz = (r[2] - r[0]) > (r[3] - r[1])
        if horiz:
            my_ = (r[1] + r[3]) / 2
            pl.line(r[0] + 2, my_, r[2] - 2, my_, L_VERT, lw=0.4)
            for k in range(1, 6):
                xx = r[0] + 2 + k * (r[2] - r[0] - 4) / 6
                pl.line(xx, r[1], xx, r[3], L_VERT, lw=0.2)
        else:
            mxs = (r[0] + r[2]) / 2
            pl.line(mxs, r[1] + 2, mxs, r[3] - 2, L_VERT, lw=0.4)
            for k in range(1, 6):
                yy = r[1] + 2 + k * (r[3] - r[1] - 4) / 6
                pl.line(r[0], yy, r[2], yy, L_VERT, lw=0.2)
        cxs = (r[0] + r[2]) / 2
        x_, y_ = pl.P(cxs, max(by1, r[3]) + 1.6) if r[1] > 100 else pl.P(cxs, by0 - 4.6)
        lab = st["id"] + (f" · {stair_exit[st['id']]} EXIT ONLY" if lvl == 1 and st["id"] in stair_exit else "")
        al_ = "center"
        if lvl == 1 and st["id"] == "ST-2":
            lab = st["id"]
        elif lvl == 1 and st["id"] in stair_exit:
            al_ = "right" if st["id"] == "ST-1" else "left"
            x_, y_ = pl.P(cxs - 2.2 if al_ == "right" else cxs + 2.2, by1 + 1.6 if r[1] > 100 else by0 - 4.6)
        sh.text(x_, y_, lab, size=5.6, bold=True, align=al_, layer=L_TAG)
    el = vert["elevator"]
    pl.rect(el["rect"], L_VERT, lw=1.0)
    pl.line(el["rect"][0], el["rect"][1], el["rect"][2], el["rect"][3], L_VERT, lw=0.4)
    pl.line(el["rect"][0], el["rect"][3], el["rect"][2], el["rect"][1], L_VERT, lw=0.4)
    ex_, ey_ = pl.P(el["rect"][0] - 0.8, (el["rect"][1] + el["rect"][3]) / 2)
    sh.text(ex_, ey_ - 0.03, "EL", size=5.6, bold=True, align="right", layer=L_TAG)

    if lvl == 1:
        x_, y_ = pl.P(bx1 + 4.4, next(d_["at"] for d_ in lv["doors"]["items"] if d_["id"] == stair_exit.get("ST-2")))
        sh.text(x_, y_ - 0.03, f"{stair_exit.get('ST-2', '')} EXIT ONLY (ST-2)", size=5.4, bold=True, layer=L_TAG)
    nx, ny = pl.P(bx1 + 9, by1 - 52)
    sh.line(nx, ny, nx, ny + 0.55, layer=L_DIM, lw=1.1)
    sh.line(nx, ny + 0.55, nx - 0.09, ny + 0.36, layer=L_DIM, lw=1.1)
    sh.line(nx, ny + 0.55, nx + 0.09, ny + 0.36, layer=L_DIM, lw=1.1)
    sh.text(nx, ny + 0.62, "N", size=10, bold=True, align="center", layer=L_DIM)
    sh.text(nx, ny - 0.13, "APPROX.", size=5.6, align="center", layer=L_DIM)
    sh.text(nx, ny - 0.24, "SITE TBD", size=5.6, align="center", layer=L_DIM)
    gx0, gy0 = pl.P(bx1 + 4, by0 + 100)
    for a_, b_, k in ((0, 8, 0), (8, 16, 1), (16, 32, 2)):
        sh.rect(gx0 + a_ * s, gy0 - 0.30, (b_ - a_) * s, 0.06, layer=L_DIM, lw=0.6)
        if k != 1:
            sh.line(gx0 + a_ * s, gy0 - 0.30, gx0 + b_ * s, gy0 - 0.24, layer=L_DIM, lw=0.3)
    for v in (0, 8, 16, 32):
        sh.text(gx0 + v * s, gy0 - 0.42, f"{v}'", size=5.6, align="center", layer=L_DIM)
    sh.text(gx0, gy0 - 0.14, "GRAPHIC SCALE (FT)", size=5.6, layer=L_DIM)

    # ================= right panel =================
    rx = max(px0 + (bx1 - bx0) * s + 1.05, 9.35)
    rw = W - M - 0.22 - rx
    sh.line(rx - 0.2, body_bottom + 0.12, rx - 0.2, top, lw=0.5)
    y = top - 0.05
    sh.rect(rx, y - 0.42, rw, 0.42, lw=1.6)
    sh.text(rx + rw / 2, y - 0.29, pm["label"], size=14, bold=True, align="center")
    sh.text(rx, y - 0.68, f"LEVEL {lvl} — OVERALL FLOOR PLAN (REV E)", size=12, bold=True)
    sh.text(rx, y - 0.88, "scale 1/32\" = 1'-0\" on 17 x 11 in · north approximate, road assumed south, site TBD", size=7.8)
    y -= 1.18
    sh.text(rx, y, "LEGEND", size=9.5, bold=True)
    y -= 0.05
    if lvl == 1:
        leg = [("box", f"Lower tier, TELESCOPIC (extended, {lo['rows']} rows x 24 in; {X_['seat_sf_lower']:.2f} SF/seat) — D-009"),
               ("mat", "42' wrestling mat (4, 2 x 2)"), ("court", "84' x 50' court + 10' runout (overlay)"),
               ("dash", "Portal / vomitory through the telescopic tier (V1, V2)"),
               ("exit", "X# = EXIT ONLY — alarmed, no exterior entry hardware (symbol; width not drawn)"),
               ("svc", "S1 = SERVICE / LOADING door (staff-controlled, not a people entrance; D-034)"),
               ("dash", "Fine dash = low band under upper-tier rows 1-2 (D-049); hatch = under-tier storage"),
               ("ck", "Security checkpoint zone (size TBD) · CD-1 controlled door (staff / teams)")]
    else:
        leg = [("box", f"Upper tier, FIXED ({X_['seat_sf_upper']:.1f} SF/seat) on the Level 2 deck — D-009"),
               ("open", "Open to below (arena; lobby double height)"),
               ("loop", "Running / training loop, 2 lanes x 42 in (dashed = lane line) — D-035"),
               ("guard", "42 in guard at an open edge (IBC 2021 1015.2, 1015.3)")]
    leg += [("box", "Room block (tag number + drawn SF)"), ("stair", "Stair (4) / elevator (X), same position on both levels")]
    for kind, t_ in leg:
        y -= 0.150 if lvl == 1 else 0.165
        lx = rx + 0.05
        if kind == "dash":
            sh.dashed(lx, y + 0.04, lx + 0.4, y + 0.04, lw=0.6, dash=0.04, gap=0.03)
        elif kind in ("box", "mat"):
            sh.rect(lx + 0.08, y - 0.03, 0.24, 0.14, lw=1.0)
        elif kind == "court":
            sh.dashed(lx, y + 0.04, lx + 0.4, y + 0.04, lw=0.7, dash=0.07, gap=0.04)
        elif kind == "open":
            sh.rect(lx + 0.08, y - 0.03, 0.24, 0.14, lw=0.5); sh.line(lx + 0.08, y - 0.03, lx + 0.32, y + 0.11, lw=0.25)
        elif kind == "exit":
            sh.line(lx + 0.08, y + 0.04, lx + 0.24, y + 0.04, lw=3.0); sh.line(lx + 0.16, y + 0.04, lx + 0.16, y + 0.14, lw=0.8)
            sh.line(lx + 0.16, y + 0.14, lx + 0.12, y + 0.10, lw=0.8); sh.line(lx + 0.16, y + 0.14, lx + 0.20, y + 0.10, lw=0.8)
        elif kind == "svc":
            sh.line(lx + 0.08, y + 0.04, lx + 0.24, y + 0.04, lw=3.0)
        elif kind == "ck":
            sh.dashed(lx + 0.02, y - 0.03, lx + 0.30, y - 0.03, lw=0.9, dash=0.05, gap=0.03); sh.dashed(lx + 0.02, y + 0.11, lx + 0.30, y + 0.11, lw=0.9, dash=0.05, gap=0.03)
            sh.line(lx + 0.40, y - 0.04, lx + 0.40, y + 0.12, lw=2.4)
        elif kind == "loop":
            sh.rect(lx + 0.02, y - 0.03, 0.40, 0.14, lw=1.0); sh.dashed(lx + 0.02, y + 0.04, lx + 0.42, y + 0.04, lw=0.35, dash=0.06, gap=0.04)
        elif kind == "guard":
            sh.line(lx + 0.02, y + 0.04, lx + 0.42, y + 0.04, lw=2.0)
        elif kind == "stair":
            sh.rect(lx + 0.08, y - 0.03, 0.12, 0.14, lw=1.0); sh.rect(lx + 0.24, y - 0.03, 0.12, 0.14, lw=1.0)
            sh.line(lx + 0.24, y - 0.03, lx + 0.36, y + 0.11, lw=0.4)
        sh.text(lx + 0.55, y, t_, size=7.2)
    y -= 0.30
    sh.text(rx, y, f"ROOM SCHEDULE — LEVEL {lvl} (DRAWN vs PROGRAM side by side, P2-G-003 Rev G; C-3)", size=9.5, bold=True)
    hdr = [("TAG", 0, "l"), ("ROOM", 0.36, "l"), ("DRAWN SF", 2.65, "r"), ("PROGRAM", 3.35, "r"), ("NOTE", 3.5, "l")]
    rp = 0.126 if lvl == 1 else 0.138
    y -= rp
    for lab, dx, al in hdr:
        sh.text(rx + dx, y + 0.02, lab, size=6.8, bold=True, align="left" if al == "l" else "right", layer=TB)
    sh.line(rx, y - 0.04, rx + rw, y - 0.04, layer=TB, lw=0.6)
    for tg, nm, a_, ps, note in sched:
        y -= rp
        while text_width_in(note, 6.4) > rw - 3.52 and len(note) > 4:
            note = note[:-2].rstrip() + "…"
        for (lab, dx, al), c in zip(hdr, [tg, nm, n(a_), "—" if ps is None else n(ps), note]):
            sh.text(rx + dx, y, c, size=6.4 if lab == "NOTE" else 7.0, align="left" if al == "l" else "right", layer=TB)
    sh.line(rx, y - 0.05, rx + rw, y - 0.05, layer=TB, lw=0.4)
    lv2 = plan["level_2"]
    lp2 = lv2["loop"]
    l2_drawn = fp - sum(area(o["rect"]) for o in lv2["open_below"])
    y -= 0.03
    sh.text(rx, y - 0.16, "AREA CHECK — D-057 (no SF cap, D-056)", size=9.0, bold=True)
    y -= 0.18
    at = [("", 0, "l"), ("DRAWN REV E", 1.75, "r"), ("REV D", 2.45, "r"), ("CHANGE", 3.10, "r"), ("PROGRAM G-003 G", 4.20, "r"), ("DRAWN − PROG.", rw, "r")]
    y -= rp
    for lab, dx, al in at:
        sh.text(rx + dx, y + 0.02, lab, size=6.4, bold=True, align="left" if al == "l" else "right", layer=TB)
    sh.line(rx, y - 0.04, rx + rw, y - 0.04, layer=TB, lw=0.6)

    def sgn(v):
        return ("+" if v > 0.05 else "−" if v < -0.05 else "±") + n(abs(v))
    for lab, d_, dd, pg in (("L1 FOOTPRINT", DR["L1"], DD["L1"], X_["F"]), ("L2 AREA", DR["L2"], DD["L2"], X_["L2"]),
                            ("TOTAL GSF", DR["G"], DD["G"], X_["F"] + X_["L2"])):
        y -= rp
        for (l_, dx, al), c in zip(at, [lab, n(d_), n(dd), sgn(d_ - dd), n(pg), sgn(d_ - pg)]):
            sh.text(rx + dx, y, c, size=7.0, bold=l_ in ("", "DRAWN REV E"), align="left" if al == "l" else "right", layer=TB)
    sh.line(rx, y - 0.05, rx + rw, y - 0.05, layer=TB, lw=0.4)
    y -= 0.06
    team = next(z for z in plan["level_1"]["zones"] if z["id"] == "team_asm")
    sw = next(r for r in plan["level_1"]["rooms"] if r["id"] == "storage_sw")
    if lvl == 1:
        txt = (f"Floor 120 x 144, east tier 16 ft from the mats (D-053). Program = footprint / L2 gross (R-021). Seats N {bys['N']['total']} / "
               f"S {bys['S']['total']} / E {bys['E']['total']} (Rev D {' / '.join(str(r_['lower'] + r_['upper']) for r_ in rows_f)}). Mech {n(mech_drawn)} vs "
               f"{n(X_['M'])}. FLEX kept: team assembly ≈ {n(area(team['rect']))}, FLEX / STORAGE {n(area(sw['rect']))} SF.")
    else:
        txt = (f"L2 = footprint minus open-to-below (arena 132 x 168, lobby 58 x 34). S&C {n(X_['sf']['strength_conditioning'])} program vs "
               f"{n(49 * 110.8 - 12.667 * 21.333)} drawn: the 76 in ST-1 takes {n(12.667 * 21.333 - 10.8 * 19)} SF more than Rev D (C-3).")
    y = sh.para(rx, y, rw, txt, size=6.9)
    sh.text(rx, y - 0.14, "ACCESS CONTROL + EGRESS (D-033 DECIDED; layout ASSUMED)" if lvl == 1 else
            "LEVEL 2 LOOP (D-035 DECIDED; geometry ASSUMED) + EGRESS", size=9.0, bold=True)
    y -= 0.16
    acc1 = ["ONE WAY IN (D-033): E1 → security checkpoint (size TBD) → lobby; teams go west through CD-1 to team assembly, athlete corridor, lockers.",
            "X1-X10 EXIT ONLY: alarmed, no exterior entry hardware, free egress (IBC 2021 1010.2), panic hardware (1010.2.9), no delayed egress in "
            "Group A (1010.2.13). > 1,000 per story → 4 exits (T1006.3.3); main exit ≥ 1/2 the load (1030.2); checkpoint must not narrow it (R-015).",
            "S1 service / deliveries at the north door (D-034 DECIDED); team / bus drop loop south, offset E / W of E1. Freestanding portal "
            "30 ft south of E1 over the 28 x 30 ft brick Champion Walk (D-043, D-046, D-050): outside, drawn on P2-C-101 / P2-A-201."]
    acc2 = [f"LOOP (D-035, Shane 4:55 AM CT): continuous around the top of Level 2 — rear walkway (N), walkway (E), upper concourse / "
            f"balcony (S) and a new west leg cut from S&C + cross-training. {lp2['lanes']} lanes x {lp2['lane_width_in']} in = {lp2['width_ft']:g} ft "
            f"everywhere, squared corners; {n(lg['centerline'])} ft centerline = {lg['laps_per_mile']:.2f} laps/mile.",
            "Lane width: UFC 4-740-02N 4.1.7 (indoor track ≥ 12 ft, 3 lanes x 42 in); Athletic Business (3 lanes of 36-42 in; max 12 "
            "laps/mile, 8-10 preferred). 2 lanes ASSUMED (3 would need 10.5 ft; the upper tier would move).",
            "Event days the loop is the upper concourse: spectators cross it at the upper-tier entries (marked, locations ASSUMED) and at "
            "the stairs / elevator, which open onto it. Training on non-event days; crossing users are a known track hazard (Athletic Business).",
            "Guards 42 in min. where the loop is open more than 30 in above the floor below (IBC 2021 1015.2, 1015.3; 4 in sphere 1015.4): "
            "west edge over the arena, south edge over the lobby. Tier backs: rail / guard per 1030.17 (architect).",
            "Stairs 76 in (D-052) with 76 in intermediate landings (D-051) = 12.67 x 21.33 ft, same spot both levels. ST-2 sits in a 21.33 x "
            "6.67 ft NE stair tower (Rev D 19 x 5): 6.67 ft is what keeps it clear of the loop's north leg. Egress: 4 stairs discharge at L1 "
            "through EXIT ONLY doors X4, X6, X9, X10 (D-033)."]
    for t_ in (acc1 if lvl == 1 else acc2):
        y = sh.para(rx, y + 0.02, rw, t_, size=6.4 if lvl == 1 else 6.6, indent=0.12, bullet="·")
    if lvl == 2:
        sh.text(rx, y - 0.14, "LAYOUT NOTES (KEYSTONE, ASSUMED — architect to confirm)", size=9.0, bold=True)
        y -= 0.16
    notes1 = ["D-049: rows 1-2 of the upper tier (front 6 ft) leave < 7'-6\" clear (≈ 1'-6\" structure ASSUMED): storage / mech only; event lockers "
              "start behind them. FINDING: EXIT (N), EXIT (E), SE concourse, lobby / portal / athlete-route edge also pass under rows 1-2; egress "
              "needs ≥ 7'-6\" (IBC 1003.2): omit or raise rows 1-2 there. Travel distance NOT checked."]
    notes2 = [f"Upper tier 15 ft deep: {up['rows']} rows x {up['row_depth_in']} in, {up['riser_in']} in risers (D-053; section P2-A-301 / A-302), stepping "
              "DOWN from the loop to the court (D-049). N / S bands now 132 ft (east shift); seat split by side changes, totals stay 1,100 + 1,100.",
              "6 ft stretch strip on the N side. Exit separation, travel distance, structure NOT checked. Floor-to-floor 15 ft ASSUMED."]
    for t_ in (notes1 if lvl == 1 else notes2):
        y = sh.para(rx, y + 0.02, rw, t_, size=6.4 if lvl == 1 else 6.6, indent=0.12, bullet="·")
    y = sh.para(rx, y - 0.02, rw, "Sources: phase2.yaml (D-009, D-030, D-033, D-034, D-035, D-049, D-051-D-053, D-056, D-057); Shane 2026-10-04 9:10 AM CT; "
                "P2-G-003 Rev G; R-008, R-009, R-014, R-015, R-020, R-021; IBC 2021 Ch. 10 (UpCodes, Alabama); UFC 4-740-02N (retrieved 2026-10-04). "
                "Geometry: params/phase2_plan_rev_e.yaml.", size=6.3)
    fl = body_bottom + 0.08
    if y < fl:
        raise SystemExit(f"LAYOUT OVERFLOW: right panel runs {fl - y:.2f} in into the stamp band")
    print(f"layout margin right panel (in): {y - fl:.2f}")
    return sh

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sheet", choices=list(LEVEL_OF), required=True)
    ap.add_argument("--png", help="optional PNG preview path (outside the repo)")
    ap.add_argument("--out-dir", help="write PDF/DXF here instead of phase2/out/{pdf,dxf}")
    ap.add_argument("--force", action="store_true", help="allow overwriting a FROZEN revision in the repo")
    ap.add_argument("--rev", choices=["A", "B", "C", "D", "E"], default="E",
                    help="A = first block plan (frozen); B = Shane 4:30 AM CT changes (frozen); C = single controlled entry, D-033 (frozen); D = Level 2 loop, D-035 (frozen); E = reviewer C-1..C-4: 76 in stairs, east +6 ft, D-049, D-057 (default)")
    a = ap.parse_args()
    if a.rev == "A":
        p2, prog, plan, F_, T_ = load_all()
        sh, rv_letter = build(a.sheet, p2, prog, plan, F_, T_)
    elif a.rev == "B":
        p2, prog, ob, out = tf.summary_e()
        sh, rv_letter = build_b(a.sheet, p2, prog, out["plan"], out["mix"], (out["rows"], out["tot"])), "B"
    elif a.rev == "E":
        p2, prog, ob, out = tf.summary_g()
        sh, rv_letter = build_e(a.sheet, p2, prog, out["plan"], out["loop"], (out["rows"], out["tot"]), out["geom"],
                                out["drawn"], out["drawn_d"], out["rev_f"]["rows"]), "E"
    elif a.rev == "D":
        p2, prog, ob, out_e = tf.summary_e()
        p2, prog, ob, out = tf.summary_f()
        if [(r["side"], r["lower"], r["upper"]) for r in out["rows"]] != [(r["side"], r["lower"], r["upper"]) for r in out_e["rows"]]:
            sys.exit(f"Rev D seat counts differ from P2-G-003 Rev E: {out['rows']}")
        sh, rv_letter = build_d(a.sheet, p2, prog, out["plan"], out["loop"], (out["rows"], out["tot"]), out["geom"]), "D"
    else:
        p2, prog, ob, out = tf.summary_e()
        plan_c = yaml.safe_load((BP / "params" / "phase2_plan_rev_c.yaml").read_text(encoding="utf-8"))
        rows_c, tot_c = tf.seats_by_side(plan_c, prog, out["mix"])
        if [(r["side"], r["lower"], r["upper"]) for r in rows_c] != [(r["side"], r["lower"], r["upper"]) for r in out["rows"]]:
            sys.exit(f"Rev C seat counts differ from P2-G-003 Rev E: {rows_c}")
        sh, rv_letter = build_c(a.sheet, p2, prog, plan_c, out["mix"], (rows_c, tot_c)), "C"
    rv = p2["sheets"][a.sheet]["revisions"][rv_letter]
    if a.out_dir:
        pdf, dxf = (Path(a.out_dir) / f"{rv['file']}.{e}" for e in ("pdf", "dxf"))
    else:
        pdf = BP / "phase2" / "out" / "pdf" / f"{rv['file']}.pdf"
        dxf = BP / "phase2" / "out" / "dxf" / f"{rv['file']}.dxf"
        if rv.get("frozen") and (pdf.exists() or dxf.exists()) and not a.force:
            sys.exit("Revision is FROZEN; use --out-dir to regenerate for checking.")
    pdf.parent.mkdir(parents=True, exist_ok=True)
    dxf.parent.mkdir(parents=True, exist_ok=True)
    sh.render_pdf(pdf, title=f"{a.sheet} Rev {rv_letter} {p2['sheets'][a.sheet]['title']}", png_path=a.png)
    sh.render_dxf(dxf)
    print(f"wrote {pdf}\nwrote {dxf}" + (f"\nwrote {a.png}" if a.png else ""))


if __name__ == "__main__":
    main()
