from src.cls.NPC import *

class World():
    def __init__(self):
        self.cfg = {}
        self.人物 = []
        self.人数 = 0
        self.已故人物 = []
        self.已故人数 = 0
        self.门派 = ['\033[32m凌霄派\033[0m','\033[32m圣火门\033[0m','\033[32m玄天洞\033[0m','\033[32m魔门\033[0m','\033[32m散修\033[0m']#TODO 增加
        self.地点 = ['古战场']
        self.事件 = 0
        #self.随机事件权重 = [['加人',12],['恩怨',10],['奇遇',5],['帮战',2],['无事',80]]
        self.随机事件权重 = {'加人':12,'恩怨':10,'奇遇':5,'帮战':2,'无事':80}
        self.随机事件分段 = []
        self.run = 1
        self.time = [0, 1]
        self.print = [0]
        self.alive_limit = 300
        self.dead_limit = 300
        self.mail = []
        self.END = 0
    def initial(self):
        for i in range(20):
            tmp = NPC()
            tmp.creat_random_npc()
            tmp.门派 = random.choice(self.门派)
            self.人物.append(tmp)
            self.人数 += 1

    def add_one(self):
        self.人数 += 1
        tmp = NPC()
        tmp.creat_random_npc()
        tmp.门派 = random.choice(self.门派)
        self.人物.append(tmp)
        return tmp
    def 增加蛐蛐(self, name):
        self.人数 += 1
        tmp = NPC()
        tmp.creat_random_npc()
        tmp.门派 = random.choice(self.门派)
        tmp.姓名 = f'\033[35m{name}\033[0m'
        tmp.天命 = 1
        tmp.转世 = 1
        tmp.全名计算()
        self.人物.append(tmp)
        tmp.历史 = f"大造化将{tmp.姓名}投入这一方小世界中\n"
        print(f"大造化将{tmp.姓名}投入这一方小世界中\n")
    def dzqq(self):
        a = []#
        p = ''
        self.人数 += len(a)
        for i in a:
            tmp = NPC()
            tmp.creat_random_npc()
            tmp.门派 = random.choice(self.门派)
            tmp.姓名 = f'\033[35m{i}\033[0m'
            tmp.天命 = 1
            tmp.转世 = 1
            tmp.全名计算()
            self.人物.append(tmp)
            p += f"大造化将{tmp.姓名}投入这一方小世界中\n"
        return p
    def new_mp(self):
        a = random.choice(['星云','天河','昆仑','崆峒','元华','墨佬','化生','乾坤'])
        b = random.choice(['谷','洞','派','山','宗','门'])
        self.门派.append('\033[32m' + a+b + '\033[0m')
        for i in range(3):
            self.人数 += 1
            tmp = NPC()
            tmp.creat_random_npc()
            tmp.门派 = '\033[32m' + a+b + '\033[0m'
            self.人物.append(tmp)
    def 排天榜(self):
        #def x(a =NPC()):
        #    return a.战斗力
        #self.人物.sort(key = x, reverse=True)
        self.人物.sort(key = lambda x: x.战斗力, reverse = True)