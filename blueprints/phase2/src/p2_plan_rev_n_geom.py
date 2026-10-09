"""Rev N geometry (D-086): the old NE stair strip on Level 1 becomes MECH (remote). Everything else = p2_plan_rev_m_geom.py.

Read-only on top of Rev M; asserts that GSF does not change. Used by p2_a_101_rev_n.py and p2_g_003_rev_n.py.
"""
import os
import sys

import yaml
from shapely.geometry import box

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import p2_plan_rev_m_geom as gm  # noqa: E402

N = yaml.safe_load(open(os.path.join(gm.PAR, "phase2_plan_rev_n.yaml")))
SR = N["level_1_add"][0]
STRIP = box(*SR["rect"]).intersection(gm.ring).difference(gm.drum)
assert abs(STRIP.area - gm.old_st2_left) < 1e-6
assert STRIP.intersection(gm.stairs_m).area < 1e-9
for r in gm.L1_ROOMS:                                           # no overlap with any Level 1 room
    assert gm.l1_geo(r).intersection(STRIP).area < 1e-6, r["id"]
STRIP_SF = STRIP.area

# GSF: the strip is inside the envelope, so L1 / L2 / total do not change
L1_N, L2_N, TOT_N = gm.L1_M, gm.L2_M, gm.TOT_M
BM, BD = N["baseline"]["rev_mi"], N["baseline"]["set_rev_d"]
assert (L1_N, L2_N, TOT_N) == (BM["l1_footprint_sf"], BM["l2_area_sf"], BM["total_gsf"])
assert gm.env.contains(STRIP.buffer(-1e-6))

l1_sched = sorted(list(gm.l1_sched) + [(SR["tag"], SR["name"], STRIP_SF)], key=lambda t: t[0])

# connection to the mechanical bay (D-086 rule) and shared edges with the other mech rooms
BAY_TAG = N["mech_target"]["bay_tag"]
GAP_TO_BAY = STRIP.distance(gm.BAY)
TOUCHES_BAY = GAP_TO_BAY < 1e-6
ROOMS_BY_TAG = {int(r["tag"]): r for r in gm.L1_ROOMS}
shared = {}
for r in gm.L1_ROOMS:
    e = gm.l1_geo(r).intersection(STRIP)
    if not e.is_empty and e.length > 0.01:
        shared[int(r["tag"])] = (r["name"], e.length)

# mechanical %
MECH_NAMES = [n for t, n, a in gm.l1_sched if "MECH" in n]
MECH_M = sum(a for t, n, a in gm.l1_sched if "MECH" in n)
MECH_N = MECH_M + STRIP_SF
TARGET = N["mech_target"]["pct_of_gsf"]
PCT_M = 100.0 * MECH_M / gm.TOT_M
PCT_N = 100.0 * MECH_N / TOT_N
PCT_D = 100.0 * BD["mech_sf"] / BD["total_gsf"]
SHORT_N = TARGET / 100.0 * TOT_N - MECH_N
mech_rows = [(t, n, a) for t, n, a in l1_sched if "MECH" in n]
