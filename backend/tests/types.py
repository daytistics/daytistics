from typing import Protocol, TypeVar

T = TypeVar("T")


class Resolver(Protocol):
    async def __call__(self, type_: type[T]) -> T: ...
