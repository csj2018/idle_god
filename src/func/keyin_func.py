from int_cls import *
from src.func.base_func import *
from src.func.action_func import *
from src.func.pk_func import *

def keyin():
    while 1:
        try:
            cmd = input('>>>')
            if world.run == 1:
                world.run = 0
                print('暂停')
            elif cmd == '':
                world.run = 1
                print('继续')
            elif 'dzqq' in cmd:
                p = world.dzqq()
                printj(p)
            elif cmd == 'addone':
                tmp = world.add_one()
                printj('机缘巧合，凡人' + tmp.姓名 + '踏入修炼一途，拜入' + tmp.门派, [tmp])
            elif re.match('pk',cmd) != None:
                tmp = re.split(';',cmd)
                try:
                    a = int(tmp[1])
                    b = int(tmp[2])
                    pk(a,b)
                except:
                    print("命令输入错误。。。")
            elif cmd == 'save':
                save()
            elif cmd == 'load':
                load()
            elif cmd == 'cd':
                data = ''
                for i in range(world.已故人数):
                    data += str(i) + ' ' + world.已故人物[i].全名 + '  '
                    if i % 8 == 7:
                        data += '\n'
                print(data)
                aa = int(input('看谁?'))
                tar = world.已故人物[aa]
                print(f'【名号】：{tar.全名}\n'
                      f'【年龄】：{str(tar.年龄)}/{str(tar.寿命)}\n'
                      f'【门派】：{tar.门派}\n'
                      f'【境界】：{境界[tar.境界]}·{小境界[tar.小境界]}\n'
                      f'【体质】：{tar.体质}【先天】{str(tar.先天资质)} 【后天】{str(tar.后天资质)}\n'
                      f'【转世】：{tar.转世}\n'
                      f'【修炼进度】：{str(int(tar.能量))}/{str(tar.瓶颈)}')
                print(tar.历史)
            elif re.match('ck',cmd) != None:
                tmp = re.split(' ',cmd)
                if len(tmp) == 1:
                    print(world.随机事件权重)
                    data = ''
                    for i in range(world.人数):
                        data += str(i) + ' ' + world.人物[i].全名 + '  '
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
                tar = world.人物[aa]
                print(f'【名号】：{tar.全名}\n'
                      f'【年龄】：{str(tar.年龄)}/{str(tar.寿命)}\n'
                      f'【门派】：{tar.门派}\n'
                      f'【境界】：{境界[tar.境界]}·{小境界[tar.小境界]}\n'
                      f'【体质】：{tar.体质}【先天】{str(tar.先天资质)} 【后天】{str(tar.后天资质)}\n'
                      f'【转世】：{tar.转世}\n'
                      f'【修炼进度】：{str(int(tar.能量))}/{str(tar.瓶颈)}')
                print(tar.历史)
            elif re.match('ls',cmd) != None:
                tmp = re.split(' ',cmd)
                if len(tmp) == 1:
                    data = ''
                    for i in range(world.人数):
                        data += str(i) + ' ' + world.人物[i].全名 + '  '
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
            elif re.match('jj',cmd) != None:
                tmp = re.split(' ',cmd)
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
                        data += str(i) + ' ' + world.人物[i].全名 + '  '
                        if c % 8 == 0:
                            data += '\n'
                print(data)
            elif re.match('mp',cmd) != None:
                tmp = re.split(' ',cmd)
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
                        data += str(i) + ' ' + world.人物[i].全名 + '  '
                        if c%8 == 0:
                            data += '\n'
                print(data)
            elif cmd == 'print0':
                world.print[0] = 1 - world.print[0]
            elif cmd == 'addmp':
                world.new_mp()
                print('新门派【'+world.门派[-1]+'】成立了！')
            else:
                print("无效命令")
        except:
            print("无效命令")