"""Sets the GitHub SSH deploy key."""
import time

from browsercontroller.helper import click_element_by_xpath
from typeguard import typechecked

from ..GitHub.github_login import github_login
from ..Hardcoded import Hardcoded
from .remove_previous_github_ssh_key import remove_previous_github_ssh_key


class Ssh_deploy_key_setter:
    """Gets the GitHub SSH deploy key."""

    @typechecked
    def __init__(
        self,
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
        # TODO: write function to verify ssh key format.
        self.public_ssh_sha = public_ssh_sha

        # Store the hardcoded values used within this project
        hardcoded = Hardcoded()

        # pylint: disable = R0801
        self.github_username = github_username
        if self.github_username is None:
            raise ValueError(
                "Error, expected a GitHub username as incoming argument."
            )
        self.github_pwd = github_pwd

        # TODO: get gitlab-ci-build-statuses from hardcoded.txt
        github_repo_name = "gitlab-ci-build-statuses"

        driver = github_login(
            hardcoded=hardcoded,
            login_url=hardcoded.github_login_url,
            user_element_id=hardcoded.github_user_element_id,
            pw_element_id=hardcoded.github_pw_element_id,
            signin_button_xpath=hardcoded.github_signin_button_xpath,
            username=github_username,
            pwd=github_pwd,
        )

        driver = self.open_github_build_status_repo_keys(
            driver=driver,
            github_username=self.github_username,
            github_build_status_repo_name=github_repo_name,
        )

        # Remove pre-existing ssh keys matching target description.
        remove_previous_github_ssh_key(
            github_username=self.github_username,
            hardcoded=hardcoded,
            driver=driver,
        )

        # Reload add new token page
        repository_url = (
            f"https://github.com/{github_username}/"
            + f"{github_repo_name}/settings/keys/new"
        )

        # Go to source repository
        driver.get(repository_url)

        # wait five seconds for page to load
        # input("Are you done with loggin into GitHub?")

        self.fill_in_ssh_key(hardcoded, driver, self.public_ssh_sha)

        # TODO: verify output fill_in_ssh_key does not contain:
        # "Key is invalid. You must supply a key in OpenSSH public key format"
        # TODO: verify key is indeed added.

        print(
            "Done adding the ssh deploy key from your machine to:"
            f"{github_repo_name}. Waiting 10 seconds and then the browser."
        )
        time.sleep(10)

        # close website controller
        driver.close()

        print(f"Done setting GitHub deployment token repo:{github_repo_name}.")

    @typechecked
    def open_github_build_status_repo_keys(
        self,
        driver,
        github_username,
        github_build_status_repo_name,
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
        repository_url = (
            f"https://github.com/{github_username}/"
            + f"{github_build_status_repo_name}/settings/keys/new"
        )

        # Go to source repository
        driver.get(repository_url)

        return driver

    @typechecked
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
