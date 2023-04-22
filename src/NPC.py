import random


class NPC():
    def __init__(self):
        self.姓 = ''
        self.姓名 = ''
        self.称号 = ''
        self.全名 = ''
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
        self.天命 = 0
        self.转世 = 1
        self.影响力 = 0
        self.战斗力 = 0
    def creat_random_npc(self):
        self.姓 = random.choice(['罗', '麻', '东皇', '苍', '蓝', '叶', '轩辕', '姬', '冷', '寒', '南宫', '炎', '令狐', '东方', '北冥', '西门',
          '秋', '太苍', '麒麟', '刘', '柳', '服部', '吉田', '李', '黄', '黑', '白', '铁', '木', '林', '沧海', '吉布森·', '布鲁斯·', '詹姆斯·',
          '欧阳', '魏', '蓝', '江', '聂', '金', '温', '薛', '宋', '阿', '云', '秦', '姚', '欧'])
        名 = random.choice(['亿', '元', '太一', '命', '无忌', '悔', '逍遥', '陨', '炎', '莫愁', '爱国', '爱民', '秋水', '子', '阿牛', '克',
         '星', '月', '阳', '朔', '顶天', '无敌', '权', '崇', '明', '晨', '斩天', '猛', '无缺', '牛牛', '光', '雷', '泪', '小小', '无羡', '忘机',
         '澄', '怀桑', '光瑶', '曦臣', '凌', '宁', '洋', '岚', '星星', '庆', '苏', '棉棉', '子轩', '安县令', '少恭', '安陵容', '莫言', '豫津', '星尘',
        '温情', '温宁', '温八', '温华', '温清', '温青', '温柔'])
        self.姓名 = f"\033[33m{self.姓}{名}\033[0m"
        self.称号 = ''
        self.全名 = ''
        self.全名计算()
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
        self.战斗力计算()
        self.拥有者 = ''
    def print_npc_detial(self):
        print('【姓名】 {self.姓名}'+
              '【先天资质】 {self.体质}{self.先天资质}')
    def creat_ch(self):
        a = random.choice(['命','元','咒','陨','皇','凰','灵','血','魔','影','英','狂','夜','天','葬','无','嗜'])
        b = random.choice(['命','元','咒','陨','皇','凰','灵','血','魔','影','英','狂','夜','天','葬','无','嗜'])
        c =  random.choice(["剑仙", "魔头", "仙女", "鬼王", "天师", "魔女", "仙子", "鬼手", "天尊", "龙王", "魔尊", "仙王", "鬼仙",
                           "天仙", "龙仙", "魔仙", "仙帝", "鬼帝", "天帝", '尊者','真君','天师','真人','神君','神王','罗汉','高手',
                           '怪盗','花手'])
        self.称号 = '\033[31m★' + a + b + c + '★\033[0m'
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
    def 全名计算(self):
        if self.转世 == 1:
            self.全名 = self.称号 + self.姓名
        else:
            self.全名 = self.称号 + self.姓名 + f"\033[34m第{self.转世}世\033[0m"
    def 战斗力计算(self):
        a = self.先天资质 + self.后天资质 + 20
        b = 8 ** self.境界 * (6 + self.小境界)
        self.战斗力 = a * b