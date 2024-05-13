#!/usr/bin/env python3

# Container With Most Water
#
# https://leetcode.com/problems/container-with-most-water/
#
# You are given an integer array height of length n. There are n vertical lines
# drawn such that the two endpoints of the ith line are (i, 0) and (i,
# height[i]).
#
# Find two lines that together with the x-axis form a container, such that the
# container contains the most water.
#
# Return the maximum amount of water a container can store.
#
# Notice that you may not slant the container.


from typing import List, Tuple


def test():
    """
    Run `pytest <this-file > `.
    """

    def test_algo(algo):
        # Choose indices 1 and 8 as container edges.
        assert algo([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49

        assert algo([1, 1]) == 1

        # Edge cases
        assert algo([1]) == 0
        assert algo([]) == 0

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.greedy_two_pointer, solution.greedy_two_pointer_optimized]:
        test_algo(algo)


class Solution:
    def brute_force(self, height: List[int]) -> int:
        """
        Approach:  Brute-force.
        Idea:      Try all possible containers, and return the container that fits the most amount of water.
        Time:      O(n^2): There are O(n^2) possible containers, and calculating the amount of water each can hold is O(1), so getting the maximum is O(n^2).
        Space:     O(1): We do not store anything besides the local max value (assuming Python generators don't allocate).
        Leetcode:  Time Limit Exceeded
        """

        def container_amount_water(l: int, r: int) -> int:
            """
            Find the amount of water (technically an area) of a container that has its left and right edges at l and r, respectively (this implies l <= r).
            """
            l_height, r_height = height[l], height[r]
            container_width = r - l
            container_height = min(l_height, r_height)
            return container_width * container_height

        n = len(height)

        # Try all possible containers, and return the container that fits the most amount of water.
        return max((container_amount_water(l, r) for l in range(0, n) for r in range(l + 1, n)), default=0)

    def greedy_two_pointer(self, height: List[int]) -> int:
        """
        Approach:  Greedy with two pointers.
        Idea:      We maintain a left and right pointer that enclose the current container. Whenever we find a container with more water than the maximum we have seen, we update our maximum. In every step, we are trying to maximize the water amount of the next container we look at. When we check how much water fits into a container, that amount will be limited by one (or potentially both, if they have equal height) of the container sides/edges. If we were to move the pointer of the taller side, the next container we check is guaranteed to be at most as large as the one we previously looked at, because the water amount is still limited by the smaller side (which we decided to keep). Therefore, in order to *possibly* find a container with more water, we should move the pointer of the smaller side. By doing this repeatedly, we will eventually find the largest container. This algorithm is greedy, because it disregards the solution where we move the pointer of taller side of the previous container, because this solution cannot be optimal.
        Time:      O(n): We only ever increment the left and decrement the right pointer by one, and do so until they meet somewhere in the middle. Therefore, every index is covered by either l or r once, so there are n iterations. Each iteration is O(1).
        Space:     O(1): We do not store anything besides the local max value.
        Leetcode:  502 ms runtime, 30.02 MB memory
        """

        def container_amount_water(l: int, r: int) -> Tuple[int, int]:
            """
            Find the amount of water (technically an area) of a container that has its left and right edges at l and r, respectively (this implies l <= r). Also return the index of the container edge with the smaller height.
            """
            l_height, r_height = height[l], height[r]

            container_width = r - l
            # Get the height of the smaller of the two edges/pointers, and the corresponding edge index.
            if l_height <= r_height:
                container_height, smaller_height_ptr = l_height, l
            else:
                container_height, smaller_height_ptr = r_height, r

            water_amount = container_width * container_height
            return water_amount, smaller_height_ptr

        n = len(height)

        max_water_amount = 0
        l, r = 0, n - 1

        while l < r:
            water_amount, smaller_height_ptr = container_amount_water(l, r)
            if water_amount > max_water_amount:
                # Update current maximum if necessary.
                max_water_amount = water_amount

            # Move the pointer with the smaller height, since the amount of water was previously limited by this pointer.
            if smaller_height_ptr == l:
                l += 1
            else:
                r -= 1

        return max_water_amount

    def greedy_two_pointer_optimized(self, height: List[int]) -> int:
        """
        Approach:  Greedy with two pointers, optimized.
        Idea:      The same as the regular greedy two pointer approach, just that we are even more greedy in the sense that we not only move the pointer with the smaller height from the previous container by one step, we move it until we find a larger height than the previous smaller height (as this is the only way to increase the overall water amount, since we were bounded by the smaller height).
        Time:      O(n): While we might be able to skip some more elements for some input arrays, in the worst case we still have to visit every list element once.
        Space:     O(1): We do not store anything besides the local max value.
        Leetcode:  433 ms runtime, 29.22 MB memory
        """

        def container_amount_water(l: int, r: int) -> Tuple[int, int, int]:
            """
            Find the amount of water (technically an area) of a container that has its left and right edges at l and r, respectively (this implies l <= r). Additionally, return the index of the container edge with the smaller height, as well as the smaller height value itself.
            """
            l_height, r_height = height[l], height[r]

            container_width = r - l
            # Get the height of the smaller of the two edges/pointers, and the corresponding edge index.
            if l_height <= r_height:
                smaller_height, smaller_height_ptr = l_height, l
            else:
                smaller_height, smaller_height_ptr = r_height, r

            water_amount = container_width * smaller_height
            return water_amount, smaller_height_ptr, smaller_height

        n = len(height)

        max_water_amount = 0
        l, r = 0, n - 1

        while l < r:
            water_amount, smaller_height_ptr, smaller_height = container_amount_water(l, r)
            if water_amount > max_water_amount:
                # Update current maximum if necessary.
                max_water_amount = water_amount

            # By moving the left pointer right or the right pointer left, we are decreasing the size of the x-axis, which, if all else stays the same, decreases the container size. Therefore, the only possible way to find a larger container with a smaller x-axis is if one of the container edge heights increases. We've already established that moving the pointer that previously had greater height doesn't make sense, as we'd still be bounded by the smaller height. However, moving the pointer with the previously smaller height also only makes sense if we actually move the smaller pointer until we find a pointer with larger height than the previous smaller height, as this would give us a guaranteed larger height than before (the previously taller height is fixed, and the previously smaller height is now larger than before). This way, we might be able to skip many indices. Basically, we can be even more greedy (hehe).
            if smaller_height_ptr == l:
                # TODO: where python do-while loop
                l += 1
                while height[l] < smaller_height:
                    l += 1
            else:
                # TODO: where python do-while loop
                r -= 1
                while height[r] < smaller_height:
                    r -= 1

        return max_water_amount
