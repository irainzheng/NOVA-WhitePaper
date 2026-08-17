#!/usr/bin/env python3
"""
NOVA macro simulation — whitepaper 21.7 / 21.8
V1.5.0 · runnable without Jupyter

Usage:
  pip install pyyaml matplotlib
  python nova_macro.py
  python nova_macro.py --params params/baseline_v1.5.yaml --years 20
"""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    import yaml
except ImportError as e:
    raise SystemExit("Install PyYAML: pip install pyyaml") from e

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


def load_params(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def simulate(params: dict, years: int = 20) -> dict:
    """Simplified NPT circulation + immortality revenue model."""
    npt = params["npt"]
    agents = params["agents"]
    compute = params["compute"]
    imm = params["immortality_subscription"]

    daily_cap = npt["daily_earn_cap_per_user"]
    destroy_rate = npt["consume_destroy_rate_median"]
    dau = {
        0: agents["dau_growth"]["phase0_end"] // 2,
        1: agents["dau_growth"]["phase0_end"],
        2: agents["dau_growth"]["phase1_end"],
        3: agents["dau_growth"]["phase2_end"],
    }
    contrib = agents["contributor_ratio"]

    months = years * 12
    rows = []
    supply = 0.0
    revenue_usd = 0.0

    for m in range(1, months + 1):
        phase = 0 if m <= 12 else (1 if m <= 36 else (2 if m <= 84 else 3))
        dau_m = dau.get(phase, dau[3])
        # linear interpolate within phase for smoother curve
        if phase == 0:
            dau_m = int(dau[0] + (dau[1] - dau[0]) * m / 12)
        elif phase == 1:
            dau_m = int(dau[1] + (dau[2] - dau[1]) * (m - 12) / 24)
        elif phase == 2:
            dau_m = int(dau[2] + (dau[3] - dau[2]) * (m - 36) / 48)

        cr = contrib[f"phase{phase}"]
        earn = dau_m * cr * daily_cap * 30
        destroy = supply * destroy_rate * 0.02  # monthly consumption fraction
        supply = max(0, supply + earn - destroy)

        pen = imm["penetration_neutral"] if m < 120 else imm["penetration_optimistic"]
        rev = dau_m * pen * imm["arpu_usd_neutral"] / 12
        revenue_usd += rev

        compute_cost = rev * (0.55 if phase <= 1 else 0.45)  # scissors gap early
        gamma = compute_cost / rev if rev > 0 else 1.0

        rows.append(
            {
                "month": m,
                "phase": phase,
                "dau": dau_m,
                "npt_supply": round(supply, 0),
                "revenue_usd": round(rev, 0),
                "gamma": round(gamma, 3),
                "gamma_alert": gamma > compute["gamma_phase0_target"],
            }
        )

    return {
        "rows": rows,
        "summary": {
            "years": years,
            "final_npt_supply": rows[-1]["npt_supply"],
            "cumulative_revenue_usd": round(revenue_usd, 0),
            "months_gamma_above_target": sum(1 for r in rows if r["gamma_alert"]),
            "gamma_red_line_breaches": sum(
                1 for r in rows if r["gamma"] > compute["gamma_red_line"] + 0.1
            ),
        },
    }


def print_summary(result: dict) -> None:
    s = result["summary"]
    print("=== NOVA Macro Simulation Summary ===")
    print(f"Horizon: {s['years']} years")
    print(f"Final NPT supply (model): {s['final_npt_supply']:,.0f}")
    print(f"Cumulative revenue USD: ${s['cumulative_revenue_usd']:,.0f}")
    print(f"Months gamma > phase0 target: {s['months_gamma_above_target']}")
    print(f"Months gamma > red line +10%: {s['gamma_red_line_breaches']}")
    print("\nLast 5 months:")
    for r in result["rows"][-5:]:
        print(
            f"  M{r['month']:3d} phase={r['phase']} DAU={r['dau']:7,d} "
            f"NPT={r['npt_supply']:12,.0f} rev=${r['revenue_usd']:10,.0f} γ={r['gamma']:.2f}"
        )


def plot(result: dict, out: Path) -> None:
    if plt is None:
        print("matplotlib not installed — skip chart")
        return
    rows = result["rows"]
    months = [r["month"] for r in rows]
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle("NOVA Macro Simulation (V1.5 baseline)")

    axes[0, 0].plot(months, [r["dau"] for r in rows])
    axes[0, 0].set_title("DAU")
    axes[0, 0].set_xlabel("Month")

    axes[0, 1].plot(months, [r["npt_supply"] for r in rows])
    axes[0, 1].set_title("NPT Supply")
    axes[0, 1].set_xlabel("Month")

    axes[1, 0].plot(months, [r["revenue_usd"] for r in rows])
    axes[1, 0].set_title("Monthly Revenue (USD)")
    axes[1, 0].set_xlabel("Month")

    axes[1, 1].plot(months, [r["gamma"] for r in rows])
    axes[1, 1].axhline(0.5, color="orange", linestyle="--", label="phase0 target")
    axes[1, 1].axhline(0.4, color="red", linestyle="--", label="red line")
    axes[1, 1].set_title("Compute γ (cost/revenue)")
    axes[1, 1].legend()
    axes[1, 1].set_xlabel("Month")

    plt.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out, dpi=120)
    print(f"Chart saved: {out}")


def main() -> None:
    parser = argparse.ArgumentParser(description="NOVA macro simulation")
    parser.add_argument(
        "--params",
        type=Path,
        default=Path(__file__).parent / "params" / "baseline_v1.5.yaml",
    )
    parser.add_argument("--years", type=int, default=20)
    parser.add_argument("--chart", type=Path, default=Path(__file__).parent / "output" / "macro_v1.5.png")
    args = parser.parse_args()

    params = load_params(args.params)
    result = simulate(params, years=args.years)
    print_summary(result)
    plot(result, args.chart)


if __name__ == "__main__":
    main()
