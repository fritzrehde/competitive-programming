#!/usr/bin/env python3

# Product of Array Except Self
#
# https://leetcode.com/problems/product-of-array-except-self
#
# Given an integer array nums, return an array answer such that answer[i] is
# equal to the product of all the elements of nums except nums[i].
# The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit
# integer.
# You must write an algorithm that runs in O(n) time and without using the
# division operation.


from functools import reduce
from typing import Callable, Iterable, List, Optional


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(nums=[1, 2, 3, 4]) == [24, 12, 8, 6]
        assert algo(nums=[-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [
        solution.brute_force,
        solution.prefix_suffix_product,
        solution.prefix_suffix_product_two_pass,
    ]:
        test_algo(algo)


class Solution:
    def brute_force(self, nums: List[int]) -> List[int]:
        """
        Approach:  Brute-force.
        Idea:      Calculate each answer[i] as the product of all nums[j] where j != i.
        Time:      O(n^2): We calculate each of the n answer[i] values by multiplying n-1 numbers.
        Space:     O(1): No additional memory is used.
        Leetcode:  Time Limit Exceeded.
        """

        n = len(nums)

        def product(nums: Iterable[int]) -> int:
            return reduce(lambda a, b: a * b, nums)

        def answer_i(i: int) -> int:
            return product(nums[j] for j in range(0, n) if i != j)

        return [answer_i(i) for i in range(0, n)]

    def prefix_suffix_product(self, nums: List[int]) -> List[int]:
        """
        Approach:  Prefix product and suffix product.
        Idea:      Pre-calculate the prefix and suffix products (products of all numbers until/from each index), so answer[i] can be roughly calculated as prefix_product[i-1] * suffix_product[i+1].
        Time:      O(n): Creating the prefix and suffix product arrays takes O(n) each, and then we need to calculate answer[i] for all n i's, taking O(1) each.
        Space:     O(n): The prefix and suffix product arrays contain n elements each.
        Leetcode:  336 ms runtime, 26.24 MB memory
        """

        n = len(nums)

        def idx_or_default(arr: List[Optional[int]], idx: int, default: int):
            if 0 <= idx < n:
                return arr[idx]
            else:
                return default

        # prefix_product[i] = product(nums[j] for j in range(0, i+1))
        prefix_product = [None] * n
        for i in range(0, n):
            prefix_product[i] = (
                idx_or_default(prefix_product, idx=i - 1, default=1) * nums[i]
            )

        # suffix_product[i] = product(nums[j] for j in range(i, n))
        suffix_product = [None] * n
        for i in reversed(range(0, n)):
            suffix_product[i] = (
                idx_or_default(suffix_product, idx=i + 1, default=1) * nums[i]
            )

        def answer_i(i: int) -> int:
            return idx_or_default(prefix_product, i - 1, 1) * idx_or_default(
                suffix_product, i + 1, 1
            )

        return [answer_i(i) for i in range(0, n)]

    def prefix_suffix_product_two_pass(self, nums: List[int]) -> List[int]:
        """
        Approach:  Prefix product and suffix product, with constant space.
        Idea:      Calculate the prefix and suffix products (products of all numbers until/from each index) on the fly while calculating answer[i].
        Time:      O(n): Do two O(n) passes, one to dynamically calculate and directly apply prefix product to each answer[i], and the same for suffix product.
        Space:     O(1): No additional memory is used, since we calculate prefix and suffix products on the fly.
        Leetcode:  271 ms runtime, 25.77 MB memory
        """

        n = len(nums)

        # answer[i] = prefix_product[i-1] * suffix_product[i+1]
        # <=>
        # answer[i] = 1;
        # answer[i] *= prefix_product[i-1];
        # answer[i] *= suffix_product[i+1]

        answer = [1] * n

        # prefix_product[i] = product(nums[j] for j in range(0, i+1))
        prefix_product_i_minus_1 = 1
        for i in range(0, n):
            answer[i] *= prefix_product_i_minus_1
            prefix_product_i_minus_1 *= nums[i]

        # suffix_product[i] = product(nums[j] for j in range(0, i+1))
        suffix_product_i_plus_1 = 1
        for i in reversed(range(0, n)):
            answer[i] *= suffix_product_i_plus_1
            suffix_product_i_plus_1 *= nums[i]

        return answer
