import unittest
import os

from isort import file
from ..src.Main import Main
from ..src.helper import delete_file_if_exists
from ..src.Hardcoded import Hardcoded
from ..src.export_token import add_two as export_token_add_two
from ..src.export_token import file_contains_substring
from ..src.export_token import replace_line_in_file_if_contains_substring
from ..src.export_token import file_content_equals
import testbook


class Test_main(unittest.TestCase):

    # Initialize test object
    def __init__(self, *args, **kwargs):
        super(Test_main, self).__init__(*args, **kwargs)
        self.script_dir = self.get_script_dir()
        self.hc = Hardcoded()
        self.filepath_without_substring = "without_substring.txt"
        self.filepath_with_filepath_at_start = "with_substring_in_start.txt"
        self.filepath_with_filepath_at_middle = "with_substring_in_middle.txt"
        self.filepath_with_filepath_at_end = "with_substring_in_end.txt"
        self.dummy_token = "some_custom_token"
        self.new_line = f"{self.hc.github_pac_bash_precursor}{self.dummy_token}"

        self.without_substring_content = (
            'THISISAFILLER="something"\n' + 'THISISAFILLER="something"\n'
        )
        self.with_substring_content_at_start = (
            f"{self.hc.github_pac_bash_precursor}something_in_start\n"
            + 'THISISAFILLER="something"\n'
            + 'THISISAFILLER="something"\n'
        )
        self.with_substring_content_at_middle = (
            'THISISAFILLER="something"\n'
            + f"{self.hc.github_pac_bash_precursor}something_in_start\n"
            + 'THISISAFILLER="something"\n'
        )
        self.with_substring_content_at_end = (
            'THISISAFILLER="something"\n'
            + 'THISISAFILLER="something"\n'
            + f"{self.hc.github_pac_bash_precursor}something_in_start\n"
        )

        self.expected_without_substring_content = (
            f'THISISAFILLER="something"\n'
            + 'THISISAFILLER="something"\n{self.new_line}'
        )
        self.expected_with_substring_content_at_start = (
            f"{self.hc.github_pac_bash_precursor}{self.dummy_token}\n"
            + 'THISISAFILLER="something"\n'
            + 'THISISAFILLER="something"\n'
        )
        self.expected_with_substring_content_at_middle = (
            'THISISAFILLER="something"\n'
            + f"{self.hc.github_pac_bash_precursor}{self.dummy_token}\n"
            + 'THISISAFILLER="something"\n'
        )
        self.expected_with_substring_content_at_end = (
            'THISISAFILLER="something"\n'
            + 'THISISAFILLER="something"\n'
            + f"{self.hc.github_pac_bash_precursor}{self.dummy_token}\n"
        )

        # Create test files
        # self.create_test_file_with_substring_in_middle()
        # exit()

    # returns the directory of this script regardles of from which level the code is executed
    def get_script_dir(self):
        return os.path.dirname(__file__)

    # tests unit test on addTwo function of main class
    def test_add_two(self):

        expected_result = 5

        actual_result = export_token_add_two(3)
        self.assertEqual(expected_result, actual_result)

    # tests unit test on addTwo function of main class
    def test_add_two_input_four(self):

        expected_result = 6

        actual_result = export_token_add_two(4)
        self.assertEqual(expected_result, actual_result)

    def test_file_contains_without(self):
        self.create_test_file_without_substring()
        self.assertFalse(
            file_contains_substring(
                self.filepath_without_substring, self.hc.github_pac_bash_precursor
            )
        )

    def test_file_contains_with(self):
        self.create_test_file_with_substring_at_start()
        # start
        self.assertTrue(
            file_contains_substring(
                self.filepath_with_filepath_at_start, self.hc.github_pac_bash_precursor
            )
        )
        # middle
        self.create_test_file_with_substring_in_middle()
        self.assertTrue(
            file_contains_substring(
                self.filepath_with_filepath_at_middle, self.hc.github_pac_bash_precursor
            )
        )
        # end
        self.create_test_file_with_substring_in_end()
        self.assertTrue(
            file_contains_substring(
                self.filepath_with_filepath_at_end, self.hc.github_pac_bash_precursor
            )
        )

    def test_file_content_equals_without(self):
        self.create_test_file_without_substring()
        self.assertTrue(
            file_contains_substring(
                self.filepath_without_substring, self.without_substring_content
            )
        )

    def test_file_content_equals_with(self):
        self.create_test_file_with_substring_at_start()
        # start
        self.assertTrue(
            file_content_equals(
                self.filepath_with_filepath_at_start,
                self.with_substring_content_at_start,
            )
        )
        # middle
        self.create_test_file_with_substring_in_middle()
        self.assertTrue(
            file_content_equals(
                self.filepath_with_filepath_at_middle,
                self.with_substring_content_at_middle,
            )
        )
        # end
        self.create_test_file_with_substring_in_end()
        self.assertTrue(
            file_content_equals(
                self.filepath_with_filepath_at_end, self.with_substring_content_at_end
            )
        )

    def test_replace_with_str_at_start(self):
        self.create_test_file_with_substring_at_start()
        # Apply replacement
        filepath = self.filepath_with_filepath_at_start
        substring = self.hc.github_pac_bash_precursor
        new_string = f"{self.hc.github_pac_bash_precursor}{self.dummy_token}"
        print(f"new_string={new_string}")
        replace_line_in_file_if_contains_substring(filepath, substring, new_string)
        self.assertTrue(
            file_contains_substring(self.filepath_with_filepath_at_start, new_string)
        )

    def test_replace_with_str_at_middle(self):
        self.create_test_file_with_substring_in_middle()
        # Apply replacement
        filepath = self.filepath_with_filepath_at_middle
        substring = self.hc.github_pac_bash_precursor
        new_string = f"{self.hc.github_pac_bash_precursor}{self.dummy_token}"
        replace_line_in_file_if_contains_substring(filepath, substring, new_string)
        self.assertTrue(
            file_contains_substring(self.filepath_with_filepath_at_middle, new_string)
        )

    def test_replace_with_str_at_end(self):
        self.create_test_file_with_substring_in_end()
        # 2 Apply replacement
        filepath = self.filepath_with_filepath_at_end
        substring = self.hc.github_pac_bash_precursor
        new_string = f"{self.hc.github_pac_bash_precursor}{self.dummy_token}"
        replace_line_in_file_if_contains_substring(filepath, substring, new_string)
        self.assertTrue(
            file_contains_substring(self.filepath_with_filepath_at_end, new_string)
        )

    def create_test_file_without_substring(self):
        delete_file_if_exists(self.filepath_without_substring)
        with open(self.filepath_without_substring, "w") as f:
            # f.write('THISISAFILLER="something"\n')
            # f.write('THISISAFILLER2="something"\n')
            f.write(self.without_substring_content)
            f.close()

    def create_test_file_with_substring_at_start(self):
        delete_file_if_exists(self.filepath_with_filepath_at_start)
        with open(self.filepath_with_filepath_at_start, "w") as f:
            # f.write(f"{self.hc.github_pac_bash_precursor}something_in_start\n")
            # f.write('THISISAFILLER="something"\n')
            # f.write('THISISAFILLER2="something"\n')
            f.write(self.with_substring_content_at_start)
            f.close()

    def create_test_file_with_substring_in_middle(self):
        delete_file_if_exists(self.filepath_with_filepath_at_middle)
        with open(self.filepath_with_filepath_at_middle, "w") as f:
            # f.write('THISISAFILLER="something"\n')
            # f.write(f"{self.hc.github_pac_bash_precursor}something_in_middle\n")
            # f.write('THISISAFILLER2="something"\n')
            f.write(self.with_substring_content_at_middle)
            f.close()

    def create_test_file_with_substring_in_end(self):
        delete_file_if_exists(self.filepath_with_filepath_at_end)
        with open(self.filepath_with_filepath_at_end, "w") as f:
            # f.write('THISISAFILLER="something"\n')
            # f.write('THISISAFILLER2="something"\n')
            # f.write(f"{self.hc.github_pac_bash_precursor}something_in_end\n")
            f.write(self.with_substring_content_at_end)
            f.close()


if __name__ == "__main__":
    unittest.main()
