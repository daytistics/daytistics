import strawberry
from strawberry.fastapi import GraphQLRouter
from aioinject.ext.strawberry import AioInjectExtension

from .injections import container
from daytistics.apps.auth.queries import Query as UserQuery
from daytistics.apps.auth.mutations import Mutation as UserMutation


@strawberry.type
class _Query(UserQuery):
    pass


@strawberry.type
class _Mutation(UserMutation):
    pass


schema = strawberry.Schema(
    query=_Query, mutation=_Mutation, extensions=[AioInjectExtension(container)]
)


def create_graphql_router():
    router = GraphQLRouter(schema)
    return router
