#!/usr/bin/env python3

# Minimum Number Of Moves To Seat Everyone
#
# https://leetcode.com/problems/minimum-number-of-moves-to-seat-everyone/
#
# There are n seats and n students in a room. You are given an array seats of
# length n, where seats[i] is the position of the ith seat. You are also given
# the array students of length n, where students[j] is the position of the jth
# student.
#
# You may perform the following move any number of times:
#
# - Increase or decrease the position of the ith student by 1 (i.e., moving the
# ith student from position x to x + 1 or x - 1)
#
# Return the minimum number of moves required to move each student to a seat
# such that no two students are in the same seat.
#
# Note that there may be multiple seats or students in the same position at the
# beginning.


from collections import Counter
from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        # First student moved from pos 2 to 1 (chair 2), second student moved from pos 7 to 5 (chair 3), third student moved from pos 2 to 3 (chair 1).
        assert algo(seats=[3, 1, 5], students=[2, 7, 4]) == 4

        assert algo(seats=[4, 1, 5, 9], students=[1, 3, 2, 6]) == 7

        assert algo(seats=[2, 2, 6, 6], students=[1, 3, 2, 6]) == 4

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.counting_sort]:
        test_algo(algo)


class Solution:
    def brute_force(self, seats: List[int], students: List[int]) -> int:
        """
        Approach:  Brute-force.
        Idea:      By sorting the positions of the seats and students, we can pair up a seat with its closest student, and then sum up the distances between all seat and student pairs.
        Time:      O(n log n): We sort two lists (seats and students), each of which have length n.
        Space:     O(n): We sort in-place, which still uses O(n) of extra space with mergesort, and only aggregate the sum in a local variable.
        Leetcode:  58 ms runtime, 16.37 MB memory
        """

        seats.sort()
        students.sort()
        return sum(abs(seat_pos - student_pos) for seat_pos, student_pos in zip(seats, students))

    def counting_sort(self, seats: List[int], students: List[int]) -> int:
        """
        Approach:  Linear time sorting with counting sort.
        Idea:      Same as idea as naive, but make use of the fact that the size of the range of numbers in the input array, k, is probably similar to the size of the array, so counting sort becomes viable.
        Time:      O(n + k): Sorting with counting sort only takes O(n + k).
        Space:     O(n + k): We allocate intermediate arrays mapping each array value to its number of occurences and index in the final sorted array, each of which have sich k.
        Leetcode:  66 ms runtime, 16.45 MB memory
        """

        def counting_sorted(arr: List[int]) -> List[int]:
            """
            Sort the input array in TC O(n+k) and SC O(n+k), where n is the length of the array and k is the size of the range of the array values.
            """
            min_val, max_val = min(arr), max(arr)
            # The size of the range of values in the input array.
            k = max_val - min_val + 1

            def norm(val: int) -> int:
                "Transform (normalize) the original array values into indices for auxiliary arrays."
                return val - min_val

            # Map each value in the array to its number of occurences in the array.
            value_occurences = [0] * k
            for val in arr:
                value_occurences[norm(val)] += 1

            # Map each value in the original array to the index in the final sorted array.
            value_index = [None] * k
            next_idx = 0
            for val, occurences in enumerate(value_occurences, start=min_val):
                value_index[norm(val)] = next_idx
                next_idx += occurences

            # Sort the array using the mapping of values to starting indices.
            sorted = [None] * len(arr)
            for val in arr:
                idx = value_index[norm(val)]
                # Since there can be multiple occurences of each value, the next time we see the same value, it needs to be inserted one place right of this value.
                value_index[norm(val)] += 1
                sorted[idx] = val

            return sorted

        seats = counting_sorted(seats)
        students = counting_sorted(students)

        return sum(abs(seat_pos - student_pos) for seat_pos, student_pos in zip(seats, students))
