from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.repositories.procedimientos import llamar


class BusquedaRepository(ABC):
    @abstractmethod
    def porapellido(self, apellido: str) -> list[tuple[Any, ...]]:
        """Filas completas de estudiante cuyo apellido empieza con el texto. Viene del procedimiento p06."""

    @abstractmethod
    def edad(self, codest: int) -> int | None:
        """Edad en años. Viene de la función f3."""


class SQLAlchemyBusquedaRepository(BusquedaRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def porapellido(self, apellido: str) -> list[tuple[Any, ...]]:
        return llamar(self.session, "call p06(:apellido)", {"apellido": apellido})

    def edad(self, codest: int) -> int | None:
        return self.session.scalar(select(func.f3(codest)))
