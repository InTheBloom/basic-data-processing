from builder_utils import Problem
from builder_utils import build_html_problem_section
import pathlib
import os
import sys
import traceback

def test ():
    problem = Problem(pathlib.Path("./resources/problem1"))
    print(problem.get_title())
    print(problem.get_problem_statement())
    print(problem.get_input_description())
    print(problem.get_has_input())
    print(problem.get_output_description())
    print(problem.get_more_information())
    print(problem.get_use_special_judge())

    print(problem.get_input_text())

    print(problem.get_answer_text())

    print(problem.get_judge_code())

from logging import getLogger, StreamHandler, FileHandler, DEBUG, Formatter
# loggerの設定
logger = getLogger()
logger.setLevel(DEBUG)
st_handler = StreamHandler()
st_handler.setLevel(DEBUG)
st_handler.setFormatter(Formatter('[%(levelname)s] %(asctime)s :In function %(funcName)s, line: %(lineno)s %(message)s'))
logger.addHandler(st_handler)

# 定数
RESOURCE_DIR_NAME = "resources"
TARGET_DIR_NAME = "docs"

def main ():
    current_dir = pathlib.Path.cwd()
    logger.info("Started to build.")
    logger.info(f"Current directory is {current_dir}")

    # リソースディレクトリの検索
    resource_dir = current_dir.joinpath(RESOURCE_DIR_NAME)
    logger.info(f"Trying to find resource directory {resource_dir}")

    if not resource_dir.exists():
        logger.error(f"{resource_dir} is not found.")
        sys.exit(1)
    if not resource_dir.is_dir():
        logger.error(f"{resource_dir} must be a directory.")
        sys.exit(1)

    logger.info(f"Resource directory is found.")

    # リソースディレクトリの全ディレクトリをProblemディレクトリだとみなして構築
    logger.info("Read the problems.")
    for dir_entry in resource_dir.iterdir():
        if not dir_entry.is_dir():
            continue
        try:
            problem = Problem(dir_entry)
        except AssertionError as e:
            logger.error(f"Error occurred while reading {dir_entry}\n" + traceback.format_exc())
            sys.exit(1)

if __name__ == "__main__":
    main()
