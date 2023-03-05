"""Gets the GitLab runner token from local GitLab server and stores it in local
personal credentials.

TODO: Change to get it from within docker instead
of using browser controller.
"""
import time

from browsercontroller.helper import click_element_by_xpath, source_contains
from typeguard import typechecked

from src.gitbrowserinteract.helper import get_value_from_html_source


@typechecked
def get_gitlab_runner_registration_token_from_page(*, hc, driver):
    """

    :param hc:
    :param driver:

    """
    goto_runner_token_site(driver=driver)
    visualise_runner_token(hc=hc, driver=driver)
    gitlab_runner_token = read_gitlab_runner_token_from_page(driver=driver)
    print(f"gitlab_runner_token={gitlab_runner_token}")
    return gitlab_runner_token


@typechecked
def goto_runner_token_site(*, driver):
    """

    :param driver:

    """
    # visit website with runner token
    driver.get("http://127.0.0.1/admin/runners")

    # wait five seconds for page to load
    time.sleep(5)


@typechecked
def visualise_runner_token(*, hc, driver):
    """

    :param hc:
    :param driver:

    """
    # if click_display_token_through_css_V0(driver=driver):
    #    return driver
    # if unhide_registration_token_through_xpath_V1(driver=driver):
    #    # TODO: verify whether after this function, another button must be clicked.
    #    return driver
    click_element_by_xpath(driver=driver, xpath=hc.gitlab_dropdown_arrow_xpath)
    click_element_by_xpath(driver=driver, xpath=hc.gitlab_eye_xpaths[-1])

    # driver = gitlab_visualise_runner_token_through_dropdown_boxV2(hc=hc, driver=driver)
    return driver


@typechecked
def click_display_token_through_css_V0(*, driver):
    """

    :param driver:

    """
    # click the button to display registration code through css selector (if it exists)
    try:
        driver.find_element(
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


@typechecked
def unhide_registration_token_through_xpath_V1(*, driver):
    """Tries to show the GitLab runner registration token.

    :param driver:
    """
    try:
        # Click unhide registration-token through xpath
        click_element_by_xpath(
            driver,
            '//*[@id="eye"]',
        )

        # Click the button to display registration code through element id
        driver.find_element("id", "eye").click()
        return True
    # pylint: disable=W0702
    except:
        print(
            '\n \n Note: did not find button to click "unhide"runner '
            + "registration token with second method. Will try third method now"
        )
        return False


@typechecked
def gitlab_visualise_runner_token_through_dropdown_boxV2(*, hc, driver):
    """

    :param hc:
    :param driver:

    """
    driver = click_dropdown_box_V2(driver=driver)
    time.sleep(2)
    driver, successfull = gitlab_click_eye_button_through_xpath_V2(
        hc=hc, driver=driver
    )
    if not successfull:
        (
            driver,
            successfull,
        ) = gitlab_click_eye_button_through_id_V2(hc=hc, driver=driver)
    if not successfull:
        input(
            "Please manually click the eye button to show the GitLab"
            + "runner registration token."
        )
        # raise ValueError("Did not find the GitLab Runner Registration token.")

    return driver


@typechecked
def click_dropdown_box_V2(*, driver):
    """

    :param driver:

    """

    # Click dropdown button
    driver, _ = try_to_click_by_xpath(
        driver=driver,
        xpath='//*[@id="__BVID__31"]',
        error_msg=(
            "\n \n Note: did not find button to dropwdown the runner registration"
            + " token box with third method. Will try fourth method now."
        ),
        raise_error=True,
    )
    return driver


@typechecked
def gitlab_click_eye_button_through_xpath_V2(*, hc, driver):
    """

    :param driver:

    """

    successfull = False
    for i, xpath in enumerate(hc.gitlab_eye_xpaths):
        print(f"{i},xpath={xpath}")
        if not successfull:
            driver, successfull = try_to_click_by_xpath(
                driver=driver,
                xpath=xpath,
                error_msg="xpath-eye try loop",
                raise_error=False,
            )
        time.sleep(1)
    return driver, successfull


@typechecked
def gitlab_click_eye_button_through_id_V2(*, hc, driver):
    """

    :param hc:
    :param driver:

    """
    successfull = False

    for i, gitlab_eye_id in enumerate(hc.gitlab_eye_ids):
        print(f"{i},gitlab_eye_id={gitlab_eye_id}")
        if not successfull:
            driver, successfull = try_to_click_by_id(
                driver=driver,
                some_id=gitlab_eye_id,
                error_msg="gitlab_eye_id try",
                raise_error=False,
            )
        time.sleep(1)
    return driver, successfull


@typechecked
def try_to_click_by_id(*, driver, some_id, error_msg, raise_error):
    """Tries to click an object in website using the class id.

    :param driver:
    :param id:
    :param error_msg:
    :param raise_error:
    """
    try:
        # Click the button to display registration code through element id
        driver.find_element("id", some_id).click()

        return driver, True
    # pylint: disable=W1309
    # pylint: disable=W0702
    except:
        # pylint: disable=W0702
        if raise_error:
            # pylint: disable=W0707
            raise SystemError(error_msg)
        return driver, False


@typechecked
def try_to_click_by_xpath(*, driver, xpath, error_msg, raise_error):
    """Tries to click an object in website using the xpath of that object.

    :param driver:
    :param xpath:
    :param error_msg:
    :param raise_error:
    """
    try:
        # Click the button to display registration code through element id
        driver = click_element_by_xpath(
            driver,
            xpath,
        )
        return driver, True
    # pylint: disable=W0702
    except:
        if raise_error:
            # pylint: disable=W0707
            raise SystemError(error_msg)
        return driver, False


@typechecked
def read_gitlab_runner_token_from_page(*, driver):
    """

    :param driver:

    """
    # get the page source:
    source = driver.page_source

    token_identification_string_0 = '<code id="registration_token">'  # nosec
    token_identification_string_1 = 'data-registration-token="'  # nosec
    token_identification_string_2 = 'data-clipboard-text="'  # nosec

    token_identification_string_3 = (
        '<code data-testid="registration-token"><span>'  # nosec
    )

    # TODO: New update requires clicking dropdown box, xpath=

    # verify the source contains the runner token
    if not source_contains(driver, token_identification_string_0):
        if not source_contains(driver, token_identification_string_1):
            if not source_contains(driver, token_identification_string_2):
                if not source_contains(driver, token_identification_string_3):
                    raise ValueError(
                        "Expected runner registration token to be CONTAINED"
                        f" in the source code, but it is not: {source}."
                    )
                return get_value_from_html_source(
                    source=source,
                    substring=token_identification_string_3,
                    closing_substring="</code>",
                )
            return get_value_from_html_source(
                source=source,
                substring=token_identification_string_2,
                closing_substring='"',
            )
        return get_value_from_html_source(
            source=source,
            substring=token_identification_string_1,
            closing_substring='"',
        )
    # Extract the runner registration token from the source code
    return get_value_from_html_source(
        source=source,
        substring=token_identification_string_0,
        closing_substring="</code>",
    )
