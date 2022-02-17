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
from ..src.export_token import append_line
from ..src.export_token import export_github_pac_to_personal_creds_txt
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
            + f'THISISAFILLER="something"\n{self.new_line}'
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

    # tests unit test on addTwo function in the file that is being tested.
    def test_add_two_input_four(self):

        expected_result = 6

        actual_result = export_token_add_two(4)
        self.assertEqual(expected_result, actual_result)

    # Assert the file_contains_substring returns False if a substring is not
    # contained in a file.
    def test_file_contains_without(self):
        self.create_test_file_without_substring()
        self.assertFalse(
            file_contains_substring(
                self.filepath_without_substring, self.hc.github_pac_bash_precursor
            )
        )

    # Assert the file_contains_substring returns True if a substring is
    # contained in a file. Does this for all 3 test files that contain the
    # substring (start, middle, end).
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

    # Asserts the file content of the test files are identified as equal before
    # they are modified. For the without testfile.
    def test_file_content_equals_without(self):
        self.create_test_file_with_substring_at_start()
        # start
        self.assertTrue(
            file_content_equals(
                self.filepath_without_substring,
                self.without_substring_content,
            )
        )

    # Asserts the file content of the test files are identified as equal before
    # they are modified. For the start, middle and end testfiles.
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

    # Tests whether the append_line indeed appends a target line in start file,
    # by checking whether the file contains the target line.
    def test_append_line_without(self):
        self.create_test_file_without_substring()
        # Apply replacement
        filepath = self.filepath_without_substring
        new_string = f"{self.hc.github_pac_bash_precursor}{self.dummy_token}"
        append_line(filepath, new_string)
        self.assertTrue(
            file_contains_substring(self.filepath_without_substring, new_string)
        )

    # Tests whether the replace_line_in_file_if_contains_substring indeed
    # replaces a target line in start file, by checking whether the file
    # contains the target line.
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

    # Tests whether the replace_line_in_file_if_contains_substring indeed
    # replaces a target line in middle file, by checking whether the file
    # contains the target line.
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

    # Tests whether the replace_line_in_file_if_contains_substring indeed
    # replaces a target line in end file, by checking whether the file
    # contains the target line.
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

    # Tests whether the append_line indeed appends a target line in start file,
    # by checking whether the file contains the target line. And by verifying
    # its file contents.
    def test_append_line_without_on_filecontent(self):
        self.create_test_file_without_substring()
        # Apply replacement
        filepath = self.filepath_without_substring
        new_string = f"{self.hc.github_pac_bash_precursor}{self.dummy_token}"
        print(f"new_string={new_string}")
        append_line(filepath, new_string)
        self.assertTrue(
            file_contains_substring(self.filepath_without_substring, new_string)
        )
        self.assertTrue(
            file_content_equals(
                self.filepath_without_substring,
                self.expected_without_substring_content,
            )
        )

    # Tests whether the replace_line_in_file_if_contains_substring indeed
    # replaces a target line in start file, by checking file content equality.
    def test_replace_with_str_at_start_entire_filecontent(self):
        self.create_test_file_with_substring_at_start()
        # Apply replacement
        filepath = self.filepath_with_filepath_at_start
        substring = self.hc.github_pac_bash_precursor
        new_string = f"{self.hc.github_pac_bash_precursor}{self.dummy_token}"
        replace_line_in_file_if_contains_substring(filepath, substring, new_string)
        self.assertTrue(
            file_contains_substring(self.filepath_with_filepath_at_start, new_string)
        )
        self.assertTrue(
            file_content_equals(
                self.filepath_with_filepath_at_start,
                self.expected_with_substring_content_at_start,
            )
        )

    # Tests whether the replace_line_in_file_if_contains_substring indeed
    # replaces a target line in middle file, by checking file content equality.
    def test_replace_with_str_at_middle_entire_filecontent(self):
        self.create_test_file_with_substring_in_middle()
        # Apply replacement
        filepath = self.filepath_with_filepath_at_middle
        substring = self.hc.github_pac_bash_precursor
        new_string = f"{self.hc.github_pac_bash_precursor}{self.dummy_token}"
        replace_line_in_file_if_contains_substring(filepath, substring, new_string)
        self.assertTrue(
            file_contains_substring(self.filepath_with_filepath_at_middle, new_string)
        )
        self.assertTrue(
            file_content_equals(
                self.filepath_with_filepath_at_middle,
                self.expected_with_substring_content_at_middle,
            )
        )

    # Tests whether the replace_line_in_file_if_contains_substring indeed
    # replaces a target line in end file, by checking file content equality.
    def test_replace_with_str_at_end_entire_filecontent(self):
        self.create_test_file_with_substring_in_end()
        # 2 Apply replacement
        filepath = self.filepath_with_filepath_at_end
        substring = self.hc.github_pac_bash_precursor
        new_string = f"{self.hc.github_pac_bash_precursor}{self.dummy_token}"
        replace_line_in_file_if_contains_substring(filepath, substring, new_string)
        self.assertTrue(
            file_contains_substring(self.filepath_with_filepath_at_end, new_string)
        )
        self.assertTrue(
            file_content_equals(
                self.filepath_with_filepath_at_end,
                self.expected_with_substring_content_at_end,
            )
        )

    ## Test function that outputs token in all circumstances.
    # Tests whether the export_github_pac_to_personal_creds_txt outputs the
    # GitHub personal access token if it is not yet in the output file.
    def test_export_github_pac_to_personal_creds_txt_without(self):
        self.create_test_file_without_substring()
        # Apply replacement
        filepath = self.filepath_without_substring
        export_github_pac_to_personal_creds_txt(filepath, self.hc, self.dummy_token)
        self.assertTrue(
            file_contains_substring(self.filepath_without_substring, self.dummy_token)
        )
        self.assertTrue(
            file_content_equals(
                self.filepath_without_substring,
                self.expected_without_substring_content,
            )
        )

    # Tests whether the replace_line_in_file_if_contains_substring indeed
    # replaces a target line in start file, by checking file content equality.
    def test_export_github_pac_to_personal_creds_txt_start(self):
        self.create_test_file_with_substring_at_start()
        # Apply replacement
        filepath = self.filepath_with_filepath_at_start
        export_github_pac_to_personal_creds_txt(filepath, self.hc, self.dummy_token)
        self.assertTrue(
            file_contains_substring(
                self.filepath_with_filepath_at_start, self.dummy_token
            )
        )
        self.assertTrue(
            file_content_equals(
                self.filepath_with_filepath_at_start,
                self.expected_with_substring_content_at_start,
            )
        )

    # Tests whether the replace_line_in_file_if_contains_substring indeed
    # replaces a target line in middle file, by checking file content equality.
    def test_export_github_pac_to_personal_creds_txt_middle(self):
        self.create_test_file_with_substring_in_middle()
        # Apply replacement
        filepath = self.filepath_with_filepath_at_middle
        export_github_pac_to_personal_creds_txt(filepath, self.hc, self.dummy_token)
        self.assertTrue(
            file_contains_substring(
                self.filepath_with_filepath_at_middle, self.dummy_token
            )
        )
        self.assertTrue(
            file_content_equals(
                self.filepath_with_filepath_at_middle,
                self.expected_with_substring_content_at_middle,
            )
        )

    # Tests whether the replace_line_in_file_if_contains_substring indeed
    # replaces a target line in end file, by checking file content equality.
    def export_github_pac_to_personal_creds_txt_end(self):
        self.create_test_file_with_substring_in_end()
        # 2 Apply replacement
        filepath = self.filepath_with_filepath_at_end
        export_github_pac_to_personal_creds_txt(filepath, self.hc, self.dummy_token)
        self.assertTrue(
            file_contains_substring(
                self.filepath_with_filepath_at_end, self.dummy_token
            )
        )
        self.assertTrue(
            file_content_equals(
                self.filepath_with_filepath_at_end,
                self.expected_with_substring_content_at_end,
            )
        )

    ## Create test files function.
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
