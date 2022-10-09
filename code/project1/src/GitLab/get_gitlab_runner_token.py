"""Gets the GitLab runner token from local GitLab server and stores it in local
personal credentials.

TODO: Change to get it from within docker instead
of using browser controller.
"""
import time
from code.project1.src.helper import (
    click_element_by_xpath,
    get_value_from_html_source,
    open_url,
    source_contains,
)


def get_gitlab_runner_registration_token_from_page(hc, website_controller):
    """

    :param hc:
    :param website_controller:

    """
    goto_runner_token_site(website_controller)
    visualise_runner_token(hc, website_controller)
    gitlab_runner_token = read_gitlab_runner_token_from_page(
        website_controller
    )
    print(f"gitlab_runner_token={gitlab_runner_token}")
    return gitlab_runner_token


def goto_runner_token_site(website_controller):
    """

    :param website_controller:

    """
    # visit website with runner token
    website_controller.driver = open_url(
        website_controller.driver, "http://127.0.0.1/admin/runners"
    )

    # wait five seconds for page to load
    time.sleep(5)


def visualise_runner_token(hc, website_controller):
    """

    :param hc:
    :param website_controller:

    """
    # if click_display_token_through_css_V0(website_controller):
    #    return website_controller
    # if unhide_registration_token_through_xpath_V1(website_controller):
    #    # TODO: verify whether after this function, another button must be clicked.
    #    return website_controller

    website_controller = gitlab_visualise_runner_token_through_dropdown_boxV2(
        hc, website_controller
    )
    return website_controller


def click_display_token_through_css_V0(website_controller):
    """

    :param website_controller:

    """
    # click the button to display registration code through css selector (if it exists)
    try:
        website_controller.driver.find_element(
            "css selector", r".gl-text-body\! > svg:nth-child(1)"
        ).click()
        time.sleep(2)
        return True
    # pylint: disable=W0702
    except:
        print(
            '\n \n Note: did not find button to click "unhide" runner '
            + "registration token with first method. Will try second method now"
        )
        return False


def unhide_registration_token_through_xpath_V1(website_controller):
    """Tries to show the GitLab runner registration token.

    :param website_controller:
    """
    try:
        # Click unhide registration-token through xpath
        click_element_by_xpath(
            website_controller,
            '//*[@id="eye"]',
        )

        # Click the button to display registration code through element id
        website_controller.driver.find_element("id", "eye").click()
        return True
    # pylint: disable=W0702
    except:
        print(
            '\n \n Note: did not find button to click "unhide"runner '
            + "registration token with second method. Will try third method now"
        )
        return False


def gitlab_visualise_runner_token_through_dropdown_boxV2(
    hc, website_controller
):
    """

    :param hc:
    :param website_controller:

    """
    website_controller = click_dropdown_box_V2(website_controller)
    time.sleep(2)
    website_controller, successfull = gitlab_click_eye_button_through_xpath_V2(
        hc, website_controller
    )
    if not successfull:
        (
            website_controller,
            successfull,
        ) = gitlab_click_eye_button_through_id_V2(hc, website_controller)
    if not successfull:
        input(
            "Please manually click the eye button to show the GitLab"
            + "runner registration token."
        )
        # raise Exception("Did not find the GitLab Runner Registration token.")

    return website_controller


def click_dropdown_box_V2(website_controller):
    """

    :param website_controller:

    """

    # Click dropdown button
    website_controller, _ = try_to_click_by_xpath(
        website_controller,
        '//*[@id="__BVID__31"]',
        (
            "\n \n Note: did not find button to dropwdown the runner registration"
            + " token box with third method. Will try fourth method now."
        ),
        True,
    )
    return website_controller


def gitlab_click_eye_button_through_xpath_V2(hc, website_controller):
    """

    :param website_controller:

    """

    successfull = False
    for i, xpath in enumerate(hc.gitlab_eye_xpaths):
        print(f"{i},xpath={xpath}")
        if not successfull:

            website_controller, successfull = try_to_click_by_xpath(
                website_controller,
                xpath,
                "xpath-eye try loop",
                False,
            )
        time.sleep(1)
    return website_controller, successfull


def gitlab_click_eye_button_through_id_V2(hc, website_controller):
    """

    :param hc:
    :param website_controller:

    """
    successfull = False

    for i, gitlab_eye_id in enumerate(hc.gitlab_eye_ids):
        print(f"{i},gitlab_eye_id={gitlab_eye_id}")
        if not successfull:

            website_controller, successfull = try_to_click_by_id(
                website_controller,
                gitlab_eye_id,
                "gitlab_eye_id try",
                False,
            )
        time.sleep(1)
    return website_controller, successfull


def try_to_click_by_id(website_controller, some_id, error_msg, raise_error):
    """Tries to click an object in website using the class id.

    :param website_controller:
    :param id:
    :param error_msg:
    :param raise_error:
    """
    try:
        # Click the button to display registration code through element id
        website_controller.driver.find_element("id", some_id).click()

        return website_controller, True
    # pylint: disable=W1309
    # pylint: disable=W0702
    except:
        # pylint: disable=W0702
        if raise_error:
            # pylint: disable=W0707
            raise Exception(error_msg)
        return website_controller, False


def try_to_click_by_xpath(website_controller, xpath, error_msg, raise_error):
    """Tries to click an object in website using the xpath of that object.

    :param website_controller:
    :param xpath:
    :param error_msg:
    :param raise_error:
    """
    try:
        # Click the button to display registration code through element id
        website_controller = click_element_by_xpath(
            website_controller,
            xpath,
        )
        return website_controller, True
    # pylint: disable=W0702
    except:
        if raise_error:
            # pylint: disable=W0707
            raise Exception(error_msg)
        return website_controller, False


def read_gitlab_runner_token_from_page(website_controller):
    """

    :param website_controller:

    """
    # get the page source:
    source = website_controller.driver.page_source

    token_identification_string_0 = '<code id="registration_token">'  # nosec
    token_identification_string_1 = 'data-registration-token="'  # nosec
    token_identification_string_2 = 'data-clipboard-text="'  # nosec

    token_identification_string_3 = (
        '<code data-testid="registration-token"><span>'  # nosec
    )

    # TODO: New update requires clicking dropdown box, xpath=

    # verify the source contains the runner token
    if not source_contains(website_controller, token_identification_string_0):
        if not source_contains(
            website_controller, token_identification_string_1
        ):
            if not source_contains(
                website_controller, token_identification_string_2
            ):
                if not source_contains(
                    website_controller, token_identification_string_3
                ):
                    raise Exception(
                        "Expected runner registration token to be CONTAINED"
                        f" in the source code, but it is not: {source}."
                    )
                return get_value_from_html_source(
                    source, token_identification_string_3, "</code>"
                )
            return get_value_from_html_source(
                source, token_identification_string_2, '"'
            )
        return get_value_from_html_source(
            source, token_identification_string_1, '"'
        )
    # Extract the runner registration token from the source code
    return get_value_from_html_source(
        source, token_identification_string_0, "</code>"
    )
