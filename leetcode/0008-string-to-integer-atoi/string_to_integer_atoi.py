#!/usr/bin/env python3

# String To Integer (Atoi)
#
# https://leetcode.com/problems/string-to-integer-atoi/
#
# Implement the myAtoi(string s) function, which converts a string to a 32-bit
# signed integer.
#
# The algorithm for myAtoi(string s) is as follows:
#
# Whitespace: Ignore any leading whitespace (" ").
# Signedness: Determine the sign by checking if the next character is '-' or
# '+', assuming positivity is neither present.
# Conversion: Read the integer by skipping leading zeros until a non-digit
# character is encountered or the end of the string is reached. If no digits
# were read, then the result is 0.
# Rounding: If the integer is out of the 32-bit signed integer range [-2^31,
# 2^31 - 1], then round the integer to remain in the range. Specifically,
# integers less than -2^31 should be rounded to -2^31, and integers greater than
# 2^31 - 1 should be rounded to 2^31 - 1.
#
# Return the integer as the final result.


from enum import Enum


def test():
    """
    Run `pytest <this-file > `.
    """

    def test_algo(algo):
        assert algo("42") == 42

        assert algo("+42") == 42

        assert algo("-042") == -42

        # Both - and + signs not allowed.
        assert algo("-+42") == 0

        # Stop reading at first non-digit character ' '.
        assert algo("4 2") == 4

        # Stop reading at first non-digit character 'c'.
        assert algo("1337c0d3") == 1337

        # Stop reading at first non-digit character '-'.
        assert algo("0-1") == 0

        # Stop reading at first non-digit character 'w'.
        assert algo("words and 987") == 0

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force]:
        test_algo(algo)


class Solution:
    def brute_force(self, s: str) -> int:
        """
        Approach:  Brute-force.
        Idea:      Iterate over the chars of the string, consuming chars according to the rules. Use python's built-in string to int function for actual conversion.
        Time:      O(n): Given a string of length n, we iterate over each character once.
        Space:     O(1): We don't allocate anything.
        Leetcode:  40 ms runtime, 16.48 MB memory
        """

        i = 0
        n = len(s)

        # Skip leading whitespace.
        while i < n and s[i] == " ":
            i += 1

        # Extract sign, if one exists.
        negative = False
        if i < n:
            match s[i]:
                case "-":
                    negative = True
                    i += 1
                case "+":
                    negative = False
                    i += 1

        # Skip leading zeros.
        while i < n and s[i] == "0":
            i += 1

        def is_ascii_digit(c: str) -> bool:
            "Return whether the char is a valid ASCII digit."
            return "0" <= c <= "9"

        # Capture all valid digits, and convert
        l = i
        r = i
        while r < n and is_ascii_digit(s[r]):
            r += 1

        if l == r:
            # If there were no valid digits, return 0 as default.
            number = 0
        else:
            digits = s[l:r]
            number = int(digits, 10)

        # Apply sign.
        signed = -number if negative else number

        def clamp(n: int, smallest: int, largest: int) -> int:
            return max(smallest, min(n, largest))

        # Rounding to min and max 32-bit values.
        i32_min, i32_max = -2**31, 2**31-1
        return clamp(signed, i32_min, i32_max)
