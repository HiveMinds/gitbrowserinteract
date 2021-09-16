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

        # Click unhide registration-token through xpath
        #click_element_by_xpath(
        #    website_controller,
        #    #'/html/body/div[3]/div/div[3]/main/div[2]/div[1]/div[2]/div/ol/li[3]/code/span/button/svg',
        #    '//*[@id="eye"]',
        #    #'/symbol/path',
        #)
        
        # click the button to display registration code through element id
        #website_controller.driver.find_element_by_id("eye").click()
        
        # click the button to display registration code through css selector (if it exists)
        try:
            website_controller.driver.find_element_by_css_selector(".gl-text-body\! > svg:nth-child(1)").click()
        except:
            print(f'\n\n Note: did not find button to click "unhide" runner registration token. This code proceeds and assumes the token was directly visible.')
        
        time.sleep(2)
        
        # get the page source:
        source = website_controller.driver.page_source
        
        token_identification_string_0='<code id="registration_token">'
        #token_identification_string_1='data-registration-token='
        token_identification_string_2='<code data-testid="registration-token"><span>'
        
        
        # verify the source contains the runner token
        if not source_contains(website_controller,token_identification_string_0):
            if not source_contains(website_controller,token_identification_string_2):
                raise Exception("Expected runner registration token to be CONTAINED in the source code, but it is not.")

        # Extract the runner registration token from the source code
        runner_registration_token_0 = get_value_from_html_source(source, token_identification_string_0, '</code>')
        runner_registration_token_2 = get_value_from_html_source(source, token_identification_string_0, '</code>')
        
        # Export runner registration token to file
        if len(runner_registration_token_0)>14:
            write_string_to_file(runner_registration_token_0, get_runner_registration_token_filepath())
        elif len(runner_registration_token_2)>14:
            write_string_to_file(runner_registration_token_2, get_runner_registration_token_filepath())
        else:
            raise Exception("Expected runner registration token to be EXTRACTED from the source code, but it is not.")
        
        # close website controller
        website_controller.driver.close()
        
        print(f'Done.')

if __name__ == "__main__":
    # initialize main class
    main = Main()
