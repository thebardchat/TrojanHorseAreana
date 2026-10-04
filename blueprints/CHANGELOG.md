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

## 2026-10-03 17:53 CT
- D-018 logged (solar + stormwater per MOVIE MAKER brief; stays parked). Look reference: /workspace/trojan-horse-arena/ (MOVIE MAKER, read-only).

## 2026-10-03 17:57 CT
- CHANGE APPROVED (Shane): solar + stormwater storage into Phase 2 as design intent, unsized. Retractable roof CUT. D-018 DECIDED. phase2.yaml `sustainability` added.

## 2026-10-03 · P1-T-003 · R-001 wall pads + R-003 ADA single-user restroom
- `research/R-001-wall-pads.md`:
  - NFHS guidance (HST 2022): about 6 ft high, 2 in pads, recessed door hardware.
  - The NFHS rules book is paywalled, so no NFHS *rule* on practice-room pads was verified.
  - IBC 2021 806.2 makes pads interior finish. 803.4 → 2603.9 means foam pads need a large-scale test of the finished assembly (NFPA 286 or equal). Table 803.13 room minimum is Class C, but the foam rule governs.
  - Alabama DCM adopts the 2021 IBC/IEBC/IFC for K-12.
  - Flag: some common pads are "foam core not fire-rated" or E84-only.
- `research/R-003-ada-single-user-restroom.md`:
  - 2010 ADA governs (Title II alteration; DCM says ADA supersedes IBC/A117.1).
  - Key-numbers table with section cites: 304, 305/306, 404, 603, 604, 606, 609, 703.
  - Flags: 213.2 Exc. 4 read conservatively (both rooms comply); path of travel may be triggered.
- `params/phase1.yaml`: new `standards` group (governing codes, wall_pads, ada_single_user_restroom), with `source: R-001` / `R-003`. Reference values only. No room dimensions. W1/W3 still TBD.
- BACKLOG: P1-T-003 done, P1-T-004 next. STATUS → P1-T-004, P1 10%, YELLOW, waiting on measurements.

## 2026-10-03 · R-001/R-003 approval: decisions recorded
- D-019 DECIDED (Shane, chat): full 2010 ADA compliance on BOTH new restrooms. This settles the 213.2 Exc. 4 question. phase1.yaml W3 `ada_compliance`, `restroom_type: single-user, one per sex`, `both_rooms_comply: YES`.
- D-020 DECIDED (Shane, chat): the scope sheet carries the NFPA 286 note verbatim. phase1.yaml W1 `purchase_note`.
- D-003 stays OPEN. Shane returned the pad-height template unfilled ("coach's call"). `pad_height: TBD`, with a note and sheet label "6 ft proposed (R-001 guidance), coach to confirm".
- Open decisions: 16, unchanged.

## 2026-10-03 · P1-T-004 · P1-G-001 scope sheet v1 (rev A)
- New `shared/titleblock.py`: one layout model renders to both a vector PDF (matplotlib, embedded searchable TrueType) and a DXF (ezdxf, inches). It draws the standard border, the PRELIMINARY stamp band and the title block (prompt §9).
- New `phase1/src/p1_g_001.py`: 11x17 landscape scope sheet built from phase1.yaml.
  - Work items W1, W2 and W3. W3 includes a 14-row 2010 ADA key-number table with section cites.
  - Sections: NOT INCLUDED, WHO APPROVES (draft/TBD), WAITING ON, and 2 "PHOTOS TBD" boxes.
  - The Phase 2 total is read from phase2.yaml for the NOT INCLUDED line.
  - The script exits non-zero if text runs past any box.
- Outputs: `phase1/out/pdf/P1-G-001.pdf`, `phase1/out/dxf/P1-G-001.dxf` (layers G-ANNO-TTLB, A-ANNO-TEXT). PNG preview kept outside the repo at /workspace/keystone_previews/P1-G-001.png.
- phase1.yaml additions:
  - `sheets.P1-G-001`: title block data, waiting_on, photo boxes
  - `approvals.chain_shown` / `research_pending`
  - `standards.wall_pads.sheet_basis`
  - `standards.ada_single_user_restroom.cites`
  - W1 `supplied_by_options`
  - No room dimensions added.
- Validate: the PDF stamp check is now non-vacuous and passes.

## 2026-10-03 · D-003 decided + P1-G-001 Rev B (principal version)
- D-003 DECIDED (Shane, chat): pad height 6 ft. phase1.yaml W1 `pad_height: 6 ft`.
- The unsettled parts of D-003 (which walls get pads, who supplies them) moved to new **D-021 OPEN**. Open count stays 16.
- **Rev A = INTERNAL copy, frozen.** Files renamed with `git mv`, bytes unchanged:
  - `phase1/out/pdf/P1-G-001_RevA_internal.pdf` (sha256 bfcffb05…)
  - `phase1/out/dxf/P1-G-001_RevA_internal.dxf` (sha256 31a36c02…)
- Rev A content is frozen in phase1.yaml `sheets.P1-G-001.revisions.A`.
- Reproducibility check: `p1_g_001.py --rev A --out-dir /tmp/…` gives identical PDF text, identical DXF entity text and geometry, and identical rendered pixels. The generator refuses to overwrite a frozen revision in the repo without `--force`.
- **Rev B = PRINCIPAL version:** `phase1/out/pdf/P1-G-001_RevB_principal.pdf` + `phase1/out/dxf/P1-G-001_RevB_principal.dxf`, built from `revisions.B`. Changes from Rev A:
  - No D-/R- codes and no name-spelling lines. IBC and ADA section numbers stay.
  - Requester line under the title.
  - W1 and W2 each get a "Why:" line.
  - Pad height prints "6 ft".
  - "WHAT WE'RE ASKING THE SCHOOL FOR" (3 asks) replaces WAITING ON.
  - WHO APPROVES reads: Principal / District facilities (Madison County Schools) / Others as the district requires.
  - Title block shows rev B.
- New phase1.yaml fields, sourced "Shane 2026-10-03": `contacts.requester`, W1/W2 `why`, `approvals.chain_plain`, `standards.wall_pads.sheet_basis_plain`.
- `shared/titleblock.py`: the PDF CreationDate is no longer stamped, so later builds can be reproduced exactly.
- `shared/validate.py` adds check 6b: every `*principal*.pdf` must contain no `D-0`/`R-0` codes and no "spelling". Tested against the Rev A text, it catches 9 codes plus "spelling".

## 2026-10-03 · P1-T-009 · R-002 approval path + R-004 donated labor/materials
- `research/R-002-approval-path.md`:
  - DCM says all public K-12 work gets DCM plan review, a pre-construction conference and inspections, at any cost and from any funding source, donations included. DCM fees are waived at or below $750k. DCM's own "Step 1" verifies each small scope.
  - The MCSS Booster & Support Organizations Guidelines (2021 file) say: campus building/land improvements go to the Board of Education; a Board employee is in charge; full design team; state review and inspection; "same process regardless of funding."
  - District facilities office: MCSS Operations & Facilities.
  - Gap: MCSS board policy (Simbli) was not readable.
- `research/R-004-donated-labor-materials.md`:
  - Public works sealed bids above $100,000 (§39-2-2). School-board purchases $40,000+ (§16-13B-1, per Examiners Feb 2025).
  - AG opinions (via Examiners): work paid entirely with private funds is not "public works" for bid law. None involve a school board.
  - GC license at $100,000+ (Act 2024-277).
  - Plumbing (§34-37-15) and electrical (303-X-3-.07) licenses required except owner / owner-employee exemptions. Volunteers are not addressed.
  - Bonds not required under $100,000. Insurance: DCM tells self-performing owners to consult their carrier.
  - Every finding is flagged NEEDS DISTRICT CONFIRMATION. No legal advice.
- phase1.yaml: `approvals.chain_per_sources`, `approvals.district_facilities_office`, `approvals.note_plain`, `standards.approvals_refs` (sources R-002 / R-004). Rev B approver line 2 is now "District facilities (MCSS Operations & Facilities)".
- P1-G-001 Rev B regenerated:
  - WHO APPROVES adds a plain note: "District guidelines send campus building improvements to the Board of Education. State building review (Alabama DCM) may also apply."
  - Row-2 widths changed for Rev B, and long box headings now shrink to fit.
- **Rev A unchanged.** Regenerating to /tmp still gives identical text. It stays frozen as the internal copy, so its "Who approves" was not edited, even though the R-files are in.
- D-004 notes updated; still OPEN. DECISIONS open count: 16.

## 2026-10-03 20:49 CT
- D-023 DECIDED: Rev B approved as-is, contact info stays, no history rewrite. D-022 OPEN: 1A/1B split, no restructure until Shane decides.
