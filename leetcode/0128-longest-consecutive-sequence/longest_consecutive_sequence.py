#!/usr/bin/env python3

# Longest Consecutive Sequence
#
# https://leetcode.com/problems/longest-consecutive-sequence
#
# Given an unsorted array of integers nums, return the length of the longest
# consecutive elements sequence.
# You must write an algorithm that runs in O(n) time.


from typing import Dict, List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(nums=[100, 4, 200, 1, 3, 2]) == 4
        assert algo(nums=[0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
        assert algo(nums=[9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6]) == 7
        assert algo(nums=[1, 2, 0, 1]) == 3
        assert algo(nums=[]) == 0
        assert algo(nums=[0, -1]) == 2

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [
        solution.brute_force,
        solution.brute_force_chunkby,
        solution.hashset,
        solution.hashset_optimized,
    ]:
        test_algo(algo)


class Solution:
    def brute_force(self, nums: List[int]) -> int:
        """
        Approach:  Brute-force.
        Idea:      Sort the numbers, and collect sequences, taking the longest one.
        Time:      O(n log n): Sorting takes O(n log n), and then we do one pass, keeping track of the current longest consecutive sequence (O(n)).
        Space:     O(1): No additional memory is used.
        Leetcode:  358 ms runtime, 30.82 MB memory
        """

        longest_seq_len = 0
        curr_seq_len = 0
        curr_seq_last_elem = None

        for num in sorted(nums):
            if curr_seq_last_elem is None:
                # Ensure this number is part of/starts the sequence.
                curr_seq_last_elem = num - 1

            if (curr_seq_last_elem + 1) == num:
                # Extend sequence.
                curr_seq_len += 1
            elif curr_seq_last_elem == num:
                # Ignore same element.
                pass
            else:
                # Reset current sequence.
                curr_seq_len = 1

            curr_seq_last_elem = num

            longest_seq_len = max(curr_seq_len, longest_seq_len)

        return longest_seq_len

    def brute_force_chunkby(self, nums: List[int]) -> int:
        """
        Approach:  Brute-force, but cleaner.
        Idea:      Sort the numbers, and collect sequences, taking the longest one. Use a custom chunk/group by impl that groups based on a predicate taking two consecutive elements.
        Time:      O(n log n): Sorting takes O(n log n), and then we do one pass, keeping track of the current longest consecutive sequence (O(n)).
        Space:     O(n): Every element (besides duplicates) will be copied into one of the groups.
        Leetcode:  334 ms runtime, 31.93 MB memory
        """

        def chunkby(iterable, predicate):
            """
            Returns an iterator over the slice producing non-overlapping runs of
            elements using the predicate to separate them.
            """
            it = iter(iterable)
            if (first := next(it, None)) is not None:
                curr_group = [first]
            else:
                return

            for elem in it:
                if predicate(curr_group[-1], elem):
                    curr_group.append(elem)
                else:
                    yield curr_group
                    # Create new group.
                    curr_group = [elem]

            yield curr_group

        def continues_sequence(a: int, b: int) -> bool:
            return (a + 1) == b

        duplicates_removed = set(nums)
        return max(
            map(len, chunkby(sorted(duplicates_removed), continues_sequence)),
            default=0,
        )

    def hashmap(self, nums: List[int]) -> int:
        """
        Approach:  Collect all sequences simultaneously.
        Idea:      While iterating over all unique numbers, keep track of each sequence, and provide quick lookup whether a new elements continues a sequence.
        Time:      O(n): Checking whether a number continues any sequence, continuing the sequence, and starting a new sequence all take O(1).
        Space:     O(n): Every (unique) element (besides duplicates) will be stored (copied) in one of the sequences.
        Leetcode:  ? ms runtime, ? MB memory
        """

        # TODO: improve: don't need to store entire sequence, just len.
        sequences: List[List[int]] = []
        # Map the last value in a sequence to the idx that sequence has in sequences.
        last_val_to_idx: Dict[int, int] = dict()

        unique_nums = set(nums)
        for num in unique_nums:
            predecessor_num = num - 1
            match last_val_to_idx.get(predecessor_num, None):
                case None:
                    # Start new sequence.
                    new_sequence_idx = len(sequences)
                    new_sequence = [num]

                    sequences.append(new_sequence)
                    last_val_to_idx[num] = new_sequence_idx
                case storage_idx:
                    # Continue sequence.
                    sequences[storage_idx].append(num)
                    del last_val_to_idx[predecessor_num]
                    last_val_to_idx[num] = storage_idx

        print(sequences)

        return max(map(len, sequences), default=0)

    def hashset(self, nums: List[int]) -> int:
        """
        Approach:  Collect sequences one-by-one.
        Idea:      Everytime we see an element that starts a sequence (predecessor is not in numbers), collect that sequence entirely.
        Time:      O(n): Due to fast number hashset lookup, checking if a number starts a sequence is O(1), and collecting an entire sequence of length m is O(m).
        Space:     O(n): Every (unique) element (besides duplicates) will be stored (copied) in one of the sequences.
        Leetcode:  405 ms runtime, 44.60 MB memory
        """

        from more_itertools import ilen

        nums = set(nums)

        def starts_sequence(num: int) -> bool:
            return (num - 1) not in nums

        def sequence_starting_at(start_num: int):
            num = start_num
            while num in nums:
                yield num
                num += 1

        def all_sequences():
            for x in nums:
                if starts_sequence(x):
                    # Collect the entire sequence starting at x.
                    yield sequence_starting_at(x)

        return max(map(ilen, all_sequences()), default=0)

    def hashset_optimized(self, nums: List[int]) -> int:
        """
        Approach:  Collect sequences one-by-one, but only store sequence length.
        Idea:      Everytime we see an element that starts a sequence (predecessor is not in numbers), collect that sequence entirely.
        Time:      O(n): Due to fast number hashset lookup, checking if a number starts a sequence is O(1), and collecting an entire sequence of length m is O(m).
        Space:     O(n): Every (unique) element (besides duplicates) will be stored (copied) in one of the sequences.
        Leetcode:  335 ms runtime, 31.86 MB memory
        """

        nums = set(nums)

        def starts_sequence(num: int) -> bool:
            return (num - 1) not in nums

        def len_of_sequence_starting_at(start_num: int) -> int:
            num = start_num
            while num in nums:
                num += 1
            return num - start_num

        def all_sequences():
            for x in nums:
                if starts_sequence(x):
                    # Collect the entire sequence starting at x.
                    yield len_of_sequence_starting_at(x)

        return max(all_sequences(), default=0)
