#!/usr/bin/env python3

# Kids With the Greatest Number of Candies
#
# https://leetcode.com/problems/kids-with-the-greatest-number-of-candies
#
# There are n kids with candies. You are given an integer array candies, where
# each candies[i] represents the number of candies the ith kid has, and an
# integer extraCandies, denoting the number of extra candies that you have.
# Return a boolean array result of length n, where result[i] is true if, after
# giving the ith kid all the extraCandies, they will have the greatest number of
# candies among all the kids, or false otherwise.
# Note that multiple kids can have the greatest number of candies.


from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(candies=[2, 3, 5, 1, 3], extraCandies=3) == [
            True,
            True,
            True,
            False,
            True,
        ]
        assert algo(candies=[4, 2, 1, 1, 2], extraCandies=1) == [
            True,
            False,
            False,
            False,
            False,
        ]
        assert algo(candies=[12, 1, 12], extraCandies=10) == [True, False, True]

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force]:
        test_algo(algo)


class Solution:
    def brute_force(self, candies: List[int], extraCandies: int) -> List[bool]:
        """
        Approach:  Brute-force.
        Idea:      Calculate the maximum amount of candy a kid had before getting extra candy, and then compare each kid's candy plus the extra candy with this maximum value.
        Time:      O(n): Getting the max takes O(n), and checking if each kid has more candy than the max after adding the extra candy takes O(n).
        Space:     O(1): No additional memory is used.
        Leetcode:  34 ms runtime, 16.53 MB memory
        """

        max_candy_without_extra = max(candies)

        def kid_has_most_candies_after_extra(kid: int) -> bool:
            return (candies[kid] + extraCandies) >= max_candy_without_extra

        n = len(candies)
        return [kid_has_most_candies_after_extra(kid=i) for i in range(0, n)]
