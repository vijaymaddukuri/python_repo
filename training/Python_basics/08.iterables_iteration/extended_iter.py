"""
Extended iter() is often used for creating infinite sequences from existing functions
"""
import datetime
i = iter(datetime.datetime.now, None)
print(next(i))
print(next(i))
print(next(i))

import os
import sys
dir_path = (sys.path)[0]
file_path = os.path.join(dir_path,'extended_iter_sample')
with open(file_path, 'rt') as f:
    for line in iter(lambda: f.readline().strip(), 'End'):
        print(line)

import random
import itertools
import time
class Sensor:
    def __iter__(self):
        return self
    def __next__(self):
        return random.random()

sensor = Sensor()
timestamps = iter(datetime.datetime.now, None)

for stamp, value in itertools.islice(zip(timestamps, sensor), 10):
    print(stamp, value)
    time.sleep(1)