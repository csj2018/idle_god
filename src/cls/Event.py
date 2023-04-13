import random

class Event():
    def __init__(self):
        self.开始 = 0
        self.结束 = 0
        self.tag = ''#NPC/World
        self.名称 = ''
    def random(self):
        self.开始 = random.randint(3,12)
        self.结束 = self.开始 + random.randint(3,12)
        self.名称 = random.choice(['荒莽','妖鬼','异界','古神'])+random.choice(['幻境','秘境','战场','降临'])