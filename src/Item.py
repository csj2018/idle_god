import random

class Item():
    def __init__(self, owner = None):
        self.名称 = ''
        self.兵刃 = 0
        self.境界 = 0
        self.能量 = 0
        self.拥有者 = owner
    def 钓鱼(self, owner):
        if owner.境界 <= 1:
            self.名称 = random.choice(['飞鱼','鲤鱼','鲑鱼','黄鱼','黑鱼','四驱车'])
        elif owner.境界 <= 3:
            self.名称 = random.choice(['抹香鲸','大白鲨','黑熊','游艇'])
        elif owner.境界 <= 5:
            self.名称 = random.choice(['钢铁侠','蛟龙','北海巨龟','鳖鳖'])
        elif owner.境界 <= 7:
            self.名称 = random.choice(['护卫舰','巡洋舰','驱逐舰'])
        else:
            self.名称 = random.choice(['战列巡洋舰','战列舰','航空母舰'])
        self.名称 = f'\033[33m{self.名称}\033[0m'
        owner.物品.append(self)
        owner.world.printj(f'{owner.全名}沉迷钓鱼，在大海之上钓到{self.名称}，喜不自胜，随身携带', [owner], p = 2)
        if len(owner.物品) > 5:
            tmp = owner.物品.pop(0)
            owner.world.printj(f'{owner.全名}突然觉得手里的{tmp.名称}不香了，随手丢弃', [owner], p = 2)