#!/usr/bin/env python3

# Reverse Integer
#
# https://leetcode.com/problems/reverse-integer/
#
# Given a signed 32-bit integer x, return x with its digits reversed. If
# reversing x causes the value to go outside the signed 32-bit integer range
# [-2^31, 2^31 - 1], then return 0.


import math


def test():
    """
    Run `pytest <this-file > `.
    """

    def test_algo(algo):
        assert algo(123) == 321

        assert algo(-123) == -321

        assert algo(120) == 21

        # Edge case: single digit
        assert algo(9) == 9

        # Edge case: single digit
        assert algo(9) == 9

        # Edge case: smallest 32-bit integer.
        assert algo(-8463847412) == -2147483648

        # Edge case: one beyond smallest 32-bit integer.
        assert algo(-9463847412) == 0

        # Edge case: largest 32-bit integer.
        assert algo(7463847412) == 2147483647

        # Edge case: one beyond smallest 32-bit integer.
        assert algo(8463847412) == 0

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force]:
        test_algo(algo)


class Solution:
    def brute_force(self, x: int) -> int:
        """
        Approach:  Brute-force.
        Idea:      Convert the number to a string to reverse the digits.
        Time:      O(n): Reversing a number with n digits takes O(n).
        Space:     O(n): We temporarily store the n digits in a list.
        Leetcode:  28 ms runtime, 16.54 MB memory
        """

        # The sign of the reversed number.
        sign = "-" if x < 0 else ""
        x = abs(x)

        # Convert number to string to extract digits.
        digits = [digit for digit in str(x)]
        # Reverse digits.
        digits.reverse()

        # Combine sign and reversed digits
        res = int(sign + "".join(digits))

        # Edge case: return 0 if not representable in 32-bits.
        i32_min, i32_max = -2**31, 2**31-1
        if not (i32_min <= res <= i32_max):
            return 0

        return res
