from code.project1.src.control_website import open_url, wait_until_page_is_loaded
from selenium.webdriver.common.by import By

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
        if hardcoded.github_pat_description in elem.text:
            # Find delete button

            # Delete the GitHub personal access token.
