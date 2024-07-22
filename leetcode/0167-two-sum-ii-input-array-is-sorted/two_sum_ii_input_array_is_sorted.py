#!/usr/bin/env python3

# Two Sum Ii - Input Array Is Sorted
#
# https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/
#
# Given a 1-indexed array of integers numbers that is already sorted in non-
# decreasing order, find two numbers such that they add up to a specific target
# number. Let these two numbers be numbers[index1] and numbers[index2] where 1
# <= index1 < index2 <= numbers.length.
#
# Return the indices of the two numbers, index1 and index2, added by one as an
# integer array [index1, index2] of length 2.
#
# The tests are generated such that there is exactly one solution. You may not
# use the same element twice.
#
# Your solution must use only constant extra space.


from typing import List, Optional


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(numbers=[2, 7, 11, 15], target=9) == [1, 2]

        assert algo(numbers=[2, 3, 4], target=6) == [1, 3]

        assert algo(numbers=[-1, 0], target=-1) == [1, 2]

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.number_index_map, solution.two_pointer, solution.binary_search]:
        test_algo(algo)


class Solution:
    def brute_force(self, numbers: List[int], target: int) -> List[int]:
        """
        Approach:  Brute-force.
        Idea:      Iterate over all pairs of unique indices, and check if their elements' sum is equal to the target for each.
        Time:      O(n^2): There are n^2 pairs of unique indices, checking each sum takes O(1).
        Space:     O(1): No additional memory is allocated.
        Leetcode:  Time Limit Exceeded
        """

        n = len(numbers)

        def unique_index_pairs():
            """Generate all pairs of unique indices."""
            for i in range(0, n):
                # May not use the same element twice.
                for j in range(i + 1, n):
                    yield ((i, j))

        for (i, j) in unique_index_pairs():
            sum = numbers[i] + numbers[j]
            if sum == target:
                return [i + 1, j + 1]

        return []

    def binary_search(self, numbers: List[int], target: int) -> List[int]:
        """
        Approach:  Binary search.
        Idea:      For each number i, check if number j exists where target = i + j. This check is done with a binary search.
        Time:      O(n log n): We do the check for each of the n numbers, and each binary search takes O(log n).
        Space:     O(1): No additional memory is used.
        Leetcode:  145 ms runtime, 17.85 MB memory
        """

        n = len(numbers)

        def get_numbers_index(number: int, start_idx: int) -> Optional[int]:
            (left, right) = (start_idx, n - 1)
            while left <= right:
                mid = (right + left) // 2
                number_mid = numbers[mid]
                if number_mid == number:
                    return mid
                elif number_mid < number:
                    left = mid + 1
                else:
                    right = mid - 1
            return None

        for (i, number_i) in enumerate(numbers):
            # target = number_i + number_j => number_j = target - number_i
            number_j = target - number_i
            if (j := get_numbers_index(number_j, i + 1)) is not None:
                return [i + 1, j + 1]

        return []

    def number_index_map(self, numbers: List[int], target: int) -> List[int]:
        """
        Approach:  Number index hashmap.
        Idea:      Collect a map from number to index it appears in the array. This allows efficient O(1) checking of whether the complement is in the array.
        Time:      O(n): Building the number index map takes O(n), and then a single pass over all numbers, each iteration searching for the (target - number) is required (also O(n)).
        Space:     O(n): The index map uses O(n).
        Leetcode:  100 ms runtime, 17.80 MB memory
        """

        # We know there will only be exactly one solution, so we don't need to store all indices at which a number occurs.
        number_indices = dict()
        for (i, number) in enumerate(numbers):
            number_indices[number] = i

        def get_numbers_index(number: int) -> Optional[int]:
            return number_indices.get(number_j, None)

        for (i, number_i) in enumerate(numbers):
            # target = number_i + number_j => number_j = target - number_i
            number_j = target - number_i
            if (j := get_numbers_index(number_j)) is not None:
                return [i + 1, j + 1]

        return []

    def two_pointer(self, numbers: List[int], target: int) -> List[int]:
        """
        Approach:  Two pointer.
        Idea:      Since array is sorted, we can greedily decide that next possible solution, without skipping any solutions, can be obtained by moving left/right pointers towards middle.
        Time:      O(n): The left and right pointers start at the left and right indices of the array, and we iterate until they meet in the middle, thus visiting every index exactly once. Each iteration is O(1).
        Space:     O(1): No additional memory is used.
        Leetcode:  105 ms runtime, 17.79 MB memory
        """

        n = len(numbers)

        left = 0
        right = n - 1

        while left < right:
            sum = numbers[left] + numbers[right]
            if sum == target:
                return [left + 1, right + 1]
            elif sum < target:
                left += 1
            else:
                # assert sum > target
                right -= 1

        return []
