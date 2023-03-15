"""Asks user input through CLI."""
from getpass import getpass

from typeguard import typechecked


@typechecked
def ask_two_factor_code() -> str:
    """Asks for the 2fac.

    TODO: make safe, hide code instead of displaying on terminal.
    """
    two_fac_code = get_input(
        text="Please enter the two factor authentication you just received:"
    )
    return two_fac_code


@typechecked
def get_input(*, text: str) -> str:
    """Asks user input through CLI.

    :param text:
    """
    return getpass(text)
