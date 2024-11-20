# 環境変数PYTHONUTF8を1に設定しないと標準出力がcp932になる。注意。

from builder_utils import Problem
import builder_utils.constants
import pathlib
import os
import sys
import traceback

def test_runner ():
    test_directory_tree()
    test_file_scanner()

def test_directory_tree ():
    from builder_utils.directory_tree import DirectoryTree
    rootdir = pathlib.Path("tests/root").resolve()
    d = DirectoryTree(rootdir)
    targetdir = pathlib.Path("tests/target").resolve()
    dirs = d.build_from(targetdir)
    print(dirs)

def test_file_scanner ():
    from builder_utils.file_scanner import FileScanner
    rootdir = pathlib.Path("tests/root").resolve()
    f = FileScanner(rootdir)

test_runner()
sys.exit(0)

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

def init_target_directory (target_dir):
    assert(isinstance(target_dir, pathlib.Path))
    logger.info(f"Trying to find target directory {target_dir}")

    if not target_dir.exists():
        logger.info(f"{target_dir} is not found.")
        os.makedirs(target_dir)
        logger.info(f"{target_dir} is created.")
        return

    logger.info(f"Trying to recreate {target_dir}")
    import shutil
    shutil.rmtree(target_dir)
    os.makedirs(target_dir)

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
    jinja_env = Environment(loader = FileSystemLoader(template_dir))

def main ():
    current_dir = pathlib.Path.cwd()
    logger.info("Started to build.")
    logger.info(f"Current directory is {current_dir}")

    # ディレクトリチェック
    resource_dir = current_dir.joinpath(RESOURCE_DIR_NAME)
    check_resource_directory(resource_dir)

    target_dir = current_dir.joinpath(TARGET_DIR_NAME)
    init_target_directory(target_dir)

    # jinjaの初期化
    template_dir = current_dir.joinpath(TEMPLATE_DIR_NAME)
    jinja_init(template_dir)

    outer_template = jinja_env.get_template("outer.html")
    section_template = jinja_env.get_template("section.html")

    # リソースディレクトリの全ディレクトリをProblemディレクトリだとみなして構築
    logger.info("Read the problems.")
    section_list = []
    for problem_number, dir_entry in enumerate(sorted(list(resource_dir.iterdir())), start = 1):
        if not dir_entry.is_dir():
            continue
        try:
            problem = Problem(dir_entry)
        except AssertionError as e:
            logger.error(f"Error occurred while reading {dir_entry}\n" + traceback.format_exc())
            sys.exit(1)
        
        logger.info(f"Loaded {dir_entry}")
        logger.info(f"Build problem section from {dir_entry}")

        section = section_template.render({
                "title": problem.get_title(),
                "problemNumber": problem_number,
                "problemStatement": problem.get_problem_statement(),
                "inputDescription": problem.get_input_description(),
                "useInput": problem.get_has_input(),
                "useAnswer": problem.get_has_answer(),
                "outputDescription": problem.get_output_description(),
                "moreInformation": problem.get_more_information(),
                "useSpecialJudge": problem.get_use_special_judge(),
                "input_text": problem.get_input_text(),
                "answer_text": problem.get_answer_text(),
                "judge_code": problem.get_judge_code(),
                "INPUT_FILE_NAME": builder_utils.constants.INPUT_FILE_NAME,
                })
        section_list.append(section)

        logger.info(f"Building successed!")

        # 必要なファイルの配置
        if problem.get_has_input():
            input_file_path = target_dir.joinpath("problem" + str(problem_number) + "_" + builder_utils.constants.INPUT_FILE_NAME)

            logger.info(f"Generate input file {input_file_path}")
            input_file_path.write_text(problem.get_input_text())
            logger.info(f"Generation successed!")

    logger.info(f"Build whole html...")
    body = "".join(section_list)
    html = outer_template.render({"contents": body})
    logger.info(f"Successed!")

    # index.htmlの出力
    target_dir.joinpath("index.html").write_text(html)
    logger.info(f'Generated {target_dir.joinpath("index.html")}')

    logger.info(f"All done! see {target_dir}")

if __name__ == "__main__":
    main()
