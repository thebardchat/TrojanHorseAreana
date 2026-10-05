B = "C:/Users/Hubby/AppData/Local/Temp/claude/C--Users-Hubby-Desktop-ARENA/202807a2-361c-4275-8ca9-11bac63af77d/scratchpad/repo/blueprints/"
import yaml

s = open(B + "params/phase2_life_safety_rev_c.yaml", encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, a[:90]
    s = s.replace(a, b)


hdr = ("# phase2_life_safety_rev_d.yaml: P2-A-111 LIFE SAFETY PLAN Rev D inputs. Read by phase2/src/p2_a_111.py --rev D.\n"
       "# Rev D = Shane 2026-10-04 evening, D-072 (Claude Code session): plan Rev J — core-2 bump-out 42 ft south of EXIT (E), 8 ft public\n"
       "# corridor (E) from Concourse (E), restroom doors only onto it, EXIT (E) clear with X7 back on the building wall, new exit X11 off\n"
       "# the corridor. Loads: params/phase2_code_rev_d.yaml via p2_g_002.compute(\"D\") (unchanged totals; X11 adds 64 in).\n"
       "# Rev C inputs stay in phase2_life_safety_rev_c.yaml (P2-A-111 Rev C APPROVED, D-071).\n# Rev C header (kept for history):\n")
rep("  revision: C\n  file: P2-A-111_RevC", "  revision: D\n  file: P2-A-111_RevD")
rep("  plan: params/phase2_plan_rev_i.yaml", "  plan: params/phase2_plan_rev_j.yaml")
rep('    - {id: T1, level: 1, label: "event floor center → V2 → EXIT (E) + corridor → X7 (moved 30 ft east)", pts: [[116, 140], [116, 179.09], [240, 179.09]], source: "KEYSTONE diagram measurement on plan Rev I (UNVERIFIED); X7 at the bump-out east face x 240 (D-069)"}',
    '    - {id: T1, level: 1, label: "event floor center → V2 → EXIT (E) → X7 (back on the building wall)", pts: [[116, 140], [116, 179.09], [210, 179.09]], source: "diagram measurement on plan Rev J (UNVERIFIED); X7 at x 210 (D-072)"}')
rep('    - {id: T7, level: 1, label: "women\'s room (2) far corner → corridor → X7", pts: [[210.5, 216.6], [215, 216.6], [215, 179.09], [240, 179.09]], source: "KEYSTONE diagram measurement on plan Rev I (UNVERIFIED; entry at x 215 ASSUMED, test-fit P2-A-401 Rev C)"}',
    '    - {id: T7, level: 1, label: "women\'s room (2) far corner → door (east wall, y 125) → public corridor → X11", pts: [[239.5, 152.6], [214, 152.6], [214, 125], [206, 125], [206, 112], [210, 112]], source: "diagram measurement on plan Rev J (UNVERIFIED; door y 121-129, test-fit P2-A-401 Rev D)"}\n'
    '    - {id: T8, level: 1, label: "men\'s room (2) far corner → door → public corridor → X11", pts: [[188.5, 133.7], [188.5, 121], [206, 121], [206, 112], [210, 112]], source: "diagram measurement on plan Rev J (UNVERIFIED; door location ASSUMED, test-fit P2-A-401 Rev D)"}')
rep('    - {space: "Restroom core 2 (D-069)", load: "accessory", result: "one entry each, off the corridor: women far corner → door 38 ft, men 34 ft (≤ 75), then two ways: W to V2 / floor, E to X7", status: "OK as planned (doors ASSUMED, UNVERIFIED)", source: "plan Rev I rooms 25-26; P2-A-401 Rev C; IBC 2021 Table 1006.2.1"}',
    '    - {space: "Restroom core 2 (D-072)", load: "accessory", result: "one door each onto the public corridor; there two ways: S to X11 or on to Concourse (E). Common path women 61 ft, men 30 ft (≤ 75). Without X11 women ≈ 130 ft (FAIL) — hence X11", status: "OK as planned (doors ASSUMED, UNVERIFIED)", source: "plan Rev J rooms 25-27 + pc_e + X11; P2-A-401 Rev D; IBC 2021 Table 1006.2.1"}')
rep('bump-out NE (240, 217.09) 323.6 ft: shorter); used for both levels"', 'bump-out NE (240, 175.09) 297.1 ft: shorter); used for both levels"')
rep('    text: "D-069 DECIDED Option 2 (Shane 3:31 PM CT): core 2 in a one-storey 30 x 56 ft bump-out on the east wall at V2 / EXIT (E).',
    '    text: "D-069 / D-070 / D-072: core 2 = WOMEN (2) in the one-storey 30 x 56 ft bump-out (now south of EXIT (E)) + MEN (2) and DF / JAN. in the old Mech (E) strip, all off the 8 ft public corridor (E).')
rep('      - "Floor chair layouts must keep an aisle to V2: core 2 is reached only through V2 / EXIT (E) (next A-103 rev)."',
    '      - "Public reaches core 2 from CONCOURSE (E) through the public corridor — never across the floor or through EXIT (E). Chair layouts keep the V2 aisle for egress (A-103 Rev D)."')
rep('    source: "Shane 2026-10-04 3:31 PM CT (D-069 Option 2); plan Rev I; P2-A-401 Rev C;', '    source: "Shane 2026-10-04 3:31 PM CT (D-069 Option 2) + evening (D-072); plan Rev J; P2-A-401 Rev D;')
rep('    text: "EXIT (E) runs 30 ft on through the bump-out to X7: 8 ft = 96 in ≥ 44 in corridor (T1020.3) and the 64 in X7 pair; restroom doors and the DF alcove open off it, no queuing in it (1003.6). T1 163 ft ≤ 250. X7 discharges east: path to a public way TBD (1028, D-006; C-101 Rev E)."',
    '    text: "PUBLIC CORRIDOR (E) 8 ft = 96 in ≥ 44 in (T1020.3), Concourse (E) → core 2, behind the tier line; restroom + DF doors open only onto it; dead end beyond the last door ≈ 5 ft ≤ 20 ft (1020.5). X11 (64 in) off it, south of the bump-out. EXIT (E) clear: no doors, no queues (1003.6); X7 back on the wall, T1 133 ft ≤ 250. X7 / X11 discharge to a public way TBD (1028, D-006; C-101 Rev F)."')
rep('    source: "plan Rev I zones.exit_e + doors.X7; IBC 2021 1003.6, T1020.3 (R-018), 1028; Shane 3:31 PM CT"',
    '    source: "plan Rev J zones.pc_e / exit_e + doors.X7 / X11; IBC 2021 1003.6, T1020.3 (R-018), 1020.5, 1028; Shane evening (D-072)"')
rep("P2-C-101 Rev D.\"\n", "P2-C-101 Rev F.\"\n")
open(B + "params/phase2_life_safety_rev_d.yaml", "w", encoding="utf-8").write(hdr + s)
yaml.safe_load(open(B + "params/phase2_life_safety_rev_d.yaml", encoding="utf-8"))
print("ls rev d ok")

p = B + "phase2/src/p2_a_111.py"
g = open(p, encoding="utf-8").read()


def rg(a, b):
    global g
    assert g.count(a) == 1, a[:90]
    g = g.replace(a, b)


rg('    rc = rev == "C"                 # Rev C (Shane 3:31 PM CT): D-069 east restroom bump-out, plan Rev I; Revs A / B stay byte-identical\n'
   '    rb = rev in ("B", "C")\n    d = g2.compute("B" if rb else "A")',
   '    rc = rev in ("C", "D")          # Rev C (Shane 3:31 PM CT): D-069 east restroom bump-out, plan Rev I; Revs A / B stay byte-identical\n'
   '    rb = rev in ("B", "C", "D")\n    d = g2.compute("D" if rev == "D" else "B" if rb else "A")')
rg('    if rc:\n        ls, plan = rd("phase2_life_safety_rev_c.yaml"), rd("phase2_plan_rev_i.yaml")',
   '    if rc:\n        ls, plan = rd("phase2_life_safety_rev_c.yaml"), rd("phase2_plan_rev_i.yaml")\n'
   '    if rev == "D":                  # Rev D (D-072): plan Rev J, public corridor (E), X11, X7 back on the wall\n'
   '        ls, plan = rd("phase2_life_safety_rev_d.yaml"), rd("phase2_plan_rev_j.yaml")')
rg('    rb = c["rev"] in ("B", "C")\n    rc = c["rev"] == "C"\n    py0 = 4.62',
   '    rb = c["rev"] in ("B", "C", "D")\n    rc = c["rev"] in ("C", "D")\n    rdd = c["rev"] == "D"\n    py0 = 4.62')
rg('    if rc:\n        sh.text(3.55, top - 0.16, "LEVEL 1 — PLAN REV I", size=9.5, bold=True)',
   '    if rdd:\n        sh.text(3.55, top - 0.16, "LEVEL 1 — PLAN REV J", size=9.5, bold=True)\n'
   '        sh.text(3.55, top - 0.31, "D-065 bay · D-067 annex · D-072 public corridor (E)", size=6.0)\n'
   '    elif rc:\n        sh.text(3.55, top - 0.16, "LEVEL 1 — PLAN REV I", size=9.5, bold=True)')
rg('    if rc:\n        pl.text(225, 203, "WOMEN (2)", size=3.9, bold=True, align="center", layer=L_TAG)',
   '    if rdd:\n'
   '        pl.text(225, 141, "WOMEN (2)", size=3.9, bold=True, align="center", layer=L_TAG)\n'
   '        pl.text(225, 135.5, "24 WC · 7 LAV", size=3.6, align="center", layer=L_TAG)\n'
   '        pl.text(195, 127, "MEN (2)", size=3.4, bold=True, align="center", layer=L_TAG)\n'
   '        a_, b_ = pl.P(206.8, 84)\n'
   '        sh.text(a_, b_, "PUBLIC CORR. 8\'", size=3.6, bold=True, align="center", layer=L_TAG, rot=90, color=GRN)\n'
   '        draw_path(pl, paths["T7"], RED, 243.5, 150)\n'
   '        draw_path(pl, paths["T8"], RED, 163, 116)\n'
   '    elif rc:\n        pl.text(225, 203, "WOMEN (2)", size=3.9, bold=True, align="center", layer=L_TAG)')
rg('''           "mech_e": (199, 95), "mech_ne": (198, 235), "first_aid": (136, 31.5), "concession": (134.5, 46)}''',
   '''           "mech_e": (199, 95), "mech_ne": (198, 235), "first_aid": (136, 31.5), "concession": (134.5, 46)}
    if rdd:
        olp.update(mech_e=(195, 76), mech_e2=(225, 162))''')
rg('''             ("discharge", "EXIT DISCHARGE — 40 FT WALK (D-066 DECIDED) — CHECK")) if rc else''',
   '''             ("discharge", "EXIT DISCHARGE — 40 FT WALK (D-066 DECIDED) — CHECK")) if rc and not rdd else
            (("screening", "SCREENING BAY vs EGRESS (D-065 DECIDED) — CHECK"), ("restrooms", "RESTROOMS — CORE 2 OFF THE PUBLIC CORRIDOR (D-072)"),
             ("discharge", "EXIT DISCHARGE — 40 FT WALK (D-066 DECIDED) — CHECK")) if rdd else''')
rg('''    if rc:\n        c2.head("EXIT (E) THROUGH THE BUMP-OUT (D-069) — CHECK", size=7.0)''',
   '''    if rc:\n        c2.head("PUBLIC CORRIDOR (E) + X11, EXIT (E) CLEAR (D-072) — CHECK" if rdd else "EXIT (E) THROUGH THE BUMP-OUT (D-069) — CHECK", size=7.0)''')
rg('''    c2.para("Sources: P2-G-002 Rev B; P2-A-101 Rev I / A-102 Rev F (params/phase2_plan_rev_i.yaml); params/phase2_life_safety_rev_c.yaml; IBC 2021 "''',
   '''    c2.para("Sources: P2-G-002 Rev D; P2-A-101 Rev J / A-102 Rev F (params/phase2_plan_rev_j.yaml); params/phase2_life_safety_rev_d.yaml; IBC 2021 "
            "1003.6, 1006.2.1, 1007.1, 1017.2-3, T1020.3, 1020.5, 1028, 1030.2-3, 2902.3.3; Shane 3:31 PM CT + evening (D-072)." if rdd else
            "Sources: P2-G-002 Rev B; P2-A-101 Rev I / A-102 Rev F (params/phase2_plan_rev_i.yaml); params/phase2_life_safety_rev_c.yaml; IBC 2021 "''')
rg('    ap.add_argument("--rev", choices=["A", "B", "C"], default="C")', '    ap.add_argument("--rev", choices=["A", "B", "C", "D"], default="D")')
rg('Usage (from the repo root):', 'Rev D (2026-10-04 evening, D-072): plan Rev J, public corridor (E), X11, X7 back on the wall; T1 / T7 / T8 re-measured.\nUsage (from the repo root):')
open(p, "w", encoding="utf-8").write(g)
print("a111 patched")
