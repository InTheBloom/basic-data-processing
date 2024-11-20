# DirectoryTree
# - __init__ (self, rootdir): rootdir以下のディレクトリ構造を解析
# - build_from (self, rootdir): rootdir以下にディレクトリ構造を再現し、すべての相対パスを詰めたリストを返却

from pathlib import Path
from queue import Queue

class DirectoryTree:
    def __init__ (self, rootdir):
        if not isinstance(rootdir, Path):
            raise Exception(f"{rootdir} is invalid.")
        if not rootdir.exists():
            raise Exception(f"{rootdir} doesn't exists.")
        if not rootdir.is_dir():
            raise Exception(f"{rootdir} is not directory.")

        # 幅優先探索
        q = Queue()
        self.child = {}
        q.put(rootdir)

        while not q.empty():
            cur = q.get()
            self.child[cur.relative_to(rootdir)] = []

            # ディレクトリを詰める(rootdirからの相対パスで詰める)
            for entry in cur.iterdir():
                if not entry.is_dir():
                    continue
                self.child[cur.relative_to(rootdir)].append(entry.relative_to(rootdir))
                q.put(entry)

    # rootdir以下に取得しているディレクトリ構造を作成。
    # 幅優先順にした相対パスのリストを返却
    def build_from (self, rootdir):
        if not isinstance(rootdir, Path):
            raise Exception(f"{rootdir} is invalid.")
        if not rootdir.exists():
            raise Exception(f"{rootdir} doesn't exist.")
        if not rootdir.is_dir():
            raise Exception(f"{rootdir} is not directory.")

        # ディレクトリの初期化
        import shutil
        shutil.rmtree(rootdir)
        rootdir.mkdir()

        # ディレクトリの生成
        ret = []
        q = Queue()
        q.put(rootdir.relative_to(rootdir))
        ret.append(rootdir.relative_to(rootdir))
        
        while not q.empty():
            cur = q.get()
            for d in self.child[cur]:
                ret.append(d)
                rootdir.joinpath(d).mkdir()
                q.put(d)

        return ret
