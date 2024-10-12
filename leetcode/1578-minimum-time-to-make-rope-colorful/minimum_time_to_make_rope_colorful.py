#!/usr/bin/env python3

# Minimum Time to Make Rope Colorful
#
# https://leetcode.com/problems/minimum-time-to-make-rope-colorful
#
# Alice has n balloons arranged on a rope. You are given a 0-indexed string
# colors where colors[i] is the color of the ith balloon.
# Alice wants the rope to be colorful. She does not want two consecutive
# balloons to be of the same color, so she asks Bob for help. Bob can remove
# some balloons from the rope to make it colorful. You are given a 0-indexed
# integer array neededTime where neededTime[i] is the time (in seconds) that Bob
# needs to remove the ith balloon from the rope.
# Return the minimum time Bob needs to make the rope colorful.


from itertools import groupby
from typing import Iterable, List, Optional, Tuple

from more_itertools import ilen


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(colors="abaac", neededTime=[1, 2, 3, 4, 5]) == 3
        assert algo(colors="abc", neededTime=[1, 2, 3]) == 0
        assert algo(colors="aabaa", neededTime=[1, 2, 3, 4, 1]) == 2

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.greedy]:
        test_algo(algo)


class Solution:
    def greedy(self, colors: str, neededTime: List[int]) -> int:
        """
        Approach:  Greedy.
        Idea:      For each run of same consecutive colored balloons, we want to pick the most expensive to *not* remove, and remove all others.
        Time:      O(n): Iterate over every balloon, keeping track of current same color runs.
        Space:     O(n): We allocate each group (from groupby) to a list, which isn't necessary, i'm just lazy.
        Leetcode:  872 ms runtime, 28.80 MB memory
        """

        def color_only(item):
            (color, _cost) = item
            return color

        def costs():
            for color, group in groupby(
                zip(colors, neededTime), key=color_only
            ):
                group = list(group)
                if len(group) >= 2:
                    # Delete everyone but the most expensive from the group.
                    total_cost = sum(cost for (_color, cost) in group)
                    most_expensive_color = max(cost for (_color, cost) in group)
                    cost = total_cost - most_expensive_color
                    yield cost

        return sum(costs())
