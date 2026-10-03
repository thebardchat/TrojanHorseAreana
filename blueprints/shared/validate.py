#!/usr/bin/env python3
"""KEYSTONE validate.py: run before every commit. Exit 0 = pass, 1 = fail.

Usage (from repo root):  python blueprints/shared/validate.py
Needs: pyyaml. Optional: pdftotext (poppler-utils) for the PDF stamp check.

Checks (v1, Phase 1 bootstrap):
  1. params/phase1.yaml exists and parses (phase2.yaml too, if present)
  2. Every mapping that holds values carries a non-empty `source`
  3. No superseded Feb 2026 concept numbers in any params file
  4. No Phase 2 program numbers in phase1.yaml
  5. Every PDF in phase*/out/pdf contains the PRELIMINARY stamp text (passes if no PDFs)
  6. STATUS.json (if present) matches schema_version 2 and its open_decisions
     equals the OPEN count in DECISIONS.md
Not yet built: room overlap, area reconciliation, locker parity, mat fit,
occupant-load factor checks. Those come with drawings (P2-T-002 for Phase 2).
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
    ok("superseded / cross-phase number scan done")


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
    check_status()
    if failures:
        print(f"\nVALIDATE FAILED: {len(failures)} problem(s). Do not commit.")
        sys.exit(1)
    print("\nVALIDATE PASSED")
    sys.exit(0)
