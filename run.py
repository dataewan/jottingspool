#!python
from rich.console import Console
import sys
from jottingspool import files


def run(path: str = "./"):
    c = Console()
    markdown_files = files.file_or_dir(path)
    c.print(markdown_files)
    checks = files.check_files(markdown_files)
    for check in checks:
        c.print(check)
        files.correct_missing(check)


if __name__ == "__main__":
    run(sys.argv[1])
