# Code that automatically copies all issues of a repository to another
from .control_website import login
from .Hardcoded import Hardcoded
from .helper import get_labels_from_issues
from .get_website_controller import get_website_controller
from .get_data import get_value_from_html_source
from .helper import get_browser_drivers
from .helper import parse_creds
from .helper import click_element_by_xpath
from .helper import get_runner_registration_token_filepath
from .helper import source_contains
from .helper import write_string_to_file
from .control_website import open_url
from .Website_controller import Website_controller
from .get_data import get_issues
from .set_data import set_labels
from .set_data import set_issues
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
        
        website_controller = login(self.hc)

        # wait five seconds for page to load
        time.sleep(5)

        # visit website with runner token
        website_controller.driver = open_url(website_controller.driver, "http://127.0.0.1/admin/runners")

        # wait five seconds for page to load
        time.sleep(5)

        # get the page source:
        source = website_controller.driver.page_source

        # verify the source contains the runner token
        if not source_contains(website_controller,'<code id="registration_token">'):
           raise Exception("Expected runner registration token to be contained in the source code, but it is not.")

        # Extract the runner registration token from the source code
        runner_registration_token = get_value_from_html_source(source, '<code id="registration_token">', '</code>')

        # Export runner registration token to file
        write_string_to_file(runner_registration_token, get_runner_registration_token_filepath())

        # close website controller
        website_controller.driver.close()


        print(f'Done.')

if __name__ == "__main__":
    # initialize main class
    main = Main()
