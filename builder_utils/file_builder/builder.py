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

    def build_from (self, rootdir, baseURL, env, module_dir = None):
        if not isinstance(rootdir, Path):
            raise Exception(f"{rootdir} is not Path.")
        if not rootdir.exists():
            raise Exception(f"{rootdir} doesn't exist.")
        if not rootdir.is_dir():
            raise Exception(f"{rootdir} is not directory.")

        if not isinstance(baseURL, str):
            raise Exception(f"{baseURL} is not str.")

        if not isinstance(env, Environment):
            raise Exception(f"{env} is not jinja2.environment.Environment")

        if not module_dir is None:
            if not isinstance(module_dir, Path):
                raise Exception(f"{module_dir} is not Path.")
            if not module_dir.exists():
                raise Exception(f"{module_dir} doesn't exist.")
            if not module_dir.is_dir():
                raise Exception(f"{module_dir} is not directory.")

        if len(baseURL) == 0 or not baseURL[-1] == "/":
            baseURL += "/"

        module_dir = module_dir.resolve()
        rootdir = rootdir.resolve()

        # 辞書の構築(特殊フィールドの追加も含めて)
        from builder_utils.constants import FileType
        from jinja2.exceptions import (
                TemplateNotFound,
                TemplateAssertionError,
        )

        context = {}
        context["baseURL"] = baseURL
        context["module"] = {}
        for v in FileType:
            context[v.value] = {}

        for entry, binary in self.other.items():
            context[FileType.OTHER.value][str(entry)] = {}
            context[FileType.OTHER.value][str(entry)]["value"] = binary.decode("utf-8")
            context[FileType.OTHER.value][str(entry)]["path"] = str(entry)

        def load_all_module ():
            if module_dir is None:
                return
            # 幅優先探索
            from queue import Queue
            q = Queue()
            q.put(module_dir)
            while not q.empty():
                cur = q.get()
                for entry in cur.iterdir():
                    if entry.is_dir():
                        q.put(entry)
                    if entry.is_file():
                        try:
                            template = env.from_string(
                                    entry.read_text(encoding = "utf-8")
                                    )
                        except TemplateAssertionError as e:
                            raise Exception(f"Failed to interpret the contents of the {entry} as a template.\nError: {e}")
                        context["module"][str(entry.relative_to(module_dir))] = template.render()
        load_all_module()

        import json
        for entry, binary in self.meta.items():
            json_content = json.loads(binary.decode())
            context[FileType.META.value][str(entry)] = json_content
            context[FileType.META.value][str(entry)]["path"] = str(entry)

        for entry, binary in self.problem.items():
            json_content = json.loads(binary.decode())
            context[FileType.PROBLEM.value][str(entry)] = json_content
            context[FileType.PROBLEM.value][str(entry)]["path"] = str(entry)

        # otherを生成
        for entry, binary in self.other.items():
            p = rootdir.joinpath(entry)
            p.write_bytes(binary)

        # metaを生成
        for entry in self.meta.keys():
            context["here"] = str(entry)
            try:
                template = env.get_template(
                        context[FileType.META.value][str(entry)]["templateFileName"]
                        )
            except TemplateNotFound as e:
                raise Exception(f"Failed get template {context[FileType.META.value][str(entry)]['templateFileName']}\nError: {e}")
            except TemplateAssertionError as e:
                raise Exception(f"There's an issue with the template {context[FileType.META.value][str(entry)]['templateFileName']}\nError: {e}")
            rootdir.joinpath(entry).joinpath("index.html").write_text(
                    template.render(context), encoding = "utf-8"
                    )

        # problemを生成
        for entry in self.problem.keys():
            context["here"] = entry
            try:
                template = env.get_template(
                        context[FileType.PROBLEM.value][str(entry)]["templateFileName"]
                        )
            except TemplateNotFound as e:
                raise Exception(f"Failed get template {context[FileType.PROBLEM.value][str(entry)]['templateFileName']}\nError: {e}")
            except TemplateAssertionError as e:
                raise Exception(f"There's an issue with the template {context[FileType.PROBLEM.value][str(entry)]['templateFileName']}\nError: {e}")
            rootdir.joinpath(entry).joinpath("index.html").write_text(
                    template.render(context), encoding = "utf-8"
                    )
