"""Simple worker with files."""


class FileHelper(object):
    """Class which help work with files."""

    @staticmethod
    def differ(file_one, file_two):
        """Files differ if not equal."""
        return not FileHelper.equal(file_one, file_two)

    @staticmethod
    def equal(file_one, file_two):
        """Private: return true if files differ."""
        with open(file_one) as fhandler_one:
            file_one_content = fhandler_one.read()
        with open(file_two) as fhandler_two:
            file_two_content = fhandler_two.read()
        return bool(file_one_content == file_two_content)
