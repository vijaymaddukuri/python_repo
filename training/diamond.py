def diamond(n):
    diamond=''
    if n%2!=0:
        for i in range(1,n+1,2):
            center=int((n-i)/2)
            diamond=diamond+(' '*center+ '*'*i)+'\n'
        for j in range(n-2,0,-2):
            center=int((n-j)/2)
            diamond=diamond+(' '*center+ '*'*j)+'\n'
    else:
        diamond="Unable to form diamond with even number"
    return diamond

diamond=diamond(3)
print(diamond)