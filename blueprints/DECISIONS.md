# DECISIONS — KEYSTONE

Status values: **OPEN** / **DECIDED** / **PARKED**.
When Shane answers, KEYSTONE records `DECIDED 2026-MM-DD — <answer> — "Shane, <channel>"` and updates the params file first.
Source for D-001…D-012: KEYSTONE_ARCHITECT_PROMPT.md v1.1 Section 5. D-013…D-015 logged by KEYSTONE at bootstrap, 2026-10-03. D-016…D-017 logged at the reference plan intake, 2026-10-03.

## Phase 1 — existing wrestling room remodel

| ID | Question | Status | Notes / feeds |
|---|---|---|---|
| D-001 | Existing room dimensions, ceiling height, door locations, wall material (needs Shane's tape measure + photos) | OPEN | phase1.yaml `existing.*`. Checklist: phase1/MEASUREMENT_CHECKLIST.md. **Partial 2026-10-03:** wrestling room MEASURED: 55'-0" N-S × 45'-0" E-W inside, wall to wall, rectangle ("Shane tape, inside wall-to-wall, 2026-10-03") → `existing.wrestling_room.length_ft/width_ft`, drawn on P1-A-101 Rev A. The aerial estimate (≈55.1 × 46.9 ft exterior) agreed and stays a cross-check only. Door locations are APPROX. from the sketch only. **Still TBD:** support wing dims, door positions/widths, ceiling, wall material/thickness, photos. **10:12 PM CT (Shane):** ceiling 10'-0"; CMU building (8" walls ASSUMED unless noted); 4 doors ASSUMED standard 3'-0" × 7'-0" single HM, VERIFY (locations still APPROX.; south exit may be a pair). Dr. Headen has taken photos (copies requested) |
| D-002 | Where the plumbing fails, what fixtures exist, where water/drain lines run | OPEN | phase1.yaml `existing.plumbing`, work item W2. **Update 2026-10-03 (Shane, firsthand):** no running water to the area; all fixtures out of service; cause unknown. Still needed: plumber visit to diagnose (shutoff, supply line, or other), plus photos. **10:06 PM CT (Shane):** fixtures = 2 showers, 1 private toilet, 2 toilets, 1 urinal, sinks (count TBD), water fountain/sink, all out of service; problem spots = entire support wing (showers broken before the water loss); where = support wing east of the wrestling room, along the open hallway. Still TBD: cause, sink count, water/drain lines |
| D-003 | Which walls get pads, pad height, and whether pads are bought by the school, donated, or fundraised | DECIDED | DECIDED 2026-10-03 — Pad height 6 ft — "Shane, chat". This matches the R-001 guidance. Applied in phase1.yaml W1 `pad_height: 6 ft`. Earlier the same day the template came back unfilled, so 6 ft had only been proposed. **Which walls and who supplies the pads are not decided; they moved to D-021 (OPEN)** |
| D-004 | Who must approve work on school property (principal → district facilities → anyone else) | OPEN | phase1.yaml `approvals`. Legal/procurement advice is out of scope for KEYSTONE. **2026-10-03: R-002 + R-004 done.** Sources point to principal → MCSS Operations & Facilities → Board of Education (building/land improvements) → Alabama DCM review + inspections (any cost, any funding). Donated work: bid law may not apply to entirely private funds (AG opinions, via Examiners), but DCM review still does. **Needs district confirmation** before DECIDED |
| D-005 | Principal's name spelling (Headen or Hedden) | DECIDED | DECIDED 2026-10-03 — "Dr. Headen" — "Shane, firsthand 2026-10-03 10:12 PM CT". Stored in phase1.yaml `contacts.principal` (name, display_name). Used on P1-G-001 Rev D. Frozen Revs A/B/C unchanged |

## Phase 2 — new building + campus

| ID | Question | Status | Notes / feeds |
|---|---|---|---|
| D-006 | Site / parcel / address | OPEN | Campus drawn as SITE TBD diagram until decided |
| D-007 | Owner of record for the new building (school system, county, town, nonprofit, partnership) | OPEN | Drives D-008 and R-006 |
| D-008 | Authority Having Jurisdiction for permitting | OPEN | R-006 |
| D-009 | Seating type (fixed, telescopic) and final count | OPEN | Concept sheet shows 2,200 (locked total). Repo diorama text says "Permanent stadium seating" (see ASSETS.md); not treated as a decision. **Reference-plan seating label conflict → see D-016** |
| D-010 | Locker room parity (equal SF?) | OPEN | See D-013 |
| D-011 | Concessions scope | OPEN | |
| D-012 | Any budget target for Phase 2 | OPEN | Do not reuse the superseded Feb 2026 concept budget |

## Logged at bootstrap (2026-10-03)

| ID | Question | Status | Notes / feeds |
|---|---|---|---|
| D-013 | Girls locker 3,503 SF vs boys 3,500 SF. Real difference, or a drawing-tag slip? | OPEN | Prompt §3 says this is likely a tag slip. **Draw both lockers equal until Shane decides.** Also, the intake says AI renders show girls as 3,500 |
| D-014 | Mat size check: concept notes say "four 42-foot mats ≈ 7,000 SF." Check against current NFHS rules (mat, circle, safety area, spacing) before laying out mats | OPEN | Research → R-005 (Phase 2, P2-T-003). No mats get drawn until R-005 is done |
| D-015 | The intake file `KEYSTONE_INTAKE_2026-10-03.md` starts with "MOVIE MAKER INTAKE," but everything in it is for KEYSTONE. Label slip? | OPEN | KEYSTONE treated the content as its own intake. Shane, please confirm |

## Logged at reference plan intake (2026-10-03)

| ID | Question | Status | Notes / feeds |
|---|---|---|---|
| D-016 | Reference plan seating labels: north bank 3,200, south bank 2,200. Locked: 2,200 total (Shane 2026-10-03). Which label is wrong, and is 2,200 the total or per bank? | OPEN | phase2.yaml `spaces.seating`. The reference plan legend also says "Arena Capacity: 2,200 Spectators." The tabletop render swaps the two labels. Keep 2,200 total until Shane answers |
| D-017 | Which image is the Phase 2 reference plan, and what may be taken from it? | DECIDED | DECIDED 2026-10-03 — Phase 2 reference plan = Phase2-floor-plan-flat.png; use zones, adjacencies, 5 SF tags, room list; ignore dimension strings, scale bar, garbled text, green/gold legend — "Shane, chat". Diorama demoted to secondary; `Phase2-floor-plan.jpeg` is presentation only, not a source |
| D-018 | Promote rooftop solar + stormwater storage into Phase 2? Retractable roof? | DECIDED | DECIDED 2026-10-03 — Solar + stormwater storage promoted to Phase 2 as design intent only (no sizes, panel counts, or gallons until a cited R-file sizes them for this building). Retractable roof CUT. — "CHANGE APPROVED", Shane, chat. Applied in phase2.yaml `sustainability` |

## Logged at R-001/R-003 approval (2026-10-03)

| ID | Question | Status | Notes / feeds |
|---|---|---|---|
| D-019 | Must both new athlete restrooms (1 male + 1 female, single-user) meet full 2010 ADA, or only some (2010 ADA 213.2 Exception 4)? | DECIDED | DECIDED 2026-10-03 — Full 2010 ADA compliance on BOTH new restrooms — "Shane, chat". Resolves the R-003 Exception 4 question. Applied in phase1.yaml W3 + `standards.ada_single_user_restroom.both_rooms_comply` |
| D-020 | Wall pad fire-test wording on the scope sheet | DECIDED | DECIDED 2026-10-03 — Scope sheet must include, verbatim: "Wall pads must have an NFPA 286 assembly test report — not a foam-only rating. Ask the vendor before purchase." — "Shane, chat". Applied in phase1.yaml W1 `purchase_note` (basis: R-001) |
| D-021 | Which walls get pads, and whether pads are bought by the school, donated, or fundraised (the rest of D-003 after pad height was decided) | OPEN | Split from D-003 on 2026-10-03. phase1.yaml W1 `walls`, `supplied_by`, `funding.pad_funding`. Walls need Shane's measurements + photos (D-001). 2026-10-03: Shane's pad estimate (revised 10:12 PM CT: ~188 LF after 4 doors, ~94 panels at 2×6 ft) assumes all 4 walls; which walls is still OPEN |
| D-022 | Split Phase 1 into 1A (wall pads — may be maintenance, ask facilities) and 1B (plumbing + restrooms — licensed designer + DCM review likely)? | OPEN | Logged 2026-10-03 at Shane's request ("Shane, chat"). Do NOT restructure backlog, params, or sheets until Shane decides. Feeds from R-002/R-004 |
| D-023 | Is P1-G-001 Rev B approved for the principal, and does Shane's contact info stay on it in the public repo? | DECIDED | DECIDED 2026-10-03 — Rev B approved as-is; contact info stays (already public); no history rewrite — "Shane, chat" |
| D-024 | Priority order of the three Phase 1 work items | DECIDED | DECIDED 2026-10-03 — W2 (restore water) first → W3 (restroom split) second → W1 (wall pads) third; W1 can run in parallel because it doesn't depend on water — "Shane, firsthand 2026-10-03". Applied as phase1.yaml `work_items[].priority` and on P1-G-001 Rev C. Does not decide D-022 (1A/1B split) |
| D-025 | Is P1-G-001 Rev D (principal version) approved? | DECIDED | DECIDED 2026-10-03 — Rev D approved — "Shane, 10:29 PM CT". Frozen (`frozen: true`); committed PDF/DXF unchanged. Bundled first in Phase1_Package_for_Dr_Headen.pdf |
| D-026 | Is P1-A-101 Rev A (existing conditions, room outline) approved, and are the door marks right? | DECIDED | DECIDED 2026-10-03 — Rev A approved; door locations match Shane's markup; exits swing out (correct) — "Shane, 10:29 PM CT". Hallway door swing and south exit single/pair were left unfilled → stay "assumed, verify" (no sheet change). Frozen; committed PDF/DXF unchanged |
