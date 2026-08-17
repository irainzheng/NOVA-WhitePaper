#!/usr/bin/env python3
"""
NOVA Monte Carlo stress test — whitepaper 21.9
V1.6.0

Usage:
  pip install pyyaml numpy
  python monte_carlo.py
  python monte_carlo.py --sims 10000 --years 20
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

try:
    import yaml
except ImportError as e:
    raise SystemExit("Install PyYAML: pip install pyyaml") from e

try:
    import numpy as np
except ImportError:
    np = None  # type: ignore


def load_params(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_single(params: dict, years: int, rng: random.Random) -> dict:
    """One stochastic draw; returns stress metrics."""
    mc = params["monte_carlo"]
    npt = params["npt"]
    agents = params["agents"]
    compute = params["compute"]
    imm = params["immortality_subscription"]

    pi = rng.uniform(mc["penetration_min"], mc["penetration_max"])
    arpu = max(50, rng.gauss(mc["arpu_mean"], mc["arpu_std"]))
    cost_ratio = rng.uniform(mc["compute_cost_ratio_min"], mc["compute_cost_ratio_max"])
    dau_mult = rng.lognormvariate(mc["dau_log_mu"], mc["dau_log_sigma"])

    daily_cap = npt["daily_earn_cap_per_user"]
    destroy_rate = npt["consume_destroy_rate_median"]

    months = years * 12
    supply = 0.0
    cumulative_rev = 0.0
    cumulative_cost = 0.0
    gamma_high_streak = 0
    max_gamma_streak = 0
    deficit = False

    dau_end = {
        0: agents["dau_growth"]["phase0_end"],
        1: agents["dau_growth"]["phase1_end"],
        2: agents["dau_growth"]["phase2_end"],
        3: int(agents["dau_growth"]["phase2_end"] * dau_mult),
    }

    for m in range(1, months + 1):
        phase = 0 if m <= 12 else (1 if m <= 36 else (2 if m <= 84 else 3))
        base = dau_end.get(min(phase, 2), dau_end[3])
        if phase == 3:
            dau_m = int(dau_end[3] * (m / months))
        elif phase == 0:
            dau_m = int(dau_end[0] * m / 12)
        elif phase == 1:
            dau_m = int(dau_end[0] + (dau_end[1] - dau_end[0]) * (m - 12) / 24)
        else:
            dau_m = int(dau_end[1] + (dau_end[2] - dau_end[1]) * (m - 36) / 48)

        cr = agents["contributor_ratio"][f"phase{min(phase, 3)}"]
        earn = dau_m * cr * daily_cap * 30
        destroy = supply * destroy_rate * 0.02
        supply = max(0, supply + earn - destroy)

        rev = dau_m * pi * arpu / 12
        cost = rev * cost_ratio if rev > 0 else 0
        cumulative_rev += rev
        cumulative_cost += cost

        gamma = cost / rev if rev > 0 else 1.0
        if gamma > compute["gamma_phase0_target"]:
            gamma_high_streak += 1
            max_gamma_streak = max(max_gamma_streak, gamma_high_streak)
        else:
            gamma_high_streak = 0

    if cumulative_cost > cumulative_rev:
        deficit = True

    return {
        "max_gamma_streak_months": max_gamma_streak,
        "cumulative_deficit": deficit,
        "final_pi": pi,
        "final_arpu": arpu,
    }


def run_monte_carlo(params: dict, sims: int, years: int, seed: int | None) -> dict:
    rng = random.Random(seed)
    results = [run_single(params, years, rng) for _ in range(sims)]

    streaks = [r["max_gamma_streak_months"] for r in results]
    deficits = [r["cumulative_deficit"] for r in results]

    p_gamma_12 = sum(1 for s in streaks if s >= 12) / sims
    p_deficit = sum(1 for d in deficits if d) / sims

    thresholds = params["monte_carlo"]["alert_thresholds"]
    alert = "green"
    if p_gamma_12 > thresholds["orange_gamma_streak_12m"]:
        alert = "red"
    elif p_gamma_12 > thresholds["yellow_gamma_streak_12m"]:
        alert = "orange"
    elif p_gamma_12 > thresholds["yellow_gamma_streak_12m"] * 0.8:
        alert = "yellow"

    if p_deficit > thresholds["red_cumulative_deficit"]:
        alert = "red"
    elif p_deficit > thresholds.get("orange_cumulative_deficit", 0.25) and alert in ("green", "yellow"):
        alert = "orange"

    return {
        "simulations": sims,
        "years": years,
        "p_gamma_streak_ge_12m": round(p_gamma_12, 4),
        "p_cumulative_deficit": round(p_deficit, 4),
        "alert_level": alert,
        "sample_draws": results[:5],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="NOVA Monte Carlo stress test")
    parser.add_argument(
        "--params",
        type=Path,
        default=Path(__file__).parent / "params" / "baseline_v1.6.yaml",
    )
    parser.add_argument("--sims", type=int, default=10000)
    parser.add_argument("--years", type=int, default=20)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).parent / "output" / "monte_carlo_v1.6.json",
    )
    args = parser.parse_args()

    params = load_params(args.params)
    result = run_monte_carlo(params, args.sims, args.years, args.seed)

    print("=== NOVA Monte Carlo Stress Test ===")
    print(f"Simulations: {result['simulations']:,} · Horizon: {result['years']} years")
    print(f"P(γ > 50% streak ≥ 12M): {result['p_gamma_streak_ge_12m']:.1%}")
    print(f"P(cumulative cost > revenue): {result['p_cumulative_deficit']:.1%}")
    print(f"Alert level (MC-01): {result['alert_level'].upper()}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"Report saved: {args.out}")


if __name__ == "__main__":
    main()
