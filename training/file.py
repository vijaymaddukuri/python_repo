import os
import sys
import os.path
os.getcwd()
os.chdir(r'D:\new')
from itertools import islice
fname='vijay.txt'
fsize = os.stat(fname).st_size
print fsize
nlines=10
def slice(filename,nLines):
    with open(filename) as f:
        for line in islice(f,nLines):
            print(line)
#slice(fname,nlines)


def writeContent(filename,content):
    with open(filename,'w') as f:
        f.write('vicky \n')
        f.write(content)

    txt=open(filename)
    print(txt.read())
writeContent(fname,'vijaykumar')

def slice(filename,nLines):
    with open(filename) as f:
        for line in islice(f,nLines):
            print(line)
slice(fname,nlines)
fsize = os.stat(fname).st_size
print fsize

def textList(filename):
    with open(filename) as f:
        contentList=f.readlines()
        print contentList
textList(fname)

def longestWord(fname)