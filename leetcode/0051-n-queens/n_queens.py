#!/usr/bin/env python3

# N-Queens
#
# https://leetcode.com/problems/n-queens/
#
# The n-queens puzzle is the problem of placing n queens on an n x n chessboard
# such that no two queens attack each other.
#
# Given an integer n, return all distinct solutions to the n-queens puzzle. You
# may return the answer in any order.
#
# Each solution contains a distinct board configuration of the n-queens'
# placement, where 'Q' and '.' both indicate a queen and an empty space,
# respectively.


from typing import List, Tuple
import itertools


def test():
    """
    Run `pytest <this-file > `.
    """

    def test_algo(algo):
        def assert_sorted_eq(a, b):
            assert sorted(a) == sorted(b)

        assert_sorted_eq(algo(4), [[".Q..", "...Q", "Q...", "..Q."], ["..Q.", "Q...", "...Q", ".Q.."]])

        assert_sorted_eq(algo(3), [])

        assert_sorted_eq(algo(2), [])

        assert_sorted_eq(algo(1), [["Q"]])

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force]:
        test_algo(algo)


class Solution:
    def brute_force(self, n: int) -> List[List[str]]:
        """
        Approach:  Brute-force.
        Idea:      Try every possible board with n queens, and return it if it is valid. A board is valid if no queen sees another queen.
        Time:      O((n^2 choose n)(n^2)): There are (n^2 choose n) possible boards (the number of ways to choose n positions from n^2 total positions; combinations), and checking whether each game is valid takes O(n^2).
        Space:     O(n^2): We allocate the entire nxn board when formatting a game.
        Leetcode:  Time Limit Exceeded
        """

        def game_is_valid(queens: List[Tuple[int, int]]) -> bool:
            """
            Check if the given game with n queens on a chess board is valid. A game is valid if no queens can see/attack each other.
            O(n^2)
            """

            def queen_sees_other_queens(queen: Tuple[int, int]) -> bool:
                """
                Check if this queen can see any other queen on the board.
                O(n)
                """

                def queens_see_each_other(queen_a: Tuple[int, int], queen_b: Tuple[int, int]) -> bool:
                    """
                    Check if two queens can see each other.
                    O(1)
                    """
                    a_x, a_y = queen_a
                    b_x, b_y = queen_b

                    # Same row.
                    def same_row(): return a_x == b_x

                    # Same column.
                    def same_column(): return a_y == b_y

                    # Same diagonal (either north-west to south-east or south-west to north-east).
                    def same_diagonal(): return abs(a_x - b_x) == abs(a_y - b_y)

                    return same_row() or same_column() or same_diagonal()

                for other_queen in (q for q in queens if q != queen):
                    if queens_see_each_other(queen, other_queen):
                        return True

                return False

            for queen in queens:
                if queen_sees_other_queens(queen):
                    return False

            return True

        def format_game(queens: List[Tuple[int, int]]) -> List[str]:
            queens = set(queens)
            board = [["." for _ in range(n)] for _ in range(n)]
            for q_row, q_col in queens:
                board[q_row][q_col] = "Q"
            return ["".join(row) for row in board]

        # Try all possible games, and return those that are valid.
        possible_board_positions = ((row, col) for row in range(n) for col in range(n))
        # Find all ways we can place n (indistinguishable) queens onto n^2 board positions. We are interested only in the combinations (rather than permutations), because we do not care about the order in which the queens are placed onto the board, we only care about the final board.
        possible_games = itertools.combinations(possible_board_positions, n)
        return [format_game(game) for game in possible_games if game_is_valid(game)]

    def brute_force(self, n: int) -> List[List[str]]:
        """
        Approach:  Brute-force.
        Idea:      Try every possible board with n queens, and return it if it is valid. A board is valid if no queen sees another queen.
        Time:      O((n^2 choose n)(n^2)): There are (n^2 choose n) possible boards (the number of ways to choose n positions from n^2 total positions; combinations), and checking whether each game is valid takes O(n^2).
        Space:     O(n^2): We allocate the entire nxn board when formatting a game.
        Leetcode:  Time Limit Exceeded
        """

        def game_is_valid(queens: List[Tuple[int, int]]) -> bool:
            """
            Check if the given game with n queens on a chess board is valid. A game is valid if no queens can see/attack each other.
            O(n^2)
            """

            def queen_sees_other_queens(queen: Tuple[int, int]) -> bool:
                """
                Check if this queen can see any other queen on the board.
                O(n)
                """

                def queens_see_each_other(queen_a: Tuple[int, int], queen_b: Tuple[int, int]) -> bool:
                    """
                    Check if two queens can see each other.
                    O(1)
                    """
                    a_x, a_y = queen_a
                    b_x, b_y = queen_b

                    # Same row.
                    def same_row(): return a_x == b_x

                    # Same column.
                    def same_column(): return a_y == b_y

                    # Same diagonal (either north-west to south-east or south-west to north-east).
                    def same_diagonal(): return abs(a_x - b_x) == abs(a_y - b_y)

                    return same_row() or same_column() or same_diagonal()

                for other_queen in (q for q in queens if q != queen):
                    if queens_see_each_other(queen, other_queen):
                        return True

                return False

            for queen in queens:
                if queen_sees_other_queens(queen):
                    return False

            return True

        def format_game(queens: List[Tuple[int, int]]) -> List[str]:
            queens = set(queens)
            board = [["." for _ in range(n)] for _ in range(n)]
            for q_row, q_col in queens:
                board[q_row][q_col] = "Q"
            return ["".join(row) for row in board]

        # Try all possible games, and return those that are valid.
        possible_board_positions = ((row, col) for row in range(n) for col in range(n))
        # Find all ways we can place n (indistinguishable) queens onto n^2 board positions. We are interested only in the combinations (rather than permutations), because we do not care about the order in which the queens are placed onto the board, we only care about the final board.
        possible_games = itertools.combinations(possible_board_positions, n)
        return [format_game(game) for game in possible_games if game_is_valid(game)]
