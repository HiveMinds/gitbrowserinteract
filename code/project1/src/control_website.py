"""Controls a firefox or chromium browser instance to allow automation of
setting a GitHub SSH deploy key, GitHub personal access token, or getting a
GitLab runner token."""
from getpass import getpass

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .helper import (
    creds_file_contains_gitlab_pwd,
    creds_file_contains_gitlab_username,
    read_creds,
)


def wait_until_page_is_loaded(time_limit_sec: int, driver):
    """Waits untill page is loaded for some time frame."""
    delay = time_limit_sec  # seconds
    try:
        _ = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.CLASS_NAME, "Header-link"))
        )
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")


def gitlab_login(hardcoded, gitlab_username=None, gitlab_pwd=None):
    """Gets the GitLab login."""
    print(f"GOT ={gitlab_pwd}")
    if gitlab_pwd is None or gitlab_username is None:
        gitlab_username, gitlab_pwd = get_gitlab_credentials(
            hardcoded, "GitLab", gitlab_username, gitlab_pwd
        )
        if gitlab_username is None:
            raise Exception("Did not get Username.")
        if gitlab_pwd is None:
            raise Exception("Did not get pwd.")
    driver = login(
        hardcoded,
        hardcoded.gitlab_login_url,
        hardcoded.gitlab_user_element_id,
        hardcoded.gitlab_pw_element_id,
        hardcoded.gitlab_signin_button_xpath,
        gitlab_username,
        gitlab_pwd,
        "GitLab",
    )
    return driver, gitlab_username, gitlab_pwd


def get_gitlab_credentials(
    hardcoded, company, gitlab_username=None, gitlab_pwd=None
):
    """Gets  credentials from a hardcoded file and asks the user for them if
    they are not found.

    # TODO: export the credentials of the user if the user grants permission for that.

    :param hardcoded: An object containing all the hardcoded settings used in this program.
    """
    if (
        hardcoded.use_cred_file
        and creds_file_contains_gitlab_username(hardcoded)
        and creds_file_contains_gitlab_pwd(hardcoded)
    ):
        gitlab_username, gitlab_pwd = read_creds(hardcoded)
    else:
        if gitlab_username is None:
            gitlab_username = get_username(company)
        if gitlab_pwd is None:
            gitlab_pwd = get_pwd(company)
    return gitlab_username, gitlab_pwd


def get_username(company):
    """Gets the username for login and returns it."""
    username = getpass(
        f"\nPlease enter your {company} Username: \n(you can also manually log"
        + f" into {company},\n and fill in nonsense in this field,\n if you"
        + " prefer typing your Username into GitHub directly.)\n"
    )
    if username in ["nonsense", "Nonsense"]:
        print("That is funny. This is unprofessional.")
    return username


def get_pwd(company):
    """Gets the password for login and returns it."""
    pwd = getpass(
        f"Please enter your {company} Password \n(you can also manually log "
        + "into {company},\n and fill in gibberish in this field,\n if you "
        + "prefer typing your Password into GitHub directly.)\n"
    )
    return pwd
