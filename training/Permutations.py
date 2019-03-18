def permutations1(string):
    def factorial(n):
        fact=1
        for i in range(1,n+1):
            fact=fact*i
        return fact
    repeat=len(string)-len(''.join(set(string)))
    n=factorial(len(string))
    k=factorial(repeat)
    loop=n/(k**repeat)
    final=[]
    j=0
    for i in range(loop):
        if i>=2:
            j=0
        else:
            j+=1
        new = string[j-1:] + string[j-1:]

        final.append(new)
        string=new
    return final

    return loop

def permutations(string):
    result = set(string)
    if len(string) == 2:
        result.add(string[1] + string[0])

    elif len(string) > 2:
        for i, c in enumerate(string):
            for s in permutations(string[:i] + string[i + 1:]):
                result.add(c + s)
    return list(result)
a='abc'
per=permutations(a)
print(per)


