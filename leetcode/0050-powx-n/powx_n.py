#!/usr/bin/env python3

# Pow(X, N)
#
# https://leetcode.com/problems/powx-n/
#
# Implement pow(x, n), which calculates x raised to the power n (i.e., x^n).


def test():
    """
    Run `pytest <this-file > `.
    """

    def test_algo(algo):
        assert algo(2, 10) == 1024

        assert algo(5, 0) == 1

        assert algo(2, -2) == 0.25

        # Edge case: undefined in maths, we define 0^0 = 1
        assert algo(0, 0) == 1

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.std_lib, solution.exponentiation_by_squaring_recursive, solution.exponentiation_by_squaring_iterative]:
        test_algo(algo)


class Solution:
    def brute_force(self, x: float, n: int) -> float:
        """
        Approach:  Brute-force.
        Idea:      We use the property that x^n is equal to multiplying x with itself n times.
        Time:      O(n): We perform n multiplications (each assumed O(1)).
        Space:     O(1): No additional space is used besides the output integer.
        Leetcode:  Time Limit Exceeded
        """

        product = 1

        # x^(-n) = (x^(-1))^n = (1/x)^n
        if n < 0:
            x = 1/x
            n = abs(n)

        # x^n is equivalent to multiplying x with itself n times.
        for _ in range(0, n):
            product *= x

        return product

    def std_lib(self, x: float, n: int) -> float:
        """
        Approach:  Standard library implementation.
        Idea:      We cheat by simply calling Python's standard library power implementation.
        Time:      O(?): We treat it as a black-box, so we don't know what algorithm it uses internally.
        Space:     O(?): We treat it as a black-box, so we don't know what algorithm it uses internally.
        Leetcode:  30 ms runtime, 16.50 MB memory
        """

        return x ** n

    def exponentiation_by_squaring_recursive(self, x: float, n: int) -> float:
        """
        Approach:  Exponentiation by squaring, recursively.
        Idea:      We use the property that x^n is equal to multiplying (x^2)^(n/2) if n is even and (x(x^2)^((n-1)/2)) if n is odd.
        Time:      O(log n): According to the master theorem, we get T(n) = a*T(n/b)+f(n), where a=1 and b=2 because every problem of size n is reduced to a=1 subproblems of size n/b=n/2, and the overhead to divide (split in half) and combine (squaring x, another multiplication with x if n is odd) is f(n) = O(1). This puts us in case 2 of the master theorem, giving us O(log n).
        Space:     O(1): No additional space is used besides the output integer.
        Leetcode:  39 ms runtime, 16.44 MB memory
        """

        def pow(x: float, n: int) -> float:
            if n == 0:
                # Base case: x^0 = 1
                return 1
            elif n == 1:
                # Base case: x^1 = x
                return x
            else:
                x_squared = x * x
                if n % 2 == 0:
                    # If n even: x^n = (x^2)^(n/2)
                    return pow(x_squared, n/2)
                else:
                    # If n odd: x^n = x(x^2)^((n-1)/2)
                    return x * pow(x_squared, (n-1)/2)

        # x^(-n) = (x^(-1))^n = (1/x)^n
        if n < 0:
            x = 1/x
            n = abs(n)

        return pow(x, n)

    def exponentiation_by_squaring_iterative(self, x: float, n: int) -> float:
        """
        Approach:  Exponentiation by squaring, iteratively.
        Idea:      Same as recursive implementation of exponentiation by squaring.
        Time:      O(log n): Same as recursive implementation of exponentiation by squaring.
        Space:     O(1): Same as recursive implementation of exponentiation by squaring.
        Leetcode:  23 ms runtime, 16.59 MB memory
        """

        # x^(-n) = (x^(-1))^n = (1/x)^n
        if n < 0:
            x = 1/x
            n = abs(n)

        result = 1

        while n > 0:
            if n % 2 == 0:
                # If n even: x^n = (x^2)^(n/2)
                x = x * x
                n = n/2
            else:
                # If n odd: x^n = x(x^2)^((n-1)/2)
                result = x * result
                x = x * x
                n = (n-1)/2

        return result
