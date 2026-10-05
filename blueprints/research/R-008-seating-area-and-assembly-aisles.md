# R-008 — Spectator seating area for 2,200 seats: SF per seat, assembly aisles, row spacing (Phase 2)

Researched by KEYSTONE 2026-10-03 for P2-T-003b (program test-fit, sheet P2-G-003). All sources retrieved 2026-10-03.
Status: research note for a test-fit. Not a seating layout. Seating type is OPEN (D-009); the 2,200 total is locked (D-016 still OPEN on the plan labels). **PRELIMINARY — CONCEPTUAL DESIGN — NOT FOR CONSTRUCTION.**
Format follows prompt §10. Covers the seating-area part of R-008 (egress). Exit counts, exit widths and travel distance are NOT done yet (later, with R-007 and a plan).

**Code edition note:** Shane said Alabama uses the 2021 IBC. The text below is the 2021 IBC as published on UpCodes ("Alabama Building Code 2021"). **But Madison County's Building Codes page lists the 2018 IBC/IPC** (effective January 2021) for county permits. Phase 2 is a private build (D-028), so the AHJ is probably local and is OPEN (D-008). **Section numbers:** the 2021 IBC puts assembly egress in **Section 1030** (Section 1029 is Egress Courts). The same rules were Section 1029 in the 2018 IBC, which is why "IBC 1029" is commonly quoted.

## Sources
- **S1** — IBC 2021, Chapter 10, as published by UpCodes (Alabama Building Code 2021) — https://up.codes/viewer/alabama/ibc-2021/chapter/10/means-of-egress — retrieved 2026-10-03. PRIMARY (code text via a third-party viewer; codes.iccsafe.org would not render without a login).
- **S2** — Madison County, AL, "Building Codes" — https://www.madisoncountyal.gov/departments/inspection/building-codes — retrieved 2026-10-03. PRIMARY.
- **S3** — Loudoun County, VA, *Capital Facilities Manual* (June 2014), §4.3 Recreation Center standard area requirement — https://www.loudoun.gov/DocumentCenter/View/123942/Attach-2---Pre-Program-Summary?bidId= — retrieved 2026-10-03. PUBLISHED PLANNING STANDARD (another jurisdiction, 2014).
- **S4** — Hussey Seating, *MAXAM Telescopic Systems* brochure — https://husseyseatway.com/wp-content/uploads/2025/03/MAXAM_Brochure.pdf — retrieved 2026-10-03. MANUFACTURER (secondary).
- **S5** — Hussey Seating, ARCAT spec 12 60 00 Telescopic Stands — https://www.arcat.com/specification/hussey-seating-co-33161/12_60_00hsy — retrieved 2026-10-03 (search excerpt). MANUFACTURER (secondary).

---

## R-008.1 — Area per seat for planning (base case)

QUESTION: What area per seat (including aisles) should a test-fit use for 2,200 seats?

ANSWER (one paragraph): **Base case: 6.0 SF per seat.** Loudoun County's recreation-center standard (S3) allots a "Spectator/Team Seating" area of 4,800 SF for its stated seat count, noting "Area can be reduced with use of tip-and-roll bleachers … Elevated seating preferred." 4,800 ÷ that seat count = **6.0 SF/seat** (arithmetic from S3). For 2,200 seats: 2,200 × 6.0 = **13,200 SF**. (S3's seat count is not repeated in params because that number collides with a superseded concept number blocked by validate.py; it is a different project.) No US building code gives an area per seat; codes control aisle and row widths (R-008.2).

SOURCE: S3.

EDITION / SECTION: Loudoun County Capital Facilities Manual, June 2014, §4.3 Recreation Center, "Program Space — Spectator/Team Seating".

CONFIDENCE: MEDIUM (a published public planning standard, but for a natatorium seating area in 2014, not an arena).

NEEDS ARCHITECT CONFIRMATION: YES.

---

## R-008.2 — Code limits that set the seating geometry (IBC 2021)

QUESTION: Which code rules set row spacing, row length and aisle widths?

ANSWER (one paragraph): From S1 (IBC 2021):
- **1004.6 Fixed seating:** occupant load = number of fixed seats; "For areas having fixed seating without dividing arms, the occupant load shall be not less than the number of seats based on one person for each **18 inches** … of seating length."
- **1030.1.1 Bleachers:** bleachers, grandstands and folding/telescopic seating that are not building elements "shall comply with **ICC 300**." (ICC 300 not read; paywalled.)
- **1030.1.1.1:** spaces under grandstands or bleachers need 1-hour fire barriers, except ticket booths under 100 SF, toilet rooms, and other accessory areas of 1,000 SF or less with sprinklers. (Matters for DR3 rooms "under the bowl".)
- **1030.9.1 Minimum aisle width:** **48 in** for stepped aisles with seating on both sides (36 in if serving fewer than 50 seats); 36 in with seating on one side; 42 in for level/ramped aisles with seating on both sides.
- **1030.13.2 Aisle accessways:** rows of 14 or fewer seats need at least **12 in** clear between the back of one row and the nearest projection of the row behind.
- **1030.13.2.1 Dual access:** with aisles at both ends, max **100 seats per row**; the 12 in minimum grows 0.3 in per seat beyond **14 seats (with backrests)** or **21 seats (without backrests)**, up to 22 in.
- **1030.6.1 Aisle capacity (no smoke protection):** 0.3 in per occupant on stepped aisles (risers ≤ 7 in, treads ≥ 11 in); 0.2 in per occupant on level or ramped aisles ≤ 1:12.
- **1030.8 Common path:** 30 ft max from any seat to a choice of two paths (50 ft smoke-protected).

SOURCE: S1.

EDITION / SECTION: IBC 2021 §§1004.6, 1030.1.1, 1030.1.1.1, 1030.6.1, 1030.8, 1030.9.1, 1030.13.2, 1030.13.2.1. (2018 IBC: same rules numbered 1029.x — not re-checked line by line.)

CONFIDENCE: HIGH for the 2021 text. MEDIUM that the AHJ will use 2021 (S2 says 2018 for the county).

NEEDS ARCHITECT CONFIRMATION: YES.

---

## R-008.3 — Lean check: telescopic-bleacher geometry

QUESTION: What is the smallest area per seat the cited dimensions support?

ANSWER (one paragraph): **3.38 SF/seat (KEYSTONE arithmetic from cited dimensions).** Hussey's MAXAM telescopic system offers standard row spacing of "22” (559 mm), 24” (610 mm), and 26” (660 mm)" (S4); its spec bases net capacity on 18 in per seat (S5), matching IBC 1004.6. Using **24 in rows × 18 in per person = 3.0 SF**, plus one **48 in** stepped aisle (1030.9.1) per block of **21 seats** (bleachers without backrests can run 21 seats before the 12 in accessway must widen, 1030.13.2.1): 3.0 × (21 × 18 + 48) ÷ (21 × 18) = **3.38 SF/seat** → 2,200 × 3.38 ≈ **7,440 SF**. Left out: front walkway, cross aisles, vomitories, wheelchair spaces and companion seats (R-010 not done), rail and end clearances. So the true figure lies above 3.38. Fixed chairs with backrests would be larger (wider seats, deeper rows, 14-seat blocks).

SOURCE: S4, S5, S1.

EDITION / SECTION: Hussey MAXAM brochure (row spacing); IBC 2021 1004.6, 1030.9.1, 1030.13.2.1.

CONFIDENCE: MEDIUM (the arithmetic is exact; it is a lower bound, not a layout).

NEEDS ARCHITECT CONFIRMATION: YES.

---

## Gaps and conflicts
1. Code edition: 2021 (Shane; UpCodes Alabama) vs 2018 (Madison County page). AHJ OPEN (D-008). R-006 not done.
2. ICC 300 (bleachers) not read (paywalled).
3. Wheelchair seating counts and dispersion (2010 ADA 221 / IBC 1108) not done → R-010.
4. Exit count, exit widths, travel distance, main-exit rule (1030.2) not applied: they need a plan (later R-008 sections).
5. The base 6.0 SF/seat comes from one 2014 county standard for a different venue type. A sports-venue planning guide (e.g. NIRSA, Sawyer's *Facility Planning*) would be better; those are paid books and were not obtained.
