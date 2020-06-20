from jottingspool.interface import Interface
from jottingspool.files import FileInformation

interface = Interface("")

fi_missing_both = FileInformation("./test.md", ["missing.md"],
                                  ["backlink_too"])
fi_missing_just_reference = FileInformation("./test.md", ["missing.md"], [])
fi_missing_just_backlink = FileInformation("./test.md", [], ["backlink_too"])
fi_missing_nothing = FileInformation("./test.md", [], [])


def test_check_user_input_default_n():
    assert interface.check_input_default_no("y") == True
    assert interface.check_input_default_no("Y") == True
    assert interface.check_input_default_no("yes") == True
    assert interface.check_input_default_no("yup") == True

    assert interface.check_input_default_no("n") == False
    assert interface.check_input_default_no("w") == False
    assert interface.check_input_default_no("no") == False
    assert interface.check_input_default_no("N") == False


def test_check_missing_reference():
    assert interface.is_missing(fi_missing_both) == True
    assert interface.is_missing(fi_missing_just_reference) == True
    assert interface.is_missing(fi_missing_just_backlink) == False
    assert interface.is_missing(fi_missing_nothing) == False
