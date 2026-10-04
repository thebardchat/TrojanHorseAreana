#!/usr/bin/env bash
# keystone_status.sh — ShaneBrain preflight bridge to KEYSTONE (Grok Bot on pulsar00100)
# Reads KEYSTONE's daily STATUS.json and prints a short block for session open.
#
# Source order:
#   1. pulsar00100 over Tailscale SSH (live file)
#   2. GitHub raw, branch grok/keystone (mirror, works when pulsar is asleep)
#
# Never fails preflight: always exits 0.
#
# Hook it into scripts/preflight.sh with ONE line, after session_context.py:
#   bash "$(dirname "$0")/keystone_status.sh" || true

set -u

PULSAR_HOST="${KEYSTONE_HOST:-hubby@pulsar00100}"
WIN_PATH='C:\Users\Hubby\Desktop\ARENA\_KEYSTONE\STATUS.json'
RAW_URL="${KEYSTONE_RAW_URL:-https://raw.githubusercontent.com/thebardchat/TrojanHorseAreana/grok/keystone/blueprints/STATUS.json}"
STALE_HOURS="${KEYSTONE_STALE_HOURS:-26}"
LOCAL_FILE="${KEYSTONE_LOCAL_FILE:-}"   # testing override

json=""
source_used=""

if [ -n "$LOCAL_FILE" ] && [ -f "$LOCAL_FILE" ]; then
  json="$(cat "$LOCAL_FILE")"; source_used="local:$LOCAL_FILE"
fi

if [ -z "$json" ]; then
  json="$(ssh -o BatchMode=yes -o ConnectTimeout=5 -o StrictHostKeyChecking=accept-new \
          "$PULSAR_HOST" "type \"$WIN_PATH\"" 2>/dev/null | tr -d '\r')"
  [ -n "$json" ] && source_used="pulsar00100"
fi

if [ -z "$json" ]; then
  json="$(curl -fsS --max-time 8 "$RAW_URL" 2>/dev/null)"
  [ -n "$json" ] && source_used="github:grok/keystone"
fi

echo "=== KEYSTONE · Trojan Horse Arena ==="

if [ -z "$json" ]; then
  echo "RED    — no status found (pulsar00100 unreachable and no GitHub mirror yet)"
  echo "====================================="
  exit 0
fi

KEYSTONE_JSON="$json" KEYSTONE_SRC="$source_used" KEYSTONE_STALE="$STALE_HOURS" python3 - 2>/dev/null <<'PY' || echo "RED    — STATUS.json unreadable (bad JSON?)"
import json, os
from datetime import datetime, timezone

d = json.loads(os.environ["KEYSTONE_JSON"])
src = os.environ["KEYSTONE_SRC"]
stale_h = float(os.environ["KEYSTONE_STALE"])

health = str(d.get("health", "RED")).upper()
age_note = "age unknown"
try:
    ts = datetime.fromisoformat(d["updated_at"])
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    age_h = (datetime.now(timezone.utc) - ts).total_seconds() / 3600
    age_note = f"{age_h:.0f}h old"
    if age_h > stale_h:
        health = "RED"
        age_note += f" — STALE (>{stale_h:.0f}h, daily update missed)"
except Exception:
    health = "RED"
    age_note = "bad or missing updated_at"

def g(k, default="-"):
    v = d.get(k)
    return v if v not in (None, "", []) else default

print(f"{health:<7}— {age_note} · via {src}")
print(f"Ticket : {g('current_ticket')} {g('current_ticket_title','')}".rstrip())
if "phase1_percent" in d or "phase2_percent" in d:
    print(f"Phases : active {g('active_phase')} · P1 {g('phase1_percent')}% · P2 {g('phase2_percent')}%")
else:
    print(f"SD set : {g('percent_complete_sd_set')}%")
done = d.get("sheets_done") or []
print(f"Done   : {', '.join(done) if done else '-'}")
print(f"Changed: {g('what_changed')}")
print(f"Verify : {g('what_to_verify')}")
print(f"Next   : {g('next_action')}")
if g("blocked_on") != "-":
    print(f"BLOCKED: {g('blocked_on')}")
if g("question_for_shane") != "-":
    print(f"ASK    : {g('question_for_shane')}")
print(f"Open decisions: {g('open_decisions')}")
PY

echo "====================================="
exit 0
