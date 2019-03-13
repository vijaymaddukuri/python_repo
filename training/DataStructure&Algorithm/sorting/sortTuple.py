l =[('apple', '3.2','22'), ('apple', '30.2','21'), ('pear', '4.5','24')]
l2 = sorted(l, key=lambda x: x[0] and x[1])
print l2