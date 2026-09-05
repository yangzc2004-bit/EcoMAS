"""Agent 基类：所有决策机制共享的统一接口。

Rule Agent / RL Agent / LLM Agent 都必须通过同一组接口与环境交互
（设计文档第 5、6 节）：observe -> decide -> act。
基类不实现任何策略。
"""


class BaseAgent:
    """智能体接口：状态、局部感知与动作执行。"""

    def observe(self, world):
        """从环境获取局部观察。"""
        raise NotImplementedError

    def decide(self, observation, policy):
        """基于观察，借助 policy 选择动作。"""
        raise NotImplementedError

    def act(self, action, world):
        """执行动作，改变自身与环境状态。"""
        raise NotImplementedError
