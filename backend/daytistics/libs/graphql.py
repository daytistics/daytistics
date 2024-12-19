import strawberry
from strawberry.fastapi import GraphQLRouter
from aioinject.ext.strawberry import AioInjectExtension

from daytistics.domains.users.mutations import Mutation as UserMutation
from daytistics.libs.container import create_container


@strawberry.type
class _Query:
    @strawberry.field
    def health() -> None:
        return None


@strawberry.type
class _Mutation(UserMutation):
    pass


schema = strawberry.Schema(
    query=_Query,
    mutation=_Mutation,
    extensions=[AioInjectExtension(create_container())],
)


def create_graphql_router():
    router = GraphQLRouter(schema)
    return router
