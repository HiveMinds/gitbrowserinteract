# Code that automatically copies all issues of a repository to another
import time

from browsercontroller.helper import (
    click_element_by_xpath,
    open_url,
    source_contains,
)

from src.gitbrowserinteract.GitHub.github_login import github_login
from src.gitbrowserinteract.GitHub.remove_previous_github_pat import (
    remove_previous_github_pat,
)

from ..export_token import export_github_pac_to_personal_creds_txt
from ..Hardcoded import Hardcoded
from ..helper import get_value_from_html_source


class Github_personal_access_token_getter:
    """Gets a GitHub personal access token."""

    def __init__(
        self,
        github_username=None,
        github_pwd=None,
    ):
        """Initialises object that gets the browser controller, then it gets
        the issues from the source repo, and copies them to the target repo.

        :param project_nr: [Int] that indicates the folder in which this code is stored.
        :param login: [Boolean] True if the driver object should be
        created and should login to GitHub.
        """

        # Store the hardcoded values used within this project
        self.hc = Hardcoded()

        # TODO: get github_user_name from argument parser
        # TODO: get github_user_name from hardcoded.txt
        self.github_username = github_username
        if self.github_username is None:
            raise Exception(
                "Error, expected a GitHub username as incoming argument."
            )
        self.github_pwd = github_pwd

        driver = self.set_github_personal_access_token(
            self.hc,
            github_username=self.github_username,
            github_pwd=self.github_pwd,
        )

        # wait five seconds for page to load
        # input("Are you done with loggin into GitHub?")

        print("Logged in")

        self.create_github_personal_access_token(self.hc, driver)

        print(
            "Done GitHub personal access token. Waiting 10 seconds and then the browser."
        )
        time.sleep(10)
        pac = self.read_github_personal_access_token(driver)
        print(f"pac={pac}")

        # Export GitHub personal access token to ../../personal_creds.txt
        export_github_pac_to_personal_creds_txt(
            self.hc.personal_creds_path, self.hc, pac
        )
        # close website controller
        driver.close()

        print(
            "Hi, I'm done creating the GitHub personal access token to set the GitHub commit build status."
        )

    def set_github_personal_access_token(
        self, hardcoded, github_username, github_pwd
    ):
        """USED Gets the issues from a github repo. Opens a separate browser
        instance and then closes it again. Returns the rsc_data object that
        contains the parsed availability of the relevant activities.

        TODO: determine and document how get_next_activity manages the difference between primary and secondary
        choice.

        :param hardcoded: An object containing all the hardcoded settings used in this program.
        :param user_choices: Object that contains the choices/schedule that user wants to follow.
        :param github_username:
        :param github_pwd:
        """

        # login
        driver = github_login(
            hardcoded=hardcoded,
            login_url=hardcoded.github_login_url,
            user_element_id=hardcoded.github_user_element_id,
            pw_element_id=hardcoded.github_pw_element_id,
            signin_button_xpath=hardcoded.github_signin_button_xpath,
            username=github_username,
            pwd=github_pwd,
        )

        # Remove GitHub personal access token if it already exists.
        remove_previous_github_pat(hardcoded=hardcoded, driver=driver)

        # repository_url = f"https://github.com/{github_username}/{github_build_status_repo_name}/issues"
        personal_access_token_url = (
            "https://github.com/settings/tokens/new"  # nosec
        )

        # Go to source repository
        driver = open_url(driver, personal_access_token_url)

        return driver

    def create_github_personal_access_token(self, hardcoded, driver):
        """

        :param hardcoded:
        :param driver:

        """
        github_pac_input_field = driver.find_element(
            "xpath", hardcoded.github_pac_input_field_xpath
        )

        # github_pac_repo_status_checkbox = driver.find_element_by_id(
        #    hardcoded.github_pac_repo_status_checkbox_xpath
        # )
        # github_pac_generate_token_button = driver.find_element_by_id(
        #    hardcoded.github_pac_generate_token_button_xpath
        # )

        # Specify what the GitHub personal access token is used for.
        github_pac_input_field.send_keys(hardcoded.github_pat_description)

        # Give read and write permission to GitHub commit build statuses.
        self.click_repo_status_checkbox(driver, hardcoded)

        # Submit token.
        self.click_submit_token(driver, hardcoded)

    def click_repo_status_checkbox(self, driver, hardcoded):
        """

        :param driver:
        :param hardcoded:

        """
        clicked = False
        try:
            click_element_by_xpath(
                driver,
                hardcoded.github_pac_repo_status_checkbox_xpathV0,
            )
            clicked = True
        except:  # nosec
            pass
        if not clicked:
            try:
                click_element_by_xpath(
                    driver,
                    hardcoded.github_pac_repo_status_checkbox_xpathV1,
                )
                clicked = True
            except:  # nosec
                pass
        if not clicked:
            try:
                click_element_by_xpath(
                    driver,
                    hardcoded.github_pac_repo_status_checkbox_xpathV2,
                )
                clicked = True
            except:  # nosec
                pass
        if not clicked:
            click_element_by_xpath(
                driver,
                hardcoded.github_pac_repo_status_checkbox_xpathV3,
            )

    def click_submit_token(self, driver, hardcoded):
        """

        :param driver:
        :param hardcoded:

        """
        clicked = False
        try:
            click_element_by_xpath(
                driver,
                hardcoded.github_pac_generate_token_button_xpathV0,
            )
            clicked = True
        except:  # nosec
            pass
        if not clicked:
            try:
                click_element_by_xpath(
                    driver,
                    hardcoded.github_pac_generate_token_button_xpathV1,
                )
                clicked = True
            except:  # nosec
                pass
        # TODO: click button by text: "Generate token"
        if not clicked:
            click_element_by_xpath(
                driver,
                hardcoded.github_pac_generate_token_button_xpathV2,
            )

    def read_github_personal_access_token(self, driver):
        """Reads the GitHub personal acccess token from website.

        :param driver:
        """
        # <code id="new-oauth-token" class="token">sometoken</code>
        # get the page source:
        source = driver.page_source

        lhs = '<code id="new-oauth-token" class="token">'
        rhs = "</code>"
        if source_contains(driver, lhs):
            if source_contains(driver, rhs):
                return get_value_from_html_source(source, lhs, rhs)
            else:
                raise Exception(
                    "The token identification string:{rhs} was not found."
                )
        else:
            raise Exception(
                "The token identification string:{rhs} was not found."
            )
