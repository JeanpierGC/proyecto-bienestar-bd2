from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


class ReporteBecaRepository(ABC):
    """Consultas de reporte que ya resuelve la base de datos (vistas y procedimientos)."""

    @abstractmethod
    def otorgadasconv(self) -> list[tuple[Any, ...]]:
        """(convocatoria, beca, cantidad). Viene de la vista v02."""

    @abstractmethod
    def cuposconv(self) -> list[tuple[Any, ...]]:
        """(convocatoria, cupos, postulaciones, aprobadas). Viene de la vista v06."""

    @abstractmethod
    def rankingbecas(self, anio: int) -> list[tuple[Any, ...]]:
        """(beca, postulaciones, año). Viene del procedimiento p07."""


class SQLAlchemyReporteBecaRepository(ReporteBecaRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def otorgadasconv(self) -> list[tuple[Any, ...]]:
        return self.rows("select * from v02")

    def cuposconv(self) -> list[tuple[Any, ...]]:
        return self.rows("select * from v06")

    def rankingbecas(self, anio: int) -> list[tuple[Any, ...]]:
        return self.rows("call p07(:anio)", {"anio": anio})

    def rows(self, sql: str, params: dict[str, Any] | None = None) -> list[tuple[Any, ...]]:
        # Se leen por posición: los alias de las vistas llevan espacios y puntos.
        return [tuple(row) for row in self.session.execute(text(sql), params or {})]
