#!/usr/bin/env python3

# Median Of Two Sorted Arrays
#
# https://leetcode.com/problems/median-of-two-sorted-arrays/
#
# Given two sorted arrays nums1 and nums2 of size m and n respectively, return
# the median of the two sorted arrays.
#
# The overall run time complexity should be O(log (m+n)).


from typing import List


def test():
    """
    Run `pytest <this-file > `.
    """

    def test_algo(algo):
        # Median of [1, 2, 3, 5, 7]
        assert algo([1, 3], [2, 5, 7]) == 3.0

        # Median of [1, 2, 4, 5, 7]
        assert algo([1, 2], [4, 5, 7]) == 4.0

        # Median of [1, 2, 3]
        assert algo([1, 3], [2]) == 2.0

        # Median of [1, 2, 3, 4]
        assert algo([1, 2], [3, 4]) == 2.5

        # Edge case: Single element
        assert algo([42], []) == 42
        assert algo([], [42]) == 42

        # Edge case: Zero elements
        assert algo([], []) == 0

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.merge_sort, solution.merge_sort_without_allocations]:
        test_algo(algo)


class Solution:
    def brute_force(self, nums1: List[int], nums2: List[int]) -> float:
        """
        Approach:  Brute-force.
        Idea:      Concatenate both lists, then sort the resulting list and get its median.
        Time:      O((n+m)log(n+m)): The concatenated list will have length n+m (given the input lists have lengths n and m), so using merge sort takes O((n+m)log(n+m)). Finding the median is O(1).
        Space:     O(n+m): We are allocating the concatenated list with length n+m.
        Leetcode:  81 ms runtime, 16.84 MB memory
        """

        def median(l: List[int]) -> float:
            """
            Find the median of a list.
            """
            n = len(l)
            if n == 0:
                return 0
            elif n % 2 == 1:
                # Odd length.
                return l[n//2]
            else:
                # Even length.
                return (l[(n//2)-1] + l[n//2]) / 2

        merged = sorted(nums1 + nums2)
        return (median(merged))

    def merge_sort(self, nums1: List[int], nums2: List[int]) -> float:
        """
        Approach:  Merge sort combine step.
        Idea:      Use the combine step of merge sort to efficiently merge the two sorted lists.
        Time:      O(n+m): Iterate over all elements of each input list (lengths n and m), and always take the smallest. Finding the median takes O(1).
        Space:     O(n+m): We are allocating the concatenated list with length n+m.
        Leetcode:  80 ms runtime, 16.95 MB memory
        """

        def merge(sorted_l1: List[int], sorted_l2: List[int]) -> List[int]:
            """
            Merge two sorted lists together (using the merge procedure from merge sort).
            """
            l1_idx = 0
            l2_idx = 0
            l1_len = len(sorted_l1)
            l2_len = len(sorted_l2)

            concat = []

            while True:
                if l1_idx < l1_len and l2_idx < l2_len:
                    # Both lists still have elements.
                    if sorted_l1[l1_idx] <= sorted_l2[l2_idx]:
                        concat.append(sorted_l1[l1_idx])
                        l1_idx += 1
                    else:
                        concat.append(sorted_l2[l2_idx])
                        l2_idx += 1
                else:
                    # At most one of the lists still has elements, so append those remaining elements to result.
                    if l1_idx < l1_len:
                        concat.extend(sorted_l1[l1_idx:])
                    elif l2_idx < l2_len:
                        concat.extend(sorted_l2[l2_idx:])
                    break

            return concat

        def median(l: List[int]) -> float:
            """
            Find the median of a list.
            """
            n = len(l)
            if n == 0:
                return 0
            elif n % 2 == 1:
                # Odd length.
                return l[n//2]
            else:
                # Even length.
                return (l[(n//2)-1] + l[n//2]) / 2

        merged = merge(nums1, nums2)
        return (median(merged))

    def merge_sort_without_allocations(self, nums1: List[int], nums2: List[int]) -> float:
        """
        Approach:  Merge sort combine step without allocations.
        Idea:      Use the combine step of merge sort to efficiently find only the elements at indices ((n+m)/2)-1 (left) and (n+m)/2 (right) in the merged list.
        Time:      O((n+m)/2) = O(n+m): Iterate over all elements of each input list, and always set the current right element to the smallest. Finding the median takes O(1).
        Space:     O(1): We are not allocating the entire concatenated/merged list, we are only storing the two middle elements.
        Leetcode:  79 ms runtime, 16.84 MB memory
        """
        sorted_l1 = nums1
        sorted_l2 = nums2
        l1_len = len(sorted_l1)
        l2_len = len(sorted_l2)
        concat_len = l1_len + l2_len

        l1_idx = 0
        l2_idx = 0

        # Edge case
        if concat_len == 0:
            return 0

        # We aim to only find the middle two elements (the middle element and one to the left if the array has odd length) of the merged array.
        left = None
        right = None
        # [..., left, right, ...]
        #       n/2-1 n/2

        # Iterate until the right element (inclusive).
        right_idx = concat_len // 2
        for _ in range(0, right_idx + 1):
            # The previous right element becomes the new left, since we are about to find the new right.
            left = right

            # Find the new right element.
            if l1_idx < l1_len and l2_idx < l2_len:
                # Both lists still have elements.
                if sorted_l1[l1_idx] <= sorted_l2[l2_idx]:
                    right = sorted_l1[l1_idx]
                    l1_idx += 1
                else:
                    right = sorted_l2[l2_idx]
                    l2_idx += 1
            else:
                # At most one of the lists still has elements, so append those remaining elements to result.
                if l1_idx < l1_len:
                    right = sorted_l1[l1_idx]
                    l1_idx += 1
                elif l2_idx < l2_len:
                    right = sorted_l2[l2_idx]
                    l2_idx += 1
                else:
                    # Neither list has elements.
                    break

        # Calculate median given left and right.
        if concat_len % 2 == 1:
            # Odd length.
            return right
        else:
            # Even length.
            return (left + right) / 2
