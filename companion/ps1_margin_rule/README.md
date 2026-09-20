# PS1 reproducible margin-rule model

This folder contains the synthetic computation for the PS1 research question: how does a fixed versus intermediary-chosen margin affect farmer participation and modeled household purchases as coordination cost K changes?

## Run

Use Python 3.10 or newer. From this folder, run:

```bash
python model.py
```

The command writes `outputs/factorial_2x2.csv`, `outputs/coordination_cost_sensitivity.csv`, `outputs/participation_thresholds.csv`, and `outputs/run_log.txt`. The Colab notebook in `notebooks/PS1_margin_rule_demo.ipynb` is self-contained and uses only the Python standard library.

## Behavioral design and calibration

The planned 2 x 2 vignette randomizes (1) fixed versus intermediary-chosen margin rules and (2) sparse versus verified seller history. Listed price, product identity, quality evidence, quantity, and delivery are held identical in all four cells. Measure purchase choice, trust, perceived price fairness, expected product quality, and willingness to pay. If seller-history information changes perceived price or quality, report that as a competing pathway; do not label the entire response a trust effect.

The model includes a single planned demand shifter, `reputation_lift` (rho_R), applied only to the verified-information condition. It defaults to zero because no behavioral data have been collected. After estimating the treatment effect on purchase probability, map that estimate to rho_R and rerun the same margin-rule comparison. To explore a hypothetical value before data exist, use `python model.py --rho 0.10`; this is an assumption exercise, not an estimate.

## Coordination-cost result

At rho_R = 0, the farmer's participation cutoff is K = 43.2 under the fixed rule and K = 38.4 under the chosen rule. For 38.4 < K <= 43.2, farmers participate only under the fixed rule, so the realized intermediary-profit ranking reverses. At K > 43.2, both rules produce no trade. When both rules are active, the fixed rule yields more modeled completed units and farmer net earnings, while the chosen rule yields more intermediary profit. These are conditional results of the synthetic assumptions, not field findings.

`completed_units` is an access proxy, not observed purchases, household welfare, or consumption inequality. The model does not claim causal or distributional effects.
