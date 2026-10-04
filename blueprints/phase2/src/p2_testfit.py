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


if __name__ == "__main__":
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
