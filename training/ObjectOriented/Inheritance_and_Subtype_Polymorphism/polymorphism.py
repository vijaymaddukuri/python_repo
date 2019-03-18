class vehicle:
    def __init__(self,name):
        self.name=name

    def tyres(self):
        raise NotImplementedError('subclass need to define')


class car(vehicle):
    def tyres(self):
        return "Four tyres"

class bike(vehicle):
    def tyres(self):
        return "Two tyrers"


class bus(vehicle):
    def tyres(self):
        return "Six tyres"


count= bike('scooty').tyres()

count1= bus('volvo').tyres()

count2= bus('').tyres()

print(count)
