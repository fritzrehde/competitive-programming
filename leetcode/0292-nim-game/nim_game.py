#!/usr/bin/env python3

# Nim Game
#
# https://leetcode.com/problems/nim-game/
#
# You are playing the following Nim Game with your friend:
#
# Initially, there is a heap of stones on the table.
# You and your friend will alternate taking turns, and you go first.
# On each turn, the person whose turn it is will remove 1 to 3 stones from the
# heap.
# The one who removes the last stone is the winner.
#
# Given n, the number of stones in the heap, return true if you can win the game
# assuming both you and your friend play optimally, otherwise return false.


def test():
    """
    Run `pytest <this-file > `.
    """

    def test_algo(algo):
        # Since we go first, we can simply take the last stone.
        assert algo(1) == True

        # Since we go first, we can simply take the last 2 stones.
        assert algo(2) == True

        # Since we go first, we can simply take the last 3 stones.
        assert algo(3) == True

        # Multiple cases:
        # - We go first and pick 1, opponent picks 3, they win.
        # - We go first and pick 2, opponent picks 2, they win.
        # - We go first and pick 3, opponent picks 1, they win.
        assert algo(4) == False

        # Optimal play: n=5 we 1; n=4 they 1-3; n = 1-3 we win
        assert algo(5) == True

        # Optimal play: n=6 we 2; n=4 they 1-3; n = 1-3 we win
        assert algo(6) == True

        # Optimal play: n=7 we 3; n=4 they 1-3; n = 1-3 we win
        assert algo(7) == True

        # Optimal play: n=8 we 1-3; n=5-7 they win
        assert algo(8) == False

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.logic, solution.logic_optimized]:
        test_algo(algo)


class Solution:
    def logic(self, n: int) -> bool:
        """
        Approach:  Logic.
        Idea:      We notice that if one player 4 stones left, player B can always beat them, and if one player has 4x stones left, where x >= 1, the other player can always beat them by smartly responding to the first player's move to ensure the first player is always left with 4(x-1) stones.
        Time:      O(1): We only perform some cheap boolean and integer operations.
        Space:     O(1): We use no additional memory.
        Leetcode:  39 ms runtime, 16.52 MB memory
        """

        def can_win_directly(stones_left: int) -> bool:
            # If there are at most 3 stones, we can use our first turn to take all stones, in which case we win.
            return 0 <= stones_left <= 3

        def can_win_eventually(stones_left: int) -> bool:
            # If there are 4 stones left and it's player A's turn, player A can never win. We can perform an exhaustive case analysis:
            # - Player A could take 1 stone, which leaves player B with 3 stones, so player B can take all remaining 3 stones and win.
            # - Player A could take 2 stones, which leaves player B with 2 stones, so player B can take all remaining 2 stones and win.
            # - Player A could take 3 stones, which leaves player B with 1 stone, so player B can take all the remaining stone and win.
            #
            # Furthermore, if it is ever player A's turn where there are 4x (x > 1) stones left, player A can never win either. Again, we can prove this with a proof by induction:
            # - Player A could take 1 stone, which leaves player B with 4x-1 stones, so player B can take 3 stones, and player A will now be left with 4x-1-3 = 4x-4 = 4(x-1) stones.
            # - Player A could take 2 stones, which leaves player B with 4x-2 stones, so player B can take 2 stones, and player A will now be left with 4x-2-2 = 4x-4 = 4(x-1) stones.
            # - Player A could take 3 stones, which leaves player B with 4x-3 stones, so player B can take 1 stone, and player A will now be left with 4x-3-1 = 4x-4 = 4(x-1) stones.
            #
            # In this way, if player A starts off with 4x stones, player B can always respond such that in player A's next turn there will be 4(x-1) stones. At some point, player A will be left with just 4 stones (which we can consider the base case), in which case player A will lose, as shown above.
            #
            # Therefore, we can win only if the number of stones left in our first turn is *not* equal to 4x, where x >= 1.
            return not (stones_left % 4 == 0)

        return can_win_directly(n) or can_win_eventually(n)

        def can_win_eventually(stones_left: int, my_turn: bool) -> bool:
            """
            Check if we can win the game (it doesn't )
            """
            if my_turn and can_win_directly(stones_left):
                return True
            else:
                # Switch which player's turn it is.
                other_turn = not my_turn

                # Try all possibilities for the number of stones this player could take. The player can take at most `stones_left` stones.
                for stones_taken in range(1, min(3, stones_left) + 1):
                    if can_win_eventually(stones_left - stones_taken, other_turn):
                        return True
                return False

        # We get the first turn.
        return can_win_eventually(n, my_turn=True)

    def logic_optimized(self, n: int) -> bool:
        """
        Approach:  Logic, but with bit optimizations.
        Idea:      Same as the regular solution.
        Time:      O(1): Same as the regular solution.
        Space:     O(1): Same as the regular solution.
        Leetcode:  9 ms runtime, 16.52 MB memory
        """

        # If the lower 2 bits of n are 0 (i.e. match this pattern), that means n is divisible by 4, in which case we would lose the game.
        loss_pattern = 0b00
        mask = 0b11
        lose_game = (n & mask) == loss_pattern
        return not (lose_game)
