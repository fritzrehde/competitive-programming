#!/usr/bin/env python3

# Best Time To Buy And Sell Stock
#
# https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
#
# You are given an array prices where prices[i] is the price of a given stock on
# the ith day.
#
# You want to maximize your profit by choosing a single day to buy one stock and
# choosing a different day in the future to sell that stock.
#
# Return the maximum profit you can achieve from this transaction. If you cannot
# achieve any profit, return 0.


from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo([7, 1, 5, 3, 6, 4]) == 5

        assert algo([7, 6, 4, 3, 1]) == 0

        # Impossible to buy and sell without any prices.
        assert algo([]) == 0
        # Impossible to buy and sell on same day.
        assert algo([1]) == 0

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.one_pass]:
        test_algo(algo)


class Solution:
    def brute_force(self, prices: List[int]) -> int:
        """
        Approach:  Brute-force.
        Idea:      Try all possible buy and sell times, and get pair with largest profit.
        Time:      O(n^2): There are O(n^2) possible pairs.
        Space:     O(1): No additional data structures are used.
        Leetcode:  Time Limit Exceeded
        """

        n = len(prices)
        return max(max((prices[j] - prices[i] for i in range(0, n) for j in range(i + 1, n)), default=0), 0)

    # def sorting(self, prices: List[int]) -> int:
    #     """
    #     Approach:  Brute-force.
    #     Idea:      Try all possible buy and sell times, and get pair with largest profit.
    #     Time:      O(n^2): There are O(n^2) possible pairs.
    #     Space:     O(1): No additional data structures are used.
    #     Leetcode:  ? ms runtime, ? MB memory
    #     """

    #     prices_with_time = [(price, time) for (time, price) in enumerate(prices)]
    #     # Sort ascendingly by price, then ascendingly by time.
    #     prices_with_time.sort(key=lambda x: (x[0], x[1]))

    #     l = 0
    #     r = n - 1
    #     while

    #     n = len(prices)
    #     return max(max((prices[j] - prices[i] for i in range(0, n) for j in range(i + 1, n)), default=-1), 0)

    def one_pass(self, prices: List[int]) -> int:
        """
        Approach:  One pass.
        Idea:      Maintain the current cheapest buying price, and check on what day afterwards it's most profitable to sell.
        Time:      O(n): Iterate over every price once, and possibly update the cheapest buy price seen so far and calculate profit if you sell at that day (O(1)).
        Space:     O(1): No additional data structures are used.
        Leetcode:  758 ms runtime, 27.18 MB memory
        """
        n = len(prices)

        if n <= 1:
            return 0

        def profit_on_each_day():
            min_buy_price_seen_so_far = prices[0]
            for i in range(1, n):
                # Check if selling on day i is the most profitable.
                sell_price = prices[i]
                profit = sell_price - min_buy_price_seen_so_far

                # Also consider buying on day i, if it's cheaper.
                min_buy_price_seen_so_far = min(min_buy_price_seen_so_far, prices[i])

                yield profit

        return max(max(profit_on_each_day()), 0)
