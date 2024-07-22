class InvalidEmailError(Exception):
    """
    Exception raised when an invalid email is provided for a user.
    """

    pass


class EmailInUseError(Exception):
    """
    Exception raised when an email is already in use.
    """

    pass
