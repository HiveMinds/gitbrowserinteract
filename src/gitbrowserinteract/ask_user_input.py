"""Asks user input through CLI."""
from typeguard import typechecked


@typechecked
def ask_two_factor_code():
    """Asks for the 2fac.

    TODO: make save, hide code instead of displaying on terminal.
    """
    two_fac_code = get_input(
        text="Please enter the two factor authentication you just received:"
    )
    return two_fac_code


@typechecked
def get_input(*, text):
    """

    :param text:

    """
    return input(text=text)
