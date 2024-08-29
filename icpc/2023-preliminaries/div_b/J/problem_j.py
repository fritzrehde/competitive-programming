#!/usr/bin/env python3

# Jay, Jay’s son ja$on, and their Socks
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
                input="""6
WASHSOCK 1
WASHSOCK 9
SLEEP
WASHSOCK 1
WASHSOCK 1
WASHSOCK 6"""
            )
            == """SOCK 1 -1
SOCK 9 -1"""
        )

        assert (
            algo(
                input="""6
SLEEP
WEARSOCK 5
WEARSOCK 1
WEARSOCK 9
WASHSOCK 1
WAKE"""
            )
            == """SOCK 5 1
SOCK 9 1"""
        )

        assert (
            algo(
                input="""4
SLEEP
WEARSOCK 1
WASHSOCK 1
WAKE"""
            )
            == """"""
        )

        assert (
            algo(
                input="""3
SLEEP
WEARSOCK 1
WAKE"""
            )
            == """SOCK 1 1"""
        )

        assert (
            algo(
                input="""1
WEARSOCK 1"""
            )
            == """SOCK 1 1"""
        )

    # Test all different algorithms/implementations.
    solution = Solution()
    for algo in [solution.brute_force]:
        test_algo(algo)


class Solution:
    def brute_force(self, input=str) -> str:
        """
        Approach:  Brute force.
        Idea:      Maintain two hashmaps mapping sock id to wear score, one for while awake and one for while sleeping. Upon awaking, print those id's that have a different score from before sleeping.
        Time:      O(n): Given n events, in the worst case, our solution essentially has two O(n) passes: first, each event mutates the count of one id (O(1)). Then, each wake causes at most m updates (O(m)), where the sum of all m is n.
        Space:     O(n): Given n events, at most n different sock ids can have counts, so our hashmaps both have a max size of n.
        """

        from collections import defaultdict

        def output():
            sleeping = False

            wear_score_while_awake = defaultdict(lambda: 0)
            wear_score_during_sleep = defaultdict(lambda: 0)

            for action in input.splitlines()[1:]:
                match action.split():
                    case ["WEARSOCK", id]:
                        if sleeping:
                            wear_score_during_sleep[id] += 1
                        else:
                            wear_score_while_awake[id] += 1
                            yield f"SOCK {id} {wear_score_while_awake[id]}"

                    case ["WASHSOCK", id]:
                        if sleeping:
                            wear_score_during_sleep[id] -= 1
                        else:
                            wear_score_while_awake[id] -= 1
                            yield f"SOCK {id} {wear_score_while_awake[id]}"

                    case ["SLEEP"]:
                        sleeping = True

                    case ["WAKE"]:
                        sleeping = False

                        # Order: insertion order.
                        for (
                            id,
                            score_during_sleep,
                        ) in wear_score_during_sleep.items():
                            if score_during_sleep != wear_score_while_awake[id]:
                                wear_score_while_awake[id] = score_during_sleep
                                yield f"SOCK {id} {score_during_sleep}"

                        # Reset wear scores that were gathered during sleep.
                        wear_score_during_sleep.clear()

        return "\n".join(output())
