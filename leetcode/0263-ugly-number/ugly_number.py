#!/usr/bin/env python3

# Ugly Number
#
# https://leetcode.com/problems/ugly-number
#
# An ugly number is a positive integer whose prime factors are limited to 2, 3,
# and 5.
# Given an integer n, return true if n is an ugly number.


from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(n=6) == True
        assert algo(n=1) == True
        assert algo(n=14) == False
        assert algo(n=-2147483648) == False
        assert algo(n=0) == False

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [
        solution.brute_force,
        solution.brute_force_caching,
        solution.brute_force_early_exit,
        solution.math,
    ]:
        test_algo(algo)


class Solution:
    def brute_force(self, n: int) -> bool:
        """
        Approach:  Brute-force.
        Idea:      Check if the number is ugly by checking if its prime factors are limited to 2, 3 and 5.
        Time:      O(n^2): Go through all factors (O(n)), keep only the prime ones (O(n) each, so O(n^2) to find all prime factors), and check they are limited to 2, 3 and 5.
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

            if num < 0:
                yield -1
                num = abs(num)
            else:
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

        if n <= 0:
            # Edge case:
            return False
        else:
            # O(n^2)
            # Number is ugly if prime factors are limited to 2, 3 and 5.
            extra_prime_factors = set(get_all_prime_factors(n)) - set([2, 3, 5])
            return len(extra_prime_factors) == 0

    def brute_force_caching(self, n: int) -> int:
        """
        Approach:  Optimize by caching.
        Idea:      Check if the number is ugly by checking if its prime factors are limited to 2, 3 and 5.
        Time:      O(n^2): Go through all factors (O(n)), keep only the prime ones (O(n) each, so O(n^2) to find all prime factors), and check they are limited to 2, 3 and 5.
        Space:     O(n^2): For each factor of n, we check if its prime, meaning we store its factors (at most n).
        Leetcode:  Time Limit Exceeded.
        """

        from functools import cache

        def is_factor_of(num: int, factor: int) -> bool:
            # O(1)
            return (num % factor) == 0

        @cache
        def is_prime(num: int) -> bool:
            # O(1) if cached, O(num) otherwise.
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

        if n <= 0:
            # Edge case:
            return False
        else:
            # O(n^2)
            # Number is ugly if prime factors are limited to 2, 3 and 5.
            extra_prime_factors = set(get_all_prime_factors(n)) - set([2, 3, 5])
            return len(extra_prime_factors) == 0

    def brute_force_early_exit(self, n: int) -> int:
        """
        Approach:  Optimize through early exit.
        Idea:      Check if the number is ugly by checking if its prime factors are limited to 2, 3 and 5.
        Time:      O(n^2): Go through all factors (O(n)), keep only the prime ones (O(n) each, so O(n^2) to find all prime factors), and check they are limited to 2, 3 and 5.
        Space:     O(n^2): For each factor of n, we check if its prime, meaning we store its factors (at most n).
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
            # O(num)
            for factor in get_all_factors(num):
                if is_prime(factor):
                    print(factor)
                    yield factor

        if n <= 0:
            # Edge case:
            return False
        else:
            # Number is ugly if prime factors are limited to 2, 3 and 5.
            return all(
                prime_factor in [2, 3, 5]
                for prime_factor in get_all_prime_factors(n)
            )

    def math(self, n: int) -> int:
        """
        Approach:  Optimize through early exit.
        Idea:      A number n is ugly if n = (2^a)(3^b)(5^c).
        Time:      O(log n): n/((2^a)(3^b)(5^c)) can be calculated by dividing by [2, 3, 5] as long as possible, and then check if equal to 1. O(log n) because we are decreasing search space by factor of [2, 3, 5] every iteration.
        Space:     O(1): No additional memory is used.
        Leetcode:  35 ms runtime, 16.60 MB memory
        """

        if n <= 0:
            return False
        else:
            # n is ugly if n = (2^a)(3^b)(5^c) <=> 1 = n/((2^a)(3^b)(5^c))
            for div in [2, 3, 5]:
                while (n % div) == 0:
                    n //= div
            return n == 1
