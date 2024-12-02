import strawberry


@strawberry.input
class UserRegistrationInput:
    username: str
    email: str
    password: str


@strawberry.input
class UserLoginInput:
    email: str
    password: str
