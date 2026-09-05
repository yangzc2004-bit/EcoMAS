"""Rule-based Agent：人工规则 baseline（设计文档 6.1，Phase 1）。

逻辑：
    携带着食物 -> 回巢
    能量不足 -> 回巢补给
    脚下有食物 -> 采集
    视野内有食物 -> 朝食物移动
    否则 -> 随机探索
"""

LOW_ENERGY = 15


class RulePolicy:
    def __init__(self, rng=None):
        self.rng = rng

    def choose_action(self, observation):
        if observation["carrying_food"] > 0:
            return ("return_home",)
        if observation["energy"] < LOW_ENERGY:
            return ("return_home",)

        nearby = observation["nearby_food"]
        if nearby:
            here = observation["position"]
            for pos, _amount in nearby:
                if pos == here:
                    return ("collect_food",)
            target = min(nearby, key=lambda f: abs(f[0][0] - here[0]) + abs(f[0][1] - here[1]))
            return ("move_to", target[0])

        return ("explore",)
