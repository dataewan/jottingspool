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


def is_markdown_link(el) -> bool:
    if el.__class__ == mistletoe.span_token.Link:
        if ".md" in el.target:
            # Ignoring anything that doesn't have the filetype markdown
            return True
    return False


def get_children(el):
    if has_children(el):
        for child in el.children:
            yield from get_children(child)

    if is_markdown_link(el):
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
    return os.path.exists(link.target)


def backlink_exists(filename: str,
                    links: List[mistletoe.span_token.Link]) -> bool:
    """Check if `links` contains a link that points back at `filename`.
    """
    for link in links:
        if link.target == filename:
            return True

    return False


def missing_links(links: List[mistletoe.span_token.Link]) -> List[str]:
    """Which links don't exist?

    Args:
    links: list of links to check

    Returns: filenames that don't exist

    """
    return [link.target for link in links if not link_exists(link)]


def missing_backlinks(filename: str,
                      links: List[mistletoe.span_token.Link]) -> List[str]:
    """Do all the files linked to in links have a corresponding backlink?

    Args:
    filename: name of the original file
    links: all the links that are in that file

    Returns: list of the missing backlinks
    """
    missing_backlinks = []
    for link in links:
        backlinks = get_links_from_file(link.target)
        if not backlink_exists(filename, backlinks):
            missing_backlinks.append(link.target)

    return missing_backlinks


def check_links_exist(filename: str):
    """Check that all the links in the file actually exist.

    Args:
    filename: file to get links from

    Returns: missing links

    """
    links = get_links_from_file(filename)
    return missing_links(links)


def check_backlinks_exist(filename: str):
    """Check that files that this links to, also have a corresponding backlink

    Args:
    filename: file to get the links from

    Returns: missing backlinks
    """
    links = get_links_from_file(filename)
    return missing_backlinks(filename, links)


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
        links = check_links_exist(file)
        backlinks = check_backlinks_exist(file)
        if len(links) > 0:
            print("Missing link", file, links)

        if len(backlinks) > 0:
            print("Missing backlink", file, backlinks)


if __name__ == "__main__":
    files = file_or_dir(sys.argv[1])
    check_files(files)
