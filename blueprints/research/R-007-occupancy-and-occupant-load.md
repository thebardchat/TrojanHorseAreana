# R-007 — Occupancy classification and occupant load factors for a 2,200-seat arena (Phase 2)

Researched by KEYSTONE 2026-10-04 (Shane 7:44 AM CT). All sources retrieved 2026-10-04. Text read: Alabama Building Code 2021 (adopts IBC 2021) on UpCodes. The county enforces the **2018** IBC (R-006); 2018 text NOT re-read.
Status: research note. The building official assigns the occupancy and the occupant load (1004.5); the architect confirms.

## Sources
- **S1** — IBC 2021 (Alabama) Chapter 3, §§303.1-303.6, 304.1 — https://up.codes/viewer/alabama/ibc-2021/chapter/3/occupancy-classification-and-use — box copy `research_src/upc_ibc2021_ch3.txt`.
- **S2** — IBC 2021 (Alabama) Chapter 10, Table 1004.5, §§1004.5.1, 1004.6, 1004.9, 1030.1.1 — https://up.codes/viewer/alabama/ibc-2021/chapter/10/means-of-egress — box copy `research_src/upc_ibc10.txt`.
- **S3** — IBC 2021 (Alabama) Chapter 5, §508.2-508.3 — https://up.codes/viewer/alabama/ibc-2021/chapter/5/general-building-heights-and-areas — box copy `research_src/upc_ibc2021_ch5.txt`.
- **S4** — Alabama Fire Code 2021 (IFC) §403.2, 403.2.1 (Group A fire safety and evacuation plan with seating plan) — https://up.codes/viewer/alabama/ifc-2021/chapter/4/emergency-planning-and-preparedness.
- **S5** — params/phase2_program.yaml (sprinkler 903.2.1.4 and voice/alarm 907.2.1.1 triggers, cited there from IBC 2021, R-015).

## R-007.1 — Occupancy classification
QUESTION: What occupancy group is the arena and its support space?

ANSWER: The bowl and event floor are **Group A-4**: "assembly uses intended for viewing of indoor sporting events and activities with spectator seating including … arenas" (303.5, S1). A gym *without* spectator seating would be A-3 (303.4) and outdoor bleachers / stadiums A-5 (303.6). Support spaces are classified individually and handled by §508 (S3): **accessory occupancies** (≤ 10 % of the floor area of their story and ≤ the nonsprinklered Table 506.2 value each; no separation required, 508.2.3-508.2.4), or **nonseparated** (each space under its own occupancy, the most restrictive Chapter 9 provisions over the whole area, 508.3.1), or separated (508.4). Likely groups: offices / admin **B**; locker rooms and event lockers part of A-4 or B; storage **S-1**; S&C and cross-training **A-3** (exercise / gymnasium without spectator seating) — **or B**, because 304.1 lists "training and skill development not in a school or academic program (… martial arts studios, gymnastics and similar uses regardless of the ages served, and where not classified as a Group A occupancy)" (S1). A room under 750 SF or under 50 occupants accessory to another occupancy is B or part of that occupancy (303.1.2). KEYSTONE recommendation for G-002: **A-4 main occupancy, nonseparated mixed occupancy, fully sprinklered** (required anyway, S5) — architect to choose.

SOURCE: S1, S3, S5 — retrieved 2026-10-04
EDITION / SECTION: IBC 2021 §§303.1.2, 303.4, 303.5, 303.6, 304.1, 508.2, 508.3.
CONFIDENCE: HIGH for A-4 (explicit "arenas") / MEDIUM for the support-space groups (building official's call)
NEEDS ARCHITECT CONFIRMATION: YES

## R-007.2 — Occupant load factors (Table 1004.5, IBC 2021)
QUESTION: Which occupant load factors apply?

ANSWER: Fixed seats: **the number of seats** (1004.6); **seating without dividing arms (benches, typical telescopic bleachers): 1 person per 18 in of seat length** (1004.6) — the telescopic lower tier must be counted this way if it has bench seats; wheelchair space + companion seat = 1 each. Non-seated areas are added to the seats (1004.6). Table 1004.5 (S2): assembly without fixed seats — concentrated (chairs only) **7 net**, standing **5 net**, unconcentrated (tables and chairs) **15 net**; stages and platforms 15 net; exercise rooms **50 gross**; locker rooms **50 gross**; business areas 150 gross; commercial kitchens 200 gross; accessory storage / mechanical **300 gross**; skating rink / pool area 50 gross (decks 15 gross). The building official may approve a higher load up to 1 per 7 SF of occupiable floor with a seating diagram (1004.5.1). The maximum occupant load must be **posted** in Group A (1004.9). Telescopic seating that is not a building element must comply with **ICC 300** (1030.1.1). The IFC requires a fire safety and evacuation plan with a **detailed seating plan, occupant load and occupant load limit** for Group A (S4, 403.2.1).

**Event floor — the big sensitivity.** KEYSTONE's program uses 50 gross ("exercise rooms") for the 114 x 144 ft = 16,416 SF floor (ASSUMED function, phase2_program.yaml) → **329** occupants. If the floor is also used for non-sport events: unconcentrated (15 net) → **1,095**; chairs only (7 net) → **2,346**; standing (5 net) → **3,284**. That is a building-official decision driven by the intended uses; it changes Level 1 exit capacity (doors, the main exit 1030.2) and fixtures, not the Level 2 stairs (R-018). Logged as D-054 (OPEN).

SOURCE: S2, S4 — retrieved 2026-10-04
EDITION / SECTION: IBC 2021 Table 1004.5, §§1004.5.1, 1004.6, 1004.9, 1030.1.1; IFC 2021 §403.2.1. 2018 IBC: same table number expected, NOT verified.
CONFIDENCE: HIGH for the factors (2021 text read) / LOW for the event-floor function (owner's intended use)
NEEDS ARCHITECT CONFIRMATION: YES

## What changes for KEYSTONE
- A-4 confirmed (the program and plans already ASSUMED it) → G-002 can cite 303.5.
- Telescopic lower tier: if benches, occupant load = seat length ÷ 18 in, which may exceed the nominal 1,100 seats; seat type OPEN (D-009 mixed seating decided, product TBD).
- D-054 OPEN: event floor uses (wrestling / sports only vs concerts, graduations, expos with floor chairs or standing).

## R-007.3 Addendum 2026-10-04 10:48 AM CT — sections looked up for P2-G-002 Rev A (code analysis)

Source: IBC 2021 (Alabama) Chapter 10 on UpCodes (https://up.codes/viewer/alabama/ibc-2021/chapter/10/means-of-egress), from the box copy `research_src/upc_ibc10.txt` (retrieved 2026-10-04, S2 above). The 2018 text was NOT re-read (R-006, D-008).

- **1010.1.1 Size of doors:** "The required capacity of each door opening shall be sufficient for the occupant load thereof and shall provide a minimum clear opening width of 32 inches … measured between the face of the door and the stop, with the door open 90 degrees … Where … a door opening includes two door leaves without a mullion, one leaf shall provide a minimum clear opening width of 32 inches." Used for the ASSUMED 64 in clear per door pair (2 × 32 in). Real leaf widths are the architect's call.
- **1030.2 Assembly main exit (full text):** the main exit carries "not less than one-half of the occupant load, but such capacity shall be not less than the total required capacity of all means of egress leading to the exit." In Group A it fronts a street, or an unoccupied space ≥ 10 ft that adjoins a street or public way. Alternative: "where there is not a well-defined main exit or where multiple main exits are provided, exits shall be permitted to be distributed around the perimeter of the building provided that the total capacity of egress is not less than 100 percent of the required capacity." This alternative is G-002 Option 2.
- **1030.3 Assembly other exits:** each level has additional means of egress for "not less than one-half of the total occupant load served by that level." It carries the same distributed-perimeter alternative (total width ≥ 100%).
- **1004.2.1 Intervening spaces:** egress capacity is based on "the cumulative portion of occupant loads of all rooms, areas or spaces to that point along the path of egress travel." Lobbies and concourses are therefore not added as separate loads (R-018.1 method). Their exits still carry the cumulative load (1006.2.1 exception).
- **1005.5:** losing any one exit must not reduce capacity below 50% of the required.
- **Table 1006.2.1** (Group A, sprinklered): 49 occupants / 75 ft common path for a space with one exit.
- **Table 1017.2** (A, sprinklered): 250 ft exit access travel.

**G-002 numbers.** These are KEYSTONE arithmetic on the drawn Plan Rev F areas.

| | Value |
|---|---|
| L1 without the floor | 1,474 |
| L1 with the floor | 1,803 / 2,569 / 3,820 / 4,758 (floor 329 / 1,095 / 2,346 / 3,284) |
| L2 | 1,277 base / 1,462 worst (D-052) |
| Building at the worst case | 6,220 |

L1 doors at 0.15 in (1005.3.2 exception) with 11 openings × 64 in = 704 in:
- **Worst case: SHORT.**
  - Total: 933.0 in needed, short 229.0 in.
  - Main exit: 466.5 in needed vs 64 in.
- **Sports case:** the total passes (489.8 in), but the main exit E1 still needs 244.9 in = 4 pairs.

CONFIDENCE: HIGH for the text (2021 read) / LOW for the door widths (not drawn) and the floor function (D-054). NEEDS ARCHITECT CONFIRMATION: YES.
