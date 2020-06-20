from rich.console import Console
from jottingspool import files


class Interface(object):
    """User interface for knowledge repository"""
    def __init__(self, path: str):
        """
        Setup
        
        Args:
        path: either a markdown file or a directory containing markdown files.
        """
        self.path = path
        self.c = Console()

    def run(self):
        self.find_files()
        self.get_ignores()
        self.check_files()
        self.correct_files()
        self.write_ignores()

    def find_files(self):
        self.directory, self.markdown_files = files.file_or_dir(self.path)

    def get_ignores(self):
        self.ignores = files.read_ignores(self.directory)

    def check_files(self):
        self.checks = files.check_files(self.markdown_files)

    def correct_files(self):
        for check in self.checks:
            self.create_missing(check)
            self.create_backlinks(check)

    def write_ignores(self):
        files.write_ignores(self.directory, self.ignores)

    def create_missing(self, checked_file: files.FileInformation):
        if self.is_missing(checked_file):
            for missing_reference in checked_file.missinglinks:
                if self.ask_user_about_missing(checked_file,
                                               missing_reference):
                    files.correct_missing(checked_file, missing_reference)

    def create_backlinks(self, checked_file: files.FileInformation):
        if self.has_missing_backlinks(checked_file):
            for missing_backlink in checked_file.missingbacklinks:
                backlink_ignore_description = files.BacklinkIgnores(
                    referenced_file=checked_file.filepath,
                    backlink_path=missing_backlink)
                if not self.should_ignore_backlink(
                        backlink_ignore_description):
                    self.ask_user_about_backlink(checked_file,
                                                 missing_backlink,
                                                 backlink_ignore_description)

    @staticmethod
    def is_missing(check: files.FileInformation) -> bool:
        return len(check.missinglinks) > 0

    @staticmethod
    def has_missing_backlinks(checked_file: files.FileInformation) -> bool:
        return len(checked_file.missingbacklinks) > 0

    def ask_user_about_missing(self, check: files.FileInformation,
                               missing_reference: str) -> bool:
        prompt = f"{check.filepath} references missing file {missing_reference}, create it?(yN) "
        return self.check_input_default_no(prompt)

    def check_input_default_no(self, prompt: str) -> bool:
        userinput = self.c.input(prompt)
        return self.user_input_default_no_logic(userinput)

    @staticmethod
    def user_input_default_no_logic(userinput: str) -> bool:
        if userinput == "":
            return False
        if userinput.lower()[0] == "y":
            return True
        else:
            return False

    def should_ignore_backlink(
            self, backlink_ignore_description: files.BacklinkIgnores) -> bool:
        return backlink_ignore_description in self.ignores

    def ask_user_about_backlink(
            self, checked_file: files.FileInformation, missing_backlink: str,
            backlink_ignore_description: files.BacklinkIgnores):
        prompt = f"{checked_file.filepath} is referenced by {missing_backlink}.\nShould I add the link in at the end of {missing_backlink}? (yN)"
        should_add_link = self.check_input_default_no(prompt)
        if should_add_link:
            files.add_missing_backlink(checked_file, missing_backlink)
        if not should_add_link:
            prompt = f"Would you like to ignore this warning in future? (yN)"
            should_add_ignore = self.check_input_default_no(prompt)
            if should_add_ignore:
                self.ignores.append(backlink_ignore_description)
