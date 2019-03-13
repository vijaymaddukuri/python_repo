"""
Process: Running a program 
Data segment (CPU)
Code Area  (INstruction to execute code)
Stack (manage function variables, calls)
Heap (Dynamic memory allocation)

Threading: An effective way of concurrency, bcoz it defined as light weight process. 
Thread share the code area, data segemnt of parent process
Threading is cost effective and uses lesser CPU power

Threading contains thrad local storage, stack
"""
import threading
import time
from random import random

def worker(delay):
    t_id=threading.current_thread().ident
    t_name= threading.current_thread().getName()
    time.sleep(delay)
    print("{} : {} waited for the: {}\n".format(time.ctime(),t_name,delay))
    pass

def main():
    thread_objects = []

    for item in range(1,6):
        rand_value=random()
        t=threading.Thread(target=worker, args=(rand_value,))
        thread_objects.append(t)
        t.start()

    for t in thread_objects:
        t.join() #Main thread to wait for child thread execution

    print('Main thread terminates')

if __name__ == '__main__':
    main()