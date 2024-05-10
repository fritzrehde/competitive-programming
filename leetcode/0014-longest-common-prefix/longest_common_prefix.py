#!/usr/bin/env python3

# Longest Common Prefix
#
# https://leetcode.com/problems/longest-common-prefix/
#
# Write a function to find the longest common prefix string amongst an array of
# strings.
#
# If there is no common prefix, return an empty string "".


from typing import List


def test():
    """
    Run `pytest <this-file > `.
    """

    def test_algo(algo):
        assert algo(["flower", "flight", "flow"]) == "fl"

        assert algo(["dog", "racecar", "car"]) == ""

        # Edge case: all chars besides a middle char are same.
        assert algo(["flower", "floper"]) == "flo"

        # Edge case: a whole word is part of the longest common prefix.
        assert algo(["flower", "flow"]) == "flow"

        # Edge case: one input string is empty.
        assert algo(["", "flower"]) == ""

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.lexicographical_sort]:
        test_algo(algo)


class Solution:
    def brute_force(self, strs: List[str]) -> str:
        """
        Approach:  Brute-force.
        Idea:      Try all possible lengths for a prefix.
        Time:      O(nm): Given a list of n strings where the smallest string has m characters, we try at most m different prefix lengths, and for each prefix length i check whether all strings have the same ith element (O(n)).
        Space:     O(1): There are no additional allocations besides the output string.
        Leetcode:  37 ms runtime, 16.63 MB memory
        """

        def same_ith_element(strs: List[str], i: int) -> str:
            """
            If all strings in a list have the same ith element, return that element, otherwise return None.
            """
            ith_element = None

            for s in strs:
                # Initialize the ith_element once with ith element from first string.
                if ith_element is None:
                    ith_element = s[i]

                if s[i] != ith_element:
                    return None

            return ith_element

        prefix = ""

        # The longest common prefix can be at most as long as the shortest string in the list.
        shortest_str_len = min([len(s) for s in strs], default=0)
        for prefix_len in range(0, shortest_str_len):
            if (ith_element := same_ith_element(strs, prefix_len)) is not None:
                # All strings have the same ith element, so use it to extend our current longest prefix.
                prefix += ith_element
            else:
                break

        return prefix

    def lexicographical_sort(self, strs: List[str]) -> str:
        """
        Approach:  Sort strings lexicographically beforehand.
        Idea:      By sorting the strings lexicographically, we can make use of the property that if the first and last strings have a common prefix, all strings in between will have that same common prefix.
        Time:      O((n log n) m): Given a list of n strings where the longest string has m characters, we first sort the strings lexicographically (O(n log n) comparisons, but each comparison takes at most O(m)), and then we try at most m different prefix lengths, and for each prefix length i we check whether all strings have the same ith element (O(1) due to lexicographical sorting trick).
        Space:     O(1): We sort the string list in-place, so no additional space is used besides the input and output space.
        Leetcode:  35 ms runtime, 16.57 MB memory
        """

        # We sort the strings lexicographically.
        strs.sort()

        def same_ith_element_in_sorted_list(strs: List[str], i: int) -> str:
            """
            If all strings in a lexicographically sorted list have the same ith element, return that element, otherwise return None.
            All strings must be non-empty, and there must be at least one string in the list.
            """

            first_str = strs[0]
            last_str = strs[-1]

            # Since the list of strings is lexicographically sorted, we know that if the first and last string have the same prefix, all other strings in between will also have the same prefix. This implies that if the first and last strings have the same ith element, all other strings in between will also have the same ith element.
            if first_str[i] == last_str[i]:
                return first_str[i]
            else:
                return None

        prefix = ""

        # The longest common prefix can be at most as long as the shortest string in the list.
        shortest_str_len = min([len(s) for s in strs], default=0)
        for prefix_len in range(0, shortest_str_len):
            if (ith_element := same_ith_element_in_sorted_list(strs, prefix_len)) is not None:
                # All strings have the same ith element, so use it to extend our current longest prefix.
                prefix += ith_element
            else:
                break

        return prefix
