import inspect
from training.Inheritance_and_Subtype_Polymorphism import sorted_list
print(dir(inspect))

print(inspect.getmembers(sorted_list, inspect.isclass))

from training.Inheritance_and_Subtype_Polymorphism.sorted_list import IntList