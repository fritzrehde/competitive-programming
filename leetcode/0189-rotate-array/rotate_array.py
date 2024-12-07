#!/usr/bin/env python3

# Rotate Array
#
# https://leetcode.com/problems/rotate-array
#
# Given an integer array nums, rotate the array to the right by k steps, where k
# is non-negative.


from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def assert_in_place_is(nums, k, expected):
        algo(nums, k)
        assert nums == expected

    def test_algo(algo):
        assert_in_place_is(
            nums=[1, 2, 3, 4, 5, 6, 7], k=3, expected=[5, 6, 7, 1, 2, 3, 4]
        )
        assert_in_place_is(
            nums=[-1, -100, 3, 99], k=2, expected=[3, 99, -1, -100]
        )
        # Test with large k.
        assert_in_place_is(
            nums=[1, 2, 3, 4, 5, 6, 7], k=17, expected=[5, 6, 7, 1, 2, 3, 4]
        )

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.rev, solution.cycles]:
        test_algo(algo)


class Solution:
    # def brute_force(self, nums: List[int], k: int) -> None:
    #     """
    #     Approach:  Brute-force.
    #     Idea:      ?
    #     Time:      O(?): ?
    #     Space:     O(?): ?
    #     Leetcode:  ? ms runtime, ? MB memory
    #     """
    #     n = len(nums)
    #     k = n % k

    #     def rotated_idx(i: int) -> int:
    #         j = i + k
    #         return j if j < n else j - n

    #     for i in range(0, n):
    #         j = rotated_idx(i)
    #         print(i, j)
    #         nums[i], nums[j] = nums[j], nums[i]

    # def smort(self, nums: List[int], k: int) -> None:
    #     """
    #     Approach:  Brute-force.
    #     Idea:      ?
    #     Time:      O(?): ?
    #     Space:     O(?): ?
    #     Leetcode:  ? ms runtime, ? MB memory
    #     """
    #     n = len(nums)
    #     k = n % k

    #     def next(i: int) -> int:
    #         j = i + k
    #         return j if j < n else j - n

    #     i, j = 0, k
    #     while j != 0:
    #         nums[i], nums[j] = nums[j], nums[i]
    #         i, j = j, next(i)

    def brute_force(self, nums: List[int], k: int) -> None:
        """
        Approach:  Brute-force.
        Idea:      Calculate the rotated index for each index, and fill up copied array that way.
        Time:      O(n): ?
        Space:     O(n): ?
        Leetcode:  7 ms runtime, 25.01 MB memory
        """
        n = len(nums)

        copy = [-1 for _ in range(n)]

        def rotated_idx(i: int) -> int:
            return (i + k) % n

        for i in range(0, n):
            copy[rotated_idx(i)] = nums[i]

        nums[:] = copy

    def rev(self, nums: List[int], k: int) -> None:
        """
        Approach:  Reverse ranges.
        Idea:      ?
        Time:      O(n): ?
        Space:     O(1): ?
        Leetcode:  3 ms runtime, 25.10 MB memory
        """
        n = len(nums)
        k = k % n

        def rev_range(arr: List[int], i: int, j: int):
            "i inclusive, j inclusive"
            l = i
            r = j
            while l < r:
                arr[l], arr[r] = arr[r], arr[l]
                l += 1
                r -= 1

        # If we shift right by k, that means that the last k values will
        # overflow to the front. By reversing the array, the first k elements
        # will now be exactly those last k elements we want at the front, just
        # in the wrong order, which we can fix by reversing. The remaining
        # elements (from k onwards) will also be in the right position but
        # reversed, so we reverse them as well.

        # Reverse whole array.
        rev_range(nums, 0, n - 1)
        # Reverse left of k.
        rev_range(nums, 0, k - 1)
        # Reverse right of (including) k.
        rev_range(nums, k, n - 1)

    def cycles(self, nums: List[int], k: int) -> None:
        """
        Approach:  In cycles.
        Idea:      ?
        Time:      O(n): ?
        Space:     O(1): ?
        Leetcode:  11 ms runtime, 25.21 MB memory
        """
        n = len(nums)

        def rotated_idx(i: int) -> int:
            return (i + k) % n

        num_rotated = 0
        start = 0
        while num_rotated < n:
            # Iterate in steps of k (wrapping around) until we reach start again
            # (complete a cycle).
            i = start
            nums_i = nums[i]
            while num_rotated < n:
                j = rotated_idx(i)
                # We have to store nums[j] elsewhere so we don't lose it when
                # it's overridden.
                nums[j], nums_j = nums_i, nums[j]
                num_rotated += 1
                # Take next step of length k to j.
                i = j
                nums_i = nums_j

                if i == start:
                    break

            # The next value is guaranteed not to have been visited yet.
            start += 1
