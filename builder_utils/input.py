from pathlib import Path
from builder_utils.constants import INPUT_FILE_NAME

class ProblemInput:
    def __init__ (self, dir_path):
        assert(isinstance(dir_path, Path))

        # パスチェック
        self.dir_path = dir_path
        assert(self.dir_path.is_dir())

        # inputファイル探索
        self.input_file = None
        for entry in self.dir_path.iterdir():
            if entry.name == INPUT_FILE_NAME:
                self.input_file = entry

    def file_exists (self):
        return self.input_file is not None

    def get_input_text (self):
        if not self.file_exists():
            return ""
        return self.input_file.read_text()
