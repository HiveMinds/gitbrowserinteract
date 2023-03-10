"""Gets a website controller and opens it."""
from Hardcoded import Hardcoded
from selenium import webdriver
from typeguard import typechecked


# pylint: disable=R0903
class driver:
    """Controls/commands website using selenium."""

    @typechecked
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
            self.driver = webdriver.Firefox(
                executable_path=r"firefox_driver/geckodriver"
            )
        # pylint: disable=W0707
        except:
            # pylint: disable=W0707
            raise ValueError(
                "Error, you have the snap Firefox browser installed"
                + ". Please use the apt one instead. This switching is automated"
                + " in a bash script of the Self-host GitLab."
            )

        # To run Firefox browser in background
        # os.environ["MOZ_HEADLESS"] = "1"
        # self.driver = webdriver.Firefox(executable_path=r"firefox_driver/geckodriver")

        # To run Chrome browser in background
        # options = webdriver.ChromeOptions();
        # options.add_argument('headless');
        # options.add_argument('window-size=1200x600'); // optional
