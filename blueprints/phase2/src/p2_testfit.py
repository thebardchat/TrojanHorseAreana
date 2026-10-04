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
    arena = dig(p2, "spaces.arena.sf") if arena_sf is None else arena_sf
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
    sf = 2 * width_in * (run + 2 * landing) / 144.0 * (flights // 2)
    return dict(risers=risers, flights=flights, per_flight=per_flight, riser_in=vc["floor_to_floor_in"] / risers,
                run_in=run, landing_in=landing, width_in=width_in, sf=sf)


def compute_two_level(p2, prog, scenario="base", arena_sf=None, seats=None, upper_share=None):
    f, vc = prog["factors"], prog["vertical_circulation"]
    g, mech = f["gross_up"][scenario], f["mechanical"]["share_of_gross"]
    seats = p2["spaces"]["seating"]["total"] if seats is None else seats
    arena = dig(p2, "spaces.arena.sf") if arena_sf is None else arena_sf
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
    for a in range(0, dig(p2, "spaces.arena.sf") + 1, step):
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


if __name__ == "__main__":
    import sys as _s
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
