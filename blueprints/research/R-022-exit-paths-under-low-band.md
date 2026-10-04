# R-022 — Exit paths under the upper tier's low band (Phase 2)

Written 2026-10-04 by KEYSTONE for Shane (9:47 AM CT order: "do NOT redesign silently — write the finding with TWO options with numbers, log OPEN, show the conflict on A-301 Rev C"). This is arithmetic only. Nothing is redesigned: P2-A-101/102 Rev E stay as drawn and P2-A-301 Rev C shows the conflict in red. Decision: **D-061 OPEN**.

## Sources

- **S1** `params/phase2_plan_rev_e.yaml` (P2-A-101/102 Rev E). Upper tier: 5 rows × 36 in, 19 in risers, front row 7.08 ft, steps down from the loop at L2 FF 15 ft (D-049, D-053). `low_band_ft: 6` = rows 1–2. Zones: exit_n [123.85,224,131.85,252], exit_e [188,175.09,210,183.09], conc_e [165,0,210,56], lobby [84,0,142,56] (PORTAL x 107–119), ath_route [56,48,84,56], concession [127,37.67,142,56]. Upper bands: N [56,224,188,239], S [56,41,188,56], E [188,41,203,239].
- **S2** `params/phase2_sect.yaml` `rev_c`: 1.5 ft deck structure under each tread (ASSUMED). Clear under rows 1–5 = 5.58 / 7.17 / 8.75 / 10.33 / 11.92 ft.
- **S3** IBC 2021 1003.2: the means of egress needs a ceiling height of at least 7 ft 6 in (UpCodes, retrieved 2026-10-04, the same citation as P2-A-301 Rev B and P2-A-302 Rev A).
- **S4** `phase2/src/p2_testfit.py` `summary_g()` / P2-G-003 Rev G: upper-tier capacity 1,155 for the 1,100 required (55 spare). Upper seat factor is 6.0 SF/seat (R-008) on 3 ft rows, so 2 ft of row per seat = **0.5 seat per foot per row**.
- **S5** `phase2/src/p2_a_302.py` `calc()`: C-values for the raised-tier variant (Option B).
- **S6** D-052 (76 in stairs, 26 risers at 6.92 in), D-051 (intermediate landing = width, IBC 2021 1011.6), IBC 2021 1011.5.2 (risers 4–7 in, treads ≥ 11 in), 1030.14.2 (aisle risers 4–8 in), 1030.6.2.2 (roof ≥ 15 ft above the highest aisle, if smoke-protected).

## 1. Finding: exit paths under the 6 ft low band

The clear height under rows 1–2 is 5.6 ft and 7.2 ft (S2). Both are below 7'-6" (S3). These paths cross the band:

| Path | Where it crosses the band | Length under rows 1–2 |
|---|---|---:|
| EXIT (N) | x 123.85–131.85, y 224–230 (V1 → X5) | 8 ft |
| EXIT (E) | y 175.09–183.09, x 188–194 (V2 → X7) | 8 ft |
| SE concourse | S strip x 165–188 (y 50–56) + E strip y 41–56 (x 188–194) | 23 + 15 = 38 ft |
| Lobby / portal / athlete-route edge | x 56–127, y 50–56: athlete route 28 ft (x 56–84) + lobby 43 ft (x 84–127, incl. PORTAL 12 ft at x 107–119) | 71 ft |
| **Total** | | **125 ft** |

Also noted (not an egress path): the concession's north 6 ft (x 127–142) is under the band. An occupiable room also needs a 7'-6" ceiling (IBC 2021 1208.2, KEYSTONE recollection, not re-read today). That strip should be counter-back storage, or it is resolved by Option B.

D-060 (which locker reading) stays OPEN, drawn as on A-101 Rev E: event lockers start behind the band (2,723 SF vs 3,600 programmed).

## 2. Option A — omit upper rows 1–2 over each path (vomitory-style cut)

Seats lost = 2 rows × length × 0.5 seat/ft (S4).

| Path | Seats lost |
|---|---:|
| EXIT (N) 8 ft | 8 |
| EXIT (E) 8 ft | 8 |
| SE concourse 38 ft | 38 |
| Lobby / portal / athlete-route edge 71 ft | 71 |
| **A (all paths)** | **125** |

- Upper capacity 1,155 → **1,030**, which is **70 short** of the 1,100 upper seats (only 55 spare). Holding 1,100 would need 70 × 6.0 = 420 SF of upper band somewhere else, or 70 seats moved to the lower tier (lower-tier room not checked).
- Building SF is unchanged. Seats delivered = 1,100 lower + 1,030 upper = 2,130, so GSF per seat = 81,976.4 ÷ 2,200 = 37.3 → 81,976.4 ÷ 2,130 = **38.5 SF/seat** if the 70 are not replaced.
- **A-min variant:** rail off the strips that are not exit paths (the SE concourse strip as storage, the lobby strip except the portal as display). Cut rows 1–2 only over EXIT (N) 8 + EXIT (E) 8 + PORTAL 12 + athlete route 28 = **56 seats** → 1,099, **1 short** of 1,100. The athlete route is 8 ft wide with 6 ft under the band, so it cannot be railed off.
- Clear under the cut: the soffit becomes row 3 = 8.75 ft ≥ 7'-6". The upper tier gets openings with guards at each cut (1015 / 1030.17). Lower-tier vomitories V1 / V2 already line up with Exit N / Exit E.
- Not drawn. (A non-option note: shifting the athlete route 6 ft south into Concourse W would take it out from under the band and cut A-min to 28 seats. That is a layout change and is not drawn either.)

## 3. Option B — raise the upper tier (and all of Level 2) so row 1 clears 7'-6"

The tier's back stays at the loop = L2 FF (D-049), so clearing row 1 means raising L2.

- **L2 FF 15'-0" → 17'-9" (213 in), upper risers 19 → 21 in** (3 aisle risers of 7.0 in, 12 in treads, inside 1030.14.2). Front row = 17.75 − 5 × 1.75 = **9.0 ft**. Clear under row 1 = 9.0 − 1.5 = **7.5 ft = 7'-6"** (meets 1003.2 exactly; no margin).
- Why 21 in and not 19: raising L2 by 1.92 ft with 19 in risers would also give a 9.0 ft front row, but east seated C would drop to 68 mm (standing 40, FAIL) (S5). At 21 in the minimum C equals Rev E: **N/S seated 149 / standing 127, E seated 101 / standing 72 mm**. Higher risers gain nothing because the lower tier then sets the minimum.
- **Seats lost: 0.** The low band disappears, so the event lockers can run back to the tier lines: **3,600 SF (+877)**, which makes D-060 moot.
- **Stairs:** 213 in ÷ 7 in max → 31 risers at 6.87 in, 2 flights (16 + 15), 15 treads × 11 in = 165 in run. Each stair is 152 × (48 + 165 + 76) = 152 × 289 in = 12.67 × 24.08 ft = **305.1 SF vs 270.2: +34.8 SF per stair per level, ≈ +279 SF** for 4 stairs × 2 levels (clear dimensions). Each stair is 2.75 ft longer. If ST-2 grows outward, the NE tower goes 6.67 → about 9.4 ft deep (+58.7 SF L1 footprint).
- **SF/seat:** +279 SF ÷ 2,200 = **+0.13 SF/seat** (37.3 → 37.4 GSF/seat), with no seats lost.
- **Heights:** ring roof 30 → **32.75 ft** (L2 + 15). Ring walls on A-201 are 2.75 ft taller. Arena U/S structure stays 36 ft and roof 42 ft, so the court clear is unchanged. 1030.6.2.2 (if smoke-protected): highest aisle = loop 17.75 ft → roof ≥ 32.75 ft; 36 ft drawn (3.25 ft margin). Elevator travel 17.75 ft.
- **Also re-check:** the telescopic stack still sits at the tier face (P2-A-302 Rev B). L2 rooms (S&C, cross-training) sit 2.75 ft higher. The 26 in fascia at the front still clears (U1 C unchanged).

## 4. Comparison

| | Option A (cut rows 1–2) | A-min (rails + cut 4 paths) | Option B (L2 17'-9", 21 in risers) |
|---|---:|---:|---:|
| Upper capacity lost | 125 | 56 | 0 |
| Upper capacity vs 1,100 | 1,030 (−70) | 1,099 (−1) | 1,155 (+55) |
| Building SF change | 0 | 0 | ≈ +279 (stairs) |
| Seats delivered / GSF per seat | 2,130 / 38.5 | 2,199 / 37.3 | 2,200 / 37.4 |
| Event lockers | 2,723 SF (D-060 open) | 2,723 SF (D-060 open) | 3,600 SF (D-060 moot) |
| Sight lines (min C seated N/S / E) | unchanged 149 / 101 | unchanged | 149 / 101 |
| Other | guards at each cut | rails + storage strips | ring roof 32.75', taller walls, longer stairs |

KEYSTONE does not pick an option. Shane decides **D-061**.

## 5. Decided (2026-10-04 10:27 AM CT)

Shane chose **Option B** (D-061 DECIDED): "raise Level 2 to 17'-9" with 21 in upper risers. No seats lost; upper-tier front row ≥ 7'-6" clear over ALL exit paths." D-060 is settled in the same message: event lockers go back to the full 3,600 SF behind the tier.

How it was drawn (P2-A-101/102 Rev F, P2-A-301 Rev D, P2-A-302 Rev C, P2-A-201 Rev G, P2-C-101 Rev C, P2-G-003 Rev I):

- **Stairs grow inward.** Each stair is 12.67 × 24.08 ft (31 risers at 6.87 in, 16 + 15). ST-2 grows **west** along the north wall, not north. The NE tower becomes 24.08 × 6.67 ft (was 21.33 × 6.67), not the ~9.4 ft deep tower estimated in §3. The rest of the growth comes out of interior rooms (mech N, S&C, stretch).
- **Drawn size (D-057):** L1 53,080.6 / L2 28,932.6 / TOTAL 82,013.1 GSF, which is **+36.7 vs Rev E** (only the tower's +18.3 SF on each level). §3's ≈ +279 SF was the program-side growth. The program (G-003 Rev I) grows +371.6 (L1 + L2 gross 81,119.1) because vertical circulation goes from 1,144.9 to 1,284.2 SF per level.
- **Clearance:** front row 9.0 ft. Clear = 7'-6" exactly with 1.5 ft structure ASSUMED: **no margin, structural engineer to confirm.**
- **Sight lines (A-302 Rev C):** the lower tier still governs, at N/S 149 / 127 and E 101 / 72 mm. Upper tier N/S 179 / 156, E 105 / 76 mm. No FAIL. East standing stays MARGINAL.
- **1030.6.2.2 (if smoke-protected):** highest aisle = loop 17.75 ft, so the roof must be ≥ 32.75 ft. The arena's U/S structure is drawn at 36 ft, so it PASSES with a 3.25 ft margin.
