class Customer(object):
    def __init__(self, name, balance=10000.0, limit=5000.0):
        self.name=name
        self.balance=balance
        self.limit=limit
    def currentBalance(self):
        return self.balance

    def deposit(self,amount):
        self.balance += amount
        return self.balance

    def withdraw(self,amount):
        if amount > self.balance:
            raise RuntimeError('Insufficent Balance available in the account')
        if amount > self.limit:
            raise RuntimeError('Amount exceeded the limit')
        self.balance -= amount
        return self.balance


class Car(object):
    @staticmethod
    def carSound():
        return 'pipee'

car1=Car()
print(car1.carSound())
acc1 = Customer('vijay')
acc1Balance=acc1.withdraw(501)
print('%s' %(acc1Balance))