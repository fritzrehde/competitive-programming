#!/usr/bin/env python3

# Jewels and Stones
#
# https://leetcode.com/problems/jewels-and-stones
#
# You're given strings jewels representing the types of stones that are jewels,
# and stones representing the stones you have. Each character in stones is a
# type of stone you have. You want to know how many of the stones you have are
# also jewels.
# Letters are case sensitive, so "a" is considered a different type of stone
# from "A".


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(jewels="aA", stones="aAAbbbb") == 3
        assert algo(jewels="z", stones="ZZ") == 0

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.hash_set, solution.regex]:
        test_algo(algo)


class Solution:
    def brute_force(self, jewels: str, stones: str) -> int:
        """
        Approach:  Brute-force.
        Idea:      Keep only the stones that are jewels in a filtering pass, and count them.
        Time:      O(n*m): For each of the n stones, check whether it is a jewel (O(m)).
        Space:     O(1): No additional memory is used.
        Leetcode:  39 ms runtime, 16.43 MB memory
        """

        def is_jewel(stone: str) -> bool:
            """Check if a stone is a jewel."""
            for jewel in jewels:
                if stone == jewel:
                    return True
            return False

        def count(iter) -> int:
            """Count the number of elements in a iterator without collecting."""
            return sum(1 for _ in iter)

        return count(filter(is_jewel, stones))

    def hash_set(self, jewels: str, stones: str) -> int:
        """
        Approach:  Use hashset.
        Idea:      Keep only the stones that are jewels in a filtering pass, and count them.
        Time:      O(n): For each of the n stones, check whether it is a jewel (O(1) due to hashset contains efficiency).
        Space:     O(m): Store the m jewels as a hashset.
        Leetcode:  39 ms runtime, 16.51 MB memory
        """

        jewels_set = set(jewels)

        def is_jewel(stone: str) -> bool:
            """Check if a stone is a jewel."""
            return stone in jewels_set

        def count(iter) -> int:
            """Count the number of elements in a iterator without collecting."""
            return sum(1 for _ in iter)

        return count(filter(is_jewel, stones))

    def regex(self, jewels: str, stones: str) -> int:
        """
        Approach:  Use regex.
        Idea:      Remove all non-jewels using regex, and count remaining.
        Time:      O(n): Assume regex substitution takes O(n) for n stones.
        Space:     O(m): Store the all jewels in a string (at most size m).
        Leetcode:  52 ms runtime, 16.49 MB memory
        """

        import re

        # Remove all non-jewels.
        jewels_only = re.sub(rf"[^{jewels}]", "", stones)
        return len(jewels_only)

    def occurences_in_string(self, jewels: str, stones: str) -> int:
        """
        Approach:  Count jewel occurences in stones.
        Idea:      For each jewel, count its number of occurences in the stones string, and return the total sum.
        Time:      O(n*m): For each of the m jewels, count the number of times it occurs in the stones string (O(n)).
        Space:     O(1): No additional memory is used.
        Leetcode:  47 ms runtime, 16.54 MB memory
        """

        return sum(map(lambda jewel: stones.count(jewel), jewels))

    def occurences_in_string_2(self, jewels: str, stones: str) -> int:
        """
        Approach:  Count stone occurences in jewels.
        Idea:      For each stone, count its number of occurences in the jewels string, and return the total sum.
        Time:      O(n*m): For each of the n stones, count the number of times it occurs in the jewels string (O(m)).
        Space:     O(1): No additional memory is used.
        Leetcode:  30 ms runtime, 16.40 MB memory
        """

        return sum(map(lambda stone: jewels.count(stone), stones))
