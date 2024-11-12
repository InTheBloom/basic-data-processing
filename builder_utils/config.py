import json
from pathlib import Path
from builder_utils.constants import JSON_CONTENTS, JSON_FILE_NAME

class ProblemConfig:
    def __init__ (self, dir_path):
        assert(isinstance(dir_path, Path))

        # パスチェック
        self.dir_path = dir_path
        assert(self.dir_path.is_dir())

        # jsonファイル探索
        self.json_file = None
        for entry in self.dir_path.iterdir():
            if entry.name == JSON_FILE_NAME:
                self.json_file = entry
        assert(self.json_file is not None)

        # json読み取り + 内容チェック
        self.json_contents = json.loads(self.json_file.read_text())
        for detail in JSON_CONTENTS.values():
            assert(detail[0] in self.json_contents)
            assert(type(self.json_contents[detail[0]]) is detail[1])

    def get_field (self, field_name):
        return self.json_contents[field_name]
