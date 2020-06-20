from typing import List, Tuple
import os
import glob
from dataclasses import dataclass
from . import links
import json

IGNORES_FILENAME = ".ignore.json"


@dataclass
class FileInformation:
    filepath: str
    missinglinks: List[str]
    missingbacklinks: List[str]


@dataclass
class BacklinkIgnores:
    referenced_file: str
    backlink_path: str


def file_or_dir(filename: str) -> Tuple[str, List[str]]:
    """Deal with both files and directories.
    If this is a file then just return that individual markdown file.
    If it is a dir, then return all markdown files in that directory.

    Returns:
    (
        basedirectory: the directory that all the files live in
        files: the paths of all the files
    )
    """
    if os.path.isdir(filename):
        return filename, glob.glob(os.path.join(filename, "*.md"))
    else:
        directory = os.path.dirname(filename)
        return directory, [filename]


def check_files(files: List[str]) -> List[FileInformation]:
    checks = []
    for file in files:
        linksinfile = links.check_links_exist(file)
        backlinks = links.check_backlinks_exist(file)
        checks.append(FileInformation(file, linksinfile, backlinks))

    return checks


def correct_missing(
    fileinfo: FileInformation, missing_reference: str, placeholder: str = "TODO"
):
    """Creates missing files.

    args:
    fileinfo: summary of the file
    missing_reference: file reference that is missing
    placeholder: text to create in the new file
    """
    if not os.path.exists(missing_reference):
        with open(missing_reference, "w") as f:
            f.write(placeholder)


def add_missing_backlink(
    fileinfo: FileInformation, missing_backlink: str, placeholder: str = "TODO"
):
    """Adds a reference to fileinfo at the bottom of the `missing_backlink` file.

    args:
    fileinfo: file that's to be referenced
    missing_backlink: file to add the link into
    placeholder: text to use for the link anchor
    """
    with open(missing_backlink, "a") as f:
        f.write(f"\n[{placeholder}]({fileinfo.filepath})")


def get_ignores_filename(directory: str) -> str:
    """Figure out the ignores filename,
    args:
    directory: base directory
    """
    return os.path.join(directory, IGNORES_FILENAME)


def read_ignores(directory: str) -> List[BacklinkIgnores]:
    ignores_filename = get_ignores_filename(directory)
    if os.path.exists(ignores_filename):
        with open(ignores_filename, "r") as f:
            ignores = [
                BacklinkIgnores(referenced_file=i[0], backlink_path=i[1])
                for i in json.load(f)
            ]

    else:
        ignores = []

    return ignores


def write_ignores(directory: str, ignores: List[BacklinkIgnores]):
    ignores_filename = get_ignores_filename(directory)
    with open(ignores_filename, "w") as f:
        ignore_serialisable = [
            (ignore.referenced_file, ignore.backlink_path) for ignore in ignores
        ]
        json.dump(ignore_serialisable, f, indent=2)
