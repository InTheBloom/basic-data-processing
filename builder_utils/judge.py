from pathlib import Path
from builder_utils.constants import JUDGE_FILE_NAME

class ProblemJudge:
    def __init__ (self, dir_path):
        assert(isinstance(dir_path, Path))

        # パスチェック
        self.dir_path = dir_path
        assert(self.dir_path.is_dir())

        # judgeファイル探索
        self.judge_file = None
        for entry in self.dir_path.iterdir():
            if entry.name == JUDGE_FILE_NAME:
                self.judge_file = entry

    def file_exists (self):
        return self.judge_file is not None

    def get_judge_code (self):
        assert(self.judge_file is not None)
        return self.judge_file.read_text()
