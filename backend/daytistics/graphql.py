import strawberry
from fastapi import FastAPI, Depends
from strawberry.fastapi import GraphQLRouter

from daytistics.modules.auth.queries import Query as UserQuery
from daytistics.modules.auth.mutations import Mutation as UserMutation
from daytistics.dependencies import get_session


async def _get_graphql_context(session=Depends(get_session)):
    """
    Get the GraphQL context. Used for dependency injection.
    """
    return {"session": session}


@strawberry.type
class Query(UserQuery):
    pass


@strawberry.type
class Mutation(UserMutation):
    pass


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)

graphql_app = GraphQLRouter(schema, context_getter=_get_graphql_context)


def setup_graphql(app: FastAPI) -> None:
    app.include_router(graphql_app, prefix="/graphql")
