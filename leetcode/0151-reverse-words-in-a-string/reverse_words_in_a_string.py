#!/usr/bin/env python3

# Reverse Words in a String
#
# https://leetcode.com/problems/reverse-words-in-a-string
#
# Given an input string s, reverse the order of the words.
# A word is defined as a sequence of non-space characters. The words in s will
# be separated by at least one space.
# Return a string of the words in reverse order concatenated by a single space.
# Note that s may contain leading or trailing spaces or multiple spaces between
# two words. The returned string should only have a single space separating the
# words. Do not include any extra spaces.


from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(s="the sky is blue") == "blue is sky the"
        assert algo(s="  hello world  ") == "world hello"
        assert algo(s="a good   example") == "example good a"

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.reverse]:
        test_algo(algo)


class Solution:
    def brute_force(self, s: str) -> str:
        """
        Approach:  Brute-force.
        Idea:      ?
        Time:      O(n): ?
        Space:     O(n): ?
        Leetcode:  44 ms runtime, 16.64 MB memory
        """

        return " ".join(reversed(s.split()))

    def reverse(self, s: str) -> str:
        """
        Approach:  Brute-force.
        Idea:      ?
        Time:      O(n): ?
        Space:     O(1): ?
        Leetcode:  58 ms runtime, 16.56 MB memory
        """

        def collapse_spaces(chars: List[str]):
            n = len(chars)
            write_ptr = 0
            read_ptr = 0
            while read_ptr < n:
                # Skip whitespace.
                while read_ptr < n and chars[read_ptr] == " ":
                    read_ptr += 1

                if write_ptr == 0 or read_ptr == n:
                    # Don't keep leading or trailing whitespace.
                    pass
                else:
                    chars[write_ptr] = " "
                    write_ptr += 1

                # Write next word.
                while read_ptr < n and chars[read_ptr] != " ":
                    chars[write_ptr] = chars[read_ptr]
                    write_ptr += 1
                    read_ptr += 1
            new_size = write_ptr
            chars[:] = chars[:new_size]

        def iter_words():
            """Return (starting index, ending index), both inclusive, of each word."""
            n = len(chars)
            i = 0
            while i < n:
                # Skip whitespace before next word.
                while i < n and chars[i] == " ":
                    i += 1
                start_idx = i
                # Skip word.
                while i < n and chars[i] != " ":
                    i += 1
                end_idx = i - 1
                yield (start_idx, end_idx)

        chars = list(s)

        collapse_spaces(chars)

        # Reverse whole string.
        chars.reverse()

        # Reverse each individual word.
        for start_idx, end_idx in iter_words():
            l = start_idx
            r = end_idx
            while l < r:
                chars[l], chars[r] = chars[r], chars[l]
                l += 1
                r -= 1

        return "".join(chars)
