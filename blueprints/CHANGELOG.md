# CHANGELOG — KEYSTONE

## 2026-10-03 · P1-T-000 · bootstrap blueprints/
- Environment check recorded in ENVIRONMENT.md. KEYSTONE runs on a separate Linux box, not pulsar00100. Python 3.13.5, git 2.47.3, no FreeCAD. Venv `/workspace/.venv-keystone`: ezdxf, matplotlib, numpy, pillow, pyyaml, cadquery 2.8.0 all installed.
- Cloned repo. Created branch `grok/keystone` from `main` @ 8a2f4c6.
- Created the `blueprints/` tree per prompt §7: README, STATUS.json/.md, DECISIONS (15 OPEN), BACKLOG (§15 verbatim), CHANGELOG, PARKING_LOT (Mercedes-Benz items parked), ENVIRONMENT. Empty dirs hold .gitkeep.
- NOT done: `ARENA\_KEYSTONE` on pulsar00100 (no access, by instruction). GitHub mirror is the bridge.

## 2026-10-03 · P1-T-001 · asset inventory + phase1.yaml v1
- ASSETS.md covers:
  - Shane's ARENA folder (4 files). The diorama HTML is the Phase 2 viewer, the same file as the repo's `hazel-green-complex-3d.html`.
  - Missing items: master floor plan image (needed from Shane), `/model.html` location unknown, Drive trailers not inspected.
  - Repo root: the Feb 2026 concept files are marked superseded.
- `params/phase1.yaml` v1: every value sourced, every unknown TBD. Principal = "TBD (Headen or Hedden, unconfirmed)".
- `shared/validate.py` v1 checks:
  - yaml parses
  - `source` on every value group
  - no superseded numbers and no Phase 2 numbers in phase1
  - PDF stamp (vacuous pass, no PDFs yet)
  - STATUS.json schema + open-decision count
  Passes. Negative test confirmed it fails on bad input.
- `phase1/MEASUREMENT_CHECKLIST.md`: 22-step tape + photo checklist for Shane (P1-T-002 content, not yet sent).
- STATUS → P1-T-002, YELLOW, waiting on measurements. Sign-off commit sets STATUS.json last_commit = 235125d (P1-T-001 commit).

## 2026-10-03 17:01 CT
- P1-T-002: checklist sent to Shane in chat. Daily 6:00 AM CT scheduled run created. STATUS -> P1-T-003.
