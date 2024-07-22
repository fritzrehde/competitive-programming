#!/usr/bin/env python3

# Valid Palindrome
#
# https://leetcode.com/problems/valid-palindrome/
#
# A phrase is a palindrome if, after converting all uppercase letters into
# lowercase letters and removing all non-alphanumeric characters, it reads the
# same forward and backward. Alphanumeric characters include letters and
# numbers.
#
# Given a string s, return true if it is a palindrome, or false otherwise.


from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(s="A man, a plan, a canal: Panama") == True

        assert algo(s="race a car") == False

        assert algo(s=" ") == True

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.two_pointer, solution.two_pointer_inplace, solution.reverse, solution.reverse_less_allocation]:
        test_algo(algo)


class Solution:
    def two_pointer(self, s: str) -> bool:
        """
        Approach:  Two pointer.
        Idea:      Filter out all non-alphanumeric chars and lower all chars, and then iterate with left and right pointer and assert left and right chars are equal.
        Time:      O(n): O(n) for filtering out non-alphanumeric chars, O(n) for mapping to lower, and O(n) for one two pointer pass for checking palindrome validity.
        Space:     O(n): We re-allocate the filtered and lowerd string.
        Leetcode:  51 ms runtime, 21.84 MB memory
        """

        def is_valid_palindrome(chars: List[str]) -> bool:
            n = len(chars)
            (left, right) = (0, n - 1)
            while left < right:
                if chars[left] != chars[right]:
                    return False
                left += 1
                right -= 1
            return True

        return is_valid_palindrome(list(map(str.lower, filter(str.isalnum, s))))

    def two_pointer_inplace(self, s: str) -> bool:
        """
        Approach:  Two pointer, in-place.
        Idea:      Filter out all non-alphanumeric chars and lower all chars, and then iterate with left and right pointer and assert left and right chars are equal.
        Time:      O(n): O(n) for filtering out non-alphanumeric chars, O(n) for mapping to lower, and O(n) for one two pointer pass for checking palindrome validity.
        Space:     O(1): There is no additional allocation.
        Leetcode:  52 ms runtime, 17.04 MB memory
        """

        n = len(s)
        (left, right) = (0, n - 1)
        while left < right:
            (s_left, s_right) = (s[left], s[right])

            # Filter out non-alphanumeric characters.
            if not s_left.isalnum():
                left += 1
                continue
            if not s_right.isalnum():
                right -= 1
                continue

            if s[left].lower() != s[right].lower():
                return False

            left += 1
            right -= 1
        return True

    def reverse(self, s: str) -> bool:
        """
        Approach:  Reverse string.
        Idea:      Filter out all non-alphanumeric chars and lower all chars, and compare string with reversed string.
        Time:      O(n): O(n) for filtering out non-alphanumeric chars, O(n) for mapping to lower, and one two pointer pass for checking palindrome validity.
        Space:     O(n): We collect the filtered, lowered list, and the reversed list.
        Leetcode:  43 ms runtime, 22.59 MB memory
        """

        chars = list(map(str.lower, filter(str.isalnum, s)))
        return chars == list(reversed(chars))

    def reverse_less_allocation(self, s: str) -> bool:
        """
        Approach:  Two pointer, in-place.
        Idea:      Filter out all non-alphanumeric chars and lower all chars, and then iterate with left and right pointer and assert left and right chars are equal.
        Time:      O(n): O(n) for filtering out non-alphanumeric chars, O(n) for mapping to lower, and one two pointer pass for checking palindrome validity.
        Space:     O(n): There is no additional allocation.
        Leetcode:  55 ms runtime, 21.79 MB memory
        """

        def iters_eq(iter_a, iter_b) -> bool:
            """Check whether two iterators (assume same length) contain same elements."""
            return all(item_a == item_b for (item_a, item_b) in zip(iter_a, iter_b))

        chars = list(map(str.lower, filter(str.isalnum, s)))
        return iters_eq(chars, reversed(chars))
