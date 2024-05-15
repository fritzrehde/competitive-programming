#!/usr/bin/env python3

# Find The Index Of The First Occurrence In A String
#
# https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/
#
# Given two strings needle and haystack, return the index of the first
# occurrence of needle in haystack, or -1 if needle is not part of haystack.


def test():
    """
    Run `pytest <this-file > `.
    """

    def test_algo(algo):
        assert algo("sadbutsad", "sad") == 0

        assert algo("leetcode", "leeto") == -1

        assert algo("abc", "c") == 2

        # Edge cases that aren't defined in spec.
        # assert algo("", "c") == -1
        # assert algo("abc", "") == -1
        # assert algo("", "") == -1

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.std_lib]:
        test_algo(algo)


class Solution:
    def brute_force(self, haystack: str, needle: str) -> int:
        """
        Approach:  Brute-force.
        Idea:      Use a sliding window with the same size as the needle and slide it right until we find the needle.
        Time:      O(nm): Given a haystack of size n and a needle of size m, our sliding windows covers all n indices (in the worst-case where the needle is not present), and for each sliding window position we do a O(m) string comparison with the needle.
        Space:     O(nm): We are creating a string slice of length m for every one of the n possible sliding window positions, and Python's string slices (unfortunately, unlike e.g. Rust) require allocation.
        Leetcode:  40 ms runtime, 16.50 MB memory
        """

        # Get every possible index in the haystack at which the needle could possibly start.
        for start_idx in range(0, len(haystack) - len(needle) + 1):
            end_idx = start_idx + len(needle) - 1
            if needle == haystack[start_idx:end_idx + 1]:
                return start_idx

        return -1

    def std_lib(self, haystack: str, needle: str) -> int:
        """
        Approach:  Standard library.
        Idea:      Cheat by using the standard library implementation.
        Time:      O(?): We treat it as a black-box.
        Space:     O(?): We treat it as a black-box.
        Leetcode:  33 ms runtime, 16.48 MB memory
        """

        return haystack.find(needle)
