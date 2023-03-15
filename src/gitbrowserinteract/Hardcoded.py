"""Contains the hardcoded data for this project."""

from typing import List

from typeguard import typechecked


# pylint: disable=C0301
# pylint: disable=R0902
# pylint: disable=R0903
class Hardcoded:
    """Runs jupyter notebooks, converts them to pdf, exports the notebook pdfs
    to latex and compiles the latex report of the incoming project nr."""

    # pylint: disable=R0915
    @typechecked
    def __init__(self) -> None:
        """Constructs an object that contains all the hardcoded values that are
        used in this script.

        TODO: adjust browser drivers based on the detected device type.
        """

        self.firefox_driver_folder: str = "firefox_driver"
        self.firefox_driver_tarname: str = "firefox_driver.tar.gz"
        self.firefox_driver_filename: str = "geckodriver"
        # self.firefox_driver_link:str = "https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz"
        self.firefox_driver_link: str = "https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz"

        self.chromium_driver_folder: str = "chrome_driver"
        self.chromium_driver_tarname: str = "chrome_driver.zip"
        self.chromium_driver_link: str = "https://chromedriver.storage.googleapis.com/90.0.4430.24/chromedriver_linux64.zip"
        self.chromium_driver_unmodified_filename: str = "chromedriver"
        self.chromium_driver_filename: str = "chromedriver90"

        # specify source repository
        self.source_username: str = "HiveMinds-EU"

        self.source_reponame: str = "Taskwarrior-installation-original"

        self.source_repo_url: str = f"https://github.com/{self.source_username}/{self.source_reponame}/issues"

        self.pickle_driver_filename: str = "driver.p"

        self.use_cred_file: str = True
        self.personal_creds_path: str = "../personal_creds.txt"
        self.cred_path: str = self.personal_creds_path
        # TODO: verify if called from path using bash, if the
        # python path is still the same root.
        self.github_pac_bash_precursor: str = (
            "GITHUB_PERSONAL_ACCESS_TOKEN_GLOBAL="
        )
        # website properties
        self.gitlab_login_url: str = "http://127.0.0.1"
        self.gitlab_user_element_id: str = "user_login"
        self.gitlab_pw_element_id: str = "user_password"
        # self.gitlab_signin_button_xpath:str = '//*[@id="new_user"]/div[5]/input'
        self.gitlab_signin_button_xpath: str = "/html/body/div[1]/div[2]/div/div[3]/div/div/div/div/div/form/div[5]/button"
        url: str = "/assets/icons-7b0fcccb8dc2c0d0883e05f97e4678621a71b996ab2d30bb42fafc906c1ee13f.svg#eye"
        self.gitlab_eye_xpaths: List[str] = [
            # "/html/body/div[3]/div/div[3]/main/div[2]/div[2]/div[2]/ul/div/div/li[3]/form/fieldset/div/div/button[1]",
            # "/html/body/div[3]/div/div[3]/main/div[2]/div[2]/div[2]/ul/div/div/li[3]/form/fieldset/div/div/button[1]/svg",
            # "/html/body/div[3]/div/div[3]/main/div[2]/div[2]/div[2]/ul/div/div/li[3]/form/fieldset/div/div/button[1]/svg/use",
            # '//*[@id="eye"]',
            # "/html/body/div[3]/div/div[3]/main/div[2]/div[2]/div[2]/ul/div/div/li[3]/form/div/div/div/div/button[1]",
            # "/html/body/div[3]/div/div[3]/main/div[2]/div[2]/div[2]/ul/div/div/li[3]/form/div/div/div/div/button[1]/svg",
            # "/html/body/div[3]/div/div[3]/main/div[2]/div[2]/div[2]/ul/div/div/li[3]/form/div/div/div/div/button[1]/svg/use",
            # '//*[@id="eye"]',
            # "/symbol/path",
            '//a[@href="' + url + '"]',
            "/html/body/div[3]/div/div[3]/main/div[2]/div[1]/div[2]/ul/div/div/li[3]/form/div/div/div/div/button[1]",
        ]
        # self.gitlab_dropdown_arrow_xpath="/html/body/div[3]/div/div[3]/main/div[2]/div[1]/div[2]/button/svg"
        self.gitlab_dropdown_arrow_xpath: str = '//*[@id="__BVID__21"]'

        self.gitlab_eye_ids: List[str] = [
            "eye",
            "eye-icon",
        ]

        self.github_login_url: str = "https://www.github.com/login"
        self.github_user_element_id: str = "login_field"
        self.github_pw_element_id: str = "password"
        # self.github_signin_button_xpath:str = '//*[@id="login"]/div[4]/form/div/input[12]'
        self.github_signin_button_xpath: str = (
            # "/html/body/div[3]/main/div/div[4]/form/div/input[11]"
            "/html/body/div[1]/div[3]/main/div/div[4]/form/div/input[11]"
        )

        # xpath two_factor code input field:
        self.github_2fa_input_filed_xpath: str = '//*[@id="sms_totp"]'

        self.github_deploy_key_title_element_id: str = "public_key_title"
        self.github_deploy_key_key_element_id: str = "public_key_key"
        self.github_deploy_key_allow_write_access_button_xpath: str = (
            '//*[@id="public_key_read_only"]'
        )
        self.add_github_deploy_key_button_xpath: str = (
            # "/html/body/div[6]/div/main/div[2]/div/div/div[2]/div/div/form/button"
            # "/html/body/div[5]/div/main/turbo-frame/div/div/div/div[2]/div/div/form/button"
            "/html/body/div[1]/div[5]/div/main/turbo-frame/div/div/div/div[2]/div/div/form/div/button/span/span"
        )

        # print(f"github_login_url={self.github_login_url}")
        # This is in the page source if the user is logged in.
        # It is assumed this string does not occur in the page source
        # if the user is not logged in.
        self.github_logged_in_or_not_string: str = "View profile and more"
        self.gitlab_logged_in_or_not_string: str = (
            "<title>Projects · Dashboard · GitLab</title>"
        )

        self.github_pat_tokens_url: str = "https://github.com/settings/tokens/"
        self.github_pat_description: str = (
            "Set GitHub commit build status values."
        )
        self.github_pat_description_elem_classname: str = "token-description"
        self.github_pat_table_xpath: str = (
            # "/html/body/div[5]/main/div[2]/div/div[2]/div/div/div[1]/div[2]"
            # "/html/body/div[1]/div[5]/main/div[2]/div/div[2]/div/div/div[1]/div[2]/div/div"
            # "/html/body/div[1]/div[5]/main/div[2]/div/div[2]/div/div/div[1]/div[2]"
            "/html/body/div[1]/div[6]/main/div[2]/div/div[2]/div/div/div[1]/div[2]"
        )

        self.github_ci_build_status_repo_name: str = "gitlab-ci-build-statuses"
        self.github_username_placeholder: str = "github_username_placeholder"
        self.github_ssh_key_tokens_url: str = f"https://github.com/{self.github_username_placeholder}/{self.github_ci_build_status_repo_name}/settings/keys/"
        self.github_ssh_key_description: str = (
            "github_build_status_deployment_key"
        )
        self.github_ssh_key_table_xpath: str = "/html/body/div[5]/div/main/turbo-frame/div/div/div/div[2]/div/div/ul"

        # Xpath of input field: Note, what's the token for?
        self.github_pac_input_field_xpath: str = (
            '//*[@id="oauth_access_description"]'
        )

        # Xpath of "repo:status" checkbox
        # /html/body/div[6]/main/div[2]/div[2]/form/div/dl[2]/dd/div/ul/li[1]/ul/li[1]/label/div/input
        self.github_pac_repo_status_checkbox_xpathV0: str = "/html/body/div[6]/main/div[2]/div[2]/form/div/dl[2]/dd/div/ul/li[1]/ul/li[1]/label/div/input"
        self.github_pac_repo_status_checkbox_xpathV1: str = "/html/body/div[6]/main/div[2]/div/div[2]/div/div/form/div/dl[2]/dd/div/ul/li[1]/ul/li[1]/label/div/input"
        self.github_pac_repo_status_checkbox_xpathV2: str = "/html/body/div[5]/main/div[2]/div/div[2]/div/div/form/div/dl[2]/dd/div/ul/li[1]/ul/li[1]/label/div/input"
        # self.github_pac_repo_status_checkbox_xpathV3:str = "/html/body/div[1]/div[5]/main/div[2]/div/div[2]/div/div/form/div/dl[2]/dd/div/ul/li[1]/ul/li[1]/label/div/input"
        self.github_pac_repo_status_checkbox_xpathV3: str = "/html/body/div[1]/div[6]/main/div[2]/div/div[2]/div/div/form/div/dl[2]/dd/div/ul/li[1]/ul/li[1]/label/div/input"

        # Xpath of "Generate token" button
        # /html/body/div[6]/main/div[2]/div[2]/form/p/button
        self.github_pac_generate_token_button_xpathV0: str = (
            "/html/body/div[6]/main/div[2]/div[2]/form/p/button"  # nosec
        )
        self.github_pac_generate_token_button_xpathV1: str = "/html/body/div[6]/main/div[2]/div/div[2]/div/div/form/p/button"  # nosec
        # self.github_pac_generate_token_button_xpathV2:str = "/html/body/div[5]/main/div[2]/div/div[2]/div/div/form/p/button"  # nosec
        # self.github_pac_generate_token_button_xpathV2:str = "/html/body/div[1]/div[5]/main/div[2]/div/div[2]/div/div/form/p/button"  # nosec
        self.github_pac_generate_token_button_xpathV2: str = "/html/body/div[1]/div[6]/main/div[2]/div/div[2]/div/div/form/p/button"  # nosec
