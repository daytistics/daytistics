import aioinject

from .services import UserService, AuthenticationService
from .repositories import UserRepository

injectables = [
    aioinject.Singleton(UserService),
    aioinject.Singleton(AuthenticationService),
    aioinject.Singleton(UserRepository),
]
