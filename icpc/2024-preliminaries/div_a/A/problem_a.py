#!/usr/bin/env python3

# Arranging Sticks


from typing import List

from more_itertools import sliding_window


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        def median(three_nums) -> int:
            return sorted(three_nums)[1]

        def no_middle_medians(nums_str: str) -> bool:
            nums = map(int, nums_str.split())
            return all(
                median(window) != window[1]
                for window in sliding_window(nums, 3)
            )

        assert no_middle_medians(
            algo(
                input="""7
2 3 5 7 11 13 17"""
            )
        )

        assert no_middle_medians(
            algo(
                input="""4
10 100 1 1000"""
            )
        )

        assert no_middle_medians(
            algo(
                input="""8
1 3 5 7 2 4 6 8"""
            )
        )

    # Test all different algorithms/implementations.
    solution = Solution()
    for algo in [solution.brute_force]:
        test_algo(algo)


class Solution:
    def brute_force(self, input=str) -> str:
        """
        Approach:  Greedy.
        Idea:      We can ensure no 3-length subarray has the middle element as median by greedily choosing the largest, smallest, 2nd largest, 2nd smallest etc. elements.
        Time:      O(n log n): We sort the n input numbers (O(n log n)), and then iterate with two pointers from front and back over each element once (in total, so O(n)).
        Space:     O(1): No additional memory is used (we sort in-place).
        """

        input_lines: List[str] = list(
            map(lambda line: line.rstrip("\n"), input.splitlines())
        )

        n = int(input_lines[0])
        nums = list(map(int, input_lines[1].split()))

        nums.sort()

        def ans():
            l, r = 0, n - 1
            next_ptr = "r"
            while l <= r:
                match next_ptr:
                    case "l":
                        yield nums[l]
                        l += 1
                        next_ptr = "r"
                    case "r":
                        yield nums[r]
                        r -= 1
                        next_ptr = "l"

        return " ".join(map(str, ans()))
