#!/usr/bin/env python3

# Ugly Number II
#
# https://leetcode.com/problems/ugly-number-ii
#
# An ugly number is a positive integer whose prime factors are limited to 2, 3,
# and 5.
# Given an integer n, return the nth ugly number.


import itertools
from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(n=10) == 12
        assert algo(n=1) == 1

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [
        solution.brute_force,
        solution.brute_force_cached,
        solution.math,
        solution.dynamic_programming,
        solution.dynamic_programming_optimized,
    ]:
        test_algo(algo)


class Solution:
    def brute_force(self, n: int) -> int:
        """
        Approach:  Brute-force.
        Idea:      For each number, check if it's ugly by checking if its prime factors are limited to 2, 3 and 5.
        Time:      O(n^3): Checking if number m is ugly is O(m^2), and we need to check at least the first n numbers (probably a few more, but most numbers are ugly) for ugliness. We assume the largest number we check for ugliness is n (will be slightly larger).
        Space:     O(1): No additional memory is used.
        Leetcode:  Time Limit Exceeded.
        """

        def is_factor_of(num: int, factor: int) -> bool:
            # O(1)
            return (num % factor) == 0

        def is_prime(num: int) -> bool:
            # O(num)
            if num <= 1:
                return False
            else:
                # TODO: optimization: only go to half
                for i in range(2, num):
                    if is_factor_of(num, i):
                        return False
                return True

        def get_all_factors(num: int):
            # O(num)
            yield 1
            i = 2
            while num > 1:
                if is_factor_of(num, i):
                    yield i
                    num //= i
                else:
                    i += 1

        def get_all_prime_factors(num: int):
            # O(num^2)
            for factor in get_all_factors(num):
                if is_prime(factor):
                    yield factor

        def is_ugly(num: int) -> bool:
            # O(num^2)
            # Number is ugly if prime factors are limited to 2, 3 and 5.
            extra_prime_factors = set(get_all_prime_factors(num)) - set(
                [2, 3, 5]
            )
            return len(extra_prime_factors) == 0

        def ugly_numbers():
            i = 1
            while True:
                if is_ugly(i):
                    yield i
                i += 1

        return next(itertools.islice(ugly_numbers(), n - 1, None))

    def brute_force_cached(self, n: int) -> int:
        """
        Approach:  Optimize by caching.
        Idea:      For each number, check if it's ugly by checking if its prime factors are limited to 2, 3 and 5.
        Time:      O(n^2): Checking if number m is ugly is O(m), and we need to check at least the first n numbers (probably a few more, but most numbers are ugly) for ugliness. We assume the largest number we check for ugliness is n (will be slightly larger).
        Space:     O(n^2): For each number we check for ugliness (assumed to be O(n)), we cache its factors (of which there are at most n).
        Leetcode:  Time Limit Exceeded.
        """

        from functools import cache

        def is_factor_of(num: int, factor: int) -> bool:
            # O(1)
            return (num % factor) == 0

        @cache
        def is_prime(num: int) -> bool:
            # O(1): num's factors will definitely already be cached.
            if num <= 1:
                return False
            else:
                return [1, num] == get_all_factors(num)

        @cache
        def get_all_factors(num: int) -> List[int]:
            # O(num)
            def generator():
                nonlocal num
                yield 1
                i = 2
                while num > 1:
                    if is_factor_of(num, i):
                        yield i
                        num //= i
                    else:
                        i += 1

            return list(generator())

        def get_all_prime_factors(num: int):
            # O(num)
            for factor in get_all_factors(num):
                if is_prime(factor):
                    yield factor

        def is_ugly(num: int) -> bool:
            # O(num)
            # Number is ugly if prime factors are limited to 2, 3 and 5.
            extra_prime_factors = set(get_all_prime_factors(num)) - set(
                [2, 3, 5]
            )
            return len(extra_prime_factors) == 0

        def ugly_numbers():
            i = 1
            while True:
                if is_ugly(i):
                    yield i
                i += 1

        return next(itertools.islice(ugly_numbers(), n - 1, None))

    def math(self, n: int) -> int:
        """
        Approach:  Math.
        Idea:      A number n is ugly if n = (2^a)(3^b)(5^c). Go through all numbers until n ugly numbers are found.
        Time:      O(n log n): n/((2^a)(3^b)(5^c)) can be calculated by dividing by [2, 3, 5] as long as possible, and then check if equal to 1. O(log n) because we are decreasing search space by factor of [2, 3, 5] every iteration. We assume there are more ugly numbers than non-ugly (INCORRECT assumption, hence this is slow), so we need to try O(n) numbers before we find n ugly numbers.
        Space:     O(1): No additional memory is used.
        Leetcode:  Time Limit Exceeded.
        """

        def is_ugly(num: int) -> bool:
            # O(log n)
            # num is ugly if num = (2^a)(3^b)(5^c) <=> 1 = num/((2^a)(3^b)(5^c))
            for div in [2, 3, 5]:
                while (num % div) == 0:
                    num //= div
            return num == 1

        def ugly_numbers():
            i = 1
            while True:
                if is_ugly(i):
                    yield i
                i += 1

        return next(itertools.islice(ugly_numbers(), n - 1, None))

    def dynamic_programming(self, n: int) -> int:
        """
        Approach:  Dynamic Programming.
        Idea:      Given a previous ugly number m, we can calculate the next ugly number as the smallest larger number whose prime factors are (still) limited by 2, 3 and 5, which we can find by multiplying m by those factors.
        Time:      O(n^2): There are n subproblems, and each subproblem takes O(n).
        Space:     O(n): Our DP table contains n elements.
        Leetcode:  ? ms runtime, ? MB memory
        """

        # Subproblem: dp[i] is the (i+1)th (due to zero indexing) ugly number.
        dp = [None] * n
        dp_set = set()

        # Order of computation: increasing order of i, since dp[i] only depends on dp[i-1] in the recurrence.
        for i in range(0, n):
            # Base case:
            if i == 0:
                dp[i] = 1
            else:
                # Recurrence: Given the previous ugly number m, the next ugly number is the smallest larger number whose prime factors are (still) limited by 2, 3 and 5.
                dp[i] = min(
                    next
                    for prev in dp_set
                    for next in (2 * prev, 3 * prev, 5 * prev)
                    if next not in dp_set
                )

            dp_set.add(dp[i])

        # Final result:
        return dp[n - 1]

    def dynamic_programming_optimized(self, n: int) -> int:
        """
        Approach:  Dynamic Programming.
        Idea:      Given a previous ugly number m, we can calculate the next ugly number as the smallest larger number whose prime factors are (still) limited by 2, 3 and 5, which we can find by multiplying m by those factors.
        Time:      O(n): There are n subproblems, and each subproblem takes O(1).
        Space:     O(n): Our DP table contains n elements.
        Leetcode:  84 ms runtime, 16.43 MB memory
        """

        # Subproblem: dp[i] is the (i+1)th (due to zero indexing) ugly number.
        dp = [None] * n

        # Base case:
        dp[0] = 1

        next_2_factor_idx = 1
        next_3_factor_idx = 1
        next_5_factor_idx = 1

        next_2_factor_val = 2
        next_3_factor_val = 3
        next_5_factor_val = 5

        # Order of computation: increasing order of i, since dp[i] only depends on dp[i-1] in the recurrence.
        for i in range(1, n):
            # Recurrence: Given the previous ugly number m, the next ugly number is the smallest larger number whose prime factors are (still) limited by 2, 3 and 5.
            next_ugly_number = min(
                next_2_factor_val, next_3_factor_val, next_5_factor_val
            )
            dp[i] = next_ugly_number

            # Because the next factor values might share factors, check if each needs updating.
            if next_ugly_number == next_2_factor_val:
                next_2_factor_val = dp[next_2_factor_idx] * 2
                next_2_factor_idx += 1
            if next_ugly_number == next_3_factor_val:
                next_3_factor_val = dp[next_3_factor_idx] * 3
                next_3_factor_idx += 1
            if next_ugly_number == next_5_factor_val:
                next_5_factor_val = dp[next_5_factor_idx] * 5
                next_5_factor_idx += 1

        # Final result:
        return dp[n - 1]
