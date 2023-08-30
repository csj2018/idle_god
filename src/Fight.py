import src.NPC
import copy
import random

class Fight():
    def __init__(self, w = None):
        self.fid = 0
        self.进攻方 = []
        self.防守方 = []
        self.文本 = ''
        self.简报 = ''
        self.w = w

    def 生成战斗(self, 进攻方 = [], 防守方 = [], max = 15, min = 15, 原因 = '', 地点 = None):
        dead = []
        for i in 进攻方+防守方:
            if 地点 != None:
                i.移动(地点)
            i.战斗力计算()
            i.outline = random.randint(min, max)
            if i in 进攻方:
                self.进攻方.append(copy.copy(i))
            else:
                self.防守方.append(copy.copy(i))
        if 原因 != '':
            self.文本 += f"【前情提要】 {原因}\n"
        self.文本 += f"    {self.w.time[1]}年{self.w.time[0]}月{random.randint(1, 28)}日 {random.choice(['夜', '深夜', '清晨', '正午'])} " \
                     f"{random.choice(['晴朗', '大雨', '暴雨'])}\n    进攻方："
        for i in 进攻方:
            self.文本+= f' {i.全名}'
        self.文本 += f'\n大战\n    防守方：'
        for i in 防守方:
            self.文本+= f' {i.全名}'
        self.文本 += '\n'
        self.简报 = self.文本

        while len(进攻方) > 0 and len(防守方) > 0:
            flag = 0
            src = random.choice(进攻方+防守方)
            if src in 进攻方:
                tar = random.choice(防守方)
            else:
                tar = random.choice(进攻方)
            zs = random.choice(src.招式)
            jsz = tar.体力 - src.战斗力
            limit = tar.战斗力 * tar.outline
            if jsz < limit:
                jsz = limit
                flag = 1
            #构建出招
            走位 = random.choice([
                f"{src.全名}突然发难，",
                f"只见{src.全名}跃上半空，",
                f"{src.全名}猛地爆退开去，",
                f"{src.全名}脚下踩着玄奥的步伐，",
                f"突然间天空卷起风沙{src.全名}的身形若隐若现，"
            ])
            起手 = random.choice([
                f"他双手虚握，于虚空中凝聚出一招{zs}向前爆射而去！",
                f"右手打出一道{zs}闪电般冲向前方！",
                f"袖口中甩出三道咒文，召唤出一记{zs}！"
            ])
            self.文本 += 走位+起手
            if jsz > 18 * tar.战斗力:
                tar.体力 = jsz
                self.文本 += f"猛烈的攻击甚至没有掀动{tar.全名}的衣角。(-{src.战斗力}/{jsz})\n"
            elif jsz > 14 * tar.战斗力:
                self.文本 += f"{tar.全名}随手接下。(-{src.战斗力}/{jsz})\n"
                tar.体力 = jsz
            elif jsz > 10 * tar.战斗力:
                self.文本 += f"{tar.全名}全力运转护体真气抵挡。(-{src.战斗力}/{jsz})\n"
                tar.体力 = jsz
            elif tar.物品 != []:
                bm = tar.物品.pop(0)
                flag = 0
                self.文本 += f"危机之下,{tar.全名}从口袋中甩出一个{bm.名称}，硬生生承受住这次攻击！\n"
                self.简报 += f"{tar.全名}的{bm.名称}被击碎\n"
            elif jsz > 5 * tar.战斗力:
                self.文本 += f"{tar.全名}吐出一口鲜血，护体真气已薄不可见！(-{src.战斗力}/{jsz})\n"
                tar.体力 = jsz
            elif jsz > 0:
                self.文本 += f"{tar.全名}胡乱的抵挡，已经是摇摇欲坠！(-{src.战斗力}/{jsz})\n"
                tar.体力 = jsz
            elif jsz <= 0:
                flag = 1
                self.文本 += f"{tar.全名}被打得粉碎！(-{src.战斗力}/{jsz})\n"
                dead.append(tar)
            if flag == 1:
                if tar in 进攻方:
                    进攻方.remove(tar)
                else:
                    防守方.remove(tar)
                if jsz > 10 * src.战斗力:
                    self.w.printj(
                        f'\033[31m【江湖恩怨】\033[0m{tar.门派}{tar.全名}技不如人，在{tar.地点.地名}被{src.门派}{src.全名}用{zs}打败！（fid：{self.fid}）',
                        [tar, src], 2)
                    self.简报 += f'{tar.门派}{tar.全名}技不如人，在{tar.地点.地名}被{src.门派}{src.全名}用{zs}打败！\n'
                    src.业障 += 1
                elif jsz > 0:
                    self.w.printj(
                        f'\033[31m【江湖恩怨】\033[0m{tar.门派}{tar.全名}技不如人，在{tar.地点.地名}被{src.门派}{src.全名}用{zs}打成重伤！（fid：{self.fid}）',
                        [tar, src], 2)
                    self.简报 += f'{tar.门派}{tar.全名}技不如人，在{tar.地点.地名}被{src.门派}{src.全名}用{zs}打成重伤！\n'
                    tar.降级()
                    src.业障 += 2
                else:
                    self.w.printj(
                        f'\033[31m【江湖恩怨】\033[0m{tar.门派}{tar.全名}技不如人，在{tar.地点.地名}被{src.门派}{src.全名}用{zs}活活打死！（fid：{self.fid}）',
                        [tar, src], 2)
                    self.简报 += f'{tar.门派}{tar.全名}技不如人，在{tar.地点.地名}被{src.门派}{src.全名}用{zs}活活打死！\n'
                    src.业障 += 5
                    tar.死亡()
                if 进攻方 == [] or 防守方 == []:
                    break
                    return dead
