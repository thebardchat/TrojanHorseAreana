B = "C:/Users/Hubby/AppData/Local/Temp/claude/C--Users-Hubby-Desktop-ARENA/202807a2-361c-4275-8ca9-11bac63af77d/scratchpad/repo/blueprints/"
import re
import yaml

# ---- site yaml: rev_f block (copy of rev_e with plan Rev J + bump-out moved)
s = open(B + "params/phase2_site.yaml", encoding="utf-8").read()
SKIP = "\nrev_f:\n" in s
i = s.index("\nrev_e:\n") + 1
m = re.search(r"\n\S", s[i + 6:])
j = i + 6 + m.start() + 1 if m else len(s)
blk = s[i:j]
f = blk.replace("rev_e:\n  revision: E\n  plan_file: phase2_plan_rev_i.yaml", "rev_f:\n  revision: F\n  plan_file: phase2_plan_rev_j.yaml")
f = f.replace("    bumpout: [210, 161.09, 240, 217.09]", "    bumpout: [210, 119.09, 240, 175.09]")
f = f.replace('    source: "phase2_plan_rev_i.yaml building + projection + annex + bumpout; Shane 2026-10-04 3:31 PM CT (D-069 Option 2)"',
              '    source: "phase2_plan_rev_j.yaml building + projection + annex + bumpout (moved 42 ft south, D-072); Shane 2026-10-04 3:31 PM CT (D-069) + evening (D-072)"')
f = f.replace('  source: "Shane 2026-10-04 3:31 PM CT (D-069 closed = Option 2, east restroom bump-out; C-101 Rev E if the outline changes)"',
              '  source: "Shane 2026-10-04 evening (D-072: bump-out 42 ft south of EXIT (E), public corridor (E), X11; C-101 Rev F)"')
assert f.count("rev_f:") == 1 and "119.09" in f and "plan_rev_j" in f
if not SKIP:
    s = s[:j] + f + s[j:] if s[j - 1] == "\n" else s[:j] + "\n" + f + s[j:]
    open(B + "params/phase2_site.yaml", "w", encoding="utf-8").write(s)
yaml.safe_load(open(B + "params/phase2_site.yaml", encoding="utf-8"))["rev_f"]["building"]["bumpout"]
print("site rev_f ok")

# ---- generator
p = B + "phase2/src/p2_c_101.py"
g = open(p, encoding="utf-8").read()
n0 = g.count('REV in ("D", "E")') + g.count('REV == "E"') + g.count('REV in ("B", "C", "D", "E")')
g = g.replace('REV in ("B", "C", "D", "E")', 'REV in ("B", "C", "D", "E", "F")')
g = g.replace('REV in ("D", "E")', 'REV in ("D", "E", "F")')
g = g.replace('REV == "E"', 'REV in ("E", "F")')
print("generic replacements", n0)


def rg(a, b):
    global g
    assert g.count(a) == 1, (g.count(a), a[:90])
    g = g.replace(a, b)


rg('        rb = si[{"B": "rev_b", "C": "rev_c", "D": "rev_d", "E": "rev_e"}[REV]]',
   '        rb = si[{"B": "rev_b", "C": "rev_c", "D": "rev_d", "E": "rev_e", "F": "rev_f"}[REV]]')
rg('''            v.text(bo[2] + 3, (bo[1] + bo[3]) / 2 + 4, "BUMP-OUT (D-069)", 4.4, bold=True)''',
   '''            v.text(bo[2] + 3, (bo[1] + bo[3]) / 2 + 4, "BUMP-OUT (D-072)" if REV == "F" else "BUMP-OUT (D-069)", 4.4, bold=True)''')
rg('''            v.text(bo[2] + 3, (bo[1] + bo[3]) / 2 - 34, "1 storey; X7 moved 30' E", 4.0)''',
   '''            v.text(bo[2] + 3, (bo[1] + bo[3]) / 2 - 34, "1 storey; 42' S of EXIT (E)" if REV == "F" else "1 storey; X7 moved 30' E", 4.0)''')
rg('''        items = [(C["bldg"], "Building, P2-A-101 Rev I (210' + NE tower + annex + bump-out)" if REV in ("E", "F") else''',
   '''        items = [(C["bldg"], f"Building, P2-A-101 Rev {'J' if REV == 'F' else 'I'} (210' + NE tower + annex + bump-out)" if REV in ("E", "F") else''')
rg('''    _, _, _, j = tf.summary_k()''', '''    _, _, _, j = tf.summary_kj() if REV == "F" else tf.summary_k()''')
rg('''    cols = [("", 0, "l"), ("DRAWN Rev I", 2.30, "r"), ("REV H drawn", 3.20, "r"),''',
   '''    cols = [("", 0, "l"), ("DRAWN Rev J" if REV == "F" else "DRAWN Rev I", 2.30, "r"), ("REV I drawn" if REV == "F" else "REV H drawn", 3.20, "r"),''')
rg('''bold=k == "G" or l_ in ("", "DRAWN Rev I"),''', '''bold=k == "G" or l_ in ("", "DRAWN Rev I", "DRAWN Rev J"),''')
rg('''    if abs((dr["L1"] - dd["L1"]) - bsf) > 0.5 or abs(dr["L2"] - dd["L2"]) > 0.5:
        raise SystemExit("C-101 Rev E: L1 change is not the bump-out area (or L2 changed)")''',
   '''    if REV == "F":
        if abs(dr["G"] - dd["G"]) > 0.5:
            raise SystemExit("C-101 Rev F: GSF changed vs Rev I (D-072 keeps it)")
    elif abs((dr["L1"] - dd["L1"]) - bsf) > 0.5 or abs(dr["L2"] - dd["L2"]) > 0.5:
        raise SystemExit("C-101 Rev E: L1 change is not the bump-out area (or L2 changed)")''')
rg('''    y = sh.para(x, y, width - 0.45, f"Drawn = P2-A-101 Rev I / A-102 Rev F (L2 unchanged).''',
   '''    y = sh.para(x, y, width - 0.45, "Drawn = P2-A-101 Rev J / A-102 Rev F. Program = P2-G-003 Rev K (unchanged). No change vs Rev I: the 30' x 56' bump-out "
                "(1,680 SF) slid 42' south and the public corridor came out of Mech (E) (D-072). Size is set by budget and parcel (D-012, D-006).", size=5.6) if REV == "F" else \\
        sh.para(x, y, width - 0.45, f"Drawn = P2-A-101 Rev I / A-102 Rev F (L2 unchanged).''')
rg('''        ("BUILDING (AS DRAWN ON P2-A-101 REV I)", None),''', '''        ("BUILDING (AS DRAWN ON P2-A-101 REV J)" if REV == "F" else "BUILDING (AS DRAWN ON P2-A-101 REV I)", None),''')
rg('''         "X7 moves 30' east to the bump-out's east face; its discharge path to a public way is TBD with the parcel (D-006).", "•"),''',
   '''         "X7 moves 30' east to the bump-out's east face; its discharge path to a public way is TBD with the parcel (D-006).", "•") if REV != "F" else
        (f"210' x 252' (unchanged) + NE stair tower + storage annex {an[2] - an[0]:g}' x {an[3] - an[1]:g}' (D-067) + restroom bump-out {bo[2] - bo[0]:g}' x {bo[3] - bo[1]:g}' "
         "on the east wall, now 42' further south and entirely south of EXIT (E) (D-072), one storey. X7 is back on the building wall; new exit X11 off the public "
         "corridor, just south of the bump-out. X7 / X11 discharge paths to a public way TBD with the parcel (D-006).", "•"),''')
_ne0 = g.index('def notes_e('); _ne1 = g.index('\ndef ', _ne0 + 5)
_ng = g[_ne0:_ne1]
_a = '''Exit discharge from X1-X10 to a public way (IBC 1028) TBD with the parcel.", "•"),'''
assert _ng.count(_a) == 1
_ng = _ng.replace(_a, 
   '''Exit discharge from X1-X10 to a public way (IBC 1028) TBD with the parcel.", "•") if REV != "F" else
        ("Fire apparatus access roads, hydrants and fire flow per IFC Appendices B, C, D (State Fire Marshal, 2021 IFC; D107 recommended) and the county's 2018 IFC. Exit discharge from X1-X11 to a public way (IBC 1028) TBD with the parcel.", "•"),''')
g = g[:_ne0] + _ng + g[_ne1:]
rg('''    y, mg = (notes_e if REV in ("E", "F") else''', '''    y, mg = (notes_e if REV in ("E", "F") else''')
open(p, "w", encoding="utf-8").write(g)
print("c101 patched")
