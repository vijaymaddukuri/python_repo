from pprint import pprint as pp
class Prime(object):
    def pprint(self):
        print('print from the class prime')

class Alpha(object):
    def pprint(self):
        print('print from the class Alpha')

class Beta(object):
    def pprint(prime):
        print('print from the class Beta')

class vijay(Alpha, Beta):
    def pprint(self):
        super(vijay, self).pprint() #method reading object

if __name__ == '__main__':
    vijay().pprint()

