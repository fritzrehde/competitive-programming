#!/usr/bin/env python3

# Spiral Matrix
#
# https://leetcode.com/problems/spiral-matrix
#
# Given an m x n matrix, return all elements of the matrix in spiral order.


from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(matrix=[[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [
            1,
            2,
            3,
            6,
            9,
            8,
            7,
            4,
            5,
        ]
        assert algo(matrix=[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]) == [
            1,
            2,
            3,
            4,
            8,
            12,
            11,
            10,
            9,
            5,
            6,
            7,
        ]

        assert algo(matrix=[[7], [9], [6]]) == [
            7,
            9,
            6,
        ]

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.recursion, solution.transpose]:
        test_algo(algo)


class Solution:
    def recursion(self, matrix: List[List[int]]) -> List[int]:
        """
        Approach:  Recursive spiralling.
        Idea:      In each recursive call, follow the outside edge of the square, and the recurse into the rest inside.
        Time:      O(n): Given n elements in the matrix, we visit each element once taking O(1).
        Space:     O(1): No additional memory is used.
        Leetcode:  33 ms runtime, 16.59 MB memory
        """

        row_count = len(matrix)
        col_count = len(matrix[0])

        going_in_dir_diff = {
            "north": (-1, 0),
            "south": (1, 0),
            "east": (0, 1),
            "west": (0, -1),
        }

        def steps_in_dir(start_cell, dir: str, steps: int):
            (row_diff, col_diff) = going_in_dir_diff[dir]
            (row_idx, col_idx) = start_cell
            for _ in range(0, steps):
                row_idx += row_diff
                col_idx += col_diff
                yield (row_idx, col_idx)

        def cell_value(cell):
            (row_idx, col_idx) = cell
            return matrix[row_idx][col_idx]

        spiral_order = []

        def spiral(start_cell, row_count: int, col_count: int):
            if col_count == 0 or row_count == 0:
                return

            spiral_order.append(cell_value(start_cell))

            latest_cell = start_cell

            # Go east.
            for cell in steps_in_dir(latest_cell, "east", steps=col_count - 1):
                spiral_order.append(cell_value(cell))
                latest_cell = cell

            if row_count == 1:
                return

            # Go south.
            for cell in steps_in_dir(latest_cell, "south", steps=row_count - 1):
                spiral_order.append(cell_value(cell))
                latest_cell = cell

            if col_count == 1:
                return

            # Go west.
            for cell in steps_in_dir(latest_cell, "west", steps=col_count - 1):
                spiral_order.append(cell_value(cell))
                latest_cell = cell

            # Go north.
            for cell in steps_in_dir(latest_cell, "north", steps=row_count - 2):
                spiral_order.append(cell_value(cell))
                latest_cell = cell

            # Start inner spiral one step east.
            spiral(
                next(steps_in_dir(latest_cell, "east", steps=1)),
                row_count - 2,
                col_count - 2,
            )

        spiral((0, 0), row_count, col_count)
        return spiral_order

    def transpose(self, matrix: List[List[int]]) -> List[int]:
        """
        Approach:  Traverse and remove row, then rotate anti-clockwise.
        Idea:      See approach above.
        Time:      O(n): Given n elements in the matrix, we visit each element once taking O(1).
        Space:     O((n+m)(n*m)): Given an m x n matrix, we recurse n+m times, and each time we rotate the matrix anti-clockwise, taking O(n*m).
        Leetcode:  43 ms runtime, 16.59 MB memory
        """

        def rotate_anti_clockwise(matrix: List[List[int]]) -> List[List[int]]:
            transposed = list(zip(*matrix))
            return list(reversed(transposed))

        def spiral(matrix: List[List[int]]) -> List[int]:
            if matrix:
                return list(matrix.pop(0)) + spiral(
                    rotate_anti_clockwise(matrix)
                )
            else:
                return []

        return spiral(matrix)
