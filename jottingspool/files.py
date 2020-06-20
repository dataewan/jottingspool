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


def correct_missing(fileinfo: FileInformation,
                    missing_reference: str,
                    placeholder: str = "TODO"):
    """Creates missing files.

    args:
    fileinfo: summary of the file
    missing_reference: file reference that is missing
    placeholder: text to create in the new file
    """
    if not os.path.exists(missing_reference):
        with open(missing_reference, "w") as f:
            f.write(placeholder)


def add_missing_backlink(fileinfo: FileInformation,
                         missing_backlink: str,
                         placeholder: str = "TODO"):
    """Adds a reference to fileinfo at the bottom of the `missing_backlink` file.

    args:
    fileinfo: file that's to be referenced
    missing_backlink: file to add the link into
    placeholder: text to use for the link anchor
    """
    with open(missing_backlink, "a") as f:
        f.write(f"\n[{placeholder}]({fileinfo.filepath})")
