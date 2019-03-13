"""
Instance bound proxy:
super(class, instance-of-class)

Finds the MRO of second argument.
Finds the location of the first argument in the MRO
Uses everything  after that for resolving methods
"""
from training.ObjectOriented.Inheritance_and_Subtype_Polymorphism.sorted_list import *

sil = SortedIntlist([5, 15, 10])
super(SortedList, sil)
super(SortedList, sil).add(6)


