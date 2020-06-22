from jottingspool import links
from typing import List, Tuple
from mistletoe.span_token import Link


def mistletoe_link_to_tuple(link: Link) -> Tuple[str, str]:
    return (
        link.children[0].content,
        link.target,
    )


def mistletoe_links_to_tuples(links: List[Link]) -> List[Tuple[str, str]]:
    return [mistletoe_link_to_tuple(link) for link in links]


fp1 = "./test/test-file-1.md"
fp2 = "./test/test-file-2.md"
fp3 = "./test/test-file-3.md"
fp4 = "./test/test-file-4.md"
fp5 = "./test/test-file-5.md"


def test_link_extraction():
    file1_links = links.get_links_from_file(fp1)
    file2_links = links.get_links_from_file(fp2)
    file3_links = links.get_links_from_file(fp3)
    file4_links = links.get_links_from_file(fp4)
    assert mistletoe_links_to_tuples(file1_links) == [
        ("link to 2", "./test/test-file-2.md"),
        ("link to 3", "./test/test-file-3.md"),
        ("link to 5", "./test/test-file-5.md"),
    ]
    assert mistletoe_links_to_tuples(file2_links) == []
    assert mistletoe_links_to_tuples(file3_links) == [
        ("link to file that doesn't exist", "./test/test-file-1000.md"),
    ]
    assert mistletoe_links_to_tuples(file4_links) == [
        ("link to 1", "./test/test-file-1.md"),
    ]


def test_missing_links():
    file1_missing = links.check_links_exist(fp1)
    file2_missing = links.check_links_exist(fp2)
    file3_missing = links.check_links_exist(fp3)
    file4_missing = links.check_links_exist(fp4)
    file5_missing = links.check_links_exist(fp5)
    assert file1_missing == []
    assert file2_missing == []
    assert file3_missing == ["./test/test-file-1000.md"]
    assert file4_missing == []
    assert file5_missing == []


def test_backlinks_extraction():
    file1_backlinks = links.check_backlinks_exist(fp1)
    file2_backlinks = links.check_backlinks_exist(fp2)
    file3_backlinks = links.check_backlinks_exist(fp3)
    file4_backlinks = links.check_backlinks_exist(fp4)
    assert file1_backlinks == ["./test/test-file-2.md", "./test/test-file-3.md"]
    assert file2_backlinks == []
    assert file3_backlinks == []
    assert file4_backlinks == ["./test/test-file-1.md"]
