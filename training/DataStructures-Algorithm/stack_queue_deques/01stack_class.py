# Stacks:
# A stack is an ordered collection of items where the addition of new items and the removal of existing
# items always take place in the same end.
#
# This end commonly referred as the top.
#
# The opposite end of the top is base.
#
# The base of the stack is significant since items stored in the stack, that are closer to the
# base represent those that have been in the stack the longest
#
# Most recently added item is the one that is in position to be removed first. (LIFO)
#
# Newers items are near to the top, older items near to the base.
#
# Order of insertion is the reverse of order of removal.
#
# Example: Every web browser has a back button.
#
# As you navigate from web page to web page, those pages are placed on a stack (URLS that are going on the stack).


class stack(object):
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        return self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    def size(self):
        return len(self.items)

obj = stack()
print(obj.isEmpty())
obj.push(1)
print(obj.peek())
print(obj.size())
print(obj.isEmpty())
print(obj.pop())
print(obj.size())
