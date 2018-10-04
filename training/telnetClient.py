import telnetlib

host="localhost"
user = "training".encode('ascii') #unicode to byte string
passwd= "training"

try:
    telnet = telnetlib.Telnet(host)
    telnet.read_until(b'login: ')
    telnet.write(user + b'\n')
    telnet.read_until(b'Password: ')
    telnet.write(passwd + b'\n')
    telnet.write( b'date\n')
    telnet.write(b'free\n')
    telnet.write(b'exit\n')
    print(telnet.read_all().decode('ascii')) #byte string to unicode

finally:
    telnet.close()