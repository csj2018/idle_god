from int_cls import *
from src.func.base_func import *
from src.func.action_func import *
from src.func.pk_func import *
def create_world_events():
    d = world.随机事件分段
    r = random.randint(1,d[-1])
    nl = list(world.随机事件权重.keys())
    for i in range(len(d)-1):
        if d[i]<r<=d[i+1]:
            tmp = nl[i]
    if tmp == '加人' and world.人数 < cfg['人数限制']:
        tmp = world.add_one()
        printj('机缘巧合，凡人' + tmp.姓名 + '踏入修炼一途，拜入' + tmp.门派, [tmp], 1)
    elif tmp == '恩怨':
        a = random.randint(0, world.人数 - 1)
        b = random.randint(0, world.人数 - 1)
        count = 0
        while (a == b or len(world.人物[a].行动) <= 1 or len(world.人物[b].行动) <= 1) and count <= 6:
            count += 1
            a = random.randint(0, world.人数 - 1)
            b = random.randint(0, world.人数 - 1)
        if count <= 6:
            pk(world.人物[a], world.人物[b], random.randint(0, 4))
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
    elif tmp == '帮战' and len(world.门派) >= 2:
        f = 1
        while f:
            a = random.choice(world.门派)
            b = random.choice(world.门派)
            if a != b:
                f = 0
        printp(a+'对'+b+'发起帮派战争', 3)
        try:
            for i in range(random.randint(4,12)):
                counta = 0
                countb = 0
                lista = []
                listb = []
                for i in world.人物:
                    if a in i.门派:
                        counta += 1
                        lista.append(i)
                    if b in i.门派:
                        countb += 1
                        listb.append(i)
                pk(random.choice(lista),random.choice(listb),random.randint(0,1))
        except:
            counta = 0
            countb = 0
            for i in world.人物:
                if a in i.门派:
                    counta += 1
                if b in i.门派:
                    countb += 1
            if counta == 0:
                c = a
            if countb == 0:
                c = b
            try:
                printp(c+'惨遭灭门！', 4)
                world.门派.pop(world.门派.index(c))
            except:#TODO
                print('TODO')
def config_world_events():
    tar = world.随机事件权重
    all = 0
    world.随机事件分段 = [0]
    for i in tar.values():
        all += i
        world.随机事件分段.append(all)
def world_events():
    if world.事件 == 1:
        event.开始 -= 1
        event.结束 -= 1
        if event.开始 ==0:
            printp(''+event.名称+'开始了！',1)
        if event.结束==0:
            world.事件 = 0
            printp('' + event.名称 + '结束了！', 1)
            for i in range(world.人数):
                if world.人物[i].行动[0] == '事件':
                    world.人物[i].后天资质 += random.randint(1,5)
                    if world.人物[i].后天资质 >= 3 * world.人物[i].先天资质 * world.人物[i].境界 + 30:
                        world.人物[i].后天资质 = 3 * world.人物[i].先天资质 * world.人物[i].境界 + 30
                        #print(''+world.人物[i].称号+''+world.人物[i].姓名+'后天资质提升至境界极限！')
                    else:
                        printp(world.人物[i].全名+'后天资质提升！', 1)
def random_events():
    create_world_events()
    check_state()
    creat_npc_actions()
    do_actions()
    world_events()
def 清理死人():
    while world.已故人数 > cfg['人数限制']:
        world.已故人数 -= 1
        world.已故人物.pop(0)
def 天道检验():
    if world.time[1]%cfg['天道检验'] == 0 and world.time[0] == 2:
        if world.人数 > 30:
            world.排天榜()
            printj(f'修仙历{world.time[1]}年，修仙百晓生发布天榜排名：', [world], 10)
            for i in range(10):
                tar = world.人物[i]
                tar.影响力 += 15 - i
                printj(f'{tar.全名}当选天榜第{i+1}名', [tar, world], 10)
        清理死人()
def check_state():
    for tar in world.人物:
        if tar.能量 >= tar.瓶颈 and tar.可突破 == 0:
            tar.可突破 = 1
            tar.行动.append('突破')
def loop():
    world.time[0] += 1
    if world.time[0] == 13:
        world.time[1] += 1
        world.time[0] = 1
        寿命检测()
    printp(str(world.time[1])+'年'+str(world.time[0])+'月', 6)
    天道检验()
    random_events()