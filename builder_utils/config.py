import json
from pathlib import Path

JSON_FILE_NAME = "config.json"
JSON_CONTENTS = {
        "title": ("title", str),
        "problemStatement": ("problemStatement", str),
        "inputDescription": ("inputDescription", str),
        "outputDescription": ("outputDescription", str),
        "moreInformation": ("moreInformation", str),
        "useSpecialJudge": ("useSpecialJudge", bool),
        }

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

    def get_title (self):
        return self.json_contents[JSON_CONTENTS["title"][0]]

    def get_problem_statement (self):
        return self.json_contents[JSON_CONTENTS["problemStatement"][0]]

    def get_input_description (self):
        return self.json_contents[JSON_CONTENTS["inputDescription"][0]]

    def get_output_description (self):
        return self.json_contents[JSON_CONTENTS["outputDescription"][0]]

    def get_more_information (self):
        return self.json_contents[JSON_CONTENTS["moreInformation"][0]]

    def get_use_special_judge (self):
        return self.json_contents[JSON_CONTENTS["useSpecialJudge"][0]]
