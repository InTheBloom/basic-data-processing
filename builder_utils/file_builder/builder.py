from pathlib import Path
from jinja2.environment import Environment

class FileBuilder:
    def __init__ (self, problem, meta, other):
        if not isinstance(problem, dict):
            raise Exception(f"{problem} is not dict.")
        if not isinstance(meta, dict):
            raise Exception(f"{meta} is not dict.")
        if not isinstance(other, dict):
            raise Exception(f"{other} is not dict.")

        self.problem = problem
        self.meta = meta
        self.other = other

    def build_from (self, rootdir, env):
        if not isinstance(rootdir, Path):
            raise Exception(f"{rootdir} is not Path.")
        if not rootdir.exists():
            raise Exception(f"{rootdir} doesn't exist.")
        if not rootdir.is_dir():
            raise Exception(f"{rootdir} is not directory.")

        if not isinstance(env, Environment):
            raise Exception(f"{env} is not jinja2.environment.Environment")

        rootdir = rootdir.resolve()

        # 辞書の構築
        from builder_utils.constants import FileType
        context = {}
        for v in FileType:
            context[v.value] = {}

        for entry, binary in self.other.items():
            context[FileType.OTHER.value][entry] = binary

        import json
        for entry, binary in self.meta.items():
            json_content = json.loads(binary.decode())
            context[FileType.META.value][entry] = json_content
        for entry, binary in self.problem.items():
            json_content = json.loads(binary.decode())
            context[FileType.PROBLEM.value][entry] = json_content

        # otherの構築
        for entry, binary in self.other.items():
            p = rootdir.joinpath(entry)
            p.write_bytes(binary)

        from jinja2.exceptions import (
                TemplateNotFound,
                TemplateAssertionError,
        )
        # metaの構築
        for entry in self.meta.keys():
            context["here"] = entry
            try:
                template = env.get_template(
                        context[FileType.META.value][entry]["templateFileName"]
                        )
            except TemplateNotFound as e:
                raise Exception(f"Failed get template {context[FileType.META.value][entry]['templateFileName']}\nError: {e}")
            except TemplateAssertionError as e:
                raise Exception(f"There's an issue with the template {context[FileType.META.value][entry]['templateFileName']}\nError: {e}")
            rootdir.joinpath(entry).parent.joinpath("index.html").write_text(
                    template.render(context), encoding = "utf-8"
                    )

        # problemの構築
        for entry in self.problem.keys():
            context["here"] = entry
            try:
                template = env.get_template(
                        context[FileType.PROBLEM.value][entry]["templateFileName"]
                        )
            except TemplateNotFound as e:
                raise Exception(f"Failed get template {context[FileType.PROBLEM.value][entry]['templateFileName']}\nError: {e}")
            except TemplateAssertionError as e:
                raise Exception(f"There's an issue with the template {context[FileType.PROBLEM.value][entry]['templateFileName']}\nError: {e}")
            rootdir.joinpath(entry).parent.joinpath("index.html").write_text(
                    template.render(context), encoding = "utf-8"
                    )
