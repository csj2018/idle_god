from post_main import *
from src.func.base_func import *
from src.func.action_func import *

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
        s = r #胜
        f = q #败
    if c == 0:#0杀1重2轻3切磋4指导
        printj('【江湖仇杀】'+world.人物[f].全名+'技不如人，被'
               +world.人物[s].全名+'斩杀！',[world.人物[f],world.人物[s]])
        死亡(f)
    elif c == 1:
        world.人物[f].寿命-= 10 * world.人物[f].境界
        if world.人物[f].小境界 > 0:
            world.人物[f].小境界 -= 1
        else:
            world.人物[f].境界 -= 1
            world.人物[f].小境界 = 9
        printj('【江湖恩怨】'+world.人物[f].全名+'技不如人，被'
              +world.人物[s].全名+'打成重伤，境界跌落!',[world.人物[f],world.人物[s]])
    elif c == 2:
        world.人物[f].能量 == 0
        printj('【江湖恩怨】'+world.人物[f].全名+'技不如人，被'
              +world.人物[s].全名+'打成轻伤!',[world.人物[f],world.人物[s]])
    elif c == 3:
        printj('【江湖切磋】'+world.人物[f].全名+'技不如人，被'
              +world.人物[s].全名+'击败!',[world.人物[f],world.人物[s]])
    elif c == 4:
        world.人物[f].能量 += world.人物[f].瓶颈/4
        printj('【江湖指导】'+world.人物[f].全名+'受'
              +world.人物[s].全名+'点拨，修为大进!',[world.人物[f],world.人物[s]])