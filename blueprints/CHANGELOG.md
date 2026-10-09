# CHANGELOG — KEYSTONE

## 2026-10-04 ~6:10 AM CT · P1-T-008 · P1-P-001 Rev A plumbing / water restore scope narrative
- **Unblocked Phase 1 ticket** taken ahead of P2-T-009 A-301 (Phase 1 outranks; P1-T-005…007 still wait on Dr. Headen / support-wing measurements).
- **params/phase1.yaml:** structured `existing.plumbing` fields for the sheet — `fixture_inventory.items` (2 showers, 1 private toilet, 2 toilets, 1 urinal, sinks TBD, 1 water fountain/sink; all OOS), `scope_of_work.items`, `open_asks.items`, `licensed_trade` (note + R-004.3 cite), `cross_refs` to frozen P1-G-001 Rev D / P1-A-101 Rev A package. New `sheets.P1-P-001` register (Rev A). Every group sourced; no invented pipe sizes or costs. D-002 stays OPEN.
- **New sheet** `phase1/out/{pdf,dxf}/P1-P-001_RevA` from new `phase1/src/p1_p_001.py` (11x17 landscape, NTS): existing-condition narrative, fixture inventory table, scope-of-work bullets (diagnose / restore / repair as plumber directs — NOT design), BY LICENSED PLUMBER / ENGINEER OF RECORD callout (Ala. Code §§34-37-6(a), 34-37-15 via R-004.3), open asks, cross-refs. PRELIMINARY stamp + title block via shared/titleblock.py. Drawn by KEYSTONE (AI) for Shane Brazelton.
- Preview (box only): `/workspace/keystone_previews/P1-P-001.png`.
- Frozen P1-G-001 Revs A–D and P1-A-101 Rev A untouched. Phase 2 Schematic Set Rev A untouched.
- BACKLOG: P1-T-008 done. Next: resume P2-T-009 (A-301) or P2-T-007; Phase 1 jumps when data arrives.
- DECISIONS: no new decisions; D-002 remains OPEN until plumber visit + photos.
- ASSETS + STATUS updated.

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

## 2026-10-03 ~10:00 PM CT · W2 no-water update + P1-G-001 Rev C
- **Shane, firsthand 2026-10-03:**
  - There is no running water to the area. All fixtures (showers, toilets, sinks) are out of service, not just leaking. Cause unknown.
  - phase1.yaml W2 is renamed "Restore water / plumbing repair". New fields: `status` (exact text), `status_detail`, `cause: TBD`, and a new `scope` and `why`. It is still BY LICENSED PLUMBER / ENGINEER OF RECORD, narrative only.
  - `existing.plumbing.condition` is updated; the old wording is kept as `condition_before_2026_10_03`.
- **D-024 DECIDED:** priority is W2 → W3 → W1, and W1 (pads) can run in parallel. Each work item now has a `priority` field.
- **Shane's aerial sketch** (`wrestle-room-measure.png`, not committed) → `existing.wrestling_room.estimate_aerial`:
  - KEYSTONE estimate of the exterior roof footprint: ≈55 ft N-S × 47 ft E-W.
  - Basis: path 276.85 ft, 7.49 px/ft, cross-checked against the 5 ft ticks and the 50/150/250 ft labels.
  - Confidence LOW. Length and width stay TBD. Never drawn.
- **`existing.layout_notes`:** qualitative room layout from the markup. ASSETS.md §1c and its table now show the folder at 8 files.
- DECISIONS: D-001 notes partial info (estimate + layout; tape + photos still needed). D-002 notes the no-water finding. Open count stays 17.
- **P1-G-001 Rev C (principal) added:** `phase1/out/pdf/P1-G-001_RevC_principal.pdf` + `.dxf`. It is Rev B plus these changes:
  - Panels are ordered W2, W3, W1, with "PRIORITY 1 / 2 / 3 — CAN RUN IN PARALLEL" labels. W1 also says "Does not depend on water."
  - The W2 panel shows the no-water status box, the new scope line and Why, and the licensed-plumber callout.
  - The asks list adds #4, a plumber visit to diagnose the missing water.
  - Row-1 text is slightly smaller (9.6 pt body, 8.4 pt ADA table) so the priority lines fit. Layout changed, content did not.
  - No codes. No aerial estimate.
- **Rev B frozen** (`frozen: true`) and its committed PDF is untouched. Regenerating it to /tmp gives a byte-identical PDF (sha256 6c05e8df…).
  - Rev A regenerates to the same PDF as before the change, with identical text.
  - Frozen revisions read their W2 wording from a `w2_as_issued` snapshot.
- Generator: `--rev A|B|C` (default C). It refuses to overwrite frozen A/B files without `--force`.
  - validate 6b already checks every `*principal*.pdf` (B and C); only the docstring was updated.
- D-022 is still OPEN. No 1A/1B restructure.

## 2026-10-03 ~10:30 PM CT · tape measurement, W2 fill-ins, P1-G-001 Rev D, P1-A-101 Rev A started
- **Wrestling room taped by Shane** ("Shane tape, inside wall-to-wall, 2026-10-03"): 55'-0" N-S × 45'-0" E-W, rectangle, long side N-S.
  - Recorded as `existing.wrestling_room.length_ft: 55` / `width_ft: 45`, with shape, long_side, and measured_at.
  - `floor_area_sf_calc: 2475` is calculated by KEYSTONE.
  - `estimate_aerial` is kept as a cross-check only and notes the agreement (55.1 × 46.9 ft exterior).
- **W2 fill-ins (Shane, firsthand):**
  - Fixtures: 2 showers, 1 private toilet, 2 toilets, 1 urinal, sinks (count TBD), water fountain/sink. All are out of service, with no running water.
  - Problem spots: the entire support wing. The showers were broken before the water loss.
  - Where: the support wing east of the wrestling room, along the open hallway.
- **W1 `pad_estimate` (Shane's estimate):** ~200 LF, ~1,200 SF at 6 ft, ~100 panels of 2×6 ft, before door deductions (3 exits + 1 hallway door). It assumes all 4 walls. KEYSTONE checked the math: 2(55+45) = 200; 200 × 6 = 1,200; 1,200 / 12 = 100. Walls stay TBD (D-021 OPEN). Pad thickness stays TBD.
- **P1-G-001 Rev D (principal)** = Rev C plus:
  - W2 Where / Problem spots / Existing fixtures filled in.
  - A W1 "Estimate:" line.
  - Rev D layout only: panel widths W2 .325 / W3 .36 / W1 .315, 9.2 pt body, ADA table columns widened. Content unchanged.
  - Outputs: `out/pdf/P1-G-001_RevD_principal.pdf` + `.dxf`. Default `--rev` is now D.
  - Shane's single-file copy: `/workspace/keystone_previews/P1-G-001.pdf`.
- **Rev C is now frozen** too. Revs A, B, and C print W2 from their `w2_as_issued` snapshots. Regenerating A/B/C to /tmp gives PDFs identical to before (B and C byte-identical to the committed files).
- **P1-A-101 Rev A (new, `phase1/src/p1_a_101.py`):** existing conditions plan at 1/8" = 1'-0". The 1/4" and 3/16" scales do not fit 55 ft on the 11x17 body.
  - Inside-face rectangle with overall dimension strings.
  - Four door marks tagged APPROX. (west, south, NE exits + east hallway door), with no dimensioned locations or widths.
  - Wall thickness TBD (single line at the inside face).
  - Support wing as a dashed, undimensioned "NOT YET MEASURED" outline.
  - Also: north arrow (approx.), graphic scale, notes, legend, PRELIMINARY stamp.
  - Outputs: `out/pdf/P1-A-101_RevA.pdf` + `out/dxf/P1-A-101_RevA.dxf` (paper inches; 1 in = 8 ft).
- shared/titleblock.py: optional `dashed()` lines, an optional text rotation (stored only when used), and extra DXF layers added only when a sheet uses them. Existing sheets render unchanged.
- DECISIONS: D-001 (room measured; wing, doors, ceiling, and photos TBD), D-002 (fixtures and spots), and D-021 (the estimate assumes all 4 walls). All still OPEN; the count stays 17. ASSETS §1c notes the tape and the door reads. BACKLOG: P1-T-005 IN PROGRESS.

## 2026-10-03 ~10:45 PM CT · Shane update 10:12 PM: Dr. Headen, CLG 10 ft, CMU, doors · Rev D + P1-A-101 Rev A revised in place
- **D-005 DECIDED:** the principal is "Dr. Headen" (phase1.yaml `contacts.principal.name/display_name`). Open count goes to 16.
- **phase1.yaml `existing.wrestling_room`:**
  - `ceiling_ft: 10` (Shane, firsthand)
  - wall_material CMU
  - `wall_thickness_assumed_in: 8` (ASSUMED; actual thickness stays TBD)
  - `door_assumed` 3'-0" × 7'-0" single HM, "ASSUMED STANDARD, VERIFY", including the south-exit pair note
- **W1 `pad_estimate` replaced** (Shane's estimate): ~188 LF after 4 doors (200 − 4×3), ~94 panels (188×6/12), 6'-0" pads under a 10'-0" ceiling, assumes all 4 walls. `pad_area_sf_calc: 1128` is a KEYSTONE calc and is not on the sheet. The earlier estimate is recorded as superseded.
- **W3 `location`:** support wing (waiting on support wing measurements).
- **P1-G-001 Rev D revised in place** (it had not been shown to Shane; no Rev E):
  - "For review by: Dr. Headen (principal) + district facilities".
  - WHO APPROVES 1 reads "Principal (Dr. Headen)".
  - Ask 1 now covers the support wing + walk-through room. New ask 5: "Copies of the photos Dr. Headen took".
  - W3 Where: "Support wing — waiting on support wing measurements."
  - New W1 Estimate line.
  - Asks text is 10 pt to fit five items.
- **Frozen revs:** the snapshot key is renamed `as_issued` (W2 + W3 Where). Regenerating A/B/C to /tmp gives identical PDFs (B and C byte-identical to the committed files).
- **P1-A-101 Rev A revised in place:**
  - Walls are 8" CMU double lines OUTSIDE the tape inside face. The dimension strings are marked INSIDE.
  - Four 3'-0" door openings with jambs, leaves, and 90° swings. Outward swing and hinge side are ASSUMED. Each is tagged "LOCATION APPROX." + "3'-0" × 7'-0" HM — ASSUMED STANDARD, VERIFY". The south tag adds "May be a pair of doors (markup) — verify".
  - New tags: CLG 10'-0" and "WALLS: 8" CMU — ASSUMED".
  - Notes (9) and legend are updated.
- Single-file copies for Shane: `/workspace/keystone_previews/P1-G-001.pdf` (Rev D) and `/workspace/keystone_previews/P1-A-101.pdf`.

## 2026-10-03 ~10:40 PM CT · approvals + Phase 1 package + P2-T-003 (R-005)
- Shane (10:29 PM CT): "P1-A-101 Rev A and P1-G-001 Rev D approved." **D-025** (Rev D approved, frozen) and **D-026** (A-101 Rev A approved, frozen; door locations match his markup; exits swing out) logged as DECIDED. Open count unchanged at 16.
- `params/phase1.yaml`: P1-G-001 Rev D and P1-A-101 Rev A set `frozen: true`. Both generators refuse to overwrite without `--force` (checked). `door_assumed` gets the confirmation note: "locations confirmed by Shane vs markup 2026-10-03; exit swings out confirmed; hallway door swing + south exit single/pair still to verify." Hallway swing + south exit leaves stay ASSUMED, verify. **No sheet regenerated**; /tmp regen of Rev B/C/D and A-101 Rev A is byte-identical to the committed files.
- New `phase1/out/pdf/Phase1_Package_for_Dr_Headen.pdf` (copy in `/workspace/keystone_previews/`): G-001 Rev D then A-101 Rev A via `pdfunite`. Checks: 2 pages, both 1224 × 792 pt (11x17 landscape), stamp on both pages, no D-0/R-0 codes, no "spelling".
- `shared/validate.py` check 6b now also covers `*Package*.pdf` (principal-facing bundles).
- **P2-T-003 started:** `research/R-005-nfhs-wrestling-mats.md`. NFHS Rule 2-1: 28-ft min circle + ~5-ft safety area (38 ft square by arithmetic), 1-in PVC foam equivalent to 4 in max, 10-ft surrounding space and benches/table 10 ft where facilities permit; no padding rule found; AHSAA uses NFHS rules, nothing extra found. Current rulebook paywalled → current wording UNVERIFIED. Arithmetic: 4 mats fit 22,000 SF by area in all cases checked; real fit needs room dims. D-014 stays OPEN; phase2.yaml untouched.
- BACKLOG / ASSETS updated.

## 2026-10-03 ~11:30 PM CT · Phase 2 ACTIVE · P2-T-003b program test-fit (P2-G-003 Rev A)
- Shane (10:45 PM CT): Phase 2 active in parallel (**D-027** DECIDED); Phase 1 package delivered, Phase 1 waits on Dr. Headen, Phase 1 tickets jump the line when data arrives. Phase 2 is Shane's build, not a school project (**D-028** DECIDED). Owner of record stays OPEN: **D-007** reworded to Shane / Hazel Green Trojan Youth Wrestling / partnership. Mats **42' × 42'** (**D-014** DECIDED). Design events home duals + AHSAA/regional tournaments (**D-029** DECIDED). New **D-030** OPEN (test-fit direction). Open count 16.
- `params/phase2.yaml` v2: meta (active, Shane's build, location site TBD, sheet date, drawn by), `spaces.arena.mat_size` 42 ft x 42 ft + `design_events`, `open_items.owner_of_record` and `program_fit`, `sheets.P2-G-003`, courts source → R-012. **Nothing school-derived was found in phase2.yaml to remove** (no school ownership, district approval, DCM/school review, school bidding or principal entries existed). Locked values (55,000 / 22,000 / 4 mats / 2,200 / 5 tags) unchanged.
- New `params/phase2_program.yaml` (test-fit factors + room list, all sourced), `phase2/src/p2_testfit.py` (arithmetic), `phase2/src/p2_g_003.py` (sheet). Output `phase2/out/pdf/P2-G-003_RevA.pdf` + `.dxf`, tabloid landscape, 1 page, 1224 × 792 pt, stamp present; previews `/workspace/keystone_previews/P2-G-003.{png,pdf}` (visually checked, no overlaps).
- **Result:** net program 64,568 SF + mechanical (5% of gross) → **≈ 86,100 GSF (base, gross-up 1.25)** vs 55,000 → **does not fit** (over ≈ 31,100). Lean check (telescopic seating 3.38 SF/seat, gross-up 1.15): ≈ 71,800 GSF, still over ≈ 16,800. The 5 tagged spaces alone gross to ≈ 52,000.
  - A) grow to ≈ 86,100 GSF (lean ≈ 71,800).
  - B) event floor 114 × 126 ft = 14,364 SF (4 × 42' mats 2×2, 10 ft around/between, 6 ft table strips ASSUMED; 84×50 court + 10 ft runout fits) → ≈ 75,800 GSF (lean ≈ 62,300): still over.
  - C) cutting seats alone cannot fit (0 seats → ≈ 61,200 GSF; lean ≈ 56,000). B + C: ≈ 360 seats (base) / ≈ 1,190 (lean).
- Research: **R-008** seating area + IBC 2021 assembly aisles (note: 2021 IBC numbers assembly as §1030, 1029 in 2018), **R-009** occupant load + IBC Table 2902.1 fixtures (18 WC men, 33 WC women, 7 + 9 lavs, 3 DF, 1 service sink at load 2,640), **R-012** NFHS basketball court (partial), **R-014** planning factors (Loudoun 2014, Groton, MIL-HDBK-1027/4A).
- **Code edition flag:** Madison County's page lists the **2018** IBC/IPC; Shane said 2021. Fixture ratios identical in both. AHJ OPEN (D-008).
- README, BACKLOG (priority note; P2-T-003b first Phase 2 ticket; P2-T-003 done), ASSETS updated.

## 2026-10-03 ~11:25 PM CT · D-031 footprint cap · P2-T-003b two-level test-fit (P2-G-003 Rev B)
- Shane, firsthand (11:09 PM CT): 55,000 SF is a **FOOTPRINT cap that could allow two levels**, not a total floor area cap. Logged as **D-031 DECIDED**. Open count unchanged at 16.
- `params/phase2.yaml` v3:
  - `building.footprint_cap_sf: 55000`, `levels: up to 2`, `stories: up to 2 (D-031)`, `total_gsf_cap: none`. Locked `total_sf: 55000` is kept, with its meaning noted (it is the footprint cap).
  - `open_items.program_fit` reworded.
  - `sheets.P2-G-003`: Rev A `frozen: true`; Rev B added (`frozen: false`).
- `params/phase2_program.yaml`: the Rev A sections are unchanged. New sections `meta_rev_b`, `stacking` (L1/L2 room lists with why + source), `seat_split` (50/50 ASSUMED; best of 30-70%) and `vertical_circulation` (IBC/ADA rules plus ASSUMED 15 ft floor-to-floor and 64 SF hoistway).
- `phase2/src/p2_testfit.py`: new two-level functions `compute_two_level`, `best_split`, `exits_required`, `stair_sf`, `max_seats_two_level`, `max_floor_two_level`, `summary_b` (print with `--rev-b`). Footprint = max(L1 gross, arena volume gross + L2 gross).
- `phase2/src/p2_g_003.py`: `--rev A|B` (default B). The frozen `build()` is untouched; new `build_b()`.
- **Rev A frozen check:** regenerated to /tmp after all changes. PDF byte-identical (sha256 6d5bee82…3d92d). DXF entity-identical; only header timestamps and GUIDs differ (ezdxf).
- **Rev B result (full program: 22,000 SF floor, 2,200 seats):**
  - **Base:** ground footprint ≈ 62,700 at the 50/50 split, ≈ 62,300 at the best split (55% upper). Over 55,000 by ≈ 7,300. Total ≈ 88,900 GSF.
  - **Lean:** ≈ 53,500 at 50/50 and ≈ 51,600 at 65% upper. **Fits.** Total ≈ 74,700 GSF.
  - **Option B floor (14,364 SF):** base ≈ 52,200 footprint and ≈ 78,200 GSF (fits with all 2,200 seats); lean ≈ 42,600–44,000.
  - **Smallest change for base:** use the option B floor. Alternatives: keep 22,000 SF and cut to ≈ 1,370 seats, or any floor of ≈ 16,400 SF or less with all seats.
- **Stacking:**
  - L1: event floor + lower tier (double-height arena volume, nothing above), boys/girls lockers, 4 event lockers, foyer, lower concourse, L1 restrooms (41 fixtures), concession, first aid, mat storage, equipment room, mechanical.
  - L2: upper tier, S&C, cross-training (DR4 flips: the daily mat is the mezzanine), admin, upper concourse + hall of champions wall, L2 restrooms (29 fixtures).
  - The upper tier and L2 rooms sit over the L1 ring around the bowl.
- **Vertical circulation (base 50/50):**
  - L2 load 1,304 → 4 exits (T1006.3.3), 0.2 in/occupant (1005.3.1 exception; sprinklers 903.2.1.4 + voice alarm 907.2.1.1) → 4 stairs × 65 in.
  - About 206 SF per stair per level (26 risers of 6.92 in, 11 in treads, 2 flights, 48 in landings).
  - Elevator 1 (IBC 1104.4; ADA car 80 × 54 in; 64 SF hoistway ASSUMED).
  - About 890 net SF on each level.
- New research **R-015** (two-level stacking + vertical circulation; IBC 2021 ch. 9/10/11 via UpCodes, 2010 ADA Standards, Reed and Orleans arena guides as precedent).
- New sheet `phase2/out/pdf/P2-G-003_RevB.pdf` + `.dxf`: 1 page, 1224 × 792 pt, stamp present, reproducible.
- Previews:
  - `/workspace/keystone_previews/P2-G-003.png` = Rev B.
  - `P2-G-003_RevA.png` = the old Rev A preview.
  - `P2-G-003.pdf` = Rev B.
- **D-030** reworded (still OPEN): pick option B floor / cut seats / lean inputs / mix.
- BACKLOG, ASSETS and STATUS updated.

## 2026-10-03 ~11:35 PM CT · D-032 · P2-T-003b suites study (P2-G-003 Rev C)
- Shane, firsthand (11:26 PM CT): rejects the ≈ 1,370-seat option ("not enough") → **D-032 DECIDED**. His direction: keep ≈ 2,200 total spectators by adding rentable **suites just above the top seats**. Recorded under **D-030**, which stays **OPEN** until he picks. Open count unchanged at 16.
- `params/phase2.yaml` v4:
  - `spaces.seating.rejected_option` and `suites_direction`.
  - `open_items.program_fit` reworded.
  - `sheets.P2-G-003`: Rev B `frozen: true`; Rev C added.
  - Locked values unchanged.
- `params/phase2_program.yaml`: Rev A/B sections unchanged. New `meta_rev_c` and `suites`:
  - guests 12/16/20, 25 SF/guest, ASSUMED width rule, 44 in corridor;
  - code load = seats + lounge ÷ 15;
  - placements L2_back / L3_top, 3rd-level flags, floors checked, headline case.
- `phase2/src/p2_testfit.py`: new `suite_module`, `compute_suites` (footprint = max(L1, AV+L2, AV+L3)), `best_suites`, `max_bowl_with_suites`, `max_spectators_with_suites`, `largest_floor_with_suites`, `summary_c` (`--rev-c`). Rev B's `compute_two_level` is untouched.
- `phase2/src/p2_g_003.py`: `--rev A|B|C` (default C), new `build_c()`; `build()` and `build_b()` untouched.
- **Frozen checks:** regenerated A, B and C to /tmp. PDFs byte-identical (A sha256 6d5bee82…, B d16b2dbe…). DXFs entity-identical (227 / 294 entities); only headers differ (ezdxf).
- **Rev C result (base inputs):**
  - **22,000 SF floor:** suites cannot reach 2,200 inside 55,000 at 12, 16 or 20 guests, with suites on L2 or L3. The most that fits is ≈ 1,640 (1,180 bowl + 23 × 20; footprint 54,986; ≈ 96,800 GSF; 3 levels).
  - **Suites on L2** (back of the upper tier) never fit: L2 is already about the size of the L1 ring.
  - **Largest floor that reaches 2,200 with suites:** ≈ 20,200–20,300 SF.
  - **20,000 SF floor:** 1,610 bowl + 50×12 / 37×16 / 30×20 suites; ≈ 105,300–105,800 GSF; 510–550 ft of suite front.
  - **18,000 SF floor (headline):** 1,940 bowl + 13 × 20 = 2,200 (or 17×16 = 2,212, 22×12 = 2,204). Footprint ≈ 54,994 vs 55,000 (no margin). ≈ 92,300–92,900 GSF. 3 levels (L3 suite level ≈ 11,300 GSF, over the L1 ring). Suite SF 6,500 + 810 corridor. 221–242 ft of suite front.
  - **16,400 SF floor:** 2,200 bowl, no suites, 2 levels (≈ 80,900 GSF).
  - **Lean inputs, 22,000 SF:** no suites needed (≈ 74,700 GSF).
- **Headline fixtures and egress:**
  - Fixtures: L1 30 / L2 30 / L3 16 = 76 (Rev B: 70).
  - Stairs: 4 × 68 in on all 3 levels (L2 load 1,368, L3 code load 598). Stairs must be enclosed, 1-hour (1019.3, 1023.2). Elevator to L3 (1104.4).
  - Wheelchair spaces: 16 in the bowl + 1 in each suite (1109.2.2).
- New research **R-016**: suites in small arenas. Precedents: Diddle/WKU, Texas Tech, Pitt Petersen, Sheldon ISD. Code: IBC 1004.6/T1004.5, 1109.2.2, ADA 221.2. No $ figures (revenue out of scope).
- New sheet `phase2/out/{pdf,dxf}/P2-G-003_RevC`: 1 page, 1224 × 792 pt, stamp present, reproducible.
- Previews:
  - `/workspace/keystone_previews/P2-G-003.png` = Rev C.
  - `P2-G-003_RevB.png` kept.
  - `P2-G-003.pdf` = Rev C.
- BACKLOG, ASSETS and STATUS updated.

## 2026-10-03 ~11:50 PM CT · D-030 DECIDED · locked program (P2-G-003 Rev D) · P2-T-004 block plans (P2-A-101/102 Rev A)
- **D-030 DECIDED** — 16,400 SF event floor, all 2,200 seats in the bowl, 2 levels, no suites — "Shane, firsthand, 11:39 PM CT". Open decisions 16 → 15.
- Suites → PARKING_LOT ("future add-on, study after attendance is proven"). Seating type stays OPEN (D-009); D-009 notes updated.
- `params/phase2.yaml` v5 (locked, change only on CHANGE APPROVED):
  - `spaces.arena.event_floor_sf: 16400`, `event_floor_dims` 114 ft E-W × 144 ft N-S = 16,416 SF drawn, with basis (NFHS 2-1-5, 2-3 from R-005; court from R-012).
  - `spaces.arena.sf: 22000` renamed `sf_tagged_superseded: 22000` + history note (frozen Revs A-C read it; their PDFs regenerate byte-identical).
  - `mat_ft: 42`, `mat_layout` 2 × 2; `seating.bowl: 2200` (+ suites PARKED, `type_note` D-009); `building.levels: 2`; S&C + cross-training `level: 2`.
  - `open_items.program_fit` DECIDED; `sheets.P2-G-003` Rev C frozen, Rev D added; new `sheets.P2-A-101`, `P2-A-102` (Rev A).
- `shared/validate.py`: locked checks added for event_floor_sf 16400, sf_tagged_superseded 22000, mat_ft 42, seating.bowl 2200, levels 2, S&C + cross-training level 2.
- **Floor check:** E-W 2 × 42 + 3 × 10 clear = 114 ft; N-S 114 + two 15 ft table/bench zones (depth ASSUMED) = 144 ft. Holds the Rev A 114 × 126 = 14,364 SF layout and an 84 × 50 court + 10 ft runout (104 × 70).
- `params/phase2_program.yaml`: new `meta_rev_d`, `locked_program` (50/50 tiers, FIXED vs TELESCOPIC columns, same 1.25 gross-up, wheelchair table). Earlier sections unchanged.
- `phase2/src/p2_testfit.py`: new `wheelchair_spaces`, `compute_locked` (Rev B method at the locked floor + bowl), `summary_d` (`--rev-d`). Frozen functions read `ARENA_TAG`.
- `phase2/src/p2_g_003.py`: `--rev A|B|C|D` (default D), new `build_d()`; `build()`, `build_b()`, `build_c()` untouched.
- **Frozen checks:** Revs A, B, C regenerated to /tmp after the key rename: PDFs byte-identical, DXFs entity-identical (227 / 294 / 320).
- **P2-G-003 Rev D (LOCKED PROGRAM)**, base = FIXED 6.0 SF/seat, alt = TELESCOPIC 3.38 SF/seat:
  - L1 gross 54,949 / 50,868; L2 gross 25,981 / 22,380; arena volume 28,750 / 25,149.
  - Footprint 54,949 / 50,868 vs 55,000: both FIT (fixed margin 51 SF; the drawn 16,416 floor gives ≈ 54,971).
  - Total 80,930 / 73,248 GSF.
  - Fixtures: L1 37 (WC 10 M / 18 W, lav 4 / 5), L2 29 (WC 8 / 14, lav 3 / 4) = 66; 4 drinking fountains; same both columns.
  - 4 stairs × 65 in (L2 load 1,304), ≈ 206 SF each per level + 1 elevator (64 SF hoistway) = 890 SF per level.
  - Wheelchair spaces 18 (T1109.2.2.1), dispersed.
- **New `params/phase2_plan.yaml`** + **`phase2/src/p2_a_plan.py`** → `phase2/out/{pdf,dxf}/P2-A-101_RevA` (Level 1), `P2-A-102_RevA` (Level 2):
  - Schematic block plans at 1/32 in = 1 ft-0 in (1/16 does not fit) on tabloid; building 250 × 220 ft = 55,000 SF footprint.
  - Floor with 4 mats + court overlay; fixed tiers solid, telescopic depth dashed (9.5 ft lower, 8.5 ft upper vs 16.5 / 15 fixed).
  - 4 stairs + elevator at the same coordinates on both levels; room tags with drawn SF; room schedules vs program.
  - Level 2: S&C + cross-training over the lockers, restrooms + admin stacked, open to the lobby and arena below. Drawn L2 ≈ 27,570 SF vs 25,981 program.
- Previews: `P2-G-003.png/.pdf` = Rev D, `P2-G-003_RevC.png` kept, `P2-A-101.png/.pdf`, `P2-A-102.png/.pdf`.
- DECISIONS, PARKING_LOT, BACKLOG (P2-T-003b done, P2-T-004 in progress, P2-T-005 → A-103), ASSETS, STATUS updated.

## 2026-10-04 ~4:40 AM CT · D-009 DECIDED (MIX seating) · P2-G-003 Rev E · P2-A-101/102 Rev B
- **Shane review (4:30 AM CT):** P2-A-101/102 Rev A "good first block plan". Rev A of both sheets FROZEN (regenerate byte-identical with `--rev A`); previews kept as `P2-A-101_RevA.png`, `P2-A-102_RevA.png`.
- **D-009 DECIDED** — MIX: telescopic lower tier, fixed upper tier — "Shane, firsthand, 4:30 AM CT". Open decisions 15 → 14.
- `params/phase2.yaml` v6: `spaces.seating.type` MIX (LOCKED), new `lower_tier_type: telescopic`, `upper_tier_type: fixed`, `seats_per_tier`, `sides` (N, S, E); `entry.location_block_plan` (south-center, road assumed south, site TBD); `support_rooms.mechanical.location_block_plan` (NW / N / E, off the west public side); `open_items.seating_type` DECIDED; sheets: P2-G-003 Rev D frozen + Rev E, P2-A-101/102 Rev A frozen + Rev B.
- `shared/validate.py`: locks `seating.lower_tier_type == telescopic`, `upper_tier_type == fixed` (D-009).
- `params/phase2_program.yaml`: `meta_rev_e`, `mixed_seating` (target margin 2,000 SF). Earlier sections unchanged.
- `phase2/src/p2_testfit.py`: `compute_mix`, `largest_remainder`, `seats_by_side`, `summary_e` (`--rev-e`). `p2_g_003.py`: `build_e`, `--rev` default E; Revs A–D untouched.
- **P2-G-003 Rev E (MIX):** lower 1,100 telescopic at 3.38 SF/seat, upper 1,100 fixed at 6.0 SF/seat, same 1.25 gross-up. L1 net 37,032 → gross 51,108; L2 net 20,785 → gross 25,981; arena volume 25,149; footprint = max(L1, arena volume + L2) = **51,130 → margin 3,870 SF under 55,000 (target ≥ 2,000 met)**; mech 3,854; **total 77,089 GSF** (all-fixed Rev D: 54,949 / margin 51 / 80,930). Fixtures 66, 4 stairs × 65 in + elevator, 18 wheelchair spaces (unchanged).
- **Seats by side / tier (sheet table, sum 2,200):** N 353 telescopic + 308 fixed = 661; S 341 + 308 = 649; E 406 + 484 = 890; lower 1,100 + upper 1,100. Split per tier by largest remainder in proportion to drawn capacity (lower 1,306, upper 1,125).
- **New `params/phase2_plan_rev_b.yaml`** (Rev A geometry in `phase2_plan.yaml` frozen) + `p2_a_plan.py` `build_b` (`--rev A|B`, default B; room-overlap check fails the build):
  - Box shrinks 250 × 220 → **204 × 252 ft = 51,408 SF** (3,592 under the cap; 278 over the program footprint). Floor 114 × 144 on the arena N-S axis (x = 113 ft).
  - Entry south-center on the axis: vestibule + lobby / hall of champions (double height) under the south tier, 12 ft portal straight to the floor. Men (W of lobby) and women (E) flank it; concession and first aid in the lobby zone.
  - Mech/elec moved off the west side: NW corner (tag 3), N ring (15), E ring behind the bowl (16); old SE mech gone. West = boys + girls lockers + athlete corridor only; team/service entry at the SW.
  - Event lockers N (2) + E (2) via vomitories V1 (N) and V2 (E); equipment storage/room N; 4 stairs + elevator aligned L1/L2.
  - Level 2: S&C + cross-training over the lockers, men/women L2 stacked over L1, admin over the team entry, balcony / upper concourse across the lobby (hall of champions wall), lobby open to below centered south, upper tier N/S/E with rear walkways.
  - Layout fix: plan title moved to the right panel, scale bar beside the building, axis note at the entry arrow (252 ft box fills the sheet height at 1/32 in).
- **Frozen checks:** P2-G-003 Revs A–D and P2-A-101/102 Rev A regenerated to /tmp: PDFs byte-identical; DXFs entity-identical (227 / 294 / 320 / 361; 714 / 598).
- Previews: `P2-G-003.png/.pdf` = Rev E (`P2-G-003_RevD.png` kept); `P2-A-101.png/.pdf`, `P2-A-102.png/.pdf` = Rev B.
- DECISIONS, BACKLOG, ASSETS, STATUS updated.

## 2026-10-04 ~4:50 AM CT · D-033 DECIDED (single controlled entry) · D-034 OPEN · P2-A-101/102 Rev C
- **D-033 DECIDED** — single controlled entry point for all people (public, teams, staff): "Everyone passes through the grand entrance; it will serve as a checkpoint, a security feature." — "Shane, firsthand, 4:43 AM CT".
- **D-034 OPEN** — how deliveries and team buses work under the single-entry rule (no sizes set). Open decisions 14 → 15.
- P2-A-101/102 **Rev B FROZEN** (regenerate byte-identical with `--rev B`; previews kept as `P2-A-101_RevB.png`, `P2-A-102_RevB.png`).
- `params/phase2.yaml` v7: `spaces.entry.access_control` (rule, quote, checkpoint, team route, perimeter exits, service door; sources D-033, R-015, IBC 2021 Ch. 10); `open_items.access_control` DECIDED, `deliveries_buses` OPEN; sheets P2-A-101/102 Rev B frozen + Rev C.
- **New `params/phase2_plan_rev_c.yaml`** (Rev B geometry frozen in `phase2_plan_rev_b.yaml`) + `p2_a_plan.py` `build_c` (`--rev A|B|C`, default C; Rev C seat counts are checked against P2-G-003 Rev E):
  - SW team / service entry removed. Freed SW area: TEAM ASSEMBLY / HOLDING ≈ 2,072 SF + STORAGE (SW) 1,011 SF (tag 23), both unprogrammed, ASSUMED.
  - SECURITY CHECKPOINT — size TBD (ASSUMED): dashed zone between the vestibule and lobby, location only.
  - CD-1 controlled door off the lobby → 8 ft ATHLETE ROUTE along the back of the south tier → team assembly → athlete corridor / lockers; walls separate it from the west concourse (which loses its north 8 ft).
  - Perimeter doors (symbols, widths not drawn): E1 main entry / main exit; X1-X10 EXIT ONLY — alarmed, no exterior entry hardware (team assembly W, girls + boys lockers W, ST-1..ST-4 discharges, exit passages N + E, east concourse); S1 SERVICE / LOADING at equipment storage (staff-controlled, not a people entrance; D-034 OPEN).
  - New exit passages N + E (8 ft = vomitory width, ASSUMED) from V1 / V2 to the north and east walls so the north and east tiers reach perimeter exits (T1006.3.3, 1030.3). V1 moved 3.85 ft east, V2 3.91 ft south (same widths, seat counts unchanged). Event locker 2 shifted east, event locker 4 shifted south (900 SF each kept); Mech N 588, Mech E 1,720, new Mech (NE) 327 (tag 22) → mech drawn 3,804 vs 3,854 program.
  - Sheet blocks: ACCESS CONTROL + EGRESS (both levels) with the IBC citations; legend adds exit / service / checkpoint symbols.
- **Code basis (new R-015.6, IBC 2021 Alabama via UpCodes, retrieved 2026-10-04):** 1010.2 (egress side openable without a key; 2018 1010.1.9), 1010.2.9 (panic hardware only, Group A ≥ 50; 2018 1010.1.10), 1010.2.7 exc. 1 (stair discharge doors lock from outside only), 1010.2.13 (no delayed egress in Group A → alarm only), T1006.3.3 (4 exits per story > 1,000), 1030.2 (main exit ≥ 1/2 occupant load, fronts a street), 1030.3 (other exits ≥ 1/2), 1005.3.2 exc. 1 (0.15 in/occupant; seats alone → E1 ≥ 165 in clear), 1003.6 / 1010.5 (checkpoint may not narrow the egress width), T1004.5 + T1006.2.1 (locker rooms need 2 exits).
- **P2-G-003:** program numbers unchanged → Rev E stands (regenerates byte-identical); no Rev F. Box 204 × 252 = 51,408 SF, 3,592 SF under 55,000; program footprint 51,130 (margin 3,870); 77,089 GSF; seats N 661 / S 649 / E 890 = 2,200.
- **Frozen checks:** P2-A-101/102 Revs A + B and P2-G-003 Rev E regenerated to /tmp: PDFs byte-identical, DXFs entity-identical (714 / 598; 677 / 472; 292).
- Previews: `P2-A-101.png/.pdf`, `P2-A-102.png/.pdf` = Rev C.
- DECISIONS, BACKLOG, ASSETS, STATUS updated.

## 2026-10-04 ~5:10 AM CT · D-035 DECIDED (Level 2 running / training loop) · P2-G-003 Rev F · P2-A-101/102 Rev D
- **Shane, firsthand, 4:55 AM CT:** complete continuous walkway / running-training loop around the top of Level 2, joining REAR WALKWAY (N), WALKWAY (E) and UPPER CONCOURSE / HALL OF CHAMPIONS BALCONY (S); S&C (17) and cross-training (18) may be cut. He wrote "eastside"; those rooms are on the west, so the missing leg is the west one, along their arena-side edge. Logged **D-035 DECIDED**. Open decisions stay 15.
- **params/phase2.yaml v8** (Shane's approval = CHANGE APPROVED): S&C `sf` 5,224 (was 6,000), cross-training `sf` 3,500 (was 4,000), old values kept as `sf_tagged_superseded`; new `spaces.training_loop` (2 lanes x 42 in = 7 ft, squared corners, 706 ft centerline, 7.48 laps/mile, guards, event-day use). Sheets: P2-G-003 Rev E frozen + Rev F; P2-A-101/102 Rev C frozen + Rev D. `phase2_program.yaml`: room tag_paths read `sf_tagged_superseded` so frozen revisions keep 6,000 / 4,000; new `meta_rev_f` + `training_loop` method. `validate.py` PHASE2_LOCKED updated.
- **New `params/phase2_plan_rev_d.yaml`** + `p2_a_plan.py` `build_d` (`--rev A|B|C|D`, default D; seats checked against P2-G-003 Rev E; loop checked against stairs / elevator / rooms):
  - Loop outer [49, 34, 204, 246], inner [56, 41, 197, 239] (= upper-tier backs + arena edge); 4,942 SF; lane line dashed; leg labels; event-day crossing arrows at mid-side tier entries (ASSUMED locations); 42 in guards on the west edge over the arena and the south edge over the lobby.
  - S&C 49 x 110.8 less ST-1 = 5,224 SF; cross-training 49 x 71.43 = 3,500 SF; L2 corridor [0, 18.8, 49, 69.77]; balcony / walkways replaced by the loop; 6 ft STRETCH / WARM-UP STRIP (N) left over (ASSUMED).
  - ST-1 3.55 ft west (L1 Mech NW 1,070, X4 at x 43.6); ST-2 5 ft north into a new 19 x 5 ft NE stair tower (+95 SF; L1 Mech NE 422, X6 at y 251.6); elevator 1 ft south (opens onto the loop). Building 51,503 SF, 3,497 under 55,000. Seats unchanged (N 661 / S 649 / E 890 = 2,200).
- **P2-G-003 Rev F** (`p2_testfit.compute_loop` / `summary_f`, `p2_g_003.py build_f`, default F): Rev E method with the new S&C / XT SF (loads, stairs 64.0 in, fixtures recomputed); the loop replaces the upper concourse line (1,375) and is added to L2 gross as drawn, **not grossed up** (ASSUMED; it is circulation). L1 51,194; L2 27,590; footprint 52,738 (arena volume + L2), **margin 2,262** (≥ 2,000 target met); **78,784 GSF**. Grossed-up alternative shown: 53,974 / margin 1,026 (misses). Flag: program footprint is 1,235 SF more than the drawn building, so the gross-up allowance no longer fully fits inside it.
- **Research:** new `research/R-017-indoor-running-track-and-guards.md` (UFC 4-740-02N 4.1.7, Athletic Business x 2, IBC 2021 1015.2-1015.4 / 1030.17; retrieved 2026-10-04).
- **Frozen checks:** P2-G-003 Revs A-E and P2-A-101/102 Revs A-C regenerated to /tmp: PDFs byte-identical, DXFs entity-identical (227 / 294 / 320 / 361 / 292; 714 / 677 / 786; 598 / 472 / 482).
- Previews: `P2-G-003.png/.pdf` = Rev F (`P2-G-003_RevE.png` kept); `P2-A-101.png/.pdf`, `P2-A-102.png/.pdf` = Rev D (`_RevC.png` kept).
- DECISIONS, BACKLOG, ASSETS, STATUS updated.

## 2026-10-04 ~5:45 AM CT · D-036 approval + Phase 2 Schematic Set Rev A freeze · R-018 egress · P2-A-201 Rev A
- **Shane, firsthand, 5:27 AM CT:** "P2-A-101/102 Rev D + P2-G-003 Rev F approved. Entry south-center, mech off the public side, mixed seating, 2,262 margin — all good." Logged **D-036** DECIDED, **D-037** DECIDED (loop 2 x 42 in = 7 ft for now), **D-038** OPEN (upper concourse width vs egress; 3 lanes / 10.5 ft if code requires), **D-039** DECIDED (west unprogrammed space kept as-is, labeled FLEX), **D-040** OPEN (brand / HGHS badge on the portal). Open decisions 15 → 17.
- **FLEX relabel = label-only re-issue of P2-A-101 Rev D before the freeze** (D-039; Shane's message left the template bracket, KEYSTONE used the stated default KEEP AS-IS): `params/phase2_plan_rev_d.yaml` team assembly → "FLEX / TEAM ASSEMBLY", storage SW → "FLEX / STORAGE"; area-check line in `p2_a_plan.py build_d`. DXF 791 entities before and after, every non-text entity identical, only text strings changed; areas unchanged (≈ 2,072 / 1,011 SF). Revision letter kept (Rev D) because nothing but labels changed. P2-A-102 Rev D and P2-G-003 Rev F untouched (byte-identical).
- **Freeze — Phase 2 Schematic Set Rev A** (`params/phase2.yaml` v9: P2-G-003 Rev F, P2-A-101 Rev D, P2-A-102 Rev D `frozen: true` + `approved`; new `sets.phase2_schematic_set_rev_a`): new `phase2/src/p2_set.py` writes one 3-page 17 x 11 in PDF `phase2/out/pdf/Phase2_Schematic_Set_RevA.pdf` (G-003 F, A-101 D, A-102 D) with matplotlib PdfPages from the same builders; copied to `/workspace/keystone_previews/`. `pdfunite` was rejected because it writes a random /ID (not reproducible). `--out-dir` rebuild is byte-identical; pages pixel-identical to the single-sheet PDFs; stamp on every page. Frozen guard like the sheet generators. Generators' docstrings mark the revisions FROZEN. Git tag `p2-schematic-revA` on the freeze commit (tags are not branches; README limits branches only).
- **shared/titleblock.py**: `text(..., color=)` (stored only when used), new `poly()` primitive (PDF filled polygon; DXF solid HATCH with true color + outline), `render_pdf` split into `figure()` + save (for the bundle). Frozen checks after the change: all P1 sheets, P2-G-003 Revs A-F and P2-A-101/102 Revs A-D regenerate with entity-identical DXFs and byte-identical PDFs, except **P1-G-001 Rev A internal PDF**, which differs in bytes only (text and pixels identical) and also differs with the old titleblock.py, so it is pre-existing drift, not caused by this change; the committed file was left as is.
- **Research:** new `research/R-018-level-2-egress-assembly.md` (IBC 2021 Ch. 10 via UpCodes, retrieved 2026-10-04; 2018 1029.x from secondary excerpts, UNVERIFIED; NFPA 101 / ICC 300 paywalled): L2 load 1,279 (1,100 seats + S&C 105 + cross-training 70 + admin 4); stairs 255.8 in = 4 x 64 in (zero slack); loop 64 in balanced / 79.2 in unbalanced vs 84 in → code does not require > 7 ft; 10.5 ft satisfies; travel ≤ ≈ 144 ft vs 250 ft; guards 42 in; event-day cross-flow rules. New `research/R-019-arena-clear-height.md` (≥ 25 ft clear over the court: Draper reprint of NFHS specs, LA Rec & Parks standard; wrestling practice rooms 9-10 ft, NFHS).
- **P2-A-201 Exterior Elevations Rev A** (P2-T-009; new `params/phase2_elev.yaml`, new `phase2/src/p2_a_201.py`): south elevation at 1/16 in = 1 ft-0 in with the south portal (limestone arch 44 ft wide x 50 ft high, 28 ft opening, springline 26 ft, crown 40 ft, crimson inside the arch, gold soffit / intrados, entry glazing, "BRAND / SIGNAGE — TBD" in brand red / black, no school logo, D-040); north, east and west at 1/32 in. Heights: L2 FF 15 ft (ASSUMED, R-015), ring roof 30 ft (ASSUMED), arena clear ≥ 25 ft (CITED, R-019), underside of arena structure 36 ft and roof 42 ft (ASSUMED), parapet TBD. Portal proportions from Shane's MOVIE MAKER arch render; sizes ASSUMED. Other materials TBD. Color elevations; stamp present.
- Previews: `P2-A-201.png/.pdf`, `Phase2_Schematic_Set_RevA.pdf`; `P2-A-101.png/.pdf` = Rev D with FLEX labels.
- DECISIONS, BACKLOG, ASSETS, STATUS updated.

## 2026-10-04 ~6:30 AM CT · D-041 official mark · D-043 freestanding portal + Champion Walk · P2-A-201 Rev B
- **Shane, firsthand, 6:16 AM CT:** "OFFICIAL MARK — circular horse-head badge with Greek key border." Logged **D-041** DECIDED (supersedes logo Concepts 01 / 02, kept as history, nothing deleted; the concept files are not in the repo or on the box), **D-040 closed** (the portal carries the Trojan Horse Arena mark, not the HGHS badge), **D-042** OPEN (trademark search before signage / apparel).
- **Brand files:** new `brand/THA_logo_black.svg` / `_red.svg` / `_white.svg` = Shane's 3 SVG attachments, identified by fill (#1A1A1A / #CC0000 / #FFFFFF); identical geometry (one even-odd path, viewBox 1373 x 1379); sha256 in ASSETS. His JPG (black mark on a transparency checker) and the PNGs on his PC were not committed.
- **Shane, firsthand, 6:22 AM CT:** the Grand Entrance Portal is **FREESTANDING**, just before the south entrance, straddling the brick **Champion Walk** (engraved donor / sponsor bricks). Logged **D-043** DECIDED (next A-101 revision adds the portal + walk; Rev D stays frozen) and **D-044** OPEN (walk length / width, donor-brick program). New `references/portal_freestanding_champion_walk_ref.png` (his reference photo, sha256 in ASSETS). phase2.yaml v10 (`brand.official_mark`) + v11 (`approach`).
- **P2-A-201 Rev A frozen** (regenerates byte-identical PDF, entity-identical DXF; `phase2_elev.yaml` unchanged). **Rev B** (`p2_a_201.py --rev B`, default; new overlay `params/phase2_elev_rev_b.yaml`):
  - Official mark (black) Ø 6 ft centred above the arch (40.4-46.4 ft, replaces the keystone) + "TROJAN HORSE ARENA" wordmark in brand red, 18 in caps, 26.1 ft long on the 44 ft attic (layout guard stops it overflowing the portal); side panel "HAZEL GREEN REGIONAL / ATHLETIC COMPLEX" (black, red stripe, white letters) on the west ring wall, 46 x 7.5 ft. All sizes ASSUMED.
  - Portal freestanding: open arch (no glazing in the portal); the building's E1 entry glazing (18 x 16 ft ASSUMED) shows behind it; crimson soffit band with a thin gold edge (split TBD); title "GRAND ENTRANCE PORTAL (FREESTANDING) — stands ≈ 30' south of the entrance (gap ASSUMED)"; Champion Walk brick strip at grade + "Engraved donor / sponsor bricks".
  - Key plan (north up, 1 in = 60 ft): building south wall + E1, 30 ft gap (ASSUMED, dimensioned), 2 piers (depth 6 ft ASSUMED), brick walk 28 ft wide (= arch opening, ASSUMED), length TBD.
  - Brand detail at 3/32 in = 1 ft-0 in (portal attic) so the mark and wordmark read at print size. Brick added to the finishes legend; notes updated (D-041 to D-044).
- **shared/titleblock.py:** new `mark()` primitive + `load_svg_mark()`: one-path SVG (M/L/C/Z) drawn as a **vector** path in the PDF (sub-paths re-oriented by nesting depth so the PDF non-zero fill matches the SVG even-odd; no raster: `pdfimages` lists 0 images); DXF block `THA_MARK` (solid HATCH, true colour + outline polylines) inserted twice (scale 0.375 / 0.5625 in). svglib / cairosvg not installed and not needed. Frozen checks re-run after the change (all P1 sheets, P2-G-003 A-F, P2-A-101/102 A-D, the set bundle and P2-A-201 Rev A).
- Previews: `P2-A-201.png/.pdf` = Rev B; `P2-A-201_RevA.png` kept.
- DECISIONS, ASSETS, BACKLOG, STATUS updated.

## 2026-10-04 ~7:00 AM CT · P2-A-201 Rev B frozen · Rev C (11 ft badge) · D-034 / D-038 / D-044..D-048 · P2-A-301 Rev A sections
- **Shane, firsthand, 6:45 AM CT:** "P2-A-201 Rev B APPROVED with changes for Rev C." **Rev B frozen** (`phase2.yaml` v12: `frozen: true`; regenerates byte-identical PDF / entity-identical DXF; preview `P2-A-201_RevB.png` kept).
- **Decisions:** **D-045** DECIDED arch underside crimson + gold trim (as drawn). **D-046** DECIDED Champion Walk 28 x 30 ft (portal to doors) "for now", 840 SF; tiers 4x8 single name / 8x8 family-business; ≈ 3,700 4x8 bricks (840 ÷ 0.222 = 3,780 gross, less border / joints); option to extend to parking later. **D-044** stays OPEN, narrowed to pricing. **D-047** DECIDED badge 11 ft. **D-048** OPEN arch photo rights. **D-038 CLOSED** stairs 70 in clear. **D-034 DECIDED** (default): service / deliveries at north door S1; bus drop loop on the south, offset east or west of the portal view. Open decisions 18 → **17**.
- **P2-A-201 Rev C** (`p2_a_201.py --rev C`, default; new overlay `params/phase2_elev_rev_c.yaml`; Rev B output untouched because every Rev C behaviour is keyed on overlay fields Rev B lacks):
  - Badge Ø 11 ft (was 6), centre 45.9 ft → 40.4-51.4 ft. Wordmark caps 27 in (was 18 in), 39.1 ft long: proportional scaling (2.75 ft caps) gives a 47.9 ft line, wider than the 44 ft portal, so caps are held at 27 in. The badge + wordmark do not fit under 50 ft, so the **portal / attic was raised 50 → 56 ft (ASSUMED; attic band 42-56 ft)**; width 44, opening 28, springline 26, crown 40 unchanged.
  - South elevation moved down 0.45 in on the sheet; brand detail re-fit (attic 40-56 ft at 3/32 in = 1 ft); callouts "CRIMSON underside (D-045)", "GOLD trim (D-045)"; title "30' in front of the E1 doors (D-046) · 56' h ASSUMED".
  - Key plan: Champion Walk 28 x 30 ft brick (portal at the walk's south end, 30 ft = gap, D-046), tiers + capacity note, dashed "extend to parking later", bus drop note (south loop offset E / W, D-034). Notes rewritten (portal, brand, walk).
- **Arch reference photo:** `git rm references/portal_freestanding_champion_walk_ref.png` (no history rewrite); box copy `/workspace/keystone_previews/refs/` (sha256 in ASSETS); ASSETS says "held off-repo pending rights confirmation from Shane".
- **params/phase2.yaml v12:** portal reference held off-repo (D-048), underside D-045, height 56 ASSUMED; `approach.champion_walk` 28 x 30, 840 SF, tiers, capacity, extension, pricing TBD; new `approach.site_access` (D-034) and `approach.egress_next_revision` (stairs 70 in, D-038); `brand.official_mark.portal_badge_dia_ft` 11 (D-047); new sheet entry **P2-A-301** Rev A.
- **R-018.8 addendum** (stairs 70 in): 4 x 70 = 280 in vs 255.8 base (+24.2), 275.6 loop counted (+4.4), 272.6 rail standing (+7.4), 292.4 both (12.4 short); one stair lost 210 ≥ 137.8; handrail projection 4.5 in (1014.8) — architect to confirm how "clear" is measured; stair plan ≈ 11.67 x 19 ft (+16.5 SF per stair per level) at the next A-101/A-102 revision. Frozen set unchanged.
- **P2-A-301 Rev A building sections** (new `params/phase2_sect.yaml`, new `phase2/src/p2_a_301.py`): (1) A-A N-S at x = 100 looking west and (2) B-B E-W at y = 150 looking north, 1/32 in = 1 ft; (3) north bowl edge enlarged, 3/32 in; (4) typical exit stair 70 in clear, 1/8 in; (5) key plan with the cuts; legend + notes.
  - Heights: L2 FF 15, ring roof 30, arena structure underside 36, arena roof 42 (all ASSUMED, phase2_elev.yaml); ≥ 25 ft clear CITED (R-019).
  - Lower tier telescopic 6 rows x 24 in (R-008 / plan), Hussey 11-5/8 in rise (CITED option, ASSUMED choice): top seat 6'-3 1/8", closed 3'-6" (Hussey tables). Upper tier fixed 15 ft band, 5 rows x 36 in, 14 in per row (2 x 7 in aisle risers) ASSUMED, stepping down from the loop (top cross aisle at 15 ft) to a 9.17 ft front row; L1 headroom under the tier front ≈ 9.2 ft less structure — TBD. Guards 42 in at the loop's open edges (1015), ≥ 26 in fascia at the tier front (1030.17.3). Sight lines NOT checked — TBD. Slab / roof thicknesses graphic only.
- **Frozen checks:** P1-G-001 A-D, P1-A-101 A, P2-G-003 A-F, P2-A-101/102 A-D, P2-A-201 A-B and Phase 2 Schematic Set Rev A regenerated to /tmp: PDFs byte-identical and DXFs entity-identical (P2-A-201 A / B: 879 / 1,028 entities); only the known pre-existing P1-G-001 Rev A internal PDF byte difference (text + pixels identical, predates this work).
- Previews: `P2-A-201.png/.pdf` = Rev C (`P2-A-201_RevB.png`, `_RevA.png` kept); `P2-A-301.png/.pdf`.
- DECISIONS, ASSETS, BACKLOG, STATUS updated.

## 2026-10-04 ~7:40 AM CT · D-048 closed · D-049..D-051 decided · D-052 / D-053 proposed · P2-A-201 Rev D · P2-A-301 Rev B · P2-A-302 Rev A

Shane, firsthand, 7:24 AM CT (+ PDF vendor cost sheet for the Champion Walk bricks).
- **D-048 CLOSED:** arch photo is Shane's own image (rights clear); removal stands, no history rewrite; ASSETS "Shane's own image; held off-repo by choice".
- **D-044 input:** vendor cost averages $19.17 (4x8) / $29.50 (8x8), logo +$6, engraving + shipping included; ~3,700 x $19.17 ≈ $70.9k if all 4x8 (excl. install / base). Donor pricing still OPEN. PDF kept box-only (sha256 in ASSETS).
- **D-049 DECIDED:** upper tier steps down from the L2 loop (as drawn); storage / mech / stack under the low front; lockers only at full height. Plan overlaps listed in DECISIONS; event lockers re-planned at the next A-101.
- **P2-A-201 Rev C FROZEN; Rev D (D-050):** portal 50 ft max (was 56 ASSUMED); arch crown 40 → 34 ft, springline 26 → 22.1 ft (proportional, ASSUMED), semi-elliptical (rise 11.9 ft); attic band 36-50; badge 11 ft at 34.4-45.4 ft; wordmark 27 in caps, baseline 46.1, caps top 48.35, under the 48.8-50 ft cornice. `p2_a_201.py`: generic `portal_override`, elliptical `arch_pts`, `callout_targets`, `notes_override.heights`.
- **P2-A-301 Rev A FROZEN; Rev B (D-051):** detail 4 intermediate landing 70 in (= stair width, IBC 2021 1011.6), floor landings 48 in; per stair 11.67 x 20.83 ft = 243.1 SF per level vs frozen 205.2 (+37.9; ≈ +303 GSF for 4 stairs x 2 levels at the next A-101/A-102). A-A / B-B / detail 3: under-tier storage / mech (D-049), lockers at full height; notes point to P2-A-302 (D-053) and R-018.9 (D-052).
- **P2-A-302 Rev A sight-line study (new) + R-020:** Green Guide C-values, seated 1.2 m / standing 1.6 m eyes, focal = near mat edge (N/S 25 ft, E 10 ft). As drawn: upper tier fails everywhere (N/S 40-49 mm seated, east negative); east lower 46-74 seated. Proposed: upper 19 in risers (front 9.17 → 7.08 ft) + east tier 6 ft further out → all seated ≥ 101, standing ≥ 72. Stack: closed recess under the front fits only with ≤ 32.6 in structure; open rows under the overhang conflict with 7'-6" → keep the stack at the tier face.
- **R-018.9 / D-052 (proposed):** worst case 292.4 in; 4 x 76 in = 304 (+11.6), +217.8 GSF vs 70 in; vs 74 / 78 in and a 5th stair (44 in: 324 in, +273.8 GSF + new core). Plans not redrawn.
- **params/phase2.yaml v13:** portal height / arch / badge / wordmark, photo wording, `champion_walk.vendor_cost`, `egress_next_revision_2`, `under_tier_use`, `sight_lines`; sheets A-201 Rev C frozen + Rev D, A-301 Rev A frozen + Rev B, new P2-A-302.
- Frozen checks re-run (adds P2-A-201 Rev C and P2-A-301 Rev A). DECISIONS (open 18), ASSETS, BACKLOG, STATUS updated.

## 2026-10-04 ~7:55 AM CT · D-053 + D-052 DECIDED · footprint margin · R-006 / R-007 · P2-C-101 Rev A site plan

- **Shane, firsthand, 7:44 AM CT — D-053 DECIDED:** upper-tier risers 19 in (front row 7.08 ft) AND east seats 6 ft further from the mats (+≈1,512 SF). Applies at the next A-101/A-102/A-301 revision; frozen sheets stay frozen.
- **Shane, firsthand, 7:49 AM CT — D-052 DECIDED:** 4 exit stairs at 76 in clear with intermediate handrails; worst case 304 in vs 292.4 in (≈ 11.6 in spare); ≈ 12.67 x 21.33 ft per stair per level. Applies at the next A-101/A-102/A-301 revision.
- **Footprint vs 55,000 SF cap (D-031)**, east shift + 76 in stairs: drawn basis (P2-A-101 Rev D 51,503 + 1,512 shift + 11.67 NE tower widening) **53,026.7 SF → 1,973.3 SF margin**; if all stair growth went outward 53,275.1 → 1,724.9; program basis (P2-G-003 Rev F method) **54,588.9 → 411.1 SF**. `phase2.yaml` `building.footprint_margin_next_revision`; `phase2_site.yaml` `footprint_check`.
- **R-006 (code edition + AHJ):** unincorporated Hazel Green → Madison County Inspection Department (2018 IBC / IFC / NFPA 101 adopted; State Fire Marshal enforces 2021 IFC → edition conflict to settle at pre-application); DCM (2021 IBC) only if the "schoolhouse" test applies; assembly occupancy needs an Alabama-registered architect. D-008 stays OPEN (site + pre-app).
- **R-007 (occupancy + occupant load):** Group A-4 main (arena with spectator seating); S&C / cross-training A-3 or accessory; offices B; storage S-1 (ASSUMED until G-002). Fixed seats counted by seat (IBC 2021 1004.6). Event floor 16,416 SF: 329 (50 gross) → 1,095 / 2,346 / 3,284 if used for unconcentrated / chairs / standing → **D-054 OPEN** (event floor uses).
- **P2-C-101 Rev A (new site sheet, campus diagram, SITE TBD):** building outline with the east shift and the 76 in stairs (frozen Rev D outline dashed), freestanding portal 30 ft south of E1 over the 28 x 30 ft brick Champion Walk, south bus drop loop offset east (west mirror allowed), service drive + apron to north door S1, assumed south road, fire access note, footprint table, entry inset 1 in = 30 ft. Generator `phase2/src/p2_c_101.py`, inputs `params/phase2_site.yaml`.
- **params/phase2.yaml v14:** `egress_next_revision_3` (76 in), `sight_lines.decision`, `building.footprint_margin_next_revision`, `open_items.ahj` / `occupancy`, sheet `P2-C-101` Rev A.
- Frozen checks re-run (P1-G-001 A-D, P1-A-101 A, P2-G-003 A-F, P2-A-101/102 A-D, P2-A-201 A-C, P2-A-301 A, Phase 2 Schematic Set Rev A): PDFs byte-identical, DXFs entity-identical (only the known pre-existing P1-G-001 Rev A internal PDF byte drift). Current P2-A-201 Rev D / A-301 Rev B / A-302 Rev A also regenerate unchanged. DECISIONS (open 17), ASSETS, BACKLOG, STATUS updated.

## 2026-10-04 ~8:20 AM CT · prompt v1.3 · D-055 DECIDED · C-0 ARENA inventory

- **KEYSTONE prompt v1.3 (Shane, 8:13 AM CT):** ARENA (`C:\Users\Hubby\Desktop\ARENA`, Pulsar00100) is the master; repo `blueprints/` is a mirror whose layout follows ARENA; never move / rename / reorganize / delete / overwrite in ARENA; new revs = new files (sheet + rev letter) in the folder where like files live; only `_KEYSTONE` is ours. Reviewer correction orders C-0..C-12 first; stop after each report for GO + option number.
- **D-055 DECIDED ("Shane, Grok chat", CHANGE APPROVED 8:14 AM CT):** today's decisions win over v1.3 text (D-052 76 in stairs, D-050 50 ft portal, D-049 upper tier steps down, D-048 closed, D-053 applied, 55,000 SF = footprint cap only).
- **C-0 (read-only):** ARENA inventoried with Get-ChildItem -Recurse + SHA256 (1 folder, 27 files, flat root). `ASSETS.md` §0: tree, full table (type, size, modified, what it shows, phase), SUPERSEDED marks (first-draft master floor plan ×2 + tabletop render, diorama zone data — protected, intake conflicts; Feb 2026 concept is repo-only), ARENA vs repo location map, 9 differences incl. **C-1 evidence** (ARENA `P2-A-101.pdf` = pre-freeze Rev D "STORAGE (SW)", sha256 6abfa622…; repo frozen `P2-A-101_RevD.pdf` "FLEX / STORAGE (D-039)", 6916d611…). Nothing fixed (ARENA wins). Saved first to `ARENA\_KEYSTONE\ASSETS.md`, then the repo.
- `STATUS.json`: sheets_done = current revs only (11, max 12); `STATUS.md` regenerated (it had been stale since the 7:24 AM session). `shared/validate.py` fails if sheets_done > 12.

## 2026-10-04 ~8:50 AM CT · D-056 no 55,000 SF cap · D-057 area tables · R-021 reconciliation · ARENA backup check

Shane, Grok chat, 8:36 AM CT (correction; supersedes the stopped 8:35 message — the margin-recovery list was NOT done).
- **D-056 DECIDED:** "55,000 SF = early rough estimate, not a limit." No footprint or total cap. **D-031 → SUPERSEDED (retired)**; D-055's "cap is footprint only" clause struck. Margin language removed from `params/phase2.yaml` (header v15, `building.total_sf_meaning`, `footprint_cap_status`, new `size_basis` + `size_next_revision` replacing `footprint_margin_next_revision`, `total_gsf_cap`, source), `phase2_program.yaml` (`target_status` RETIRED), `phase2_site.yaml` (`cap_status`, `footprint_check.basis`), STATUS, D-053 notes, R-018 line 106. Keys read by generators stay (marked RETIRED) so frozen / issued sheets regenerate byte-identical; frozen-sheet descriptions in `sheets:` keep their history wording.
- **D-057 DECIDED:** every area table reports L1 footprint, L2 area, TOTAL GSF and change vs the last revision; size is controlled by budget and parcel.
- **R-021 (new):** true size (decided, next revision) **L1 53,026.7 / L2 28,878.7 / TOTAL 81,905.3 SF** (+1,523.7 / +515.7 / +2,039.3 vs Rev D drawn 51,503 / 28,363 / 79,866). Program basis 54,588.9 vs drawn 53,026.7: +3,980.8 arena-volume gross-up, −773.5 L2 deck, −1,972 lobby void, +326.9 stairs (grossed vs inward), 0 east shift = 1,562.2. TOTAL GSF program 81,521.9 vs drawn 81,905.3. Saved to `ARENA\_KEYSTONE\R-021-area-reconciliation.md` first, then the repo.
- **ARENA backup check (read-only):** no backup found (details in STATUS / report). Box copies exist for every ARENA-only file.
- `shared/validate.py`: comments say `building.total_sf` is a history key, not a cap.
- Frozen checks: all frozen PDFs byte-identical, DXFs entity-identical (known P1-G-001 Rev A internal byte drift only); P2-A-201 D, A-301 B, A-302 A, C-101 A unchanged.
- v1.3.1 ERRATA block drafted for Shane's review — **not saved anywhere** (per order).

## 2026-10-04 ~9:40 AM CT · D-058 · v1.3.1 errata saved · Plan Rev E set (C-1..C-4) · D-059 backup live
- **D-058 DECIDED (Shane 9:10 AM CT):** no GO waits / no "next build options" — proceed with the standard next step (overrides v1.3 §11 / §14). Errata E-1..E-11 accepted → NEW file `ARENA\_KEYSTONE\KEYSTONE_PROMPT_v1.3.1_ERRATA.md` + repo mirror.
- **P2-A-101 / P2-A-102 Rev E** (new `build_e`, `params/phase2_plan_rev_e.yaml`): event floor 120 x 144 (east tier 16 ft from the mats, D-053), building 210 x 252; 4 stairs 76 in with 76 in intermediate landings (D-052 / D-051) = 12.67 x 21.33 ft; ST-2 in a 21.33 x 6.67 ft NE tower (must project 6.67 ft, not 5, to clear the loop); loop 5,026 SF, 718 ft, 7.35 laps/mile; FLEX / STORAGE kept (D-039 → C-1); D-049 low band under upper-tier rows 1-2 drawn, event lockers 1-4 start behind it (−877 SF), under-tier storage hatched; portal + Champion Walk label near E1 and S1 / bus notes (D-034 DECIDED; "D-034 OPEN" removed); 19 in risers noted; D-057 area check with drawn vs program side by side (C-3); no cap / margin text.
- **P2-G-003 Rev G** (new `build_g`, `compute_rev_g`, `summary_g`, `drawn_size`): Rev F + 76 in stairs (vc 874 → 1,145 SF) + 864 SF east clear zone + Rev E loop. Program footprint 54,240.9, L2 28,012.1, L1 + L2 80,747.5. D-057 table: drawn 53,062.2 / 28,914.2 / 81,976.4 (+1,559.2 / +551.2 / +2,110.4 vs Rev D).
- **C-4:** A-201 Rev D (= ARENA `P2-A-201.pdf`) already says the highest aisle is the loop at 15', matching A-301 → no change. A-201 Rev E still needed later for the 210 ft width + 6.67 ft tower (BACKLOG).
- **D-060 OPEN:** D-049 headroom reading + egress passages under rows 1-2.
- **D-059 DECIDED (Shane 9:35 AM CT):** ARENA backup live (nightly scp to shanebrain:/tank/backups/ARENA + ZFS snapshots, 30 days); no-backup flag cleared; bullfrog retired (no references found anywhere).
- Frozen revs unchanged (see report); Rev D / F generators untouched.


## 2026-10-04 ~10:00 AM CT · Set coordinated with Plan Rev E · R-022 · D-061 open
- **P2-A-201 Rev E** (`p2_a_201.py --rev E`, default; new overlay `params/phase2_elev_rev_e.yaml` with `plan_file` = Plan Rev E): building 210 ft wide, arena volume flush with the new east wall ([49,34,210,246]), NE stair tower +6.67 ft, doors from A-101 Rev E, heights note with 19 in risers / D-061. Portal + brand as Rev D. Rev D FROZEN.
- **P2-A-301 Rev C** (`p2_a_301.py --rev C`, default; `phase2_sect.yaml` `rev_c`): Plan Rev E cuts, 19 in upper risers (3 × 6.33 in aisle risers, 12 in treads), stepped tier soffit (1.5 ft structure ASSUMED) → 6 ft low band (5.6' / 7.2' clear) as storage per D-049, lockers behind it (D-060 OPEN, as drawn on A-101 Rev E), 76 in stair + 76 in mid landing (12.67' × 21.33'), exit-path conflict red on A-A + key plan (D-061). Rev B FROZEN.
- **P2-A-302 Rev B** (`p2_a_302.py --rev B`, default; `phase2_sightlines.yaml` `rev_b`): the 'as drawn' basis changed (Rev A as drawn 14 in / east 10 ft; Rev E draws 19 in / 16 ft = Rev A proposed). Re-cased: AS DRAWN (Rev E) vs REV D BASIS (superseded); C-values unchanged (seated min 149 N/S, 101 E). Closed recessed stack does not fit at the 7.08' front. Rev A FROZEN.
- **P2-C-101 Rev B** (`p2_c_101.py --rev B`, default; `phase2_site.yaml` `rev_b`): outline 210 × 252 + NE tower 21.33 × 6.67 (Rev A understated it at 5 ft, −35.6 SF), stairs and doors from Plan Rev E, Rev D outline dashed; the cap table is replaced by the D-057 table (L1 53,062.2 / L2 28,914.2 / TOTAL 81,976.4; +1,559.2 / +551.2 / +2,110.4 vs Rev D; program G-003 G 54,240.9 / 28,012.1 / 82,253.0). No cap / margin language. Rev A FROZEN.
- **R-022** (new): exit paths under the low band. Option A cuts rows 1-2 (−125 seats, or −56 with rails); Option B raises L2 to 17'-9" with 21 in risers (0 seats, +279 SF stairs, ring roof 32.75'). **D-061 OPEN** (open count 18 → 19).
- Sizes unchanged from Plan Rev E (drawn 53,062.2 / 28,914.2 / 81,976.4).

## 2026-10-04 ~10:15 AM CT · Reviewer C-5..C-11 (items that do not depend on D-061) · P2-A-201 Rev F · P1-G-001 Rev E · P2-G-003 Rev H
- **C-5 (25' clear = REFERENCE, not CITED):** P2-A-201 Rev F heights note now reads "Arena clear ≥ 25' REFERENCE (NFHS via Draper, LA RAP; R-019)". P2-A-301 (Rev C prints "CITED") is relabelled in its D-061 revision (Rev D) so A-301 is revised only once. R-019 note added. No other current sheet carries it.
- **C-6:** **P1-G-001 Rev E** (principal, 11x17; `p1_g_001.py --rev E`, default; `phase1.yaml` revision E): Rev D + " — 2021 ASSUMED, verify with AHJ" on the W1 code basis and W2 plumbing code lines, and "Edition still open: county lists 2018 codes; State Fire Marshal uses 2021." (R-006; D-008 stays OPEN, note added). Phase 1 content only: the Phase 2 size no longer prints in NOT INCLUDED (it was stale since D-056). No D-/R- codes on the sheet. Rev D FROZEN (approved, D-025). The delivered Phase1_Package_for_Dr_Headen.pdf is not regenerated.
- **C-7:** A-301 Rev C does not show intermediate handrails on the 76 in stairs. Stair geometry depends on D-061 (Option B changes it), so this goes in **BACKLOG for P2-A-301 Rev D** (IBC 2021 1014.9; D-052; architect to confirm).
- **C-8:** **P2-A-201 Rev F** (`p2_a_201.py --rev F`, default; new overlay `params/phase2_elev_rev_f.yaml`): red callout "STRUCTURAL ENGINEER REQUIRED (freestanding portal)" on the east pier + "STRUCTURAL ENGINEER REQUIRED." in the portal note; ETFE roof / solar removed from NOT SHOWN and listed only as "OPEN QUESTION: ETFE roof / solar (aspirations) — not designed, not in the SF or budget." Notes block raised 0.25 in to fit. Geometry, heights and seats unchanged. Rev E FROZEN.
- **C-9:** confirmed done in C-0 (ASSETS §0 SUPERSEDED marks). No change.
- **C-10:** new `shared/status_writer.py` (stamps `updated_at` from the box clock with the -05:00 offset, enforces sheets_done ≤ 12 / strings < 300 / open count, regenerates STATUS.md, prints the age the way the preflight computes it, `--preflight` runs the bridge). `shared/keystone_status.sh` = byte-identical copy of `ARENA\keystone_status.sh` (sha256 47ecb063…). Tested on the box: offset timestamp 5h20m old → "5h old"; 30 h → "RED — STALE"; Z → correct; a naive CT time reads 5 h too old (why the offset is required); the GitHub fallback path also worked.
- **C-11:** **P2-G-003 Rev H** (`p2_g_003.py --rev H`, default; `phase2_program.yaml` `meta_rev_h`; same `summary_g` numbers): Rev G's SUM column was WC + lav only (37 / 29 / 66), so the label alone would have been wrong. Rev H adds a WC+LAV column (the restroom-SF basis, 66 × 50 SF) and SUM now includes the fountains (39 / 31 / 70), labelled "SUM incl. 4 drinking fountains" with a footnote. Rev G FROZEN. P2-G-003 is the only current sheet with a fixture table (P1-P-001's fixture list is an existing-conditions inventory, not a code table).
- Frozen revisions re-rendered byte-identical (PDF) / entity-identical (DXF): A-201 D, E; A-301 B, C; A-302 A; C-101 A; G-003 A-G; P1-G-001 B-D; set Rev A. P1-G-001 Rev A internal: known PDF drift only.
- Open decisions unchanged: 19.

## 2026-10-04 ~10:20 AM CT · R-023 Champion Walk brick budget (vendor cost only)
- **New research** `research/R-023-champion-walk-brick-budget.md` (saved to `ARENA\_KEYSTONE` first). Source: Shane's vendor price sheet (2026-10-04, REFERENCE; engraving + shipping included). 840 SF walk (D-046), nominal face sizes, no border / joint deduction (upper bound).
- Scenarios (vendor range / S1 average / + logo on every brick): all 4x8 3,780 bricks $71,820–$73,710 / $72,450 / +$22,680; all 8x8 1,890 bricks $51,975–$58,590 / $55,755 / +$11,340; 80/20 by area (ASSUMED) 3,024 + 378 = 3,402 bricks $68,796–$69,363 / $69,111 / +$20,412.
- Break-even donor price per brick to cover the vendor cost only: 4x8 $19.00–$19.50, 8x8 $27.50–$31.00 (+$6 with logo). Donor pricing OPEN (D-044, note added).
- Installation, base / sub-base, border and engraving beyond the vendor price are NOT included and NOT estimated. The only published figure is HomeGuide's residential $8–$16/SF labor (REFERENCE, LOW, not added). Not a final cost estimate (v1.3 §2).
- No sheet changed. Open decisions unchanged: 19.


## 2026-10-04 ~10:45 AM CT · D-061 Option B (L2 17'-9", 21 in risers) + D-060 settled + approvals
- **Decisions:** D-061 DECIDED, Option B (Shane 10:27 AM CT). D-060 SETTLED: event lockers 3,600 SF behind the tier. D-062 logs the approvals of P2-A-201 Rev F, P2-G-003 Rev H, P1-G-001 Rev E and R-023; those revs are FROZEN and byte-identical. Open decisions: 19 → 17.
- **Params first:** new `params/phase2_plan_rev_f.yaml` and `params/phase2_elev_rev_g.yaml`. `phase2_program.yaml` gets `meta_rev_i` and `rev_i` (floor-to-floor 213 in, lockers 3,600). `phase2_sect.yaml` gets `rev_d`, `phase2_sightlines.yaml` gets `rev_c`, and `phase2_site.yaml` gets `rev_c`. `phase2.yaml` is v16: new sheet entries plus frozen / approved flags. `phase1.yaml` sets P1-G-001 E to frozen.
- **P2-A-101 / A-102 Rev F** (`p2_a_plan.py --rev F`):
  - Stairs: ST-1..ST-4 are 12.67 × 24.08 ft (31 risers at 6.87 in, 16 + 15), grown inward. ST-2 grows west, so the NE tower is 24.08 × 6.67 ft.
  - Rooms: mech N, S&C and stretch trimmed.
  - Low band and under-tier zones removed. Event lockers run to the tier lines (3,600 SF), and the exit paths under the tier front are clear at 7'-6".
  - D-057 table vs Rev E: L1 53,080.6 (+18.3), L2 28,932.6 (+18.3), TOTAL 82,013.1 GSF (+36.7). Seats unchanged at 2,200.
- **P2-G-003 Rev I:** program on Plan Rev F with floor-to-floor 17'-9". Stair 305.1 SF per stair per level (was 270.2). L1 + L2 gross 81,119.1 (+371.6 vs Rev G/H); footprint 54,415.1; L2 gross 28,186.3.
- **P2-A-301 Rev D:**
  - Heights and tiers: L2 FF 17'-9", ring roof 32.75', upper risers 21 in, front row 9.0 ft with 7'-6" clear (1.5 ft structure ASSUMED).
  - C-5: the 25' clear is labelled REFERENCE (R-019).
  - C-7: the stair detail shows the 16 / 15 flights and an intermediate handrail, labelled "architect to confirm" (IBC 2021 1014.9).
  - Notes cover 1030.6.2.2 and the 17'-9" elevator travel.
- **P2-A-302 Rev C:** sight lines with 21 in risers at L2 17.75.
  - Lower tier governs and is unchanged: N/S seated 149 / standing 127, E seated 101 / standing 72 mm.
  - Upper tier: N/S 179 / 156, E 105 / 76 mm.
  - No FAIL; E standing MARGINAL (L4–L6, U3–U5).
  - Stack: closed fits with 30.6 in for structure. Open still conflicts, so it stays at the tier face.
- **P2-A-201 Rev G:** L2 line at 17'-9" and ring roof at 32'-9" (datums), with the parapet and arena-behind labels raised. NE tower and doors follow Plan Rev F.
- **P2-C-101 Rev C:** NE tower 24.08 × 6.67 (Rev E tower dashed), stairs from Plan Rev F, D-057 table vs Rev E with program G-003 Rev I.
- **IBC 2021 1030.6.2.2 (if smoke-protected):** highest aisle = loop at 17.75 ft, so the roof must be ≥ 32.75 ft. The arena's U/S structure is drawn at 36 ft: PASS, 3.25 ft margin. The ring roof at 32.75 covers the perimeter rooms, not the seating.
- **Research:** R-022 §5 "Decided" added with the as-drawn numbers. R-023 marked APPROVED.
- **Frozen check:** the newly frozen revs were re-rendered and compared: A-101 E, A-102 E, G-003 H, A-201 F, A-301 C, A-302 B, C-101 B and P1-G-001 E. Results are in the commit message / report.

## 2026-10-04 ~10:58 AM CT · C-12 closed (D-063) + P2-G-002 Rev A code analysis
- **C-12 / D-063 (rule, v1.3 §15):** the 250 / 150 / 50 / 276.85 ft labels on Shane's Google measure markup are ignored and never used as dimensions.
  - Logged in DECISIONS (D-063 DECIDED).
  - ASSETS #11 / §1a / §1c are marked.
  - phase1.yaml `estimate_aerial.c12_rule` added (history / cross-check only; the tape governs).
  - `validate.py` gets **check 8**. It fails if 276.85 is a numeric value anywhere in params, or if 250 / 150 / 50 / 276.85 is a dimension value under phase1.yaml `existing`. Tested by injecting both cases into a temp copy: both FAIL; the real repo passes.
  - C-12 CLOSED.
- **Upper-tier structure 1'-6" = ASSUMED design basis** (Shane 10:48 AM CT; not a decision) until a structural engineer sizes it. Zero margin at 7'-6". The note is `phase2_sect.yaml rev_d.structure_status` (A-301 Rev D re-rendered byte-identical) and the flag is in STATUS what_to_verify.
- **P2-G-002 Rev A — CODE ANALYSIS (SCHEMATIC)** (`phase2/src/p2_g_002.py`, new `params/phase2_code.yaml`, phase2.yaml v17). Tabloid sheet with title block and PRELIMINARY stamp.
  - **Code basis:** editions table, 2021 ASSUMED vs 2018 county (verify with AHJ, R-006).
  - **Occupancy and construction:** A-4 main / A-3 or B / B / S-1, nonseparated recommended (R-007.1). Construction type TBD.
  - **Fire protection:** sprinklers + voice alarm ASSUMED (R-015.5). Smoke-protected seating not assumed.
  - **Occupant load by space** from the Plan Rev F drawn areas (T1004.5):
    - L1 1,474 without the floor.
    - L1 with the floor at 329 / 1,095 / 2,346 / 3,284: 1,803 / 2,569 / 3,820 / 4,758.
    - L2 1,277 base / 1,462 worst. Building worst 6,220.
  - **L1 exit check vs D-054:** door widths not drawn, so 64 in per pair is ASSUMED, giving 704 in.
    - Worst case SHORT: total 933.0 in (−229.0) and main exit E1 466.5 in vs 64 in (−402.5).
    - The sports case passes the total, but E1 still needs 4 pairs.
    - Other exits (1030.3) and lose-one (1005.5) pass in every case.
  - **Options (no redesign):** (1) an E1 bank of 8 pairs (512 in; total 1,152 in), or (2) distributed main exits under 1030.2's last sentence: 15 pairs total (+4).
  - **L2 stairs:** 304 in vs 292.4 in worst (+11.6).
  - **Plumbing:** fixture basis G-003 Rev I. The standing case would need 26 / 50 WC on L1 (vs 10 / 18).
  - **Other sections:** travel and common path, plus open items.
- **Research:** R-007.3 addendum quotes the sections looked up this session: 1010.1.1, 1030.2 (full), 1030.3, 1004.2.1, 1005.5, T1006.2.1, T1017.2. A D-054 note is added (still OPEN).
- No frozen sheet changed.

## 2026-10-04 11:07 AM CT — L1 exits Option 1 DECIDED; P2-A-101 Rev G + P2-A-111 Rev A (life safety)
- **Decision (Shane 11:07 AM CT):** Level 1 exits use Option 1, an 8-pair door bank at E1 across the lobby's 58 ft south wall.
  - 512 in clear, with 64 in per pair ASSUMED.
  - The single controlled entry stays (D-033).
  - Folded into the D-054 note. D-054 floor use stays OPEN, but the exits are sized for the standing worst case.
- **New findings (OPEN, not redesigned):**
  - **D-064 restrooms at the worst case:** 26 M / 50 W WC needed vs 10 / 18 drawn.
    - Option 1: size the restrooms for the worst case.
    - Option 2: limit standing events, or bring temporary facilities.
  - **D-065 security checkpoint vs egress:** the clear width beside the checkpoint is 312 in, but the main exit needs 466.5 in (IBC 1003.6, 1010.5, 1030.2).
    - Option 1: move screening to a side bay of the lobby.
    - Option 2: move screening outdoors onto the plaza.
  - Open count 17 → 19.
- **P2-A-101 Rev G** (Level 1 only; new `params/phase2_plan_rev_g.yaml`; `p2_a_plan.py --rev G`):
  - E1 drawn as an 8-pair bank, with an outer bank and an inner (vestibule) bank.
  - Vestibule widened to 52 ft (520 SF).
  - First aid moved to the lobby's east side (ASSUMED).
  - Checkpoint flagged "EGRESS CONFLICT — see P2-A-111".
  - Rev F is frozen and byte-identical. P2-A-102 stays at Rev F. Footprint, areas and seats are unchanged.
- **P2-A-111 Rev A life safety plan** (new `params/phase2_life_safety.yaml`, `phase2/src/p2_a_111.py`): L1 + L2 at 1" = 50'-0".
  - Exits are shown with clear widths and capacities, and occupant loads per room come from P2-G-002.
  - **L1 checks at the worst case (6,220), all PASS:**
    - Total: 1,152 in vs 933.0.
    - E1: 512 vs 466.5.
    - Other L1 exits: 420.7 vs 356.8.
    - Lose E1: 640 vs 466.5.
    - Sensitivity, whole floor zone of 17,280 SF standing: E1 needs 479.4 in, which also passes.
  - **L2 stairs:** 304 vs 292.4 in. Lose one stair: 228 vs 146.2. Loop: 84 vs 78.6.
  - **Travel distance (T1017.2 limit 250 ft; diagram measurements, UNVERIFIED):** L1 maximum 133 ft, L2 maximum 128 ft.
  - **Exit separation (1007.1.1 exception 2):** the diagonal is 333.2 ft, so the minimum is 111.1 ft. E1–X5 is 252.0 ft, ST-1–ST-3 255.1 ft and ST-2–ST-4 281.5 ft. All PASS.
  - **Common path:** event lockers pass if their door is placed within 75 ft (UNVERIFIED). Seating is TBD.
  - **TBD:** exit discharge from E1 needs ≥ 466.5 in (1028.3). The 28 ft walk is 336 in.
- **Data:** `phase2.yaml` v18 (A-101 Rev F frozen, Rev G entry, new sheet P2-A-111).
- **Research:** R-007.4 addendum (1003.6, 1010.5, 1007.1.1–1007.1.2, 1017.3, T1006.2.1 / 1006.2.1 exception 3, 1030.8, 1028.3, 1028.5).
- **Frozen check:** every other revision re-renders byte-identical (PDF cmp, DXF entities).

## 2026-10-04 11:24 AM CT — D-066 OPEN (exit discharge); P2-A-401 Rev A enlarged plans (event locker rooms 1-4)
- **New finding D-066 (OPEN, no redesign):** the exit discharge from E1 must be ≥ 466.5 in (IBC 1028.3). The Champion Walk is 28 ft = 336 in (D-046), and so is the portal arch opening (D-050), so the discharge must bypass the arch too.
  - Option 1: widen the walk / plaza to ≥ 39 ft at the discharge.
  - Option 2: add a parallel paved discharge path of ≥ 130.5 in beside the walk / portal.
  - Open count 19 → 20.
- **P2-A-401 Rev A** (new `params/phase2_enlarged.yaml`, `phase2/src/p2_a_401.py`; `phase2.yaml` v19): the 4 event locker rooms only, at 1/8" = 1'-0", with a key plan.
  - Envelopes come from plan Rev G: 4 × 900 = 3,600 SF (D-060), under the upper tier at the tier line (D-061, 7'-6" clear).
  - Two templates: rooms 1-2 have the door on the side wall to EXIT (N); rooms 3-4 have it on the end wall to EXIT (E). Rooms 2 and 4 are mirrors.
  - **Each room (ASSUMED):**
    - 2 WC: 1 wheelchair 60×60 (ADA 604.8.1.1) + 1 ambulatory 36×60 (604.8.2.1).
    - 2 lavatories: 1 accessible (606).
    - 60 in turning circle (304.3.1).
    - 4 showers: 1 roll-in 30×60 with 30×60 clearance (608.2.2) + 3 at 36×36.
    - 31-32 lockers, 15 in (2 accessible, 225.2.1 / 811).
    - 2 team benches + 1 accessible bench, 24×48 wall-affixed (903).
    - Trainer table.
    - Room door 36 in (34 in clear, 404.2.3), swinging into the room (IBC 1010.1.2.1, < 50 occupants; ADA 803.3).
  - **Common path (T1006.2.1, ≤ 49 occupants, ≤ 75 ft), measured on this layout:** rooms 1-2 45.6 ft, rooms 3-4 50.9 ft. All PASS.
  - Travel to X5 / X7 is ≤ 66 ft (vs 250).
  - The restroom core is NOT drawn: it waits on D-064, and the sheet says so.
- **Research:** ADA 2010 Standards text saved to the box (`research_src/ada2010_v2.txt`, www.ada.gov, retrieved 2026-10-04). Sections are quoted in the new note `research/R-024-ada-locker-rooms.md`.
- **Frozen check:** every other revision re-renders byte-identical.

## 2026-10-04 11:45 AM CT — P2-A-103 Rev A floor overlays (mats, court, telescopic tier, floor cases)
- D-064, D-065 and D-066 stay OPEN (Shane has not answered; nothing assumed). D-054 (floor uses) stays OPEN. Open count stays 20.
- **P2-A-103 Rev A** (new `params/phase2_overlays.yaml`, `phase2/src/p2_a_103.py`; `phase2.yaml` v20): four overlays on the P2-A-101 Rev G plan at 1" = 50'-0" (cases at 1" = 100'-0").
  - **(a) Wrestling:** 4 × 42 ft mats, 2 × 2 (D-014, D-030). Checked on the layout, all PASS:
    - circle + safety area: 42 ft mat vs ≥ 38 ft (NFHS 2-1-2);
    - space around each mat: W 10 / between 10 / E 16 / S and N 25 ft vs ≥ 10 (2-1-5);
    - scorer's table 10.5 ft from the mat (2-3); benches 10.5 ft from the mat and 10 ft from the table (2-1-5);
    - circle to walls / tier front: W 17 / E 23 / S and N 32 ft vs about 10 ft (KHSAA recommendation).
    - Tables (8 × 2.5 ft) and benches (10 × 1.5 ft) are ASSUMED. The portal and V1 aisles are kept clear. NFHS text is the 2014-15 edition (current book UNVERIFIED).
  - **(b) Basketball:** only the 1 court already in params: 84 × 50 ft (NFHS 1-1) + 10 ft runout (1-2-1); 22 / 28 / 20 / 20 ft to the floor edges. Volleyball and a 2nd court are TBD (not in params or decisions; not drawn).
  - **(c) Telescopic lower tier:** open (12 ft) floor 120 × 144 = 17,280 SF vs closed (3'-6" Hussey stack at the upper-tier face) 128'-6" × 161'-0" = 20,689 SF (+3,409 SF, lower seats stowed). ICC 300 via IBC 1030.1.1.
  - **(d) Floor cases from P2-G-002 Rev A,** hatched on 114 × 144 = 16,416 SF: sports 329 / tables + chairs 1,095 / chairs 2,346 / standing 3,284 (L1 1,803 / 2,569 / 3,820 / 4,758), with layout notes (IBC 1030.9.1, 1030.13.1, 1030.13.2, 1030.13.2.1; posting 1004.9).
    - Tier closed: standing 4,138 / chairs 2,956 with no lower seats gives L1 4,512 / 3,330, below the 4,758 design case (arithmetic).
  - Flag (no new program): chair / table / stage storage is not in the program (TBD, D-054).
- **Research:** R-007.5 addendum (1004.9, 1030.1.1, 1030.1.1.1, 1030.9.1, 1030.13.1, 1030.13.2, 1030.13.2.1).
- **Frozen check:** every other revision re-renders byte-identical.

## 2026-10-04 12:10 PM CT — P2-A-901 Rev A 3D massing model + views (P2-T-011)
- D-054, D-064, D-065 and D-066 stay OPEN. Nothing on the sheet or in the model implies a choice: no checkpoint modelled (D-065), no added restroom volume (D-064), no floor-use staging (D-054), Champion Walk shown at the drawn 28 ft with a D-066 note. Open count stays 20.
- **P2-A-901 Rev A** (new `params/phase2_massing.yaml`, `phase2/src/p2_a_901.py`; `phase2.yaml` v21): MASSING ONLY, PRELIMINARY, NTS axonometric views built from the current params (plan Rev G L1 / Rev F L2, A-201 Rev G heights / portal / brand / walk, A-301 Rev D / A-302 Rev C sections, C-101 Rev C site; D-041, D-043, D-046, D-047, D-050).
  - V1 aerial from the SW (with site: walk, bus loop diagram, road, service apron); V2 cutaway at L2 FF 17'-9" from the SW (roofs removed: tiers, event floor + mats, lobby open to below); V3 aerial from the SE; V4 aerial from the NW (service side, S1); V5 portal + Champion Walk from the SSW.
  - Heights are only those already in params (L2 FF 17'-9" DECIDED; ring roof 32.75 ft / arena roof 42 ft ASSUMED per A-201 Rev G; portal 50 ft max, crown 34 ft, springline 22'-1"). Door 6 × 8 ft drawn symbol ASSUMED. Colours: finish ids from `phase2_elev.yaml` (hex ASSUMED swatches).
  - Not modelled: parapets, rooftop units, structure, windows / cladding, grading, landscaping, lighting, parking (site TBD, D-006), signage content.
  - **Model file:** `phase2/out/3d/P2-A-901_RevA_massing.obj` + `.mtl` (feet, Y-up; deterministic, byte-identical on re-run).
- **Frozen check:** every other revision re-renders byte-identical.

## 2026-10-04 1:21 PM CT — Decisions D-054 / 064 / 065 / 066 + storage room (D-067) applied to the sheets
- **Decisions (Shane, Grok chat, 1:21 / 1:22 PM CT):**
  - **D-054 CLOSED:** event floor = chairs only, 7 net → 2,346 (no standing floor case).
  - **D-064 CLOSED, Option 2:** restrooms sized to the chairs-only case; posted occupant loads; temporary units above that.
  - **D-065 CLOSED, Option 1:** screening in a lobby side bay; 468 in clear kept to the E1 bank (≥ 466.5 in).
  - **D-066 CLOSED:** Champion Walk 40 ft = 28 ft brick + 6 ft bands both sides, around both piers (IBC 1028.3).
  - **D-067 DECIDED (new program item):** chair / table / stage storage annex [52,252]-[122,282] ft = 70 × 30 = 2,100 SF on the north wall, S1 moved to y 282 (sizing ASSUMED except the cart data).
  - **D-068:** approvals logged and frozen: P2-A-111 Rev A, P2-A-401 Rev A, P2-A-103 Rev A, P2-G-002 Rev A.
  - **D-069 OPEN (new finding):** chairs-only L1 restrooms need 22 M / 42 W WC, lav 9 / 12, DF 4 vs 10 / 18, 4 / 5, 2 drawn (+48 fixtures), about +535 to +2,400 SF; 3 options, rooms not redrawn.
  - Open count 20 → **17**.
- **New revisions** (all new params files; frozen revisions untouched; `phase2.yaml` v22):
  - **P2-A-101 Rev H** (`phase2_plan_rev_h.yaml`): storage annex + S1 on the north, screening side bay (468 in clear), restroom D-069 flags (rooms not redrawn).
  - **P2-A-111 Rev B** (`phase2_life_safety_rev_b.yaml`): life safety at the chairs-only floor, screening bay outside the egress width, 40 ft discharge walk.
  - **P2-G-002 Rev B** (`phase2_code_rev_b.yaml`): occupant loads at 2,346 floor, fixture count and D-069 finding with the +535 to +2,400 SF range.
  - **P2-G-003 Rev J** (`phase2_program.yaml` rev_j): program + loop + storage; F 56,515 / L2 28,186 / total 84,701 SF program vs 84,113 drawn.
  - **P2-A-401 Rev B** (`phase2_enlarged_rev_b.yaml`): L1 restroom core tight test-fit (men 34 × 23 ft = 860 SF vs 700; women 41 × 33 ft = 1,488 vs 1,150; + 2 fountain alcoves 36 SF ≈ +535 SF).
  - **P2-A-103 Rev B** (`phase2_overlays_rev_b.yaml`): chairs-only floor case, storage route diagram annex → floor.
  - **P2-C-101 Rev D** (`phase2_site.yaml` rev_d): annex footprint, 40 ft walk with 6 ft bands (mirrored about x 226), service apron [52,282]-[85,306] ft.
  - **P2-A-901 Rev B** (`phase2_massing_rev_b.yaml`): annex (16 ft high ASSUMED), walk bands, screening zone; model `phase2/out/3d/P2-A-901_RevB_massing.obj` + `.mtl`.
- **Areas:** GSF drawn 82,013 → **84,113** (+2,100); L1 53,081 → 55,181; L2 28,933 unchanged.
- **Follow-up:** P2-A-201 north elevation does not yet show the annex. G-001 cover, combined set and PR are ON HOLD (Shane 1:46 PM CT).
- **Frozen check:** every frozen / approved revision re-renders byte-identical (PDF + DXF entities; A-901 Rev A OBJ / MTL unchanged).

## 2026-10-04 3:31 PM CT — D-069 closed: east restroom bump-out (Option 2)
- **Decision (Shane, 3:31 PM CT):** **D-069 CLOSED = Option 2** ("Option B"): second restroom pair in a one-storey bump-out opposite the lobby core. East concourse width and the SW FLEX room unchanged (D-039 unchanged). Open count 17 → **16**.
- **Location: EAST** (KEYSTONE pick, as asked): bump-out [210,161.09]-[240,217.09] = **30 × 56 ft = 1,680 SF**, one storey, 16 ft ASSUMED, centred on V2 / EXIT (E). Why east: the north side is the back-of-house yard (service drive, S1 apron, storage annex x 52-122, X4 / X5 / ST-2 discharges); the east side is open and the public reaches it straight from the floor / east tier through V2 and the EXIT (E) passage, which continues 30 ft east as the core-2 corridor. X7 moves 30 ft east to the bump-out east face (x 240).
- **Fixtures (chairs-only, load 3,446, IBC 2021 Table 2902.1, R-009):** required 22 M / 42 W WC, 9 / 12 lav, 4 DF. Lobby core 10 / 18, 4 / 5, 2 (unchanged) + **core 2: men 5 WC + 7 urinals, 5 lav; women 24 WC, 7 lav; 2 DF hi-lo + janitor**. Urinals 7 ≤ 67% of 12 = 8 (IPC 2021 424.2). Totals 22 / 42, 9 / 12, 4 = required.
- **Params first:** `phase2.yaml` v23; `DECISIONS.md` D-069 DECIDED; `phase2_program.yaml` rev_k; new `phase2_plan_rev_i.yaml`, `phase2_life_safety_rev_c.yaml`, `phase2_enlarged_rev_c.yaml`, `phase2_massing_rev_c.yaml`, `phase2_elev_rev_h.yaml`; `phase2_site.yaml` rev_e.
- **New revisions** (frozen revisions untouched):
  - **P2-G-003 Rev K:** program + fixture split (lobby core / core 2) + bump-out 1,680 SF; program F 58,195 / L2 28,186 / total 86,381 SF.
  - **P2-A-101 Rev I:** bump-out drawn (rooms 25-27, corridor), east wall open at EXIT (E), X7 at x 240, D-069 flags removed.
  - **P2-A-111 Rev C:** T1 133.1 → 163.1 ft; new T7 (women's far corner → X7) 67.0 ft; common path women 38 / men 34 ft (≤ 75); diagonal unchanged at 333.2 ft (all outline corners checked); E1-X5 separation 252 ≥ 111.1 ft; locker rooms 3-4 travel 95.9 ft.
  - **P2-A-401 Rev C:** core-2 enlarged plan at 1/16" (men 26 × 14 = 364 SF, women 30 × 34 = 1,020 SF, DF / janitor 56 SF, corridor 240 SF) + fixture table + why-east note; locker rooms unchanged.
  - **P2-C-101 Rev E:** outline + bump-out; area table vs Rev H; X7 east discharge TBD with the parcel.
  - **P2-A-901 Rev C:** bump-out mass (16 ft ASSUMED) with X7; model `phase2/out/3d/P2-A-901_RevC_massing.obj` + `.mtl`.
  - **P2-A-201 Rev H:** annex + bump-out on every face where they show (north: annex in front with S1, bump-out at the east end; east: bump-out in front with X7, annex beyond; west: annex; south: bump-out beyond the east end); N / E / W at 1" = 40'.
- **Areas (D-057):** L1 55,181 → **56,861** (+1,680); L2 28,933 (unchanged); TOTAL GSF 84,113 → **85,793** (+1,680). Program Rev K 86,381.
- **Findings:** (1) chair layouts on the floor must keep an aisle to V2 (core 2 is reached through V2); (2) X7's discharge path from x 240 to a public way is TBD with the parcel (D-006); (3) core-2 plumbing (waste, vent, water) is an MEP item; (4) P2-G-002 Rev B still shows D-069 OPEN (no G-002 Rev C was ordered).
- **Still PAUSED:** G-001 cover, combined set PDF and PR not built.
- **Frozen check:** `/tmp/cur_check7.sh` (explicit `--rev`, now including the 1:21 PM revs, A-201 A-G and the new revs): every frozen / committed revision re-renders byte-identical (PDF + DXF entities; A-901 OBJ / MTL); new revs deterministic.

## 2026-10-05 4:48 PM CT — palette
- palette.py added from existing script colors; no sheet output changed.
- 2026-10-05 5:22 PM CT: p2_c_101 now imports palette.py; output identical.
- 2026-10-05 5:25 PM CT: p2_a_103 now imports palette.py; output identical.
- 2026-10-05 5:25 PM CT: p2_a_111 now imports palette.py; output identical.
- 2026-10-05 5:25 PM CT: p2_a_201 now imports palette.py; output identical.
- 2026-10-05 5:25 PM CT: p2_a_301 now imports palette.py; output identical.
- 2026-10-05 5:25 PM CT: p2_a_302 now imports palette.py; output identical.
- 2026-10-05 5:25 PM CT: p2_a_401 now imports palette.py; output identical.
- 2026-10-05 5:25 PM CT: p2_a_901 now imports palette.py; output identical.
- 2026-10-05 5:25 PM CT: p2_a_plan now imports palette.py; output identical.
- 2026-10-05 5:25 PM CT: p2_g_002 now imports palette.py; output identical.
- 2026-10-05 5:25 PM CT: p2_g_003 now imports palette.py; output identical.

## 2026-10-09 — P2-T-017 · D-081 NE stair drum (A-101 L, A-102 H, G-003 L)
- Sync: DECISIONS_ARENA.md mirrored through D-081 (D-081 row also added in ARENA _KEYSTONE); KEYSTONE_PROMPT_v1.3.2_ERRATA.md; handoff_2026-10-08/ (Claude Code handoff + ARENA CLAUDE.md copy).
- Sync from origin/main: p2_a_101_rev_k.py, p2_a_102_rev_g.py, p2_g_002_rev_e.py + phase2_plan_rev_k.yaml, phase2_plan_rev_g_l2.yaml + their PDF/DXF; regenerated PDFs byte-identical to ARENA's approved files. `source` lines added to the K / G params (validate), one mech-bay basis note reworded (banned number); outputs unchanged.
- New: phase2_plan_rev_l.yaml, p2_plan_rev_l_geom.py, p2_a_101_rev_l.py (--rev L), p2_a_102_rev_h.py (--rev H), p2_g_003_rev_l.py (--rev L). Base = approved Rev K / G geometry (DXF read). L1 57,861 / L2 29,033 / TOTAL 86,894 GSF (+682 vs Rev K/G 86,212; +1,101 vs Set Rev D 85,793).
- phase2.yaml v24: A-101 K/L, A-102 G/H, G-002 E, G-003 L registered. Set Rev D patch (handoff_2026-10-04/keystone_repo.patch) still NOT applied: it trips validate (missing sources; a banned number inside frozen-sheet text).

## 2026-10-09 9:39 AM CT — P2-T-017 cont. · D-082 / D-083 / D-084 (A-101 M, A-102 I, G-003 M)
- DECISIONS_ARENA.md: D-082 (30 ft drum), D-083 (drum door west, IBC 2021 1010.1.5 landing), D-084 (east side = D-072 / plan Rev J). Same rows appended to ARENA _KEYSTONE/DECISIONS_ARENA.md.
- New: params/phase2_plan_rev_j.yaml (from handoff_2026-10-04/keystone_repo.patch, read only; regenerates the Set Rev D P2-A-101 Rev J byte-identical), params/phase2_plan_rev_m.yaml, p2_plan_rev_m_geom.py, p2_a_101_rev_m.py (--rev M), p2_a_102_rev_i.py (--rev I), p2_g_003_rev_m.py (--rev M).
- Areas: L1 57,896 / L2 29,068 / TOTAL 86,964 GSF; +35 / +35 / +70 vs Rev L/H; +1,035 / +135 / +1,171 vs Set Rev D.
- Stair fit 1.49 ft spare (was 0.49). Drum door 235 deg: 61.7 in to the loop edge; full 76 x 44 in landing reaches 4.9 in onto the loop (finding, architect).
- East side: T1 133 ft, common path 61 / 30 ft, corridor 96 in, dead end 5.2 ft, X7 / X11 / X8 on the wall (ASSUMED, Set Rev D method).
- phase2.yaml v25: A-101 M, A-102 I, G-003 M registered. Revs K/L, G/H, E, L untouched. G-001, combined set, PR on hold.

## 2026-10-09 10:11 AM CT — D-085 / D-086 · A-101 N, G-003 N
- D-085 logged (drum door landing overlap left for the architect; no redraw).
- D-086: old NE stair strip on Level 1 = 30 MECH (remote), 67 SF (not connected to the MECH / ELEC BAY; access TBD). New: params/phase2_plan_rev_n.yaml, p2_plan_rev_n_geom.py, p2_a_101_rev_n.py (--rev N), p2_g_003_rev_n.py (--rev N).
- Mechanical 4,234 -> 4,302 SF = 4.87 % -> 4.95 % of GSF vs 5 % (D-072 method; Set Rev D 4.1 %). GSF unchanged: 57,896 / 29,068 / 86,964.
- phase2.yaml v26. A-102 Rev I unchanged (Level 2 not touched). G-001, combined set, PR on hold.

## 2026-10-09 1:05 PM CT — D-087 bus loop cut (C-101 G, A-901 E, A-201 J)
- DECISIONS_ARENA.md: D-087 (cut the bus loop; service stays at S1; team bus + van drop-off curbside along the parking drive aisle, ASSUMED, TBD with the parcel, D-006).
- New: params/phase2_site_rev_g.yaml, phase2_massing_rev_e.yaml, phase2_elev_rev_j.yaml; phase2/src/p2_c_101_rev_g.py (--rev G), p2_a_901_rev_e.py (--rev E), p2_a_201_rev_j.py (--rev J). Each is the Set Rev D handoff generator (checked: C-101 F and A-901 D regenerate byte-identical from the handoff patch in a scratch copy) with the bus loop removed. Building on these sheets is still Set Rev D (A-101 J).
- Checked and not revised: A-111 Rev D, G-002 Rev D / E (no bus loop shown). G-001 Rev C cover mentions the loop (on hold).
- STATUS: land-need planning note (10-15 ac, ASSUMED).
- phase2.yaml v27: C-101 G, A-901 E, A-201 J registered.

## 2026-10-09 1:23 PM CT — current building onto C-101 H, A-901 F, A-201 K (no new decision)
- Building = P2-A-101 Rev N / A-102 Rev I via p2_plan_rev_n_geom.py: R 20 ft corners, 30 ft drum (true circle / ARC in the C-101 DXF), mech / elec bay, east side per D-072 / D-084, exits X1 / X9 / X10 as Rev K, X6 on the drum.
- C-101 Rev H: D-057 table L1 / L2 / TOTAL / delta vs Rev G (Set Rev D): 57,896 / 29,068 / 86,964 vs 56,861 / 28,933 / 85,793 (+1,035 / +135 / +1,171). D-087 kept (no loop, curbside drop-off label).
- A-901 Rev F: ring and drum as extruded polygons (Prism class, facets sorted, back faces culled); bay 16 ft ASSUMED. D-087 kept.
- A-201 Rev K: Rev J showed the old NE tower and square corners. Rev K: drum, bay (16 ft ASSUMED), thin R 20 tangent lines, key plan corners radiused, X6 on the drum.
- New: params/phase2_site_rev_h.yaml, phase2_massing_rev_f.yaml, phase2_elev_rev_k.yaml; p2_c_101_rev_h.py, p2_a_901_rev_f.py, p2_a_201_rev_k.py. phase2.yaml v28.
- STATUS sheets_done merged (A-101 L / M and C-101 G / A-901 E / A-201 J lines folded into superseded entries); history kept here.
