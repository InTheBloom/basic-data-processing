from pathlib import Path
from builder_utils.config import ProblemConfig
from builder_utils.input import ProblemInput
from builder_utils.answer import ProblemAnswer
from builder_utils.judge import ProblemJudge

class Problem:
    def __init__ (self, dir_path):
        assert(isinstance(dir_path, Path))

        # パスチェック
        self.dir_path = dir_path
        assert(self.dir_path.is_dir())

        self.problem_config = ProblemConfig(self.dir_path)
        self.problem_input = ProblemInput(self.dir_path)
        self.problem_answer = ProblemAnswer(self.dir_path)
        self.problem_judge = ProblemJudge(self.dir_path)

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

    # ProblemInputに委譲してる分
    def get_input_text (self):
        return self.problem_input.get_input_text()

    # ProblemAnswerに委譲してる分
    def get_answer_text (self):
        return self.problem_answer.get_answer_text()

    # ProblemJudgeに委譲してる分
    def get_judge_code (self):
        return self.problem_judge.get_judge_code()
