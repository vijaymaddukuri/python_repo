import socket

class Resolver:

    def __init__(self):
        self._cache={}

    def __call__(self, host):
        if host not in self._cache:
            self._cache[host] = socket.gethostbyname(host)
            print(self._cache[host] )
        return host in self._cache

    def clear(self):
        self._cache.clear()

    def has_host(self, host):
        return host in self._cache

resolve = Resolver()
print(resolve.has_host('localhost'))
print(resolve('localhost'))
print(resolve.has_host('localhost'))