# R-009 — Occupant load and plumbing fixture counts for the Phase 2 arena (2,200 seats)

Researched by KEYSTONE 2026-10-03 for P2-T-003b (program test-fit, sheet P2-G-003). All sources retrieved 2026-10-03.
Status: research note for a test-fit. Not a plumbing design. **PRELIMINARY — CONCEPTUAL DESIGN — NOT FOR CONSTRUCTION.** Formal occupancy classification is R-007 (not done); A-4 is ASSUMED here.

**Code edition note:** computed with **IBC/IPC 2021** as Shane asked. **Madison County's Building Codes page lists the 2018 IBC/IPC** (effective Jan 2021). The 2018 IBC Table 2902.1 row for arenas was checked and **reads the same** as 2021, so the fixture counts below do not change between the two editions. AHJ OPEN (D-008).

## Sources
- **S1** — IBC 2021 Chapter 29 (UpCodes, Alabama Building Code 2021) — https://up.codes/viewer/alabama/ibc-2021/chapter/29/plumbing-systems — retrieved 2026-10-03. PRIMARY (via viewer).
- **S2** — IBC 2021 Chapter 10 (UpCodes) — https://up.codes/viewer/alabama/ibc-2021/chapter/10/means-of-egress — retrieved 2026-10-03. PRIMARY (via viewer).
- **S3** — IPC 2021 Chapter 4 (UpCodes, Alabama) — https://up.codes/viewer/alabama/ipc-2021/chapter/4/fixtures-faucets-and-fixture-fittings — retrieved 2026-10-03. PRIMARY (via viewer).
- **S4** — IBC 2018 Chapter 29 (UpCodes, Texas edition, used only to compare the model table) — https://up.codes/viewer/texas/ibc-2018/chapter/29/plumbing-systems — retrieved 2026-10-03.
- **S5** — Madison County, AL, "Building Codes" — https://www.madisoncountyal.gov/departments/inspection/building-codes — retrieved 2026-10-03. PRIMARY.
- **S6** — American Specialties Inc., "2 Stall Restroom Layout: Dimensions and ADA Requirements" (Apr 2025) — https://americanspecialties.com/2-stall-restroom-layout-dimensions-and-ada-requirements/ — retrieved 2026-10-03. MANUFACTURER (secondary).

---

## R-009.1 — Occupant load

QUESTION: What occupant load drives the fixture count?

ANSWER (one paragraph): **2,640 (test-fit value) = 2,200 seats + 440 on the event floor.** IBC 1004.6: "For areas having fixed seats and aisles, the occupant load shall be determined by the number of fixed seats installed therein. The occupant load for areas in which fixed seating is not installed … shall be determined in accordance with Section 1004.5 and added to the number of fixed seats." The 22,000 SF event floor has no fixed seats. Table 1004.5 lists no "arena floor" use; 1004.5 says the building official picks the nearest listed function. **KEYSTONE ASSUMED "Exercise rooms — 50 gross"**: 22,000 ÷ 50 = **440**. Other Table 1004.5 choices would change this a lot: "Assembly without fixed seats — unconcentrated (tables and chairs) 15 net" would give ~1,467; "standing space 5 net" far more. The athlete spaces (lockers, S&C, cross-training) are left out of the public count; the test-fit assumes their toilets sit inside the locker-room tags.

SOURCE: S2 (IBC 2021 1004.5, Table 1004.5, 1004.6).

EDITION / SECTION: IBC 2021 §1004.5, Table 1004.5, §1004.6.

CONFIDENCE: HIGH for the seat count rule; LOW for the floor factor (a choice the building official makes).

NEEDS ARCHITECT CONFIRMATION: YES.

---

## R-009.2 — Fixture ratios (IBC 2021 Table 2902.1)

QUESTION: What does the code require for an indoor arena?

ANSWER (one paragraph): Table 2902.1, Assembly, "**Coliseums, arenas, skating rinks, pools and tennis courts for indoor sporting events and activities**" (S1):
- Water closets, male: "1 per 75 for the first 1,500 and 1 per 120 for the remainder exceeding 1,500"
- Water closets, female: "1 per 40 for the first 1,520 and 1 per 60 for the remainder exceeding 1,520"
- Lavatories: male 1 per 200; female 1 per 150
- Drinking fountains: 1 per 1,000
- Other: 1 service sink

2902.1.1: "To determine the occupant load of each sex, the total occupant load shall be divided in half"; fractions are rounded up (for multiple occupancies, fractions are summed first, then rounded). Urinals (S3, IPC 2021 424.2): "urinals shall not be substituted for more than **67 percent** of the required water closets in assembly and educational occupancies." 2902.3.3: public toilets no more than one story away and within 500 ft travel. 2903.1.1: water closet compartments at least 30 in × 60 in (floor-mounted). The 2018 IBC table (S4) has the identical arena row.

SOURCE: S1, S3, S4.

EDITION / SECTION: IBC 2021 Table 2902.1, §§2902.1.1, 2902.3.3, 2903.1.1; IPC 2021 §424.2.

CONFIDENCE: HIGH.

NEEDS ARCHITECT CONFIRMATION: YES (occupancy and load).

---

## R-009.3 — Fixture counts for this building (arithmetic)

QUESTION: How many fixtures, and how much floor area?

ANSWER (one paragraph): Load 2,640 → 1,320 per sex.
- WC men: 1,320 ÷ 75 = 17.6 → **18** (up to 12 may be urinals, 67%)
- WC women: 1,320 ÷ 40 = 33.0 → **33**
- Lavatories: men 1,320 ÷ 200 = 6.6 → **7**; women 1,320 ÷ 150 = 8.8 → **9**
- Drinking fountains: 2,640 ÷ 1,000 → **3**; service sink **1**

**67 fixtures in the toilet rooms (WC + urinals + lavatories).** Area: **50 SF per fixture is ASSUMED** (no published SF-per-fixture planning factor was found). Check: a bare water-closet module from cited minimums is 36 in × 60 in stall (S6; code minimum is 30 in × 60 in) plus a 48 in aisle in front (S6 recommends 42–48 in) ≈ 15 + 12 = 27 SF. 50 SF/fixture adds lavatory clear floor space (30 × 48 in), accessible stalls (60 in wide), entries and pipe chases. 67 × 50 = **3,350 SF**, split across the 2 public restrooms on the reference plan. Drinking fountains (concourse alcoves) and the service sink (utility room, TBD) are not in that area. If the event floor were counted as unconcentrated assembly (~1,467), the load would be ~3,667 and the counts would rise (WC men 23, women 44, by the same table).

SOURCE: arithmetic from R-009.1–.2; S6 for stall sizes.

EDITION / SECTION: as above.

CONFIDENCE: HIGH for counts at the stated load; LOW for SF per fixture (ASSUMED).

NEEDS ARCHITECT CONFIRMATION: YES.

---

## Gaps and conflicts
1. Edition: 2021 per Shane vs 2018 on Madison County's page; same table values. AHJ OPEN (D-008); R-006 not done.
2. Event-floor occupant factor is a building-official choice; 50 gross is ASSUMED.
3. R-007 (occupancy classification) not done; A-4 assumed.
4. No published SF-per-fixture factor found; 50 SF ASSUMED.
5. Family/assisted-use toilet rooms (IBC 1110.2.1) and accessible fixture counts not done.
