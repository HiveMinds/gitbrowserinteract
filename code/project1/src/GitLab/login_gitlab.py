"""Performs GitLab login."""


def user_is_logged_in_in_gitlab(hardcoded, driver):
    """Returns True if the user is logged in, False otherwise."""
    source = driver.page_source
    if hardcoded.gitlab_logged_in_or_not_string in source:
        return True
    return False
