"""MARLIN v5: hybrid-concept screening model (bubble curtain + angled boom + adaptive control + manual catch).

Plan-view cohort model. Weighted cohorts of jellyfish are advected by a prescribed current,
may be lifted to the surface by a bubble curtain, guided by an angled floating boom to a
collector, and swept by a small manual-catch crew near the intake entrance. Whatever still
enters the intake opening counts as "reached the screens" (the quantity to minimise).

This is an ILLUSTRATIVE, UNCALIBRATED comparison tool (it ranks control strategies under the
same assumptions). It is not CFD, not a field-performance prediction, and never controls equipment.
No ML / computer-vision model runs here; the controller is a transparent rule set.
"""
from dataclasses import dataclass, field
import math
import numpy as np

DISCLAIMER = ("MARLIN v5: illustrative plan-view screening model with uncalibrated parameters. "
              "Use for comparing strategies, not for predicting field catch rates.")

# ---- fixed geometry (metres; current flows toward +x; breakwater wall at x = WALL_X) ----
WALL_X = 300.0
ENTR_Y = (-30.0, 30.0)               # intake entrance opening in the wall
CURTAIN_X = 120.0
CURTAIN_Y = (-135.0, 135.0)
ZONES = 3                            # independently switched curtain zones across y
BOOM_A = np.array([150.0, -40.0])    # fixed upstream pivot of the boom
BOOM_L = 194.0
DESIGN_REL_ANGLE = math.radians(55.5)  # boom angle relative to current direction
SENSOR_X = 60.0                      # upstream sensing gate
DT = 30.0                            # seconds
HOURS = 10.0
FULL_AIR_KW = 4.8                    # per curtain, borrowed from the v4 estimate (77.1 kWh / 8 h / 2 lines)

@dataclass
class Params:
    """Uncertain physical values. Defaults are mid-range placeholders; run_scenarios samples ranges."""
    surface_frac0: float = 0.35      # share of bloom mass already in the upper layer the boom skirt covers
    p_lift_max: float = 0.55         # share of non-surface mass lifted when a zone is at full air, calm sea
    esc_per_m: float = 0.0008        # escape per metre of boom travel
    esc_per_h: float = 0.25          # escape per hour spent being guided
    sensor_sigma: float = 0.35       # lognormal sensor noise
    crew_kg_h: float = 250.0         # manual crew sweep capacity
    collector_kg_h: float = 2000.0   # collector throughput
    wave_lift_loss_hs: float = 2.0   # significant wave height (m) at which the curtain loses all lift

@dataclass
class Scenario:
    name: str
    label: str
    rate_kg_h: float = 1200.0
    arrival_h: float = 4.0
    y_range: tuple = (-150.0, 150.0)
    hs: float = 0.4                      # significant wave height, m
    u: float = 0.12                      # current speed toward the wall, m/s
    dir_shift_deg: float = 0.0           # current direction change ramped in over hour 2-3
    collector_out: tuple = None          # (start_h, end_h) collector down
    sensor_blind: bool = False
    crew_available: bool = True

@dataclass
class Policy:
    name: str
    label: str
    bubble: str = "off"      # off | fixed_on | adaptive
    boom: str = "fixed"      # none | fixed | adaptive
    crew: bool = False
    crew_when: str = "never" # never | adaptive (only after the estimate shows leakage risk)

POLICIES = [
    Policy("none", "Do nothing (intake screens only)", "off", "none", False),
    Policy("bubble_only", "Bubble curtain only, fixed full air", "fixed_on", "none", False),
    Policy("boom_only", "Angled boom only, fixed angle", "off", "fixed", False),
    Policy("hybrid_fixed", "Bubble + boom, fixed full air, fixed angle", "fixed_on", "fixed", False),
    Policy("hybrid_adaptive", "Bubble + boom, adaptive control", "adaptive", "adaptive", False),
    Policy("hybrid_adaptive_crew", "Adaptive + manual-catch layer 3", "adaptive", "adaptive", True, "adaptive"),
    Policy("hybrid_fixed_crew", "Fixed + manual-catch layer 3", "fixed_on", "fixed", True, "adaptive"),
]

def _seg_cross(p0, p1, a, b):
    """Vectorised: does segment p0->p1 cross segment a->b? p0,p1: (n,2). Returns bool mask and u, the fraction along a->b."""
    r = p1 - p0
    s = b - a
    den = r[:, 0] * s[1] - r[:, 1] * s[0]
    ok = np.abs(den) > 1e-9
    qp = a - p0
    t = np.where(ok, (qp[:, 0] * s[1] - qp[:, 1] * s[0]) / np.where(ok, den, 1), -1)
    u = np.where(ok, (qp[:, 0] * r[:, 1] - qp[:, 1] * r[:, 0]) / np.where(ok, den, 1), -1)
    return ok & (t >= 0) & (t < 1) & (u >= 0) & (u <= 1), u    # u = position along the second segment a->b (0 at a)

def run(scn: Scenario, pol: Policy, par: Params = None, seed: int = 1) -> dict:
    par = par or Params()
    rng = np.random.default_rng(seed)          # same seed -> same arrivals/diffusion for every policy
    nsteps = int(HOURS * 3600 / DT)
    per_step = 4                                # cohorts released per step
    # ---- state arrays (grown by concatenation; sizes are small) ----
    pos = np.zeros((0, 2)); mass = np.zeros(0); sf = np.zeros(0)
    crossed_c = np.zeros(0, bool); crossed_b = np.zeros(0, bool); fate = np.zeros(0, int)  # 0 afloat
    L = {"arrived": 0.0, "screens": 0.0, "collected": 0.0, "crew": 0.0, "wall": 0.0, "lost_far": 0.0}
    guided = []                                 # (arrival_step, kg)
    collector_q = 0.0
    air = np.zeros(ZONES)                       # current zone air levels 0..1
    est_zone = np.zeros(ZONES)
    off_timer = np.zeros(ZONES)
    air_kwh = 0.0; air_on_h = 0.0; boom_deg_moved = 0.0
    alpha_cmd = DESIGN_REL_ANGLE
    crew_active = False; crew_h = 0.0
    sensor_flux = np.zeros(ZONES)
    zone_edges = np.linspace(CURTAIN_Y[0], CURTAIN_Y[1], ZONES + 1)
    est_total = 0.0

    def wave_factor():
        return max(0.0, 1.0 - scn.hs / par.wave_lift_loss_hs)
    overtop = min(0.6, max(0.0, (scn.hs - 0.8) / 1.5))
    crew_ok = scn.crew_available and scn.hs < 1.5

    for k in range(nsteps):
        t_h = k * DT / 3600
        # ---- current direction ----
        shift = math.radians(scn.dir_shift_deg) * min(1.0, max(0.0, (t_h - 2.0)))
        ux, uy = scn.u * math.cos(shift), scn.u * math.sin(shift)
        cur_dir = shift
        # ---- arrivals ----
        if t_h < scn.arrival_h:
            m = scn.rate_kg_h * DT / 3600 / per_step
            y0 = rng.uniform(scn.y_range[0], scn.y_range[1], per_step)
            pos = np.vstack([pos, np.column_stack([np.zeros(per_step), y0])])
            mass = np.concatenate([mass, np.full(per_step, m)])
            sf = np.concatenate([sf, np.full(per_step, par.surface_frac0)])
            crossed_c = np.concatenate([crossed_c, np.zeros(per_step, bool)])
            crossed_b = np.concatenate([crossed_b, np.zeros(per_step, bool)])
            fate = np.concatenate([fate, np.zeros(per_step, int)])
            L["arrived"] += m * per_step
        # ---- sensing (every 5 min) ----
        if pol.bubble == "adaptive" or pol.boom == "adaptive" or pol.crew_when == "adaptive":
            if k % 10 == 0:
                live = (fate == 0) & (pos[:, 0] >= SENSOR_X - 12) & (pos[:, 0] < SENSOR_X + 12)
                for z in range(ZONES):
                    inz = live & (pos[:, 1] >= zone_edges[z]) & (pos[:, 1] < zone_edges[z + 1])
                    true_flux = mass[inz].sum() * 3600.0 / (24.0 / max(ux, 1e-3))   # kg/h through the 24 m sensing window
                    meas = 0.0 if scn.sensor_blind else true_flux * math.exp(rng.normal(0, par.sensor_sigma))
                    est_zone[z] = 0.6 * est_zone[z] + 0.4 * meas
                est_total = est_zone.sum()
        # ---- controller ----
        if pol.bubble == "fixed_on":
            on = t_h < scn.arrival_h + 1.0
            air[:] = 1.0 if on else 0.0
        elif pol.bubble == "adaptive":
            if scn.sensor_blind:
                air[:] = 1.0 if t_h < scn.arrival_h + 0.5 else 0.0     # fail-safe: full on after alert window
            else:
                for z in range(ZONES):
                    e = est_zone[z]
                    target = 0.0 if e < 120 else (0.4 if e < 350 else 1.0)
                    if target > 0:
                        off_timer[z] = 0; air[z] = target
                    else:
                        off_timer[z] += DT / 60
                        if off_timer[z] > 15: air[z] = 0.0
        else:
            air[:] = 0.0
        if wave_factor() <= 0.0 and pol.bubble == "adaptive":
            air[:] = 0.0                                              # no benefit in these seas: stop wasting energy
        air_kwh += float(air.sum()) / ZONES * FULL_AIR_KW * DT / 3600
        air_on_h += float((air > 0).any()) * DT / 3600
        # ---- boom geometry ----
        if pol.boom == "adaptive":
            want = cur_dir + DESIGN_REL_ANGLE
            alpha_cmd = alpha_cmd if k else want
            step = math.radians(1.0) * DT / 60
            delta = max(-step, min(step, want - alpha_cmd))
            alpha_cmd += delta; boom_deg_moved += abs(math.degrees(delta))
            alpha = alpha_cmd
        else:
            alpha = DESIGN_REL_ANGLE
        boom_on = pol.boom != "none"
        B = BOOM_A + BOOM_L * np.array([math.cos(alpha), math.sin(alpha)])
        # ---- crew (layer 3) ----
        if pol.crew:
            crew_active = crew_ok and (pol.crew_when != "adaptive" or t_h < scn.arrival_h + 1.5)
            if crew_active: crew_h += DT / 3600
        # ---- advect ----
        if len(mass):
            live = fate == 0
            idx = np.where(live)[0]
            p0 = pos[idx].copy()
            diff = rng.normal(0, math.sqrt(2 * 0.05 * DT), (len(idx), 2))
            p1 = p0 + np.array([ux, uy]) * DT + diff
            # curtain crossing
            if pol.bubble != "off":
                x0, x1 = p0[:, 0], p1[:, 0]
                hit = (~crossed_c[idx]) & (x0 < CURTAIN_X) & (x1 >= CURTAIN_X)
                yc = p0[:, 1] + (p1[:, 1] - p0[:, 1]) * (CURTAIN_X - x0) / np.where(x1 == x0, 1, x1 - x0)
                inside = hit & (yc >= CURTAIN_Y[0]) & (yc < CURTAIN_Y[1])
                zi = np.clip(np.searchsorted(zone_edges, yc, side="right") - 1, 0, ZONES - 1)
                lvl = air[zi] * wave_factor() * par.p_lift_max
                j = idx[inside]
                sf[j] = sf[j] + (1 - sf[j]) * lvl[inside]
                crossed_c[idx[hit]] = True
            else:
                crossed_c[idx] = True
            # boom crossing: split into guided / passing mass
            if boom_on:
                cr, tt = _seg_cross(p0, p1, BOOM_A, B)
                cr &= ~crossed_b[idx]
                jj = idx[cr]
                if len(jj):
                    s_hit = tt[cr]                                    # fraction along the boom from A (pivot)
                    dist = (1 - s_hit) * BOOM_L
                    bvec = (B - BOOM_A) / BOOM_L
                    speed = max(0.02, ux * bvec[0] + uy * bvec[1])
                    dwell_h = dist / speed / 3600
                    retain = np.exp(-par.esc_per_m * dist - par.esc_per_h * dwell_h)
                    g_frac = sf[jj] * (1 - overtop) * retain
                    g_kg = mass[jj] * g_frac
                    for kg, dh in zip(g_kg, dwell_h):
                        guided.append((k + int(dh * 3600 / DT) + 1, float(kg)))
                    mass[jj] = mass[jj] - g_kg
                    # remaining mass keeps drifting; surface share of remainder is whatever was not guided
                    sf[jj] = np.where(mass[jj] > 1e-12, np.clip(sf[jj] * (1 - (1 - overtop) * retain) / np.maximum(1 - g_frac, 1e-9), 0, 1), 0)
                    crossed_b[jj] = True
            pos[idx] = p1
            # wall / entrance
            x1 = pos[:, 0]
            gone = (fate == 0) & (x1 >= WALL_X)
            for j in np.where(gone)[0]:
                if ENTR_Y[0] <= pos[j, 1] <= ENTR_Y[1]:
                    L["screens"] += mass[j]; fate[j] = 1
                else:
                    L["wall"] += mass[j]; fate[j] = 2
            # crew sweep in approach zone (surface mass only)
            if pol.crew and crew_active:
                cap = par.crew_kg_h * DT / 3600
                zone = (fate == 0) & (pos[:, 0] > 250) & (pos[:, 0] < WALL_X) & (pos[:, 1] > ENTR_Y[0] - 20) & (pos[:, 1] < ENTR_Y[1] + 20)
                zi_ = np.where(zone)[0]
                if len(zi_):
                    avail = (mass[zi_] * sf[zi_]).sum()
                    take = min(cap, avail)
                    if avail > 0:
                        frac = take / avail
                        removed = mass[zi_] * sf[zi_] * frac
                        mass[zi_] -= removed
                        L["crew"] += float(removed.sum())
                        sf[zi_] = np.where(mass[zi_] > 1e-12, np.clip(sf[zi_] * (1 - frac) / np.maximum(1 - sf[zi_] * frac, 1e-9), 0, 1), 0)
        if k % 20 == 0 and len(mass):               # drop finished cohorts (speed only; ledger already updated)
            keep = (fate == 0) & (mass > 1e-12)
            pos, mass, sf, crossed_c, crossed_b, fate = pos[keep], mass[keep], sf[keep], crossed_c[keep], crossed_b[keep], fate[keep]
        # ---- collector ----
        arrivals_now = sum(kg for (s, kg) in guided if s <= k)
        guided = [(s, kg) for (s, kg) in guided if s > k]
        collector_q += arrivals_now
        out = scn.collector_out and scn.collector_out[0] <= t_h < scn.collector_out[1]
        rate = 0.0 if out else par.collector_kg_h * DT / 3600
        done = min(collector_q, rate)
        L["collected"] += done; collector_q -= done
        if collector_q > 3000:                                         # buffer full -> overflow released at boom end, drifts on
            spill = collector_q - 3000; collector_q = 3000
            pos = np.vstack([pos, [[B[0] + 3, B[1] + 3]]]); mass = np.append(mass, spill); sf = np.append(sf, 0.0)
            crossed_c = np.append(crossed_c, True); crossed_b = np.append(crossed_b, True); fate = np.append(fate, 0)
    L["held_in_collector"] = collector_q
    afloat = float(mass[fate == 0].sum()) if len(mass) else 0.0
    L["afloat"] = afloat + sum(kg for _, kg in guided)
    res = dict(L)
    res["screens_pct"] = 100 * L["screens"] / L["arrived"]
    res["collected_pct"] = 100 * L["collected"] / L["arrived"]
    res["crew_pct"] = 100 * L["crew"] / L["arrived"]
    res["air_kwh"] = air_kwh; res["air_on_h"] = air_on_h; res["crew_h"] = crew_h; res["boom_deg_moved"] = boom_deg_moved
    ledger = L["screens"] + L["collected"] + L["crew"] + L["wall"] + L["held_in_collector"] + L["afloat"]
    res["ledger_err_kg"] = ledger - L["arrived"]
    return res
