"""Removes previously existing GitHub personal access tokens, if they exist."""
from code.project1.src.control_website import wait_until_page_is_loaded
from typing import List

from selenium.webdriver.common.by import By


def remove_previous_github_pat(*, hardcoded, driver):
    """Assumes the user is logged in into GitHub.

    Then lists the already existing GitHub personal access token (PAT)
    descriptions. If the new GitHub PAT description is already existing,
    it deletes the existing GitHub PAT. Then it verifies the GitHub PAT
    is not yet in GitHub/is removed succesfully.
    """

    # Check if the token exists, and if yes, get a link containing token id.
    github_pat_exists, link = github_pat_description_exists(hardcoded, driver)
    if github_pat_exists:
        # Delete the GitHub personal access token.
        delete_github_pat(link, hardcoded, driver)

    # Verify token is deleted.
    if github_pat_description_exists(hardcoded, driver)[0]:
        raise Exception("Error, GitHub pat is not deleted succesfully.")


def github_pat_description_exists(hardcoded, driver):
    """Assumes the user is logged in into GitHub.

    Then lists the already existing GitHub personal access token (PAT)
    descriptions. If the new GitHub PAT description is already existing,
    it returns True, otherwise returns False. Also returns the url of
    the GitHub pat that contains the token id.
    """
    # Go to url containing GitHub pat.
    driver.get(hardcoded.github_pat_tokens_url)

    # Wait until url is loaded.
    wait_until_page_is_loaded(6, driver)

    # Get the token descriptions through the href element.
    elems = driver.find_elements(
        By.CSS_SELECTOR,
        f".{hardcoded.github_pat_description_elem_classname} [href]",
    )
    for elem in elems:
        link = elem.get_attribute("href")
        if hardcoded.github_pat_description in elem.text:
            return True, link
    return False, None


def delete_github_pat(link, hardcoded, driver):
    """Gets the GitHub pat id from the link, then clicks the delete button, and
    the confirm deletion button, to delete the GitHub pat."""

    if (
        link[: len(hardcoded.github_pat_tokens_url)]
        == hardcoded.github_pat_tokens_url
    ):
        github_pat_id = int(link[len(hardcoded.github_pat_tokens_url) :])
        print(f"github_pat_id={github_pat_id}")

        # TODO: make this method more robust, e.g. by clicking on element
        # based on text or finding table based on id: listgroup.
        # Get the right table row nr.
        valid_indices = list_of_valid_xpath_indices(
            valid_indices=[],
            left=f"{hardcoded.github_pat_table_xpath}/div[",
            right="]",
            driver=driver,
        )
        row_nr = get_desired_token_index(hardcoded, driver, valid_indices)

        # Click delete button and deletion confirmation button.
        click_github_pat_delete_button(hardcoded, driver, row_nr)
    else:
        raise Exception(
            f"{link[:len(hardcoded.github_pat_tokens_url)]}"
            + f" is not:{hardcoded.github_pat_tokens_url}"
        )


def list_of_valid_xpath_indices(*, valid_indices, left, right, driver):
    """Returns the row numbers of the GitHub personal access tokens table,
    starting at index =1.

    Basically gets how much GitHub pats are stored.
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
                valid_indices, left, right, driver
            )
        return valid_indices
    # pylint: disable=W0702
    except:
        if len(valid_indices) == 0:
            # pylint: disable=W0707
            raise Exception(
                "Did not find any valid indices. So was not able "
                "to delete the previous GitHub PAT token."
            )
        return valid_indices


# pylint: disable=R1710
def get_desired_token_index(hardcoded, driver, valid_indices: List[int]):
    """TODO: remove duplicate function, fix pylint: disable=R1710.
    Finds the index/row number of the GitHub pat's that corresponds to the
    description of the GitHub pat that is to be created, and returns this
    index."""
    for row_nr in valid_indices:
        row_elem = driver.find_element(
            By.XPATH, f"{hardcoded.github_pat_table_xpath}/div[{row_nr}]"
        )
        if hardcoded.github_pat_description in row_elem.text:
            return row_nr


def click_github_pat_delete_button(hardcoded, driver, row_nr: int):
    """Clicks the delete GitHub pat button, and then clicks the confirm
    deletion button."""
    delete_button = driver.find_element(
        By.XPATH,
        f"{hardcoded.github_pat_table_xpath}/div[{row_nr}]/div/div[1]/details/summary",
    )
    delete_button.click()

    confirm_deletion_button = driver.find_element(
        By.XPATH,
        (
            f"{hardcoded.github_pat_table_xpath}/div[{row_nr}]"
            + "/div/div[1]/details/details-dialog/div[4]/form/button"
        ),
    )
    confirm_deletion_button.click()
