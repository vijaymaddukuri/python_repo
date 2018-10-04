"""
No access needed to either class or instance object
Most likely an implementation detail of the class
ABle to moved to become a module-scope function
"""

class ShippingContainer:
    next_serial = 1337

    @staticmethod
    def _get_next_serail():
        result = ShippingContainer.next_serial
        ShippingContainer.next_serial+=1
        return result

    def __init__(self, code, content):
        self.code = code
        self.content = content
        self.serial = ShippingContainer._get_next_serail()

c = ShippingContainer('YML', 'coffee')
print(c.serial)
print(c.next_serial)