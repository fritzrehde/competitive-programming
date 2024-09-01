#!/usr/bin/env python3

# LLM


from collections import defaultdict
from functools import reduce


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):

        def float_eq(float1_str: str, float2_str: str) -> bool:
            E = 10**-9
            float1, float2 = float(float1_str), float(float2_str)
            return float2 - E <= float1 <= float2 + E

        assert float_eq(
            algo(
                input="""test
4
international
collegiate
programming
contest"""
            ),
            "0.03",
        )

        assert float_eq(
            algo(
                input="""ab
2
jab
table"""
            ),
            "0.5",
        )

        assert float_eq(
            algo(
                input="""x
3
x
xy
xyz"""
            ),
            "0.333333333333",
        )

        assert float_eq(
            algo(
                input="""abc
1
ab"""
            ),
            "0.0",
        )

        assert float_eq(
            algo(
                input="""aa
1
aa"""
            ),
            "0.25",
        )

        assert float_eq(
            algo(
                input="""a
3
a
a
aa"""
            ),
            "0.75",
        )

    # Test all different algorithms/implementations.
    solution = Solution()
    for algo in [solution.brute_force]:
        test_algo(algo)


class Solution:
    def brute_force(self, input=str) -> str:
        """
        Approach:  Brute force.
        Idea:      For each l0,l1 pair (adjacent chars in T), calculate the probability that l1 follows l0, and multiply all probabilities to get the probability of the entire word T appearing.
        Time:      O(n*m): Given T has length n and m total chars in all words combined, there are O(n) l0,l1 pairs, and for each find all chars following l0 (at most O(m) many), count them (O(m)), take their sum (O(m)). Then, multiply all probabilities (O(n)).
        Space:     O(n*m): For each of the n l0,l1 pairs, store the count of chars following l0 (at most O(m)).
        """

        input_lines = list(
            map(lambda line: line.rstrip("\n"), input.splitlines())
        )

        # Input characters will always only be lowercase letters.
        stop_token = "X"

        T = input_lines[0] + stop_token
        n = int(input_lines[1])
        words = [f"{word}{stop_token}" for word in input_lines[2:]]

        def chars_following_char(c: str):
            for word in words:
                for i in range(0, len(word)):
                    if word[i] == c:
                        yield word[i + 1]

        def probability_l1_follows_l0(T_l0, T_l1):
            # Count all chars that follow l0.
            following_l0_count = defaultdict(lambda: 0)
            for following in chars_following_char(T_l0):
                following_l0_count[following] += 1

            l0_l1_count = following_l0_count[T_l1]
            l0_count = sum(following_l0_count.values())

            return (l0_l1_count, l0_count)

        def all_probabilities():
            return [
                probability_l1_follows_l0(T[l0], T[l1])
                for (l0, l1) in zip(range(0, len(T) - 1), range(1, len(T)))
            ]

        def product(nums) -> int:
            return reduce(lambda a, b: a * b, nums, 1)

        def ans() -> float:
            numerator, denominator = map(product, zip(*all_probabilities()))
            if denominator == 0:
                return 0.0
            else:
                return numerator / denominator

        return str(ans())
