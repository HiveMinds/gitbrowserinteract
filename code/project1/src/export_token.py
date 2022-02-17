import getpass
import os
import sys
import time
import math
import fileinput

import shutil


def add_two(x):
    """Adds two to an incoming integer.

    :param x:

    """
    return x + 2


def export_github_pac_to_personal_creds_txt(filepath, hardcoded, pac):
    new_line = f"{hardcoded.github_pac_bash_precursor}{pac}"
    if os.path.isfile(filepath):
        print(f"File exists,new_line={new_line}")
        # if the precursor exists:
        if file_contains_substring(filepath, hardcoded.github_pac_bash_precursor):
            # Replace the line starting with:self.github_pac_bash_precursor
            replace_line_in_file_if_contains_substring(
                filepath, hardcoded.github_pac_bash_precursor, new_line
            )
        else:
            print(f"hi")
            append_line(filepath, new_line)
    else:
        append_line(filepath, new_line)


def append_line(filepath, line):
    print(f"line={line}")
    with open(filepath, "a") as fd:
        fd.write(f"{line}")


def file_contains_substring(filepath, substring):
    f = open(filepath, "r")
    if substring in f.read():
        return True
    else:
        return False


def replace_line_in_file_if_contains_substring(filepath, substring, new_string):
    with open(filepath) as old, open("newtest", "w") as new:
        for line in old:
            if substring in line:
                # NOTE: adds new line to substring.
                new.write(f"{new_string}\n")
            else:
                new.write(line)
    shutil.move("newtest", filepath)


def file_content_equals(filepath, lines):
    # This is how you should open files
    with open(filepath, "r") as f:
        # Get the entire contents of the file
        file_contents = f.read()

        # Remove any whitespace at the end, e.g. a newline
        # file_contents = file_contents.strip()
    if file_contents == lines:
        return True
    else:
        print(f"actual content=\n\n{file_contents}")
        print(f"expected content=\n\n{lines}")
        return False
