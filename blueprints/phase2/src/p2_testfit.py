"""P2-T-003b program test-fit arithmetic (Phase 2). Pure functions; all inputs from params.

compute(p2, prog, scenario, arena_sf=None, seats=None) -> dict
  scenario "base": seating SF/seat + gross-up from factors.*.base
  scenario "lean": telescopic geometry seating + gross-up factors.gross_up.lean
Gross = g * (N + M), M = mech_share * Gross  =>  Gross = g * N / (1 - g * mech_share)
N = every programmed net room except mechanical. TBD rooms are left out (total is a lower bound).
Run directly to print the numbers:  python blueprints/phase2/src/p2_testfit.py
"""
from __future__ import annotations

import math
from pathlib import Path

import yaml

BP = Path(__file__).resolve().parents[2]
# Frozen Revs A-C read the original 22,000 SF arena tag, kept in phase2.yaml as history after D-030 (11:39 PM CT).
ARENA_TAG = "spaces.arena.sf_tagged_superseded"


def load():
    p2 = yaml.safe_load((BP / "params" / "phase2.yaml").read_text(encoding="utf-8"))
    prog = yaml.safe_load((BP / "params" / "phase2_program.yaml").read_text(encoding="utf-8"))
    return p2, prog


def dig(d, path):
    for k in path.split("."):
        d = d[k]
    return d


def fixtures(total_load: int) -> dict:
    """IBC 2021 Table 2902.1, assembly: coliseums/arenas for indoor sporting events. 50/50 split (2902.1.1)."""
    per = total_load / 2
    wc_m = math.ceil(min(per, 1500) / 75 + max(per - 1500, 0) / 120)
    wc_f = math.ceil(min(per, 1520) / 40 + max(per - 1520, 0) / 60)
    lav_m = math.ceil(per / 200)
    lav_f = math.ceil(per / 150)
    df = math.ceil(total_load / 1000)
    return dict(load=total_load, per_sex=per, wc_m=wc_m, wc_f=wc_f, lav_m=lav_m, lav_f=lav_f,
                df=df, service_sink=1, urinals_max=math.floor(0.67 * wc_m),
                in_rooms=wc_m + wc_f + lav_m + lav_f)


def seat_sf(prog, scenario):
    s = prog["factors"]["seating"]
    if scenario == "base":
        return float(s["base_sf_per_seat"])
    n, w, d, a = s["lean_seats_between_aisles"], s["lean_seat_width_in"], s["lean_row_depth_in"], s["lean_aisle_in"]
    return (w * d / 144.0) * (n * w + a) / (n * w)


def compute(p2, prog, scenario="base", arena_sf=None, seats=None):
    f = prog["factors"]
    g = f["gross_up"][scenario]
    mech = f["mechanical"]["share_of_gross"]
    seats = p2["spaces"]["seating"]["total"] if seats is None else seats
    arena = dig(p2, ARENA_TAG) if arena_sf is None else arena_sf
    occ_floor = math.ceil(arena / f["occupant_load"]["event_floor_sf_per_occupant"])
    fx = fixtures(seats + occ_floor)
    sps = seat_sf(prog, scenario)
    rows = []
    for r in prog["rooms"]:
        m = r["method"]
        if m == "tag":
            sf = arena if r["id"] == "arena" else dig(p2, r["tag_path"])
        elif m == "each":
            sf = r["count"] * r["sf_each"]
        elif m == "parts":
            sf = sum(r["parts_sf"])
        elif m == "seating":
            sf = round(seats * sps)
        elif m == "restrooms":
            sf = fx["in_rooms"] * f["restrooms"]["sf_per_fixture"]
        elif m == "concourse":
            sf = round(seats * r["peak_share"] * r["sf_per_person"])
        elif m == "locker_load":
            sf = r["count"] * (r["team_wrestlers"] + r["team_staff"]) * r["sf_per_occupant"]
        elif m in ("tbd", "mechanical"):
            sf = None
        else:
            raise ValueError(m)
        rows.append(dict(r, sf=sf))
    net = sum(x["sf"] for x in rows if x["sf"] is not None)
    gross = g * net / (1 - g * mech)
    mech_sf = mech * gross
    for x in rows:
        if x["method"] == "mechanical":
            x["sf"] = round(mech_sf)
    return dict(scenario=scenario, g=g, mech=mech, seats=seats, arena=arena, occ_floor=occ_floor,
                fx=fx, seat_sf=sps, rows=rows, net=net, net_with_mech=net + mech_sf,
                gross=gross, cap=p2["building"]["total_sf"], over=gross - p2["building"]["total_sf"])


def option_b_floor(prog):
    o = prog["option_b"]
    ew = 2 * o["mat_ft"] + 2 * o["clear_around_ft"] + o["clear_between_ft"]
    ns = ew + 2 * o["table_zone_ft"]
    court = (o["court_length_ft"] + 2 * o["court_runout_preferred_ft"], o["court_width_ft"] + 2 * o["court_runout_preferred_ft"])
    fits = (court[0] <= max(ew, ns) and court[1] <= min(ew, ns))
    return dict(ew=ew, ns=ns, sf=ew * ns, court=court, court_fits=fits)


def max_seats(p2, prog, scenario, arena_sf=None):
    """Largest seat count (step 10) with gross <= cap; None if even 0 seats is over."""
    cap = p2["building"]["total_sf"]
    if compute(p2, prog, scenario, arena_sf, seats=0)["gross"] > cap:
        return None
    lo = 0
    for s in range(0, p2["spaces"]["seating"]["total"] + 1, 10):
        if compute(p2, prog, scenario, arena_sf, seats=s)["gross"] <= cap:
            lo = s
    return lo


def summary():
    p2, prog = load()
    ob = option_b_floor(prog)
    out = {}
    for sc in ("base", "lean"):
        a = compute(p2, prog, sc)
        b = compute(p2, prog, sc, arena_sf=ob["sf"])
        out[sc] = dict(A=a, B=b, C=max_seats(p2, prog, sc), BC=max_seats(p2, prog, sc, arena_sf=ob["sf"]),
                       C0=compute(p2, prog, sc, seats=0))
    return p2, prog, ob, out



# ============================ REV B: TWO LEVELS (D-031) ============================
# Footprint F = max(L1, AV + L2). AV = arena volume (event floor + lower seats), double height, nothing above it.
# L1 = g * (N1 + M), L2 = g * N2, M = mech * (L1 + L2)  =>  G = g * (N1 + N2) / (1 - g * mech).

def exits_required(load: int) -> int:
    """IBC 2021 Table 1006.3.3 (per story)."""
    return 2 if load <= 500 else 3 if load <= 1000 else 4


def stair_sf(vc, width_in: float) -> dict:
    """Plan SF of one switch-back stair on one level (IBC 1011.5.2 risers/treads, 1011.6 landings, 1011.8 flight rise)."""
    risers = math.ceil(vc["floor_to_floor_in"] / vc["riser_max_in"])
    flights = max(2, math.ceil(vc["floor_to_floor_in"] / vc["flight_rise_max_in"]))
    flights += flights % 2                      # switch-back returns to the same side
    per_flight = math.ceil(risers / flights)
    run = (per_flight - 1) * vc["tread_min_in"]
    landing = min(width_in, 48)
    if vc.get("intermediate_landing_equals_width"):  # Rev G (D-051): intermediate landing = stair width
        sf = 2 * width_in * (run + landing + width_in) / 144.0 * (flights // 2)
    else:
        sf = 2 * width_in * (run + 2 * landing) / 144.0 * (flights // 2)
    return dict(risers=risers, flights=flights, per_flight=per_flight, riser_in=vc["floor_to_floor_in"] / risers,
                run_in=run, landing_in=landing, width_in=width_in, sf=sf)


def compute_two_level(p2, prog, scenario="base", arena_sf=None, seats=None, upper_share=None):
    f, vc = prog["factors"], prog["vertical_circulation"]
    g, mech = f["gross_up"][scenario], f["mechanical"]["share_of_gross"]
    seats = p2["spaces"]["seating"]["total"] if seats is None else seats
    arena = dig(p2, ARENA_TAG) if arena_sf is None else arena_sf
    up = prog["seat_split"]["upper_share_assumed"] if upper_share is None else upper_share
    su = int(round(seats * up))
    sl = seats - su
    sps = seat_sf(prog, scenario)
    occ_floor = math.ceil(arena / f["occupant_load"]["event_floor_sf_per_occupant"])
    fx1 = fixtures(sl + occ_floor)
    fx2 = fixtures(su) if su else None
    sfpf = f["restrooms"]["sf_per_fixture"]
    conc = {r["id"]: r for r in prog["rooms"]}["concourse"]
    room = {r["id"]: r for r in compute(p2, prog, scenario, arena_sf=arena, seats=seats)["rows"]}
    # L2 occupant load -> exits, stair width
    other = 0
    for o in vc["l2_other_occupants"]:
        other += math.ceil(room[o["id"]]["sf"] / o["sf_per_occupant"])
    l2_load = su + other
    nex = exits_required(l2_load)
    width = max(vc["stair_min_width_in"], l2_load * vc["stair_capacity_in_per_occupant"] / nex)
    st = stair_sf(vc, width)
    elev = vc["elevator_count"] * vc["elevator_hoistway_sf_per_level"]
    vc_sf = nex * st["sf"] + elev
    sf = {
        "arena": arena, "seating_lower": sl * sps, "seating_upper": su * sps,
        "concourse_lower": sl * conc["peak_share"] * conc["sf_per_person"],
        "concourse_upper": su * conc["peak_share"] * conc["sf_per_person"],
        "public_restroom_lower": fx1["in_rooms"] * sfpf,
        "public_restroom_upper": (fx2["in_rooms"] * sfpf) if fx2 else 0,
        "vertical_circulation": vc_sf,
    }
    for rid, r in room.items():
        if rid not in sf and r["method"] not in ("seating", "concourse", "restrooms", "tbd", "mechanical"):
            sf[rid] = r["sf"]
    l1_ids = [r["id"] for r in prog["stacking"]["level_1"] if r["id"] != "mechanical"]
    l2_ids = [r["id"] for r in prog["stacking"]["level_2"]]
    N1 = sum(sf[i] for i in l1_ids)
    N2 = sum(sf[i] for i in l2_ids)
    G = g * (N1 + N2) / (1 - g * mech)
    M = mech * G
    L1, L2 = g * (N1 + M), g * N2
    AV = g * sum(sf[i] for i in prog["stacking"]["arena_volume"])
    F = max(L1, AV + L2)
    cap = p2["building"]["footprint_cap_sf"]
    return dict(scenario=scenario, g=g, mech=mech, seats=seats, arena=arena, up=up, su=su, sl=sl, seat_sf=sps,
                occ_floor=occ_floor, fx1=fx1, fx2=fx2, l2_load=l2_load, l2_other=other, exits=nex, stair=st,
                elev_sf=elev, vc_sf=vc_sf, sf=sf, l1_ids=l1_ids, l2_ids=l2_ids, N1=N1, N2=N2, M=M,
                L1=L1, L2=L2, AV=AV, ring=L1 - AV, F=F, G=G, cap=cap, over=F - cap, fits=F <= cap,
                l2_fits_over_ring=L2 <= L1 - AV)


def split_range(prog):
    s = prog["seat_split"]
    k0, k1, st = round(s["upper_share_min"] * 100), round(s["upper_share_max"] * 100), round(s["step"] * 100)
    return [k / 100.0 for k in range(k0, k1 + 1, st)]


def best_split(p2, prog, scenario, arena_sf=None, seats=None):
    return min((compute_two_level(p2, prog, scenario, arena_sf, seats, u) for u in split_range(prog)), key=lambda d: (round(d["F"]), d["up"]))


def max_seats_two_level(p2, prog, scenario, arena_sf=None, step=10):
    best = None
    for s_ in range(0, p2["spaces"]["seating"]["total"] + 1, step):
        if best_split(p2, prog, scenario, arena_sf, s_)["fits"]:
            best = s_
    return best


def max_floor_two_level(p2, prog, scenario, step=100):
    """Largest event floor (SF, step 100) that fits the footprint cap with all seats (best split)."""
    best = None
    for a in range(0, dig(p2, ARENA_TAG) + 1, step):
        if best_split(p2, prog, scenario, arena_sf=a)["fits"]:
            best = a
    return best


def summary_b():
    p2, prog = load()
    ob = option_b_floor(prog)
    out = {}
    for sc in ("base", "lean"):
        out[sc] = dict(A50=compute_two_level(p2, prog, sc), Abest=best_split(p2, prog, sc),
                       B50=compute_two_level(p2, prog, sc, arena_sf=ob["sf"]), Bbest=best_split(p2, prog, sc, arena_sf=ob["sf"]),
                       seats_max=max_seats_two_level(p2, prog, sc), floor_max=max_floor_two_level(p2, prog, sc),
                       seats_max_B=max_seats_two_level(p2, prog, sc, arena_sf=ob["sf"]))
    return p2, prog, ob, out



# ============================ REV C: SUITES (Shane 11:26 PM CT) ============================
# Separate from compute_two_level (Rev B, frozen). Footprint F = max(L1, AV + L2, AV + L3).

def suite_module(prog, guests, scenario):
    su = prog["suites"]
    sps = seat_sf(prog, scenario)
    sf = guests * su["sf_per_guest"]
    lounge = max(sf - guests * sps, 0.0)
    code_load = guests + math.ceil(lounge / 15.0)          # IBC 1004.6 + T1004.5 unconcentrated 15 net
    width_ft = math.ceil(guests / 2) * 1.5 + 2.0            # ASSUMED frontage rule (suites.frontage_rule)
    corridor = width_ft * su["corridor_width_in"] / 12.0
    return dict(guests=guests, sf=sf, lounge=lounge, code_load=code_load, width_ft=width_ft, corridor_sf=corridor)


def compute_suites(p2, prog, scenario="base", arena_sf=None, bowl=None, guests=16, placement="L3_top", upper_share=None, n_suites=None):
    f, vc = prog["factors"], prog["vertical_circulation"]
    g, mech = f["gross_up"][scenario], f["mechanical"]["share_of_gross"]
    target = p2["spaces"]["seating"]["total"]
    bowl = target if bowl is None else bowl
    arena = dig(p2, ARENA_TAG) if arena_sf is None else arena_sf
    up = prog["seat_split"]["upper_share_assumed"] if upper_share is None else upper_share
    ns = max(0, math.ceil((target - bowl) / guests)) if n_suites is None else n_suites
    mod = suite_module(prog, guests, scenario)
    s_sf, s_corr, s_load = ns * mod["sf"], ns * mod["corridor_sf"], ns * mod["code_load"]
    su = int(round(bowl * up)); sl = bowl - su
    sps = seat_sf(prog, scenario)
    occ_floor = math.ceil(arena / f["occupant_load"]["event_floor_sf_per_occupant"])
    sfpf = f["restrooms"]["sf_per_fixture"]
    conc = {r["id"]: r for r in prog["rooms"]}["concourse"]
    room = {r["id"]: r for r in compute(p2, prog, scenario, arena_sf=arena, seats=target)["rows"]}
    other = sum(math.ceil(room[o["id"]]["sf"] / o["sf_per_occupant"]) for o in vc["l2_other_occupants"])
    three = placement == "L3_top" and ns > 0
    l2_load = su + other + (0 if three else s_load)
    l3_load = s_load if three else 0
    fx1 = fixtures(sl + occ_floor)
    fx2 = fixtures(su + (0 if three else s_load)) if (su + (0 if three else s_load)) else None
    fx3 = fixtures(l3_load) if three else None
    loads = [x for x in (l2_load, l3_load) if x]
    nex = max(exits_required(x) for x in loads)
    width = max([vc["stair_min_width_in"]] + [x * vc["stair_capacity_in_per_occupant"] / nex for x in loads])
    st = stair_sf(vc, width)
    elev = vc["elevator_count"] * vc["elevator_hoistway_sf_per_level"]
    vc_sf = nex * st["sf"] + elev
    sf = {
        "arena": arena, "seating_lower": sl * sps, "seating_upper": su * sps,
        "concourse_lower": sl * conc["peak_share"] * conc["sf_per_person"],
        "concourse_upper": su * conc["peak_share"] * conc["sf_per_person"],
        "public_restroom_lower": fx1["in_rooms"] * sfpf,
        "public_restroom_upper": (fx2["in_rooms"] * sfpf) if fx2 else 0,
        "vertical_circulation": vc_sf,
    }
    for rid, r in room.items():
        if rid not in sf and r["method"] not in ("seating", "concourse", "restrooms", "tbd", "mechanical"):
            sf[rid] = r["sf"]
    l1_ids = [r["id"] for r in prog["stacking"]["level_1"] if r["id"] != "mechanical"]
    l2_ids = [r["id"] for r in prog["stacking"]["level_2"]]
    N1 = sum(sf[i] for i in l1_ids)
    N2 = sum(sf[i] for i in l2_ids) + (0 if three else s_sf + s_corr)
    N3 = (s_sf + s_corr + fx3["in_rooms"] * sfpf + vc_sf) if three else 0
    G = g * (N1 + N2 + N3) / (1 - g * mech)
    M = mech * G
    L1, L2, L3 = g * (N1 + M), g * N2, g * N3
    AV = g * sum(sf[i] for i in prog["stacking"]["arena_volume"])
    F = max(L1, AV + L2, AV + L3)
    cap = p2["building"]["footprint_cap_sf"]
    # wheelchair spaces (IBC T1109.2.2.1 / ADA T221.2.1.1): bowl as one area + 1 per suite
    def ws(n_):
        if n_ < 4: return 0
        for hi, v in ((25, 1), (50, 2), (100, 4), (300, 5), (500, 6)):
            if n_ <= hi: return v
        if n_ <= 5000: return 6 + math.ceil((n_ - 500) / 150)
        return 36 + math.ceil((n_ - 5000) / 200)
    return dict(scenario=scenario, placement=placement, three=three, g=g, mech=mech, arena=arena, bowl=bowl, up=up, su=su, sl=sl,
                guests=guests, ns=ns, mod=mod, s_sf=s_sf, s_corr=s_corr, s_load=s_load, spectators=bowl + ns * guests,
                frontage_ft=ns * mod["width_ft"], fx1=fx1, fx2=fx2, fx3=fx3, l2_load=l2_load, l3_load=l3_load,
                exits=nex, stair=st, vc_sf=vc_sf, N1=N1, N2=N2, N3=N3, M=M, L1=L1, L2=L2, L3=L3, AV=AV, ring=L1 - AV,
                F=F, G=G, cap=cap, over=F - cap, fits=F <= cap, levels=3 if three else 2,
                ws_bowl=ws(bowl), ws_suites=ns, seat_sf=sps)


def best_suites(p2, prog, scenario, arena_sf, bowl, guests, placement):
    return min((compute_suites(p2, prog, scenario, arena_sf, bowl, guests, placement, u) for u in split_range(prog)),
               key=lambda d: (round(d["F"]), d["up"]))


def max_bowl_with_suites(p2, prog, scenario, arena_sf, guests, placement, step=10):
    """Largest bowl seat count (step 10) that fits the footprint cap once suites make up the rest of the target."""
    best = None
    for b in range(0, p2["spaces"]["seating"]["total"] + 1, step):
        d = best_suites(p2, prog, scenario, arena_sf, b, guests, placement)
        if d["fits"]:
            best = d
    return best


def max_spectators_with_suites(p2, prog, scenario, arena_sf, guests, placement, step=10):
    """Most spectators (bowl + suites, target not required) that fit the footprint cap. Binary search on suite count per bowl size."""
    best = None
    for b in range(0, p2["spaces"]["seating"]["total"] + 1, step):
        def fit(ns):
            return min((compute_suites(p2, prog, scenario, arena_sf, b, guests, placement, u, n_suites=ns) for u in split_range(prog)),
                       key=lambda d: (round(d["F"]), d["up"]))
        if not fit(0)["fits"]:
            break
        lo, hi = 0, 200
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if fit(mid)["fits"]:
                lo = mid
            else:
                hi = mid - 1
        d = fit(lo)
        if best is None or d["spectators"] > best["spectators"]:
            best = d
    return best


def largest_floor_with_suites(p2, prog, scenario, guests, placement, step=100):
    lo = prog["suites"]["floors_checked"][-1]
    best = None
    for a in range(lo, dig(p2, ARENA_TAG) + 1, step):
        if max_bowl_with_suites(p2, prog, scenario, a, guests, placement) is not None:
            best = a
    return best


def summary_c():
    p2, prog = load()
    su = prog["suites"]
    gl = [su["guests_per_suite"][k] for k in ("low", "mid", "high")]
    out = {}
    for sc in ("base", "lean"):
        for fl in su["floors_checked"]:
            for pl in ("L2_back", "L3_top"):
                for gu in gl:
                    out[(sc, fl, pl, gu)] = max_bowl_with_suites(p2, prog, sc, fl, gu, pl)
    full = dig(p2, ARENA_TAG)
    out["max22"] = {gu: max_spectators_with_suites(p2, prog, "base", full, gu, "L3_top") for gu in gl}
    out["maxfloor"] = {gu: largest_floor_with_suites(p2, prog, "base", gu, "L3_top") for gu in gl}
    out["guests"] = gl
    return p2, prog, out


# ============================ REV D: LOCKED PROGRAM (D-030, Shane 11:39 PM CT) ============================
# Event floor + bowl seats read from the locked phase2.yaml keys; no suites; Rev B two-level method.

LOCKED_FLOOR = "spaces.arena.event_floor_sf"
LOCKED_BOWL = "spaces.seating.bowl"


def wheelchair_spaces(n_: int) -> int:
    """IBC 2021 Table 1109.2.2.1 / ADA Table 221.2.1.1."""
    if n_ < 4:
        return 0
    for hi, v in ((25, 1), (50, 2), (100, 4), (300, 5), (500, 6)):
        if n_ <= hi:
            return v
    if n_ <= 5000:
        return 6 + math.ceil((n_ - 500) / 150)
    return 36 + math.ceil((n_ - 5000) / 200)


def compute_locked(p2, prog, seat_type="base", arena_sf=None):
    """seat_type: 'base' (FIXED, 6.0 SF/seat) or 'telescopic' (bleacher geometry). Same gross-up both."""
    import copy
    lp = prog["locked_program"]
    pr = copy.deepcopy(prog)
    pr["factors"]["gross_up"]["telescopic"] = lp["gross_up_telescopic"]
    arena = dig(p2, LOCKED_FLOOR) if arena_sf is None else arena_sf
    bowl = dig(p2, LOCKED_BOWL)
    d = compute_two_level(p2, pr, seat_type, arena_sf=arena, seats=bowl, upper_share=lp["upper_share"])
    d["ws"] = wheelchair_spaces(bowl)
    d["bowl"] = bowl
    d["seat_type"] = seat_type
    return d


def summary_d():
    p2, prog = load()
    ob = option_b_floor(prog)
    out = {c["id"]: compute_locked(p2, prog, c["id"]) for c in prog["locked_program"]["columns"]}
    return p2, prog, ob, out


# ============================ REV E: MIXED SEATING (D-009, Shane 2026-10-04 4:30 AM CT) ============================
# Telescopic lower tier (L1, inside the arena volume) + fixed upper tier (L2). Same method and gross-up as Rev D.

def compute_mix(p2, prog):
    fx = compute_locked(p2, prog, "base")
    tl = compute_locked(p2, prog, "telescopic")
    sf = dict(fx["sf"])
    sf["seating_lower"] = tl["sf"]["seating_lower"]
    g, mech = fx["g"], fx["mech"]
    N1 = sum(sf[i] for i in fx["l1_ids"])
    N2 = sum(sf[i] for i in fx["l2_ids"])
    G = g * (N1 + N2) / (1 - g * mech)
    M = mech * G
    L1, L2 = g * (N1 + M), g * N2
    AV = g * sum(sf[i] for i in prog["stacking"]["arena_volume"])
    F = max(L1, AV + L2)
    cap = p2["building"]["footprint_cap_sf"]
    d = dict(fx)
    d.update(scenario="mix", sf=sf, N1=N1, N2=N2, G=G, M=M, L1=L1, L2=L2, AV=AV, ring=L1 - AV, F=F, cap=cap,
             over=F - cap, fits=F <= cap, l2_fits_over_ring=L2 <= L1 - AV, seat_sf_lower=tl["seat_sf"],
             seat_sf_upper=fx["seat_sf"], margin=cap - F,
             governs="arena volume + L2" if AV + L2 >= L1 else "L1")
    return d


def largest_remainder(total, weights):
    s = sum(weights)
    raw = [total * w / s for w in weights]
    out = [int(math.floor(r)) for r in raw]
    for i in sorted(range(len(raw)), key=lambda i: -(raw[i] - out[i]))[: total - sum(out)]:
        out[i] += 1
    return out


def seats_by_side(plan, prog, d):
    """Seat counts per side and tier from block-plan bands (phase2_plan_rev_b.yaml). Each tier = d['sl'] / d['su']."""
    t = plan["tiers"]
    lo, up = t["lower"], t["upper"]
    spf = lo["row_depth_ft"] / d["seat_sf_lower"]                  # seats per foot of row
    rows = []
    for b in lo["bands"]:
        r = b["rect"]
        horiz = (r[2] - r[0]) >= (r[3] - r[1])
        length = (r[2] - r[0]) if horiz else (r[3] - r[1])
        cut = sum((o["rect"][2] - o["rect"][0]) if horiz else (o["rect"][3] - o["rect"][1]) for o in lo["openings"] if o["side"] == b["side"])
        rows.append(dict(side=b["side"], length=length, cut=cut, cap_lower=(length - cut) * lo["rows"] * spf))
    up_area = {b["side"]: (b["rect"][2] - b["rect"][0]) * (b["rect"][3] - b["rect"][1]) for b in up["bands"]}
    for r_ in rows:
        r_["area_upper"] = up_area[r_["side"]]
        r_["cap_upper"] = up_area[r_["side"]] / d["seat_sf_upper"]
    lw = largest_remainder(d["sl"], [r_["cap_lower"] for r_ in rows])
    uw = largest_remainder(d["su"], [r_["cap_upper"] for r_ in rows])
    for r_, a, b in zip(rows, lw, uw):
        r_["lower"], r_["upper"], r_["total"] = a, b, a + b
    tot = dict(side="TOTAL", lower=sum(lw), upper=sum(uw), total=sum(lw) + sum(uw),
               cap_lower=sum(r_["cap_lower"] for r_ in rows), cap_upper=sum(r_["cap_upper"] for r_ in rows))
    return rows, tot


def summary_e():
    p2, prog = load()
    ob = option_b_floor(prog)
    plan = yaml.safe_load((BP / "params" / "phase2_plan_rev_b.yaml").read_text(encoding="utf-8"))
    mix = compute_mix(p2, prog)
    rows, tot = seats_by_side(plan, prog, mix)
    out = dict(mix=mix, fixed=compute_locked(p2, prog, "base"), rows=rows, tot=tot, plan=plan)
    return p2, prog, ob, out


# ============================ REV F: LEVEL 2 RUNNING / TRAINING LOOP (D-035, Shane 2026-10-04 4:55 AM CT) ============================
# S&C and cross-training read their new locked SF (phase2.yaml spaces.*.sf; frozen revisions read sf_tagged_superseded).
# The loop replaces the upper concourse line (on event days the loop IS the upper concourse). The loop is circulation drawn
# at full size, so it is added to L2 gross WITHOUT the x 1.25 gross-up (ASSUMED; the gross-up allowance is for circulation
# and walls around net rooms). The fully grossed-up alternative is reported too.

LOOP_ROOMS = ("strength_conditioning", "cross_training")


def loop_geometry(plan):
    lp = plan["level_2"]["loop"]
    o, i = lp["outer"], lp["inner"]
    w = lp["width_ft"]
    area_ = (o[2] - o[0]) * (o[3] - o[1]) - (i[2] - i[0]) * (i[3] - i[1])
    cx = (o[2] - o[0]) - w
    cy = (o[3] - o[1]) - w
    cl = 2 * (cx + cy)
    legs = {"S": [o[0], o[1], o[2], i[1]], "N": [o[0], i[3], o[2], o[3]], "W": [o[0], i[1], i[0], i[3]], "E": [i[2], i[1], o[2], i[3]]}
    return dict(area=area_, centerline=cl, laps_per_mile=5280 / cl, legs=legs, width=w, cx=cx, cy=cy)


def compute_loop(p2, prog, loop_sf):
    import copy
    pr = copy.deepcopy(prog)
    for r in pr["rooms"]:
        if r["id"] in LOOP_ROOMS:
            r["tag_path"] = f"spaces.{r['id']}.sf"
    m = compute_mix(p2, pr)
    g, mech = m["g"], m["mech"]
    sf = dict(m["sf"])
    N1 = m["N1"]
    N2x = m["N2"] - sf["concourse_upper"]
    G = (g * (N1 + N2x) + loop_sf) / (1 - g * mech)
    M = mech * G
    L1, L2 = g * (N1 + M), g * N2x + loop_sf
    AV = m["AV"]
    F = max(L1, AV + L2)
    Galt = g * (N1 + N2x + loop_sf) / (1 - g * mech)
    L2alt = g * (N2x + loop_sf)
    Malt = mech * Galt
    Falt = max(g * (N1 + Malt), AV + L2alt)
    cap = p2["building"]["footprint_cap_sf"]
    d = dict(m)
    d.update(scenario="loop", sf=sf, loop=loop_sf, N2x=N2x, N2=N2x + loop_sf, G=G, M=M, L1=L1, L2=L2, ring=L1 - AV, F=F,
             over=F - cap, fits=F <= cap, l2_fits_over_ring=L2 <= L1 - AV, margin=cap - F,
             governs="arena volume + L2" if AV + L2 >= L1 else "L1", alt=dict(G=Galt, L2=L2alt, F=Falt, margin=cap - Falt, M=Malt))
    return d


def summary_f():
    p2, prog, ob, out = summary_e()
    plan = yaml.safe_load((BP / "params" / "phase2_plan_rev_d.yaml").read_text(encoding="utf-8"))
    lg = loop_geometry(plan)
    lp = compute_loop(p2, prog, lg["area"])
    rows, tot = seats_by_side(plan, prog, lp)
    out_f = dict(loop=lp, mix=out["mix"], geom=lg, rows=rows, tot=tot, plan=plan)
    return p2, prog, ob, out_f


# ============================ REV G (Shane 2026-10-04 9:10 AM CT): Plan Rev E set ============================
def compute_rev_g(p2, prog, loop_sf):
    """Rev F method + 76 in stairs with 76 in intermediate landings (D-052, D-051) + 6 ft east clear zone (D-053)."""
    import copy
    rg = prog["rev_g"]
    pr = copy.deepcopy(prog)
    pr["vertical_circulation"]["stair_min_width_in"] = rg["stair_width_in"]
    pr["vertical_circulation"]["intermediate_landing_equals_width"] = True
    d = compute_loop(p2, pr, loop_sf)
    g, mech = d["g"], d["mech"]
    ex = rg["east_clear_sf"]
    N1 = d["N1"] + ex
    AV = d["AV"] + g * ex
    N2x = d["N2x"]
    G = (g * (N1 + N2x) + loop_sf) / (1 - g * mech)
    M = mech * G
    L1, L2 = g * (N1 + M), g * N2x + loop_sf
    F = max(L1, AV + L2)
    sf = dict(d["sf"])
    sf["arena"] = sf["arena"] + ex
    d.update(scenario="rev_g", sf=sf, east_clear=ex, N1=N1, AV=AV, G=G, M=M, L1=L1, L2=L2, ring=L1 - AV, F=F,
             governs="arena volume + L2" if AV + L2 >= L1 else "L1", l2_fits_over_ring=L2 <= L1 - AV)
    for k_ in ("over", "fits", "margin", "alt", "cap"):
        d.pop(k_, None)
    return d


def drawn_size(plan):
    """D-057 size of a drawn block plan: L1 footprint (box + projection), L2 area (footprint minus open-to-below), TOTAL GSF."""
    def a_(r):
        return (r[2] - r[0]) * (r[3] - r[1])
    l1 = a_(plan["building"]["rect"]) + a_(plan["building"]["projection"]["rect"])
    l2 = l1 - sum(a_(o["rect"]) for o in plan["level_2"]["open_below"])
    return dict(L1=l1, L2=l2, G=l1 + l2)


def summary_g():
    p2, prog, ob, out_f = summary_f()
    plan = yaml.safe_load((BP / "params" / "phase2_plan_rev_e.yaml").read_text(encoding="utf-8"))
    lg = loop_geometry(plan)
    lp = compute_rev_g(p2, prog, lg["area"])
    rows, tot = seats_by_side(plan, prog, lp)
    out_g = dict(loop=lp, mix=out_f["mix"], geom=lg, rows=rows, tot=tot, plan=plan, rev_f=out_f,
                 drawn=drawn_size(plan), drawn_d=drawn_size(out_f["plan"]))
    return p2, prog, ob, out_g


if __name__ == "__main__":
    import sys as _s
    if "--rev-e" in _s.argv:
        p2, prog, ob, out = summary_e()
        x = out["mix"]
        print({k: (round(v) if isinstance(v, float) else v) for k, v in x.items() if k in ("N1", "N2", "M", "L1", "L2", "AV", "ring", "F", "G", "margin", "governs", "l2_fits_over_ring", "seat_sf_lower")})
        for r in out["rows"] + [out["tot"]]:
            print(r)
        b = out["plan"]["building"]["rect"]
        print("box", b[2] - b[0], b[3] - b[1], (b[2] - b[0]) * (b[3] - b[1]))
        raise SystemExit
    if "--rev-d" in _s.argv:
        p2, prog, ob, out = summary_d()
        print("option B floor", ob)
        for k, x in out.items():
            print(f"[{k}] seat_sf {x['seat_sf']:.3f} g {x['g']} ({x['sl']}/{x['su']}) N1 {x['N1']:,.0f} N2 {x['N2']:,.0f} M {x['M']:,.0f} "
                  f"L1 {x['L1']:,.0f} L2 {x['L2']:,.0f} AV {x['AV']:,.0f} ring {x['ring']:,.0f} F {x['F']:,.0f} G {x['G']:,.0f} "
                  f"fits {x['fits']} l2fits {x['l2_fits_over_ring']} exits {x['exits']} w {x['stair']['width_in']:.1f} st {x['stair']['sf']:.0f} "
                  f"vc {x['vc_sf']:.0f} l2load {x['l2_load']} fx1 {x['fx1']} fx2 {x['fx2']} ws {x['ws']}")
            print({k_: round(v) for k_, v in x['sf'].items()})
        x16 = compute_locked(p2, prog, "base", arena_sf=16416)
        print("drawn 16416 F", round(x16["F"]), "G", round(x16["G"]))
        raise SystemExit
    if "--rev-c" in _s.argv:
        p2, prog, out = summary_c()
        print("max spectators at full floor:", {k: (v["bowl"], v["ns"], v["spectators"], round(v["F"])) for k, v in out["max22"].items()})
        print("largest floor reaching target:", out["maxfloor"])
        for k, x in out.items():
            if not isinstance(k, tuple):
                continue
            if x is None:
                print(k, "NO FIT"); continue
            print(f"{k}: bowl {x['bowl']} ({x['sl']}/{x['su']}) suites {x['ns']}x{x['guests']} = {x['spectators']} | F {x['F']:,.0f} "
                  f"L1 {x['L1']:,.0f} L2 {x['L2']:,.0f} L3 {x['L3']:,.0f} AV {x['AV']:,.0f} G {x['G']:,.0f} lv {x['levels']} "
                  f"suiteSF {x['s_sf']:,.0f} corr {x['s_corr']:,.0f} front {x['frontage_ft']:.0f} load2 {x['l2_load']} load3 {x['l3_load']} "
                  f"ex {x['exits']} w {x['stair']['width_in']:.0f} fx {x['fx1']['in_rooms']}/{x['fx2']['in_rooms'] if x['fx2'] else 0}/{x['fx3']['in_rooms'] if x['fx3'] else 0}")
        raise SystemExit
    if "--rev-b" in _s.argv:
        p2, prog, ob, out = summary_b()
        for sc, d in out.items():
            for k in ("A50", "Abest", "B50", "Bbest"):
                x = d[k]
                print(f"[{sc} {k}] up {x['up']:.2f} ({x['sl']}/{x['su']}) L1 {x['L1']:,.0f} L2 {x['L2']:,.0f} AV {x['AV']:,.0f} "
                      f"ring {x['ring']:,.0f} F {x['F']:,.0f} G {x['G']:,.0f} over {x['over']:,.0f} exits {x['exits']} "
                      f"w {x['stair']['width_in']:.0f} stair {x['stair']['sf']:.0f} vc {x['vc_sf']:.0f} l2load {x['l2_load']} "
                      f"fx1 {x['fx1']['in_rooms']} fx2 {x['fx2']['in_rooms'] if x['fx2'] else 0}")
            print(f"   max seats (22k floor) {d['seats_max']}; max floor (all seats) {d['floor_max']}; max seats (B floor) {d['seats_max_B']}")
        raise SystemExit
    p2, prog, ob, out = summary()
    print("option B floor", ob)
    for sc, d in out.items():
        a = d["A"]
        print(f"\n[{sc}] g={a['g']} seat_sf={a['seat_sf']:.3f} occ_floor={a['occ_floor']} fixtures={a['fx']}")
        for r in a["rows"]:
            print(f"   {r['name'][:55]:55s} {r['sf']}")
        print(f"   NET {a['net']:,}  mech {a['net_with_mech']-a['net']:,.0f}  GROSS {a['gross']:,.0f}  over {a['over']:,.0f}")
        b = d["B"]
        print(f"   B: arena {b['arena']:,} net {b['net']:,} gross {b['gross']:,.0f} over {b['over']:,.0f} fx {b['fx']['in_rooms']}")
        print(f"   C (arena 22k) max seats: {d['C']}; gross at 0 seats {d['C0']['gross']:,.0f}")
        print(f"   B+C max seats: {d['BC']}")
