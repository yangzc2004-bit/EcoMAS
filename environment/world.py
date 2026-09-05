"""二维蚁群世界：空间、蚁巢、食物与时间推进。

对应设计文档第 4 节。World 只负责环境状态与物理推进，不做任何决策
（"看到食物要不要采集"属于 decision/ 层）。
"""

from environment.food import Food


class World:
    """二维网格世界。"""

    def __init__(self, width=40, height=20, n_foods=5, vision=5, rng=None):
        self.width = width
        self.height = height
        self.nest = (width // 2, height // 2)
        self.foods = []
        self.timestep = 0

        self.vision = vision
        self.colony_food = 0
        self.total_food = 0
        self.agents = []

        import random

        self.rng = rng or random.Random()
        for _ in range(n_foods):
            self.spawn_food()

    # ------------------------------------------------------------------
    # 环境结构
    # ------------------------------------------------------------------
    def spawn_food(self, amount=10, min_dist_from_nest=5):
        """在远离蚁巢的随机位置生成一处食物。"""
        while True:
            pos = (self.rng.randrange(self.width), self.rng.randrange(self.height))
            if self.distance(pos, self.nest) >= min_dist_from_nest:
                break
        self.foods.append(Food(pos, amount))
        self.total_food += amount

    def register(self, agent):
        self.agents.append(agent)

    @staticmethod
    def distance(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def in_bounds(self, pos):
        return 0 <= pos[0] < self.width and 0 <= pos[1] < self.height

    def food_at(self, position):
        for food in self.foods:
            if food.position == position and not food.depleted:
                return food
        return None

    # ------------------------------------------------------------------
    # 局部观察：只返回 agent 视野内的信息（设计文档第 5 节）
    # ------------------------------------------------------------------
    def observe(self, agent):
        nearby_food = [
            (food.position, food.amount)
            for food in self.foods
            if not food.depleted and self.distance(agent.position, food.position) <= self.vision
        ]
        nearby_agents = [
            other.id
            for other in self.agents
            if other is not agent
            and other.alive
            and self.distance(agent.position, other.position) <= self.vision
        ]
        return {
            "position": agent.position,
            "energy": agent.energy,
            "carrying_food": agent.carrying_food,
            "nest": self.nest,
            "nearby_food": nearby_food,
            "nearby_agents": nearby_agents,
            "timestep": self.timestep,
        }

    # ------------------------------------------------------------------
    # 时间推进
    # ------------------------------------------------------------------
    def step(self):
        self.foods = [food for food in self.foods if not food.depleted]
        self.timestep += 1
