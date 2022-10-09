# Code that automatically copies all issues of a repository to another
import time
from code.project1.src.GitHub.remove_previous_github_pat import (
    remove_previous_github_pat,
)

from ..ask_user_input import ask_two_factor_code
from ..control_website import github_login, github_two_factor_login, open_url
from ..export_token import export_github_pac_to_personal_creds_txt
from ..Hardcoded import Hardcoded
from ..helper import (
    click_element_by_xpath,
    get_value_from_html_source,
    source_contains,
)


class Github_personal_access_token_getter:
    """Gets a GitHub personal access token."""

    def __init__(
        self,
        project_nr,
        github_username=None,
        github_pwd=None,
    ):
        """Initialises object that gets the browser controller, then it gets
        the issues from the source repo, and copies them to the target repo.

        :param project_nr: [Int] that indicates the folder in which this code is stored.
        :param login: [Boolean] True if the website_controller object should be
        created and should login to GitHub.
        """

        # project_nr is an artifact of folder structure
        self.project_nr = project_nr

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

        # TODO: get gitlab-ci-build-statuses from argument parser
        # github_repo_name = "gitlab-ci-build-statuses"

        # website_controller = get_website_controller(self.hc)
        # TODO: change
        website_controller = self.login_github_for_personal_access_token(
            self.hc,
            github_username=self.github_username,
            github_pwd=self.github_pwd,
        )

        # TODO: include check to see if (2FA) verification code is asked. (This check is
        # already in login_github_to_build_status_repo() yet it did not work. So improve it)

        # wait five seconds for page to load
        # input("Are you done with loggin into GitHub?")

        print("Logged in")

        self.create_github_personal_access_token(self.hc, website_controller)

        print(
            "Done GitHub personal access token. Waiting 10 seconds and then the browser."
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
            "Hi, I'm done creating the GitHub personal access token to set the GitHub commit build status."
        )

    def login_github_for_personal_access_token(
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
        website_controller = github_login(
            hardcoded, github_pwd, github_username
        )
        # website_controller = github_login(hardcoded)

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

        # Remove GitHub personal access token if it already exists.
        remove_previous_github_pat(hardcoded, website_controller)

        # repository_url = f"https://github.com/{github_username}/{github_build_status_repo_name}/issues"
        personal_access_token_url = (
            "https://github.com/settings/tokens/new"  # nosec
        )

        # Go to source repository
        website_controller.driver = open_url(
            website_controller.driver, personal_access_token_url
        )

        return website_controller

    def create_github_personal_access_token(
        self, hardcoded, website_controller
    ):
        """

        :param hardcoded:
        :param website_controller:

        """
        github_pac_input_field = website_controller.driver.find_element(
            "xpath", hardcoded.github_pac_input_field_xpath
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
        """

        :param website_controller:
        :param hardcoded:

        """
        clicked = False
        try:
            click_element_by_xpath(
                website_controller,
                hardcoded.github_pac_repo_status_checkbox_xpathV0,
            )
            clicked = True
        except:  # nosec
            pass
        if not clicked:
            try:
                click_element_by_xpath(
                    website_controller,
                    hardcoded.github_pac_repo_status_checkbox_xpathV1,
                )
            except:  # nosec
                pass
        if not clicked:
            click_element_by_xpath(
                website_controller,
                hardcoded.github_pac_repo_status_checkbox_xpathV2,
            )

    def click_submit_token(self, website_controller, hardcoded):
        """

        :param website_controller:
        :param hardcoded:

        """
        clicked = False
        try:
            click_element_by_xpath(
                website_controller,
                hardcoded.github_pac_generate_token_button_xpathV0,
            )
            clicked = True
        except:  # nosec
            pass
        if not clicked:
            try:
                click_element_by_xpath(
                    website_controller,
                    hardcoded.github_pac_generate_token_button_xpathV1,
                )
                clicked = True
            except:  # nosec
                pass
        if not clicked:
            click_element_by_xpath(
                website_controller,
                hardcoded.github_pac_generate_token_button_xpathV2,
            )

    def read_github_personal_access_token(self, website_controller):
        """Reads the GitHub personal acccess token from website.

        :param website_controller:
        """
        # <code id="new-oauth-token" class="token">sometoken</code>
        # get the page source:
        source = website_controller.driver.page_source

        lhs = '<code id="new-oauth-token" class="token">'
        rhs = "</code>"
        if source_contains(website_controller, lhs):
            if source_contains(website_controller, rhs):
                return get_value_from_html_source(source, lhs, rhs)
            else:
                raise Exception(
                    "The token identification string:{rhs} was not found."
                )
        else:
            raise Exception(
                "The token identification string:{rhs} was not found."
            )
