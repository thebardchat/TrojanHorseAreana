B = "C:/Users/Hubby/AppData/Local/Temp/claude/C--Users-Hubby-Desktop-ARENA/202807a2-361c-4275-8ca9-11bac63af77d/scratchpad/repo/blueprints/"
import yaml

s = open(B + "params/phase2_cover_rev_b.yaml", encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b)


rep("# phase2_cover_rev_b.yaml: P2-G-001 Rev B (Set Rev C). Rev A inputs stay in phase2_cover.yaml.\n",
    "# phase2_cover_rev_c.yaml: P2-G-001 Rev C (Set Rev D, D-072 public corridor). Rev A / B inputs stay in phase2_cover.yaml / phase2_cover_rev_b.yaml.\n")
rep("  revision: B\n", "  revision: C\n")
rep('  set_name: "PHASE 2 — SCHEMATIC DESIGN SET · REV C"', '  set_name: "PHASE 2 — SCHEMATIC DESIGN SET · REV D"')
rep('  index_head: "SHEET INDEX — PHASE 2 SCHEMATIC SET REV C (sheet-number order)"', '  index_head: "SHEET INDEX — PHASE 2 SCHEMATIC SET REV D (sheet-number order)"')
rep('  size_col: "SET REV C"', '  size_col: "SET REV D"')
for a, b in [('revision: B, status: "NEW (this sheet)"}', 'revision: C, status: "NEW (this sheet)"}'),
             ('title: "Code analysis (schematic)", revision: C}', 'title: "Code analysis (schematic)", revision: D}'),
             ('title: "Site plan — campus diagram (site TBD)", revision: E}', 'title: "Site plan — campus diagram (site TBD)", revision: F}'),
             ('title: "Overall floor plan — Level 1 (block plan)", revision: I}', 'title: "Overall floor plan — Level 1 (block plan)", revision: J}'),
             ('title: "Floor overlays — mats, seating + conversions (aisle to V2)", revision: C}', 'title: "Floor overlays — mats, seating + conversions (V2 egress aisle)", revision: D}'),
             ('title: "Life safety plan — Levels 1 + 2", revision: C}', 'title: "Life safety plan — Levels 1 + 2", revision: D}'),
             ('title: "Exterior elevations", revision: H}', 'title: "Exterior elevations", revision: I}'),
             ('title: "Enlarged plans — locker rooms + restroom core 2", revision: C}', 'title: "Enlarged plans — locker rooms + core 2 + public corridor", revision: D}'),
             ('title: "3D massing model — views", revision: C}', 'title: "3D massing model — views", revision: D}'),
             ('  - {d: "D-069/070", t: "Second restroom pair (core 2) in a one-storey 30 x 56 ft bump-out on the EAST wall at V2."}',
              '  - {d: "D-069/070", t: "Second restroom pair (core 2) in a one-storey 30 x 56 ft bump-out on the EAST wall."}\n'
              '  - {d: "D-072", t: "Bump-out south of EXIT (E); 8 ft public corridor from Concourse (E); X7 on the wall, X11 new; Mech (E) 675 SF."}'),
             ('  - {d: "MEP", t: "Core-2 plumbing routing and 16 ft bump-out height (ASSUMED)"}',
              '  - {d: "MEP", t: "Total mech ≈ 4.1 % vs 5 % (D-072; annex can absorb ~800 SF); core-2 plumbing"}')]:
    rep(a, b)
i = s.index("index_note: ")
j = s.index("\n", i)
s = s[:i] + ('index_note: "D-071: Set Rev B approved (G-001 A, G-002 C, G-003 K, C-101 E, A-101 I, A-102 F, A-111 C, A-201 H, A-301 D, A-302 C, '
             'A-901 C; frozen). Rev D sheets carry D-072 (core 2 off the public corridor (E), X11; GSF unchanged) and are IN REVIEW. Set Rev A / B / C kept unchanged."') + s[j:]
open(B + "params/phase2_cover_rev_c.yaml", "w", encoding="utf-8").write(s)
yaml.safe_load(s)

p = B + "phase2/src/p2_g_001.py"
g = open(p, encoding="utf-8").read()
for a, b in [('    ap.add_argument("--rev", choices=["A", "B"], default="B")', '    ap.add_argument("--rev", choices=["A", "B", "C"], default="C")'),
             ('rd({"A": "phase2_cover.yaml", "B": "phase2_cover_rev_b.yaml"}[a.rev])', 'rd({"A": "phase2_cover.yaml", "B": "phase2_cover_rev_b.yaml", "C": "phase2_cover_rev_c.yaml"}[a.rev])')]:
    assert g.count(a) == 1, a
    g = g.replace(a, b)
open(p, "w", encoding="utf-8").write(g)
print("cover rev c ok")
