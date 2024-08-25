#!/usr/bin/env python3

# Number of Islands
#
# https://leetcode.com/problems/number-of-islands
#
# Given an m x n 2D binary grid grid which represents a map of '1's (land) and
# '0's (water), return the number of islands.
# An island is surrounded by water and is formed by connecting adjacent lands
# horizontally or vertically. You may assume all four edges of the grid are all
# surrounded by water.


from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert (
            algo(
                grid=[
                    ["1", "1", "1", "1", "0"],
                    ["1", "1", "0", "1", "0"],
                    ["1", "1", "0", "0", "0"],
                    ["0", "0", "0", "0", "0"],
                ]
            )
            == 1
        )
        assert (
            algo(
                grid=[
                    ["1", "1", "0", "0", "0"],
                    ["1", "1", "0", "0", "0"],
                    ["0", "0", "1", "0", "0"],
                    ["0", "0", "0", "1", "1"],
                ]
            )
            == 3
        )
        assert (
            algo(grid=[["1", "1", "1"], ["0", "1", "0"], ["1", "1", "1"]]) == 1
        )

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force]:
        test_algo(algo)


class Solution:
    def brute_force(self, grid: List[List[str]]) -> int:
        """
        Approach:  Brute-force.
        Idea:      Go through all cells. Once we find a land cell, explore all recursively adjacent land cells, and count these as one island.
        Time:      O(n): Given n cells (e.g. a m x m grid), visit every cell exactly once.
        Space:     O(n): Keep a set containing all visited cells, which will be n at the end.
        Leetcode:  329 ms runtime, 31.60 MB memory
        """

        # Edge case: empty grid.
        if len(grid) == 0:
            return 0

        dir_to_step = {
            "north": (-1, 0),
            "south": (1, 0),
            "east": (0, 1),
            "west": (0, -1),
        }

        row_count = len(grid)
        col_count = len(grid[0])

        def adjacent_cells(cell):
            (row_idx, col_idx) = cell
            for row_diff, col_diff in map(
                lambda dir: dir_to_step[dir], ["north", "east", "south", "west"]
            ):
                new_row_idx = row_idx + row_diff
                new_col_idx = col_idx + col_diff
                # Check in-bounds.
                if (
                    0 <= new_row_idx < row_count
                    and 0 <= new_col_idx < col_count
                ):
                    yield (new_row_idx, new_col_idx)

        def is_land(cell) -> bool:
            (row_idx, col_idx) = cell
            return grid[row_idx][col_idx] == "1"

        visited_cells = set()
        island_count = 0

        def explore_island_from(cell):
            """Visit all cells on an island, starting with a given cell."""
            for neighbour in adjacent_cells(cell):
                if neighbour not in visited_cells:
                    visited_cells.add(neighbour)
                    if is_land(neighbour):
                        explore_island_from(neighbour)

        for row_idx in range(0, row_count):
            for col_idx in range(0, col_count):
                cell = (row_idx, col_idx)
                if cell not in visited_cells:
                    visited_cells.add(cell)
                    if is_land(cell):
                        explore_island_from(cell)
                        island_count += 1

        return island_count
