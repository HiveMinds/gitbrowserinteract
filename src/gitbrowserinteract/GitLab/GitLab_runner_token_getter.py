"""Object to run code based on incoming arguments."""
import time
from typing import Optional

from typeguard import typechecked

from src.gitbrowserinteract.GitLab.get_gitlab_runner_token import (
    get_gitlab_runner_registration_token_from_page,
)
from src.gitbrowserinteract.GitLab.login_gitlab import gitlab_login
from src.gitbrowserinteract.Hardcoded import Hardcoded
from src.gitbrowserinteract.helper import (
    get_runner_registration_token_filepath,
    loiter_till_gitlab_server_is_ready_for_login,
    write_string_to_file,
)


# pylint: disable=R0903
class Get_gitlab_runner_token:
    """Gets the GitLab runner from the GitLab server."""

    @typechecked
    def __init__(
        self,
        gitlab_username: Optional[str] = None,
        gitlab_pwd: Optional[str] = None,
    ):
        """Initialises object that gets the browser controller, then it gets
        the issues from the source repo, and copies them to the target repo.

        :param login: [Boolean] True if the driver object should be
        created and should login to GitHub.
        """

        # Store the hardcoded values used within this project
        hardcoded = Hardcoded()

        debugging = True
        if not debugging:
            driver, gitlab_username, gitlab_pwd = gitlab_login(
                hardcoded=hardcoded,
                gitlab_username=gitlab_username,
                gitlab_pwd=gitlab_pwd,
            )

            # Create for loop that checks if GitLab server page is loaded and ready for login.
            # loop it for 900 seconds, check page source every 5 seconds
            loiter_till_gitlab_server_is_ready_for_login(
                hardcoded=hardcoded,
                scan_duration=1200,
                interval_duration=5,
                driver=driver,
            )
            driver, _, _ = gitlab_login(
                hardcoded=hardcoded,
                gitlab_username=gitlab_username,
                gitlab_pwd=gitlab_pwd,
            )
        else:
            driver, _, _ = gitlab_login(
                hardcoded=hardcoded,
                gitlab_username=gitlab_username,
                gitlab_pwd=gitlab_pwd,
            )

        # wait five seconds for page to load
        time.sleep(5)

        runner_registration_token = (
            get_gitlab_runner_registration_token_from_page(
                hc=hardcoded, driver=driver
            )
        )

        # Export runner registration token to file
        if len(runner_registration_token) > 14:
            write_string_to_file(
                string=runner_registration_token,
                output_path=get_runner_registration_token_filepath(),
            )
        else:
            raise ValueError(
                "Expected runner registration token to be EXTRACTED from the "
                + "source code, but it is not."
            )

        # close website controller
        driver.close()

        print(
            "Got the GitLab runner registration token, can now proceed with "
            + "setting up the GitLab CI."
        )
