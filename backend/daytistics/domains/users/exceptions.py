class UserNotFoundError(Exception):
    def __init__(self, message="USER_NOT_FOUND"):
        super().__init__(message)


class UserAlreadyExistsError(Exception):
    def __init__(self, message="USER_ALREADY_EXISTS"):
        super().__init__(message)


class VerificationFailedError(Exception):
    def __init__(self, message="VERIFICATION_FAILED"):
        super().__init__(message)


class UserAlreadyVerifiedError(Exception):
    def __init__(self, message="USER_ALREADY_VERIFIED"):
        super().__init__(message)


class WrongPasswordError(Exception):
    def __init__(self, message="WRONG_PASSWORD"):
        super().__init__(message)


class InvalidEmailError(Exception):
    def __init__(self, message="INVALID_EMAIL"):
        super().__init__(message)


class InvalidPasswordError(Exception):
    def __init__(self, message="INVALID_PASSWORD"):
        super().__init__(message)


class InvalidUsernameError(Exception):
    def __init__(self, message="INVALID_USERNAME"):
        super().__init__(message)
