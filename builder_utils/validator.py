class ProblemValidator:
    @staticmethod
    def validate (problem):
        # useInput
        assert(problem.get_has_input() == problem.problem_input.file_exists())
        # useSpecialJudge
        assert(problem.get_use_special_judge() == problem.problem_judge.file_exists())
        # useAnswer
        assert(problem.get_has_answer() == problem.problem_answer.file_exists())
