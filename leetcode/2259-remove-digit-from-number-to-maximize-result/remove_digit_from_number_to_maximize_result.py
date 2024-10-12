#!/usr/bin/env python3

# Remove Digit From Number to Maximize Result
#
# https://leetcode.com/problems/remove-digit-from-number-to-maximize-result
#
# You are given a string number representing a positive integer and a character
# digit.
# Return the resulting string after removing exactly one occurrence of digit
# from number such that the value of the resulting string in decimal form is
# maximized. The test cases are generated such that digit occurs at least once
# in number.


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(number="123", digit="3") == "12"
        assert algo(number="1231", digit="1") == "231"
        assert algo(number="551", digit="5") == "51"

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.greedy]:
        test_algo(algo)


class Solution:
    def brute_force(self, number: str, digit: str) -> str:
        """
        Approach:  Brute-force.
        Idea:      Generate all possible numbers with the digit removed (at most n), and find the largest.
        Time:      O(n): Given the number has n digits, any of them could be the input digit we need to remove.
        Space:     O(n^2): We generate at most n strings of length n-1.
        Leetcode:  38 ms runtime, 16.58 MB memory
        """

        n = len(number)

        def all_possibilities():
            for i in range(0, n):
                if number[i] == digit:
                    yield number[:i] + number[i + 1 :]

        return max(all_possibilities())

    def greedy(self, number: str, digit: str) -> str:
        """
        Approach:  Greedy.
        Idea:      Our greedy observation is that the number will be largest if we remove the highest (bitwise) digit that is followed by a larger digit.
        Time:      O(n): Given the number has n digits, any of them could be the input digit we need to remove.
        Space:     O(1): No additional memory is used.
        Leetcode:  25 ms runtime, 16.46 MB memory
        """

        n = len(number)

        def all_occurences():
            for i in range(0, n):
                if number[i] == digit:
                    yield i

        last_i = -1
        for i in all_occurences():
            if (i + 1) < n:
                # There is a larger digit after number[i].
                if number[i] < number[i + 1]:
                    # Remove digit at index i.
                    return number[:i] + number[i + 1 :]
            last_i = i

        # We found no better i to remove, so we're forced to remove last
        # occurence of digit.
        return number[:last_i] + number[last_i + 1 :]
