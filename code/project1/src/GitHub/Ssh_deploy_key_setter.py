"""Sets the GitHub SSH deploy key."""
import time
from code.project1.src.ask_user_input import ask_two_factor_code
from code.project1.src.control_website import (
    github_login,
    github_two_factor_login,
)
from code.project1.src.GitHub.remove_previous_github_ssh_key import (
    remove_previous_github_ssh_key,
)
from code.project1.src.Hardcoded import Hardcoded
from code.project1.src.helper import (
    click_element_by_xpath,
    open_url,
    source_contains,
)


class Ssh_deploy_key_setter:
    """Gets the GitHub SSH deploy key."""

    def __init__(
        self,
        project_nr,
        public_ssh_sha,
        github_username=None,
        github_pwd=None,
    ):
        """Initialises object that gets the browser controller, then it gets
        the issues from the source repo, and copies them to the target repo.

        :param project_nr: [Int] that indicates the folder in which this code is stored.
        :param login: [Boolean] True if the driver object should be
        created and should login to GitHub.
        """

        # project_nr is an artifact of folder structure
        self.project_nr = project_nr
        self.public_ssh_sha = public_ssh_sha

        # Store the hardcoded values used within this project
        self.hc = Hardcoded()

        self.github_username = github_username
        if self.github_username is None:
            raise Exception(
                "Error, expected a GitHub username as incoming argument."
            )
        self.github_pwd = github_pwd

        # TODO: get gitlab-ci-build-statuses from hardcoded.txt
        github_repo_name = "gitlab-ci-build-statuses"

        # TODO: separate login and browsing to the add token page.
        # TODO: re-use the 2fac authentication login method created for adding pac.
        driver = self.login_github_to_build_status_repo(
            self.hc,
            self.github_username,
            github_repo_name,
            github_pwd=github_pwd,
        )

        # Remove pre-existing ssh keys matching target description.
        remove_previous_github_ssh_key(self.github_username, self.hc, driver)

        # Reload add new token page
        repository_url = (
            f"https://github.com/{github_username}/"
            + f"{github_repo_name}/settings/keys/new"
        )

        # Go to source repository
        driver = open_url(driver, repository_url)

        # wait five seconds for page to load
        # input("Are you done with loggin into GitHub?")

        self.fill_in_ssh_key(self.hc, driver, self.public_ssh_sha)

        print(
            "Done adding the ssh deploy key from your machine to:"
            f"{github_repo_name}. Waiting 10 seconds and then the browser."
        )
        time.sleep(10)

        # close website controller
        driver.close()

        print(f"Done setting GitHub deployment token repo:{github_repo_name}.")

    def login_github_to_build_status_repo(
        self,
        hardcoded,
        github_username,
        github_build_status_repo_name,
        github_pwd=None,
    ):
        """USED Gets the issues from a github repo. Opens a separate browser
        instance and then closes it again. Returns the rsc_data object that
        contains the parsed availability of the relevant activities.

        TODO: determine and document how get_next_activity manages the
        difference between primary and secondary choice.

        :param hardcoded: An object containing all the hardcoded settings used
        in this program.
        :param user_choices: Object that contains the choices/schedule that
        user wants to follow.
        :param github_username:
        :param github_build_status_repo_name:
        :param github_pwd:  (Default value = None)
        """

        # login
        driver = github_login(hardcoded, github_pwd, github_username)

        # check if 2factor
        if source_contains(driver, "<h1>Two-factor authentication</h1>"):
            # if 2 factor ask code from user
            two_factor_code = ask_two_factor_code()

            # enter code
            github_two_factor_login(
                hardcoded, two_factor_code, driver, "GitHub"
            )

        repository_url = (
            f"https://github.com/{github_username}/"
            + f"{github_build_status_repo_name}/settings/keys/new"
        )

        # Go to source repository
        driver = open_url(driver, repository_url)

        return driver

    def fill_in_ssh_key(self, hardcoded, driver, public_ssh_sha):
        """

        :param hardcoded:
        :param driver:
        :param public_ssh_sha:

        """

        github_deployment_key_title_field = driver.find_element(
            "id", hardcoded.github_deploy_key_title_element_id
        )

        github_deployment_key_key_field = driver.find_element(
            "id", hardcoded.github_deploy_key_key_element_id
        )

        # Set the title and ssh key for the GitHub deploy key for the GitLab build status repo.
        github_deployment_key_title_field.send_keys(
            hardcoded.github_ssh_key_description
        )
        github_deployment_key_key_field.send_keys(public_ssh_sha)

        # Give write permission to deploy key for the GitLab build status repository (in GitHub)
        click_element_by_xpath(
            driver,
            hardcoded.github_deploy_key_allow_write_access_button_xpath,
        )

        # Click: add the new deploy key to the GitHub repository.
        click_element_by_xpath(
            driver, hardcoded.add_github_deploy_key_button_xpath
        )
