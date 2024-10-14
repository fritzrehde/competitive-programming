#!/usr/bin/env python3

# Reverse Linked List
#
# https://leetcode.com/problems/reverse-linked-list
#
# Given the head of a singly linked list, reverse the list, and return the
# reversed list.


from typing import Optional
from linked_list import ListNode


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert ListNode.to_list(
            algo(head=ListNode.from_list([1, 2, 3, 4, 5]))
        ) == [5, 4, 3, 2, 1]
        assert ListNode.to_list(algo(head=ListNode.from_list([1, 2]))) == [2, 1]
        assert ListNode.to_list(algo(head=ListNode.from_list([]))) == []

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.iterative, solution.recursive]:
        test_algo(algo)


class Solution:
    def iterative(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Approach:  Iterative.
        Idea:      Invert every pointer between two nodes.
        Time:      O(n): For each of the n elements, invert the pointer to the prev element (O(1) each).
        Space:     O(1): No additional memory is used.
        Leetcode:  39 ms runtime, 17.73 MB memory
        """

        curr = head
        prev = None

        while curr is not None:
            # Convert prev -> curr to prev <- curr.
            next = curr.next
            curr.next = prev

            prev = curr
            curr = next

        return prev

    def recursive(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Approach:  Recursive.
        Idea:      Invert every pointer between two nodes.
        Time:      O(n): For each of the n elements, invert the pointer to the prev element (O(1) each).
        Space:     O(1): No additional memory is used (besides OS recursion stack).
        Leetcode:  47 ms runtime, 17.73 MB memory
        """

        def reverse(
            curr: Optional[ListNode], prev: Optional[ListNode]
        ) -> Optional[ListNode]:
            if curr is None:
                return prev
            else:
                # Convert prev -> curr to prev <- curr.
                next = curr.next
                curr.next = prev

                return reverse(prev=curr, curr=next)

        return reverse(prev=None, curr=head)
