import time, threading

def op():
    od = ''
    while 1:
        time.sleep(1)
        try:
            with open('output.tmp') as f:
                data = f.read()
                if od != data:
                    print(data)
                    od = data
        except:
            continue

def ip():
    odl = 0
    while 1:
        cmd = input(">>>")
        with open('input.tmp','w+') as f:
            f.write(cmd)

thread_l =[]
thread0 = threading.Thread(target = op, args = ())
thread_l.append(thread0)
thread1 = threading.Thread(target = ip, args = ())
thread_l.append(thread1)

for i in thread_l:
    i.start()
for i in thread_l:
    i.join()