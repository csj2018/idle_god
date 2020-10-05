#!/usr/bin/python3
from cl import *
import random
import time as pkg_time
import re
import pickle
event = Event()
world = World()
world.initial()
境界 = ['炼气期', '筑基期', '金丹期', '元婴期', '出窍期', '分神期', '合体期', '渡劫期', '大乘期','飞升']
小境界 = ['一重天', '二重天', '三重天', '四重天', '五重天','六重天','七重天','八重天','九重天','大圆满']

def loop():
    world.time[0] += 1
    if world.time[0] == 13:
        world.time[1] += 1
        world.time[0] = 1
        check_age()
    print(str(world.time[1])+'年'+str(world.time[0])+'月')
    random_events()
    pkg_time.sleep(1)
def random_events():
    create_world_events()
    check_state()
    creat_npc_actions()
    do_actions()
    world_events()
def check_age():
    c = 0
    for i in range(world.人数):
        world.人物[i-c].年龄 += 1
        if world.人物[i-c].年龄 > world.人物[i-c].寿命:
            print(world.人物[i-c].姓名+'寿终正寝')
            world.人物.pop(i-c)
            world.人数 -= 1
            c +=1
def check_state():
    for i in range(world.人数):
        tar = world.人物[i]
        if tar.能量 >= tar.瓶颈 and tar.可突破 == 0:
            tar.可突破 = 1
            tar.行动.append('突破')
def creat_npc_actions():
    for i in range(world.人数):
        tar = world.人物[i]
        while len(tar.行动) <= 1:
            r = random.randint(0, 100)
            if r <= 93:
                tar.行动.append('修炼')
            elif r <= 100:
                for i in range(random.randint(6+world.人物[i].境界,24+world.人物[i].境界)):
                    tar.行动.append('闭关')
def create_world_events():
    d = world.随机事件分段
    r = random.randint(1,d[-1])
    for i in range(len(d)-1):
        if d[i]<r<=d[i+1]:
            tmp = world.随机事件权重[i][0]
    if tmp == '加人' and world.人数 < 300:
        tmp = world.add_one()
        printj('机缘巧合，凡人' + tmp.姓名 + '踏入修炼一途，拜入' + tmp.门派, [tmp])
    elif tmp == '恩怨':
        a = random.randint(0, world.人数 - 1)
        b = random.randint(0, world.人数 - 1)
        count = 0
        while (a == b or len(world.人物[a].行动) <= 1 or len(world.人物[b].行动) <= 1) and count <= 6:
            count += 1
            a = random.randint(0, world.人数 - 1)
            b = random.randint(0, world.人数 - 1)
        if count <= 6:
            pk(a, b, random.randint(0, 4))
    elif tmp == '奇遇' and world.事件 == 0:
        world.事件 = 1
        event.random()
        print(str(event.开始) + '个月后发生奇遇' + str(event.名称) + '!')
        for i in range(world.人数):
            xd = len(world.人物[i].行动)
            if xd <= event.开始 and random.randint(0, 2):
                for j in range(event.开始 - xd + 1):
                    world.人物[i].行动.append('修炼')
                for j in range(event.结束 - event.开始):
                    world.人物[i].行动.append('事件')
    elif tmp == '帮战':
        f = 1
        while f:
            a = random.choice(world.门派)
            b = random.choice(world.门派)
            if a != b:
                f = 0
        print(a+'对'+b+'发起帮派战争')
        try:
            for i in range(random.randint(4,12)):
                counta = 0
                countb = 0
                lista = []
                listb = []
                for i in range(world.人数):
                    if a in world.人物[i].门派:
                        counta += 1
                        lista.append(i)
                    if b in world.人物[i].门派:
                        countb += 1
                        listb.append(i)
                pk(random.choice(lista),random.choice(listb),random.randint(0,1))
        except:
            counta = 0
            countb = 0
            for i in range(world.人数):
                if a in world.人物[i].门派:
                    counta += 1
                    lista.append(i)
                if b in world.人物[i].门派:
                    countb += 1
            if counta == 0:
                c = a
            if countb == 0:
                c = b
            print(c+'惨遭灭门！')
            world.门派.pop(world.门派.index(c))
def config_world_events():
    tar = world.随机事件权重
    all = 0
    world.随机事件分段 = [0]
    for i in range(len(tar)):
        all += tar[i][1]
        world.随机事件分段.append(all)
def world_events():
    if world.事件 == 1:
        event.开始 -= 1
        event.结束 -= 1
        if event.开始 ==0:
            print(''+event.名称+'开始了')
        if event.结束==0:
            world.事件 = 0
            for i in range(world.人数):
                if world.人物[i].行动[0] == '事件':
                    world.人物[i].后天资质 += random.randint(1,5)
                    if world.人物[i].后天资质 >= 3 * world.人物[i].先天资质 * world.人物[i].境界 + 30:
                        world.人物[i].后天资质 = 3 * world.人物[i].先天资质 * world.人物[i].境界 + 30
                        #print(''+world.人物[i].称号+''+world.人物[i].姓名+'后天资质提升至境界极限！')
                    else:
                        print(''+world.人物[i].称号+''+world.人物[i].姓名+'后天资质提升！')
def do_actions():
    for i in range(world.人数):
        tar = world.人物[i]
        act = tar.行动[1]
        if act == '修炼':
            tar.能量 += (tar.先天资质+tar.后天资质)*tar.效率
            if world.print[0] == 1:
                print(''+tar.姓名+' 修炼进度 '+str(tar.能量)+'/'+str(tar.瓶颈)+'')
        elif act == '闭关':
            tar.能量 += (tar.先天资质+tar.后天资质)*tar.效率*1.5
            if tar.行动[0] != '闭关':
                print(''+tar.姓名+' 有所感悟，开始闭关...')
            if len(tar.行动) >2:
                if tar.行动[2] != '闭关':
                    print(''+tar.姓名+' 破关而出！修炼进度 '+str(int(tar.能量))+'/'+str(tar.瓶颈))
            if len(tar.行动) == 2:
                print(tar.姓名+' 破关而出！修炼进度 '+str(int(tar.能量))+'/'+str(tar.瓶颈))
        elif act == '突破':
            突破(tar)
        tar.行动.pop(0)
def 突破(tar):
    r = random.randint(0,100)
    if r <= tar.成功率:
        tar.可突破 = 0
        tar.能量 -= tar.瓶颈
        tar.瓶颈 = int(300+tar.境界*1800+tar.小境界+180)
        tar.小境界 += 1
        if tar.小境界 == 10:
            tar.小境界 = 0
            tar.境界 += 1
        tar.计算成功率()
        printj('经过不懈努力，'+tar.姓名+'突破到'+境界[tar.境界]+'·'+小境界[tar.小境界],[tar])
        tar.寿命+=20*tar.境界+20
        if tar.境界 == 2 and tar.小境界 == 0:
            tar.creat_ch()
            printj('天地感应，授予'+tar.姓名+'称号【'+tar.称号+'】',[tar])
        if tar.境界 == 9:
            printj('【'+tar.称号+'】'+tar.姓名+'超脱天地，白日飞升！',[tar])
    else:
        tar.能量 = int(tar.瓶颈/5)
        tar.可突破 = 0
        tar.成功率 += random.randint(5,10)
        printj(tar.姓名+'突破'+境界[tar.境界]+'·'+小境界[tar.小境界]+'失败，散失大半灵气',[tar])
def main():
    while 1:
        if world.run ==1:
            loop()
def keyin():
    while 1:
        try:
            aaa = input('>>>')
            if aaa == '':
                if world.run ==1:
                    world.run = 0
                    print('暂停')
                elif world.run == 0:
                    world.run = 1
                    print('继续')
            elif aaa == 'addone':
                tmp = world.add_one()
                printj('机缘巧合，凡人' + tmp.姓名 + '踏入修炼一途，拜入' + tmp.门派, [tmp])
            elif re.match('pk',aaa) != None:
                tmp = re.split(';',aaa)
                try:
                    a = int(tmp[1])
                    b = int(tmp[2])
                    pk(a,b)
                except:
                    print("命令输入错误。。。")
            elif aaa == 'save':
                save()
            elif aaa == 'load':
                load()
            elif re.match('check',aaa) != None:
                tmp = re.split(' ',aaa)
                if len(tmp) == 1:
                    print(world.随机事件权重)
                    data = ''
                    for i in range(world.人数):
                        data += str(i) + ' ' + world.人物[i].姓名 + '  '
                        if i % 8 == 7:
                            data += '\n'
                    print(data)
                    aa = int(input('看谁?'))
                else:
                    try:
                        aa = int(tmp[1])
                    except:
                        aa = int(input('看谁?'))
                        print('无效命令')
                print('【名号】：'+world.人物[aa].称号+world.人物[aa].姓名+'\n'+
                      '【年龄】：' + str(world.人物[aa].年龄)+'/'+str(world.人物[aa].寿命)+'\n'+
                      '【门派】：'+world.人物[aa].门派+'\n'+
                      '【境界】：'+境界[world.人物[aa].境界]+'·'+小境界[world.人物[aa].小境界]+'\n'+
                      '【体质】：'+world.人物[aa].体质+'【先天】'+str(world.人物[aa].先天资质)+' 【后天】'+str(world.人物[aa].后天资质)+'\n'+
                      '【修炼进度】：'+str(int(world.人物[aa].能量))+'/'+str(world.人物[aa].瓶颈))
            elif re.match('ls',aaa) != None:
                tmp = re.split(' ',aaa)
                if len(tmp) == 1:
                    data = ''
                    for i in range(world.人数):
                        data += str(i) + ' ' + world.人物[i].姓名 + '  '
                        if i % 8 == 7:
                            data += '\n'
                    print(data)
                    aa = int(input('看谁?'))
                else:
                    try:
                        aa = int(tmp[1])
                    except:
                        aa = int(input('看谁?'))
                        print('无效命令')
                print(world.人物[aa].历史)
            elif re.match('jj',aaa) != None:
                tmp = re.split(' ',aaa)
                data = ''
                if len(tmp) == 1:
                    for i in range(len(境界)):
                        count = 0
                        for j in range(world.人数):
                            if world.人物[j].境界 == i:
                                count += 1
                        data += str(i) + ' ' + 境界[i] + str(count) + '人  '
                    print(data)
                    data = ''
                    aa = int(input('看什么境界?'))
                else:
                    try:
                        aa = int(tmp[1])
                    except:
                        print('无效命令')
                        aa = int(input('看什么境界?'))
                c =0
                for i in range(world.人数):
                    if world.人物[i].境界 == aa:
                        c += 1
                        data += str(i) + ' ' + world.人物[i].姓名 + '  '
                        if c % 8 == 0:
                            data += '\n'
                print(data)
            elif re.match('mp',aaa) != None:
                tmp = re.split(' ',aaa)
                data = ''
                if len(tmp) == 1:
                    for i in range(len(world.门派)):
                        count = 0
                        for j in range(world.人数):
                            if world.门派[i] in world.人物[j].门派:
                                count += 1
                        data += str(i) + ' ' + world.门派[i] + str(count) + '人  '
                    print(data)
                    data = ''
                    aa = int(input('看什么门派?'))
                else:
                    try:
                        aa = int(tmp[1])
                    except:
                        print('无效命令')
                        aa = int(input('看什么门派?'))
                c = 0
                for i in range(world.人数):
                    if world.门派[aa] in world.人物[i].门派:
                        c += 1
                        data += str(i) + ' ' + world.人物[i].姓名 + '  '
                        if c%8 == 0:
                            data += '\n'
                print(data)
            elif aaa == 'print0':
                world.print[0] = 1 - world.print[0]
            elif aaa == 'addmp':
                world.new_mp()
                print('新门派【'+world.门派[-1]+'】成立了！')
            else:
                print("无效命令")
        except:
            print("无效命令")
def pk(a,b,c=0):
    aa = world.人物[a].境界 * 10 + world.人物[a].小境界
    bb = world.人物[b].境界 * 10 + world.人物[b].小境界
    if aa >= bb:#分强弱
        q = a
        r = b
    else:
        q = b
        r = a
    if (q - r) * 10 + 50 >= random.randint(0, 100):  # 强胜
        s = q
        f = r
    else:
        s = r
        f = q
    if c == 0:#0杀1重2轻3切磋4指导
        printj('【江湖仇杀】'+world.人物[f].称号+''+world.人物[f].姓名+'技不如人，被'
               +world.人物[s].称号+world.人物[s].姓名+'斩杀！',[world.人物[f],world.人物[s]])
        world.人物.pop(f)
        world.人数 -= 1
    elif c == 1:
        world.人物[f].寿命-= 10 * world.人物[f].境界
        if world.人物[f].小境界 > 0:
            world.人物[f].小境界 -= 1
        else:
            world.人物[f].境界 -= 1
            world.人物[f].小境界 = 9
        printj('【江湖恩怨】'+world.人物[f].称号+''+world.人物[f].姓名+'技不如人，被'
              +world.人物[s].称号+''+world.人物[s].姓名+'打成重伤，境界跌落!',[world.人物[f],world.人物[s]])
    elif c == 2:
        world.人物[f].能量 == 0
        printj('【江湖恩怨】'+world.人物[f].称号+''+world.人物[f].姓名+'技不如人，被'
              +world.人物[s].称号+''+world.人物[s].姓名+'打成轻伤!',[world.人物[f],world.人物[s]])
    elif c == 3:
        printj('【江湖切磋】'+world.人物[f].称号+''+world.人物[f].姓名+'技不如人，被'
              +world.人物[s].称号+''+world.人物[s].姓名+'击败!',[world.人物[f],world.人物[s]])
    elif c == 4:
        world.人物[f].能量 += world.人物[f].瓶颈/4
        printj('【江湖指导】'+world.人物[f].称号+''+world.人物[f].姓名+'受'
              +world.人物[s].称号+''+world.人物[s].姓名+'点拨，修为大进!',[world.人物[f],world.人物[s]])
def save():
    data = [world,event]
    f = open('save.pckl', 'wb')
    pickle.dump(data, f)
    f.close()
def load():
    f = open('save.pckl', 'rb')
    data = pickle.load(f)
    f.close()
    world.time = data[0].time
    world.人数 = data[0].人数
    world.人物 = data[0].人物
    world.print = data[0].print
    world.门派=data[0].门派
    world.事件=data[0].事件
    world.随机事件分段=data[0].随机事件分段
    world.随机事件权重=data[0].随机事件权重
    event = data[1]
def printj(p,tar = []):
    print(p)
    for i in tar:
        i.历史 += str(world.time[1])+'年'+str(world.time[0])+'月 '+p+'\n'

begin = 1
while begin:
    try:
        a = input('【0】  新的故事\n【1】  旧的故事\n')
        if a == '0':
            begin = 0
        elif a == '1':
            begin = 0
            load()
    except:
        print('无效输入...')

config_world_events()
thread_l =[]
thread1 = threading.Thread(target = main, args = ())
thread_l.append(thread1)
thread2 = threading.Thread(target = keyin, args = ())
thread_l.append(thread2)
for i in thread_l:
    i.start()
for i in thread_l:
    i.join()