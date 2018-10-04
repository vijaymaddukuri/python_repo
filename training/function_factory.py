def raise_to(exp):
    def raise_to_expr(x):
        return pow(x, exp)
    return raise_to_expr

square = raise_to(2)
print(square(5))
cube = raise_to(3)
print(cube(3))
print(square.__closure__)