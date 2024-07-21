class UserExistsError(Exception):
    """
    Exception raised when an attempt is made to create a user that already exists.
    """

    pass


class UserNotFoundError(Exception):
    """
    Exception raised when an attempt is made to access a user that does not exist.
    """

    pass


class BadPasswordError(Exception):
    """
    Exception raised when a password does not meet the required security standards.
    """

    pass


class InvalidNameError(Exception):
    """
    Exception raised when an invalid name is provided for a user.
    """

    pass


class InvalidRoleError(Exception):
    """
    Exception raised when an invalid role is assigned to a user.
    """

    pass


class IncorrectPasswordError(Exception):
    """
    Exception raised when an incorrect password is provided for a user.
    """

    pass


class SamePasswordError(Exception):
    """
    Exception raised when a new password is the same as the old password during a password change operation.
    """

    pass

