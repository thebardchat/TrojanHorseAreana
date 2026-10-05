# R-021 — Area reconciliation: program basis vs drawn basis (Phase 2)

Written 2026-10-04 8:40 AM CT by KEYSTONE for Shane (8:36 AM CT order, item 4). Read-only arithmetic; no drawing, no new sheet.
**Rules applied:** there is **no 55,000 SF cap** (D-056 — "55,000 SF = early rough estimate, not a limit"; D-031 retired), so this note has no margin lines. Every area table reports **L1 footprint, L2 area, TOTAL GSF and change vs the last revision** (D-057).

## Sources

- **S1** `params/phase2_plan_rev_d.yaml` — P2-A-101/102 Rev D geometry (building 204 x 252 ft + NE tower 19 x 5; arena volume [56,56,182,224]; L2 open-to-below: arena 126 x 168, lobby 58 x 34). Frozen with Phase 2 Schematic Set Rev A (D-036).
- **S2** P2-A-102 Rev D area check (sheet text): "Drawn L2 floor 28,363 SF (building minus open-to-below) … Total drawn ≈ 79,866 vs 78,784 program GSF (P2-G-003 Rev F)."
- **S3** `phase2/src/p2_testfit.py` `summary_f()` / `compute_loop()` + `params/phase2_program.yaml` — P2-G-003 Rev F method: gross-up g = 1.25, mechanical 5 % of gross on L1, arena volume AV = g x (event floor + lower seating), footprint F = max(L1, AV + L2), loop 4,942 SF added to L2 without gross-up. Re-run 2026-10-04 8:38 AM CT (unchanged code, output below).
- **S4** D-052 (4 stairs x 76 in, mid landing = width → 152 x 256 in = 12.67 x 21.33 ft = 270.2 SF per stair per level; Rev F program stair = 63.95 in x (132 + 2 x 48) in = 202.5 SF); D-051 (landing ≥ width, IBC 2021 1011.6).
- **S5** D-053 (east seats 6 ft further from the mats → east wall + 6 ft; 6 x 252 = 1,512 SF L1).
- **S6** `params/phase2_site.yaml` `footprint_check` (P2-C-101 Rev A arithmetic, 7:44 AM CT).

ASSUMED (KEYSTONE, LOW): the east shift widens the arena volume / L2 open-to-below by 6 ft over its 168 ft N-S length (6 x 168 = 1,008 SF), so L2 gains 1,512 − 1,008 = 504 SF; the 19 in upper risers (D-053) change heights, not plan area; the 76 in stairs grow inward from their corners (P2-C-101 Rev A), so only the NE tower (ST-2) widens (2.333 x 5 = 11.67 SF, on both levels).

## 1. True current size (drawn basis) — D-057 table

| Basis | L1 footprint (SF) | L2 area (SF) | TOTAL GSF (SF) | Change vs last revision |
|---|---:|---:|---:|---|
| **As drawn: P2-A-101/102 Rev D** (frozen) | 51,503.0 | 28,363.0 | 79,866.0 | vs Rev C: see P2-A-102 Rev D |
| **Decided, next A-101/A-102 revision** (D-052 + D-053, not yet drawn) | **53,026.7** | **28,878.7** | **81,905.3** | **+1,523.7 / +515.7 / +2,039.3** vs Rev D |

Arithmetic:
- Rev D L1 = 204 x 252 = 51,408 + 19 x 5 = 95 → **51,503.0** (S1).
- Rev D L2 = 51,503 − 126 x 168 (21,168, arena open) − 58 x 34 (1,972, lobby open) → **28,363.0** (S1, S2). TOTAL = 51,503 + 28,363 = **79,866.0**.
- Next rev L1 = 51,503 + 1,512 (east shift) + 11.67 (NE tower) = **53,026.7**.
- Next rev L2 = 28,363 + 1,512 − 1,008 (wider arena opening, ASSUMED) + 11.67 = **28,878.7**. TOTAL = **81,905.3**.

**Answer: the true current size is L1 footprint 53,027 SF / L2 area 28,879 SF / TOTAL GSF 81,905 SF** (decided state; the frozen drawings still show 51,503 / 28,363 / 79,866). The program basis below is a planning-factor estimate, not the size.

## 2. Program basis (P2-G-003 Rev F method) — same table form

| Step | L1 gross (SF) | L2 gross (SF) | Footprint F (SF) | TOTAL GSF (SF) |
|---|---:|---:|---:|---:|
| Rev F as approved (S3) | 51,194.1 | 27,589.5 | 52,738.4 (AV 25,148.8 + L2) | 78,783.6 |
| + 76 in stairs (S4): stairs + elevator 874.0 → 1,144.9 net per level (+270.9) | 51,577.8 | 27,928.1 | 53,076.9 | 79,505.9 |
| + east shift (S5, flat add as on P2-C-101 Rev A; L2 +504 ASSUMED as above) | — | 28,432.1 | **54,588.9** | **81,521.9** (79,505.9 + 1,512 + 504) |

Note: in the program the footprint is set by AV + L2 (25,148.8 + 27,589.5 = 52,738.4), which is larger than the programmed L1 gross (51,194.1): the L2 deck needs 1,544 SF more ring than the L1 rooms make, so the footprint carries ≈ 1,544 SF of L1 space that no program line counts. In the drawn plan that is the FLEX space (team assembly ≈ 2,072, FLEX / storage 1,011).

## 3. Line-by-line reconciliation: footprint 54,588.9 (program) vs 53,026.7 (drawn) = 1,562.2

| # | Line | What the program counts | What the drawing counts | Program | Drawn | Δ (P − D) |
|---|---|---|---|---:|---:|---:|
| 1 | Arena volume (event floor + telescopic lower tier, double height) | 1.25 x (16,400 floor + 3,719 telescopic seats [1,100 x 3.38]) | 126 x 168 box: floor 114 x 144 = 16,416 + tier bands N/S 2 x 126 x 12 = 3,024 + E 12 x 144 = 1,728 | 25,148.8 | 21,168.0 | **+3,980.8** |
| 2 | L2 deck over the L1 ring (upper tier, S&C, cross-training, admin, restrooms, stairs/elevator, loop) | 1.25 x 18,118.0 net + 4,942 loop | building − arena opening − lobby opening (incl. L2 corridor, stretch strip, upper concourse) | 27,589.5 | 28,363.0 | **−773.5** |
| 3 | Lobby open-to-below (double-height lobby inside the footprint) | not modelled (foyer is 800 net on L1 only) | 58 x 34 inside the footprint, no L2 floor | 0.0 | 1,972.0 | **−1,972.0** |
| = | Subtotal: Rev F program vs Rev D drawn | | | 52,738.4 | 51,503.0 | **+1,235.4** |
| 4 | 76 in stairs (D-052) | 4 x (270.2 − 202.5) = 270.9 net per level, x 1.25 on L2 (F follows AV + L2) | stairs grow inward; only the NE tower widens 2.333 x 5 | +338.6 | +11.7 | **+326.9** |
| 5 | East shift 6 ft (D-053) | flat +6 x 252 | +6 x 252 | +1,512.0 | +1,512.0 | **0.0** |
| = | **Total** | | | **54,588.9** | **53,026.7** | **+1,562.2** |

Check: 3,980.8 − 773.5 − 1,972.0 = 1,235.3 (1,235.35 unrounded) + 326.9 + 0 = **1,562.2** ✓.

Where the gap comes from, in plain terms:
1. **+3,981** — the program grosses up the event floor and seats by 25 % as if they were rooms with walls and corridors (16,400 x 0.25 = 4,100 alone). The real arena volume is one open box, so the drawing is smaller there.
2. **−774** — the drawn L2 deck is a bit bigger than the program's L2 (the drawing has a full L2 corridor zone and a 6 ft stretch strip that the program does not list).
3. **−1,972** — the program never counted the double-height lobby's footprint above the 800 SF foyer; the drawing does.
4. **+327** — the program adds the 76 in stairs as new grossed-up area; the drawing absorbs them inside the existing box.

## 4. TOTAL GSF reconciliation (decided state)

| | Program estimate | Drawn basis | Δ (P − D) |
|---|---:|---:|---:|
| L1 | 53,089.8 (51,577.8 + 1,512; programmed rooms only) | 53,026.7 (full footprint) | +63.1 |
| L2 | 28,432.1 | 28,878.7 | −446.6 |
| **TOTAL GSF** | **81,521.9** | **81,905.3** | **−383.4** |

The totals sit within 0.5 %: the program's extra arena gross-up is roughly offset by the space it never counts (lobby void footprint, unprogrammed L1 ring under the L2 overhang).

## Confidence

HIGH for the arithmetic (re-run from params); LOW for the geometry behind it (every plan coordinate is ASSUMED, schematic). The east-shift L2 split (+504) is ASSUMED until the next A-101/A-102 revision draws it.
