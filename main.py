#!/usr/bin/python3
from post_main import *

from src.func.base_func import *
from src.func.action_func import *
from src.func.events_func import *
from src.func.pk_func import *
from src.func.keyin_func import *

def loop():
    world.time[0] += 1
    if world.time[0] == 13:
        world.time[1] += 1
        world.time[0] = 1
        寿命检测()
    print(str(world.time[1])+'年'+str(world.time[0])+'月')
    random_events()
    time.sleep(0.3)

def main():
    while 1:
        if world.run ==1:
            loop()

world.initial()
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
thread1 = threading.Thread(target = main, args = ())
thread_l.append(thread1)
thread2 = threading.Thread(target = keyin, args = ())
thread_l.append(thread2)
for i in thread_l:
    i.start()
for i in thread_l:
    i.join()
