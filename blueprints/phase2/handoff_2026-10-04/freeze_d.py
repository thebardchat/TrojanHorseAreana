"""D-073: freeze the approved Set Rev D revisions in params/phase2.yaml; register P2-G-001 (A, B, C)."""
import re
import yaml

P = "C:/Users/Hubby/AppData/Local/Temp/claude/C--Users-Hubby-Desktop-ARENA/202807a2-361c-4275-8ca9-11bac63af77d/scratchpad/repo/blueprints/params/phase2.yaml"
s = open(P, encoding="utf-8").read()
APPR = '"Shane 2026-10-04 evening (D-073: Set Rev D reviewed; APPROVED + FROZEN G-001 C, G-002 D, A-101 J, A-103 D, A-111 D, A-201 I, A-401 D, A-901 D, C-101 F; G-003 K, A-102 F, A-301 D, A-302 C unchanged)"'
newly = {"P2-G-002": "D", "P2-A-101": "J", "P2-A-103": "D", "P2-A-111": "D", "P2-A-201": "I", "P2-A-401": "D", "P2-A-901": "D", "P2-C-101": "F"}


def block(sheet):
    i = s.index(f"\n  {sheet}:\n") + 1
    m = re.search(r"\n  \S", s[i + 3:])
    return i, i + 3 + m.start() + 1 if m else len(s)


for sh, rv in newly.items():
    i, j = block(sh)
    b = s[i:j]
    k = b.index(f"\n      {rv}:\n")
    fk = b.index("        frozen:", k)
    fe = b.index("\n", fk)
    b = b[:fk] + f"        frozen: true\n        approved: {APPR}" + b[fe:]
    s = s[:i] + b + s[j:]

# P2-G-001 registration (cover): A and B exist as files; C = Set Rev D cover
g001 = '''  P2-G-001:
    title: COVER SHEET — SHEET INDEX + DECISIONS
    size: "17 x 11 in (tabloid), landscape"
    inputs: "params/phase2_cover*.yaml + params/phase2.yaml (approval status) + phase2_plan_rev_d/h/i.yaml (size table)"
    revisions:
      A:
        file: P2-G-001_RevA
        frozen: true
        approved: "Shane 2026-10-04 evening (D-071: Set Rev B reviewed; APPROVED G-001 A)"
        inputs: "params/phase2_cover.yaml"
        source: "Shane 2026-10-04 5:03 PM CT (go: cover sheet, ARENA CLAUDE.md step 3)"
      B:
        file: P2-G-001_RevB
        frozen: false
        inputs: "params/phase2_cover_rev_b.yaml"
        source: "Shane 2026-10-04 (A-103 Rev C + Set Rev C); index for Set Rev C; superseded by Rev C"
      C:
        file: P2-G-001_RevC
        frozen: true
        approved: ''' + APPR + '''
        inputs: "params/phase2_cover_rev_c.yaml"
        source: "Shane 2026-10-04 evening (D-072 GO: new cover for Set Rev D)"
    source: "Shane 2026-10-04 5:03 PM CT; ARENA CLAUDE.md step 3"
'''
if "\n  P2-G-001:\n" not in s:
    i = s.index("\n  P2-G-002:\n") + 1
    s = s[:i] + g001 + s[i:]
open(P, "w", encoding="utf-8").write(s)
d = yaml.safe_load(open(P, encoding="utf-8"))
for sh in sorted(set(newly) | {"P2-G-001"}):
    r = d["sheets"][sh]["revisions"]
    print(sh, {k: ("A" if v.get("approved") else "") + ("F" if v.get("frozen") else "") for k, v in r.items()})
