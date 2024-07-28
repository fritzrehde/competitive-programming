#!/usr/bin/env python3

import sys
import itertools
import re
from dataclasses import dataclass
import pprint
from typing import List, Optional
import requests
from bs4 import BeautifulSoup


# Leetcode's graphql api endpoint.
BASE_URL = "https://leetcode.com/graphql"


@dataclass
class CodeTemplate:
    # Function arguments in the format "<arg_name>: <arg_type>(, <arg_name> = <arg_type>)*".
    args: str
    return_type: str


@dataclass
class ExampleTest:
    # Input arguments in the format "<arg_name> = <arg_val>(, <arg_name> = <arg_val>)*".
    input_args: str
    expected_output_val: str


@dataclass
class Question:
    id: int
    url: str
    title: str
    title_slug: str
    description_lines: List[str]
    difficulty: str
    code_template: Optional[CodeTemplate]
    example_tests: Optional[List[ExampleTest]]


def format_problem_url(problem_url: str):
    # Only keep `https://leetcode.com/problems/<title-slug>`, and remove anything after.
    if (m := re.search(r"^(https://leetcode.com/problems/([^/]+))", problem_url)):
        url = m.group(1)
        title_slug = m.group(2)
        return (url, title_slug)
    else:
        raise Exception("failed to parse leetcode problem url")


def get_question(problem_url: str):
    (url, title_slug) = format_problem_url(problem_url)

    graphql_query = {
        "query":
            """query questionHints($titleSlug: String!) {
                question(titleSlug: $titleSlug) {
                    questionFrontendId
                    title
                    difficulty
                    codeSnippets {
                        lang
                        langSlug
                        code
                    }
                    content
                    isPaidOnly
                }
            }
            """,
        "variables": {"titleSlug": title_slug},
    }
    response = requests.post(BASE_URL, json=graphql_query)
    if response.status_code == 404:
        raise Exception("leetcode's graphql API can't be found")

    response = response.json()
    question_data = response["data"]["question"]

    content = question_data["content"]
    soup = BeautifulSoup(content, "lxml")
    content_text = soup.text.replace('\xa0', ' ')
    content_lines = content_text.splitlines()

    return Question(
        id=question_data["questionFrontendId"],
        url=url,
        title_slug=title_slug,
        title=question_data["title"],
        description_lines=parse_description_lines(content_lines),
        difficulty=question_data["difficulty"],
        code_template=parse_code_template(question_data),
        example_tests=parse_example_tests(content_lines),
    )


def parse_description_lines(content_lines: List[str]) -> List[str]:
    return list(itertools.takewhile(lambda line: line != " ", content_lines))


def parse_code_template(question_data) -> CodeTemplate:
    code = next(code_snippet["code"] for code_snippet in question_data["codeSnippets"] if code_snippet["lang"] == "Python3")
    fn_definition = code.splitlines()[1]
    print(fn_definition)
    if (m := re.search(r'^\s*def [^(]+\(self, ([^)]+)\) -> ([^:]+):', fn_definition)):
        args = m.group(1)
        return_type = m.group(2)
        return CodeTemplate(args, return_type)
    else:
        raise Exception(f"invalid code template format received: {code}")


def parse_example_tests(content_lines: List[str]) -> List[ExampleTest]:
    input_regex = re.compile(r'^Input: (.+)$')
    inputs = [m.group(1) for line in content_lines if (m := input_regex.search(line))]

    output_regex = re.compile(r'^Output: (.+)$')
    outputs = [m.group(1) for line in content_lines if (m := output_regex.search(line))]

    return [ExampleTest(input, output) for (input, output) in zip(inputs, outputs)]


def main():
    pprint.pprint(get_question(sys.argv[1]))


if __name__ == "__main__":
    main()
