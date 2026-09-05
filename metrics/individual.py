"""个体层面指标（设计文档 10. Individual Level）。

输入只有 world.history 与 agent 终态，不读仿真内部状态。
"""


def gini(values):
    """基尼系数：衡量个体贡献的不平等程度（0=完全均等，趋近1=高度集中）。"""
    vals = sorted(values)
    n = len(vals)
    total = sum(vals)
    if n == 0 or total == 0:
        return 0.0
    weighted = sum(i * v for i, v in enumerate(vals, 1))
    return (2 * weighted) / (n * total) - (n + 1) / n


def individual_metrics(history, ants, total_steps):
    """个体层面指标。

    - survival_rate: 存活比例
    - mean_energy: 存活个体的平均终态能量
    - contribution_gini: 食物贡献的基尼系数（个体贡献分化程度）
    - per_ant: 每只蚂蚁的 survival_time / final_energy / contribution
    """
    traj = [e for e in history if "action" in e]
    delivered = [e for e in history if e.get("event") == "delivered"]

    last_seen = {}
    for e in traj:
        last_seen[e["ant_id"]] = e["timestep"]

    per_ant = []
    for ant in ants:
        survival_time = total_steps if ant.alive else last_seen.get(ant.id, 0) + 1
        contribution = sum(e["amount"] for e in delivered if e["ant_id"] == ant.id)
        per_ant.append({
            "ant_id": ant.id,
            "alive": ant.alive,
            "survival_time": survival_time,
            "final_energy": ant.energy if ant.alive else 0,
            "contribution": contribution,
        })

    alive_ants = [a for a in ants if a.alive]
    return {
        "survival_rate": len(alive_ants) / len(ants) if ants else 0.0,
        "mean_energy": (sum(a.energy for a in alive_ants) / len(alive_ants)) if alive_ants else 0.0,
        "contribution_gini": gini([p["contribution"] for p in per_ant]),
        "per_ant": per_ant,
    }
