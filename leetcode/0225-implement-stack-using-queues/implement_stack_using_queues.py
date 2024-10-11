#!/usr/bin/env python3

# Implement Stack using Queues
#
# https://leetcode.com/problems/implement-stack-using-queues
#
# Implement a last-in-first-out (LIFO) stack using only two queues. The
# implemented stack should support all the functions of a normal stack (push,
# top, pop, and empty).
# Implement the MyStack class:
#
# void push(int x) Pushes element x to the top of the stack.
# int pop() Removes the element on the top of the stack and returns it.
# int top() Returns the element on the top of the stack.
# boolean empty() Returns true if the stack is empty, false otherwise.
#
# Notes:
#
# You must use only standard operations of a queue, which means that only push
# to back, peek/pop from front, size and is empty operations are valid.
# Depending on your language, the queue may not be supported natively. You may
# simulate a queue using a list or deque (double-ended queue) as long as you use
# only a queue's standard operations.


from collections import deque
from typing import Deque


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        stack = algo()

        stack.push(1)
        assert stack.empty() == False
        stack.push(2)
        assert stack.top() == 2
        assert stack.pop() == 2
        assert stack.top() == 1
        assert stack.pop() == 1
        assert stack.empty() == True

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.two_queue_brute_force, solution.one_queue]:
        test_algo(algo)


class Solution:
    def two_queue_brute_force(self):
        """
        Approach:  Brute-force.
        Idea:      ?
        Time:      O(?): ?
        Space:     O(?): ?
        Leetcode:  ? ms runtime, ? MB memory
        """

        class MyStack:
            def __init__(self):
                # Our stack from top to bottom element is: whichever of q1 and
                # q2 is non-empty.
                self.q1 = deque()
                self.q2 = deque()

            def non_emtpy_queue(self) -> Deque:
                if len(self.q1) == 0:
                    return self.q2
                elif len(self.q2) == 0:
                    return self.q1
                else:
                    raise Exception("one of the queues is always empty")

            def emtpy_queue(self) -> Deque:
                if len(self.q1) == 0:
                    return self.q1
                elif len(self.q2) == 0:
                    return self.q2
                else:
                    raise Exception("one of the queues is always empty")

            def push(self, x: int) -> None:
                # O(1)
                self.non_emtpy_queue().append(x)

            def shuffle(self) -> Deque:
                # O(n)
                # Move all elements besides leftmost (top of stack) from
                # non-empty to empty queue.
                q1 = self.non_emtpy_queue()
                q2 = self.emtpy_queue()
                while len(q1) > 1:
                    q2.append(q1.popleft())
                # Return the queue that now contains the top of the stack.
                return q1

            def pop(self) -> int:
                # O(n)
                return self.shuffle().popleft()

            def top(self) -> int:
                # O(1)
                return self.non_emtpy_queue()[-1]

            def empty(self) -> bool:
                # O(1)
                return len(self.q1) == 0 and len(self.q2) == 0

        return MyStack()

    def one_queue(self):
        """
        Approach:  Brute-force.
        Idea:      ?
        Time:      O(?): ?
        Space:     O(?): ?
        Leetcode:  ? ms runtime, ? MB memory
        """

        class MyStack:
            def __init__(self):
                # Our stack from top to bottom element is: q.
                self.q = deque()

            def push(self, x: int) -> None:
                # O(1)
                self.q.append(x)

            def pop(self) -> int:
                # O(n)
                # Bring leftmost (top of stack) all the way to the right (where
                # it can be popped) by repeatedly popping and re-appending all
                # other elements.
                n = len(self.q)
                for _ in range(0, n - 1):
                    self.q.append(self.q.popleft())
                return self.q.popleft()

            def top(self) -> int:
                # O(1)
                return self.q[-1]

            def empty(self) -> bool:
                # O(1)
                return len(self.q) == 0

        return MyStack()
