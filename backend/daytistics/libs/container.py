import aioinject
import functools
import itertools
from collections.abc import Iterable
from typing import Any

from aioinject import Object, Provider

from daytistics.settings import get_settings, settings_classes
from daytistics.domains import users
from daytistics import shared
from daytistics.libs import database

modules: Iterable[Iterable[Provider[Any]]] = [
    users.providers,
    shared.providers,
    database.providers,
]


@functools.cache
def create_container() -> aioinject.Container:
    container = aioinject.Container()

    for provider in itertools.chain.from_iterable(modules):
        container.register(provider)

    for settings_cls in settings_classes:
        container.register(Object(get_settings(settings_cls)))

    return container
