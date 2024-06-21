#!/usr/bin/env python3

# Grumpy Bookstore Owner
#
# https://leetcode.com/problems/grumpy-bookstore-owner/
#
# There is a bookstore owner that has a store open for n minutes. Every minute,
# some number of customers enter the store. You are given an integer array
# customers of length n where customers[i] is the number of the customer that
# enters the store at the start of the ith minute and all those customers leave
# after the end of that minute.
#
# On some minutes, the bookstore owner is grumpy. You are given a binary array
# grumpy where grumpy[i] is 1 if the bookstore owner is grumpy during the ith
# minute, and is 0 otherwise.
#
# When the bookstore owner is grumpy, the customers of that minute are not
# satisfied, otherwise, they are satisfied.
#
# The bookstore owner knows a secret technique to keep themselves not grumpy for
# minutes consecutive minutes, but can only use it once.
#
# Return the maximum number of customers that can be satisfied throughout the
# day.


from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        # Explanation: The bookstore owner keeps themselves not grumpy for the last 3 minutes.
        # The maximum number of customers that can be satisfied = 1 + 1 + 1 + 1 + 7 + 5 = 16.
        assert algo(customers=[1, 0, 1, 2, 1, 1, 7, 5], grumpy=[0, 1, 0, 1, 0, 1, 0, 1], minutes=3) == 16

        assert algo(customers=[2, 6, 6, 9], grumpy=[0, 0, 1, 1], minutes=1) == 17

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force]:
        test_algo(algo)


class Solution:
    def brute_force(self, customers: List[int], grumpy: List[int], minutes: int) -> int:
        """
        Approach:  Brute-force.
        Idea:      Try out all possible time periods as the non-grumpy one, and return the maximum satisfaction.
        Time:      O(n^2): There are O(n) possible places we can put the non-grumpy window, and for each we need to sum all customers that are satisfied (O(n)).
        Space:     O(1): No additional space is used.
        Leetcode:  Time Limit Exceeded
        """

        def is_grumpy(i: int):
            match grumpy[i]:
                case 1: return True
                case 0: return False

        n = len(customers)

        def generator():
            # Left and right (inclusive) ends of the non-grumpy period of length `minutes`.
            l = 0
            r = min(minutes, n)

            while r <= n:
                def is_grumpy_with_minutes(i):
                    if l <= i < r:
                        return False
                    else:
                        return is_grumpy(i)

                yield sum(customers[i] for i in range(0, n) if not is_grumpy_with_minutes(i))
                l += 1
                r += 1

        return max(generator())
