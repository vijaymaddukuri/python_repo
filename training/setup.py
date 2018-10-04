#To make packages distributable

from distutils.core import setup
#"disutils:Distrubuted utilities"

setup(name='processmanager',
      version=1.0,
      packages=['processmanager'])

#Command: C:\Python27\python.exe setup.py sdist
#Install pckg: C:\Python27\python.exe -mpip install dist/processmanager-1.0.zip