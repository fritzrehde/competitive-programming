#!/usr/bin/env python3

# Water Bottles
#
# https://leetcode.com/problems/water-bottles/
#
# There are numBottles water bottles that are initially full of water. You can
# exchange numExchange empty water bottles from the market with one full water
# bottle.
#
# The operation of drinking a full water bottle turns it into an empty bottle.
#
# Given the two integers numBottles and numExchange, return the maximum number
# of water bottles you can drink.


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(numBottles=9, numExchange=3) == 13

        assert algo(numBottles=15, numExchange=4) == 19

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force]:
        test_algo(algo)


class Solution:
    def brute_force(self, numBottles: int, numExchange: int) -> int:
        """
        Approach:  Brute-force.
        Idea:      One "stage" consists of drinking all full water bottles, and then getting as many now-empty bottles refunded as possible. Repeat this stage until there are no more full bottles to drink.
        Time:      O(log_m(n)): Given n initial bottles and an exchange rate of m, we divide n by m in each iteration.
        Space:     O(1): No additional data structures are stored.
        Leetcode:  ? ms runtime, ? MB memory
        """

        consumed_bottles = 0

        full_bottles = numBottles
        empty_bottles = 0

        while full_bottles != 0:
            # Drink all of the full bottles we have (turning them empty).
            consumed_bottles += full_bottles
            empty_bottles += full_bottles

            # Calculate how many refunded bottles we get.
            refunded_bottles = empty_bottles // numExchange
            leftover_empty_bottles = empty_bottles % numExchange

            full_bottles = refunded_bottles
            empty_bottles = leftover_empty_bottles

        return consumed_bottles
