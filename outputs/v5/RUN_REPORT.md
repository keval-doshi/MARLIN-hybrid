# MARLIN v5 hybrid screening results

MARLIN v5: illustrative plan-view screening model with uncalibrated parameters. Use for comparing strategies, not for predicting field catch rates.

Each cell: median (10th-90th percentile) of 40 Monte Carlo draws over uncertain parameters, same draws for every policy.
Metric: **% reduction in jellyfish mass reaching the intake entrance versus doing nothing.** Higher is better. Energy is compressor electricity per event from the v4 estimate scaled by air level.

## Bubble lift drawn from 0.2-0.8 of non-surface mass at full air

| Scenario | Angled boom only, fixed angle | Bubble + boom, fixed full air, fixed angle | Bubble + boom, adaptive control | Adaptive + manual-catch layer 3 | Fixed + manual-catch layer 3 |
|---|---|---|---|---|---|
| Calm reference (1200 kg/h, 4 h) | 36 (22-43) | 52 (40-62) | 49 (36-56) | 60 (45-70) | 66 (49-77) |
| Storm: Hs 2 m (curtain loses lift, boom overtopped, crew stood down) | 12 (8-17) | 12 (8-17) | 12 (6-20) | 12 (6-20) | 12 (6-20) |
| Moderate sea: Hs 1.2 m | 21 (14-33) | 29 (21-38) | 28 (14-38) | 47 (31-63) | 51 (34-65) |
| Triple bloom load (3600 kg/h) | 28 (18-46) | 50 (39-64) | 49 (39-67) | 61 (49-79) | 61 (49-79) |
| Current direction rotates +30 deg after hour 2 | 24 (15-30) | 36 (29-45) | 34 (26-48) | 58 (47-72) | 66 (51-80) |
| Current direction rotates -30 deg after hour 2 | 32 (18-43) | 52 (37-61) | 50 (32-56) | 61 (42-71) | 67 (47-76) |
| Bloom arrives only on one side (y -150..-20) | 28 (20-42) | 50 (34-58) | 39 (25-51) | 50 (39-64) | 67 (51-78) |
| Collector down for 2 h (hours 1-3) | 33 (20-46) | 53 (38-64) | 47 (30-59) | 58 (40-73) | 66 (47-78) |
| Sensors blind (adaptive falls back to fail-safe full air) | 30 (21-43) | 52 (38-60) | 52 (38-60) | 64 (49-73) | 64 (49-73) |
| Weak current 0.05 m/s | 28 (15-38) | 43 (28-53) | 38 (27-50) | 57 (40-71) | 64 (48-76) |

## Stress case: bubbles give zero lift

| Scenario | Angled boom only, fixed angle | Bubble + boom, fixed full air, fixed angle | Bubble + boom, adaptive control | Adaptive + manual-catch layer 3 | Fixed + manual-catch layer 3 |
|---|---|---|---|---|---|
| Calm reference (1200 kg/h, 4 h) | 31 (20-42) | 31 (20-42) | 31 (19-42) | 40 (24-56) | 40 (24-56) |
| Storm: Hs 2 m (curtain loses lift, boom overtopped, crew stood down) | 12 (8-17) | 12 (8-17) | 13 (2-20) | 13 (2-20) | 13 (2-20) |
| Moderate sea: Hs 1.2 m | 20 (15-29) | 20 (15-29) | 20 (11-32) | 37 (23-52) | 37 (23-52) |
| Triple bloom load (3600 kg/h) | 31 (20-41) | 31 (20-41) | 32 (21-43) | 38 (26-51) | 38 (26-51) |
| Current direction rotates +30 deg after hour 2 | 21 (13-31) | 21 (13-31) | 22 (12-32) | 38 (24-54) | 38 (24-55) |
| Current direction rotates -30 deg after hour 2 | 27 (17-41) | 27 (17-41) | 27 (15-47) | 34 (19-58) | 34 (19-58) |
| Bloom arrives only on one side (y -150..-20) | 26 (17-41) | 26 (17-41) | 26 (18-47) | 37 (24-57) | 37 (24-57) |
| Collector down for 2 h (hours 1-3) | 31 (19-43) | 31 (19-43) | 30 (22-42) | 40 (26-52) | 40 (26-52) |
| Sensors blind (adaptive falls back to fail-safe full air) | 31 (19-45) | 31 (19-45) | 31 (19-45) | 38 (26-54) | 38 (26-54) |
| Weak current 0.05 m/s | 27 (17-38) | 27 (17-38) | 27 (19-39) | 40 (29-54) | 40 (29-54) |

## Energy and effort (median per event)

| Scenario | Policy | Air kWh | Air-on hours | Crew hours | Crew-caught kg |
|---|---|---:|---:|---:|---:|
| calm | Bubble + boom, fixed full air, fixed angle | 24.0 | 5.0 | 0.0 | 0.0 |
| calm | Bubble + boom, adaptive control | 14.8 | 4.42 | 0.0 | 0.0 |
| calm | Adaptive + manual-catch layer 3 | 14.8 | 4.42 | 5.5 | 281.8 |
| storm | Bubble + boom, fixed full air, fixed angle | 24.0 | 5.0 | 0.0 | 0.0 |
| storm | Bubble + boom, adaptive control | 0.0 | 0.0 | 0.0 | 0.0 |
| storm | Adaptive + manual-catch layer 3 | 0.0 | 0.0 | 0.0 | 0.0 |
| moderate_sea | Bubble + boom, fixed full air, fixed angle | 24.0 | 5.0 | 0.0 | 0.0 |
| moderate_sea | Bubble + boom, adaptive control | 14.8 | 4.42 | 0.0 | 0.0 |
| moderate_sea | Adaptive + manual-catch layer 3 | 14.8 | 4.42 | 5.5 | 379.5 |
| triple | Bubble + boom, fixed full air, fixed angle | 24.0 | 5.0 | 0.0 | 0.0 |
| triple | Bubble + boom, adaptive control | 20.6 | 4.58 | 0.0 | 0.0 |
| triple | Adaptive + manual-catch layer 3 | 20.6 | 4.58 | 5.5 | 809.5 |
| current_shift | Bubble + boom, fixed full air, fixed angle | 24.0 | 5.0 | 0.0 | 0.0 |
| current_shift | Bubble + boom, adaptive control | 14.4 | 4.42 | 0.0 | 0.0 |
| current_shift | Adaptive + manual-catch layer 3 | 14.4 | 4.42 | 5.5 | 360.8 |
| current_shift_neg | Bubble + boom, fixed full air, fixed angle | 24.0 | 5.0 | 0.0 | 0.0 |
| current_shift_neg | Bubble + boom, adaptive control | 14.4 | 4.42 | 0.0 | 0.0 |
| current_shift_neg | Adaptive + manual-catch layer 3 | 14.4 | 4.42 | 5.5 | 259.3 |
| one_sided | Bubble + boom, fixed full air, fixed angle | 24.0 | 5.0 | 0.0 | 0.0 |
| one_sided | Bubble + boom, adaptive control | 9.7 | 4.5 | 0.0 | 0.0 |
| one_sided | Adaptive + manual-catch layer 3 | 9.7 | 4.5 | 5.5 | 369.6 |
| collector_out | Bubble + boom, fixed full air, fixed angle | 24.0 | 5.0 | 0.0 | 0.0 |
| collector_out | Bubble + boom, adaptive control | 14.9 | 4.42 | 0.0 | 0.0 |
| collector_out | Adaptive + manual-catch layer 3 | 14.9 | 4.42 | 5.5 | 294.5 |
| sensor_blind | Bubble + boom, fixed full air, fixed angle | 24.0 | 5.0 | 0.0 | 0.0 |
| sensor_blind | Bubble + boom, adaptive control | 21.6 | 4.5 | 0.0 | 0.0 |
| sensor_blind | Adaptive + manual-catch layer 3 | 21.6 | 4.5 | 5.5 | 294.3 |
| weak_current | Bubble + boom, fixed full air, fixed angle | 24.0 | 5.0 | 0.0 | 0.0 |
| weak_current | Bubble + boom, adaptive control | 14.9 | 4.42 | 0.0 | 0.0 |
| weak_current | Adaptive + manual-catch layer 3 | 14.9 | 4.42 | 5.5 | 392.8 |

## Idle check (no bloom)

Adaptive control air use with no bloom: 0.00 kWh, 0.00 h on. Fixed schedule: 24.0 kWh, 5.00 h on.

## Honest limits

- Parameters are placeholders drawn from stated ranges, not measurements. The model ranks strategies; it does not predict a field catch rate.
- Bubbles act only by lifting animals so the boom can guide them (a bubble line alone is not an exclusion barrier, consistent with Lo 1991). With zero lift they add nothing, and the report shows that case.
- Plan-view only: no CFD, no depth-resolved flow, no intake hydraulics, no bycatch or injury, no vessel dynamics.
- The boom end and collector are assumed to follow a winch-adjusted mooring (1 deg/min limit).
- Sensor is a synthetic noisy flux gate; no trained ML or computer vision runs.
- Mass ledger closes to numerical precision in every run (asserted).