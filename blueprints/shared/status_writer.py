"""KEYSTONE status writer (reviewer C-10). Stamps blueprints/STATUS.json and regenerates STATUS.md from it.

What it enforces (same rules as validate.py check_status, so a stamped file always validates):
  * updated_at = the real box clock, ISO 8601 WITH the UTC offset (America/Chicago, e.g. -05:00). A naive timestamp
    would be read as UTC by keystone_status.sh and print the wrong age (5-6 h off).
  * sheets_done = current revisions only, at most 12 entries.
  * every string < 300 characters; open_decisions = the OPEN rows in DECISIONS.md.
Then it prints the age exactly the way the ShaneBrain preflight bridge (keystone_status.sh) computes it and, with
--preflight, runs that script against the local file (KEYSTONE_LOCAL_FILE) so the printed block can be checked.

Usage (repo root):
  /workspace/.venv-keystone/bin/python blueprints/shared/status_writer.py [--stamp] [--commit SHA] [--preflight]
  --stamp      set updated_at to now (local zone, with offset); without it the file's own updated_at is kept
  --commit     set last_commit
  --preflight  run blueprints/shared/keystone_status.sh on the written file and show its output
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

BP = Path(__file__).resolve().parents[1]
SJ, SM, DEC = BP / "STATUS.json", BP / "STATUS.md", BP / "DECISIONS.md"
MAX_DONE, MAX_STR = 12, 299


def age_line(updated_at: str, stale_h: float = 26) -> str:
    """Same arithmetic as keystone_status.sh (naive -> UTC, whole hours, STALE past 26 h)."""
    ts = datetime.fromisoformat(updated_at)
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    age_h = (datetime.now(timezone.utc) - ts).total_seconds() / 3600
    s = f"{age_h:.0f}h old ({age_h * 60:.0f} min)"
    return s + (f" — STALE (>{stale_h:.0f}h)" if age_h > stale_h else "")


def write_md(d: dict) -> str:
    t = datetime.fromisoformat(d["updated_at"])
    hh = t.strftime("%I:%M %p").lstrip("0")
    md = (f"# KEYSTONE — {t:%Y-%m-%d} {hh} CT\n"
          f"HEALTH: {d['health']} · P1 {d['phase1_percent']}% · P2 {d['phase2_percent']}% · Ticket {d['current_ticket']}\n"
          f"WHAT CHANGED: {d['what_changed']}\n"
          f"WHAT TO VERIFY: {d['what_to_verify']}\n"
          f"NEXT ACTION: {d['next_action']}\n"
          f"QUESTION FOR SHANE: {d['question_for_shane']}\n")
    SM.write_text(md, encoding="utf-8")
    return md


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stamp", action="store_true")
    ap.add_argument("--commit")
    ap.add_argument("--preflight", action="store_true")
    a = ap.parse_args()
    d = json.loads(SJ.read_text(encoding="utf-8"))
    if a.stamp:
        d["updated_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
    if a.commit:
        d["last_commit"] = a.commit
    errs = []
    if datetime.fromisoformat(d["updated_at"]).tzinfo is None:
        errs.append("updated_at has no UTC offset")
    if len(d.get("sheets_done", [])) > MAX_DONE:
        errs.append(f"sheets_done has {len(d['sheets_done'])} entries (max {MAX_DONE}, current revs only)")
    for k, v in d.items():
        for s in (v if isinstance(v, list) else [v]):
            if isinstance(s, str) and len(s) > MAX_STR:
                errs.append(f"{k} string is {len(s)} chars (max {MAX_STR})")
    n_open = len(re.findall(r"^\|\s*D-\d{3}\s*\|.*\|\s*OPEN\s*\|", DEC.read_text(encoding="utf-8"), flags=re.M))
    if d.get("open_decisions") != n_open:
        errs.append(f"open_decisions={d.get('open_decisions')} but DECISIONS.md has {n_open} OPEN")
    if errs:
        print("STATUS NOT WRITTEN:\n  " + "\n  ".join(errs))
        return 1
    SJ.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_md(d)
    print(f"STATUS.json + STATUS.md written · updated_at {d['updated_at']} · age {age_line(d['updated_at'])} · "
          f"sheets_done {len(d['sheets_done'])} · open {n_open}")
    if a.preflight:
        sh = BP / "shared" / "keystone_status.sh"
        r = subprocess.run(["bash", str(sh)], env={"KEYSTONE_LOCAL_FILE": str(SJ), "PATH": "/usr/bin:/bin"},
                           capture_output=True, text=True, timeout=60)
        print(r.stdout.rstrip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
