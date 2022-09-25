from pprint import pprint
from code.project1.src.Website_controller import Website_controller
from code.project1.src.control_website import click_element_by_xpath, open_url, wait_until_page_is_loaded
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains
from code.project1.src.helper import scroll_shim

def remove_previous_github_pat(hardcoded,website_controller):
    """Assumes the user is logged in into GitHub. Then lists the already 
    existing GitHub personal access token (PAT) descriptions. If the new GitHub
    PAT description is already existing, it deletes the existing GitHub PAT. 
    Then it verifies the GitHub PAT is not yet in GitHub/is removed 
    succesfully."""

    if github_pat_description_exists(hardcoded,website_controller):

        # Delete the token.
        pass

    # Verify token is deleted.
    if not github_pat_description_exists(hardcoded,website_controller):
        raise Exception("Error, GitHub pat is not deleted succesfully.")
        

def github_pat_description_exists(hardcoded,website_controller):
    """Assumes the user is logged in into GitHub. Then lists the already 
    existing GitHub personal access token (PAT) descriptions. If the new GitHub
    PAT description is already existing, it returns True, otherwise returns 
    False."""
    # Go to url.
    website_controller.driver = open_url(
        website_controller.driver,
        hardcoded.github_pat_tokens_url,
    )
    # Wait until url is loaded. 
    wait_until_page_is_loaded(6,website_controller)

    # source
    #source = website_controller.driver.page_source
    
    # Get list of GitHub personal access token descriptions.
    github_pat_elements = website_controller.driver.find_elements(By.CLASS_NAME,hardcoded.github_pat_description_elem_classname)
    

    elems = website_controller.driver.find_elements(By.CSS_SELECTOR,f".{hardcoded.github_pat_description_elem_classname} [href]")
    #links = [elem.get_attribute('href') for elem in elems]
    for elem in elems:
        link=elem.get_attribute('href')
        print(f'link={link}')
        print(f'text={elem.text}')
        print(f'Set GitHub commit build status values.')
        print(hardcoded.github_pat_description)
        if hardcoded.github_pat_description in elem.text:
            # Find delete button
            find_delete_github_pat_button(link,hardcoded,website_controller)
            # Delete the GitHub personal access token.
            

def find_delete_github_pat_button(link,hardcoded,website_controller):
    if link[:len(hardcoded.github_pat_tokens_url)] == hardcoded.github_pat_tokens_url:
        github_pat_id=int(link[len(hardcoded.github_pat_tokens_url):])
        print(f'github_pat_id={github_pat_id}')

        table = website_controller.driver.find_element(By.XPATH,
        hardcoded.github_pat_table_xpath
        )
        print("table")
        print(table)
        print(table.text)
        print_attributes_of_elements([table],website_controller)

        valid_indices=list_of_valid_xpath_indices([],f"{hardcoded.github_pat_table_xpath}/div[","]",website_controller)
        print(f'valid_indices={valid_indices}')
    else:
        raise Exception(f'{link[:len(hardcoded.github_pat_tokens_url)]} is not:{hardcoded.github_pat_tokens_url}')


def print_attributes_of_elements(elements,website_controller):
    for elem in elements:
        attrs = website_controller.driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', elem)
        pprint(attrs)

def list_of_valid_xpath_indices(valid_indices,left,right,website_controller):
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