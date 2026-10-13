# MARLIN strategy update (v5)

## The concept
Post-alert response to jellyfish blooms for the ENEC challenge, in four parts:
1. **Layer 1 - bubble curtain** lifts drifting jellyfish toward the surface.
2. **Layer 2 - angled floating boom** guides the lifted jellyfish along its face to one collector.
3. **Adaptive control software** estimates arrivals and sets curtain air per zone and the boom angle; it switches off when nothing arrives.
4. **Layer 3 - manual catch** is a small crew for rare stragglers.
The existing intake screens stay untouched as the last line. Nothing in the concept alters plant or nuclear-safety systems, which the brief excludes.

## Why this concept (against the ENEC weights)
| Criterion | Weight | Where MARLIN is strong |
|---|---|---|
| Feasibility and practicality | 25% | Off-the-shelf parts, modular, no deep-water netting |
| Challenge relevance | 20% | Post-alert only, less manual work |
| Innovation | 20% | Adaptive control of a smart barrier ("Smart Barrier and Deflection", "Decision Support" areas in the brief) |
| Sustainability and marine-life protection | 20% | Guides rather than traps; air off when idle |
| Communication and evidence | 15% | Field and flume literature plus the v5 simulation with stated limits |

## What the v5 simulation found (read before presenting)
Source: `outputs/v5/RUN_REPORT.md`. 40 Monte Carlo draws per cell, same draws for every strategy. Metric: % less jellyfish mass reaching the intake entrance than doing nothing.

- **Bubbles + boom beat the boom alone** when bubbles can lift animals: calm 52% vs 36%. If bubbles give zero lift, they add nothing (both 31%). The bubble curtain only helps because it feeds the boom.
- **Layer 3 (manual catch) adds about 11-19 points** in calm and moderate seas (calm: 49% adaptive -> 60% with crew; Hs 1.2 m: 28% -> 47%).
- **Adaptive control saves air energy, not catch.** Calm: 14.8 kWh vs 24.0 kWh for a fixed schedule (about 38% less), zero kWh with no bloom, and 0 kWh in a 2 m storm. But adaptive did not beat fixed settings on catch (calm 49% vs 52%), and in the one-sided-bloom case it was worse (39% vs 50%) because the zone thresholds under-react to noisy sensors.
- **Adaptive boom angle did not help** in the rotating-current case (34% vs 36% fixed). In this geometry a fixed boom still intercepts most of the flow. The claim "changing the boom direction improves catch" is **not supported yet**.
- **Storms defeat everything**: about 12% in a 2 m sea for every strategy (curtain loses lift, boom overtopped, crew stood down). The operations plan must say so.
- **Absolute numbers are modest** (roughly 50-65% in calm seas). Do not present them as expected field performance; they are placeholders from stated ranges. The v4 repo headline of 97.5% captured should not appear next to them.

## How to present it honestly
- Say the software's proven benefit is **less energy, less disturbance, and a safe fail-state**; present catch improvement as a hypothesis for the flume.
- Say bubbles are **conditional**: they help when waves are low and only through the boom.
- Show the stress table (storm, triple load, blind sensors, collector outage) as evidence that the team knows where the system fails.

## Next steps
1. Tune zone thresholds and test an arrival-forecast controller (fixes the one-sided case).
2. Test a boom with a movable pivot or a second boom section to see if direction control then helps.
3. Replace placeholder ranges with flume data (bubble lift versus airflow and Hs; boom escape per metre).
4. Add a bycatch/injury proxy so marine-life protection can be compared, not just asserted.
5. Reconcile the proposal deck in the repo with this concept (see UPDATE_NOTES.md).
