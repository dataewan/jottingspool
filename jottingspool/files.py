from typing import List
import os
import glob
from dataclasses import dataclass
from . import links


@dataclass
class FileInformation:
    filepath: str
    missinglinks: List[str]
    missingbacklinks: List[str]


def file_or_dir(filename: str) -> List[str]:
    """Deal with both files and directories.
    If this is a file then just return that individual markdown file.
    If it is a dir, then return all markdown files in that directory.
    """
    if os.path.isdir(filename):
        return glob.glob(os.path.join(filename, "*.md"))
    else:
        return [filename]


def check_files(files: List[str]) -> List[FileInformation]:
    checks = []
    for file in files:
        linksinfile = links.check_links_exist(file)
        backlinks = links.check_backlinks_exist(file)
        checks.append(FileInformation(file, linksinfile, backlinks))

    return checks


def correct_missing(fileinfo: FileInformation, placeholder: str = "TODO"):
    """Creates missing files.

    args:
    fileinfo: summary of the file
    placeholder: text to create in the new file
    """
    for missing_file in fileinfo.missinglinks:
        with open(missing_file, "w") as f:
            f.write(placeholder)
