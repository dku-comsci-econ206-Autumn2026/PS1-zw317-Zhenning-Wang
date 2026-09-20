"""Synthetic margin-rule model with a planned reputation demand shifter.

Outputs remain illustrative until the proposed behavioral study supplies an
estimate of reputation_lift. Standard library only.
"""
from dataclasses import dataclass, asdict
import argparse
import csv
from pathlib import Path


@dataclass(frozen=True)
class Params:
    w: float = 6.0
    c: float = 4.0
    K: float = 12.0
    effort_cost: float = 30.0
    demand_scale: float = 12.0
    choke_margin: float = 4.0
    reputation_lift: float = 0.0


def quantity(m: float, e: float, p: Params, verified: bool = False) -> float:
    """Modeled completed units; verified info applies the assumed lift rho_R."""
    lift = p.reputation_lift if verified else 0.0
    return p.demand_scale * e * max(0.0, p.choke_margin - m) * (1.0 + lift)


def intermediary_profit(m: float, e: float, p: Params, verified: bool = False) -> float:
    return m * quantity(m, e, p, verified) - p.effort_cost * e * e


def optimize_fixed_margin(p: Params, verified: bool = False, fixed_m: float = 1.0):
    candidates = ((intermediary_profit(fixed_m, i / 100, p, verified), fixed_m, i / 100)
                  for i in range(101))
    best = max(candidates, key=lambda x: x[0])
    return best[1], best[2]


def optimize_chosen_margin(p: Params, verified: bool = False):
    # m in [0, 4] by 0.05; effort e in [0, 1] by 0.01.
    candidates = ((intermediary_profit(j * 0.05, i / 100, p, verified), j * 0.05, i / 100)
                  for j in range(81) for i in range(101))
    best = max(candidates, key=lambda x: x[0])
    return best[1], best[2]


def evaluate_rule(rule: str, information: str, p: Params):
    verified = information == "Verified"
    if rule == "Fixed":
        m, e = optimize_fixed_margin(p, verified)
    elif rule == "Chosen":
        m, e = optimize_chosen_margin(p, verified)
    else:
        raise ValueError(f"Unknown rule: {rule}")
    q_if_join = quantity(m, e, p, verified)
    farmer_net_if_join = (p.w - p.c) * q_if_join - p.K
    joins = farmer_net_if_join >= 0
    return {
        "information": information,
        "rule": rule,
        "margin": m,
        "effort": e,
        "completed_units": q_if_join if joins else 0.0,
        "farmer_joins": joins,
        "farmer_net_if_join": farmer_net_if_join,
        "farmer_net": farmer_net_if_join if joins else 0.0,
        "intermediary_profit": intermediary_profit(m, e, p, verified) if joins else 0.0,
        "assumed_reputation_lift": p.reputation_lift,
    }


def run_factorial(K: float = 12.0, reputation_lift: float = 0.0):
    """Two-by-two cells: margin rule x seller-information condition."""
    p = Params(K=K, reputation_lift=reputation_lift)
    return [evaluate_rule(rule, info, p)
            for info in ("Sparse", "Verified")
            for rule in ("Fixed", "Chosen")]


def run_coordination_sensitivity(K_values=range(46), reputation_lift: float = 0.0):
    """Vary K under sparse information, isolating the coordination-cost check."""
    rows = []
    for K in K_values:
        p = Params(K=float(K), reputation_lift=reputation_lift)
        for rule in ("Fixed", "Chosen"):
            row = evaluate_rule(rule, "Sparse", p)
            row["coordination_cost_K"] = K
            rows.append(row)
    return rows


def participation_thresholds():
    """Baseline K cutoffs at which the farmer is just willing to participate."""
    p = Params()
    out = []
    for rule in ("Fixed", "Chosen"):
        m, e = (optimize_fixed_margin(p) if rule == "Fixed" else optimize_chosen_margin(p))
        cutoff = (p.w - p.c) * quantity(m, e, p)
        out.append({"rule": rule, "margin": m, "effort": e,
                    "units_before_participation": quantity(m, e, p),
                    "max_K_for_participation": cutoff})
    return out


def _write_csv(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows([{k: round(v, 4) if isinstance(v, float) else v
                           for k, v in row.items()} for row in rows])


def write_outputs(directory="outputs", reputation_lift: float = 0.0):
    out = Path(directory)
    factorial = run_factorial(reputation_lift=reputation_lift)
    sensitivity = run_coordination_sensitivity(reputation_lift=reputation_lift)
    thresholds = participation_thresholds()
    _write_csv(out / "factorial_2x2.csv", factorial)
    _write_csv(out / "coordination_cost_sensitivity.csv", sensitivity)
    _write_csv(out / "participation_thresholds.csv", thresholds)
    with (out / "run_log.txt").open("w", encoding="utf-8") as f:
        f.write("Standard-library model run; outputs are synthetic, not field evidence.\n")
        f.write(f"Assumed reputation demand lift rho_R: {reputation_lift:.4f}\n")
        f.write("Factorial cells vary margin rule and seller information; sparse cells use rho_R=0.\n")
        f.write("Price, product-quality evidence, and delivery are held fixed in the proposed experiment.\n")
        f.write("Baseline farmer participation thresholds (K): Fixed 43.2; Chosen 38.4.\n")
        f.write("Change rho_R only after estimating it from the planned behavioral study.\n")
    return factorial, sensitivity, thresholds


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rho", type=float, default=0.0,
                        help="assumed verified-information demand lift; default 0 until estimated")
    parser.add_argument("--output", default="outputs", help="directory for generated CSV files")
    args = parser.parse_args()
    factorial, sensitivity, thresholds = write_outputs(args.output, args.rho)
    for row in factorial:
        print({k: (round(v, 2) if isinstance(v, float) else v) for k, v in row.items()})
    print("Participation cutoffs:", thresholds)
    print("K sensitivity rows:", len(sensitivity))
