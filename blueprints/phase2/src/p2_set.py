"""KEYSTONE P2 sheet set bundler: draws the frozen member sheets into one multi-page tabloid PDF (matplotlib PdfPages,
same drawing code and inputs as the single-sheet generators, so the pages match the frozen single PDFs and the bundle
regenerates byte-identical; poppler pdfunite was not used because it writes a random /ID).

Phase 2 Schematic Set Rev A (FROZEN, Shane 2026-10-04 5:27 AM CT, D-036): P2-G-003 Rev F + P2-A-101 Rev D + P2-A-102 Rev D.
The set and its sheet list live in params/phase2.yaml `sets`. Every member sheet must be frozen. The bundle is FROZEN:
regenerate only with --out-dir for checking (it must come out byte-identical).
Usage (from the repo root):
  /workspace/.venv-keystone/bin/python blueprints/phase2/src/p2_set.py [--set phase2_schematic_set_rev_a] [--out-dir DIR] [--copy-to DIR] [--force]
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import yaml

BP = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BP / "shared"))
sys.path.insert(0, str(Path(__file__).resolve().parent))


def build_sheet(sheet, rev):
    """Rebuild one frozen sheet with its own generator's builder (same inputs as that generator's main())."""
    import p2_testfit as tf
    if sheet == "P2-G-003" and rev == "F":
        import p2_g_003 as g
        p2, prog, ob, out = tf.summary_f()
        return g.build_f(p2, prog, ob, out), f"{sheet} Rev {rev} {prog['meta_rev_f']['title']}"
    if sheet in ("P2-A-101", "P2-A-102") and rev == "D":
        import p2_a_plan as ap_
        p2, prog, ob, out = tf.summary_f()
        sh = ap_.build_d(sheet, p2, prog, out["plan"], out["loop"], (out["rows"], out["tot"]), out["geom"])
        return sh, f"{sheet} Rev {rev} {p2['sheets'][sheet]['title']}"
    sys.exit(f"no builder registered for {sheet} Rev {rev}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", default="phase2_schematic_set_rev_a")
    ap.add_argument("--out-dir", help="write the bundle here instead of phase2/out/pdf")
    ap.add_argument("--copy-to", help="also copy the bundle here (e.g. the preview folder, outside the repo)")
    ap.add_argument("--force", action="store_true", help="allow overwriting a FROZEN set in the repo")
    a = ap.parse_args()
    p2 = yaml.safe_load((BP / "params" / "phase2.yaml").read_text(encoding="utf-8"))
    st = p2["sets"][a.set]
    for m in st["sheets"]:
        rv = p2["sheets"][m["sheet"]]["revisions"][m["revision"]]
        if not rv.get("frozen"):
            sys.exit(f"{m['sheet']} Rev {m['revision']} is not frozen; a set may only hold frozen sheets.")
    out = (Path(a.out_dir) if a.out_dir else BP / "phase2" / "out" / "pdf") / f"{st['file']}.pdf"
    if not a.out_dir and st.get("frozen") and out.exists() and not a.force:
        sys.exit("Set is FROZEN; use --out-dir to regenerate for checking.")
    out.parent.mkdir(parents=True, exist_ok=True)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    meta = {"Title": st["name"], "Author": "KEYSTONE (AI) for Shane Brazelton", "Creator": "KEYSTONE p2_set.py", "CreationDate": None}
    with PdfPages(out, metadata=meta) as pdf:
        for m in st["sheets"]:
            sh, _ = build_sheet(m["sheet"], m["revision"])
            fig = sh.figure()
            pdf.savefig(fig)
            plt.close(fig)
    print(f"wrote {out} ({len(st['sheets'])} pages)")
    if a.copy_to:
        shutil.copy2(out, Path(a.copy_to) / out.name)
        print(f"copied to {Path(a.copy_to) / out.name}")


if __name__ == "__main__":
    main()
