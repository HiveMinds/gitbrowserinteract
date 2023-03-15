"""Contains functions that are used to help other Python files."""
import math
import os
import time
from getpass import getpass
from typing import Any, List

from typeguard import typechecked

from src.gitbrowserinteract import Hardcoded


@typechecked
def loiter_till_gitlab_server_is_ready_for_login(
    *,
    hardcoded: Hardcoded,
    scan_duration: int,
    interval_duration: int,
    driver: Any,
) -> None:
    """Waits untill a GitLab server is ready for the user to log in.

    :param hardcoded:
    :param scan_duration:
    :param interval_duration:
    :param driver:
    """
    # driver = driver()

    for _ in range(0, math.ceil(scan_duration / interval_duration)):
        # Refresh page
        try:
            # TODO: get the open_url function from the control_website.py file.
            driver = open_url(driver=driver, url=hardcoded.gitlab_login_url)
            driver.implicitly_wait(1)
        # pylint: disable=W0702
        except:
            print("GitLab server was not yet ready to show website")

        print(
            f"Waiting for the GitLab server to get ready for {interval_duration} seconds"
        )
        time.sleep(interval_duration)

        # Break loop if page is succesfully loaded.
        if check_if_gitlab_login_page_is_loaded(driver=driver):
            # GitLab server page is loaded correctly, can move on in script.
            break

    # close website controller
    driver.close()
    print(
        "GitLab server is ready for first login. "
        "Code proceeding now to login and get GitLab runner Token."
    )


@typechecked
def check_if_gitlab_login_page_is_loaded(*, driver: Any) -> bool:
    """Checks if a GitLab login page is loaded or not.

    :param driver:
    """
    # This identifier only occurs in the first, and not-yet-ready stage.
    error_stage_identifier = (
        "The connection to the server was reset while the page was loading."
    )

    # This identifier only occurs in the second, and not-yet-ready stage.
    too_soon_stage_identifier = "GitLab is taking too much time to respond."

    # This identifier only occurs in the second, and ready stage.
    ready_stage_identifier = "Sign in"

    # Already logged into GitLab
    already_logged_in = "<title>Projects · Dashboard · GitLab</title>"

    # Verify if that condition is met.
    source = driver.page_source
    if error_stage_identifier in source:
        return False
    if too_soon_stage_identifier in source:
        return False
    if ready_stage_identifier in source:
        return True
    if already_logged_in in source:
        return True
    raise ValueError(
        "The GitLab server webpage is in a state that is not yet known/"
        + f"recognised, its source code contains:{source}"
    )


@typechecked
def file_is_found(*, filepath: str) -> bool:
    """Checks if file is found or not.

    :param filepath: param hardcoded: An object containing all the hardcoded
    settings used in this program.
    :param hardcoded:
    """
    return os.path.isfile(filepath)


@typechecked
def get_firefox_browser_driver(*, hardcoded: Hardcoded) -> None:
    """USED Creates a folder to store the firefox browser controller downloader
    and then downloads it into that.

    :param hardcoded: An object containing all the hardcoded settings used in this program.
    """
    # TODO: include os identifier and select accompanying file
    os.system(f"mkdir {hardcoded.firefox_driver_folder}")  # nosec
    curl_firefox_drive = (
        f"wget -O {hardcoded.firefox_driver_folder}/"
        + f"{hardcoded.firefox_driver_tarname} {hardcoded.firefox_driver_link}"
    )
    os.system(curl_firefox_drive)  # nosec
    # unpack_firefox_driver = (
    #    f"tar -xf {hardcoded.firefox_driver_folder}/{hardcoded.firefox_driver_tarname}"
    # )
    unpack_firefox_driver = (
        f"tar -xf {hardcoded.firefox_driver_folder}/"
        + f"{hardcoded.firefox_driver_tarname} -C "
        + f"{hardcoded.firefox_driver_folder}/"
    )
    print(f"unpacking with:{unpack_firefox_driver}")
    os.system(unpack_firefox_driver)  # nosec


@typechecked
def install_firefox_browser() -> None:
    """USED."""
    install_firefox_browser_command = "sudo apt install firefox --yes"
    print(f"install_firefox_browser:{install_firefox_browser_command}")
    os.system(install_firefox_browser_command)  # nosec


@typechecked
def get_chromium_browser_driver(*, hardcoded: Hardcoded) -> None:
    """Creates a folder to store the chromium browser controller downloader and
    then downloads it into that.
    TODO: include os identifier and select accompanying file

    :param hardcoded: An object containing all the hardcoded settings used in this program.

    """
    # mak dir
    os.system(f"mkdir {hardcoded.chromium_driver_folder}")  # nosec
    # get the zip
    curl_chromium_drive = (
        f"wget -O {hardcoded.chromium_driver_folder}/"
        + f"{hardcoded.chromium_driver_tarname} "
        + f"{hardcoded.chromium_driver_link}"
    )
    os.system(curl_chromium_drive)  # nosec
    # unpak the zip
    unpack_chromium_driver = (
        f"unzip -d  {hardcoded.chromium_driver_folder}/"
        + f"{hardcoded.chromium_driver_filename} "
        + f"{hardcoded.chromium_driver_folder}/"
        + f"{hardcoded.chromium_driver_tarname}"
    )
    os.system(unpack_chromium_driver)  # nosec

    # move file one dir up
    move_chromium_driver = (
        f"mv  {hardcoded.chromium_driver_folder}/"
        + f"{hardcoded.chromium_driver_filename}/"
        + f"{hardcoded.chromium_driver_unmodified_filename} "
        + f"{hardcoded.chromium_driver_folder}"
    )
    print(move_chromium_driver)
    os.system(move_chromium_driver)  # nosec
    # remove unpacked dir
    cleanup = (
        f"rm -r {hardcoded.chromium_driver_folder}/"
        + f"{hardcoded.chromium_driver_filename}"
    )
    print(cleanup)
    os.system(cleanup)  # nosec

    # remove zip file
    cleanup = (
        f"rm -r {hardcoded.chromium_driver_folder}/"
        + f"{hardcoded.chromium_driver_tarname}"
    )
    print(cleanup)
    os.system(cleanup)  # nosec

    # rename driver file name to include hardcoded version name
    rename_chromium_driver = (
        f"mv  {hardcoded.chromium_driver_folder}/"
        + f"{hardcoded.chromium_driver_unmodified_filename} "
        + f"{hardcoded.chromium_driver_folder}/"
        + f"{hardcoded.chromium_driver_filename}"
    )
    print(rename_chromium_driver)
    os.system(rename_chromium_driver)  # nosec


@typechecked
def scroll_shim(*, passed_in_driver: Any, browser_object: Any) -> None:
    """Scrolls down till object is found.

    :param passed_in_driver: An object within the object that controls an internet browser.
    :param object: Unknown, most likely an arbitrary html object..
    """
    x = browser_object.location["x"]
    y = browser_object.location["y"]
    scroll_by_coord = f"window.scrollTo({x},{y});"
    scroll_nav_out_of_way = "window.scrollBy(0, -120);"
    passed_in_driver.execute_script(scroll_by_coord)
    passed_in_driver.execute_script(scroll_nav_out_of_way)


@typechecked
def write_string_to_file(*, string: str, output_path: str) -> None:
    """Writes a string to an output file.

    :param string: content you write to file
    :param output_path: Relative path to a file that is outputted.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(string)


@typechecked
def get_runner_registration_token_filepath() -> str:
    """Gets the GitLab runner registration token filepath."""
    # get lines from hardcoded data
    lines = read_file_content(filepath="../src/hardcoded_variables.txt")
    runner_registration_token_filepath_identifier = (
        "RUNNER_REGISTRATION_TOKEN_FILEPATH="  # nosec
    )
    runner_registration_token_filepath = None
    for line in lines:
        if (
            line[: len(runner_registration_token_filepath_identifier)]
            == runner_registration_token_filepath_identifier
        ):
            runner_registration_token_filepath = line[
                len(runner_registration_token_filepath_identifier) :
            ]
    if runner_registration_token_filepath is not None:
        # remove newline character
        print(f"FILEPATH=../{runner_registration_token_filepath.strip()}")
        return f"../{runner_registration_token_filepath.strip()}"
    raise ValueError("Did not get runner_registration_token_filepath.")


@typechecked
def read_file_content(*, filepath: str) -> List[str]:
    """

    :param filepath:

    """
    with open(filepath, encoding="utf-8") as f:
        lines = []
        for line in f:
            lines.append(line)
    return lines


@typechecked
def open_url(*, driver: Any, url: str) -> Any:
    """USED # TODO: eliminate duplicate function. Makes the browser open an url
    through the driver object in the webcontroller.

    :param driver: object within driver that can controll the driver.
    :param url: A link to a website.
    """
    driver.get(url)
    return driver


@typechecked
def get_value_from_html_source(
    *, source: str, substring: str, closing_substring: str
) -> str:
    """Returns value from html source code.

    :param source: Source code of website that is being controlled.
    :param substring::param substring: A substring that is sought.
    :param closing_substring: A substring that indicates the end of text that is searched.
    """
    nr_of_pages_index = source.find(substring) + len(substring)
    # print(f'nr_of_pages_index={nr_of_pages_index}')
    closing_quotation = source.find(closing_substring, nr_of_pages_index)
    # print(f'closing_quotation={closing_quotation}')
    # print(f'nr={source[nr_of_pages_index:closing_quotation]}')
    value = source[nr_of_pages_index:closing_quotation]
    return value


@typechecked
def get_username(*, company: str) -> str:
    """Gets the username for login and returns it."""
    username = getpass(
        f"\nPlease enter your {company} Username: \n(you can also manually log"
        + f" into {company},\n and fill in nonsense in this field,\n if you"
        + " prefer typing your Username into GitHub directly.)\n"
    )
    if username in ["nonsense", "Nonsense"]:
        print("That is funny. This is unprofessional.")
    return username


@typechecked
def get_pwd(*, company: str) -> str:
    """Gets the password for login and returns it."""
    pwd = getpass(
        f"Please enter your {company} Password \n(you can also manually log "
        + "into {company},\n and fill in gibberish in this field,\n if you "
        + "prefer typing your Password into GitHub directly.)\n"
    )
    return pwd
