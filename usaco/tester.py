#!/usr/bin/env python3

import os
import re
import glob
import subprocess
import tempfile
import sys


def compile_cpp(cpp_file_path):
    """Compile the C++ file using g++."""
    cpp_flags = [
        "-Wall",
        "-Wextra",
        "-Wshadow",
        "-Wformat=2",
        "-Wfloat-equal",
        "-Wconversion",
        "-Wlogical-op",
        "-D_GLIBCXX_DEBUG",
        "-D_GLIBCXX_DEBUG_PEDANTIC",
        "-D_FORTIFY_SOURCE=2",
        "-fsanitize=address",
        "-fsanitize=undefined",
        "-fno-sanitize-recover",
        "-fstack-protector",
        # "-static-libasan",
        "-O2",
        "--std=c++17",
        "-g",
    ]
    command = (
        ["g++"]
        + cpp_flags
        + [
            cpp_file_path,
        ]
    )
    subprocess.run(command, check=True)


def run_test(test_dir):
    stdin_filepath = os.path.join(test_dir, "input_stdin.txt")
    expected_stdout_filepath = os.path.join(test_dir, "expected_stdout.txt")

    # Read expected output.
    with open(expected_stdout_filepath, "r") as file:
        expected_stdout = file.read()

    # Execute the compiled program and capture the output.
    with tempfile.NamedTemporaryFile(
        mode="w+", delete=True
    ) as observed_stdout_file:
        with tempfile.NamedTemporaryFile(
            mode="w+", delete=True
        ) as observed_stderr_file:
            with open(stdin_filepath, "r") as stdin_file:
                subprocess.run(
                    ["./a.out"],
                    stdin=stdin_file,
                    stdout=observed_stdout_file,
                    stderr=observed_stderr_file,
                    check=True,
                )

            # Read observed stdout and stderr.
            observed_stdout_file.seek(0)
            observed_stdout = observed_stdout_file.read()
            observed_stderr_file.seek(0)
            observed_stderr = observed_stderr_file.read()

            if observed_stdout.strip() != expected_stdout.strip():
                print(f"FAILED: {test_dir}")
                print("Expected stdout:")
                print(expected_stdout)
                print("Observed stdout:")
                print(observed_stdout)
                print("Observed stderr:")
                print(observed_stderr)
                return False
            else:
                print(f"PASSED: {test_dir}")
                return True


def test_impl(cpp_filepath, test_regex=r"^.*$"):
    print(f"TESTING: {cpp_filepath}")
    compile_cpp(cpp_filepath)

    test_directory = "tests/"
    for test_dir in sorted(glob.glob(os.path.join(test_directory, "*/"))):
        if re.search(test_regex, test_dir) is not None:
            if not run_test(test_dir):
                # Stop on first test failure.
                return


def main():
    match sys.argv[1:]:
        case [cpp_file]:
            test_impl(cpp_file)
        case [cpp_file, test_regex]:
            test_impl(cpp_file, test_regex)
        case []:
            # Test all .cpp files in the current directory.
            for cpp_file in sorted(glob.glob("./*.cpp")):
                test_impl(cpp_file)


if __name__ == "__main__":
    main()
