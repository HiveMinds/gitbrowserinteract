# Code that automatically copies all issues of a repository to another
from .control_website import login
from .Hardcoded import Hardcoded
from .helper import get_labels_from_issues
from .get_data import get_value_from_html_source
from .get_gitlab_runner_token import get_runner_registration_token_from_page
from .get_website_controller import get_website_controller
from .helper import get_browser_drivers
from .helper import parse_creds
from .helper import click_element_by_xpath
from .helper import get_runner_registration_token_filepath
from .helper import source_contains
from .helper import write_string_to_file
from .helper import loiter_till_gitlab_server_is_ready_for_login
from .control_website import open_url
from .Website_controller import Website_controller
from .get_data import get_issues
from .set_data import set_labels
from .set_data import set_issues
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time


class Main:
    """ """

    def __init__(self, project_nr, should_login=True):
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

        # get browser drivers
        get_browser_drivers(self.hc)

        website_controller = get_website_controller(self.hc)

        # Create for loop that checks if GitLab server page is loaded and ready for login.
        # loop it for 900 seconds, check page source every 5 seconds
        loiter_till_gitlab_server_is_ready_for_login(
            self.hc, 1200, 5, website_controller
        )

        # Log into GitLab server.
        website_controller = login(self.hc)

        # wait five seconds for page to load
        time.sleep(5)

        runner_registration_token = get_runner_registration_token_from_page(
            website_controller
        )

        # Export runner registration token to file
        if len(runner_registration_token) > 14:
            write_string_to_file(
                runner_registration_token, get_runner_registration_token_filepath()
            )
        else:
            raise Exception(
                "Expected runner registration token to be EXTRACTED from the source code, but it is not."
            )

        # close website controller
        website_controller.driver.close()

        print(
            f"Got the GitLab runner registration token, can now proceed with setting up the GitLab CI."
        )


if __name__ == "__main__":
    # initialize main class
    main = Main()
