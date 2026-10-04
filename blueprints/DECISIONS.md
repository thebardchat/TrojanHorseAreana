# DECISIONS — KEYSTONE

Status values: **OPEN** / **DECIDED** / **PARKED**.
When Shane answers, KEYSTONE records `DECIDED 2026-MM-DD — <answer> — "Shane, <channel>"` and updates the params file first.
Source for D-001…D-012: KEYSTONE_ARCHITECT_PROMPT.md v1.1 Section 5. D-013…D-015 logged by KEYSTONE at bootstrap, 2026-10-03. D-016…D-017 logged at the reference plan intake, 2026-10-03. D-009 DECIDED 2026-10-04 4:30 AM CT (Shane review of P2-A-101/102 Rev A).

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
| D-007 | Owner of record for the new building: Shane / Hazel Green Trojan Youth Wrestling / partnership | OPEN | Drives D-008 and R-006. **Updated 2026-10-03 10:45 PM CT (Shane):** Phase 2 is Shane's build, not a school project (D-028), so the school-system/county/town options were dropped from this question. phase2.yaml `open_items.owner_of_record` |
| D-008 | Authority Having Jurisdiction for permitting | OPEN | R-006. **Note 2026-10-03 (P2-T-003b):** Madison County's Building Codes page lists the 2018 IBC/IPC (effective Jan 2021) for county permits; Shane said 2021. The test-fit used 2021; its fixture table reads the same in 2018. Depends on the site (D-006) |
| D-009 | Seating type (fixed, telescopic) and final count | DECIDED | DECIDED 2026-10-04 — MIX: telescopic lower tier, fixed upper tier — "Shane, firsthand, 4:30 AM CT". Total stays 2,200 (locked; D-016 label question still OPEN), seats on N, S, E only (west = lockers + athlete corridor), 50/50 tier split ASSUMED (1,100 + 1,100). phase2.yaml `spaces.seating.type` MIX, `lower_tier_type: telescopic`, `upper_tier_type: fixed` (locked in validate.py). P2-G-003 Rev E (Rev D frozen): telescopic 3.38 SF/seat lower, fixed 6.0 SF/seat upper, same 1.25 gross-up → L1 gross 51,108, L2 gross 25,981, footprint 51,130 (arena volume + L2 governs) = 3,870 SF under 55,000 (target ≥ 2,000 met); 77,089 GSF. Block box shrinks 250 × 220 → 204 × 252 ft = 51,408 SF (3,592 under the cap). Seats by side: N 353 + 308 = 661, S 341 + 308 = 649, E 406 + 484 = 890 (lower 1,100 + upper 1,100 = 2,200). Earlier note: concept sheet shows 2,200; diorama text "Permanent stadium seating" not treated as a decision; Rev D compared fixed 54,949 vs telescopic 50,868 |
| D-010 | Locker room parity (equal SF?) | OPEN | See D-013 |
| D-011 | Concessions scope | OPEN | |
| D-012 | Any budget target for Phase 2 | OPEN | Do not reuse the superseded Feb 2026 concept budget |

## Logged at bootstrap (2026-10-03)

| ID | Question | Status | Notes / feeds |
|---|---|---|---|
| D-013 | Girls locker 3,503 SF vs boys 3,500 SF. Real difference, or a drawing-tag slip? | OPEN | Prompt §3 says this is likely a tag slip. **Draw both lockers equal until Shane decides.** Also, the intake says AI renders show girls as 3,500 |
| D-014 | Mat size check: concept notes say "four 42-foot mats ≈ 7,000 SF." Check against current NFHS rules (mat, circle, safety area, spacing) before laying out mats | DECIDED | DECIDED 2026-10-03 — mats are 42' × 42' — "Shane, 10:45 PM CT". R-005: meets the NFHS 28 ft minimum circle + ~5 ft safety area. Applied in phase2.yaml `spaces.arena.mat_size`. Design events → D-029 |
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

## Logged 2026-10-03 10:45 PM CT (Phase 2 active)

| ID | Question | Status | Notes / feeds |
|---|---|---|---|
| D-027 | Does Phase 2 wait for Phase 1 to finish? | DECIDED | DECIDED 2026-10-03 — Phase 2 is ACTIVE now, in parallel with Phase 1. Phase 1 package delivered; Phase 1 waits on Dr. Headen. When Shane brings Phase 1 data, Phase 1 tickets jump the line (Phase 1 still outranks when its data exists) — "Shane, 10:45 PM CT". Applied in BACKLOG priority note, STATUS, README, phase2.yaml meta |
| D-028 | Is Phase 2 a school project? | DECIDED | DECIDED 2026-10-03 — No. Phase 2 is Shane's build; it may not involve Dr. Headen. No school ownership, district approval, school review or school bidding is assumed for Phase 2 — "Shane, 10:45 PM CT". Owner of record stays OPEN (D-007). phase2.yaml had no school-derived entries to remove; locked facts kept |
| D-029 | What events is the Phase 2 arena designed for? | DECIDED | DECIDED 2026-10-03 — home duals + AHSAA / regional tournaments — "Shane, 10:45 PM CT". phase2.yaml `spaces.arena.design_events` |
| D-030 | Program direction (two levels, footprint cap D-031). Shane's direction under study (11:26 PM CT): keep ≈ 2,200 spectators with rentable suites just above the top seats. P2-G-003 Rev C (base inputs): at the locked 22,000 SF floor, suites cannot reach 2,200 inside 55,000 (most that fits ≈ 1,640 = 1,180 bowl + 23 suites × 20); an 18,000 SF floor fits 1,940 bowl + 13-22 suites (12-20 guests) ≈ 2,200, footprint ≈ 54,994, ≈ 92,300-92,900 GSF, 3 levels (suite level). Which way: a) 18,000 SF floor + suites (3 levels), b) 16,400 SF floor, all 2,200 in the bowl, no suites (2 levels), c) keep 22,000 SF on lean inputs (telescopic lower tier), no suites (2 levels), or d) another mix? | DECIDED | DECIDED 2026-10-03 — 16,400 SF event floor, all 2,200 seats in the bowl, 2 levels, no suites — "Shane, firsthand, 11:39 PM CT". Suites → PARKING_LOT (future add-on, study after attendance is proven). Seating type (fixed vs telescopic) stays OPEN (D-009); plans show both as an overlay. phase2.yaml locked: `spaces.arena.event_floor_sf: 16400` (drawn 114 × 144 ft = 16,416), 4 × 42 ft mats 2 × 2 (`mat_ft`, `mat_layout`), `seating.bowl: 2200`, `building.levels: 2`, S&C + cross-training `level: 2` over the lockers; the 22,000 SF tag is SUPERSEDED for the event floor and kept as history (`sf_tagged_superseded`). P2-G-003 Rev D = LOCKED PROGRAM sheet (Rev C frozen). Feeds P2-T-004 (P2-A-101 Level 1, P2-A-102 Level 2) |

## Logged 2026-10-03 11:09 PM CT

| ID | Question | Status | Notes / feeds |
|---|---|---|---|
| D-031 | Is the 55,000 SF a cap on total floor area or on the building footprint? | DECIDED | DECIDED 2026-10-03 — 55,000 SF is a FOOTPRINT cap that could allow two levels; it is not a total floor area cap — "Shane, firsthand, 11:09 PM CT". phase2.yaml `building.footprint_cap_sf: 55000`, `levels: up to 2`, `total_gsf_cap: none` (locked `total_sf: 55000` kept, meaning noted). Test-fit redone as P2-G-003 Rev B; Rev A frozen. D-030 stays OPEN |

## Logged 2026-10-03 11:26 PM CT

| ID | Question | Status | Notes / feeds |
|---|---|---|---|
| D-032 | Keep the 22,000 SF floor and drop to ≈ 1,370 seats (P2-G-003 Rev B option)? | DECIDED | DECIDED 2026-10-03 — No. Shane rejects the ≈ 1,370-seat option ("not enough") — "Shane, firsthand, 11:26 PM CT". His direction (suites just above the top seats to keep ≈ 2,200 spectators) is recorded under D-030, which stays OPEN until he picks. phase2.yaml `spaces.seating.rejected_option`, `suites_direction` |

## Logged 2026-10-04 4:43 AM CT

| ID | Question | Status | Notes / feeds |
|---|---|---|---|
| D-033 | Access control: how do people (public, teams, staff) enter the arena? | DECIDED | DECIDED 2026-10-04 — single controlled entry point for all people (public, teams, staff): "Everyone passes through the grand entrance; it will serve as a checkpoint, a security feature." — "Shane, firsthand, 4:43 AM CT". phase2.yaml `spaces.entry.access_control` (v7). P2-A-101/102 Rev C (Rev B frozen): SW team / service entry removed; SECURITY CHECKPOINT (size TBD, ASSUMED) between the vestibule and lobby; CD-1 controlled door off the lobby → athlete route → team assembly / athlete corridor / lockers; all other perimeter doors X1-X10 EXIT ONLY — alarmed, no exterior entry hardware (IBC 2021 1010.2, 1010.2.7 exc. 1, 1010.2.9; 2018 1010.1.9, 1010.1.10; no delayed egress in Group A, 1010.2.13). Exits kept per R-015 / R-015.6: 4 per story (T1006.3.3), main exit ≥ 1/2 occupant load (1030.2), other exits ≥ 1/2 (1030.3); checkpoint may not narrow the main exit (1003.6, 1010.5). Program unchanged (P2-G-003 Rev E stands) |
| D-034 | Deliveries and team buses under the single-entry rule (D-033): where do trucks unload mats / equipment and concessions, and where do team buses drop athletes and gear? Rev C shows S1 SERVICE / LOADING at equipment storage (north wall) — staff-controlled, not a people entrance — and teams walking in through the grand entrance. Options: a) staff-only service door as drawn, deliveries scheduled outside event hours; b) a screened service / loading entrance with its own checkpoint; c) other | OPEN | No sizes set (dock, door, apron, bus lane all TBD; site TBD, D-006). Feeds P2-A-101 (S1), C-101 campus diagram (P2-T-006), D-011 concessions scope |

## Logged 2026-10-04 4:55 AM CT

| ID | Question | Status | Notes / feeds |
|---|---|---|---|
| D-035 | Should Level 2 have a complete, continuous walkway / running-training loop around the top, and what gives up space for it? | DECIDED | DECIDED 2026-10-04 — continuous L2 running / training loop joining the rear walkway (N), walkway (E) and upper concourse / hall of champions balcony (S); S&C and cross-training reduced to fit — "Shane, firsthand, 4:55 AM CT". Shane wrote "eastside", but rooms 17 and 18 sit on the west, so the new leg runs along their arena-side (east) edge. phase2.yaml v8: `spaces.strength_conditioning.sf` 6,000 → **5,224**, `spaces.cross_training.sf` 4,000 → **3,500** (old values kept as `sf_tagged_superseded` for frozen revisions), new `spaces.training_loop`. Loop = 2 lanes x 42 in = 7 ft all around (lane width UFC 4-740-02N 4.1.7 / Athletic Business, R-017; 2 lanes ASSUMED, guides prefer 3), squared corners, 706 ft centerline, 7.48 laps/mile, 4,942 SF. 42 in guards at open edges (IBC 2021 1015.2, 1015.3). Event days: upper concourse (spectators cross at tier entries). P2-A-101/102 Rev D (ST-1 3.55 ft W, ST-2 into a 19 x 5 ft NE stair tower, elevator 1 ft S); P2-G-003 Rev F footprint 52,738, margin 2,262, 78,784 GSF |


## Logged 2026-10-04 5:27 AM CT

| ID | Question | Status | Notes / feeds |
|---|---|---|---|
| D-036 | Are P2-A-101/102 Rev D and P2-G-003 Rev F approved as the Phase 2 schematic baseline? | DECIDED | DECIDED 2026-10-04 — "P2-A-101/102 Rev D + P2-G-003 Rev F approved. Entry south-center, mech off the public side, mixed seating, 2,262 margin — all good." — "Shane, firsthand, 5:27 AM CT". Frozen as **Phase 2 Schematic Set Rev A** (phase2.yaml `sets.phase2_schematic_set_rev_a`; bundle `phase2/out/pdf/Phase2_Schematic_Set_RevA.pdf`, `p2_set.py`; git tag `p2-schematic-revA`). P2-A-101 Rev D was re-issued label-only for D-039 before the freeze. Confirms D-009 (MIX), D-033 (south-center entry), footprint margin 2,262 SF (P2-G-003 Rev F). |
| D-037 | Level 2 running / training loop width | DECIDED | DECIDED 2026-10-04 "for now" — 2 lanes x 42 in = 7 ft (D-035 geometry unchanged) — "Shane, firsthand, 5:27 AM CT". Revisit only through D-038. |
| D-038 | Upper concourse width vs egress calc — if code requires wider, go to 3 lanes (10.5 ft). | OPEN | Opened by Shane 2026-10-04 5:27 AM CT. R-018 (IBC 2021 Ch. 10 via UpCodes; 2018 = 1029.x, UNVERIFIED): L2 load 1,279; loop at 0.2 in/occupant needs 64 in (balanced, 1030.9.2) / 79.2 in (unbalanced check) vs 84 in drawn → **code does not require > 7 ft on KEYSTONE's calc**; 10.5 ft (126 in) would also satisfy it. Thin margin: keep the 7 ft clear, recess room doors. Stairs 4 x 64 in = zero slack (≈ 68-69 in if the AHJ counts the loop or rail standing). Needs architect egress model + AHJ (D-008). Frozen set unchanged. |
| D-039 | West unprogrammed space on Level 1 (team assembly ≈ 2,072 SF, storage SW 1,011 SF): keep or change? | DECIDED | DECIDED 2026-10-04 — keep as-is, labeled FLEX — "Shane, 5:27 AM CT". His message left the template bracket "keep as-is, labeled flex — [or: change to ___]"; KEYSTONE took the stated default (KEEP AS-IS) and did not invent a change. Labels: "FLEX / TEAM ASSEMBLY", "FLEX / STORAGE" (P2-A-101 Rev D label-only re-issue before the freeze; geometry, areas and DXF non-text entities unchanged). |
| D-040 | Brand / signage on the south portal and arena faces: does the Hazel Green High School (HGHS) badge belong, or Shane's own complex brand? | OPEN | Opened by KEYSTONE 2026-10-04 for P2-A-201. Phase 2 is Shane's build, not a school project (D-028), so no school logo is drawn; placeholder "BRAND / SIGNAGE — TBD" in brand red / black. Portal look (limestone arch, crimson inside the arch, gold soffit) from Shane's MOVIE MAKER arch render (`/workspace/trojan-horse-arena/assets/arch_src.png`, box only). Needs Shane. |
