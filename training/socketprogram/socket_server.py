'''
A dummy tcp server
'''
import socketserver
from time import ctime

class CustomerRequestHandler(socketserver.BaseRequestHandler):
    """
       RequestHandler handling incoming request
       """
    def handle(self):
        """
        Will get invoked for request
        """
        print("received : {}".format(self.client_address))
        ts = ctime().encode('ascii')
        self.request.send(ts)

def main():
    """
    Create & invoke tcp server instance
    """
    server_add=('localhost', 7788)
    server =socketserver.TCPServer(server_add, CustomerRequestHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()
