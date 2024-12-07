import strawberry
from sqlmodel import Session, select
import bcrypt

from .schemas import UserRegistrationInput, UserLoginInput, UserType
from .models import User
from .exceptions import UserAlreadyExistsError


@strawberry.type
class Mutation:
    @strawberry.mutation
    def register_user(
        self, user: UserRegistrationInput, info: strawberry.Info
    ) -> UserType:
        session: Session = info.context["session"]

        if session.exec(select(User).where(User.email == user.email)).first():
            raise UserAlreadyExistsError()

        hashed_password = str(
            bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
        )

        new_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return UserType(**new_user.model_dump())

    @strawberry.mutation
    def login_user(self, user: UserLoginInput, info: strawberry.Info) -> UserType:
        session: Session = info.context["session"]
        user_from_db = session.get(User, {"email": user.email})
