import unittest
import os
from ..src.Main import Main
import testbook


class Test_main(unittest.TestCase):

    # Initialize test object
    def __init__(self, *args, **kwargs):
        super(Test_main, self).__init__(*args, **kwargs)
        self.script_dir = self.get_script_dir()

        self.main = Main(1, False)
        print(f"self.main.addTwo(3)={self.main.addTwo(3)}")

    # returns the directory of this script regardles of from which level the code is executed
    def get_script_dir(self):
        return os.path.dirname(__file__)

    # tests unit test on addTwo function of main class
    def test_parse_creds(self):

        expected_result = "someusername"
        lines = []
        lines.append("gitlab_server_account=someusername")
        lines.append(
            "# notice the password is currently hardcoded in src/install_and_boot_gitlab_server.sh"
        )
        lines.append("gitlab_server_password=yoursecretone")
        lines.append("GITLAB_ROOT_EMAIL=root@protonmail.com")
        result_username, result_pwd = self.main.parse_creds(lines)
        self.assertEqual(expected_result, result_username)


if __name__ == "__main__":
    unittest.main()
