# EcoMAS

## 复杂环境中智能体协作与涌现行为研究框架

------------------------------------------------------------------------

# 1. 项目简介

EcoMAS（Emergent Multi-Agent System）旨在研究：

> 智能体如何在复杂环境中形成可靠协作，并产生超越单个个体能力的群体涌现行为。

本项目使用蚁群环境作为第一个实验场景。

需要强调：

**本项目不是模拟蚂蚁的大脑，也不是让大语言模型扮演蚂蚁。**

蚁群只是一个天然存在协作行为的复杂系统，用于研究：

-   个体决策机制
-   智能体交互
-   通信机制
-   群体协作
-   涌现行为

------------------------------------------------------------------------

# 2. 科学问题

传统多智能体系统通常依赖人工设计规则：

    如果发现食物:
        收集资源

    如果发现信息:
        跟随路径

这种方式的问题：

-   行为规则需要人工指定；
-   难以适应未知环境；
-   群体行为来自设计，而不是自然形成。

EcoMAS探索：

> 当智能体拥有不同程度的决策能力时，群体协作是否会产生不同形式的涌现？

------------------------------------------------------------------------

# 3. 核心研究假设

## H1

不同个体决策机制会导致不同群体行为模式。

比较：

    规则驱动 Agent

    ↓

    强化学习 Agent

    ↓

    推理驱动 Agent（LLM）

------------------------------------------------------------------------

## H2

具备推理能力的智能体可能具有更强的：

-   环境适应能力；
-   协作能力；
-   长期规划能力。

------------------------------------------------------------------------

# 4. 实验环境：Ant Colony World

二维空间环境：

包含：

-   蚁巢；
-   食物资源；
-   障碍物；
-   动态环境变化。

示例：

    +----------------+

            Food


       #        #

            A


    Nest

    +----------------+

------------------------------------------------------------------------

# 5. Agent设计

## Ant Agent

每个蚂蚁智能体具有：

## 状态(State)

    position

    energy

    carrying_food

    memory

    communication_history

    role

------------------------------------------------------------------------

## 感知(Observation)

智能体只能获得局部信息：

    nearby_food

    nearby_agents

    pheromone_signal

    environment_change

模拟真实复杂系统中的局部信息限制。

------------------------------------------------------------------------

## 行动(Action)

动作空间：

    explore

    collect_food

    return_home

    communicate

    help

    rest

------------------------------------------------------------------------

# 6. 决策模块设计

核心实验变量：

只改变决策机制。

保持：

-   环境一致；
-   Agent身体一致；
-   Action空间一致。

------------------------------------------------------------------------

# 6.1 Rule-based Agent

传统ABM方法。

行为由人工规则定义：

    if food nearby:

        collect

    elif pheromone high:

        follow

    else:

        explore

作为基础baseline。

------------------------------------------------------------------------

# 6.2 Reinforcement Learning Agent

学习型智能体。

输入：

    agent state

    environment state

    neighbor information

输出：

action。

------------------------------------------------------------------------

奖励：

## Individual Reward

个人收益：

    food collected

    survival

    energy

## Collective Reward

群体收益：

    colony food storage

    team survival

研究合作是否能够通过学习形成。

------------------------------------------------------------------------

# 6.3 LLM Reasoning Agent

LLM不模拟蚂蚁。

LLM作为：

> 高层决策模块。

输入：

    Current colony state:

    Food discovered:
    3

    Nearby agents:
    10

    Resource demand:
    High


    Available strategies:

    1 Exploration
    2 Recruitment
    3 Resource transport
    4 Conservation

输出：

    strategy:

    recruit


    reason:

    Resource location is valuable,
    additional agents should be coordinated.

------------------------------------------------------------------------

# 7. 系统架构

                    Environment

                         |

                  Observation

                         |

                    Agent

                         |

            ------------------------

            |          |           |

          Rule       RL          LLM


                         |

                      Action

                         |

                  Environment Update


                         |

                  Emergent Behavior

------------------------------------------------------------------------

# 8. 通信模块

通信是MAS区别于普通ABM的重要部分。

Agent之间可以发送：

    food location

    resource quality

    danger signal

    strategy information

通信策略比较：

-   无通信；
-   固定通信；
-   自主通信。

------------------------------------------------------------------------

# 9. 实验设计

## Experiment 1：搜索效率

问题：

不同智能机制寻找资源能力如何？

指标：

-   discovery time
-   exploration coverage

------------------------------------------------------------------------

## Experiment 2：协作效率

问题：

智能体是否形成有效合作？

指标：

-   food collection rate
-   energy efficiency

------------------------------------------------------------------------

## Experiment 3：角色分化

问题：

是否产生自然分工？

观察：

    Explorer

    Collector

    Communicator

    Supporter

指标：

-   behavior diversity
-   role distribution

------------------------------------------------------------------------

## Experiment 4：环境适应

改变：

-   食物位置；
-   资源减少；
-   障碍增加。

指标：

-   recovery time
-   survival rate

------------------------------------------------------------------------

# 10. 评价指标

## Individual Level

-   survival
-   reward
-   behavior

## Collective Level

-   cooperation efficiency
-   specialization
-   stability
-   adaptability

------------------------------------------------------------------------

# 11. 项目目录

    ecomas_ant_demo/

    ├── README.md

    ├── environment/

    │   ├── world.py

    │   ├── food.py

    │   └── pheromone.py


    ├── agents/

    │   ├── base_agent.py

    │   └── ant.py


    ├── decision/

    │   ├── rule_policy.py

    │   ├── rl_policy.py

    │   └── llm_policy.py


    ├── communication/

    │   └── message.py


    ├── memory/

    │   └── memory.py


    ├── simulation/

    │   └── simulator.py


    ├── experiments/

    │   ├── baseline.py

    │   └── comparison.py


    ├── visualization/

    │   └── visualize.py


    └── docs/

        └── design.md

------------------------------------------------------------------------

# 12. 开发路线

## Phase 1

完成：

-   环境；
-   Agent；
-   Rule baseline。

目标：

跑通蚁群系统。

------------------------------------------------------------------------

## Phase 2

加入：

RL Agent。

目标：

建立学习型baseline。

------------------------------------------------------------------------

## Phase 3

加入：

LLM Decision。

目标：

比较三种智能机制。

------------------------------------------------------------------------

## Phase 4

研究：

-   通信；
-   记忆；
-   长期规划。

------------------------------------------------------------------------

# 13. 长期方向

EcoMAS不是蚁群模拟器。

蚁群只是第一个benchmark。

未来扩展：

    Ant Colony

    ↓

    River Ecosystem

    ↓

    Carbon Cycle

    ↓

    General Complex Systems

最终目标：

研究：

> 智能体如何在复杂世界中组织自己，并形成集体智能。
