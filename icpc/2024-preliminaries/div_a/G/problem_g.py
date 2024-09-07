#!/usr/bin/env python3

# Grouping Words


from collections import defaultdict
from copy import deepcopy
import pprint
from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        def fmt(s: str):
            return "\n".join(
                sorted(
                    map(
                        lambda line: " ".join(sorted(line.split(" "))),
                        s.splitlines(),
                    )
                )
            )

        assert (
            fmt(
                algo(
                    input="""CCC A AAA
DDD DDDD BB
DD BBB D
18
BBB DDD
DDDD CCC
A DD
A D
DD DDDD
CCC DDD
BB BBB
BB DD
DDD DDDD
AAA D
D BBB
DDD D
DD DDD
DD D
AAA A
DDDD D
DD BBB
A DDDD"""
                )
            )
            == fmt(
                """Possible
CCC DDD DDDD
A AAA D
BB DD BBB"""
            )
        )

        assert (
            fmt(
                algo(
                    input="""PACIFIC NEW FIJI
PROGRAMMING ZEALAND CPLUSPLUS
PYTHON SOUTH JAVA
12
SOUTH PACIFIC
SOUTH PROGRAMMING
PROGRAMMING PACIFIC
SOUTH ZEALAND
SOUTH FIJI
NEW ZEALAND
NEW FIJI
NEW SOUTH
FIJI ZEALAND
CPLUSPLUS JAVA
CPLUSPLUS PYTHON
JAVA PYTHON"""
                )
            )
            == fmt(
                """Possible
PACIFIC PROGRAMMING SOUTH
NEW FIJI ZEALAND
CPLUSPLUS PYTHON JAVA"""
            )
        )

        assert (
            fmt(
                algo(
                    input="""A AA AAA
B BB BBB
C CC CCC
12
A AA
AA AAA
B BB
BB BBB
C CC
CC CCC
A B
AA BB
AAA BBB
A C
AA CC
AAA CCC"""
                )
            )
            == fmt("""Impossible""")
        )

    # Test all different algorithms/implementations.
    solution = Solution()
    for algo in [solution.brute_force]:
        test_algo(algo)


# The length of the sides of the grid of input words (i.e.e there are
# GRID_SIZE^2 input words).
GRID_SIZE = 3


class Solution:
    def brute_force(self, input=str) -> str:
        """
        Approach:  Brute force.
        Idea:      Try out all partitions until a valid one is found.
        Time:      O(?): There are 280 ways to partition 9 elements into 3 groups of 3 (order doesn't matter).
        Space:     O(n): Given there are n words, we store a groups hashmap of size O(n).
        """

        input_lines: List[str] = list(
            map(lambda line: line.rstrip("\n"), input.splitlines())
        )

        input_words = [
            word for line in input_lines[:GRID_SIZE] for word in line.split()
        ]

        groups = defaultdict(lambda: set())
        for a, b in map(str.split, input_lines[GRID_SIZE + 1 :]):
            groups[a].add(b)
            groups[b].add(a)

        def same_group(a, b) -> bool:
            return b in groups[a]

        def valid_group(group) -> bool:
            return all(same_group(a, b) for (a, b) in combinations(group, 2))

        def valid_partition(partition) -> bool:
            return (
                # All groups must be valid.
                all(valid_group(group) for group in partition)
            )

        def combinations(values: List, length: int):
            combination: List = []

            def dfs(start_idx: int, depth: int):
                if depth == length:
                    yield combination.copy()
                else:
                    for i in range(start_idx, len(values)):
                        combination.append(values[i])
                        yield from dfs(i + 1, depth + 1)
                        combination.pop()

            yield from dfs(0, 0)

        # TODO: why does this approach not work? (running the tests is non-deterministic, sometimes it fails, sometimes it succeeds).
        # def partitions(values: List, group_size: int):
        #     def dfs(values: Set):
        #         if len(values) == 0:
        #             yield []
        #         else:
        #             for group in combinations(list(values), group_size):
        #                 remaining_values = set(values) - set(group)
        #                 for remaining_partitions in dfs(remaining_values):
        #                     yield [group, *remaining_partitions]
        #     yield from dfs(set(values))

        def partitions(values: List, group_size: int):
            partition: List[List] = []

            def step(i: int):
                if i == len(values):
                    yield deepcopy(partition)
                else:
                    # Add values[i] to each of the existing groups.
                    for group in partition:
                        if len(group) < group_size:
                            group.append(values[i])
                            yield from step(i + 1)
                            group.pop()

                    # Add values[i] as a new group.
                    if len(partition) * group_size < len(values):
                        partition.append([values[i]])
                        yield from step(i + 1)
                        partition.pop()

            yield from step(0)

        possible_partitions = partitions(input_words, group_size=GRID_SIZE)
        if (
            partition := next(
                filter(valid_partition, possible_partitions), None
            )
        ) is not None:
            output_groups = "\n".join(" ".join(group) for group in partition)
            return f"Possible\n{output_groups}"
        else:
            return "Impossible"
