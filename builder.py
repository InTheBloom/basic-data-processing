from builder_utils import Problem
import pathlib
import os
import sys
import datetime

def test ():
    problem = Problem(pathlib.Path("./resources/problem1"))
    print(problem.get_title())
    print(problem.get_problem_statement())
    print(problem.get_input_description())
    print(problem.get_output_description())
    print(problem.get_more_information())
    print(problem.get_use_special_judge())

    print(problem.get_input_text())

    print(problem.get_answer_text())

    print(problem.get_judge_code())

RESOURCE_DIR_NAME = "resources"
TARGET_DIR_NAME = "docs"

def main ():
    current_dir = pathlib.Path.cwd()
    resource_dir = current_dir.joinpath(RESOURCE_DIR_NAME)

    # リソースディレクトリの検索
    if not resource_dir.exists():
        print(f"[ERROR] {resource_dir} is not found.", file = sys.stderr)
        sys.exit(1)

    if not resource_dir.is_dir():
        print(f"[ERROR] {resource_dir} must be a directory.", file = sys.stderr)
        sys.exit(1)

    print("[INFO] Resource directory is found.")

    # リソースディレクトリの全ディレクトリをProblemディレクトリだとみなして構築

if __name__ == "__main__":
    main()
