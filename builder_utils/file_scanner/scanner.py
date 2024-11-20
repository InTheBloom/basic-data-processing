from pathlib import Path

class FileScanner:
    def __init__ (self, rootdir):
        if not isinstance(rootdir, Path):
            raise Exception(f"{rootdir} is invalid.")
        if not rootdir.exists():
            raise Exception(f"{rootdir} doesn't exists.")
        if not rootdir.is_dir():
            raise Exception(f"{rootdir} is not directory.")

        # 幅優先探索
