from int_cls import *
from src.func.base_func import *
from src.func.action_func import *
from src.func.pk_func import *

def keyinthread():
    while 1:
        try:
            cmd = input('>>>')
            act_cmd(cmd, 1)
        except:
            print('keyinthread() 退出')
            world.END = 1
            exit(0)

def act_cmd(cmd, local = 0):
    try:
        if world.run == 1:
            world.run = 0
            print('暂停')
        elif cmd == '':
            world.run = 1
            print('继续')
    #//TODO 二次输入
        elif re.match('dzqq', cmd) != None:
            p = world.dzqq()
            printj(p)
        elif re.match('zjqq', cmd) != None:
            name = re.split(' ', cmd)[1]
            world.增加蛐蛐(name)
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
                print("权限不足")
        elif cmd == 'load':
            if local == 1:
                load()
            else:
                print("权限不足")
        elif re.match('ckd', cmd) != None:
            if ' ' not in cmd:
                列出所有人(0)
            else:
                aa = int(re.split(' ', cmd)[-1])
                tar = world.已故人物[aa]
                查看属性(tar)
        elif re.match('cka', cmd) != None:
            if ' ' not in cmd:
                列出所有人(1)
            else:
                aa = int(re.split(' ', cmd)[-1])
                tar = world.人物[aa]
                查看属性(tar)
        elif re.match('lsd', cmd) != None:
            aa = int(re.split(' ', cmd)[-1])
            tar = world.已故人物[aa]
            查看历史(tar)
        elif re.match('lsa', cmd) != None:
            aa = int(re.split(' ', cmd)[-1])
            tar = world.人物[aa]
            查看历史(tar)
        elif re.match('ljj',cmd) != None:
            data = ''
            if ' ' not in cmd:
                for i in range(len(境界)):
                    count = 0
                    for j in range(world.人数):
                        if world.人物[j].境界 == i:
                            count += 1
                    data += str(i) + ' ' + 境界[i] + str(count) + '人  '
                print(data)
            else:
                aa = int(re.split(' ', cmd)[1])
                c = 0
                for i in range(world.人数):
                    if world.人物[i].境界 == aa:
                        c += 1
                        data += str(i) + ' ' + world.人物[i].全名 + '  '
                        if c % 8 == 0:
                            data += '\n'
                print(data)
        elif re.match('lmp',cmd) != None:
            data = ''
            if ' ' not in cmd:
                for i in range(len(world.门派)):
                    count = 0
                    for j in range(world.人数):
                        if world.门派[i] in world.人物[j].门派:
                            count += 1
                    data += str(i) + ' ' + world.门派[i] + str(count) + '人  '
                print(data)
            else:
                aa = int(re.split(' ', cmd)[1])
                c = 0
                for i in range(world.人数):
                    if world.门派[aa] in world.人物[i].门派:
                        c += 1
                        data += str(i) + ' ' + world.人物[i].全名 + '  '
                        if c%8 == 0:
                            data += '\n'
                print(data)
        elif cmd == 'print0':
            world.print[0] = 1 - world.print[0]
        elif cmd == 'addmp':
            world.new_mp()
            print('新门派【'+world.门派[-1]+'】成立了！')
        elif re.match('ptb', cmd) != None:
            world.排天榜()
        else:
            print("无效命令")
    except:
        print("无效命令")

def 查看属性(tar):
    print(f'【名号】：{tar.全名}\n'
          f'【年龄】：{str(tar.年龄)}/{str(tar.寿命)}\n'
          f'【门派】：{tar.门派}\n'
          f'【境界】：{境界[tar.境界]}·{小境界[tar.小境界]}\n'
          f'【体质】：{tar.体质}【先天】{str(tar.先天资质)} 【后天】{str(tar.后天资质)}\n'
          f'【战斗力】：{tar.战斗力} 【影响力】：{tar.影响力}\n'
          f'【转世】：{tar.转世}\n'
          f'【修炼进度】：{str(int(tar.能量))}/{str(tar.瓶颈)}')
def 查看历史(tar):
    print(tar.历史)

def 列出所有人(alive = 0):
    data = ''
    if alive == 0:
        for i in range(world.已故人数):
            data += str(i) + ' ' + world.已故人物[i].全名 + '  '
            if i % 8 == 7:
                data += '\n'
    else:
        for i in range(world.人数):
            data += str(i) + ' ' + world.人物[i].全名 + '  '
            if i % 8 == 7:
                data += '\n'
    print(data)