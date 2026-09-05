"""主仿真器：时间循环（设计文档第 7 节）。

    for step:
        for ant:
            observation = ant.observe()
            action = policy.choose_action(observation)
            ant.act(action)
        world.step()

轨迹记录由 Simulator 统一在每次 ant.act 之后写入 world.history，
agent 自身不参与记录，保证未来 RL/LLM agent 不会漏记。
"""

STATUS_INTERVAL = 10


class Simulator:
    def __init__(self, world, ants, policy):
        self.world = world
        self.ants = ants
        self.policy = policy
        for ant in ants:
            world.register(ant)

    def run(self, steps):
        world = self.world
        print("=== EcoMAS Ant Demo ===")
        print(f"World {world.width}x{world.height}, nest at {world.nest}, "
              f"{len(world.foods)} food sources ({world.total_food} units)")
        print()

        for _ in range(steps):
            t = world.timestep
            step_events = []

            for ant in self.ants:
                if not ant.alive:
                    continue
                observation = ant.observe(world)
                action = ant.decide(observation, self.policy)
                food_before = world.colony_food
                ant.act(action, world)

                world.record({
                    "timestep": t,
                    "ant_id": ant.id,
                    "action": action[0],
                    "position": ant.position,
                    "energy": ant.energy,
                    "carrying_food": ant.carrying_food,
                })

                for pos in observation["new_food_found"]:
                    world.record({"timestep": t, "ant_id": ant.id,
                                  "event": "food_found", "position": pos})
                    step_events.append(f"Ant-{ant.id} found food at {pos}")
                delivered = world.colony_food - food_before
                if delivered > 0:
                    world.record({"timestep": t, "ant_id": ant.id,
                                  "event": "delivered", "amount": delivered})
                    step_events.append(
                        f"Ant-{ant.id} delivered {delivered} food "
                        f"(colony: {world.colony_food}/{world.total_food})"
                    )

            world.step()

            if t % STATUS_INTERVAL == 0:
                alive = sum(a.alive for a in self.ants)
                print(f"Step {t:>4} | foods left: {len(world.foods)}, "
                      f"colony food: {world.colony_food}/{world.total_food}, "
                      f"ants alive: {alive}")
            for event in step_events:
                print(f"Step {t:>4} | {event}")

        self._print_summary()

    def _print_summary(self):
        world = self.world
        alive = sum(a.alive for a in self.ants)
        print()
        print("Colony:")
        print(f"  ants alive: {alive}/{len(self.ants)}")
        print(f"  food collected: {world.colony_food}/{world.total_food}")
        print(f"  history records: {len(world.history)}")
