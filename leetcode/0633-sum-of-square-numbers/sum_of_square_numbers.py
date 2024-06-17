#!/usr/bin/env python3

# Sum Of Square Numbers
#
# https://leetcode.com/problems/sum-of-square-numbers/
#
# Given a non-negative integer c, decide whether there're two integers a and b
# such that a^2 + b^2 = c.


from math import ceil, sqrt


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        # 1^2 + 2^2 = 5
        assert algo(5) == True

        assert algo(3) == False

        # 0^2 + 2^2 = 4
        assert algo(4) == True

        # 0^2 + 0^2 = 0
        assert algo(0) == True

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.store_squares, solution.store_squares_and_reuse, solution.check_sqrt_directly]:
        test_algo(algo)


class Solution:
    def brute_force(self, c: int) -> bool:
        """
        Approach:  Brute-force.
        Idea:      Try all possible values for a^2 and b^2, sum them, and check if they equal c.
        Time:      O(c): Try all combinations of a and b, both lie in (0, sqrt(c), so O(sqrt(c) * sqrt(c)) = O(c).
        Space:     O(1): No additional space used.
        Leetcode:  Time Limit Exceeded
        """

        upper = ceil(sqrt(c)) + 1
        for a in range(0, upper):
            for b in range(0, upper):
                if (a**2 + b**2) == c:
                    return True
        return False

    def store_squares(self, c: int) -> bool:
        """
        Approach:  Store squares.
        Idea:      Get all possible values for a**2, so we can quickly check for all possible b's whether there is an a**2 = c - b**2.
        Time:      O(sqrt(c)): Calculate all squares of a (O(c)), and then check if a matching a**2 exists (O(1)) for every possible b**2 (O(c)).
        Space:     O(sqrt(c)): We store all n possible squares of a in a hashset.
        Leetcode:  147 ms runtime, 20.49 MB memory
        """

        upper = ceil(sqrt(c)) + 1
        a_squares = set(a**2 for a in range(0, upper))

        for b in range(0, upper):
            # a**2 + b**2 = c => a**2 = c - b**2
            a_squared = c - b**2
            if a_squared >= 0 and a_squared in a_squares:
                return True
        return False

    def store_squares_and_reuse(self, c: int) -> bool:
        """
        Approach:  Store and reuse squares.
        Idea:      Get all possible values for a**2, then check for all possible b's whether there is an a**2 = c - b**2. Also, reuse squares of a as squares of b.
        Time:      O(sqrt(c)): Calculate all squares of a (O(sqrt(c))), and then check if a matching a**2 exists (O(1)) for every possible b**2 (O(sqrt(c))).
        Space:     O(sqrt(c)): We store all possible squares of a in a hashset.
        Leetcode:  139 ms runtime, 20.60 MB memory
        """

        upper = ceil(sqrt(c)) + 1
        a_squares = set(a**2 for a in range(0, upper))

        # The values of a**2 are the same as the values of b**2.
        for b_squared in a_squares:
            # a**2 + b**2 = c => a**2 = c - b**2
            a_squared = c - b_squared
            if a_squared in a_squares:
                return True
        return False

    def check_sqrt_directly(self, c: int) -> bool:
        """
        Approach:  Calculate and check b.
        Idea:      Get all possible values for a**2, and then check if b = c - a**2 is a whole number.
        Time:      O(sqrt(c)): Iterate over all values of a and check if a matching b exists (O(sqrt(c))).
        Space:     O(1): No additional memory is used.
        Leetcode:  140 ms runtime, 16.65 MB memory
        """

        upper = ceil(sqrt(c)) + 1
        for a in range(0, upper):
            # a**2 + b**2 = c => b = sqrt(c - a**2)
            c_minus_a_squared = c - a**2
            if c_minus_a_squared >= 0:
                b = sqrt(c - a**2)
                if b == int(b):
                    # b is a whole number, and therefore valid.
                    return True
        return False
