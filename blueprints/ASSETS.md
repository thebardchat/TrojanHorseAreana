# ASSETS — KEYSTONE inventory

Inventory date: 2026-10-03 (P1-T-001). Updated 2026-10-03 ~5:50 PM CT (reference plan intake, P2-T-001 seed). Times are Central (CT).
Rule: Shane's files are read-only. **None of Shane's originals are committed to this repo.**

## 1. Shane's ARENA folder: `C:\Users\Hubby\Desktop\ARENA\` (pulsar00100)

Per Shane, the folder first held **exactly 4 files**. On 2026-10-03 Shane added 2 images, and a byte-identical copy of the reference plan was saved there as `Phase2-floor-plan-flat.png`. **The folder then held 7 files.** Later on 2026-10-03 Shane added `wrestle-room-measure.png` (Phase 1 site sketch). **The folder now holds 8 files.** KEYSTONE read the box copies in `/workspace/arena_src/` and got nothing from Shane's PC. Sizes/times for the new files: box copies, plus Shane's info.

| File | Type | Size | Modified (CT) | What it is / shows | Phase |
|---|---|---|---|---|---|
| `KEYSTONE_ARCHITECT_PROMPT.md` | Markdown | 26,643 B | 2026-10-03 4:08 PM | KEYSTONE standing instructions, prompt v1.1: locked facts, repo contract, backlog, status bridge | Both (governing doc) |
| `KEYSTONE_INTAKE_2026-10-03.md` | Markdown | 4,901 B | 2026-10-03 4:08 PM | First-session intake compiled from the Gemini, Grok, and Claude sessions. **Header says "MOVIE MAKER INTAKE," but the content is KEYSTONE's** (D-015) | Both |
| `keystone_status.sh` | Bash script | 3,360 B | 2026-10-03 4:08 PM | Pi-side ShaneBrain preflight reader. Reads STATUS.json from pulsar00100 over SSH, falls back to the GitHub raw mirror on `grok/keystone`, flags stale after 26 h, always exits 0. Has a `KEYSTONE_LOCAL_FILE` test override | Bridge (both) |
| `north_alabama_3d_diorama.html` | HTML + Three.js r128 (CDN) | 19,103 B | 2026-10-03 4:02 PM | Interactive 3D diorama, see §1a. **Demoted to secondary 2026-10-03:** presentation viewer, not the layout source | Phase 2 (secondary) |
| `Phase2-floor-plan-flat.png` | PNG, 1024×687 | 744,067 B | 2026-10-03, time not given (copy saved on Shane's PC) | Byte-identical copy of `arenav1-floor-plan.png` (sha256 `d030dcb4…bd54`). **Phase 2 REFERENCE PLAN (primary), designated by Shane 2026-10-03.** See §1b | **Phase 2 (primary reference)** |
| `arenav1-floor-plan.png` | PNG, 1024×687 | 744,067 B | 2026-10-03, time not given (added by Shane) | Flat color-coded "HAZEL GREEN REGIONAL ATHLETIC COMPLEX - Master Floor Plan." sha256 `d030dcb46a65d98e47b2c0041a20554dc38465aa0028c8130b196723f880bd54`. **Phase 2 REFERENCE PLAN (primary), designated by Shane 2026-10-03** (D-017). See §1b | **Phase 2 (primary reference)** |
| `Phase2-floor-plan.jpeg` | Image, 1024×687. **The file is WebP-encoded despite the .jpeg name** | 105,532 B | 2026-10-03, time not given (added by Shane) | Photo-style render of a lit 3D tabletop model of the same plan in a lobby. sha256 `528414ead71092ce357e592dc0028bdb06672a901a6de23ce2094a853aba1b20`. **Presentation render only, NOT a source.** Its text is wrong: boys 3,900, girls 3,500, seating labels swapped (north 2,200 / south 3,200), and a "Conversion" legend (Wrestling 15,000 / Jiujitsu 36,000 / Basketball 25,000 / Volleyball 15,000 SF) that conflicts with the 22,000 SF floor | Phase 2 (presentation only) |
| `wrestle-room-measure.png` | PNG, 1108×816 (RGBA) | 127,301 B | 2026-10-03 ~9:46 PM (box copy; Shane's time not given) | Google Maps aerial of the wrestling room building with the 'Measure distance' tool (total path 276.85 ft / 84.38 m) and Shane's hand markup of rooms, exits, and fixtures. sha256 `4cd9756ae606f7e8c688053619528abc0220d6045f12230eddc17ba071df5808`. Original `C:\Users\Hubby\Desktop\ARENA\wrestle-room-measure.png`. **Not committed.** See §1c | **Phase 1 (rough estimate + layout notes only)** |

### 1a. What the diorama shows (`north_alabama_3d_diorama.html`)

- Page title "North Alabama Interactive Diorama." A dark scene with a 3D presentation board (100 × 60 scene units, **not to scale, no feet**) under bloom lighting and orbit controls.
- The board top starts as a grid placeholder: "DRAG & DROP MASTER FLOOR PLAN HERE." Dropping an image on the page maps it onto the board. **The master floor plan image is not bundled.**
- 5 hidden hover zones light up with a neon glow and an info panel (name, SF, blurb):
  - Championship Arena, 22,000 SF: "4 regulation wrestling mats… Permanent stadium seating surrounds the lowered event floor"
  - Boys Locker Room, 3,500 SF
  - Girls Locker Room, 3,503 SF
  - Strength & Conditioning, 6,000 SF
  - Cross-Training Mat Area, 4,000 SF
- SF values match the prompt §3 Phase 2 table. **Nothing in it is Phase 1** (no wrestling-room remodel content).
- **Same file as the repo's `hazel-green-complex-3d.html` (commit 8a2f4c6).** Content is identical once line endings are ignored. The repo copy uses CRLF (19,531 B); Shane's copy uses LF (19,103 B).
- Findings (no changes made):
  - The arena blurb says "Permanent stadium seating" and "lowered event floor." Seating type is still OPEN (D-009), and a lowered floor isn't a locked fact.
  - "4 regulation wrestling mats" is unverified (D-014 / R-005). **Update 2026-10-03:** R-005 written; 4 mats fit 22,000 SF by area only (arithmetic, room dims TBD). D-014 still OPEN.
  - Zone glow colors include blue and pink. That's a viewer UI choice, not a brand color, but brand colors are red/black (prompt §3).

### 1b. Phase 2 reference plan: what it shows (`Phase2-floor-plan-flat.png` = `arenav1-floor-plan.png`)

Shane's rule (D-017): **USE** zones, adjacencies, the 5 SF tags, and the room list. **IGNORE** dimension strings, scale bar, garbled text (e.g. "CENTEB," "ETAKD"), and the green/gold legend (red/black is locked). North is taken as up per prompt §3. The north arrow sits bottom-right but its direction isn't legible at this resolution.

**SF tags used:** Championship Wrestling Arena 22,000 · Boys Locker Room 3,500 · Girls Locker Room 3,503 · Strength & Conditioning 6,000 · Cross-Training Mat Area 4,000. Legend: "Total Square Footage 55,0?0 SF" (digits garbled) and "Arena Capacity: 2,200 Spectators."

**Adjacencies as drawn (objective read):**
- **Northwest:** Strength & Conditioning.
- **North center:** Cross-Training Mat Area, east of S&C.
- **West side:** Boys Locker Room directly above (north of) Girls Locker Room, under S&C. A north–south athlete corridor (solid gray arrows) runs on their east side.
- **Center:** concourse / concession core. A "Concession Stand" with a counter and seating sits next to a "Public Restroom" (flanked by two small fixture rooms labeled "RR"/"RM," garbled). The **Stage** is on the arena's west edge, facing the concourse.
- **East:** the arena, 4 mats labeled Wrestling Mat 1–4 in a 2×2 grid, on a red floor border. Seating banks on the **north** ("Stadium Seating (3,200 Capacity)"), **south** ("(2,200 Capacity)"), and **east** (no label). Short curved banks wrap the NW and SW corners and flank the stage on the west.
- **South center:** Public Entry. Dashed red spectator-flow arrows go from the entry north into the concourse and east into the arena. More dashed arrows run east–west along the north concourse between the Cross-Training door and the arena's NW corner.
- **Southwest of the concourse:** "Public Restroom," two "First Aid" rooms, an "Administrative Office," and a "First Aid Room" further south by the entry.
- **South edge, east of entry** (service strip under the south seating): an unlabeled room with toilets/sinks, an unlabeled room with a table, "Utility Room," "Administrative Storage," "Equipment Room," and "Mechanical / Electrical Room."
- **Northeast corner:** "Equipment Storage."
- **Southeast corner:** "Mechanical / Storage / Utility."
- Other small rooms: a fixture room at the north wall between Cross-Training and the arena (label garbled "P&D #08"), and a small room SW of the stage with a stair/lift-like symbol (label garbled).

**Observations (nothing changed):**
- **No 4 event/visitor locker rooms** under the bowl are shown yet, and **no mezzanine overlook** on the daily mat. Both are §3 design rules (3) and (4) still to add.
- The plan shows a **"Public Restroom" in the concourse core and another "Public Restroom" SW.** That's two, matching Shane's x2.
- Seating labels: north 3,200 vs south 2,200, while the legend says arena capacity 2,200. Locked value stays **2,200 total** (D-016 OPEN).
- The legend calls spectator arrows "Dashed Gold," but they're drawn red. The legend calls the arena "Nelly Green/Gold," but the arena is drawn red. Ignored per D-017.
- A gray athlete-flow arrow runs east–west from the locker corridor into the concourse, where the dashed spectator arrows also run. Whether the athlete/spectator split holds (§3 design rule 1) needs checking at A-101. No change made.
- Dimension strings and scale bar are inconsistent (e.g., overall "27.30'"). Ignored per D-017.

### 1c. Phase 1 aerial sketch: what it shows (`wrestle-room-measure.png`, Shane 2026-10-03)

**What it is:** a Google Maps aerial with the measure tool, plus Shane's hand markup. **It is a rough aerial estimate, NOT a tape measurement.** It is never drawn as existing conditions and does not close D-001.

**Measure path (KEYSTONE check):** starts at "0" at the NW corner of the wrestling room roof, runs down the west side, across the south, up the east side, back across the north, then diagonally NW → SE. Total **276.85 ft (84.38 m)**. Side pixel lengths are about 413 / 350 / 413 / 354 px, and the diagonal is about 545 px. That gives 7.49 px/ft, and the 5 ft minor ticks independently measure 7.46 px/ft. **Exterior roof footprint ≈ 55 ft N-S × 47 ft E-W (diagonal ≈ 72.7 ft), confidence LOW.** The interior room will be smaller (walls, eaves). Tick check: the 50 ft tick lands about 49.9 ft down the west side, the 150 ft tick about 7 ft below the NE corner, and the 250 ft label about 63% along the diagonal. All three match the labels. Recorded in phase1.yaml `existing.wrestling_room.estimate_aerial`. **Update 2026-10-03 10:06 PM CT:** Shane's tape gives the inside dimensions as 55'-0" × 45'-0", which agrees with the estimate. The estimate stays a cross-check only.

**Used on P1-A-101 Rev A (door marks only):** the four door/exit triangles were read off this sketch as APPROX. positions along each wall (`existing.wrestling_room.doors_approx`):
- west exit about 0.65 of the way down from the north
- south exit at about mid-wall (two triangles, possibly a pair of doors)
- NE exit on the east wall about 0.30 from the north
- hallway door on the east wall about 0.70 from the north

These are not measured, and no dimensions are given.

**Update 2026-10-03 10:12 PM CT:**
- P1-A-101 now draws these four openings as 3'-0" doors. That size is ASSUMED STANDARD, VERIFY; the locations are still APPROX.
- The walls are drawn as 8" CMU (ASSUMED).
- **Photos not yet received:** Shane says Dr. Headen (principal) took photos. Copies are requested on P1-G-001 Rev D (ask #5). Once received, they go here.

**Layout per Shane's markup (qualitative, phase1.yaml `existing.layout_notes`):**
- The **wrestling room** is the large west block.
- **Emergency exits** are marked on its west side, its south side, and one near its NE corner.
- **Support wing** to the east:
  - two "broken showers"
  - a "private toilet"
  - a urinal
  - two toilets
  - a washer/dryer
  - an office
  - two storage rooms
- Two **"open hallway"** segments run east–west through the wing. This is the walk-through route.
- **Yellow stars** (water fountain / sink) sit near the urinal and hallway.
- The map label reads "Hazel Green Wrestling."
- Doors and exits are drawn as triangles.
- A **"flag football side"** field lies to the east.

**Odd or unclear items (no change made):**
- The vertex circles sit a few px off the path's corners. It looks like a screenshot rendering offset. KEYSTONE measured the path lines and ticks, not the circles.
- The path is drawn about 1.4° off north. So the aspect ratio taken from the diagonal (0.82) differs from the side lengths (0.85).
- The NE emergency-exit triangle is drawn just outside the roof outline.
- The "Hazel Green Wrestling" map label overlaps the support wing.
- The yellow-star legend floats north of the wing.
- There is a whited-out blank area between the private toilet and the storage rooms.
- One storage room has a green scribbled oval in it.
- The office/wing reaches east toward the red-outlined "flag football side" area.
- A separate gray building edge shows at the far west.

## 2. Assets referenced but NOT in the ARENA folder

| Asset | Status | Action |
|---|---|---|
| **Phase 2 master floor plan image** (55,000 SF, color-coded). Base reference for Phase 2 layout | **RECEIVED 2026-10-03:** `arenav1-floor-plan.png`, saved in ARENA as `Phase2-floor-plan-flat.png` (§1, §1b) | Use per D-017. Phase 1 still first |
| Grok session "Wrestling Facility Phase One Remodel Planning": proposal page with `/model.html` maquette | **Location unknown.** Not on this box. pulsar00100 not searched (see ENVIRONMENT.md) | Ask Shane where it's hosted/saved |
| Google Drive: "Trojan Horse Arena Trailer v2 - Widescreen.m4v", "Trojan Horse Arena Trailer v2 - Vertical.m4v" | Exist per intake. **Not inspected** | Reference only. Not needed for drawings |

### 2a. Possibly related material found on the KEYSTONE box (not in ARENA, not used, not committed)

- `/workspace/trojan-horse-arena/assets/floorplan_src.png` (1024×687), from an earlier trailer session on this box. It's an **AI render of a "HAZEL GREEN REGIONAL ATHLETIC COMPLEX - Master Floor Plan" board.** It *may* be a render of the master floor plan Shane means, but that's **unconfirmed.** Its AI text is unreliable and conflicts with locked facts:
  - boys locker tag reads like "3,900 SF"
  - girls reads "3,500 SF"
  - one seating sign reads "3,200"
  - legend says "Neily Green/Gold"
  - a "Conversion" legend lists SF numbers that don't match the 22,000 SF floor
  Per the intake: **don't copy text from renders.**
  **Update 2026-10-03:** this file (sha256 `39467dabdc8caef54f9fb200ae9b3d450c934e6afa3465d8030adc2263ec07f3`) is a **different file from both** new ARENA images. It's the same tabletop render as `Phase2-floor-plan.jpeg` (pixel mean difference ~0.8/255, i.e. a re-encode), with the same wrong labels. **Still unused.** The reference plan is `Phase2-floor-plan-flat.png`.
- `/workspace/trojan-horse-arena/loudon/` is a clone of `thebardchat/loudon-desarro` ("Loudon / DeSarro Athletic Complex," 50,000 SF). Its `wrestling_facility_phase1.py` describes a *new* 10,000 SF metal building as "Phase 1." **That's a different, older concept.** It doesn't match the locked Phase 1 (remodel) or Phase 2 (55,000 SF). Ignored.

## 3. Repo root inventory: `thebardchat/TrojanHorseAreana` @ `main` 8a2f4c6 (read-only)

| File | Last commit | What it is | Status |
|---|---|---|---|
| `README.md` | a102198 (2026-05-11) | Says "Phase 1 3D Model": 120 ft × 250 ft, ~30,000 SF, 24 ft ceiling, ~800 seats, $4M–$6M | **Superseded Feb 2026 concept.** Protected |
| `CLAUDE.md` | 537af8e (2026-03-14) | Claude Code config. Describes the same Feb 2026 model. Tells Claude to push to `claude/trojans-sports-complex-3d-r07Pw` | Protected. Claude's rules, not KEYSTONE's |
| `build_3d_model.py` | 3795c57 (2026-02-05) | CadQuery generator: 120×250×24 ft building | **Superseded Feb 2026 concept** |
| `render_floorplan.py` | 3795c57 (2026-02-05) | matplotlib 2D floor plan of that building | **Superseded** |
| `render_3d_views.py` | f834e50 (2026-02-05) | matplotlib 3D views of that building | **Superseded** |
| `import_to_freecad.py` | f834e50 (2026-02-05) | FreeCAD macro: STEP → FCStd | Superseded-concept tooling |
| `Hazel_Green_Trojans_Complex.step` / `.stl` | 3795c57 (2026-02-05) | CAD output of the Feb 2026 model | **Superseded** |
| `render_floorplan_2d.png` | 3795c57 (2026-02-05) | 2D plan render of the Feb 2026 model | **Superseded** |
| `render_aerial.png`, `render_entrance.png`, `render_arena.png` | f834e50 (2026-02-05) | 3D renders of the Feb 2026 model | **Superseded** |
| `hazel-green-complex-3d.html` | 8a2f4c6 (2026-10-03) | Phase 2 interactive diorama. Same as Shane's `north_alabama_3d_diorama.html` (§1a) | **Current, Phase 2.** Protected |
| `index.html` | 6beb65e (2026-04-23) | Public landing page: "Trojan Horse Arena — A strategy battle arena built in the ShaneBrain ecosystem." Doesn't describe the complex (see PARKING_LOT) | Protected. Auto-deploys |
| `LICENSE` | c0e58fa | GPL v3 | Protected |
| `.github/workflows/deploy.yml` | 435aed6 | Push to `main` → `wrangler pages deploy .` to Cloudflare Pages project `trojan-horse-arena` (public) | Protected. **Why KEYSTONE never touches `main`** |
| `.github/` other | — | FUNDING.yml, PR template, issue templates | Read-only |

Remote branches seen: `main`, `claude/add-article-vii-sponsorship-qtkOG`, `claude/trojans-sports-complex-3d-r07Pw` (not touched), plus `grok/keystone` (KEYSTONE's).
**Superseded numbers (120×250, ~30,000 SF, ~800 seats, $4–6M) are history. They're blocked from `params/` by `shared/validate.py`.**

## 2026-10-03 additions (10:29 PM CT session)
- **R-005 source copies** (box scratch `/workspace/research_src/`, **not committed**): `utah_2014_15.pdf` / `utah.txt` (NFHS 2014-15 Wrestling Rules Book, full public copy), `ahsaa_wr_2026_27.pdf` / `ahsaa.txt` (AHSAA 2026-27 Wrestling), `nfhs_changes_2026_27.pdf` (NFHS 2026-27 rule changes via LHSAA). `nfhs_wr_2023_24.pdf` is an AccessDenied error page, not a rulebook. The current NFHS rulebook is paywalled and was not obtained.
- **Print bundle** `blueprints/phase1/out/pdf/Phase1_Package_for_Dr_Headen.pdf` (also `/workspace/keystone_previews/`): `pdfunite` of the frozen `P1-G-001_RevD_principal.pdf` + `P1-A-101_RevA.pdf`, 2 pages, 1224 × 792 pt. Built from the committed files, not regenerated.

## 2026-10-03 additions (10:45 PM CT session, P2-T-003b)
- **Research source copies** (box scratch `/workspace/research_src/`, **not committed**): `upc_ibc10.txt` (IBC 2021 ch. 10 via UpCodes, Alabama), `upc_alabama_ipc-2021_…txt` (IPC 2021 ch. 4), `upc_texas_ibc-2018_…txt` (IBC 2018 ch. 29, for comparison), `loudoun.pdf/.txt` (Loudoun County Capital Facilities Manual 2014), `groton.pdf` (Groton MA feasibility study), `hussey_maxam.pdf` (Hussey MAXAM brochure). codes.iccsafe.org pages need a login to render; UFC 4-740-02 PDF returned 403.
- **New Phase 2 data file** `params/phase2_program.yaml` (test-fit factors + room list, every group sourced). Locked values stay in `phase2.yaml`.
- **New Phase 2 sheet** `phase2/out/pdf/P2-G-003_RevA.pdf` + `phase2/out/dxf/P2-G-003_RevA.dxf` (tabloid landscape, one page), generated by `phase2/src/p2_g_003.py`. Previews (box only): `/workspace/keystone_previews/P2-G-003.png`, `/workspace/keystone_previews/P2-G-003.pdf`.

## 2026-10-03 additions (11:09 PM CT session, P2-G-003 Rev B)
- **New Phase 2 sheet** `phase2/out/pdf/P2-G-003_RevB.pdf` + `phase2/out/dxf/P2-G-003_RevB.dxf` (two-level test-fit, tabloid landscape, one page), from `phase2/src/p2_g_003.py --rev B`. Rev A files are FROZEN and unchanged.
- **Previews (box only):** `/workspace/keystone_previews/P2-G-003.png` (now Rev B), `/workspace/keystone_previews/P2-G-003_RevA.png` (Rev A preview kept), `/workspace/keystone_previews/P2-G-003.pdf` (now Rev B).
- **New research** `research/R-015-two-level-stacking-and-vertical-circulation.md`.
- **Research source copies** (box scratch `/workspace/research_src/`, **not committed**): `upc_ibc_chapter_11_accessibility.html/.txt` (IBC 2021 ch. 11), `upc_ibc_chapter_9_fire-protection-and-life-safety-systems.html/.txt` (IBC 2021 ch. 9), `ada2010.html/.txt` (2010 ADA Standards, access-board.gov), `reed.pdf/.txt` (Reed Arena Facility Guide), `orleans.pdf/.txt` (Orleans Arena Production Guide 2024).

## 2026-10-03 additions (11:26 PM CT session, P2-G-003 Rev C)
- **New Phase 2 sheet** `phase2/out/pdf/P2-G-003_RevC.pdf` + `phase2/out/dxf/P2-G-003_RevC.dxf` (suites study, tabloid landscape, one page), from `phase2/src/p2_g_003.py --rev C`. Rev A and Rev B are FROZEN and unchanged.
- **Previews (box only):** `/workspace/keystone_previews/P2-G-003.png` (now Rev C), `P2-G-003_RevB.png` (Rev B kept), `P2-G-003_RevA.png`, `P2-G-003.pdf` (now Rev C).
- **New research** `research/R-016-suites-small-arenas.md`.
- **Research source copies** (box scratch `/workspace/research_src/`, **not committed**): `pitt.pdf/.txt` (Petersen Events Center Production Guide 2020), `wku.html/.txt` (College Heights Herald 2002), `sheldon.pdf/.txt` (Sheldon ISD Panther Stadium), `ttu.html/.txt` (Texas Tech arena facts).

## 2026-10-03 additions (11:39 PM CT session, D-030 locked program + block plans)
- **New Phase 2 sheet** `phase2/out/pdf/P2-G-003_RevD.pdf` + `phase2/out/dxf/P2-G-003_RevD.dxf` (LOCKED PROGRAM, tabloid landscape, one page), from `phase2/src/p2_g_003.py --rev D` (now the default). Revs A, B and C are FROZEN and unchanged.
- **New Phase 2 sheets** `phase2/out/{pdf,dxf}/P2-A-101_RevA` (Level 1) and `P2-A-102_RevA` (Level 2): schematic block plans, 1/32 in = 1 ft-0 in on tabloid, from `phase2/src/p2_a_plan.py --sheet P2-A-101|P2-A-102`. DXF in paper inches (1 in = 32 ft).
- **New Phase 2 data file** `params/phase2_plan.yaml` (block-plan coordinates in feet, every group sourced; layout ASSUMED).
- **Previews (box only):** `/workspace/keystone_previews/P2-G-003.png` + `P2-G-003.pdf` (now Rev D), `P2-G-003_RevC.png` (Rev C kept), `P2-G-003_RevB.png`, `P2-G-003_RevA.png`; `P2-A-101.png` + `P2-A-101.pdf`, `P2-A-102.png` + `P2-A-102.pdf`.
- Layout reference used (box only, not committed): `/workspace/arena_src/arenav1-floor-plan.png` (same plan as `Phase2-floor-plan-flat.png`).

## 2026-10-04 additions (4:30 AM CT session, D-009 MIX seating + Rev B block plans)
- **New Phase 2 sheet** `phase2/out/pdf/P2-G-003_RevE.pdf` + `phase2/out/dxf/P2-G-003_RevE.dxf` (LOCKED PROGRAM, MIX seating, tabloid landscape, one page), from `phase2/src/p2_g_003.py --rev E` (now the default). Revs A–D are FROZEN and unchanged.
- **New Phase 2 sheets** `phase2/out/{pdf,dxf}/P2-A-101_RevB` (Level 1) and `P2-A-102_RevB` (Level 2), from `phase2/src/p2_a_plan.py --sheet P2-A-101|P2-A-102` (`--rev B` default). Rev A files are FROZEN and unchanged (`--rev A` regenerates them byte-identical).
- **New Phase 2 data file** `params/phase2_plan_rev_b.yaml` (Rev B block-plan coordinates in feet, 204 × 252 ft box, every group sourced; layout ASSUMED). `params/phase2_plan.yaml` stays as the frozen Rev A geometry.
- **Previews (box only):** `/workspace/keystone_previews/P2-G-003.png` + `.pdf` (now Rev E), `P2-G-003_RevD.png` (Rev D kept); `P2-A-101.png` + `.pdf`, `P2-A-102.png` + `.pdf` (now Rev B), `P2-A-101_RevA.png`, `P2-A-102_RevA.png` (Rev A kept).

## 2026-10-04 additions (4:43 AM CT session, D-033 single controlled entry, Rev C block plans)
- **New Phase 2 sheets** `phase2/out/{pdf,dxf}/P2-A-101_RevC` (Level 1) and `P2-A-102_RevC` (Level 2), from `phase2/src/p2_a_plan.py --sheet P2-A-101|P2-A-102` (`--rev C` default). Rev A and Rev B files are FROZEN and unchanged.
- **New Phase 2 data file** `params/phase2_plan_rev_c.yaml` (Rev C geometry: checkpoint, controlled door, perimeter doors, exit passages; ASSUMED). `phase2_plan_rev_b.yaml` stays as the frozen Rev B geometry (also read by P2-G-003 Rev E).
- **Research:** `research/R-015-two-level-stacking-and-vertical-circulation.md` gains R-015.6 (single controlled entry: exit-only doors, main exit, checkpoint; IBC 2021 Ch. 10 re-read 2026-10-04).
- **Previews (box only):** `/workspace/keystone_previews/P2-A-101.png` + `.pdf`, `P2-A-102.png` + `.pdf` (now Rev C); `P2-A-101_RevB.png`, `P2-A-102_RevB.png` (Rev B kept); Rev A previews kept.

## 2026-10-04 additions (4:55 AM CT session, D-035 Level 2 loop, Rev D block plans, P2-G-003 Rev F)
- **New Phase 2 sheets** `phase2/out/{pdf,dxf}/P2-A-101_RevD` (Level 1) and `P2-A-102_RevD` (Level 2), from `phase2/src/p2_a_plan.py --sheet P2-A-101|P2-A-102` (`--rev D` default). Revs A-C are FROZEN and unchanged.
- **New Phase 2 sheet** `phase2/out/{pdf,dxf}/P2-G-003_RevF` (locked program + Level 2 loop), from `phase2/src/p2_g_003.py` (`--rev F` default). Revs A-E are FROZEN and unchanged.
- **New Phase 2 data file** `params/phase2_plan_rev_d.yaml` (Rev D geometry: loop, NE stair tower, moved stairs / elevator, trimmed S&C + cross-training; ASSUMED). `phase2_plan_rev_c.yaml` stays as the frozen Rev C geometry.
- **New research** `research/R-017-indoor-running-track-and-guards.md`.
- **Previews (box only):** `/workspace/keystone_previews/P2-G-003.png` + `.pdf` (now Rev F), `P2-G-003_RevE.png` (Rev E kept); `P2-A-101.png` + `.pdf`, `P2-A-102.png` + `.pdf` (now Rev D), `P2-A-101_RevC.png`, `P2-A-102_RevC.png` (Rev C kept).

## 2026-10-04 additions (5:27 AM CT session, Phase 2 Schematic Set Rev A freeze, R-018 egress, P2-A-201 Rev A)
- **New set bundle** `phase2/out/pdf/Phase2_Schematic_Set_RevA.pdf` (3 pages, 17 x 11 in: P2-G-003 Rev F, P2-A-101 Rev D, P2-A-102 Rev D; FROZEN) from new `phase2/src/p2_set.py`.
- **Re-issued (label-only)** `phase2/out/{pdf,dxf}/P2-A-101_RevD` with the FLEX labels (D-039); `params/phase2_plan_rev_d.yaml` labels updated.
- **New Phase 2 sheet** `phase2/out/{pdf,dxf}/P2-A-201_RevA` (exterior elevations: south primary with the portal, north / east / west schematic), from new `phase2/src/p2_a_201.py`; new data file `params/phase2_elev.yaml` (heights, portal, finishes; every group sourced, ASSUMED where marked).
- **New research** `research/R-018-level-2-egress-assembly.md`, `research/R-019-arena-clear-height.md`. IBC 2021 Ch. 10 text copy kept box-only (`/workspace/research_src/ibc2021_ch10_upcodes_full.txt`, not committed).
- **Look references used (box only, not committed):** `/workspace/trojan-horse-arena/PROJECT-BRIEF.md`, `assets/arch_src.png` (portal proportions, colors); `assets/logo_hghs_rgba.png` reviewed but NOT used (D-040).
- **Previews (box only):** `/workspace/keystone_previews/P2-A-201.png` + `.pdf`, `Phase2_Schematic_Set_RevA.pdf`; `P2-A-101.png` + `.pdf` (Rev D with FLEX labels).

## 2026-10-04 additions (~6:10 AM CT session, P1-T-008 plumbing scope)
- **New Phase 1 sheet** `phase1/out/{pdf,dxf}/P1-P-001_RevA` (plumbing / water restore scope narrative, 11x17 landscape, NTS), from new `phase1/src/p1_p_001.py`. Params: `existing.plumbing` structured inventory/scope/asks/licensed_trade + `sheets.P1-P-001`. Scope narrative only — no pipe sizing / no design. Cross-refs frozen P1-G-001 Rev D + P1-A-101 Rev A (`Phase1_Package_for_Dr_Headen`).
- **Preview (box only):** `/workspace/keystone_previews/P1-P-001.png`.

## 2026-10-04 additions (6:16 / 6:22 AM CT session, official mark, freestanding portal, P2-A-201 Rev B)
- **New brand files** (`blueprints/brand/`), Shane's chat attachments 6:16 AM CT = copies of `Desktop\ARENA\THA_logo_*.svg` on his PC; colour identified by the `fill` of the single path; identical geometry; official mark per D-041:

| File | Fill | sha256 |
|---|---|---|
| `brand/THA_logo_black.svg` | #1A1A1A | `81d190a7d3f9f95072ce683fa216d7c94a93202f9e7d77f8e41255cd67e6487f` |
| `brand/THA_logo_red.svg` | #CC0000 | `ae2423c926759bc07babfaef70b2154fb73be7a09222250de45687104741ed16` |
| `brand/THA_logo_white.svg` | #FFFFFF | `b6a8fea9a77b0e7d3d9a6cde903e0f5daa9e9f690e63ed5ca385aeb387b50510` |

- Not committed: Shane's JPG preview (black mark on a transparency checker, 2256 x 1888, sha256 `452cbfde78659d0dbed0a75ba7c9b553d9c1884c664992064f6f03eaf06ddd81`, box attachment only) and the `THA_logo_*.png` files on his PC (not on the box). Logo Concepts 01 / 02: SUPERSEDED by D-041, kept as history; not located in the repo or on the box.
- **New reference** `references/portal_freestanding_champion_walk_ref.png` (Shane 6:22 AM CT: freestanding limestone arch, crimson soffit, paved promenade, low walls / planters; 1024 x 576 PNG; sha256 `93ae1c778c192c3db4af6a21463264571d8e39402b64d5c71a8b80eedadd7570`). Look reference only (D-043).
- **New Phase 2 sheet** `phase2/out/{pdf,dxf}/P2-A-201_RevB` (exterior elevations with the official mark, freestanding portal, Champion Walk, key plan, brand detail) from `phase2/src/p2_a_201.py --rev B` (default); Rev A FROZEN and unchanged. New data file `params/phase2_elev_rev_b.yaml` (Rev B overlay; `phase2_elev.yaml` stays the frozen Rev A input).
- **Previews (box only):** `/workspace/keystone_previews/P2-A-201.png` + `.pdf` (now Rev B), `P2-A-201_RevA.png` (Rev A kept).
