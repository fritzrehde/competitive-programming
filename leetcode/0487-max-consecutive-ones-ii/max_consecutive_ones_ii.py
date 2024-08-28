#!/usr/bin/env python3

# Max Consecutive Ones Ii
#
# https://leetcode.com/problems/max-consecutive-ones-ii
#
# Given a binary array, find the maximum number of consecutive 1s in this array
# if you can flip at most one 0.


from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(nums=[1, 0, 1, 1, 0]) == 4

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.sliding_window]:
        test_algo(algo)


class Solution:
    def sliding_window(self, nums=List[int]) -> int:
        """
        Approach:  Sliding window.
        Idea:      Maintain a sliding window that contains at most one zero. Once a zero is encountered, move the left pointer right until at most one zero is in sliding window.
        Time:      O(n): Each number in input array will both be the left and right exactly once.
        Space:     O(1): No additional memory is used.
        Leetcode:  ? ms runtime, ? MB memory
        """

        def all_1s_subarray_lengths():
            ones_window_len = 0
            zeroes_in_window = 0
            l = 0
            for r, num in enumerate(nums):
                if num == 1:
                    ones_window_len += 1
                else:
                    zeroes_in_window += 1

                    if zeroes_in_window > 1:
                        # This ones window ends here.
                        yield ones_window_len

                        # Move left pointer right until at most one zero is in
                        # window.
                        while zeroes_in_window > 1:
                            if nums[l] == 0:
                                zeroes_in_window -= 1
                            l += 1

                        ones_window_len = 0
                    else:
                        ones_window_len += 1

            yield ones_window_len

        return max(all_1s_subarray_lengths(), default=0)
