import mistletoe
import sys
from typing import List
import os
import glob


def has_children(el) -> bool:
    try:
        return len(el.children) > 0
    except AttributeError:
        return False


def is_link(el) -> bool:
    return el.__class__ == mistletoe.span_token.Link


def get_children(el):
    if has_children(el):
        for child in el.children:
            yield from get_children(child)

    if is_link(el):
        yield el


def extract_links(markdowntext: str) -> List[mistletoe.span_token.Link]:
    doc = mistletoe.Document(markdowntext)
    children = get_children(doc)
    return list(children)


def get_links_from_file(filename: str) -> List[mistletoe.span_token.Link]:
    with open(filename, "r") as f:
        text = f.read()
        return extract_links(text)


def link_exists(link: mistletoe.span_token.Link) -> bool:
    target = link.target
    if "http" in target:
        # Just assume that all remote links are okay
        return True
    else:
        return os.path.exists(link.target)


def missing_links(links: List[mistletoe.span_token.Link]) -> List[str]:
    """Which links don't exist?

    Args:
    links: list of links to check

    Returns: filenames that don't exist

    """
    return [link.target for link in links if not link_exists(link)]


def check_links_exist(filename: str):
    """Check that all the links in the file actually exist.

    Args:
    filename: file to get links from

    Returns: missing links

    """
    links = get_links_from_file(filename)
    return missing_links(links)


def file_or_dir(filename: str) -> List[str]:
    """Deal with both files and directories.
    If this is a file then just return that individual markodwn file.
    If it is a dir, then return all markdown files in that directory.
    """
    if os.path.isdir(filename):
        return glob.glob(os.path.join(filename, "*.md"))
    else:
        return [filename]


def check_files(files: List[str]):
    for file in files:
        missing_links = check_links_exist(file)
        if len(missing_links) > 0:
            print("Missing link", file, missing_links)


if __name__ == "__main__":
    files = file_or_dir(sys.argv[1])
    check_files(files)
