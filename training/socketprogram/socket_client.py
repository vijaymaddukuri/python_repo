import socket

try:
    sock = None
    server_addr = ('localhost', 7788)
    sock = socket.socket()
    sock.connect(server_addr)
    ts=sock.recv(1024)
    print(ts.decode('ascii'))
finally:
    if sock:
        sock.close()