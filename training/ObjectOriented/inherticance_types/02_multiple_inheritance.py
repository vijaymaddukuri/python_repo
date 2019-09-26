# first parent class
class Person(object):
    def __init__(self, name, idnumber):
        self.name = name
        self.idnumber = idnumber
        self.place = 'Yanam'

    # second parent class


class Employee(object):
    def __init__(self, salary, post):
        self.salary = salary
        self.post = post
        self.place = 'Bangalore'

    # inheritance from both the parent classes


class Leader(Person, Employee):
    def __init__(self, name, idnumber, salary, post, points):
        self.points = points
        Person.__init__(self, name, idnumber)
        Employee.__init__(self, salary, post)
    def show_data(self):
        print("Name is", self.name)
        print("idnumber is", self.idnumber)
        print("salary is", self.salary)
        print("post is", self.post)
        print("points is", self.points)
        print("Place is", self.place)

ins = Leader('Rahul', 882016, 75000, 'Assistant Manager', 560)
ins.show_data()


class First(object):
  def __init__(self):
    print("First(): entering")
    super(First, self).__init__()
    print("First(): exiting")

class Second(object):
  def __init__(self):
    print("Second(): entering")
    super(Second, self).__init__()
    print("Second(): exiting")

class Third(First, Second):
  def __init__(self):
    print("Third(): entering")
    super(Third, self).__init__()
    print("Third(): exiting")
print('\n')
Third()