from jottingspool.interface import Interface
from jottingspool.files import FileInformation, BacklinkIgnores

interface = Interface("")

fi_missing_both = FileInformation("./test.md", ["missing.md"],
                                  ["backlink_too"])
fi_missing_just_reference = FileInformation("./test.md", ["missing.md"], [])
fi_missing_just_backlink = FileInformation("./test.md", [], ["backlink_too"])
fi_missing_nothing = FileInformation("./test.md", [], [])


def test_check_user_input_default_n():
    assert interface.user_input_default_no_logic("y") == True
    assert interface.user_input_default_no_logic("Y") == True
    assert interface.user_input_default_no_logic("yes") == True
    assert interface.user_input_default_no_logic("yup") == True

    assert interface.user_input_default_no_logic("n") == False
    assert interface.user_input_default_no_logic("w") == False
    assert interface.user_input_default_no_logic("no") == False
    assert interface.user_input_default_no_logic("N") == False
    assert interface.user_input_default_no_logic("") == False


def test_check_missing_reference():
    assert interface.is_missing(fi_missing_both) == True
    assert interface.is_missing(fi_missing_just_reference) == True
    assert interface.is_missing(fi_missing_just_backlink) == False
    assert interface.is_missing(fi_missing_nothing) == False


def test_should_ignore_backlink():
    interface.ignores = []
    backlink_example = BacklinkIgnores(referenced_file="a", backlink_path="b")
    assert interface.should_ignore_backlink(backlink_example) == False

    interface.ignores = [backlink_example]
    assert interface.should_ignore_backlink(backlink_example) == True

