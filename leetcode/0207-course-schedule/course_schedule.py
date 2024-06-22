#!/usr/bin/env python3

# Course Schedule
#
# https://leetcode.com/problems/course-schedule/
#
# There are a total of numCourses courses you have to take, labeled from 0 to
# numCourses - 1. You are given an array prerequisites where prerequisites[i] =
# [ai, bi] indicates that you must take course bi first if you want to take
# course ai.
#
# For example, the pair [0, 1], indicates that to take course 0 you have to
# first take course 1.
#
# Return true if you can finish all courses. Otherwise, return false.


from collections import defaultdict
from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(numCourses=2, prerequisites=[[1, 0]]) == True

        assert algo(numCourses=2, prerequisites=[[1, 0], [0, 1]]) == False

        # None of the courses have depend on other courses.
        assert algo(numCourses=42, prerequisites=[]) == True

        # Course 2 depends on course 0 "twice", once directly and once transitively through course 1. This is fine.
        assert algo(numCourses=3, prerequisites=[[1, 0], [2, 0], [2, 1]]) == True

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.dfs, solution.dfs_optimized]:
        test_algo(algo)


class Solution:
    def dfs(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        """
        Approach:  DFS.
        Idea:      Try every course as "starting course from which we visit other courses that have it as prerequisite", which will eventually visit all courses. If we see a cycle at any point, it's impossible to finish all courses.
        Time:      O(V + E): We only visit every node/course once (O(V)) and every edge/prerequisite/dependency once (O(E)).
        Space:     O(V + E): We store all courses in a hashset (O(V)) and all dependencies in a hashmap (O(E)).
        Leetcode:  97 ms runtime, 18.87 MB memory
        """

        # It is possible to finish all courses, if **all** of the following hold:
        # - There are no cycles in the dependency graph.

        courses = set()
        # Map each course x to all of its dependents, i.e. all courses that depend on x/have x as a prerequisite.
        dependents = defaultdict(lambda: [])

        for (course, prerequisite) in prerequisites:
            dependents[prerequisite].append(course)
            courses.add(course)
            courses.add(prerequisite)

        visited = set()
        current_path_stack = set()

        def explore_from(node: int):
            """DFS."""
            visited.add(node)
            current_path_stack.add(node)

            for neighbour in dependents[node]:
                if neighbour in visited:
                    # If we see a visited node in our current path again, we have encountered a cycle.
                    if neighbour in current_path_stack:
                        raise Exception("found a cycle in the graph")
                else:
                    explore_from(neighbour)

            current_path_stack.remove(node)

        # Try to visit all courses/nodes.
        for starting_course in courses:
            # Only explore from this course/node if we haven't yet visited it.
            if starting_course not in visited:
                try:
                    explore_from(starting_course)
                except Exception:
                    # If the dependents graph contains a cycle, we can never finish all courses.
                    return False

        # We will always have visited all courses at this point, since we tried each node as starting node and encountered no cycles.
        return True

    def dfs_optimized(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        """
        Approach:  DFS.
        Idea:      Try every course as "starting course from which we visit other courses that have it as prerequisite", which will eventually visit all courses. If we see a cycle at any point, it's impossible to finish all courses.
        Time:      O(V + E): We only visit every node/course once (O(V)) and every edge/prerequisite/dependency once (O(E)).
        Space:     O(E): We store all dependencies in a hashmap (O(E)).
        Leetcode:  96 ms runtime, 18.20 MB memory
        """

        # It is possible to finish all courses, if **all** of the following hold:
        # - There are no cycles in the dependency graph.

        def courses():
            for course in range(0, numCourses):
                yield course

        # Map each course x to all of its dependents, i.e. all courses that depend on x/have x as a prerequisite.
        dependents = defaultdict(lambda: [])
        for (course, prerequisite) in prerequisites:
            dependents[prerequisite].append(course)

        visited = set()
        current_path_stack = set()

        def explore_from(node: int):
            """DFS."""
            visited.add(node)
            current_path_stack.add(node)

            for neighbour in dependents[node]:
                if neighbour in visited:
                    # If we see a visited node in our current path again, we have encountered a cycle.
                    if neighbour in current_path_stack:
                        raise Exception("found a cycle in the graph")
                else:
                    explore_from(neighbour)

            current_path_stack.remove(node)

        # Try to visit all courses/nodes.
        for starting_course in courses():
            # Only explore from this course/node if we haven't yet visited it.
            if starting_course not in visited:
                try:
                    explore_from(starting_course)
                except Exception:
                    # If the dependents graph contains a cycle, we can never finish all courses.
                    return False

        # We will always have visited all courses at this point, since we tried each node as starting node and encountered no cycles.
        return True
