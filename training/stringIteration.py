# example where s = "String" and x = 3:
# after 0 iteration  s = "String" 012345
#                        gnirts      543210
# after 1 iteration  s = "gSntir" 504132
# after 2 iterations s = "rgiStn" 253014
# after 3 iterations s = "nrtgSi" 421503

def reverse_fun(s):
    if len(s)==0:
        return s
    else:
        s=s[::-1]
        for iter in range(1, len(s)):
            s = s[:iter]+s[iter:][::-1]
            print s
        return s
print reverse_fun("012345")


arr=[5,4,3,1,2]