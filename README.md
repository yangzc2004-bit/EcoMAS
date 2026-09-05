# EcoMAS-Ant

**复杂环境中智能体协作与涌现行为研究框架**（Emergent Multi-Agent System）

> 智能体如何在复杂环境中形成可靠协作，并产生超越单个个体能力的群体涌现行为。

本项目使用蚁群环境作为第一个实验场景。**本项目不是模拟蚂蚁的大脑，也不是让大语言模型扮演蚂蚁**——蚁群只是一个天然存在协作行为的复杂系统，用于研究个体决策机制、智能体交互、通信机制、群体协作与涌现行为。

## 核心研究假设

- **H1**：不同个体决策机制会导致不同群体行为模式（规则驱动 → 强化学习 → 推理驱动 LLM）。
- **H2**：具备推理能力的智能体可能具有更强的环境适应能力、协作能力与长期规划能力。

## 实验设计

| 实验 | 问题 | 指标 |
| --- | --- | --- |
| 1 搜索效率 | 不同智能机制寻找资源能力如何？ | discovery time / exploration coverage |
| 2 协作效率 | 智能体是否形成有效合作？ | food collection rate / energy efficiency |
| 3 角色分化 | 是否产生自然分工？ | behavior diversity / role distribution |
| 4 环境适应 | 环境变化后能否恢复？ | recovery time / survival rate |

## 项目结构

```
ecomas_ant_demo/
├── README.md
├── environment/        # world.py / food.py / pheromone.py
├── agents/             # base_agent.py / ant.py
├── decision/           # rule_policy.py / rl_policy.py / llm_policy.py
├── communication/      # message.py
├── memory/             # memory.py
├── simulation/         # simulator.py
├── experiments/        # baseline.py / comparison.py
├── visualization/      # visualize.py
└── docs/               # design.md（开发设计文档 v0.1）
```

## 开发路线

1. **Phase 1**：环境 + Agent + Rule baseline，跑通蚁群系统
2. **Phase 2**：加入 RL Agent，建立学习型 baseline
3. **Phase 3**：加入 LLM Decision，比较三种智能机制
4. **Phase 4**：通信、记忆与长期规划

## 长期方向

Ant Colony → River Ecosystem → Carbon Cycle → General Complex Systems

最终目标：研究智能体如何在复杂世界中组织自己，并形成集体智能。

详细设计见 [docs/design.md](docs/design.md)。
