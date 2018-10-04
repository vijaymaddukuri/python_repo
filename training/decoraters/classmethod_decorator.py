# If we prefer to use class object, use class method
#Requires access to the class object to call other class methods or the constructor

class ShippingMethod:
    next_serail = 1234

    @classmethod
    def _get_next_serail(cls):
        result = cls.next_serail
        cls.next_serail+=1
        return result

    @classmethod
    def create_empty(cls, owner_code):
        return cls(owner_code, content=None)

    @classmethod
    def create_with_items(cls, owner_code, items):
        return cls(owner_code, content=list(items))

    def __init__(self, goods, content):
        self.goods= goods
        self.content = content
        self.serail = ShippingMethod._get_next_serail()


c = ShippingMethod('YML', 'books')

print(c.next_serail)
print(c.serail)

c1 = ShippingMethod.create_with_items('MEM', ['food', 'clothes'])
print(c1.content)