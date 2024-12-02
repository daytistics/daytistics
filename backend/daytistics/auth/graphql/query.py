import strawberry
from sqlmodel import Session

from ..models import User
from ..exceptions import UserNotFoundError
from .types import UserType


@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: int, info: strawberry.Info) -> UserType:
        session: Session = info.context["session"]
        user = session.get(User, id)
        if not user:
            raise UserNotFoundError()

        return UserType(
            **user.model_dump(
                include={field for field in UserType.__annotations__.keys()}
            )
        )
