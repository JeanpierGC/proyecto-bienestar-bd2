from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


class ReporteBienestarRepository(ABC):
    """Reportes de bienestar que ya resuelven las vistas de la base de datos."""

    @abstractmethod
    def citasprofesional(self) -> list[tuple[Any, ...]]:
        """(profesional, servicio, citas). Viene de la vista v03."""

    @abstractmethod
    def casosriesgo(self) -> list[tuple[Any, ...]]:
        """(estudiante, fecha de cita, nivel, estado, próxima fecha). Viene de la vista v04."""


class SQLAlchemyReporteBienestarRepository(ReporteBienestarRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def citasprofesional(self) -> list[tuple[Any, ...]]:
        return self.rows("select * from v03")

    def casosriesgo(self) -> list[tuple[Any, ...]]:
        return self.rows("select * from v04")

    def rows(self, sql: str) -> list[tuple[Any, ...]]:
        # Se leen por posición: los alias de las vistas llevan espacios.
        return [tuple(row) for row in self.session.execute(text(sql))]
