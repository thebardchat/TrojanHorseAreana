# CLAUDE.md — Trojan Horse Arena (ARENA work folder)

You are picking up from **KEYSTONE** (Shane's Grok architect bot), which is paused until ~2026-10-09 (usage limit).
Same job, same rules: schematic architecture for the **Hazel Green Regional Athletic Complex — Trojan Horse Arena**.
Owner: **Shane Brazelton**. Everything here is **PRELIMINARY — CONCEPTUAL DESIGN — NOT FOR CONSTRUCTION**.

## Ground rules (from KEYSTONE's operating contract — keep them)
1. **ARENA is home.** `C:\Users\Hubby\Desktop\ARENA` is the source of truth. The GitHub repo `thebardchat/TrojanHorseAreana` (branch `grok/keystone`) is a mirror.
2. **Never overwrite a sheet.** New revisions are new files: `<SHEET>_Rev<X>.pdf` (e.g. `P2-A-101_RevH.pdf`). Older revs are frozen history.
3. **Decisions are Shane's.** Log every decision as `D-###` in DECISIONS (find the file in `_KEYSTONE\` or the repo). Shane wants **no option menus** — do the standard next step; stop only for a real owner decision, and then recommend one answer.
4. **Label everything.** `ASSUMED` vs `DECIDED` vs `CITED`. Code citations: IBC 2021 (assumed; county is on 2018, State Fire Marshal on 2021 — AHJ to confirm, D-008).
5. **Errata wins over the old prompt.** Read `_KEYSTONE\KEYSTONE_PROMPT_v1.3.1_ERRATA.md` before anything else. Today's decisions override older v1.x text.
6. **Status bridge.** After each work session, update `_KEYSTONE\STATUS.json` + `STATUS.md` (schema v2, Central-time stamp). The ShaneBrain Pi preflight reads it and flags RED after ~26–30 h.
7. **Backups are automatic** — ARENA copies nightly 11 PM to `shanebrain:/tank/backups/ARENA` + 30-day ZFS snapshots. Don't build another backup.

## Next session — do this first
- **Site is live (D-076):** main serves the concept site. Publish updates from the worktree `C:\Users\Hubby\Desktop\ARENA_site` (branch `site/srm-direction`; push with `git push origin site/srm-direction:main`). **Never push `permit-package-revD` (remote deleted; repo is public). Never switch branches inside ARENA:** it removes the private `_KEYSTONE` / sheet files from disk (they live only on `permit-package-revD`).
- Next: Plan Rev K study for D-074 (after Shane approves the look), roof / structure concept view, STATUS update each session.
- (Cleared 2026-10-08: Pi snapshot cron confirmed — `30 23 * * *` zfs snapshot of `tank/backups`, keeps newest 30.)

## Locked facts (as of 2026-10-04 evening)
- **Building:** 210 × 252 ft + NE stair tower. 2 levels. **L2 FF 17'-9"** (D-061). Ring roof 32.75 ft, arena roof 42 ft, structure underside 36 ft (assumed).
- **Size:** **85,793 GSF** drawn (L1 56,861 + L2 28,933; includes the 2,100 SF storage annex and the 1,680 SF restroom bump-out; P2-G-003 Rev K / P2-A-101 Rev J, unchanged from Rev I). **No SF cap** (D-056) — size is controlled by budget + parcel. Every area table shows L1, L2, TOTAL GSF, change vs last rev (D-057).
- **Event floor:** 120 × 144 ft, 4 × 42 ft mats (2×2). **2,200 seats** = 1,100 telescopic lower + 1,100 fixed upper (21" risers, steps DOWN from the L2 loop, D-049/D-053/D-061). East seats 16 ft from mats.
- **Floor uses (D-054):** sports + **chairs-only** events (graduations, banquets, expos; 7 net SF ≈ 2,346). No standing-concert design. L1 exits stay sized for standing (extra margin).
- **Exits:** E1 main = **8-pair door bank** (outer + inner vestibule), single controlled entry kept (D-033). Stairs 4 × **76"** clear, 31 risers, intermediate handrails (D-052). 7'-6" clear under upper tier front — **zero margin, needs tier structure ≤ 1'-6"** (top structural question).
- **Screening (D-065):** side bay of the lobby, off the egress path.
- **Restrooms (D-064/D-069):** sized to chairs-only case = **22 men's / 42 women's WC**; second restroom pair (core 2): women in a **one-story 30 × 56 ft bump-out on the EAST wall, entirely south of EXIT (E)** (D-069/D-070/D-072), men + DF in the old Mech (E) strip, all reached by an **8 ft public corridor from Concourse (E)**; EXIT (E) clear, X7 back on the wall, new exit X11. Mech (E) 1,720 → 675 SF + Mech (E2) 660 SF (MEP OPEN: total mech ≈ 4.1 % vs 5 %). East concourse + SW FLEX room unchanged (D-039). Chair layouts keep an 8 ft V2 egress aisle open (P2-A-103 Rev D).
- **Storage (D-067):** chair/table/stage storage = **room 24, 2,100 SF** (70 × 30 ft one-story annex on the north wall, S1 on it), for ~2,350 chairs + tables + portable stage.
- **Event lockers:** 4 × 900 SF = 3,600 SF (D-060).
- **Approved set (D-073):** Phase 2 Schematic Set Rev D (`Phase2_Schematic_Set_RevD.pdf`, 13 sheets) is approved and frozen — new revisions are new files.
- **Working budget number (D-073, planning only):** $39M mid, range $28–57M, excl. land. D-012 (budget target) stays OPEN; no lender / donor use until a GC prices the set. See `_KEYSTONE\R-025-rom-cost-estimate_RevB.md` ($37.3M mid after the A/E fix).
- **Portal (D-043/D-050/D-045/D-047):** freestanding limestone, **50 ft max**, arch crown 34 ft, crimson underside + gold trim, official badge 11 ft dia + 27" wordmark. **Structural engineer required.**
- **Champion Walk (D-046/D-066):** 28 ft brick center, **widened to 40 ft at the doors** (6 ft paved bands each side; egress flows around both piers). 4×8 single-name / 8×8 family-business donor bricks; donor pricing OPEN. Vendor avg $19.17 (4×8) / $29.50 (8×8), install + base NOT included (R-023).
- **Service/buses (D-034):** deliveries at north door S1; bus loop south, offset from the portal view.
- **Site:** TBD (D-006). Madison County, unincorporated Hazel Green. **Alabama requires a registered architect** for this building — this set is the program package for that architect.
- **Brand:** red #CC0000 / black, Shane's circular horse-head badge with Greek-key border is official. Trademark search still OPEN (D-042).

## Where KEYSTONE stopped — do these next, in order
1. **Inventory first (read-only).** List every file in ARENA + `_KEYSTONE\`, newest rev of each sheet, and confirm D-064/065/066/069 + storage room show as DECIDED/drawn. Report gaps to Shane before changing anything.
2. **G-002 → Rev C** showing D-069 closed (restroom counts per core, chairs-only case controlling).
3. **Cover sheet** (P2-G-001): project, sheet index with current revs, decisions summary, "NOT FOR CONSTRUCTION".
4. **Combined Phase 2 PDF** — cover + every current-rev sheet in sheet-number order → `Phase2_Schematic_Set_RevB.pdf`. Don't touch `Phase2_Schematic_Set_RevA.pdf`.
5. **Rough-order-of-magnitude cost estimate** on the current GSF: low / mid / high $/SF for a NE Alabama assembly / athletic building, **cited sources**, plus separate lines for portal, Champion Walk, site work. This is the number Shane needs next for land, money and architect conversations.
6. Update STATUS.json/.md. Repo mirror / draft PR can wait for KEYSTONE — don't push to `main`.

## Open items (not yours to decide — list them, recommend, don't assume)
Parcel/site (D-006) · code edition + AHJ pre-app (D-008) · donor brick pricing (D-044) · trademark search (D-042) · upper-tier structure depth (structural) · MEP: core-2 plumbing + total mech ≈ 4.1 % vs 5 % planning (annex can absorb ~800 SF) · X7 / X11 discharge path waits on the parcel.

## Phase 1 (separate, waiting)
Remodel of the borrowed Hazel Green HS wrestling room, 55 × 45 ft, 10 ft ceilings, no running water. Package delivered to **Dr. Headen** (principal). Waiting on her answer. Don't change Phase 1 unless Shane asks.
