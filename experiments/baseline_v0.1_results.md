# Baseline v0.1：RulePolicy 实验结果

**日期**：2026-09-05
**代码**：仓库 main 分支「Add multi-seed baseline experiment runner」提交对应版本
**复现**：

```bash
python -m experiments.baseline
```

## 实验配置

| 参数 | 值 |
| --- | --- |
| 决策机制 | RulePolicy（纯规则 baseline） |
| 世界 | 40 × 20 网格，蚁巢居中 |
| 食物 | 5 处 × 10 单位 = 50 单位 |
| 蚂蚁数量 | 20 |
| 步数 | 200 |
| 扰动 | 第 100 步全部食物搬移（`world.perturb()`） |
| 种子 | 0–9，共 10 次独立运行 |

## 指标定义

- **survival rate**：终态存活个体比例
- **contribution gini**：个体食物贡献的基尼系数（0=均等，趋近 1=高度集中）
- **throughput**：群体采集速率（food / timestep），合作效率
- **division of labor**：分工指数 = H(群体混合分布) − mean H(个体分布)，归一化到 [0,1]；全员通才趋近 0，个体各自专精趋近 1
- **recovery time**：扰动后到下一次食物交付入库的步数
- **pre/post rate**：扰动前/后窗口内的采集速率

## 结果（mean ± std，n=10）

### Individual

| 指标 | 值 |
| --- | --- |
| survival rate | 0.840 ± 0.158 |
| mean energy | 24.429 ± 2.768 |
| contribution gini | 0.385 ± 0.142 |

### Collective

| 指标 | 值 |
| --- | --- |
| throughput (food/step) | 0.135 ± 0.060 |
| division of labor (0–1) | 0.012 ± 0.008 |
| role distribution | explorer 1.00, collector 0.00, transporter 0.00, rest 0.00 |

### Robustness

| 指标 | 值 |
| --- | --- |
| recovery time | 12.9 ± 4.7 steps（9/10 次恢复） |
| rate pre-perturb | 0.175 ± 0.072 |
| rate post-perturb | 0.094 ± 0.066 |

## 解读

纯规则驱动下，群体**能采集、扰动后能恢复，但完全没有分工涌现**（DOL ≈ 0.01，所有个体行为同质的通才）。这组数字构成后续对比的零假设：

- v0.2 通信实验：观察通信是否提升 throughput、缩短 recovery time
- v0.3 RL 实验：观察学习是否产生 DOL 显著大于 0 的角色分化
- v0.4 LLM 实验：观察推理型决策在鲁棒性上是否与规则驱动有质差异

任一指标显著偏离本 baseline，即为该决策机制下群体涌现的证据。
