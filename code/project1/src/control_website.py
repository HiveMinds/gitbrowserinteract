import time
from .Website_controller import Website_controller
from getpass import getpass
from .helper import read_creds
from .helper import scroll_shim
import sys

from selenium.webdriver.common.action_chains import ActionChains


def open_url(driver, url):
    """USED
    Makes the browser open an url through the driver object in the webcontroller.

    :param driver: object within website_controller that can controll the driver.
    :param url: A link to a website.

    """
    driver.get(url)
    return driver


def login(
    hardcoded,
    login_url,
    user_element_id,
    pw_element_id,
    signin_button_xpath,
    username,
    pswd,
):
    """Performs login of user into  website.
    Returns the website_controller  object.

    :param hardcoded: An object containing all the hardcoded settings used in this program.

    """

    website_controller = Website_controller()
    website_controller.driver = open_url(website_controller.driver, login_url)
    website_controller.driver.implicitly_wait(6)
    username_input = website_controller.driver.find_element_by_id(user_element_id)
    password_input = website_controller.driver.find_element_by_id(pw_element_id)

    if username is None:
        username = get_username()
    if pswd is None:
        pswd = get_pswd()

    # TODO: Include check to determine whether the user has already manually
    # logged into GitHub, if so, skip setting username and pwd and clicking
    # the login button.
    username_input.send_keys(username)
    password_input.send_keys(pswd)
    website_controller.driver.implicitly_wait(6)

    # website_controller.driver.find_element_by_css_selector(".btn-primary").click()
    click_element_by_xpath(
        website_controller, signin_button_xpath,
    )
    # Wait till login completed
    time.sleep(5)
    return website_controller


def github_login(hardcoded):
    website_controller = login(
        hardcoded,
        hardcoded.github_login_url,
        hardcoded.github_user_element_id,
        hardcoded.github_pw_element_id,
        hardcoded.github_signin_button_xpath,
        None,
        None,
    )
    return website_controller


def gitlab_login(hardcoded):
    username, pswd = get_credentials(hardcoded)
    website_controller = login(
        hardcoded,
        hardcoded.gitlab_login_url,
        hardcoded.gitlab_user_element_id,
        hardcoded.gitlab_pw_element_id,
        hardcoded.gitlab_signin_button_xpath,
        username,
        pswd,
    )
    return website_controller


def two_factor_login(two_factor_code, website_controller):
    """USED
    Performs login of user into website.
    Returns the website_controller object.

    :param hardcoded: An object containing all the hardcoded settings used in this program.
    :param two_factor_code: param website_controller:
    :param website_controller: Object controlling the browser.

    """
    two_factor_input = website_controller.driver.find_element_by_id("otp")

    two_factor_input.send_keys(two_factor_code)
    website_controller.driver.implicitly_wait(6)

    website_controller.driver.find_element_by_css_selector(".btn-primary").click()
    return website_controller


def get_credentials(hardcoded):
    """Gets  credentials from a hardcoded file and asks the user for
    them if they are not found.

    # TODO: export the credentials of the user if the user grants permission for that.

    :param hardcoded: An object containing all the hardcoded settings used in this program.

    """
    if hardcoded.use_cred_file:
        username, pswd = read_creds(hardcoded)
    else:
        username = get_username()
        pswd = get_pswd()
    return username, pswd


def get_username():
    """Gets the username for login and returns it."""
    username = getpass("Website Username:")

    return username


def get_pswd():
    """Gets the password for login and returns it."""
    pswd = getpass("Website Password:")
    return pswd


def click_element_by_xpath(website_controller, xpath):
    """Clicks an html element based on its xpath.

    :param website_controller: Object controlling the browser. Object that controls the browser.
    :param xpath: A direct link to an object in an html page.

    """
    source_element = website_controller.driver.find_element_by_xpath(xpath)
    if "firefox" in website_controller.driver.capabilities["browserName"]:
        scroll_shim(website_controller.driver, source_element)

    # scroll_shim is just scrolling it into view, you still need to hover over it to click using an action chain.
    actions = ActionChains(website_controller.driver)
    actions.move_to_element(source_element)
    actions.click()
    actions.perform()
    return website_controller
