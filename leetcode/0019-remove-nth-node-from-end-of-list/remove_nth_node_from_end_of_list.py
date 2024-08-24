#!/usr/bin/env python3

# Remove Nth Node From End of List
#
# https://leetcode.com/problems/remove-nth-node-from-end-of-list
#
# Given the head of a linked list, remove the nth node from the end of the list
# and return its head.

from typing import Optional
from linked_list import ListNode


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert ListNode.to_list(
            algo(head=ListNode.from_list([1, 2, 3, 4, 5]), n=2)
        ) == [1, 2, 3, 5]
        assert ListNode.to_list(algo(head=ListNode.from_list([1]), n=1)) == []
        assert ListNode.to_list(algo(head=ListNode.from_list([1, 2]), n=1)) == [
            1
        ]
        assert ListNode.to_list(algo(head=ListNode.from_list([1, 2]), n=2)) == [
            2
        ]

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.two_pass, solution.one_pass]:
        test_algo(algo)


class Solution:
    def two_pass(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        """
        Approach:  Two pass.
        Idea:      Find the length of the linked list in one pass, and then remove the element in another pass.
        Time:      O(n): We must traverse all n elements to find the length of the list, and then potentially all elements again to remove the desired element.
        Space:     O(1): No additional memory is used.
        Leetcode:  40 ms runtime, 16.60 MB memory
        """

        def len(head: Optional[ListNode]) -> int:
            i = 0
            curr = head
            while curr is not None:
                curr = curr.next
                i += 1
            return i

        prev = None
        curr = head
        # The 1-based index of the element to be removed.
        m = len(head) - n
        for _ in range(1, m + 1):
            assert curr is not None
            prev = curr
            curr = curr.next

        assert curr is not None

        if prev is None:
            # The head should be removed.
            head = curr.next
        else:
            prev.next = curr.next

        return head

    def one_pass(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        """
        Approach:  One pass with two pointers.
        Idea:      Have pointers starting at head and head+n (advanced by n), and find element to delete by iterating until head+n pointer reaches end.
        Time:      O(n): We traverse linked list once with two pointers.
        Space:     O(1): No additional memory is used.
        Leetcode:  31 ms runtime, 16.57 MB memory
        """

        def advance_by_n(head: ListNode, n: int) -> ListNode:
            curr = head
            for i in range(0, n):
                assert curr is not None
                curr = curr.next
            return curr

        assert head is not None

        prev = None
        curr = head
        curr_plus_n = advance_by_n(head, n)

        # The 1-based index of the element to be removed.
        while curr_plus_n is not None:
            # Advance both pointers.
            assert curr is not None
            prev = curr
            curr = curr.next
            assert curr_plus_n is not None
            curr_plus_n = curr_plus_n.next

        assert curr is not None

        if prev is None:
            # The head should be removed.
            head = curr.next
        else:
            prev.next = curr.next

        return head
