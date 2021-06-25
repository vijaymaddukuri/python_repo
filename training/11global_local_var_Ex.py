# Nonlocal: Introduces names from the enclosing namespace  into the local namespace

message = 'global'

def enclosing():
    message = 'enclosing'
    def local():
        global message
        message = 'local'
        print('Name inside local def', message)
    print('enclosing message', message)
    local()
    print('enclosing message', message)

print('global message', message)
enclosing()
print('global message', message)
