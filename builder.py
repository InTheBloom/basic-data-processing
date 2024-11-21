# 環境変数PYTHONUTF8を1に設定しないと標準出力がcp932になる。注意。

import pathlib
import os
import sys
import traceback
from builder_utils.directory_tree import DirectoryTree
from builder_utils.file_scanner import FileScanner
from builder_utils.file_builder import FileBuilder

# loggerの設定
from logging import getLogger, StreamHandler, FileHandler, DEBUG, Formatter
logger = getLogger()
logger.setLevel(DEBUG)
st_handler = StreamHandler()
st_handler.setLevel(DEBUG)
st_handler.setFormatter(Formatter('[%(levelname)s] %(asctime)s :In function %(funcName)s, line: %(lineno)s %(message)s'))
logger.addHandler(st_handler)

# 定数
RESOURCE_DIR = "tests/root"
TEMPLATE_DIR = "tests/templates"
TARGET_DIR = "tests/target"
BASEURL = "/"

def jinja_init (template_dir):
    from jinja2 import Environment, FileSystemLoader
    assert(isinstance(template_dir, pathlib.Path))
    logger.info(f"Trying to find html template directory {template_dir}")

    if not template_dir.exists():
        raise Exception(f"{template_dir} is not found.")
    if not template_dir.is_dir():
        raise Exception(f"{template_dir} must be a directory.")

    global jinja_env
    jinja_env = Environment(loader = FileSystemLoader(template_dir))

def main ():
    current_dir = pathlib.Path.cwd()
    logger.info("Start building.")
    logger.info(f"Current directory is {current_dir}")

    # jinjaの初期化
    logger.info("jinja2 initialization.")
    template_dir = current_dir.joinpath(TEMPLATE_DIR)
    jinja_init(template_dir)

    resource_dir = current_dir.joinpath(RESOURCE_DIR)
    target_dir = current_dir.joinpath(TARGET_DIR)

    # ディレクトリスキャン
    logger.info(f"Scanning directory tree from {resource_dir}")
    dir_tree = DirectoryTree(resource_dir)
    logger.info(f"Copying directory tree from {target_dir}")
    dir_tree.build_from(target_dir)

    # ファイルスキャン
    logger.info(f"Scanning files from {resource_dir}")
    file_scanner = FileScanner(resource_dir)
    problem, meta, other = file_scanner.get_file_information()

    # 構築
    logger.info(f"Preparing for file generation.")
    file_builder = FileBuilder(problem, meta, other)
    logger.info(f"Start generating files from {target_dir}")
    file_builder.build_from(target_dir, BASEURL, jinja_env)

if __name__ == "__main__":
    main()
