#!/usr/bin/env python3

# Maximum Product Subarray
#
# https://leetcode.com/problems/maximum-product-subarray
#
# Given an integer array nums, find a subarray that has the largest product, and
# return the product.
# The test cases are generated so that the answer will fit in a 32-bit integer.


from functools import reduce
from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(nums=[2, 3, -2, 4]) == 6
        assert algo(nums=[-2, 0, -1]) == 0
        assert algo(nums=[-2]) == -2
        assert algo(nums=[2, 3, -2, 4]) == 6

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.greedy]:
        test_algo(algo)


class Solution:
    def brute_force(self, nums: List[int]) -> int:
        """
        Approach:  Brute-force.
        Idea:      Generate all n^2 possible subarrays, calculate the product for each, and take the largest.
        Time:      O(n^3): For each of the n^2 possible subarrays, get the product (O(n)), and then take the max of all of those products (O(n^2) since there are O(n^2) products).
        Space:     O(n^3): We generate n^2 subarrays, each of at most size n.
        Leetcode:  ? ms runtime, ? MB memory
        """

        def all_subarrays(array: List[int]):
            n = len(array)
            for subarray_len in range(1, n + 1):
                for subarray_start in range(0, (n + 1) - subarray_len):
                    subarray_end = subarray_start + subarray_len
                    yield array[subarray_start:subarray_end]

        def product(array: List[int]) -> int:
            return reduce(lambda a, b: a * b, array, 1)

        return max(map(product, all_subarrays(nums)))

    def greedy(self, nums: List[int]) -> int:
        """
        Approach:  Greedy.
        Idea:      While iterating over nums, maintain a largest and smallest product.
        Time:      O(n): For each of the n numbers, calculate the largest and smallest product of a subarray ending at and including that number (O(1) each).
        Space:     O(1): No additional memory is used.
        Leetcode:  68 ms runtime, 17.03 MB memory
        """

        n = len(nums)

        def max_products():
            for i in range(0, n):
                # Calculate the maximum subarray product in nums[:i], always
                # including nums[i].
                if i == 0:
                    # Base case:
                    min_product = nums[i]
                    max_product = nums[i]
                else:
                    # Either extend the subarray if total product is
                    # smaller/larger, or start new subarray from here.
                    (min_product, max_product) = (
                        min(
                            nums[i]
                            * (min_product if nums[i] >= 0 else max_product),
                            nums[i],
                        ),
                        max(
                            nums[i]
                            * (max_product if nums[i] >= 0 else min_product),
                            nums[i],
                        ),
                    )
                yield max_product

        return max(max_products())
