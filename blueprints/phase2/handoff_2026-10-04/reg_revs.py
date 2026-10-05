"""Register D-071 approvals and the D-072 revisions in params/phase2.yaml (text edits so comments survive)."""
import re
import yaml

P = "C:/Users/Hubby/AppData/Local/Temp/claude/C--Users-Hubby-Desktop-ARENA/202807a2-361c-4275-8ca9-11bac63af77d/scratchpad/repo/blueprints/params/phase2.yaml"
s = open(P, encoding="utf-8").read()
APPR = '"Shane 2026-10-04 evening (D-071: Set Rev B reviewed; APPROVED G-001 A, G-002 C, G-003 K, C-101 E, A-101 I, A-102 F, A-111 C, A-201 H, A-301 D, A-302 C, A-901 C)"'
approved = {"P2-G-002": "C", "P2-G-003": "K", "P2-C-101": "E", "P2-A-101": "I", "P2-A-102": "F", "P2-A-111": "C",
            "P2-A-201": "H", "P2-A-301": "D", "P2-A-302": "C", "P2-A-901": "C"}
SRC = "Shane 2026-10-04 evening (D-072 GO: core-2 bump-out 42 ft south, entirely south of EXIT (E); 8 ft public corridor from Concourse (E); restroom doors only onto it; EXIT (E) clear; X11; Mech (E) 675 SF accepted)"
new = {
    "P2-A-101": ("J", "params/phase2_plan_rev_j.yaml + params/phase2_program.yaml (rev_k)"),
    "P2-A-111": ("D", "params/phase2_life_safety_rev_d.yaml + params/phase2_plan_rev_j.yaml + params/phase2_code_rev_d.yaml"),
    "P2-A-401": ("D", "params/phase2_enlarged_rev_d.yaml + params/phase2_plan_rev_j.yaml"),
    "P2-A-103": ("D", "params/phase2_overlays_rev_d.yaml + params/phase2_plan_rev_j.yaml + params/phase2_code_rev_d.yaml"),
    "P2-C-101": ("F", "params/phase2_site.yaml rev_f + params/phase2_plan_rev_j.yaml"),
    "P2-A-201": ("I", "params/phase2_elev_rev_i.yaml + params/phase2_plan_rev_j.yaml"),
    "P2-A-901": ("D", "params/phase2_massing_rev_d.yaml + params/phase2_plan_rev_j.yaml"),
    "P2-G-002": ("D", "params/phase2_code_rev_d.yaml + params/phase2_plan_rev_j.yaml"),
}


def block(sheet):
    i = s.index(f"\n  {sheet}:\n") + 1
    m = re.search(r"\n  \S", s[i + 3:])
    j = i + 3 + m.start() + 1 if m else len(s)
    return i, j


for sh, rv in approved.items():
    i, j = block(sh)
    b = s[i:j]
    k = b.index(f"\n      {rv}:\n")
    fk = b.index("        frozen:", k)
    fe = b.index("\n", fk)
    b = b[:fk] + f"        frozen: true\n        approved: {APPR}" + b[fe:]
    s = s[:i] + b + s[j:]

for sh, (rv, inputs) in new.items():
    i, j = block(sh)
    b = s[i:j]
    assert f"\n      {rv}:\n" not in b, (sh, rv)
    k = b.rindex("\n    source:")
    file_ = f"{sh}_Rev{rv}"
    b = b[:k] + f"\n      {rv}:\n        file: {file_}\n        frozen: false\n        inputs: \"{inputs}\"\n        source: \"{SRC}\"" + b[k:]
    s = s[:i] + b + s[j:]

open(P, "w", encoding="utf-8").write(s)
d = yaml.safe_load(open(P, encoding="utf-8"))
for sh in sorted(set(approved) | set(new)):
    r = d["sheets"][sh]["revisions"]
    print(sh, {k: ("A" if v.get("approved") else "") + ("F" if v.get("frozen") else "") for k, v in r.items()})
