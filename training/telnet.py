import telnetlib
import os
import getpass

host = "localhost"
username = 'D433'
password = 'vijaykumar.m'
tn=telnetlib.Telnet(host)
tn.read_until("login: ")
tn.write(username + "\n")
tn.read_until("Password: ")
tn.write(password + "\n")
tn.write("ls\n")
tn.wrtie("exit")
tn.read_all
