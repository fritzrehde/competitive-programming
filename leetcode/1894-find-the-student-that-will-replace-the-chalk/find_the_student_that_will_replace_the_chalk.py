#!/usr/bin/env python3

# Find the Student that Will Replace the Chalk
#
# https://leetcode.com/problems/find-the-student-that-will-replace-the-chalk
#
# There are n students in a class numbered from 0 to n - 1. The teacher will
# give each student a problem starting with the student number 0, then the
# student number 1, and so on until the teacher reaches the student number n -
# 1. After that, the teacher will restart the process, starting with the student
# number 0 again.
# You are given a 0-indexed integer array chalk and an integer k. There are
# initially k pieces of chalk. When the student number i is given a problem to
# solve, they will use chalk[i] pieces of chalk to solve that problem. However,
# if the current number of chalk pieces is strictly less than chalk[i], then the
# student number i will be asked to replace the chalk.
# Return the index of the student that will replace the chalk pieces.


from itertools import repeat
from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(chalk=[5, 1, 5], k=22) == 0
        assert algo(chalk=[3, 4, 1, 2], k=25) == 1

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.optimized]:
        test_algo(algo)


class Solution:
    def brute_force(self, chalk: List[int], k: int) -> int:
        """
        Approach:  Brute-force.
        Idea:      Iterate over the chalk array many (at most over k students) times, until all chalk has been used up.
        Time:      O(k): There is k chalk in total, in the worst case each student uses 1 chalk piece, so we need to iterate over k students (O(1) each).
        Space:     O(1): No additional memory is used.
        Leetcode:  Time Limit Exceeded.
        """

        n = len(chalk)
        used_chalk = 0
        while True:
            for i in range(0, n):
                used_chalk += chalk[i]
                if used_chalk > k:
                    return i
        raise Exception("unreachable")

    def optimized(self, chalk: List[int], k: int) -> int:
        """
        Approach:  Optimized.
        Idea:      Calculate total chalk usage per round as sum(chalk), so we can skip all complete rounds and focus only on the remaining chalk pieces after m full rounds. Then, iterate over the chalk array at most n times, until all chalk has been used up.
        Time:      O(n): We know all chalk wil be used up before the end of one round, and one round has length n.
        Space:     O(1): No additional memory is used.
        Leetcode:  580 ms runtime, 30.56 MB memory
        """

        n = len(chalk)
        k = k % sum(chalk)
        used_chalk = 0
        for i in range(0, n):
            used_chalk += chalk[i]
            if used_chalk > k:
                return i
        raise Exception("unreachable")
