#!/usr/bin/env python3

# Course Schedule Ii
#
# https://leetcode.com/problems/course-schedule-ii/
#
# There are a total of numCourses courses you have to take, labeled from 0 to
# numCourses - 1. You are given an array prerequisites where prerequisites[i] =
# [ai, bi] indicates that you must take course bi first if you want to take
# course ai.
#
# For example, the pair [0, 1], indicates that to take course 0 you have to
# first take course 1.
#
# Return the ordering of courses you should take to finish all courses. If there
# are many valid answers, return any of them. If it is impossible to finish all
# courses, return an empty array.


from collections import defaultdict, deque
from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(numCourses=2, prerequisites=[[1, 0]]) == [0, 1]

        assert algo(numCourses=4, prerequisites=[[1, 0], [2, 0], [3, 1], [3, 2]]) == [0, 1, 2, 3]

        assert algo(numCourses=1, prerequisites=[]) == [0]

        assert algo(numCourses=3, prerequisites=[[2, 0], [2, 1]]) == [0, 1, 2]

        assert algo(numCourses=3, prerequisites=[[0, 1], [0, 2], [1, 2]]) == [2, 1, 0]

        # Contains cycle.
        assert algo(numCourses=8, prerequisites=[[1, 0], [2, 6], [1, 7], [5, 1], [6, 4], [7, 0], [0, 5]]) == []

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.dfs, solution.bfs]:
        test_algo(algo)


class Solution:
    def dfs(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        """
        Approach:  DFS.
        Idea:      We iterate from the courses with no dependents (no courses depend on them) towards the courses with no dependencies, using DFS with a post-order traversal. If we see a cycle, we exit.
        Time:      O(V + E): We only visit every node/course once (O(V)) and every edge/prerequisite/dependency once (O(E)).
        Space:     O(E): We store all dependencies and dependents in separate hashmaps (O(E)).
        Leetcode:  88 ms runtime, 18.69 MB memory
        """

        def courses():
            for course in range(0, numCourses):
                yield course

        # Map each course x to all of its dependencies, i.e. all courses that x depends on/has as a prerequisite.
        dependencies = defaultdict(lambda: [])
        # Map each course x to all of its dependents, i.e. all courses that depend on x/have x as a prerequisite.
        dependents = defaultdict(lambda: [])
        for (course, prerequisite) in prerequisites:
            dependencies[course].append(prerequisite)
            dependents[prerequisite].append(course)

        visited = set()
        explore_order = []
        current_path_stack = set()

        def explore_from(node: int):
            """DFS."""
            visited.add(node)
            current_path_stack.add(node)

            for neighbour in dependencies[node]:
                if neighbour in visited:
                    # If we see a visited node in our current path again, we have encountered a cycle.
                    if neighbour in current_path_stack:
                        raise Exception("found a cycle in the graph")
                else:
                    explore_from(neighbour)

            current_path_stack.remove(node)

            # Post-order traversal: add children to order first, since they must be explored before the parent (that depends on their children).
            explore_order.append(node)

        # Try to visit all courses/nodes.
        for ending_course in courses():
            # Only explore from this course/node if we haven't yet visited it.
            if ending_course not in visited:
                # We only iterate from the end nodes, which are those courses that have no dependents (no courses depend on them).
                if len(dependents[ending_course]) == 0:
                    try:
                        explore_from(ending_course)
                    except Exception:
                        # If the dependents graph contains a cycle, we can never finish all courses.
                        return []

        if len(explore_order) != numCourses:
            # We must have skipped one connected component of the graph because it has no nodes with no dependents, which means every node in this connected component must be a cycle.
            return []

        return explore_order

    def bfs(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        """
        Approach:  Topological sorting with Kahn's algorithm (BFS).
        Idea:      We store the in_degree value (number of remaining incoming edges) for each node and continuosly decrement on visit and possibly declare a node ready once it has no remaining incoming edges.
        Time:      O(V + E): We only visit every node/course once (O(V)) and every edge/prerequisite/dependency once (O(E)).
        Space:     O(E): We store all dependencies and dependents in separate hashmaps (O(E)).
        Leetcode:  98 ms runtime, 18.48 MB memory
        """

        # Map each course x to all of its dependencies, i.e. all courses that x depends on/has as a prerequisite.
        dependencies = defaultdict(lambda: [])
        # Map each course x to all of its dependents, i.e. all courses that depend on x/have x as a prerequisite.
        dependents = defaultdict(lambda: [])
        # The number of incoming edges for each node, i.e. the number of remaining dependencies (we'll decrement once the dependency has been fulfilled).
        in_degree = {i: 0 for i in range(0, numCourses)}

        for (course, prerequisite) in prerequisites:
            dependencies[course].append(prerequisite)
            dependents[prerequisite].append(course)
            in_degree[course] += 1

        explore_order = []

        def explore_from(starting_courses):
            """BFS."""
            unvisited = deque(starting_courses)

            while unvisited:
                cur = unvisited.popleft()

                # Pre-order traversal: parent, add children to order first, since they must be explored before the parent (that depends on their children).
                explore_order.append(cur)

                for neighbour in dependents[cur]:
                    in_degree[neighbour] -= 1
                    if in_degree[neighbour] == 0:
                        unvisited.append(neighbour)

        explore_from([node for node in in_degree if in_degree[node] == 0])

        if len(explore_order) != numCourses:
            # There must have been a cycle.
            return []

        return explore_order
