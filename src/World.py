import os, sys, traceback
import time

import src.NPC as NPC
import src.Event as Event
import src.Place as Place
import src.Item as Item
import src.Fight as Fight
import random, re, pickle
import copy

class World():
    def __init__(self):
        self.id = 0 #npc
        self.fid = 0
        self.战斗日志 = []
        self.cfg = {}
        self.event = Event.Event()
        self.境界 = ['炼气期', '筑基期', '金丹期', '元婴期', '出窍期', '分神期', '合体期', '渡劫期', '大乘期', ' 飞升']
        self.小境界 = ['一重天', '二重天', '三重天', '四重天', '五重天', '六重天', '七重天', '八重天', '九重天', '大圆满']
        self.地点 = []
        self.人物 = []
        self.已故人物 = []
        self.飞升人物 = []
        self.门派 = ['\033[32m散修\033[0m','\033[32m凌霄派\033[0m','\033[32m圣火门\033[0m','\033[32m玄天洞\033[0m','\033[32m魔门\033[0m']#TODO 增加
        self.事件 = 0
        self.世界事件权重 = {'新门派':2, '加人':12, '奇遇':5, '帮战':2, '无事':80}
        self.世界事件分段 = []
        self.个人事件权重 = {'修炼':80, '闭关':1, '行走':20, '恩怨':2, '钓鱼':1, '悟招':1}
        self.个人事件分段 = []
        self.run = 1
        self.time = [0, 1]
        self.END = 0
        self.历史 = ''
        self.水友 = []
        self.读取配置文件()
    def initial(self):
        for i in self.门派:
            tar = Place.Place(self)
            tar.绑定门派(i)
            self.地点.append(tar)
            if '散修' in i:
                tar.地名 = '\033[33m成都\033[0m'
        for i in range(10):
            p = Place.Place(self)
            p.产生地点(jj=random.randint(0,len(self.境界)-1))
        if self.cfg['NPC'] == 1:
            for i in range(20):
                tmp = NPC.NPC(self)
                tmp.初始化()
                self.人物.append(tmp)
        if self.cfg['qy'] == 1:
            with open('qy.ini', encoding='UTF-8') as f:
                n = f.read()
                l = n.split(' ')
            for name in l:
                tmp = NPC.NPC(self)
                tmp.初始化()
                tmp.姓名 = f'\033[35m{name}\033[0m'
                tmp.天命 = 1
                tmp.转世 = 1
                tmp.全名计算()
                self.人物.append(tmp)
                tmp.历史 = f"大造化将{tmp.姓名}投入这一方小世界中\n"
                self.printj(f"大造化将{tmp.姓名}投入这一方小世界中\n", tar=[self, tmp], key_gui=1)
    def add_one(self):
        tmp = NPC.NPC(self)
        tmp.初始化()
        self.人物.append(tmp)
        return tmp
    def 增加蛐蛐(self, name, owner):
        tmp = NPC.NPC(self)
        tmp.初始化()
        tmp.姓名 = f'\033[35m{name}\033[0m'
        tmp.天命 = 1
        tmp.转世 = 1
        tmp.拥有者 = owner
        tmp.全名计算()
        self.人物.append(tmp)
        tmp.历史 = f"大造化将{tmp.姓名}投入这一方小世界中\n"
        self.printj(f"大造化将{tmp.姓名}投入这一方小世界中\n", tar = [self, tmp], key_gui=1)
    def dzqq(self):
        a = []#
        p = ''
        for i in a:
            tmp = NPC.NPC(self)
            tmp.初始化()
            tmp.姓名 = f'\033[35m{i}\033[0m'
            tmp.天命 = 1
            tmp.转世 = 1
            tmp.全名计算()
            self.人物.append(tmp)
            p += f"大造化将{tmp.姓名}投入这一方小世界中\n"
        return p
    def 成立门派(self):
        a = random.choice(['星云','天河','昆仑','崆峒','元华','墨佬','化生','乾坤', '天剑', '九星'])
        b = random.choice(['谷','洞','派','山','宗','门'])
        temp = f'\033[32m{a+b}\033[0m'
        while 1:
            if temp not in self.门派:
                break

        self.排天榜()
        for tar in self.人物:
            if tar.境界 > 2 and random.randint(0, 11) < 2:
                self.printj(f'{tar.全名}决定开宗立派成立{temp}', tar=[self, tar], p=6)
                self.门派.append(temp)
                a = Place.Place(self)
                a.绑定门派(temp)
                self.地点.append(a)
                tar.门派 = temp

                for tar in self.人物:
                    if '散修' in tar.门派 and random.randint(0, 11) < 2:
                        tar.门派 = temp
                        self.printj(f'散修{tar.全名}厌倦了孤身一人，决定加入{temp}', tar=[tar], p=4)

                for i in range(3):
                    tmp = NPC.NPC(self)
                    tmp.初始化()
                    tmp.门派 = temp
                    self.人物.append(tmp)
                break
    def 排天榜(self):
        #def x(a =NPC()):
        #    return a.战斗力
        #self.人物.sort(key = x, reverse=True)
        self.人物.sort(key = lambda x: x.战斗力, reverse = True)
    def printm(self, a):
        if self.cfg['副窗口'] == 1:
            with open('output.tmp', 'w+', encoding='utf-8') as f:
                f.write(str(a))
    def printj(self, c, tar=[], p=0, key_gui=0):
        self.printp(c, p, key_gui)
        for i in tar:
            i.历史 += str(self.time[1]) + '年' + str(self.time[0]) + '月 ' + c + '\n'
    def printp(self, c, p=100, key_gui=0):  # 优先级
        if key_gui == 1:
            self.printm(c)
        if self.cfg['打印等级'] <= p:
            print(c)
    def 寿命检测(self):
        for tar in self.人物:
            tar.年龄 += 1
            if tar.年龄 > tar.寿命:
                self.printj(tar.全名 + '寿终正寝', tar)
                tar.死亡()
    def 读取配置文件(self):
        with open('config.ini', encoding='utf-8') as f:
            data = f.read()
        dl = data.split('\n')
        for i in dl:
            tmp = i.split(' ')
            if '#' not in i:
                try:
                    self.cfg[tmp[0]] = int(tmp[1])
                except:
                    self.cfg[tmp[0]] = tmp[1]
        tmp = self.世界事件权重.keys()
        for i in tmp:
            self.世界事件权重[i] = self.cfg[i]
        tmp = self.个人事件权重.keys()
        for i in tmp:
            self.个人事件权重[i] = self.cfg[i]
    def 生成个人行为(self):
        for tar in self.人物:
            tar.生成个人行为()
    def 执行个人行为(self):
        for tar in self.人物:
            tar.执行个人行为()
    def 生成世界行为(self):
        d = self.世界事件分段
        r = random.randint(1, d[-1])
        nl = list(self.世界事件权重.keys())
        for i in range(len(d) - 1):
            if d[i] < r <= d[i + 1]:
                tmp = nl[i]
        if tmp == '加人' and len(self.人物) < self.cfg['人数限制'] and self.cfg['NPC'] == 1:
            tmp = self.add_one()
            self.printj('机缘巧合，凡人' + tmp.姓名 + '踏入修炼一途，拜入' + tmp.门派, [tmp], 1)
        elif tmp == '新门派' and len(self.门派) < 10:
            self.成立门派()
        elif tmp == '奇遇' and self.事件 == 0:
            self.事件 = 1
            self.event.random()
            print(str(self.event.开始) + '个月后发生奇遇' + str(self.event.名称) + '!')
            for tar in self.人物:
                xd = len(tar.行动)
                if xd <= self.event.开始 and random.randint(0, 2):
                    for j in range(self.event.开始 - xd + 1):
                        tar.行动.append('修炼')
                    for j in range(self.event.结束 - self.event.开始):
                        tar.行动.append('事件')
        elif tmp == '帮战' and len(self.门派) > 2:
            self.帮战()
    def 帮战(self):
        while 1:
            a = random.choice(self.门派)
            b = random.choice(self.门派)
            if a != b and '散修' not in a and '散修' not in b:
                break
        lista = []
        listb = []
        规模 = random.randint(3,10)
        毁灭 = random.randint(0,6)
        for i in self.地点:
            if i.门派 == b:
                dd = i
                break
        for src in self.人物:
            if src.门派 == a and (len(lista) < 规模 or 毁灭 == 6):
                lista.append(src)
                src.行动 = ['帮战'] + src.行动
                src.移动(dd)
            if src.门派 == b and (len(listb) < 规模 or 毁灭 == 6):
                listb.append(src)
                src.行动 = ['帮战'] + src.行动
                src.移动(dd)
        try:
            if 毁灭 != 6:
                self.printj(f'{a}对{b}发起帮派战争(fid: {self.fid})', tar=lista + listb + [self], p=3)
                self.新战斗(lista, listb, 15, -4)
            else:
                self.printj(f'{a}对{b}发起帮派毁灭战争(fid: {self.fid})', tar=lista + listb + [self], p=3)
                self.新战斗(lista, listb, -2, -4)
                if lista == []:
                    self.printj(f'{a}覆灭了', tar=[self], p=3)
                elif listb == []:
                    self.printj(f'{b}覆灭了', tar=[self], p=3)
        except Exception as e:
            self.printp("门派战斗出错，请查看debug.log", key_gui=1)
            debug_data = f'{e}\n{sys.exc_info()}\n{traceback.print_exc()}\n{traceback.format_exc()}'
            with open('debug.log', 'w+') as f:
                f.write(debug_data)
    def 配置世界事件(self):
        tar = self.世界事件权重
        all = 0
        self.世界事件分段 = [0]
        for i in tar.values():
            all += i
            self.世界事件分段.append(all)
    def 配置个人事件(self):
        tar = self.个人事件权重
        all = 0
        self.个人事件分段 = [0]
        for i in tar.values():
            all += i
            self.个人事件分段.append(all)
    def world_events(self):
        if self.事件 == 1:
            self.event.开始 -= 1
            self.event.结束 -= 1
            if self.event.开始 == 0:
                self.printp('' + self.event.名称 + '开始了！', 1)
            if self.event.结束 == 0:
                self.事件 = 0
                self.printp('' + self.event.名称 + '结束了！', 1)
                for tar in self.人物:
                    if len(tar.行动) > 0:
                        if tar.行动[0] == '事件':
                            tar.后天资质 += random.randint(1, 5)
                            if tar.后天资质 >= 3 * tar.先天资质 * tar.境界 + 30:
                                tar.后天资质 = 3 * tar.先天资质 * tar.境界 + 30
                                # print(''+tar.称号+''+tar.姓名+'后天资质提升至境界极限！')
                            else:
                                self.printp(tar.全名 + '后天资质提升！', 1)
    def random_events(self):
        self.生成世界行为()
        self.检查突破()
        self.生成个人行为()
        self.执行个人行为()
        self.world_events()
    def 清理死人(self):
        while len(self.已故人物) > self.cfg['人数限制']:
            self.已故人物.pop(0)
    def 天道检验(self):
        if self.time[1] % self.cfg['天道检验'] == 0 and self.time[0] == 2:
            if len(self.人物) > 30:
                self.排天榜()
                self.printj(f'修仙历{self.time[1]}年，修仙百晓生发布天榜排名：', [self], 10)
                num = 1
                for tar in self.人物:
                    tar.影响力 += 15 - num
                    self.printj(f'{tar.门派}{tar.全名}当选天榜第{num}名', [tar, self], 10)
                    if num == 10:
                        break
                    num += 1
            self.清理死人()
        if self.time[1] % 3 == 0 and self.time[0] == 8:
            for tar in self.人物:
                tar.解愁()
    def 检查突破(self):
        for tar in self.人物:
            if tar.能量 >= tar.瓶颈 and tar.可突破 == 0:
                tar.可突破 = 1
                tar.行动.append('突破')
    def loop(self):
        self.time[0] += 1
        if self.time[0] == 13:
            self.time[1] += 1
            self.time[0] = 1
            self.寿命检测()
        self.printp(str(self.time[1]) + '年' + str(self.time[0]) + '月', 6)
        self.天道检验()
        self.random_events()
    def 战斗(self, a, b, c=0):
        总战斗力 = a.战斗力 + b.战斗力
        if random.randint(1, 总战斗力) <= a.战斗力:  # a win
            s = a
            f = b
        else:
            s = b
            f = a
        if c == 0:  # 0杀 1重 2轻 3切磋 4指导
            self.printj(f'\033[31m【江湖恩怨】\033[0m{f.全名}技不如人，在{s.地点.地名}被{s.全名}用{random.choice(s.招式)}活活打死！', [f, s], 2)
            f.死亡()
            return f
        elif c == 1:
            f.寿命 -= 10 * f.境界
            if f.小境界 > 0:
                f.小境界 -= 1
            elif f.境界 > 0:
                f.境界 -= 1
                f.小境界 = 9
            # TODO
            self.printj(f'\033[31m【江湖恩怨】\033[0m{f.全名}技不如人，在{s.地点.地名}被{s.全名}用{random.choice(s.招式)}打成重伤，境界跌落！', [f, s], 2)
        elif c == 2:
            f.能量 == 0
            self.printj(f'\033[31m【江湖恩怨】\033[0m{f.全名}技不如人，在{s.地点.地名}被{s.全名}用{random.choice(s.招式)}打成轻伤！', [f, s], 2)
        elif c == 3:
            self.printj(f'\033[31m【江湖恩怨】\033[0m{f.全名}技不如人，在{s.地点.地名}被{s.全名}用{random.choice(s.招式)}打败！', [f, s], 2)
    def 新战斗(self, 进攻方 =[], 防守方 = [], max = 20, min = 10):
        f = Fight.Fight(self)
        f.fid = self.fid
        self.fid += 1
        dead = f.生成战斗(进攻方, 防守方, max, min)
        self.战斗日志.append(f)
        if dead != None:
            for i in dead:
                i.死亡()
    def save(world):
        data = world
        f = open('save.pckl', 'wb')
        pickle.dump(data, f)
        f.close()
    def load(world):
        f = open('save.pckl', 'rb')
        data = pickle.load(f)
        f.close()
        #world = data
        world.time = data.time
        world.人物 = data.人物
        world.已故人物 = data.已故人物
        world.飞升人物 = data.飞升人物
        world.门派 = data.门派
        world.事件 = data.事件
        world.历史 = data.历史
        world.世界事件分段 = data.世界事件分段
        world.世界事件权重 = data.世界事件权重
        world.event = data.event
        world.水友 = data.水友
    def 列出所有人(world, staute=0):
        data = ''
        ns = 0
        if staute == 0:  # 如果状态为0，即已故人数
            tmpl = world.已故人物
        elif staute == 1:  # 如果状态为1，即未飞升人数
            tmpl = world.人物
        else:  # 如果状态为其他，即飞升人数
            tmpl = world.飞升人物
        num = 0
        for tar in tmpl:
            data += f'{num} {tar.全名}  '
            num += 1
        world.printp(data, key_gui=1)  # 输出data
    def 查看属性(world, tar):
        data = (f'【名号】：{tar.全名}\n'
                f'【年龄】：{tar.年龄}/{tar.寿命}\n'
                f'【门派】：{tar.门派} 【地点】： {tar.地点.地名}\n'
                f'【境界】：{world.境界[tar.境界]}·{world.小境界[tar.小境界]}\n'
                f'【体质】：{tar.体质}【先天】{tar.先天资质} 【后天】{tar.后天资质}\n'
                f'【战斗力】：{tar.战斗力} 【影响力】：{tar.影响力}\n'
                f'【绝学】： {tar.招式[-1]}\n'
                f'【转世】：{tar.转世}  【唯一id】：{tar.id}\n'
                f'【修炼进度】：{int(tar.能量)}/{tar.瓶颈}')
        if tar.拥有者 != '':
            data += f'\n【拥有者】: {tar.拥有者}'
        data += f'\n【随身物品】：'
        for i in tar.物品:
            data += f' {i.名称}'
        data += f'\n【仇人】：'
        for i in tar.仇人:
            data += f' {i.全名}'
        world.printp(data, key_gui=1)
    def 查看历史(world, tar):
        world.printp(tar.历史, key_gui=1)
    def act_cmd(world, cmd, local=0, owner='', gui=0):
        try:
            if world.run == 1 and cmd == '' or cmd == 'zt':
                world.run = 0
                world.printp('暂停', key_gui=1)
            elif world.run == 0 and cmd == '' or cmd == 'jx':
                world.run = 1
                world.printp('继续', key_gui=1)
            # //TODO 二次输入
            elif re.match('dzqq', cmd) != None:
                p = world.dzqq()
                world.printj(p, key_gui=gui)
            elif re.match('qq', cmd) != None:
                name = re.split(' ', cmd)[1]
                world.增加蛐蛐(name, owner)
            elif re.match('addone', cmd) != None:
                tmp = world.add_one()
                world.printj('机缘巧合，凡人' + tmp.姓名 + '踏入修炼一途，拜入' + tmp.门派, [tmp])
            elif re.match('pk', cmd) != None:
                if local == 1:
                    tmp = re.split(' ', cmd)
                    a = int(tmp[1])
                    b = int(tmp[2])
                    c = int(tmp[3])
                    for i in world.人物:
                        if a == i.id:
                            aa = i
                        if b == i.id:
                            bb = i
                    world.战斗(aa, bb, c)
            elif cmd == 'save':
                if local == 1:
                    world.save()
                    world.printp("存储成功", key_gui=1)
                else:
                    world.printp("权限不足", key_gui=1)
            elif cmd == 'load':
                if local == 1:
                    world.load()
                    world.printp("读取成功", key_gui=1)
                else:
                    world.printp("权限不足", key_gui=1)
            elif re.match('ck', cmd) != None:
                world.cmd_ck(cmd, owner)
            elif re.match('sh', cmd) != None:
                world.cmd_search(cmd, owner)
            elif re.match('ls', cmd) != None:
                world.cmd_ls(cmd, owner)
            elif re.match('ljj', cmd) != None:
                data = ''
                if ' ' not in cmd:
                    cnt = 0
                    for i in range(len(world.境界) - 1):
                        count = 0
                        for j in world.人物:
                            if j.境界 == i:
                                count += 1
                        data += f'{cnt} {world.境界[i]} {count}人 \n'
                        cnt += 1
                    data += f'{cnt} {world.境界[-1]} {len(world.飞升人物)}人'
                    world.printp(data, key_gui=1)
                else:
                    aa = int(re.split(' ', cmd)[1])
                    c = 0
                    if aa == len(world.境界) - 1:
                        for tar in world.飞升人物:
                            data += f'{c} {tar.全名}  '
                            c += 1
                    else:
                        for tar in world.人物:
                            if tar.境界 == aa:
                                data += f'{c} {tar.全名}  '
                                c += 1
                    world.printp(data, key_gui=1)
            elif re.match('lmp', cmd) != None:
                data = ''
                if ' ' not in cmd:
                    i = 0
                    for mp in world.门派:
                        count = 0
                        for r in world.人物:
                            if mp == r.门派:
                                count += 1
                        data += f'{i} {mp} {count}人  '
                        i += 1
                    world.printp(data, key_gui=1)
                else:
                    aa = int(re.split(' ', cmd)[1])
                    c = 0
                    for tar in world.人物:
                        if world.门派[aa] == tar.门派:
                            data += f'{c} {tar.全名}  '
                            c += 1
                    world.printp(data, key_gui=1)
            elif re.match('ptb', cmd) != None:
                world.排天榜()
            elif re.match('lcfg', cmd) != None:
                if local == 1:
                    world.printp(world.cfg, key_gui=1)
            elif re.match('ccfg', cmd) != None:
                if local == 1:
                    aa = re.split(' ', cmd)
                    world.cfg[aa[1]] = int(aa[2])
                    if aa[1] in world.世界事件权重:
                        world.世界事件权重[aa[1]] = int(aa[2])
                    world.配置世界事件()
                    if aa[1] in world.个人事件权重:
                        world.个人事件权重[aa[1]] = int(aa[2])
                    world.配置个人事件()
            elif re.match('push', cmd) != None:
                if local == 1:
                    aa = int(re.split(' ', cmd)[1])
                    tmp_state = world.run
                    world.run = 0
                    world.cfg['打印等级'] += 10
                    for i in range(aa * 12):
                        world.loop()
                    world.cfg['打印等级'] -= 10
                    world.run = tmp_state
                    world.printp(f"世界外伟力推动下时光快速流逝，不知不觉已过{aa}载！", key_gui=1)
            elif re.match('改名', cmd) != None:
                tmp = re.split(' ', cmd)
                for tar in world.人物:
                    if owner == tar.拥有者 and owner != '':
                        tar.姓名 = f'\033[35m{tmp[1]}\033[0m'
                        tar.全名计算()
                        world.printp('改名成功', key_gui=1)
                        break
            elif re.match('clr', cmd) != None:
                os.system("cls")
            else:
                world.printp("无效命令：未识别的命令", key_gui=1)
        except Exception as e:
            world.printp("命令执行出错，请查看debug.log", key_gui=1)
            debug_data = f'{e}\n{sys.exc_info()}\n{traceback.print_exc()}\n{traceback.format_exc()}'
            with open('debug.log','w+') as f:
                f.write(debug_data)
    def cmd_ck(world, cmd, owner):
        if re.match('ckm', cmd) != None:
            if 'ckma' in cmd:
                for tar in world.人物:
                    if tar.拥有者 == owner:
                        world.查看属性(tar)
                        break
        elif re.match('ckd', cmd) != None:
            if ' ' not in cmd:
                world.列出所有人(0)
            else:
                aa = int(re.split(' ', cmd)[1])
                tar = world.已故人物[aa]
                world.查看属性(tar)
        elif re.match('cka', cmd) != None:
            if ' ' not in cmd:
                world.列出所有人(1)
            else:
                aa = int(re.split(" ", cmd)[1])
                tar = world.人物[aa]
                world.查看属性(tar)
        elif re.match('ckf', cmd) != None:
            if ' ' not in cmd:
                world.列出所有人(2)
            else:
                aa = int(re.split(" ", cmd)[1])
                tar = world.飞升人物[aa]
                world.查看属性(tar)
        elif re.match('ckid', cmd) != None:
            id = int(cmd.split(' ')[1])
            for tar in world.人物+world.已故人物+world.飞升人物:
                if tar.id == id:
                    world.查看属性(tar)
                    break
        elif re.match('ckw', cmd) != None:
            data = '已有地点：'
            for i in world.地点:
                data += f" {i.地名}"
            world.printp(data, key_gui=1)
        elif re.match('ckzd', cmd) != None:
            fid = int(cmd.split(' ')[1])
            for tar in world.战斗日志:
                if tar.fid == fid:
                    world.printp(tar.文本, key_gui=1)
                    break
    def cmd_search(world, cmd, owner):
        if 'shid' in cmd:
            mz = cmd.split(' ')[1]
            tmp = ''
            for tar in world.人物+world.已故人物+world.飞升人物:
                if mz in tar.全名:
                    tmp+= f"{tar.全名} ID:{tar.id}\n"
            world.printp(tmp, key_gui=1)
    def cmd_ls(world, cmd, owner):
        if re.match('lsm', cmd) != None:
            if 'lsma' in cmd:
                for tar in world.人物:
                    if tar.拥有者 == owner:
                        world.查看历史(tar)
                        break
        elif re.match('lsd', cmd) != None:
            aa = int(re.split(' ', cmd)[1])
            tar = world.已故人物[aa]
            world.查看历史(tar)
        elif re.match('lsa', cmd) != None:
            aa = int(re.split(' ', cmd)[1])
            tar = world.人物[aa]
            world.查看历史(tar)
        elif re.match('lsf', cmd) != None:
            aa = int(re.split(' ', cmd)[1])
            tar = world.飞升人物[aa]
            world.查看历史(tar)
        elif re.match('lsw', cmd) != None:
            world.查看历史(world)
        elif re.match('lsid', cmd) != None:
            id = int(cmd.split(' ')[1])
            for tar in world.人物+world.已故人物+world.飞升人物:
                if tar.id == id:
                    world.查看历史(tar)
                    break