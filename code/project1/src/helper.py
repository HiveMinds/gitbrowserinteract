"""Contains functions that are used to help other Python files."""
import getpass
import math
import os
import time

from selenium.webdriver.common.action_chains import ActionChains


def creds_file_contains_gitlab_username(hardcoded):
    """Returns True if the credentials file contains the GitLab username."""
    with open(hardcoded.cred_path, encoding="utf-8") as f:
        lines = []
        for line in f:
            lines.append(line)
    username_identifier = "GITLAB_SERVER_ACCOUNT_GLOBAL="
    for line in lines:
        if line[: len(username_identifier)] == username_identifier:
            return True
    return False


def creds_file_contains_gitlab_pwd(hardcoded):
    """Returns True if the credentials file contains the GitLab pwd."""
    with open(hardcoded.cred_path, encoding="utf-8") as f:
        lines = []
        for line in f:
            lines.append(line)
    pwd_identifier = "GITLAB_SERVER_PASSWORD_GLOBAL="  # nosec
    for line in lines:
        if line[: len(pwd_identifier)] == pwd_identifier:
            return True
    return False


def read_creds(hardcoded):
    """Reads username and password from credentials file, if the file exists,
    asks the user to manually enter them if the file is not found.

    TODO: verify this is not a duplicate method.

    :param hardcoded: An object containing all the hardcoded settings used in this program.
    """
    get_creds_if_not_exist(hardcoded)
    with open(hardcoded.cred_path, encoding="utf-8") as f:
        lines = []
        for line in f:
            lines.append(line)

    # creds.txt is changed to bash format in other project so the credentials need to be parsed
    # username = lines[0][:-1]
    # pwd = lines[1]
    username, pwd = parse_creds(lines)

    return username, pwd


def parse_creds(lines):
    """Gets the GitLab server credentials from the local credentials file.

    :param lines:
    """
    username_identifier = "GITLAB_SERVER_ACCOUNT_GLOBAL="
    pwd_identifier = "GITLAB_SERVER_PASSWORD_GLOBAL="  # nosec
    username = None
    pwd = None
    for line in lines:
        if line[: len(username_identifier)] == username_identifier:
            username = line[len(username_identifier) :]
        if line[: len(pwd_identifier)] == pwd_identifier:
            pwd = line[len(pwd_identifier) :]
    if username is not None:
        if pwd is not None:
            return username, pwd
        raise Exception("Did not get password.")
    raise Exception("Did not get username.")


def get_creds_if_not_exist(hardcoded):
    """Asks the user to enter the username and password for the login to the
    Radboud Universitiy Sports Center login.

    TODO: ask user to include 'read' before username and password,
    to indicate that they read the source code before entering their username
    and password (and verified that it is not shared). Give them a warning about
    security otherwise.

    :param hardcoded: An object containing all the hardcoded settings used in this program.
    """
    if not os.path.isfile(hardcoded.cred_path):
        username = getpass.getpass(prompt="What is your username for GitHub?")
        pwd = getpass.getpass(prompt="What is your password for GitHub?")

        with open(hardcoded.cred_path, "a", encoding="utf-8") as some_file:
            some_file.write(f"{username}\n")
            some_file.write(pwd)
            some_file.close()


def loiter_till_gitlab_server_is_ready_for_login(
    hardcoded, scan_duration, interval_duration, website_controller
):
    """Waits untill a GitLab server is ready for the user to log in.

    :param hardcoded:
    :param scan_duration:
    :param interval_duration:
    :param website_controller:
    """
    # website_controller = Website_controller()

    for _ in range(0, math.ceil(scan_duration / interval_duration)):
        # Refresh page
        try:
            # TODO: get the open_url function from the control_website.py file.
            website_controller.driver = open_url(
                website_controller.driver, hardcoded.gitlab_login_url
            )
            website_controller.driver.implicitly_wait(1)
        # pylint: disable=W0702
        except:
            print("GitLab server was not yet ready to show website")

        print(
            f"Waiting for the GitLab server to get ready for {interval_duration} seconds"
        )
        time.sleep(interval_duration)

        # Break loop if page is succesfully loaded.
        if check_if_login_page_is_loaded(website_controller):
            # GitLab server page is loaded correctly, can move on in script.
            break

    # close website controller
    website_controller.driver.close()
    print(
        "GitLab server is ready for first login. "
        "Code proceeding now to login and get GitLab runner Token."
    )


def check_if_login_page_is_loaded(website_controller):
    """Checks if a GitLab login page is loaded or not.

    :param website_controller:
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
    source = website_controller.driver.page_source
    if error_stage_identifier in source:
        return False
    if too_soon_stage_identifier in source:
        return False
    if ready_stage_identifier in source:
        return True
    if already_logged_in in source:
        return True
    raise Exception(
        "The GitLab server webpage is in a state that is not yet known/"
        + f"recognised, its source code contains:{source}"
    )


def source_contains(website_controller, string):
    """USED Evaluates complete html source of the website that is being
    controlled, to determine if it contains the incoming string. Returns true
    if the string is found in the html source of the website, false if it is
    not found.

    :param website_controller: Object controlling the browser. Object that controls the browser.
    :param string: Set of characters that is searched for in the html code.
    """
    source = website_controller.driver.page_source
    source_contains_string = string in source
    return source_contains_string


def get_browser_drivers(hardcoded):
    """USED Installs wget and then uses that to download the firefox and
    chromium browser controller drivers.

    :param hardcoded: An object containing all the hardcoded settings used in this program.
    """
    os.system("yes | sudo apt install wget")  # nosec

    if not file_is_found(
        f"{hardcoded.firefox_driver_folder}/{hardcoded.firefox_driver_filename}",
    ):
        get_firefox_browser_driver(hardcoded)
        install_firefox_browser()
    if not file_is_found(
        f"{hardcoded.chromium_driver_folder}/{hardcoded.chromium_driver_filename}",
    ):
        get_chromium_browser_driver(hardcoded)


def file_is_found(filepath):
    """Checks if file is found or not.

    :param filepath: param hardcoded: An object containing all the hardcoded
    settings used in this program.
    :param hardcoded:
    """
    return os.path.isfile(filepath)


def get_firefox_browser_driver(hardcoded):
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


def install_firefox_browser():
    """USED."""
    install_firefox_browser_command = "yes | sudo apt install firefox"
    print(f"install_firefox_browser:{install_firefox_browser_command}")
    os.system(install_firefox_browser_command)  # nosec


def get_chromium_browser_driver(hardcoded):
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


def click_element_by_xpath(website_controller, xpath):
    """Clicks an html element based on its xpath.

    :param website_controller: Object controlling the browser. Object that
    controls the browser.
    :param xpath: A direct link to an object in an html page.
    """
    source_element = website_controller.driver.find_element("xpath", xpath)
    if "firefox" in website_controller.driver.capabilities["browserName"]:
        scroll_shim(website_controller.driver, source_element)

    # scroll_shim is just scrolling it into view, you still need to hover over
    # it to click using an action chain.
    actions = ActionChains(website_controller.driver)
    actions.move_to_element(source_element)
    actions.click()
    actions.perform()
    return website_controller


def scroll_shim(passed_in_driver, browser_object):
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


def write_string_to_file(string, output_path):
    """Writes a string to an output file.

    :param string: content you write to file
    :param output_path: Relative path to a file that is outputted.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(string)


def get_runner_registration_token_filepath():
    """Gets the GitLab runner registration token filepath."""
    # get lines from hardcoded data
    lines = read_file_content("../src/hardcoded_variables.txt")
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
    raise Exception("Did not get runner_registration_token_filepath.")


def read_file_content(filepath):
    """

    :param filepath:

    """
    with open(filepath, encoding="utf-8") as f:
        lines = []
        for line in f:
            lines.append(line)
    return lines


def open_url(driver, url):
    """USED # TODO: eliminate duplicate function. Makes the browser open an url
    through the driver object in the webcontroller.

    :param driver: object within website_controller that can controll the driver.
    :param url: A link to a website.
    """
    driver.get(url)
    return driver


def get_value_from_html_source(source, substring, closing_substring):
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
