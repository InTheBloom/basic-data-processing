def test_runner ():
    test_directory_tree()
    test_file_scanner()

def test_directory_tree ():
    from builder_utils.directory_tree import DirectoryTree
    rootdir = pathlib.Path("tests/root").resolve()
    d = DirectoryTree(rootdir)
    targetdir = pathlib.Path("tests/target").resolve()
    dirs = d.build_from(targetdir)
    print(dirs)

def test_file_scanner ():
    from builder_utils.file_scanner import FileScanner
    from builder_utils.file_builder import FileBuilder
    rootdir = pathlib.Path("tests/root").resolve()
    file = FileScanner(rootdir)
    info = file.get_file_information()

    builder = FileBuilder(*info)

    from jinja2 import Environment, FileSystemLoader, select_autoescape
    jinja_env = Environment(loader = FileSystemLoader("tests/templates"))
    builder.build_from(pathlib.Path("tests/target"), jinja_env)

if __name__ == "__main__":
    test_runner()
test_runner()
