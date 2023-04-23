#!/usr/bin/env python3

# Two Sum
#
# https://leetcode.com/problems/two-sum/
#
# Given an array of integers `nums` and an integer `target`, return indices of
# the two numbers such that they add up to `target`.

def test():
    # specify approach
    two_sum = Solution().one_pass

    # pytest
    assert two_sum([2,7,11,15], 9) == [0,1]
    assert two_sum([3,2,4], 6) == [1,2]
    assert two_sum([3,3], 6) == [0,1]

class Solution:
    """
    Approach:  Naive/brute-force solution
    Idea:      For each number, check if addition with any other number equals `target`
    Time:      O(n^2), for each element we loop through entire list
    Space:     O(1), no allocations
    Leetcode:  3653 ms runtime, 14.9 MB memory
    """
    def naive(self, nums: list[int], target: int) -> list[int]:
        ln = len(nums)
        for i in range(ln):
            for j in range(i+1, ln):
                if (nums[i] + nums[j] == target):
                    return [i, j]

    """
    Approach:  Two-pass with dictionary
    Idea:      Create a dictionary storing the complements of each list number, and then find complement
    Time:      O(2n) -> O(n), list is traversed twice, once to build dict and once to find complement
    Space:     O(n), space for dictionary
    Leetcode:  62 ms runtime, 15.4 MB memory
    """
    def two_pass(self, nums: list[int], target: int) -> list[int]:
        # create dict of the complements (value and index) of each number
        complements = {target-num:i for i,num in enumerate(nums)}

        # find position for which complement exists in list, filter out same index
        for i, num in enumerate(nums):
            if i != complements.get(num, i):
                return [i, complements[num]]

    """
    Approach:  One-pass with dictionary
    Idea:      Only check if compliment for a value has already been seen
    Time:      O(n), list is traversed once (second traversal is avoided through faster dict.get())
    Space:     O(n), space for dictionary
    Leetcode:  51 ms runtime, 15.1 MB memory
    """
    def one_pass(self, nums: list[int], target: int) -> list[int]:
        complements = dict()
        for i, num in enumerate(nums):
            complement = target - num

            # check if complement has already been seen
            if (j := complements.get(complement)) is not None:
                return [j, i]
            else:
                complements[num] = i
