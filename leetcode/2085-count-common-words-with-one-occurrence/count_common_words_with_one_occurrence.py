#!/usr/bin/env python3

# Count Common Words With One Occurrence
#
# https://leetcode.com/problems/count-common-words-with-one-occurrence/
#
# Given two string arrays words1 and words2, return the number of strings that
# appear exactly once in each of the two arrays.


from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        # indices in words1: [0, 5]
        assert algo(["once both", "once here", "twice", "twice", "three", "1"], ["1", "another here", "three", "once both", "three"]) == 2

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.hashmap, solution.hashmap_cleaner]:
        test_algo(algo)


class Solution:
    def hashmap(self, words1: List[str], words2: List[str]) -> int:
        """
        Approach:  Store occurences in hashmap.
        Idea:      Maintain a hashmap mapping strings to occurring indices to quickly be able to lookup each string in both lists.
        Time:      O(n): Building up the hashmaps takes O(n), and the final iteration aggregating the indices takes O(n).
        Space:     O(n): The hashmap take O(n) space.
        Leetcode:  69 ms runtime, 17.10 MB memory
        """

        def appearing_indices(l: List[str]) -> dict[str, List[int]]:
            """Map each string to the indices in the list it appears at."""
            map = dict()
            for (i, e) in enumerate(l):
                if not e in map:
                    map[e] = [i]
                else:
                    map[e].append(i)
            return map

        freq1 = appearing_indices(words1)
        freq2 = appearing_indices(words2)

        indices = []
        for (s, indices1) in freq1.items():
            indices2 = freq2[s] if s in freq2 else []
            if len(indices1) == len(indices2) == 1:
                indices.append(indices1[0])

        return len(indices)

    def hashmap_cleaner(self, words1: List[str], words2: List[str]) -> int:
        """
        Approach:  Store only strings with single occurence in hashmap.
        Idea:      Maintain a hashmap mapping strings to their single occurring index to quickly be able to lookup each string in both lists.
        Time:      O(n): Building up the hashmaps takes O(n), and the final iteration aggregating the indices takes O(n).
        Space:     O(n): The hashmap take O(n) space.
        Leetcode:  68 ms runtime, 17.20 MB memory
        """

        def appearing_indices(l: List[str]) -> dict[str, int]:
            """Map each string that only appears once in the string to the index it appears at."""
            map = dict()
            for (i, s) in enumerate(l):
                if not s in map:
                    map[s] = [i]
                else:
                    map[s].append(i)

            # Only keep strings with exactly one occurence.
            reduced = dict()
            for (s, indices) in map.items():
                if len(indices) == 1:
                    reduced[s] = indices[0]

            return reduced

        freq1 = appearing_indices(words1)
        freq2 = appearing_indices(words2)

        indices = []
        for (s, index1) in freq1.items():
            if s in freq2:
                indices.append(index1)

        return len(indices)
