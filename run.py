"""EcoMAS-Ant 最小可运行 demo 入口。

运行：

    python run.py

创建 world / ants / policy / simulator，然后运行 100 步。
"""

import random

from agents.ant import Ant
from decision.rule_policy import RulePolicy
from environment.world import World
from simulation.simulator import Simulator

SEED = 42
N_ANTS = 20
STEPS = 100


def main():
    rng = random.Random(SEED)
    world = World(width=40, height=20, n_foods=5, rng=rng)
    ants = [Ant(ant_id=i + 1, position=world.nest) for i in range(N_ANTS)]
    policy = RulePolicy(rng=rng)
    simulator = Simulator(world, ants, policy)
    simulator.run(STEPS)


if __name__ == "__main__":
    main()
