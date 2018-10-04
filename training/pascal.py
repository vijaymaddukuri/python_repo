def pascal(p):
    def create_row(n):
        row = [1]
        for k in range(n):
            row.append(row[k] * (n-k) / (k+1))
        return row
    tri = []
    for a in range(p):
        tri.append(create_row(a))
    return tri

p=pascal(7)
print p