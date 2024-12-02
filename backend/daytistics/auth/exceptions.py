class UserNotFoundError(Exception):
    def __init__(self, message="USER_NOT_FOUND"):
        super().__init__(message)


class UserAlreadyExistsError(Exception):
    def __init__(self, message="USER_ALREADY_EXISTS"):
        super().__init__(message)
