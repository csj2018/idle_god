import src.NPC
import copy
import random

class Fight():
    def __init__(self, w = None):
        self.fid = 0
        self.进攻方 = []
        self.防守方 = []
        self.文本 = ''
        self.w = w

    def 生成战斗(self, 进攻方 = [], 防守方 = [], 尺度 = 15):
        dead = []
        for i in 进攻方+防守方:
            i.战斗力计算()
            if i in 进攻方:
                self.进攻方.append(copy.copy(i))
            else:
                self.防守方.append(copy.copy(i))

        self.文本 += f"    {self.w.time[1]}年{self.w.time[0]}月{random.randint(1, 28)}日 {random.choice(['夜', '深夜', '清晨', '正午'])} " \
                     f"{random.choice(['晴朗', '大雨', '暴雨'])}\n"

        while len(进攻方) > 0 and len(防守方) > 0:
            flag = 0
            src = random.choice(进攻方+防守方)
            if src in 进攻方:
                tar = random.choice(防守方)
            else:
                tar = random.choice(进攻方)
            zs = random.choice(src.招式)
            jsz = tar.体力 - src.战斗力
            limit = src.战斗力 * 尺度
            if jsz < limit:
                jsz = limit
                flag = 1
            self.文本 += f"{src.全名}突然发难，打出一招{zs}。"
            if jsz > 10 * src.战斗力:
                tar.体力 = jsz
                self.文本+=f"{tar.全名}全力抵挡，稳稳接下这招。\n"
            elif jsz > 0:
                if src.物品 != []:
                    bm = src.物品.pop(0)
                    self.文本 += f"危机之下,{tar.全名}从口袋中甩出一个{bm.名称}，硬生生承受住这次攻击!\n"
                else:
                    self.文本 += f"{tar.全名}被打得摇摇欲坠!\n"
                    tar.体力 =jsz
            elif jsz <= 0:
                flag = 1
                self.文本 += f"{tar.全名}被打得四分五裂\n!"
                dead.append(tar)
            if flag == 1:
                if tar in 进攻方:
                    进攻方.remove(tar)
                else:
                    防守方.remove(tar)
                if jsz > 10 * src.战斗力:
                    self.w.printj(
                        f'\033[31m【江湖恩怨】\033[0m{tar.全名}技不如人，在{tar.地点.地名}被{src.全名}用{zs}打败！（fid：{self.fid}）',
                        [tar, src], 2)
                elif jsz > 0:
                    self.w.printj(
                        f'\033[31m【江湖恩怨】\033[0m{tar.全名}技不如人，在{tar.地点.地名}被{src.全名}用{zs}打成重伤！（fid：{self.fid}）',
                        [tar, src], 2)
                else:
                    self.w.printj(
                        f'\033[31m【江湖恩怨】\033[0m{tar.全名}技不如人，在{tar.地点.地名}被{src.全名}用{zs}活活打死！（fid：{self.fid}）',
                        [tar, src], 2)
                if 进攻方 == [] or 防守方 == []:
                    break
                    return dead
