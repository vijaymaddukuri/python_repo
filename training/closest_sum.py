"""
Given an array (ints) of n integers, find three integers in arr such that the sum is closest
to a given number (num), target.

Return the sum of the three integers. You may assume that each input would have exactly one solution.

closest_sum([-1, 2, 1, -4], 1) # 2 (-1 + 2 + 1 = 2)
"""

def closest_sum(nums, target):

    closest = nums[0] + nums[1] + nums[2]
    for i in range(len(nums)):
        if i != len(nums) - 1:
            temp = nums[:i] + nums[i + 1:]
        else:
            temp = nums[:len(nums) - 1]

        temp = sorted(temp)

        l, r = 0, len(temp) - 1
        t = target - nums[i]

        while (l < r):
            if abs(temp[l] + temp[r] + nums[i] - target) < abs(closest - target):
                closest = temp[l] + temp[r] + nums[i]

            if temp[l] + temp[r] == t:

                return target
            elif temp[l] + temp[r] > t:
                r = r - 1
            else:
                l = l + 1

    return closest

from itertools import combinations
def closest_sum1(ints, num):
    return sum(min(combinations(ints, 3), key=lambda a: abs(num - sum(a))))

print(closest_sum([-2, 2, -3, 1], 3))

