#!/usr/bin/env python3

# String Compression
#
# https://leetcode.com/problems/string-compression
#
# Given an array of characters chars, compress it using the following algorithm:
# Begin with an empty string s. For each group of consecutive repeating
# characters in chars:
#
# If the group's length is 1, append the character to s.
# Otherwise, append the character followed by the group's length.
#
# The compressed string s should not be returned separately, but instead, be
# stored in the input character array chars. Note that group lengths that are 10
# or longer will be split into multiple characters in chars.
# After you are done modifying the input array, return the new length of the
# array.
# You must write an algorithm that uses only constant extra space.


from typing import Iterator, List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        chars = ["a", "a", "b", "b", "c", "c", "c"]
        assert algo(chars) == 6
        assert chars == ["a", "2", "b", "2", "c", "3"]

        chars = ["a"]
        assert algo(chars) == 1
        assert chars == ["a"]

        chars = [
            "a",
            "b",
            "b",
            "b",
            "b",
            "b",
            "b",
            "b",
            "b",
            "b",
            "b",
            "b",
            "b",
        ]
        assert algo(chars) == 4
        assert chars == ["a", "b", "1", "2"]

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [
        solution.out_of_place,
        solution.in_place,
        solution.in_place_optimized,
    ]:
        test_algo(algo)


class Solution:
    def out_of_place(self, chars: List[str]) -> int:
        """
        Approach:  Out-of-place array manipulation.
        Idea:      Collect the compressed data into a new array, and replace input array with compressed array.
        Time:      O(n): Iterate of each of the input chars, and add to compressed array (O(1)).
        Space:     O(n): The out-of-place compressed array has at most length n.
        Leetcode:  66 ms runtime, 16.76 MB memory
        """

        def digits(num: int) -> List[str]:
            return list(str(num))

        compressed = []

        def append_to_compressed(extended: List[str]):
            compressed.extend(extended)

        def finalize_compression():
            # Keep only the compressed chars.
            chars[:] = compressed

        n = len(chars)
        i = 0
        while i < n:
            curr_char = chars[i]
            curr_char_count = 0
            while i < n and chars[i] == curr_char:
                curr_char_count += 1
                i += 1

            append_to_compressed(
                [curr_char]
                + (digits(curr_char_count) if curr_char_count > 1 else [])
            )

        finalize_compression()
        return len(compressed)

    def in_place(self, chars: List[str]) -> int:
        """
        Approach:  In-place array manipulation.
        Idea:      Overwrite input chars array with compressed chars, which works only because the compressed data will always have smaller or equal size compared to the uncompressed data.
        Time:      O(n): Iterate of each of the input chars, and add to compressed array (O(1)).
        Space:     O(1): We use no additional memory, since the input array is manipulated in-place.
        Leetcode:  43 ms runtime, 16.69 MB memory
        """

        def digits(num: int) -> List[str]:
            return list(str(num))

        # The index pointing to the next place to put a compressed char will
        # always be smaller than the index pointing to the next place to read an
        # uncompressed char from, as the compression *always* results in a
        # smaller or equal output size.
        compressed_idx = 0

        def append_to_compressed(extended: List[str]):
            nonlocal compressed_idx
            for e in extended:
                chars[compressed_idx] = e
                compressed_idx += 1

        def finalize_compression():
            # Keep only the compressed chars.
            chars[:] = chars[:compressed_idx]

        n = len(chars)
        uncompressed_idx = 0
        while uncompressed_idx < n:
            curr_char = chars[uncompressed_idx]
            curr_char_count = 0
            while uncompressed_idx < n and chars[uncompressed_idx] == curr_char:
                curr_char_count += 1
                uncompressed_idx += 1

            append_to_compressed(
                [curr_char]
                + (digits(curr_char_count) if curr_char_count > 1 else [])
            )

        finalize_compression()
        return len(chars)

    def in_place_optimized(self, chars: List[str]) -> int:
        """
        Approach:  In-place array manipulation, with even less allocation.
        Idea:      Overwrite input chars array with compressed chars, which works only because the compressed data will always have smaller or equal size compared to the uncompressed data.
        Time:      O(n): Iterate of each of the input chars, and add to compressed array (O(1)).
        Space:     O(1): We use no additional memory, since the input array is manipulated in-place.
        Leetcode:  45 ms runtime, 16.67 MB memory
        """

        import itertools

        def digits(num: int) -> Iterator[str]:
            return iter(str(num))

        # The index pointing to the next place to put a compressed char will
        # always be smaller than the index pointing to the next place to read an
        # uncompressed char from, as the compression *always* results in a
        # smaller or equal output size.
        compressed_idx = 0

        def append_to_compressed(elements):
            nonlocal compressed_idx
            for e in elements:
                chars[compressed_idx] = e
                compressed_idx += 1

        def finalize_compression():
            # Keep only the compressed chars.
            chars[:] = chars[:compressed_idx]

        n = len(chars)
        uncompressed_idx = 0
        while uncompressed_idx < n:
            curr_char = chars[uncompressed_idx]
            curr_char_count = 0
            while uncompressed_idx < n and chars[uncompressed_idx] == curr_char:
                curr_char_count += 1
                uncompressed_idx += 1

            append_to_compressed(
                itertools.chain(
                    curr_char,
                    (
                        digits(curr_char_count)
                        if curr_char_count > 1
                        else iter(())
                    ),
                )
            )

        finalize_compression()
        return len(chars)
