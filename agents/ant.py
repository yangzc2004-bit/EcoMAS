"""Ant Agent：蚁群场景中的具体智能体（设计文档第 5 节）。

只实现身体能力（移动、采集、回巢）与状态，不包含任何策略——
"什么时候做什么"由 decision/ 层决定。
"""

from agents.base_agent import BaseAgent

MOVE_COST = 1
REST_GAIN = 2
EAT_GAIN = 30
MAX_ENERGY = 100
DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


class Ant(BaseAgent):
    def __init__(self, ant_id, position, energy=MAX_ENERGY):
        self.id = ant_id
        self.position = position
        self.energy = energy
        self.carrying_food = 0
        self.memory = {"known_food": set()}
        self.role = None
        self.alive = True

    # ------------------------------------------------------------------
    # 接口实现
    # ------------------------------------------------------------------
    def observe(self, world):
        obs = world.observe(self)
        known = self.memory["known_food"]
        obs["new_food_found"] = [pos for pos, _ in obs["nearby_food"] if pos not in known]
        known.update(pos for pos, _ in obs["nearby_food"])
        return obs

    def decide(self, observation, policy):
        return policy.choose_action(observation)

    def act(self, action, world):
        if not self.alive:
            return
        name = action[0]
        if name == "explore":
            self.move(self._random_step(world), world)
        elif name == "move_to":
            self.move(self._step_toward(action[1]), world)
        elif name == "collect_food":
            self.collect_food(world)
        elif name == "return_home":
            self.return_home(world)
        elif name == "rest":
            self.energy = min(MAX_ENERGY, self.energy + REST_GAIN)
        if self.energy <= 0:
            self.alive = False

    # ------------------------------------------------------------------
    # 身体能力
    # ------------------------------------------------------------------
    def move(self, new_position, world):
        if world.in_bounds(new_position):
            self.position = new_position
        self.energy -= MOVE_COST

    def collect_food(self, world):
        food = world.food_at(self.position)
        if food is not None:
            self.carrying_food += food.collect(1)

    def return_home(self, world):
        if self.position == world.nest:
            if self.carrying_food > 0:
                world.colony_food += self.carrying_food
                self.carrying_food = 0
            self.energy = min(MAX_ENERGY, self.energy + EAT_GAIN)
        else:
            self.move(self._step_toward(world.nest), world)

    # ------------------------------------------------------------------
    # 移动辅助（纯运动学，不含策略）
    # ------------------------------------------------------------------
    def _random_step(self, world):
        dx, dy = world.rng.choice(DIRECTIONS)
        return (self.position[0] + dx, self.position[1] + dy)

    def _step_toward(self, target):
        x, y = self.position
        tx, ty = target
        if tx > x:
            x += 1
        elif tx < x:
            x -= 1
        elif ty > y:
            y += 1
        elif ty < y:
            y -= 1
        return (x, y)
