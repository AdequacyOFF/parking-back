from dataclasses import dataclass, field
from typing import Any
from uuid import UUID


@dataclass
class Service:
    id: UUID
    title: str

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return other.id == self.id

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass
class Oil:
    id: UUID
    title: str
    price: int

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return other.id == self.id

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass
class Station:
    id: UUID
    name: str
    address: str
    latitude: float
    longitude: float
    services: set[Service] = field(default_factory=set)
    oils: set[Oil] = field(default_factory=set)
