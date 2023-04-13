from post_main import *
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
    world.已故人数 = data[0].已故人数
    world.已故人物 = data[0].已故人物
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
def 寿命检测():
    c = 0
    for i in range(world.人数):
        tar = world.人物[i-c]
        tar.年龄 += 1
        if tar.年龄 > tar.寿命:
            printj(tar.姓名+'寿终正寝', tar)
            死亡(i-c)
            world.已故人物.append(world.人物.pop(i-c))
            world.人数 -= 1
            world.已故人数 += 1
            c += 1
def check_state():
    for i in range(world.人数):
        tar = world.人物[i]
        if tar.能量 >= tar.瓶颈 and tar.可突破 == 0:
            tar.可突破 = 1
            tar.行动.append('突破')
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
def 转生(tar):
    #tar = NPC()
    a = tar.转世 + 1
    world.add_one()
    world.人物[-1].姓名 = tar.姓名[:-8]+f'第{a}世'+tar.姓名[-7:]
    printj(f'神秘力量下{tar.姓名}转世重生', [tar, world.人物[-1]])
def 死亡(num):
    world.已故人物.append(world.人物.pop(num))
    world.人数 -= 1
    world.已故人数 += 1
    if world.人物(num).天命 == 1 or random.randint(0,10) > 8:
        转生(world.已故人物[-1])