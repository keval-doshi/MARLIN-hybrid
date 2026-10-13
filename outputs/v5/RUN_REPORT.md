# MARLIN v5 hybrid screening results

MARLIN v5: illustrative plan-view screening model with uncalibrated parameters. Use for comparing strategies, not for predicting field catch rates.

Each cell: median (10th-90th percentile) of 40 Monte Carlo draws over uncertain parameters, same draws for every policy.
Metric: **% reduction in jellyfish mass reaching the intake entrance versus doing nothing.** Higher is better. Energy is compressor electricity per event from the v4 estimate scaled by air level.

## Bubble lift drawn from 0.2-0.8 of non-surface mass at full air

| Scenario | Angled boom only, fixed angle | Bubble + boom, fixed full air, fixed angle | Bubble + boom, adaptive control | Adaptive + manual-catch layer 3 | Fixed + manual-catch layer 3 |
|---|---|---|---|---|---|
| Calm reference (1200 kg/h, 4 h) | 32 (20-40) | 46 (34-56) | 44 (32-52) | 60 (45-70) | 66 (49-77) |
| Storm: Hs 2 m (curtain loses lift, boom overtopped, crew stood down) | 11 (8-15) | 11 (8-15) | 11 (5-18) | 11 (5-18) | 11 (5-18) |
| Moderate sea: Hs 1.2 m | 19 (12-29) | 26 (18-35) | 25 (11-35) | 47 (31-61) | 51 (34-65) |
| Triple bloom load (3600 kg/h) | 26 (16-41) | 44 (35-59) | 43 (34-62) | 58 (49-76) | 58 (49-76) |
| Current direction rotates +30 deg after hour 2 | 21 (13-27) | 32 (25-41) | 30 (22-43) | 58 (47-72) | 66 (51-80) |
| Current direction rotates -30 deg after hour 2 | 29 (16-40) | 49 (32-57) | 46 (30-53) | 61 (42-71) | 67 (47-76) |
| Bloom arrives only on one side (y -150..-20) | 24 (16-35) | 42 (28-49) | 33 (20-46) | 50 (39-64) | 66 (51-77) |
| Collector down for 2 h (hours 1-3) | 30 (18-41) | 48 (33-57) | 43 (27-54) | 58 (40-73) | 66 (47-78) |
| Sensors blind (adaptive falls back to fail-safe full air) | 27 (18-38) | 46 (34-56) | 46 (34-56) | 64 (49-73) | 64 (49-73) |
| Weak current 0.05 m/s | 23 (11-32) | 34 (21-44) | 30 (21-44) | 57 (40-71) | 64 (48-76) |

## Stress case: bubbles give zero lift

| Scenario | Angled boom only, fixed angle | Bubble + boom, fixed full air, fixed angle | Bubble + boom, adaptive control | Adaptive + manual-catch layer 3 | Fixed + manual-catch layer 3 |
|---|---|---|---|---|---|
| Calm reference (1200 kg/h, 4 h) | 28 (18-38) | 28 (18-38) | 28 (15-40) | 40 (24-56) | 40 (24-56) |
| Storm: Hs 2 m (curtain loses lift, boom overtopped, crew stood down) | 11 (7-16) | 11 (7-16) | 11 (1-18) | 11 (1-18) | 11 (1-18) |
| Moderate sea: Hs 1.2 m | 18 (14-27) | 18 (14-27) | 18 (9-30) | 37 (23-52) | 37 (23-52) |
| Triple bloom load (3600 kg/h) | 28 (18-36) | 28 (18-36) | 28 (18-40) | 37 (26-51) | 37 (26-51) |
| Current direction rotates +30 deg after hour 2 | 19 (12-27) | 19 (12-27) | 21 (9-29) | 38 (24-54) | 38 (24-54) |
| Current direction rotates -30 deg after hour 2 | 25 (16-37) | 25 (16-37) | 25 (14-45) | 34 (19-58) | 34 (19-58) |
| Bloom arrives only on one side (y -150..-20) | 23 (14-35) | 23 (14-35) | 22 (15-41) | 37 (24-57) | 37 (24-57) |
| Collector down for 2 h (hours 1-3) | 28 (16-38) | 28 (16-38) | 26 (20-38) | 40 (26-52) | 40 (26-52) |
| Sensors blind (adaptive falls back to fail-safe full air) | 29 (17-41) | 29 (17-41) | 29 (17-41) | 38 (26-54) | 38 (26-54) |
| Weak current 0.05 m/s | 22 (13-32) | 22 (13-32) | 22 (13-34) | 40 (29-54) | 40 (29-54) |

## Energy and effort (median per event)

| Scenario | Policy | Air kWh | Air-on hours | Crew hours | Crew-caught kg |
|---|---|---:|---:|---:|---:|
| calm | Bubble + boom, fixed full air, fixed angle | 24.0 | 5.0 | 0.0 | 0.0 |
| calm | Bubble + boom, adaptive control | 14.8 | 4.42 | 0.0 | 0.0 |
| calm | Adaptive + manual-catch layer 3 | 14.8 | 4.42 | 5.5 | 335.3 |
| storm | Bubble + boom, fixed full air, fixed angle | 24.0 | 5.0 | 0.0 | 0.0 |
| storm | Bubble + boom, adaptive control | 0.0 | 0.0 | 0.0 | 0.0 |
| storm | Adaptive + manual-catch layer 3 | 0.0 | 0.0 | 0.0 | 0.0 |
| moderate_sea | Bubble + boom, fixed full air, fixed angle | 24.0 | 5.0 | 0.0 | 0.0 |
| moderate_sea | Bubble + boom, adaptive control | 14.8 | 4.42 | 0.0 | 0.0 |
| moderate_sea | Adaptive + manual-catch layer 3 | 14.8 | 4.42 | 5.5 | 412.9 |
| triple | Bubble + boom, fixed full air, fixed angle | 24.0 | 5.0 | 0.0 | 0.0 |
| triple | Bubble + boom, adaptive control | 20.6 | 4.58 | 0.0 | 0.0 |
| triple | Adaptive + manual-catch layer 3 | 20.6 | 4.58 | 5.5 | 944.2 |
| current_shift | Bubble + boom, fixed full air, fixed angle | 24.0 | 5.0 | 0.0 | 0.0 |
| current_shift | Bubble + boom, adaptive control | 14.4 | 4.42 | 0.0 | 0.0 |
| current_shift | Adaptive + manual-catch layer 3 | 14.4 | 4.42 | 5.5 | 418.7 |
| current_shift_neg | Bubble + boom, fixed full air, fixed angle | 24.0 | 5.0 | 0.0 | 0.0 |
| current_shift_neg | Bubble + boom, adaptive control | 14.4 | 4.42 | 0.0 | 0.0 |
| current_shift_neg | Adaptive + manual-catch layer 3 | 14.4 | 4.42 | 5.5 | 299.3 |
| one_sided | Bubble + boom, fixed full air, fixed angle | 24.0 | 5.0 | 0.0 | 0.0 |
| one_sided | Bubble + boom, adaptive control | 9.7 | 4.5 | 0.0 | 0.0 |
| one_sided | Adaptive + manual-catch layer 3 | 9.7 | 4.5 | 5.5 | 409.6 |
| collector_out | Bubble + boom, fixed full air, fixed angle | 24.0 | 5.0 | 0.0 | 0.0 |
| collector_out | Bubble + boom, adaptive control | 14.9 | 4.42 | 0.0 | 0.0 |
| collector_out | Adaptive + manual-catch layer 3 | 14.9 | 4.42 | 5.5 | 361.4 |
| sensor_blind | Bubble + boom, fixed full air, fixed angle | 24.0 | 5.0 | 0.0 | 0.0 |
| sensor_blind | Bubble + boom, adaptive control | 21.6 | 4.5 | 0.0 | 0.0 |
| sensor_blind | Adaptive + manual-catch layer 3 | 21.6 | 4.5 | 5.5 | 357.9 |
| weak_current | Bubble + boom, fixed full air, fixed angle | 24.0 | 5.0 | 0.0 | 0.0 |
| weak_current | Bubble + boom, adaptive control | 14.9 | 4.42 | 0.0 | 0.0 |
| weak_current | Adaptive + manual-catch layer 3 | 14.9 | 4.42 | 5.5 | 486.1 |

## Idle check (no bloom)

Adaptive control air use with no bloom: 0.00 kWh, 0.00 h on. Fixed schedule: 24.0 kWh, 5.00 h on.

## Honest limits

- Parameters are placeholders drawn from stated ranges, not measurements. The model ranks strategies; it does not predict a field catch rate.
- Bubbles act only by lifting animals so the boom can guide them (a bubble line alone is not an exclusion barrier, consistent with Lo 1991). With zero lift they add nothing, and the report shows that case.
- Plan-view only: no CFD, no depth-resolved flow, no intake hydraulics, no bycatch or injury, no vessel dynamics.
- The boom end and collector are assumed to follow a winch-adjusted mooring (1 deg/min limit).
- Sensor is a synthetic noisy flux gate; no trained ML or computer vision runs.
- Mass ledger closes to numerical precision in every run (asserted).