#!/usr/bin/env python3

# Implement Queue using Stacks
#
# https://leetcode.com/problems/implement-queue-using-stacks
#
# Implement a first in first out (FIFO) queue using only two stacks. The
# implemented queue should support all the functions of a normal queue (push,
# peek, pop, and empty).
# Implement the MyQueue class:
#
# void push(int x) Pushes element x to the back of the queue.
# int pop() Removes the element from the front of the queue and returns it.
# int peek() Returns the element at the front of the queue.
# boolean empty() Returns true if the queue is empty, false otherwise.
#
# Notes:
#
# You must use only standard operations of a stack, which means only push to
# top, peek/pop from top, size, and is empty operations are valid.
# Depending on your language, the stack may not be supported natively. You may
# simulate a stack using a list or deque (double-ended queue) as long as you use
# only a stack's standard operations.


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        queue = algo()

        queue.push(1)
        assert queue.empty() == False
        queue.push(2)
        assert queue.pop() == 1
        assert queue.peek() == 2
        assert queue.pop() == 2
        assert queue.empty() == True

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force]:
        test_algo(algo)


class Solution:
    def brute_force(self):
        """
        Approach:  Brute-force.
        Idea:      ?
        Time:      O(?): ?
        Space:     O(?): ?
        Leetcode:  ? ms runtime, ? MB memory
        """

        class MyQueue:
            def __init__(self):
                # Our queue from newest to oldest element is: rev(s1) + s2
                # s1[-1] is the most recent item (last to be popped).
                self.s1 = []
                # s2[-1] is the oldest item (next to be popped).
                self.s2 = []

            def push(self, x: int) -> None:
                self.s1.append(x)

            def shuffle(self):
                # Amortised O(1), because we move every element from s1 to s2
                # exactly once.
                # Ensure s2 has elements.
                if self.s2 == []:
                    # Move all elements from s1 to s2 in reversed order.
                    while len(self.s1) > 0:
                        self.s2.append(self.s1.pop())

            def pop(self) -> int:
                self.shuffle()
                return self.s2.pop()

            def peek(self) -> int:
                self.shuffle()
                return self.s2[-1]

            def empty(self) -> bool:
                return len(self.s1) == 0 and len(self.s2) == 0

        return MyQueue()
