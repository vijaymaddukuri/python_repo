def sqInRect(lng, wdth):
    if lng == wdth:
        return None
    else:
        total=lng*wdth
        print total
        squares=[]
        for i in range(total,0,-1):
            for j in range(i+1):
                if j*j==i:
                    squares.append(j)
        highest=squares[0]*squares[0]
        square=[squares[0]]
        for i in squares:
            if highest+(i*i)<=total:
                highest = highest + (i * i)
                square.append(i)
        while highest!=total:
            highest = highest + 1
            square.append(1)
        return square


s=sqInRect(5,4)
print s

16+9+4+1
