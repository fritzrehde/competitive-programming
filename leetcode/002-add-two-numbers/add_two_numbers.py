#!/usr/bin/env python3

# Add Two Numbers
#
# https://leetcode.com/problems/add-two-numbers/
#
# You are given two non-empty linked lists representing two non-negative
# integers. The digits are stored in reverse order, and each of their nodes
# contains a single digit. Add the two numbers and return the sum as a
# linked list.

from typing import Callable, Optional, TypeVar
from linked_list import ListNode


def test():
    """
    Run `pytest <this-file>`.
    """

    def exec_algo(l1: list[int], l2: list[int]) -> list[int]:
        return ListNode.to_list(algo(ListNode.from_list(l1), ListNode.from_list(l2)))

    def test_algo(algo):
        # Lists of same length:
        # 342 + 465 = 807
        assert exec_algo([2, 4, 3], [5, 6, 4]) == [7, 0, 8]

        # Lists of different length:
        # 1 + 32 = 33
        assert exec_algo([1], [2, 3]) == [3, 3]

        # A lot of overflow when doing digit-wise addition:
        # 99 + 999 = 1098
        assert exec_algo([9, 9], [9, 9, 9]) == [8, 9, 0, 1]

        # Edge case: the result is a list that only contains 0:
        # 0 + 0 = 0
        assert exec_algo([0], [0]) == [0]

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.digit_wise_addition]:
        test_algo(algo)


class Solution:
    def brute_force(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        """
        Approach:  Brute-force
        Idea:      Convert each list to the integer representation, sum those integers, and convert back to list representation
        Time:      O(2n) = O(n): iterate over each linked-list to collect to integer (O(n) each), sum two integers (O(1)), and convert back to list (O(n))
        Space:     O(n): only allocate two integers (O(1)), and allocate list for the returned value (O(n))
        Leetcode:  65 ms runtime, 16.66 MB memory
        """

        def list_to_integer(head: ListNode) -> int:
            """
            Convert a linked-list that stores the digits of an integer in reverse order to an integer.
            """
            integer_str = ""
            cur = head
            while (cur != None):
                # Prepend the digit, since the digit list is in reverse.
                integer_str = str(cur.val) + integer_str
                cur = cur.next
            return int(integer_str)

        def integer_to_list(integer: int) -> ListNode:
            """
            Convert an integer to a linked-list that stores the digits of the integer in reverse order.
            """
            # Edge case
            if (integer == 0):
                return ListNode(0)

            head = None
            prev = None
            while (integer != 0):
                digit = integer % 10
                integer //= 10
                cur = ListNode(digit)
                if head is None:
                    # Set the head to the first element
                    head = cur
                else:
                    prev.next = cur
                prev = cur
            return head

        int1 = list_to_integer(l1)
        int2 = list_to_integer(l2)
        sum = int1 + int2
        return integer_to_list(sum)

    def digit_wise_addition(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        """
        Approach:  Add digits individually.
        Idea:      Iterate through both linked-lists at the same time, and calculate the result digit for each pair of digits, accounting for overflows using a carry digit.
        Time:      O(n): zip together the linked-lists (but iterate until both are consumed), and calculate each digit from the digit pair.
        Space:     O(n): allocate list for the returned value.
        Leetcode:  102 ms runtime, 16.86 MB memory
        """
        T = TypeVar('T')
        U = TypeVar('U')

        def map_or(option: Optional[T], f: Callable[[T], U], default: U) -> U:
            """
            Returns the provided default result (if none), or applies a function to the contained value (if any).
            A Python implementation of Rust's `Option::map_or` method.
            """
            if (some := option) is not None:
                return f(some)
            else:
                return default

        def lval(l: ListNode) -> int:
            "Return the value contained in a list node"
            return l.val

        head = None
        prev = None
        cur1 = l1
        cur2 = l2
        carry_digit = 0

        # Iterate over digits of both lists while at least one still has digits, or we still have a carry bit to add.
        while (cur1 is not None or cur2 is not None or carry_digit != 0):
            # Add the current digits (or 0 if one list has no more digits) plus the possible carry digit.
            digit = map_or(cur1, lval, 0) + map_or(cur2, lval, 0) + carry_digit

            # Reset carry digit after using it.
            carry_digit = 0

            # Capture a carry bit if the digit is too large.
            if (digit >= 10):
                digit -= 10
                carry_digit = 1

            # Insert the digit into the linked-list as a node.
            cur = ListNode(digit)
            if head is None:
                # Set the head to the first element
                head = cur
            else:
                prev.next = cur
            prev = cur

            # Only iterate to next list element if we're not currently at last element.
            if (cur1 is not None):
                cur1 = cur1.next
            if (cur2 is not None):
                cur2 = cur2.next

        return head
