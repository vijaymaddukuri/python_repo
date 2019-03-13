import inspect

from training.ObjectOriented.Inheritance_and_Subtype_Polymorphism import sorted_list

print(dir(inspect))

print(inspect.getmembers(sorted_list, inspect.isclass))

