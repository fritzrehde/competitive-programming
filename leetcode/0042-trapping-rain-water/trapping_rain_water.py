#!/usr/bin/env python3

# Trapping Rain Water
#
# https://leetcode.com/problems/trapping-rain-water
#
# Given n non-negative integers representing an elevation map where the width of
# each bar is 1, compute how much water it can trap after raining.


from typing import List, Optional, Tuple


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(height=[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
        assert algo(height=[4, 2, 0, 3, 2, 5]) == 9
        assert algo(height=[0, 2, 0]) == 0

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [
        solution.sliding_window,
        solution.tallest_towers_left_right,
        solution.two_pointer,
    ]:
        test_algo(algo)


class Solution:
    def sliding_window(self, height: List[int]) -> int:
        """
        Approach:  Two pointer sliding window.
        Idea:      Given a left boundary for some body of water, find the most suitable right boundary, which will be either one taller or of equal height to left boundary, or the tallest remaining boundary. Calculate water trapped between these boundaries, and move onto next "window".
        Time:      O(n^2): We move our sliding window from left to right, and it will never overlap, so every element will be in exactly one window state. However, calculating the right boundary of each window takes O(n).
        Space:     O(1): We use no additional space.
        Leetcode:  Time Limit Exceeded
        """

        n = len(height)

        trapped_water = 0

        def trapped_water_between(l: int, r: int) -> int:
            """
            Return amount of trapped water between the left and right
            boundaries.
            """

            h = min(height[l], height[r])
            return sum(h - height[k] for k in range(l + 1, r))

        def find_right_barrier(l: int) -> Optional[int]:
            """Given the left barrier, find the next possible right barrier."""

            # Try to find the next right boundary that is same height as, or
            # larger than, the left boundary.
            match next(
                filter(lambda r: height[r] >= height[l], range(l + 1, n)),
                None,
            ):
                case None:
                    pass
                case taller_r:
                    return taller_r

            # Try to find the largest possible right boundary (will always be
            # smaller than left boundary).
            match max(
                ((height[r], r) for r in range(l + 1, n)),
                default=None,
            ):
                case None:
                    pass
                case (_tallest_height, tallest_idx):
                    return tallest_idx

            # We found no possible right barrier.
            return None

        l = 0
        while (r := find_right_barrier(l)) is not None:
            trapped_water += trapped_water_between(l, r)
            l = r

        return trapped_water

    # def sliding_window_optimized(self, height: List[int]) -> int:
    #     """
    #     Approach:  Two pointer sliding window.
    #     Idea:      Given a left boundary for some body of water, find the most suitable right boundary, which will be either one taller or of equal height to left boundary, or the tallest remaining boundary. Calculate water trapped between these boundaries, and move onto next "window".
    #     Time:      O(n): We move our sliding window from left to right, and it will never overlap, so every element will be in exactly one window state.
    #     Space:     O(1): We use no additional space.
    #     Leetcode:  ? ms runtime, ? MB memory
    #     """

    #     n = len(height)

    #     trapped_water = 0

    #     def find_right_barrier(l: int) -> Optional[Tuple[int, int]]:
    #         """
    #         Given the left boundary, find the next possible right boundary, and
    #         also return the water trapped in between the left and right
    #         boundaries.
    #         """

    #         def max_opt(
    #             a_opt: Optional[int], b_opt: Optional[int]
    #         ) -> Optional[int]:
    #             match (a_opt, b_opt):
    #                 case (None, None):
    #                     return None
    #                 case (None, b):
    #                     return b
    #                 case (a, None):
    #                     return a
    #                 case (a, b):
    #                     (_max_height, max_idx) = max(
    #                         (height[a], a), (height[b], b)
    #                     )
    #                     return max_idx
    #                 case _:
    #                     raise Exception("unreachable")

    #         # trapped_water = 0

    #         # Try to find the next right boundary that is same height as, or
    #         # larger than, the left boundary, while also collecting the overall
    #         # maximum.
    #         assumed_h = height[l]
    #         max_r = None
    #         # trapped_water = [0 for _ in range(l + 1, n)]
    #         trapped_water = [0 for _ in range(0, n)]
    #         for r in range(l + 1, n):
    #             if height[r] >= height[l]:
    #                 return (r, trapped_water[r])
    #             else:
    #                 max_r = max_opt(r, max_r)
    #             if r == (l + 1):
    #                 trapped_water[r] = assumed_h - height[r]
    #             else:
    #                 trapped_water[r] = trapped_water[r - 1] + (
    #                     assumed_h - height[r]
    #                 )

    #         # trapped_water -= assumed_h - height[r]

    #         # Try to find the largest possible right boundary (will always be
    #         # smaller than left boundary).
    #         match max_r:
    #             case None:
    #                 # We found no possible right barrier.
    #                 return None
    #             case r:
    #                 actual_h = height[r]
    #                 # The right boundary is smaller than left, so substract the
    #                 # water we added too much of.
    #                 slots_in_window = r - l - 1
    #                 # slots_in_window = (r -l -1) if l < r else (l - )
    #                 print(trapped_water, slots_in_window, assumed_h, actual_h)
    #                 trapped_water[r] -= slots_in_window * (assumed_h - actual_h)
    #                 return (r, trapped_water[r])

    #     l = 0
    #     while True:
    #         match find_right_barrier(l):
    #             case None:
    #                 break
    #             case (r, trapped_water_between):
    #                 print(f"l: {l}, r: {r}, trapped: {trapped_water_between}")
    #                 trapped_water += trapped_water_between
    #                 l = r

    #     return trapped_water

    def tallest_towers_left_right(self, height: List[int]) -> int:
        """
        Approach:  Tallest towers left and right.
        Idea:      The amount of water level/height at tower i depends only on the largest tower to the left and largest tower to the right. These can be pre-calculated.
        Time:      O(n): Pre-calculating the largest towers to left and right takes O(n) for each. Then, we calculate the water level at each of the n towers in O(1).
        Space:     O(n): We store the largest towers to the left and right of each tower.
        Leetcode:  141 ms runtime, 18.66 MB memory
        """

        n = len(height)

        # The maximum height of a tower left of the i-th tower.
        max_to_left = [0] * n
        for i in range(1, n):
            max_to_left[i] = max(max_to_left[i - 1], height[i - 1])

        # The maximum height of a tower right of the i-th tower.
        max_to_right = [0] * n
        for i in reversed(range(0, n - 1)):
            max_to_right[i] = max(max_to_right[i + 1], height[i + 1])

        trapped_water = 0

        for i in range(0, n):
            # The left and right boundaries of this tower.
            (l, r) = (max_to_left[i], max_to_right[i])
            water_height = min(l, r)
            if height[i] >= water_height:
                # This tower is larger than the two boundaries, so it will be
                # above the water.
                pass
            else:
                trapped_water_at_i = water_height - height[i]
                trapped_water += trapped_water_at_i

        return trapped_water

    def two_pointer(self, height: List[int]) -> int:
        """
        Approach:  Tallest current towers left and right, with two pointer.
        Idea:      The amount of water level/height at tower i depends only on the largest tower to the left and largest tower to the right. There is no need to pre-calculate these, as we can calculate them on-the-fly using two pointers converging towards the middle from either side.
        Time:      O(n): The left and right pointers start at the two sides and converge until they meet in the middle, visiting every tower once.
        Space:     O(1): No additional memory is used.
        Leetcode:  111 ms runtime, 18.41 MB memory
        """

        n = len(height)

        trapped_water = 0

        (l, r) = (0, n - 1)
        (max_left, max_right) = (height[l], height[r])

        while l <= r:
            if max_left < max_right:
                # The water height will be capped at max_left.
                water_height = max_left
                if height[l] > max_left:
                    # Update max left.
                    max_left = height[l]
                else:
                    # l-th tower is underwater.
                    trapped_water_at_l = water_height - height[l]
                    trapped_water += trapped_water_at_l
                l += 1
            else:
                # The water height will be capped at max_right.
                water_height = max_right
                if height[r] > max_right:
                    # Update max right.
                    max_right = height[r]
                else:
                    # r-th tower is underwater.
                    trapped_water_at_r = water_height - height[r]
                    trapped_water += trapped_water_at_r
                r -= 1

        return trapped_water
