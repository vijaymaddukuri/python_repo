import socket

def connectToHost():
    socketObj=socket.socket()
    host=socket.gethostname()
    port=12345
    print host
    socketObj.bind((host,port))
    socketObj.listen(5)
    while True:
        client,addr=socketObj.accept()
        print 'got connect from ', addr
        client.send('Thank you for connecting')
        client.close

connectToHost()