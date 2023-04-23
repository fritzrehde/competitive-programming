#!/usr/bin/env python3

# Array Left Rotation
#
# https://www.hackerrank.com/challenges/array-left-rotation/problem
#
# A left rotation operation on an array of size `n` shifts each of the array's
# elements unit to the left. Given an integer `d`, rotate the array that many
# steps left and return the result.

def test():
    # specify approach
    rotateLeft = Solution().slicing

    # pytest
    assert rotateLeft(2, [1,2,3,4,5]) == [3,4,5,1,2]
    assert rotateLeft(2, [1,2,3]) == [3,1,2]
    assert rotateLeft(5, [1,1,1]) == [1,1,1]
    assert rotateLeft(5, [1]) == [1]
    assert rotateLeft(1, []) == []

class Solution:
    """
    Approach:  Shift index right with modulo
    Idea:      Shift the starting index of the list `d` steps to the right and use modulo for elements that would now be out-of-bounds
    Time:      O(3n) -> O(n), perform addition, modulo and assignment operation every iteration
    Space:     O(n), create the rotated replica of `arr` before returning it
    """
    def listComprehension(self, d: int, arr: list[int]) -> list[int]:
        # modulo below will fail for n=0
        if not arr: return arr

        n = len(arr)
        # example: 2, [1,2,3] => [arr[2%3=2], arr[3%3=0], arr[2%3=1]] => [3,1,2]
        return [arr[(i+d) % n] for i in range(n)]

    """
    Approach:  Slice twice
    Idea:      Shift the starting index of the list `d` steps to the right (1st slice) and concatenate with rest (2nd slice)
    Time:      O(n), slicing array twice costs O(n)
    Space:     O(n), used additional space for two slices, which adds up to input `arr` size
    """
    def slicing(self, d: int, arr: list[int]) -> list[int]:
        # modulo below will fail for n=0
        if not arr: return arr

        # modulo: in case d > len(arr), don't rotate entire array (otherwise out-of-range)
        d = d % len(arr)

        # example: 2, [1,2,3,4,5] => [3,4,5] + [1,2]
        return arr[d:] + arr[:d]
