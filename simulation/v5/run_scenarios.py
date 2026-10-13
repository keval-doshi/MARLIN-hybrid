"""Run all scenarios x policies with Monte Carlo over uncertain parameters. Writes outputs/v5/."""
import csv, json, math, sys
from pathlib import Path
import numpy as np
from engine import *

N = 40
SCENARIOS = [
 Scenario("calm", "Calm reference (1200 kg/h, 4 h)"),
 Scenario("storm", "Storm: Hs 2 m (curtain loses lift, boom overtopped, crew stood down)", hs=2.0),
 Scenario("moderate_sea", "Moderate sea: Hs 1.2 m", hs=1.2),
 Scenario("triple", "Triple bloom load (3600 kg/h)", rate_kg_h=3600.0),
 Scenario("current_shift", "Current direction rotates +30 deg after hour 2", dir_shift_deg=30.0),
 Scenario("current_shift_neg", "Current direction rotates -30 deg after hour 2", dir_shift_deg=-30.0),
 Scenario("one_sided", "Bloom arrives only on one side (y -150..-20)", y_range=(-150.0, -20.0)),
 Scenario("collector_out", "Collector down for 2 h (hours 1-3)", collector_out=(1.0, 3.0)),
 Scenario("sensor_blind", "Sensors blind (adaptive falls back to fail-safe full air)", sensor_blind=True),
 Scenario("weak_current", "Weak current 0.05 m/s", u=0.05),
]

def sample_params(rng, zero_bubble=False):
    return Params(
        surface_frac0=rng.uniform(0.2, 0.6),
        p_lift_max=0.0 if zero_bubble else rng.uniform(0.2, 0.8),
        esc_per_m=rng.uniform(0.0004, 0.0016),
        esc_per_h=rng.uniform(0.1, 0.5),
        sensor_sigma=rng.uniform(0.2, 0.5),
        crew_kg_h=rng.uniform(100, 400),
        collector_kg_h=rng.uniform(1200, 3000),
    )

def _job(sc_i, variant):
    sc = SCENARIOS[sc_i]; rows = []
    rng = np.random.default_rng(1000 + sc_i)
    draws = [sample_params(rng, variant == "bubble_zero") for _ in range(N)]
    base = [run(sc, POLICIES[0], draws[i], seed=500 + i)["screens"] for i in range(N)]
    for pol in POLICIES:
        red, kwh, onh, crewh, crewkg = [], [], [], [], []
        for i in range(N):
            r = run(sc, pol, draws[i], seed=500 + i)
            assert abs(r["ledger_err_kg"]) < 1e-6, "mass ledger error"
            red.append(100 * (1 - r["screens"] / base[i]) if base[i] > 0 else float("nan"))
            kwh.append(r["air_kwh"]); onh.append(r["air_on_h"]); crewh.append(r["crew_h"]); crewkg.append(r["crew"])
        q = lambda a, p: float(np.nanpercentile(a, p))
        rows.append(dict(scenario=sc.name, bubble_assumption=variant, policy=pol.name,
            reduction_p10=round(q(red, 10), 1), reduction_median=round(q(red, 50), 1), reduction_p90=round(q(red, 90), 1),
            air_kwh_median=round(q(kwh, 50), 1), air_on_h_median=round(q(onh, 50), 2),
            crew_h_median=round(q(crewh, 50), 2), crew_kg_median=round(q(crewkg, 50), 1)))
    return rows

def main(out="../../outputs/v5"):
    out = Path(__file__).resolve().parent / out
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    from multiprocessing import Pool
    jobs = [(i, v) for i in range(len(SCENARIOS)) for v in ("bubble_effective", "bubble_zero")]
    with Pool() as pool:
        for part in pool.starmap(_job, jobs):
            rows.extend(part)
    _unused = None
    for sc_i, sc in enumerate([]):
        for variant in ():
            rng = np.random.default_rng(1000 + sc_i)
            draws = [sample_params(rng, variant == "bubble_zero") for _ in range(N)]
            base = [run(sc, POLICIES[0], draws[i], seed=500 + i)["screens"] for i in range(N)]
            for pol in POLICIES:
                red, kwh, onh, crewh, crewkg, coll = [], [], [], [], [], []
                for i in range(N):
                    r = run(sc, pol, draws[i], seed=500 + i)
                    assert abs(r["ledger_err_kg"]) < 1e-6, "mass ledger error"
                    red.append(100 * (1 - r["screens"] / base[i]) if base[i] > 0 else float("nan"))
                    kwh.append(r["air_kwh"]); onh.append(r["air_on_h"]); crewh.append(r["crew_h"])
                    crewkg.append(r["crew"]); coll.append(r["collected"])
                q = lambda a, p: float(np.nanpercentile(a, p))
                rows.append(dict(scenario=sc.name, bubble_assumption=variant, policy=pol.name,
                    reduction_p10=round(q(red, 10), 1), reduction_median=round(q(red, 50), 1), reduction_p90=round(q(red, 90), 1),
                    air_kwh_median=round(q(kwh, 50), 1), air_on_h_median=round(q(onh, 50), 2),
                    crew_h_median=round(q(crewh, 50), 2), crew_kg_median=round(q(crewkg, 50), 1)))
    with open(out / "scenario_summary.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    (out / "results.json").write_text(json.dumps(dict(disclaimer=DISCLAIMER, draws=N, rows=rows), indent=1))
    # idle check: zero arrivals -> adaptive should use no air
    idle = run(Scenario("idle", "no bloom", rate_kg_h=0.0001), [p for p in POLICIES if p.name == "hybrid_adaptive"][0], Params(), seed=1)
    idle_fixed = run(Scenario("idle", "no bloom", rate_kg_h=0.0001), [p for p in POLICIES if p.name == "hybrid_fixed"][0], Params(), seed=1)
    write_report(out, rows, idle, idle_fixed)
    print("wrote", out)

def get(rows, sc, var, pol):
    return next(r for r in rows if r["scenario"] == sc and r["bubble_assumption"] == var and r["policy"] == pol)

def write_report(out, rows, idle, idle_fixed):
    lab = {p.name: p.label for p in POLICIES}
    L = ["# MARLIN v5 hybrid screening results", "", DISCLAIMER, "",
         f"Each cell: median (10th-90th percentile) of {N} Monte Carlo draws over uncertain parameters, same draws for every policy.",
         "Metric: **% reduction in jellyfish mass reaching the intake entrance versus doing nothing.** Higher is better. "
         "Energy is compressor electricity per event from the v4 estimate scaled by air level.", ""]
    for var, title in (("bubble_effective", "Bubble lift drawn from 0.2-0.8 of non-surface mass at full air"), ("bubble_zero", "Stress case: bubbles give zero lift")):
        L += [f"## {title}", "", "| Scenario | " + " | ".join(lab[p.name] for p in POLICIES[2:]) + " |", "|---|" + "---|" * (len(POLICIES) - 2)]
        for sc in SCENARIOS:
            cells = []
            for p in POLICIES[2:]:
                r = get(rows, sc.name, var, p.name)
                cells.append(f"{r['reduction_median']:.0f} ({r['reduction_p10']:.0f}-{r['reduction_p90']:.0f})")
            L.append(f"| {sc.label} | " + " | ".join(cells) + " |")
        L.append("")
    L += ["## Energy and effort (median per event)", "", "| Scenario | Policy | Air kWh | Air-on hours | Crew hours | Crew-caught kg |", "|---|---|---:|---:|---:|---:|"]
    for sc in SCENARIOS:
        for pn in ("hybrid_fixed", "hybrid_adaptive", "hybrid_adaptive_crew"):
            r = get(rows, sc.name, "bubble_effective", pn)
            L.append(f"| {sc.name} | {lab[pn]} | {r['air_kwh_median']} | {r['air_on_h_median']} | {r['crew_h_median']} | {r['crew_kg_median']} |")
    L += ["", "## Idle check (no bloom)", "",
          f"Adaptive control air use with no bloom: {idle['air_kwh']:.2f} kWh, {idle['air_on_h']:.2f} h on. Fixed schedule: {idle_fixed['air_kwh']:.1f} kWh, {idle_fixed['air_on_h']:.2f} h on.", "",
          "## Honest limits", "",
          "- Parameters are placeholders drawn from stated ranges, not measurements. The model ranks strategies; it does not predict a field catch rate.",
          "- Bubbles act only by lifting animals so the boom can guide them (a bubble line alone is not an exclusion barrier, consistent with Lo 1991). With zero lift they add nothing, and the report shows that case.",
          "- Plan-view only: no CFD, no depth-resolved flow, no intake hydraulics, no bycatch or injury, no vessel dynamics.",
          "- The boom end and collector are assumed to follow a winch-adjusted mooring (1 deg/min limit).",
          "- Sensor is a synthetic noisy flux gate; no trained ML or computer vision runs.",
          "- Mass ledger closes to numerical precision in every run (asserted)."]
    (out / "RUN_REPORT.md").write_text("\n".join(L))

if __name__ == "__main__":
    main()
