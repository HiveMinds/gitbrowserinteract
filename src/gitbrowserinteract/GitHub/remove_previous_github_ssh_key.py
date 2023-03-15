"""Removes pre-existing GitHub SSH deploy keys with the same name if they
exist."""
from typing import Any, List

from selenium.webdriver.common.by import By
from typeguard import typechecked

from ..control_website import wait_until_page_is_loaded
from ..Hardcoded import Hardcoded
from ..helper import open_url


@typechecked
def remove_previous_github_ssh_key(
    *, github_username: str, hardcoded: Hardcoded, driver: Any
) -> None:
    """Assumes the user is logged in into GitHub.

    Then lists the already existing GitHub personal access token (PAT)
    descriptions. If the new GitHub PAT description is already existing,
    it deletes the existing GitHub PAT. Then it verifies the GitHub PAT
    is not yet in GitHub/is removed succesfully.

    :param github_username:
    :param hardcoded:
    :param driver:
    """

    # Check if the token exists, and if yes, get a link containing token id.
    while github_ssh_key_description_exists(
        github_username=github_username, hardcoded=hardcoded, driver=driver
    ):
        # Delete the GitHub personal access token.
        delete_github_ssh_key(hardcoded=hardcoded, driver=driver)

    # Verify token is deleted.
    if github_ssh_key_description_exists(
        github_username=github_username, hardcoded=hardcoded, driver=driver
    ):
        raise SystemError("Error, GitHub ssh_key is not deleted succesfully.")


@typechecked
def github_ssh_key_description_exists(
    *, github_username: str, hardcoded: Hardcoded, driver: Any
) -> bool:
    """Assumes the user is logged in into GitHub.

    Then lists the already existing GitHub personal access token (PAT)
    descriptions. If the new GitHub PAT description is already existing,
    it returns True, otherwise returns False. Also returns the url of
    the GitHub ssh_key that contains the token id.

    :param github_username:
    :param hardcoded:
    :param driver:
    """
    # Go to url containing GitHub ssh_key.
    driver = open_url(
        driver=driver,
        url=hardcoded.github_ssh_key_tokens_url.replace(
            hardcoded.github_username_placeholder, github_username
        ),
    )
    # Wait until url is loaded.
    wait_until_page_is_loaded(time_limit_sec=6, driver=driver)

    # Get the token descriptions through the href element.
    if (
        len(
            list_of_valid_xpath_indices(
                valid_indices=[],
                left=f"{hardcoded.github_ssh_key_table_xpath}/li[",
                right="]",
                driver=driver,
            )
        )
        > 0
    ):
        return True
    return False


@typechecked
def delete_github_ssh_key(*, hardcoded: Hardcoded, driver: Any) -> None:
    """Gets the GitHub ssh_key id from the link, then clicks the delete button,
    and the confirm deletion button, to delete the GitHub ssh_key.

    :param hardcoded:
    :param driver:
    """

    # Get the right table row nr.
    valid_indices = list_of_valid_xpath_indices(
        valid_indices=[],
        left=f"{hardcoded.github_ssh_key_table_xpath}/li[",
        right="]",
        driver=driver,
    )
    row_nr = get_desired_token_index(
        hardcoded=hardcoded, driver=driver, valid_indices=valid_indices
    )

    # Click delete button and deletion confirmation button.
    click_github_ssh_key_delete_button(
        hardcoded=hardcoded, driver=driver, row_nr=row_nr
    )


@typechecked
def list_of_valid_xpath_indices(
    *, valid_indices, left, right, driver
) -> List[int]:
    """Returns the row numbers of the GitHub personal access tokens table,
    starting at index =1.

    Basically gets how much GitHub ssh_keys are stored.

    :param valid_indices:
    :param left:
    :param right:
    :param driver:
    """
    if valid_indices == []:
        latest_index = 1
    else:
        latest_index = valid_indices[-1] + 1

    try:
        row = driver.find_element(By.XPATH, f"{left}{latest_index}{right}")
        if row is not None:
            print(row.text)
            valid_indices.append(latest_index)
            return list_of_valid_xpath_indices(
                valid_indices=valid_indices,
                left=left,
                right=right,
                driver=driver,
            )
        return valid_indices
    # pylint: disable=W0702
    except:
        return valid_indices


# pylint: disable=R1710
@typechecked
def get_desired_token_index(
    *, hardcoded: Hardcoded, driver: Any, valid_indices: List[int]
) -> int:
    """Finds the index/row number of the GitHub ssh_key's that corresponds to
    the description of the GitHub ssh_key that is to be created, and returns
    this index.
    TODO: first check if table has the token, and then return it, otherwise
    don't call this function (To disable pylint: disable=R1710)

    :param hardcoded:
    :param driver:
    :param valid_indices: List[int]:
    """
    for row_nr in valid_indices:
        row_elem = driver.find_element(
            By.XPATH, f"{hardcoded.github_ssh_key_table_xpath}/li[{row_nr}]"
        )
        if hardcoded.github_ssh_key_description in row_elem.text:
            return row_nr


@typechecked
def click_github_ssh_key_delete_button(
    *, hardcoded: Hardcoded, driver: any, row_nr: int
) -> None:
    """Clicks the delete GitHub ssh_key button, and then clicks the confirm
    deletion button.

    :param hardcoded:
    :param driver:
    :param row_nr: int:
    """
    delete_button = driver.find_element(
        By.XPATH,
        f"{hardcoded.github_ssh_key_table_xpath}/li[{row_nr}]/span[3]/div/details/summary",
    )
    delete_button.click()

    confirm_deletion_button = driver.find_element(
        By.XPATH,
        (
            f"{hardcoded.github_ssh_key_table_xpath}/li[{row_nr}]"
            + "/span[3]/div/details/details-dialog/div[3]/form/button"
        ),
    )
    confirm_deletion_button.click()
