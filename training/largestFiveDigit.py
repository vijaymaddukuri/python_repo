def solution(digits):
    temp=[]
    j=0
    if len(digits)>5:
        for i in range(5,len(digits),5):
            new=digits[j:i]
            temp.append(new)
            j=i
        new=sorted(temp)
        if digits[-6:-1]==new[-1]:
            return 'Failed when max 5 digits is at end of number'
        else:
            return new[-1]
    else:
        return 0

a='1234567898765'

sol=solution(a)
print(sol)