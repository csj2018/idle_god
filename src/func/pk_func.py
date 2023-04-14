from int_cls import *
from src.func.base_func import *
from src.func.action_func import *

def pk(a,b,c=0):
    a.战斗力 = a.境界 * 10 + a.小境界
    b.战斗力 = b.境界 * 10 + b.小境界
    if a.战斗力 >= b.战斗力:#分强弱
        q = a
        r = b
    else:
        q = b
        r = a
    if (q.战斗力 - r.战斗力) * 10 + 50 >= random.randint(0, 100):  # 强胜
        s = q
        f = r
    else:
        s = r #胜
        f = q #败
    if c == 0:#0杀1重2轻3切磋4指导
        printj('【江湖仇杀】'+f.全名+'技不如人，被'
               +s.全名+'斩杀！',[f,s])
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