import threading
import logging
from time import sleep
from random import random

fmt="%(threadName)s: %(message)s"
logging.basicConfig(level=logging.DEBUG, format=fmt)

def consumer(cond, data):
    logging.debug('created')
    if not data:
        logging.debug('Content is unavailable & gets wait')
    with cond:
        cond.wait()
        logging.debug('recv notify, consumes : {}'.format(data.pop(0)))

def producer(cond, data):
    logging.debug('Created & Produces')
    data.append(random())
    data.append(random())

    with cond:
        logging.debug('Notifes the waiting thread')
        cond.notify_all()

def main():
    cond = threading.Condition()
    data = []
    c1= threading.Thread(target=consumer, name="C1", args=(cond, data))
    c2 = threading.Thread(target=consumer, name="C2", args=(cond, data))
    c1.start()
    c2.start()
    sleep(2)
    p=threading.Thread(target=producer, name="P", args=(cond, data))
    p.start()

if __name__ == '__main__':
    main()