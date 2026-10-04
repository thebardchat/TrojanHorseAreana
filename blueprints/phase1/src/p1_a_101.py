"""P1-A-101 — Phase 1 existing conditions plan, wrestling room (11x17 landscape), vector PDF + DXF.

Rev A = ROOM OUTLINE ONLY:
  * inside-face rectangle from Shane's tape (phase1.yaml existing.wrestling_room.length_ft / width_ft)
  * dimension strings, north arrow, graphic scale, title block, PRELIMINARY stamp
  * door marks tagged APPROX. at positions read off Shane's aerial sketch
    (existing.wrestling_room.doors_approx); no dimensioned locations, no widths
  * support wing as a dashed, undimensioned, NOT-YET-MEASURED outline
The aerial estimate (estimate_aerial) is never used here.

Geometry is drawn on paper in INCHES at the sheet scale (sheets.P1-A-101.scale_in_per_ft),
so the PDF prints true to scale on 11x17 at 100%. The DXF uses the same paper-inch
geometry: 1 DXF inch = 8 ft at 1/8" = 1'-0" (scale by 96 for real-world inches).
Layout constants below are sheet geometry, not project dimensions.

Run from the repo root:
  /workspace/.venv-keystone/bin/python blueprints/phase1/src/p1_a_101.py --rev A [--png PATH]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

BP = Path(__file__).resolve().parents[2]          # blueprints/
sys.path.insert(0, str(BP / "shared"))
from titleblock import TEXT, Sheet, add_titleblock, pitch, text_width_in  # noqa: E402

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


def door_mark(sh, x, y, wall, tag, inside=False):
    """Open triangle on the wall pointing outward (like Shane's markup) + APPROX. tag. Not to scale."""
    s = 0.22
    out = {"west": (-1, 0), "east": (1, 0), "south": (0, -1), "north": (0, 1)}[wall]
    ox, oy = out
    px, py = -oy, ox                               # along-wall unit vector
    tip = (x + ox * s * 1.3, y + oy * s * 1.3)
    a = (x + px * s / 2, y + py * s / 2)
    b = (x - px * s / 2, y - py * s / 2)
    for p, q in ((a, tip), (tip, b), (b, a)):
        sh.line(*p, *q, layer=DOOR, lw=1.1)
    lines = tag.split("\n")
    if wall in ("west", "east") and inside:       # tag on the room side of the wall
        tx, ty, al = x - ox * 0.12, y + 0.02, "left" if wall == "west" else "right"
    elif wall == "west":
        tx, ty, al = tip[0] - 0.08, y + 0.02, "right"
    elif wall == "east":
        tx, ty, al = tip[0] + 0.08, y + 0.02, "left"
    else:                                          # south/north: tag beside the mark
        tx, ty, al = x + s * 0.8, y + (-0.15 if wall == "south" else 0.2), "left"
    for i, ln in enumerate(lines):
        sh.text(tx, ty - i * pitch(8.5), ln, size=8.5, bold=(i == 0), align=al, layer=DOOR)


def build(p1: dict, rev: str = "A") -> Sheet:
    meta, site = p1["meta"], p1["site"]
    room = p1["existing"]["wrestling_room"]
    sp = p1["sheets"][SHEET_NO]
    S = float(sp["scale_in_per_ft"])
    L_ns, W_ew = float(room["length_ft"]), float(room["width_ft"])   # tape, inside

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
    ox = 2.0                                        # room SW corner (inside face) on paper
    oy = body_bottom + 0.6
    assert oy + ph + 0.75 < top - 0.1, "plan does not fit the sheet body at this scale"
    sh.rect(ox, oy, pw, ph, layer=WALL, lw=2.2)
    cx, cy = ox + pw / 2, oy + ph / 2
    sh.text(cx, cy + 0.12, "WRESTLING ROOM", size=14, bold=True, align="center")
    sh.text(cx, cy - 0.12, f"{ft_in(L_ns)} × {ft_in(W_ew)} (inside, tape)", size=10, align="center")
    sh.text(cx, cy - 0.32, f"Floor area (calc.): {room['floor_area_sf_calc']:,} SF", size=9, align="center")
    sh.text(cx, cy - 0.52, f"Wall thickness: {room['wall_thickness']}", size=9, align="center")

    # dimension strings (overall only)
    dim_h(sh, ox, ox + pw, oy + ph + 0.55, oy + ph, ft_in(W_ew))
    dim_v(sh, oy, oy + ph, ox - 0.55, ox, ft_in(L_ns))

    # doors, APPROX.
    labels = {"exit_west": "EXIT — APPROX.\nlocation/size TBD", "exit_south": "EXIT — APPROX.\nlocation/size TBD",
              "exit_northeast": "EXIT — APPROX.\nlocation/size TBD", "hallway_door": "HALLWAY DOOR — APPROX.\nto support wing; size TBD"}
    for key, d in room["doors_approx"].items():
        f = float(d["fraction_approx"])
        if d["wall"] in ("west", "east"):
            x = ox if d["wall"] == "west" else ox + pw
            y = oy + ph - f * ph if d["along_wall_from"] == "north" else oy + f * ph
        else:
            y = oy if d["wall"] == "south" else oy + ph
            x = ox + f * pw if d["along_wall_from"] == "west" else ox + pw - f * pw
        door_mark(sh, x, y, d["wall"], labels[key], inside=key in ("exit_west", "hallway_door"))

    # support wing: dashed, schematic, undimensioned (sheet-geometry placeholder, not a size)
    wx0, wx1 = ox + pw, ox + pw + 3.0               # attached to the east wall (3 dashed sides)
    wy1, wy0 = oy + ph * 0.55, oy - 0.35
    for a, b in (((wx0, wy0), (wx1, wy0)), ((wx1, wy0), (wx1, wy1)), ((wx1, wy1), (wx0, wy1))):
        sh.dashed(*a, *b, layer=WING, lw=0.8)
    sh.dashed(wx0, oy, wx0, wy0, layer=WING, lw=0.8)   # wing's west edge south of the room
    wcx = (wx0 + wx1) / 2 + 0.15
    sh.text(wcx, (wy0 + wy1) / 2 + 0.25, "SUPPORT WING", size=11, bold=True, align="center", layer=WING)
    sh.text(wcx, (wy0 + wy1) / 2 + 0.05, "NOT YET MEASURED", size=11, bold=True, align="center", layer=WING)
    sh.text(wcx, (wy0 + wy1) / 2 - 0.18, sp["support_wing_note"], size=8, align="center", layer=WING)

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
    y = top - 1.35
    sh.text(nx0, y, "NOTES", size=12, bold=True)
    y -= 0.12
    for i, n in enumerate(sp["notes"], 1):
        y = sh.para(nx0, y, ncw, n, size=9.5, indent=0.25, bullet=f"{i}.")
    y -= 0.35
    sh.text(nx0, y, "LEGEND", size=12, bold=True)
    y -= 0.35
    sh.line(nx0, y + 0.05, nx0 + 0.5, y + 0.05, layer=WALL, lw=2.2)
    sh.text(nx0 + 0.65, y, "Inside face of wall (tape-measured)", size=9.5)
    y -= 0.3
    sh.dashed(nx0, y + 0.05, nx0 + 0.5, y + 0.05, layer=WING, lw=0.8)
    sh.text(nx0 + 0.65, y, "Not yet measured (schematic only)", size=9.5)
    y -= 0.32
    door_mark(sh, nx0 + 0.2, y + 0.04, "east", "")
    sh.text(nx0 + 0.65, y, "Door / exit mark — APPROX. location, size TBD", size=9.5)
    return sh


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", default="A", choices=["A"], help="sheet revision (A = room outline only)")
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
