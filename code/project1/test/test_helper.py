"""Tests whether the parse_creds function returns the correct credentials based
on a given input."""
import unittest
from code.project1.src.helper import parse_creds


class Test_parse_creds(unittest.TestCase):
    """Object used to test a parse_creds function."""

    # Initialize test object
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_parse_creds(self):
        """Tests whether the parse_creds function returns the correct
        credentials based on a given input."""

        expected_result = "someusername"
        lines = []
        lines.append("gitlab_server_account=someusername")
        lines.append(
            "# notice the password is currently hardcoded in src/install_and_boot_gitlab_server.sh"
        )
        lines.append("gitlab_server_password=yoursecretone")
        lines.append("GITLAB_ROOT_EMAIL=root@protonmail.com")
        result_username, _ = parse_creds(lines)
        self.assertEqual(expected_result, result_username)


if __name__ == "__main__":
    unittest.main()
