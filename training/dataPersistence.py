"""
If data want to save when python process ends and reload the data later when restarts, 

we need to perform data persistence

The available option is pickle & Shelve

Serialization:

High level object into bits and bytes

Unserilazation:

Convert bits and bytes into High level object

Shelve:

Objects will store as keys and values in dbm (data base manager).

We can update the values into the file.

We can store objects in well organized way like keys and values.

"""
import pickle
import shelve
from contextlib import closing
def do_serilize():
    data_set = {
        'lang': 'python',
        'auth': 'larry',
        'version': 2.14,
        'platform': ['linux', 'windows']
    }

    pickle.dump(data_set, open('serial.dat', 'wb'))

def do_unserialize():
    content=pickle.load(open('serial.dat','rb'))
    print(content)

def dump_it():
    sh=shelve.open('dump.shelve')
    sh['nums'] = [1.1,2.4,3.5,4.5]
    sh['prop'] = {
        'release': '1',
        'version': 1.1
    }
    sh['host'] = 'ws1'
    sh['version'] = 2.2

    sh.close()

def load_it():
    sh=shelve.open('dump.shelve')
    for key,value in sh.items():
        print(key, ':', value)
    sh.close()

def add_item(key,value):
    '''
    with:
     context manager to perform IO operation effectively by handling events (entry(allocate), exit (deallocate))
    '''
    with closing(shelve.open('dump.shelve')) as sh:
        sh[key] = value

# do_serilize()
# do_unserialize()
dump_it()
add_item('os','windows')
load_it()