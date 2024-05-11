#!/usr/bin/env python3

# Given details of a leetcode problem, setup the template directories, files and additions to the README.

import os
import re
import textwrap
import tempfile
import subprocess
import itertools

this_dir = os.path.dirname(os.path.abspath(__file__))

# TODO: prepare the git commit message as well


def create_leetcode_problem():
    def input_editor(prompt: str) -> str:
        with tempfile.NamedTemporaryFile(mode='r+', delete=True) as f:
            # Ensure prompt is written to disk before opening editor.
            f.write(prompt)
            f.flush()

            # Open the editor
            editor = os.getenv('EDITOR', 'vim')
            subprocess.call([editor, f.name])

            # The editor leaves the file pointer at EOF, so move back to start.
            f.seek(0)
            return f.read()

    # Prompting user for inputs
    problem_url = input("Enter the problem URL: ")
    problem_id = input("Enter the problem identifier: ")
    problem_title = input("Enter the problem title: ")
    problem_difficulty = input("Enter the problem difficulty: ")
    problem_description = input_editor(
        "Replace this line with the text describing the problem.\n")

    # Make the difficulty title-case.
    problem_difficulty = problem_difficulty.title()

    # Only keep `https://leetcode.com/problems/<problem-name>/`, and remove anything after.
    match = re.match(r"https://leetcode.com/problems/([^/]+)/", problem_url)
    if match:
        problem_url = match.group(0)
        # Leetcode already has a nicely formatted name to use for the directory and file names, so extract it.
        problem_name = match.group(1)
    else:
        raise RuntimeError("failed to parse leetcode problem url")

    # Convert problem number to 4 digit number, filling unused digit spaces with zeros.
    digits = 4
    problem_id_filled = str(problem_id).zfill(digits)
    if (len(problem_id_filled) > digits):
        raise RuntimeError(f"Problem id has too many digitis: {problem_id}")

    # Capitalize every word in problem title.
    problem_title_titled = problem_title.title()

    # Get the directory and file names for the problem.
    problem_name = problem_name.lower()
    dir_name = f"{problem_id_filled}-{problem_name}"
    file_name = f"{problem_name.replace("-", "_")}.py"

    # Split each line of the description into chunks of at most 80-2=78 (since "# " starts each line).
    wrapper = textwrap.TextWrapper(
        width=78, break_long_words=False, replace_whitespace=False)
    problem_description_lines = []
    for line in problem_description.split('\n'):
        # problem_description_lines.extend(wrapper.wrap(line))
        wrapped = wrapper.wrap(line)
        if wrapped:
            problem_description_lines.extend(wrapped)
        else:
            # Append an empty string to represent an empty line.
            problem_description_lines.append("")

    # Remove the last description line if it was an empty newline.
    if problem_description_lines[-1] == "":
        problem_description_lines.pop()

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
                    return i

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
# {"\n# ".join(problem_description_lines)}


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
