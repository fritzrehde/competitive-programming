#!/usr/bin/env python3

# Roman to Integer
#
# https://leetcode.com/problems/roman-to-integer
#
# Roman numerals are represented by seven different symbols: I, V, X, L, C, D
# and M.
#
# Symbol       Value
# I             1
# V             5
# X             10
# L             50
# C             100
# D             500
# M             1000
# For example, 2 is written as II in Roman numeral, just two ones added
# together. 12 is written as XII, which is simply X + II. The number 27 is
# written as XXVII, which is XX + V + II.
# Roman numerals are usually written largest to smallest from left to right.
# However, the numeral for four is not IIII. Instead, the number four is written
# as IV. Because the one is before the five we subtract it making four. The same
# principle applies to the number nine, which is written as IX. There are six
# instances where subtraction is used:
#
# I can be placed before V (5) and X (10) to make 4 and 9.
# X can be placed before L (50) and C (100) to make 40 and 90.
# C can be placed before D (500) and M (1000) to make 400 and 900.
#
# Given a roman numeral, convert it to an integer.


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(s="III") == 3
        assert algo(s="LVIII") == 58
        assert algo(s="MCMXCIV") == 1994

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.no_special_map]:
        test_algo(algo)


class Solution:
    def brute_force(self, s: str) -> int:
        """
        Approach:  Brute-force.
        Idea:      ?
        Time:      O(n): ?
        Space:     O(1): ?
        Leetcode:  57 ms runtime, 16.54 MB memory
        """

        n = len(s)

        normal = {
            "I": 1,
            "V": 5,
            "X": 10,
            "L": 50,
            "C": 100,
            "D": 500,
            "M": 1000,
        }

        special = {
            "IV": 4,
            "IX": 9,
            "XL": 40,
            "XC": 90,
            "CD": 400,
            "CM": 900,
        }

        res = 0
        i = 0
        while i < n:
            # If we still have capacity for special, try parsing special.
            if i + 1 < n:
                if (value := special.get(s[i : i + 2], None)) is not None:
                    res += value
                    i += 2
                    continue

            # Otherwise parse normal.
            value = normal[s[i]]
            res += value
            i += 1

        return res

    def no_special_map(self, s: str) -> int:
        """
        Approach:  Brute-force.
        Idea:      ?
        Time:      O(n): ?
        Space:     O(1): ?
        Leetcode:  41 ms runtime, 16.61 MB memory
        """

        n = len(s)

        roman_to_int = {
            "I": 1,
            "V": 5,
            "X": 10,
            "L": 50,
            "C": 100,
            "D": 500,
            "M": 1000,
        }

        res = 0
        i = 0
        while i < n:
            # If we still have capacity for special, try parsing special.
            if i + 1 < n:
                # If the higher roman char is smaller than the lower roman char,
                # then this must be a special case.
                if roman_to_int[s[i]] < roman_to_int[s[i + 1]]:
                    value = roman_to_int[s[i + 1]] - roman_to_int[s[i]]
                    res += value
                    i += 2
                    continue

            # Otherwise parse normally.
            value = roman_to_int[s[i]]
            res += value
            i += 1

        return res
