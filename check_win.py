import os, sys, traceback
import time, threading
os.chdir(os.path.dirname(__file__))
def op():
    with open('output.tmp', encoding='utf-8') as f:
        od = f.read()
    while 1:
        time.sleep(1)
        try:
            with open('output.tmp', encoding='utf-8') as f:
                data = f.read()
                if od != data:
                    print(data)
                    od = data
        except Exception as e:
            print("副窗口出错，请查看debug.log")
            debug_data = f'{e}\n{sys.exc_info()}\n{traceback.print_exc()}\n{traceback.format_exc()}'
            with open('debug.log', 'w+', encoding='utf-8') as f:
                f.write(debug_data)

def ip():
    od = ''
    while 1:
        cmd = input(">>>")
        if od != cmd:
            with open('input.tmp','w+', encoding='utf-8') as f:
                f.write(cmd)
            if cmd == 'clr':
                os.system('cls')

thread_l =[]
thread0 = threading.Thread(target = op, args = ())
thread_l.append(thread0)
thread1 = threading.Thread(target = ip, args = ())
thread_l.append(thread1)

for i in thread_l:
    i.start()
for i in thread_l:
    i.join()