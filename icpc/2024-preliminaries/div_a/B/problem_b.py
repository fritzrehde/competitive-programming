#!/usr/bin/env python3

# Birthday Wizard


from typing import List

from more_itertools import ilen


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert (
            algo(
                input="""5
"""
            )
            == "1"
        )
        assert (
            algo(
                input="""51
"""
            )
            == "3"
        )
        assert (
            algo(
                input="""10000000000
"""
            )
            == "1"
        )
        assert (
            algo(
                input="""10000000000000000000
"""
            )
            == "1"
        )

    # Test all different algorithms/implementations.
    solution = Solution()
    for algo in [solution.brute_force]:
        test_algo(algo)


class Solution:
    def brute_force(self, input=str) -> str:
        """
        Approach:  Brute force.
        Idea:      For each base, calculate the required candle count as the sum of all digits of N in that base, and take min candle count.
        Time:      O(log n): Given an input number with value n, each conversion into another base B takes log n, because decreasing the number by a factor of B every iteration (until it's zero).
        Space:     O(n): We convert N into the digits of each base (roughly proportional to N's length), which we have to allocate (NO! We could remove this allocation to get O(1), it's just done to be able to reverse digits to have them in correct order).
        """

        input_lines: List[str] = list(
            map(lambda line: line.rstrip("\n"), input.splitlines())
        )

        N = int(input_lines[0])

        def to_base_digits(num: int, base: int):
            """
            Convert a base 10 number to another base, and return the digits of
            the resulting number.
            """

            def digits():
                nonlocal num
                while num > 0:
                    num, digit = divmod(num, base)
                    yield digit

            return reversed(list(digits()))

        def candle_count(base: int) -> int:
            return sum(to_base_digits(N, base))

        def ans() -> int:
            return min(candle_count(base) for base in range(2, 10 + 1))

        return str(ans())
