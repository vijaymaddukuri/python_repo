import os
import sys
import os.path
os.getcwd()
os.chdir(r'D:\new')
import shutil

def fileCreate():
    ''''
    Open the file and read the content
    '''

    #srcfile = 'a/long/long/path/to/file.py'
    #dstroot = '/home/myhome/new_folder'
    srcfile = r'D:\new\profile.txt'
    dstfile = r'D:\softy\profile1.txt'
    text_file = open(srcfile, 'r+')
    # Copy the content from Source file into a variable
    lines = text_file.read()
    #Create File in the destination folder
    WriteToFile=open(dstfile,'w')
    #Copy the content from source file
    WriteToFile.write(lines)
    WriteToFile.close()
    ReadNewFile = open(dstfile, 'r+')
    lines = ReadNewFile.read()
    print(lines)


fileCreate()

