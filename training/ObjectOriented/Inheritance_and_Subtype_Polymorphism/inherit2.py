class Pet(object):
    def __init__(self,name,species):
        self.name=name
        self.species=species

    def getName(self):
        return self.name

    def getSpecies(self):
        return self.species

class Dog(Pet):
    def __init__(self,name,chaseCat):
        Pet.__init__(self,name,'Dog')
        self.chaseCat=chaseCat

    def chaseCats(self):
        return self.chaseCat


class Cat(Pet):
    def __init__(self, name, HateDog):
        Pet.__init__(self, name, 'Cat')
        self.HateDog = HateDog

    def HateDogs(self):
        return self.HateDog
pet=Pet('cherry','Dog')
print pet.getName()
dog=Dog('Tommy', True)
print dog.chaseCats()
print dog.getName()
print dog.getSpecies()