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


def export_github_pac_to_personal_creds_txt(filepath, hardcoded, substring):

    if os.path.isfile(filepath):
        print(f"hi")
        # if the precursor exists:
        if file_contains_substring(filepath, substring):
            # Replace the line starting with:self.github_pac_bash_precursor
            print(f"hi")
        else:
            print(f"hi")
            # append self.github_pac_bash_precursor.
    else:

        # Create the personal_creds file and append:
        output_line = f"{hardcoded.github_pac_bash_precursor}{substring}"


def file_contains_substring(filepath, substring):
    f = open(filepath, "r")
    if substring in f.read():
        return True
    else:
        return False


def replace_line_in_file_if_contains_substringV0(filepath, substring, new_string):

    print(f"hi")
    for line in fileinput.input(filepath, inplace=True):
        # print('{} {}'.format(fileinput.filelineno(), line), end='') # for Python 3
        print(f"line={line}")
        if substring in line:
            line = new_string

        sys.stdout.write(line)
        # print "%d: %s" % (fileinput.filelineno(), line), # for Python 2


def replace_line_in_file_if_contains_substringV1(filepath, substring, new_string):
    print(f"hinew")
    for line in fileinput.FileInput(filepath, inplace=1):
        if substring in line:
            # line = new_string
            print(new_string)
        else:
            print(line)


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
        print(f"file_contents={file_contents}")
        print(f"lines={lines}")
        return False
