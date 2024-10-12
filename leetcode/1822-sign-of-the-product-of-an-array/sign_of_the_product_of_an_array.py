#!/usr/bin/env python3

# Sign of the Product of an Array
#
# https://leetcode.com/problems/sign-of-the-product-of-an-array
#
# Implement a function signFunc(x) that returns:
#
# 1 if x is positive.
# -1 if x is negative.
# 0 if x is equal to 0.
#
# You are given an integer array nums. Let product be the product of all values
# in the array nums.
# Return signFunc(product).


from functools import reduce
from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(nums=[-1, -2, -3, -4, 3, 2, 1]) == 1
        assert algo(nums=[1, 5, 0, 2, -3]) == 0
        assert algo(nums=[-1, 1, -1, 1, -1]) == -1

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [
        solution.brute_force,
        solution.track_sign_with_int,
        solution.track_sign_with_bool,
        solution.count_negatives,
    ]:
        test_algo(algo)


class Solution:
    def brute_force(self, nums: List[int]) -> int:
        """
        Approach:  Brute-force.
        Idea:      Just calculate the product.
        Time:      O(n): Multiply n numbers together.
        Space:     O(1): No additional memory is used.
        Leetcode:  60 ms runtime, 16.96 MB memory
        """

        product = reduce(lambda a, b: a * b, nums)
        if product > 0:
            return 1
        elif product < 0:
            return -1
        else:
            return 0

    def track_sign_with_int(self, nums: List[int]) -> int:
        """
        Approach:  Track sign with int.
        Idea:      Iterate over the numbers, tracking the current sign of the result as 1 or -1.
        Time:      O(n): Iterate over n numbers.
        Space:     O(1): No additional memory is used.
        Leetcode:  61 ms runtime, 16.96 MB memory
        """

        sign = 1
        for num in nums:
            if num == 0:
                # If any factor is 0, the product is 0.
                return 0

            if num < 0:
                # If we see a negative number, the sign is flipped.
                sign *= -1

        return sign

    def track_sign_with_bool(self, nums: List[int]) -> int:
        """
        Approach:  Track sign with bool.
        Idea:      Iterate over the numbers, tracking the current sign of the result as negative or positive (bool).
        Time:      O(n): Iterate over n numbers.
        Space:     O(1): No additional memory is used.
        Leetcode:  55 ms runtime, 16.88 MB memory
        """

        positive = True
        for num in nums:
            if num == 0:
                # If any factor is 0, the product is 0.
                return 0

            if num < 0:
                # If we see a negative number, the sign is flipped.
                positive = not positive

        return 1 if positive else -1

    def count_negatives(self, nums: List[int]) -> int:
        """
        Approach:  Count negatives.
        Idea:      We notice that the positive factors don't affect the sign of the result, only if we have uneven number negatives negatives can the sign of the result be negative.
        Time:      O(n): Iterate over n number.
        Space:     O(1): No additional memory is used.
        Leetcode:  61 ms runtime, 16.80 MB memory
        """

        def is_even(i: int) -> bool:
            return i % 2 == 0

        negative_count = 0
        for num in nums:
            if num == 0:
                # If any factor is 0, the product is 0.
                return 0
            if num < 0:
                negative_count += 1

        return 1 if is_even(negative_count) else -1
