"""KEYSTONE P2-C-101 SITE PLAN — CAMPUS DIAGRAM (Phase 2, P2-T-006). Schematic, SITE TBD (D-006).

Rev A (2026-10-04, Shane 7:44 AM CT): building outline with the D-053 east shift (+6 ft; frozen Rev D outline dashed),
exit stairs grown inward to 76 in clear (D-052 DECIDED 7:49 AM CT; mid landing = width, D-051), freestanding portal + 28 x 30 ft
Champion Walk (D-043, D-046, D-050), south bus drop loop offset east (D-034; west equally possible), service drive to the
north door S1 (D-034), assumed road south, enlarged entry inset, footprint check vs the 55,000 SF cap (D-031).
Every site element is a diagram (locations ASSUMED, sizes TBD unless sourced). Data: params/phase2_site.yaml.
Rev A FROZEN 9:47 AM CT.
Rev B (Shane 9:47 AM CT): coordinated with P2-A-101/102 Rev E — outline 210 x 252 + NE stair tower 21.33 x 6.67 ft, stairs
and doors read from phase2_plan_rev_e.yaml, superseded Rev D outline dashed; the cap table is replaced by the D-057 size
table (L1 / L2 / TOTAL GSF, change vs Rev D, program G-003 Rev G; no cap, no margin — D-056). Data: site yaml rev_b.
Rev C (Shane 10:27 AM CT, D-061 Option B): P2-A-101 Rev F — NE stair tower 24.08 x 6.67 ft (ST-2 2.75 ft longer, 31 risers),
stairs 12.67 x 24.08, D-057 table vs Rev E with program G-003 Rev I (p2_testfit.summary_h). Data: site yaml rev_c. Rev B FROZEN.
Rev D (Shane 1:21 / 1:22 PM CT, P2-T-012): P2-A-101 Rev H — D-066 40 ft walk (28 ft brick + 6 ft bands, around both portal piers),
D-067 storage annex on the north wall with S1 + apron moved north, D-057 table vs Rev G with program G-003 Rev J
(p2_testfit.summary_j). Data: site yaml rev_d. Rev C FROZEN.
Usage (from the repo root):
  /workspace/.venv-keystone/bin/python blueprints/phase2/src/p2_c_101.py [--rev A|B|C|D] [--png PATH] [--out-dir DIR] [--force]
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import yaml

BP = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BP / "shared"))
from titleblock import Sheet, add_titleblock, text_width_in  # noqa: E402

W, H, M = 17.0, 11.0, 0.5
SHEET_NO = "P2-C-101"
L_SITE, L_BLDG, L_HID, L_TAG, L_STR, L_DIM = "C-SITE", "A-WALL", "A-AREA-OPEN", "A-ANNO-TEXT", "A-FLOR-STRS", "A-ANNO-DIMS"
C = dict(road="#C9C9C9", bldg="#EFE9DE", floor="#E6D3A8", stair="#8C8C8C", brick="#B5654A", stone="#D8CFC0",
         drive="#DADADA", bus="#CFCFCF", red="#CC0000", band="#D9B79A")
REV = "A"          # set by main(); Rev B branches only (Rev A output stays byte-identical)


def load():
    rd = lambda n: yaml.safe_load((BP / "params" / n).read_text(encoding="utf-8"))
    p2, si, plan = rd("phase2.yaml"), rd("phase2_site.yaml"), rd("phase2_plan_rev_d.yaml")
    if REV in ("B", "C", "D"):                         # Rev B: P2-A-101/102 Rev E; Rev C: Rev F (D-061); Rev D: Rev H
        rb = si[{"B": "rev_b", "C": "rev_c", "D": "rev_d"}[REV]]
        plan = rd(rb["plan_file"])
        si["meta"]["revision"] = rb["revision"]
        bb = rb["building"]
        si["building"].update(rect=bb["rect"], tower=bb["tower"], frozen_rect=bb["prior_rect"], frozen_tower=bb["prior_tower"],
                              east_shift_ft=0)
        if REV == "D":
            si["building"]["annex"] = bb["annex"]
            si["service"].update(apron=rb["service"]["apron"], drive_turn_y=rb["service"]["drive_turn_y"])
            si["walk_d"] = rb["walk"]
    return p2, si, plan


def bands(wk):
    """D-066 walk bands: west polygon from params + its mirror about x = mirror_x."""
    w = [tuple(q) for q in wk["band_w"]]
    e = [(wk["mirror_x"] - x, y) for x, y in w]
    return w, e


def grown_stairs(st, shift):
    """Grown stair rects (inward from each stair's exterior corner); ST-2 / ST-3 move east with the wall."""
    w, l = st[st["drawn"] + "_ft"]
    out = []
    for it in st["items"]:
        x0, y0, x1, y1 = it["rect_frozen"]
        if it["id"] in ("ST-2", "ST-3"):
            x0, x1 = x0 + shift, x1 + shift
        a, b = (l, w) if it.get("turned") else (w, l)          # E-W, N-S size
        if it["anchor"] == "NE":
            r = [x1 - a, y1 - b, x1, y1]
        elif it["anchor"] == "SE":
            r = [x1 - a, y0, x1, y0 + b]
        else:
            r = [x0, y0, x0 + a, y0 + b]
        out.append((it["id"], r, [x0, y0, x1, y1]))
    return out


def ellipse(cx, cy, rx, ry, n=48):
    return [(cx + rx * math.cos(2 * math.pi * k / n), cy + ry * math.sin(2 * math.pi * k / n)) for k in range(n)]


class View:
    def __init__(self, sh, x0, y0, fpi):
        self.sh, self.x0, self.y0, self.s = sh, x0, y0, 1.0 / fpi

    def P(self, x, y):
        return self.x0 + x * self.s, self.y0 + y * self.s

    def poly(self, pts, fill=None, layer=L_SITE, lw=0.5):
        self.sh.poly([self.P(*p) for p in pts], fill=fill, layer=layer, lw=lw)

    def rect(self, r, fill=None, layer=L_SITE, lw=0.5):
        self.poly([(r[0], r[1]), (r[2], r[1]), (r[2], r[3]), (r[0], r[3])], fill, layer, lw)

    def dline(self, x0, y0, x1, y1, layer=L_HID, lw=0.45, dash=0.06, gap=0.04):
        a, b = self.P(x0, y0), self.P(x1, y1)
        self.sh.dashed(a[0], a[1], b[0], b[1], layer=layer, lw=lw, dash=dash, gap=gap)

    def drect(self, r, layer=L_HID, lw=0.45, dash=0.06, gap=0.04):
        for (a, b, c, d) in ((r[0], r[1], r[2], r[1]), (r[2], r[1], r[2], r[3]), (r[2], r[3], r[0], r[3]), (r[0], r[3], r[0], r[1])):
            self.dline(a, b, c, d, layer, lw, dash, gap)

    def line(self, x0, y0, x1, y1, layer=L_SITE, lw=0.6):
        a, b = self.P(x0, y0), self.P(x1, y1)
        self.sh.line(a[0], a[1], b[0], b[1], layer=layer, lw=lw)

    def text(self, x, y, s, size=5.5, **kw):
        a = self.P(x, y)
        self.sh.text(a[0], a[1], s, size=size, layer=kw.pop("layer", L_TAG), **kw)


def door_xy(wall, at, b):
    x0, y0, x1, y1 = b
    return {"S": (at, y0), "N": (at, y1), "W": (x0, at), "E": (x1, at)}[wall]


def draw_site(v, si, plan, full=True):
    b, sh_ = si["building"], si["building"]["east_shift_ft"]
    pt, cw, bus, sv, rd = si["portal"], si["champion_walk"], si["bus_drop"], si["service"], si["road"]
    if full:
        # road (assumed south)
        v.rect([-75, rd["y"] - 12, 265, rd["y"] + 12], C["road"], lw=0.3)
        v.dline(-75, rd["y"], 265, rd["y"], L_SITE, 0.4, 0.1, 0.08)
        # service drive (west side) to S1 + apron
        ap = sv["apron"]
        ty = sv.get("drive_turn_y", 292)
        v.poly([(-52, rd["y"] + 12), (-32, rd["y"] + 12), (-32, ty), (ap[0], ty), (ap[0], ap[3]), (-52, ap[3])], C["drive"], lw=0.3)
        v.rect(ap, C["drive"], lw=0.3)
        # bus loop (diagram): ring + two stubs to the road
        cx, cy = bus["loop_center"]
        rx, ry = bus["loop_rx"], bus["loop_ry"]
        for sx in (cx - rx + 4, cx + rx - 16):
            v.rect([sx, rd["y"] + 12, sx + 12, cy - ry + 6], C["bus"], lw=0.3)
        v.poly(ellipse(cx, cy, rx, ry), C["bus"], lw=0.4)
        v.poly(ellipse(cx, cy, rx - 12, ry - 12), "#FFFFFF", lw=0.4)
        c0, c1 = bus["curb_at"]
        v.line(c0, cy + ry + 1.5, c1, cy + ry + 1.5, L_SITE, 1.4)
        v.dline(c0, cy + ry + 2, pt["center_x"] + pt["width"] / 2, -pt["gap_to_building"] - pt["depth"] / 2, L_SITE, 0.6, 0.05, 0.035)
        # walk extension toward parking (later)
        v.drect([cw["rect"][0], rd["y"] + 14, cw["rect"][2], -pt["gap_to_building"] - pt["depth"]], L_HID, 0.4)
    # building: frozen outline dashed, new outline solid (east shift)
    v.rect(b["rect"], C["bldg"], L_BLDG, 0.9)
    v.rect(b["tower"], C["bldg"], L_BLDG, 0.9)
    ef = plan["event_floor"]["rect"]
    v.rect([ef[0], ef[1], ef[2] + sh_, ef[3]], C["floor"], L_SITE, 0.3)
    if REV == "D":
        v.rect(b["annex"], C["bldg"], L_BLDG, 0.9)
    else:
        v.drect(b["frozen_rect"], L_HID, 0.5)
        v.drect(b["frozen_tower"], L_HID, 0.5)
    # stairs
    if REV in ("B", "C", "D"):
        for it in plan["vertical"]["stairs"]:
            v.rect(it["rect"], C["stair"], L_STR, 0.4)
    else:
        for sid, r, fr in grown_stairs(si["stairs"], sh_):
            v.rect(r, C["stair"], L_STR, 0.4)
            v.drect(fr, L_HID, 0.35, 0.04, 0.03)
    # Champion Walk + portal
    if REV == "D":
        for bp in bands(si["walk_d"]):
            v.poly(bp, C["band"], L_SITE, 0.35)
    v.rect(cw["rect"], C["brick"], L_SITE, 0.4)
    g, d, wd, cx = pt["gap_to_building"], pt["depth"], pt["width"], pt["center_x"]
    op = cw["width"]
    v.rect([cx - op / 2, -g - d, cx + op / 2, -g], C["brick"], L_SITE, 0.3)
    v.rect([cx - wd / 2, -g - d, cx - op / 2, -g], C["stone"], L_SITE, 0.6)
    v.rect([cx + op / 2, -g - d, cx + wd / 2, -g], C["stone"], L_SITE, 0.6)
    v.dline(cx - op / 2, -g - d / 2, cx + op / 2, -g - d / 2, L_HID, 0.4, 0.04, 0.03)
    # doors
    nb = b["rect"]
    pdoors = {d["id"]: d for d in plan["level_1"]["doors"]["items"]}
    for did, kind in (("E1", "main"), ("S1", "service")):
        dd = pdoors[did] if REV in ("B", "C", "D") else si["doors"][did]
        x, y = door_xy(dd["wall"], dd["at"], nb)
        if REV == "D" and "y" in dd:
            y = dd["y"]
        tri = [(x - 4, y), (x + 4, y), (x, y - 6)] if dd["wall"] == "S" else [(x - 4, y), (x + 4, y), (x, y + 6)]
        v.poly(tri, C["red"], L_SITE, 0)
    ex = ({d["id"]: [d["wall"], d["at"]] for d in plan["level_1"]["doors"]["items"] if d["kind"] == "exit"} if REV in ("B", "C", "D")
          else si["doors"]["exits_frozen"])
    for k, val in ex.items():
        if k == "source":
            continue
        wall, at = val
        if wall == "S" and at > 150:
            at += sh_
        x, y = door_xy(wall, at, nb)
        dx, dy = {"S": (0, -3), "N": (0, 3), "W": (-3, 0), "E": (3, 0)}[wall]
        v.line(x, y, x + dx, y + dy, L_SITE, 1.0)
        if full:
            off = {"S": (0, -9), "N": (0, 5), "W": (-4, -1.5), "E": (4, -1.5)}[wall]
            v.text(x + off[0], y + off[1], k, 4.0, align={"W": "right", "E": "left"}.get(wall, "center"))


def draw_inset(iv, si, ins):
    pt, cw = si["portal"], si["champion_walk"]
    x0, y0, x1, y1 = ins
    iv.rect([x0, 0, x1, y1], C["bldg"], L_BLDG, 0)
    iv.line(x0, 0, x1, 0, L_BLDG, 1.2)
    g, d, wd, cx, op = pt["gap_to_building"], pt["depth"], pt["width"], pt["center_x"], cw["width"]
    if REV == "D":
        for bp in bands(si["walk_d"]):
            iv.poly(bp, C["band"], L_SITE, 0.4)
    iv.rect(cw["rect"], C["brick"], L_SITE, 0.4)
    iv.rect([cx - op / 2, -g - d, cx + op / 2, -g], C["brick"], L_SITE, 0.3)
    iv.rect([cx - wd / 2, -g - d, cx - op / 2, -g], C["stone"], L_SITE, 0.7)
    iv.rect([cx + op / 2, -g - d, cx + wd / 2, -g], C["stone"], L_SITE, 0.7)
    iv.dline(cx - op / 2, -g - d / 2, cx + op / 2, -g - d / 2, L_HID, 0.4, 0.04, 0.03)
    iv.dline(cw["rect"][0], -g - d, cw["rect"][0], y0, L_HID, 0.4)
    iv.dline(cw["rect"][2], -g - d, cw["rect"][2], y0, L_HID, 0.4)
    iv.poly([(cx - 3, 0), (cx + 3, 0), (cx, -4)], C["red"], L_SITE, 0)
    # dimensions: walk width (south of the portal) and length (east side)
    a, b = iv.P(cw["rect"][0], -g - d - 4), iv.P(cw["rect"][2], -g - d - 4)
    iv.sh.line(a[0], a[1], b[0], b[1], layer=L_DIM, lw=0.4)
    for q in (a, b):
        iv.sh.line(q[0], q[1] - 0.03, q[0], q[1] + 0.03, layer=L_DIM, lw=0.4)
    iv.sh.text((a[0] + b[0]) / 2, a[1] - 0.12, f"{cw['width']:g}'", size=5, align="center", layer=L_DIM)
    if REV == "D":
        wk = si["walk_d"]
        xs = [93, 99, 127, 133]
        a, b = iv.P(xs[0], -3), iv.P(xs[-1], -3)
        iv.sh.line(a[0], a[1], b[0], b[1], layer=L_DIM, lw=0.4)
        for xx in xs:
            q = iv.P(xx, -3)
            iv.sh.line(q[0], q[1] - 0.03, q[0], q[1] + 0.03, layer=L_DIM, lw=0.4)
        for (x0_, x1_), lab in zip(zip(xs[:-1], xs[1:]), ("6'", "28'", "6'")):
            q = iv.P((x0_ + x1_) / 2, -3)
            iv.sh.text(q[0], q[1] - 0.1, lab, size=4.4, align="center", layer=L_DIM)
        for x0_, x1_ in ((85, 91), (135, 141)):
            q = iv.P((x0_ + x1_) / 2, -33)
            iv.sh.text(q[0], q[1] - 0.02, "6'", size=4.4, align="center", layer=L_DIM)
        q = iv.P(x0, -52)
        iv.sh.text(q[0], q[1], f"{wk['width_at_doors_ft']}' at the doors = 6 + 28 + 6 = {wk['width_at_doors_ft'] * 12} in ≥ {wk['need_in']} in (E1, standing margin)",
                   size=4.6, bold=True, layer=L_DIM)
        q = iv.P(x0, -56.5)
        iv.sh.text(q[0], q[1], "bands pass outside both 8' piers: 6 + 28 + 6 = 40' at the portal (D-066)", size=4.4, layer=L_DIM)
    a, b = iv.P(x1 - (1 if REV == "D" else 4), -g), iv.P(x1 - (1 if REV == "D" else 4), 0)
    iv.sh.line(a[0], a[1], b[0], b[1], layer=L_DIM, lw=0.4)
    for q in (a, b):
        iv.sh.line(q[0] - 0.03, q[1], q[0] + 0.03, q[1], layer=L_DIM, lw=0.4)
    iv.sh.text(a[0] - 0.05, (a[1] + b[1]) / 2, f"{g:g}'", size=5, align="right", layer=L_DIM)
    iv.text(x0 + 2, 4, "BUILDING (south wall)", 4.4)


def legend(sh, x, y):
    if REV == "D":
        items = [(C["bldg"], "Building, P2-A-101 Rev H (210' + NE tower + annex)"),
                 (C["stair"], "Exit stairs 76\" clear (D-052)"), (C["floor"], "Event floor"),
                 (C["brick"], "Champion Walk (brick, 28')"), (C["band"], "Walk bands 6' each side (D-066)"),
                 (C["stone"], "Portal piers (limestone)"),
                 (C["drive"], "Service drive / apron (diagram)"), (C["bus"], "Bus drop loop (diagram)"),
                 (C["road"], "Road (assumed)"), (C["red"], "E1 main entry / S1 service door")]
        sh.text(x, y, "LEGEND", size=6.4, bold=True)
        for i, (f, lab) in enumerate(items):
            yy = y - 0.2 - i * 0.17
            sh.poly([(x, yy), (x + 0.25, yy), (x + 0.25, yy + 0.11), (x, yy + 0.11)], fill=f, layer=L_SITE, lw=0.3)
            sh.text(x + 0.32, yy + 0.015, lab, size=5.4)
        return y - 0.2 - len(items) * 0.17
    items = [(C["bldg"], "Building, P2-A-101 Rev F (210' + NE tower)" if REV == "C" else
              "Building, P2-A-101 Rev E (210' + NE tower)" if REV == "B" else "Building, next revision (D-053 east shift)"),
             (None, "Superseded Rev E tower (dashed)" if REV == "C" else
              "Superseded Rev D outline (dashed)" if REV == "B" else "Frozen Rev D outline (dashed)"),
             (C["stair"], "Exit stairs 76\" clear (D-052)"), (C["floor"], "Event floor"),
             (C["brick"], "Champion Walk (brick)"), (C["stone"], "Portal piers (limestone)"),
             (C["drive"], "Service drive / apron (diagram)"), (C["bus"], "Bus drop loop (diagram)"),
             (C["road"], "Road (assumed)"), (C["red"], "E1 main entry / S1 service door")]
    sh.text(x, y, "LEGEND", size=6.4, bold=True)
    for i, (f, lab) in enumerate(items):
        yy = y - 0.2 - i * 0.17
        if f is None:
            sh.dashed(x, yy + 0.05, x + 0.25, yy + 0.05, layer=L_HID, lw=0.5, dash=0.05, gap=0.03)
        else:
            sh.poly([(x, yy), (x + 0.25, yy), (x + 0.25, yy + 0.11), (x, yy + 0.11)], fill=f, layer=L_SITE, lw=0.3)
        sh.text(x + 0.32, yy + 0.015, lab, size=5.4)
    return y - 0.2 - len(items) * 0.17


def build(p2, si, plan):
    meta2, sm = p2["meta"], si["meta"]
    sh = Sheet(W, H)
    body_bottom = add_titleblock(sh, {
        "project": f"{meta2['project']}\n{meta2['arena_name']} · {meta2['location']}",
        "phase": "PHASE 2",
        "title": "SITE PLAN — CAMPUS DIAGRAM\nSITE TBD · SCHEMATIC",
        "scale": "AS NOTED",
        "date": meta2["sheet_date"],
        "revision": sm["revision"],
        "drawn_by": meta2["drawn_by"],
        "sheet_no": SHEET_NO,
        "stamp": meta2["stamp"],
    }, margin=M, tb_h=0.95, stamp_h=0.40)
    fpi = si["scale"]["ft_per_in"]
    v = View(sh, 2.15, 5.05, fpi)
    draw_site(v, si, plan, full=True)
    b, pt, bus, rd = si["building"], si["portal"], si["bus_drop"], si["road"]
    fc = si["footprint_check"]
    # labels
    v.text(105, 150, "TROJAN HORSE ARENA", 7.0, align="center", bold=True)
    v.text(105, 138, "(Phase 2 building, 2 levels)", 5.2, align="center")
    v.text(116, 105, "EVENT FLOOR", 5.0, align="center", bold=True)
    if REV == "D":
        tw = b["tower"]
        an = b["annex"]
        v.text(116, 96, "east clear 16' (D-053, drawn)", 4.6, align="center")
        v.text(105, 26, f"{b['rect'][2]:g}' x {b['rect'][3]:g}' + NE stair tower + storage annex (P2-A-101 Rev H)", 4.8, align="center")
        v.text(105, 16, "unchanged walls; the annex is the only footprint change", 4.4, align="center")
        v.text(tw[2] + 4, tw[3] + 2, f"NE TOWER {tw[2] - tw[0]:.2f}' x {tw[3] - tw[1]:.2f}'", 4.2, bold=True)
        v.text((an[0] + an[2]) / 2, (an[1] + an[3]) / 2 + 2, "STORAGE ANNEX (D-067)", 4.4, align="center", bold=True)
        v.text((an[0] + an[2]) / 2, (an[1] + an[3]) / 2 - 7, f"{an[2] - an[0]:g}' x {an[3] - an[1]:g}' = {(an[2] - an[0]) * (an[3] - an[1]):,.0f} SF, 1 storey", 4.0, align="center")
    elif REV == "C":
        tw = b["tower"]
        v.text(116, 96, "east clear 16' (D-053, drawn)", 4.6, align="center")
        v.text(105, 26, f"{b['rect'][2]:g}' x {b['rect'][3]:g}' + NE stair tower (P2-A-101 Rev F)", 4.8, align="center")
        v.text(105, 16, "dashed = superseded Rev E tower 21.33' x 6.67'", 4.4, align="center")
        v.text(tw[2] + 4, tw[3] + 2, f"NE TOWER {tw[2] - tw[0]:.2f}' x {tw[3] - tw[1]:.2f}'", 4.2, bold=True)
    elif REV == "B":
        tw = b["tower"]
        v.text(116, 96, "east clear 16' (D-053, drawn)", 4.6, align="center")
        v.text(105, 26, f"{b['rect'][2]:g}' x {b['rect'][3]:g}' + NE stair tower (P2-A-101 Rev E)", 4.8, align="center")
        v.text(105, 16, "dashed = superseded Rev D outline 204' x 252' + 19' x 5' tower", 4.4, align="center")
        v.text(tw[2] + 4, tw[3] + 2, f"NE TOWER {tw[2] - tw[0]:.2f}' x {tw[3] - tw[1]:.2f}'", 4.2, bold=True)
    else:
        v.text(116, 96, "east clear 10' → 16' (D-053)", 4.6, align="center")
        v.text(105, 26, f"{b['rect'][2]:g}' x {b['rect'][3]:g}' + NE stair tower (next A-101/A-102)", 4.8, align="center")
        v.text(105, 16, "dashed = frozen Rev D outline 204' x 252'", 4.4, align="center")
    v.text(214, 244, "ST-2", 4.4)
    v.text(214, 4, "ST-3", 4.4)
    v.text(-4, 4, "ST-4", 4.4, align="right")
    v.text(30, 236, "ST-1", 4.4, align="right")
    v.text(pt["center_x"] - 26, -36, "PORTAL", 5.0, align="right", bold=True)
    v.text(pt["center_x"] - 26, -46, "(freestanding, 50' max)", 4.4, align="right")
    if REV == "D":
        v.text(pt["center_x"] + 31, -18, "CHAMPION WALK 28' + 6' BANDS = 40'", 4.6, bold=True)
        v.text(pt["center_x"] + 31, -27, "brick 28' x 30' (D-046); bands around the piers (D-066)", 4.2)
    else:
        v.text(pt["center_x"] + 17, -18, "CHAMPION WALK 28' x 30'", 4.6, bold=True)
        v.text(pt["center_x"] + 17, -27, "brick, donor bricks (D-046)", 4.2)
    v.text(pt["center_x"] - 15, -95, "extend to", 4.2, align="right")
    v.text(pt["center_x"] - 15, -104, "parking later", 4.2, align="right")
    cx, cy = bus["loop_center"]
    v.text(cx, cy + 3, "BUS DROP", 4.8, align="center", bold=True)
    v.text(cx, cy - 6, "LOOP", 4.8, align="center", bold=True)
    v.text(cx + bus["loop_rx"] + 4, cy + 14, "offset E (or W) of the", 4.3)
    v.text(cx + bus["loop_rx"] + 4, cy + 5, "portal view (D-034);", 4.3)
    v.text(cx + bus["loop_rx"] + 4, cy - 4, "diagram — size TBD", 4.3)
    v.text(bus["curb_at"][1] + 2, cy + bus["loop_ry"] + 4, "drop curb", 4.2)
    v.text(-42, 120, "SERVICE DRIVE (diagram)", 4.6, rot=90, align="center", bold=True)
    ap = si["service"]["apron"]
    if REV == "D":
        v.text(ap[2] + 42, ap[1] + 10, "S1 SERVICE / LOADING (D-034), on the annex", 4.6, bold=True)
    else:
        v.text((ap[0] + ap[2]) / 2, ap[3] + 4, "S1 SERVICE / LOADING (D-034)", 4.6, align="center", bold=True)
    v.text(95, rd["y"] - 4, rd["label"], 5.0, align="center", bold=True)
    v.text(-70, 318, "PARCEL / PROPERTY LINES, SETBACKS, PARKING, UTILITIES, STORMWATER: TBD (D-006)", 5.0, bold=True, color=C["red"])
    # north arrow + scale bar
    nx, ny = v.P(250, 300)
    sh.line(nx, ny - 0.22, nx, ny + 0.16, lw=0.9)
    sh.poly([(nx - 0.05, ny + 0.08), (nx, ny + 0.2), (nx + 0.05, ny + 0.08)], fill="#000000", lw=0)
    sh.text(nx, ny + 0.25, "N", size=7, bold=True, align="center")
    sx, sy = v.P(150, rd["y"] - 22)
    for k in range(3):
        sh.poly([(sx + k * 1.0, sy), (sx + (k + 1) * 1.0, sy), (sx + (k + 1) * 1.0, sy + 0.06), (sx + k * 1.0, sy + 0.06)],
                fill="#000000" if k % 2 == 0 else "#FFFFFF", lw=0.4, layer=L_DIM)
        sh.text(sx + k * 1.0, sy - 0.12, f"{int(k * fpi)}'", size=5, align="center", layer=L_DIM)
    sh.text(sx + 3.0, sy - 0.12, f"{int(3 * fpi)}'", size=5, align="center", layer=L_DIM)
    t1 = "1  SITE PLAN — CAMPUS DIAGRAM (SITE TBD)"
    tx, ty = 0.75, 2.12
    sh.text(tx, ty, t1, size=7.5, bold=True)
    sh.line(tx, ty - 0.05, tx + text_width_in(t1, 7.5, True), ty - 0.05, lw=0.7)
    sh.text(tx, ty - 0.18, "1\" = 60'-0\" · north approximate · road assumed south · diagram only (no surveyed dimensions)", size=5.4)
    # extents guard
    for (x_, y_) in (v.P(-75, rd["y"] - 12), v.P(265, 322), v.P(250, 318)):
        if not (M < x_ < 10.0 and body_bottom < y_ < H - M):
            raise SystemExit(f"LAYOUT OVERFLOW: site plan point at {x_:.2f}, {y_:.2f}")
    # inset: enlarged entry 1" = 30' (entry elements only)
    iv = View(sh, 7.2 - 80 / 30.0, 9.62, 30.0)
    ins = (80, -48, 146, 10)
    draw_inset(iv, si, ins)
    a0, a1 = iv.P(ins[0], ins[1]), iv.P(ins[2], ins[3])
    sh.text(a0[0], a1[1] + 0.12, "2  ENTRY — PORTAL + CHAMPION WALK — 1\" = 30'", size=6.5, bold=True)
    # legend
    legend(sh, 7.05, 7.55)
    return sh, body_bottom, v, iv, ins


def notes_b(sh, p2, si, body_bottom, x, y, width):
    """Rev B: D-057 size table (no cap, no margin) + notes coordinated with P2-A-101/102 Rev E."""
    import p2_testfit as tf
    at = si["rev_b"]["area_table"]
    _, _, _, g = tf.summary_g()
    dr, dd = g["drawn"], at["rev_d_drawn"]
    X_ = g["loop"]
    pg = dict(L1=X_["F"], L2=X_["L2"], G=X_["F"] + X_["L2"])

    def n(v):
        return f"{v:,.1f}"

    def sgn(v):
        return ("+" if v > 0.05 else "−" if v < -0.05 else "±") + n(abs(v))
    sh.text(x, y, "SIZE — D-057 (no cap, no margin; D-056)", size=6.8, bold=True)
    cols = [("", 0, "l"), ("DRAWN Rev E", 2.30, "r"), ("REV D drawn", 3.20, "r"), ("CHANGE", 4.05, "r"), ("PROGRAM G", 5.05, "r"),
            ("DRAWN − PROG.", width, "r")]
    y -= 0.16
    for lab, dx, al in cols:
        sh.text(x + dx, y, lab, size=5.4, bold=True, align="left" if al == "l" else "right")
    y -= 0.04
    sh.line(x, y, x + width, y, lw=0.5)
    for lab, k in (("L1 FOOTPRINT", "L1"), ("L2 AREA", "L2"), ("TOTAL GSF", "G")):
        y -= 0.15
        vals = [lab, n(dr[k]), n(dd[k]), sgn(dr[k] - dd[k]), n(pg[k]), sgn(dr[k] - pg[k])]
        for (l_, dx, al), c in zip(cols, vals):
            sh.text(x + dx, y, c, size=5.4, bold=k == "G" or l_ in ("", "DRAWN Rev E"), align="left" if al == "l" else "right")
    sh.line(x, y - 0.05, x + width, y - 0.05, lw=0.5)
    y -= 0.08
    y = sh.para(x, y, width, f"Drawn = P2-A-101/102 Rev E (L2 = L1 minus open-to-below). Program = P2-G-003 Rev G: footprint (max of L1 gross, "
                f"arena volume + L2) + L2 gross; L1 + L2 gross = {n(X_['G'])}. C-101 Rev A showed L1 {n(at['c101_rev_a_l1'])} with a 5' tower; "
                f"Rev E draws the tower 6.67' deep: {sgn(dr['L1'] - at['c101_rev_a_l1'])} SF. Size is set by budget and parcel (D-012, D-006).",
                size=5.6)
    tw = si["building"]["tower"]
    items = [
        ("STATUS", None),
        ("SITE TBD (D-006): this is a layout diagram, not a site plan for permit. Parcel, property lines, setbacks, grading, parking count, utilities and stormwater are TBD. AHJ (R-006): Madison County Inspection Department if the parcel is unincorporated (Hazel Green is); the county states no zoning limits on construction; county codes 2018 IBC / IFC / NFPA 101; State Fire Marshal 2021 IFC.", "•"),
        ("ENTRY (DECIDED)", None),
        ("Freestanding limestone portal over the walk (D-043), 50' max (D-050), 44' wide x 6' deep (ASSUMED), 30' south of the E1 doors (D-046). Champion Walk 28' x 30' = 840 SF brick, ≈ 3,700 4x8 donor bricks; vendor cost ≈ $70.9k if all 4x8 (Shane's sheet, D-044 input; install + base not included). Dashed: later extension to parking.", "•"),
        ("BUS + SERVICE (D-034 DECIDED defaults)", None),
        ("South bus drop loop offset EAST so it does not block the portal view (west is equally allowed; the SW FLEX / team assembly room would favor west). Drop curb links to the walk's south end. Service / deliveries at the north door S1 by a west-side drive (alignment TBD). Loop, drive and apron are diagrams: lane widths, bus turning template and apron size TBD (civil).", "•"),
        ("BUILDING (AS DRAWN ON P2-A-101 / A-102 REV E)", None),
        (f"210' x 252': east seats 16' from the mats (D-053); exits X6–X9 on the new east wall. NE stair tower {tw[2] - tw[0]:.2f}' x {tw[3] - tw[1]:.2f}' = "
         f"{(tw[2] - tw[0]) * (tw[3] - tw[1]):.1f} SF (the 76\" ST-2 sits north of the loop's north leg; Rev A showed 5'). Stairs ST-1..ST-4 76\" clear, "
         "12.67' x 21.33' (D-052, D-051).", "•"),
        ("Upper tier 19\" risers; 6' low band under its front (D-049). Exit paths under the band: D-061 OPEN (R-022). Option B (raise L2 to 17'-9\") would lengthen each stair ≈ 2.75' (NE tower ≈ 9.4' deep).", "•"),
        ("FIRE ACCESS / WATER (TBD)", None),
        ("Fire apparatus access roads, hydrants and fire flow per IFC Appendices B, C, D (State Fire Marshal, 2021 IFC; D107 recommended) and the county's 2018 IFC. Exit discharge from X1-X10 to a public way (IBC 1028) TBD with the parcel.", "•"),
    ]
    for t_, b_ in items:
        if b_ is None:
            y = sh.para(x, y - 0.04, width, t_, size=6.2, bold=True)
        else:
            y = sh.para(x, y, width, t_, size=5.9, indent=0.1, bullet=b_)
    if y < body_bottom + 0.05:
        raise SystemExit(f"LAYOUT OVERFLOW: notes {body_bottom + 0.05 - y:.2f} in into the stamp band")
    return y, dict(L1=dr["L1"], L2=dr["L2"], G=dr["G"], prog=pg)


def notes_c(sh, p2, si, body_bottom, x, y, width):
    """Rev C: D-057 size table vs Rev E (program G-003 Rev I) + notes coordinated with P2-A-101/102 Rev F (D-061)."""
    import p2_testfit as tf
    _, _, _, h = tf.summary_h()
    dr, dd = h["drawn"], h["drawn_d"]
    X_ = h["loop"]
    pg = dict(L1=X_["F"], L2=X_["L2"], G=X_["F"] + X_["L2"])

    def n(v):
        return f"{v:,.1f}"

    def sgn(v):
        return ("+" if v > 0.05 else "−" if v < -0.05 else "±") + n(abs(v))
    sh.text(x, y, "SIZE — D-057 (no cap, no margin; D-056)", size=6.8, bold=True)
    cols = [("", 0, "l"), ("DRAWN Rev F", 2.30, "r"), ("REV E drawn", 3.20, "r"), ("CHANGE", 4.05, "r"), ("PROGRAM I", 5.05, "r"),
            ("DRAWN − PROG.", width, "r")]
    y -= 0.16
    for lab, dx, al in cols:
        sh.text(x + dx, y, lab, size=5.4, bold=True, align="left" if al == "l" else "right")
    y -= 0.04
    sh.line(x, y, x + width, y, lw=0.5)
    for lab, k in (("L1 FOOTPRINT", "L1"), ("L2 AREA", "L2"), ("TOTAL GSF", "G")):
        y -= 0.15
        vals = [lab, n(dr[k]), n(dd[k]), sgn(dr[k] - dd[k]), n(pg[k]), sgn(dr[k] - pg[k])]
        for (l_, dx, al), c in zip(cols, vals):
            sh.text(x + dx, y, c, size=5.4, bold=k == "G" or l_ in ("", "DRAWN Rev F"), align="left" if al == "l" else "right")
    sh.line(x, y - 0.05, x + width, y - 0.05, lw=0.5)
    y -= 0.08
    tw, tp = si["building"]["tower"], si["building"]["frozen_tower"]
    y = sh.para(x, y, width - 0.45, f"Drawn = P2-A-101/102 Rev F (L2 = L1 minus open-to-below). Program = P2-G-003 Rev I: footprint = the larger of "
                f"L1 gross and arena volume + L2, plus L2 gross (L1 + L2 gross = {n(X_['G'])}). The change is the NE tower growing "
                f"{tp[0] - tw[0]:.2f}' west for the longer ST-2 (L2 17'-9\"). Size is set by budget and parcel (D-012, D-006).",
                size=5.6)
    items = [
        ("STATUS", None),
        ("SITE TBD (D-006): this is a layout diagram, not a site plan for permit. Parcel, property lines, setbacks, grading, parking count, utilities and stormwater are TBD. AHJ (R-006): Madison County Inspection Department if the parcel is unincorporated (Hazel Green is); the county states no zoning limits on construction; county codes 2018 IBC / IFC / NFPA 101; State Fire Marshal 2021 IFC.", "•"),
        ("ENTRY (DECIDED)", None),
        ("Freestanding limestone portal over the walk (D-043), 50' max (D-050), 44' wide x 6' deep (ASSUMED), 30' south of the E1 doors (D-046). Champion Walk 28' x 30' = 840 SF brick, ≈ 3,700 4x8 donor bricks; vendor cost ≈ $70.9k if all 4x8 (Shane's sheet, D-044 input; install + base not included). Dashed: later extension to parking.", "•"),
        ("BUS + SERVICE (D-034 DECIDED defaults)", None),
        ("South bus drop loop offset EAST so it does not block the portal view (west is equally allowed; the SW FLEX / team assembly room would favor west). Drop curb links to the walk's south end. Service / deliveries at the north door S1 by a west-side drive (alignment TBD). Loop, drive and apron are diagrams: lane widths, bus turning template and apron size TBD (civil).", "•"),
        ("BUILDING (AS DRAWN ON P2-A-101 / A-102 REV F)", None),
        (f"210' x 252' (unchanged): east seats 16' from the mats (D-053); exits X6–X9 on the east wall. NE stair tower {tw[2] - tw[0]:.2f}' x {tw[3] - tw[1]:.2f}' = "
         f"{(tw[2] - tw[0]) * (tw[3] - tw[1]):.1f} SF (Rev E {tp[2] - tp[0]:.2f}' x {tp[3] - tp[1]:.2f}', dashed). Stairs ST-1..ST-4 76\" clear, "
         "12.67' x 24.08', 31 risers (D-052, D-051).", "•"),
        ("L2 at 17'-9\" with 21\" upper risers (D-061 DECIDED, Option B): upper-tier front row 7'-6\" clear over the exit paths below; no seats lost. Event lockers 3,600 SF behind the tier (D-060).", "•"),
        ("FIRE ACCESS / WATER (TBD)", None),
        ("Fire apparatus access roads, hydrants and fire flow per IFC Appendices B, C, D (State Fire Marshal, 2021 IFC; D107 recommended) and the county's 2018 IFC. Exit discharge from X1-X10 to a public way (IBC 1028) TBD with the parcel.", "•"),
    ]
    for t_, b_ in items:
        if b_ is None:
            y = sh.para(x, y - 0.04, width, t_, size=6.2, bold=True)
        else:
            y = sh.para(x, y, width, t_, size=5.9, indent=0.1, bullet=b_)
    if y < body_bottom + 0.05:
        raise SystemExit(f"LAYOUT OVERFLOW: notes {body_bottom + 0.05 - y:.2f} in into the stamp band")
    return y, dict(L1=dr["L1"], L2=dr["L2"], G=dr["G"], prev=dd, prog=pg)


def notes_d(sh, p2, si, body_bottom, x, y, width):
    """Rev D: D-057 size table vs Rev G (program G-003 Rev J) + notes coordinated with P2-A-101 Rev H (D-066, D-067)."""
    import p2_testfit as tf
    _, _, _, j = tf.summary_j()
    dr, dd = j["drawn"], j["drawn_d"]
    X_ = j["loop"]
    pg = dict(L1=X_["F"], L2=X_["L2"], G=X_["F"] + X_["L2"])
    wk = si["walk_d"]
    an = si["building"]["annex"]

    def n(v):
        return f"{v:,.1f}"

    def sgn(v):
        return ("+" if v > 0.05 else "−" if v < -0.05 else "±") + n(abs(v))
    sh.text(x, y, "SIZE — D-057 (no cap, no margin; D-056)", size=6.8, bold=True)
    cols = [("", 0, "l"), ("DRAWN Rev H", 2.30, "r"), ("REV G drawn", 3.20, "r"), ("CHANGE", 4.05, "r"), ("PROGRAM J", 5.05, "r"),
            ("DRAWN − PROG.", width, "r")]
    y -= 0.16
    for lab, dx, al in cols:
        sh.text(x + dx, y, lab, size=5.4, bold=True, align="left" if al == "l" else "right")
    y -= 0.04
    sh.line(x, y, x + width, y, lw=0.5)
    for lab, k in (("L1 FOOTPRINT", "L1"), ("L2 AREA", "L2"), ("TOTAL GSF", "G")):
        y -= 0.15
        vals = [lab, n(dr[k]), n(dd[k]), sgn(dr[k] - dd[k]), n(pg[k]), sgn(dr[k] - pg[k])]
        for (l_, dx, al), c in zip(cols, vals):
            sh.text(x + dx, y, c, size=5.4, bold=k == "G" or l_ in ("", "DRAWN Rev H"), align="left" if al == "l" else "right")
    sh.line(x, y - 0.05, x + width, y - 0.05, lw=0.5)
    y -= 0.08
    asf = (an[2] - an[0]) * (an[3] - an[1])
    if abs((dr["L1"] - dd["L1"]) - asf) > 0.5:
        raise SystemExit("C-101 Rev D: L1 change is not the annex area")
    y = sh.para(x, y, width - 0.45, f"Drawn = P2-A-101/102 Rev H (L2 = L1 minus open-to-below; L2 unchanged). Program = P2-G-003 Rev J: footprint = the larger of "
                f"L1 gross and arena volume + L2, plus L2 gross; Rev J adds the storage room gross. The change is the one-storey storage annex "
                f"{an[2] - an[0]:g}' x {an[3] - an[1]:g}' = {asf:,.0f} SF (D-067). Size is set by budget and parcel (D-012, D-006).", size=5.6)
    items = [
        ("STATUS", None),
        ("SITE TBD (D-006): this is a layout diagram, not a site plan for permit. Parcel, property lines, setbacks, grading, parking count, utilities and stormwater are TBD. AHJ (R-006): Madison County Inspection Department if the parcel is unincorporated (Hazel Green is); the county states no zoning limits on construction; county codes 2018 IBC / IFC / NFPA 101; State Fire Marshal 2021 IFC.", "•"),
        ("ENTRY + EXIT DISCHARGE (D-066 DECIDED, Shane 1:22 PM CT)", None),
        ("Freestanding limestone portal over the walk (D-043), 50' max (D-050), 44' wide x 6' deep with 8' piers and a 28' arch (ASSUMED), 30' south of the E1 doors (D-046). Champion Walk 28' x 30' brick (D-046) + a 6' band each side = "
         f"{wk['width_at_doors_ft']}' at the doors = {wk['width_at_doors_ft'] * 12} in ≥ {wk['need_in']} in (E1 at the standing margin, P2-G-002 Rev B; IBC 2021 1028.3). At the portal the bands pass outside both piers: 6 + 28 + 6 = "
         f"{wk['width_at_portal_ft']}'. Bands paved now, could be brick later (D-044). Band shape between doors and portal ASSUMED. Dashed: later extension to parking.", "•"),
        ("BUS + SERVICE (D-034 DECIDED defaults)", None),
        ("South bus drop loop offset EAST so it does not block the portal view (west is equally allowed). Drop curb links to the walk's south end. Service / deliveries at S1, now on the storage annex's north wall (same x, 30' further north); the west-side drive and apron move north with it. Loop, drive and apron are diagrams: lane widths, turning templates and apron size TBD (civil).", "•"),
        ("BUILDING (AS DRAWN ON P2-A-101 REV H)", None),
        (f"210' x 252' (unchanged) + NE stair tower + storage annex {an[2] - an[0]:g}' x {an[3] - an[1]:g}' on the north wall between X4 and X5, one storey (height ASSUMED, D-067). "
         "Chairs, tables and stage carts roll from the annex to the floor through equipment storage and the athlete corridor (P2-A-103 Rev B).", "•"),
        ("FIRE ACCESS / WATER (TBD)", None),
        ("Fire apparatus access roads, hydrants and fire flow per IFC Appendices B, C, D (State Fire Marshal, 2021 IFC; D107 recommended) and the county's 2018 IFC. Exit discharge from X1-X10 to a public way (IBC 1028) TBD with the parcel.", "•"),
    ]
    for t_, b_ in items:
        if b_ is None:
            y = sh.para(x, y - 0.04, width, t_, size=6.2, bold=True)
        else:
            y = sh.para(x, y, width, t_, size=5.9, indent=0.1, bullet=b_)
    if y < body_bottom + 0.05:
        raise SystemExit(f"LAYOUT OVERFLOW: notes {body_bottom + 0.05 - y:.2f} in into the stamp band")
    return y, dict(L1=dr["L1"], L2=dr["L2"], G=dr["G"], prev=dd, prog=pg)


def notes(sh, p2, si, body_bottom, x, y, width):
    fc = si["footprint_check"]
    cap = fc["cap_sf"]
    e = fc["frozen_drawn_sf"] + fc["east_shift_sf"]
    d76 = e + fc["tower_widen_sf_76"]
    d70 = e + fc["tower_widen_sf_70"]
    bound = e + fc["stair_growth_outward_bound_sf_76"]
    pg = fc["program_basis_f_76_sf"] + fc["east_shift_sf"]
    rows = [
        ("Frozen Rev D drawn footprint (204 x 252 + tower)", fc["frozen_drawn_sf"], cap - fc["frozen_drawn_sf"]),
        ("+ east shift 6' x 252' (D-053 DECIDED)", e, cap - e),
        ("+ NE tower widened for 76\" ST-2 (D-052 DECIDED)", d76, cap - d76),
        ("Bound: all 4 stairs grow outward at 76\"", bound, cap - bound),
        ("Program basis (G-003 Rev F method), 76\" stairs + shift", pg, cap - pg),
    ]
    sh.text(x, y, "FOOTPRINT vs 55,000 SF CAP (D-031)", size=6.8, bold=True)
    y -= 0.16
    sh.text(x + 3.75, y, "footprint SF", size=5.4, bold=True, align="right")
    sh.text(x + width, y, "margin SF", size=5.4, bold=True, align="right")
    y -= 0.04
    sh.line(x, y, x + width, y, lw=0.5)
    for lab, a, m in rows:
        y -= 0.15
        bold = lab.startswith("+ NE") or lab.startswith("Program")
        sh.text(x, y, lab, size=5.4, bold=bold)
        sh.text(x + 3.75, y, f"{a:,.1f}", size=5.4, align="right", bold=bold)
        sh.text(x + width, y, f"{m:,.1f}", size=5.4, align="right", bold=bold, color=C["red"] if m < 1000 else None)
    sh.line(x, y - 0.05, x + width, y - 0.05, lw=0.5)
    y -= 0.08
    items = [
        ("STATUS", None),
        ("SITE TBD (D-006): this is a layout diagram, not a site plan for permit. Parcel, property lines, setbacks, grading, parking count, utilities and stormwater are TBD. AHJ (R-006): Madison County Inspection Department if the parcel is unincorporated (Hazel Green is); the county states no zoning limits on construction; county codes 2018 IBC / IFC / NFPA 101; State Fire Marshal 2021 IFC.", "•"),
        ("ENTRY (DECIDED)", None),
        ("Freestanding limestone portal over the walk (D-043), 50' max (D-050), 44' wide x 6' deep (ASSUMED), 30' south of the E1 doors (D-046). Champion Walk 28' x 30' = 840 SF brick, ≈ 3,700 4x8 donor bricks; vendor cost ≈ $70.9k if all 4x8 (Shane's sheet, D-044 input; install + base not included). Dashed: later extension to parking.", "•"),
        ("BUS + SERVICE (D-034 DECIDED defaults)", None),
        ("South bus drop loop offset EAST so it does not block the portal view (west is equally allowed; the SW FLEX / team assembly room would favor west). Drop curb links to the walk's south end. Service / deliveries at the north door S1 by a west-side drive (alignment TBD). Loop, drive and apron are diagrams: lane widths, bus turning template and apron size TBD (civil).", "•"),
        ("BUILDING CHANGES FOR THE NEXT A-101 / A-102 / A-301 REVISION (frozen sheets stay frozen)", None),
        ("East seats 6' further from the mats (D-053 DECIDED): east wall + exits X6-X9 move 6' east → 210' x 252'. Upper-tier risers 19\" (front row 7.08') — section only.", "•"),
        ("Exit stairs 76\" clear with intermediate handrails (D-052 DECIDED, 7:49 AM CT; worst-case egress 304\" vs 292.4\" required) and a mid landing = width (D-051): 12.67' x 21.33' each, grown inward from their corners; frozen 10.8' x 19' dashed. ST-2's NE tower widens to 21.33' x 5'.", "•"),
        ("Event lockers re-planned to full-height zones (D-049); exits under the tier front need ≥ 7'-6\".", "•"),
        ("FIRE ACCESS / WATER (TBD)", None),
        ("Fire apparatus access roads, hydrants and fire flow per IFC Appendices B, C, D (State Fire Marshal, 2021 IFC; D107 recommended) and the county's 2018 IFC. Exit discharge from X1-X10 to a public way (IBC 1028) TBD with the parcel.", "•"),
    ]
    for t_, b_ in items:
        if b_ is None:
            y = sh.para(x, y - 0.04, width, t_, size=6.2, bold=True)
        else:
            y = sh.para(x, y, width, t_, size=5.9, indent=0.1, bullet=b_)
    if y < body_bottom + 0.05:
        raise SystemExit(f"LAYOUT OVERFLOW: notes {body_bottom + 0.05 - y:.2f} in into the stamp band")
    return y, dict(drawn76=cap - d76, drawn70=cap - d70, bound=cap - bound, program=cap - pg, e=e, d76=d76, pg=pg)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", choices=["A", "B", "C", "D"], default="D")
    ap.add_argument("--png")
    ap.add_argument("--out-dir")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    global REV
    REV = a.rev
    p2, si, plan = load()
    rv = p2["sheets"][SHEET_NO]["revisions"][a.rev]
    if a.out_dir:
        pdf, dxf = (Path(a.out_dir) / f"{rv['file']}.{e}" for e in ("pdf", "dxf"))
    else:
        pdf = BP / "phase2" / "out" / "pdf" / f"{rv['file']}.pdf"
        dxf = BP / "phase2" / "out" / "dxf" / f"{rv['file']}.dxf"
        if rv.get("frozen") and (pdf.exists() or dxf.exists()) and not a.force:
            sys.exit("Revision is FROZEN; use --out-dir to regenerate for checking.")
    sh, body_bottom, v, iv, ins = build(p2, si, plan)
    y, mg = (notes_d if REV == "D" else notes_c if REV == "C" else notes_b if REV == "B" else notes)(sh, p2, si, body_bottom, 10.35, 10.2, 6.05)
    print(f"notes margin {y - body_bottom - 0.05:.2f} in; margins {mg}")
    pdf.parent.mkdir(parents=True, exist_ok=True)
    dxf.parent.mkdir(parents=True, exist_ok=True)
    sh.render_pdf(pdf, title=f"{SHEET_NO} Rev {a.rev} {p2['sheets'][SHEET_NO]['title']}", png_path=a.png)
    sh.render_dxf(dxf)
    print(f"wrote {pdf}\nwrote {dxf}" + (f"\nwrote {a.png}" if a.png else ""))


if __name__ == "__main__":
    main()
