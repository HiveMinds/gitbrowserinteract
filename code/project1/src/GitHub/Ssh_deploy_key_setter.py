# Code that automatically copies all issues of a repository to another
from code.project1.src.GitHub.remove_previous_github_ssh_key import remove_previous_github_ssh_key
from ..ask_user_input import ask_two_factor_code
from ..control_website import click_element_by_xpath
from ..control_website import github_login
from ..Hardcoded import Hardcoded
from ..get_gitlab_runner_token import get_runner_registration_token_from_page
from ..helper import get_runner_registration_token_filepath
from ..helper import source_contains
from ..helper import write_string_to_file
from ..helper import loiter_till_gitlab_server_is_ready_for_login
from ..control_website import open_url
from ..Website_controller import Website_controller
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time


class Ssh_deploy_key_setter:
    """ """

    def __init__(
        self,
        project_nr,
        public_ssh_sha,
        github_username=None,
        github_pwd=None,
        should_login=True,
    ):
        """Initialises object that gets the browser controller, then it gets the issues
        from the source repo, and copies them to the target repo.

        :param project_nr: [Int] that indicates the folder in which this code is stored.
        :param login: [Boolean] True if the website_controller object should be
        created and should login to GitHub.
        """

        # project_nr is an artifact of folder structure
        self.project_nr = project_nr
        self.public_ssh_sha = public_ssh_sha
        self.relative_src_filepath = f"code/project{self.project_nr}/src/"
        # Store the hardcoded values used within this project
        self.hc = Hardcoded()

        self.github_username = github_username
        if self.github_username is None:
            raise Exception("Error, expected a GitHub username as incoming argument.")
        self.github_pwd = github_pwd

        # TODO: get gitlab-ci-build-statuses from hardcoded.txt
        github_repo_name = "gitlab-ci-build-statuses"

        # TODO: separate login and browsing to the add token page.
        # TODO: re-use the 2fac authentication login method created for adding pac.
        website_controller = self.login_github_to_build_status_repo(
            self.hc, self.github_username, github_repo_name, github_pwd=github_pwd
        )

        # Remove pre-existing ssh keys matching target description.
        remove_previous_github_ssh_key(self.github_username,self.hc,website_controller)

        # Reload add new token page
        repository_url = f"https://github.com/{github_username}/{github_repo_name}/settings/keys/new"

        # Go to source repository
        website_controller.driver = open_url(website_controller.driver, repository_url)

        # wait five seconds for page to load
        # input("Are you done with loggin into GitHub?")

        self.fill_in_ssh_key(self.hc, website_controller, self.public_ssh_sha)

        print(
            f"Done adding the ssh deploy key from your machine to:{github_repo_name}. Waiting 10 seconds and then the browser."
        )
        time.sleep(10)

        # close website controller
        website_controller.driver.close()

        print(
            f"Hi, I'm done setting the GitHub deployment token to your repository:{github_repo_name}."
        )

    def login_github_to_build_status_repo(
        self, hardcoded, github_username, github_build_status_repo_name, github_pwd=None
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

        # check if 2factor
        if source_contains(website_controller, "<h1>Two-factor authentication</h1>"):

            # if 2 factor ask code from user
            two_factor_code = ask_two_factor_code()

            # enter code
            two_factor_login(two_factor_code, website_controller)

        # repository_url = f"https://github.com/{github_username}/{github_build_status_repo_name}/issues"
        repository_url = f"https://github.com/{github_username}/{github_build_status_repo_name}/settings/keys/new"

        # Go to source repository
        website_controller.driver = open_url(website_controller.driver, repository_url)

        return website_controller

    def fill_in_ssh_key(self, hardcoded, website_controller, public_ssh_sha):
        
        github_deployment_key_title_field = (
            website_controller.driver.find_element("id", 
                hardcoded.github_deploy_key_title_element_id
            )
        )
        
        github_deployment_key_key_field = website_controller.driver.find_element("id", 
            hardcoded.github_deploy_key_key_element_id
        )
        
        # Set the title and ssh key for the GitHub deploy key for the GitLab build status repo.
        github_deployment_key_title_field.send_keys(hardcoded.github_ssh_key_description)
        github_deployment_key_key_field.send_keys(public_ssh_sha)

        
        # Give write permission to deploy key for the GitLab build status repository (in GitHub)
        click_element_by_xpath(
            website_controller,
            hardcoded.github_deploy_key_allow_write_access_button_xpath,
        )

        
        # Click: add the new deploy key to the GitHub repository.
        click_element_by_xpath(
            website_controller, hardcoded.add_github_deploy_key_button_xpath
        )

