from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import dotenv
from asgi_csrf import asgi_csrf

from .integrations.graphql import create_graphql_router
from .integrations.database import Database
from .integrations.injections import container, register_dependencies
from .config import SecurityConfig


def create_app():
    dotenv.load_dotenv()
    app = FastAPI()

    register_dependencies()

    with container.sync_context() as ctx:
        db = ctx.resolve(Database)
        db.connect()

        graphql_router = create_graphql_router()

        # Routes
        app.include_router(graphql_router, prefix="/graphql")

        security_config = ctx.resolve(SecurityConfig)

        # Middlewares
        app.add_middleware(
            CORSMiddleware,
            allow_origins=security_config.CORS_ALLOW_ORIGINS,
            allow_credentials=security_config.CORS_ALLOW_CREDENTIALS,
            allow_methods=security_config.CORS_ALLOW_METHODS,
            allow_headers=security_config.CORS_ALLOW_HEADERS,
        )

        return asgi_csrf(
            app, signing_secret=security_config.SECRET_KEY, always_set_cookie=True
        )


app = create_app()
