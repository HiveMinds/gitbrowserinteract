import time
from .control_website import open_url
from .helper import source_contains
from .get_data import get_value_from_html_source
from .helper import click_element_by_xpath


def get_runner_registration_token_from_page(website_controller):
    goto_runner_token_site(website_controller)
    visualise_runner_token(website_controller)
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


def visualise_runner_token(website_controller):
    if click_display_token_through_css_V0(website_controller):
        return website_controller
    elif unhide_registration_token_through_xpath_V1(website_controller):
        # TODO: verify whether after this function, another button must be clicked.
        return website_controller
    source = website_controller.driver.page_source
    website_controller = visualise_runner_token_through_dropdown_boxV2(
        website_controller
    )
    return website_controller


def click_display_token_through_css_V0(website_controller):
    # click the button to display registration code through css selector (if it exists)
    try:
        website_controller.driver.find_element_by_css_selector(
            ".gl-text-body\! > svg:nth-child(1)"
        ).click()
        time.sleep(2)
        return True
    except:
        print(
            f'\n\n Note: did not find button to click "unhide" runner registration token. This code proceeds and assumes the token was directly visible.'
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
        website_controller.driver.find_element_by_id("eye").click()
        return True
    except:
        print(
            f'\n\n Note: did not find the dropdownbutton that shows the "unhide" registration token button, so I currently cannot get the runner registration token.'
        )


def visualise_runner_token_through_dropdown_boxV2(website_controller):
    website_controller = click_dropdown_box_V2(website_controller)
    source = website_controller.driver.page_source
    website_controller, succesfull = click_eye_button_through_id_V2(website_controller)
    if not succesfull:
        website_controller = click_eye_button_through_xpath_V2(website_controller)
    return website_controller


def click_dropdown_box_V2(website_controller):
    source = website_controller.driver.page_source
    # Click dropdown button
    website_controller, succesfull = try_to_click_by_xpath(
        website_controller,
        '//*[@id="__BVID__31"]',
        "\n\n Did not find dropdown button in website.",
        True,
    )
    return website_controller


def click_eye_button_through_id_V2(website_controller):
    source = website_controller.driver.page_source
    website_controller, succesfull = try_to_click_by_id(
        website_controller,
        "eye",
        "\n\n Did not find unhide button with element id:eye in website.",
        False,
    )
    if not succesfull:
        source = website_controller.driver.page_source
        website_controller, succesfull = try_to_click_by_id(
            website_controller,
            "eye-icon",
            "\n\n Did not find unhide button with element id:eye-icon in website.",
            False,
        )
    return website_controller, succesfull


def click_eye_button_through_xpath_V2(website_controller):
    source = website_controller.driver.page_source
    website_controller, succesfull = try_to_click_by_xpath(
        website_controller,
        "/html/body/div[3]/div/div[3]/main/div[2]/div[2]/div[2]/ul/div/div/li[3]/form/fieldset/div/div/button[1]",
        "xpath-eye try 0",
        False,
    )
    if not succesfull:
        source = website_controller.driver.page_source
        website_controller, succesfull = try_to_click_by_xpath(
            website_controller,
            "/html/body/div[3]/div/div[3]/main/div[2]/div[2]/div[2]/ul/div/div/li[3]/form/fieldset/div/div/button[1]/svg",
            "xpath-eye try 1",
            False,
        )
    if not succesfull:
        source = website_controller.driver.page_source
        website_controller, succesfull = try_to_click_by_xpath(
            website_controller,
            "/html/body/div[3]/div/div[3]/main/div[2]/div[2]/div[2]/ul/div/div/li[3]/form/fieldset/div/div/button[1]/svg/use",
            "xpath-eye try 2",
            False,
        )

    if not succesfull:
        source = website_controller.driver.page_source
        website_controller, succesfull = try_to_click_by_xpath(
            website_controller,
            '//*[@id="eye"]',
            "xpath-eye try 3",
            False,
        )

    if not succesfull:
        source = website_controller.driver.page_source
        website_controller, succesfull = try_to_click_by_xpath(
            website_controller,
            "/symbol/path",
            "xpath-eye try 4",
            True,
        )

    return website_controller


def try_to_click_by_id(website_controller, id, error_msg, raise_error):
    try:
        # Click the button to display registration code through element id
        website_controller.driver.find_element_by_id(id).click()
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
