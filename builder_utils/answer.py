from pathlib import Path
from builder_utils.constants import ANSWER_FILE_NAME

class ProblemAnswer:
    def __init__ (self, dir_path):
        assert(isinstance(dir_path, Path))

        # パスチェック
        self.dir_path = dir_path
        assert(self.dir_path.is_dir())

        # answerファイル探索
        self.answer_file = None
        for entry in self.dir_path.iterdir():
            if entry.name == ANSWER_FILE_NAME:
                self.answer_file = entry

    def file_exists (self):
        return self.answer_file is not None

    def get_answer_text (self):
        if not self.file_exists():
            return ""
        return self.answer_file.read_text()
