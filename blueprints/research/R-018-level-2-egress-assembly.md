# R-018 — Level 2 egress: occupant load, stair and concourse (loop) capacity, assembly aisles, travel, guards, event-day cross-flow

Researched by KEYSTONE 2026-10-04 for D-038 (OPEN: "Upper concourse width vs egress calc — if code requires wider, go to 3 lanes (10.5 ft)"), after Shane approved P2-A-101/102 Rev D + P2-G-003 Rev F (5:27 AM CT). Geometry: params/phase2_plan_rev_d.yaml (frozen, Phase 2 Schematic Set Rev A). Builds on R-015 (stairs, sprinklers + voice alarm) and R-017 (track lanes, guards).
Status: research note, not a code review. KEYSTONE is not an architect or code official: the occupant load, catchments and widths must be confirmed by the architect of record and the AHJ (D-008). No legal advice.

## Sources
- **S1** — IBC 2021, Chapter 10 Means of Egress (Alabama), UpCodes viewer — https://up.codes/viewer/alabama/ibc-2021/chapter/10/means-of-egress — retrieved 2026-10-04 (full chapter text saved on the box, not committed). PRIMARY via a free viewer; the ICC original is paywalled / script-only.
- **S2** — IBC 2018 text, secondary copies seen as search excerpts on 2026-10-04: a flipbuilder copy of the 2018 code, §1029.6 / 1029.6.1 / Table 1029.6.2 (https://online.flipbuilder.com/mewf/msoi/files/basic-html/page323.html), and UpCodes 2018 IBC state viewers (Texas, Illinois) showing the 1005.3.1 / 1005.3.2 exceptions pointing to §1029 (https://up.codes/viewer/texas/ibc-2018/chapter/10/means-of-egress, https://up.codes/viewer/illinois/ibc-2018/chapter/10/means-of-egress). **UNVERIFIED**: excerpts only, not the full chapter, and not the Alabama/Madison County adoption; ICC original (https://codes.iccsafe.org/content/IBC2018/chapter-10-means-of-egress) is paywalled / script-only.
- **S3** — R-015 §R-015.5: IBC 2021 903.2.1.4 (sprinklers, Group A-4) and 907.2.1.1 (emergency voice/alarm, Group A ≥ 1,000 occupants), retrieved 2026-10-03.
- **S4** — Athletic Business, "Designing Tracks for Recreational Users" (users crossing a track are a hazard) — see R-017, retrieved 2026-10-04. TRADE PRESS.
- Not reviewed (paywalled): NFPA 101 (life safety evaluation required by IBC 1030.6.2 for smoke-protected seating), ICC 300 (bleachers / telescopic seating, governs the L1 lower tier).

Edition note: Madison County lists the 2018 IBC for county permits; Shane said 2021 (D-008 OPEN). The assembly section is **1029 in 2018 and 1030 in 2021** (same subsection numbers: 1029.6 ↔ 1030.6, 1029.7 ↔ 1030.7 …). S2 shows 2018 1029.6.1 with the same aisle factors as 2021 1030.6.1, the same Table 1029.6.2 values (≤ 5,000 seats: 0.200 / 0.250 / 0.150 / 0.165) and the same 1005.3.1 / 1005.3.2 sprinkler + voice-alarm exceptions (0.2 / 0.15 in). 1004.5, 1005.3, 1015, 1017.2 and 1020.3 keep their numbers; their 2018 text was not re-read (UNVERIFIED).

## R-018.1 Level 2 occupant load (event day)

| Space | Basis (S1) | Area | Load |
|---|---|---|---|
| Upper tier, fixed seats | 1004.6 (number of fixed seats) | — | 1,100 |
| S&C (17) | T1004.5 exercise rooms, 50 gross | 5,224 SF | 5,224 / 50 = 104.5 → 105 |
| Cross-training (18) | T1004.5 exercise rooms, 50 gross | 3,500 SF | 3,500 / 50 = 70 |
| Admin (21) | T1004.5 business areas, 150 gross | 470 SF | 470 / 150 = 3.1 → 4 |
| Restrooms, loop, corridor, stretch strip | circulation / accessory (same people) | — | not added |
| **Total** | | | **1,279** (= P2-G-003 Rev F) |

Sensitivities (AHJ decisions, not KEYSTONE's): (a) loop counted as an exercise room while seats are full: 4,942 / 50 = 98.8 → 99, total 1,378; (b) spectators standing at the west-leg rail over the arena counted as standing space (T1004.5, 5 net): e.g. a 2.5 ft strip x 168 ft = 420 SF / 5 = 84 (strip depth ASSUMED), total 1,363. The table also lists "concourse 100 gross", but only under airport terminals.

1,279 > 1,000 → **4 exits from Level 2** (T1006.3.3) = the 4 stairs. 1030.5: a balcony / gallery with ≥ 50 seats needs 2 means of egress, one from each side — the loop gives both directions on every side.

## R-018.2 Stair capacity (1005.3.1)

1005.3.1: 0.3 in per occupant; **exception 1** (all but H and I-2): 0.2 in per occupant with sprinklers (903.3.1.1) + emergency voice/alarm (907.5.2.2), both required here anyway (S3). Exception 2 allows Table 1030.6.2 stepped-aisle factors only for smoke-protected seating with a 909 smoke-control system along the whole path.

- 1,279 x 0.2 = **255.8 in** total → 4 stairs x 64 in (P2-G-003 Rev F: 63.95 in). **Zero slack.**
- Without the exception: 1,279 x 0.3 = 383.7 in → 96 in per stair.
- Sensitivity (a): 1,378 x 0.2 = 275.6 in → 69 in per stair; (b): 1,363 x 0.2 = 272.6 in → 68 in per stair.
- 1005.5: losing any one stair leaves 3 x 64 = 192 in ≥ 50% x 255.8 = 127.9 in ✓.
- 1030.6.1 (0.3 in stepped / 0.2 in level, no sprinkler reduction) applies to **aisles** in the seating, not to the exit stairs (2021 title "Capacity of aisle for assembly"; same in 2018 per S2).

## R-018.3 The loop as the upper concourse (egress path to the stairs)

Width factor: where the loop is the cross aisle behind the seats it is an assembly aisle → **0.2 in per occupant** for level aisles (1030.6.1 item 4; no sprinkler reduction). As an "other egress component" it could use 0.15 in (1005.3.2 exc. 1); KEYSTONE uses the stricter 0.2.

Catchment: 1030.9.2 — assume **balanced use of all means of egress, people in proportion to egress capacity**. 4 equal stairs → 1,279 / 4 = 319.75 → 320 per stair. Rooms go straight to a stair (S&C 105 → ST-1; cross-training 70 + admin 4 → ST-4 via the L2 corridor), so the loop carries seat occupants only:

| Path on the loop | Occupants | Required width (x 0.2 in) |
|---|---|---|
| into ST-2 (NE corner, from N + E legs) | 320 | 64.0 in |
| into ST-3 (SE corner → upper concourse E) | 320 | 64.0 in |
| into ST-4 (SW corner → L2 corridor) | 320 − 74 = 246 | 49.2 in |
| into ST-1 (W leg) | 320 − 105 = 215 | 43.0 in |
| **Unbalanced check** (each tier side splits to its two end stairs: N 308 → 154 + 154; E 484 → 242 + 242; S 308 → 154 + 154; NE and SE corners each take 154 + 242) | 396 | **79.2 in** |
| Loop as drawn | — | **84 in (7 ft)** |

Minimum widths: 36 in level aisle with seating on one side (1030.9.1); 44 in corridor (T1020.3) if the AHJ calls it a corridor; 36 in accessible route. 84 in clears all of them. 1030.9.4: a path usable in two directions must be uniform in width — the loop is a uniform 7 ft. Dead ends (1030.9.5): none on a continuous loop. 1005.4: width may not shrink toward the exit — the corners and the paths to ST-3 (35 ft concourse) and ST-4 (49 ft corridor) are wider.

Clear width is measured to walls, edges of seating and tread edges, with no obstructions (1030.9.6, 1030.9.6.1). At the worst-case corner the spare width is 84 − 79.2 = **4.8 in**; in the balanced case 20 in.

Doors onto the loop: S&C and cross-training each hold ≥ 50 people, so their doors swing out into the loop (1010.1.2.1). 1005.7.1: a fully open door may take ≤ 7 in of the required width and ≤ 1/2 in any position (a 36 in leaf swinging into 84 in leaves 48 in ≥ 39.6 in, OK) — recessed door alcoves keep the lanes clear. Stair doors swing into the stairs.

## R-018.4 Travel distance, common path, aisles

- T1017.2 (1030.7): Group A, sprinklered, **250 ft** exit access (400 ft total if smoke-protected). Rough worst cases measured along the plan (stepped aisle ≈ 15 ft + loop + to the stair door): E-tier middle → ST-2 ≈ 15 + 102.5 + 10 ≈ **128 ft**; S-tier middle → ST-3 ≈ 15 + 81.5 + 26.7 ≈ 123 ft (→ ST-4 ≈ 141 ft); N-tier middle → ST-1 ≈ 86 ft; S&C far corner → ST-1 ≈ 136 ft; cross-training far corner → ST-4 ≈ 127 ft. All < 250 ft.
- 1030.8: common path ≤ 30 ft from any seat to a choice of two paths. The upper tier is only 15 ft deep, so a stepped aisle reaches the loop (two directions) within ≈ 15 ft; row layout is not drawn, so rows with an aisle at each end (1030.13.2.1) are ASSUMED.
- 1030.9.1: stepped aisles 48 in (seats both sides) / 36 in (one side); handrails per 1030.16; aisle capacity 0.3 in per occupant on stepped aisles with ≤ 7 in risers (1030.6.1).

## R-018.5 Guards and handrails

- Loop open edges (west over the arena / athlete corridor, south over the lobby): drop ≈ 15 ft > 30 in → **42 in guards** (1015.2, 1015.3), 4 in sphere (4-3/8 in from 36 to 42 in) (1015.4).
- Upper tier: perimeter guards (1030.17.1) at the arena edge — 42 in from the seatboard where seats are next to the edge, or a 26 in sightline-constrained guard (1030.17.3); 36 in rail at the foot of each stepped aisle (1030.17.4). Where the loop is the cross aisle at the back of the tier: guard per 1015 if the drop is > 30 in, 26 in if ≤ 30 in, none if the seat backs stand ≥ 24 in above the aisle (1030.17.2). The tier section is not drawn, so which applies is TBD (architect).
- Handrails: none required on the level loop; stepped aisles need them (1030.16); stairs need them (1011.11, 1014).

## R-018.6 Event-day cross-flow

Everyone enters at the L1 grand entrance (D-033), so ingress to the upper tier comes up the south stairs / elevator and walks along the loop to the N and E tiers; egress at the end splits to all 4 stairs. Conflicts: training users vs spectators (S4: crossing users are a hazard); S&C / cross-training users stepping out onto the loop; restroom and concession queues on the south leg; spectators stopping at the west rail to watch. Recommendation (operational, not code): the loop is closed to running from doors-open until the building clears; lane markings and crossing marks at tier entries and stair doors; queue space off the loop; no standing / viewing zone inside the 7 ft (or the AHJ may count it, sensitivity b).

## R-018.7 Conclusion (D-038)

QUESTION: Does code require the upper concourse / loop to be wider than 7 ft?

ANSWER: **No, not on this calculation.** At 0.2 in per occupant the loop needs 64 in with balanced use of the 4 stairs (1030.9.2) and 79.2 in in a deliberately unbalanced check; 7 ft = 84 in. All minimum widths (36 / 44 in) are met. **3 lanes (10.5 ft = 126 in) would satisfy it** with 46.8 in to spare and would absorb queues, standing at the rail or an AHJ load increase. The 7 ft works only if it stays **clear** (no columns, guard posts, queues or doors in the lanes; ≤ 4.8 in of projections in the worst case). The loop would need to exceed 84 in only if more than 420 people (84 / 0.2) were assigned to one loop path.

The tighter item is the **stairs**: 4 x 64 in = 255.8 in required, zero slack; if the AHJ counts the loop (a) or rail standing (b), each stair grows to ≈ 68-69 in. Recommendation: no change to the frozen set; carry D-038 OPEN for the architect's egress model and the AHJ (D-008); when the stairs are detailed, size them ≈ 70 in or more (or add capacity), and keep the loop clear.

EDITION / SECTION: IBC 2021 §§1004.5 (Table), 1004.6, 1005.3.1, 1005.3.2, 1005.4, 1005.5, 1005.7.1, 1006.3.3 (Table), 1010.1.2.1, 1015.2-1015.4, 1017.2 (Table), 1020.3 (Table), 1030.5, 1030.6.1, 1030.6.2, 1030.7, 1030.8, 1030.9.1-1030.9.6, 1030.13.2, 1030.16, 1030.17. 2018: 1029.x for the assembly sections (S2, UNVERIFIED).

CONFIDENCE: HIGH for the code factors (2021 text read) / MEDIUM for the 2018 equivalence / LOW for the occupant distribution (tier aisles, vomitories and the tier section are not designed).

NEEDS ARCHITECT CONFIRMATION: YES (occupant load classification, catchments, stair widths, guard types, smoke protection, final egress plan).
