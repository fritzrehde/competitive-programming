#!/usr/bin/env python3

# Maximum Score From Removing Substrings
#
# https://leetcode.com/problems/maximum-score-from-removing-substrings/
#
# You are given a string s and two integers x and y. You can perform two types
# of operations any number of times.
#
# Remove substring "ab" and gain x points.
# For example, when removing "ab" from "cabxbae" it becomes "cxbae".
# Remove substring "ba" and gain y points.
# For example, when removing "ba" from "cabxbae" it becomes "cabxe".
#
# Return the maximum points you can gain after applying the above operations on
# s.


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(s="cdbcbbaaabab", x=4, y=5) == 19
        assert algo(s="aabbaaxybbaabb", x=5, y=4) == 20

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force]:
        test_algo(algo)


class Solution:
    def brute_force(self, s: str, x: int, y: int) -> int:
        """
        Approach:  Brute-force.
        Idea:      In a first linear pass, we count and remove all occurences of the higher valued substrings, and in the second we do the same for the lower valued substrings.
        Time:      O(n): Each pass iterates over all n elements, doing O(1) work for each.
        Space:     O(n): The stack we build up can be at most as large as the input array if no valued substring is found/removed.
        Leetcode:  354 ms runtime, 18.54 MB memory
        """

        str_for_score = {x: "ab", y: "ba"}
        higher_score, lower_score = (x, y) if x >= y else (y, x)

        score = 0

        def single_pass(desired_score: int) -> str:
            nonlocal score
            leftover_s_stack = []
            for c in s:
                if leftover_s_stack and (leftover_s_stack[-1] + c) == str_for_score[desired_score]:
                    leftover_s_stack.pop()
                    score += desired_score
                else:
                    leftover_s_stack.append(c)

            return leftover_s_stack

        # First pass: remove all instances of higher scoring substring.
        s = single_pass(higher_score)

        # Second pass: remove all instances of lower scoring substring.
        s = single_pass(lower_score)

        return score
