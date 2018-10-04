def add_fracs(*args):
    sum1 = (map(lambda x:x.split('/'), args))
    print sum1
    sum2 = 0
    first, second = sum1

    if first[1] == second[1]:
        numerator = first[0]+ second[0]
        return '{}/{}'.format(numerator, first[1])
    for x in sum1:
        sum2 += float(x[0])/int(x[1])
    print sum2


add_fracs('1/2', '1/4')

# print float('2/3')