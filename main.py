#!/usr/bin/python3
import time, threading, os
import src.World as World

#event = World.Event.Event()
world = World.World()
world.initial()

from src.Danmu import *
danmu = Danmu()

def fckthread():
    od = ''
    while 1:
        time.sleep(1)
        if world.cfg['副窗口']:
            try:
                with open('input.tmp') as f:
                    data = f.read()
                    if od != data:
                        world.act_cmd(data, 1, '管理员', 1)
                        od = data
            except:
                continue
def keyinthread():
    while 1:
        try:
            cmd = input('>>>')
            world.act_cmd(cmd, 1, '管理员', world.cfg['副窗口'])
        except:
            print('keyinthread() 退出')
            world.END = 1
            exit(-1)
def mainthread():
    while 1:
        if world.END:
            exit(-1)
        if world.run ==1:
            world.loop()
        time.sleep(1 / world.cfg['速度倍数'])
def dmthread():
    danmu.getdanmu(1)
    while 1:
        cmd_time = 0
        danmu.getdanmu()
        while danmu.seq != []:
            tr = danmu.seq.pop(0)
            if tr[2] == 1:
                if tr[0] in ['赤司酱']:
                    world.act_cmd(tr[1], 1, tr[0])
                else:
                    world.act_cmd(tr[1], 0, tr[0])
                cmd_time += 1
                time.sleep(1)
            else:
                if tr[0] not in world.水友:
                    world.水友.append(tr[0])
                    world.act_cmd(f'qq {tr[0]}', 0, tr[0])
                    cmd_time += 1
                    time.sleep(1)
        if cmd_time < 3:
            time.sleep(4-cmd_time)

while 1:
    #try:
    a = input('【0】  新的故事\n【1】  旧的故事\n')
    if a == '0':
        break
    elif a == '1':
        world.load()
    break
    #except:
        #print('无效输入...')

world.config_world_events()

thread_l =[]
thread0 = threading.Thread(target = mainthread, args = ())
thread_l.append(thread0)
thread1 = threading.Thread(target = keyinthread, args = ())
thread_l.append(thread1)
print(world.cfg)
if world.cfg['副窗口']:
    thread2 = threading.Thread(target = fckthread, args = ())
    thread_l.append(thread2)


if world.cfg['弹幕控制']:
    thread3 = threading.Thread(target = dmthread, args = ())
    thread_l.append(thread3)

for i in thread_l:
    i.start()
if world.cfg['副窗口']:
    os.system('start check_win.py')
for i in thread_l:
    i.join()
