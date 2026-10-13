# Update package: MARLIN hybrid strategy (v5)

## What is in this zip
| Path | What |
|---|---|
| `simulation/v5/` | New self-contained hybrid simulation, 15 tests, README |
| `outputs/v5/` | Report, CSV, JSON and chart from the final run |
| `docs/STRATEGY_V5.md` | Strategy, ENEC mapping, findings, honest limits, next steps |
| `deck/MARLIN_Hybrid_Proposal.pptx` and `.pdf` | 10-slide deck for the hybrid concept, Layer 3 labelled, test target made honest |

Nothing in the existing repo is overwritten: v4 is untouched, and the original `MARLIN_ENEC_Proposal.*` stays until you decide which deck to submit.

## Check performed on the existing repo before this update
- `MARLIN_Simulation_v4.zip`: all 27 unit tests pass.
- v4 `run_scenarios.py` **cannot be re-run from the repo**: it needs `data/processed/environment_windows.json` plus ERA5 wind/wave and SMOC current CSVs, which are not committed. Add them (or document where to get them) so others can reproduce the 97.5% result.
- v4's proposal slides depend on that 97.5% synthetic-input result and treat bubbles as optional; the hybrid concept does not match them.

## Push steps
```
git clone https://github.com/AbdulBari357/MARLIN
cd MARLIN
unzip ../MARLIN_hybrid_update_v5.zip -d .
git checkout -b hybrid-v5
git add simulation outputs docs deck UPDATE_NOTES.md
git commit -m "Add v5 hybrid simulation, strategy doc and updated deck"
git push -u origin hybrid-v5      # then open a pull request, or merge to main
```
If you unzip into a folder that already has `simulation/` or `outputs/`, the new `v5` subfolders are added beside the existing `v4` ones.
