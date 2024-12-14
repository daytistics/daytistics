import strawberry
from aioinject import Injected
from aioinject.ext.strawberry import inject

from .schemas import UserRegistrationInput, UserType
from .services.user import UserService


@strawberry.type
class Mutation:
    @strawberry.mutation
    @inject
    async def register_user(
        self, user: UserRegistrationInput, user_service: Injected[UserService]
    ) -> UserType:
        created_user = await user_service.register_user(user)

        return UserType(
            **created_user.model_dump(
                include={field for field in UserType.__annotations__.keys()}
            )
        )
