from collections.abc import AsyncIterator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from asgi_csrf import asgi_csrf
from contextlib import asynccontextmanager

from daytistics.libs.graphql import create_graphql_router
from daytistics.settings import CorsSettings, AppSettings, get_settings
from daytistics.libs.container import create_container


def init_cors(app: FastAPI):
    cors_config = get_settings(CorsSettings)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_config.ALLOW_ORIGINS,
        allow_credentials=cors_config.ALLOW_CREDENTIALS,
        allow_methods=cors_config.ALLOW_METHODS,
        allow_headers=cors_config.ALLOW_HEADERS,
    )

    return app


def init_graphql(app: FastAPI):
    graphql_router = create_graphql_router()
    app.include_router(graphql_router, prefix="/graphql")

    return app


def csrf_app(app: FastAPI):
    app_settings = get_settings(AppSettings)

    return asgi_csrf(
        app,
        signing_secret=app_settings.SECRET_KEY,
        always_set_cookie=True,
    )


def create_app():
    container = create_container()
    app = FastAPI()

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        async with container:
            yield

    app = FastAPI(lifespan=lifespan)

    init_graphql(app)
    init_cors(app)

    return csrf_app(app)


app = create_app()
