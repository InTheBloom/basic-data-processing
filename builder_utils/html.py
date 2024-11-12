from builder_utils.problem import Problem
from builder_utils.constants import INPUT_FILE_NAME

def buld_html_problem_section (problem):
    assert(isinstance(problem, Problem))
    script = ""
    script += "<script>"
    # スペシャルジャッジの場合、inputを埋め込む
    if problem.get_use_special_judge():
        script += f"input_{problemget_title()} = \"{problem.get_input_text()}\";"

    # ジャッジボタンが押されたらジャッジする
    script += "document.addEventListener(\"DOMContentLoaded\", () => {"
    script += "document.getElementById(\"\")"
    script += "});"
    script += "</script>"

    section = ""
    section += "<li><div>"
    section += f"<h2>{problem.get_title()}</h2>"
    section += f"<h3>問題</h3>"
    section += f"<p>problem.get_problem_statement()</p>"
    section += f"<h3>入力</h3>"
    section += f"<p>problem.get_input_description()</p>"
    if (problem.get_has_input()):
        ret += f"<p><a href=\"/{problem.get_title()}/{INPUT_FILE_NAME}\">入力ファイル</a></p>"

    section += f"<h3>出力</h3>"
    section += f"<p>problem.get_output_description()</p>"
    section += f"<div><label for=\"file\">提出ファイルを選択してください。</label><input type=\"file\" id=\"{problem.get_title()}_input\" name=\"{problem.get_title()}_input\"><button id=\"{problem.get_title()}_submit\">提出</button></div>"
    section += f"</div></li>"
    return script + section
