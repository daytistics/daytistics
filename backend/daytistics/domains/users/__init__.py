import aioinject

from daytistics.domains.users.services import UserService, AuthenticationService
from daytistics.domains.users.repositories import UserRepository

providers = [
    aioinject.Singleton(UserService),
    aioinject.Singleton(UserRepository),
    aioinject.Singleton(AuthenticationService),
]
