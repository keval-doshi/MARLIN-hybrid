# MARLIN v5 - hybrid concept screening model

Models the team strategy: **Layer 1** bubble curtain + **Layer 2** angled floating boom, steered by **adaptive control software**, backed by **Layer 3** manual catch, with the intake screens as the last line.

Illustrative and uncalibrated. It ranks control strategies under the same assumptions. It does not predict field catch rates and never controls equipment. No ML/CV model runs; the controller is a readable rule set.

Self-contained: no external data files are needed (v4 needs an ERA5/SMOC `data/processed/` folder that is not in the repo).

## Run (Python 3.9+, numpy)

```
cd simulation/v5
python test_hybrid.py        # 16 checks, ~10 s
python run_scenarios.py      # 10 scenarios x 2 bubble assumptions x 7 policies x 40 draws, ~6 min on 2 cores
```

Outputs go to `outputs/v5/`: `RUN_REPORT.md`, `scenario_summary.csv`, `results.json`, `results_chart.png`.

## What is modelled
- Plan-view cohorts drift with a prescribed current plus diffusion toward a breakwater wall with a 60 m intake opening.
- The curtain (3 independently switched zones) lifts a share of non-surface mass to the surface; waves reduce lift to zero at Hs 2 m.
- The boom guides the surface share along its face to a collector (escape per metre and per hour; overtopping above Hs 0.8 m). A bubble line alone gives no exclusion; lift only helps the boom.
- Adaptive control: noisy flux gate upstream, zone air 0 / 0.4 / 1.0, 15 min idle-off, fail-safe to full air if sensors go blind, air stopped when waves remove lift, boom follows current direction at 1 deg/min.
- Layer 3 crew sweeps surface mass near the entrance up to a capacity, stood down above Hs 1.5 m.
- Every run asserts that the mass ledger closes.

## Not modelled
CFD, depth-resolved flow, intake hydraulics, bycatch or injury, vessel dynamics, real sensor physics, calibrated bubble lift.
