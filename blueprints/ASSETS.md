# ASSETS — KEYSTONE inventory

Inventory date: 2026-10-03 (P1-T-001). Times are Central (CT).
Rule: Shane's files are read-only. **None of Shane's originals are committed to this repo.**

## 1. Shane's ARENA folder: `C:\Users\Hubby\Desktop\ARENA\` (pulsar00100)

Per Shane, the folder holds **exactly 4 files**. KEYSTONE read the box copies in `/workspace/arena_src/`. Byte sizes match Shane's list.

| File | Type | Size | Modified (CT) | What it is / shows | Phase |
|---|---|---|---|---|---|
| `KEYSTONE_ARCHITECT_PROMPT.md` | Markdown | 26,643 B | 2026-10-03 4:08 PM | KEYSTONE standing instructions, prompt v1.1: locked facts, repo contract, backlog, status bridge | Both (governing doc) |
| `KEYSTONE_INTAKE_2026-10-03.md` | Markdown | 4,901 B | 2026-10-03 4:08 PM | First-session intake compiled from the Gemini, Grok, and Claude sessions. **Header says "MOVIE MAKER INTAKE," but the content is KEYSTONE's** (D-015) | Both |
| `keystone_status.sh` | Bash script | 3,360 B | 2026-10-03 4:08 PM | Pi-side ShaneBrain preflight reader. Reads STATUS.json from pulsar00100 over SSH, falls back to the GitHub raw mirror on `grok/keystone`, flags stale after 26 h, always exits 0. Has a `KEYSTONE_LOCAL_FILE` test override | Bridge (both) |
| `north_alabama_3d_diorama.html` | HTML + Three.js r128 (CDN) | 19,103 B | 2026-10-03 4:02 PM | Interactive 3D diorama, see §1a | **Phase 2** |

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
  - "4 regulation wrestling mats" is unverified (D-014 / R-005).
  - Zone glow colors include blue and pink. That's a viewer UI choice, not a brand color, but brand colors are red/black (prompt §3).

## 2. Assets referenced but NOT in the ARENA folder

| Asset | Status | Action |
|---|---|---|
| **Phase 2 master floor plan image** (55,000 SF, color-coded). Base reference for Phase 2 layout | **Not in the ARENA folder.** Logged as **needed from Shane** | Ask Shane for the original file/path. Needed before P2-T-004, not for Phase 1 |
| Grok session "Wrestling Facility Phase One Remodel Planning": proposal page with `/model.html` maquette | **Location unknown.** Not on this box. pulsar00100 not searched (see ENVIRONMENT.md) | Ask Shane where it's hosted/saved |
| Google Drive: "Trojan Horse Arena Trailer v2 - Widescreen.m4v", "Trojan Horse Arena Trailer v2 - Vertical.m4v" | Exist per intake. **Not inspected** | Reference only. Not needed for drawings |

### 2a. Possibly related material found on the KEYSTONE box (not in ARENA, not used, not committed)

- `/workspace/trojan-horse-arena/assets/floorplan_src.png` (1024×687), from an earlier trailer session on this box. It's an **AI render of a "HAZEL GREEN REGIONAL ATHLETIC COMPLEX - Master Floor Plan" board.** It *may* be a render of the master floor plan Shane means, but that's **unconfirmed.** Its AI text is unreliable and conflicts with locked facts:
  - boys locker tag reads like "3,900 SF"
  - girls reads "3,500 SF"
  - one seating sign reads "3,200"
  - legend says "Neily Green/Gold"
  - a "Conversion" legend lists SF numbers that don't match the 22,000 SF floor
  Per the intake: **don't copy text from renders.** Shane should send the original master floor plan.
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
