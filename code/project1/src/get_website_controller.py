"""Returns the website controller object."""
from .control_website import gitlab_login
from .helper import get_browser_drivers


def get_website_controller(hc):
    """USED Monitors the subscription availabilities of the Radboud University
    Sports Centre. Gets the desired user schedule and enrolls the user for the
    desired schedule when available.

    :param hc: An object containing all the hardcoded settings used in this program.
    """
    # get browser drivers
    get_browser_drivers(hc)

    # login GitHub
    website_controller = gitlab_login(hc)
    return website_controller
