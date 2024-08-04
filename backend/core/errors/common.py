class InvalidCharactersError(Exception):
    """
    Exception raised when invalid characters are encountered.
    """

    pass


class MissingFieldError(Exception):
    """
    Exception raised when a required field is missing.
    """

    pass


class ExplicitContentError(Exception):
    """
    Exception raised when explicit content is encountered.
    """

    pass

class InvalidDurationTypeError(Exception):
    """
    Exception raised when an invalid duration type is encountered.
    """

    pass
