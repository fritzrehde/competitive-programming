#!/usr/bin/env python3

# Design HashMap
#
# https://leetcode.com/problems/design-hashmap
#
# Design a HashMap without using any built-in hash table libraries.
# Implement the MyHashMap class:
#
# MyHashMap() initializes the object with an empty map.
# void put(int key, int value) inserts a (key, value) pair into the HashMap. If
# the key already exists in the map, update the corresponding value.
# int get(int key) returns the value to which the specified key is mapped, or -1
# if this map contains no mapping for the key.
# void remove(key) removes the key and its corresponding value if the map
# contains the mapping for the key.


from itertools import chain
from typing import Optional, Tuple


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        hashmap = algo()

        hashmap.put(1, 1)
        # The map is now [[1,1]]
        hashmap.put(2, 2)
        # The map is now [[1,1], [2,2]]
        assert hashmap.get(1) == 1
        # return 1, The map is now [[1,1], [2,2]]
        assert hashmap.get(3) == -1
        # return -1 (i.e., not found), The map is now [[1,1], [2,2]]
        hashmap.put(2, 1)
        # The map is now [[1,1], [2,1]] (i.e., update the existing value)
        assert hashmap.get(2) == 1
        # return 1, The map is now [[1,1], [2,1]]
        hashmap.remove(2)
        # remove the mapping for 2, The map is now [[1,1]]
        assert hashmap.get(2) == -1
        # return -1 (i.e., not found), The map is now [[1,1]]

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [
        solution.list_of_tuples,
        solution.table,
        solution.hashing_by_chaining,
        solution.hashing_by_linear_probing,
        solution.double_hashing,
    ]:
        test_algo(algo)


class Solution:
    def list_of_tuples(self):
        """
        Approach:  Brute-force.
        Idea:      ?
        Time:      O(?): ?
        Space:     O(?): ?
        Leetcode:  1921 ms runtime, 19.78 MB memory
        """

        class MyHashMap:
            def __init__(self):
                # Store a list of (key, value) tuples.
                self.l = []

            def find_key_idx(self, key: int) -> Optional[int]:
                # O(n)
                # Search for existing key.
                for i, (k, _v) in enumerate(self.l):
                    if key == k:
                        return i
                return None

            def put(self, key: int, value: int) -> None:
                # O(n)
                if (i := self.find_key_idx(key)) is not None:
                    # Update value of existing key.
                    self.l[i] = (key, value)
                else:
                    # Insert new key, value pair.
                    self.l.append((key, value))

            def get(self, key: int) -> int:
                # O(n)
                if (i := self.find_key_idx(key)) is not None:
                    (_k, v) = self.l[i]
                    return v
                else:
                    return -1

            def remove(self, key: int) -> None:
                # O(n)
                if (i := self.find_key_idx(key)) is not None:
                    # O(1)
                    # Swap remove.
                    self.l[i], self.l[-1] = self.l[-1], self.l[i]
                    self.l.pop()

        return MyHashMap()

    def table(self):
        """
        Approach:  Brute-force.
        Idea:      ?
        Time:      O(?): ?
        Space:     O(?): ?
        Leetcode:  764 ms runtime, 42.42 MB memory
        """

        class MyHashMap:
            def __init__(self):
                # The key is the index into a giant fixed-size table with space
                # for every key.
                MAX_KEY = 10**6 + 1
                self.table = [None for _ in range(MAX_KEY)]

            def put(self, key: int, value: int) -> None:
                # O(1)
                self.table[key] = value

            def get(self, key: int) -> int:
                # O(1)
                if self.table[key] is not None:
                    return self.table[key]
                else:
                    return -1

            def remove(self, key: int) -> None:
                # O(1)
                self.table[key] = None

        return MyHashMap()

    def hashing_by_chaining(self):
        """
        Approach:  Brute-force.
        Idea:      ?
        Time:      O(?): ?
        Space:     O(?): ?
        Leetcode:  186 ms runtime, 19.96 MB memory
        """

        class MyHashMap:
            def __init__(self):
                # The key is the index pointing to a bucket in a fixed-sized hashtable.
                self.size = 2048
                self.table = [[] for _ in range(self.size)]

            def hash(self, x: int) -> int:
                return x % self.size

            def find_key_idx(self, key: int) -> Tuple[int, Optional[int]]:
                # Average O(1)
                # Search for existing key.
                h = self.hash(key)
                for i, (k, _v) in enumerate(self.table[h]):
                    if key == k:
                        return (h, i)
                return (h, None)

            def put(self, key: int, value: int) -> None:
                # Average O(1)
                (h, i_opt) = self.find_key_idx(key)
                if (i := i_opt) is not None:
                    # Update value of existing key.
                    self.table[h][i] = (key, value)
                else:
                    # Insert new key, value pair.
                    self.table[h].append((key, value))

            def get(self, key: int) -> int:
                # Average O(1)
                (h, i_opt) = self.find_key_idx(key)
                if (i := i_opt) is not None:
                    (_k, v) = self.table[h][i]
                    return v
                else:
                    return -1

            def remove(self, key: int) -> None:
                # Average O(1)
                (h, i_opt) = self.find_key_idx(key)
                if (i := i_opt) is not None:
                    # O(1)
                    # Swap remove.
                    self.table[h][i], self.table[h][-1] = (
                        self.table[h][-1],
                        self.table[h][i],
                    )
                    self.table[h].pop()

        return MyHashMap()

    def hashing_by_linear_probing(self):
        """
        Approach:  Brute-force.
        Idea:      ?
        Time:      O(?): ?
        Space:     O(?): ?
        Leetcode:  1147 ms runtime, 19.97 MB memory
        """

        class MyHashMap:
            def __init__(self):
                # The key is the index pointing to a bucket in a fixed-sized hashtable.
                MAX_SIZE = 10**4 + 1
                self.size = MAX_SIZE
                self.table = [None for _ in range(self.size)]

            def hash(self, x: int) -> int:
                return x % self.size

            def find_key_idx(self, key: int) -> Tuple[bool, int]:
                # Average O(1)
                # Search for existing key, and return (true, i) if the k,v pair
                # exists at idx i, or (false, i) where i is the idx at which
                # the k,v would be inserted.

                h = self.hash(key)

                # If (k,v) is not stored at table[h], it will be stored at some
                # table[h+k] (including wrap around). Check them one by one.
                # We are guaranteed to find a free spot.
                for i in chain(range(h, self.size), range(0, h)):
                    if (kv := self.table[i]) is not None:
                        (k, _v) = kv
                        if key == k:
                            return (True, i)
                    else:
                        return (False, i)

                raise Exception("there must be a free space for the new key")

            def put(self, key: int, value: int) -> None:
                # Average O(1)
                (_key_exists, i) = self.find_key_idx(key)
                self.table[i] = (key, value)

            def get(self, key: int) -> int:
                # Average O(1)
                (key_exists, i) = self.find_key_idx(key)
                if key_exists:
                    (_k, v) = self.table[i]
                    return v
                else:
                    return -1

            def remove(self, key: int) -> None:
                # Average O(1)
                (_key_exists, i) = self.find_key_idx(key)
                # NOTE: We're not allowed to "free" this slot (e.g. reset it to
                # None), because that would cause future probing walks to fail
                # to find its correct hashed key (we would find a free slot
                # before the actual hashed key). We call this slot a "tombstone".
                self.table[i] = (-1, -1)

        return MyHashMap()

    def double_hashing(self):
        """
        Approach:  Brute-force.
        Idea:      ?
        Time:      O(?): ?
        Space:     O(?): ?
        Leetcode:  3865 ms runtime, 20.08 MB memory
        """

        class MyHashMap:
            def __init__(self):
                # The key is the index pointing to a bucket in a fixed-sized hashtable.
                MAX_SIZE = 10**4 + 1
                self.size = MAX_SIZE
                self.table = [None for _ in range(self.size)]

            def h1(self, x: int) -> int:
                return x % self.size

            def h2(self, x: int) -> int:
                return 2 * x + 1

            def find_key_idx(self, key: int) -> Tuple[bool, int]:
                # Average O(1)
                # Search for existing key, and return (true, i) if the k,v pair
                # exists at idx i, or (false, i) where i is the idx at which
                # the k,v would be inserted.

                # If (k,v) is not stored at table[(h1 + j*h2)%n], continue
                # searching at table[(h1 + (j+1)*h2)%n]. Check them one by one.
                # We are guaranteed to find a free spot.
                for j in range(0, self.size):
                    i = (self.h1(key) + j * self.h2(key)) % self.size
                    if (kv := self.table[i]) is not None:
                        (k, _v) = kv
                        if key == k:
                            return (True, i)
                    else:
                        return (False, i)

                raise Exception("there must be a free space for the new key")

            def put(self, key: int, value: int) -> None:
                # Average O(1)
                (_key_exists, i) = self.find_key_idx(key)
                self.table[i] = (key, value)

            def get(self, key: int) -> int:
                # Average O(1)
                (key_exists, i) = self.find_key_idx(key)
                if key_exists:
                    (_k, v) = self.table[i]
                    return v
                else:
                    return -1

            def remove(self, key: int) -> None:
                # Average O(1)
                (_key_exists, i) = self.find_key_idx(key)
                # NOTE: We're not allowed to "free" this slot (e.g. reset it to
                # None), because that would cause future probing walks to fail
                # to find its correct hashed key (we would find a free slot
                # before the actual hashed key). We call this slot a "tombstone".
                self.table[i] = (-1, -1)

        return MyHashMap()
