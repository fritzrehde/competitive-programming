#!/usr/bin/env python3

# Min Stack
#
# https://leetcode.com/problems/min-stack
#
# Design a stack that supports push, pop, top, and retrieving the minimum
# element in constant time.
# Implement the MinStack class:
#
# MinStack() initializes the stack object.
# void push(int val) pushes the element val onto the stack.
# void pop() removes the element on the top of the stack.
# int top() gets the top element of the stack.
# int getMin() retrieves the minimum element in the stack.
#
# You must implement a solution with O(1) time complexity for each function.


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        stack = algo()

        stack.push(-2)
        stack.push(0)
        stack.push(-3)
        assert stack.getMin() == -3
        stack.pop()
        assert stack.top() == 0
        assert stack.getMin() == -2

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [
        solution.brute_force,
        solution.tuple_stack,
        solution.two_stacks,
    ]:
        test_algo(algo)


class Solution:
    def brute_force(self):
        """
        Approach:  Brute-force.
        Idea:      ?
        Time:      O(n): ?
        Space:     O(?): ?
        Leetcode:  371 ms runtime, 20.38 MB memory
        """

        class MinStack:
            def __init__(self):
                self.s = []

            # O(1)
            def push(self, val: int) -> None:
                self.s.append(val)

            # O(1)
            def pop(self) -> None:
                self.s.pop()

            # O(1)
            def top(self) -> int:
                return self.s[-1]

            # O(n)
            def getMin(self) -> int:
                return min(self.s)

        return MinStack()

    def tuple_stack(self):
        """
        Approach:  Store min for each stack element.
        Idea:      ?
        Time:      O(?): ?
        Space:     O(?): ?
        Leetcode:  11 ms runtime, 20.92 MB memory
        """

        class MinStack:
            def __init__(self):
                self.s = []

            def push(self, val: int) -> None:
                if len(self.s) == 0:
                    new_min = val
                else:
                    _curr_top, curr_min = self.s[-1]
                    new_min = min(curr_min, val)
                self.s.append((val, new_min))

            def pop(self) -> None:
                self.s.pop()

            def top(self) -> int:
                curr_top, _curr_min = self.s[-1]
                return curr_top

            def getMin(self) -> int:
                _curr_top, curr_min = self.s[-1]
                return curr_min

        return MinStack()

    def two_stacks(self):
        """
        Approach:  Store min for each stack element in separate stack.
        Idea:      ?
        Time:      O(?): ?
        Space:     O(?): ?
        Leetcode:  4 ms runtime, 20.44 MB memory
        """

        class MinStack:
            def __init__(self):
                self.elem_stack = []
                self.min_stack = []

            def push(self, val: int) -> None:
                if len(self.elem_stack) == 0:
                    new_min = val
                else:
                    curr_min = self.min_stack[-1]
                    new_min = min(curr_min, val)

                self.elem_stack.append(val)
                self.min_stack.append(new_min)

            def pop(self) -> None:
                self.elem_stack.pop()
                self.min_stack.pop()

            def top(self) -> int:
                return self.elem_stack[-1]

            def getMin(self) -> int:
                return self.min_stack[-1]

        return MinStack()
