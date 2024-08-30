#!/usr/bin/env python3

# Floor of Chocolate
#
# https://sppcontests.org/problem_pdfs/2023/prelimsB.pdf


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        # Expected output has been adjusted to fit my impl, since many
        # different outputs are valid.

        assert (
            algo(
                input="""50 1
10 15"""
            )
            == """4
0 0 10 50
10 0 1 15
10 16 1 34
11 0 39 50"""
        )

        assert (
            algo(
                input="""101 5
0 0
100 100
0 100
100 0
50 50"""
            )
            == """6
0 1 1 99
1 0 49 101
50 0 1 50
50 51 1 50
51 0 49 101
100 1 1 99"""
        )

        assert (
            algo(input="""50 0""")
            == """1
0 0 50 50"""
        )

    # Test all different algorithms/implementations.
    solution = Solution()
    for algo in [solution.brute_force]:
        test_algo(algo)


class Solution:
    def brute_force(self, input=str) -> str:
        """
        Approach:  Brute force.
        Idea:      For each support column, we create 1-unit wide tiles above and beneath it, and N-unit high tiles left and right of it.
        Time:      O(m): Given m support columns, we (at most) one tile above, beneath, left and right of it (each O(1)).
        Space:     O(m): We store groups of support columns that share their x-coordinate (column idx).
        """

        from itertools import groupby

        input_lines_it = iter(input.splitlines())

        (N, _K) = map(int, next(input_lines_it).split())
        support_cols = list(
            map(lambda line: tuple(map(int, line.split())), input_lines_it)
        )

        # Sort support columns from west to east.
        def west_to_east(item):
            x, y = item
            return x, y

        support_cols.sort(key=west_to_east)

        def col(support_col):
            support_col_x, _support_col_y = support_col
            return support_col_x

        support_cols_grouped = list(
            map(
                lambda x: (x[0], list(x[1])),
                groupby(support_cols, key=col),
            )
        )

        def tile(top_left, bottom_right):
            top_left_x, top_left_y = top_left
            bottom_right_x, bottom_right_y = bottom_right

            x = top_left_x
            y = top_left_y
            w = bottom_right_x - top_left_x
            h = bottom_right_y - top_left_y

            if w == 0 or h == 0:
                return None
            else:
                return (x, y, w, h)

        def floor_tiles():
            separator_tile_top_left = (0, 0)
            last_support_col_x = 0
            for col, support_cols in support_cols_grouped:
                # Left of next support column becomes (top to bottom) tile.
                separator_tile_bottom_right = (col, N)
                yield tile(separator_tile_top_left, separator_tile_bottom_right)

                # Find tiles between support columns in same column.
                between_tile_top_left = (col, 0)
                last_support_in_col_y = None
                for _support_col_x, support_col_y in support_cols:
                    between_tile_bottom_right = (col + 1, support_col_y)
                    yield tile(between_tile_top_left, between_tile_bottom_right)

                    between_tile_top_left = (col, support_col_y + 1)

                    last_support_in_col_y = support_col_y

                # Find tile between final support column in col and south edge.
                between_tile_top_left = (
                    col,
                    last_support_in_col_y + 1,
                )
                between_tile_bottom_right = (col + 1, N)
                yield tile(between_tile_top_left, between_tile_bottom_right)

                separator_tile_top_left = (col + 1, 0)
                last_support_col_x = col + 1

            # Find tile between final support column in final col and east edge.
            between_tile_top_left = (
                last_support_col_x,
                0,
            )
            between_tile_bottom_right = (N, N)
            yield tile(between_tile_top_left, between_tile_bottom_right)

        def is_some(item):
            return item is not None

        floor_tiles_ = list(filter(is_some, floor_tiles()))

        def visualize():
            def ids():
                chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                while True:
                    for c in chars:
                        yield c

            grid = [[" "] * N for _ in range(N)]
            id_gen = iter(ids())
            for x, y, w, h in floor_tiles_:
                # Colour every floor tile in a unique id.
                id = next(id_gen)
                for x_ in range(x, x + w):
                    for y_ in range(y, y + h):
                        grid[x_][y_] = id

            for y in range(N):
                for x in range(N):
                    print(grid[x][y], end="")
                print()

        # visualize()

        return f"{len(floor_tiles_)}\n" + "\n".join(
            f"{x} {y} {w} {h}" for x, y, w, h in floor_tiles_
        )
