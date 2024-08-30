#!/usr/bin/env python3

# Letter Combinations of a Phone Number
#
# https://leetcode.com/problems/letter-combinations-of-a-phone-number
#
# Given a string containing digits from 2-9 inclusive, return all possible
# letter combinations that the number could represent. Return the answer in any
# order.
# A mapping of digits to letters (just like on the telephone buttons) is given
# below. Note that 1 does not map to any letters.


from typing import Dict, List, Optional


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        def fmt(list):
            return sorted(list)

        assert fmt(algo(digits="23")) == fmt(
            [
                "ad",
                "ae",
                "af",
                "bd",
                "be",
                "bf",
                "cd",
                "ce",
                "cf",
            ]
        )
        assert fmt(algo(digits="")) == fmt([])
        assert fmt(algo(digits="2")) == fmt(["a", "b", "c"])

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.dfs_list_acc, solution.dfs_str_acc]:
        test_algo(algo)


class Solution:
    def dfs_list_acc(self, digits: str) -> List[str]:
        """
        Approach:  Backtracking with DFS.
        Idea:      See approach above.
        Time:      O(4^n): There are (at most) 4^n unique combinations we include.
        Space:     O(4^n * n): We store every possible combination (4^n), each having at most size n.
        Leetcode:  46 ms runtime, 16.58 MB memory
        """

        digit_to_letters: Dict[int, List[str]] = {
            2: ["a", "b", "c"],
            3: ["d", "e", "f"],
            4: ["g", "h", "i"],
            5: ["j", "k", "l"],
            6: ["m", "n", "o"],
            7: ["p", "q", "r", "s"],
            8: ["t", "u", "v"],
            9: ["w", "y", "x", "z"],
        }

        combinations = []

        n = len(digits)

        def dfs(acc: List[str], digit_idx: int):
            if digit_idx < n:
                digit = int(digits[digit_idx])
                if digit_idx == 0:
                    dfs(digit_to_letters[digit], digit_idx + 1)
                else:
                    new_acc = list(
                        f"{s}{letter}"
                        for letter in digit_to_letters[digit]
                        for s in acc
                    )
                    dfs(new_acc, digit_idx + 1)
            else:
                combinations.extend(acc)

        dfs([], digit_idx=0)
        return combinations

    def dfs_str_acc(self, digits: str) -> List[str]:
        """
        Approach:  Backtracking with DFS.
        Idea:      See approach above.
        Time:      O(4^n): There are (at most) 4^n unique combinations we include.
        Space:     O(4^n * n): We store every possible combination (4^n), each having at most size n.
        Leetcode:  33 ms runtime, 16.45 MB memory
        """

        digit_to_letters: Dict[int, List[str]] = {
            2: ["a", "b", "c"],
            3: ["d", "e", "f"],
            4: ["g", "h", "i"],
            5: ["j", "k", "l"],
            6: ["m", "n", "o"],
            7: ["p", "q", "r", "s"],
            8: ["t", "u", "v"],
            9: ["w", "y", "x", "z"],
        }

        combinations = []

        n = len(digits)

        def dfs(acc: Optional[str], digit_idx: int):
            if digit_idx < n:
                digit = int(digits[digit_idx])
                for letter in digit_to_letters[digit]:
                    dfs(
                        f"{acc}{letter}" if acc is not None else letter,
                        digit_idx + 1,
                    )
            else:
                if acc is not None:
                    combinations.append(acc)

        dfs(None, digit_idx=0)
        return combinations
