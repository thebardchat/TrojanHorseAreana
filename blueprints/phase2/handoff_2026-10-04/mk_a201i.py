B = "C:/Users/Hubby/AppData/Local/Temp/claude/C--Users-Hubby-Desktop-ARENA/202807a2-361c-4275-8ca9-11bac63af77d/scratchpad/repo/blueprints/"
import yaml

s = open(B + "params/phase2_elev_rev_h.yaml", encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:90])
    s = s.replace(a, b)


hdr = ("# phase2_elev_rev_i.yaml: P2-A-201 Rev I overlay = Rev H overlay + Plan Rev J outline (Shane 2026-10-04 evening, D-072; Claude Code\n"
       "# session): the 30 x 56 ft restroom bump-out slid 42 ft south (y 119.09-175.09, entirely south of EXIT (E)); X7 back on the building\n"
       "# wall (just north of the bump-out); new exit X11 on the east wall just south of it. Rev H overlay stays in phase2_elev_rev_h.yaml.\n")
rep("meta:\n  revision: H\n", "meta:\n  revision: I\n  drawn_by: \"Drawn by Claude (AI) for Shane Brazelton\"\n"
    "  change_rev_i: \"outline from P2-A-101 Rev J (D-072): restroom bump-out 30 x 56 ft slid 42 ft south, entirely south of EXIT (E); X7 back on the building wall; new exit X11 off the public corridor, just south of the bump-out\"\n"
    "  source_rev_i: \"Shane 2026-10-04 evening (D-072 GO: A-201 Rev I)\"\n")
rep('  outline: "OUTLINE (P2-A-101 Rev I): storage annex 70\' x 30\' on the north wall (D-067) + restroom bump-out 30\' x 56\' on the east wall (D-069), one storey, 16\' ASSUMED. Roofs / finishes TBD."',
    '  outline: "OUTLINE (P2-A-101 Rev J): storage annex 70\' x 30\' on the north wall (D-067) + restroom bump-out 30\' x 56\' on the east wall, south of EXIT (E) (D-069 / D-072), one storey, 16\' ASSUMED. X7 on the wall, X11 new. Roofs / finishes TBD."')
rep("plan_file: phase2_plan_rev_i.yaml\nplan_file_source: \"P2-A-101 Rev I geometry (Shane 3:31 PM CT: D-069 east restroom bump-out; annex D-067; L2 = A-102 Rev F, unchanged)\"",
    "plan_file: phase2_plan_rev_j.yaml\nplan_file_source: \"P2-A-101 Rev J geometry (Shane evening, D-072: bump-out 42 ft south, X7 on the wall, X11; annex D-067; L2 = A-102 Rev F, unchanged)\"")
rep('  key_wall: "BUILDING — SOUTH WALL (P2-A-101 Rev I)"\n  key_sub: "north up · site plan: P2-C-101 Rev E"',
    '  key_wall: "BUILDING — SOUTH WALL (P2-A-101 Rev J)"\n  key_sub: "north up · site plan: P2-C-101 Rev F"')
rep('  doors_note: "DOORS: symbols (6\' x 8\' ASSUMED) from P2-A-101 Rev I; X# EXIT ONLY (D-033); X7 on the bump-out, S1 on the annex, size TBD (D-034)."',
    '  doors_note: "DOORS: symbols (6\' x 8\' ASSUMED) from P2-A-101 Rev J; X# EXIT ONLY (D-033); X7 on the wall, X11 off the public corridor, S1 on the annex, size TBD."')
s = hdr + s.rstrip("\n") + '''

text_rev_i:
  south_bumpout: "beyond, 119' back (D-072)"
  east_bumpout: "in front · 16' ASSUMED · X11 S of it, X7 N of it"
  east_title: "RESTROOM BUMP-OUT 30' x 56' (D-072)"
  source: "plan Rev J building.bumpout (y 119.09) + doors X7 / X11"
'''
open(B + "params/phase2_elev_rev_i.yaml", "w", encoding="utf-8").write(s)
yaml.safe_load(open(B + "params/phase2_elev_rev_i.yaml", encoding="utf-8"))
print("elev rev i ok")

p = B + "phase2/src/p2_a_201.py"
g = open(p, encoding="utf-8").read()


def rg(a, b):
    global g
    assert g.count(a) == 1, (g.count(a), a[:90])
    g = g.replace(a, b)


rg('    if rev in ("B", "C", "D", "E", "F", "G", "H"):', '    if rev in ("B", "C", "D", "E", "F", "G", "H", "I"):')
rg('        "drawn_by": meta2["drawn_by"],', '        "drawn_by": (evb or {}).get("meta", {}).get("drawn_by", meta2["drawn_by"]),')
rg('''        elS.text((bo[0] + bo[2]) / 2, evb["bumpout"]["height_ft"] + 1.6, "beyond, 161' back (D-069)", size=4.4, align="center", layer=L_TAG)''',
   '''        elS.text((bo[0] + bo[2]) / 2, evb["bumpout"]["height_ft"] + 1.6, evb.get("text_rev_i", {}).get("south_bumpout", "beyond, 161' back (D-069)"), size=4.4, align="center", layer=L_TAG)''')
rg('''        elE.text(bm, 23.0, f"RESTROOM BUMP-OUT {bo[2] - bo[0]:g}' x {bo[3] - bo[1]:g}' (D-069)", size=4.2, bold=True, align="center", layer=L_TAG)
        elE.text(bm, 19.6, f"in front · {evb['bumpout']['height_ft']:g}' ASSUMED · X7 on its east face", size=4.0, align="center", layer=L_TAG)''',
   '''        ti = evb.get("text_rev_i", {})
        elE.text(bm, 23.0, ti.get("east_title", f"RESTROOM BUMP-OUT {bo[2] - bo[0]:g}' x {bo[3] - bo[1]:g}' (D-069)"), size=4.2, bold=True, align="center", layer=L_TAG)
        elE.text(bm, 19.6, ti.get("east_bumpout", f"in front · {evb['bumpout']['height_ft']:g}' ASSUMED · X7 on its east face"), size=4.0, align="center", layer=L_TAG)''')
rg('    ap.add_argument("--rev", choices=["A", "B", "C", "D", "E", "F", "G", "H"], default="H")',
   '    ap.add_argument("--rev", choices=["A", "B", "C", "D", "E", "F", "G", "H", "I"], default="I")')
open(p, "w", encoding="utf-8").write(g)
print("a201 patched")
