#!/usr/bin/env python3
"""KEYSTONE validate.py: run before every commit. Exit 0 = pass, 1 = fail.

Usage (from repo root):  python blueprints/shared/validate.py
Needs: pyyaml. Optional: pdftotext (poppler-utils) for the PDF stamp check.

Checks (v2, 2026-10-03: phase2.yaml seed added):
  1. params/phase1.yaml exists and parses; phase2.yaml too, if present
  2. Every mapping that holds values carries a non-empty `source` (both files)
  3. No superseded Feb 2026 concept numbers in any params file
  4. No Phase 2 program numbers in phase1.yaml; no Phase 1 values in phase2.yaml
  5. phase2.yaml locked values unchanged (55,000 SF total, 22,000 SF arena,
     2,200 seats total) and the girls locker carries the D-013 draw-equal rule
  6. Every PDF in phase*/out/pdf contains the PRELIMINARY stamp text (passes if no PDFs)
     6b. Principal-version PDFs (*principal*.pdf, e.g. P1-G-001 Rev B and Rev C) contain no 'D-0'/'R-0' codes and no 'spelling'
  7. STATUS.json (if present) matches schema_version 2 and its open_decisions
     equals the OPEN count in DECISIONS.md
SKIPPED for now: Phase 2 area reconciliation (55,000 vs room sum). Most support
room SFs are TBD. Not yet built: room overlap, mat fit, occupant-load factor
checks. Those come with drawings (P2-T-002).
"""
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("FAIL  pyyaml not installed (pip install pyyaml)")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent  # blueprints/
PARAMS = ROOT / "params"
STAMP = "PRELIMINARY — CONCEPTUAL DESIGN — NOT FOR CONSTRUCTION"
META_KEYS = {"source", "notes"}

# Superseded Feb 2026 concept (prompt §3). Matched on raw text, comments included.
SUPERSEDED = [
    (r"120\s*(ft|')?\s*[x×X*]\s*250", "120x250 footprint"),
    (r"\b30,?000\b", "30,000 SF"),
    (r"\b800\b", "800 seats"),
    (r"\$?\s*4\s*(M|million)?\s*(-|–|—|to)\s*\$?\s*6\s*(M|million)\b", "$4-6M budget"),
]
# Phase 2 program numbers (prompt §3) that must never sit in phase1.yaml.
PHASE2_ONLY = [
    (r"\b55,?000\b", "55,000 SF building"),
    (r"\b22,?000\b", "22,000 SF arena"),
    (r"\b2,?200\b", "2,200 seats"),
    (r"\b3,?50[03]\b", "locker SF"),
    (r"\b6,?000\s*SF\b", "6,000 SF S&C"),
    (r"\b4,?000\s*SF\b", "4,000 SF cross-training"),
]
# Phase 1 (remodel) values that must never sit in phase2.yaml.
PHASE1_ONLY = [
    (r"walk-?through\s+room", "Phase 1 walk-through room"),
    (r"wrestling[_ ]room", "Phase 1 wrestling room"),
    (r"wall\s+pad", "Phase 1 wall pads"),
    (r"\bHeaden\b|\bHedden\b", "Phase 1 school contact"),
    (r"11\s*x\s*17", "Phase 1 sheet size"),
    (r"\bid:\s*W[123]\b", "Phase 1 work item"),
]
# Locked Phase 2 values (prompt §3; Shane 2026-10-03). Change only with "CHANGE APPROVED".
PHASE2_LOCKED = [
    (("building", "total_sf"), 55000),
    (("spaces", "arena", "sf"), 22000),
    (("spaces", "arena", "mats"), 4),
    (("spaces", "seating", "total"), 2200),
    (("spaces", "boys_locker", "sf"), 3500),
    (("spaces", "strength_conditioning", "sf"), 6000),
    (("spaces", "cross_training", "sf"), 4000),
]
STATUS_KEYS = [
    "agent", "project", "schema_version", "updated_at", "health", "active_phase",
    "phase1_percent", "phase2_percent", "current_ticket", "current_ticket_title",
    "sheets_done", "sheets_in_progress", "last_commit", "branch", "open_decisions",
    "blocked_on", "what_changed", "what_to_verify", "next_action", "question_for_shane",
]

failures = []


def fail(msg):
    failures.append(msg)
    print(f"FAIL  {msg}")


def ok(msg):
    print(f"ok    {msg}")


def is_value(v):
    return not isinstance(v, (dict, list)) or (
        isinstance(v, list) and all(not isinstance(i, (dict, list)) for i in v)
    )


def check_sources(node, path, fname):
    """Every mapping holding at least one value (scalar or list of scalars) needs `source`."""
    count = 0
    if isinstance(node, dict):
        has_values = any(is_value(v) for k, v in node.items() if k not in META_KEYS)
        if has_values:
            src = node.get("source")
            if src is None or str(src).strip() in ("", "TBD"):
                fail(f"{fname}: {path or '<root>'} has values but no `source`")
            count += 1
        for k, v in node.items():
            if isinstance(v, (dict, list)):
                count += check_sources(v, f"{path}.{k}" if path else str(k), fname)
    elif isinstance(node, list):
        for i, item in enumerate(node):
            if isinstance(item, (dict, list)):
                count += check_sources(item, f"{path}[{i}]", fname)
    return count


def check_params():
    p1 = PARAMS / "phase1.yaml"
    if not p1.exists():
        fail("params/phase1.yaml missing")
        return
    for f in sorted(PARAMS.glob("*.yaml")):
        text = f.read_text(encoding="utf-8")
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError as e:
            fail(f"{f.name} does not parse: {e}")
            continue
        if not isinstance(data, dict):
            fail(f"{f.name} top level is not a mapping")
            continue
        ok(f"{f.name} parses ({len(data)} top-level groups)")
        before = len(failures)
        n = check_sources(data, "", f.name)
        if len(failures) == before:
            ok(f"{f.name}: {n} value groups checked for `source`")
        for pat, label in SUPERSEDED:
            for m in re.finditer(pat, text, flags=re.IGNORECASE):
                line = text.count("\n", 0, m.start()) + 1
                fail(f"{f.name}:{line} superseded concept value ({label}): '{m.group(0)}'")
        if f.name == "phase1.yaml":
            for pat, label in PHASE2_ONLY:
                for m in re.finditer(pat, text, flags=re.IGNORECASE):
                    line = text.count("\n", 0, m.start()) + 1
                    fail(f"{f.name}:{line} Phase 2 value in Phase 1 params ({label}): '{m.group(0)}'")
        if f.name == "phase2.yaml":
            for pat, label in PHASE1_ONLY:
                for m in re.finditer(pat, text, flags=re.IGNORECASE):
                    line = text.count("\n", 0, m.start()) + 1
                    fail(f"{f.name}:{line} Phase 1 value in Phase 2 params ({label}): '{m.group(0)}'")
            check_phase2_locked(data)
    ok("superseded / cross-phase number scan done")


def dig(d, keys):
    for k in keys:
        if not isinstance(d, dict) or k not in d:
            return None
        d = d[k]
    return d


def check_phase2_locked(data):
    before = len(failures)
    for keys, want in PHASE2_LOCKED:
        got = dig(data, keys)
        if got != want:
            fail(f"phase2.yaml {'.'.join(keys)} = {got!r}, locked value is {want!r}")
    girls = dig(data, ("spaces", "girls_locker")) or {}
    if "D-013" not in str(girls.get("draw_rule", "")):
        fail("phase2.yaml spaces.girls_locker needs a draw_rule citing D-013 (draw equal)")
    if len(failures) == before:
        ok("phase2.yaml locked values intact; girls locker D-013 draw-equal rule present")
    ok("phase2.yaml area reconciliation (55,000 SF vs room sum) SKIPPED: support room SFs are TBD")


def pdf_text(pdf):
    if shutil.which("pdftotext"):
        r = subprocess.run(["pdftotext", "-q", str(pdf), "-"], capture_output=True)
        if r.returncode == 0:
            return r.stdout.decode("utf-8", "replace")
    return pdf.read_bytes().decode("latin-1", "replace")


def check_pdfs():
    pdfs = sorted(ROOT.glob("phase*/out/pdf/**/*.pdf"))
    if not pdfs:
        ok("no PDFs yet: stamp check passes vacuously")
        return
    norm = lambda s: re.sub(r"\s+", " ", s.replace("–", "—")).upper()
    for pdf in pdfs:
        if norm(STAMP) in norm(pdf_text(pdf)):
            ok(f"stamp present: {pdf.relative_to(ROOT)}")
        else:
            fail(f"PRELIMINARY stamp text missing: {pdf.relative_to(ROOT)}")


def check_principal_pdfs():
    """Principal-facing sheets (file name contains 'principal'): no internal D-###/R-### codes, no name-spelling notes."""
    pdfs = sorted(ROOT.glob("phase*/out/pdf/**/*principal*.pdf"))
    if not pdfs:
        ok("no principal-version PDFs yet: code-free check passes vacuously")
        return
    for pdf in pdfs:
        text = re.sub(r"\s+", " ", pdf_text(pdf))
        bad = sorted(set(re.findall(r"[DR]-0\d*", text)))
        if re.search(r"spelling", text, flags=re.IGNORECASE):
            bad.append("'spelling'")
        if bad:
            fail(f"principal PDF shows internal codes/notes {bad}: {pdf.relative_to(ROOT)}")
        else:
            ok(f"principal PDF is code-free (no D-0/R-0, no 'spelling'): {pdf.relative_to(ROOT)}")


def check_status():
    sj = ROOT / "STATUS.json"
    if not sj.exists():
        ok("STATUS.json not present yet: skipped")
        return
    try:
        d = json.loads(sj.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(f"STATUS.json invalid JSON: {e}")
        return
    if list(d.keys()) != STATUS_KEYS:
        missing = [k for k in STATUS_KEYS if k not in d]
        extra = [k for k in d if k not in STATUS_KEYS]
        if missing or extra:
            fail(f"STATUS.json keys wrong. missing={missing} extra={extra}")
    if d.get("schema_version") != 2:
        fail("STATUS.json schema_version must be 2")
    if d.get("health") not in ("GREEN", "YELLOW", "RED"):
        fail("STATUS.json health must be GREEN/YELLOW/RED")
    try:
        ts = datetime.fromisoformat(d.get("updated_at", ""))
        if ts.tzinfo is None:
            fail("STATUS.json updated_at has no UTC offset")
    except ValueError:
        fail("STATUS.json updated_at is not ISO 8601")
    for k, v in d.items():
        vals = v if isinstance(v, list) else [v]
        for s in vals:
            if isinstance(s, str) and len(s) >= 300:
                fail(f"STATUS.json {k} string is {len(s)} chars (max 299)")
    dec = ROOT / "DECISIONS.md"
    if dec.exists():
        n_open = len(re.findall(r"^\|\s*D-\d{3}\s*\|.*\|\s*OPEN\s*\|", dec.read_text(encoding="utf-8"), flags=re.M))
        if d.get("open_decisions") != n_open:
            fail(f"STATUS.json open_decisions={d.get('open_decisions')} but DECISIONS.md has {n_open} OPEN")
        else:
            ok(f"open_decisions matches DECISIONS.md ({n_open} OPEN)")
    ok("STATUS.json schema checked")


if __name__ == "__main__":
    print(f"KEYSTONE validate: {ROOT}")
    check_params()
    check_pdfs()
    check_principal_pdfs()
    check_status()
    if failures:
        print(f"\nVALIDATE FAILED: {len(failures)} problem(s). Do not commit.")
        sys.exit(1)
    print("\nVALIDATE PASSED")
    sys.exit(0)
