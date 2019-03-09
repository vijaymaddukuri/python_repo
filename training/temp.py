class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def collinear(arr):
    n = len(arr)
    count = 0

    for p in range(n):
        for q in range(p+1, n):
            for r in range(q+1, n):
                result = arr[p].x*(arr[q].y - arr[r].y) + arr[q].x*(arr[r].y - arr[p].y) + arr[r].x*(arr[p].y - arr[q].y)
                if not result:
                    count += 1
    print(count)

a = [Point(0,0), Point(1,1), Point(2,2), Point(3,3), Point(3,2), Point(4,2), Point(5,1)]
collinear(a)