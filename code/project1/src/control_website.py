from pprint import pprint
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from code.project1.src.ask_user_input import ask_two_factor_code
from .Website_controller import Website_controller
from getpass import getpass
from .helper import read_creds, source_contains
from .helper import scroll_shim
import sys

from selenium.webdriver.common.action_chains import ActionChains


def github_login(hardcoded, github_pwd=None, github_username=None):
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


def login(
    hardcoded,
    login_url,
    user_element_id,
    pw_element_id,
    signin_button_xpath,
    username,
    pswd,
    company,
):
    """Performs login of user into  website.
    Returns the website_controller  object.

    :param hardcoded: An object containing all the hardcoded settings used in this program.

    """

    website_controller = Website_controller()
    website_controller.driver = open_url(website_controller.driver, login_url)
    website_controller.driver.implicitly_wait(6)
    username_input = website_controller.driver.find_element("id", user_element_id)
    password_input = website_controller.driver.find_element("id", pw_element_id)

    if username is None:
        username = get_username(company)
    if pswd is None:
        pswd = get_pswd(company)
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
        password_input.send_keys(pswd)
        website_controller.driver.implicitly_wait(15)

        # website_controller.driver.find_element("css selector",".btn-primary").click()
        click_element_by_xpath(
            website_controller,
            signin_button_xpath,
        )

    # Wait till login completed
    time.sleep(5)
    
    complete_github_two_factor_auth(hardcoded,website_controller)
    if not user_is_logged_in(hardcoded, website_controller, company):
        print(
            f"Hi, we were not able to verify you are logged in, (which is needed to add the ssh-deploy key).\n We will now try again. To break this loop, press CTRL+C.\n\n"
        )
        website_controller.driver.close()
        website_controller = None
        if user_passed_pwd_earlier:
            raise Exception(
                "Error, you have passed the wrong password to this method, (or GitHub is changed/down). Please try again with the correct GitHub pwd, or manually log in."
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
    # check if 2factor
    if source_contains(website_controller, "<h1>Two-factor authentication</h1>"):

        # if 2 factor ask code from user
        two_factor_code = ask_two_factor_code()

        # enter code
        two_factor_login(hardcoded,two_factor_code, website_controller,"GitHub")

    # Verify user is logged in correctly.


def open_url(driver, url):
    """USED # TODO: eliminate duplicate function.
    Makes the browser open an url through the driver object in the webcontroller.

    :param driver: object within website_controller that can controll the driver.
    :param url: A link to a website.

    """
    driver.get(url)
    return driver


def user_is_logged_in(hardcoded, website_controller, company):
    if company == "GitLab":
        source = website_controller.driver.page_source
        if hardcoded.gitlab_logged_in_or_not_string in source:
            return True
        else:
            return False
    elif company == "GitHub":
        # Read page source that indicates user is logged in.
        wait_until_page_is_loaded(6,website_controller)

        source = website_controller.driver.page_source

        if hardcoded.github_logged_in_or_not_string in source:
            return True
        else:
            return False

def wait_until_page_is_loaded(time_limit_sec:int,website_controller):
    delay = time_limit_sec # seconds
    try:
        myElem = WebDriverWait(website_controller.driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'Header-link')))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")

def gitlab_login(hardcoded,gitlab_pwd=None, gitlab_username=None):
    if gitlab_pwd is None:
        username, pswd = get_credentials(hardcoded)
    website_controller = login(
        hardcoded,
        hardcoded.gitlab_login_url,
        hardcoded.gitlab_user_element_id,
        hardcoded.gitlab_pw_element_id,
        hardcoded.gitlab_signin_button_xpath,
        username,
        pswd,
        "GitLab",
    )
    return website_controller


def two_factor_login(hardcoded,two_factor_code, website_controller, company):
    """USED to login for GitHub.
    Performs login of user into website.
    Returns the website_controller object.

    :param hardcoded: An object containing all the hardcoded settings used in this program.
    :param two_factor_code: param website_controller:
    :param website_controller: Object controlling the browser.

    """
    user_completed_2fac_in_browser=True
    try:
        if company == "GitHub":
            two_factor_input = website_controller.driver.find_element("id","totp")
            #two_factor_input = website_controller.driver.find_element("name","otp")
            user_completed_2fac_in_browser=False
        else:
            raise Exception(f"Error, 2fa not yet supported for:{company}.")
    except:
        # User has already manually logged in in browser iso CLI.
        pass

    if not user_completed_2fac_in_browser:
        two_factor_input.send_keys(two_factor_code)
        website_controller.driver.implicitly_wait(6)

        website_controller.driver.find_element("css selector",".btn-primary").click()

    # Assert user is already logged in.
    if not user_is_logged_in(hardcoded, website_controller, company):
        raise Exception("Error user is not logged in after 2fa login.")

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


def get_username(company):
    """Gets the username for login and returns it."""
    username = getpass(
        f"\nPlease enter your {company} Username: \n(you can also manually log into {company},\n and fill in nonsense in this field,\n if you prefer typing your Username into GitHub directly.)\n"
    )
    if username == "nonsense" or username == "Nonsense":
        print(f"That is funny. This is unprofessional.")
    return username


def get_pswd(company):
    """Gets the password for login and returns it."""
    pswd = getpass(
        f"Please enter your {company} Password \n(you can also manually log into {company},\n and fill in gibberish in this field,\n if you prefer typing your Password into GitHub directly.)\n"
    )
    return pswd


def click_element_by_xpath(website_controller, xpath):
    """Clicks an html element based on its xpath.

    :param website_controller: Object controlling the browser. Object that controls the browser.
    :param xpath: A direct link to an object in an html page.

    """
    source_element = website_controller.driver.find_element("xpath",xpath)
    if "firefox" in website_controller.driver.capabilities["browserName"]:
        scroll_shim(website_controller.driver, source_element)

    # scroll_shim is just scrolling it into view, you still need to hover over it to click using an action chain.
    actions = ActionChains(website_controller.driver)
    actions.move_to_element(source_element)
    actions.click()
    actions.perform()
    return website_controller
