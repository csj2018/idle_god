from int_cls import *

#if cfg['图形界面']:
import tkinter as tk
import re
import colorama

# Initialize colorama
colorama.init()

win = tk.Tk()
win.attributes ('-topmost', True)
win_ot = tk.Text(win, bg='white') # 修改output背景为黑色
win_ot.pack()

def opthread():
    tk.mainloop()

def updata_op(nv = '', win_op = win_ot):
    # 处理数据
    win_op.insert(tk.END, nv+'\n')


def printm(a):
    #if cfg['图形界面'] == 1:
    world.mail.append(a)

def up_opthread(win=win):
    while 1:
        time.sleep(1 / cfg['速度倍数'])
        for i in world.mail:
            updata_op(nv=i)
        world.mail = []