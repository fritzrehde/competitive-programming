#!/usr/bin/env python3

# Given details of a leetcode problem, setup the template directories, files and additions to the README.

import os
import re
import sys
import textwrap
import tempfile
import subprocess
from typing import List
import leetcode_graphql_api as leetcode

this_dir = os.path.dirname(os.path.abspath(__file__))

# TODO: prepare the git commit message as well
# TODO: don't make roman numerals (II, IV, etc.) title case


def input_editor(prompt: str) -> List[str]:
    with tempfile.NamedTemporaryFile(mode='r+', delete=True) as f:
        # Ensure prompt is written to disk before opening editor.
        f.write(f"{prompt}\n")
        f.flush()

        # Open the editor
        editor = os.getenv('EDITOR', 'vim')
        subprocess.call([editor, f.name])

        # The editor leaves the file pointer at EOF, so move back to start.
        f.seek(0)
        return f.readlines()


def read_question() -> leetcode.Question:
    # Prompting user for inputs
    problem_url = input("Enter the problem URL: ")

    # Try calling leetcode's API to extract infos, otherwise input manually.
    try:
        return leetcode.get_question(problem_url)
    except Exception as e:
        print(f"Failed to fetch question from leetcode API: {e}", file=sys.stderr)

    id = int(input("Enter the problem identifier: "))
    title = input("Enter the problem title: ").title()
    difficulty = input("Enter the problem difficulty: ").title()
    description_lines = input_editor(
        "Replace this line with the text describing the problem.")

    (url, title_slug) = leetcode.format_problem_url(problem_url)

    return leetcode.Question(
        id=id,
        url=url,
        title_slug=title_slug,
        title=title,
        description_lines=description_lines,
        difficulty=difficulty,
        code_template=None,
        example_tests=None,
    )


def setup_question(question: leetcode.Question):
    # Convert problem number to 4 digit number, filling unused digit spaces with zeros.
    digits = 4
    id_filled = str(question.id).zfill(digits)
    if (len(id_filled) > digits):
        raise RuntimeError(f"Problem id has too many digitis: {question.id}")

    # Get the directory and file names for the problem.
    dir_name = f"{id_filled}-{question.title_slug}"
    file_name = f"{question.title_slug.replace("-", "_")}.py"

    # Split each line of the description into chunks of at most 80-2=78 (since "# " starts each line).
    wrapper = textwrap.TextWrapper(
        width=78, break_long_words=False, replace_whitespace=False)
    wrapped_description_lines = []
    for line in question.description_lines:
        # problem_description_lines.extend(wrapper.wrap(line))
        wrapped = wrapper.wrap(line)
        if wrapped:
            wrapped_description_lines.extend(wrapped)
        else:
            # Append an empty string to represent an empty line.
            wrapped_description_lines.append("")

    # Remove the last description line if it was an empty newline.
    if wrapped_description_lines[-1] == "":
        wrapped_description_lines.pop()

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
            readme_lines, int(question.id))
        new_line_content = textwrap.dedent(f"""\
            | {question.id} | {question.difficulty} | [{question.title}]({question.url}) | [Python](./leetcode/{dir_name}/{file_name}) |
        """)
        readme_lines.insert(new_line_idx, new_line_content)
    with open(readme_path, 'w') as f:
        f.writelines(readme_lines)

    if question.example_tests is not None:
        example_tests_lines = [f"assert algo({example_test.input_args}) == {example_test.expected_output_val}" for example_test in question.example_tests]

    # Create problem directory and file.
    os.makedirs(os.path.join(this_dir, dir_name))
    file_content = textwrap.dedent(f'''\
#!/usr/bin/env python3

# {question.title}
#
# {question.url}
#
# {"\n# ".join(wrapped_description_lines)}


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        {"\n        ".join(example_tests_lines) if example_tests_lines is not None else "assert 1 == 1"}

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force]:
        test_algo(algo)


class Solution:
    def brute_force{f"(self, {question.code_template.args}) -> {question.code_template.return_type}" if question.code_template else "(self)"}:
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
    question = read_question()
    setup_question(question)
