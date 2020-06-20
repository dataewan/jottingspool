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
        if self.has_missing_backlinks(checked_file):
            for missing_backlink in checked_file.missingbacklinks:
                self.ask_user_about_backlink(checked_file, missing_backlink)

    @staticmethod
    def is_missing(check: files.FileInformation) -> bool:
        return len(check.missinglinks) > 0

    @staticmethod
    def has_missing_backlinks(checked_file: files.FileInformation) -> bool:
        return len(checked_file.missingbacklinks) > 0

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

    def ask_user_about_backlink(self, checked_file: files.FileInformation,
                                missing_backlink: str):
        prompt = f"{checked_file.filepath} is referenced by {missing_backlink}.\nShould I add the link in at the end of {missing_backlink}? (yN)"
        input = self.c.input(prompt)
        should_add_link = self.check_input_default_no(input)
        if should_add_link:
            self.c.print(
                f"Adding a link to {checked_file.filepath} from {missing_backlink}"
            )
        if not should_add_link:
            prompt = f"Would you like to ignore this warning in future? (yN)"
            input = self.c.input(prompt)
            should_add_ignore = self.check_input_default_no(input)
            if should_add_ignore:
                self.c.print(
                    f"Ignoring missing link to {checked_file.filepath} from {missing_backlink}"
                )

