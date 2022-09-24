from code.project1.src.check_if_firefox_is_installed import remove_snap_firefox, run_bash_command
from .Hardcoded import Hardcoded
import numpy as np
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os


class Website_controller:
    """Controls/commands website using selenium."""

    def __init__(self):
        """Constructs object that controlls a firefox browser.
            TODO: Allow user to switch between running browser
        in background or foreground.
        """
        self.hardcoded = Hardcoded()
        # To run Firefox browser in foreground
        print("Loading geckodriver")
        # TODO: write a try catch, if it fails:
        # TODO: check if firefox is installed with snap.
        # TODO: if yes, ask user to uninstall and re-install with link.
        try:
            self.driver = webdriver.Firefox(executable_path=r"firefox_driver/geckodriver")
        except:
            firefox_installed_with_snap  = "snap list firefox"
            output =run_bash_command(firefox_installed_with_snap)
            if "firefox" in output:
                print(f'Please uninstall firefox and re-install it without using snap.')
                print(f"https://www.omgubuntu.co.uk/2022/04/how-to-install-firefox-deb-apt-ubuntu-22-04#:%7E:text=Installing%20Firefox%20via%20Apt%20(Not%20Snap)&text=You%20add%20the%20Mozilla%20Team,%2C%20bookmarks%2C%20and%20other%20data")
                remove_snap_firefox()

                

        # To run Firefox browser in background
        # os.environ["MOZ_HEADLESS"] = "1"
        # self.driver = webdriver.Firefox(executable_path=r"firefox_driver/geckodriver")

        # To run Chrome browser in background
        # options = webdriver.ChromeOptions();
        # options.add_argument('headless');
        # options.add_argument('window-size=1200x600'); // optional
