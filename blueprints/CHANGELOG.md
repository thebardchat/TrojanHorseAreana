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

## 2026-10-03 ~5:50 PM CT · P2-T-001 (seed only) · reference plan intake + phase2.yaml v1 seed
- Shane added 2 images to ARENA. **Phase 2 REFERENCE PLAN = `Phase2-floor-plan-flat.png`** (= `arenav1-floor-plan.png`, sha256 d030dcb4…bd54), designated by Shane (D-017 DECIDED). The diorama is demoted to secondary. `Phase2-floor-plan.jpeg` is the tabletop render (WebP inside a .jpeg name), with wrong labels. Not a source.
- ASSETS.md:
  - folder now 7 files
  - §1b describes the reference plan's zones/adjacencies and observations (no event lockers or mezzanine shown yet; 2 public restrooms)
  - §2 master plan → RECEIVED
  - §2a: the box's `floorplan_src.png` (39467dab…) is a re-encode of the tabletop render, still unused
- `params/phase2.yaml` v1 seed:
  - prompt §3 Phase 2 table + reference plan
  - seating 2,200 total locked
  - girls 3,503 tag with D-013 draw-equal rule
  - 9 support rooms "shown on reference plan, SF TBD"
  - no dimensions
- `shared/validate.py` v2:
  - parses phase2.yaml with the same source/superseded checks
  - blocks Phase 1 values in phase2.yaml
  - checks locked Phase 2 values
  - area reconciliation SKIPPED until SFs exist
  Passes. Negative test confirmed it fails on bad input.
- DECISIONS: D-016 OPEN (seating labels 3,200 vs 2,200). D-017 DECIDED. D-009 now points to D-016. 16 OPEN.
- BACKLOG: P2-T-001 marked "v1 seeded… Phase 1 still first." Active ticket stays **P1-T-003**.
