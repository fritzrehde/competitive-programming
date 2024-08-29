#!/usr/bin/env python3

# Long Distance Calling
#
# https://sppcontests.org/problem_pdfs/2023/prelimsB.pdf


import pprint


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert (
            algo(
                input="""19 67
10 45
12 30
23 11 30"""
            )
            == "26 13 30"
        )

        assert (
            algo(
                input="""23 61
12 30
15 56
21 15 0"""
            )
            == "22 8 7"
        )

        assert (
            algo(
                input="""5 10
13 10
0 9
2 1 0"""
            )
            == "43 0 9"
        )

    # Test all different algorithms/implementations.
    solution = Solution()
    for algo in [solution.brute_force]:
        test_algo(algo)


class Solution:
    def brute_force(self, input=str) -> str:
        """
        Approach:  Brute force.
        Idea:      Basically just transforming math equations.
        Time:      O(1): No loops.
        Space:     O(1): No additional memory is used.
        """

        input_lines_it = iter(input.splitlines())

        (X, Y) = map(int, next(input_lines_it).split())
        (H_E, M_E) = map(int, next(input_lines_it).split())
        (H_T, M_T) = map(int, next(input_lines_it).split())
        (d_E, h_E, m_E) = map(int, next(input_lines_it).split())

        # Goal: find d_T, h_T, m_T

        # These values correspond to each other.
        first_contact_earth = (60 * H_E) + M_E
        first_contact_tatooine = (Y * H_T) + M_T

        minutes_per_day_earth = 24 * 60
        minutes_per_hour_earth = 60
        minutes_per_day_tatooine = X * Y
        minutes_per_hour_tatooine = Y

        # Total minutes on both planets since first contact.
        total_minutes_earth_since_day_0 = (
            minutes_per_day_earth * d_E + minutes_per_hour_earth * h_E + m_E
        )
        total_minutes_since_contact = (
            total_minutes_earth_since_day_0 - first_contact_earth
        )
        total_minutes_tatooine_since_day_0 = (
            total_minutes_since_contact + first_contact_tatooine
        )

        d_T, remaining_minutes = divmod(
            total_minutes_tatooine_since_day_0, minutes_per_day_tatooine
        )
        h_T, remaining_minutes = divmod(
            remaining_minutes, minutes_per_hour_tatooine
        )
        m_T = remaining_minutes

        return f"{d_T} {h_T} {m_T}"
