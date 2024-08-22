#!/usr/bin/env python3

# Number Complement
#
# https://leetcode.com/problems/number-complement
#
# The complement of an integer is the integer you get when you flip all the 0's
# to 1's and all the 1's to 0's in its binary representation.
#
# For example, The integer 5 is "101" in binary and its complement is "010"
# which is the integer 2.
#
# Given an integer num, return its complement.


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(num=5) == 2
        assert algo(num=1) == 0

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.xor, solution.invert_directly, solution.subtraction]:
        test_algo(algo)


class Solution:
    def xor(self, num: int) -> int:
        """
        Approach:  XOR.
        Idea:      If you XOR the number with all ones (11...11), then you are left with every bit inverted.
        Time:      O(?): The XOR operator is treated as a black box, I am not sure of its performance characteristics (though assume it's O(1)).
        Space:     O(?): As above.
        Leetcode:  33 ms runtime, 16.44 MB memory
        """

        binary = bin(num).replace("0b", "")
        bit_count = len(binary)
        all_ones = int("1" * bit_count, base=2)

        # XOR
        return num ^ all_ones

    def invert_directly(self, num: int) -> int:
        """
        Approach:  Invert directly with string replacements.
        Idea:      Replace every 0 in binary repr with a 1.
        Time:      O(?): The str.replace function is treated as a black box.
        Space:     O(?): As above.
        Leetcode:  35 ms runtime, 16.39 MB memory
        """

        binary: str = bin(num).replace("0b", "")
        inverted_binary = (
            binary.replace("0", "X").replace("1", "0").replace("X", "1")
        )
        return int(inverted_binary, base=2)

    def subtraction(self, num: int) -> int:
        """
        Approach:  Subtraction.
        Idea:      If you subtract the number from a version of it with all ones (11...11), then you are left with the complement.
        Time:      O(32) = O(1): In the worst case, the input number only contains 1s, so the while loop executes 32 times.
        Space:     O(1): No additional memory is used.
        Leetcode:  41 ms runtime, 16.30 MB memory
        """

        # ones = 11.11, where len(ones) == len(num)
        ones = 0
        while ones < num:
            ones = (ones << 1) | 1

        # NOTE: XOR works as well, as explored in the solution from above.
        return ones - num
