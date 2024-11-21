from pathlib import Path
from queue import Queue

class FileScanner:
    def __init__ (self, rootdir):
        if not isinstance(rootdir, Path):
            raise Exception(f"{rootdir} is invalid.")
        if not rootdir.exists():
            raise Exception(f"{rootdir} doesn't exists.")
        if not rootdir.is_dir():
            raise Exception(f"{rootdir} is not directory.")

        rootdir = rootdir.resolve()
        files = self._search_from(rootdir)
        self.problem, self.meta, self.other = self._check_and_categorize_files(rootdir, files)

    def _search_from (self, rootdir):
        # 幅優先探索
        q = Queue()
        files = {}
        q.put(rootdir)

        while not q.empty():
            cur = q.get()
            for entry in cur.iterdir():
                if entry.is_file():
                    files[entry.relative_to(rootdir)] = entry.read_bytes()

                if entry.is_dir():
                    q.put(entry)
        return files

    def _check_config (self, path, rootdir, files):
        from builder_utils.constants import (
                FileType,
                RequiredJsonKeysCommon,
        )
        from json.decoder import JSONDecodeError
        import json

        try:
            json_contents = json.loads(files[path].decode())
        except JSONDecodeError as e:
            raise Exception(f"Failed to parse {path} as json.\nError: {e}")

        for field, valuetype in RequiredJsonKeysCommon.items():
            if not field in json_contents:
                raise Exception(f"In file {path}, field {field} not found.")
            if type(json_contents[field]) is not valuetype:
                raise Exception(f"In file {path}, type of {field} must be {valuetype}")

        # fileTypeのチェック
        if ((not json_contents["fileType"] == FileType.PROBLEM.value) and
        (not json_contents["fileType"] == FileType.META.value)):
            raise Exception(f"In file {path}, field fileType must be one of following\n- {FileType.PROBLEM.value}\n- {FileType.META.value}")

        # TODO: テンプレートの存在もチェック(実装するかは不明)

        if json_contents["fileType"] == FileType.PROBLEM.value:
            self._check_problem_config(json_contents, path, rootdir, files)

        if json_contents["fileType"] == FileType.META.value:
            self._check_meta_config(json_contents, path, rootdir, files)

        return json_contents["fileType"]

    def _check_problem_config (self, json_contents, path, rootdir, files):
        from builder_utils.constants import RequiredJsonKeysProblem

        for field, valuetype in RequiredJsonKeysProblem.items():
            if not field in json_contents:
                raise Exception(f"In file {path}, field {field} not found.")
            if type(json_contents[field]) is not valuetype:
                raise Exception(f"In file {path}, type of {field} must be {valuetype}")

        # path_check(s): json_contents[s]のファイルが存在するかチェック
        # 相対パスに直した後json_contents[s]に詰めなおす
        def path_check (s):
            from pathlib import Path
            # 空の時はOK
            if json_contents[s] == "":
                return

            p = Path(json_contents[s])
            if p.is_absolute():
                np = rootdir.joinpath(p)
                if not np.exists():
                    raise Exception(f"{p} doesn't exist.")
                if not np.is_file():
                    raise Exception(f"{p} is not file.")
                # 相対パスに直す
                json_contents[s] = np.relative_to(path.parent)
                return
            if not p.exists():
                raise Exception(f"{p} doesn't exist.")
            if not p.is_file():
                raise Exception(f"{p} is not file.")

        # inputFilePath
        # outputFilePath
        # judgeFilePath
        # のチェック
        path_check("inputFilePath")
        path_check("outputFilePath")
        path_check("judgeFilePath")

    def _check_meta_config (self, json_contents, path, rootdir, files):
        from builder_utils.constants import RequiredJsonKeysMeta

        for field, valuetype in RequiredJsonKeysMeta.items():
            if not field in json_contents:
                raise Exception(f"In file {path}, field {field} not found.")
            if type(json_contents[field]) is not valuetype:
                raise Exception(f"In file {path}, type of {field} must be {valuetype}")

    def _check_and_categorize_files (self, rootdir, files):
        # 名前がFileName.CONFIG.valueのファイルはすべてチェックにかける
        # それ以外のファイルはotherに分類
        from builder_utils.constants import FileType, FileName
        problem = {}
        meta = {}
        other = {}

        # チェックをかけて、辞書に追加
        for path, val in files.items():
            if path.name == FileName.CONFIG.value:
                t = self._check_config(path, rootdir, files)
                if t == FileType.PROBLEM.value:
                    problem[path.parent] = val
                if t == FileType.META.value:
                    meta[path.parent] = val
                continue
            other[path] = val
        return (problem, meta, other)

    def get_file_information (self):
        return (self.problem, self.meta, self.other)
