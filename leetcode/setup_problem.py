#!/usr/bin/env python3

# Given the URL of a leetcode problem, setup the template directories, files and additions to the README.

import os
import re
import textwrap

this_dir = os.path.dirname(os.path.abspath(__file__))


def create_leetcode_problem():
    # Prompting user for inputs
    problem_url = input("Enter the problem URL: ")
    problem_id = input("Enter the problem identifier: ")
    problem_title = input("Enter the problem title: ")
    problem_difficulty = input("Enter the problem difficulty: ")
    problem_description = input("Enter the text describing the problem: ")

    # Make the difficulty title-case.
    problem_difficulty = problem_difficulty.title()

    # Remove `description/` or `description` from end of URL.
    remove_from_end = ["description/", "description"]
    for end in remove_from_end:
        if problem_url.endswith(end):
            # Remove the last len(end) characters.
            problem_url = problem_url[:-len(end)]
            break

    # Convert problem number to 3 digit number, filling unused digit spaces with zeros.
    digits = 3
    problem_id_filled = str(problem_id).zfill(digits)
    if (len(problem_id_filled) > digits):
        raise RuntimeError(f"Problem id has too many digitis: {problem_id}")

    # Capitalize every word in problem title.
    problem_title_titled = problem_title.title()

    # Get the directory and file names for the problem.
    problem_title_iter = problem_title.lower().split()
    dir_name = f"{problem_id_filled}-{"-".join(problem_title_iter)}"
    file_name = f"{"_".join(problem_title_iter)}.py"

    # Split the description into chunks of at most 80-2=78 (since "# " starts each line).
    wrapper = textwrap.TextWrapper(
        width=78, break_long_words=False, replace_whitespace=False)
    problem_description = wrapper.wrap(problem_description)

    def find_readme_line_to_insert(readme: list[str], new_problem_id: int) -> int:
        # Find index of leetcode section
        leetcode_header = "## [LeetCode](https://leetcode.com)"
        leetcode_section_idx = next(i for i, line in enumerate(
            readme) if leetcode_header in line)

        # Match `| <number> |`.
        pattern = re.compile(r'^\|\s(\d+)\s\|')
        found_a_problem = False
        for i in range(leetcode_section_idx, len(readme)):
            match = pattern.match(readme[i])
            if not match and found_a_problem:
                # We've arrived at the end of all existing problems, so our problem id is larger than all existing problem ids.
                return i
            if match:
                # We've found at least one problem table entry.
                found_a_problem = True
                existing_problem_id = int(match.group(1))
                if new_problem_id == existing_problem_id:
                    raise RuntimeError(
                        "New problem id and existing problem id were the same")
                elif new_problem_id < existing_problem_id:
                    return i - 1

        raise RuntimeError(
            "Did not find a suitable line to insert new problem in readme")

    # Add new problem to README.
    readme_path = os.path.join(this_dir, "../README.md")
    with open(readme_path, 'r') as f:
        readme_lines = f.readlines()
        new_line_idx = find_readme_line_to_insert(
            readme_lines, int(problem_id))
        new_line_content = textwrap.dedent(f"""\
            | {problem_id} | {problem_difficulty} | [{problem_title_titled}]({problem_url}) | [Python](./leetcode/{dir_name}/{file_name}) |
        """)
        readme_lines.insert(new_line_idx, new_line_content)
    with open(readme_path, 'w') as f:
        f.writelines(readme_lines)

    # Create problem directory and file.
    os.makedirs(os.path.join(this_dir, dir_name))
    file_content = textwrap.dedent(f'''\
        #!/usr/bin/env python3

        # {problem_title_titled}
        #
        # {problem_url}
        #
        # {"# ".join(problem_description)}


        def test():
            """
            Run `pytest <this-file > `.
            """

            def test_algo(algo):
                assert 1 == 1

            # Test all different algorithms/implementations
            solution = Solution()
            for algo in [solution.brute_force]:
                test_algo(algo)


        class Solution:
            def brute_force(self):
                """
                Approach:  Brute-force.
                Idea:      ?
                Time:      O(?): ?
                Space:     O(?): ?
                Leetcode:  ? ms runtime, ? MB memory
                """
    ''')
    with open(os.path.join(this_dir, dir_name, file_name), 'w') as f:
        f.write(file_content)


if __name__ == "__main__":
    create_leetcode_problem()
