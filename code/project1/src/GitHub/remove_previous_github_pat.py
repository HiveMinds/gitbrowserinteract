from pprint import pprint
from typing import List
from code.project1.src.Website_controller import Website_controller
from code.project1.src.control_website import  open_url, wait_until_page_is_loaded
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains
from code.project1.src.helper import scroll_shim

def remove_previous_github_pat(hardcoded,website_controller):
    """Assumes the user is logged in into GitHub. Then lists the already 
    existing GitHub personal access token (PAT) descriptions. If the new GitHub
    PAT description is already existing, it deletes the existing GitHub PAT. 
    Then it verifies the GitHub PAT is not yet in GitHub/is removed 
    succesfully."""

    # Check if the token exists, and if yes, get a link containing token id.
    github_pat_exists,link =github_pat_description_exists(hardcoded,website_controller)
    if github_pat_exists:

        # Delete the GitHub personal access token.
        delete_github_pat(link,hardcoded,website_controller)
            
    # Verify token is deleted.
    if github_pat_description_exists(hardcoded,website_controller)[0]:
        raise Exception("Error, GitHub pat is not deleted succesfully.")
        

def github_pat_description_exists(hardcoded,website_controller):
    """Assumes the user is logged in into GitHub. Then lists the already 
    existing GitHub personal access token (PAT) descriptions. If the new GitHub
    PAT description is already existing, it returns True, otherwise returns 
    False. Also returns the url of the GitHub pat that contains the token id."""
    # Go to url containing GitHub pat.
    website_controller.driver = open_url(
        website_controller.driver,
        hardcoded.github_pat_tokens_url,
    )
    # Wait until url is loaded. 
    wait_until_page_is_loaded(6,website_controller)

    # Get the token descriptions through the href element.
    elems = website_controller.driver.find_elements(By.CSS_SELECTOR,f".{hardcoded.github_pat_description_elem_classname} [href]")
    for elem in elems:
        link=elem.get_attribute('href')
        if hardcoded.github_pat_description in elem.text:
            return True, link
    return False, None

            

def delete_github_pat(link,hardcoded,website_controller):
    """Gets the GitHub pat id from the link, then clicks the delete button, and
    the confirm deletion button, to delete the GitHub pat."""
    
    if link[:len(hardcoded.github_pat_tokens_url)] == hardcoded.github_pat_tokens_url:
        github_pat_id=int(link[len(hardcoded.github_pat_tokens_url):])
        print(f'github_pat_id={github_pat_id}')

        # Get the right table row nr.
        valid_indices=list_of_valid_xpath_indices([],f"{hardcoded.github_pat_table_xpath}/div[","]",website_controller)
        row_nr= get_desired_token_index(hardcoded,website_controller,valid_indices)
        
        # Click delete button and deletion confirmation button.
        click_github_pat_delete_button(hardcoded,website_controller,row_nr)
    else:
        raise Exception(f'{link[:len(hardcoded.github_pat_tokens_url)]} is not:{hardcoded.github_pat_tokens_url}')

def list_of_valid_xpath_indices(valid_indices,left,right,website_controller):
    """Returns the row numbers of the GitHub personal access tokens table, 
    starting at index =1. Basically gets how much GitHub pats are stored."""
    if valid_indices == []:
        latest_index=1
    else:
        latest_index=valid_indices[-1]+1

    try:
        row = website_controller.driver.find_element(By.XPATH,
            f"{left}{latest_index}{right}"
            )
        if not row is None:
            print(row.text)
            valid_indices.append(latest_index)
            return list_of_valid_xpath_indices(valid_indices,left,right,website_controller)
        else:
            return valid_indices
    except:
        if len(valid_indices) ==0:
            raise Exception("Did not find any valid indices.")
        return valid_indices

def get_desired_token_index(hardcoded,website_controller,valid_indices:List[int]):
    """Finds the index/row number of the GitHub pat's that corresponds to the 
    description of the GitHub pat that is to be created, and returns this 
    index."""
    for row_nr in valid_indices:
        row_elem = website_controller.driver.find_element(By.XPATH,
            f"{hardcoded.github_pat_table_xpath}/div[{row_nr}]"
            )
        if hardcoded.github_pat_description in row_elem.text:
            return row_nr

def click_github_pat_delete_button(hardcoded,website_controller,row_nr:int):
    """Clicks the delete GitHub pat button, and then clicks the confirm 
    deletion button."""
    delete_button  = website_controller.driver.find_element(By.XPATH,
            f"{hardcoded.github_pat_table_xpath}/div[{row_nr}]/div/div[1]/details/summary"
            )
    delete_button.click()

    confirm_deletion_button = website_controller.driver.find_element(By.XPATH,
            f"{hardcoded.github_pat_table_xpath}/div[{row_nr}]/div/div[1]/details/details-dialog/div[4]/form/button"
            )
    confirm_deletion_button.click()