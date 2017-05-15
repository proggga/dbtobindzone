"""Formatter, helps format by columns"""""
import re
try:
    # Python 2
    from itertools import izip_longest as zip_longest
except ImportError:
    # Python 3
    from itertools import zip_longest


class Formatter(object):
    """Main formatter class"""

    @staticmethod
    def sort_str_by_column(string_to_sort):
        """Format string method by columns"""
        lines = string_to_sort.split('\n')
        if lines and lines[-1] == '':
            lines.pop()
        lines_array_split_by_word = []
        for raw_line in lines:
            without_tabs_line = re.sub(r'\t+', ' ', raw_line)
            line = re.sub(r' +', ' ', without_tabs_line)
            lines_splited_by_word = line.split(' ')
            if lines_splited_by_word and lines_splited_by_word[-1] == '':
                lines_splited_by_word.pop()
            if lines_splited_by_word and lines_splited_by_word[0] == '':
                lines_splited_by_word.pop(0)
            lines_array_split_by_word.append(lines_splited_by_word)
        return Formatter.sort_by_column(lines_array_split_by_word)

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
        """Format lines with by sizes table"""
        defaultoffset = 4
        result_line = ""
        for index, word in enumerate(line):
            if index < len(line) - 1:
                result_line += word.ljust(max_sizes_by_columns[index]
                                          + defaultoffset)
            else:
                result_line += word
        result_line += '\n'
        return result_line

    @staticmethod
    def collect_max_for_column(array_of_lines):
        """collect max line words by column"""
        array_with_sizes_of_words = []
        for line_array in array_of_lines:
            lines_sizes = Formatter.get_words_sizes(line_array)
            array_with_sizes_of_words.append(lines_sizes)
        zipped = zip_longest(*array_with_sizes_of_words)
        zipped_without_none = [[i for i in word_len if i is not None]
                               for word_len in zipped]
        return [max(words) for words in zipped_without_none]

    @staticmethod
    def get_words_sizes(words_array):
        """Get word sizes array"""
        return [len(word) for word in words_array]
