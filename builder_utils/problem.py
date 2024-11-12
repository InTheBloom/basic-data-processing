from pathlib import Path
from builder_utils.config import ProblemConfig

class Problem:
    def __init__ (self, dir_path):
        # パスチェック
        self.dir_path = dir_path
        assert(self.dir_path.is_dir())

        self.problem_config = ProblemConfig(self.dir_path)

    # ProblemConfigに委譲している分
    def get_title (self):
        return self.problem_config.get_title()

    def get_problem_statement (self):
        return self.problem_config.get_problem_statement()

    def get_input_description (self):
        return self.problem_config.get_input_description()

    def get_output_description (self):
        return self.problem_config.get_output_description()

    def get_more_information (self):
        return self.problem_config.get_more_information()

    def get_use_special_judge (self):
        return self.problem_config.get_use_special_judge()
