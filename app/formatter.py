"""Formatter, helps format by columns"""""
try:
    # Python 3
    from itertools import zip_longest
except ImportError:
    # Python 2
    from itertools import izip_longest as zip_longest


class Formatter(object):
    """Main formatter class"""

    @staticmethod
    def sort_by_column(array_of_lines):
        """Sort lines by column, return str with padding for lines

        ex: lines [ ['column1', 'column2'], ['value1', 'value2'] ]
        """
        max_sizes_by_columns = Formatter.collect_max_for_column(array_of_lines)
        result = ""
        for line in array_of_lines:
            result += Formatter.format_line(max_sizes_by_columns, line)
        return result

    @staticmethod
    def format_line(max_sizes_by_columns, line):
        defaultoffset = 4
        result_line = ""
        for index, word in enumerate(line):
            if index < len(line) - 1:
                result_line += word.ljust(max_sizes_by_columns[index] + defaultoffset)
            else:
                result_line += word
        result_line += '\n'
        return result_line

    @staticmethod
    def collect_max_for_column(array_of_lines):
        array_with_sizes_of_words = []
        for line_array in array_of_lines:
            lines_sizes = Formatter.get_words_sizes(line_array)
            array_with_sizes_of_words.append(lines_sizes)
        return [max([i for i in word_len if i is not None]) for word_len in zip_longest(*array_with_sizes_of_words)]

    @staticmethod
    def get_words_sizes(words_array):
        return [len(word) for word in words_array]
