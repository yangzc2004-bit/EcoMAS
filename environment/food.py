"""食物资源对象。

对应设计文档第 4 节。食物只携带位置与数量信息，不包含任何行为逻辑。
"""


class Food:
    """一处食物资源。"""

    def __init__(self, position, amount=10):
        self.position = position
        self.amount = amount

    def collect(self, quantity=1):
        """被采集 quantity 单位，返回实际采集到的数量。"""
        taken = min(quantity, self.amount)
        self.amount -= taken
        return taken

    @property
    def depleted(self):
        return self.amount <= 0
