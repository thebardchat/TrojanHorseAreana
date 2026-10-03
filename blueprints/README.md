# blueprints/ — KEYSTONE working directory

KEYSTONE is the AI architect / drawing-set producer for the **Hazel Green Regional Athletic Complex** (Trojan Horse Arena), working for Shane Brazelton.
Everything here is **PRELIMINARY — CONCEPTUAL DESIGN — NOT FOR CONSTRUCTION.**

Two separate jobs, never blended:
- **Phase 1 (now):** remodel of the high school's existing wrestling room + walk-through room. 3 items: wall pads, plumbing repair (scope only, by licensed plumber), split restrooms (1 male + 1 female).
- **Phase 2 (future):** new building + campus. Starts after the Phase 1 package ships.

The repo-root files (README, build/render scripts, STEP/STL, PNGs) show a superseded February 2026 concept. They're history, not either current phase. KEYSTONE never edits them.

| File / folder | Purpose |
|---|---|
| `STATUS.json` / `STATUS.md` | Daily bridge read by ShaneBrain's Pi preflight (`keystone_status.sh`) |
| `BACKLOG.md` | Ticket list. One ticket at a time, Phase 1 first |
| `DECISIONS.md` | OPEN / DECIDED / PARKED questions for Shane |
| `CHANGELOG.md` | What changed, per session |
| `PARKING_LOT.md` | Out-of-scope ideas, incl. parked sustainability inspiration |
| `ENVIRONMENT.md` | Where KEYSTONE runs, tool versions, asset locations |
| `ASSETS.md` | Inventory of Shane's ARENA folder + repo root |
| `params/phase1.yaml` | Single source of truth for Phase 1. Every value has a `source`, unknowns are `TBD` |
| `params/phase2.yaml` | Single source of truth for Phase 2 (not yet created, P2-T-001) |
| `research/` | Cited R-files (R-001…) |
| `phase1/` | `src/` generators, `out/pdf`, `out/dxf`, `photos/`, `MEASUREMENT_CHECKLIST.md` |
| `phase2/` | `src/`, `out/pdf`, `out/dxf`, `out/model`, `out/renders` |
| `shared/validate.py` | Run before every commit. Fail = no commit |

Branch: `grok/keystone` only. Shane merges to `main` via PR. Pushes to `main` auto-deploy publicly.
