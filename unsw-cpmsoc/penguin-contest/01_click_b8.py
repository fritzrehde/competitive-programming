#!/usr/bin/env python3

# Click B8
#
# https://contest.unswcpmsoc.com/task/click-b8/
#
# As the temperature drops, Pip the Penguin and her seven friends are preparing
# to build an igloo. Each of the eight penguins, including Pip, has a favourite
# integer Bi.
# Pip decides that the number of ice blocks in the igloo should be the sum of
# Bi x Bj over all indices i and j such that i < j. Determine the total number
# of ice blocks Pip needs.


# Run `pytest <this-file>`.
def test():
    def test_algo(algo):
        assert algo([8, 3, 100, 0, 0, 0, 0, 0]) == 1124

        assert algo([1, 1, 1, 1, 1, 1, 1, 1]) == 28

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force]:
        test_algo(algo)


class Solution:
    def brute_force(self, B: list[int]) -> int:
        """
        Approach:  Brute-force
        Idea:      Iterate over all values of i and j where i < j, calculate Bi x Bj, and return their sum.
        Time:      O(n^2): There are n possible values of i, and another O(n) possible values of j > i.
        Space:     O(1): No allocations.
        Points:    10/10
        """

        n = len(B)
        res = sum((B[i] * B[j]) for i in range(0, n) for j in range(i + 1, n))

        return res
