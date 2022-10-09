"""Controls a firefox or chromium browser instance to allow automation of
setting a GitHub SSH deploy key, GitHub personal access token, or getting a
GitLab runner token."""
import time
from code.project1.src.ask_user_input import ask_two_factor_code
from getpass import getpass

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .helper import (
    click_element_by_xpath,
    creds_file_contains_gitlab_pwd,
    creds_file_contains_gitlab_username,
    open_url,
    read_creds,
    source_contains,
)
from .Website_controller import Website_controller


def github_login(hardcoded, github_pwd=None, github_username=None):
    """Completes GitHub login."""
    website_controller = login(
        hardcoded,
        hardcoded.github_login_url,
        hardcoded.github_user_element_id,
        hardcoded.github_pw_element_id,
        hardcoded.github_signin_button_xpath,
        github_username,
        github_pwd,
        "GitHub",
    )
    return website_controller


# pylint: disable=R0913
def login(
    hardcoded,
    login_url,
    user_element_id,
    pw_element_id,
    signin_button_xpath,
    username,
    pwd,
    company,
):
    """Performs login of user into  website. Returns the website_controller
    object.

    :param hardcoded: An object containing all the hardcoded settings used in this program.
    """

    website_controller = Website_controller()
    website_controller.driver = open_url(website_controller.driver, login_url)
    website_controller.driver.implicitly_wait(6)
    username_input = website_controller.driver.find_element(
        "id", user_element_id
    )
    password_input = website_controller.driver.find_element(
        "id", pw_element_id
    )

    if username is None:
        username = get_username(company)
    if pwd is None:
        pwd = get_pwd(company)
    else:
        user_passed_pwd_earlier = True

    # TODO: Include check to determine whether the user has already manually
    # logged into GitHub, if so, skip setting username and pwd and clicking
    # the login button.
    user_has_manually_logged_in = user_is_logged_in(
        hardcoded, website_controller, company
    )
    if not user_has_manually_logged_in:
        username_input.send_keys(username)
        password_input.send_keys(pwd)
        website_controller.driver.implicitly_wait(15)

        # website_controller.driver.find_element("css selector",".btn-primary").click()
        click_element_by_xpath(
            website_controller,
            signin_button_xpath,
        )

    # Wait till login completed
    time.sleep(5)

    complete_github_two_factor_auth(hardcoded, website_controller)
    if not user_is_logged_in(hardcoded, website_controller, company):
        print(
            "Hi, we were not able to verify you are logged in, (which is "
            + "needed"
            + " to add the ssh-deploy key).\n We will now try again. To "
            + "break this"
            + " loop, press CTRL+C.\n\n"
        )
        website_controller.driver.close()
        website_controller = None
        if user_passed_pwd_earlier:
            raise Exception(
                "Error, you have passed the wrong password to this method, (or"
                + " GitHub is changed/down). Please try again with the correct "
                + "GitHub pwd, or manually log in."
            )
        return login(
            hardcoded,
            login_url,
            user_element_id,
            pw_element_id,
            signin_button_xpath,
            None,
            None,
            company,
        )
    return website_controller


def complete_github_two_factor_auth(hardcoded, website_controller):
    """Completes the GitHub 2FA."""
    # check if 2factor
    if source_contains(
        website_controller, "<h1>Two-factor authentication</h1>"
    ):

        # if 2 factor ask code from user
        two_factor_code = ask_two_factor_code()

        # enter code
        github_two_factor_login(
            hardcoded, two_factor_code, website_controller, "GitHub"
        )

    # Verify user is logged in correctly.


def user_is_logged_in(hardcoded, website_controller, company):
    """Returns True if the user is logged in, False otherwise."""
    if company == "GitLab":
        source = website_controller.driver.page_source
        if hardcoded.gitlab_logged_in_or_not_string in source:
            return True
        return False
    if company == "GitHub":
        # Read page source that indicates user is logged in.
        wait_until_page_is_loaded(6, website_controller)

        source = website_controller.driver.page_source

        if hardcoded.github_logged_in_or_not_string in source:
            return True
        return False
    raise Exception(f"Error, {company} not supported.")


def wait_until_page_is_loaded(time_limit_sec: int, website_controller):
    """Waits untill page is loaded for some time frame."""
    delay = time_limit_sec  # seconds
    try:
        _ = WebDriverWait(website_controller.driver, delay).until(
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
    website_controller = login(
        hardcoded,
        hardcoded.gitlab_login_url,
        hardcoded.gitlab_user_element_id,
        hardcoded.gitlab_pw_element_id,
        hardcoded.gitlab_signin_button_xpath,
        gitlab_username,
        gitlab_pwd,
        "GitLab",
    )
    return website_controller, gitlab_username, gitlab_pwd


def github_two_factor_login(
    hardcoded, two_factor_code, website_controller, company
):
    """USED to login for GitHub. Performs login of user into website. Returns
    the website_controller object.

    :param hardcoded: An object containing all the hardcoded settings used in this program.
    :param two_factor_code: param website_controller:
    :param website_controller: Object controlling the browser.
    """
    user_completed_2fac_in_browser = True
    try:
        if company == "GitHub":
            two_factor_input = website_controller.driver.find_element(
                "id", "totp"
            )
            # two_factor_input = website_controller.driver.find_element("name","otp")
            user_completed_2fac_in_browser = False
        else:
            raise Exception(f"Error, 2fa not yet supported for:{company}.")
    except:
        # User has already manually logged in in browser iso CLI.
        # pylint: disable=W0707
        raise Exception("Some error occured in 2fa.")

    if not user_completed_2fac_in_browser:
        two_factor_input.send_keys(two_factor_code)
        website_controller.driver.implicitly_wait(6)

        website_controller.driver.find_element(
            "css selector", ".btn-primary"
        ).click()

    # Assert user is already logged in.
    if not user_is_logged_in(hardcoded, website_controller, company):
        raise Exception("Error user is not logged in after 2fa login.")

    return website_controller


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
