from int_cls import *
from src.func.base_func import *
from src.func.action_func import *
from src.func.pk_func import *
#from src.func.win_func import *
from .events_func import *
import re

def keyinthread():
    while 1:
        try:
            cmd = input('>>>')
            act_cmd(cmd, 1, '管理员')
        except:
            print('keyinthread() 退出')
            world.END = 1
            exit(-1)

def act_cmd(cmd, local = 0, owner = '', gui = cfg['图形界面']):
    try:
        if world.run == 1 and cmd == '':
            world.run = 0
            printp('暂停', key_gui = 1)
        elif world.run == 0 and cmd == '':
            world.run = 1
            printp('继续', key_gui = 1)
        #//TODO 二次输入
        elif re.match('dzqq', cmd) != None:
            p = world.dzqq()
            printj(p, key_gui=gui)
        elif re.match('qq', cmd) != None:
            name = re.split(' ', cmd)[1]
            world.增加蛐蛐(name, owner)
        elif re.match('addone', cmd) != None:
            tmp = world.add_one()
            printj('机缘巧合，凡人' + tmp.姓名 + '踏入修炼一途，拜入' + tmp.门派, [tmp])
        elif re.match('pk', cmd) != None:
            tmp = re.split(';',cmd)
            try:
                a = int(tmp[1])
                b = int(tmp[2])
                pk(a,b)
            except:
                print("命令输入错误。。。")
        elif cmd == 'save':
            if local == 1:
                save()
            else:
                printp("权限不足", key_gui = 1)
        elif cmd == 'load':
            if local == 1:
                load()
            else:
                printp("权限不足", key_gui = 1)
        elif re.match('ckd', cmd) != None:
            if ' ' not in cmd:
                列出所有人(0)
            else:
                aa = int(re.split(' ', cmd)[1])
                tar = world.已故人物[aa]
                查看属性(tar)
        elif re.match('cka', cmd) != None:
            if ' ' not in cmd:
                列出所有人(1)
            else:
                aa = int(re.split(" ", cmd)[1])
                tar = world.人物[aa]
                查看属性(tar)
        elif re.match('ckf', cmd) != None:
            if ' ' not in cmd:
                列出所有人(2)
            else:
                aa = int(re.split(" ", cmd)[1])
                tar = world.飞升人物[aa]
                查看属性(tar)
        elif re.match('lsd', cmd) != None:
            aa = int(re.split(' ', cmd)[1])
            tar = world.已故人物[aa]
            查看历史(tar)
        elif re.match('lsa', cmd) != None:
            aa = int(re.split(' ', cmd)[1])
            tar = world.人物[aa]
            查看历史(tar)
        elif re.match('lsf', cmd) != None:
            aa = int(re.split(' ', cmd)[1])
            tar = world.飞升人物[aa]
            查看历史(tar)
        elif re.match('lsw', cmd) != None:
            查看历史(world)
        elif re.match('ljj',cmd) != None:
            data = ''
            if ' ' not in cmd:
                cnt = 0
                for i in range(len(境界)-1):
                    count = 0
                    for j in world.人物:
                        if j.境界 == i:
                            count += 1
                    data += f'{cnt} {境界[i]} {count}人 \n'
                    cnt += 1
                data += f'{cnt} {境界[-1]} {world.飞升人数}人'
                printp(data, key_gui = 1)
            else:
                aa = int(re.split(' ', cmd)[1])
                c = 0
                if aa == len(境界)-1:
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
                printp(data, key_gui = 1)
        elif re.match('lmp',cmd) != None:
            data = ''
            if ' ' not in cmd:
                for i in range(len(world.门派)):
                    count = 0
                    for j in range(world.人数):
                        if world.门派[i] in world.人物[j].门派:
                            count += 1
                    data += str(i) + ' ' + world.门派[i] + str(count) + '人  '
                printp(data, key_gui = 1)
            else:
                aa = int(re.split(' ', cmd)[1])
                c = 0
                for i in range(world.人数):
                    if world.门派[aa] in world.人物[i].门派:
                        c += 1
                        data += str(i) + ' ' + world.人物[i].全名 + '  '
                        if c%8 == 0:
                            data += '\n'
                printp(data, key_gui = 1)
        elif cmd == 'print0':
            world.print[0] = 1 - world.print[0]
        elif cmd == 'addmp':
            world.new_mp()
            print('新门派【'+world.门派[-1]+'】成立了！')
        elif re.match('ptb', cmd) != None:
            world.排天榜()
        elif re.match('cfg', cmd) != None:
            if local == 1:
                printp(cfg, key_gui = 1)
                printp('请修改：', key_gui = 1)
                aa = input()
                bb = re.split(' ', aa)
                cfg[bb[0]] = int(bb[1])
                if bb[0] in world.随机事件权重:
                    world.随机事件权重[bb[0]] = bb[1]
                config_world_events()

        elif re.match('push', cmd) != None:
            if local == 1:
                tmp = cfg['打印等级']
                cfg['打印等级'] = 10 + tmp
                aa = int(re.split(' ', cmd)[1])
                for i in range(aa*12):
                    loop()
                cfg['打印等级'] = tmp
                printp(f"世界外伟力推动下时光快速流逝，不知不觉已过{aa}载！", key_gui = 1)
        elif re.match('改名', cmd) != None:
            tmp = re.split(' ', cmd)
            for tar in world.人物:
                if owner == tar.拥有者 and owner != '':
                    tar.姓名 = f'\033[35m{tmp[1]}\033[0m'
                    tar.全名计算()
                    printp('改名成功', key_gui = 1)
                    break
        else:
            printp("无效命令", key_gui = 1)
    except:
        printp("无效命令", key_gui = 1)

def 查看属性(tar):
    printp(f'【名号】：{tar.全名}\n'
          f'【年龄】：{tar.年龄}/{tar.寿命}\n'
          f'【门派】：{tar.门派}\n'
          f'【境界】：{境界[tar.境界]}·{小境界[tar.小境界]}\n'
          f'【体质】：{tar.体质}【先天】{tar.先天资质} 【后天】{tar.后天资质}\n'
          f'【战斗力】：{tar.战斗力} 【影响力】：{tar.影响力}\n'
          f'【转世】：{tar.转世}\n'
          f'【修炼进度】：{int(tar.能量)}/{tar.瓶颈}', key_gui = 1)
    if tar.拥有者 != '':
        printp(f'【拥有者】: {tar.拥有者}', key_gui = 1)
def 查看历史(tar):
    printp(tar.历史, key_gui = 1 )

def 列出所有人(staute = 0):
    data = ''
    if staute == 0: # 如果状态为0，即已故人数
        for i in range(world.已故人数): # 遍历已故人数
            data += str(i) + ' ' + world.已故人物[i].全名 + '  ' # 将已故人物的编号和全名加入data中
            if i % 8 == 7: # 每8个人换一行
                data += '\n'
    elif staute == 1: # 如果状态为1，即未飞升人数
        for i in range(world.人数): # 遍历人数
            data += str(i) + ' ' + world.人物[i].全名 + '  ' # 将人物的编号和全名加入data中
            if i % 8 == 7: # 每8个人换一行
                data += '\n'
    else: # 如果状态为其他，即飞升人数
        for i in range(world.飞升人数): # 遍历飞升人数
            data += str(i) + ' ' + world.飞升人物[i].全名 + '  ' # 将飞升人物的编号和全名加入data中
            if i % 8 == 7: # 每8个人换一行
                data += '\n'
    printp(data, key_gui = 1) # 输出data
