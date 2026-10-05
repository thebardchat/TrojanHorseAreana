import re
import yaml

P = "C:/Users/Hubby/AppData/Local/Temp/claude/C--Users-Hubby-Desktop-ARENA/202807a2-361c-4275-8ca9-11bac63af77d/scratchpad/repo/blueprints/params/"
s = open(P + "phase2_plan_rev_i.yaml", encoding="utf-8").read()
hdr = """# phase2_plan_rev_j.yaml: P2-T-004 SCHEMATIC BLOCK PLAN geometry, REV J (Phase 2). Read by p2_a_plan.py --rev J (P2-A-101 Rev J, Level 1
# only), p2_a_111.py --rev D, p2_a_401.py --rev D, p2_a_103.py --rev D, p2_c_101.py --rev F, p2_a_201.py --rev I, p2_a_901.py --rev D,
# p2_g_002.py --rev D. Rev I geometry stays in phase2_plan_rev_i.yaml (P2-A-101 Rev I APPROVED, D-071).
# Rev J = Shane 2026-10-04 evening, D-072 (Claude Code session): public access to core 2 without crossing the floor or using EXIT (E).
# The 30 x 56 ft bump-out slides 42 ft south to y 119.09-175.09 (entirely south of EXIT (E); same 1,680 SF, east wall, D-070 kept);
# EXIT (E) + X7 back on the building wall (as Rev H); 8 ft PUBLIC CORRIDOR (E) x 202-210 from Concourse (E) north to core 2, behind
# the tier line; restroom doors open only onto it; men's room (2) + DF / janitor in the old Mech (E) strip, women's room (2) in the
# bump-out (door through the east wall at y 121-129); Mech (E) 1,720 -> 674.5 SF + MECH (E2) 660 SF in the bump-out; new exterior
# exit X11 off the corridor (common path, IBC 1006.2.1). GSF unchanged. Level 2 identical to Rev F-I.
# Rev I header (kept for history):
"""


def rep(a, b):
    global s
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)


rep("  revision: I\n  sheets: [P2-A-101, P2-A-111, P2-A-401, P2-G-003, P2-C-101, P2-A-901, P2-A-201]",
    "  revision: J\n  sheets: [P2-A-101, P2-A-111, P2-A-401, P2-A-103, P2-C-101, P2-A-201, P2-A-901, P2-G-002]")
rep('+ 3:31 PM CT (Rev I: D-069 Option 2, east restroom bump-out); KEYSTONE layout"',
    '+ 3:31 PM CT (Rev I: D-069 Option 2, east restroom bump-out) + evening (Rev J: D-072 public corridor to core 2, bump-out 42 ft south); KEYSTONE / Claude layout"')
rep('  bumpout: {id: restroom_core_2, rect: [210, 161.09, 240, 217.09], storeys: 1, height_ft: 16, note: "Rev I: one-storey restroom bump-out (core 2), 30 x 56 ft = 1,680 SF, on the east wall centred on V2 / EXIT (E) (y 179.09); the 8 ft EXIT (E) passage continues 30 ft east through it as the core corridor; X7 on its east face. Height 16 ft ASSUMED (as the annex, below the L2 line)"',
    '  bumpout: {id: restroom_core_2, rect: [210, 119.09, 240, 175.09], storeys: 1, height_ft: 16, note: "Rev J (D-072): the 30 x 56 ft = 1,680 SF one-storey bump-out slid 42 ft south so it lies entirely south of EXIT (E) (its north face = the EXIT (E) south edge, y 175.09); holds WOMEN (2) + MECH (E2); entered from the public corridor through the east wall. Height 16 ft ASSUMED"')
rep('    - {tag: "16", id: mech_e, name: MECH (E), rect: [188, 56, 210, 134.18], prog: mechanical, share: auto,',
    '    - {tag: "16", id: mech_e, name: MECH (E), rect: [188, 56, 202, 104.18], prog: mechanical, share: auto, note: "Rev J (D-072): 22 x 78.18 = 1,720 -> 14 x 48.18 = 674.5 SF (corridor + men\'s room + DF take the rest); MECH (E2) 660 SF in the bump-out; total mech about 4.1 % vs 5 % planning (MEP OPEN)",')
rep('id: rr_mb, name: "MEN (2)", rect: [210, 161.09, 236, 175.09]', 'id: rr_mb, name: "MEN (2)", rect: [188, 108.18, 202, 134.18]')
rep('id: rr_wb, name: "WOMEN (2)", rect: [210, 183.09, 240, 217.09]', 'id: rr_wb, name: "WOMEN (2)", rect: [210, 119.09, 240, 153.09]')
rep('id: df_jan, name: "DF / JAN.", rect: [236, 161.09, 240, 175.09]', 'id: df_jan, name: "DF / JAN.", rect: [188, 104.18, 202, 108.18]')
rep('note: "Rev I core 2: 5 WC (1 accessible, 1 ambulatory) + 7 urinals (1 accessible) = 12 WC-equivalents, 5 lav; entry from the corridor (north side); test-fit P2-A-401 Rev C"',
    'note: "Rev J core 2 (D-072): in the old Mech (E) strip, 14 x 26 ft; 5 WC (1 accessible, 1 ambulatory) + 7 urinals (1 accessible), 5 lav; door east onto the PUBLIC CORRIDOR (E); test-fit P2-A-401 Rev D"')
rep('note: "Rev I core 2: 24 WC (1 accessible, 1 ambulatory), 7 lav; entry from the corridor (south side); test-fit P2-A-401 Rev C"',
    'note: "Rev J core 2 (D-072): in the bump-out, 30 x 34 ft; 24 WC (1 accessible, 1 ambulatory), 7 lav; door through the east wall (y 121-129) from the PUBLIC CORRIDOR (E); test-fit P2-A-401 Rev D"')
rep('note: "Rev I core 2: hi-lo drinking fountain pair in an alcove off the corridor + janitor / service sink"',
    'note: "Rev J core 2 (D-072): hi-lo drinking fountain pair in an alcove off the PUBLIC CORRIDOR (E) + janitor / service sink"')

i = s.index('    - {tag: "27", id: df_jan')
j = s.index("\n", i) + 1
s = s[:j] + ('    - {tag: "28", id: mech_e2, name: "MECH (E2)", rect: [210, 153.09, 240, 175.09], prog: mechanical, share: auto, '
             'note: "Rev J (D-072): 30 x 22 = 660 SF in the north part of the bump-out, next to the restroom wet walls; exterior service door on the bump-out east face (ASSUMED)", '
             'source: "Shane 2026-10-04 evening (D-072: Mech (E) to 675 SF accepted at schematic; MEP OPEN)"}\n') + s[j:]

a = '    - {id: exit_e, name: "EXIT (E) + CORRIDOR", rect: [188, 175.09, 240, 183.09],'
i = s.index(a)
j = s.index("\n", i) + 1
s = s[:i] + ('    - {id: exit_e, name: "EXIT (E)", rect: [188, 175.09, 210, 183.09], note: "Rev J (D-072): back to the Rev H passage, V2 -> X7 on the building wall; no restroom doors or queues open onto it (IBC 1003.6)", '
             'source: "KEYSTONE layout (exit passage from V2 to the east wall; IBC 1006.3.3, 1030.3); 8 ft ASSUMED = vomitory width; Shane evening (D-072: keep EXIT (E) clear)"}\n'
             '    - {id: pc_e, name: "PUBLIC CORRIDOR (E)", vertical: true, rect: [202, 56, 210, 134.18], note: "Rev J (D-072): 8 ft (96 in) public corridor from CONCOURSE (E) north to core 2, behind the tier line; MEN (2), DF / JAN. and WOMEN (2) doors open only onto it; X11 exterior exit off it", '
             'source: "Shane 2026-10-04 evening (D-072); IBC 2021 T1020.3 (44 in min), 1006.2.1 (common path), 1020.5 (dead end)"}\n') + s[j:]

a = "      - {id: X7, kind: exit, wall: E, at: 179.09, x: 240,"
i = s.index(a)
j = s.index("\n", i) + 1
s = s[:i] + ('      - {id: X7, kind: exit, wall: E, at: 179.09, serves: "EXIT (E) passage: east tier via V2, event lockers 3-4", note: "Rev J (D-072): back on the building wall (x 210), just north of the bump-out", source: "KEYSTONE layout; IBC 1006.3.3, 1030.3; Shane evening (D-072)"}\n'
             '      - {id: X11, kind: exit, wall: E, at: 112, serves: "PUBLIC CORRIDOR (E): restroom core 2, Mech (E)", note: "Rev J (D-072): new exterior exit (pair, 64 in ASSUMED) off the public corridor, south of the bump-out; gives core 2 a second way out so the common path stays <= 75 ft (IBC 1006.2.1); discharge to a public way TBD (1028, D-006)", source: "Shane 2026-10-04 evening (D-072: add X11)"}\n') + s[j:]

open(P + "phase2_plan_rev_j.yaml", "w", encoding="utf-8").write(hdr + s)

p = yaml.safe_load(open(P + "phase2_plan_rev_j.yaml", encoding="utf-8"))


def ov(a, b):
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    return w * h if w > 0 and h > 0 else 0


def ar(r):
    return (r[2] - r[0]) * (r[3] - r[1])


R, Z = p["level_1"]["rooms"], p["level_1"]["zones"]
for i in range(len(R)):
    for j in range(i + 1, len(R)):
        if ov(R[i]["rect"], R[j]["rect"]) > 0.01:
            print("ROOM OVERLAP", R[i]["id"], R[j]["id"])
for z in Z:
    for r in R:
        if ov(z["rect"], r["rect"]) > 0.01:
            print("zone/room overlap", z["id"], r["id"])
for r in R:
    if r["id"] in ("mech_e", "mech_e2", "rr_mb", "rr_wb", "df_jan", "evl_4"):
        print(r["id"], r["rect"], round(ar(r["rect"]), 1))
for z in Z:
    if z["id"] in ("pc_e", "exit_e"):
        print(z["id"], z["rect"], round(ar(z["rect"]), 1))
print([(d["id"], d["at"], d.get("x")) for d in p["level_1"]["doors"]["items"] if d["wall"] == "E"])
print("mech total", round(sum(ar(r["rect"]) for r in R if r["prog"] == "mechanical"), 1))
