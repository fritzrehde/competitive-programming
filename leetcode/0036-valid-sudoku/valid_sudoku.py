#!/usr/bin/env python3

# Valid Sudoku
#
# https://leetcode.com/problems/valid-sudoku
#
# Determine if a 9 x 9 Sudoku board is valid. Only the filled cells need to be
# validated according to the following rules:
#
# Each row must contain the digits 1-9 without repetition.
# Each column must contain the digits 1-9 without repetition.
# Each of the nine 3 x 3 sub-boxes of the grid must contain the digits 1-9
# without repetition.
#
# Note:
#
# A Sudoku board (partially filled) could be valid but is not necessarily
# solvable.
# Only the filled cells need to be validated according to the mentioned rules.


from collections import Counter, defaultdict
import pprint
from typing import Dict, Iterable, List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert (
            algo(
                board=[
                    ["5", "3", ".", ".", "7", ".", ".", ".", "."],
                    ["6", ".", ".", "1", "9", "5", ".", ".", "."],
                    [".", "9", "8", ".", ".", ".", ".", "6", "."],
                    ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
                    ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
                    ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
                    [".", "6", ".", ".", ".", ".", "2", "8", "."],
                    [".", ".", ".", "4", "1", "9", ".", ".", "5"],
                    [".", ".", ".", ".", "8", ".", ".", "7", "9"],
                ]
            )
            == True
        )
        # Has two 8s in column.
        assert (
            algo(
                board=[
                    ["8", "3", ".", ".", "7", ".", ".", ".", "."],
                    ["6", ".", ".", "1", "9", "5", ".", ".", "."],
                    [".", "9", "8", ".", ".", ".", ".", "6", "."],
                    ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
                    ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
                    ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
                    [".", "6", ".", ".", ".", ".", "2", "8", "."],
                    [".", ".", ".", "4", "1", "9", ".", ".", "5"],
                    [".", ".", ".", ".", "8", ".", ".", "7", "9"],
                ]
            )
            == False
        )
        # Has two 1s in box.
        assert (
            algo(
                board=[
                    [".", ".", ".", ".", "5", ".", ".", "1", "."],
                    [".", "4", ".", "3", ".", ".", ".", ".", "."],
                    [".", ".", ".", ".", ".", "3", ".", ".", "1"],
                    ["8", ".", ".", ".", ".", ".", ".", "2", "."],
                    [".", ".", "2", ".", "7", ".", ".", ".", "."],
                    [".", "1", "5", ".", ".", ".", ".", ".", "."],
                    [".", ".", ".", ".", ".", "2", ".", ".", "."],
                    [".", "2", ".", "9", ".", ".", ".", ".", "."],
                    [".", ".", "4", ".", ".", ".", ".", ".", "."],
                ]
            )
            == False
        )

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [
        solution.brute_force,
        solution.brute_force_set,
        solution.brute_force_small_set,
    ]:
        test_algo(algo)


class Solution:
    def brute_force(self, board: List[List[str]]) -> bool:
        """
        Approach:  Brute-force.
        Idea:      Assert that each area (a row, a column or a box) is valid, i.e. contains at most one of all digits from 0 to 9.
        Time:      O(n^2): Given the board has size nxn, we iterate over every element 3 times, namely when checking rows, columns and boxes.
        Space:     O(n^2): We check that an area contains at most one of all digits from 0 to 9 by collecting all cells into a counter hashmap.
        Leetcode:  109 ms runtime, 16.58 MB memory
        """

        box_len = 3
        box_count_on_axis = 3

        def box_iter(box_row_start: int, box_col_start: int):
            box_row_end = box_row_start + box_len
            box_col_end = box_col_start + box_len
            for cell_row_idx in range(box_row_start, box_row_end):
                for cell_col_idx in range(box_col_start, box_col_end):
                    yield board[cell_row_idx][cell_col_idx]

        def all_boxes_iter():
            for box_row_idx in range(0, box_count_on_axis):
                for box_col_idx in range(0, box_count_on_axis):
                    box_row_start = box_row_idx * box_len
                    box_col_start = box_col_idx * box_len
                    yield box_iter(box_row_start, box_col_start)

        def all_unique(iterable) -> bool:
            counts: Dict = defaultdict(lambda: 0)
            for item in iterable:
                counts[item] += 1

            return all(count == 1 for count in counts.values())

        def valid_area(area_iter: Iterable[str]):
            return all_unique(filter(str.isdigit, area_iter))

        def rows():
            yield from board

        def cols():
            yield from zip(*board)

        def all_areas():
            yield from rows()
            yield from cols()
            yield from all_boxes_iter()

        return all(map(valid_area, all_areas()))

    def brute_force_set(self, board: List[List[str]]) -> bool:
        """
        Approach:  Brute-force, using a set.
        Idea:      Assert that each area (a row, a column or a box) is valid, i.e. contains at most one of all digits from 0 to 9.
        Time:      O(n^2): Given the board has size nxn, we iterate over every element 3 times, namely when checking rows, columns and boxes.
        Space:     O(n^2): We check that an area contains at most one of all digits from 0 to 9 by collecting all cells into a seen hashset.
        Leetcode:  101 ms runtime, 16.44 MB memory
        """

        box_len = 3
        box_count_on_axis = 3

        def box_iter(box_row_start: int, box_col_start: int):
            box_row_end = box_row_start + box_len
            box_col_end = box_col_start + box_len
            for cell_row_idx in range(box_row_start, box_row_end):
                for cell_col_idx in range(box_col_start, box_col_end):
                    yield board[cell_row_idx][cell_col_idx]

        def all_boxes_iter():
            for box_row_idx in range(0, box_count_on_axis):
                for box_col_idx in range(0, box_count_on_axis):
                    box_row_start = box_row_idx * box_len
                    box_col_start = box_col_idx * box_len
                    yield box_iter(box_row_start, box_col_start)

        def all_unique(iterable) -> bool:
            seen_items = set()
            for item in iterable:
                if item in seen_items:
                    return False
                else:
                    seen_items.add(item)
            return True

        def valid_area(area_iter: Iterable[str]):
            return all_unique(filter(str.isdigit, area_iter))

        def rows():
            yield from board

        def cols():
            yield from zip(*board)

        def all_areas():
            yield from rows()
            yield from cols()
            yield from all_boxes_iter()

        return all(map(valid_area, all_areas()))

    def brute_force_small_set(self, board: List[List[str]]) -> bool:
        """
        Approach:  Brute-force, using a set.
        Idea:      Assert that each area (a row, a column or a box) is valid, i.e. contains at most one of all digits from 0 to 9.
        Time:      O(n^2): Given the board has size nxn, we iterate over every element 3 times, namely when checking rows, columns and boxes.
        Space:     O(1): We check that an area contains at most one of all digits from 0 to 9 by collecting all cells into a custom O(1) SC digit hashset.
        Leetcode:  103 ms runtime, 16.74 MB memory
        """

        class DigitSet:
            def __init__(self):
                # SC: O(1)
                # If the set contains digit X, then the bit Xth highest bit is
                # set.
                self.bits = 0

            def add(self, digit: int):
                # TC: O(1)
                self.bits = self.bits | (1 << digit)

            def contains(self, digit: int) -> bool:
                # TC: O(1)
                return (self.bits & (1 << digit)) != 0

        box_len = 3
        box_count_on_axis = 3

        def box_iter(box_row_start: int, box_col_start: int):
            box_row_end = box_row_start + box_len
            box_col_end = box_col_start + box_len
            for cell_row_idx in range(box_row_start, box_row_end):
                for cell_col_idx in range(box_col_start, box_col_end):
                    yield board[cell_row_idx][cell_col_idx]

        def all_boxes_iter():
            for box_row_idx in range(0, box_count_on_axis):
                for box_col_idx in range(0, box_count_on_axis):
                    box_row_start = box_row_idx * box_len
                    box_col_start = box_col_idx * box_len
                    yield box_iter(box_row_start, box_col_start)

        def all_digits_unique(digits: Iterable[int]) -> bool:
            seen_digits = DigitSet()
            for item in digits:
                if seen_digits.contains(item):
                    return False
                else:
                    seen_digits.add(item)
            return True

        def valid_area(area_iter: Iterable[str]):
            return all_digits_unique(map(int, filter(str.isdigit, area_iter)))

        def rows():
            yield from board

        def cols():
            yield from zip(*board)

        def all_areas():
            yield from rows()
            yield from cols()
            yield from all_boxes_iter()

        return all(map(valid_area, all_areas()))
