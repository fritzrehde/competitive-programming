#!/usr/bin/env python3

# Reverse a Linked List
#
# https://www.hackerrank.com/challenges/reverse-a-linked-list/problem
#
# Given the pointer to the head node of a linked list, change the next pointers
# of the nodes so that their order is reversed. The head pointer given may be
# null meaning that the initial list is empty.

class Node(object):
    def __init__(self, data=None):
        self.data = data
        self.next = None

    @staticmethod
    def from_list(arr: list):
        head = None
        prev = None
        for element in arr:
            cur = Node(element)
            if not head:
                head = cur
            else:
                prev.next = cur
            prev = cur
        return head

    def to_list(self):
        arr = []
        node = self
        while node:
            arr.append(node.data)
            node = node.next
        return arr

def test():
    # specify approach
    reverse = Solution().iterative_without_tmp_node

    # helper
    def test(input: list, expected: list):
        reversed = reverse(Node().from_list(input))
        expected = Node().from_list(expected)

        # head might be None
        if reversed and expected:
            assert reversed.to_list() == expected.to_list()
        else:
            assert reversed == expected

    # pytest
    test([1,2,3,4,5], [5,4,3,2,1])
    test([1,1,1], [1,1,1])
    test([1], [1])
    test([], [])

class Solution:
    """
    Approach:  Iterative with temporary nodes (cur_next)
    Idea:      Loop through linked list and always swap cur with prev node (and adjust next attributes)
    Time:      O(n), iteration through entire linked list
    Space:     O(1), in-place
    """
    def iterative_with_tmp_node(self, head: Node) -> Node:
        prev, cur = None, head

        while cur:
            # state: prev -> cur -> cur.next

            cur_next = cur.next
            cur.next = prev

            # state: prev <- cur ; cur_next

            # set pointers for next iteration
            prev = cur
            cur = cur_next

            # state: old_prev <- old_cur/new_prev -> new_cur/old_cur_next

        return prev

    """
    Approach:  Iterative with no temporary nodes, otherwise same as above
    """
    def iterative_without_tmp_node(self, head: Node) -> Node:
        prev, cur = None, head

        while cur:
            cur.next, cur, prev = prev, cur.next, cur

        return prev

    """
    Approach:  Recursive
    Time:      O(n), iteration through entire linked list
    Space:     O(n), using call stack to store recursive function calls, max call stack depth == list length
    """
    def recursive(self, head: Node) -> Node:
        # base case
        if not head or not head.next:
            return head

        # reverse [head, rest_head, rest...]
        rest_head = self.recursive(head.next)
        head.next.next = head
        head.next = None

        return rest_head
