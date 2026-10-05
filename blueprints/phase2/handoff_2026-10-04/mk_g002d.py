B = "C:/Users/Hubby/AppData/Local/Temp/claude/C--Users-Hubby-Desktop-ARENA/202807a2-361c-4275-8ca9-11bac63af77d/scratchpad/repo/blueprints/"
import yaml

s = open(B + "params/phase2_code_rev_c.yaml", encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, a[:90]
    s = s.replace(a, b)


hdr = ("# phase2_code_rev_d.yaml: CODE ANALYSIS inputs for P2-G-002 Rev D (and P2-A-111 Rev D / P2-A-103 Rev D via p2_g_002.compute(rev=\"D\")).\n"
       "# Rev D = Shane 2026-10-04 evening, D-072 (Claude Code session): plan Rev J — core-2 bump-out 42 ft south, 8 ft PUBLIC CORRIDOR (E)\n"
       "# from Concourse (E), restroom doors only onto it, EXIT (E) clear (X7 back on the building wall), new exterior exit X11 off the\n"
       "# corridor, Mech (E) 1,720 -> 674.5 SF + MECH (E2) 660 SF. Rev C inputs stay in phase2_code_rev_c.yaml (G-002 Rev C APPROVED, D-071).\n"
       "# Rev C header (kept for history):\n")
rep("  revision: C\n  file: P2-G-002_RevC", "  revision: D\n  file: P2-G-002_RevD")
rep('    - {label: "Mech / elec (4 rooms)", ids: [mech_nw, mech_n, mech_e, mech_ne], factor: storage, source: "R-007.2; plan Rev F"}',
    '    - {label: "Mech / elec (5 rooms)", ids: [mech_nw, mech_n, mech_e, mech_ne, mech_e2], factor: storage, source: "R-007.2; plan Rev J (Mech (E) 674.5 + MECH (E2) 660, D-072)"}')
rep("  openings: [E1, X1, X2, X3, X4, X5, X6, X7, X8, X9, X10]", "  openings: [E1, X1, X2, X3, X4, X5, X6, X7, X8, X9, X10, X11]")
rep('    - "Exit access travel (T1017.2, A sprinklered): 250 ft. L2 worst measured ≈ 141 ft (R-018.4, Rev D plan; not re-measured on Rev F). L1 (P2-A-111 Rev C, plan Rev I): event floor centre → V2 → EXIT (E) + core-2 corridor → X7 (moved 30 ft east) ≈ 163 ft ≤ 250 (diagram measurement, UNVERIFIED)."',
    '    - "Exit access travel (T1017.2, A sprinklered): 250 ft. L2 worst ≈ 141 ft (R-018.4). L1 (P2-A-111 Rev D, plan Rev J): event floor centre → V2 → EXIT (E) → X7 (back on the wall) ≈ 133 ft; women\'s room (2) far corner → public corridor → X11 ≈ 59 ft (diagram measurements, UNVERIFIED)."')
rep('    - "Common path: seats 30 ft to two directions (1030.8; rows not drawn, TBD). Spaces with one exit: T1006.2.1 Group A 49 occupants / 75 ft — locker rooms (71 each) have 2 exits (X2 / X3 + corridor); event lockers (18 each) one door OK if the common path <= 75 ft (TBD)."',
    '    - "Common path (T1006.2.1, Group A, 75 ft): core 2 → public corridor → X11 or Concourse (E) ≈ 59 ft; without X11 it would be ≈ 115 ft (FAIL) — X11 added (D-072). Seats 30 ft (1030.8; rows TBD). Locker rooms 2 exits; event lockers one door if <= 75 ft (TBD)."')
rep('    - "Core 2 (D-069 CLOSED): plumbing routing + 16 ft height ASSUMED (MEP); X7 discharge to a public way TBD (1028, D-006); chair layouts keep an aisle to V2."',
    '    - "Core 2 (D-072): total mech ≈ 4.1 % of GSF vs 5 % planning (MEP engineer; annex can absorb ~800 SF later); plumbing + 16 ft bump-out ASSUMED; X7 / X11 discharge TBD (1028, D-006)."')
rep('  source: "D-008 (OPEN); D-069 CLOSED 3:31 PM CT + D-070 (core 2 east);', '  source: "D-008 (OPEN); D-069 CLOSED 3:31 PM CT + D-070 (core 2 east) + D-072 (public corridor, X11);')
rep('  decision: "D-069 CLOSED = Option 2 (Shane 3:31 PM CT): core 2 in a one-storey 30 x 56 ft bump-out, east wall at V2; SW FLEX unchanged (D-039). East confirmed (D-070)."',
    '  decision: "Core 2 (D-069 / D-070 / D-072): one-storey 30 x 56 ft bump-out on the east wall, south of EXIT (E); reached by the 8 ft public corridor from Concourse (E), never through EXIT (E)."')
rep("    lobby_core: {wc_m: 10, wc_f: 18, lav_m: 4, lav_f: 5, df: 2, label: \"L1 lobby core (rooms 4 + 5)\"}",
    "    lobby_core: {wc_m: 10, wc_f: 18, lav_m: 4, lav_f: 5, df: 2, label: \"L1 lobby core (rooms 4 + 5)\"}")
s = hdr + s.rstrip("\n") + '''

rev_d:
  plan_sheet: P2-A-101 Rev J
  site_sheet: P2-C-101 Rev F
  header: "CODE ANALYSIS — SCHEMATIC (REV D) · P2-A-101 REV J / A-102 REV F · P2-G-003 REV K · D-072 PUBLIC CORRIDOR (E)"
  size_note: "P2-A-101 Rev J incl. the 2,100 SF storage annex + 1,680 SF restroom bump-out (moved 42 ft south, D-072)"
  source: "Shane 2026-10-04 evening (D-072 GO); phase2_plan_rev_j.yaml"
'''
open(B + "params/phase2_code_rev_d.yaml", "w", encoding="utf-8").write(s)
yaml.safe_load(open(B + "params/phase2_code_rev_d.yaml", encoding="utf-8"))
print("code rev d ok")

# ---- generator
p = B + "phase2/src/p2_g_002.py"
g = open(p, encoding="utf-8").read()


def rg(a, b):
    global g
    assert g.count(a) == 1, a[:90]
    g = g.replace(a, b)


rg('    code, p2 = rd({"A": "phase2_code.yaml", "B": "phase2_code_rev_b.yaml", "C": "phase2_code_rev_c.yaml"}[rev]), rd("phase2.yaml")',
   '    code, p2 = rd({"A": "phase2_code.yaml", "B": "phase2_code_rev_b.yaml", "C": "phase2_code_rev_c.yaml", "D": "phase2_code_rev_d.yaml"}[rev]), rd("phase2.yaml")')
rg('    plan = h["plan"] if rev == "A" else rd("phase2_plan_rev_h.yaml" if rev == "B" else "phase2_plan_rev_i.yaml")',
   '    plan = h["plan"] if rev == "A" else rd({"B": "phase2_plan_rev_h.yaml", "C": "phase2_plan_rev_i.yaml", "D": "phase2_plan_rev_j.yaml"}[rev])')
rg('    rb = cm["revision"] in ("B", "C")\n    rc = cm["revision"] == "C"',
   '    rb = cm["revision"] in ("B", "C", "D")\n    rc = cm["revision"] in ("C", "D")\n    rdd = code.get("rev_d")')
rg('        if rc:\n            sh.text(0.75, top - 0.2, "CODE ANALYSIS — SCHEMATIC (REV C)',
   '        if rdd:\n            sh.text(0.75, top - 0.2, rdd["header"], size=11.5, bold=True)\n        elif rc:\n            sh.text(0.75, top - 0.2, "CODE ANALYSIS — SCHEMATIC (REV C)')
rg('        pl = "P2-A-101 Rev I incl. the 2,100 SF storage annex + 1,680 SF restroom bump-out" if rc else "P2-A-101 Rev H incl. the 2,100 SF storage annex"',
   '        pl = rdd["size_note"] if rdd else "P2-A-101 Rev I incl. the 2,100 SF storage annex + 1,680 SF restroom bump-out" if rc else "P2-A-101 Rev H incl. the 2,100 SF storage annex"')
rg('    cols = [(("SPACE (drawn: A-101 Rev I, A-102 Rev F)" if rc else',
   '    cols = [(("SPACE (drawn: A-101 Rev J, A-102 Rev F)" if rdd else "SPACE (drawn: A-101 Rev I, A-102 Rev F)" if rc else')
rg('        "drawn_by": "Drawn by Claude (AI) for Shane Brazelton" if cm["revision"] == "C" else meta2["drawn_by"],',
   '        "drawn_by": "Drawn by Claude (AI) for Shane Brazelton" if cm["revision"] in ("C", "D") else meta2["drawn_by"],')
rg('''X1–X10 = {d['n_open'] - 1} x {dw} in. "''', '''X1–X{d['n_open'] - 1} = {d['n_open'] - 1} x {dw} in. "''')
rg('''    rc = code["meta"]["revision"] == "C"\n    c3.para(f"Screening in a side bay of the lobby (P2-A-101 Rev {'I' if rc else 'H'}): clear''',
   '''    rc = code["meta"]["revision"] in ("C", "D")\n    pa = "J" if code.get("rev_d") else "I" if rc else "H"\n    c3.para(f"Screening in a side bay of the lobby (P2-A-101 Rev {pa}): clear''')
rg('''P2-C-101 Rev {'E' if rc else 'D'}; public way TBD''', '''P2-C-101 Rev {'F' if code.get("rev_d") else 'E' if rc else 'D'}; public way TBD''')
rg('    ap.add_argument("--rev", choices=["A", "B", "C"], default="C")', '    ap.add_argument("--rev", choices=["A", "B", "C", "D"], default="D")')
rg('Usage (from the repo root):',
   'Rev D (2026-10-04 evening, D-072): plan Rev J — X11 added to the openings, MECH (E2) to the mech rooms, travel / common path notes;\n'
   'data params/phase2_code_rev_d.yaml.\nUsage (from the repo root):')
open(p, "w", encoding="utf-8").write(g)
print("g002 patched")
