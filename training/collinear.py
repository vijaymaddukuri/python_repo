"""
Given the coordinates of the three vertices of any triangle, the area of the triangle is given by:
area	=
Ax * (By − Cy) + Bx * (Cy − Ay) +	Cx * (Ay −	By )

If the area comes out to be zero, it means the three points are collinear.
They lie in a straight line and do not form a triangle.
You can drag the points above to create this condition.

Refer: https://www.mathopenref.com/coordtrianglearea.html

       https://stackoverflow.com/questions/3813681/checking-to-see-if-3-points-are-on-the-same-line



"""

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

def solution(A):
  n = len(A)
  cnt = 0
  for p in range(n):
      for q in range(p+1, n):
          for r in range(q+1, n):
              if A[p].x*(A[q].y - A[r].y) + A[q].x*(A[r].y - A[p].y) + A[r].x*(A[p].y - A[q].y)== 0:
                  cnt += 1
              if cnt > 100000000:
                  return -1
  return cnt

a = [Point(0,0), Point(1,1), Point(2,2), Point(3,3), Point(3,2), Point(4,2), Point(5,1)]
print(solution(a))