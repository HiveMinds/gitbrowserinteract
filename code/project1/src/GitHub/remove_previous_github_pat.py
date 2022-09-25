from code.project1.src.Website_controller import Website_controller
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

        delete_github_pat_buttons = website_controller.driver.find_elements(By.CLASS_NAME,'Box-footer')
        
        for delete_button in delete_github_pat_buttons:
            data_id_elem=delete_button.get_attribute('data-id')
            print(f'data_id_elem={data_id_elem}')
            print(f'data_id_elem.text={data_id_elem.text}')

            if int(data_id_elem) == github_pat_id:
                delete_button.click()
        #css_to_delete_button=f"html body.logged-in.env-production.page-responsive.intent-mouse div.application-main main div.pt-4.container-xl.p-responsive div.Layout.Layout--flowRow-until-md.Layout--sidebarPosition-start.Layout--sidebarPosition-flowRow-start div.Layout-main div.Layout-main-centered-md div.container-md div.settings-next div.listgroup div#access-token-{github_pat_id}.access-token.js-revoke-item div.listgroup-item div.d-flex.float-right"
        #
        #website_controller.driver.find_element("css selector",
        #    css_to_delete_button
        #).click()

        
        

    else:
        raise Exception(f'{link[:len(hardcoded.github_pat_tokens_url)]} is not:{hardcoded.github_pat_tokens_url}')