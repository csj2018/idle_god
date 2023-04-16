from int_cls import *
#from .win_func import *

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
def printm(a):
    #if cfg['图形界面'] == 1:
    world.mail.append(a)
def printj(c, tar = [], p = 0, key_gui = 0):
    printp(c, p, key_gui)
    for i in tar:
        i.历史 += str(world.time[1])+'年'+str(world.time[0])+'月 '+c+'\n'
def printp(c, p = 100, key_gui = 0): #优先级
    if key_gui == 1:
        printm(c)
    #else:
    if cfg['打印等级'] <= p:
        print(c)
def 寿命检测():
    for tar in world.人物:
        tar.年龄 += 1
        if tar.年龄 > tar.寿命:
            printj(tar.全名+'寿终正寝', tar)
            死亡(tar)
def 突破(tar = NPC):
    r = random.randint(0,100)
    p = tar.天命 + 1
    if r <= tar.成功率:#成功
        tar.影响力 += int(30+tar.境界*180+tar.小境界+18)
        tar.可突破 = 0
        tar.能量 -= tar.瓶颈
        tar.瓶颈 = int(300+tar.境界*1800+tar.小境界+180)
        tar.小境界 += 1
        if tar.小境界 == 10:
            tar.小境界 = 0
            tar.境界 += 1
            p += 1
        tar.计算成功率()
        tar.战斗力计算()
        printj('经过不懈努力，'+tar.全名+'突破到'+境界[tar.境界]+'·'+小境界[tar.小境界], [tar], p)
        tar.寿命+=20*tar.境界+20
        if tar.境界 == 2 and tar.小境界 == 0:
            tar.creat_ch()
            p += 2
            printj(f'天地感应，授予{tar.姓名}称号【{tar.称号}】',[tar], p)
            tar.全名计算()
        if tar.境界 == 9:
            p += 10
            printj(f'{tar.全名}超脱天地，白日飞升！',[tar], p)
            飞升(tar)
    else:
        tar.能量 = int(tar.瓶颈/5)
        tar.可突破 = 0
        tar.成功率 += random.randint(5,10)
        printj(f'{tar.全名}突破{境界[tar.境界]}·{小境界[tar.小境界]}失败，散失大半灵气',[tar])
def 飞升(src):
    a = world.人物.index(src)
    world.飞升人物.append(world.人物.pop(a))
    world.人数 -= 1
    world.飞升人数 += 1
def 转生(src):
    a = src.转世 + 1
    world.add_one()
    tar = world.人物[-1]
    tar.姓名 = src.姓名
    tar.天命 = src.天命
    tar.拥有者 = src.拥有者
    tar.影响力 = int(src.影响力/2)
    tar.转世 = a
    tar.全名计算()
    printj(f'神秘力量下{tar.姓名}转世重生', [src, tar])
def 死亡(tar):
    world.已故人物.append(world.人物.pop(world.人物.index(tar)))
    world.人数 -= 1
    world.已故人数 += 1
    if tar.天命 == 1 or random.randint(0,10) > 8:#TODO 影响力决定
        转生(tar)

def read_cfg(cfg):
    with open('config.ini', encoding='utf-8') as f:
        data = f.read()
    dl = re.split('\n', data)
    for i in dl:
        tmp = re.split(' ', i)
        try:
            cfg[tmp[0]] = int(tmp[1])
        except:
            cfg[tmp[0]] = tmp[1]
    tmp = world.随机事件权重.keys()
    for i in tmp:
        world.随机事件权重[i] = cfg[i]