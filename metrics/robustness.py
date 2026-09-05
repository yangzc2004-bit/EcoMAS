"""鲁棒性指标（设计文档第 9 节 Experiment 4：环境适应）。

核心指标：恢复时间 = 扰动发生后，到下一次食物交付入库之间经过的步数。
辅助指标：扰动前后的采集速率（delivered amount / step）。
"""


def robustness_metrics(history, perturb_time, total_steps):
    delivered = [e for e in history if e.get("event") == "delivered"]

    after = [e for e in delivered if e["timestep"] >= perturb_time]
    recovery_time = (min(e["timestep"] for e in after) - perturb_time) if after else None

    pre_amount = sum(e["amount"] for e in delivered if e["timestep"] < perturb_time)
    post_amount = sum(e["amount"] for e in after)
    pre_window = max(perturb_time, 1)
    post_window = max(total_steps - perturb_time, 1)

    return {
        "recovery_time": recovery_time,
        "recovered": recovery_time is not None,
        "pre_rate": pre_amount / pre_window,
        "post_rate": post_amount / post_window,
    }
