#!/usr/bin/env python3

# Zigzag Conversion
#
# https://leetcode.com/problems/zigzag-conversion/
#
# The string "PAYPALISHIRING" is written in a zigzag pattern on a given number
# of rows like this: (you may want to display this pattern in a fixed font for
# better legibility)
#
# P   A   H   N
# A P L S I I G
# Y   I   R
#
# And then read line by line: "PAHNAPLSIIGYIR"
#
# Write the code that will take a string and make this conversion given a number
# of rows:
# string convert(string s, int numRows);


from math import ceil


def test():
    """
    Run `pytest <this-file > `.
    """

    def test_algo(algo):
        # P   A   H   N
        # A P L S I I G
        # Y   I   R
        assert algo("PAYPALISHIRING", 3) == "PAHNAPLSIIGYIR"

        # P     I    N
        # A   L S  I G
        # Y A   H R
        # P     I
        assert algo("PAYPALISHIRING", 4) == "PINALSIGYAHRPI"

        # Edge case: one row should just be the input text.
        assert algo("INPUTTEXT", 1) == "INPUTTEXT"

        # Edge case: as many rows as string characters.
        assert algo("INPUT", 5) == "INPUT"

        # Edge case: more rows than string characters.
        assert algo("INPUT", 6) == "INPUT"

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.grid_hashmap, solution.grid_2d_list, solution.grid_list_of_string_rows, solution.no_allocations]:
        test_algo(algo)


class Solution:
    def grid_hashmap(self, s: str, numRows: int) -> str:
        """
        Approach:  Grid represented as hashmap.
        Idea:      Represent the grid as a hashmap mapping (row index, column index) to each character, and fill in this grid by taking the zigzag route. Finally, sort the hashmap entries by row index, ascendingly, and then by column index, ascendingly, and join together in that order.
        Time:      O(n log n): Given an input string of length n, we will need to sort the grid with n values with merge sort, taking O(n log n).
        Space:     O(n): For each of the n characters in the input string, there is one entry in the hashmap.
        Leetcode:  68 ms runtime, 16.84 MB memory
        """

        # Edge case
        if numRows == 1:
            return s

        # Map (row index, column index) to each string character, forming a 2D grid.
        grid = dict()

        def go_south():
            nonlocal row_idx, going_south
            row_idx += 1
            going_south = True

        def go_north_east():
            nonlocal row_idx, col_idx, going_south
            row_idx -= 1
            col_idx += 1
            going_south = False

        # Whether we are currently going south or north-east on our zigzag route.
        going_south = True

        row_idx = 0
        col_idx = 0

        for c in s:
            grid[row_idx, col_idx] = c

            # Go to next position in zigzag route.
            if row_idx == 0:
                go_south()
            elif row_idx == (numRows - 1):
                go_north_east()
            else:
                # Continue going in same direction.
                if going_south:
                    go_south()
                else:
                    go_north_east()

        def sort_by(item):
            ((row, col), value) = item
            # Sort by rows, ascendingly, and then by columns, ascendingly.
            return (row, col)

        # Sort grid by ascending rows and then by ascending columns.
        sorted_grid = sorted(grid.items(), key=sort_by)

        # Join all characters in the grid together, in correct order due to the sorting.
        return "".join(c for (row, col), c in sorted_grid)

    def grid_2d_list(self, s: str, numRows: int) -> str:
        """
        Approach:  Grid represented as 2D list.
        Idea:      Represent the grid as a 2D list where each list represents all fields in a row, and fill in this grid by taking the zigzag route. Finally, we can directly iterate over rows and columns (which only works because insertion order in each row happens to be the same as the order from left to right), and join together in that order.
        Time:      O(n): Given an input string of length n, we will make n zigzag moves through the grid and insert an element each time.
        Space:     O(n): For each of the n characters in the input string, there is one entry in the 2D list.
        Leetcode:  67 ms runtime, 16.70 MB memory
        """

        # Edge case
        if numRows == 1:
            return s

        # Grid is represented as a list of rows, where each row contains all elements in that row along with their column indices.
        rows = [[] for _ in range(0, numRows)]

        def go_south():
            nonlocal row_idx, going_south
            row_idx += 1
            going_south = True

        def go_north_east():
            nonlocal row_idx, col_idx, going_south
            row_idx -= 1
            col_idx += 1
            going_south = False

        # Whether we are currently going south or north-east on our zigzag route.
        going_south = True

        row_idx = 0
        col_idx = 0

        for c in s:
            rows[row_idx].append((col_idx, c))

            # Go to next position in zigzag route.
            if row_idx == 0:
                go_south()
            elif row_idx == (numRows - 1):
                go_north_east()
            else:
                # Continue going in same direction.
                if going_south:
                    go_south()
                else:
                    go_north_east()

        # Join all rows in the grid together.
        return "".join(c for row in rows for (col, c) in row)

    def grid_list_of_string_rows(self, s: str, numRows: int) -> str:
        """
        Approach:  Grid represented as a list of rows, which are strings.
        Idea:      Same as representing grid as 2D list, just that we represent a row as a string instead of another list, since insertion order is final for each row anyways.
        Time:      O(n): Given an input string of length n, we will make n zigzag moves through the grid and insert an element each time.
        Space:     O(n): For each of the n characters in the input string, there is one entry in the grid.
        Leetcode:  46 ms runtime, 16.64 MB memory
        """

        # Edge case
        if numRows == 1:
            return s

        # Grid is represented as a list of rows, where each row contains all elements in that row as a string.
        rows = ["" for _ in range(0, numRows)]

        def go_south():
            nonlocal row_idx, going_south
            row_idx += 1
            going_south = True

        def go_north_east():
            nonlocal row_idx, col_idx, going_south
            row_idx -= 1
            col_idx += 1
            going_south = False

        # Whether we are currently going south or north-east on our zigzag route.
        going_south = True

        row_idx = 0
        # Technically, we have no need for the column index, since it is never read, only written to.
        col_idx = 0

        for c in s:
            rows[row_idx] += c

            # Go to next position in zigzag route.
            if row_idx == 0:
                go_south()
            elif row_idx == (numRows - 1):
                go_north_east()
            else:
                # Continue going in same direction.
                if going_south:
                    go_south()
                else:
                    go_north_east()

        # Join all rows in the grid together.
        return "".join(rows)

    def no_allocations(self, s: str, numRows: int) -> str:
        """
        Approach:  No grid representation.
        Idea:      We do not store the grid at all, but instead calculate the indices of the next elements in the grid according to the zigzag pattern.
        Time:      O(n): Given an input string of length n, we will make n zigzag moves through the grid and extend the ouput string with one character each time.
        Space:     O(1): We allocate nothing besides the final output string.
        Leetcode:  65 ms runtime, 16.74 MB memory
        """

        # Edge case
        if numRows == 1:
            return s

        # The zigzag pattern can be split up into multiple cycles: In each cycle we first go south by numRows steps, and then north-east by numRows - 2 steps (-2 because we exclude both the south-most and north-most points of the north-east route, as the former was part of our previous southbound route and the latter will be the start of the next cycle).
        cycle_len = numRows + numRows - 2

        # The number of cycles.
        cycle_count = ceil(len(s) / cycle_len)

        result = ""

        for row_idx in range(0, numRows):
            # Append all characters that appear in this row in the zigzag pattern.
            for cycle_idx in range(0, cycle_count):
                # Example: A single cycle for numRows = 4, where F is the first char in a row and S is the second char in a row (there is no second char for the first and last rows, though):
                # 0 .
                # 1 F     S
                # 2 s   n      +
                # 3 s n        | F to bottom
                # 4 s          +
                #   0 1 2 3
                #
                #     +-+
                # bottom to S

                # Append the first char F in the row (always exists).
                F_idx = row_idx + cycle_idx * cycle_len
                if (F_idx < len(s)):
                    result += s[F_idx]

                # Append the second char S in the row (sometimes exists).
                if (row_idx == 0 or row_idx == (numRows - 1)):
                    # In a single cycle, the first and last row only contain one element F, so there is no S.
                    continue
                else:
                    # In a single cycle, the middle rows contain two elements, F and S, so we need to add S.

                    # The column index of S.
                    S_col_idx = (numRows - 1) - row_idx

                    # The number of elements on the path from F (exclusive) to the bottom border (inclusive).
                    F_to_bottom = (numRows - 1) - row_idx

                    # The number of elements on the path from the bottom border (exclusive, already counted in F_to_bottom) to S (exclusive).
                    bottom_to_S = S_col_idx - 1

                    # The number of elements in between F (exclusive) and S (exclusive).
                    between_F_S = F_to_bottom + bottom_to_S

                    S_idx = F_idx + between_F_S + 1

                    if (S_idx < len(s)):
                        result += s[S_idx]

        return result
