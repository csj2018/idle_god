import random
import threading
import time
class NPC():
    def __init__(self):
        self.姓 = ''
        self.姓名 = ''
        self.称号 = ''
        self.年龄 = 0
        self.寿命 = 100
        self.境界 = 0  #炼气期 筑基期 金丹期 元婴期 出窍期 分神期
        self.小境界 = 0
        self.能量 = int(0)
        self.瓶颈 = int(0)
        self.可突破 = 0
        self.成功率 = 0
        self.基础成功率 = 0
        self.先天资质 = 0
        self.后天资质 = 0
        self.资质 = 0
        self.效率 = 1
        self.门派 = ''
        self.体质 = ''
        self.分身 = 0
        self.历史 = ''
        self.事件 = ''
        self.行动 = []
    def creat_random_npc(self):
        self.姓 = random.choice(['罗','麻','东皇','苍','蓝','叶','轩辕','姬','冷','寒','南宫','炎','令狐','东方','北冥','西门','秋','太苍','麒麟','刘'
                                ,'柳','服部','吉田','李','黄','黑','白','铁','木','林','沧海','吉布森·','布鲁斯·','詹姆斯·','欧阳'])
        名 = random.choice(['亿','元','太一','命','无忌','悔','逍遥','陨','炎','莫愁','爱国','爱民','秋水','子','阿牛','克','星','月','阳','朔','顶天'
                           ,'无敌','权','崇','明','晨','斩天','猛','无缺'])
        self.姓名 = '\033[33m'+self.姓 + 名+'\033[0m'
        self.称号 = ''
        self.先天资质 = random.randint(6,35)
        tmp = self.先天资质
        while tmp >= 1:
            if tmp >= 20:
                self.体质 += random.choice(['至尊','太古','九幽'])
                tmp -= 20
            elif tmp >= 13:
                self.体质 += random.choice(['无极', '寂灭', '混元'])
                tmp -= 13
            elif tmp >= 8:
                self.体质 += random.choice(['变异', '不灭', '阴阳'])
                tmp -= 8
            elif tmp >= 5:
                self.体质 += random.choice(['九天', '八荒', '太玄'])
                tmp -= 5
            elif tmp >= 3:
                self.体质 += random.choice(['光合', '双核', '先天'])
                tmp -= 3
            elif tmp >= 2:
                self.体质 += random.choice(['琉璃', '黄金', '光华'])
                tmp -= 2
            elif tmp >= 1:
                self.体质 += random.choice(['魔', '幽', '灵'])
                tmp -= 1
        self.体质 += '体'
        self.境界 = 0
        self.小境界 = 0
        self.瓶颈 = 300
        self.成功率 = 100
        self.年龄 = random.randint(6,70)
    def print_npc_detial(self):
        print('【姓名】 {self.姓名}'+
              '【先天资质】 {self.体质}{self.先天资质}')
    def creat_ch(self):
        a = random.choice(['命','元','咒','陨','皇','凰','灵','血','魔','影','英','狂','夜','天','葬','无'])
        b = random.choice(['命','元','咒','陨','皇','凰','灵','血','魔','影','英','狂','夜','天','葬','无'])
        c =  random.choice(['尊者','真君','天师','真人','神君','神王','罗汉'])
        self.称号 = '★' + a + b + c + '★'
    def 计算成功率(self):
        base = 95 - 8 * self.境界
        if self.小境界 == 0:
            self.成功率 = base
        elif self.小境界 == 3:
            self.成功率 = base - 3
        elif self.小境界 == 6:
            self.成功率 = base - 6
        elif self.小境界 == 9:
            self.成功率 = base/2
class World():
    def __init__(self):
        self.人物 = []
        self.人数 = 0
        self.门派 = ['\033[32m凌霄派\033[0m','\033[32m圣火门\033[0m','\033[32m玄天洞\033[0m','\033[32m魔门\033[0m','\033[32m散修\033[0m']
        self.地点 = ['古战场']
        self.事件 = 0
        self.随机事件权重 = [['加人',6],['恩怨',10],['奇遇',3],['帮战',1],['',80]]
        self.随机事件分段 = []
        self.run = 1
        self.time = [0, 1]
        self.print = [0]
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
        tmp.门派 = '\033[32m'+random.choice(self.门派)+'\033[0m'
        self.人物.append(tmp)
        return tmp
    def new_mp(self):
        a = random.choice(['星云','天河','昆仑','崆峒','元华','墨佬'])
        b = random.choice(['谷','洞','派','山','宗','门'])
        self.门派.append('\033[32m' + a+b + '\033[0m')
        for i in range(3):
            self.人数 += 1
            tmp = NPC()
            tmp.creat_random_npc()
            tmp.门派 = '\033[32m' + a+b + '\033[0m'
            self.人物.append(tmp)
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
