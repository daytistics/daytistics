from fastapi import FastAPI
import dotenv

from .integrations.graphql import create_graphql_router
from .integrations.database import Database
from .integrations.injections import container, register_dependencies


def create_app() -> FastAPI:
    dotenv.load_dotenv()
    app = FastAPI()

    register_dependencies()

    with container.sync_context() as ctx:
        db = ctx.resolve(Database)
        db.connect()

    graphql_router = create_graphql_router()
    app.include_router(graphql_router, prefix="/graphql")

    return app


app = create_app()
