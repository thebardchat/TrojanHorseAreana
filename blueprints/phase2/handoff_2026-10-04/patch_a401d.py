P = "C:/Users/Hubby/AppData/Local/Temp/claude/C--Users-Hubby-Desktop-ARENA/202807a2-361c-4275-8ca9-11bac63af77d/scratchpad/repo/blueprints/phase2/src/p2_a_401.py"
s = open(P, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('    if rev in ("B", "C"):\n        rb = rd("phase2_enlarged_rev_b.yaml" if rev == "B" else "phase2_enlarged_rev_c.yaml")',
    '    if rev in ("B", "C", "D"):\n        rb = rd({"B": "phase2_enlarged_rev_b.yaml", "C": "phase2_enlarged_rev_c.yaml", "D": "phase2_enlarged_rev_d.yaml"}[rev])')
rep('    if rev == "C":\n        out["core"] = core_calc_c(rb, plan)\n    return out',
    '    if rev == "C":\n        out["core"] = core_calc_c(rb, plan)\n    if rev == "D":\n        out["core"] = core_calc_d(rb, plan)\n    return out')
rep('        "drawn_by": meta2["drawn_by"],\n        "sheet_no": SHEET_NO,',
    '        "drawn_by": (rb or {}).get("meta", {}).get("drawn_by", meta2["drawn_by"]),\n        "sheet_no": SHEET_NO,')
rep('    if c["rev"] == "C":\n        return build_c(c, sh, body_bottom, top, rooms, en, em, rb, plan)',
    '    if c["rev"] == "C":\n        return build_c(c, sh, body_bottom, top, rooms, en, em, rb, plan)\n    if c["rev"] == "D":\n        return build_d(c, sh, body_bottom, top, rooms, en, em, rb, plan)')
rep('    ap.add_argument("--rev", choices=["A", "B", "C"]', '    ap.add_argument("--rev", choices=["A", "B", "C", "D"]')

NEW = r'''

def core_calc_d(rb, plan):
    """Rev D (D-072): core-2 test-fits vs the chairs-only split and vs the drawn rooms on plan Rev J (rooms may be turned: rot);
    area tallies: bump-out = women (2) + MECH (E2); old Mech (E) strip = men (2) + DF / JAN. + public corridor + MECH (E)."""
    import p2_testfit as tf
    lp = tf.summary_k()[3]["loop"]
    fc, sp = lp["fx1c"], lp["split"]
    lc, c2 = sp["lobby"], sp["core2"]
    co = rb["core"]
    mods = co["modules"]
    rects = {r["id"]: r for r in plan["level_1"]["rooms"]}
    need = {"men": (c2["men_wc"] + c2["men_urinals"], c2["men_lav"]), "women": (c2["women_wc"], c2["women_lav"])}
    ar = lambda r: (r[2] - r[0]) * (r[3] - r[1])  # noqa: E731
    res = {}
    for key, rm in co["rooms"].items():
        cnt = {k: 0 for k in mods}
        for row in rm["rows"]:
            run = row["x0"]
            for t_, n in row["items"]:
                cnt[t_] += n
                run += mods[t_]["w"] * n
                if mods[t_]["d"] > row["y"][1] - row["y"][0] + 1e-6:
                    sys.exit(f"{key}: {t_} deeper than its row")
            if run > rm["L"] + 1e-6:
                sys.exit(f"{key}: row {row['y']} runs {run} ft > room length {rm['L']}")
        lav = rm["lav"]
        if lav["y0"] + lav["n"] * mods["lav"]["w"] > rm["W"] + 1e-6:
            sys.exit(f"{key}: lavatory counter longer than the {rm['W']} ft wall")
        e0, e1 = rm["entry"]
        if any(row["y"][0] < 1e-6 and row["x0"] < e1 - 1e-6 for row in rm["rows"]):
            sys.exit(f"{key}: entry {rm['entry']} blocked by a fixture row on the corridor wall")
        wc = cnt["wc_std"] + cnt["wc_amb"] + cnt["wc_acc"]
        ur = cnt["urinal"] + cnt["urinal_acc"]
        n_wc, n_lav = need[key]
        ur_max = math.floor(0.67 * n_wc)                       # IPC 2021 424.2
        if wc + ur != n_wc or lav["n"] != n_lav or ur > ur_max or cnt["wc_acc"] < 1 or (wc + ur >= 6 and cnt["wc_amb"] < 1) or (ur > 1 and cnt["urinal_acc"] < 1):
            sys.exit(f"{key}: test-fit {wc} WC + {ur} urinals / {lav['n']} lav does not meet core 2 {n_wc} / {n_lav} (urinals <= {ur_max})")
        dr = rects[rm["drawn_id"]]
        r = dr["rect"]
        dw, dh = r[2] - r[0], r[3] - r[1]
        fl, fw = (dh, dw) if rm.get("rot") else (dw, dh)
        if rm["L"] > fl + 1e-6 or rm["W"] > fw + 1e-6:
            sys.exit(f"{key}: test-fit {rm['L']} x {rm['W']} does not fit the drawn room ({fl:g} x {fw:g} in its frame)")
        c2p = dr["core2"]
        if (c2p["wc"], c2p["ur"], c2p["lav"]) != (wc, ur, lav["n"]):
            sys.exit(f"{key}: plan Rev J core2 tag {c2p} differs from the test-fit")
        net = rm["L"] * rm["W"]
        res[key] = dict(cnt=cnt, wc=wc, ur=ur, lav=lav["n"], need_wc=n_wc, need_lav=n_lav, ur_max=ur_max, drawn=dw * dh, drawn_wh=(dw, dh),
                        net=net, allow=dw * dh / net - 1)
    dj = rects[co["df_jan"]["drawn_id"]]
    if dj["core2"]["df"] != c2["df"] or co["df_jan"]["df"] != c2["df"]:
        sys.exit("core-2 drinking fountains drifted")
    pc = next(z for z in plan["level_1"]["zones"] if z["id"] == co["corridor"]["zone_id"])["rect"]
    bo = plan["building"]["bumpout"]["rect"]
    me, me2 = ar(rects["mech_e"]["rect"]), ar(rects["mech_e2"]["rect"])
    dfj, corr, bo_sf = ar(dj["rect"]), ar(pc), ar(bo)
    if abs(res["women"]["drawn"] + me2 - bo_sf) > 0.5:
        sys.exit(f"bump-out rooms {res['women']['drawn'] + me2} != bump-out {bo_sf}")
    strip = res["men"]["drawn"] + dfj + corr + me
    if abs(strip - co["strip_sf"]) > 0.5:
        sys.exit(f"old Mech (E) strip rooms {strip:.1f} != {co['strip_sf']}")
    if abs((pc[2] - pc[0]) - co["corridor"]["width_ft"]) > 1e-6:
        sys.exit("public corridor width drifted")
    res.update(fc=fc, lobby=lc, core2=c2, dfj=dfj, corr=corr, corr_w=pc[2] - pc[0], corr_l=pc[3] - pc[1], pc=pc, bumpout=bo_sf, bo=bo,
               mech_e=me, mech_e2=me2, strip=strip)
    return res


def build_d(c, sh, body_bottom, top, rooms, en, em, rb, plan):
    """Rev D (D-072): key plan on plan Rev J; core 2 + public corridor enlarged plan (turned: plan north -> sheet right); split + areas."""
    co, cr_ = rb["core"], c["core"]
    bo, pc = cr_["bo"], cr_["pc"]
    rr = {r_["id"]: r_["rect"] for r_ in plan["level_1"]["rooms"]}
    # ---------------- key plan (Rev J)
    kx, ky, ks = 5.45, 2.3, 1.0 / 250
    bx0, by0, bx1, by1 = plan["building"]["rect"]
    pj = plan["building"]["projection"]["rect"]
    pts = [(bx0, by0), (bx1, by0), (bx1, pj[3]), (pj[0], pj[3]), (pj[0], by1), (bx0, by1), (bx0, by0)]
    KP = lambda x, y: (kx + x * ks, ky + y * ks)  # noqa: E731
    for (xa, ya), (xb, yb) in zip(pts[:-1], pts[1:]):
        a, b = KP(xa, ya)
        c2, d2 = KP(xb, yb)
        sh.line(a, b, c2, d2, layer=L_WALL, lw=0.9)
    an = plan["building"]["annex"]["rect"]
    for r_ in (an, bo):
        sh.poly([KP(r_[0], r_[1]), KP(r_[2], r_[1]), KP(r_[2], r_[3]), KP(r_[0], r_[3])], fill="#F4F4F4", layer=L_WALL, lw=0.6)
    av = plan["arena_volume"]["rect"]
    a, b = KP(av[0], av[1])
    sh.rect(a, b, (av[2] - av[0]) * ks, (av[3] - av[1]) * ks, layer=L_DIM, lw=0.3)
    for rid, rm in rooms.items():
        r = rm["rect"]
        sh.poly([KP(r[0], r[1]), KP(r[2], r[1]), KP(r[2], r[3]), KP(r[0], r[3])], fill="#BBBBBB", layer=L_TAG, lw=0.3)
        cx, cy = KP((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)
        sh.text(cx, cy - 0.025, rid[-1], size=4.2, bold=True, align="center", layer=L_TAG)
    for rid, lab_ in (("rr_m1", "M"), ("rr_w1", "W"), ("rr_mb", ""), ("rr_wb", "")):
        r = rr[rid]
        sh.poly([KP(r[0], r[1]), KP(r[2], r[1]), KP(r[2], r[3]), KP(r[0], r[3])], fill="#BFD7EA", layer=L_TAG, lw=0.3)
        if lab_:
            cx, cy = KP((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)
            sh.text(cx, cy - 0.025, lab_, size=4.2, bold=True, align="center", layer=L_TAG)
    sh.poly([KP(pc[0], pc[1]), KP(pc[2], pc[1]), KP(pc[2], pc[3]), KP(pc[0], pc[3])], fill="#CFE8D4", layer=L_TAG, lw=0.3)
    a, b = KP(bo[2] + 3, (bo[1] + bo[3]) / 2)
    sh.text(a, b - 0.02, "CORE 2", size=4.2, bold=True, layer=L_TAG)
    sh.text(kx, ky + an[3] * ks + 0.2, "KEY PLAN — L1 (A-101 J)", size=5.2, bold=True)
    sh.text(kx, ky + an[3] * ks + 0.09, "1\" = 250' · grey = rooms 1-4", size=4.4, color=GRY)
    sh.text(kx, ky - 0.12, "blue = restrooms · green = public corridor (E)", size=4.4, color=GRY)
    # ---------------- right panel text
    sh.line(11.72, top - 0.02, 11.72, body_bottom + 0.1, lw=0.4)
    cr = g2.Col(sh, 11.85, top + 0.12, 4.65, 1.0)
    cr.para(em["disclaimer"], size=5.1, color=GRY)
    cr.head("COMMON PATH — VERIFIED ON THIS LAYOUT (T1006.2.1)", size=6.8)
    cp = en["rules"]["common_path"]
    cr.para(f"{cp['text'][0].upper() + cp['text'][1:]} — {cp['source'].split(' (')[0]}.", size=5.1)
    cr.table([("ROOM", 0, "left"), ("OCC.", 0.62, "right"), ("WORST POINT", 0.72, "left", 1.55), ("CP ft", 2.75, "right"), ("RESULT", 2.85, "left"),
              ("+ TO EXIT", 4.6, "right")],
             [((f"{r_['id'][-1]}", f"{r_['occ']}", r_["worst"]["label"], f"{r_['worst']['length']:.1f}", f"≤ {c['lim']} PASS" if r_["ok"] else "FAIL",
                f"{r_['b']['exit']} {r_['travel']:.0f} ft"), dict(colors={4: GRN if r_["ok"] else RED})) for r_ in c["rooms"]],
             size=5.0, rh=0.108)
    cr.para(f"Rooms 1-4 unchanged (Rev A approved, D-068). Rooms 3-4 reach X7 on the building wall again (EXIT (E) clear, D-072): travel ≤ "
            f"{max(r_['travel'] for r_ in c['rooms']):.0f} ft vs 250 ft (T1017.2). Locker fixtures as Rev A (ADA 604.8, 606, 608, 803, 811, 903).", size=5.1)
    fc, lc, c2_ = cr_["fc"], cr_["lobby"], cr_["core2"]
    m, w = cr_["men"], cr_["women"]
    cr.head("L1 PUBLIC RESTROOMS — CHAIRS-ONLY (D-064 · D-069 · D-072)", size=6.8)
    cr.para(f"L1 load chairs-only 2,346 + 1,100 = {fc['load']:,} (IBC 2021 T2902.1, 50/50 split 2902.1.1). Lobby core = rooms 4 + 5; core 2 = "
            "women (2) in the bump-out + men (2) and DF in the old Mech (E) strip, all off the public corridor (E).", size=5.1)
    ok = lambda a_, b_: ("PASS", GRN) if a_ >= b_ else ("SHORT", RED)  # noqa: E731
    rows = []
    for lab_, req, lo_, c2v, c2s in (("Men WC (incl. urinals)", fc["wc_m"], lc["men_wc"], c2_["men_wc"] + c2_["men_urinals"], f"{m['wc']} + {m['ur']} ur"),
                                     ("Men lavatories", fc["lav_m"], lc["men_lav"], c2_["men_lav"], f"{m['lav']}"),
                                     ("Women WC", fc["wc_f"], lc["women_wc"], c2_["women_wc"], f"{w['wc']}"),
                                     ("Women lavatories", fc["lav_f"], lc["women_lav"], c2_["women_lav"], f"{w['lav']}"),
                                     ("Drinking fountains", fc["df"], lc["df"], c2_["df"], f"{c2_['df']} (hi-lo)")):
        r_, col_ = ok(lo_ + c2v, req)
        rows.append(((lab_, f"{req}", f"{lo_}", c2s, f"{lo_ + c2v}", r_), dict(colors={5: col_})))
    cr.table([("FIXTURE", 0, "left"), ("REQ.", 1.55, "right"), ("LOBBY", 2.05, "right"), ("CORE 2", 2.85, "right"), ("TOTAL", 3.4, "right"), ("RESULT", 3.55, "left")],
             rows, size=5.0, rh=0.108)
    cr.para(f"Urinals: core 2 {m['ur']} ≤ {m['ur_max']} = 67 % of its 12 (IPC 2021 424.2, R-009). 1 accessible urinal (ADA 213.3.3, 605); 1 wheelchair + "
            "1 ambulatory compartment per room (213.3.1, 604.8); 1 accessible lav (606); 60 in turning space (304.3); hi-lo fountains (211.2, 602).", size=5.0)
    # ---------------- enlarged plan: core 2 + public corridor, turned (plan north -> sheet right, plan east -> sheet down)
    s2 = 1.0 / co["scale_ft_per_in"]
    vy0, vy1, vx0, vx1 = rr["df_jan"][1], bo[3], 188.0, bo[2]
    ox, oy = 12.15, 2.15                                  # sheet point of plan (vx1, vy0)
    P = lambda x, y: (ox + (y - vy0) * s2, oy + (vx1 - x) * s2)  # noqa: E731

    def pl_(x1, y1, x2, y2, layer=L_WALL, lw=1.0):
        a_, b_ = P(x1, y1)
        c_, d_ = P(x2, y2)
        sh.line(a_, b_, c_, d_, layer=layer, lw=lw)

    def box(r_, lw=0.9, fill=None):
        if fill:
            sh.poly([P(r_[0], r_[1]), P(r_[2], r_[1]), P(r_[2], r_[3]), P(r_[0], r_[3])], fill=fill, layer=L_TAG, lw=0)
        for q in ((r_[0], r_[1], r_[2], r_[1]), (r_[2], r_[1], r_[2], r_[3]), (r_[2], r_[3], r_[0], r_[3]), (r_[0], r_[3], r_[0], r_[1])):
            pl_(*q, lw=lw)
    rmb, rwb, rdj, me2, evl4 = rr["rr_mb"], rr["rr_wb"], rr["df_jan"], rr["mech_e2"], rr["evl_4"]
    box([pc[0], vy0, pc[2], pc[3]], lw=0.0, fill="#E3F1E6")
    pl_(bo[0], bo[1], bo[2], bo[1], lw=1.6)                # bump-out
    pl_(bo[2], bo[1], bo[2], bo[3], lw=1.6)
    pl_(bo[2], bo[3], bo[0], bo[3], lw=1.6)
    ew = w["entry_plan"] = (rwb[1] + co["rooms"]["women"]["entry"][0], rwb[1] + co["rooms"]["women"]["entry"][1])
    pl_(bx1, vy0, bx1, ew[0], lw=1.6)                      # building wall x 210 with the women's door
    pl_(bx1, ew[1], bx1, evl4[3], lw=1.6)
    pl_(vx0, vy0, vx0, evl4[3], lw=1.0)                    # tier back wall x 188
    box(rmb)
    box(evl4, lw=0.6)
    box(me2, lw=0.9)
    pl_(rdj[0], rdj[1], rdj[2], rdj[1], lw=0.9)
    pl_(rdj[0], rdj[1], rdj[0], rdj[3], lw=0.9)            # DF alcove open to the corridor
    pl_(pc[0], rmb[1], pc[0], rmb[3], lw=0.9)              # corridor wall on the men's side (entry ticks drawn by the test-fit)
    pl_(pc[0], rmb[3], pc[2], rmb[3], lw=0.9)              # corridor north end (dead end, <= 20 ft past the last door)
    TW = lambda fx, fy: P(rwb[0] + fy, rwb[1] + fx)  # noqa: E731
    TM = lambda fx, fy: P(pc[0] - fy, rmb[3] - fx)  # noqa: E731
    draw_core_t(sh, co["rooms"]["women"], co["modules"], TW)
    draw_core_t(sh, co["rooms"]["men"], co["modules"], TM)
    # X11 + labels
    x11 = next(d for d in plan["level_1"]["doors"]["items"] if d["id"] == "X11")
    pl_(bx1, x11["at"] - 2.67, bx1, x11["at"] + 2.67, lw=3.0)
    a, b = P(bx1, x11["at"])
    sh.line(a, b, a, b - 0.16, layer=L_WALL, lw=0.8)
    sh.line(a, b - 0.16, a - 0.04, b - 0.1, layer=L_WALL, lw=0.8)
    sh.line(a, b - 0.16, a + 0.04, b - 0.1, layer=L_WALL, lw=0.8)
    sh.text(a, b - 0.27, "X11 EXIT · 64 in", size=4.4, bold=True, align="center", layer=L_TAG)
    a, b = P((pc[0] + pc[2]) / 2, vy0)
    sh.text(a - 0.04, b - 0.03, "← CONCOURSE (E)", size=4.0, bold=True, align="right", layer=L_TAG, color=GRN)
    a, b = P((pc[0] + pc[2]) / 2, 117.5)
    sh.text(a, b - 0.025, f"PUBLIC CORRIDOR (E) · {cr_['corr_w']:g}'-0\" = {cr_['corr_w'] * 12:.0f} in", size=4.0, bold=True, align="center", layer=L_TAG, color=GRN)
    a, b = P((rdj[0] + rdj[2]) / 2, (rdj[1] + rdj[3]) / 2)
    sh.text(a + 0.005, b, "27 DF + JAN.", size=3.4, bold=True, align="center", layer=L_TAG, rot=90)
    a, b = P((evl4[0] + evl4[2]) / 2, (evl4[1] + evl4[3]) / 2)
    sh.text(a, b - 0.02, "14 EVENT LOCKER 4 (unchanged)", size=4.2, align="center", layer=L_TAG, color=GRY)
    a, b = P((me2[0] + me2[2]) / 2, (me2[1] + me2[3]) / 2)
    sh.text(a, b + 0.02, f"28 MECH (E2) · {cr_['mech_e2']:,.0f} SF", size=4.4, bold=True, align="center", layer=L_TAG)
    sh.text(a, b - 0.09, "service door on the east face (ASSUMED)", size=3.8, align="center", layer=L_TAG, color=GRY)
    a, b = P(vx0 + 1, (evl4[3] + evl4[1]) / 2)
    a, b = P((rwb[0] + rwb[2]) / 2 + 9, (rwb[1] + rwb[3]) / 2)
    a2, b2 = P(bo[2], (rwb[1] + rwb[3]) / 2)
    sh.text(a2, b2 - 0.13, f"26 WOMEN (2) · {w['drawn']:,.0f} SF · {w['wc']} WC · {w['lav']} LAV", size=4.5, bold=True, align="center", layer=L_TAG)
    a, b = P(vx0, (rmb[1] + rmb[3]) / 2)
    sh.text(a, b + 0.1, f"25 MEN (2) · {m['drawn']:,.0f} SF · {m['wc']} WC + {m['ur']} UR · {m['lav']} LAV", size=4.5, bold=True, align="center", layer=L_TAG)
    a, b = P(bo[0], bo[3])
    sh.text(a + 0.04, b + 0.04, "EXIT (E) beyond — clear · X7 on the wall →", size=4.0, layer=L_TAG, color=GRY)
    # dims along the bump-out (bottom = east face) and N arrow
    a, b = P(bo[2], bo[1])
    c2, d2 = P(bo[2], bo[3])
    yd = b - 0.42
    sh.line(a, yd, c2, yd, layer=L_DIM, lw=0.3)
    for xx in (a, c2):
        sh.line(xx, yd - 0.03, xx, yd + 0.03, layer=L_DIM, lw=0.3)
    sh.text((a + c2) / 2, yd - 0.1, f"bump-out {bo[3] - bo[1]:g}'-0\" (N-S) x {bo[2] - bo[0]:g}'-0\" (E-W) = {cr_['bumpout']:,.0f} SF, one storey", size=4.5, align="center", layer=L_DIM)
    tx, ty = P(vx0, vy1)
    nx, ny = tx + 0.12, ty - 0.35
    sh.line(nx, ny, nx + 0.26, ny, layer=L_DIM, lw=0.9)
    sh.line(nx + 0.26, ny, nx + 0.18, ny + 0.045, layer=L_DIM, lw=0.9)
    sh.line(nx + 0.26, ny, nx + 0.18, ny - 0.045, layer=L_DIM, lw=0.9)
    sh.text(nx + 0.13, ny + 0.07, "N", size=6.5, bold=True, align="center", layer=L_DIM)
    ttop = P(vx0, vy0)[1]
    sh.text(11.85, ttop + 0.37, "RESTROOM CORE 2 + PUBLIC CORRIDOR (E) — D-072 · ENLARGED PLAN", size=6.4, bold=True)
    sh.text(11.85, ttop + 0.25, f"1\" = {co['scale_ft_per_in']}'-0\" · plan turned: north → right, east → down · test-fits ASSUMED", size=4.6, color=GRY)
    sh.text(11.85, 1.66, "A = accessible · AMB = ambulatory · dashed circle = 60 in turning space · grey = chase · ticks = room entry", size=4.2, color=GRY)
    if cr.y < ttop + 0.55:
        raise SystemExit(f"LAYOUT OVERFLOW: right column text runs {ttop + 0.55 - cr.y:.2f} in into the core-2 plan")
    # ---------------- lower middle: areas, why, MEP, sources
    cs = g2.Col(sh, 7.0, 4.22, 4.55, 1.0)
    cs.table([("CORE 2 AREA (SF)", 0, "left"), ("DRAWN", 1.95, "right"), ("TEST-FIT NET", 2.95, "right"), ("WALLS / CHASE", 4.1, "right")],
             [(("Women (2), 30 x 34 (bump-out)", f"{w['drawn']:,.0f}", f"{w['net']:,.0f}", f"+{w['allow'] * 100:.1f} %"), None),
              (("Mech (E2), 30 x 22 (bump-out)", f"{cr_['mech_e2']:,.0f}", "", ""), None),
              (("BUMP-OUT 30 x 56 (A-101 J)", f"{cr_['bumpout']:,.0f}", "", ""), dict(bold=True, rule=True)),
              (("Men (2), 14 x 26 (strip)", f"{m['drawn']:,.0f}", f"{m['net']:,.1f}", f"+{m['allow'] * 100:.1f} %"), None),
              (("DF alcove + janitor, 14 x 4", f"{cr_['dfj']:,.0f}", "", ""), None),
              ((f"Public corridor (E), {cr_['corr_w']:g} x {cr_['corr_l']:.2f}", f"{cr_['corr']:,.0f}", "", ""), None),
              (("Mech (E), 14 x 48.18", f"{cr_['mech_e']:,.1f}", "", "was 1,720"), None),
              (("OLD MECH (E) STRIP 22 x 78.18", f"{cr_['strip']:,.0f}", "", "GSF ±0"), dict(bold=True, rule=True))],
             size=5.0, rh=0.108)
    cs.para(co["why"], size=5.0)
    cs.para(co["mep"], size=5.0, color=RED)
    cs.para("Public toilets within one storey and 500 ft of every seat (IBC 2902.3.3): PASS. Dead end past the last door ≈ 5 ft ≤ 20 ft (1020.5).", size=5.0)
    cs.para("Sources: params/phase2_enlarged.yaml, phase2_enlarged_rev_d.yaml, phase2_plan_rev_j.yaml, phase2_program.yaml (rev_k); IBC 2021 "
            "T2902.1, 2902.3.3, 1003.6, 1006.2.1, 1020.5, T1017.2; IPC 2021 405.3.1, 405.3.5, 424.2; ADA 2010 211.2, 213.3, 304.3, 602, 604.8, 605, 606; "
            "D-064, D-068, D-069, D-070, D-072; R-014; Shane 2026-10-04 evening.", size=4.8, color=GRY)
    return sh, body_bottom, [cs]
'''
i = s.index("\ndef ft_in(v):")
s = s[:i] + NEW + "\n" + s[i:]
open(P, "w", encoding="utf-8").write(s)
print("a401 patched")
