from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


class ReportePostulacionRepository(ABC):
    """Reportes de postulaciones y seguimiento que ya resuelven las vistas de la base de datos."""

    @abstractmethod
    def porestudiante(self) -> list[tuple[Any, ...]]:
        """(estudiante, postulaciones, año). Viene de la vista v01."""

    @abstractmethod
    def promediosbeca(self) -> list[tuple[Any, ...]]:
        """(beca, promedio, seguimientos). Viene de la vista v05."""


class SQLAlchemyReportePostulacionRepository(ReportePostulacionRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def porestudiante(self) -> list[tuple[Any, ...]]:
        return self.rows("select * from v01")

    def promediosbeca(self) -> list[tuple[Any, ...]]:
        return self.rows("select * from v05")

    def rows(self, sql: str) -> list[tuple[Any, ...]]:
        # Se leen por posición: los alias de las vistas llevan espacios y puntos.
        return [tuple(row) for row in self.session.execute(text(sql))]
