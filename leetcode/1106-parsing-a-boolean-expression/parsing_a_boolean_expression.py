#!/usr/bin/env python3

# Parsing A Boolean Expression
#
# https://leetcode.com/problems/parsing-a-boolean-expression
#
# A boolean expression is an expression that evaluates to either true or false.
# It can be in one of the following shapes:
#
# 't' that evaluates to true.
# 'f' that evaluates to false.
# '!(subExpr)' that evaluates to the logical NOT of the inner expression
# subExpr.
# '&(subExpr1, subExpr2, ..., subExprn)' that evaluates to the logical AND of
# the inner expressions subExpr1, subExpr2, ..., subExprn where n >= 1.
# '|(subExpr1, subExpr2, ..., subExprn)' that evaluates to the logical OR of the
# inner expressions subExpr1, subExpr2, ..., subExprn where n >= 1.
#
# Given a string expression that represents a boolean expression, return the
# evaluation of that expression.
# It is guaranteed that the given expression is valid and follows the given
# rules.


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(expression="!(&(f,t))") == True
        assert algo(expression="&(|(f))") == False
        assert algo(expression="|(f,f,f,t)") == True
        assert algo(expression="|(&(f,t),|(f,t,f,t))") == True

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.python_eval]:
        test_algo(algo)


class Solution:
    # TODO: not working :(
    def brute_force(self, expression: str) -> bool:
        """
        Approach:  Brute-force.
        Idea:      ?
        Time:      O(?): ?
        Space:     O(?): ?
        Leetcode:  ? ms runtime, ? MB memory
        """

        import re

        def eval(expr: str) -> bool:
            print(expr)
            match expr:
                case "t":
                    return True
                case "f":
                    return False
                case _:
                    if m := re.match(r"^!\((.*)\)$", expr):
                        sub_expr = m.group(1)
                        return not eval(sub_expr)
                    elif m := re.match(r"^&\((.*)\)$", expr):
                        # TODO: splitting on "," is a bug: what if sub_exprs of the sub_exprs also contain ","s.
                        sub_exprs = m.group(1).split(",")
                        return all(eval(sub_expr) for sub_expr in sub_exprs)
                    elif m := re.match(r"^\|\((.*)\)$", expr):
                        # TODO: splitting on "," is a bug: what if sub_exprs of the sub_exprs also contain ","s.
                        sub_exprs = m.group(1).split(",")
                        return any(eval(sub_expr) for sub_expr in sub_exprs)
                    else:
                        raise Exception(
                            "unreachable: assume all input is valid."
                        )

        return eval(expression)

    def python_eval(self, expression: str) -> bool:
        """
        Approach:  Use python evaluation.
        Idea:      Transform the input expression into a python expression, by mapping "&" to `all` and "|" to `any`.
        Time:      O(n): Given that n is the length of the expression, replacing substrings is O(n) given that m is small and constant. It is assumed the evaluation is O(n) as well, though this is treated as a black box.
        Space:     O(n): We create a new python expression string with a length proportional to n.
        Leetcode:  127 ms runtime, 26.32 MB memory
        """

        # TODO: replacing the string in-place would be cool, instead of making more and more copies.
        py_expr = (
            expression.replace("t", "True")
            .replace("f", "False")
            # NOTE: "!(expr)" => "not &(expr)" would also work.
            # "!(expr)" => "not |(expr)" => "not any([expr])"
            .replace("!(", "not |(")
            .replace("&(", "all([")
            .replace("|(", "any([")
            .replace(")", "])")
        )

        return bool(eval(py_expr))
