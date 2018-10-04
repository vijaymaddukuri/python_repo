def reverse_fun(s):
    if len(s)==0:
        return s
    else:
        revStr=s[::-1]
        for iter in range(3):
            index=len(s)-iter
            lst1 = revStr[index:]
            lst2 = revStr[:index]
            final = lst1 + lst2
            print final
            # revStr = revStr[:index+1]+(revStr[index+1:])[::-1]
        return revStr

reverse_fun("string")