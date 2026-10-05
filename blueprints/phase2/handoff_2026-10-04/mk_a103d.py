B = "C:/Users/Hubby/AppData/Local/Temp/claude/C--Users-Hubby-Desktop-ARENA/202807a2-361c-4275-8ca9-11bac63af77d/scratchpad/repo/blueprints/"
import yaml

s = open(B + "params/phase2_overlays_rev_c.yaml", encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, a[:90]
    s = s.replace(a, b)


hdr = ("# phase2_overlays_rev_d.yaml: P2-A-103 Rev D overrides. Read by phase2/src/p2_a_103.py --rev D with params/phase2_overlays.yaml.\n"
       "# Rev D, 2026-10-04 evening (Shane, D-072; Claude Code session): plan Rev J. Core 2 is now reached from Concourse (E) through the\n"
       "# 8 ft public corridor (E), never across the floor or through V2 / EXIT (E). The 8 ft V2 cross-aisle in the chair layouts stays as an\n"
       "# EGRESS aisle (floor -> V2 -> EXIT (E) -> X7). Loads unchanged (P2-G-002 Rev D). Rev C inputs stay in phase2_overlays_rev_c.yaml.\n"
       "# Rev C header (kept for history):\n")
rep("  revision: C\n  file: P2-A-103_RevC\n", "  revision: D\n  file: P2-A-103_RevD\n")
rep("  plan: params/phase2_plan_rev_i.yaml\n  code: params/phase2_code_rev_c.yaml\n  code_sheet: P2-G-002 Rev C\n  plan_sheet: P2-A-101 Rev I\n  life_safety_sheet: P2-A-111 Rev C\n",
    "  plan: params/phase2_plan_rev_j.yaml\n  code: params/phase2_code_rev_d.yaml\n  code_sheet: P2-G-002 Rev D\n  plan_sheet: P2-A-101 Rev J\n  life_safety_sheet: P2-A-111 Rev D\n  plan_rev: J\n")
rep('  plan_text: "P2-A-101 Rev I (event floor, mats, court, tiers, portal, V1, V2 identical to Rev H; adds the east restroom bump-out, core 2)"',
    '  plan_text: "P2-A-101 Rev J (event floor, mats, court, tiers, portal, V1, V2 identical to Rev H / I; core 2 off the public corridor (E), D-072)"')
rep('Keep the 8 ft V2 cross-aisle clear (route to core 2). Aisles measured', 'Keep the 8 ft V2 egress aisle clear. Aisles measured')
rep('Keep the 8 ft V2 cross-aisle clear (route to core 2). Rows:', 'Keep the 8 ft V2 egress aisle clear. Rows:')
rep('  - {id: D-070, status: DECIDED, text: "core 2 stays on the EAST wall at V2: chair layouts keep the V2 cross-aisle open (this sheet)", source: "_KEYSTONE/DECISIONS_ARENA.md D-070 (to merge)"}',
    '  - {id: D-070, status: DECIDED, text: "core 2 stays on the EAST wall", source: "_KEYSTONE/DECISIONS_ARENA.md D-070 (to merge)"}\n'
    '  - {id: D-072, status: DECIDED, text: "public corridor (E) from Concourse (E) to core 2, bump-out 42 ft south of EXIT (E), X11; restroom traffic never crosses the floor — the V2 aisle stays for egress", source: "_KEYSTONE/DECISIONS_ARENA.md D-072 (to merge)"}')
rep('(P2-A-101 Rev I, P2-A-111 Rev C; outside these views)"', '(P2-A-101 Rev J, P2-A-111 Rev D; outside these views)"')
rep('reached through V2 / EXIT (E) (P2-A-101 Rev I, P2-A-401 Rev C)"', 'now reached from Concourse (E) by the public corridor (P2-A-101 Rev J, P2-A-401 Rev D)"')
rep('  basis: "8 ft (96 in) cross-aisle on the V2 line (y 175.09-183.09), full floor width: west edge (athlete corridor, open) -> east 6 ft strip -> V2 -> EXIT (E) + core-2 corridor -> X7.',
    '  basis: "8 ft (96 in) EGRESS cross-aisle on the V2 line (y 175.09-183.09), full floor width: west edge (athlete corridor, open) -> east 6 ft strip -> V2 -> EXIT (E) -> X7 (clear, D-072). Restroom traffic goes out the portal to Concourse (E) and the public corridor, not this way.')
rep('decisions_head: "DECISIONS — SHANE 1:21 / 1:22 / 3:31 PM CT + D-070"', 'decisions_head: "DECISIONS — SHANE 1:21 / 1:22 / 3:31 PM CT + D-070 / D-072"')
rep('screening_note: "Screening bay (D-065) is in the lobby, outside these views: P2-A-101 Rev I / P2-A-111 Rev C."',
    'screening_note: "Screening bay (D-065) is in the lobby, outside these views: P2-A-101 Rev J / P2-A-111 Rev D."')
s = hdr + s.rstrip("\n") + '''
aisle_label: "KEEP CLEAR 8' → V2 → EXIT (E) / X7"
aisle_head: "CHAIR LAYOUTS — V2 EGRESS AISLE (D-072)"
aisle_bullet: " Every chair layout keeps the 8' V2 aisle open for egress (floor → V2 → EXIT (E) → X7). Restrooms: portal → Concourse (E) → public corridor → core 2 (D-072)."
panel_sub: "8' V2 egress aisle kept (D-072)"
sources: "Sources: params/phase2_overlays.yaml, phase2_overlays_rev_d.yaml; phase2_plan_rev_j.yaml; phase2_code_rev_d.yaml; R-005 (NFHS Wrestling 2-1-2, 2-1-5, 2-2-1, 2-2-2, 2-3; KHSAA); R-012; R-019; R-008 / Hussey MAXAM; R-007.2 (IBC 2021 T1004.5); IBC 2021 1004.9, 1030.1.1, 1030.9.1, 1030.13.1, 1030.13.2 (UpCodes, retrieved 2026-10-04); P2-G-002 Rev D; P2-A-111 Rev D; P2-A-401 Rev D; D-053, D-054, D-064 to D-072; Shane 2026-10-04 evening."
'''
open(B + "params/phase2_overlays_rev_d.yaml", "w", encoding="utf-8").write(s)
yaml.safe_load(open(B + "params/phase2_overlays_rev_d.yaml", encoding="utf-8"))
print("overlays rev d ok")

p = B + "phase2/src/p2_a_103.py"
g = open(p, encoding="utf-8").read()


def rg(a, b):
    global g
    assert g.count(a) == 1, (g.count(a), a[:90])
    g = g.replace(a, b)


rg('    if rev in ("B", "C"):\n        rb = rd("phase2_overlays_rev_b.yaml" if rev == "B" else "phase2_overlays_rev_c.yaml")',
   '    if rev in ("B", "C", "D"):\n        rb = rd({"B": "phase2_overlays_rev_b.yaml", "C": "phase2_overlays_rev_c.yaml", "D": "phase2_overlays_rev_d.yaml"}[rev])')
rg('''f"KEEP CLEAR {va['width_in'] // 12:g}' → V2 → CORE 2"''', '''rb.get("aisle_label", f"KEEP CLEAR {va['width_in'] // 12:g}' → V2 → CORE 2")''')
rg('''chairs = design (D-054) · 8' aisle to V2 kept (D-070)", GRN)''', '''chairs = design (D-054) · " + rb.get("panel_sub", "8' aisle to V2 kept (D-070)"), GRN)''')
rg('    pr = "I" if rc else "H"', '    pr = rb["basis"].get("plan_rev", "I") if rc else "H"')
rg('''+ (" Every chair layout keeps the 8' V2 cross-aisle open: floor → V2 → EXIT (E) + core-2 corridor (restrooms, DF) → X7 (D-069 / D-070; panel d)." if rc else ""),''',
   '''+ (rb.get("aisle_bullet", " Every chair layout keeps the 8' V2 cross-aisle open: floor → V2 → EXIT (E) + core-2 corridor (restrooms, DF) → X7 (D-069 / D-070; panel d).") if rc else ""),''')
rg('''(G-002 Rev {'C' if rc else 'B'}, 114' x 144';''', '''(G-002 Rev {rb['basis']['code_sheet'][-1] if rc else 'B'}, 114' x 144';''')
rg('        cr.head("CHAIR LAYOUTS — AISLE TO V2 / CORE 2 (D-069, D-070)", size=7.2)',
   '        cr.head(rb.get("aisle_head", "CHAIR LAYOUTS — AISLE TO V2 / CORE 2 (D-069, D-070)"), size=7.2)')
rg('''    if rc:
        cr.para("Sources: params/phase2_overlays.yaml, phase2_overlays_rev_c.yaml;''',
   '''    if rb.get("sources"):
        cr.para(rb["sources"], size=5.3, color=GRY)
    elif rc:
        cr.para("Sources: params/phase2_overlays.yaml, phase2_overlays_rev_c.yaml;''')
rg('    ap.add_argument("--rev", choices=["A", "B", "C"], default="C")', '    ap.add_argument("--rev", choices=["A", "B", "C", "D"], default="D")')
rg('Usage (from the repo root):', 'Rev D (2026-10-04 evening, D-072): plan Rev J; core 2 off the public corridor (E); the V2 aisle stays as an egress aisle.\nUsage (from the repo root):')
open(p, "w", encoding="utf-8").write(g)
print("a103 patched")
