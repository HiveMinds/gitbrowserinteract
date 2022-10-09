"""Asks user input through CLI."""


def ask_two_factor_code():
    """USED."""
    two_fac_code = get_input(
        "Please enter the two factor authentication you just received:"
    )
    return two_fac_code


def get_input(text):
    """

    :param text:

    """
    return input(text)
