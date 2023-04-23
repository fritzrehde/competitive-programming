#!/usr/bin/env python3

# Arrays - DS
#
# https://www.hackerrank.com/challenges/arrays-ds/problem
#
# Reverse an array of integers.

def test():
    # specify approach
    reverseArray = Solution().loop

    # pytest
    assert reverseArray([1,2,3,4,5]) == [5,4,3,2,1]
    assert reverseArray([1,2,1]) == [1,2,1]
    assert reverseArray([1,1,1]) == [1,1,1]
    assert reverseArray([]) == []

class Solution:
    """
    Approach:  Using standard library `reverse()` function
    Idea:      Well, we're basically just cheating by using the std lib function
    Time:      O(n), must iterate through entire list at least once to "see" every element
    Space:     O(1), `reverse()` operates in-place
    """
    def stdLib(self, arr: list[int]) -> list[int]:
        arr.reverse()
        return arr

    """
    Approach:  Swap elements in loop
    Idea:      Iterate through list while swapping elements with same distance from middle
    Time:      O(n), iterate only through half the list, but two operations per iteration
    Space:     O(1), operates in-place
    """
    def loop(self, arr: list[int]) -> list[int]:
        n = len(arr)
        for i in range(n // 2):
            # swap arr[i] and arr[n-i-1]
            arr[i], arr[n-i-1] = arr[n-i-1], arr[i]
        return arr
