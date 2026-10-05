P = "C:/Users/Hubby/AppData/Local/Temp/claude/C--Users-Hubby-Desktop-ARENA/202807a2-361c-4275-8ca9-11bac63af77d/scratchpad/repo/blueprints/phase2/src/p2_a_plan.py"
s = open(P, encoding="utf-8").read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('    rf = rev in ("F", "G", "H", "I")\n    rg = rev in ("G", "H", "I")\n    rh = rev in ("H", "I")\n    r_i = rev == "I"          # Rev I (Shane 3:31 PM CT): D-069 Option 2 east restroom bump-out; Rev H output stays byte-identical',
    '    rf = rev in ("F", "G", "H", "I", "J")\n    rg = rev in ("G", "H", "I", "J")\n    rh = rev in ("H", "I", "J")\n'
    '    r_i = rev in ("I", "J")   # Rev I (Shane 3:31 PM CT): D-069 Option 2 east restroom bump-out; Rev H output stays byte-identical\n'
    '    rj = rev == "J"           # Rev J (D-072): bump-out 42 ft south, public corridor (E), X7 back on the wall, X11; Rev I output unchanged')
rep('        if r_i and xa == xb == bx1:            # Rev I: east wall open where EXIT (E) runs into the bump-out corridor\n'
    '            ez = next(z_["rect"] for z_ in plan["level_1"]["zones"] if z_["id"] == "exit_e")',
    '        if r_i and xa == xb == bx1:            # Rev I: east wall open where EXIT (E) runs into the bump-out corridor\n'
    '            ez = next(z_["rect"] for z_ in plan["level_1"]["zones"] if z_["id"] == "exit_e")\n'
    '            if rj:                             # Rev J: opening = women\'s (2) door from the public corridor into the bump-out\n'
    '                ez = [bx1, 121.0, bx1, 129.0]')
rep('    if r_i:\n        at = [("", 0, "l"), ("DRAWN REV I", 1.75, "r"), ("REV H", 2.45, "r"),',
    '    if r_i:\n        at = [("", 0, "l"), ("DRAWN REV J" if rj else "DRAWN REV I", 1.75, "r"), ("REV I" if rj else "REV H", 2.45, "r"),')
rep('bold=l_ in ("", "DRAWN REV E", "DRAWN REV F", "DRAWN REV G", "DRAWN REV H", "DRAWN REV I")',
    'bold=l_ in ("", "DRAWN REV E", "DRAWN REV F", "DRAWN REV G", "DRAWN REV H", "DRAWN REV I", "DRAWN REV J")')
rep('                   "5 lav; women 24 WC, 7 lav; hi-lo DF + janitor. With the lobby core: 22 / 42 WC, 9 / 12 lav, 4 DF = chairs-only. Checks: A-111 C, A-401 C.")',
    '                   "5 lav; women 24 WC, 7 lav; hi-lo DF + janitor. With the lobby core: 22 / 42 WC, 9 / 12 lav, 4 DF = chairs-only. Checks: A-111 C, A-401 C.")\n'
    '    if rj:\n'
    '        acc1[1] = ("CORE 2 (D-069 / D-070 / D-072): bump-out 30 x 56 = 1,680 SF, one storey, slid 42 ft south — entirely south of EXIT (E). "\n'
    '                   "PUBLIC CORRIDOR (E) 8 ft (96 in) from CONCOURSE (E) north to core 2, behind the tier line: MEN (2) 25, DF / JAN. 27 and WOMEN (2) 26 "\n'
    '                   "open only onto it; X11 exit off it. EXIT (E) clear, X7 back on the wall. MECH (E) 1,720 -> 675 + MECH (E2) 660 SF (MEP OPEN). "\n'
    '                   "Storage annex 2,100 SF, S1. With the lobby core: 22 / 42 WC, 9 / 12 lav, 4 DF. Checks: A-111 D, A-401 D.")')
rep('                "1003.6, 1030.2, T2902.1, 2902.3.3; IPC 2021 424.2 (R-009); ADA 2010 211.2, 213.3. Geometry: params/phase2_plan_rev_i.yaml.")',
    '                "1003.6, 1030.2, T2902.1, 2902.3.3; IPC 2021 424.2 (R-009); ADA 2010 211.2, 213.3. Geometry: params/phase2_plan_rev_i.yaml.")\n'
    '    if rj:\n'
    '        src_ = ("Sources: phase2.yaml (D-033-D-039, D-054, D-064-D-069); DECISIONS_ARENA D-070-D-072; Shane 2026-10-04 3:31 PM CT + evening; "\n'
    '                "P2-G-003 K, A-111 D, A-401 D; IBC 2021 1003.6, 1006.2.1, 1020.3, 1020.5, 1030.2, T2902.1; IPC 2021 424.2 (R-009); ADA 2010 211.2, 213.3. "\n'
    '                "Geometry: params/phase2_plan_rev_j.yaml.")')
rep('        "revision": rev,\n        "drawn_by": meta2["drawn_by"],',
    '        "revision": rev,\n        "drawn_by": "Drawn by Claude (AI) for Shane Brazelton" if rj else meta2["drawn_by"],')
rep('    ap.add_argument("--rev", choices=["A", "B", "C", "D", "E", "F", "G", "H", "I"], default="F",',
    '    ap.add_argument("--rev", choices=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"], default="F",')
rep('''                                out["drawn"], out["drawn_d"], out["rev_f"]["rows"], rev="I"), "I"''',
    '''                                out["drawn"], out["drawn_d"], out["rev_f"]["rows"], rev="I"), "I"
    elif a.rev == "J":
        if a.sheet != "P2-A-101":
            sys.exit("Rev J is Level 1 only (P2-A-101); P2-A-102 stays at Rev F.")
        p2, prog, ob, out = tf.summary_kj()
        if [(r["side"], r["lower"], r["upper"]) for r in out["rows"]] != [(r["side"], r["lower"], r["upper"]) for r in out["rev_f"]["rows"]]:
            sys.exit(f"Rev J seat counts differ from Plan Rev I: {out['rows']}")
        sh, rv_letter = build_e(a.sheet, p2, prog, out["plan"], out["loop"], (out["rows"], out["tot"]), out["geom"],
                                out["drawn"], out["drawn_d"], out["rev_f"]["rows"], rev="J"), "J"''')
open(P, "w", encoding="utf-8").write(s)
print("patched")
