import random
import src.Place as Place
import src.Item as Item

class NPC():
    def __init__(self, world):
        self.id = 0
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
        self.world = world
        self.仇人 = []
        self.地点 = None
        self.物品 = []
    def 初始化(self):
        self.id = self.world.id
        self.world.id += 1
        self.姓 = random.choice(['罗', '麻', '东皇', '苍', '蓝', '叶', '轩辕', '姬', '冷', '寒', '南宫', '炎', '令狐', '东方', '北冥', '西门',
          '秋', '太苍', '麒麟', '刘', '柳', '服部', '吉田', '李', '黄', '黑', '白', '铁', '木', '林', '沧海', '萧', '庆',
          '欧阳', '魏', '蓝', '江', '聂', '金', '温', '薛', '宋', '阿', '云', '秦', '姚', '欧', '赵'])
        名 = random.choice(['亿', '元', '太一', '命', '无忌', '悔', '逍遥', '陨', '炎', '莫愁', '爱国', '爱民', '秋水', '子', '阿牛', '克',
         '星', '月', '阳', '朔', '顶天', '无敌', '权', '崇', '明', '晨', '斩天', '猛', '无缺', '牛牛', '光', '雷', '泪', '小小', '无羡', '忘机',
         '澄', '怀桑', '光瑶', '曦臣', '凌', '宁', '洋', '岚', '星星', '庆', '苏', '棉棉', '子轩', '安县令', '少恭', '陵容', '莫言', '豫津', '星尘',
        '情', '宁', '八', '华', '清', '昊', '梦回', '血暴', '鼎真', '爱', '野', '不败', '白', '隼', '森', '林', '焱', '风'])
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
        self.门派 = random.choice(self.world.门派)
        for i in self.world.地点:
            if self.门派 == i.地名:
                self.地点 = i
    def 产生称号(self):
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
        self.全名 = ''
        self.全名 += self.称号
        self.全名 += self.姓名
        if self.转世 != 1:
            self.全名 += f"\033[34m第{self.转世}世\033[0m"
    def 战斗力计算(self):
        a = self.先天资质 + self.后天资质 + 20
        b = 8 ** self.境界 * (6 + self.小境界)
        self.战斗力 = a * b
    def 突破(tar):
        r = random.randint(0, 100)
        p = tar.天命 + 1
        if r <= tar.成功率:  # 成功
            tar.影响力 += int(30 + tar.境界 * 180 + tar.小境界 + 18)
            tar.可突破 = 0
            tar.能量 -= tar.瓶颈
            tar.瓶颈 = int(300 + tar.境界 * 1800 + tar.小境界 + 180)
            tar.小境界 += 1
            if tar.小境界 == 10:
                tar.小境界 = 0
                tar.境界 += 1
                p += 1
            tar.计算成功率()
            tar.战斗力计算()
            tar.world.printj('经过不懈努力，' + tar.全名 + '突破到' + tar.world.境界[tar.境界] + '·' + tar.world.小境界[tar.小境界], [tar], p)
            tar.寿命 += 20 * tar.境界 + 20
            if tar.境界 == 2 and tar.小境界 == 0:
                tar.产生称号()
                p += 2
                tar.world.printj(f'天地感应，授予{tar.姓名}称号【{tar.称号}】', [tar], p)
                tar.全名计算()
            if tar.境界 == 9:
                p += 10
                tar.world.printj(f'{tar.全名}超脱天地，白日飞升！', [tar], p)
                tar.飞升()
        else:
            tar.能量 = int(tar.瓶颈 / 5)
            tar.可突破 = 0
            tar.成功率 += random.randint(5, 10)
            tar.world.printj(f'{tar.全名}突破{tar.world.境界[tar.境界]}·{tar.world.小境界[tar.小境界]}失败，散失大半灵气', [tar])
    def 飞升(src):
        src.world.人物.remove(src)
        src.world.飞升人物.append(src)
    def 转生(src):
        if src.world.cfg['转生'] == 1:
            src.world.add_one()
            tar = src.world.人物[-1]
            tar.姓名 = src.姓名
            tar.天命 = src.天命
            tar.拥有者 = src.拥有者
            tar.影响力 = int(src.影响力 / 2)
            tar.转世 = src.转世 + 1
            tar.全名计算()
            src.world.printj(f'神秘力量下{tar.姓名}转世重生', [src, tar])
    def 死亡(tar):
        tar.world.人物.remove(tar)
        tar.world.已故人物.append(tar)
        if tar.天命 == 1 or random.randint(0, 10) > 8:  # TODO 影响力决定
            tar.转生()
    def 记恨(self, tar):
        reason = random.choice(['长得漂亮','面目可憎','阴阳怪气','抢夺资源'])
        self.world.printj(f'{self.全名}因为{tar.全名}{reason}对其心生恨意', [self])
        self.仇人.append(tar)
    def 解愁(self):
        for tar in self.仇人:
            if tar not in self.world.人物:
                self.仇人.remove(tar)
                self.world.printj(f'{self.全名}突然发现自己的仇人{tar.全名}已经不在此界，心情舒畅', [self])
    def 寻仇(self):
        tar = random.choice(self.仇人)
        if self.战斗力 > tar.战斗力 * 1.2:
            mode = 0
        else:
            mode = 1
        if mode == 0:
            if tar in self.world.人物:
                self.world.printj(f'{self.全名}巧遇仇人{tar.全名}，对其大打出手', [self, tar])
                if self not in tar.仇人:
                    tar.仇人.append(self)
                self.world.战斗(self, tar, random.randint(0,2))
        elif mode == 1:
            if '散修' in self.门派:
                for py in self.world.人物:
                    if random.randint(0, 4) < 1 and tar not in py.仇人:
                        if random.randint(0, 12) < 1:
                            self.world.printj(f'{self.全名}对好友{py.全名}说了{tar.全名}的坏话，说服其出出手教训', [self, py])
                            self.world.战斗(py, tar, random.randint(1, 2))
                            for i in self,py:
                                if i not in tar.仇人:
                                    tar.仇人.append(i)
                        break
            else:
                for py in self.world.人物:
                    if random.randint(0, 4) < 1 and self.门派 == py.门派:
                        if tar not in py.仇人:
                            if random.randint(0, 9) == 0:
                                self.world.printj(f'{self.全名}对师长{py.全名}说了{tar.全名}的坏话，说服其出手教训', [self, py])
                                self.world.战斗(py, tar, random.randint(1,2))
                                for i in self, py:
                                    if i not in tar.仇人:
                                        tar.仇人.append(i)
                            break
    def 执行个人行为(tar):
        while len(tar.行动) == 0:  # TODO bug
            tar.行动.append('修炼')
        act = tar.行动.pop(0)
        if act == '修炼':
            tar.能量 += (tar.先天资质 + tar.后天资质) * tar.效率
            tar.world.printp('' + tar.姓名 + ' 修炼进度 ' + str(tar.能量) + '/' + str(tar.瓶颈) + '', -1)
        elif act == '闭关':
            tar.能量 += (tar.先天资质 + tar.后天资质) * tar.效率 * 1.5
            if len(tar.行动) > 0:
                if tar.行动[0] != '闭关':
                    tar.world.printp('' + tar.姓名 + ' 破关而出！修炼进度 ' + str(int(tar.能量)) + '/' + str(tar.瓶颈), 1)
        elif act == '突破':
            tar.突破()
        elif act == '恩怨':
            if len(tar.仇人) > 2:
                tar.寻仇()
            else:
                a = random.choice(tar.world.人物)
                if a != tar and a not in tar.仇人 and a != tar:
                    tar.记恨(a)
        elif act == '钓鱼':
            tmp = Item.Item()
            tmp.钓鱼(tar)
    def 生成个人行为(tar):
        if len(tar.行动) == 0:
            d = tar.world.个人事件分段
            r = random.randint(1, d[-1])
            nl = list(tar.world.个人事件权重.keys())
            for i in range(len(d) - 1):
                if d[i] < r <= d[i + 1]:
                    tmp = nl[i]
            if tmp == '闭关':
                for i in range(random.randint(6 + tar.境界, 24 + tar.境界)):
                    tar.行动.append('闭关')
                tar.world.printp('' + tar.姓名 + ' 有所感悟，开始闭关...', 1)
            else:
                tar.行动.append(tmp)
