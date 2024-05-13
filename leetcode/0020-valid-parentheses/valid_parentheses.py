#!/usr/bin/env python3

# Valid Parentheses
#
# https://leetcode.com/problems/valid-parentheses/
#
# Given a string s containing just the characters '(', ')', '{', '}', '[' and
# ']', determine if the input string is valid.
#
# An input string is valid if:
#
# Open brackets must be closed by the same type of brackets.
# Open brackets must be closed in the correct order.
# Every close bracket has a corresponding open bracket of the same type.


from collections import deque


def test():
    """
    Run `pytest <this-file > `.
    """

    def test_algo(algo):
        assert algo("()") == True

        assert algo("()[]{}") == True

        assert algo("(]") == False

        # Open brackets are not closed in correct order.
        assert algo("([)]") == False

        assert algo("(())") == True

        assert algo("[()]") == True

        # Edge case: need to check that all opening parentheses are matched.
        assert algo("[") == False

        # Edge case: need to check that all opening parentheses are matched.
        assert algo("]") == False

        # Edge case: empty should be valid.
        assert algo("") == True

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.stack, solution.stack_opposite_map]:
        test_algo(algo)


class Solution:
    def stack(self, s: str) -> bool:
        """
        Approach:  Using stack, with opening to closing parentheses map.
        Idea:      Use a stack to keep track of the most recently opened parenthesis. Anytime a closing parenthesis char is read, we assert that the top element on the stack is the corresponding opening parenthesis. At the end, we need to assert the stack is empty to ensure every opening parenthesis was matched with a closing one.
        Time:      O(n): We iterate over each char in the input string exactly once, and either push an opening to the stack (O(1)) or pop an opening parenthesis from the stack and compare it with a closing parenthesis (O(1)).
        Space:     O(n): We push every opening parenthesis to the stack, and there are at most n of those (for invalid strings, whereas there would be exactly n/2 for valid strings).
        Leetcode:  33 ms runtime, 16.58 MB memory
        """

        # A stack storing the most recently encountered opening parenthesis at the top.
        opening_parenthesis_stack = []

        # Map closing to opening parentheses.
        closing_to_opening_parentheses = {")": "(", "]": "[", "}": "{"}
        opening_parentheses = set(closing_to_opening_parentheses.values())

        for c in s:
            if c in opening_parentheses:
                # Opening parentheses.
                opening_parenthesis_stack.append(c)
            elif c in closing_to_opening_parentheses:
                # Closing parentheses: if the stack is empty or the top of the stack does not match the expected opening parenthesis.
                if not opening_parenthesis_stack or opening_parenthesis_stack.pop() != closing_to_opening_parentheses[c]:
                    return False

        # In a valid string, we must have matched every opening parenthesis with a closing parenthesis, so assert the stack is empty.
        return len(opening_parenthesis_stack) == 0

    def stack_opposite_map(self, s: str) -> bool:
        """
        Approach:  Using stack, with opening to closing parentheses map.
        Idea:      Same as regular stack approach, just that we store the opening and closing parentheses differently in a hashmap.
        Time:      O(n): Same as regular stack approach.
        Space:     O(n): Same as regular stack approach.
        Leetcode:  44 ms runtime, 16.62 MB memory
        """

        # A stack storing the most recently encountered opening parenthesis at the top.
        opening_parenthesis_stack = []

        # Map opening to closing parentheses.
        opening_to_closing_parentheses = {"(": ")", "[": "]", "{": "}"}

        for c in s:
            if c in opening_to_closing_parentheses:
                # Opening parentheses.
                opening_parenthesis_stack.append(c)
            else:
                # Closing parentheses: if the stack is empty or the top of the stack does not match the expected opening parenthesis.
                if len(opening_parenthesis_stack) == 0 or opening_to_closing_parentheses[opening_parenthesis_stack.pop()] != c:
                    return False

        # In a valid string, we must have matched every opening parenthesis with a closing parenthesis, so assert the stack is empty.
        return len(opening_parenthesis_stack) == 0
