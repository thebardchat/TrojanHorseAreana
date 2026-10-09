"""P1-A-101 Rev B — Phase 1 existing conditions plan, wrestling room: wall orientation + existing conditions (D-088).

Built from p1_a_101.py (Rev A, frozen, untouched). Adds wall labels N / S / E / W, doors moved per Shane's photos 2026-10-09
(APPROX, not measured), AC units, exit sign, coach area, mats (existing conditions). Room dimensions unchanged.
Overrides: params/phase1_a101_rev_b.yaml.
Run from the repo root:
  /workspace/.venv-keystone/bin/python blueprints/phase1/src/p1_a_101_rev_b.py --rev B
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

BP = Path(__file__).resolve().parents[2]          # blueprints/
sys.path.insert(0, str(BP / "shared"))
from titleblock import TEXT, Sheet, add_titleblock, pitch, text_width_in  # noqa: E402
from palette import SCHOOL_RED, INK_MUTED  # noqa: E402
EXIST = "A-FLOR-EXST"

SHEET_NO = "P1-A-101"
W, H = 17.0, 11.0
M = 0.5
WALL, DOOR, DIMS, WING = "A-WALL", "A-DOOR-IDEN", "A-ANNO-DIMS", "A-WALL-NMSR"


def ft_in(ft: float) -> str:
    whole = int(ft)
    inches = round((ft - whole) * 12)
    return f"{whole}'-{inches}\""


def dim_h(sh, xa, xb, y, yref, label, size=10):
    """Horizontal dimension string at height y, extension lines down/up to yref, 45° ticks."""
    sh.line(xa, y, xb, y, layer=DIMS, lw=0.5)
    for x in (xa, xb):
        sh.line(x, yref + (0.06 if y > yref else -0.06), x, y + (0.08 if y > yref else -0.08), layer=DIMS, lw=0.4)
        sh.line(x - 0.06, y - 0.06, x + 0.06, y + 0.06, layer=DIMS, lw=1.0)
    sh.text((xa + xb) / 2, y + 0.06, label, size=size, bold=True, align="center", layer=DIMS)


def dim_v(sh, ya, yb, x, xref, label, size=10):
    """Vertical dimension string at x, extension lines to xref, 45° ticks, rotated label."""
    sh.line(x, ya, x, yb, layer=DIMS, lw=0.5)
    for y in (ya, yb):
        sh.line(xref + (-0.06 if x < xref else 0.06), y, x + (-0.08 if x < xref else 0.08), y, layer=DIMS, lw=0.4)
        sh.line(x - 0.06, y - 0.06, x + 0.06, y + 0.06, layer=DIMS, lw=1.0)
    sh.text(x - 0.06, (ya + yb) / 2, label, size=size, bold=True, align="center", layer=DIMS, rot=90)


NORMALS = {"west": ((-1, 0), (0, 1)), "east": ((1, 0), (0, 1)), "south": ((0, -1), (1, 0)), "north": ((0, 1), (1, 0))}


def wall_with_openings(sh, start, u, n, L, t, gaps, lw_in=1.6, lw_out=1.0):
    """Double-line wall: inner face from s=0..L at `start`, outer face offset t along n (s=-t..L+t).
    gaps = list of (a, b) door openings along s. Jamb lines close each opening."""
    def P(s, off):
        return (start[0] + u[0] * s + n[0] * off, start[1] + u[1] * s + n[1] * off)
    for off, s0, s1, lw in ((0.0, 0.0, L, lw_in), (t, -t, L + t, lw_out)):
        cur = s0
        for a, b in sorted(gaps):
            sh.line(*P(cur, off), *P(a, off), layer=WALL, lw=lw)
            cur = b
        sh.line(*P(cur, off), *P(s1, off), layer=WALL, lw=lw)
    for a, b in gaps:
        for s in (a, b):
            sh.line(*P(s, 0), *P(s, t), layer=WALL, lw=0.8)
    return P


def door_swing(sh, P, a, b, t, n, u, segs=18):
    """Single leaf hinged at s=a on the outer face, swinging outward (ASSUMED). Leaf + 90° arc to s=b."""
    import math
    hx, hy = P(a, t)
    r = b - a
    sh.line(hx, hy, hx + n[0] * r, hy + n[1] * r, layer=DOOR, lw=1.0)
    pts = []
    for i in range(segs + 1):
        th = math.radians(90 * i / segs)
        pts.append((hx + r * (math.cos(th) * n[0] + math.sin(th) * u[0]),
                    hy + r * (math.cos(th) * n[1] + math.sin(th) * u[1])))
    for p, q in zip(pts[:-1], pts[1:]):
        sh.line(*p, *q, layer=DOOR, lw=0.4)


def tag(sh, x, y, lines, align, size=8):
    for i, ln in enumerate(lines):
        sh.text(x, y - i * pitch(size), ln, size=size, bold=(i == 0), align=align, layer=DOOR)


def build(p1: dict, rev: str = "B") -> Sheet:
    RB = yaml.safe_load((BP / "params" / "phase1_a101_rev_b.yaml").read_text(encoding="utf-8"))
    p1["sheets"][SHEET_NO]["subtitle"] = RB["meta"]["subtitle"]
    p1["sheets"][SHEET_NO]["notes"] = RB["notes"]
    p1["existing"]["wrestling_room"]["doors_approx"] = RB["doors"]
    meta, site = p1["meta"], p1["site"]
    room = p1["existing"]["wrestling_room"]
    door = room["door_assumed"]
    sp = p1["sheets"][SHEET_NO]
    S = float(sp["scale_in_per_ft"])
    L_ns, W_ew = float(room["length_ft"]), float(room["width_ft"])   # tape, inside
    t = room["wall_thickness_assumed_in"] / 12.0 * S                  # ASSUMED wall, paper inches
    dw = float(door["width_ft"]) * S                                    # ASSUMED door width, paper inches

    sh = Sheet(W, H)
    body_bottom = add_titleblock(sh, {
        "project": f"{meta['project']}\n{site['location']}",
        "phase": f"PHASE {meta['phase']}\n{meta['type'].upper()}",
        "title": f"{sp['title']}\n{sp['subtitle']}",
        "sheet_no": SHEET_NO,
        "scale": sp["scale"],
        "date": meta["sheet_date"],
        "revision": rev,
        "drawn_by": meta["drawn_by"],
        "stamp": meta["stamp"],
    }, margin=M, tb_h=0.95, stamp_h=0.40)

    top = H - M
    nx0 = 11.35                                     # right-hand column: heading, notes, legend, scale
    sh.text(nx0, top - 0.42, sp["title"], size=16, bold=True)
    sh.text(nx0, top - 0.68, sp["subtitle"], size=11, bold=True)
    sh.text(nx0, top - 0.90, f"Scale {sp['scale']} (11x17 printed at 100%)", size=9.5)

    # ---- plan --------------------------------------------------------------
    pw, ph = W_ew * S, L_ns * S
    ox = 2.15                                       # room SW corner (inside face) on paper
    oy = body_bottom + 0.62
    assert oy + ph + 0.75 < top - 0.1, "plan does not fit the sheet body at this scale"
    walls = {"west": ((ox, oy), ph), "east": ((ox + pw, oy), ph), "south": ((ox, oy), pw), "north": ((ox, oy + ph), pw)}

    # door centers along each wall (s measured along u from the wall's start corner)
    doors = {}
    for key, d in room["doors_approx"].items():
        f = float(d["fraction_approx"])
        L = walls[d["wall"]][1]
        s_c = L * (1 - f) if d["along_wall_from"] in ("north", "east") else L * f
        doors[key] = (d["wall"], s_c - dw / 2, s_c + dw / 2)
    # existing conditions (APPROX from photos): zones dashed, points as markers
    for it in RB["existing"]:
        if it["kind"] == "zone":
            x0, y0, x1, y1 = it["rect"]
            a, b = (ox + x0 * S, oy + y0 * S), (ox + x1 * S, oy + y1 * S)
            for p, q in (((a[0], a[1]), (b[0], a[1])), ((b[0], a[1]), (b[0], b[1])), ((b[0], b[1]), (a[0], b[1])), ((a[0], b[1]), (a[0], a[1]))):
                sh.dashed(*p, *q, layer=EXIST, lw=0.5, dash=0.07, gap=0.05)
    Pw = {}
    for wname, (start, L) in walls.items():
        n, u = NORMALS[wname]
        gaps = [(a, b) for (wl, a, b) in doors.values() if wl == wname]
        Pw[wname] = wall_with_openings(sh, start, u, n, L, t, gaps)
    for key, (wl, a, b) in doors.items():
        n, u = NORMALS[wl]
        if room["doors_approx"][key].get("unconfirmed"):
            p, q = Pw[wl](a, t), Pw[wl](b, t)
            sh.dashed(p[0], p[1], q[0], q[1], layer=DOOR, lw=1.2, dash=0.05, gap=0.04)
            continue
        door_swing(sh, Pw[wl], a, b, t, n, u)

    for key, (wl, a, b) in doors.items():
        mid = Pw[wl]((a + b) / 2, 0)
        tg = room["doors_approx"][key]["tag"]
        if key == "exit_west":                      # tag inside the room (dimension string is outside)
            tag(sh, mid[0] + 0.12, mid[1] - 0.25, tg, "left")
        elif key == "hallway_door":
            tag(sh, mid[0] - 0.12, mid[1] - 0.05, tg, "right")
        elif key == "exit_northeast":
            for i_, ln in enumerate(tg):
                sh.text(mid[0] - 0.12, mid[1] - 0.05 - i_ * pitch(8), ln, size=8, bold=i_ == 0, align="right", layer=DOOR, color=SCHOOL_RED)
        else:                                       # south exit: tag below the wall, west of the dims
            tag(sh, mid[0] + 0.3, mid[1] - t - 0.2, tg, "left")
    # existing-condition labels
    for it in RB["existing"]:
        if it["kind"] == "zone":
            x0, y0, x1, y1 = it["rect"]
            if it["id"] == "comp_mat":
                sh.text(ox + (x0 + x1) / 2 * S, oy + y1 * S - 0.5, it["label"], size=8.5, align="center", layer=EXIST, color=INK_MUTED)
            elif it["id"] == "rubber":
                sh.text(ox + 41 * S, oy + 0.06, "RUBBER STRIP", size=6.5, align="right", layer=EXIST, color=INK_MUTED)
            elif it["id"] == "coach":
                sh.text(ox + (x0 + x1) / 2 * S, oy + y1 * S + 0.06, "COACH AREA (existing)", size=8, bold=True, align="center", layer=EXIST)
                sh.text(ox + (x0 + x1) / 2 * S, oy + 3.6 * S, "desk, TV, corkboard, lockers, mat carts", size=6.5, align="center", layer=EXIST)
            else:
                sh.text(ox + (x0 + x1) / 2 * S, oy + (y0 + y1) / 2 * S - 0.04, it["label"], size=7, align="center", layer=EXIST, color=INK_MUTED)
        else:
            x, y = ox + it["xy"][0] * S, oy + it["xy"][1] * S
            sh.rect(x - 0.06, y - 0.06, 0.12, 0.12, layer=EXIST, lw=1.0)
            dy = -0.2 if it["xy"][1] > 1 else 0.13
            if it["id"] == "exit_sign":
                sh.text(x + 0.12, y + 0.45, it["label"], size=7.5, bold=True, layer=EXIST)
            else:
                sh.text(x, y + dy, it["label"], size=7, bold=True, align="center", layer=EXIST)
    # wall labels N / S / E / W (outside each wall)
    wl_ = RB["walls"]
    sh.text(ox + pw / 2, oy + ph + 0.22, wl_["north"]["label"], size=9.5, bold=True, align="center")
    sh.text(ox + pw * 0.75, oy - t - 0.3, wl_["south"]["label"], size=9.5, bold=True, align="center")
    sh.text(ox - t - 0.12, oy + ph * 0.80, wl_["west"]["label"], size=9.5, bold=True, align="center", rot=90)
    sh.text(ox + pw + t + 0.18, oy + ph * 0.82, wl_["east"]["label"], size=9.5, bold=True, align="center", rot=90)

    cx, cy = ox + pw / 2, oy + ph / 2 + 0.3
    sh.text(cx, cy + 0.22, "WRESTLING ROOM", size=14, bold=True, align="center")
    sh.text(cx, cy - 0.02, f"{ft_in(L_ns)} × {ft_in(W_ew)} (inside, tape)", size=10, align="center")
    sh.text(cx, cy - 0.24, room["ceiling_label"], size=11, bold=True, align="center")
    sh.text(cx, cy - 0.44, f"Floor area (calc.): {room['floor_area_sf_calc']:,} SF", size=9, align="center")
    # wall tag with leader (north wall)
    wtx, wty = ox + 0.35, oy + ph - 0.45
    sh.text(wtx, wty, f"WALLS: {room['wall_thickness_label']}", size=8.5, bold=True)
    sh.line(wtx + 0.1, wty + 0.12, wtx + 0.1, oy + ph + t / 2, layer=DIMS, lw=0.5)

    # dimension strings (inside face, overall only)
    dim_h(sh, ox, ox + pw, oy + ph + 0.62, oy + ph, f"{ft_in(W_ew)} INSIDE")
    dim_v(sh, oy, oy + ph, ox - 0.8, ox, f"{ft_in(L_ns)} INSIDE")

    # support wing: dashed, schematic, undimensioned (sheet-geometry placeholder, not a size)
    wx0, wx1 = ox + pw + t, ox + pw + t + 3.0       # attached to the east wall (3 dashed sides)
    wy1, wy0 = oy + ph * 0.55, oy - 0.35
    for a, b in (((wx0, wy0), (wx1, wy0)), ((wx1, wy0), (wx1, wy1)), ((wx1, wy1), (wx0, wy1))):
        sh.dashed(*a, *b, layer=WING, lw=0.8)
    sh.dashed(wx0, oy - t, wx0, wy0, layer=WING, lw=0.8)   # wing's west edge south of the room
    wcx = (wx0 + wx1) / 2 + 0.3
    wcy = (wy0 + wy1) / 2 - 0.35
    sh.text(wcx, wcy + 0.25, "SUPPORT WING", size=11, bold=True, align="center", layer=WING)
    sh.text(wcx, wcy + 0.05, "NOT YET MEASURED", size=11, bold=True, align="center", layer=WING)
    sh.text(wcx, wcy - 0.18, sp["support_wing_note"], size=8, align="center", layer=WING)

    # north arrow
    nx, ny = ox + pw + 2.3, oy + ph + 0.1
    sh.line(nx, ny, nx, ny + 0.75, lw=1.2)
    sh.line(nx, ny + 0.75, nx - 0.12, ny + 0.5, lw=1.2)
    sh.line(nx, ny + 0.75, nx + 0.12, ny + 0.5, lw=1.2)
    sh.line(nx - 0.12, ny + 0.5, nx + 0.12, ny + 0.5, lw=0.8)
    sh.text(nx, ny + 0.85, "N", size=14, bold=True, align="center")
    sh.text(nx, ny - 0.18, "approx.", size=8, align="center")

    # graphic scale: 0-4-8-16 ft
    gx, gy = nx0, body_bottom + 0.3
    marks = [0, 4, 8, 16]
    for a, b in zip(marks[:-1], marks[1:]):
        sh.rect(gx + a * S, gy, (b - a) * S, 0.08, layer=DIMS, lw=0.6)
    for mk in marks:
        sh.text(gx + mk * S, gy + 0.14, f"{mk}'", size=7.5, align="center", layer=DIMS)
    sh.text(gx + 16 * S + 0.15, gy, f"GRAPHIC SCALE  {sp['scale']}", size=8, layer=DIMS)

    # ---- notes column --------------------------------------------------------
    ncw = W - M - 0.15 - nx0
    y = top - 1.3
    sh.text(nx0, y, "NOTES", size=12, bold=True)
    y -= 0.1
    for i, nt in enumerate(sp["notes"], 1):
        y = sh.para(nx0, y, ncw, nt, size=9, indent=0.25, bullet=f"{i}.")
    y -= 0.3
    sh.text(nx0, y, "LEGEND", size=12, bold=True)
    y -= 0.32
    # wall sample: double line
    sh.line(nx0, y + 0.05, nx0 + 0.5, y + 0.05, layer=WALL, lw=1.6)
    sh.line(nx0, y + 0.05 + 0.083, nx0 + 0.5, y + 0.05 + 0.083, layer=WALL, lw=1.0)
    yy = sh.para(nx0 + 0.65, y + pitch(9), ncw - 0.65, "CMU wall, 8\" ASSUMED (inner line = tape-measured inside face)", size=9)
    y = min(y - 0.42, yy - 0.2)
    # door sample
    P = lambda s, off: (nx0 + 0.05 + s, y - 0.02 + off)   # noqa: E731
    sh.line(nx0 - 0.05, y - 0.02, nx0 + 0.05, y - 0.02, layer=WALL, lw=1.6)
    sh.line(nx0 + 0.05 + dw, y - 0.02, nx0 + 0.15 + dw, y - 0.02, layer=WALL, lw=1.6)
    door_swing(sh, P, 0.0, dw, 0.0, (0, 1), (1, 0))
    yy = sh.para(nx0 + 0.65, y + pitch(9), ncw - 0.65, "Door, 3'-0\" leaf + swing — ASSUMED STANDARD, VERIFY; location APPROX.", size=9)
    y = min(y - 0.3, yy - 0.22)
    sh.dashed(nx0, y + 0.05, nx0 + 0.5, y + 0.05, layer=EXIST, lw=0.5, dash=0.07, gap=0.05)
    sh.rect(nx0 + 0.22, y + 0.0, 0.1, 0.1, layer=EXIST, lw=1.0)
    yy = sh.para(nx0 + 0.65, y + pitch(9), ncw - 0.65, "Existing condition (mat, zone / device), APPROX from photos 2026-10-09", size=9)
    y = min(y - 0.3, yy - 0.22)
    sh.dashed(nx0, y + 0.05, nx0 + 0.5, y + 0.05, layer=WING, lw=0.8)
    sh.text(nx0 + 0.65, y, "Not yet measured (schematic only)", size=9)
    fits_bottom = body_bottom + 0.55
    if y < fits_bottom:
        raise SystemExit(f"LAYOUT OVERFLOW: notes/legend run {fits_bottom - y:.2f} in into the scale bar")
    return sh


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", choices=["B"], help="sheet revision (B = walls + existing conditions, D-088)")
    ap.add_argument("--png", help="optional PNG preview path (outside the repo)")
    ap.add_argument("--out-dir", help="write PDF/DXF here instead of phase1/out/{pdf,dxf}")
    ap.add_argument("--force", action="store_true", help="allow overwriting a FROZEN revision in the repo")
    a = ap.parse_args()
    p1 = yaml.safe_load((BP / "params" / "phase1.yaml").read_text(encoding="utf-8"))
    rv = p1["sheets"][SHEET_NO]["revisions"][a.rev]
    if a.out_dir:
        pdf, dxf = (Path(a.out_dir) / f"{rv['file']}.{e}" for e in ("pdf", "dxf"))
    else:
        pdf = BP / "phase1" / "out" / "pdf" / f"{rv['file']}.pdf"
        dxf = BP / "phase1" / "out" / "dxf" / f"{rv['file']}.dxf"
        if rv.get("frozen") and (pdf.exists() or dxf.exists()) and not a.force:
            sys.exit(f"Rev {a.rev} is FROZEN; use --out-dir to regenerate for checking.")
    sh = build(p1, a.rev)
    pdf.parent.mkdir(parents=True, exist_ok=True)
    dxf.parent.mkdir(parents=True, exist_ok=True)
    sh.render_pdf(pdf, title=f"{SHEET_NO} Rev {a.rev} {p1['sheets'][SHEET_NO]['title']}", png_path=a.png)
    sh.render_dxf(dxf)
    print(f"wrote {pdf}\nwrote {dxf}" + (f"\nwrote {a.png}" if a.png else ""))


if __name__ == "__main__":
    main()
