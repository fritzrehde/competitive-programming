#!/usr/bin/env python3

# Encode And Decode Strings
#
# https://leetcode.com/problems/encode-and-decode-strings/
#
# Design an algorithm to encode a list of strings to a single string. The
# encoded string is then decoded back to the original list of strings.
#
# Please implement encode and decode.


from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        (encode, decode) = algo()

        def decode_encode(strings: List[str]):
            assert decode(encode(strings)) == strings

        decode_encode(["neet", "code", "love", "you"])

        decode_encode(["we", "say", ":", "yes"])

        decode_encode(["w##e", "sa###y", ":", "yes"])

        decode_encode(["w##e", "sa###y", ":##", "#yes"])

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.length_prefix_encoding]:
        test_algo(algo)


class Solution:
    def naive(self):
        """
        Approach:  Find unique separator.
        Idea:      Find a unique separator (one that does not occur in any of the strings), and use that to join and split.
        Time:      O(?): ?
        Space:     O(?): ?
        Leetcode:  ? ms runtime, ? MB memory
        """

        import itertools
        import re

        # NOTE: This approach does NOT work: if the list contains ["...#", "#..."], splitting on ("#" * i) will greedily split on the first occurring ("#" * i), which will include part of the strings.

        def unique_separator(strs: List[str]) -> str:
            for i in itertools.count(1):
                separator = "#" * i
                if all(separator not in s for s in strs):
                    return separator

            raise Exception("unreachable: we will find a suitable separator eventually")

        def encode(strs: List[str]) -> str:
            separator = unique_separator(strs)
            return f"{separator}," + separator.join(strs)

        def decode(s: str) -> List[str]:
            if (m := re.search(r'^(#+),(.*)$', s)):
                separator = m.group(1)
                s = m.group(2)
            else:
                raise Exception("unreachable: we encoded the separator at the beginning of string in encode")

            return s.split(separator)

        return (encode, decode)

    def length_prefix_encoding(self):
        """
        Approach:  Length prefix encoding.
        Idea:      We can uniquely identify every segment of the encoded string by storing the its length followed by some non-digit (e.g. "#") as a prefix.
        Time:      O(n): Both when encoding and decoding, we "visit" (O(1)) every character once.
        Space:     O(1): No additional memory is used.
        Leetcode:  ? ms runtime, ? MB memory
        """

        import re

        # En-/decoding strategy: convert [A, B, C] to "len(A)#Alen(B)#Blen(C)#C"

        def encode(strs: List[str]) -> str:
            return "".join((f"{len(s)}#{s}" for s in strs))

        def decode(s: str) -> List[str]:
            def segments():
                header_start = 0
                n = len(s)
                while header_start < n:
                    if (m := re.search(r'^([0-9]+)#', s[header_start:])):
                        segment_len_digits = m.group(1)
                        segment_len = int(segment_len_digits)
                        header_len = len(segment_len_digits) + len("#")

                        segment_start = header_start + header_len
                        segment_end = segment_start + segment_len
                        segment = s[segment_start:segment_end]
                        yield segment

                        header_start = segment_end
                    else:
                        raise Exception("unreachable: segment length was encoded as prefix")

            return list(segments())

        return (encode, decode)
