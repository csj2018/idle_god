from int_cls import *
from src.func.base_func import *
from src.func.action_func import *

def pk(a, b, c = 0):
    总战斗力 = a.战斗力 + b.战斗力
    if random.randint(1, 总战斗力) <= a.战斗力:# a win
        s = a
        f = b
    else:
        s = b
        f = a
    if c == 0:#0杀 1重 2轻 3切磋 4指导
        printj('【江湖仇杀】'+f.全名+'技不如人，被'
               +s.全名+'斩杀！',[f,s], 2)
        死亡(f)
    elif c == 1:
        f.寿命-= 10 * f.境界
        if f.小境界 > 0:
            f.小境界 -= 1
        elif f.境界 > 0:
            f.境界 -= 1
            f.小境界 = 9
        else:
            print("TODO")#TODO
        printj('【江湖恩怨】'+f.全名+'技不如人，被'
              +s.全名+'打成重伤，境界跌落!',[f,s])
    elif c == 2:
        f.能量 == 0
        printj('【江湖恩怨】'+f.全名+'技不如人，被'
              +s.全名+'打成轻伤!',[f,s])
    elif c == 3:
        printj('【江湖切磋】'+f.全名+'技不如人，被'
              +s.全名+'击败!',[f,s])
    elif c == 4:
        f.能量 += f.瓶颈/4
        printj('【江湖指导】'+f.全名+'受'
              +s.全名+'点拨，修为大进!',[f,s])