from builder_utils.problem import Problem
from builder_utils.constants import INPUT_FILE_NAME

def buld_html_problem_section (problem):
    assert(isinstance(problem, Problem))
    ret = ""
    ret += "<li><div>"

    # title
    ret += f"<h2>{problem.get_title()}</h2>"
    ret += f"<h3>問題</h3>"
    ret += f"<p>problem.get_problem_statement()</p>"
    ret += f"<h3>入力</h3>"
    ret += f"<p>problem.get_input_description()</p>"
    if (problem.get_has_input()):
        ret += f"<p><a href=\"/{problem.get_title()}/{INPUT_FILE_NAME}\">入力ファイル</a></p>"

    ret += f"<h3>出力</h3>"
    ret += f"<p>problem.get_output_description()</p>"
    ret += f"</div></li>"
    return ret
