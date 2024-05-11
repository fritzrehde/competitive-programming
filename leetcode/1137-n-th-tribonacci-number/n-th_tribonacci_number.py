#!/usr/bin/env python3

# N-Th Tribonacci Number
#
# https://leetcode.com/problems/n-th-tribonacci-number/
#
# The Tribonacci sequence Tn is defined as follows:
#
# T0 = 0, T1 = 1, T2 = 1, and Tn+3 = Tn + Tn+1 + Tn+2 for n >= 0.
#
# Given n, return the value of Tn.

def test():
    """
    Run `pytest <this-file > `.
    """

    def test_algo(algo):
        assert algo(4) == 4

        assert algo(25) == 1389537

        # Edge cases: base cases
        assert algo(0) == 0
        assert algo(1) == 1
        assert algo(2) == 1

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.dynamic_programming, solution.dynamic_programming_constant_space_table, solution.dynamic_programming_constant_space_variables, solution.matrix_exponential]:
        test_algo(algo)


class Solution:
    def dynamic_programming(self, n: int) -> int:
        """
        Approach:  Dynamic programming.
        Idea:      Define the subproblem dp[i] as the ith tribonacci number.
        Time:      O(n): There are n subproblems, each of which take O(1).
        Space:     O(n): The DP table is 1D and stores n elements.
        Leetcode:  35 ms runtime, 16.44 MB memory
        """

        # Subproblem: dp[i] is the ith tribonacci number, which is the sum of the previous three tribonacci numbers.
        dp = [None for _ in range(0, n+1)]

        # Order of computation: increasing order of i, since dp[i] only depends on dp[i-1], dp[i-2] and dp[i-3] in the recurrence.
        for i in range(0, n+1):
            if i == 0:
                # Base case
                dp[i] = 0
            elif i == 1:
                # Base case
                dp[i] = 1
            elif i == 2:
                # Base case
                dp[i] = 1
            else:
                # Recurrence:
                dp[i] = dp[i-1] + dp[i-2] + dp[i-3]

        # Overall answer: we precisely want the nth tribonacci number.
        return dp[n]

    def dynamic_programming_constant_space_table(self, n: int) -> int:
        """
        Approach:  Dynamic programming with constant space DP table.
        Idea:      We only store the three most recently calculated tribonacci numbers in the DP table.
        Time:      O(n): There are n subproblems, each of which take O(1).
        Space:     O(3) = O(1): Our DP table only needs to store the most recent three tribonacci numbers to calculate the next.
        Leetcode:  36 ms runtime, 16.51 MB memory
        """

        # Subproblem: dp[i % 3] is the ith tribonacci number, which is the sum of the previous three tribonacci numbers.
        dp = [0, 1, 1]
        dp_len = len(dp)

        def ith(i: int) -> int:
            """
            The index where the ith tribonacci number is stored, given that the ith tribonacci number is one of the last three calculated ones.
            """
            return i % dp_len

        # Order of computation: increasing order of i, since the ith tribonacci number only depends on the (i-1)th, (i-2)th and (i-3)th tribonacci numbers in the recurrence.
        for i in range(3, n+1):
            # Recurrence:
            dp[ith(i)] = dp[ith(i-1)] + dp[ith(i-2)] + dp[ith(i-3)]

        # Overall answer: we precisely want the nth tribonacci number.
        return dp[ith(n)]

    def dynamic_programming_constant_space_variables(self, n: int) -> int:
        """
        Approach:  Dynamic programming with constant space local variables.
        Idea:      We only store the three most recently calculated tribonacci numbers in local variables.
        Time:      O(n): There are n subproblems, each of which take O(1).
        Space:     O(1): We store and update local variables that store the most recent three tribonacci numbers required to calculate the next.
        Leetcode:  37 ms runtime, 16.46 MB memory
        """

        # Base cases
        if 0 <= n <= 2:
            return [0, 1, 1][n]

        # Subproblem: dp_i is the ith tribonacci number, which is the sum of the previous three tribonacci numbers.
        # dp_i_x represents the (i-x)th tribonacci number.
        dp_i_3, dp_i_2, dp_i_1 = 0, 1, 1

        # Order of computation: increasing order of i, since the ith tribonacci number only depends on the (i-1)th, (i-2)th and (i-3)th tribonacci numbers in the recurrence.
        for i in range(3, n+1):
            # Recurrence:
            dp_i = dp_i_1 + dp_i_2 + dp_i_3

            # Shift everything one to the left.
            dp_i_3 = dp_i_2
            dp_i_2 = dp_i_1
            dp_i_1 = dp_i

        # Overall answer: we precisely want the nth tribonacci number.
        return dp_i

    def matrix_exponential(self, n: int) -> int:
        """
        Approach:  Matrix exponential.
        Idea:      We formulate the calculation of the ith tribonacci element as a set of linear equations on the previous three tribonacci numbers, and solve this using matrices.
        Time:      O(log n): Raising a constant size 3x3 matrix to the power of n takes O(log n) when implemented efficiently using exponentiation by squaring (and squaring is constant, which it is for our constant size matrix).
        Space:     O(1): We only store the constant size matrix and vector M0.
        Leetcode:  73 ms runtime, 36.69 MB memory
        """

        import numpy as np

        # Given dp_i_3, dp_i_2 and dp_i_1 (where dp_i_x represents the (i-x)th tribonacci number), we can formulate a set of linear equations to calculate the ith tribonacci number:
        #
        # dp_i_2 = 0 * dp_i_3 + 1 * dp_i_2 + 0 * dp_i_1
        # dp_i_1 = 0 * dp_i_3 + 0 * dp_i_2 + 1 * dp_i_1
        # dp_i_0 = 1 * dp_i_3 + 1 * dp_i_2 + 1 * dp_i_1
        #
        # We can transform these linear equations into a multiplication of a matrix with a vector:
        # [ dp_i_2 ]   [ 0 1 0 ]   [ dp_i_3 ]
        # [ dp_i_1 ] = [ 0 0 1 ] x [ dp_i_2 ]
        # [ dp_i_0 ]   [ 1 1 1 ]   [ dp_i_1 ]
        #
        # We can give these vectors and matrices names:
        # M1 = matrix * M0
        #
        # To get the nth tribonacci number dp_n_0, we need to find Mn:
        # Mn = matrix * (matrix * (matrix * (... * M0))) = matrix^(n-2) * M0
        #
        # Then, dp_n_0 will be in Mn[2] (3rd row in vector).

        # Base cases
        if 0 <= n <= 2:
            return [0, 1, 1][n]

        matrix = np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]])
        M0 = [0, 1, 1]
        Mn = np.dot(np.linalg.matrix_power(matrix, n-2), M0)
        return Mn[2]
