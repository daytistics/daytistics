class InvalidVerificationCodeError(Exception):
    """
    Exception raised when an invalid verification code is encountered.
    """

    pass


class VerificationFailureLimitExceededError(Exception):
    """
    Exception raised when the verification failure limit has been exceeded.
    """

    pass


class VerificationTemporarilyRejectedError(Exception):
    """
    Exception raised when the verification process of a user is temporarily rejected.
    This error occurs when the user has exceeded the maximum number of verification attempts.
    """

    pass
