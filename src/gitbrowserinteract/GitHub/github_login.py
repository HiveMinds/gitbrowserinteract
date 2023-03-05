"""Performs login on GitHub."""

import time

from browsercontroller.get_controller import get_ubuntu_apt_firefox_controller
from browsercontroller.helper import click_element_by_xpath, source_contains

from src.gitbrowserinteract.ask_user_input import ask_two_factor_code
from src.gitbrowserinteract.control_website import wait_until_page_is_loaded


# pylint: disable=R0913
def github_login(
    *,
    hardcoded,
    login_url,
    user_element_id,
    pw_element_id,
    signin_button_xpath,
    username,
    pwd,
):
    """Performs login of user into  website. Returns the driver object.

    :param hardcoded: An object containing all the hardcoded settings used in this program.
    """

    # Go to extension settings.
    driver = get_ubuntu_apt_firefox_controller(
        url=login_url, default_profile=True
    )
    time.sleep(5)

    # TODO: create buffer for alternative tabs that need to be closed.

    driver.implicitly_wait(6)

    # Check to determine whether the user has already manually
    # logged into GitHub, if so, skip setting username and pwd and clicking
    # the login button.
    user_has_manually_logged_in = user_is_logged_in_in_github(
        hardcoded, driver
    )
    if not user_has_manually_logged_in:
        username_input = driver.find_element("id", user_element_id)
        password_input = driver.find_element("id", pw_element_id)

        username_input.send_keys(username)
        password_input.send_keys(pwd)
        driver.implicitly_wait(15)

        # driver.find_element("css selector",".btn-primary").click()
        click_element_by_xpath(
            driver,
            signin_button_xpath,
        )

    # Wait till login completed
    time.sleep(5)

    complete_github_two_factor_auth(hardcoded, driver)
    if not user_is_logged_in_in_github(hardcoded, driver):
        print(
            "Hi, we were not able to verify you are logged in, (which is "
            + "needed"
            + " to add the ssh-deploy key).\n We will now try again. To "
            + "break this"
            + " loop, press CTRL+C.\n\n"
        )
        driver.close()

        return github_login(
            hardcoded,
            login_url,
            user_element_id,
            pw_element_id,
            signin_button_xpath,
            None,
            None,
        )

    return driver


def user_is_logged_in_in_github(
    hardcoded,
    driver,
):
    """Returns True if the user is logged in, False otherwise."""
    # Read page source that indicates user is logged in.
    wait_until_page_is_loaded(6, driver)

    source = driver.page_source

    if hardcoded.github_logged_in_or_not_string in source:
        return True
    return False


def complete_github_two_factor_auth(hardcoded, driver):
    """Completes the GitHub 2FA."""
    # check if 2factor
    if source_contains(driver, "<h1>Two-factor authentication</h1>"):
        # if 2 factor ask code from user
        two_factor_code = ask_two_factor_code()

        # enter code
        github_two_factor_login(hardcoded, two_factor_code, driver, "GitHub")

    # Verify user is logged in correctly.


def github_two_factor_login(hardcoded, two_factor_code, driver, company):
    """USED to login for GitHub. Performs login of user into website. Returns
    the driver object.

    :param hardcoded: An object containing all the hardcoded settings used in this program.
    :param two_factor_code: param driver:
    :param driver: Object controlling the browser.
    """
    user_completed_2fac_in_browser = True
    try:
        # Unsafe order, if fails then assumes user already logged in.
        # TODO: change to check if user already logged in.
        two_factor_input = driver.find_element(
            "xpath", hardcoded.github_2fa_input_filed_xpath
        )
        # two_factor_input = driver.find_element("name","otp")
        user_completed_2fac_in_browser = False
    except:  # nosec
        # User has already manually logged in in browser iso CLI.
        # pylint: disable=W0707
        pass

    if not user_completed_2fac_in_browser:
        two_factor_input.send_keys(two_factor_code)
        driver.implicitly_wait(6)

        driver.find_element("css selector", ".btn-primary").click()

    # Assert user is already logged in.
    if not user_is_logged_in_in_github(hardcoded, driver):
        raise Exception("Error user is not logged in after 2fa login.")

    return driver
