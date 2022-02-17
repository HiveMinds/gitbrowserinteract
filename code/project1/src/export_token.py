import getpass
import os
import time
import math


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


def replace_line_in_file_if_contains_substring():
    print(f"hi")
