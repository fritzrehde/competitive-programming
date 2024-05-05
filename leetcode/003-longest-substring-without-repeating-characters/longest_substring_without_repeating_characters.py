#!/usr/bin/env python3

# Longest Substring Without Repeating Characters
#
# https://leetcode.com/problems/longest-substring-without-repeating-characters/
#
# Given a string s, find the length of the longest substring without repeating
# characters.

from typing import Callable, Optional, TypeVar


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        # "abc" in "abcabcbb" with length 3
        assert algo("abcabcbb") == 3

        # "b" in "bbbbb" with length 1
        assert algo("bbbbb") == 1

        # "wke" in "pwwkew" with length 3
        assert algo("pwwkew") == 3

        # "" in "" with length 0
        assert algo("") == 0

        # "b" in "b" with length 1
        assert algo("b") == 1

        # " " in " " with length 1
        assert algo(" ") == 1

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.brute_force_early_exit, solution.sliding_window]:
        test_algo(algo)


class Solution:
    def brute_force(self, s: str) -> int:
        """
        Approach:  Brute-force.
        Idea:      For every starting character, find the longest possible substring from that character onwards until a repeating char is found.
        Time:      O(n^2): For every starting character (of which there are n), iterate through (at most) all following characters (of which there are at most n).
        Space:     O(n^2): For every starting character (of which there are n), create a hashset that stores at most all following characters (of which there are at most n).
        Leetcode:  268 ms runtime, 16.62 MB memory
        """
        max_len_substring = 0

        n = len(s)
        for i in range(0, n):
            # All chars we have visited in our current run.
            substring = set()
            for j in range(i, n):
                # Exit once repeating char is found.
                if s[j] in substring:
                    break
                else:
                    substring.add(s[j])

            # Once the run has ended, possibly update the max length substring.
            max_len_substring = max(len(substring), max_len_substring)

        return max_len_substring

    def brute_force_early_exit(self, s: str) -> int:
        """
        Approach:  Brute-force with early exit once longer substring is impossible.
        Idea:      Same as regular brute-force, just with an early exit.
        Time:      O(n^2): Same as regular brute-force, since the early exit does not affect time complexity in a meaningful way.
        Space:     O(n^2): Same as regular brute-force, since the early exit does not affect time complexity in a meaningful way.
        Leetcode:  249 ms runtime, 16.6 MB memory
        """
        max_len_substring = 0

        n = len(s)
        for i in range(0, n):
            # The longest possible substring we could make from index i onwards.
            longest_possible_substring_len = n - i
            if (max_len_substring >= longest_possible_substring_len):
                # We cannot possibly find another longer substring.
                break

            # All chars we have visited in our current run.
            substring = set()
            for j in range(i, n):
                # Exit once repeating char is found.
                if s[j] in substring:
                    break
                else:
                    substring.add(s[j])

            # Once the run has ended, possibly update the max length substring.
            max_len_substring = max(len(substring), max_len_substring)

        return max_len_substring

    def sliding_window(self, s: str) -> int:
        """
        Approach:  Sliding window.
        Idea:      Maintain a sliding window over the string that contains only unique characters, growing the sliding window as far as possible to the right until shrinking it from the left is necessary because duplicate characters were encountered. Start with a sliding window of size 0 at the left and repeat the steps until the sliding window reaches the end of the string (where it will have size 0 again).
        Time:      O(2n) = O(n): There at most 2n iterations, since each left index and each right index could both be in any position in the string once, after which they are incremented, and each iteration takes O(1) because the hashset contains, insert and discard operations are O(1).
        Space:     O(n): The sliding window grows to at most size n of the string if all elements in the string are unique.
        Leetcode:  71 ms runtime, 16.72 MB memory
        """
        max_len_substring = 0

        n = len(s)

        # The left and right indices/pointers of the sliding window.
        left_idx = 0
        right_idx = 0

        # The sliding window, which contains all chars inside it (i.e. represents the substring from the left to right index).
        sliding_window = set()

        # Iterate until sliding window has arrived at end of string (where we will have left_idx == n and right_idx == n).
        while left_idx < n:
            if (right_idx < n) and (not s[right_idx] in sliding_window):
                # Since the next char is not in our current sliding window, we can include it by extending the right index of our sliding window by one step.
                sliding_window.add(s[right_idx])
                right_idx += 1

                # TODO: It might be faster to calculate the length of the current sliding window as (right_idx - left_idx + 1) instead.
                # Possibly update the max length substring.
                max_len_substring = max(len(sliding_window), max_len_substring)
            else:
                # Since the next char is not in our current sliding window, we can include it by extending the right index of our sliding window by one step.
                sliding_window.discard(s[left_idx])
                left_idx += 1

        return max_len_substring

    def sliding_window_early_exit(self, s: str) -> int:
        """
        Approach:  Sliding window with early exit once longer substring is impossible.
        Idea:      Same as regular sliding window, just with an early exit.
        Time:      O(n): Same as regular sliding window, since the early exit does not affect time complexity in a meaningful way.
        Space:     O(n): Same as regular sliding window, since the early exit does not affect time complexity in a meaningful way.
        Leetcode:  47 ms runtime, 16.63 MB memory
        """
        max_len_substring = 0

        n = len(s)

        # The left and right indices/pointers of the sliding window.
        left_idx = 0
        right_idx = 0

        # The sliding window, which contains all chars inside it (i.e. represents the substring from the left to right index).
        sliding_window = set()

        # Iterate until sliding window has arrived at end of string (where we will have left_idx == n and right_idx == n).
        while left_idx < n:
            # The longest possible substring we could make from the left index onwards.
            longest_possible_substring_len = n - left_idx
            if (max_len_substring >= longest_possible_substring_len):
                # We cannot possibly find another longer substring.
                break

            if (right_idx < n) and (not s[right_idx] in sliding_window):
                # Since the next char is not in our current sliding window, we can include it by extending the right index of our sliding window by one step.
                sliding_window.add(s[right_idx])
                right_idx += 1

                # TODO: It might be faster to calculate the length of the current sliding window as (right_idx - left_idx + 1) instead.
                # Possibly update the max length substring.
                max_len_substring = max(len(sliding_window), max_len_substring)
            else:
                # Since the next char is not in our current sliding window, we can include it by extending the right index of our sliding window by one step.
                sliding_window.discard(s[left_idx])
                left_idx += 1

        return max_len_substring
