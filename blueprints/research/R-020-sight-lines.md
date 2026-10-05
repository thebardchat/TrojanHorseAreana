# R-020 — Sight-line study: C-values for the telescopic lower tier and the fixed upper tier (P2-A-302 Rev A)

Researched and computed by KEYSTONE 2026-10-04 (Shane 7:24 AM CT: "sight-line study BEFORE more seating detail"). All sources retrieved 2026-10-04.
Status: research note + schematic calculation. Not a design by a licensed architect; the AHJ / architect confirm. Values and method: `params/phase2_sightlines.yaml`; sheet P2-A-302 Rev A; generator `phase2/src/p2_a_302.py` (`--md` prints the table below).

## Sources
- **S1** — Starena Group, "Sight Lines for Seated Spectators" (reprints Green Guide diagram 12.1 and the C formula) — https://www.starenaaust.com/products/stadium-seating/sight-lines — SECONDARY (the Green Guide itself, DCMS *Guide to Safety at Sports Grounds* 5th ed. 2008 §12.3, was not purchased).
- **S2** — Parametric Monkey, "Stadium seating bowl with Dynamo" (2017) — https://parametricmonkey.com/2017/10/23/seating-bowl/ — formula C = D(N+R)/(D+T) − R (Green Guide §12.3, p.109); BVN Stadium.Cvalue defaults: eye 1,200 mm above the tread, 150 mm forward of the row's rear edge, "considered industry standard"; C descriptors 60 / 90 / 120 / 150 mm.
- **S3** — FIFA, *Football Stadiums Guidelines* 2.3 Stadium Bowl — https://publications.fifa.com/es/football-stadiums-guidelines/general-process-guidelines/design/stadium-bowl/ — C = 120 optimal, 90 preferred, 60 minimum in specific areas, "should be avoided in lower tiers"; upper tiers may go lower.
- **S4** — CEN/TR 15913:2009 (iTeh preview) — https://cdn.standards.iteh.ai/samples/32554/d7b4616fb5e0479f8e98daf147f88d63/SIST-TP-CEN-TR-15913-2009.pdf — "C ≥ 90 mm generally acceptable for all newly constructed spectator stands"; uses 1.15 m (wheelchair user) and 1.8 m (standing person) in accessible-viewing checks.
- **S5** — DIN EN 13200-1:2019 summary (kpt-bj.com listing) — standing eye 1.6 m (SECONDARY; standard text not purchased). Shane's range 5'-2"–5'-6" (1.57–1.68 m) contains it.
- **S6** — Hussey Seating, MAXAM brochure, Dimensional Data + Notes (box copy `research_src/hussey_maxam.pdf`, R-008 S4): 6 rows @ 11⅝" → overall seat height 6'-3⅛", closed 3'-6"; recessed: +6" depth (4'-0"), +2¼" height (6'-5⅜"); rear row stays in the recess when open.
- **S7** — IBC 2021 1003.2 (ceiling ≥ 7'-6" in means of egress), 1003.3.1 (80" headroom), 1030.14.2 (aisle risers 4–8", treads ≥ 11"), 1030.17.3 (26" sightline-constrained guard) — UpCodes.

## Method
- C (mm) = D_front × R_behind / D_behind − R_front, every eye placed from the actual tier geometry (equivalent to S2's formula; also handles the step from the lower to the upper tier and the loop rail).
- Eyes: seated 1.2 m above the row tread, 0.15 m forward of the row's rear edge (S2); standing 1.6 m (S5). Rail stander: 1 ft behind the upper tier's back edge on the loop, standing (ASSUMED).
- Focal point (Shane): near edge of the nearest mat, at the floor (mat thickness ignored — slightly conservative). From the frozen plan Rev D: N and S tier fronts **25 ft** from the nearest mat edge (10 ft clear + 15 ft table zone); E tier front **10 ft**. No west tier.
- Grades (KEYSTONE): ≥ 90 mm PASS (S3 preferred, S4), 60–90 MARGINAL (Shane's 60–90 target; S3 minimum), < 60 FAIL.
- AS DRAWN = P2-A-301 geometry: lower 6 rows × 24" @ 11⅝" (Hussey, ASSUMED choice), front at the floor; upper 5 rows × 36" @ 14" stepping DOWN from the loop (L2 FF 15 ft, D-049) to a 9.17 ft front row; 26" fascia.
- PROPOSED (D-053, OPEN): upper riser 19" per row (3 aisle risers of 6⅓" on 12" treads — within 1030.14.2) → front row 15 − 5 × 19/12 = **7.08 ft**; east tier 6 ft further from the mats (focal 16 ft). Lower tier unchanged.
- 2D sections only (perpendicular to each side). Corners, wheelchair positions (S4 1.15 m eye), the mixed case (front row standing, row behind seated) and the focal height of a raised mat are NOT checked.

## Results (C in mm; ~ = marginal, ✗ = fail)

| Row | drawn N/S 25 ft seated | drawn N/S 25 ft standing | drawn E 10 ft seated | drawn E 10 ft standing | proposed N/S 25 ft seated | proposed N/S 25 ft standing | proposed E 16 ft seated | proposed E 16 ft standing |
|---|---|---|---|---|---|---|---|---|
| L2 | 190 | 162 | 74 ~ | 15 ✗ | 190 | 162 | 142 | 101 |
| L3 | 178 | 152 | 64 ~ | 13 ✗ | 178 | 152 | 129 | 92 |
| L4 | 167 | 142 | 57 ✗ | 11 ✗ | 167 | 142 | 118 | 84 ~ |
| L5 | 157 | 134 | 51 ✗ | 10 ✗ | 157 | 134 | 109 | 77 ~ |
| L6 | 149 | 127 | 46 ✗ | 9 ✗ | 149 | 127 | 101 | 72 ~ |
| U1 | 1014 | 984 | 829 | 780 | 428 | 397 | 352 | 313 |
| U2 | 49 ✗ | 20 ✗ | -119 ✗ | -162 ✗ | 211 | 183 | 139 | 103 |
| U3 | 45 ✗ | 19 ✗ | -107 ✗ | -146 ✗ | 198 | 171 | 127 | 94 |
| U4 | 43 ✗ | 18 ✗ | -97 ✗ | -133 ✗ | 185 | 161 | 118 | 87 ~ |
| U5 | 40 ✗ | 17 ✗ | -89 ✗ | -122 ✗ | 175 | 151 | 109 | 81 ~ |
| RAIL | 582 | 182 | 513 | 113 | 709 | 309 | 673 | 273 |
| fascia clearance U1 (mm) | 286 | 661 | 131 | 490 | 326 | 701 | 263 | 631 |
| upper front row deck (ft) | 9.17 | 9.17 | 9.17 | 9.17 | 7.08 | 7.08 | 7.08 | 7.08 |

Failures AS DRAWN:
- **Upper tier fails on every side**: N/S seated 40–49, standing 17–20; east negative (rows U2–U5 cannot see the near mat edge over the row in front). 14" per 36" row is too flat for a 25 ft (or 10 ft) focal distance.
- **East lower tier** (10 ft focal): seated L4–L6 fail (46–57), L2–L3 marginal (64–74); standing 9–15 (all fail).
- N/S lower tier passes (seated 149–190, standing 127–162). U1 sees well over the lower tier (≥ 780) and over the fascia (clearance 131–661 mm). Rail standers pass (113–582).

Riser / layout changes that close it (all seated rows ≥ 101, PROPOSED column):
1. **Upper riser 14" → 19" per row.** Because the back stays at the loop (D-049), the front row drops 9.17 → 7.08 ft. 16" passes N/S (94–114) but not the east side; 19" is the smallest round value tested that passes both with change 2.
2. **East side: move the east tier 6 ft further from the mats (10 → 16 ft clear).** With the loop fixed at 15 ft and a 10 ft focal distance no riser pair reaches 60 mm (best ≈ 46 mm with 19" upper). 12 ft → 68; 14 ft → 85; 16 ft → 101 (seated). Cost: +6 ft east-west ≈ +1,512 SF footprint (51,503 → 53,015, still < 55,000 cap, D-031), or take 6 ft from the 22 ft east support zone.
3. Lower tier stays at 11⅝" (Hussey). A 16" Hussey rise fixes the east lower rows alone, but its top (≈ 6.7 ft) then collides with the stepped-down upper tier front.
- East standing stays MARGINAL (72–103) with the proposal. Sensitivity: with S4's 1.8 m standing eye the east L6 standing value drops to 57 (fail), N/S stays ≥ 116.

## Telescopic stack under the upper-tier front (D-049)
- **Closed, recessed** (S6 minimum recess 4'-0" deep × 6'-5⅜" high): as drawn (front 9.17 ft) it fits only if the tier structure + finish at the front edge is **≤ 32.6 in** (9.17 − 6.45 ft). With the proposed 7.08 ft front only **7.6 in** remain → does not fit.
- **Open**: in a recessed application the rear rows stay in the recess (S6), so rows 5–6 would sit under the overhang. Row 6 deck 4.84 ft + 7'-6" (1003.2, aisle = means of egress) = 12.34 ft needed vs the tier deck ≈ 10.72 ft at the recess back, less structure → **CONFLICT** (as drawn and proposed).
- Recommendation: keep the stack **wall-attached in front of the upper-tier face** (as P2-A-301 Rev A/B draws it); use the low zone under the tier for storage / mechanical only (D-049). Exit passages that run under the tier front (EXIT N / E passages) still need a ≥ 7'-6" ceiling → local raise or vomitory cut at the next A-101/A-102 revision.

QUESTION: Do the drawn tiers give acceptable sight lines to the near mat edge, seated and standing?

ANSWER: **No for the upper tier (all sides) and the east lower tier.** Upper risers of 19" per row plus a 16 ft east focal distance bring every seated row to ≥ 101 mm (PASS) and standing to ≥ 72 mm (east marginal). Logged as D-053 (OPEN, Shane decides). Seating detail should wait for that decision.

CONFIDENCE: HIGH for the arithmetic / MEDIUM for the inputs (secondary sources for eye heights; geometry schematic; focal point per Shane).

NEEDS ARCHITECT CONFIRMATION: YES (final tier section, wheelchair sightlines, guard type at the fascia, structure depth under the tier, scoreboard / rigging obstructions).
