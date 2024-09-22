#!/usr/bin/env python3

# Pears
#
# https://contest.unswcpmsoc.com/task/pears/


from itertools import islice
from typing import Tuple


# Run `pytest <this-file>`.
def test():
    def test_algo(algo):
        assert algo(n=5, k=6) == (2, 4)

        assert algo(n=5, k=1) == (1, 2)
        assert algo(n=5, k=7) == (2, 5)
        assert algo(n=5, k=3) == (1, 4)
        assert algo(n=2, k=1) == (1, 2)

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [
        solution.brute_force,
        solution.brute_force_islice,
        solution.more_optimized,
    ]:
        test_algo(algo)


class Solution:
    def brute_force(self, n: int, k: int) -> Tuple[int, int]:
        """
        Approach:  Brute-force.
        Idea:      Find the kth pair by iterating over all pairs lazily.
        Time:      O(k): There are 2^n possible pairs, but we lazily generate the pairs and only iterate over the first k pairs.
        Space:     O(1): No additional memory is used (we do not allocate a list of all pairs).
        """

        def pairs():
            for i in range(1, n):
                for j in range(i + 1, n + 1):
                    yield (i, j)

        def nth(iterable, n: int):
            # n is 1-indexed.
            return next(x for i, x in enumerate(iterable, start=1) if i == n)

        return nth(pairs(), k)

    def brute_force_islice(self, n: int, k: int) -> Tuple[int, int]:
        """
        Approach:  Brute-force, with islice.
        Idea:      Find the kth pair by iterating over all pairs lazily.
        Time:      O(k): There are 2^n possible pairs, but we lazily generate the pairs and only iterate over the first k pairs.
        Space:     O(1): No additional memory is used (we do not allocate a list of all pairs).
        """

        def pairs():
            for i in range(1, n):
                for j in range(i + 1, n + 1):
                    yield (i, j)

        def nth(iterable, n: int):
            # n is 1-indexed.
            return next(islice(iterable, n - 1, None))

        return nth(pairs(), k)

    def more_optimized(self, n: int, k: int) -> Tuple[int, int]:
        """
        Approach:  Optimized.
        Idea:      Calculate the row (i) first (O(1) per row), and then offset into final row is j.
        Time:      O(k/n): Skip entire (at most) n-length rows (at most n/k of which).
        Space:     O(1): No additional memory is used.
        """

        # row_len = size of a row from (i, j) to (i, n) (row_len depends on i!).

        # Calculate i by removing as many rows as possible from k.
        i = 1
        while (row_len := (n - i)) and k > row_len:
            k -= row_len
            i += 1

        # Calculate j using offset into final row.
        j = i + k

        return (i, j)


def main():
    n = int(input())
    k = int(input())
    algo = Solution().more_optimized
    print(" ".join(map(str, algo(n, k))))


if __name__ == "__main__":
    main()
