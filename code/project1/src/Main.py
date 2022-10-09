"""Object to run code based on incoming arguments."""
import time

from .control_website import gitlab_login
from .get_gitlab_runner_token import (
    get_gitlab_runner_registration_token_from_page,
)
from .get_website_controller import get_website_controller
from .Hardcoded import Hardcoded
from .helper import (
    get_browser_drivers,
    get_runner_registration_token_filepath,
    loiter_till_gitlab_server_is_ready_for_login,
    write_string_to_file,
)


# pylint: disable=R0903
class Main:
    """Object to run code based on incoming arguments."""

    def __init__(self, project_nr):
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

        # get browser drivers
        get_browser_drivers(self.hc)

        website_controller = get_website_controller(self.hc)

        # Create for loop that checks if GitLab server page is loaded and ready for login.
        # loop it for 900 seconds, check page source every 5 seconds
        loiter_till_gitlab_server_is_ready_for_login(
            self.hc, 1200, 5, website_controller
        )

        # Log into GitLab server.
        website_controller = gitlab_login(self.hc)

        # wait five seconds for page to load
        time.sleep(5)

        runner_registration_token = (
            get_gitlab_runner_registration_token_from_page(
                self.hc, website_controller
            )
        )

        # Export runner registration token to file
        if len(runner_registration_token) > 14:
            write_string_to_file(
                runner_registration_token,
                get_runner_registration_token_filepath(),
            )
        else:
            raise Exception(
                "Expected runner registration token to be EXTRACTED from the "
                + "source code, but it is not."
            )

        # close website controller
        website_controller.driver.close()

        print(
            "Got the GitLab runner registration token, can now proceed with "
            + "setting up the GitLab CI."
        )
