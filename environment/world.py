"""二维蚁群世界：空间、蚁巢、食物与时间推进。

对应设计文档第 4 节。World 只负责环境状态与物理推进，不做任何决策
（"看到食物要不要采集"属于 decision/ 层）。

world.history 记录每一步每个 agent 的轨迹与关键事件，供 Rule/RL/LLM
对比实验做离线分析。注意：history 只写不读，绝不进入 observe()，
避免全局信息泄漏到局部观察。

world.perturb() 是受控环境扰动接口，供鲁棒性实验（Experiment 4）使用。
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
        self.history = []

        import random

        self.rng = rng or random.Random()
        for _ in range(n_foods):
            self.spawn_food()

    # ------------------------------------------------------------------
    # 环境结构
    # ------------------------------------------------------------------
    def _random_food_pos(self, min_dist_from_nest=5):
        while True:
            pos = (self.rng.randrange(self.width), self.rng.randrange(self.height))
            if self.distance(pos, self.nest) >= min_dist_from_nest:
                return pos

    def spawn_food(self, amount=10):
        """在远离蚁巢的随机位置生成一处食物。"""
        food = Food(self._random_food_pos(), amount)
        self.foods.append(food)
        self.total_food += amount

    def perturb(self):
        """受控扰动：把所有未耗尽食物搬移到新的随机位置。

        agent 记忆中的旧位置随之失效——鲁棒性实验（Experiment 4）的核心操作。
        """
        for food in self.foods:
            food.position = self._random_food_pos()
        self.record({"timestep": self.timestep, "event": "perturbation",
                     "detail": "all foods relocated"})

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
    # 轨迹记录：只追加，不消耗 RNG、不改变任何仿真状态
    # ------------------------------------------------------------------
    def record(self, entry):
        """追加一条轨迹或事件记录。

        轨迹: {"timestep", "ant_id", "action", "position", "energy", "carrying_food"}
        事件: {"timestep", "ant_id", "event", ...}
        """
        self.history.append(entry)

    # ------------------------------------------------------------------
    # 局部观察：只返回 agent 视野内的信息（设计文档第 5 节）
    # 注意：不得包含 self.history 等全局信息。
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
