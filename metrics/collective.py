"""群体层面指标（设计文档 10. Collective Level）。

- throughput: 单位时间收集资源（food / timestep），即 cooperation efficiency
- role_distribution: 按每只蚂蚁主导 action 划分的角色比例（描述性）
- division_of_labor: 分工指数 = H(群体混合分布) - mean H(个体分布)，归一化到
  [0,1]。全员通才（个体分布≈群体分布）时趋近 0；个体各自专精不同角色时趋近 1。
  这是 Experiment 3「是否产生自然分工」的核心量化。
"""

import math

# action -> 角色 映射（设计文档第 9 节 Experiment 3 的四类角色）
ROLE_MAP = {
    "explore": "explorer",
    "move_to": "collector",
    "collect_food": "collector",
    "return_home": "transporter",
    "rest": "rest",
}
ROLES = ["explorer", "collector", "transporter", "rest"]


def _entropy(proportions):
    return -sum(p * math.log(p) for p in proportions if p > 0)


def _role_vectors(history):
    """每只蚂蚁在四类角色上的步数向量。"""
    vectors = {}
    for e in history:
        if "action" not in e:
            continue
        vec = vectors.setdefault(e["ant_id"], [0] * len(ROLES))
        vec[ROLES.index(ROLE_MAP.get(e["action"], "rest"))] += 1
    return vectors


def division_of_labor(history):
    """H(pooled) - mean H(individual)，归一化；无轨迹时返回 0。"""
    vectors = _role_vectors(history)
    if not vectors:
        return 0.0
    pooled = [sum(v[i] for v in vectors.values()) for i in range(len(ROLES))]
    total = sum(pooled)
    if total == 0:
        return 0.0
    h_pooled = _entropy([x / total for x in pooled])
    h_indiv = []
    for v in vectors.values():
        t = sum(v)
        h_indiv.append(_entropy([x / t for x in v]) if t else 0.0)
    dol = h_pooled - sum(h_indiv) / len(h_indiv)
    return dol / math.log(len(ROLES))


def collective_metrics(history, world, total_steps):
    delivered = [e for e in history if e.get("event") == "delivered"]
    total_collected = sum(e["amount"] for e in delivered)
    throughput = total_collected / total_steps if total_steps else 0.0

    # 描述性角色分布：每只蚂蚁的主导角色
    vectors = _role_vectors(history)
    ant_roles = {}
    for ant_id, vec in vectors.items():
        ant_roles[ant_id] = ROLES[vec.index(max(vec))]
    n = len(ant_roles)
    role_distribution = {
        role: sum(1 for r in ant_roles.values() if r == role) / n if n else 0.0
        for role in ROLES
    }

    return {
        "total_collected": total_collected,
        "throughput": throughput,
        "role_distribution": role_distribution,
        "division_of_labor": division_of_labor(history),
        "ant_roles": ant_roles,
    }
