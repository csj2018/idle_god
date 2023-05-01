import random

class Place():
    def __init__(self):
        self.地名 = ''
        self.门槛 = 0
        self.不可破坏 = 0
        self.驻地 = 0
        self.门派 = ''
        self.角色 = []
    def 绑定门派(self, mp):
        self.驻地 = 1
        self.门派 = mp
        self.地名 = mp
    def 产生地点(self, jj = 0):
        if jj == 0:
            self.地名 = random.choice(['洛阳','金陵','五角大楼','蓬莱','阆中','大理','咸阳','纽约','巴黎','淄博','大排档','小天鹅'])
        elif jj == 1:
            self.地名 = random.choice(['浮空寺', '云梦泽', '千岛', '月之谷', '艾泽', '蓬蒿之地', '大罗谷'])
        elif jj < 4:
            self.地名 = random.choice(['北海尽头', '奈何桥', '天宫', '大雷音寺', '约束之地', '神魔古战场', '南海漩涡'])
        elif jj < 7:
            self.地名 = random.choice(['星穹之下', '三十三重天', '环世界海', '三千世界壁', '鸿蒙之下', '元宇宙', '二点五次元'])
        else:
            self.地名 = random.choice(['星穹之上', '三十三重天外', '环世界海外', '世界壁外', '鸿蒙之上', '元宇宙外', '二次元'])

