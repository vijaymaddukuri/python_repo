def sort_my_string1(S):
    e=''
    o=''
    print S[::2]
    print S[1::2]
    for i in range(len(S)):
        if i%2==0:
            e+=S[i]
        else:
            o+=S[i]
    return e + " " + o

def sort_my_string(s):
    return s[::2] + ' ' + s[1::2]

print(sort_my_string1('vijaykumar'))