# R-015 — Two-level stacking and vertical circulation (Phase 2 test-fit Rev B)

Researched by KEYSTONE 2026-10-03 for P2-T-003b Rev B (sheet P2-G-003 Rev B), after Shane's 11:09 PM CT answer that 55,000 SF is a **footprint** cap that could allow two levels (D-031). All sources retrieved 2026-10-03.
Status: research note. Code text read from UpCodes (IBC 2021, Alabama edition) and the U.S. Access Board's 2010 ADA Standards page. Arena precedents are much larger venues, used only for stacking logic. AHJ and code edition are OPEN (D-008: Madison County's page lists the 2018 I-codes). Not legal advice. **PRELIMINARY — CONCEPTUAL DESIGN — NOT FOR CONSTRUCTION.**

## Sources
- **S1** — IBC 2021 Chapter 10, Means of Egress (UpCodes, Alabama) — https://up.codes/viewer/alabama/ibc-2021/chapter/10/means-of-egress — retrieved 2026-10-03. PRIMARY (via viewer).
- **S2** — IBC 2021 Chapter 11, Accessibility (UpCodes, Alabama) — https://up.codes/viewer/alabama/ibc-2021/chapter/11/accessibility — retrieved 2026-10-03. PRIMARY (via viewer).
- **S3** — IBC 2021 Chapter 9, Fire Protection and Life Safety Systems (UpCodes, Alabama) — https://up.codes/viewer/alabama/ibc-2021/chapter/9/fire-protection-and-life-safety-systems — retrieved 2026-10-03. PRIMARY (via viewer).
- **S4** — U.S. Access Board, 2010 ADA Standards for Accessible Design (§206.2.3, Table 407.4.1) — https://www.access-board.gov/ada/ — retrieved 2026-10-03. PRIMARY.
- **S5** — Reed Arena Facility Guide (Texas A&M; Venue Coalition host) — https://venuecoalition.com/wp-content/uploads/2020/06/Reed-Arena-Facility-Guide.pdf — retrieved 2026-10-03. PRECEDENT (12,989-seat arena).
- **S6** — Orleans Arena Production Guide (July 2024; Venue Coalition host) — https://venuecoalition.com/wp-content/uploads/2025/12/Orleans-Arena-Production-Guide-July-2024.pdf — retrieved 2026-10-03. PRECEDENT.
- **S7** — phase2.yaml design rules DR1-DR5 (concept sheet).
- Tried, not obtained: a wrestling- or small-arena-specific planning guide with stacking rules (NIRSA / Sawyer books are paid). Stacking choices below are KEYSTONE's, labeled ASSUMED where no source says so.

---

## R-015.1 — What must stay at grade, what can go up

QUESTION: Which Phase 2 spaces must sit on the ground level and which can go to a second level, mezzanine or under the seating?

ANSWER (one paragraph): **Ground (L1):** the event floor and lower seating tier form one double-height arena volume with nothing above it (geometry, KEYSTONE). Athlete locker rooms and the 4 event/visitor lockers sit next to the floor — S5: Reed Arena has "locker rooms and dressing rooms on the event level"; S6: the Orleans event level "is where all of the locker rooms … are located"; S7 DR1 (athlete/spectator split) and DR3 (event lockers under the bowl). The main entry / hall of champions foyer is at grade (S7 DR5, south portal). Mat storage, equipment room, first aid (EMS access), one concession stand and mechanical are put at grade (ASSUMED). **Level 2:** the upper seating tier, Strength & Conditioning, the cross-training mat, admin offices, the upper concourse (hall of champions display wall) and upper restrooms (Shane's list, 11:09 PM CT). Cross-training on L2 *becomes* the mezzanine, so DR4 ("mezzanine overlook on daily mat") flips. S&C on L2 needs a floor designed for gym loads (structural engineer). **Under the seating:** the upper tier sits over L1 rooms (the "ring"); rooms under the lower tier are not credited. In the lean case the lower tier is telescopic: S5 says the retractable risers "can be extended or retracted under the permanent seating", so nothing can be built under them.

SOURCE: S5, S6, S7; KEYSTONE.

EDITION / SECTION: S5 §1 and §4-b; S6 Event Level section.

CONFIDENCE: MEDIUM (precedent + project design rules; the split is a judgment call).

NEEDS ARCHITECT CONFIRMATION: YES.

---

## R-015.2 — Footprint arithmetic for two levels

QUESTION: How is the ground footprint computed when part of the program goes up?

ANSWER (one paragraph): KEYSTONE method (no outside source): each level is grossed up with the Rev A factor (1.25 base / 1.15 lean, R-014); mechanical (5% of total gross, R-014) sits on L1. Footprint **F = max(L1 gross, arena volume gross + L2 gross)**, because L2 can only sit over the L1 ring, not over the arena volume. Upper-tier overhang beyond the ring is not credited (conservative). Seat split between tiers: 50/50 ASSUMED, plus the 30-70% split that gives the lowest footprint (range ASSUMED). Restrooms are sized per level from each level's occupant load (IBC 2021 Table 2902.1; per-level is conservative because 2902.3.3 allows toilets one story away — R-009). Concourse per level = 25% of that level's seats x 5 SF (R-014 factor, share ASSUMED).

SOURCE: R-008, R-009, R-014; KEYSTONE.

EDITION / SECTION: n/a (method).

CONFIDENCE: MEDIUM for the method, LOW for the split.

NEEDS ARCHITECT CONFIRMATION: YES.

---

## R-015.3 — Exits and stairs from Level 2

QUESTION: How many stairs, how wide, and how much floor area do they take on each level?

ANSWER (one paragraph): **Count:** S1 Table 1006.3.3 — 1-500 occupants: 2 exits per story; 501-1,000: 3; more than 1,000: 4. With ~1,100-1,400 seats plus S&C/cross-training/admin occupants on L2 (Table 1004.5: exercise rooms 50 gross, business 150 gross), L2 needs **4 exits**. **Width:** S1 1005.3.1 — stairs 0.3 in/occupant, or **0.2 in/occupant** "in buildings equipped throughout with an automatic sprinkler system … and an emergency voice/alarm communication system"; both are expected here (R-015.5). Minimum stair width **44 in** (1011.2). 1005.5: losing any one exit must not drop capacity below 50% (equal stairs satisfy this). **Geometry:** risers 7 in max, treads 11 in min (1011.5.2); one flight may rise at most 12 ft (1011.8); landings at least as deep as the stair width or 48 in, whichever is less (1011.6). With a **15 ft floor-to-floor (ASSUMED)**: 26 risers of 6.92 in, 2 flights, 12 treads each; a switch-back stair is about 2W wide by (132 in + 2 landings) long — ≈ 206 SF per level at 65 in wide (base 50/50). **Enclosure:** exit access stairs that "serve or atmospherically communicate between only two adjacent stories" need no shaft (1019.3 exception 1). Stairs repeat on both levels, so their area is counted on L1 and L2. Not applied yet: assembly main-exit rules (1030.2, 1030.3) — these govern exits at grade and are for the architect.

SOURCE: S1.

EDITION / SECTION: IBC 2021 §§1004.5, 1005.3.1, 1005.5, Table 1006.3.3, 1011.2, 1011.5.2, 1011.6, 1011.8, 1019.3.

CONFIDENCE: HIGH for the rules / LOW for the 15 ft floor-to-floor.

NEEDS ARCHITECT CONFIRMATION: YES (floor-to-floor, stair type, occupancy A-4).

---

## R-015.4 — Elevator and accessible means of egress

QUESTION: Does a two-level Phase 2 need an elevator, and do the stairs need refuge areas?

ANSWER (one paragraph): **Accessible route:** S2 1104.4 — "At least one accessible route shall connect each accessible story, mezzanine and occupied roofs in multilevel buildings and facilities." The exception covers stories with "an aggregate area of not more than 3,000 square feet" — L2 is ~20,000-27,000 SF, so it does not apply. S4 ADA 206.2.3 exception 1 may exempt "private buildings or facilities that are less than three stories" (not shopping centers, etc.), but the IBC still applies through the building permit. An **elevator** is assumed (a ramp for 15 ft is impractical — ASSUMED). **Car size:** S4 Table 407.4.1 — centered door: 42 in door, 80 in side to side, 51 in back wall to front return, 54 in back wall to door. **Hoistway: 64 SF per level ASSUMED** (8 x 8 ft, machine-room-less; manufacturer to confirm). **Accessible egress:** S1 1009.1 — where two exits are required, each accessible space needs two accessible means of egress. In a sprinklered building the exit stairs qualify without 48 in between handrails (1009.3.2 exception 1) and without an area of refuge (1009.3.3 exception 2). An elevator as an accessible means of egress is required only where the floor is 4+ stories above/below exit discharge (1009.2.1).

SOURCE: S1, S2, S4.

EDITION / SECTION: IBC 2021 §§1104.4, 1009.1, 1009.2.1, 1009.3.2, 1009.3.3; 2010 ADA Standards §206.2.3, Table 407.4.1.

CONFIDENCE: HIGH for the rules / LOW for the hoistway SF.

NEEDS ARCHITECT CONFIRMATION: YES.

---

## R-015.5 — Sprinklers and voice alarm (they set the stair factor)

QUESTION: Is the building sprinklered and does it have an emergency voice/alarm system?

ANSWER (one paragraph): S3 903.2.1.4 — sprinklers are required "throughout stories containing Group A-4 occupancies" where "the fire area exceeds 12,000 square feet", or "has an occupant load of 300 or more", or "is located on a floor other than a level of exit discharge". The arena alone trips all three, so sprinklers are expected. S3 907.2.1.1 — in Group A with an occupant load of 1,000 or more, fire alarm activation "shall initiate a signal using an emergency voice/alarm communications system". Together these allow the 0.2 in/occupant stair factor (R-015.3). The A-4 occupancy is ASSUMED (R-007 not yet done).

SOURCE: S3.

EDITION / SECTION: IBC 2021 §§903.2.1.4, 907.2.1.1.

CONFIDENCE: MEDIUM (depends on the A-4 classification and the AHJ).

NEEDS ARCHITECT CONFIRMATION: YES.

---

## R-015.6 — Single controlled entry: exit-only doors, main exit, checkpoint (added 2026-10-04, D-033)

QUESTION: If everyone enters through one grand entrance (Shane, D-033), how do the other required exits work, and what does the code say about the main exit and a security checkpoint?

ANSWER (one paragraph): **Exit-only doors are allowed.** S1 1010.2 — "egress doors shall be readily openable from the egress side without the use of a key or special knowledge or effort" (2018 edition: 1010.1.9); the code governs the egress side only, so exterior entry hardware can be omitted. S1 1010.2.9 — swinging doors serving Group A spaces with 50 or more occupants "shall not be provided with a latch or lock other than panic hardware or fire exit hardware" (2018: 1010.1.10). S1 1010.2.7 exception 1 — "Stairway discharge doors shall be openable from the egress side and shall only be locked from the opposite side." **Alarm, not delay:** S1 1010.2.13 lists the occupancies allowed delayed-egress locks (B, F, I, M, R, S, U, small E classrooms, A-3/B courtrooms); a Group A arena is not among them, so exit doors may carry a local alarm but no delay. Electric locks only per 1010.2.11 / 1010.2.12 (with panic hardware, 1010.2.9 exception 2). **Main exit:** S1 1030.2 — an assembly space over 300 occupants with a main exit: "that main exit shall be of sufficient capacity to accommodate not less than one-half of the occupant load", and in Group A it "shall front on not less than one street or an unoccupied space of not less than 10 feet … that adjoins a street or public way". S1 1030.3 — the other exits on each level provide "not less than one-half of the total occupant load served by that level" and comply with 1007.1. **Count and capacity:** Table 1006.3.3 (more than 1,000 per story → 4 exits) and 1006.2.1.1 (space over 1,000 → 4 exits or exit access doorways); doors and other components 0.15 in/occupant in a sprinklered building with emergency voice/alarm (1005.3.2 exception 1; R-015.5). With the 2,200 seats alone, the main exit needs ≥ 1,100 × 0.15 in = 165 in of clear width; the final occupant load (floor, lockers, S&C) waits on R-007. **Checkpoint:** S1 1003.6 — "Obstructions shall not be placed in the minimum width or required capacity of a means of egress component"; S1 1010.5 — turnstiles "shall not be placed so as to obstruct any required means of egress" except as 1010.5.1-1010.5.3 allow. Screening lanes therefore sit beside or retract out of the main-exit egress width. **Locker rooms:** Table 1004.5 locker rooms 50 gross → a 3,500 SF locker room ≈ 70 occupants > 49, so two exits or exit access doorways (Table 1006.2.1).

SOURCE: S1 (re-read 2026-10-04: https://up.codes/viewer/alabama/ibc-2021/chapter/10/means-of-egress).

EDITION / SECTION: IBC 2021 §§1003.6, 1004.5, 1005.3.2, 1006.2.1, 1006.2.1.1, Table 1006.3.3, 1010.2, 1010.2.7, 1010.2.9, 1010.2.11-1010.2.13, 1010.5, 1030.2, 1030.3. 2018 equivalents named where known (1010.1.9, 1010.1.10); the 2018 assembly sections are 1029.x (see Gaps; D-008 edition OPEN).

CONFIDENCE: HIGH for the rules / LOW for the occupant load (R-007 not done) and door widths (not drawn).

NEEDS ARCHITECT CONFIRMATION: YES (door hardware, alarm and electric-lock design, checkpoint layout vs egress width, final occupant load).

---

## Gaps
- No section or floor-to-floor height exists; 15 ft is ASSUMED. A taller L1 (e.g. for the upper tier's rake) lengthens stairs.
- Hoistway SF, stair layout and mechanical at grade are ASSUMED.
- The lower/upper seat split and sightlines are not checked; the upper-tier rake and its overhang are not drawn.
- Rooms under the lower (fixed) tier are not credited; they could shrink the footprint in the base case.
- 2018 vs 2021 IBC (D-008): the 2018 section numbers for assembly egress differ (1029 vs 1030); the sections used here were read in the 2021 text only.
