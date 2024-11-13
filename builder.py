from builder_utils import Problem
#from builder_utils import build_html_problem_section
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

# loggerの設定
from logging import getLogger, StreamHandler, FileHandler, DEBUG, Formatter
logger = getLogger()
logger.setLevel(DEBUG)
st_handler = StreamHandler()
st_handler.setLevel(DEBUG)
st_handler.setFormatter(Formatter('[%(levelname)s] %(asctime)s :In function %(funcName)s, line: %(lineno)s %(message)s'))
logger.addHandler(st_handler)

# 定数
RESOURCE_DIR_NAME = "resources/problems"
TEMPLATE_DIR_NAME = "resources/templates"
TARGET_DIR_NAME = "docs"

# jinja2(jinja_init()で初期化)
from jinja2 import Environment, FileSystemLoader, select_autoescape
jinja_env = None

def check_resource_directory (resource_dir):
    assert(isinstance(resource_dir, pathlib.Path))
    logger.info(f"Trying to find resource directory {resource_dir}")

    if not resource_dir.exists():
        logger.error(f"{resource_dir} is not found.")
        sys.exit(1)
    if not resource_dir.is_dir():
        logger.error(f"{resource_dir} must be a directory.")
        sys.exit(1)

    logger.info(f"Resource directory is found.")

def jinja_init (template_dir):
    assert(isinstance(template_dir, pathlib.Path))
    logger.info(f"Trying to find html template directory {template_dir}")

    if not template_dir.exists():
        logger.error(f"{template_dir} is not found.")
        sys.exit(1)
    if not template_dir.is_dir():
        logger.error(f"{template_dir} must be a directory.")
        sys.exit(1)
    logger.info(f"Html template directory is found.")

    global jinja_env
    jinja_env = Environment(loader = FileSystemLoader(template_dir), autoescape = select_autoescape())


def main ():
    current_dir = pathlib.Path.cwd()
    logger.info("Started to build.")
    logger.info(f"Current directory is {current_dir}")

    # ディレクトリチェック
    resource_dir = current_dir.joinpath(RESOURCE_DIR_NAME)
    check_resource_directory(resource_dir)

    # jinjaの初期化
    template_dir = current_dir.joinpath(TEMPLATE_DIR_NAME)
    jinja_init(template_dir)

    jinja_env.get_template("a.html")

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
