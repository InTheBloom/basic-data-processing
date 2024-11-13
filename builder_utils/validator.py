class ProblemValidator:
    @staticmethod
    def validate (problem):
        # useInputとuseSpecialJudgeの検査を行う。
        assert(not problem.get_has_input() or problem.problem_input.file_exists())
        assert(not problem.get_use_special_judge() or problem.problem_judge.file_exists())
