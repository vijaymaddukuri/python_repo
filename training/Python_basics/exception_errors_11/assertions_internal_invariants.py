def modulus_two(n):
    r = n%3
    if r == 0:
        print("Mul of 3")
    elif r == 1:
        print("Remainder 1")
    else:
        assert r == 2, "Rem is not 2"
        print("Reminder 2")

def modulus_four(n):
    r = n%4
    if r == 0:
        print("Mul of 4")
    elif r == 1:
        print("Remainder 1")
    elif r == 2:
        print("Remainder 2")
    elif r == 3:
        print("Remainder 3")
    else:
        assert False, "This should not happen"

modulus_four(6)
modulus_two(4)