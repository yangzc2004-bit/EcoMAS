"""Baseline 实验：Rule Agent 多种子跑批 + 鲁棒性扰动（设计文档第 9、10 节）。

运行：

    python -m experiments.baseline

每个种子跑 200 步，第 100 步施加食物搬移扰动，输出 mean ± std。
"""

import random
import statistics

from agents.ant import Ant
from decision.rule_policy import RulePolicy
from environment.world import World
from metrics.collective import ROLES, collective_metrics
from metrics.individual import individual_metrics
from metrics.robustness import robustness_metrics
from simulation.simulator import Simulator

N_SEEDS = 10
N_ANTS = 20
STEPS = 200
PERTURB_AT = 100


def run_once(seed):
    rng = random.Random(seed)
    world = World(width=40, height=20, n_foods=5, rng=rng)
    ants = [Ant(ant_id=i + 1, position=world.nest) for i in range(N_ANTS)]
    simulator = Simulator(world, ants, RulePolicy(rng=rng))
    simulator.run(STEPS, perturb_at=PERTURB_AT, verbose=False)

    individual = individual_metrics(world.history, ants, STEPS)
    collective = collective_metrics(world.history, world, STEPS)
    robustness = robustness_metrics(world.history, PERTURB_AT, STEPS)
    return {
        "survival_rate": individual["survival_rate"],
        "mean_energy": individual["mean_energy"],
        "contribution_gini": individual["contribution_gini"],
        "throughput": collective["throughput"],
        "division_of_labor": collective["division_of_labor"],
        "role_distribution": collective["role_distribution"],
        "recovery_time": robustness["recovery_time"],
        "pre_rate": robustness["pre_rate"],
        "post_rate": robustness["post_rate"],
    }


def mean_std(values):
    if len(values) < 2:
        return (values[0] if values else 0.0), 0.0
    return statistics.mean(values), statistics.stdev(values)


def main():
    results = [run_once(seed) for seed in range(N_SEEDS)]

    print(f"=== Baseline (RulePolicy) | {N_SEEDS} seeds x {STEPS} steps, "
          f"perturb at {PERTURB_AT} ===")
    print()

    print("Individual:")
    for key, label in [("survival_rate", "survival rate"),
                       ("mean_energy", "mean energy"),
                       ("contribution_gini", "contribution gini")]:
        m, s = mean_std([r[key] for r in results])
        print(f"  {label:20s}: {m:.3f} ± {s:.3f}")
    print()

    print("Collective:")
    m, s = mean_std([r["throughput"] for r in results])
    print(f"  {'throughput (food/step)':20s}: {m:.3f} ± {s:.3f}")
    m, s = mean_std([r["division_of_labor"] for r in results])
    print(f"  {'division of labor':20s}: {m:.3f} ± {s:.3f}")
    dist = "  role distribution     : "
    dist += ", ".join(
        f"{role} {statistics.mean(r['role_distribution'][role] for r in results):.2f}"
        for role in ROLES
    )
    print(dist)
    print()

    print("Robustness:")
    recovered = [r["recovery_time"] for r in results if r["recovery_time"] is not None]
    if recovered:
        m, s = mean_std(recovered)
        print(f"  {'recovery time':20s}: {m:.1f} ± {s:.1f} steps "
              f"(recovered {len(recovered)}/{len(results)} runs)")
    else:
        print("  recovery time        : never recovered")
    for key, label in [("pre_rate", "rate pre-perturb"), ("post_rate", "rate post-perturb")]:
        m, s = mean_std([r[key] for r in results])
        print(f"  {label:20s}: {m:.3f} ± {s:.3f}")


if __name__ == "__main__":
    main()
