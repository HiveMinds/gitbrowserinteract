import time
from .control_website import open_url
from .helper import source_contains
from .get_data import get_value_from_html_source
from .helper import click_element_by_xpath


def get_gitlab_runner_registration_token_from_page(hc,website_controller):
    goto_runner_token_site(website_controller)
    visualise_runner_token(hc,website_controller)
    gitlab_runner_token = read_gitlab_runner_token_from_page(website_controller)
    print(f"gitlab_runner_token={gitlab_runner_token}")
    return gitlab_runner_token


def goto_runner_token_site(website_controller):
    # visit website with runner token
    website_controller.driver = open_url(
        website_controller.driver, "http://127.0.0.1/admin/runners"
    )

    # wait five seconds for page to load
    time.sleep(5)


def visualise_runner_token(hc,website_controller):
    if click_display_token_through_css_V0(website_controller):
        return website_controller
    elif unhide_registration_token_through_xpath_V1(website_controller):
        # TODO: verify whether after this function, another button must be clicked.
        return website_controller
    source = website_controller.driver.page_source
    website_controller = visualise_runner_token_through_dropdown_boxV2(
        hc,
        website_controller
    )
    return website_controller


def click_display_token_through_css_V0(website_controller):
    # click the button to display registration code through css selector (if it exists)
    try:
        website_controller.driver.find_element("css selector",
            ".gl-text-body\! > svg:nth-child(1)"
        ).click()
        time.sleep(2)
        return True
    except:
        print(
            f'\n\n Note: did not find button to click "unhide" runner registration token with first method. Will try second method now.'
        )
        return False


def unhide_registration_token_through_xpath_V1(website_controller):
    try:
        # Click unhide registration-token through xpath
        click_element_by_xpath(
            website_controller,
            #'/html/body/div[3]/div/div[3]/main/div[2]/div[1]/div[2]/div/ol/li[3]/code/span/button/svg',
            '//*[@id="eye"]',
            #'/symbol/path',
        )

        # Click the button to display registration code through element id
        website_controller.driver.find_element("id", "eye").click()
        return True
    except:
        print(
            f'\n\n Note: did not find button to click "unhide" runner registration token with second method. Will try third method now.'
        )


def visualise_runner_token_through_dropdown_boxV2(hc,website_controller):
    website_controller = click_dropdown_box_V2(website_controller)
    source = website_controller.driver.page_source
    website_controller, succesfull = click_eye_button_through_id_V2(website_controller)
    if not succesfull:
        website_controller = gitlab_click_eye_button_through_xpath_V2(hc,website_controller)
    return website_controller


def click_dropdown_box_V2(website_controller):
    source = website_controller.driver.page_source
    # Click dropdown button
    website_controller, succesfull = try_to_click_by_xpath(
        website_controller,
        '//*[@id="__BVID__31"]',
        "\n\n Note: did not find button to dropwdown the runner registration token box with third method. Will try fourth method now.",
        True,
    )
    return website_controller


def click_eye_button_through_id_V2(website_controller):
    source = website_controller.driver.page_source
    website_controller, succesfull = try_to_click_by_id(
        website_controller,
        "eye",
        '\n\n Note: did not find button to click the "eye" icon fourth method. Will try fifth method now.',
        False,
    )
    if not succesfull:
        source = website_controller.driver.page_source
        website_controller, succesfull = try_to_click_by_id(
            website_controller,
            "eye-icon",
            '\n\n Note: did not find button to click the "eye" icon fourth method. Will try sixth method now.',
            False,
        )
    return website_controller, succesfull


def gitlab_click_eye_button_through_xpath_V2(hc,website_controller):
    successfull=False
    for xpath in hc.gitlab_eye_xpaths:
        if not successfull:
            source = website_controller.driver.page_source
            website_controller, succesfull = try_to_click_by_xpath(
                website_controller,
                xpath,for xpa
                "xpath-eye try 0",
                False,
            )
        time.sleep(1)

    if not succesfull:
        raise Exception("Did not find the GitLab Runner Registration token.")
    ###if not succesfull:
    ###    source = website_controller.driver.page_source
    ###    website_controller, succesfull = try_to_click_by_xpath(
    ###        website_controller,
    ###        "/symbol/path/",
    ###        "xpath-eye try 4",
    ###        True,
    ###    )

    return website_controller


def try_to_click_by_id(website_controller, id, error_msg, raise_error):
    try:
        # Click the button to display registration code through element id
        website_controller.driver.find_element("id", id).click()
        print(f"found_by_id")
        return website_controller, True
    except:
        if raise_error:
            raise Exception(error_msg)
        else:
            print(error_msg)
            return website_controller, False


def try_to_click_by_xpath(website_controller, xpath, error_msg, raise_error):
    try:
        # Click the button to display registration code through element id
        website_controller = click_element_by_xpath(
            website_controller,
            xpath,
        )
        print(f"found_by_xpath")
        return website_controller, True
    except:
        if raise_error:
            raise Exception(error_msg)
        else:
            print(error_msg)
            return website_controller, False


def read_gitlab_runner_token_from_page(website_controller):
    # get the page source:
    source = website_controller.driver.page_source

    token_identification_string_0 = '<code id="registration_token">'
    token_identification_string_1 = 'data-registration-token="'
    token_identification_string_2 = 'data-clipboard-text="'

    token_identification_string_3 = '<code data-testid="registration-token"><span>'

    # TODO: New update requires clicking dropdown box, xpath=

    # verify the source contains the runner token
    if not source_contains(website_controller, token_identification_string_0):
        if not source_contains(website_controller, token_identification_string_1):
            if not source_contains(website_controller, token_identification_string_2):
                if not source_contains(
                    website_controller, token_identification_string_3
                ):
                    raise Exception(
                        f"Expected runner registration token to be CONTAINED in the source code, but it is not: {source}."
                    )
                else:
                    return get_value_from_html_source(
                        source, token_identification_string_3, "</code>"
                    )
            else:
                return get_value_from_html_source(
                    source, token_identification_string_2, '"'
                )
        else:
            return get_value_from_html_source(
                source, token_identification_string_1, '"'
            )
    else:
        # Extract the runner registration token from the source code
        return get_value_from_html_source(
            source, token_identification_string_0, "</code>"
        )
