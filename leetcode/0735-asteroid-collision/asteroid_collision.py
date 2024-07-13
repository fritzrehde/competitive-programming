#!/usr/bin/env python3

# Asteroid Collision
#
# https://leetcode.com/problems/asteroid-collision/
#
# We are given an array asteroids of integers representing asteroids in a row.
#
# For each asteroid, the absolute value represents its size, and the sign
# represents its direction (positive meaning right, negative meaning left). Each
# asteroid moves at the same speed.
#
# Find out the state of the asteroids after all collisions. If two asteroids
# meet, the smaller one will explode. If both are the same size, both will
# explode. Two asteroids moving in the same direction will never meet.


from typing import List, Optional


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(asteroids=[5, 10, -5]) == [5, 10]

        assert algo(asteroids=[8, -8]) == []

        assert algo(asteroids=[10, 2, -5]) == [10]

        assert algo(asteroids=[-2, -1, 1, 2]) == [-2, -1, 1, 2]

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.stack, solution.stack_improved]:
        test_algo(algo)


class Solution:
    def stack(self, asteroids: List[int]) -> List[int]:
        """
        Approach:  Model remaining asteroids as stack.
        Idea:      Keep a stack of all (so far) non-collided asteroids, and once we see a left-moving asteroid, let it smash into any right-moving asteroids it is larger than on top of the stack.
        Time:      O(n): We handle every asteroid at most twice: Once when it might be added to the stack, and once when it might be removed from the stack due to smashing.
        Space:     O(n): We don't remove asteroids in-place from the input array, but build the output up as a stack.
        Leetcode:  97 ms runtime, 17.83 MB memory
        """

        def moves_right(asteroid): return asteroid >= 0
        def moves_left(asteroid): return asteroid < 0
        def size(asteroid): return abs(asteroid)

        asteroids_stack = []

        n = len(asteroids)

        i = 0
        while i < n:
            right_asteroid = asteroids[i]
            if not asteroids_stack:
                asteroids_stack.append(right_asteroid)
                i += 1
            else:
                if moves_right(right_asteroid):
                    asteroids_stack.append(right_asteroid)
                    i += 1
                else:
                    left_asteroid = asteroids_stack[-1]

                    # Handle collision.
                    would_collide = moves_right(left_asteroid) and moves_left(right_asteroid)
                    if would_collide:
                        left_size, right_size = size(left_asteroid), size(right_asteroid)
                        if left_size == right_size:
                            # Both asteroids are destroyed if they have equal size.
                            # Remove left asteroid (top of stack).
                            asteroids_stack.pop()
                            # Remove right asteroid by not adding to stack.
                            i += 1
                        elif left_size < right_size:
                            # If sizes differ, smaller asteroid is destroyed.
                            # Remove left asteroid (top of stack).
                            asteroids_stack.pop()
                            # Don't remove right asteroid (so don't increment i).
                        elif left_size > right_size:
                            # If sizes differ, smaller asteroid is destroyed.
                            # Don't remove left asteroid (top of stack).
                            # Remove right asteroid (so increment i).
                            i += 1
                    else:
                        asteroids_stack.append(right_asteroid)
                        i += 1

        return asteroids_stack

    def stack_improved(self, asteroids: List[int]) -> List[int]:
        """
        Approach:  Model remaining asteroids as stack, improved.
        Idea:      Keep a stack of all (so far) non-collided asteroids, and once we see a left-moving asteroid, let it smash into any right-moving asteroids it is larger than on top of the stack.
        Time:      O(n): We handle every asteroid at most twice: Once when it might be added to the stack, and once when it might be removed from the stack due to smashing.
        Space:     O(n): We don't remove asteroids in-place from the input array, but build the output up as a stack.
        Leetcode:  92 ms runtime, 17.96 MB memory
        """

        def moves_right(asteroid): return asteroid >= 0
        def moves_left(asteroid): return asteroid < 0
        def size(asteroid): return abs(asteroid)

        asteroids_stack = []

        for right_asteroid in asteroids:
            if moves_right(right_asteroid):
                asteroids_stack.append(right_asteroid)
            elif moves_left(right_asteroid):
                # Let the left-moving asteroid continuously collide with right-moving asteroids from the stack until it has destroyed all or is destroyed.
                while True:
                    if not asteroids_stack:
                        asteroids_stack.append(right_asteroid)
                        break
                    else:
                        left_asteroid = asteroids_stack[-1]

                        def destroy_left():
                            asteroids_stack.pop()

                        if moves_right(left_asteroid):
                            left_size, right_size = size(left_asteroid), size(right_asteroid)
                            if left_size == right_size:
                                # Both asteroids are destroyed.
                                destroy_left()
                                # Right asteroid is destroyed by left asteroid, so cannot continue smashing.
                                break
                            elif left_size < right_size:
                                # Left asteroid is destroyed by right asteroid.
                                destroy_left()
                                # Right asteroid can continue smashing.
                                continue
                            elif left_size > right_size:
                                # Right asteroid is destroyed by left asteroid, so cannot continue smashing.
                                break
                        else:
                            asteroids_stack.append(right_asteroid)
                            break

        return asteroids_stack
