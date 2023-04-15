from int_cls import *

if cfg['图形界面']:
    import tkinter as tk

    win = tk.Tk()
    win.attributes ('-topmost', True)
    win_ot = tk.Text(win, bg='black') # 修改output背景为黑色
    win_ot.pack()

    def opthread():
        tk.mainloop()

    def updata_op(nv = '', win_op = win_ot):
        win_op.insert(tk.END, nv)

    def printm(a):
        print(a)
        if cfg['gui'] == 1:
            world.mail.append(a)

    def up_opthread(win=win):
        while 1:
            time.sleep(1 / cfg['speed_bonus'])
            for i in world.mail:
                updata_op(nv=i)
            world.mail = []