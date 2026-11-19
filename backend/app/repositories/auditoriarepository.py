from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


class AuditoriaRepository(ABC):
    """Solo lectura: las tablas de control las llenan únicamente los triggers."""

    @abstractmethod
    def postulaciones(self) -> list[tuple[Any, ...]]:
        """(idctrl, fecha, acción, código, estado, promedio, estudiante, convocatoria)."""

    @abstractmethod
    def otorgamientos(self) -> list[tuple[Any, ...]]:
        """(idctrl, fecha, acción, código, estado, inicio, fin, postulación)."""

    @abstractmethod
    def citas(self) -> list[tuple[Any, ...]]:
        """(idctrl, fecha, acción, código, fecha cita, hora, estado, estudiante, profesional)."""


class SQLAlchemyAuditoriaRepository(AuditoriaRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def postulaciones(self) -> list[tuple[Any, ...]]:
        return self.rows(
            "select idctrl, fechacc, tipoacc, codpostc, estpostc, prompostc, codestc, codconvc "
            "from ctrl_postu order by idctrl desc"
        )

    def otorgamientos(self) -> list[tuple[Any, ...]]:
        return self.rows(
            "select idctrl, fechacc, tipoacc, codotorc, estotorc, fechiniotorc, fechfinotorc, codpostc "
            "from ctrl_otor order by idctrl desc"
        )

    def citas(self) -> list[tuple[Any, ...]]:
        return self.rows(
            "select idctrl, fechacc, tipoacc, codcitac, fechcitac, horacitac, estcitac, codestc, codperc "
            "from ctrl_cita order by idctrl desc"
        )

    def rows(self, sql: str) -> list[tuple[Any, ...]]:
        return [tuple(row) for row in self.session.execute(text(sql))]
