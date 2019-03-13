"""
_thread
"""

# import _thread
import time
import threading
from random import random

def fun():
    print("def fun()", flush=True)

# for i in range(5):
#     t1 = _thread.start_new_thread(fun, ())

def worker(Name):
    print(Name, 'Worker starts')
    time.sleep(2)
    print(Name, 'Worker ended')

for i in range(5):
    startT = time.time()
    rand_value = random()
    # t = threading.Thread(target=worker, args=(rand_value,))
    t = threading.Thread(target=worker, args= ("thread" + str(i),))
    t.start()

    endT = time.time()

    print("completed", t, "total time =", endT-startT)

print("Main thread ended")



class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting" + self.name)
        print_time(self.name, self.counter, 5)
        print("Exiting." + self.name)

def print_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print("%s %s" %(threadName, time.ctime(time.time())))
        counter -= 1 # create new thread
thread1 = myThread(1, "Therad-1", 1)
thread2 = myThread(2, "Therad-2", 2) # start new thread
thread1.start()
thread2.start()
thread1.join()
thread2.join()

print("Main thread ended")
