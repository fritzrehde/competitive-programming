#!/usr/bin/env python3

# Find Winner on a Tic Tac Toe Game
#
# https://leetcode.com/problems/find-winner-on-a-tic-tac-toe-game
#
# Tic-tac-toe is played by two players A and B on a 3 x 3 grid. The rules of
# Tic-Tac-Toe are:
#
# Players take turns placing characters into empty squares ' '.
# The first player A always places 'X' characters, while the second player B
# always places 'O' characters.
# 'X' and 'O' characters are always placed into empty squares, never on filled
# ones.
# The game ends when there are three of the same (non-empty) character filling
# any row, column, or diagonal.
# The game also ends if all squares are non-empty.
# No more moves can be played if the game is over.
#
# Given a 2D integer array moves where moves[i] = [rowi, coli] indicates that
# the ith move will be played on grid[rowi][coli]. return the winner of the game
# if it exists (A or B). In case the game ends in a draw return "Draw". If there
# are still movements to play return "Pending".
# You can assume that moves is valid (i.e., it follows the rules of Tic-Tac-
# Toe), the grid is initially empty, and A will play first.


from itertools import cycle
from typing import Iterable, List, Optional


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(moves=[[0, 0], [2, 0], [1, 1], [2, 1], [2, 2]]) == "A"
        assert (
            algo(moves=[[0, 0], [1, 1], [0, 1], [0, 2], [1, 0], [2, 0]]) == "B"
        )
        assert (
            algo(
                moves=[
                    [0, 0],
                    [1, 1],
                    [2, 0],
                    [1, 0],
                    [1, 2],
                    [2, 1],
                    [0, 1],
                    [0, 2],
                    [2, 2],
                ]
            )
            == "Draw"
        )
        assert (
            algo(moves=[[1, 2], [2, 1], [1, 0], [0, 0], [0, 1], [2, 0], [1, 1]])
            == "A"
        )

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force]:
        test_algo(algo)


class Solution:
    def brute_force(self, moves: List[List[int]]) -> str:
        """
        Approach:  Brute-force.
        Idea:      ?
        Time:      O(?): ?
        Space:     O(?): ?
        Leetcode:  46 ms runtime, 16.70 MB memory
        """

        # Number of rows and number of columns, as well as number of fields you
        # need in a row to win.
        N = 3

        board = [[None for _ in range(N)] for _ in range(N)]

        # (row diff, col diff)
        dir_dx = {
            "north": (-1, 0),
            "south": (1, 0),
            "west": (0, -1),
            "east": (0, 1),
        }

        def iter(from_r: int, from_c: int, r_dx: int, c_dx: int, len: int):
            (curr_r, curr_c) = (from_r, from_c)
            for _ in range(0, len):
                curr_r += r_dx
                curr_c += c_dx
                if curr_r in range(0, N) and curr_c in range(0, N):
                    yield (curr_r, curr_c)

        def has_chain_of_len(
            iterable: Iterable[Optional[str]], chain_elem: str, len: int
        ) -> bool:
            chain_len = 0
            chain_last = None
            for i in iterable:
                if chain_last != i:
                    chain_last = i
                    chain_len = 0
                chain_len += 1

                if chain_len == len and chain_last == chain_elem:
                    return True

            return False

        def tuple_add(tuple_a, tuple_b):
            (a1, a2) = tuple_a
            (b1, b2) = tuple_b
            return (a1 + b1, a2 + b2)

        def wins_after_move(player: str, row_i: int, col_i: int) -> bool:
            """
            Make a move, and return whether that move won the game for the player.
            """
            board[row_i][col_i] = player

            # Check for win.
            for row_dx, col_dx in [
                dir_dx["north"],
                dir_dx["south"],
                dir_dx["west"],
                dir_dx["east"],
                tuple_add(dir_dx["north"], dir_dx["west"]),
                tuple_add(dir_dx["north"], dir_dx["east"]),
                tuple_add(dir_dx["south"], dir_dx["west"]),
                tuple_add(dir_dx["south"], dir_dx["east"]),
            ]:
                iter_in_dir = map(
                    lambda rc: board[rc[0]][rc[1]],
                    iter(
                        row_i - (N * row_dx),
                        col_i - (N * col_dx),
                        row_dx,
                        col_dx,
                        2 * N - 1,
                    ),
                )
                if has_chain_of_len(
                    iter_in_dir,
                    player,
                    N,
                ):
                    return True

            return False

        for move, player in zip(moves, cycle(["A", "B"])):
            (row_i, col_i) = move
            if wins_after_move(player, row_i, col_i):
                return player

        # If all fields are filled, it's a draw.
        if all(board[r][c] is not None for r in range(N) for c in range(N)):
            return "Draw"
        else:
            return "Pending"
