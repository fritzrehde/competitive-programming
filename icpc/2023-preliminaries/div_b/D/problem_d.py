#!/usr/bin/env python3

# Darcy's Parsing Problem About Lottos
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
                input="""+----+----+----+----+
|....|....|....|....|
|....|....|....|....|
|....|....|....|....|
|....|....|....|....|
+----+----+----+----+
|....|....|....|....|
|....|....|....|....|
|....|....|....|....|
|....|....|....|....|
+----+----+----+----+
+----+----+----+----+
|....|....|....|....|
|....|....|....|....|
|....|....|....|....|
|....|....|....|....|
+----+----+----+----+
|....|....|....|....|
|....|....|....|....|
|....|....|....|....|
|....|....|....|....|
+----+----+----+----+"""
            )
            == "8"
        )

        assert (
            algo(
                input="""+----+----+----+----+
|####|####|####|####|
|####|#..#|#..#|#...|
|...#|####|####|#...|
|####|#...|#...|####|
+----+----+----+----+
|....|....|....|....|
|####|####|####|####|
|....|....|....|....|
|....|....|....|....|
+----+----+----+----+
+----+----+----+----+
|.#..|####|####|####|
|.#..|#...|#..#|#...|
|.#..|#...|####|#...|
|.#..|####|#...|####|
+----+----+----+----+
|....|....|....|....|
|....|....|....|....|
|....|....|....|....|
|....|....|....|....|
+----+----+----+----+"""
            )
            == "2"
        )

        assert (
            algo(
                input="""+----+----+----+----+
|....|....|....|....|
|#...|.#..|..#.|...#|
|....|....|....|....|
|#...|.#..|..#.|...#|
+----+----+----+----+
|....|....|....|....|
|....|....|....|....|
|....|....|....|....|
|#...|.#..|..#.|...#|
+----+----+----+----+
+----+----+----+----+
|....|....|....|....|
|#...|.#..|..#.|...#|
|....|....|....|....|
|#...|.#..|..#.|...#|
+----+----+----+----+
|#...|.#..|..#.|...#|
|....|....|....|....|
|....|....|....|....|
|....|....|....|....|
+----+----+----+----+"""
            )
            == "4"
        )

    # Test all different algorithms/implementations.
    solution = Solution()
    for algo in [solution.brute_force]:
        test_algo(algo)


class Solution:
    def brute_force(self, input=str) -> str:
        """
        Approach:  Brute force.
        Idea:      Parse all top and bottom images, and then construct hashmap mapping image to occurence count in top and bottom, so matches is equal to the min of count in top and bottom.
        Time:      O(n): Given n cells in the grid input, we include most (besides separators) in one image.
        Space:     O(16 * 16): We collect each of the 16 images (each 16 chars) to strings, and associate each image with a two counts (top and bottom).
        """

        from collections import defaultdict

        grid = [[cell for cell in row] for row in input.splitlines()]

        def parse_4_images(grid):
            # O(n)
            for i in range(4):
                top_left_row_idx = 0
                top_left_col_idx = (5 * i) + 1
                # NOTE: The newlines are unnecessary, but kept for visualization.
                image = (
                    "\n".join(
                        "".join(row[top_left_col_idx : top_left_col_idx + 4])
                        for row in grid[top_left_row_idx : top_left_row_idx + 4]
                    )
                    + "\n"
                )
                yield image

        top_images = list(parse_4_images(grid[1:5])) + list(
            parse_4_images(grid[6:10])
        )
        bottom_images = list(parse_4_images(grid[12:16])) + list(
            parse_4_images(grid[17:21])
        )
        all_images = set(top_images) | set(bottom_images)

        top_image_count = defaultdict(lambda: 0)
        for image in top_images:
            top_image_count[image] += 1

        bottom_image_count = defaultdict(lambda: 0)
        for image in bottom_images:
            bottom_image_count[image] += 1

        matches = 0
        for image in all_images:
            matches += min(top_image_count[image], bottom_image_count[image])

        return str(matches)
