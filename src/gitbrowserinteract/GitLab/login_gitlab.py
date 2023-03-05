"""Performs GitLab login."""
import getpass
import os
import time

from browsercontroller.get_controller import get_ubuntu_apt_firefox_controller
from browsercontroller.helper import click_element_by_xpath
from typeguard import typechecked

from src.gitbrowserinteract.helper import get_pwd, get_username


@typechecked
def gitlab_login(*, hardcoded, gitlab_username=None, gitlab_pwd=None):
    """Gets the GitLab login."""
    print(f"gitlab_username={gitlab_username}")
    print(f"gitlab_pwd={gitlab_pwd}")
    if gitlab_pwd is None or gitlab_username is None:
        gitlab_username, gitlab_pwd = get_gitlab_credentials(
            hardcoded=hardcoded,
            gitlab_username=gitlab_username,
            gitlab_pwd=gitlab_pwd,
        )
        if gitlab_username is None:
            raise ValueError("Did not get Username.")
        if gitlab_pwd is None:
            raise ValueError("Did not get pwd.")

    # Go to extension settings.
    driver = get_ubuntu_apt_firefox_controller(
        url=hardcoded.gitlab_login_url, default_profile=True
    )
    time.sleep(5)

    # TODO: create buffer for alternative tabs that need to be closed.

    driver.implicitly_wait(6)
    username_input = driver.find_element(
        "id",
        hardcoded.gitlab_user_element_id,
    )
    password_input = driver.find_element(
        "id",
        hardcoded.gitlab_pw_element_id,
    )

    # Check to determine whether the user has already manually
    # logged into GitHub, if so, skip setting username and pwd and clicking
    # the login button.
    user_has_manually_logged_in = user_is_logged_in_in_gitlab(
        hardcoded=hardcoded, driver=driver
    )
    if not user_has_manually_logged_in:
        username_input.send_keys(gitlab_username)
        password_input.send_keys(gitlab_pwd)
        driver.implicitly_wait(15)

        # driver.find_element("css selector",".btn-primary").click()
        click_element_by_xpath(
            driver,
            hardcoded.gitlab_signin_button_xpath,
        )

    # Wait till login completed
    time.sleep(5)

    return driver, gitlab_username, gitlab_pwd


@typechecked
def get_gitlab_credentials(
    *, hardcoded, gitlab_username=None, gitlab_pwd=None
):
    """Gets  credentials from a hardcoded file and asks the user for them if
    they are not found.

    # TODO: export the credentials of the user if the user grants permission for that.

    :param hardcoded: An object containing all the hardcoded settings used in this program.
    """
    if (
        hardcoded.use_cred_file
        and creds_file_contains_gitlab_username(hardcoded=hardcoded)
        and creds_file_contains_gitlab_pwd(hardcoded=hardcoded)
    ):
        gitlab_username, gitlab_pwd = read_gitlab_creds(hardcoded=hardcoded)
    else:
        if gitlab_username is None:
            gitlab_username = get_username(company="GitLab")
        if gitlab_pwd is None:
            gitlab_pwd = get_pwd(company="GitLab")
    return gitlab_username, gitlab_pwd


@typechecked
def user_is_logged_in_in_gitlab(*, hardcoded, driver):
    """Returns True if the user is logged in, False otherwise."""
    source = driver.page_source
    if hardcoded.gitlab_logged_in_or_not_string in source:
        return True
    return False


@typechecked
def creds_file_contains_gitlab_username(*, hardcoded):
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


@typechecked
def creds_file_contains_gitlab_pwd(*, hardcoded):
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


@typechecked
def read_gitlab_creds(*, hardcoded):
    """Reads username and password from credentials file, if the file exists,
    asks the user to manually enter them if the file is not found.

    TODO: verify this is not a duplicate method.

    :param hardcoded: An object containing all the hardcoded settings used in this program.
    """
    get_gitlab_creds_if_not_exist(hardcoded=hardcoded)
    with open(hardcoded.cred_path, encoding="utf-8") as f:
        lines = []
        for line in f:
            lines.append(line)

    # creds.txt is changed to bash format in other project so the credentials need to be parsed
    # username = lines[0][:-1]
    # pwd = lines[1]
    username, pwd = parse_gitlab_creds(lines=lines)

    return username, pwd


@typechecked
def get_gitlab_creds_if_not_exist(*, hardcoded):
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


@typechecked
def parse_gitlab_creds(*, lines):
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
        raise ValueError("Did not get password.")
    raise ValueError("Did not get username.")
