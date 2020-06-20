from rich.console import Console
from jottingspool import files


class Interface(object):
    """User interface for knowledge repository"""
    def __init__(self, path: str):
        """TODO: to be defined.

        Args:
        """
        self.path = path
        self.c = Console()

    def run(self):
        self.summary = []
        self.find_files()
        self.check_files()
        self.correct_files()

    def find_files(self):
        self.markdown_files = files.file_or_dir(self.path)

    def check_files(self):
        self.checks = files.check_files(self.markdown_files)

    def correct_files(self):
        for check in self.checks:
            self.create_missing(check)
            self.create_backlinks(check)

    def create_missing(self, checked_file: files.FileInformation):
        if self.is_missing(checked_file):
            for missing_reference in checked_file.missinglinks:
                if self.ask_user_about_missing(checked_file,
                                               missing_reference):
                    files.correct_missing(checked_file, missing_reference)

    def create_backlinks(self, checked_file: files.FileInformation):
        # TODO
        pass

    @staticmethod
    def is_missing(check: files.FileInformation) -> bool:
        return len(check.missinglinks) > 0

    def ask_user_about_missing(self, check: files.FileInformation,
                               missing_reference: str) -> bool:
        prompt = f"{check.filepath} references missing file {missing_reference}, create it?(yN) "
        input = self.c.input(prompt)
        return self.check_input_default_no(input)

    @staticmethod
    def check_input_default_no(userinput: str) -> bool:
        if userinput.lower()[0] == "y":
            return True
        else:
            return False
