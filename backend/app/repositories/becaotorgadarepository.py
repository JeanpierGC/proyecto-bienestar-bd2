from abc import abstractmethod
from datetime import date
from decimal import Decimal

from sqlalchemy import func, select

from app.models.becaotorgada import BecaOtorgada, SeguimientoBeca
from app.repositories.base import BaseRepository, SQLAlchemyRepository
from app.repositories.procedimientos import llamarmensaje


class BecaOtorgadaRepository(BaseRepository[BecaOtorgada]):
    @abstractmethod
    def findbypostulacion(self, codpost: int) -> BecaOtorgada | None: ...

    @abstractmethod
    def otorgar(self, codpost: int, fechiniotor: date, fechfinotor: date) -> str:
        """Otorga con el procedimiento p03. Devuelve su mensaje."""

    @abstractmethod
    def promedioseguimiento(self, codotor: int) -> Decimal | None:
        """Promedio de sus seguimientos según la función f2."""


class SQLAlchemyBecaOtorgadaRepository(SQLAlchemyRepository[BecaOtorgada], BecaOtorgadaRepository):
    model = BecaOtorgada

    def findbypostulacion(self, codpost: int) -> BecaOtorgada | None:
        return self.first(select(BecaOtorgada).where(BecaOtorgada.codpost == codpost))

    def otorgar(self, codpost: int, fechiniotor: date, fechfinotor: date) -> str:
        return llamarmensaje(
            self.session,
            "call p03(:codpost, :inicio, :fin)",
            {"codpost": codpost, "inicio": fechiniotor, "fin": fechfinotor},
        )

    def promedioseguimiento(self, codotor: int) -> Decimal | None:
        return self.session.scalar(select(func.f2(codotor)))

    def ordering(self):
        return (BecaOtorgada.fechotor.desc(), BecaOtorgada.codotor.desc())


class SeguimientoBecaRepository(BaseRepository[SeguimientoBeca]):
    @abstractmethod
    def listbyotorgada(self, codotor: int) -> list[SeguimientoBeca]: ...


class SQLAlchemySeguimientoBecaRepository(
    SQLAlchemyRepository[SeguimientoBeca], SeguimientoBecaRepository
):
    model = SeguimientoBeca

    def listbyotorgada(self, codotor: int) -> list[SeguimientoBeca]:
        return self.list(select(SeguimientoBeca).where(SeguimientoBeca.codotor == codotor))

    def ordering(self):
        return (SeguimientoBeca.fechsegb.desc(), SeguimientoBeca.codsegb.desc())
