from builder_utils import Problem
import pathlib

def main ():
    problem = Problem(pathlib.Path("./resources/problem1"))
    print(problem.get_title())
    print(problem.get_problem_statement())
    print(problem.get_input_description())
    print(problem.get_output_description())
    print(problem.get_more_information())
    print(problem.get_use_special_judge())

    print(problem.get_input_text())

    print(problem.get_answer_text())

    print(problem.get_judge_code())

if __name__ == "__main__":
    main()
