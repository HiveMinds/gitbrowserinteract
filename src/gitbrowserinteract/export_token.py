"""Exports a GitHub personal access token to the personal credentials file."""
import os
import shutil

from typeguard import typechecked

from .Hardcoded import Hardcoded


@typechecked
def export_github_pac_to_personal_creds_txt(
    *, filepath: str, hardcoded: Hardcoded, pac: str
) -> None:
    """

    :param filepath:
    :param hardcoded:
    :param pac:

    """
    new_line = f"{hardcoded.github_pac_bash_precursor}{pac}"
    if os.path.isfile(filepath):
        print(f"File exists,new_line={new_line}")
        # if the precursor exists:
        if file_contains_substring(
            filepath=filepath, substring=hardcoded.github_pac_bash_precursor
        ):
            # Replace the line starting with:self.github_pac_bash_precursor
            replace_line_in_file_if_contains_substring(
                filepath=filepath,
                substring=hardcoded.github_pac_bash_precursor,
                new_string=new_line,
            )
        else:
            append_line(filepath=filepath, line=new_line)
    else:
        append_line(filepath=filepath, line=new_line)


@typechecked
def append_line(*, filepath: str, line: str) -> None:
    """

    :param filepath:
    :param line:

    """
    print(f"line={line}")
    with open(filepath, "a", encoding="utf-8") as fd:
        fd.write(f"{line}")


@typechecked
def file_contains_substring(*, filepath: str, substring: str) -> bool:
    """

    :param filepath:
    :param substring:

    """
    with open(filepath, encoding="utf-8") as f:
        if substring in f.read():
            return True
        return False


@typechecked
def replace_line_in_file_if_contains_substring(
    *, filepath: str, substring: str, new_string: str
) -> None:
    """

    :param filepath:
    :param substring:
    :param new_string:

    """
    with open(filepath, encoding="utf-8") as old, open(
        "newtest", "w", encoding="utf-8"
    ) as new:
        for line in old:
            if substring in line:
                # NOTE: adds new line to substring.
                new.write(f"{new_string}\n")
            else:
                new.write(line)
    shutil.move("newtest", filepath)
