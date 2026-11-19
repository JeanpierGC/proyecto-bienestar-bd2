from abc import abstractmethod
from datetime import date, time

from sqlalchemy import select

from app.models.cita import Cita
from app.repositories.base import BaseRepository, SQLAlchemyRepository
from app.repositories.procedimientos import llamarmensaje


class CitaRepository(BaseRepository[Cita]):
    @abstractmethod
    def listfiltered(
        self, codest: int | None, codper: int | None, estcita: str | None
    ) -> list[Cita]: ...

    @abstractmethod
    def findbyhorario(self, codper: int, fechcita: date, horacita: time) -> Cita | None: ...

    @abstractmethod
    def registrar(
        self, codest: int, codper: int, fechcita: date, horacita: time, modcita: str, motcita: str | None
    ) -> str:
        """Registra con el procedimiento p04. Devuelve su mensaje."""


class SQLAlchemyCitaRepository(SQLAlchemyRepository[Cita], CitaRepository):
    model = Cita

    def listfiltered(
        self, codest: int | None, codper: int | None, estcita: str | None
    ) -> list[Cita]:
        query = select(Cita)
        if codest is not None:
            query = query.where(Cita.codest == codest)
        if codper is not None:
            query = query.where(Cita.codper == codper)
        if estcita is not None:
            query = query.where(Cita.estcita == estcita)
        return self.list(query)

    def findbyhorario(self, codper: int, fechcita: date, horacita: time) -> Cita | None:
        return self.first(
            select(Cita).where(
                Cita.codper == codper, Cita.fechcita == fechcita, Cita.horacita == horacita
            )
        )

    def registrar(
        self, codest: int, codper: int, fechcita: date, horacita: time, modcita: str, motcita: str | None
    ) -> str:
        return llamarmensaje(
            self.session,
            "call p04(:codest, :codper, :fecha, :hora, :modalidad, :motivo)",
            {
                "codest": codest, "codper": codper, "fecha": fechcita, "hora": horacita,
                "modalidad": modcita, "motivo": motcita,
            },
        )

    def ordering(self):
        return (Cita.fechcita.desc(), Cita.horacita.desc())
