"""KEYSTONE shared sheet kit: one layout model, two outputs (vector PDF + DXF).

A Sheet collects primitives in INCHES (origin bottom-left of the paper):
rectangles, lines and single-line text runs. render_pdf() draws them with
matplotlib (TrueType fonts embedded, so the text stays searchable) and
render_dxf() writes the same geometry with ezdxf, one DXF layer per primitive.

add_titleblock() draws the standard KEYSTONE border, PRELIMINARY stamp band and
title block (prompt §9). All title block values come from the caller, which
reads them from params/phase*.yaml. This module holds layout only, no project data.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath

FONT_REG = "DejaVu Sans"
LINE_FACTOR = 1.32          # line pitch = size_pt * factor
DXF_CAP = 0.72              # DXF text height ≈ cap height = 0.72 em

TTLB = "G-ANNO-TTLB"
TEXT = "A-ANNO-TEXT"
LAYER_COLORS = {TTLB: 7, TEXT: 7}   # 7 = black/white (black when plotted)


def text_width_in(s: str, size_pt: float, bold: bool = False) -> float:
    """Width of a text run in inches, measured from the real font outline."""
    if not s:
        return 0.0
    fp = FontProperties(family=FONT_REG, weight="bold" if bold else "normal")
    ext = TextPath((0, 0), s, size=size_pt, prop=fp).get_extents()
    return ext.x1 / 72.0


def wrap(s: str, width_in: float, size_pt: float, bold: bool = False) -> list[str]:
    """Greedy word wrap using measured widths."""
    out, cur = [], ""
    for word in s.split():
        trial = f"{cur} {word}".strip()
        if cur and text_width_in(trial, size_pt, bold) > width_in:
            out.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        out.append(cur)
    return out or [""]


def pitch(size_pt: float) -> float:
    return size_pt * LINE_FACTOR / 72.0


@dataclass
class Sheet:
    width: float
    height: float
    prims: list = field(default_factory=list)

    # --- primitives -------------------------------------------------------
    def rect(self, x, y, w, h, layer=TEXT, lw=0.8):
        self.prims.append(("rect", dict(x=x, y=y, w=w, h=h, layer=layer, lw=lw)))

    def line(self, x1, y1, x2, y2, layer=TEXT, lw=0.6):
        self.prims.append(("line", dict(x1=x1, y1=y1, x2=x2, y2=y2, layer=layer, lw=lw)))

    def text(self, x, y, s, size=10.5, bold=False, align="left", layer=TEXT):
        """One line of text; (x, y) is the baseline point at `align`."""
        self.prims.append(("text", dict(x=x, y=y, s=s, size=size, bold=bold, align=align, layer=layer)))

    def para(self, x, y_top, width, s, size=10.5, bold=False, layer=TEXT, indent=0.0, bullet=None):
        """Wrapped paragraph starting below y_top. Returns the y below the last line."""
        lines = wrap(s, width - indent, size, bold)
        y = y_top
        for i, ln in enumerate(lines):
            y -= pitch(size)
            if bullet and i == 0:
                self.text(x, y + 0.02 * size / 10, bullet, size=size, bold=bold, layer=layer)
            self.text(x + indent, y + 0.02 * size / 10, ln, size=size, bold=bold, layer=layer)
        return y - 0.25 * pitch(size)

    def placeholder(self, x, y, w, h, label, size=12, layer=TEXT):
        """Empty box with a light X and a centred label (photo placeholder)."""
        self.rect(x, y, w, h, layer=layer, lw=0.8)
        self.line(x, y, x + w, y + h, layer=layer, lw=0.3)
        self.line(x, y + h, x + w, y, layer=layer, lw=0.3)
        tw = text_width_in(label, size, True) + 0.2
        th = pitch(size) + 0.1
        self.prims.append(("knockout", dict(x=x + w / 2 - tw / 2, y=y + h / 2 - th / 2, w=tw, h=th)))
        self.text(x + w / 2, y + h / 2 - size / 72 * 0.35, label, size=size, bold=True, align="center", layer=layer)

    # --- outputs ----------------------------------------------------------
    def render_pdf(self, path, title="", png_path=None, dpi=150):
        import matplotlib
        matplotlib.use("Agg")
        matplotlib.rcParams["pdf.fonttype"] = 42      # embed TrueType: searchable text
        matplotlib.rcParams["font.family"] = FONT_REG
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle

        fig = plt.figure(figsize=(self.width, self.height))
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.axis("off")
        for kind, p in self.prims:
            if kind == "rect":
                ax.add_patch(Rectangle((p["x"], p["y"]), p["w"], p["h"], fill=False,
                                       edgecolor="black", linewidth=p["lw"]))
            elif kind == "knockout":
                ax.add_patch(Rectangle((p["x"], p["y"]), p["w"], p["h"], facecolor="white",
                                       edgecolor="none", zorder=2))
            elif kind == "line":
                ax.plot([p["x1"], p["x2"]], [p["y1"], p["y2"]], color="black",
                        linewidth=p["lw"], solid_capstyle="butt")
            elif kind == "text":
                ax.text(p["x"], p["y"], p["s"], fontsize=p["size"], ha=p["align"], va="baseline",
                        fontweight="bold" if p["bold"] else "normal", color="black", zorder=3)
        meta = {"Title": title, "Author": "KEYSTONE (AI) for Shane Brazelton", "Creator": "KEYSTONE titleblock.py", "CreationDate": None}
        fig.savefig(path, format="pdf", metadata=meta)
        if png_path:
            fig.savefig(png_path, format="png", dpi=dpi, facecolor="white")
        plt.close(fig)

    def render_dxf(self, path):
        import ezdxf
        from ezdxf.enums import TextEntityAlignment

        doc = ezdxf.new("R2010", setup=False)
        doc.units = ezdxf.units.IN
        doc.header["$INSUNITS"] = 1
        doc.header["$MEASUREMENT"] = 0
        doc.styles.new("KS-REG", dxfattribs={"font": "DejaVuSans.ttf"})
        doc.styles.new("KS-BOLD", dxfattribs={"font": "DejaVuSans-Bold.ttf"})
        for name, col in LAYER_COLORS.items():
            doc.layers.add(name, color=col)
        msp = doc.modelspace()
        align = {"left": TextEntityAlignment.LEFT, "center": TextEntityAlignment.CENTER,
                 "right": TextEntityAlignment.RIGHT}
        for kind, p in self.prims:
            if kind == "rect":
                x, y, w, h = p["x"], p["y"], p["w"], p["h"]
                msp.add_lwpolyline([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], close=True,
                                   dxfattribs={"layer": p["layer"]})
            elif kind == "line":
                msp.add_line((p["x1"], p["y1"]), (p["x2"], p["y2"]), dxfattribs={"layer": p["layer"]})
            elif kind == "text":
                t = msp.add_text(p["s"], height=p["size"] / 72.0 * DXF_CAP,
                                 dxfattribs={"layer": p["layer"], "style": "KS-BOLD" if p["bold"] else "KS-REG"})
                t.set_placement((p["x"], p["y"]), align=align[p["align"]])
        doc.saveas(path)


def add_titleblock(sheet: Sheet, info: dict, margin: float = 0.5, tb_h: float = 1.35,
                   stamp_h: float = 0.5) -> float:
    """Border + stamp band + title block along the bottom. Returns the top y of the stamp band.

    info keys: project, phase, title, subtitle, sheet_no, scale, date, revision, drawn_by, stamp.
    """
    W, H, m = sheet.width, sheet.height, margin
    L = TTLB
    sheet.rect(m, m, W - 2 * m, H - 2 * m, layer=L, lw=1.6)
    # stamp band
    y0 = m + tb_h
    sheet.rect(m, y0, W - 2 * m, stamp_h, layer=L, lw=1.4)
    sheet.text(W / 2, y0 + stamp_h / 2 - 0.08, info["stamp"], size=17, bold=True, align="center", layer=L)
    # title block cells: (label, value, width share)
    cells = [
        ("PROJECT", info["project"], 4.7),
        ("PHASE", info["phase"], 1.5),
        ("SHEET TITLE", info["title"], 3.1),
        ("SCALE", info["scale"], 0.9),
        ("DATE", info["date"], 1.45),
        ("REV", info["revision"], 0.75),
        ("DRAWN BY", info["drawn_by"], 2.1),
        ("SHEET", info["sheet_no"], 1.5),
    ]
    total = sum(c[2] for c in cells)
    scale = (W - 2 * m) / total
    x = m
    sheet.line(m, y0, W - m, y0, layer=L, lw=1.4)
    for i, (lab, val, share) in enumerate(cells):
        w = share * scale
        if i:
            sheet.line(x, m, x, y0, layer=L, lw=0.8)
        sheet.text(x + 0.08, y0 - 0.17, lab, size=7, bold=False, layer=L)
        pad = 0.08
        if lab == "SHEET":
            size = 20
            while text_width_in(val, size, True) > w - 0.2 and size > 10:
                size -= 1
            sheet.text(x + w / 2, m + (tb_h - 0.25) / 2 - 0.08, val, size=size, bold=True, align="center", layer=L)
        else:
            size = 13 if lab in ("PHASE", "SCALE", "REV", "DATE") else 11.5
            if lab == "DRAWN BY":
                size = 9.5
            lines = []
            for part in str(val).split("\n"):
                lines += wrap(part, w - 2 * pad, size, bold=lab != "DRAWN BY")
            yy = y0 - 0.24
            for ln in lines:
                yy -= pitch(size)
                sheet.text(x + pad, yy, ln, size=size, bold=lab != "DRAWN BY", layer=L)
        x += w
    return y0 + stamp_h
