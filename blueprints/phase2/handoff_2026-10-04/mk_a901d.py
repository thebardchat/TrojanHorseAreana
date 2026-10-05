B = "C:/Users/Hubby/AppData/Local/Temp/claude/C--Users-Hubby-Desktop-ARENA/202807a2-361c-4275-8ca9-11bac63af77d/scratchpad/repo/blueprints/"
import yaml

s = open(B + "params/phase2_massing_rev_c.yaml", encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:90])
    s = s.replace(a, b)


hdr = ("# phase2_massing_rev_d.yaml: P2-A-901 Rev D overrides. Read by phase2/src/p2_a_901.py --rev D with params/phase2_massing.yaml.\n"
       "# Rev D, 2026-10-04 evening (Shane, D-072; Claude Code session): plan Rev J — restroom bump-out 30 x 56 ft slid 42 ft south (entirely\n"
       "# south of EXIT (E)), X7 back on the building wall, new exit X11; C-101 Rev F site. Rev C inputs stay in phase2_massing_rev_c.yaml.\n"
       "# Rev C header (kept for history):\n")
rep("  revision: C\n  file: P2-A-901_RevC\n  model_file: P2-A-901_RevC_massing\n",
    "  revision: D\n  file: P2-A-901_RevD\n  model_file: P2-A-901_RevD_massing\n  drawn_by: \"Drawn by Claude (AI) for Shane Brazelton\"\n")
rep("  plan_l1: params/phase2_plan_rev_i.yaml\n  site_rev: rev_e\n", "  plan_l1: params/phase2_plan_rev_j.yaml\n  site_rev: rev_f\n")
rep('  text: "P2-A-101 Rev I (annex + east restroom bump-out, X7 at x 240); P2-C-101 Rev E (walk bands, apron unchanged); heights as Rev A (P2-A-201 Rev H)"',
    '  text: "P2-A-101 Rev J (annex + east restroom bump-out 42 ft south of EXIT (E), X7 on the wall, X11); P2-C-101 Rev F; heights as Rev A (P2-A-201 Rev I)"')
rep('  - {id: D-069, text: "restroom core 2 in a one-storey bump-out 30 x 56 ft on the east wall at V2 (16 ft ASSUMED), X7 on its east face", source: "DECISIONS.md D-069"}',
    '  - {id: D-069, text: "restroom core 2 in a one-storey bump-out 30 x 56 ft on the east wall (16 ft ASSUMED)", source: "DECISIONS.md D-069"}\n'
    '  - {id: D-072, text: "bump-out slid 42 ft south, entirely south of EXIT (E); public corridor (E) inside (not modelled); X7 back on the wall, X11 new", source: "_KEYSTONE/DECISIONS_ARENA.md D-072"}')
s = hdr + s.rstrip("\n") + '''
decisions_head: "DECISIONS MODELLED — SHANE 3:31 PM CT + EVENING (D-072)"
bumpout_label: "RESTROOM BUMP-OUT 30' x 56', 16' ASSUMED (D-072) · X11 S, X7 N"
bumpout_cut_label: "restroom bump-out, cut (D-072)"
sources: "Sources: params/phase2_massing.yaml, phase2_massing_rev_d.yaml; phase2_plan_rev_j.yaml; phase2_elev_rev_g.yaml; phase2_elev.yaml; phase2_site.yaml (rev_f); phase2_sect.yaml; D-034, D-043, D-045, D-046, D-050, D-054, D-061, D-065 to D-067, D-069, D-072; Shane 2026-10-04 evening. P2-A-201 Rev I shows the annex + bump-out."
'''
open(B + "params/phase2_massing_rev_d.yaml", "w", encoding="utf-8").write(s)
yaml.safe_load(open(B + "params/phase2_massing_rev_d.yaml", encoding="utf-8"))
print("massing rev d ok")

p = B + "phase2/src/p2_a_901.py"
g = open(p, encoding="utf-8").read()
n = g.count('REV in ("B", "C")')
g = g.replace('REV in ("B", "C")', 'REV in ("B", "C", "D")')
print("REV in replacements", n)


def rg(a, b):
    global g
    assert g.count(a) == 1, (g.count(a), a[:90])
    g = g.replace(a, b)


rg('        "drawn_by": meta2["drawn_by"],', '        "drawn_by": (mb or {}).get("meta", {}).get("drawn_by", meta2["drawn_by"]),')
rg('        cr.head("DECISIONS MODELLED — SHANE 3:31 PM CT" if REV == "C" else "DECISIONS MODELLED — SHANE 1:21 / 1:22 PM CT", size=6.6)',
   '        cr.head(mb.get("decisions_head", "DECISIONS MODELLED — SHANE 3:31 PM CT" if REV == "C" else "DECISIONS MODELLED — SHANE 1:21 / 1:22 PM CT"), size=6.6)')
rg('    if REV == "C":\n        cr.para("Sources: params/phase2_massing.yaml, phase2_massing_rev_c.yaml;',
   '    if mb and mb.get("sources"):\n        cr.para(mb["sources"], size=4.7, color=GRY)\n    elif REV == "C":\n        cr.para("Sources: params/phase2_massing.yaml, phase2_massing_rev_c.yaml;')
rg('''                    leader(sh, P, lb["bumpout"], 0.25, 0.35, "restroom bump-out, cut (D-069)", size=4.2)''',
   '''                    leader(sh, P, lb["bumpout"], 0.25, 0.35, mb.get("bumpout_cut_label", "restroom bump-out, cut (D-069)"), size=4.2)''')
rg('''                leader(sh, P, lb["bumpout"], -0.2, -0.95, f"RESTROOM BUMP-OUT 30' x 56', {mb['bumpout']['height_ft']:g}' ASSUMED (D-069) · X7", size=4.2)''',
   '''                leader(sh, P, lb["bumpout"], -0.2, -0.95, mb.get("bumpout_label", f"RESTROOM BUMP-OUT 30' x 56', {mb['bumpout']['height_ft']:g}' ASSUMED (D-069) · X7"), size=4.2)''')
rg('    ap.add_argument("--rev", choices=["A", "B", "C"], default="C")', '    ap.add_argument("--rev", choices=["A", "B", "C", "D"], default="D")')
open(p, "w", encoding="utf-8").write(g)
print("a901 patched")
