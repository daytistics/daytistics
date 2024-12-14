import aioinject
from aioinject import Container

container = Container()


def register_dependencies():
    from .database import Database
    from ..config import SecurityConfig
    from daytistics.apps.auth.injectables import injectables as auth_injectables

    container.register(
        aioinject.Singleton(Database),
        aioinject.Singleton(SecurityConfig),
        *auth_injectables,
    )
