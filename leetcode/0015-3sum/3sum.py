#!/usr/bin/env python3

# 3Sum
#
# https://leetcode.com/problems/3sum/
#
# Given an integer array nums, return all the triplets [nums[i], nums[j],
# nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k]
# == 0.
#
# Notice that the solution set must not contain duplicate triplets.


from typing import Callable, Dict, List, Tuple, TypeVar


def test():
    """
    Run `pytest <this-file > `.
    """

    def test_algo(algo):
        # nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0
        # nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0
        # nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0
        # The distinct triplets are [-1,0,1] and [-1,-1,2].
        assert sorted(algo([-1, 0, 1, 2, -1, -4])) == [[-1, -1, 2], [-1, 0, 1]]

        # Only possible triplet does not sum up to 0.
        assert sorted(algo([0, 1, 1])) == []

        # Only possible triplet does sum up to 0.
        assert sorted(algo([0, 0, 0])) == [[0, 0, 0]]

        assert sorted(algo([1, 1, -2])) == [[-2, 1, 1]]

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.store_num_indices_hashmap, solution.two_pointer]:
        test_algo(algo)


class Solution:
    def brute_force(self, nums: List[int]) -> List[List[int]]:
        """
        Approach:  Brute-force.
        Idea:      Try all possible triplets, and collect them if their sum is zero.
        Time:      O(n^3): There are (n choose 3) ways to pick 3 indices from n possible indices given that we disregard the order of the indices. (n choose 3) = O(n^3), and for each triplet, we check if its sum is zero and we potentially insert into the hashset, which is all in O(1).
        Space:     O(1): We use no additional space besides the output list of lists.
        Leetcode:  Time Limit Exceeded
        """

        # The target value that three distinct elements should sum up to.
        target = 0

        triplets = set()

        n = len(nums)
        for i in range(0, n):
            for j in range(i+1, n):
                for k in range(j+1, n):
                    three_sum = nums[i] + nums[j] + nums[k]
                    if three_sum == target:
                        # Duplicate triplets will be ignored due to sorting before inserting into hashset.
                        triplets.add(
                            tuple(sorted([nums[i], nums[j], nums[k]])))

        # Convert hashset of tuples to list of lists.
        return [list(triplet) for triplet in triplets]

    def store_num_indices_hashmap(self, nums: List[int]) -> List[List[int]]:
        """
        Approach:  Store number to index hashmap.
        Idea:      Construct a hashmap that maps a number to the list of indices at which that number occurs in the list. This way, we can iterate over all possible pairs of indices, and efficiently lookup the third remaining number such that their sum is equal to the target value 0.
        Time:      O(3n^2) = O(n^2): There are (n choose 2) = O(n^2) ways to pick 2 indices from n possible indices given that we disregard the order of the indices. For each pair, we extract all indices of the third number from our hashmap. We will check at most the first 3 of these indices, as the first and second indices might be the already used indices i or j, but in the worst-case, the third index would then be a unique index we can use. Therefore, finding the third index is O(3).
        Space:     O(n): The hashmap of numbers to indices will have exactly n elements.
        Leetcode:  Time Limit Exceeded
        """

        # The target value that three distinct elements should sum up to.
        target = 0

        V = TypeVar('V')
        K = TypeVar('K')

        def and_modify_or_insert(map: Dict[K, V], key: K, modify: Callable[[V], None], insert: V):
            """
            Provide in-place mutable access to an entry if it is occupied, otherwise insert a new value.
            A Python implementation of Rust's `Entry::and_modify` and `Entry::or_insert` methods.
            """
            # NOTE: This implementation is not as performant as Rust's Entry API, as we need to hash twice here, once to check if the key is in the map, and once to actually insert.
            if key in map:
                # Mutate the existing value according to provided function.
                modify(map[key])
            else:
                # Insert new value at empty entry.
                map[key] = insert

        # Map each number to all indices in array (since a number may appear multiple times).
        nums_indices = dict()
        for i, num in enumerate(nums):
            and_modify_or_insert(nums_indices, num, lambda v: v.append(i), [i])

        triplets = set()

        n = len(nums)
        for i in range(0, n):
            for j in range(i+1, n):
                # target = nums[i] + nums[j] + nums[k]
                nums_k = target - nums[i] - nums[j]
                # Avoid iterating over all k's by looking up nums_k in hashmap.
                if (all_ks := nums_indices.get(nums_k)) is not None:
                    # There might be multiple indices k where nums[k] is equal to the desired nums_k. Therefore, if there is any k in all ks that is unequal to both i and j, we have found a suitable third index k.
                    for k in all_ks:
                        if k != i and k != j:
                            # Duplicate triplets will be ignored due to sorting before inserting into hashset.
                            triplets.add(
                                tuple(sorted([nums[i], nums[j], nums[k]])))
                            break

        # Convert hashset of tuples to list of lists.
        return [list(triplet) for triplet in triplets]

    # INCORRECT: Unfortunately, this solution cannot handle cases where two individual elements do not sum to the third where the triplet would be part of the 3sum, e.g. [1, 1, -2].
    def store_two_sum(self, nums: List[int]) -> List[List[int]]:
        """
        Approach:  Store two sum for each number.
        Idea:      Construct a hashmap that maps a number in the list to the pairs of indices of which the elements sum up to that number. This way, we can iterate over all possible first indices of a 3sum, and efficiently look-up if we have two other elements that add up to the target 0 when summed with the first element.
        Time:      O(n^2): First, we construct the hashmap that maps each number to the index it appears in the list (O(n)). We then use this data structure to efficiently implement the two sum algorithm in O(n). We calculate the two sum for every element in the list (O(n^2) in total). Then, we iterate over all n possible first indices i, and check if each two sum complement indices j and k are valid. Instead of only collecting the first pair of j and k that form a 3sum together with i, we collect all.
        Space:     O(n^2): The hashmap of numbers to indices will have exactly n elements, and the hashmap of 2sum to indices has at most n^2 elements.
        Leetcode:  Wrong Answer
        """

        # The target value that three distinct elements should sum up to.
        target = 0

        V = TypeVar('V')
        K = TypeVar('K')

        def and_modify_or_insert(map: Dict[K, V], key: K, modify: Callable[[V], None], insert: V):
            """
            Provide in-place mutable access to an entry if it is occupied, otherwise insert a new value.
            A Python implementation of Rust's `Entry::and_modify` and `Entry::or_insert` methods.
            """
            # NOTE: This implementation is not as performant as Rust's Entry API, as we need to hash twice here, once to check if the key is in the map, and once to actually insert.
            if key in map:
                # Mutate the existing value according to provided function.
                modify(map[key])
            else:
                # Insert new value at empty entry.
                map[key] = insert

        # Map each number to all indices in array (since a number may appear multiple times).
        nums_indices = dict()
        for i, num in enumerate(nums):
            and_modify_or_insert(nums_indices, num, lambda v: v.append(i), [i])

        def two_sum(nums: List[int], target: int) -> List[Tuple[int, int]]:
            """
            Return all unique pairs of indices of which the elements sum up to the target value.
            """
            pairs = set()
            for i, nums_i in enumerate(nums):
                # target = nums[i] + nums[j]
                nums_j = target - nums_i
                if (all_js := nums_indices.get(nums_j)) is not None:
                    # There might be multiple indices j where nums[j] is equal to the desired nums_j. Therefore, if there is any j in all ks that is unequal to i, we have found a suitable second index k.
                    for j in all_js:
                        if j != i:
                            pairs.add(tuple(sorted([i, j])))

            return list(pairs)

        # Map each number to all pairs of indices of which the elements sum up to that number.
        two_sum_indices = dict((num, two_sum(nums, num)) for num in set(nums))

        triplets = set()

        n = len(nums)
        for i, nums_i in enumerate(nums):
            # target = nums[i] + nums[j] + nums[k]
            nums_j_plus_nums_k = target - nums_i

            if (all_jks := two_sum_indices.get(nums_j_plus_nums_k)) is not None:
                # There might be multiple pairs of indices j,k where nums[j] + nums[k] is equal to the desired nums_i. Therefore, if there is any pair j,k in all j,k's where both j and k are unequal to i, we have found suitable second and third indices j and k.
                for k, j in all_jks:
                    if j != i and k != i:
                        triplets.add(
                            tuple(sorted([nums[i], nums[j], nums[k]])))

        # Convert hashset of tuples to list of lists.
        return [list(triplet) for triplet in triplets]

    def two_pointer(self, nums: List[int]) -> List[List[int]]:
        """
        Approach:  Two pointer sums.
        Idea:      By sorting the list ascendingly, we are able to efficiently use a two pointer approach to find two other elements that to a certain value.
        Time:      O(n^2): First, we sort the list of n elements with merge sort, taking O(n log n). For each list element at index i (of which there are n), we can use the two pointer method to efficiently search for the second and third elements that make up a valid triplet in O(n).
        Space:     O(1): We store nothing besides the output list of lists.
        Leetcode:  1176 ms runtime, 22.06 MB memory
        """

        # The target value that three distinct elements should sum up to.
        target = 0

        # Sorting the numbers ascendingly facilitates a two pointer O(n) search for two elements that sum to some value.
        nums.sort()

        triplets = set()

        n = len(nums)
        # The last possible triplet is (nums[n-3], nums[n-2], nums[n-1]).
        for i in range(0, n-2):
            # target = nums[i] + nums[l] + nums[r]
            required_nums_l_plus_nums_r = target - nums[i]

            # We've already checked all possible triplets where l < i when the roles of i and l were reversed.
            l = i+1
            r = n-1

            while l < r:
                # Skip index i, since we can't include i twice in our triplet.
                if l == i:
                    l += 1
                    continue
                if r == i:
                    r -= 1
                    continue

                nums_l_plus_nums_r = nums[l] + nums[r]

                if nums_l_plus_nums_r < required_nums_l_plus_nums_r:
                    # The only way to make nums[l] + nums[r] larger without overshooting is to try nums[l+1] (relies on nums being sorted).
                    l += 1
                elif nums_l_plus_nums_r > required_nums_l_plus_nums_r:
                    # The only way to make nums[l] + nums[r] smaller without undershooting is to try nums[r-1] (relies on nums being )
                    r -= 1
                elif nums_l_plus_nums_r == required_nums_l_plus_nums_r:
                    triplets.add(tuple(sorted([nums[i], nums[l], nums[r]])))

                    # Skip all equal elements, since we don't care about duplicates.
                    nums_l = nums[l]
                    nums_r = nums[r]
                    while (l < r and nums[l] == nums_l):
                        l += 1
                    while (l < r and nums[r] == nums_r):
                        r -= 1

        # Convert hashset of tuples to list of lists.
        return [list(triplet) for triplet in triplets]
