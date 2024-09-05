#!/usr/bin/env python3

# Walking Robot Simulation
#
# https://leetcode.com/problems/walking-robot-simulation
#
# A robot on an infinite XY-plane starts at point (0, 0) facing north. The robot
# can receive a sequence of these three possible types of commands:
#
# -2: Turn left 90 degrees.
# -1: Turn right 90 degrees.
# 1 <= k <= 9: Move forward k units, one unit at a time.
#
# Some of the grid squares are obstacles. The ith obstacle is at grid point
# obstacles[i] = (xi, yi). If the robot runs into an obstacle, then it will
# instead stay in its current location and move on to the next command.
# Return the maximum Euclidean distance that the robot ever gets from the origin
# squared (i.e. if the distance is 5, return 25).
# Note:
#
# North means +Y direction.
# East means +X direction.
# South means -Y direction.
# West means -X direction.
# There can be obstacle in [0,0].


from collections import defaultdict
from itertools import repeat
import pprint
from typing import List, Optional, Tuple


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(commands=[4, -1, 3], obstacles=[]) == 25
        assert algo(commands=[4, -1, 4, -2, 4], obstacles=[[2, 4]]) == 65
        assert algo(commands=[6, -1, -1, 6], obstacles=[]) == 36
        assert (
            algo(
                commands=[7, -2, -2, 7, 5],
                obstacles=[
                    [-3, 2],
                    [-2, 1],
                    [0, 1],
                    [-2, 4],
                    [-1, 0],
                    [-2, -3],
                    [0, -3],
                    [4, 4],
                    [-3, 3],
                    [2, 2],
                ],
            )
            == 4
        )
        assert (
            algo(
                commands=[2, -1, 8, -1, 6],
                obstacles=[
                    [1, 5],
                    [-5, -5],
                    [0, 4],
                    [-1, -1],
                    [4, 5],
                    [-5, -3],
                    [-2, 1],
                    [-2, -5],
                    [0, 5],
                    [0, -1],
                ],
            )
            == 80
        )

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.binary_search]:
        test_algo(algo)


class Solution:
    def brute_force(
        self, commands: List[int], obstacles: List[List[int]]
    ) -> int:
        """
        Approach:  Brute-force.
        Idea:      Implement moving by checking each field we move across for whether it is an obstacle.
        Time:      O(n * k): Given n commands, m obstacles and a distance of at most k to move, in the worst case each command is a move command with no obstacles in the way of length k. Since we don't know if there are obstacles in the way, we must check for obstacles in each field on the way.
        Space:     O(m): We convert the obstacles to a hashset.
        Leetcode:  302 ms runtime, 23.52 MB memory
        """

        obstacles_set = set((x, y) for (x, y) in obstacles)

        # TODO: store direction as [1, 4], so turning is easier to implement

        one_step_in_dir = {
            "north": (0, 1),
            "south": (0, -1),
            "east": (1, 0),
            "west": (-1, 0),
        }

        def turn_left(dir: str) -> str:
            match dir:
                case "north":
                    return "west"
                case "east":
                    return "north"
                case "south":
                    return "east"
                case "west":
                    return "south"
                case _:
                    raise Exception("unreachable")

        def turn_right(dir: str) -> str:
            match dir:
                case "north":
                    return "east"
                case "east":
                    return "south"
                case "south":
                    return "west"
                case "west":
                    return "north"
                case _:
                    raise Exception("unreachable")

        def is_obstacle(x, y) -> bool:
            return (x, y) in obstacles_set

        heading_direction = "north"
        origin_x, origin_y = 0, 0
        curr_x, curr_y = origin_x, origin_y

        def bi_range(from_incl: int, to_incl: int):
            """
            Generates a range between endpoints, figuring out in which direction
            (towards infinity or negative infinity) to iterate automatically.
            """
            if from_incl <= to_incl:
                return range(from_incl, to_incl + 1)
            else:
                return reversed(range(to_incl, from_incl + 1))

        def range_along_axis(from_x: int, from_y: int, to_x: int, to_y: int):
            """
            Generate a range from (from_x, from_y) to (to_x, to_y), given that
            the path between the start and end point is strictly on either the
            x-axis or y-axis, i.e. not a diagonal.
            """
            if from_x == to_x:
                range_len = abs(to_y - from_y) + 1
                return zip(repeat(from_x, range_len), bi_range(from_y, to_y))
            elif from_y == to_y:
                range_len = abs(to_x - from_x) + 1
                return zip(bi_range(from_x, to_x), repeat(from_y, range_len))
            else:
                raise Exception(
                    "only ranges along exactly one axis (not both) are supported"
                )

        def take_steps(steps: int) -> Tuple[int, int]:
            one_step_diff_x, one_step_diff_y = one_step_in_dir[
                heading_direction
            ]
            diff_x, diff_y = one_step_diff_x * steps, one_step_diff_y * steps

            start_x = curr_x + one_step_diff_x
            start_y = curr_y + one_step_diff_y
            end_x = curr_x + diff_x
            end_y = curr_y + diff_y

            prev_intermediate_x, prev_intermediate_y = curr_x, curr_y
            for intermediate_x, intermediate_y in range_along_axis(
                start_x, start_y, end_x, end_y
            ):
                if is_obstacle(intermediate_x, intermediate_y):
                    return (prev_intermediate_x, prev_intermediate_y)

                prev_intermediate_x = intermediate_x
                prev_intermediate_y = intermediate_y

            return (end_x, end_y)

        def all_positions():
            nonlocal curr_x, curr_y, heading_direction

            for command in commands:
                match command:
                    case -2:
                        heading_direction = turn_left(heading_direction)
                    case -1:
                        heading_direction = turn_right(heading_direction)
                    case k if 1 <= k <= 9:
                        (curr_x, curr_y) = take_steps(k)
                        yield (curr_x, curr_y)
                    case _:
                        raise Exception("unreachable")

        def euclidian_distance_squared(
            from_x: int, from_y: int, to_x: int, to_y: int
        ) -> int:
            return ((to_x - from_x) ** 2) + ((to_y - from_y) ** 2)

        def euclidian_distance_squared_from_origin(xy_tuple) -> int:
            (x, y) = xy_tuple
            return euclidian_distance_squared(
                from_x=origin_x, from_y=origin_y, to_x=x, to_y=y
            )

        return max(map(euclidian_distance_squared_from_origin, all_positions()))

    def binary_search(
        self, commands: List[int], obstacles: List[List[int]]
    ) -> int:
        """
        Approach:  Binary search.
        Idea:      Implement moving by finding the obstacles that are potentially in the way using binary search.
        Time:      O(m log(m) + n * log(m)): Given n commands, m obstacles and a distance of at most k to move, we first construct hashmaps from each x/y coord to a list of corresponding y/x coords. Then, in the worst case, we assume every path contains an obstacle in its way, so we binary search what that obstacle is (O(log m)).
        Space:     O(m): We store all x,y in hashmaps as described above.
        Leetcode:  321 ms runtime, 23.51 MB memory
        """

        obstacles_on_y_axis = defaultdict(lambda: [])
        obstacles_on_x_axis = defaultdict(lambda: [])

        for x, y in obstacles:
            obstacles_on_y_axis[x].append(y)
            obstacles_on_x_axis[y].append(x)

        for all_ys in obstacles_on_y_axis.values():
            all_ys.sort()
        for all_xs in obstacles_on_x_axis.values():
            all_xs.sort()


        def smallest_element_larger(sorted_arr: List, elem):
            n = len(sorted_arr)
            l, r = 0, n - 1
            smallest_larger = None
            while l <= r:
                m = (r + l) // 2
                if sorted_arr[m] > elem:
                    # Potential solution, but keep searching left to
                    # potentially find smaller value.
                    smallest_larger = sorted_arr[m]
                    r = m - 1
                elif sorted_arr[m] <= elem:
                    # Search right.
                    l = m + 1

            return smallest_larger

        def largest_element_smaller(sorted_arr: List, elem):
            n = len(sorted_arr)
            l, r = 0, n - 1
            largest_smaller = None
            while l <= r:
                m = (r + l) // 2
                if sorted_arr[m] < elem:
                    # Potential solution, but keep searching right to
                    # potentially find smaller value.
                    largest_smaller = sorted_arr[m]
                    l = m + 1
                elif sorted_arr[m] >= elem:
                    # Search left.
                    r = m - 1

            return largest_smaller

        def opt_map(opt, func):
            return func(opt) if opt is not None else None

        def closest_obstacle(x, y, heading_dir) -> Optional[Tuple[int, int]]:
            ys = obstacles_on_y_axis[x]
            xs = obstacles_on_x_axis[y]
            match heading_dir:
                case "north":
                    return opt_map(
                        smallest_element_larger(ys, y), lambda y_i: (x, y_i)
                    )
                case "south":
                    return opt_map(
                        largest_element_smaller(ys, y), lambda y_i: (x, y_i)
                    )
                case "east":
                    return opt_map(
                        smallest_element_larger(xs, x), lambda x_i: (x_i, y)
                    )
                case "west":
                    return opt_map(
                        largest_element_smaller(xs, x), lambda x_i: (x_i, y)
                    )
                case _:
                    raise Exception("unreachable")

        one_step_in_dir = {
            "north": (0, 1),
            "south": (0, -1),
            "east": (1, 0),
            "west": (-1, 0),
        }

        def turn_left(dir: str) -> str:
            match dir:
                case "north":
                    return "west"
                case "east":
                    return "north"
                case "south":
                    return "east"
                case "west":
                    return "south"
                case _:
                    raise Exception("unreachable")

        def turn_right(dir: str) -> str:
            match dir:
                case "north":
                    return "east"
                case "east":
                    return "south"
                case "south":
                    return "west"
                case "west":
                    return "north"
                case _:
                    raise Exception("unreachable")

        heading_direction = "north"
        origin_x, origin_y = 0, 0
        curr_x, curr_y = origin_x, origin_y

        def bi_range(from_incl: int, to_incl: int):
            """
            Generates a range between endpoints, figuring out in which direction
            (towards infinity or negative infinity) to iterate automatically.
            """
            if from_incl <= to_incl:
                return range(from_incl, to_incl + 1)
            else:
                return range(from_incl, to_incl - 1, -1)

        def take_steps(steps: int) -> Tuple[int, int]:
            one_step_diff_x, one_step_diff_y = one_step_in_dir[
                heading_direction
            ]
            diff_x, diff_y = one_step_diff_x * steps, one_step_diff_y * steps
            end_x, end_y = (curr_x + diff_x, curr_y + diff_y)
            match closest_obstacle(curr_x, curr_y, heading_direction):
                case None:
                    # There is no element in our way: can go all the way.
                    return (end_x, end_y)
                case (obstacle_x, obstacle_y):
                    if obstacle_x in bi_range(
                        curr_x, end_x
                    ) and obstacle_y in bi_range(curr_y, end_y):
                        # If the obstacle is in the way, go in its direction
                        # and stop one step in front of it.
                        return (
                            obstacle_x - one_step_diff_x,
                            obstacle_y - one_step_diff_y,
                        )
                    else:
                        # The nearest obstacle isn't in the way.
                        return (end_x, end_y)
                case _:
                    raise Exception("unreachable")

        def all_positions():
            nonlocal curr_x, curr_y, heading_direction

            for command in commands:
                match command:
                    case -2:
                        heading_direction = turn_left(heading_direction)
                    case -1:
                        heading_direction = turn_right(heading_direction)
                    case k if 1 <= k <= 9:
                        (curr_x, curr_y) = take_steps(k)
                        yield (curr_x, curr_y)
                    case _:
                        raise Exception("unreachable")

        def euclidian_distance_squared(
            from_x: int, from_y: int, to_x: int, to_y: int
        ) -> int:
            return ((to_x - from_x) ** 2) + ((to_y - from_y) ** 2)

        def euclidian_distance_squared_from_origin(xy_tuple) -> int:
            (x, y) = xy_tuple
            return euclidian_distance_squared(
                from_x=origin_x, from_y=origin_y, to_x=x, to_y=y
            )

        return max(map(euclidian_distance_squared_from_origin, all_positions()))
