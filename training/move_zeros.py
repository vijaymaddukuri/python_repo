def move_zeros(array):
    import re
    z = ans = []
    print array
    for i in range(len(array)):
        if array[i] == 0 and (type(array[i]) == int or type(array[i]) == float):
            z = z + [0]
        else:
            ans = ans + [array[i]]

    return ans +z

l=move_zeros([9,0.0,0,9,1,2,0,1,False,1,0.0,3,0,1,9,0,0,0,0,9])
print l

'''
["a",0,0,"b",None,"c","d",0,1,False,0,1,0,3,[],0,1,9,0,0,{},0,0,9])
['a', 'b', None, 'c', 'd', 1, 1, 3, [], 1, 9, {}, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
["a","b",None,"c","d",1,False,1,3,[],1,9,{},9,0,0,0,0,0,0,0,0,0,0])
'''
