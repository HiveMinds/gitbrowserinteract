# Code that automatically copies all issues of a repository to another
import os.path

from code.project1.src.GitHub.remove_previous_github_pat import remove_previous_github_pat

from ..ask_user_input import ask_two_factor_code
from ..control_website import click_element_by_xpath, two_factor_login
from ..control_website import github_login
from ..Hardcoded import Hardcoded
from ..get_gitlab_runner_token import get_gitlab_runner_registration_token_from_page
from ..get_data import get_value_from_html_source
from ..helper import get_runner_registration_token_filepath
from ..helper import source_contains
from ..helper import write_string_to_file
from ..helper import loiter_till_gitlab_server_is_ready_for_login
from ..export_token import export_github_pac_to_personal_creds_txt
from ..control_website import open_url
from ..Website_controller import Website_controller
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time


class Github_personal_access_token_getter:
    """ """

    def __init__(
        self, project_nr, github_username=None, github_pwd=None, should_login=True
    ):
        """Initialises object that gets the browser controller, then it gets the issues
        from the source repo, and copies them to the target repo.

        :param project_nr: [Int] that indicates the folder in which this code is stored.
        :param login: [Boolean] True if the website_controller object should be
        created and should login to GitHub.
        """

        # project_nr is an artifact of folder structure
        self.project_nr = project_nr
        self.relative_src_filepath = f"code/project{self.project_nr}/src/"
        # Store the hardcoded values used within this project
        self.hc = Hardcoded()

        # TODO: get github_user_name from argument parser
        # TODO: get github_user_name from hardcoded.txt
        self.github_username = github_username
        if self.github_username is None:
            raise Exception("Error, expected a GitHub username as incoming argument.")
        self.github_pwd = github_pwd

        # TODO: get gitlab-ci-build-statuses from argument parser
        # github_repo_name = "gitlab-ci-build-statuses"

        # website_controller = get_website_controller(self.hc)
        # TODO: change
        website_controller = self.login_github_for_personal_access_token(
            self.hc, github_username=self.github_username, github_pwd=self.github_pwd
        )

        # TODO: include check to see if (2FA) verification code is asked. (This check is
        # already in login_github_to_build_status_repo() yet it did not work. So improve it)

        # wait five seconds for page to load
        # input("Are you done with loggin into GitHub?")

        print(f"Logged in")

        self.create_github_personal_access_token(self.hc, website_controller)

        print(
            f"Done GitHub personal access token. Waiting 10 seconds and then the browser."
        )
        time.sleep(10)
        pac = self.read_github_personal_access_token(website_controller)
        print(f"pac={pac}")

        # Export GitHub personal access token to ../../personal_creds.txt
        export_github_pac_to_personal_creds_txt(
            self.hc.personal_creds_path, self.hc, pac
        )
        # close website controller
        website_controller.driver.close()

        print(
            f"Hi, I'm done creating the GitHub personal access token to set the GitHub commit build status."
        )

    def login_github_for_personal_access_token(
        self, hardcoded, github_username, github_pwd
    ):
        """USED
        Gets the issues from a github repo. Opens a separate browser instance and then
        closes it again.
        Returns the rsc_data object that contains the parsed availability of the relevant activities.

        TODO: determine and document how get_next_activity manages the difference between primary and secondary
        choice.

        :param hardcoded: An object containing all the hardcoded settings used in this program.
        :param user_choices: Object that contains the choices/schedule that user wants to follow.

        """

        # login
        website_controller = github_login(hardcoded, github_pwd, github_username)
        # website_controller = github_login(hardcoded)

        # check if 2factor
        if source_contains(website_controller, "<h1>Two-factor authentication</h1>"):

            # if 2 factor ask code from user
            two_factor_code = ask_two_factor_code()

            # enter code
            two_factor_login(two_factor_code, website_controller)

        # Remove GitHub personal access token if it already exists.
        remove_previous_github_pat(hardcoded,website_controller)


        # repository_url = f"https://github.com/{github_username}/{github_build_status_repo_name}/issues"
        personal_access_token_url = f"https://github.com/settings/tokens/new"

        # Go to source repository
        website_controller.driver = open_url(
            website_controller.driver, personal_access_token_url
        )

        return website_controller

    def create_github_personal_access_token(self, hardcoded, website_controller):
        github_pac_input_field = website_controller.driver.find_element("xpath",
            hardcoded.github_pac_input_field_xpath
        )

        # github_pac_repo_status_checkbox = website_controller.driver.find_element_by_id(
        #    hardcoded.github_pac_repo_status_checkbox_xpath
        # )
        # github_pac_generate_token_button = website_controller.driver.find_element_by_id(
        #    hardcoded.github_pac_generate_token_button_xpath
        # )

        # Specify what the GitHub personal access token is used for.
        github_pac_input_field.send_keys(hardcoded.github_pat_description)

        # Give read and write permission to GitHub commit build statuses.
        self.click_repo_status_checkbox(website_controller, hardcoded)

        # Submit token.
        self.click_submit_token(website_controller, hardcoded)

    def click_repo_status_checkbox(self, website_controller, hardcoded):
        clicked = False
        try:
            click_element_by_xpath(
                website_controller, hardcoded.github_pac_repo_status_checkbox_xpathV0
            )
            clicked = True
        except:
            pass
        if not clicked:
            try:
                click_element_by_xpath(
                    website_controller, hardcoded.github_pac_repo_status_checkbox_xpathV1
                )
            except:
                pass
        if not clicked:
            click_element_by_xpath(
                website_controller, hardcoded.github_pac_repo_status_checkbox_xpathV2
            )

    def click_submit_token(self, website_controller, hardcoded):
        clicked = False
        try:
            click_element_by_xpath(
                website_controller, hardcoded.github_pac_generate_token_button_xpathV0
            )
            clicked = True
        except:
            pass
        if not clicked:
            try:
                click_element_by_xpath(
                    website_controller, hardcoded.github_pac_generate_token_button_xpathV1
                )
                clicked = True
            except:
                pass
        if not clicked:
            click_element_by_xpath(
                website_controller, hardcoded.github_pac_generate_token_button_xpathV2
            )

    def read_github_personal_access_token(self, website_controller):
        print(f"hi")
        # <code id="new-oauth-token" class="token">sometoken</code>
        # get the page source:
        source = website_controller.driver.page_source

        lhs = '<code id="new-oauth-token" class="token">'
        rhs = "</code>"
        if source_contains(website_controller, lhs):
            if source_contains(website_controller, rhs):
                return get_value_from_html_source(source, lhs, rhs)
            else:
                raise Exception("The token identification string:{rhs} was not found.")
        else:
            raise Exception("The token identification string:{rhs} was not found.")
