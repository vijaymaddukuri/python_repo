# Print a long integer representing the maximum area of rectangle formed.
def largestRectangle(h):
    s = []
    ans = len(h)
    h.append(0)

    for i in range(len(h)):
        left_index = i
        while len(s) > 0 and s[-1][0] >= h[i]:
            last = s.pop()
            left_index = last[1]
            ans = max(ans, h[i] * (i + 1 - last[1]))
            ans = max(ans, last[0] * (i - last[1]))
        s.append((h[i], left_index))

    return ans

print(largestRectangle([1,2,3,4,5]))