def comp(array1, array2):
    try:
        #return sorted([i ** 2 for i in array1]) == sorted(array2)

        return True
    except:
        return False

a = [121, 144, 19, 161, 19, 144, 19, 11]
b = [11*11, 121*121, 144*144, 19*19, 161*161, 19*19, 144*144, 19*19]
res=comp(a,b)
print res