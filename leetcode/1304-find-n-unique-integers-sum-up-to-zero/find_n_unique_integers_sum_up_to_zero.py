#!/usr/bin/env python3

# Find N Unique Integers Sum up to Zero
#
# https://leetcode.com/problems/find-n-unique-integers-sum-up-to-zero
#
# Given an integer n, return any array containing n unique integers such that
# they add up to 0.


from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def sums_to_0(l: List[int]) -> bool:
        return sum(l) == 0

    def test_algo(algo):
        assert sums_to_0(algo(n=5))
        assert sums_to_0(algo(n=3))
        assert sums_to_0(algo(n=1))

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.greedy]:
        test_algo(algo)


class Solution:
    def greedy(self, n: int) -> List[int]:
        """
        Approach:  Greedy.
        Idea:      If n is even, pick any numbers i and -i, since their sum cancels out. If n is odd, add a 0.
        Time:      O(n): Iterate over all i's until n // 2.
        Space:     O(1): No additional memory is used.
        Leetcode:  46 ms runtime, 16.80 MB memory
        """

        def zero_sum_even(n_even: int):
            # Ensure 0 and 1 aren't picked as parts of the sum.
            for i in map(lambda i: i + 2, range(0, n_even // 2)):
                yield i
                yield -i

        if (n % 2) == 0:
            return list(zero_sum_even(n))
        else:
            return list(zero_sum_even(n - 1)) + [0]
