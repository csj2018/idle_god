import os, sys, traceback
import time

import src.NPC as NPC
import src.Event as Event
import random, re, pickle

class World():
    def __init__(self):
        self.id = 0 #npc
        self.cfg = {}
        self.event = Event.Event()
        self.境界 = ['炼气期', '筑基期', '金丹期', '元婴期', '出窍期', '分神期', '合体期', '渡劫期', '大乘期', ' 飞升']
        self.小境界 = ['一重天', '二重天', '三重天', '四重天', '五重天', '六重天', '七重天', '八重天', '九重天', '大圆满']
        self.人物 = []
        self.人数 = 0
        self.已故人物 = []
        self.已故人数 = 0
        self.飞升人物 = []
        self.飞升人数 = 0
        self.门派 = ['\033[32m散修\033[0m','\033[32m凌霄派\033[0m','\033[32m圣火门\033[0m','\033[32m玄天洞\033[0m','\033[32m魔门\033[0m']#TODO 增加
        self.地点 = ['古战场']
        self.事件 = 0
        #self.随机事件权重 = [['加人',12],['恩怨',10],['奇遇',5],['帮战',2],['无事',80]]
        self.随机事件权重 = {'新门派':2,'加人':12,'恩怨':10,'奇遇':5,'帮战':2,'无事':80}
        self.随机事件分段 = []
        self.run = 1
        self.time = [0, 1]
        self.END = 0
        self.历史 = ''
        self.水友 = []
        self.读取配置文件()
    def initial(self):
        for i in range(20):
            tmp = NPC.NPC(self)
            tmp.creat_random_npc()
            tmp.门派 = random.choice(self.门派)
            self.人物.append(tmp)
            self.人数 += 1
    def add_one(self):
        self.人数 += 1
        tmp = NPC.NPC(self)
        tmp.creat_random_npc()
        self.人物.append(tmp)
        return tmp
    def 增加蛐蛐(self, name, owner):
        self.人数 += 1
        tmp = NPC.NPC(self)
        tmp.creat_random_npc()
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
        self.人数 += len(a)
        for i in a:
            tmp = NPC.NPC(self)
            tmp.creat_random_npc()
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
                tar.门派 = temp

                for tar in self.人物:
                    if '散修' in tar.门派 and random.randint(0, 11) < 2:
                        tar.门派 = temp
                        self.printj(f'散修{tar.全名}厌倦了孤身一人，决定加入{temp}', tar=[tar], p=4)

                for i in range(3):
                    self.人数 += 1
                    tmp = NPC.NPC(self)
                    tmp.creat_random_npc()
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
            with open('output.tmp', 'w+') as f:
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
            try:
                self.cfg[tmp[0]] = int(tmp[1])
            except:
                self.cfg[tmp[0]] = tmp[1]
        tmp = self.随机事件权重.keys()
        for i in tmp:
            self.随机事件权重[i] = self.cfg[i]
    def create_npc_actions(self):
        for tar in self.人物:
            while len(tar.行动) <= 1:
                r = random.randint(0, 100)
                if r <= 93:
                    tar.行动.append('修炼')
                elif r <= 100:
                    for i in range(random.randint(6 + tar.境界, 24 + tar.境界)):
                        tar.行动.append('闭关')
    def do_actions(self):
        for tar in self.人物:
            act = tar.行动[1]
            if act == '修炼':
                tar.能量 += (tar.先天资质 + tar.后天资质) * tar.效率
                self.printp('' + tar.姓名 + ' 修炼进度 ' + str(tar.能量) + '/' + str(tar.瓶颈) + '', -1)
            elif act == '闭关':
                tar.能量 += (tar.先天资质 + tar.后天资质) * tar.效率 * 1.5
                if tar.行动[0] != '闭关':
                    self.printp('' + tar.姓名 + ' 有所感悟，开始闭关...', 1)
                if len(tar.行动) > 2:
                    if tar.行动[2] != '闭关':
                        self.printp('' + tar.姓名 + ' 破关而出！修炼进度 ' + str(int(tar.能量)) + '/' + str(tar.瓶颈), 1)
                if len(tar.行动) == 2:
                    self.printp(tar.姓名 + ' 破关而出！修炼进度 ' + str(int(tar.能量)) + '/' + str(tar.瓶颈), 1)
            elif act == '突破':
                tar.突破()
            tar.行动.pop(0)
    def create_world_events(self):
        d = self.随机事件分段
        r = random.randint(1, d[-1])
        nl = list(self.随机事件权重.keys())
        for i in range(len(d) - 1):
            if d[i] < r <= d[i + 1]:
                tmp = nl[i]
        if tmp == '加人' and self.人数 < self.cfg['人数限制']:
            tmp = self.add_one()
            self.printj('机缘巧合，凡人' + tmp.姓名 + '踏入修炼一途，拜入' + tmp.门派, [tmp], 1)
        elif tmp == '新门派' and len(self.门派) < 10:
            self.成立门派()
        elif tmp == '恩怨' and self.人数 > 6:
            a = random.choice(self.人物)
            while 1:
                b = random.choice(self.人物)
                if a != b:
                    break
            self.战斗(a, b, random.randint(0, 4))
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
            while 1:
                a = random.choice(self.门派)
                b = random.choice(self.门派)
                if a != b and '散修' not in a and '散修' not in b:
                    break
            self.printp(a + '对' + b + '发起帮派战争', 3)
            try:
                for i in range(random.randint(4, 12)):
                    counta = 0
                    countb = 0
                    lista = []
                    listb = []
                    for i in self.人物:
                        if a in i.门派:
                            counta += 1
                            lista.append(i)
                        if b in i.门派:
                            countb += 1
                            listb.append(i)
                    self.战斗(random.choice(lista), random.choice(listb), random.randint(0, 1))
            except:
                counta = 0
                countb = 0
                for i in self.人物:
                    if a in i.门派:
                        counta += 1
                    if b in i.门派:
                        countb += 1
                if counta == 0:
                    c = a
                if countb == 0:
                    c = b
                try:
                    self.printp(c + '惨遭灭门！', 4)
                    self.门派.pop(self.门派.index(c))
                except Exception as e:
                    self.printp("门派战斗出错，请查看debug.log", key_gui=1)
                    debug_data = f'{e}\n{sys.exc_info()}\n{traceback.print_exc()}\n{traceback.format_exc()}'
                    with open('debug.log', 'w+') as f:
                        f.write(debug_data)
    def config_world_events(self):
        tar = self.随机事件权重
        all = 0
        self.随机事件分段 = [0]
        for i in tar.values():
            all += i
            self.随机事件分段.append(all)
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
                    if tar.行动[0] == '事件':
                        tar.后天资质 += random.randint(1, 5)
                        if tar.后天资质 >= 3 * tar.先天资质 * tar.境界 + 30:
                            tar.后天资质 = 3 * tar.先天资质 * tar.境界 + 30
                            # print(''+tar.称号+''+tar.姓名+'后天资质提升至境界极限！')
                        else:
                            self.printp(tar.全名 + '后天资质提升！', 1)
    def random_events(self):
        self.create_world_events()
        self.check_state()
        self.create_npc_actions()
        self.do_actions()
        self.world_events()
    def 清理死人(self):
        while self.已故人数 > self.cfg['人数限制']:
            self.已故人数 -= 1
            self.已故人物.pop(0)
    def 天道检验(self):
        if self.time[1] % self.cfg['天道检验'] == 0 and self.time[0] == 2:
            if self.人数 > 30:
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
    def check_state(self):
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
            self.printj('【江湖仇杀】' + f.全名 + '技不如人，被'
                   + s.全名 + '斩杀！', [f, s], 2)
            f.死亡()
        elif c == 1:
            f.寿命 -= 10 * f.境界
            if f.小境界 > 0:
                f.小境界 -= 1
            elif f.境界 > 0:
                f.境界 -= 1
                f.小境界 = 9
            # TODO
            self.printj('【江湖恩怨】' + f.全名 + '技不如人，被'
                   + s.全名 + '打成重伤，境界跌落!', [f, s])
        elif c == 2:
            f.能量 == 0
            self.printj('【江湖恩怨】' + f.全名 + '技不如人，被'
                   + s.全名 + '打成轻伤!', [f, s])
        elif c == 3:
            self.printj('【江湖切磋】' + f.全名 + '技不如人，被'
                   + s.全名 + '击败!', [f, s])
        elif c == 4:
            f.能量 += f.瓶颈 / 4
            self.printj('【江湖指导】' + f.全名 + '受'
                   + s.全名 + '点拨，修为大进!', [f, s])
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
        world.人数 = data.人数
        world.人物 = data.人物
        world.已故人数 = data.已故人数
        world.已故人物 = data.已故人物
        world.飞升人数 = data.飞升人数
        world.飞升人物 = data.飞升人物
        world.门派 = data.门派
        world.事件 = data.事件
        world.历史 = data.历史
        world.随机事件分段 = data.随机事件分段
        world.随机事件权重 = data.随机事件权重
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
                f'【门派】：{tar.门派}\n'
                f'【境界】：{world.境界[tar.境界]}·{world.小境界[tar.小境界]}\n'
                f'【体质】：{tar.体质}【先天】{tar.先天资质} 【后天】{tar.后天资质}\n'
                f'【战斗力】：{tar.战斗力} 【影响力】：{tar.影响力}\n'
                f'【转世】：{tar.转世}  【唯一id】：{tar.id}\n'
                f'【修炼进度】：{int(tar.能量)}/{tar.瓶颈}')
        if tar.拥有者 != '':
            data += f'\n【拥有者】: {tar.拥有者}'
        tar.world.printp(data, key_gui=1)
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
                tmp = re.split(';', cmd)
                try:
                    a = int(tmp[1])
                    b = int(tmp[2])
                    world.战斗(a, b)
                except:
                    print("命令输入错误。。。")
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
            elif re.match('ckm', cmd) != None:
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
            elif re.match('lsm', cmd) != None:
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
                    data += f'{cnt} {world.境界[-1]} {world.飞升人数}人'
                    world.printp(data, key_gui=1)
                else:
                    aa = int(re.split(' ', cmd)[1])
                    c = 0
                    if aa == len(world.境界) - 1:
                        for i in range(world.飞升人数):
                            c += 1
                            data += f'{i} {world.飞升人物[i].全名} '
                            if c % 8 == 0:
                                data += '\n'
                    else:
                        for i in range(world.人数):
                            if world.人物[i].境界 == aa:
                                c += 1
                                data += f'{i} {world.人物[i].全名} '
                                if c % 8 == 0:
                                    data += '\n'
                    world.printp(data, key_gui=1)
            elif re.match('lmp', cmd) != None:
                data = ''
                if ' ' not in cmd:
                    for i in range(len(world.门派)):
                        count = 0
                        for j in range(world.人数):
                            if world.门派[i] in world.人物[j].门派:
                                count += 1
                        data += str(i) + ' ' + world.门派[i] + str(count) + '人  '
                    world.printp(data, key_gui=1)
                else:
                    aa = int(re.split(' ', cmd)[1])
                    c = 0
                    for i in range(world.人数):
                        if world.门派[aa] in world.人物[i].门派:
                            c += 1
                            data += str(i) + ' ' + world.人物[i].全名 + '  '
                            if c % 8 == 0:
                                data += '\n'
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
                    if aa[1] in world.随机事件权重:
                        world.随机事件权重[aa[1]] = int(aa[2])
                    world.config_world_events()
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



