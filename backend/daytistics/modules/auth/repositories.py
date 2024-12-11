from sqlmodel import Session, select

from .models import User
from .exceptions import UserAlreadyExistsError, UserNotFoundError


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user: User) -> User:
        if self.session.exec(select(User).where(User.email == user.email)).first():
            raise UserAlreadyExistsError

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update_user_verification(self, is_verified: bool, user_id: int) -> User:
        user = self.session.get(User, user_id)

        if not user:
            raise UserNotFoundError

        user.is_verified = is_verified
        self.session.commit()
        self.session.refresh(user)
        return user
