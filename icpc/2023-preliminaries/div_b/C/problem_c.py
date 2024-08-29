#!/usr/bin/env python3

# Capturing Bishops
#
# https://sppcontests.org/problem_pdfs/2023/prelimsB.pdf


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert (
            algo(
                input="""........
........
........
..B.....
........
........
........
........
"""
            )
            == "12"
        )

        assert (
            algo(
                input="""........
....B...
........
........
.B......
........
........
....B...
"""
            )
            == "16"
        )

        assert (
            algo(
                input="""BBBBBBBB
........
........
........
........
........
........
........
"""
            )
            == "52"
        )

    # Test all different algorithms/implementations.
    solution = Solution()
    for algo in [solution.brute_force]:
        test_algo(algo)


class Solution:
    def brute_force(self, input=str) -> str:
        """
        Approach:  Brute force.
        Idea:      For each cell, check if it is vulnerable by checking if it lies on a diagonal with any of the bishops.
        Time:      O(n * B): Given n cells and B bishops, for every cell we check if it lies on a diagonal (O(1) operation) with any of the bishops.
        Space:     O(B): We store the bishop locations.
        """

        from more_itertools import ilen

        n = 8

        grid = [[cell for cell in row] for row in input.splitlines()]

        bishops = [
            (row_idx, col_idx)
            for (row_idx, row) in enumerate(grid)
            for col_idx, cell in enumerate(row)
            if cell == "B"
        ]

        def cells_on_diagonal(c1, c2) -> bool:
            # O(1)
            (x1, y1) = c1
            (x2, y2) = c2
            # top-left to bottom-right diagonal: x1 - y1 == x2 - y2
            # top-right to bottom-left diagonal: x1 + y1 == x2 + y2
            return (x1 - y1 == x2 - y2) or (x1 + y1 == x2 + y2)

        def bishop_can_reach_cell(bishop, cell) -> bool:
            # O(1)
            return cells_on_diagonal(bishop, cell)

        def cell_is_vulnerable(cell) -> bool:
            # O(B)
            return any(
                bishop_can_reach_cell(bishop, cell) for bishop in bishops
            )

        def all_cells():
            for row_idx, row in enumerate(grid):
                for col_idx, _cell in enumerate(row):
                    yield (row_idx, col_idx)

        # O(n * B)
        return str(ilen(filter(cell_is_vulnerable, all_cells())))
