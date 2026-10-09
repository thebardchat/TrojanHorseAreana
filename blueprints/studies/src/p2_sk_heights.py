"""KEYSTONE P2-SK-01 / P2-SK-02 — height STUDY sheets (not set revisions). Shane 2026-10-09 3:56 PM CT.

SK-01: mech / elec bay height (north elevation close-up, key plan, options a / b / c).
SK-02: NE drum height (north elevation close-up, key plan, options a / b / c).
Item being decided in red, everything else faded gray. Values from params/phase2_studies_sk.yaml; plan from p2_plan_rev_n_geom.py.
Usage (from the repo root):
  /workspace/.venv-keystone/bin/python blueprints/studies/src/p2_sk_heights.py --sheet SK-01|SK-02 [--out-dir DIR]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

BP = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BP / "shared"))
sys.path.insert(0, str(BP / "phase2" / "src"))
from palette import SCHOOL_RED, INK_MUTED, LIGHT_GRAY, WHITE  # noqa: E402
from titleblock import Sheet, add_titleblock  # noqa: E402
import p2_plan_rev_n_geom as gn  # noqa: E402

gm = gn.gm
W, H, M = 17.0, 11.0, 0.5
FADE = "#E6E6E6"
FADE2 = "#D4D4D4"
RED_FILL = "#F3C4C4"
NAMES = {"SK-01": "P2-SK-01_MechBay_Height", "SK-02": "P2-SK-02_Drum_Height"}


def rd(n):
    return yaml.safe_load((BP / "params" / n).read_text(encoding="utf-8"))


def ftin(z):
    f = int(z)
    i = round((z - f) * 12)
    if i == 12:
        f, i = f + 1, 0
    return f"{f}'-{i}\""


class El:
    """North elevation (viewer looks south): h = X0 - x (east on the left), z up."""
    def __init__(self, sh, x0, y0, fpi, xa, xb):
        self.sh, self.x0, self.y0, self.s, self.xa, self.xb = sh, x0, y0, 1.0 / fpi, xa, xb

    def P(self, x, z):
        return self.x0 + (self.xb - x) * self.s, self.y0 + z * self.s

    def mass(self, x0, x1, z, fill, edge, lw):
        x0, x1 = max(x0, self.xa), min(x1, self.xb)
        if x1 <= x0:
            return
        pts = [self.P(x0, 0), self.P(x1, 0), self.P(x1, z), self.P(x0, z)]
        self.sh.poly(pts, fill=fill, lw=lw, edge=edge)

    def hline(self, z, color, lw=0.6, dashed=False, label=None, size=11):
        a, b = self.P(self.xb, z), self.P(self.xa, z)
        if dashed:
            self.sh.dashed(a[0], a[1], b[0], b[1], lw=lw, dash=0.1, gap=0.07)
        else:
            self.sh.line(a[0], a[1], b[0], b[1], lw=lw)
        if label:
            self.sh.text(b[0] + 0.1, b[1] - 0.06, label, size=size, color=color)

    def vdim(self, x, z, label, color, size=12, bold=True, left=False):
        a, b = self.P(x, 0), self.P(x, z)
        self.sh.line(a[0], a[1], b[0], b[1], lw=1.0 if color == SCHOOL_RED else 0.5)
        for p in (a, b):
            self.sh.line(p[0] - 0.07, p[1], p[0] + 0.07, p[1], lw=1.0 if color == SCHOOL_RED else 0.5)
        self.sh.text(b[0] + (-0.08 if left else 0.08), b[1] - 0.2, label, size=size, bold=bold, color=color, align="right" if left else "left")


def masses(item, zi):
    """(x0, x1, z, is_item) back to front, north view."""
    S = rd("phase2_studies_sk.yaml")["heights"]
    ar = (49.0, 210.0)
    an, ba, bo = gm.ANNEX.bounds, gm.BAY.bounds, gm.BUMP.bounds
    dx0, _, dx1, _ = gm.drum.bounds
    out = [(bo[0], bo[2], S["annex"]["value"] if False else 16.0, False),
           (ar[0], ar[1], S["high_roof"]["value"], False),
           (0.0, 210.0, S["ring_roof"]["value"], False),
           (dx0, dx1, zi if item == "drum" else S["drum"]["value"], item == "drum"),
           (an[0], an[2], S["annex"]["value"], False),
           (ba[0], ba[2], zi if item == "bay" else S["bay"]["value"], item == "bay")]
    if item == "bay":          # bay in front of everything: draw last
        return out
    return [m for m in out if not m[3]] + [m for m in out if m[3]]


def draw_el(el, item, zi, lw_item=2.0):
    for x0, x1, z, it in masses(item, zi):
        el.mass(x0, x1, z, RED_FILL if it else FADE, SCHOOL_RED if it else LIGHT_GRAY, lw_item if it else 0.5)
    a, b = el.P(el.xb, 0), el.P(el.xa, 0)
    el.sh.line(a[0] - 0.1, a[1], b[0] + 0.1, b[1], lw=1.6)


def key_plan(sh, x0, y0, fpi, item):
    s = 1.0 / fpi

    def P(x, y):
        return x0 + x * s, y0 + y * s
    for po in (gm.ANNEX, gm.BUMP, gm.env):
        sh.poly([P(*q) for q in po.exterior.coords], fill=FADE, lw=0.5, edge=LIGHT_GRAY)
    other = gm.drum if item == "bay" else gm.BAY
    sh.poly([P(*q) for q in other.exterior.coords], fill=FADE2, lw=0.5, edge=LIGHT_GRAY)
    tgt = gm.BAY if item == "bay" else gm.drum
    sh.poly([P(*q) for q in tgt.exterior.coords], fill=SCHOOL_RED, lw=1.2, edge=SCHOOL_RED)
    c = tgt.centroid
    tx, ty = P(c.x - 20, c.y + 45)
    sh.text(tx, ty, "MECH / ELEC BAY" if item == "bay" else "30 FT DRUM", size=11, bold=True, align="center", color=SCHOOL_RED)
    ax, ay = P(-12, 250)
    sh.line(ax, ay - 0.3, ax, ay + 0.15, lw=1.2)
    sh.poly([(ax - 0.07, ay + 0.08), (ax, ay + 0.24), (ax + 0.07, ay + 0.08)], fill="#000000", lw=0)
    sh.text(ax, ay + 0.3, "N", size=12, bold=True, align="center")
    sh.text(x0, y0 - 0.32, "KEY PLAN (P2-A-101 Rev N) · not to scale", size=11, bold=True)
    sh.text(x0, y0 - 0.55, "looking south at the north side", size=10, color=INK_MUTED)
    vx, vy = P(25, 300)
    sh.line(vx, vy + 0.25, vx, vy, lw=1.0)
    sh.poly([(vx - 0.06, vy + 0.08), (vx, vy - 0.04), (vx + 0.06, vy + 0.08)], fill="#000000", lw=0)
    sh.text(vx + 0.1, vy + 0.12, "view", size=10, color=INK_MUTED)


def build(which):
    p2, S = rd("phase2.yaml"), rd("phase2_studies_sk.yaml")
    hz = S["heights"]
    item = "bay" if which == "SK-01" else "drum"
    opts = S["sk01_options"] if item == "bay" else S["sk02_options"]
    sh = Sheet(W, H)
    meta2 = p2["meta"]
    bb = add_titleblock(sh, {
        "project": f"{meta2['project']}\n{meta2['arena_name']} · {meta2['location']}",
        "phase": "PHASE 2",
        "title": ("STUDY: MECH / ELEC BAY\nHEIGHT (to decide)" if item == "bay" else "STUDY: NE DRUM\nHEIGHT (to decide)"),
        "scale": "NTS",
        "date": S["meta"]["date"],
        "revision": "STUDY",
        "drawn_by": meta2["drawn_by"],
        "sheet_no": f"P2-{which}",
        "stamp": meta2["stamp"],
    }, margin=M, tb_h=0.95, stamp_h=0.40)
    # heading
    q = "How tall should the mech / elec bay be?" if item == "bay" else "How tall should the NE stair drum be?"
    sh.text(0.85, 10.05, q, size=24, bold=True)
    sh.text(0.85, 9.68, "Red = the thing to decide. Gray = everything else, as drawn (A-201 Rev K / A-901 Rev F). Pick (a), (b) or (c) below.",
            size=12.5, color=INK_MUTED)
    # main elevation
    if item == "bay":
        xa, xb, fpi, x0, y0 = 40.0, 215.0, 18.0, 0.95, 6.15
    else:
        xa, xb, fpi, x0, y0 = 110.0, 215.0, 11.0, 0.95, 5.7
    el = El(sh, x0, y0, fpi, xa, xb)
    zi = hz[item]["value"]
    draw_el(el, item, zi)
    el.hline(hz["l2_ff"]["value"], INK_MUTED, lw=0.5, dashed=True, label=f"L2 floor {ftin(hz['l2_ff']['value'])} (decided, D-061)")
    rx = xa - 3                      # dims at the west (right-hand) end
    if item == "bay":
        ba, an = gm.BAY.bounds, gm.ANNEX.bounds
        el.vdim((ba[0] + ba[2]) / 2, zi, f"BAY {ftin(zi)} (ASSUMED)", SCHOOL_RED, size=15)
        el.vdim(an[0] + 12, hz["annex"]["value"], f"annex {ftin(hz['annex']['value'])} (ASSUMED)", INK_MUTED, size=12, bold=False)
        el.vdim(185.0, hz["ring_roof"]["value"], f"ring roof {ftin(hz['ring_roof']['value'])} (ASSUMED)", INK_MUTED, size=12, bold=False)
        el.vdim(100.0, hz["high_roof"]["value"], f"high roof {ftin(hz['high_roof']['value'])} (ASSUMED)", INK_MUTED, size=12, bold=False)
        lab = [((ba[0] + ba[2]) / 2, 5.0, "MECH / ELEC BAY"), ((an[0] + an[2]) / 2, 5.0, "storage annex"), (190.0, 5.0, "drum")]
    else:
        dx0, _, dx1, _ = gm.drum.bounds
        el.vdim(gm.DC[0], zi, f"DRUM {ftin(zi)} (ASSUMED)", SCHOOL_RED, size=15)
        el.vdim(112.0, hz["ring_roof"]["value"], f"ring roof {ftin(hz['ring_roof']['value'])} (ASSUMED)", INK_MUTED, size=12, bold=False)
        el.vdim(130.0, hz["high_roof"]["value"], f"high roof {ftin(hz['high_roof']['value'])} (ASSUMED)", INK_MUTED, size=12, bold=False)
        lab = [(gm.DC[0], 4.0, "30 FT DRUM (ST-2)"), (149.0, 4.0, "bay"), (116.0, 4.0, "annex")]
    for x, z, t in lab:
        p = el.P(x, z)
        sh.text(p[0], p[1], t, size=12 if t.isupper() else 11, bold=t.isupper(), align="center", color=SCHOOL_RED if t.isupper() else INK_MUTED)
    p = el.P(xb, -6 if item == "bay" else -4)
    sh.text(p[0], p[1], "NORTH ELEVATION, CLOSE-UP (east on the left) · not to scale", size=12, bold=True)
    # options row
    sh.text(0.85, 4.45, "CHOICES", size=16, bold=True)
    for k, o in enumerate(opts):
        tx0 = 0.95 + k * 3.75
        if item == "bay":
            e2 = El(sh, tx0, 3.1, 62.0, 100.0, 215.0)
        else:
            e2 = El(sh, tx0, 3.1, 38.0, 125.0, 215.0)
        draw_el(e2, item, o["z"], lw_item=1.4)
        top = e2.P((gm.BAY.bounds[0] + gm.BAY.bounds[2]) / 2 if item == "bay" else gm.DC[0], o["z"])
        sh.text(top[0], top[1] + 0.06, ftin(o["z"]), size=11, bold=True, align="center", color=SCHOOL_RED)
        sh.text(tx0, 2.85, o["title"], size=12, bold=True, color=SCHOOL_RED)
        sh.para(tx0, 2.67, 3.5, o["note"], size=10.5)
    # right column: key plan + notes
    key_plan(sh, 12.55, 6.6, 85.0, item)
    sh.text(12.3, 5.65, "WHAT'S FIXED / WHAT'S ASSUMED", size=13, bold=True)
    lines = [f"L2 floor {ftin(hz['l2_ff']['value'])}: decided (D-061).",
             f"Ring roof {ftin(hz['ring_roof']['value'])}, high roof {ftin(hz['high_roof']['value'])}: ASSUMED.",
             f"Annex {ftin(hz['annex']['value'])}: ASSUMED (one storey, D-067)."]
    if item == "bay":
        lines += ["Bay 30' x 30' (D-081); height ASSUMED, no MEP input yet.",
                  "Heights in the choices are examples, ASSUMED."]
    else:
        lines += ["Drum 30 ft across (D-082); height ASSUMED.", S["roof_access"]["text"]]
    y = 5.35
    for t_ in lines:
        y = sh.para(12.3, y, 4.15, t_, size=10.5, bullet="•", indent=0.16) - 0.04
    return sh


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sheet", choices=list(NAMES), required=True)
    ap.add_argument("--out-dir")
    a = ap.parse_args()
    out = Path(a.out_dir) if a.out_dir else BP / "studies"
    out.mkdir(parents=True, exist_ok=True)
    sh = build(a.sheet)
    pdf = out / f"{NAMES[a.sheet]}.pdf"
    sh.render_pdf(pdf, title=f"P2-{a.sheet} height study")
    print(f"wrote {pdf}")


if __name__ == "__main__":
    main()
