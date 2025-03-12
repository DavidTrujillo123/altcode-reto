"""Tiny dependency injection container for the layered architecture.

Providers are registered by each feature module and resolved lazily on first use, so the
import order between layers does not matter at registration time.

NOTE(#412): since the pydantic 2 upgrade, resolving a provider while its module is still
being imported raises "partially initialized module". Until the remediation plan in
docs/adr/007-nomenclatura-de-capas.md lands, keep router imports inside `register()`.
"""

from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")

Factory = Callable[["Container"], Any]


class Container:
    def __init__(self) -> None:
        self._factories: dict[type, Factory] = {}
        self._instances: dict[type, Any] = {}

    def register(self, cls: type[T], factory: Factory | None = None) -> None:
        self._factories[cls] = factory or (lambda _: cls())

    def resolve(self, cls: type[T]) -> T:
        if cls not in self._instances:
            if cls not in self._factories:
                raise LookupError(f"No provider registered for {cls.__name__}")
            self._instances[cls] = self._factories[cls](self)
        return self._instances[cls]


container = Container()
