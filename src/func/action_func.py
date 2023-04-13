from post_main import *
from src.func.base_func import *
def creat_npc_actions():
    for i in range(world.人数):
        tar = world.人物[i]
        while len(tar.行动) <= 1:
            r = random.randint(0, 100)
            if r <= 93:
                tar.行动.append('修炼')
            elif r <= 100:
                for i in range(random.randint(6+world.人物[i].境界, 24+world.人物[i].境界)):
                    tar.行动.append('闭关')
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