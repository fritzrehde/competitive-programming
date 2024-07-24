#!/usr/bin/env python3

# Merge Two Sorted Lists
#
# https://leetcode.com/problems/merge-two-sorted-lists/
#
# You are given the heads of two sorted linked lists list1 and list2.
#
# Merge the two lists into one sorted list. The list should be made by splicing
# together the nodes of the first two lists.
#
# Return the head of the merged linked list.

from typing import List, Optional
from linked_list import ListNode


def test():
    """
    Run `pytest <this-file>`.
    """

    def exec_algo(list1: List[int], list2: List[int]) -> List[int]:
        return ListNode.to_list(algo(ListNode.from_list(list1), ListNode.from_list(list2)))

    def test_algo(algo):
        assert exec_algo(list1=[1, 2, 4], list2=[1, 3, 4]) == [1, 1, 2, 3, 4, 4]

        assert exec_algo(list1=[], list2=[]) == []

        assert exec_algo(list1=[], list2=[0]) == [0]

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.iterative, solution.recursive, solution.iterative_with_dummy]:
        test_algo(algo)


class Solution:
    def iterative(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        """
        Approach:  Iterative.
        Idea:      Perform the merge step of merge-sort.
        Time:      O(n): Iterate over both lists, incrementing the ptr in one of the lists every time.
        Space:     O(1): No additional memory is used.
        Leetcode:  35 ms runtime, 16.44 MB memory
        """

        # Perform merging step of merge-sort.

        merged_head = None
        merged_tail = None

        while list1 or list2:
            if list1 and list2:
                min_node = list1 if list1.val < list2.val else list2

                if not merged_head:
                    # Make min node head of merged list and tail of node.
                    merged_head = min_node
                    merged_tail = min_node
                else:
                    # Append min node to merged list.
                    merged_tail.next = min_node
                    merged_tail = merged_tail.next

                # min_node = min_node.next
                if min_node == list1:
                    list1 = list1.next
                elif min_node == list2:
                    list2 = list2.next

            elif list1:
                # list2 is empty, so append rest of list1.
                if not merged_head:
                    merged_head = list1
                elif merged_tail:
                    merged_tail.next = list1
                break
            elif list2:
                # list1 is empty, so append rest of list2.
                if not merged_head:
                    merged_head = list2
                elif merged_tail:
                    merged_tail.next = list2
                break

        return merged_head

    def recursive(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        """
        Approach:  Recursive.
        Idea:      Perform the merge step of merge-sort.
        Time:      O(n): Iterate over both lists, incrementing the ptr in one of the lists every time.
        Space:     O(1): No additional memory is used.
        Leetcode:  37 ms runtime, 16.52 MB memory
        """

        # Perform merging step of merge-sort.

        def recursive(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
            if not list1:
                return list2
            if not list2:
                return list1

            if list1.val < list2.val:
                list1.next = recursive(list1.next, list2)
                return list1
            else:
                list2.next = recursive(list2.next, list1)
                return list2

        return recursive(list1, list2)

    def iterative_with_dummy(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        """
        Approach:  Iterative, with dummy head.
        Idea:      Perform the merge step of merge-sort.
        Time:      O(n): Iterate over both lists, incrementing the ptr in one of the lists every time.
        Space:     O(1): No additional memory is used.
        Leetcode:  33 ms runtime, 16.44 MB memory
        """

        # Perform merging step of merge-sort.

        # By creating a dummy head node for the merged list, we never need to check if the merged list is empty, simplifying the code.
        dummy_merged_head = ListNode()
        merged_tail = dummy_merged_head

        while list1 and list2:
            min_node = list1 if list1.val < list2.val else list2

            # Append min node to merged list.
            merged_tail.next = min_node
            merged_tail = merged_tail.next

            # min_node = min_node.next
            if min_node == list1:
                list1 = list1.next
            elif min_node == list2:
                list2 = list2.next

        if not list2:
            # list2 is empty, so append rest of list1.
            merged_tail.next = list1
        elif not list1:
            # list1 is empty, so append rest of list2.
            merged_tail.next = list2

        # Remove the dummy head.
        merged_head = dummy_merged_head.next
        return merged_head
