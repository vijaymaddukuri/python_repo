# 1) Sort the activities according to their finishing time
# 2) Select the first activity from the sorted array and print it.
# 3) If the start time of this activity is greater than or equal to the finish time
#    of previously selected activity then select this activity and print it.

def printMaxActivities(s , f ):

    # Sort the activities according to their finishing time
    for i in range(len(f)-1, 0 , -1):
        for j in range(i):
            if f[j]>f[j+1]:
                temp = f[j]
                f[j] = f[j+1]
                f[j+1]=temp

                temp = s[j]
                s[j] = s[j+1]
                s[j+1]=temp
    print(s)
    print(f)
    n = len(f)
    #  Select the first activity from the sorted array and print it.
    i = 0
    activities=[]
    activities.append(i)

    # If the start time of this activity is greater than or equal to the finish time, select it
    for j in range(n):
        if s[j]>=f[i]:
            activities.append(j)
            i=j
    return activities

s=[3, 1, 0, 5, 8, 5]
f=[4, 2, 6, 7, 9, 9]
print(printMaxActivities(s, f))
