class Hardcoded:
    """Runs jupyter notebooks, converts them to pdf,
    exports the notebook pdfs to latex and compiles the
    latex report of the incoming project nr


    """

    def __init__(self):
        """
        Constructs an object that contains all the hardcoded values that are used in this script.
        TODO: adjust browser drivers based on the detected device type.
        """
        self.script_dir = 5
        self.firefox_driver_folder = "firefox_driver"
        self.firefox_driver_tarname = "firefox_driver.tar.gz"
        self.firefox_driver_filename = "geckodriver"
        # self.firefox_driver_link = "https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz"
        self.firefox_driver_link = "https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz"

        self.chromium_driver_folder = "chrome_driver"
        self.chromium_driver_tarname = "chrome_driver.zip"
        self.chromium_driver_link = "https://chromedriver.storage.googleapis.com/90.0.4430.24/chromedriver_linux64.zip"
        self.chromium_driver_unmodified_filename = "chromedriver"
        self.chromium_driver_filename = "chromedriver90"

        # specify source repository
        self.source_username = "HiveMinds-EU"
        self.target_username = "HiveMinds-EU"
        self.source_reponame = "Taskwarrior-installation-original"
        self.target_reponame = "Taskwarrior-installation"
        self.source_repo_url = (
            f"https://github.com/{self.source_username}/{self.source_reponame}/issues"
        )

        self.pickle_website_controller_filename = "website_controller.p"

        self.use_cred_file = True
        self.cred_path = "../src/creds.txt"
        # website properties
        self.gitlab_login_url = "http://127.0.0.1"
        self.gitlab_user_element_id = "user_login"
        self.gitlab_pw_element_id = "user_password"
        self.gitlab_signin_button_xpath = '//*[@id="new_user"]/div[5]/input'

        self.github_login_url = "https://www.github.com/login"
        self.github_user_element_id = "login_field"
        self.github_pw_element_id = "password"
        self.github_signin_button_xpath = '//*[@id="login"]/div[4]/form/div/input[12]'

        self.github_deploy_key_title_element_id = "public_key_title"
        self.github_deploy_key_key_element_id = "public_key_key"
        self.deployment_key_title = "github_build_status_deployment_key"
        self.github_deploy_key_allow_write_access_button_xpath = (
            '//*[@id="public_key_read_only"]'
        )
        self.add_github_deploy_key_button_xpath = (
            "/html/body/div[6]/div/main/div[2]/div/div/div[2]/div/div/form/button"
        )
        # print(f"github_login_url={self.github_login_url}")
