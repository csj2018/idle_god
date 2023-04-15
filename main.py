#!/usr/bin/python3
import time
import tkinter as tk

from int_cls import *

from src.func.base_func import *
read_cfg(cfg)
from src.func.action_func import *
from src.func.events_func import *
from src.func.pk_func import *
from src.func.keyin_func import *
from src.func.win_func import *


def loop():
    world.time[0] += 1
    if world.time[0] == 13:
        world.time[1] += 1
        world.time[0] = 1
        寿命检测()
    print(str(world.time[1])+'年'+str(world.time[0])+'月')
    random_events()

def test():
    #world.排天榜()
    return 0
def mainthread():
    cnt = 0
    while 1:
        if world.END:
            exit(-1)
        if world.run ==1:
            loop()
        time.sleep(1 / cfg['speed_bonus'])

def dmthread():
    danmu.getdanmu(1)
    while 1:
        cmd_time = 0
        danmu.getdanmu()
        while danmu.cmd != []:
            act_cmd(danmu.cmd.pop(0), 0)
            cmd_time += 1
            time.sleep(1)
        if cmd_time < 5:
            time.sleep(5-cmd_time)

begin = 1
while begin:
    try:
        a = input('【0】  新的故事\n【1】  旧的故事\n')
        if a == '0':
            begin = 0
        elif a == '1':
            begin = 0
            load()
    except:
        print('无效输入...')

config_world_events()

thread_l =[]
thread0 = threading.Thread(target = mainthread, args = ())
thread_l.append(thread0)
thread1 = threading.Thread(target = keyinthread, args = ())
thread_l.append(thread1)
if cfg['gui']:
    thread2 = threading.Thread(target = up_opthread, args = ())
    thread_l.append(thread2)
if cfg['danmu_control']:
    thread3 = threading.Thread(target = dmthread, args = ())
    thread_l.append(thread3)

for i in thread_l:
    i.start()
if cfg['gui']:
    win.mainloop()
for i in thread_l:
    i.join()
